#!/usr/bin/env python3
"""[SYSTEM REPORT] Final authoritative OWS-003 heavy-rebuild geometry.

`build_003()` reproduces the Gate-B r7 intact Cold-Chain Culture Nursery, the
Gate-C r3 approved D1/D3 history, and restrained Pass-19 microdetail. This module
is side-effect-free and imports no review/rendering machinery. Production Old
World generation and Gate D must consume this exact builder.
"""
from __future__ import annotations

import generate_wasteland_sites as base

PROOF_LOOT_TABLE = "infinite_domain:chests/old_world/ows_003_vcf_cold_chain_culture_nursery"
PROOF_POS = (53, 2, 12)
AIR = {"minecraft:air", "minecraft:cave_air", "minecraft:void_air", "minecraft:structure_void"}


def _block_name(t: base.Template, x: int, y: int, z: int) -> str:
    row = t.blocks.get((x, y, z))
    if row is None:
        return "minecraft:air"
    state, _ = row
    return t.palette[state]["Name"]


def _door(t: base.Template, x: int, y: int, z: int, facing: str, *, material: str = "iron", hinge: str = "left") -> None:
    base.door(t, x, y, z, facing=facing, material=material, hinge=hinge)


def _assert_clear(t: base.Template, a: tuple[int, int, int], b: tuple[int, int, int], label: str) -> None:
    for x in range(min(a[0], b[0]), max(a[0], b[0]) + 1):
        for y in range(min(a[1], b[1]), max(a[1], b[1]) + 1):
            for z in range(min(a[2], b[2]), max(a[2], b[2]) + 1):
                name = _block_name(t, x, y, z)
                if name not in AIR:
                    raise AssertionError(f"{label} obstructed at {(x, y, z)} by {name}")


def _assert_door(t: base.Template, x: int, y: int, z: int, label: str, *, block_name: str = "minecraft:iron_door") -> None:
    for yy in (y, y + 1):
        actual = _block_name(t, x, yy, z)
        if actual != block_name:
            raise AssertionError(f"{label} missing {block_name} at {(x, yy, z)}; found {actual}")


def _assert_block(t: base.Template, x: int, y: int, z: int, name: str, label: str) -> None:
    actual = _block_name(t, x, y, z)
    if actual != name:
        raise AssertionError(f"{label} expected {name} at {(x, y, z)}; found {actual}")


def _count(t: base.Template, name: str) -> int:
    return sum(1 for pos in t.blocks if _block_name(t, *pos) == name)


def _sign_on_wall(t: base.Template, wall_x: int, wall_y: int, wall_z: int, facing: str, *lines: str) -> None:
    offsets = {"north": (0, 0, -1), "south": (0, 0, 1), "west": (-1, 0, 0), "east": (1, 0, 0)}
    if facing not in offsets:
        raise ValueError(f"Unsupported sign facing: {facing}")
    if _block_name(t, wall_x, wall_y, wall_z) in AIR:
        raise AssertionError(f"Cannot mount {' / '.join(lines)}: support is air at {(wall_x, wall_y, wall_z)}")
    dx, dy, dz = offsets[facing]
    sx, sy, sz = wall_x + dx, wall_y + dy, wall_z + dz
    if _block_name(t, sx, sy, sz) not in AIR:
        raise AssertionError(f"Cannot mount {' / '.join(lines)} at {(sx, sy, sz)}")
    base.wall_sign(t, sx, sy, sz, facing, *lines)


def _light(t: base.Template, x: int, y: int, z: int) -> None:
    t.set(x, y, z, "minecraft:sea_lantern")


# ---------------------------------------------------------------------------
# Gate-A approved adaptive-reuse massing.
# ---------------------------------------------------------------------------

def _orchard_context(t: base.Template) -> None:
    for x in (5, 10, 15, 20):
        for z in (10, 17, 24, 31, 38, 45):
            t.fill((x, 1, z), (x, 4, z), "minecraft:oak_log", axis="y")
            t.fill((x - 2, 4, z - 2), (x + 2, 6, z + 2), "minecraft:oak_leaves", persistent="true")
    t.fill((21, 0, 8), (23, 0, 45), "minecraft:coarse_dirt")


