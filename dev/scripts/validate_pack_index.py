#!/usr/bin/env python3
"""Revalidate every pack index against what is actually installed.

Covers the four index artifacts:

  dev/docs/registry-inventory/  item-ids, block-ids, item-block-registry.{csv,json},
                                namespace-summary.csv, entity-ids.txt, mod-jar-index.json
  dev/docs/recipe-index/        recipe-index/-inputs/-outputs/-definitions, cross-mod-candidates
  dev/docs/MOD_LIST.md          human-readable mod table
  dev/docs/registry-inventory/README.md   hand-maintained coverage numbers

Checks internal consistency, agreement between the artifacts, and drift against
the jars in mods/ plus kubejs/data. Read-only: it never rewrites an index — run
build_mod_index.py / build_effective_recipe_index.py for that.

The item/block registry came from a one-time live KubeJS registry dump and cannot
be regenerated without launching the instance, so it is validated by presence and
cross-reference rather than rebuilt.
"""

from __future__ import annotations

import csv
import io
import json
import re
import sys
import tomllib
import zipfile
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REG = ROOT / "dev/docs/registry-inventory"
RECIPES = ROOT / "dev/docs/recipe-index"
MOD_LIST = ROOT / "dev/docs/MOD_LIST.md"
MODS = ROOT / "mods"

ID_RE = re.compile(r"^[a-z0-9_.-]+:[a-z0-9_./-]+$")

results: list[tuple[str, str, str]] = []  # (level, section, message)


def ok(section: str, msg: str) -> None:
    results.append(("PASS", section, msg))


def warn(section: str, msg: str) -> None:
    results.append(("WARN", section, msg))


def fail(section: str, msg: str) -> None:
    results.append(("FAIL", section, msg))


def check(section: str, cond: bool, good: str, bad: str, soft: bool = False) -> bool:
    (ok if cond else (warn if soft else fail))(section, good if cond else bad)
    return cond


def read_lines(path: Path) -> list[str]:
    return [l.strip() for l in path.read_text(encoding="utf-8-sig").splitlines() if l.strip()]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def sample(values, n: int = 8) -> str:
    values = sorted(values)
    head = ", ".join(values[:n])
    return head + (f" ... (+{len(values) - n} more)" if len(values) > n else "")


