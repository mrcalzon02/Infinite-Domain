"""Audit the loot tree against the quest tree for consistency and attainability.

Three failure modes make authored content silently unreachable in play, and none
of them are caught by the existing per-file audits:

  * a loot table rolls an item that was never registered, so the entry is dead;
  * a loot table is authored but nothing references it, so it never rolls;
  * a quest demands an item whose only source is a structure that is not placed
    by any structure set, so the quest cannot be completed.

This audit joins the loot graph, the worldgen placement graph and the quest tree
so those breaks surface as findings instead of as in-play dead ends.

Outputs:
  dev/docs/quest-loot-attainability/report.json    machine-readable findings
  dev/docs/quest-loot-attainability/findings.csv   one row per finding
  stdout                                           summary grouped by severity

Deterministic: no network, no randomness, stable ordering throughout.
"""

from __future__ import annotations

import csv
import gzip
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit_quest_tree_coherence import SNBTParser  # noqa: E402
from pack_content_oracle import ItemOracle, script_recipe_outputs, script_touched_items  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]

REGISTRY_ITEMS = ROOT / "dev/docs/registry-inventory/item-ids.txt"
REGISTRY_BLOCKS = ROOT / "dev/docs/registry-inventory/block-ids.txt"
RECIPE_OUTPUTS = ROOT / "dev/docs/recipe-index/recipe-outputs.csv"
KUBEJS_DATA = ROOT / "kubejs/data"
KUBEJS_STARTUP = ROOT / "kubejs/startup_scripts"
KUBEJS_CONFIG = ROOT / "kubejs/config"
DATAPACKS = ROOT / "datapacks"
CHAPTER_DIR = ROOT / "config/ftbquests/quests/chapters"

OUT_DIR = ROOT / "dev/docs/quest-loot-attainability"

# Loot tables the game addresses by a fixed convention rather than by an explicit
# reference, so absence of an inbound edge is not evidence that they are dead.
IMPLICIT_TABLE_PREFIXES = (
    "blocks/",       # block drops, bound by block id
    "entities/",     # entity drops, bound by entity id
    "gameplay/",     # vanilla gameplay hooks (fishing, hero of the village, ...)
    "archaeology/",  # brushable block loot
    "shearing/",     # shearing loot
    "spawners/",     # trial spawner loot
    "dispensers/",   # vanilla dispenser loot
    "pots/",         # decorated pot loot
    "equipment/",    # mob equipment tables
)


# --------------------------------------------------------------------------- #
# Item existence oracle
# --------------------------------------------------------------------------- #
def build_item_oracle() -> tuple[set[str], set[str]]:
    """Return (known_items, kubejs_defined_names).

    Mod items come from the registry snapshot. KubeJS items are registered at
    startup from scripts and their driving config JSON, so the snapshot lags
    behind them; a bare name quoted anywhere under startup_scripts/ or
    kubejs/config/ is treated as a definition site. Those two directories only
    ever declare content, so scanning them cannot mistake a reference for a
    definition the way scanning recipes would.
    """
    known: set[str] = set()
    for path in (REGISTRY_ITEMS, REGISTRY_BLOCKS):
        if path.exists():
            for line in path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line:
                    known.add(line)

    defined: set[str] = set()
    sources: list[str] = []
    if KUBEJS_STARTUP.is_dir():
        sources += [p.read_text(encoding="utf-8", errors="replace") for p in sorted(KUBEJS_STARTUP.glob("*.js"))]
    if KUBEJS_CONFIG.is_dir():
        sources += [p.read_text(encoding="utf-8", errors="replace") for p in sorted(KUBEJS_CONFIG.glob("*.json"))]
    for text in sources:
        for name in re.findall(r"['\"]([a-z][a-z0-9_]{2,})['\"]", text):
            defined.add(name)
    known |= {f"kubejs:{name}" for name in defined}
    return known, defined


# --------------------------------------------------------------------------- #
# Loot graph
# --------------------------------------------------------------------------- #
def loot_table_id(path: Path, data_root: Path) -> str:
    rel = path.relative_to(data_root)
    namespace = rel.parts[0]
    tail = Path(*rel.parts[2:]).with_suffix("").as_posix()
    return f"{namespace}:{tail}"