def _front_admin_massing(t: base.Template) -> None:
    base.shell(t, (24, 1, 5), (55, 9, 18), "minecraft:bricks", "minecraft:polished_andesite", "minecraft:smooth_stone")
    t.fill((31, 2, 4), (48, 7, 4), "minecraft:white_concrete")
    t.fill((35, 3, 3), (44, 6, 3), "create:framed_glass")
    t.clear((39, 2, 3), (40, 5, 4))
    t.fill((34, 8, 4), (46, 9, 4), "minecraft:white_concrete")
    t.fill((37, 9, 3), (43, 11, 3), "minecraft:lime_concrete")
    t.fill((34, 8, 1), (46, 8, 4), "minecraft:white_concrete")
    for x in (34, 46):
        t.fill((x, 1, 2), (x, 7, 2), "minecraft:light_gray_concrete")


def _main_cold_hall_massing(t: base.Template) -> None:
    base.shell(t, (24, 1, 17), (55, 17, 43), "minecraft:bricks", "tfmg:factory_floor", "minecraft:smooth_stone")
    for z in (20, 26, 32, 38, 43):
        t.fill((23, 1, z), (23, 16, z), "minecraft:light_gray_concrete")
        t.fill((56, 1, z), (56, 16, z), "minecraft:light_gray_concrete")
    for x in (28, 35, 42, 49, 55):
        t.fill((x, 1, 16), (x, 16, 16), "minecraft:light_gray_concrete")
        t.fill((x, 1, 44), (x, 16, 44), "minecraft:light_gray_concrete")
    for x1, x2 in ((28, 30), (37, 39), (46, 48)):
        t.fill((x1, 17, 20), (x2, 17, 39), "create:framed_glass")
        t.fill((x1 - 1, 17, 20), (x1 - 1, 18, 39), "tfmg:steel_block")
        t.fill((x2 + 1, 17, 20), (x2 + 1, 18, 39), "tfmg:steel_block")
    t.fill((31, 13, 16), (39, 14, 16), "minecraft:white_concrete")
    t.fill((40, 13, 16), (48, 14, 16), "minecraft:lime_concrete")


def _east_receiving_massing(t: base.Template) -> None:
    t.fill((55, 0, 20), (58, 0, 31), "tfmg:factory_floor")
    t.fill((55, 2, 21), (55, 8, 30), "minecraft:white_concrete")
    t.clear((55, 2, 23), (55, 6, 27))
    for z in (21, 30):
        t.fill((57, 1, z), (57, 8, z), "tfmg:steel_block")
    t.fill((57, 8, 21), (57, 8, 30), "tfmg:steel_block")
    t.fill((55, 8, 21), (58, 8, 30), "minecraft:light_gray_concrete")
    t.fill((56, 2, 21), (56, 7, 21), "minecraft:light_blue_concrete")


def _south_dispatch_massing(t: base.Template) -> None:
    t.fill((39, 0, 43), (56, 0, 50), "tfmg:asphalt")
    t.clear((44, 2, 43), (49, 6, 44))
    t.fill((42, 8, 42), (52, 8, 48), "minecraft:light_gray_concrete")
    for x in (42, 52):
        t.fill((x, 1, 47), (x, 8, 47), "tfmg:steel_block")
    t.fill((42, 9, 44), (52, 9, 44), "tfmg:steel_block")
    t.fill((44, 0, 44), (49, 0, 50), "minecraft:yellow_concrete")


def _roof_plant_massing(t: base.Template) -> None:
    t.fill((32, 18, 24), (49, 18, 37), "minecraft:smooth_stone")
    for a, b in (
        ((33, 19, 25), (36, 21, 29)),
        ((38, 19, 25), (41, 22, 29)),
        ((33, 19, 32), (37, 21, 36)),
        ((40, 19, 32), (44, 22, 36)),
        ((46, 19, 27), (49, 21, 34)),
    ):
        t.fill(a, b, "immersiveengineering:sheetmetal_steel")
    t.fill((36, 19, 30), (48, 19, 30), "tfmg:steel_block")
    t.fill((45, 18, 30), (45, 20, 38), "tfmg:steel_block")
    base.shell(t, (50, 1, 31), (55, 20, 38), "minecraft:light_gray_concrete", "minecraft:smooth_stone", "minecraft:white_concrete")
    t.fill((51, 18, 30), (54, 20, 31), "minecraft:white_concrete")