# --------------------------------------------------------------------------
# 1. Mod index: mod-jar-index.json / MOD_LIST.md vs mods/*.jar
# --------------------------------------------------------------------------
def scan_jars() -> tuple[dict, dict, set]:
    """Return (per-namespace static evidence, per-jar declared mod IDs, all mod IDs).

    The per-jar map covers only each jar's own `[[mods]]` tables, matching what
    build_mod_index.py records. The third value additionally includes mod IDs from
    JarJar-nested jars, which register real content but are not their own file in
    mods/ — needed so bundled mods are not mistaken for uninstalled ones.
    """
    evidence: dict[str, dict[str, int]] = defaultdict(
        lambda: {"item_models": 0, "blockstates": 0, "lang_items": 0, "lang_blocks": 0,
                 "fluids": 0, "assets": 0, "data": 0}
    )
    jar_modids: dict[str, list[str]] = {}
    all_modids: set[str] = set()
    asset_re = re.compile(r"^assets/([a-z0-9_.-]+)/")
    data_re = re.compile(r"^data/([a-z0-9_.-]+)/")
    item_model_re = re.compile(r"^assets/([a-z0-9_.-]+)/models/item/.+\.json$")
    blockstate_re = re.compile(r"^assets/([a-z0-9_.-]+)/blockstates/.+\.json$")
    lang_re = re.compile(r"^assets/([a-z0-9_.-]+)/lang/en_us\.json$")
    modid_re = re.compile(r'modId\s*=\s*"([a-z0-9_\-]+)"')

    def absorb(zf: zipfile.ZipFile, names: list[str]) -> None:
        for n in names:
            m = item_model_re.match(n)
            if m:
                evidence[m.group(1)]["item_models"] += 1
            m = blockstate_re.match(n)
            if m:
                evidence[m.group(1)]["blockstates"] += 1
            m = asset_re.match(n)
            if m:
                evidence[m.group(1)]["assets"] += 1
            m = data_re.match(n)
            if m:
                evidence[m.group(1)]["data"] += 1
            if lang_re.match(n):
                try:
                    lang = json.loads(zf.read(n).decode("utf-8", "replace"))
                except Exception:
                    continue
                if not isinstance(lang, dict):
                    continue
                for key in lang:
                    parts = key.split(".")
                    if len(parts) >= 3 and parts[0] in ("item", "block", "fluid_type", "fluid"):
                        bucket = {"item": "lang_items", "block": "lang_blocks"}.get(parts[0], "fluids")
                        evidence[parts[1]][bucket] += 1

    def declared_modids(zf: zipfile.ZipFile, names: list[str]) -> set[str]:
        """Mod IDs from the [[mods]] tables only — a regex over the whole file
        would also pick up [[dependencies.*]] modId entries."""
        found: set[str] = set()
        for candidate in ("META-INF/neoforge.mods.toml", "META-INF/mods.toml"):
            if candidate not in names:
                continue
            raw = zf.read(candidate).decode("utf-8", "replace")
            try:
                found.update(m["modId"] for m in tomllib.loads(raw).get("mods", []) if m.get("modId"))
            except Exception:
                found.update(modid_re.findall(raw))
        return found - {"minecraft", "forge", "neoforge"}

    for jar in sorted(MODS.glob("*.jar")):
        try:
            with zipfile.ZipFile(jar) as zf:
                names = zf.namelist()
                absorb(zf, names)
                jar_modids[jar.name] = sorted(declared_modids(zf, names))
                all_modids.update(jar_modids[jar.name])
                # "Bundled" mods ship their real content in JarJar-nested jars; the
                # outer jar registers nothing itself.
                for nested in (n for n in names
                               if n.startswith("META-INF/jarjar/") and n.endswith(".jar")):
                    try:
                        with zipfile.ZipFile(io.BytesIO(zf.read(nested))) as inner:
                            inner_names = inner.namelist()
                            absorb(inner, inner_names)
                            all_modids.update(declared_modids(inner, inner_names))
                    except (zipfile.BadZipFile, KeyError):
                        warn("mod-index", f"{jar.name} bundles an unreadable nested jar: {nested}")
        except zipfile.BadZipFile:
            fail("mod-index", jar.name + " is not a readable zip")
            jar_modids[jar.name] = []
    return evidence, jar_modids, all_modids


def check_mod_index(jar_modids: dict[str, list[str]]) -> None:
    s = "mod-index"
    disk = set(jar_modids)
    index = json.loads((REG / "mod-jar-index.json").read_text(encoding="utf-8-sig"))
    indexed = {r["file"] for r in index}

    check(s, disk == indexed,
          f"mod-jar-index.json covers all {len(disk)} jars in mods/",
          f"jar drift - on disk only: {sample(disk - indexed)}; indexed only: {sample(indexed - disk)}")

    mismatched = [r["file"] for r in index
                  if sorted(r.get("modids") or []) != jar_modids.get(r["file"], [])]
    check(s, not mismatched,
          "every indexed jar's mod IDs match its neoforge.mods.toml",
          f"{len(mismatched)} jar(s) with stale mod IDs: {sample(mismatched)}")

    no_modid = [r["file"] for r in index if not r.get("modids")]
    check(s, not no_modid,
          "every jar declares at least one mod ID",
          f"{len(no_modid)} jar(s) declare no mod ID: {sample(no_modid)}", soft=True)

    unnamed = [r["file"] for r in index if not r.get("name")]
    check(s, not unnamed,
          "every jar resolves to a CurseForge display name in minecraftinstance.json",
          f"{len(unnamed)} jar(s) missing a manifest entry: {sample(unnamed)}", soft=True)

    # MOD_LIST.md must enumerate exactly the same jars.
    text = MOD_LIST.read_text(encoding="utf-8-sig")
    listed = set(re.findall(r"\|\s*`([^`]+\.jar)`\s*\|", text))
    check(s, listed == disk,
          f"MOD_LIST.md table rows cover all {len(disk)} jars",
          f"MOD_LIST.md drift - missing: {sample(disk - listed)}; extra: {sample(listed - disk)}")

    stated = re.search(r"(\d+) jars total: (\d+) third-party \+ (\d+) project-built", text)
    if check(s, stated is not None, "MOD_LIST.md states a jar total",
             "MOD_LIST.md has no jar-total sentence"):
        total, third, own = (int(g) for g in stated.groups())
        check(s, total == len(disk) and third + own == total,
              f"MOD_LIST.md totals are self-consistent and match disk ({total} = {third} + {own})",
              f"MOD_LIST.md says {total} jars ({third}+{own}) but mods/ holds {len(disk)}")

    # Project-built jars must point at a source tree that exists.
    for jar_file, src in re.findall(r"- `([^`]+\.jar)` \(`[^`]+`\) - source: `([^`]+)/`",
                                    text.replace("—", "-")):
        check(s, (ROOT / src).is_dir(),
              f"project source exists: {src}",
              f"{jar_file} claims source `{src}/` which does not exist")


