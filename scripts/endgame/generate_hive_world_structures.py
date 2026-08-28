#!/usr/bin/env python3
"""Authoritative generator for the Hive World jigsaw district.

Endgame: advances Phase 4 (modular architectural grammar) at spike scale, by owner
direction ("actual structure ... a functional and useful place"). The real module
schema, connector validator, and per-band families are C0051-C0068.
Authority: docs/Endgame.md §2.7 (structures own legibility), §2.2 (compression/release).

Emits (do not hand-edit):
  kubejs/data/infinite_domain/structure/hive_world/*.nbt          (7 modules)
  kubejs/data/infinite_domain/worldgen/template_pool/hive_world/*.json
  kubejs/data/infinite_domain/worldgen/structure/hive_world_district.json
  kubejs/data/infinite_domain/worldgen/structure_set/hive_world_district.json
  kubejs/data/infinite_domain/loot_table/chests/hive_world_salvage.json

Topology: transit_hub (start) -> 4 connectors draw from the `branch` pool
{corridor, corridor_bend, habitation_cell, industrial_bay, stair_shaft}, fallback
`terminal` {bulkhead}. Corridors, bays and stairs re-draw from `branch`; rooms are
leaves. The assembly stamps a connected room-and-corridor network into the solid
mass (generate_hive_world_density.py).
"""
from __future__ import annotations

import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))
import generate_wasteland_sites as base  # noqa: E402

DATA = REPO / "kubejs/data/infinite_domain"
MANIFEST = REPO / "docs/endgame/hive-world-module-manifest.json"

# module id -> (band, role) per docs/endgame/contracts/module-schema.md §4
MODULE_META = {
    "transit_hub": ("any", "start"),
    "corridor": ("any", "branch"),
    "corridor_bend": ("any", "branch"),
    "habitation_cell": ("any", "leaf"),
    "industrial_bay": ("any", "branch"),
    "stair_shaft": ("any", "transition"),
    "bulkhead": ("any", "terminal"),
}
_ORIENT_FACING = {"north_up": "north", "south_up": "south", "east_up": "east", "west_up": "west"}
CAT = "hive_world"
DOOR = "infinite_domain:hive_world/door"
BRANCH = "infinite_domain:hive_world/branch"
TERMINAL = "infinite_domain:hive_world/terminal"

BRICK = "minecraft:polished_blackstone_bricks"
FLOOR = "minecraft:blackstone"
TRIM = "minecraft:polished_blackstone"
DEEP = "minecraft:deepslate_tiles"
LIGHT = "minecraft:sea_lantern"


def _jig(t, x, y, z, *, name, target, pool, orientation, final_state="minecraft:air"):
    t.set(x, y, z, "minecraft:jigsaw", {
        "id": "minecraft:jigsaw", "name": name, "target": target,
        "pool": pool, "final_state": final_state, "joint": "aligned",
    }, orientation=orientation)


def _room_shell(t, sx, sy, sz):
    t.fill((0, 0, 0), (sx - 1, 0, sz - 1), FLOOR)
    t.fill((0, 1, 0), (sx - 1, sy - 2, sz - 1), BRICK)
    t.clear((1, 1, 1), (sx - 2, sy - 3, sz - 2))
    t.fill((0, sy - 1, 0), (sx - 1, sy - 1, sz - 1), TRIM)


def _door_gap(t, x, z, *, sy=3):
    for y in range(1, 1 + sy):
        t.set(x, y, z, "minecraft:air")


def _write(name, t):
    blocks = []
    for pos, (state, nbt) in sorted(t.blocks.items(), key=lambda r: (r[0][1], r[0][2], r[0][0])):
        entry = {"pos": base.NbtList(base.TAG_INT, list(pos)), "state": state}
        if nbt:
            entry["nbt"] = nbt
        blocks.append(entry)
    root = {
        "DataVersion": base.DATA_VERSION,
        "size": base.NbtList(base.TAG_INT, list(t.size)),
        "palette": base.NbtList(base.TAG_COMPOUND, t.palette),
        "blocks": base.NbtList(base.TAG_COMPOUND, blocks),
        "entities": base.NbtList(base.TAG_COMPOUND, t.entities),
    }
    base.write_nbt(DATA / "structure" / CAT / f"{name}.nbt", root)

    band, role = MODULE_META[name]
    connectors = []
    non_air = 0
    block_entities = 0
    for pos, (state, nbt) in t.blocks.items():
        entry = t.palette[state]
        if entry["Name"] != "minecraft:air":
            non_air += 1
        if nbt and "id" in nbt and entry["Name"] != "minecraft:jigsaw":
            block_entities += 1
        if entry["Name"] == "minecraft:jigsaw" and nbt:
            orient = entry.get("Properties", {}).get("orientation", "north_up")
            ctype = nbt["name"].split("/")[-1]
            connectors.append({
                "type": ctype,
                "local_pos": list(pos),
                "facing": _ORIENT_FACING.get(orient, orient),
                "pool": nbt["pool"],
                "final_state": nbt["final_state"],
            })
    floor_data = sorted({c["local_pos"][1] for c in connectors}) or [1]
    return {
        "id": f"infinite_domain:{CAT}/{name}",
        "nbt": f"kubejs/data/infinite_domain/structure/{CAT}/{name}.nbt",
        "size": list(t.size),
        "band": band,
        "role": role,
        "floor_data": floor_data,
        "non_air": non_air,
        "block_entities": block_entities,
        "connectors": sorted(connectors, key=lambda c: c["local_pos"]),
    }