def _build_massing() -> base.Template:
    t = base.Template((59, 24, 51))
    t.fill((1, 0, 1), (57, 0, 49), "minecraft:grass_block")
    t.fill((29, 0, 1), (50, 0, 7), "minecraft:smooth_stone")
    t.fill((55, 0, 20), (58, 0, 31), "tfmg:factory_floor")
    t.fill((39, 0, 43), (56, 0, 50), "tfmg:asphalt")
    _orchard_context(t)
    _front_admin_massing(t)
    _main_cold_hall_massing(t)
    _east_receiving_massing(t)
    _south_dispatch_massing(t)
    _roof_plant_massing(t)
    return t


# ---------------------------------------------------------------------------
# Gate-B r7 intact operating building.
# ---------------------------------------------------------------------------

def _build_admin_and_records(t: base.Template) -> None:
    t.clear((25, 2, 6), (54, 8, 16))
    t.fill((25, 1, 6), (54, 1, 16), "minecraft:polished_andesite")
    t.fill((31, 2, 4), (48, 7, 4), "minecraft:white_concrete")
    t.fill((35, 3, 3), (44, 6, 3), "create:framed_glass")
    t.clear((39, 2, 3), (40, 5, 5))
    _door(t, 39, 2, 4, "south", material="dark_oak", hinge="left")
    _door(t, 40, 2, 4, "south", material="dark_oak", hinge="right")
    t.fill((35, 2, 6), (35, 7, 16), "minecraft:bricks")
    t.clear((35, 2, 10), (35, 4, 10)); _door(t, 35, 2, 10, "east")
    t.fill((43, 2, 6), (43, 7, 16), "minecraft:white_concrete")
    t.clear((43, 2, 10), (43, 4, 10)); _door(t, 43, 2, 10, "west")
    t.fill((26, 2, 8), (32, 2, 9), "zvhouses:stone_brick_countertop")
    t.set(27, 3, 8, "the_wasteland_reworked:radio")
    t.fill((26, 2, 13), (31, 3, 14), "minecraft:barrel")
    t.fill((44, 2, 8), (52, 2, 9), "zvhouses:stone_brick_countertop")
    t.set(45, 3, 8, "minecraft:lectern")
    t.set(47, 3, 8, "create:depot")
    t.set(51, 3, 8, "the_wasteland_reworked:radio")
    t.fill((46, 2, 13), (53, 4, 15), "minecraft:bookshelf")
    t.set(49, 2, 12, "minecraft:lectern")
    t.clear((37, 2, 17), (38, 4, 17))
    _door(t, 37, 2, 17, "north", hinge="left"); _door(t, 38, 2, 17, "north", hinge="right")
    t.clear((50, 2, 17), (50, 4, 17)); _door(t, 50, 2, 17, "north")


def _build_hall_structure(t: base.Template) -> None:
    t.clear((25, 2, 18), (54, 16, 42))
    t.fill((25, 1, 18), (54, 1, 42), "tfmg:factory_floor")
    for z in (20, 26, 32, 38):
        for x in (25, 31, 37, 43, 49, 54):
            t.fill((x, 2, z), (x, 15, z), "tfmg:steel_block")
        t.fill((25, 15, z), (54, 15, z), "tfmg:steel_block")
    for x1, x2 in ((28, 30), (37, 39), (46, 48)):
        t.fill((x1, 17, 20), (x2, 17, 39), "create:framed_glass")
        for z in (20, 26, 32, 38):
            t.fill((x1 - 1, 16, z), (x2 + 1, 16, z), "tfmg:steel_block")


def _build_cold_vault(t: base.Template) -> None:
    t.fill((25, 1, 19), (35, 1, 35), "minecraft:light_gray_concrete")
    t.fill((35, 2, 19), (35, 8, 35), "minecraft:white_concrete")
    t.fill((25, 2, 19), (35, 8, 19), "minecraft:white_concrete")
    t.fill((25, 2, 35), (35, 8, 35), "minecraft:white_concrete")
    for z in (22, 31):
        t.clear((35, 2, z), (35, 4, z)); _door(t, 35, 2, z, "east")
    t.fill((35, 3, 24), (35, 5, 28), "create:framed_glass")
    t.fill((26, 2, 20), (28, 2, 34), "oritech:cooler_block")
    t.fill((32, 2, 20), (34, 2, 34), "oritech:cooler_block")
    for z in (21, 25, 29, 33):
        t.fill((26, 3, z), (28, 3, z), "immersiveengineering:crate")
        t.fill((32, 3, z), (34, 3, z), "minecraft:barrel")
    t.fill((26, 4, 20), (28, 4, 20), "minecraft:lime_concrete")
    t.fill((32, 4, 20), (34, 4, 20), "minecraft:light_blue_concrete")


