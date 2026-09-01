"""Comprehensive coherence audit of the live FTB Quests tree.

Parses every chapter under config/ftbquests/quests/chapters/, builds the global
dependency graph, and reports structural, progression, task-authentication,
reward, and layout incoherences.

Outputs:
  docs/quest-tree-coherence-audit.json   full machine-readable inventory + findings
  stdout                                 finding summary grouped by severity

Deterministic: no network, no randomness, stable ordering.
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER_DIR = ROOT / "config/ftbquests/quests/chapters"
LANG = ROOT / "config/ftbquests/quests/lang/en_us.snbt"
CHAPTER_GROUPS = ROOT / "config/ftbquests/quests/chapter_groups.snbt"
DATA_SNBT = ROOT / "config/ftbquests/quests/data.snbt"
REGISTRY_ITEMS = ROOT / "docs/registry-inventory/item-ids.txt"
REGISTRY_ENTITIES = ROOT / "docs/registry-inventory/entity-ids.txt"
MOD_JAR_INDEX = ROOT / "docs/registry-inventory/mod-jar-index.json"
GRAPH_NODES = ROOT / "docs/progression-graph/graph-nodes.csv"
RECIPE_OUTPUTS = ROOT / "docs/recipe-index/recipe-outputs.csv"
KUBEJS_STARTUP = ROOT / "kubejs/startup_scripts"
KUBEJS_DIR = ROOT / "kubejs"
REWARD_BAG_SCRIPT = ROOT / "kubejs/server_scripts/era_reward_bags.js"
REWARD_BAG_REGISTRATION = ROOT / "kubejs/startup_scripts/main.js"

OUT_JSON = ROOT / "docs/quest-tree-coherence-audit.json"


# --------------------------------------------------------------------------- #
# Minimal SNBT parser (FTB Quests dialect)
# --------------------------------------------------------------------------- #
class SNBTParser:
    def __init__(self, text: str):
        self.s = text
        self.i = 0
        self.n = len(text)

    def error(self, msg: str):
        line = self.s.count("\n", 0, self.i) + 1
        raise ValueError(f"SNBT parse error at line {line}: {msg}")

    def skip_ws(self):
        while self.i < self.n:
            c = self.s[self.i]
            if c in " \t\r\n,":
                self.i += 1
            elif c == "#" or (c == "/" and self.i + 1 < self.n and self.s[self.i + 1] == "/"):
                while self.i < self.n and self.s[self.i] != "\n":
                    self.i += 1
            else:
                break

    def parse(self):
        self.skip_ws()
        value = self.parse_value()
        self.skip_ws()
        return value

    def parse_value(self):
        self.skip_ws()
        if self.i >= self.n:
            self.error("unexpected end of input")
        c = self.s[self.i]
        if c == "{":
            return self.parse_object()
        if c == "[":
            return self.parse_array()
        if c in ('"', "'"):
            return self.parse_string()
        return self.parse_token()

    def parse_object(self):
        obj = {}
        self.i += 1  # {
        while True:
            self.skip_ws()
            if self.i >= self.n:
                self.error("unterminated object")
            if self.s[self.i] == "}":
                self.i += 1
                return obj
            key = self.parse_string() if self.s[self.i] in ('"', "'") else self.parse_bare_key()
            self.skip_ws()
            if self.i < self.n and self.s[self.i] == ":":
                self.i += 1
            obj[key] = self.parse_value()

    def parse_array(self):
        arr = []
        self.i += 1  # [
        # typed-array prefix like [I; or [L;
        self.skip_ws()
        if self.i + 1 < self.n and self.s[self.i] in "ILBil" and self.s[self.i + 1] == ";":
            self.i += 2
        while True:
            self.skip_ws()
            if self.i >= self.n:
                self.error("unterminated array")
            if self.s[self.i] == "]":
                self.i += 1
                return arr
            arr.append(self.parse_value())

    def parse_bare_key(self):
        start = self.i
        while self.i < self.n and (self.s[self.i].isalnum() or self.s[self.i] in "_.-+"):
            self.i += 1
        if self.i == start:
            self.error("empty key")
        return self.s[start:self.i]

    def parse_string(self):
        quote = self.s[self.i]
        self.i += 1
        out = []
        while self.i < self.n:
            c = self.s[self.i]
            if c == "\\":
                nxt = self.s[self.i + 1] if self.i + 1 < self.n else ""
                out.append({"n": "\n", "t": "\t", "r": "\r"}.get(nxt, nxt))
                self.i += 2
                continue
            if c == quote:
                self.i += 1
                return "".join(out)
            out.append(c)
            self.i += 1
        self.error("unterminated string")

    def parse_token(self):
        start = self.i
        while self.i < self.n and self.s[self.i] not in " \t\r\n,{}[]:\"'":
            self.i += 1
        tok = self.s[start:self.i]
        low = tok.lower()
        if low == "true":
            return True
        if low == "false":
            return False
        m = re.fullmatch(r"(-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)[dDfFbBsSlL]?", tok)
        if m:
            num = m.group(1)
            return float(num) if ("." in num or "e" in num or "E" in num) else int(num)
        return tok


def parse_snbt(text: str):
    return SNBTParser(text.lstrip("﻿")).parse()


# --------------------------------------------------------------------------- #
# Loading
# --------------------------------------------------------------------------- #
def load_lang() -> dict:
    text = LANG.read_text(encoding="utf-8-sig")
    out = {}
    for m in re.finditer(r'^\t([\w.\-]+):\s*"(.*)"\s*$', text, re.M):
        out[m.group(1)] = m.group(2)
    return out


def load_registry(path: Path) -> set:
    if not path.exists():
        return set()
    ids = set()
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # files may be "namespace:path" or "namespace:path\tcount" etc.
        ids.add(line.split()[0].split(",")[0])
    return ids


def load_csv_col(path: Path, col: str, where=None) -> set:
    import csv
    if not path.exists():
        return set()
    out = set()
    with path.open(encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            if where and not where(row):
                continue
            v = row.get(col)
            if v:
                out.add(v.strip())
    return out


def load_mod_namespaces() -> set:
    if not MOD_JAR_INDEX.exists():
        return set()
    data = json.loads(MOD_JAR_INDEX.read_text(encoding="utf-8"))
    ns = set()
    for entry in data:
        for mid in entry.get("modids", []):
            ns.add(mid)
    return ns


def load_graph_item_nodes() -> set:
    import csv
    if not GRAPH_NODES.exists():
        return set()
    out = set()
    with GRAPH_NODES.open(encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            if row.get("node_kind") in ("item", "item+block", "block", "external_resource"):
                out.add(row["id"].strip())
    return out


def load_dynamic_sourced_items() -> set:
    """Item ids referenced by runtime recipe scripts and their JSON config files.
    The static recipe index cannot see these, so they suppress false 'no recipe'
    findings while still letting genuinely loot-only gating surface.

    KubeJS recipe scripts frequently pass bare item names to helper functions
    (`I('reinforced_frame')` -> `kubejs:reinforced_frame`), so bare lowercase
    tokens inside script files are also treated as candidate project items.
    """
    out = set()
    # namespace:path references anywhere in scripts/config = "seen"
    for sub in ("server_scripts", "startup_scripts", "config"):
        base = KUBEJS_DIR / sub
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.suffix not in (".js", ".json") or not path.is_file():
                continue
            txt = path.read_text(encoding="utf-8", errors="ignore")
            for m in re.finditer(r"([a-z0-9_]+:[a-z0-9_/.]+)", txt):
                out.add(m.group(1))
    # bare item names passed to recipe helpers live ONLY in server_scripts
    # (startup_scripts bare names are item *registration*, not a craft source)
    base = KUBEJS_DIR / "server_scripts"
    if base.exists():
        for path in base.glob("*.js"):
            txt = path.read_text(encoding="utf-8", errors="ignore")
            for m in re.finditer(r"[`'\"]([a-z][a-z0-9_]{2,})[`'\"]", txt):
                out.add(f"kubejs:{m.group(1)}")
    return out


def load_loot_sources() -> dict:
    """item id -> {'guaranteed': bool, 'tables': [rel paths]}.
    'guaranteed' means the item sits in a pool that always yields it
    (single item entry, rolls >= 1, no chance/quality conditions)."""
    out: dict[str, dict] = {}

    def note(item, guaranteed, path):
        rec = out.setdefault(item, {"guaranteed": False, "tables": []})
        rec["guaranteed"] = rec["guaranteed"] or guaranteed
        p = str(path.relative_to(ROOT))
        if p not in rec["tables"]:
            rec["tables"].append(p)

    def walk_pool(pool, path):
        entries = pool.get("entries", []) if isinstance(pool, dict) else []
        item_entries = [e for e in entries if isinstance(e, dict) and e.get("type", "").endswith("item")]
        conds = pool.get("conditions") or []
        chance_cond = any(isinstance(c, dict) and "chance" in c.get("condition", "") for c in conds)
        rolls = pool.get("rolls", 1)
        rolls_min = rolls.get("min", 1) if isinstance(rolls, dict) else rolls
        for e in item_entries:
            name = e.get("name")
            if not name:
                continue
            e_conds = e.get("conditions") or []
            e_chance = any(isinstance(c, dict) and "chance" in c.get("condition", "") for c in e_conds)
            guaranteed = (len(item_entries) == 1 and not chance_cond and not e_chance
                          and isinstance(rolls_min, (int, float)) and rolls_min >= 1
                          and "weight" not in e)
            note(name, guaranteed, path)

    for base in (KUBEJS_DIR / "data", ROOT / "data", ROOT / "datapacks"):
        if not base.exists():
            continue
        for path in base.rglob("*.json"):
            if "loot_table" not in path.parts and "loot_tables" not in path.parts:
                continue
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError, UnicodeDecodeError):
                continue
            for pool in (data.get("pools", []) if isinstance(data, dict) else []):
                walk_pool(pool, path)
    return out


def load_kubejs_created_items() -> set:
    """Literal event.create('name') declarations across kubejs startup scripts,
    plus every kubejs:/infinite_domain*: id referenced anywhere under kubejs/."""
    created = set()
    if KUBEJS_STARTUP.exists():
        for path in KUBEJS_STARTUP.glob("*.js"):
            txt = path.read_text(encoding="utf-8", errors="ignore")
            for m in re.finditer(r"event\.create\(\s*'([a-z0-9_/]+)'", txt):
                created.add(f"kubejs:{m.group(1)}")
            for m in re.finditer(r"event\.create\(\s*`([a-z0-9_/]+)`", txt):
                created.add(f"kubejs:{m.group(1)}")
    if KUBEJS_DIR.exists():
        for path in KUBEJS_DIR.rglob("*"):
            if path.suffix not in (".js", ".json") or not path.is_file():
                continue
            txt = path.read_text(encoding="utf-8", errors="ignore")
            for m in re.finditer(r"\b((?:kubejs|infinite_domain|infinite_domain_space):[a-z0-9_/.]+)", txt):
                created.add(m.group(1))
    return created


# --------------------------------------------------------------------------- #
# Chapter / quest model
# --------------------------------------------------------------------------- #
ERA_CHAPTERS = {
    "lets_get_started_shall_we": 0,
    "era_01_mechanical_reconstruction": 1,
    "era_02_heavy_industry": 2,
    "era_03_petrochemical_civilization": 3,
    "era_04_the_electrical_grid": 4,
    "era_05_automated_industry": 5,
    "era_06_high_energy_and_nuclear_engineering": 6,
    "era_07_orbital_industry": 7,
    "era_08_infinite_domain": 8,
}
SHAPE_BRANCH = {
    "hexagon": "mining",
    "heart": "farming",
    "diamond": "exploration",
    "gear": "ancillary",
    "octagon": "gate",
}
# id first digit in generated era chapters -> expected branch
GEN_PREFIX_BRANCH = {"1": "mining", "2": "farming", "3": "exploration", "4": "ancillary", "7": "ancillary", "5": "gate"}


def iter_quest_blocks(chapter: dict, file: str):
    quests = chapter.get("quests", [])
    for q in quests:
        yield q


def main() -> None:
    lang = load_lang()
    reg_items = load_registry(REGISTRY_ITEMS)
    reg_entities = load_registry(REGISTRY_ENTITIES)
    mod_ns = load_mod_namespaces()
    graph_items = load_graph_item_nodes()
    kubejs_items = load_kubejs_created_items()
    producible = load_csv_col(RECIPE_OUTPUTS, "output_id",
                              where=lambda r: str(r.get("enabled", "")).lower() == "true")
    dynamic_sourced = load_dynamic_sourced_items()
    loot_sources = load_loot_sources()
    loot_items = set(loot_sources)
    # produced = craftable by an enabled JSON recipe OR by a runtime recipe script
    produced = producible | dynamic_sourced
    # union oracle: does this item id exist in the pack at all?
    known_items = reg_items | graph_items | kubejs_items | producible | dynamic_sourced | loot_items
    PROJECT_NS = {"kubejs", "infinite_domain", "infinite_domain_space"}
    RAW_OK_RE = re.compile(r":(raw_|.*_ore$|.*_log$|deepslate|cobblestone|dirt|sand|gravel|"
                           r"stone$|netherrack|end_stone|clay|.*_sapling$)")

    group_text = CHAPTER_GROUPS.read_text(encoding="utf-8")
    registered_groups = set(re.findall(r'id:\s*"([0-9A-Fa-f]{16})"', group_text))
    data_cfg = parse_snbt(DATA_SNBT.read_text(encoding="utf-8"))

    bag_script = REWARD_BAG_SCRIPT.read_text(encoding="utf-8") if REWARD_BAG_SCRIPT.exists() else ""
    bag_reg = REWARD_BAG_REGISTRATION.read_text(encoding="utf-8") if REWARD_BAG_REGISTRATION.exists() else ""
    defined_bags = set(re.findall(r"'(kubejs:era\d+_(?:supply_bag|priority_cache))'", bag_script))
    registered_bags = {f"kubejs:{m}" for m in re.findall(r"\['(era\d+_(?:supply_bag|priority_cache))'", bag_reg)}

    quests: dict[str, dict] = {}
    quest_order: list[str] = []
    chapters: list[dict] = []
    obj_ids: dict[str, str] = {}
    dup_obj_ids: list = []
    dup_quest_ids: list = []

    for path in sorted(CHAPTER_DIR.glob("*.snbt")):
        raw = path.read_text(encoding="utf-8").replace("\r\n", "\n")
        chapter = parse_snbt(raw)
        fname = path.stem
        cid = chapter.get("id")
        gid = chapter.get("group")
        chapters.append({
            "file": fname,
            "id": cid,
            "group": gid,
            "order_index": chapter.get("order_index"),
            "icon": chapter.get("icon"),
            "quest_count": len(chapter.get("quests", [])),
            "era": ERA_CHAPTERS.get(fname),
        })
        for q in chapter.get("quests", []):
            qid = q.get("id")
            if not qid:
                continue
            if qid in quests:
                dup_quest_ids.append((qid, quests[qid]["file"], fname))
            deps = q.get("dependencies", []) or []
            tasks = q.get("tasks", []) or []
            rewards = q.get("rewards", []) or []
            for coll in (tasks, rewards):
                for obj in coll:
                    oid = obj.get("id")
                    if not oid:
                        continue
                    if oid in obj_ids:
                        dup_obj_ids.append((oid, obj_ids[oid], fname))
                    else:
                        obj_ids[oid] = fname
            rec = {
                "id": qid,
                "file": fname,
                "chapter_id": cid,
                "group": gid,
                "era": ERA_CHAPTERS.get(fname),
                "x": q.get("x"),
                "y": q.get("y"),
                "shape": q.get("shape", chapter.get("default_quest_shape", "circle")),
                "size": q.get("size"),
                "optional": bool(q.get("optional", False)),
                "hide": bool(q.get("hide", False)),
                "dependencies": [d for d in deps if isinstance(d, str)],
                "dependency_requirement": q.get("dependency_requirement"),
                "min_required_dependencies": q.get("min_required_dependencies"),
                "tasks": tasks,
                "rewards": rewards,
                "title": lang.get(f"quest.{qid}.title"),
                "subtitle": lang.get(f"quest.{qid}.subtitle"),
                "description": q.get("description"),
            }
            quests[qid] = rec
            quest_order.append(qid)

    for q in quests.values():
        q["dependents"] = []
    for q in quests.values():
        for d in q["dependencies"]:
            if d in quests:
                quests[d]["dependents"].append(q["id"])

    findings: list[dict] = []

    def add(severity: str, category: str, message: str, **extra):
        findings.append({"severity": severity, "category": category, "message": message, **extra})

    # ---- ID / graph integrity ------------------------------------------- #
    for qid, a, b in dup_quest_ids:
        add("critical", "duplicate-id", f"Quest id {qid} defined in both {a} and {b}", quest=qid)
    for oid, a, b in dup_obj_ids:
        add("critical", "duplicate-id", f"Task/reward object id {oid} reused ({a} / {b})", object_id=oid)

    for q in quests.values():
        for d in q["dependencies"]:
            if d == q["id"]:
                add("critical", "self-dependency", f"{q['id']} ({q['file']}) depends on itself", quest=q["id"])
            elif d not in quests:
                add("critical", "unresolved-dependency",
                    f"{q['id']} ({q['file']}) depends on missing quest {d}", quest=q["id"], missing=d)

    # cycle detection (full graph)
    WHITE, GREY, BLACK = 0, 1, 2
    color = defaultdict(int)
    cycles: list[list[str]] = []

    def dfs(node, stack):
        color[node] = GREY
        stack.append(node)
        for nb in quests.get(node, {}).get("dependencies", []):
            if nb not in quests:
                continue
            if color[nb] == GREY:
                idx = stack.index(nb)
                cycles.append(stack[idx:] + [nb])
            elif color[nb] == WHITE:
                dfs(nb, stack)
        stack.pop()
        color[node] = BLACK

    import sys
    sys.setrecursionlimit(10000)
    for qid in quest_order:
        if color[qid] == WHITE:
            dfs(qid, [])
    for cyc in cycles:
        add("critical", "dependency-cycle", "Dependency cycle: " + " -> ".join(cyc))

    # ---- roots / orphans ---------------------------------------------- #
    by_chapter: dict[str, list[dict]] = defaultdict(list)
    for q in quests.values():
        by_chapter[q["file"]].append(q)

    for fname, qs in sorted(by_chapter.items()):
        roots = [q for q in qs if not q["dependencies"]]
        external_roots = [q for q in qs
                          if q["dependencies"] and all(d not in quests or quests[d]["file"] != fname
                                                       for d in q["dependencies"])]
        entry_points = roots + external_roots
        if len(roots) > 1:
            add("warning", "multi-root-chapter",
                f"{fname}: {len(roots)} quests have no dependencies at all "
                f"({', '.join(sorted(r['id'] for r in roots))})", file=fname)
        for q in qs:
            if not q["dependencies"] and not q["dependents"]:
                add("warning", "orphan-quest",
                    f"{fname}: {q['id']} '{q['title'] or '?'}' is isolated (no deps, no dependents)",
                    quest=q["id"])

    # ---- era chain linkage ------------------------------------------- #
    era_files = {v: k for k, v in ERA_CHAPTERS.items()}
    era_orientation: dict[int, dict] = {}
    era_capstone: dict[int, dict] = {}
    for era, fname in era_files.items():
        qs = by_chapter.get(fname, [])
        # orientation = octagon at y==0 with fewest deps / lowest y
        octs = [q for q in qs if q["shape"] == "octagon"]
        orient = min(qs, key=lambda q: (q["y"] if isinstance(q["y"], (int, float)) else 0, len(q["dependencies"])),
                     default=None)
        for q in qs:
            if q["y"] in (0, 0.0):
                orient = q
                break
        era_orientation[era] = orient
        caps = [q for q in qs if q["dependency_requirement"] == "one_completed"]
        # capstone = the one_completed octagon whose task is a *_core / furnace
        cap = None
        for q in caps:
            tids = " ".join(t.get("item", {}).get("id", "") if isinstance(t.get("item"), dict) else ""
                            for t in q["tasks"])
            if "core" in tids or "furnace" in tids:
                cap = q
        cap = cap or (caps[-1] if caps else None)
        era_capstone[era] = cap

    for era in range(1, 9):
        orient = era_orientation.get(era)
        prev_cap = era_capstone.get(era - 1)
        if not orient or not prev_cap:
            continue
        # is prev capstone an ancestor of this era's orientation?
        seen = set()
        stack = list(orient["dependencies"])
        reached = False
        while stack:
            cur = stack.pop()
            if cur in seen:
                continue
            seen.add(cur)
            if cur == prev_cap["id"]:
                reached = True
                break
            stack.extend(quests.get(cur, {}).get("dependencies", []))
        if not reached:
            add("critical", "broken-era-chain",
                f"Era {era} ({era_files[era]}) orientation {orient['id']} does not depend "
                f"(transitively) on the Era {era-1} capstone {prev_cap['id']}. "
                f"Era {era} is reachable without finishing Era {era-1}.",
                era=era)

    # ---- checkmark audit -------------------------------------------- #
    STARTER_CHECKMARK_ALLOW = {
        "7D194089522507AB", "6F01000000000001", "6002100000000001", "6002100000000002",
        "6F01000000000010", "6F01000000000011", "6F01000000000012", "6F01000000000013",
        "6F01000000000014",
        # Domain Compendium capstone - earned behind 305 collection quests.
        "7C0DE0C0000000FF",
    }
    PROLOGUE_FILES = {"another_lost_soul", "lets_get_started_shall_we", "spawn_exchange"}
    # An optional, exhaustive completion catalogue (docs/DOMAIN_COMPENDIUM_CHAPTER.md).
    # It gates nothing real; its root/capstone checkmarks and capstone emblem are by design.
    CATALOGUE_FILES = {"domain_compendium"}
    checkmark_rows = []
    for q in quests.values():
        types = [t.get("type") for t in q["tasks"]]
        if not types or any(t != "checkmark" for t in types):
            continue
        material_reward = [r for r in q["rewards"] if r.get("type") in ("item", "loot", "random", "choice")]
        row = {
            "quest": q["id"], "file": q["file"], "era": q["era"],
            "title": q["title"], "shape": q["shape"], "optional": q["optional"],
            "reward_types": sorted({r.get("type") for r in q["rewards"]}),
            "has_material_reward": bool(material_reward),
            "dependents": len(q["dependents"]),
        }
        checkmark_rows.append(row)
        if row["has_material_reward"] and q["id"] not in STARTER_CHECKMARK_ALLOW \
                and q["file"] not in CATALOGUE_FILES:
            add("critical", "rewarded-checkmark",
                f"{q['file']}: checkmark quest {q['id']} '{q['title']}' grants a material reward "
                f"({', '.join(r.get('item', {}).get('id', r.get('type', '?')) if isinstance(r.get('item'), dict) else r.get('type','?') for r in q['rewards'])})",
                quest=q["id"])
        if q["file"] not in PROLOGUE_FILES:
            era = q["era"]
            # an octagon at (or above) the chapter's top that other quests hang
            # off is a chapter-orientation node — an acceptable use of a checkmark
            chapter_min_y = min((c["y"] for c in by_chapter[q["file"]]
                                 if isinstance(c["y"], (int, float))), default=0)
            is_orientation = (q["shape"] == "octagon"
                              and isinstance(q["y"], (int, float)) and q["y"] <= chapter_min_y
                              and len(q["dependents"]) >= 1)
            is_mastery_warning = q["file"].startswith("mastery_era_") or q["file"] in CATALOGUE_FILES
            if is_orientation:
                sev, note = "info", "chapter orientation gate"
            elif is_mastery_warning:
                sev, note = "info", "mastery warning node"
            else:
                sev, note = "warning", "self-certified checkmark outside prologue"
            add(sev, "checkmark-outside-prologue",
                f"{q['file']}: {q['id']} '{q['title']}' ({note}; shape={q['shape']}, "
                f"optional={q['optional']}, dependents={len(q['dependents'])})",
                quest=q["id"], note=note)

    # ---- task authentication quality ------------------------------- #
    OP_VERB = re.compile(
        r"\b(operate|run|assemble|commission|demonstrate|pass|test|synchron|maintain|"
        r"start|scram|restore|deploy|install|build|launch|survive|witness)\w*\b", re.I)
    for q in quests.values():
        for t in q["tasks"]:
            tt = t.get("type")
            if tt == "item":
                it = t.get("item")
                iid = it.get("id") if isinstance(it, dict) else None
                if not iid and isinstance(it, dict):
                    continue
                if iid in ("ftbquests:missing_item", "minecraft:air"):
                    intended = None
                    comp = it.get("components") if isinstance(it, dict) else None
                    if isinstance(comp, dict):
                        intended = comp.get("ftbquests:missing_item")
                    add("critical", "missing-item-placeholder",
                        f"{q['file']}: {q['id']} '{q['title']}' task item is unresolved "
                        f"({iid}" + (f", intended '{intended}'" if intended else "")
                        + f") — this quest is uncompletable",
                        quest=q["id"], item=iid, intended=intended)
                    continue
                if iid and iid not in known_items:
                    ns = iid.split(":", 1)[0]
                    if ns not in mod_ns and ns not in PROJECT_NS:
                        add("critical", "unknown-namespace-item",
                            f"{q['file']}: {q['id']} item task references {iid} — namespace '{ns}' "
                            f"is not an installed mod", quest=q["id"], item=iid)
                    elif ns in PROJECT_NS:
                        add("info", "project-item-unverified",
                            f"{q['file']}: {q['id']} task item {iid} not found in static registries "
                            f"(runtime-registered project item; verify it exists)", quest=q["id"], item=iid)
                    else:
                        add("warning", "unresolved-item-task",
                            f"{q['file']}: {q['id']} item task references unknown item {iid}",
                            quest=q["id"], item=iid)
            elif tt == "kill":
                ent = t.get("entity")
                if not ent:
                    add("warning", "malformed-task", f"{q['file']}: {q['id']} kill task missing entity", quest=q["id"])
                elif reg_entities and ent not in reg_entities:
                    add("info", "unresolved-entity-task",
                        f"{q['file']}: {q['id']} kill task references unknown entity {ent}", quest=q["id"], entity=ent)
            elif tt in ("structure", "biome", "dimension"):
                if not t.get(tt):
                    add("warning", "malformed-task",
                        f"{q['file']}: {q['id']} {tt} task missing '{tt}' field", quest=q["id"])
        # weak-authentication heuristic
        title = q["title"] or ""
        only_check = q["tasks"] and all(t.get("type") == "checkmark" for t in q["tasks"])
        single_possess = len(q["tasks"]) == 1 and q["tasks"][0].get("type") == "item" \
            and (q["tasks"][0].get("count", 1) in (1, None))
        if OP_VERB.search(title) and (only_check or single_possess) and q["file"] not in PROLOGUE_FILES:
            add("info", "weak-authentication",
                f"{q['file']}: {q['id']} '{title}' implies an operation but is proven by "
                f"{'a checkmark' if only_check else 'single-item possession'}",
                quest=q["id"])

    # ---- reward consistency --------------------------------------- #
    reward_id_seen: dict[str, str] = {}
    for q in quests.values():
        for r in q["rewards"]:
            rid = r.get("id")
            if rid:
                if rid in reward_id_seen:
                    add("warning", "duplicate-reward-id",
                        f"reward id {rid} reused ({reward_id_seen[rid]} / {q['id']})", quest=q["id"])
                else:
                    reward_id_seen[rid] = q["id"]
            if r.get("type") == "random":
                add("warning", "random-wheel-reward",
                    f"{q['file']}: {q['id']} uses a 'random' (spin-wheel) reward instead of a loot bag item",
                    quest=q["id"])
            if r.get("type") == "item":
                it = r.get("item")
                iid = it.get("id") if isinstance(it, dict) else None
                cnt = r.get("count") or (it.get("count") if isinstance(it, dict) else 1) or 1
                if iid and iid not in known_items:
                    ns = iid.split(":", 1)[0]
                    if ns not in mod_ns and ns not in PROJECT_NS:
                        add("critical", "unknown-namespace-item",
                            f"{q['file']}: {q['id']} reward references {iid} — namespace '{ns}' is not an installed mod",
                            quest=q["id"], item=iid)
                    elif ns not in PROJECT_NS:
                        add("warning", "unresolved-reward-item",
                            f"{q['file']}: {q['id']} reward references unknown item {iid}", quest=q["id"], item=iid)
                if iid and iid.startswith("kubejs:era") and ("supply_bag" in iid or "priority_cache" in iid):
                    if iid not in defined_bags:
                        add("critical", "reward-bag-undefined",
                            f"{q['file']}: {q['id']} rewards {iid} but that bag has no loot table in era_reward_bags.js",
                            quest=q["id"], item=iid)
                    if iid not in registered_bags:
                        add("warning", "reward-bag-unregistered",
                            f"{q['file']}: {q['id']} rewards {iid} but that item is not registered in startup_scripts/main.js",
                            quest=q["id"], item=iid)
                if isinstance(cnt, (int, float)) and cnt > 64:
                    add("info", "large-reward-stack",
                        f"{q['file']}: {q['id']} reward {iid} count {cnt}", quest=q["id"])

    # era reward-bag coverage
    era_bag_quests = defaultdict(list)
    for q in quests.values():
        if q["era"] is None or q["era"] < 1:
            continue
        for r in q["rewards"]:
            it = r.get("item") if isinstance(r.get("item"), dict) else None
            iid = it.get("id") if it else None
            if iid and re.match(r"kubejs:era\d+_(supply_bag|priority_cache)", iid):
                era_bag_quests[q["era"]].append((q["id"], iid))
    for era in range(1, 9):
        if not era_bag_quests.get(era):
            add("warning", "reward-bag-missing-in-era",
                f"Era {era} has no quest that rewards an era supply bag / priority cache "
                f"(assign_era_reward_bags.py output not present in live file)", era=era)

    # ---- recipe / acquisition provability ------------------------ #
    # produced = enabled JSON recipe OR runtime-script/config recipe.
    # A progression-gating task item that is only obtainable from a loot table is
    # the real "advancement depends on random loot" hazard.
    for q in quests.values():
        gating = bool(q["dependents"]) and not q["optional"]
        for t in q["tasks"]:
            if t.get("type") != "item":
                continue
            it = t.get("item")
            iid = it.get("id") if isinstance(it, dict) else None
            if not iid or iid in produced or iid == "ftbquests:missing_item":
                continue
            loot = loot_sources.get(iid)
            iid_ns = iid.split(":", 1)[0]
            third_party = iid_ns in mod_ns and iid_ns not in PROJECT_NS
            if gating and loot and not loot["guaranteed"] and not third_party:
                add("critical", "gate-item-random-loot",
                    f"{q['file']}: {q['id']} '{q['title']}' gates {len(q['dependents'])} quest(s) on "
                    f"{iid}, obtainable only as a WEIGHTED/chance loot roll ({'; '.join(loot['tables'][:3])})",
                    quest=q["id"], item=iid)
            elif gating and loot and not loot["guaranteed"] and third_party:
                add("warning", "third-party-loot-gate",
                    f"{q['file']}: {q['id']} '{q['title']}' gates {len(q['dependents'])} quest(s) on "
                    f"{iid}; the only repo-visible source is a weighted table ({'; '.join(loot['tables'][:2])}) "
                    f"— verify native mob/loot drops in the installed {iid_ns} jar",
                    quest=q["id"], item=iid)
            elif gating and loot and loot["guaranteed"]:
                add("warning", "gate-item-structure-loot",
                    f"{q['file']}: {q['id']} '{q['title']}' gates {len(q['dependents'])} quest(s) on "
                    f"{iid}; craftless but a guaranteed drop in {'; '.join(loot['tables'][:3])} "
                    f"(verify explorer-map handoff and single-chest exhaustion risk)",
                    quest=q["id"], item=iid)
            elif gating and iid.split(':', 1)[0] in PROJECT_NS:
                add("critical", "unprovable-gate-item",
                    f"{q['file']}: {q['id']} '{q['title']}' gates {len(q['dependents'])} quest(s) "
                    f"on {iid} but nothing produces it (no recipe, no loot)",
                    quest=q["id"], item=iid)
            elif iid.split(":", 1)[0] in PROJECT_NS:
                add("info", "recipe-coverage-gap",
                    f"{q['file']}: {q['id']} task item {iid} has no source visible to static analysis "
                    f"(pack uses config/templated runtime recipes — verify against a live recipe dump)",
                    quest=q["id"], item=iid)
            elif not iid.startswith("minecraft:") and not RAW_OK_RE.search(iid) and iid not in loot_sources:
                add("info", "acquisition-unverified",
                    f"{q['file']}: {q['id']} task item {iid} not craftable by an enabled recipe "
                    f"(verify loot/worldgen/mob access in the intended era)", quest=q["id"], item=iid)

    # ---- layout coherence -------------------------------------- #
    LEGEND_SHAPES = {"hexagon", "heart", "diamond", "gear", "octagon", "rsquare"}
    for fname, qs in sorted(by_chapter.items()):
        off_legend = [q["id"] for q in qs if q["shape"] not in LEGEND_SHAPES]
        if off_legend:
            add("info", "non-legend-shape",
                f"{fname}: {len(off_legend)}/{len(qs)} quests use a non-legend shape "
                f"('{qs[0]['shape'] or 'empty'}' etc.) — the six-shape legend "
                f"(hexagon/heart/diamond/gear/rsquare/octagon) is not applied here", file=fname)
        coord_seen: dict[tuple, str] = {}
        for q in qs:
            key = (q["x"], q["y"])
            if key in coord_seen and isinstance(q["x"], (int, float)):
                add("info", "coord-collision",
                    f"{fname}: {q['id']} and {coord_seen[key]} share position {key}", quest=q["id"])
            else:
                coord_seen[key] = q["id"]
        # generated-era shape vs id-prefix branch (only for the structured id scheme
        # used by the Era 2-8 generator: <branch><era>1<13 digits>)
        for q in qs:
            if not re.fullmatch(r"[1-7][1-8]1[0-9]{13}", q["id"]):
                continue
            expect = GEN_PREFIX_BRANCH.get(q["id"][0])
            got = SHAPE_BRANCH.get(q["shape"])
            if expect and got and expect != got:
                add("info", "shape-branch-mismatch",
                    f"{fname}: {q['id']} '{q['title']}' id-scheme implies {expect} branch "
                    f"but shape is {q['shape']} ({got})", quest=q["id"])
        # backward dependency lines (child above parent)
        for q in qs:
            for d in q["dependencies"]:
                p = quests.get(d)
                if not p or p["file"] != fname:
                    continue
                if isinstance(q["y"], (int, float)) and isinstance(p["y"], (int, float)) and q["y"] < p["y"] - 0.01:
                    add("info", "backward-dependency-line",
                        f"{fname}: {q['id']} (y={q['y']}) depends on {d} (y={p['y']}) — dependency line points upward",
                        quest=q["id"])

    # ---- localization ----------------------------------------- #
    lang_quest_titles = {k[len("quest."):-len(".title")] for k in lang
                         if k.startswith("quest.") and k.endswith(".title")}
    for qid in sorted(lang_quest_titles):
        if qid not in quests:
            add("info", "ghost-localization",
                f"lang has quest.{qid}.title but no live quest {qid}", quest=qid)
    for q in quests.values():
        if not q["title"]:
            add("warning", "missing-title", f"{q['file']}: {q['id']} has no localized title", quest=q["id"])

    # ---- chapter/group membership --------------------------- #
    used_groups = {ch["group"] for ch in chapters}
    for gid in sorted(registered_groups - used_groups):
        add("warning", "unused-chapter-group",
            f"chapter group {gid} is registered in chapter_groups.snbt but no chapter uses it "
            f"(and it has {'a' if f'chapter_group.{gid}.title' in lang else 'no'} localized title)",
            group=gid)
    for ch in chapters:
        if ch["group"] not in registered_groups:
            add("critical", "unregistered-group", f"{ch['file']} group {ch['group']} not in chapter_groups.snbt", file=ch["file"])
        if not ch["icon"]:
            add("info", "chapter-icon-missing", f"{ch['file']} has no chapter icon", file=ch["file"])
        raw = (CHAPTER_DIR / f"{ch['file']}.snbt").read_text(encoding="utf-8")
        dqs = re.search(r'default_quest_shape:\s*"([^"]*)"', raw)
        if dqs and dqs.group(1) == "":
            add("warning", "empty-default-shape",
                f"{ch['file']}: default_quest_shape is \"\" (empty) — quests without an explicit "
                f"shape have no legend identity", file=ch["file"])
    grp_order = defaultdict(list)
    for ch in chapters:
        grp_order[ch["group"]].append((ch["order_index"], ch["file"]))
    for gid, entries in grp_order.items():
        idxs = [e[0] for e in entries]
        if len(idxs) != len(set(idxs)):
            add("warning", "order-index-collision",
                f"group {gid}: duplicate order_index among {sorted(entries)}", group=gid)

    # --------------------------------------------------------------------- #
    # Inventory summary
    # --------------------------------------------------------------------- #
    task_type_hist = Counter()
    reward_type_hist = Counter()
    shape_hist = Counter()
    for q in quests.values():
        for t in q["tasks"]:
            task_type_hist[t.get("type")] += 1
        for r in q["rewards"]:
            reward_type_hist[r.get("type")] += 1
        shape_hist[q["shape"]] += 1

    # ---- cross-chapter dependency inventory ----------------- #
    cross_edges = []
    for q in quests.values():
        for d in q["dependencies"]:
            p = quests.get(d)
            if not p or p["file"] == q["file"]:
                continue
            direction = "same"
            if q["era"] is not None and p["era"] is not None:
                direction = ("forward" if q["era"] > p["era"]
                             else "backward" if q["era"] < p["era"] else "same-era")
            cross_edges.append({
                "from_quest": d, "from_file": p["file"], "from_title": p["title"],
                "to_quest": q["id"], "to_file": q["file"], "to_title": q["title"],
                "direction": direction,
            })
            if direction == "backward":
                add("warning", "era-regression-dependency",
                    f"{q['file']} (Era {q['era']}) quest {q['id']} '{q['title']}' depends on "
                    f"{p['file']} (Era {p['era']}) quest {d} — later era gates an earlier one",
                    quest=q["id"])
    cross_edges.sort(key=lambda e: (e["to_file"], e["from_file"], e["to_quest"]))

    # ---- era branch reward-rhythm table -------------------- #
    branch_reward_table = {}
    for era in range(2, 9):
        fname = era_files[era]
        rows_e = {}
        for q in by_chapter.get(fname, []):
            m = re.fullmatch(r"([1-3])" + str(era) + r"10{11}([0-9]{2})", q["id"])
            if not m:
                continue
            branch = {"1": "mining", "2": "farming", "3": "exploration"}[m.group(1)]
            pos = int(m.group(2))
            rtypes = [r.get("type") for r in q["rewards"]]
            ritems = [r.get("item", {}).get("id") if isinstance(r.get("item"), dict) else r.get("type")
                      for r in q["rewards"]]
            rows_e.setdefault(branch, {})[pos] = {"types": rtypes, "items": ritems}
        branch_reward_table[f"era{era}"] = rows_e

    capstone_rewards = {}
    for era in range(0, 9):
        cap = era_capstone.get(era)
        if cap:
            capstone_rewards[f"era{era}"] = [
                {"type": r.get("type"),
                 "item": r.get("item", {}).get("id") if isinstance(r.get("item"), dict) else None,
                 "xp": r.get("xp"), "command": (r.get("command") or "")[:80]}
                for r in cap["rewards"]
            ]

    # ---- per-chapter rollup -------------------------------- #
    finding_file = defaultdict(lambda: Counter())
    for f in findings:
        fl = f.get("file")
        if not fl and f.get("quest") in quests:
            fl = quests[f["quest"]]["file"]
        if fl:
            finding_file[fl][f["severity"]] += 1
    for ch in chapters:
        qs = by_chapter.get(ch["file"], [])
        ch["shapes"] = dict(Counter(q["shape"] for q in qs))
        ch["task_types"] = dict(Counter(t.get("type") for q in qs for t in q["tasks"]))
        ch["checkmark_quests"] = sum(1 for q in qs if q["tasks"] and all(t.get("type") == "checkmark" for t in q["tasks"]))
        ch["reward_quests"] = sum(1 for q in qs if q["rewards"])
        ch["roots"] = [q["id"] for q in qs if not q["dependencies"]]
        ch["findings"] = dict(finding_file.get(ch["file"], {}))

    sev_order = {"critical": 0, "warning": 1, "info": 2}
    findings.sort(key=lambda f: (sev_order.get(f["severity"], 9), f["category"], f["message"]))
    sev_counts = Counter(f["severity"] for f in findings)
    cat_counts = Counter((f["severity"], f["category"]) for f in findings)

    report = {
        "generated_by": "scripts/audit_quest_tree_coherence.py",
        "progression_mode": data_cfg.get("progression_mode"),
        "totals": {
            "chapters": len(chapters),
            "quests": len(quests),
            "dependencies": sum(len(q["dependencies"]) for q in quests.values()),
            "tasks": sum(len(q["tasks"]) for q in quests.values()),
            "rewards": sum(len(q["rewards"]) for q in quests.values()),
        },
        "task_type_histogram": dict(task_type_hist.most_common()),
        "reward_type_histogram": dict(reward_type_hist.most_common()),
        "shape_histogram": dict(shape_hist.most_common()),
        "cross_chapter_dependencies": cross_edges,
        "era_branch_reward_rhythm": branch_reward_table,
        "capstone_rewards": capstone_rewards,
        "era_chain": [
            {
                "era": e,
                "file": era_files[e],
                "orientation": era_orientation[e]["id"] if era_orientation.get(e) else None,
                "capstone": era_capstone[e]["id"] if era_capstone.get(e) else None,
                "capstone_task": [
                    t.get("item", {}).get("id") for t in (era_capstone[e]["tasks"] if era_capstone.get(e) else [])
                    if isinstance(t.get("item"), dict)
                ],
            }
            for e in range(0, 9)
        ],
        "checkmark_quests": sorted(checkmark_rows, key=lambda r: (r["file"], str(r["quest"]))),
        "reward_bags": {
            "defined_in_loot_script": sorted(defined_bags),
            "registered_as_items": sorted(registered_bags),
            "referenced_by_quests": {str(k): v for k, v in sorted(era_bag_quests.items())},
        },
        "chapters": chapters,
        "finding_counts": {
            "by_severity": dict(sev_counts),
            "by_category": {f"{s}/{c}": n for (s, c), n in sorted(cat_counts.items(), key=lambda kv: (-kv[1], kv[0]))},
        },
        "findings": findings,
        "inventory": {
            qid: {
                k: quests[qid][k] for k in
                ("file", "era", "shape", "x", "y", "optional", "title",
                 "dependencies", "dependents", "dependency_requirement", "min_required_dependencies")
            } | {
                "tasks": [{"type": t.get("type"),
                           "item": t.get("item", {}).get("id") if isinstance(t.get("item"), dict) else None,
                           "count": t.get("count"),
                           "entity": t.get("entity"), "structure": t.get("structure"),
                           "biome": t.get("biome"), "dimension": t.get("dimension")}
                          for t in quests[qid]["tasks"]],
                "rewards": [{"type": r.get("type"),
                             "item": r.get("item", {}).get("id") if isinstance(r.get("item"), dict) else None,
                             "count": r.get("count") or (r.get("item", {}).get("count") if isinstance(r.get("item"), dict) else None),
                             "xp": r.get("xp"), "command": r.get("command")}
                            for r in quests[qid]["rewards"]],
            }
            for qid in quest_order
        },
    }
    OUT_JSON.write_text(json.dumps(report, indent=2), encoding="utf-8")

    # --------------------------------------------------------------------- #
    # stdout summary
    # --------------------------------------------------------------------- #
    print(f"Quest tree: {len(chapters)} chapters, {len(quests)} quests, "
          f"{report['totals']['dependencies']} dependency edges, progression_mode={report['progression_mode']}")
    print(f"Task types: {dict(task_type_hist.most_common())}")
    print(f"Reward types: {dict(reward_type_hist.most_common())}")
    print()
    print("Findings by severity:")
    for sev in ("critical", "warning", "info"):
        print(f"  {sev:9} {sev_counts.get(sev, 0)}")
    print()
    print("Findings by category:")
    for (s, c), n in sorted(cat_counts.items(), key=lambda kv: (sev_order.get(kv[0][0], 9), -kv[1])):
        print(f"  [{s:8}] {c:28} {n}")
    print()
    print("CRITICAL findings:")
    for f in findings:
        if f["severity"] == "critical":
            print(f"  - {f['message']}")
    print(f"\nFull report: {OUT_JSON.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