# --- modules -----------------------------------------------------------------

def transit_hub():
    t = base.Template((13, 9, 13))
    _room_shell(t, 13, 9, 13)
    t.fill((5, 1, 5), (7, 1, 7), TRIM)
    t.set(6, 2, 6, "minecraft:lodestone")
    for x, z in ((2, 2), (10, 2), (2, 10), (10, 10)):
        t.set(x, 6, z, LIGHT)
    for x, z in ((6, 3), (6, 9), (3, 6), (9, 6)):
        t.set(x, 7, z, "minecraft:chain")
    conns = [(6, 0, "north_up"), (6, 12, "south_up")]
    for x, z, o in conns:
        _door_gap(t, x, z)
        _jig(t, x, 1, z, name=DOOR, target=DOOR, pool=BRANCH, orientation=o)
    for z, o in [(6, "west_up"), (6, "east_up")]:
        gx = 0 if o == "west_up" else 12
        for y in range(1, 4):
            t.set(gx, y, z, "minecraft:air")
        _jig(t, gx, 1, z, name=DOOR, target=DOOR, pool=BRANCH, orientation=o)
    return t


def corridor():
    t = base.Template((5, 5, 11))
    _room_shell(t, 5, 5, 11)
    t.set(2, 3, 5, LIGHT)
    t.set(1, 1, 5, "minecraft:polished_blackstone_slab")
    t.set(3, 1, 5, "minecraft:polished_blackstone_slab")
    for z, o in ((0, "north_up"), (10, "south_up")):
        _door_gap(t, 2, z)
        _jig(t, 2, 1, z, name=DOOR, target=DOOR, pool=BRANCH, orientation=o)
    return t


def corridor_bend():
    t = base.Template((9, 5, 9))
    _room_shell(t, 9, 5, 9)
    t.set(4, 3, 4, LIGHT)
    # -Z entry and +X exit
    _door_gap(t, 4, 0)
    _jig(t, 4, 1, 0, name=DOOR, target=DOOR, pool=BRANCH, orientation="north_up")
    for y in range(1, 4):
        t.set(8, y, 4, "minecraft:air")
    _jig(t, 8, 1, 4, name=DOOR, target=DOOR, pool=BRANCH, orientation="east_up")
    return t


def habitation_cell():
    t = base.Template((9, 5, 9))
    _room_shell(t, 9, 5, 9)
    for z in (2, 4, 6):
        t.set(1, 1, z, "minecraft:polished_blackstone_slab")
        t.set(1, 2, z, "minecraft:polished_blackstone_slab")
        t.set(7, 1, z, "minecraft:polished_blackstone_slab")
    t.set(4, 3, 4, LIGHT)
    t.set(4, 1, 7, "minecraft:crafting_table")
    _door_gap(t, 4, 0)
    _jig(t, 4, 1, 0, name=DOOR, target=DOOR, pool="minecraft:empty", orientation="north_up")
    return t


def industrial_bay():
    t = base.Template((11, 9, 13))
    _room_shell(t, 11, 9, 13)
    t.fill((2, 1, 3), (3, 5, 5), DEEP)
    t.fill((7, 1, 7), (8, 6, 9), "minecraft:polished_deepslate")
    # catwalk railing, split so it never blocks the south doorway at x=5
    t.fill((1, 1, 10), (3, 1, 10), "minecraft:iron_bars")
    t.fill((7, 1, 10), (9, 1, 10), "minecraft:iron_bars")
    for x, z in ((2, 2), (8, 2), (2, 10), (8, 10)):
        t.set(x, 7, z, LIGHT)
    t.set(3, 6, 4, "minecraft:chain")
    t.chest(5, 1, 6, "infinite_domain:chests/hive_world_salvage", "north")
    for z, o in ((0, "north_up"), (12, "south_up")):
        _door_gap(t, 5, z)
        _jig(t, 5, 1, z, name=DOOR, target=DOOR, pool=BRANCH, orientation=o)
    return t


def stair_shaft():
    t = base.Template((7, 13, 7))
    t.fill((0, 0, 0), (6, 0, 6), FLOOR)
    t.fill((0, 1, 0), (6, 11, 6), BRICK)
    t.clear((1, 1, 1), (5, 10, 5))
    t.fill((0, 12, 0), (6, 12, 6), TRIM)
    for y in range(1, 11):
        t.set(3, y, 5, "minecraft:ladder", facing="south")
    for y in (2, 6, 10):
        t.set(1, y, 1, LIGHT)
    _door_gap(t, 3, 0)
    _jig(t, 3, 1, 0, name=DOOR, target=DOOR, pool=BRANCH, orientation="north_up")
    for y in range(9, 12):
        t.set(3, y, 6, "minecraft:air")
    _jig(t, 3, 9, 6, name=DOOR, target=DOOR, pool=BRANCH, orientation="south_up")
    return t