def _build_nursery_cells(t: base.Template) -> None:
    t.fill((39, 2, 21), (39, 8, 36), "minecraft:white_concrete")
    for z in (21, 26, 31, 36):
        t.fill((39, 2, z), (47, 8, z), "minecraft:white_concrete")
    for z in (23, 28, 33):
        t.clear((39, 2, z), (39, 4, z)); _door(t, 39, 2, z, "east")
        t.fill((39, 3, z - 1), (39, 5, z - 1), "create:framed_glass")
        t.fill((39, 3, z + 1), (39, 5, z + 1), "create:framed_glass")
    for z1, z2 in ((22, 25), (27, 30), (32, 35)):
        t.fill((45, 2, z1), (47, 2, z2), "oritech:cooler_block")
        t.fill((41, 2, z1 + 1), (42, 3, z1 + 2), "immersiveengineering:crate")


def _build_receiving_quality_and_outbound(t: base.Template) -> None:
    t.fill((48, 1, 18), (54, 1, 28), "minecraft:white_concrete")
    t.fill((48, 2, 18), (48, 7, 28), "minecraft:white_concrete")
    t.fill((48, 2, 18), (54, 7, 18), "minecraft:white_concrete")
    t.fill((48, 2, 28), (54, 7, 28), "minecraft:white_concrete")
    t.fill((55, 2, 21), (55, 8, 30), "minecraft:white_concrete")
    t.clear((55, 2, 23), (55, 5, 27))
    _door(t, 55, 2, 24, "west", hinge="left"); _door(t, 55, 2, 25, "west", hinge="right")
    t.fill((55, 6, 23), (55, 7, 27), "tfmg:steel_block")
    t.fill((49, 2, 19), (53, 2, 20), "zvhouses:stone_brick_countertop")
    t.set(50, 3, 19, "create:depot"); t.set(52, 3, 19, "minecraft:lectern")
    t.fill((49, 2, 21), (50, 2, 22), "oritech:cooler_block")
    t.fill((53, 2, 21), (54, 2, 22), "oritech:cooler_block")
    t.set(54, 3, 27, "jaffabricate:pallet_full")
    t.clear((48, 2, 22), (48, 4, 23))
    _door(t, 48, 2, 22, "west", hinge="left"); _door(t, 48, 2, 23, "west", hinge="right")
    t.fill((48, 1, 29), (54, 1, 31), "minecraft:yellow_concrete")
    t.fill((48, 2, 29), (48, 7, 31), "minecraft:white_concrete")
    t.clear((48, 2, 30), (48, 4, 30)); _door(t, 48, 2, 30, "west")
    t.fill((50, 2, 29), (54, 2, 29), "zvhouses:stone_brick_countertop")
    t.set(51, 3, 29, "oritech:cooler_block"); t.set(53, 3, 29, "immersiveengineering:crate"); t.set(54, 3, 30, "minecraft:barrel")
    t.fill((25, 1, 36), (35, 1, 42), "minecraft:white_concrete")
    t.fill((26, 2, 37), (33, 2, 38), "zvhouses:stone_brick_countertop")
    t.set(28, 3, 37, "create:depot"); t.set(31, 3, 37, "minecraft:lectern")
    t.fill((39, 1, 37), (47, 1, 42), "minecraft:light_gray_concrete")
    t.fill((40, 2, 38), (43, 2, 39), "zvhouses:stone_brick_countertop")
    t.fill((45, 2, 38), (47, 3, 39), "immersiveengineering:crate")
    t.set(41, 3, 41, "jaffabricate:pallet_full")
    t.fill((48, 1, 38), (54, 1, 42), "minecraft:light_blue_concrete")
    t.fill((49, 2, 39), (50, 2, 41), "oritech:cooler_block")
    t.fill((53, 2, 39), (54, 2, 41), "oritech:cooler_block")
    t.fill((24, 2, 43), (55, 16, 43), "minecraft:bricks")
    for x in (25, 31, 37, 43, 49, 54):
        t.fill((x, 2, 43), (x, 15, 43), "minecraft:light_gray_concrete")
    t.clear((44, 2, 43), (49, 5, 43))
    _door(t, 46, 2, 43, "north", hinge="left"); _door(t, 47, 2, 43, "north", hinge="right")
    t.fill((44, 6, 43), (49, 7, 43), "tfmg:steel_block")
    t.fill((44, 0, 44), (49, 0, 50), "minecraft:yellow_concrete")