def walk_loot(node: object, items: set[str], refs: set[str], tags: set[str]) -> None:
    if isinstance(node, list):
        for child in node:
            walk_loot(child, items, refs, tags)
        return
    if not isinstance(node, dict):
        return

    kind = node.get("type")
    if kind in {"item", "minecraft:item"}:
        name = node.get("name")
        if isinstance(name, str):
            items.add(name)
    elif kind in {"tag", "minecraft:tag"}:
        name = node.get("name")
        if isinstance(name, str):
            tags.add(name.lstrip("#"))
    elif kind in {"loot_table", "minecraft:loot_table"}:
        value = node.get("value")
        if isinstance(value, str):
            refs.add(value)

    if node.get("function") in {"set_loot_table", "minecraft:set_loot_table"}:
        name = node.get("name")
        if isinstance(name, str):
            refs.add(name)

    for child in node.values():
        walk_loot(child, items, refs, tags)


def collect_loot_tables() -> dict[str, dict]:
    """Map loot table id -> {path, items, refs, tags, source}."""
    tables: dict[str, dict] = {}
    roots: list[tuple[Path, str]] = [(KUBEJS_DATA, "kubejs")]
    if DATAPACKS.is_dir():
        for pack in sorted(DATAPACKS.iterdir()):
            data_dir = pack / "data"
            if data_dir.is_dir():
                roots.append((data_dir, "datapack:" + pack.name))

    for data_root, source in roots:
        for path in sorted(data_root.glob("*/loot_table/**/*.json")):
            try:
                payload = json.loads(path.read_text(encoding="utf-8-sig"))
            except json.JSONDecodeError as exc:
                tables[loot_table_id(path, data_root)] = {
                    "path": path, "items": set(), "refs": set(), "tags": set(),
                    "source": source, "parse_error": str(exc),
                }
                continue
            items: set[str] = set()
            refs: set[str] = set()
            tags: set[str] = set()
            walk_loot(payload, items, refs, tags)
            tables[loot_table_id(path, data_root)] = {
                "path": path, "items": items, "refs": refs, "tags": tags,
                "source": source, "parse_error": None,
            }
    return tables


# --------------------------------------------------------------------------- #
# Structure NBT -> loot table edges
# --------------------------------------------------------------------------- #
def nbt_loot_refs(path: Path) -> set[str]:
    """Read every LootTable string tag out of a structure NBT."""
    raw = path.read_bytes()
    try:
        data = gzip.decompress(raw) if raw[:2] == b"\x1f\x8b" else raw
    except OSError:
        return set()

    found: set[str] = set()
    key = b"LootTable"
    idx = 0
    while True:
        i = data.find(key, idx)
        if i < 0:
            break
        idx = i + len(key)
        # A TAG_String named "LootTable": 0x08, name length (2 bytes BE), name.
        if i < 3 or data[i - 3] != 0x08:
            continue
        if int.from_bytes(data[i - 2:i], "big") != len(key):
            continue
        if idx + 2 > len(data):
            continue
        length = int.from_bytes(data[idx:idx + 2], "big")
        try:
            value = data[idx + 2:idx + 2 + length].decode("utf-8")
        except UnicodeDecodeError:
            continue
        if ":" in value:
            found.add(value)
    return found


def collect_structure_loot() -> dict[str, set[str]]:
    """Map structure NBT id -> referenced loot table ids."""
    out: dict[str, set[str]] = {}
    for path in sorted(KUBEJS_DATA.glob("*/structure/**/*.nbt")):
        rel = path.relative_to(KUBEJS_DATA)
        namespace = rel.parts[0]
        tail = Path(*rel.parts[2:]).with_suffix("").as_posix()
        refs = nbt_loot_refs(path)
        if refs:
            out[namespace + ":" + tail] = refs
    return out