# --------------------------------------------------------------------------
# 2. Item/block registry: internal consistency
# --------------------------------------------------------------------------
def check_registry() -> tuple[set[str], set[str], dict]:
    s = "registry"
    data = json.loads((REG / "item-block-registry.json").read_text(encoding="utf-8-sig"))
    items, blocks = list(data["items"]), list(data["blocks"])
    item_set, block_set = set(items), set(blocks)

    check(s, len(items) == len(item_set), f"{len(items)} item IDs are unique",
          f"{len(items) - len(item_set)} duplicate item IDs in JSON")
    check(s, len(blocks) == len(block_set), f"{len(blocks)} block IDs are unique",
          f"{len(blocks) - len(block_set)} duplicate block IDs in JSON")
    # The live dump sorted with a collator that differs from byte order in a few
    # spots (radium226_* vs radium_*), which is cosmetic. What must hold is that
    # all three representations agree on one order.
    check(s, items == sorted(items) and blocks == sorted(blocks),
          "JSON item and block arrays are in byte-sorted order",
          f"{sum(1 for a, b in zip(items, sorted(items)) if a != b)} item and "
          f"{sum(1 for a, b in zip(blocks, sorted(blocks)) if a != b)} block position(s) deviate "
          f"from byte order (collation difference in the source dump, not missing data)", soft=True)

    bad = [i for i in items + blocks if not ID_RE.match(i)]
    check(s, not bad, "every registry ID is a well-formed namespaced ID",
          f"{len(bad)} malformed ID(s): {sample(bad)}")

    counts = data["counts"]
    check(s, counts.get("items") == len(items) and counts.get("blocks") == len(blocks),
          "JSON counts block matches the arrays",
          f"JSON counts say items={counts.get('items')} blocks={counts.get('blocks')}, "
          f"arrays hold {len(items)}/{len(blocks)}")
    total = counts.get("total_registry_entries")
    check(s, total == len(items) + len(blocks),
          f"total_registry_entries ({total}) equals items + blocks",
          f"total_registry_entries={total} but items+blocks={len(items) + len(blocks)}")
    both_key = next((k for k in counts if "both" in k), None)
    if both_key:
        check(s, counts[both_key] == len(item_set & block_set),
              f"{both_key} ({counts[both_key]}) matches the registry intersection",
              f"counts claim {counts[both_key]} shared IDs, intersection holds "
              f"{len(item_set & block_set)}")

    # Flat text dumps must agree with the JSON.
    txt_items, txt_blocks = read_lines(REG / "item-ids.txt"), read_lines(REG / "block-ids.txt")
    check(s, set(txt_items) == item_set, "item-ids.txt matches the JSON item array",
          f"item-ids.txt drift - txt only: {sample(set(txt_items) - item_set)}; "
          f"json only: {sample(item_set - set(txt_items))}")
    check(s, set(txt_blocks) == block_set, "block-ids.txt matches the JSON block array",
          f"block-ids.txt drift - txt only: {sample(set(txt_blocks) - block_set)}; "
          f"json only: {sample(block_set - set(txt_blocks))}")

    # CSV must be a faithful long-form of the same data, with correct flags.
    rows = read_csv(REG / "item-block-registry.csv")
    csv_items = {r["id"] for r in rows if r["registry"] == "item"}
    csv_blocks = {r["id"] for r in rows if r["registry"] == "block"}
    check(s, len(rows) == len(items) + len(blocks),
          f"item-block-registry.csv holds one row per registry entry ({len(rows)})",
          f"CSV holds {len(rows)} rows, expected {len(items) + len(blocks)}")
    check(s, csv_items == item_set and csv_blocks == block_set,
          "CSV item/block rows match the JSON arrays",
          f"CSV drift - items+/-{len(csv_items ^ item_set)}, blocks+/-{len(csv_blocks ^ block_set)}")
    check(s, [r["id"] for r in rows if r["registry"] == "item"] == items
          and [r["id"] for r in rows if r["registry"] == "block"] == blocks
          and txt_items == items and txt_blocks == blocks,
          "CSV, text dumps and JSON agree on entry order",
          "the CSV / text dumps / JSON disagree on entry order")

    ns_bad = [r["id"] for r in rows if ":" not in r["id"]
              or r["namespace"] != r["id"].split(":", 1)[0]
              or r["path"] != r["id"].split(":", 1)[1]]
    check(s, not ns_bad, "every CSV row's namespace/path columns match its ID",
          f"{len(ns_bad)} row(s) with a namespace/path that disagrees with the ID: {sample(ns_bad)}")

    # `also_registered_as_block` is an item-row column; block rows leave it blank.
    flag_col = next((c for c in rows[0] if c.startswith("also_registered_as")), None)
    if flag_col:
        wrong = [r["id"] for r in rows
                 if r["registry"] == "item" and (r[flag_col] == "True") != (r["id"] in block_set)]
        check(s, not wrong, f"every item row's `{flag_col}` flag agrees with the block registry",
              f"{len(wrong)} item row(s) with a wrong `{flag_col}` flag: {sample(wrong)}")
        stray = [r["id"] for r in rows if r["registry"] == "block" and r[flag_col]]
        check(s, not stray, f"block rows leave `{flag_col}` blank",
              f"{len(stray)} block row(s) carry a `{flag_col}` value: {sample(stray)}")

    # namespace-summary.csv must be a faithful rollup.
    derived_i: dict[str, int] = defaultdict(int)
    derived_b: dict[str, int] = defaultdict(int)
    for i in items:
        derived_i[i.split(":", 1)[0]] += 1
    for b in blocks:
        derived_b[b.split(":", 1)[0]] += 1
    summary = {r["namespace"]: r for r in read_csv(REG / "namespace-summary.csv")}
    all_ns = set(derived_i) | set(derived_b)
    check(s, set(summary) == all_ns,
          f"namespace-summary.csv lists all {len(all_ns)} namespaces",
          f"namespace-summary drift - missing: {sample(all_ns - set(summary))}; "
          f"extra: {sample(set(summary) - all_ns)}")
    off = [ns for ns in all_ns & set(summary)
           if int(summary[ns]["item_count"]) != derived_i[ns]
           or int(summary[ns]["block_count"]) != derived_b[ns]
           or int(summary[ns]["total_registry_entries"]) != derived_i[ns] + derived_b[ns]]
    check(s, not off, "every namespace-summary.csv count matches the registry",
          f"{len(off)} namespace(s) with wrong counts: {sample(off)}")

    return item_set, block_set, {"items": derived_i, "blocks": derived_b, "meta": data}