def _add_process_boundaries(t: base.Template) -> None:
    t.fill((35, 2, 36), (35, 7, 42), "minecraft:white_concrete"); t.clear((35, 2, 40), (35, 4, 40)); _door(t, 35, 2, 40, "east")
    t.fill((39, 2, 37), (39, 7, 42), "minecraft:white_concrete"); t.clear((39, 2, 40), (39, 4, 40)); _door(t, 39, 2, 40, "east")
    t.fill((48, 2, 38), (48, 7, 42), "minecraft:white_concrete"); t.clear((48, 2, 40), (48, 4, 40)); _door(t, 48, 2, 40, "east")


def _build_operations_spine(t: base.Template) -> None:
    t.fill((36, 1, 18), (38, 1, 42), "minecraft:light_gray_concrete")
    t.clear((36, 2, 18), (38, 4, 42))


def _build_plant_and_maintenance(t: base.Template) -> None:
    for pos in ((34, 22, 27), (40, 23, 27), (35, 22, 34), (42, 23, 34), (48, 22, 30)):
        t.set(*pos, "oritech:cooler_block")
    t.fill((32, 18, 23), (49, 18, 23), "create:fluid_pipe")
    t.fill((45, 12, 23), (45, 18, 23), "create:fluid_pipe")
    t.fill((52, 12, 31), (52, 18, 31), "create:fluid_pipe")
    t.fill((28, 12, 23), (52, 12, 23), "create:fluid_pipe")
    t.fill((28, 12, 30), (52, 12, 30), "create:fluid_pipe")
    for x in (28, 34, 42, 47, 52):
        t.fill((x, 8, 23), (x, 12, 23), "create:fluid_pipe")
    for z in (23, 30):
        t.fill((34, 8, z), (34, 12, z), "create:fluid_pipe")
        t.fill((47, 8, z), (47, 12, z), "create:fluid_pipe")
    for x, z in ((30, 22), (30, 28), (30, 33), (37, 22), (37, 28), (37, 34), (43, 23), (43, 28), (43, 33), (51, 22), (51, 27), (30, 39), (43, 40), (51, 40)):
        _light(t, x, 14 if z < 36 else 8, z)
    t.clear((51, 2, 32), (54, 19, 37))
    t.fill((54, 2, 36), (54, 18, 36), "minecraft:ladder", facing="west", waterlogged="false")
    t.fill((51, 18, 32), (54, 18, 37), "minecraft:light_gray_concrete")
    t.set(54, 18, 36, "minecraft:ladder", facing="west", waterlogged="false")
    t.clear((50, 2, 36), (50, 4, 36)); _door(t, 50, 2, 36, "west")
    t.clear((50, 18, 35), (50, 19, 35)); _door(t, 50, 18, 35, "west")
    t.fill((45, 18, 35), (49, 18, 35), "tfmg:steel_block")


def _articulate_exterior(t: base.Template) -> None:
    for z1, z2 in ((21, 24), (27, 30), (33, 36)):
        t.fill((24, 10, z1), (24, 12, z2), "create:framed_glass")
    for z1, z2 in ((19, 21), (33, 35), (39, 41)):
        t.fill((55, 10, z1), (55, 12, z2), "create:framed_glass")
    for x1, x2 in ((26, 29), (32, 35), (40, 43), (50, 53)):
        t.fill((x1, 10, 43), (x2, 12, 43), "create:framed_glass")
    for z in (20, 26, 32, 38, 43):
        t.fill((23, 1, z), (23, 16, z), "minecraft:light_gray_concrete")
        t.fill((56, 1, z), (56, 16, z), "minecraft:light_gray_concrete")


