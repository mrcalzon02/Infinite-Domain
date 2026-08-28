#!/usr/bin/env python3
"""Connector validator for the Hive World jigsaw modules.

Endgame checkpoint EG-P04-S01-C0052 (connector validator), authored ahead of Phase 4.
Contract: docs/endgame/contracts/module-schema.md.
Runs offline. Exit 0 = pass. Palette mismatches are warnings, not failures, until the
per-band module families land (C0055-C0060).
"""
from __future__ import annotations

import gzip
import json
import pathlib
import struct
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
DATA = REPO / "kubejs/data/infinite_domain"
NBT_DIR = DATA / "structure/hive_world"
POOL_DIR = DATA / "worldgen/template_pool/hive_world"
MANIFEST = REPO / "docs/endgame/hive-world-module-manifest.json"

CONNECTOR_HEIGHT = {"door": 3, "hall": 4, "service": 2}
CONNECTOR_WIDTH = {"door": 1, "hall": 3, "service": 1}
LEGAL_FINAL_STATE = {"minecraft:air", "minecraft:chiseled_polished_blackstone"}
FACING_DELTA = {"north": (0, 0, -1), "south": (0, 0, 1), "east": (1, 0, 0), "west": (-1, 0, 0)}
SPIKE_MAX = (48, 32, 48)
BUDGET_NON_AIR = 48_000
BUDGET_BE = 6

failures: list[str] = []
warnings: list[str] = []


def fail(m: str) -> None:
    failures.append(m)


def warn(m: str) -> None:
    warnings.append(m)


# ---- minimal NBT reader ---------------------------------------------------
def _p(d, i, tag):
    if tag == 1:
        return d[i], i + 1
    if tag == 2:
        return struct.unpack(">h", d[i:i + 2])[0], i + 2
    if tag == 3:
        return struct.unpack(">i", d[i:i + 4])[0], i + 4
    if tag == 4:
        return struct.unpack(">q", d[i:i + 8])[0], i + 8
    if tag == 5:
        return struct.unpack(">f", d[i:i + 4])[0], i + 4
    if tag == 6:
        return struct.unpack(">d", d[i:i + 8])[0], i + 8
    if tag == 8:
        n = struct.unpack(">H", d[i:i + 2])[0]
        return d[i + 2:i + 2 + n].decode("utf-8"), i + 2 + n
    if tag == 9:
        et = d[i]
        i += 1
        count = struct.unpack(">i", d[i:i + 4])[0]
        i += 4
        out = []
        for _ in range(count):
            v, i = _p(d, i, et)
            out.append(v)
        return out, i
    if tag == 10:
        out = {}
        while d[i] != 0:
            t = d[i]
            i += 1
            ln = struct.unpack(">H", d[i:i + 2])[0]
            i += 2
            key = d[i:i + ln].decode("utf-8")
            i += ln
            v, i = _p(d, i, t)
            out[key] = v
        return out, i + 1
    if tag in (7, 11, 12):  # byte/int/long array
        n = struct.unpack(">i", d[i:i + 4])[0]
        w = {7: 1, 11: 4, 12: 8}[tag]
        return list(d[i + 4:i + 4 + n * w]), i + 4 + n * w
    raise ValueError(f"tag {tag}")


def read_nbt(path: pathlib.Path) -> dict:
    raw = gzip.decompress(path.read_bytes())
    assert raw[0] == 10, "root is not a compound"
    nlen = struct.unpack(">H", raw[1:3])[0]
    val, _ = _p(raw, 3 + nlen, 10)
    return val