# --------------------------------------------------------------------------- #
# Worldgen placement graph
# --------------------------------------------------------------------------- #
def collect_worldgen() -> tuple[dict[str, dict], dict[str, list[str]], dict[str, list[str]]]:
    """Return (structures, structure_sets, template_pool_elements)."""
    structures: dict[str, dict] = {}
    for path in sorted(KUBEJS_DATA.glob("*/worldgen/structure/**/*.json")):
        rel = path.relative_to(KUBEJS_DATA)
        namespace = rel.parts[0]
        tail = Path(*rel.parts[3:]).with_suffix("").as_posix()
        try:
            payload = json.loads(path.read_text(encoding="utf-8-sig"))
        except json.JSONDecodeError:
            payload = {}
        structures[namespace + ":" + tail] = {"path": path, "payload": payload}

    sets: dict[str, list[str]] = {}
    for path in sorted(KUBEJS_DATA.glob("*/worldgen/structure_set/**/*.json")):
        rel = path.relative_to(KUBEJS_DATA)
        namespace = rel.parts[0]
        tail = Path(*rel.parts[3:]).with_suffix("").as_posix()
        try:
            payload = json.loads(path.read_text(encoding="utf-8-sig"))
        except json.JSONDecodeError:
            payload = {}
        members = []
        for entry in payload.get("structures", []) or []:
            target = entry.get("structure") if isinstance(entry, dict) else None
            if isinstance(target, str):
                members.append(target)
        sets[namespace + ":" + tail] = members

    pools: dict[str, list[str]] = {}
    for path in sorted(KUBEJS_DATA.glob("*/worldgen/template_pool/**/*.json")):
        rel = path.relative_to(KUBEJS_DATA)
        namespace = rel.parts[0]
        tail = Path(*rel.parts[3:]).with_suffix("").as_posix()
        try:
            payload = json.loads(path.read_text(encoding="utf-8-sig"))
        except json.JSONDecodeError:
            payload = {}
        elements: list[str] = []

        def harvest(node: object) -> None:
            if isinstance(node, list):
                for child in node:
                    harvest(child)
            elif isinstance(node, dict):
                loc = node.get("location")
                if isinstance(loc, str):
                    elements.append(loc)
                for child in node.values():
                    harvest(child)

        harvest(payload)
        pools[namespace + ":" + tail] = elements
    return structures, sets, pools


# --------------------------------------------------------------------------- #
# Quest tree
# --------------------------------------------------------------------------- #
def collect_quest_tasks() -> list[dict]:
    tasks: list[dict] = []
    for path in sorted(CHAPTER_DIR.glob("*.snbt")):
        try:
            payload = SNBTParser(path.read_text(encoding="utf-8")).parse()
        except Exception as exc:  # noqa: BLE001 - report, do not abort the audit
            tasks.append({
                "chapter": path.stem, "quest": None, "task": None,
                "type": "parse_error", "value": str(exc),
            })
            continue
        for quest in payload.get("quests", []) or []:
            if not isinstance(quest, dict):
                continue
            quest_id = quest.get("id")
            for task in quest.get("tasks", []) or []:
                if not isinstance(task, dict):
                    continue
                ttype = task.get("type")
                value = None
                if ttype == "item":
                    item = task.get("item")
                    if isinstance(item, dict):
                        value = item.get("id")
                    elif isinstance(item, str):
                        value = item
                elif ttype == "structure":
                    value = task.get("structure")
                elif ttype == "dimension":
                    value = task.get("dimension")
                tasks.append({
                    "chapter": path.stem, "quest": quest_id,
                    "task": task.get("id"), "type": ttype, "value": value,
                })
    return tasks


def load_craftable() -> set[str]:
    craftable: set[str] = set()
    if not RECIPE_OUTPUTS.exists():
        return craftable
    with RECIPE_OUTPUTS.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            if (row.get("enabled") or "").strip().lower() == "true":
                output = (row.get("output_id") or "").strip()
                if output:
                    craftable.add(output)
    return craftable