def _repair_r3_to_r7(t: base.Template) -> None:
    # r3 maintenance-sign support.
    t.fill((50, 4, 36), (50, 8, 36), "minecraft:light_gray_concrete")
    # r4 cold-vault transfer frames.
    for z in (26, 32):
        t.clear((31, 2, z), (31, 8, z))
        t.fill((25, 2, z), (25, 9, z), "tfmg:steel_block")
        t.fill((35, 2, z), (35, 9, z), "tfmg:steel_block")
        t.fill((25, 9, z), (35, 9, z), "tfmg:steel_block")
    # r5 nursery support stock moved onto east equipment banks.
    for z1 in (22, 27, 32):
        t.clear((41, 2, z1 + 1), (42, 3, z1 + 2))
        t.fill((45, 3, z1 + 1), (46, 4, z1 + 2), "immersiveengineering:crate")
    # r6 receiving frame transfer.
    t.clear((49, 2, 26), (49, 7, 26))
    t.fill((48, 8, 26), (55, 8, 26), "tfmg:steel_block")
    t.fill((48, 2, 26), (48, 8, 26), "tfmg:steel_block")
    t.fill((55, 2, 26), (55, 8, 26), "tfmg:steel_block")
    # r7 nursery-3 frame transfer.
    t.clear((43, 2, 32), (43, 8, 32))
    t.fill((39, 9, 32), (47, 9, 32), "tfmg:steel_block")
    t.fill((39, 2, 32), (39, 9, 32), "tfmg:steel_block")
    t.fill((47, 2, 32), (47, 9, 32), "tfmg:steel_block")


def _add_identity(t: base.Template) -> None:
    _sign_on_wall(t, 32, 6, 4, "north", "VERDANT", "CONTINUUM", "FOODS")
    _sign_on_wall(t, 46, 6, 4, "north", "COLD-CHAIN", "CULTURE", "NURSERY")
    _sign_on_wall(t, 55, 7, 22, "east", "RECEIVING", "COLD CHAIN")
    _sign_on_wall(t, 54, 7, 43, "south", "OUTBOUND", "CULTURES")
    _sign_on_wall(t, 43, 6, 8, "west", "BATCH", "REGISTRATION")
    _sign_on_wall(t, 43, 6, 13, "west", "LICENSE", "ROUTING")
    _sign_on_wall(t, 35, 6, 14, "east", "AUTHORIZED", "OPERATIONS")
    _sign_on_wall(t, 48, 6, 19, "east", "CONDITION", "CHECK")
    _sign_on_wall(t, 48, 6, 27, "east", "RECEIVING", "HOLD / PRE-COOL")
    _sign_on_wall(t, 35, 6, 20, "east", "COLD VAULT", "A")
    _sign_on_wall(t, 39, 6, 22, "west", "DORMANCY", "NURSERY 1")
    _sign_on_wall(t, 39, 6, 27, "west", "DORMANCY", "NURSERY 2")
    _sign_on_wall(t, 39, 6, 32, "west", "DORMANCY", "NURSERY 3")
    _sign_on_wall(t, 48, 6, 29, "west", "QUALITY HOLD", "SEAL INSPECTION")
    _sign_on_wall(t, 35, 6, 38, "east", "RELEASE", "INSPECTION")
    _sign_on_wall(t, 39, 6, 38, "west", "CONDITIONED", "PACKING")
    _sign_on_wall(t, 48, 6, 39, "west", "OUTBOUND", "COLD STAGING")
    _sign_on_wall(t, 50, 6, 36, "west", "PLANT ACCESS", "STAFF ONLY")


def _build_d0() -> base.Template:
    t = _build_massing()
    _build_admin_and_records(t)
    _build_hall_structure(t)
    _build_cold_vault(t)
    _build_nursery_cells(t)
    _build_receiving_quality_and_outbound(t)
    _add_process_boundaries(t)
    _build_operations_spine(t)
    _build_plant_and_maintenance(t)
    _articulate_exterior(t)
    _repair_r3_to_r7(t)
    _add_identity(t)
    return t


# ---------------------------------------------------------------------------
# Gate-C accepted chronology.
# ---------------------------------------------------------------------------

def _apply_d1(t: base.Template) -> None:
    t.fill((45, 1, 32), (47, 1, 35), "minecraft:yellow_concrete")
    t.set(47, 2, 34, "minecraft:yellow_concrete")
    t.set(47, 8, 30, "minecraft:yellow_concrete")
    t.set(50, 2, 31, "immersiveengineering:crate")
    t.set(53, 2, 31, "minecraft:barrel")
    t.set(52, 3, 30, "minecraft:yellow_concrete")
    t.set(49, 3, 30, "immersiveengineering:crate")
    t.set(54, 2, 31, "minecraft:barrel")