# --------------------------------------------------------------------------
# 3. Registry vs the installed mod set
# --------------------------------------------------------------------------
def check_registry_drift(item_set: set[str], block_set: set[str],
                         evidence: dict, all_modids: set[str]) -> None:
    s = "registry-drift"
    reg_ns = {i.split(":", 1)[0] for i in item_set | block_set}
    # Namespaces a currently-installed jar could plausibly register content under.
    jar_ns = set(evidence) | all_modids | {"minecraft"}

    orphans = sorted(reg_ns - jar_ns - {"kubejs"})
    if orphans:
        detail = ", ".join(
            f"{ns} ({sum(1 for i in item_set if i.startswith(ns + ':'))} items, "
            f"{sum(1 for b in block_set if b.startswith(ns + ':'))} blocks)" for ns in orphans)
    check(s, not orphans,
          f"all {len(reg_ns)} registry namespaces trace back to an installed jar",
          f"{len(orphans)} registry namespace(s) have no installed jar - the dump predates a mod "
          f"removal: {detail if orphans else ''}")

    # A namespace shipping item models or blockstates but holding no registry entry
    # means the dump predates that mod. Lang keys are deliberately not used as
    # evidence: mods routinely ship translation keys under namespaces they do not own.
    # ...and only for a namespace some installed jar actually declares as a mod ID.
    # Mods routinely ship compat assets under namespaces owned by mods that are not
    # installed (supplementaries -> dynamictrees, vslab_compat); those register nothing.
    content_ns = {ns for ns, e in evidence.items() if e["item_models"] or e["blockstates"]}
    missing = sorted((content_ns & all_modids) - reg_ns)
    if missing:
        detail = ", ".join(f"{ns} ({evidence[ns]['item_models']} item models, "
                           f"{evidence[ns]['blockstates']} blockstates)" for ns in missing)
    check(s, not missing,
          "every installed mod that ships item/block assets appears in the registry",
          f"{len(missing)} installed mod namespace(s) ship item/block assets but have no registry "
          f"entry - the dump predates them: {detail if missing else ''}")
    compat_only = sorted(content_ns - all_modids - reg_ns)
    if compat_only:
        ok(s, f"{len(compat_only)} namespace(s) carry compat assets for mods that are not "
              f"installed and correctly register nothing: {sample(compat_only, 10)}")

    # KubeJS-registered content lives in startup scripts, not in a jar, so it needs
    # its own comparison against the dump.
    startup = "\n".join(p.read_text(encoding="utf-8", errors="replace")
                        for p in sorted((ROOT / "kubejs/startup_scripts").rglob("*.js")))
    declared = set(re.findall(r"""event\.create\(\s*['"]([a-z0-9_./]+)['"]""", startup))
    dumped = {i.split(":", 1)[1] for i in item_set | block_set if i.startswith("kubejs:")}
    absent = sorted(declared - dumped)
    check(s, not absent,
          f"every literally-named KubeJS item ({len(declared)}) is in the registry dump",
          f"{len(absent)} KubeJS-registered ID(s) are missing from the registry dump: "
          f"{sample(absent, 12)}")

    # A KubeJS *recipe* override for an uninstalled mod is dead weight. Tag and
    # worldgen directories may legitimately use an invented namespace, so only
    # recipe-bearing directories are judged.
    kube_data = ROOT / "kubejs/data"
    recipe_dirs = [d for d in sorted(kube_data.iterdir())
                   if d.is_dir() and ((d / "recipe").is_dir() or (d / "recipes").is_dir())]
    dead = [d.name for d in recipe_dirs if d.name not in jar_ns and d.name != "kubejs"]
    check(s, not dead,
          f"every recipe-bearing kubejs/data namespace targets an installed mod "
          f"({len(recipe_dirs)} dirs)",
          f"{len(dead)} kubejs/data recipe namespace(s) target uninstalled mods: {sample(dead)}")