# --------------------------------------------------------------------------- #
# Audit
# --------------------------------------------------------------------------- #
def main() -> int:
    oracle = ItemOracle()
    tables = collect_loot_tables()
    structure_loot = collect_structure_loot()
    structures, structure_sets, pools = collect_worldgen()
    tasks = collect_quest_tasks()
    craftable = load_craftable() | script_recipe_outputs()
    # Recipes built in loops over a config JSON never expose a literal output
    # id, so presence in the scripts is the only available evidence that pack
    # machinery exists for an item.
    script_touched, script_patterns = script_touched_items()

    def has_pack_machinery(item_id: str) -> bool:
        if item_id in script_touched:
            return True
        name = item_id.partition(':')[2]
        return any(p.match(name) for p in script_patterns)

    # Mod jars own most of the pack's content; without them every mod-provided
    # structure and drop looks like a break.
    known_structures = set(structures) | oracle.mods.structures
    mod_loot_sources: dict[str, set[str]] = defaultdict(set)
    for table_id, mod_items in oracle.mods.loot_tables.items():
        for item in mod_items:
            mod_loot_sources[item].add(table_id)

    findings: list[dict] = []

    def add(code: str, severity: str, message: str, **extra: object) -> None:
        findings.append({"code": code, "severity": severity, "message": message, **extra})

    # -- which structures actually get placed -------------------------------- #
    placed: set[str] = set(oracle.mods.placed_structures)
    for members in structure_sets.values():
        placed.update(members)
    # Jigsaw children reached through template pools are placed by their parent.
    pool_elements: set[str] = set()
    for elements in pools.values():
        pool_elements.update(elements)

    # -- loot table reachability --------------------------------------------- #
    referenced: set[str] = set()
    for refs in structure_loot.values():
        referenced.update(refs)
    for meta in tables.values():
        referenced.update(meta["refs"])

    # -- C1: loot item references resolve ------------------------------------ #
    for table_id in sorted(tables):
        meta = tables[table_id]
        if meta["parse_error"]:
            add("LOOT-PARSE", "critical",
                table_id + ": loot table does not parse (" + meta["parse_error"] + ")",
                table=table_id, path=meta["path"].relative_to(ROOT).as_posix())
            continue
        for item in sorted(meta["items"]):
            if not oracle.exists(item):
                add("LOOT-ITEM-UNKNOWN", "critical",
                    table_id + ": rolls unregistered item '" + item + "' (" + oracle.why_missing(item) + ") - this entry can never drop",
                    table=table_id, item=item,
                    path=meta["path"].relative_to(ROOT).as_posix())

    # -- C2: loot table references resolve ----------------------------------- #
    for table_id in sorted(tables):
        for ref in sorted(tables[table_id]["refs"]):
            if ref not in tables and ref not in oracle.mods.loot_tables and not ref.startswith("minecraft:"):
                add("LOOT-REF-MISSING", "critical",
                    table_id + ": references loot table '" + ref + "' which does not exist",
                    table=table_id, reference=ref)
    for structure_id in sorted(structure_loot):
        for ref in sorted(structure_loot[structure_id]):
            if ref not in tables and ref not in oracle.mods.loot_tables and not ref.startswith("minecraft:"):
                add("STRUCT-LOOT-MISSING", "critical",
                    structure_id + ": structure NBT references loot table '" + ref + "' which does not exist",
                    structure=structure_id, reference=ref)

    # -- C3: authored loot tables are reachable ------------------------------ #
    for table_id in sorted(tables):
        namespace, _, tail = table_id.partition(":")
        if tail.startswith(IMPLICIT_TABLE_PREFIXES):
            continue
        if table_id in referenced:
            continue
        if table_id in oracle.mods.loot_tables:
            continue  # overrides a mod's own table, which the mod still references
        add("LOOT-ORPHAN", "warning",
            table_id + ": authored loot table is referenced by no structure, block or table - it never rolls",
            table=table_id,
            path=tables[table_id]["path"].relative_to(ROOT).as_posix())

    # -- C4/C5/C6: quest tasks ----------------------------------------------- #
    loot_sources: dict[str, set[str]] = defaultdict(set)
    for table_id, meta in tables.items():
        for item in meta["items"]:
            loot_sources[item].add(table_id)

    structures_for_table: dict[str, set[str]] = defaultdict(set)
    for structure_id, refs in structure_loot.items():
        for ref in refs:
            structures_for_table[ref].add(structure_id)

    for task in tasks:
        if task["type"] == "parse_error":
            add("QUEST-PARSE", "critical",
                task["chapter"] + ": chapter does not parse (" + str(task["value"]) + ")",
                chapter=task["chapter"])
            continue

        label = str(task["chapter"]) + "/" + str(task["quest"])

        if task["type"] == "item" and task["value"]:
            item = task["value"]
            if not oracle.exists(item):
                add("QUEST-ITEM-UNKNOWN", "critical",
                    label + ": task item '" + item + "' is not registered (" + oracle.why_missing(item) + ")",
                    chapter=task["chapter"], quest=task["quest"], item=item)
                continue
            if item in craftable:
                continue
            sources = loot_sources.get(item, set())
            if mod_loot_sources.get(item):
                continue  # a mod's own loot provides it
            if not sources:
                # Mod items without a pack recipe are usually obtainable through
                # their own mod's systems; only pack-authored items are a break.
                if item.startswith("kubejs:") and not has_pack_machinery(item):
                    # Registered, but nothing in the pack makes, drops or even
                    # mentions it. Reported as a warning because a script recipe
                    # this audit cannot parse could still exist.
                    add("QUEST-ITEM-UNSOURCED", "warning",
                        label + ": pack item '" + item + "' has no recipe, no loot table entry, "
                        "and no mention in any server script or config",
                        chapter=task["chapter"], quest=task["quest"], item=item)
                continue
            # Loot-only item: at least one providing structure must be placed.
            providers = set()
            for table_id in sources:
                providers |= structures_for_table.get(table_id, set())
            if providers:
                reachable = {s for s in providers if s in placed or s in pool_elements}
                if not reachable:
                    add("QUEST-ITEM-UNPLACED-SOURCE", "critical",
                        label + ": item '" + item + "' only drops from structures that no structure set places ("
                        + ", ".join(sorted(providers)) + ")",
                        chapter=task["chapter"], quest=task["quest"], item=item,
                        providers=sorted(providers))

        elif task["type"] == "structure" and task["value"]:
            target = task["value"]
            if target not in known_structures:
                add("QUEST-STRUCT-MISSING", "critical",
                    label + ": structure task targets '" + target + "' which has no worldgen structure definition",
                    chapter=task["chapter"], quest=task["quest"], structure=target)
            elif target not in placed:
                add("QUEST-STRUCT-UNPLACED", "critical",
                    label + ": structure '" + target + "' is defined but belongs to no structure set, "
                    "so it never generates",
                    chapter=task["chapter"], quest=task["quest"], structure=target)

    # -- report -------------------------------------------------------------- #
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    severity_rank = {"critical": 0, "warning": 1, "info": 2}
    findings.sort(key=lambda f: (severity_rank.get(f["severity"], 9), f["code"], f["message"]))

    report = {
        "totals": {
            "loot_tables": len(tables),
            "loot_table_items": sum(len(m["items"]) for m in tables.values()),
            "structures_with_loot": len(structure_loot),
            "worldgen_structures": len(structures),
            "structure_sets": len(structure_sets),
            "placed_structures": len(placed),
            "template_pools": len(pools),
            "quest_tasks": len(tasks),
            "craftable_outputs": len(craftable),
        },
        "counts_by_code": dict(sorted(
            (code, sum(1 for f in findings if f["code"] == code))
            for code in {f["code"] for f in findings}
        )),
        "findings": findings,
    }
    (OUT_DIR / "report.json").write_text(
        json.dumps(report, indent=2, sort_keys=False) + "\n", encoding="utf-8")

    fields = ["severity", "code", "message"]
    with (OUT_DIR / "findings.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for finding in findings:
            writer.writerow(finding)

    print("Quest/loot attainability audit")
    for key, value in report["totals"].items():
        print("  " + key.ljust(24) + " " + str(value))
    print()
    if not findings:
        print("No findings: every loot entry resolves, every table is reachable, "
              "and every quest item is attainable.")
        return 0
    for code, count in report["counts_by_code"].items():
        severity = next(f["severity"] for f in findings if f["code"] == code)
        print("  " + severity.ljust(8) + " " + code.ljust(28) + " " + str(count))
    print("\nFull report: " + (OUT_DIR / "report.json").relative_to(ROOT).as_posix())
    return 1 if any(f["severity"] == "critical" for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