def _apply_d3_r1(t: base.Template) -> None:
    t.clear((40, 19, 32), (44, 22, 36))
    t.clear((45, 16, 23), (45, 18, 23))
    t.clear((42, 18, 23), (46, 18, 23))
    t.set(42, 18, 34, "minecraft:gravel")
    t.set(44, 18, 35, "minecraft:cobweb")
    t.clear((46, 17, 32), (48, 17, 36))
    t.clear((37, 17, 34), (39, 17, 37))
    for pos in ((47, 16, 34), (38, 16, 36), (45, 16, 35)):
        t.set(*pos, "minecraft:cobweb")
    t.fill((44, 1, 33), (47, 1, 36), "minecraft:mossy_stone_bricks")
    t.fill((32, 1, 33), (35, 1, 35), "minecraft:cracked_stone_bricks")
    t.set(46, 2, 36, "minecraft:gravel")
    t.clear((44, 5, 36), (47, 7, 36))
    t.clear((39, 5, 34), (39, 7, 35))
    t.set(46, 3, 34, "minecraft:cobweb")
    t.clear((55, 6, 26), (55, 7, 28))
    t.set(57, 0, 27, "minecraft:gravel")
    t.set(58, 0, 28, "minecraft:coarse_dirt")
    t.set(54, 2, 30, "minecraft:gravel")
    t.set(53, 2, 30, "minecraft:cobweb")
    t.clear((50, 8, 45), (52, 8, 48))
    t.fill((50, 0, 46), (54, 0, 50), "minecraft:gravel")
    t.set(52, 1, 47, "minecraft:coarse_dirt")
    t.clear((35, 5, 3), (36, 6, 3))
    for x, z in ((5, 45), (15, 31), (20, 17)):
        t.clear((x - 2, 4, z - 2), (x + 2, 6, z + 2))
        t.clear((x, 2, z), (x, 4, z))
        t.set(x, 1, z, "minecraft:coarse_dirt")
        t.set(x + 1, 1, z, "minecraft:dead_bush")
    t.spawner(52, 2, 30, "minecraft:zombie", count=1, nearby=4)
    t.spawner(51, 2, 40, "minecraft:spider", count=1, nearby=3)
    t.set(PROOF_POS[0], PROOF_POS[1] + 1, PROOF_POS[2], "minecraft:air")
    t.chest(*PROOF_POS, PROOF_LOOT_TABLE, facing="west")


def _apply_d3_r3(t: base.Template) -> None:
    # East receiving upper-service facade and exposed ground.
    t.clear((55, 9, 27), (55, 12, 29))
    t.fill((55, 8, 26), (55, 8, 30), "minecraft:cracked_stone_bricks")
    t.set(55, 7, 29, "minecraft:mossy_stone_bricks")
    t.set(56, 1, 29, "minecraft:gravel")
    t.set(57, 1, 30, "minecraft:coarse_dirt")
    # South dispatch canopy / upper logistics edge.
    t.clear((49, 6, 43), (52, 8, 43))
    t.clear((50, 8, 44), (52, 8, 47))
    t.fill((48, 5, 43), (48, 8, 43), "minecraft:cracked_stone_bricks")
    t.set(53, 6, 43, "minecraft:mossy_stone_bricks")
    t.fill((49, 1, 39), (53, 1, 42), "minecraft:cracked_stone_bricks")
    # Refrigeration service deck / edge failures.
    t.clear((32, 18, 24), (35, 18, 26))
    t.clear((36, 19, 30), (39, 19, 30))
    t.clear((45, 18, 31), (45, 20, 34))
    t.set(34, 17, 25, "minecraft:gravel")
    t.set(35, 17, 26, "minecraft:mossy_stone_bricks")
    t.set(45, 17, 33, "minecraft:cobweb")
    # Additional roof-light wet-zone failures.
    t.clear((28, 17, 25), (30, 17, 29))
    t.clear((37, 17, 22), (39, 17, 24))
    # Wet service masonry/floors below those failures.
    for y in range(9, 13):
        t.set(56, y, 32, "minecraft:cracked_stone_bricks")
        if y in (10, 11):
            t.set(56, y, 38, "minecraft:mossy_stone_bricks")
    t.clear((56, 12, 33), (56, 14, 35))
    t.fill((39, 1, 34), (43, 1, 37), "minecraft:mossy_stone_bricks")
    t.fill((28, 1, 24), (31, 1, 29), "minecraft:cracked_stone_bricks")
    t.clear((41, 10, 43), (43, 12, 43))
    t.set(40, 10, 43, "minecraft:cracked_stone_bricks")
    t.set(44, 11, 43, "minecraft:mossy_stone_bricks")