# --------------------------------------------------------------------------
# 4. Recipe index: internal consistency + agreement with mods/ and kubejs/
# --------------------------------------------------------------------------
def check_recipe_index() -> None:
    s = "recipe-index"
    index = read_csv(RECIPES / "recipe-index.csv")
    ids = {r["recipe_id"] for r in index}
    check(s, len(index) == len(ids), f"{len(index)} recipe rows, one per recipe ID",
          f"{len(index) - len(ids)} duplicate recipe_id row(s)")

    bad = [r["recipe_id"] for r in index
           if r["recipe_namespace"] != r["recipe_id"].split(":", 1)[0]
           or r["recipe_path"] != r["recipe_id"].split(":", 1)[1]]
    check(s, not bad, "every row's namespace/path columns match its recipe ID",
          f"{len(bad)} row(s) with a namespace/path that disagrees: {sample(bad)}")

    defs = read_csv(RECIPES / "recipe-definitions.csv")
    def_ids = {r["recipe_id"] for r in defs}
    check(s, def_ids == ids, "recipe-definitions.csv covers exactly the indexed recipe IDs",
          f"definition drift - defs only: {sample(def_ids - ids)}; index only: {sample(ids - def_ids)}")

    winners: dict[str, int] = defaultdict(int)
    tally: dict[str, int] = defaultdict(int)
    for r in defs:
        tally[r["recipe_id"]] += 1
        if r["is_winner"] == "True":
            winners[r["recipe_id"]] += 1
    multi = [k for k, v in winners.items() if v != 1]
    check(s, not multi and len(winners) == len(ids),
          "every recipe ID has exactly one winning definition",
          f"{len(multi)} recipe(s) without exactly one winner; "
          f"{len(ids - set(winners))} with none: {sample(multi)}")

    by_id = {r["recipe_id"]: r for r in index}
    counts_off = [rid for rid in ids if int(by_id[rid]["definition_count"]) != tally[rid]]
    check(s, not counts_off, "definition_count matches recipe-definitions.csv",
          f"{len(counts_off)} row(s) with a wrong definition_count: {sample(counts_off)}")

    over_off = [rid for rid in ids if (by_id[rid]["overridden"] == "True") != (tally[rid] > 1)]
    check(s, not over_off, "the `overridden` flag matches having multiple definitions",
          f"{len(over_off)} row(s) with a wrong `overridden` flag: {sample(over_off)}")

    xmod = read_csv(RECIPES / "cross-mod-candidates.csv")
    expected = {r["recipe_id"] for r in index if r["cross_mod_candidate"] == "True"}
    check(s, {r["recipe_id"] for r in xmod} == expected,
          f"cross-mod-candidates.csv matches the {len(expected)} flagged rows",
          "cross-mod-candidates.csv disagrees with the cross_mod_candidate column")

    failures = read_csv(RECIPES / "parse-failures.csv")
    check(s, not failures, "no recipe JSON failed to parse",
          f"{len(failures)} recipe(s) failed to parse: {sample(r['recipe_id'] for r in failures)}")

    # Every winning source path must still exist where the index says it does.
    kube_missing = [r["recipe_id"] for r in index
                    if r["winning_source_kind"] == "kubejs_override"
                    and not (ROOT / r["winning_source_path"]).is_file()]
    check(s, not kube_missing, "every winning KubeJS override file still exists on disk",
          f"{len(kube_missing)} KubeJS override path(s) missing: {sample(kube_missing)}")

    jars_on_disk = {j.name for j in MODS.glob("*.jar")} | {"minecraft-1.21.1.jar"}
    ghost = sorted({r["winning_source"] for r in index
                    if r["winning_source_kind"] in ("mod_jar", "vanilla")} - jars_on_disk)
    check(s, not ghost, "every winning jar source is still installed",
          f"{len(ghost)} recipe source jar(s) no longer in mods/: {sample(ghost)}")

    # The index must cover every KubeJS recipe file actually present.
    kube_root = ROOT / "kubejs/data"
    kube_re = re.compile(r"^([^/]+)/recipes?/(.+)\.json$")
    on_disk = set()
    for f in kube_root.rglob("*.json"):
        m = kube_re.match(f.relative_to(kube_root).as_posix())
        if m:
            on_disk.add(f"{m.group(1)}:{m.group(2)}")
    check(s, not (on_disk - ids),
          f"all {len(on_disk)} KubeJS recipe files are represented in the index",
          f"{len(on_disk - ids)} KubeJS recipe file(s) missing from the index: {sample(on_disk - ids)}")

    stated = (RECIPES / "README.md").read_text(encoding="utf-8-sig")
    for label, actual in (("Unique recipe IDs", len(ids)),
                          ("Enabled effective recipes", sum(1 for r in index if r["enabled"] == "True")),
                          ("Deliberately disabled recipes", sum(1 for r in index if r["enabled"] != "True"))):
        m = re.search(r"\| " + re.escape(label) + r" \| (\d+) \|", stated)
        check(s, m is not None and int(m.group(1)) == actual,
              f"recipe-index README states the right {label.lower()} ({actual})",
              f"recipe-index README says {label} = {m.group(1) if m else '(absent)'}, actual {actual}")


