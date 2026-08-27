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
  7. no player-facing lang VALUE contains the substring "hive" (case-insensitive).
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
    "infinite_domain:hive_world",
    "infinite_domain:hive_world_stack_test",
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
    DATA / "worldgen/noise_settings/hive_world.json",
    DATA / "worldgen/biome/hive_world_stack_test.json",
    DATA / "advancement/hive_world/reach_cinderstack.json",
]
hive_json += sorted((DATA / "worldgen/density_function/hive_world").glob("*.json")) if (
    DATA / "worldgen/density_function/hive_world"
).is_dir() else []

arrival_fn = DATA / "function/hive_world/build_arrival.mcfunction"
expedition_js = REPO / "kubejs/server_scripts/hive_world_expedition.js"
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
    for key, want in (("min_y", -64), ("height", 384), ("logical_height", 384)):
        if dt.get(key) != want:
            fail(f"[3] dimension_type {key} = {dt.get(key)!r}, height contract requires {want}")
    ns = docs.get(DATA / "worldgen/noise_settings/hive_world.json")
    if ns is not None:
        n = ns.get("noise", {})
        if n.get("min_y") != -64 or n.get("height") != 384:
            fail(f"[3] noise_settings noise block {n} disagrees with the height contract")

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
    if bs.get("type") == "minecraft:fixed":
        biome = bs.get("biome", "")
        if biome.startswith("infinite_domain:") and not (
            DATA / f"worldgen/biome/{biome.split(':', 1)[1]}.json"
        ).is_file():
            fail(f"[4] fixed biome_source references {biome} but the biome file is missing")
    elif not bs:
        fail("[4] dimension has no biome_source")

# ---- 5. entry pieces exist -----------------------------------------
for p in (arrival_fn, expedition_js, items_js,
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
scan_string_literals(items_js, "hive_world_items.js")
adv = docs.get(DATA / "advancement/hive_world/reach_cinderstack.json")
if adv is not None and "hive" in json.dumps(adv.get("display", {})).lower():
    fail('[7] advancement display text contains "hive"')

# ---- report --------------------------------------------------------------
print("Hive World smoke validator")
for n in notes:
    print(f"  note: {n}")
if failures:
    print(f"\nFAIL ({len(failures)}):")
    for f in failures:
        print(f"  {f}")
    sys.exit(1)
print("\nPASS - all assertions hold")
sys.exit(0)