def _apply_microdetail(t: base.Template) -> None:
    # Pass-19 additions stay off all protected routes and reinforce existing work.
    t.set(49, 2, 37, "immersiveengineering:crate")
    t.set(52, 2, 37, "minecraft:barrel")
    t.set(33, 3, 38, "minecraft:lantern")
    t.set(44, 3, 39, "minecraft:barrel")
    t.set(57, 1, 28, "minecraft:gravel")
    t.set(46, 16, 33, "minecraft:cobweb")


# ---------------------------------------------------------------------------
# Final shipping invariants.
# ---------------------------------------------------------------------------

def _assert_proof(t: base.Template) -> None:
    row = t.blocks.get(PROOF_POS)
    if row is None:
        raise AssertionError("OWS-003 proof chest is missing")
    state_id, nbt = row
    if t.palette[state_id]["Name"] != "minecraft:chest":
        raise AssertionError("OWS-003 proof coordinate is not a chest")
    if not nbt or nbt.get("LootTable") != PROOF_LOOT_TABLE:
        raise AssertionError("OWS-003 proof chest loot table drifted")
    if _block_name(t, PROOF_POS[0], PROOF_POS[1] + 1, PROOF_POS[2]) not in AIR:
        raise AssertionError("OWS-003 proof chest is not openable")
    matches = sum(1 for _, (_, nbt_row) in t.blocks.items() if nbt_row and nbt_row.get("LootTable") == PROOF_LOOT_TABLE)
    if matches != 1:
        raise AssertionError(f"OWS-003 requires exactly one canonical proof chest; found {matches}")


def _assert_final(t: base.Template) -> None:
    if tuple(t.size) != (59, 24, 51):
        raise AssertionError(f"OWS-003 final dimensions changed: {t.size}")
    _assert_door(t, 39, 2, 4, "front staff west leaf", block_name="minecraft:dark_oak_door")
    _assert_door(t, 40, 2, 4, "front staff east leaf", block_name="minecraft:dark_oak_door")
    _assert_door(t, 43, 2, 10, "batch/licensing office door")
    _assert_door(t, 55, 2, 24, "receiving west leaf")
    _assert_door(t, 55, 2, 25, "receiving east leaf")
    _assert_door(t, 46, 2, 43, "dispatch west leaf")
    _assert_door(t, 47, 2, 43, "dispatch east leaf")
    _assert_clear(t, (44, 2, 11), (53, 3, 11), "batch/licensing office aisle")
    _assert_clear(t, (50, 2, 12), (52, 3, 12), "proof-chest final approach")
    _assert_clear(t, (36, 2, 18), (38, 4, 42), "conditioned operations spine")
    _assert_clear(t, (29, 2, 21), (31, 4, 33), "cold-vault center aisle")
    _assert_clear(t, (40, 2, 22), (44, 4, 25), "nursery-1 service area")
    _assert_clear(t, (40, 2, 27), (44, 4, 30), "nursery-2 service area")
    _assert_clear(t, (49, 2, 23), (53, 4, 27), "receiving freight lane")
    _assert_clear(t, (44, 2, 40), (47, 4, 42), "packing-to-dispatch transfer")
    _assert_block(t, 54, 18, 36, "minecraft:ladder", "maintenance ladder top")
    for pos, label in (
        ((32, 6, 3), "VCF corporate identity"),
        ((46, 6, 3), "facility identity"),
        ((56, 7, 22), "receiving identity"),
        ((54, 7, 44), "dispatch identity"),
    ):
        _assert_block(t, *pos, "minecraft:oak_wall_sign", label)
    if _count(t, "minecraft:oak_wall_sign") < 12:
        raise AssertionError("OWS-003 lost too much operational wayfinding")
    if _count(t, "oritech:cooler_block") < 90:
        raise AssertionError("OWS-003 lost too much surviving cold-chain equipment")
    if _count(t, "create:fluid_pipe") < 55:
        raise AssertionError("OWS-003 lost too much surviving refrigeration/service piping")
    if _count(t, "minecraft:spawner") != 2:
        raise AssertionError("OWS-003 final D3 must contain exactly two optional spawners")
    _assert_proof(t)


def build_003() -> base.Template:
    t = _build_d0()
    _apply_d1(t)
    _apply_d3_r1(t)
    _apply_d3_r3(t)
    _apply_microdetail(t)
    _assert_final(t)
    return t