# --------------------------------------------------------------------------
# 5. Recipes vs the item/block registry
# --------------------------------------------------------------------------
def check_recipe_registry_coherence(item_set: set[str], block_set: set[str],
                                    evidence: dict, installed: set[str]) -> None:
    s = "recipe-vs-registry"
    known = item_set | block_set
    reg_ns = {i.split(":", 1)[0] for i in known}
    fluid_ns = {ns for ns, e in evidence.items() if e["fluids"]} | {"minecraft", "c"}
    startup = "\n".join(p.read_text(encoding="utf-8", errors="replace")
                        for p in sorted((ROOT / "kubejs/startup_scripts").rglob("*.js")))

    def kubejs_registered(path: str) -> bool:
        """True if a startup script creates this ID, literally or via a template."""
        if re.search(r"""['"`]""" + re.escape(path) + r"""['"`]""", startup):
            return True
        parts = path.split("_")
        # Loop-built IDs: `darknet_session_injector_tier_${tier}`, `${metal.id}_mineral_trace`
        return any(re.search(re.escape("_".join(parts[:i])) + r"""_?\$\{""", startup)
                   or re.search(r"""\$\{[^}]*\}_?""" + re.escape("_".join(parts[i:])), startup)
                   for i in range(1, len(parts)))

    # Winning source path per recipe, so an unresolved reference can be traced back
    # to the JSON that declares it and checked for load conditions.
    source_of = {r["recipe_id"]: (r["winning_source_kind"], r["winning_source"],
                                  r["winning_source_path"])
                 for r in read_csv(RECIPES / "recipe-index.csv")}
    jar_cache: dict[str, zipfile.ZipFile] = {}
    condition_cache: dict[str, bool | None] = {}

    def evaluate(node: object) -> bool | None:
        """Three-valued NeoForge condition evaluation: True met, False unmet,
        None not decidable from disk (mod-specific config flags)."""
        if not isinstance(node, dict):
            return None
        ctype = node.get("type")
        if ctype == "neoforge:mod_loaded":
            return node.get("modid") in installed
        if ctype == "neoforge:not":
            inner = evaluate(node.get("value"))
            return None if inner is None else not inner
        if ctype in ("neoforge:and", "neoforge:or"):
            values = [evaluate(v) for v in node.get("values", [])]
            if ctype == "neoforge:and":
                return False if False in values else (None if None in values else True)
            return True if True in values else (None if None in values else False)
        if ctype == "neoforge:true":
            return True
        if ctype == "neoforge:false":
            return False
        return None

    raw_cache: dict[str, str] = {}

    def raw_recipe(recipe_id: str) -> str:
        """The winning definition's JSON text, or '' if it cannot be read."""
        if recipe_id in raw_cache:
            return raw_cache[recipe_id]
        kind, source, spath = source_of.get(recipe_id, ("", "", ""))
        text = ""
        try:
            if kind == "kubejs_override":
                text = (ROOT / spath).read_text(encoding="utf-8-sig")
            elif kind in ("mod_jar", "vanilla"):
                jar = MODS / source
                if jar.is_file():
                    if source not in jar_cache:
                        jar_cache[source] = zipfile.ZipFile(jar)
                    text = jar_cache[source].read(spath).decode("utf-8-sig")
        except Exception:
            text = ""
        raw_cache[recipe_id] = text
        return text

    def load_status(recipe_id: str) -> bool | None:
        """Whether the winning definition's load conditions are met."""
        if recipe_id in condition_cache:
            return condition_cache[recipe_id]
        try:
            data = json.loads(raw_recipe(recipe_id))
        except Exception:
            data = None
        conditions = data.get("neoforge:conditions") if isinstance(data, dict) else None
        if not conditions:
            result: bool | None = True
        else:
            if not isinstance(conditions, list):
                conditions = [conditions]
            values = [evaluate(c) for c in conditions]
            result = False if False in values else (None if None in values else True)
        condition_cache[recipe_id] = result
        return result

    def verdict(ref: str, refs_by_id: dict[str, set[str]]) -> bool | None:
        """Worst-case load status across every recipe that uses this reference."""
        statuses = {load_status(rid) for rid in refs_by_id[ref]}
        return True if True in statuses else (None if None in statuses else False)

    for kind, path, col in (("input", RECIPES / "recipe-inputs.csv", "input_id"),
                            ("output", RECIPES / "recipe-outputs.csv", "output_id")):
        rows = read_csv(path)
        refs_by_id: dict[str, set[str]] = defaultdict(set)
        for r in rows:
            refs_by_id[r[col]].add(r["recipe_id"])
        strict = {r[col] for r in rows if r["ref_kind"] == "item"}

        # KubeJS items exist only at runtime; validate them against the scripts
        # that create them rather than against the live-dump registry.
        kube_refs = {r for r in strict if r.startswith("kubejs:")}
        unregistered = sorted(r for r in kube_refs if not kubejs_registered(r.split(":", 1)[1]))
        check(s, not unregistered,
              f"every `kubejs:` {kind} reference ({len(kube_refs)}) is created by a startup script",
              f"{len(unregistered)} `kubejs:` {kind} reference(s) are created by no startup script: "
              f"{sample(unregistered, 12)}")

        strict -= kube_refs
        unresolved = strict - known
        live = {u for u in unresolved if verdict(u, refs_by_id) is True}
        undecidable = {u for u in unresolved if verdict(u, refs_by_id) is None}
        dead = unresolved - live - undecidable

        check(s, not live,
              f"every loadable `item` {kind} reference resolves to a registered item or block "
              f"({len(strict)} distinct)",
              f"{len(live)} `item` {kind} reference(s) are used by recipes that do load but are "
              f"absent from the registry: {sample(live, 15)}")
        if dead:
            ok(s, f"{len(dead)} unresolvable `item` {kind} reference(s) are reached only through "
                  f"load conditions that are not met: {sample(dead, 6)}")
        if undecidable:
            warn(s, f"{len(undecidable)} `item` {kind} reference(s) hang off mod-specific config "
                    f"flags that cannot be evaluated from disk: {sample(undecidable, 10)}")

        loose = {r[col] for r in rows if r["ref_kind"] == "resource"}
        residue = {u for u in loose - known
                   if u.split(":", 1)[0] in reg_ns and u.split(":", 1)[0] not in fluid_ns
                   and verdict(u, refs_by_id) is not False}
        # The index normalizer also picks up potion-registry IDs out of item
        # components; those are not expected to resolve to an item or block.
        potions = {u for u in residue
                   if any(f'"potion": "{u}"' in raw_recipe(rid) for rid in refs_by_id[u])}
        residue -= potions
        if potions:
            ok(s, f"{len(potions)} `resource` {kind} reference(s) are potion-registry IDs read out "
                  f"of item components, not items: {sample(potions, 6)}")
        check(s, not residue,
              f"every untyped `resource` {kind} reference resolves to an item, block, or fluid",
              f"{len(residue)} `resource` {kind} reference(s) resolve to nothing known: "
              f"{sample(residue, 15)}", soft=True)