# ---- checks -------------------------------------------------------------
def check_module(entry: dict, pools: dict) -> None:
    mid = entry["id"].split("/")[-1]
    p = REPO / entry["nbt"]
    if not p.is_file():
        fail(f"[1] {mid}: NBT file missing at {entry['nbt']}")
        return
    try:
        root = read_nbt(p)
    except Exception as exc:  # noqa: BLE001
        fail(f"[1] {mid}: NBT does not parse: {exc}")
        return

    if root.get("DataVersion") != 3955:
        fail(f"[1] {mid}: DataVersion {root.get('DataVersion')} != 3955")
    for key in ("size", "palette", "blocks"):
        if key not in root:
            fail(f"[1] {mid}: missing '{key}'")
    size = tuple(root.get("size", []))
    if size != tuple(entry["size"]):
        fail(f"[9] {mid}: manifest size {entry['size']} != NBT size {list(size)}")
    for axis, (v, cap) in enumerate(zip(size, SPIKE_MAX)):
        if v > cap:
            fail(f"[2] {mid}: size axis {axis} = {v} exceeds spike cap {cap}")

    palette = [b["Name"] for b in root["palette"]]
    props = [b.get("Properties", {}) for b in root["palette"]]
    grid: dict[tuple, tuple] = {}
    non_air = 0
    block_entities = 0
    jigsaws = []
    for b in root["blocks"]:
        pos = tuple(b["pos"])
        st = b["state"]
        name = palette[st]
        grid[pos] = name
        if name != "minecraft:air":
            non_air += 1
        bnbt = b.get("nbt")
        if bnbt and "id" in bnbt:
            if name == "minecraft:jigsaw":
                jigsaws.append((pos, bnbt, props[st].get("orientation", "north_up")))
            else:
                block_entities += 1

    if non_air > BUDGET_NON_AIR:
        fail(f"[2] {mid}: {non_air} non-air blocks exceed budget {BUDGET_NON_AIR}")
    if block_entities > BUDGET_BE:
        fail(f"[2] {mid}: {block_entities} block entities exceed budget {BUDGET_BE}")
    if entry["non_air"] != non_air:
        fail(f"[9] {mid}: manifest non_air {entry['non_air']} != actual {non_air}")
    if entry["block_entities"] != block_entities:
        fail(f"[9] {mid}: manifest block_entities {entry['block_entities']} != actual {block_entities}")

    # connectors
    role = entry["role"]
    declared = {tuple(c["local_pos"]): c for c in entry["connectors"]}
    actual_pos = {pos for pos, _, _ in jigsaws}
    if set(declared) != actual_pos:
        fail(f"[9] {mid}: manifest connector positions {sorted(declared)} != NBT jigsaw positions {sorted(actual_pos)}")

    empty_conns = 0
    for pos, bnbt, orient in jigsaws:
        nm = bnbt.get("name", "")
        tg = bnbt.get("target", "")
        if nm != tg:
            fail(f"[3] {mid} @ {pos}: name {nm!r} != target {tg!r}")
        ctype = nm.split("/")[-1]
        if ctype not in CONNECTOR_HEIGHT:
            fail(f"[3] {mid} @ {pos}: connector type {ctype!r} not in {sorted(CONNECTOR_HEIGHT)}")
            continue
        if bnbt.get("final_state") not in LEGAL_FINAL_STATE:
            fail(f"[3] {mid} @ {pos}: final_state {bnbt.get('final_state')!r} not legal")
        if bnbt.get("joint") not in ("aligned", "rollable"):
            fail(f"[3] {mid} @ {pos}: joint {bnbt.get('joint')!r} not legal")
        if bnbt.get("joint") == "rollable" and len(jigsaws) != 1:
            fail(f"[3] {mid} @ {pos}: joint 'rollable' only allowed on single-connector modules")
        sealing = bnbt.get("final_state") != "minecraft:air"
        if bnbt.get("pool") == "minecraft:empty":
            empty_conns += 1
        elif bnbt.get("pool", "").split("/")[-1] not in pools:
            fail(f"[8] {mid} @ {pos}: pool {bnbt.get('pool')!r} does not resolve")

        # a sealing terminal has no open passage - skip the opening / clearance checks
        if sealing:
            continue

        # opening carved: the jigsaw cell + (height-1) above are air or jigsaw
        dx, _, dz = FACING_DELTA.get(declared[pos]["facing"], (0, 0, 0))
        h = CONNECTOR_HEIGHT[ctype]
        for dy in range(h):
            cell = grid.get((pos[0], pos[1] + dy, pos[2]), "minecraft:air")
            if cell not in ("minecraft:air", "minecraft:jigsaw"):
                fail(f"[4] {mid} @ {pos}: opening blocked at +{dy}Y by {cell}")
        # one step into the module must be walkable with a floor
        walkable = ("minecraft:air", "minecraft:ladder", "minecraft:jigsaw")
        into = (pos[0] - dx, pos[1], pos[2] - dz)
        if grid.get(into, "minecraft:air") not in walkable:
            warn(f"[6] {mid} @ {pos}: first step into the module is {grid.get(into)}, not walkable")
        below = (into[0], into[1] - 1, into[2])
        if grid.get(below, "minecraft:air") in ("minecraft:air",):
            warn(f"[6] {mid} @ {pos}: no floor one step into the module")

    # floor-datum consistency
    data = sorted({p[1] for p in declared})
    if role == "transition":
        if len(data) < 2:
            fail(f"[5] {mid}: role 'transition' but only one connector floor datum {data}")
    elif len(data) > 1:
        fail(f"[5] {mid}: role '{role}' (level) but connectors on multiple data {data}")

    # role vs connectors / pools
    n = len(jigsaws)
    if role == "start" and n < 3:
        fail(f"[7] {mid}: role 'start' needs >=3 connectors, has {n}")
    if role == "branch" and n < 2:
        fail(f"[7] {mid}: role 'branch' needs >=2 connectors, has {n}")
    if role in ("leaf", "terminal"):
        if n != 1 or empty_conns != 1:
            fail(f"[7] {mid}: role '{role}' needs exactly 1 minecraft:empty connector (has {n}, {empty_conns} empty)")
    if role == "terminal":
        if any(bn.get("final_state") == "minecraft:air" for _, bn, _ in jigsaws):
            fail(f"[7] {mid}: terminal connector must seal (final_state != air)")


def check_pools(pools: dict, module_ids: set) -> None:
    for name, pj in pools.items():
        fb = pj.get("fallback", "")
        if fb.startswith("infinite_domain:hive_world/") and fb.split("/")[-1] not in pools:
            fail(f"[8] pool {name}: fallback {fb} does not resolve")
        for el in pj.get("elements", []):
            loc = el.get("element", {}).get("location", "")
            if loc.split("/")[-1] not in module_ids:
                fail(f"[8] pool {name}: element {loc} has no module")
    if "start" in pools and len(pools["start"].get("elements", [])) != 1:
        fail("[4] 'start' pool must have exactly one element")
    if "branch" in pools and len(pools["branch"].get("elements", [])) < 3:
        fail("[4] 'branch' pool must have >=3 elements")


def main() -> int:
    if not MANIFEST.is_file():
        fail("module manifest missing - run generate_hive_world_structures.py")
        print("FAIL: no manifest")
        return 1
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    pools = {}
    for pj in sorted(POOL_DIR.glob("*.json")):
        pools[pj.stem] = json.loads(pj.read_text(encoding="utf-8"))
    module_ids = {m["id"].split("/")[-1] for m in manifest["modules"]}

    check_pools(pools, module_ids)
    for entry in manifest["modules"]:
        check_module(entry, pools)

    print("Hive World module / connector validator")
    for w in warnings:
        print(f"  warn {w}")
    if failures:
        print(f"\nFAIL ({len(failures)}):")
        for f in failures:
            print(f"  {f}")
        return 1
    print(f"\nPASS - {len(manifest['modules'])} modules, {len(pools)} pools, "
          f"{len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
