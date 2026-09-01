#!/usr/bin/env python3
"""Offline smoke validator for the Hive World spike.

Endgame checkpoint EG-P01-S05-C0022. Spec: docs/endgame/test-strategy.md section 7.
Runs with no live Minecraft instance. Exit 0 = pass.

Assertions:
  1. every Hive JSON file parses;
  2. block/item registry references resolve against docs/registry-inventory/
     (kubejs: spike-declared IDs are allowed);
  3. dimension_type bounds equal the C0006 height contract;
  4. dimension.json references a real noise_settings and a biome source;
  5. the arrival function and the entry item / advancement files exist;
  6. no Hive file is written under a forbidden shared path;
  7. no player-facing lang VALUE contains the substring "hive" (case-insensitive);
  8. each Hive server script is IIFE-wrapped (KubeJS shares one global scope);
  9. every infinite_domain:hive_world/* density-function reference resolves to a file;
 10. the jigsaw district's pools, module NBTs, structure and structure_set resolve.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
DATA = REPO / "kubejs/data/infinite_domain"
ASSETS = REPO / "kubejs/assets"
REG = REPO / "docs/registry-inventory"

SPIKE_DECLARED = {
    "kubejs:cinderstack_marker",
    "kubejs:cinderstack_return_marker",
    "kubejs:cinderstack_filter",
    "kubejs:cinderstack_mask",
    "infinite_domain:hive_world",
    "infinite_domain:hive_world_sump",
    "infinite_domain:hive_world_works",
    "infinite_domain:hive_world_vault",
    "infinite_domain:hive_world_acid_pool",
    "infinite_domain:hive_world_fixture_light",
    "infinite_domain:hive_world_salvage",
    "infinite_domain:hive_world_network",
    "infinite_domain:hive_world_shaft",
    "infinite_domain:hive_world_hall",
    "infinite_domain:hive_world_columns",
    "infinite_domain:hive_world_district",
    "infinite_domain:chests/hive_world_salvage",
}

failures: list[str] = []
notes: list[str] = []


def fail(msg: str) -> None:
    failures.append(msg)


def load_json(path: pathlib.Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        fail(f"[1] {path.relative_to(REPO)} does not parse: {exc}")
        return None


# ---- collect Hive files ------------------------------------------------------
hive_json = [
    DATA / "dimension/hive_world.json",
    DATA / "dimension_type/hive_world.json",
    DATA / "advancement/hive_world/reach_cinderstack.json",
    DATA / "loot_table/chests/hive_world_salvage.json",
]
hive_json += sorted(p for p in (DATA / "worldgen").rglob("*hive_world*.json"))
hive_json += sorted(p for p in (DATA / "worldgen/template_pool/hive_world").glob("*.json")) \
    if (DATA / "worldgen/template_pool/hive_world").is_dir() else []

arrival_fn = DATA / "function/hive_world/build_arrival.mcfunction"
expedition_js = REPO / "kubejs/server_scripts/hive_world_expedition.js"
atmosphere_js = REPO / "kubejs/server_scripts/hive_world_atmosphere_proto.js"
items_js = REPO / "kubejs/startup_scripts/hive_world_items.js"

# ---- 1. parse --------------------------------------------------------------
docs = {}
for p in hive_json:
    if not p.is_file():
        fail(f"[1] missing expected Hive file: {p.relative_to(REPO)}")
        continue
    docs[p] = load_json(p)

# ---- 2. registry references ----------------------------------------------
known_blocks = set()
bidf = REG / "block-ids.txt"
if bidf.is_file():
    known_blocks = {ln.strip() for ln in bidf.read_text(encoding="utf-8").splitlines() if ln.strip()}
else:
    notes.append("block-ids.txt not found; skipped block-reference resolution")

if known_blocks:
    blob = json.dumps({str(k): v for k, v in docs.items() if v is not None})
    for ref in sorted(set(re.findall(r'"Name"\s*:\s*"([a-z0-9_]+:[a-z0-9_/]+)"', blob))):
        if ref in known_blocks or ref in SPIKE_DECLARED:
            continue
        fail(f"[2] unresolved block reference: {ref}")

# ---- 3. height contract -------------------------------------------------
dt = docs.get(DATA / "dimension_type/hive_world.json")
if dt is not None:
    for key, want in (("min_y", -64), ("height", 672), ("logical_height", 672)):
        if dt.get(key) != want:
            fail(f"[3] dimension_type {key} = {dt.get(key)!r}, height contract requires {want}")
    ns = docs.get(DATA / "worldgen/noise_settings/hive_world.json")
    if ns is not None:
        n = ns.get("noise", {})
        if n.get("min_y") != -64 or n.get("height") != 672:
            fail(f"[3] noise_settings noise block {n} disagrees with the height contract")
        if ns.get("sea_level") != 0:
            fail(f"[3] noise_settings sea_level = {ns.get('sea_level')!r}, planetary datum requires 0")
        if ns.get("default_fluid", {}).get("Name") != "the_wasteland_reworked:acid":
            fail("[3] noise_settings default_fluid must be the established static acid block")

# ---- 4. dimension wiring ----------------------------------------------
dim = docs.get(DATA / "dimension/hive_world.json")
if dim is not None:
    gen = dim.get("generator", {})
    if gen.get("type") != "minecraft:noise":
        fail(f"[4] dimension generator type = {gen.get('type')!r}, expected minecraft:noise")
    if gen.get("settings") != "infinite_domain:hive_world":
        fail(f"[4] dimension generator settings = {gen.get('settings')!r}")
    if not (DATA / "worldgen/noise_settings/hive_world.json").is_file():
        fail("[4] dimension references noise_settings infinite_domain:hive_world but the file is missing")
    bs = gen.get("biome_source", {})
    referenced_biomes = []
    if bs.get("type") == "minecraft:fixed":
        referenced_biomes = [bs.get("biome", "")]
    elif bs.get("type") == "minecraft:multi_noise":
        referenced_biomes = [e.get("biome", "") for e in bs.get("biomes", [])]
        if len(referenced_biomes) < 2:
            fail("[4] multi_noise biome_source has fewer than 2 entries (routing needs a split)")
        # Every horizontal climate role must cover the full depth range. Exterior
        # roles do that with one [-1, 1] window; the core tiles it with six bands.
        windows_by_horizontal = {}
        for entry in bs.get("biomes", []):
            params = entry.get("parameters", {})
            depth = params.get("depth")
            horizontal = params.get("continentalness")
            if isinstance(depth, list) and isinstance(horizontal, list):
                windows_by_horizontal.setdefault(tuple(horizontal), []).append(depth)
        for horizontal, windows in windows_by_horizontal.items():
            windows = sorted(windows)
            if not windows or windows[0][0] != -1.0 or windows[-1][1] != 1.0:
                fail(f"[4] continentalness {horizontal} does not cover depth [-1, 1]: {windows}")
            for lo, hi in zip(windows, windows[1:]):
                if abs(lo[1] - hi[0]) > 1e-6:
                    fail(
                        f"[4] continentalness {horizontal} depth windows have a "
                        f"gap/overlap: {lo} then {hi}"
                    )
    elif not bs:
        fail("[4] dimension has no biome_source")
    for biome in referenced_biomes:
        if biome.startswith("infinite_domain:") and not (
            DATA / f"worldgen/biome/{biome.split(':', 1)[1]}.json"
        ).is_file():
            fail(f"[4] biome_source references {biome} but the biome file is missing")

# ---- 5. entry pieces exist -----------------------------------------
for p in (arrival_fn, expedition_js, atmosphere_js, items_js,
          DATA / "advancement/hive_world/reach_cinderstack.json"):
    if not p.is_file():
        fail(f"[5] missing entry component: {p.relative_to(REPO)}")

# ---- 6. no forbidden shared paths --------------------------------
for shared in ("kubejs/data/minecraft", "kubejs/data/wastelands"):
    d = REPO / shared
    if d.is_dir():
        for f in d.rglob("*hive_world*"):
            fail(f"[6] Hive file under shared namespace: {f.relative_to(REPO)}")
for f in (DATA / "worldgen").rglob("*.nbt"):
    if "hive_world" in f.name:
        fail(f"[6] binary NBT under a JSON worldgen path: {f.relative_to(REPO)}")

# ---- 7. no "hive" in player-facing values -----------------------
def scan_lang_values() -> None:
    for langf in ASSETS.rglob("lang/*.json"):
        try:
            obj = json.loads(langf.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        for k, v in obj.items():
            if isinstance(v, str) and "hive" in v.lower():
                fail(f'[7] lang value contains "hive": {langf.relative_to(REPO)} :: {k} = {v!r}')


def scan_string_literals(path: pathlib.Path, label: str) -> None:
    """Only inspect strings passed to player-facing sinks, not resource IDs or commands."""
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    text = "\n".join(re.sub(r"//.*$", "", ln) for ln in text.splitlines())
    sink = re.compile(
        r"(?:\.tell|\.tooltip|\.displayName|\.title|\bcharles)\s*\(\s*"
        r"(?:player\s*,\s*)?"
        r"((?:'(?:[^'\\]|\\.)*'|\"(?:[^\"\\]|\\.)*\")(?:\s*\+\s*[^,)]+)*)"
    )
    for m in sink.finditer(text):
        for lit in re.findall(r"'((?:[^'\\]|\\.)*)'|\"((?:[^\"\\]|\\.)*)\"", m.group(1)):
            s = lit[0] or lit[1]
            if "hive" in s.lower():
                fail(f'[7] player-facing string in {label} contains "hive": {s!r}')


scan_lang_values()
scan_string_literals(expedition_js, "hive_world_expedition.js")
scan_string_literals(atmosphere_js, "hive_world_atmosphere_proto.js")
scan_string_literals(items_js, "hive_world_items.js")
adv = docs.get(DATA / "advancement/hive_world/reach_cinderstack.json")
if adv is not None and "hive" in json.dumps(adv.get("display", {})).lower():
    fail('[7] advancement display text contains "hive"')

# ---- 8. server scripts are IIFE-scoped ---------------------------
# KubeJS server scripts share one global scope; a bare top-level `const` collides
# across files (this bit the spike once: "redeclaration of const HIVE").
for js in (expedition_js, atmosphere_js):
    if not js.is_file():
        continue
    source = js.read_text(encoding="utf-8")
    body = "\n".join(
        ln for ln in source.splitlines()
        if not ln.lstrip().startswith("//")
    ).strip()
    if not re.match(r"\(\s*(?:\(\s*\)\s*=>|function\b)", body):
        fail(f"[8] {js.name} is not wrapped in an IIFE - its top-level consts share global scope")
    if re.search(r"\breturn\s*\{\s*[A-Za-z_$][\w$]*\s*(?:,\s*[A-Za-z_$][\w$]*\s*)*\}", source):
        fail(f"[8] {js.name} uses object-property shorthand, which KubeJS Rhino rejects")
    if ".level.dimension()" in source:
        fail(f"[8] {js.name} calls level.dimension() even though current KubeJS exposes dimension as a property")

# ---- 9. density-function reference integrity --------------------
df_dir = DATA / "worldgen/density_function/hive_world"
if df_dir.is_dir():
    df_files = {p.stem for p in df_dir.glob("*.json")}
    scope = list(df_dir.glob("*.json")) + [DATA / "worldgen/noise_settings/hive_world.json"]
    for p in scope:
        try:
            blob = p.read_text(encoding="utf-8")
        except OSError:
            continue
        for m in re.findall(r'"(infinite_domain:hive_world/([a-z_]+))"', blob):
            if m[1] not in df_files:
                fail(f"[9] {p.name} references density function {m[0]} but hive_world/{m[1]}.json is missing")
    # every density function must parse
    for p in df_dir.glob("*.json"):
        try:
            density = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(f"[9] density function {p.name} does not parse: {exc}")
            continue
        if density.get("type") == "minecraft:range_choice":
            if "max_inclusive" in density:
                fail(f"[9] density function {p.name} uses obsolete range_choice field max_inclusive")
            if "max_exclusive" not in density:
                fail(f"[9] density function {p.name} range_choice is missing max_exclusive")
else:
    notes.append("no hive_world density_function directory (spike may predate the density graph)")

# ---- 10. jigsaw district integrity ----------------------------
pool_dir = DATA / "worldgen/template_pool/hive_world"
struct_nbt_dir = DATA / "structure/hive_world"
structure_dir = DATA / "worldgen/structure"
set_dir = DATA / "worldgen/structure_set"
district_files = sorted(structure_dir.glob("hive_world_district*.json"))
expected_band_districts = {
    f"hive_world_district_{slug}"
    for slug in ("drown", "underworks", "furnace", "billet", "vaulting", "crown")
}
if district_files:
    modules = {p.stem for p in struct_nbt_dir.glob("*.nbt")} if struct_nbt_dir.is_dir() else set()
    pools = {p.stem for p in pool_dir.glob("*.json")} if pool_dir.is_dir() else set()
    for pj in pool_dir.glob("*.json"):
        pd = json.loads(pj.read_text(encoding="utf-8"))
        fb = pd.get("fallback", "")
        if fb.startswith("infinite_domain:hive_world/") and fb.split("/")[-1] not in pools:
            fail(f"[10] pool {pj.name} fallback {fb} does not resolve")
        for el in pd.get("elements", []):
            loc = el.get("element", {}).get("location", "")
            if loc.startswith("infinite_domain:hive_world/") and loc.split("/")[-1] not in modules:
                fail(f"[10] pool {pj.name} element {loc} has no matching NBT")
    actual_band_districts = {path.stem for path in district_files if path.stem != "hive_world_district"}
    missing_band_districts = sorted(expected_band_districts - actual_band_districts)
    extra_band_districts = sorted(actual_band_districts - expected_band_districts)
    if missing_band_districts or extra_band_districts:
        fail(
            f"[10] six-band district inventory drift: missing={missing_band_districts}, "
            f"extra={extra_band_districts}"
        )
    for district in district_files:
        dj = json.loads(district.read_text(encoding="utf-8"))
        sp = dj.get("start_pool", "")
        if sp.split("/")[-1] not in pools:
            fail(f"[10] {district.name} start_pool {sp} does not resolve")
        for b in dj.get("biomes", []):
            if b.startswith("infinite_domain:") and not (DATA / f"worldgen/biome/{b.split(':',1)[1]}.json").is_file():
                fail(f"[10] {district.name} biome {b} missing")
        ss = set_dir / district.name
        if not ss.is_file():
            fail(f"[10] {district.stem} structure_set is missing")
            continue
        structures = json.loads(ss.read_text(encoding="utf-8")).get("structures", [])
        if district.stem == "hive_world_district":
            if structures:
                fail("[10] unrouted compatibility district structure_set must remain inert")
            continue
        expected_structure = f"infinite_domain:{district.stem}"
        if structures != [{"structure": expected_structure, "weight": 1}]:
            fail(f"[10] {district.name} structure_set does not exclusively own {expected_structure}")
        for s in structures:
            sid = s.get("structure", "")
            if sid.startswith("infinite_domain:") and not (DATA / f"worldgen/structure/{sid.split(':',1)[1]}.json").is_file():
                fail(f"[10] structure_set references {sid} but no structure file")
else:
    fail("[10] no Hive World district structures are present")

# ---- report --------------------------------------------------------------
print("Hive World smoke validator")
for n in notes:
    print(f"  note: {n}")

if "--json" in sys.argv:
    dest = sys.argv[sys.argv.index("--json") + 1]
    out = pathlib.Path(dest)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "validator": "hive_world_smoke",
        "passed": not failures,
        "failure_count": len(failures),
        "failures": failures,
        "notes": notes,
        "files_checked": [str(p.relative_to(REPO)).replace("\\", "/") for p in hive_json],
    }, indent=2) + "\n", encoding="utf-8")
    print(f"  report -> {out}")

if failures:
    print(f"\nFAIL ({len(failures)}):")
    for f in failures:
        print(f"  {f}")
    sys.exit(1)
print("\nPASS - all assertions hold")
sys.exit(0)