# --------------------------------------------------------------------------
# 6. Hand-maintained registry README numbers
# --------------------------------------------------------------------------
def check_registry_readme(item_set: set[str], block_set: set[str], derived: dict) -> None:
    s = "registry-readme"
    text = (REG / "README.md").read_text(encoding="utf-8-sig")
    entity_count = len(read_lines(REG / "entity-ids.txt"))
    ns_count = len({i.split(":", 1)[0] for i in item_set | block_set})
    for label, actual in (("Item IDs", len(item_set)), ("Block IDs", len(block_set)),
                          ("Total registry entries", len(item_set) + len(block_set)),
                          ("IDs present in both registries", len(item_set & block_set)),
                          ("Namespaces represented", ns_count)):
        m = re.search(r"- " + re.escape(label) + r": (\d+)", text)
        check(s, m is not None and int(m.group(1)) == actual,
              f"README states the right {label} ({actual})",
              f"README says {label} = {m.group(1) if m else '(absent)'}, actual {actual}")

    # The "Largest namespaces" table must agree with namespace-summary.csv.
    table = re.findall(r"^\| ([a-z0-9_.-]+) \| (\d+) \| (\d+) \| (\d+) \|$", text, re.M)
    off = [ns for ns, i, b, t in table
           if derived["items"].get(ns, 0) != int(i) or derived["blocks"].get(ns, 0) != int(b)
           or int(t) != int(i) + int(b)]
    check(s, not off, f"README's largest-namespace table ({len(table)} rows) matches the registry",
          f"{len(off)} README namespace row(s) disagree with the registry: {sample(off)}")
    ok(s, f"entity-ids.txt holds {entity_count} entity IDs")


def main() -> int:
    print("scanning mods/ ...", file=sys.stderr)
    evidence, jar_modids, all_modids = scan_jars()
    check_mod_index(jar_modids)
    item_set, block_set, derived = check_registry()
    check_registry_drift(item_set, block_set, evidence, all_modids)
    check_recipe_index()
    check_recipe_registry_coherence(item_set, block_set, evidence, all_modids | {'minecraft'})
    check_registry_readme(item_set, block_set, derived)

    width = max(len(sec) for _, sec, _ in results)
    for level in ("FAIL", "WARN", "PASS"):
        for lv, sec, msg in results:
            if lv == level:
                print(f"{lv:4}  {sec:<{width}}  {msg}")
    fails = sum(1 for lv, _, _ in results if lv == "FAIL")
    warns = sum(1 for lv, _, _ in results if lv == "WARN")
    passes = sum(1 for lv, _, _ in results if lv == "PASS")
    print(f"\n{passes} passed, {warns} warned, {fails} failed")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