def bulkhead():
    t = base.Template((5, 5, 3))
    t.fill((0, 0, 0), (4, 4, 2), BRICK)
    t.set(2, 1, 0, TRIM)
    t.set(2, 2, 0, "minecraft:chiseled_polished_blackstone")
    t.set(2, 3, 0, TRIM)
    _jig(t, 2, 1, 0, name=DOOR, target=DOOR, pool="minecraft:empty",
         orientation="north_up", final_state="minecraft:chiseled_polished_blackstone")
    return t


MODULES = {
    "transit_hub": transit_hub, "corridor": corridor, "corridor_bend": corridor_bend,
    "habitation_cell": habitation_cell, "industrial_bay": industrial_bay,
    "stair_shaft": stair_shaft, "bulkhead": bulkhead,
}

POOLS = {
    "start": [("transit_hub", 1)],
    "branch": [("corridor", 4), ("corridor_bend", 3), ("habitation_cell", 3),
               ("industrial_bay", 2), ("stair_shaft", 2)],
    "terminal": [("bulkhead", 1)],
}
POOL_FALLBACK = {"start": "minecraft:empty", "branch": TERMINAL, "terminal": "minecraft:empty"}


def pool_json(name):
    return {
        "fallback": POOL_FALLBACK[name],
        "elements": [
            {"weight": w, "element": {
                "location": f"infinite_domain:{CAT}/{mod}",
                "processors": "minecraft:empty", "projection": "rigid",
                "element_type": "minecraft:single_pool_element",
            }}
            for mod, w in POOLS[name]
        ],
    }


LOOT = {
    "type": "minecraft:chest",
    "pools": [
        {"rolls": {"type": "minecraft:uniform", "min": 2, "max": 4}, "entries": [
            {"type": "minecraft:item", "weight": w, "name": item,
             "functions": [{"function": "minecraft:set_count",
                            "count": {"type": "minecraft:uniform", "min": lo, "max": hi}}]}
            for item, w, lo, hi in [
                ("minecraft:raw_iron", 10, 2, 8),
                ("minecraft:raw_copper", 10, 3, 10),
                ("minecraft:coal", 8, 3, 9),
                ("minecraft:redstone", 6, 2, 7),
                ("minecraft:amethyst_shard", 4, 1, 4),
                ("minecraft:lapis_lazuli", 4, 2, 6),
                ("minecraft:iron_block", 2, 1, 2),
            ]
        ]},
    ],
}

DISTRICT_BIOMES = [
    "infinite_domain:hive_world_sump",
    "infinite_domain:hive_world_works",
    "infinite_domain:hive_world_vault",
]


def main() -> int:
    entries = {name: _write(name, fn()) for name, fn in MODULES.items()}
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps({
        "$note": "Generated by scripts/endgame/generate_hive_world_structures.py. "
                 "Contract: docs/endgame/contracts/module-schema.md. "
                 "Validated by scripts/endgame/validate_hive_world_modules.py.",
        "version": "hive-world-module-manifest-v1",
        "pools": {
            n: {"fallback": POOL_FALLBACK[n],
                "elements": [{"module": m, "weight": w} for m, w in POOLS[n]]}
            for n in POOLS
        },
        "modules": [entries[n] for n in MODULES],
    }, indent=2) + "\n", encoding="utf-8")
    placed = {n: e["non_air"] for n, e in entries.items()}
    for name in POOLS:
        base.write_json(DATA / "worldgen/template_pool" / CAT / f"{name}.json", pool_json(name))
    base.write_json(DATA / "worldgen/structure/hive_world_district.json", {
        "type": "minecraft:jigsaw",
        "biomes": DISTRICT_BIOMES,
        "step": "underground_structures",
        "spawn_overrides": {},
        "terrain_adaptation": "none",
        "start_pool": f"infinite_domain:{CAT}/start",
        "size": 6,
        "start_height": {"type": "minecraft:uniform",
                         "min_inclusive": {"absolute": 96},
                         "max_inclusive": {"absolute": 351}},
        "max_distance_from_center": 96,
        "use_expansion_hack": False,
        "liquid_settings": "ignore_waterlogging",
    })
    base.write_json(DATA / "worldgen/structure_set/hive_world_district.json", {
        "structures": [{"structure": "infinite_domain:hive_world_district", "weight": 1}],
        "placement": {"type": "minecraft:random_spread", "spacing": 20, "separation": 8, "salt": 927133},
    })
    base.write_json(DATA / "loot_table/chests/hive_world_salvage.json", LOOT)
    print(f"wrote {len(MODULES)} modules {placed}, {len(POOLS)} pools, 1 structure + set + loot table")
    return 0


if __name__ == "__main__":
    sys.exit(main())
