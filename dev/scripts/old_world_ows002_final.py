#!/usr/bin/env python3
"""[SYSTEM REPORT] Final authoritative OWS-002 heavy-rebuild geometry.

This module is side-effect-free. `build_002()` returns the Gate-C r2 approved D3
Emergency Community Grow Hall plus restrained Pass-19 microdetail. Production
Old World generation and Gate D must consume this exact builder so reviewed and
shipping geometry cannot drift apart.
"""
from __future__ import annotations

import generate_wasteland_sites as base

PROOF_LOOT_TABLE = "infinite_domain:chests/old_world/ows_002_vcf_emergency_community_grow_hall"
PROOF_POS = (23, 2, 14)
AIR = {"minecraft:air", "minecraft:cave_air", "minecraft:void_air", "minecraft:structure_void"}


def _block_name(t: base.Template, x: int, y: int, z: int) -> str:
    row = t.blocks.get((x, y, z))
    if row is None:
        return "minecraft:air"
    state, _ = row
    return t.palette[state]["Name"]


def _door(
    t: base.Template,
    x: int,
    y: int,
    z: int,
    facing: str,
    *,
    material: str = "iron",
    hinge: str = "left",
) -> None:
    base.door(t, x, y, z, facing=facing, material=material, hinge=hinge)


def _light(t: base.Template, x: int, y: int, z: int) -> None:
    t.set(x, y, z, "minecraft:sea_lantern")


def _assert_clear(t: base.Template, a: tuple[int, int, int], b: tuple[int, int, int], label: str) -> None:
    for x in range(min(a[0], b[0]), max(a[0], b[0]) + 1):
        for y in range(min(a[1], b[1]), max(a[1], b[1]) + 1):
            for z in range(min(a[2], b[2]), max(a[2], b[2]) + 1):
                name = _block_name(t, x, y, z)
                if name not in AIR:
                    raise AssertionError(f"{label} obstructed at {(x, y, z)} by {name}")


def _assert_door(
    t: base.Template,
    x: int,
    y: int,
    z: int,
    label: str,
    *,
    block_name: str = "minecraft:iron_door",
) -> None:
    for yy in (y, y + 1):
        name = _block_name(t, x, yy, z)
        if name != block_name:
            raise AssertionError(f"{label} missing {block_name} at {(x, yy, z)}; found {name}")


def _assert_block(t: base.Template, x: int, y: int, z: int, name: str, label: str) -> None:
    actual = _block_name(t, x, y, z)
    if actual != name:
        raise AssertionError(f"{label} expected {name} at {(x, y, z)}; found {actual}")


def _sign_on_wall(
    t: base.Template,
    wall_x: int,
    wall_y: int,
    wall_z: int,
    facing: str,
    *lines: str,
) -> None:
    offsets = {"north": (0, 0, -1), "south": (0, 0, 1), "west": (-1, 0, 0), "east": (1, 0, 0)}
    support = _block_name(t, wall_x, wall_y, wall_z)
    if support in AIR:
        raise AssertionError(f"Cannot mount {' / '.join(lines)}: support {(wall_x, wall_y, wall_z)} is {support}")
    dx, dy, dz = offsets[facing]
    sx, sy, sz = wall_x + dx, wall_y + dy, wall_z + dz
    occupied = _block_name(t, sx, sy, sz)
    if occupied not in AIR:
        raise AssertionError(f"Cannot mount {' / '.join(lines)} at {(sx, sy, sz)}: occupied by {occupied}")
    base.wall_sign(t, sx, sy, sz, facing, *lines)


def _rack_bank(t: base.Template, x1: int, x2: int, *, z1: int = 18, z2: int = 30) -> None:
    for y in (2, 7):
        t.fill((x1, y, z1), (x2, y, z2), "farmersdelight:rich_soil")
        t.fill((x1, y + 1, z1), (x2, y + 1, z2), "minecraft:wheat", age="7")
    for x in (x1, x2):
        for z in (z1, 24, z2):
            t.fill((x, 2, z), (x, 6, z), "minecraft:scaffolding")
    t.fill((x1, 5, z2), (x2, 6, z2), "minecraft:scaffolding")


def _public_canopy(t: base.Template) -> None:
    t.fill((21, 7, 1), (29, 7, 5), "minecraft:white_concrete")
    for x in (21, 29):
        t.fill((x, 1, 2), (x, 6, 2), "minecraft:polished_blackstone_bricks")
    t.fill((22, 8, 4), (28, 9, 4), "minecraft:lime_concrete")
    t.fill((18, 8, 5), (19, 11, 5), "minecraft:yellow_concrete")


def _east_receiving(t: base.Template) -> None:
    t.fill((46, 0, 18), (50, 0, 31), "tfmg:factory_floor")
    t.fill((46, 2, 22), (46, 6, 28), "minecraft:gray_concrete")
    t.clear((46, 2, 24), (46, 5, 26))
    for z in (21, 29):
        t.fill((48, 1, z), (48, 7, z), "tfmg:steel_block")
    t.fill((48, 8, 21), (48, 8, 29), "tfmg:steel_block")
    t.fill((46, 7, 21), (50, 7, 29), "minecraft:light_gray_concrete")
    t.fill((47, 2, 21), (47, 6, 21), "minecraft:lime_concrete")


def _south_dispatch(t: base.Template) -> None:
    t.fill((23, 0, 41), (38, 0, 46), "tfmg:asphalt")
    t.clear((29, 2, 41), (32, 5, 41))
    t.fill((27, 7, 39), (35, 7, 45), "minecraft:light_gray_concrete")
    for x in (27, 35):
        t.fill((x, 1, 44), (x, 7, 44), "tfmg:steel_block")
    t.fill((27, 8, 42), (35, 8, 42), "tfmg:steel_block")
    t.fill((28, 8, 40), (34, 8, 40), "minecraft:yellow_concrete")


def _roof_service(t: base.Template) -> None:
    t.fill((10, 12, 32), (19, 12, 40), "minecraft:smooth_stone")
    for a, b in (
        ((10, 13, 33), (12, 15, 35)),
        ((14, 13, 33), (16, 16, 35)),
        ((11, 13, 37), (13, 15, 39)),
        ((16, 13, 37), (18, 16, 39)),
    ):
        t.fill(a, b, "immersiveengineering:sheetmetal_steel")
    t.fill((12, 13, 36), (17, 13, 36), "tfmg:steel_block")


def _build_massing() -> base.Template:
    t = base.Template((51, 21, 47))
    t.fill((1, 0, 1), (49, 0, 45), "minecraft:grass_block")
    t.fill((18, 0, 0), (32, 0, 7), "minecraft:smooth_stone")
    t.fill((3, 0, 7), (6, 0, 41), "minecraft:smooth_stone")
    t.fill((46, 0, 18), (50, 0, 31), "tfmg:factory_floor")
    t.fill((23, 0, 41), (38, 0, 46), "tfmg:asphalt")

    base.shell(t, (4, 1, 7), (21, 11, 41), "minecraft:mud_bricks", "tfmg:factory_floor", "minecraft:smooth_stone")
    base.shell(t, (18, 1, 7), (46, 12, 15), "minecraft:smooth_stone", "minecraft:polished_andesite", "minecraft:smooth_stone")
    base.shell(t, (22, 1, 15), (46, 18, 41), "minecraft:bricks", "minecraft:smooth_stone", "minecraft:weathered_cut_copper")
    base.shell(t, (18, 1, 4), (32, 8, 9), "minecraft:smooth_stone", "minecraft:polished_andesite", "minecraft:smooth_stone_slab")
    t.fill((20, 2, 4), (30, 5, 4), "create:framed_glass")
    t.clear((24, 2, 4), (25, 4, 4))
    _door(t, 24, 2, 4, "south", material="dark_oak", hinge="left")
    _door(t, 25, 2, 4, "south", material="dark_oak", hinge="right")
    for z1, z2 in ((11, 15), (20, 24), (31, 35)):
        t.fill((4, 3, z1), (4, 6, z2), "create:framed_glass")
    for x1, x2 in ((34, 38), (41, 45)):
        t.fill((x1, 4, 7), (x2, 7, 7), "create:framed_glass")
    t.fill((27, 18, 21), (40, 20, 34), "create:framed_glass")
    _public_canopy(t)
    _east_receiving(t)
    _south_dispatch(t)
    _roof_service(t)
    t.fill((44, 2, 38), (44, 18, 38), "minecraft:ladder", facing="west", waterlogged="false")
    t.set(44, 19, 38, "minecraft:iron_trapdoor", facing="north", half="bottom", open="false", powered="false", waterlogged="false")
    t.fill((25, 13, 14), (43, 14, 14), "minecraft:lime_concrete")
    return t


def _articulate_intact_exterior(t: base.Template) -> None:
    for x in (33, 40, 46):
        t.fill((x, 2, 7), (x, 10, 7), "minecraft:light_gray_concrete")
    t.fill((33, 9, 7), (45, 10, 7), "minecraft:lime_concrete")
    for x1, x2 in ((34, 38), (41, 45)):
        t.fill((x1, 4, 7), (x2, 7, 7), "create:framed_glass")

    for z in (18, 23, 31, 38):
        t.fill((46, 2, z), (46, 14, z), "minecraft:light_gray_concrete")
    for z1, z2 in ((19, 21), (24, 28), (32, 36)):
        t.fill((46, 8, z1), (46, 10, z2), "create:framed_glass")
    t.fill((46, 12, 18), (46, 13, 38), "minecraft:lime_concrete")
    for z in (18, 23, 31, 38):
        t.fill((46, 2, z), (46, 14, z), "minecraft:light_gray_concrete")

    for z in (23, 26):
        t.fill((46, 2, z), (46, 7, z), "minecraft:white_concrete")
    t.fill((46, 7, 23), (46, 7, 26), "tfmg:steel_block")
    t.fill((46, 5, 27), (46, 6, 28), "create:framed_glass")
    t.fill((47, 0, 24), (50, 0, 25), "minecraft:yellow_concrete")
    t.set(49, 1, 27, "jaffabricate:pallet_full")

    for x in (24, 27, 35, 40, 45):
        t.fill((x, 2, 41), (x, 14, 41), "minecraft:light_gray_concrete")
    for x1, x2 in ((25, 26), (36, 39), (41, 44)):
        t.fill((x1, 8, 41), (x2, 10, 41), "create:framed_glass")
    t.fill((28, 2, 41), (28, 6, 41), "minecraft:white_concrete")
    t.fill((33, 2, 41), (33, 6, 41), "minecraft:white_concrete")
    t.fill((28, 6, 41), (33, 7, 41), "tfmg:steel_block")
    t.fill((28, 9, 41), (34, 10, 41), "minecraft:lime_concrete")
    t.fill((29, 0, 41), (32, 0, 46), "minecraft:yellow_concrete")
    t.fill((24, 1, 43), (25, 2, 44), "immersiveengineering:crate")
    t.fill((36, 1, 43), (37, 2, 44), "immersiveengineering:crate")

    for z1, z2 in ((18, 21), (24, 28), (32, 35)):
        t.fill((22, 12, z1), (22, 14, z2), "create:framed_glass")
    t.fill((22, 15, 18), (22, 15, 38), "minecraft:lime_concrete")
    t.fill((18, 13, 36), (22, 13, 36), "create:fluid_pipe")
    t.fill((23, 11, 36), (23, 13, 36), "create:fluid_pipe")
    t.set(22, 13, 36, "create:fluid_pipe")


def _build_d0() -> base.Template:
    t = _build_massing()
    t.clear((19, 2, 5), (31, 7, 8))
    t.clear((19, 2, 8), (45, 11, 14))
    t.clear((5, 2, 8), (20, 10, 40))
    t.clear((23, 2, 16), (45, 17, 40))

    t.fill((20, 2, 4), (30, 5, 4), "create:framed_glass")
    t.clear((24, 2, 4), (25, 4, 4))
    _door(t, 24, 2, 4, "south", material="dark_oak", hinge="left")
    _door(t, 25, 2, 4, "south", material="dark_oak", hinge="right")
    t.fill((19, 1, 5), (31, 1, 13), "minecraft:polished_andesite")
    t.fill((24, 1, 5), (26, 1, 12), "minecraft:white_concrete")
    t.clear((24, 2, 5), (26, 4, 12))
    t.fill((19, 2, 11), (22, 2, 12), "zvhouses:stone_brick_countertop")
    t.set(20, 3, 11, "minecraft:lectern")
    t.fill((32, 2, 11), (38, 2, 12), "zvhouses:stone_brick_countertop")
    t.set(36, 3, 11, "create:depot")

    t.fill((18, 2, 13), (46, 6, 13), "minecraft:white_concrete")
    t.fill((19, 3, 13), (22, 5, 13), "create:framed_glass")
    t.fill((32, 3, 13), (38, 5, 13), "create:framed_glass")
    t.clear((28, 2, 13), (28, 4, 13))
    _door(t, 28, 2, 13, "north")
    t.fill((19, 1, 14), (24, 1, 14), "minecraft:light_gray_concrete")
    t.fill((19, 2, 14), (22, 2, 14), "zvhouses:stone_brick_countertop")
    t.set(20, 3, 14, "minecraft:bookshelf")
    t.set(22, 3, 14, "the_wasteland_reworked:radio")
    t.fill((38, 1, 14), (44, 1, 14), "minecraft:light_gray_concrete")
    t.set(39, 2, 14, "oritech:cooler_block")
    t.set(41, 2, 14, "immersiveengineering:crate")
    t.set(43, 2, 14, "minecraft:barrel")
    t.clear((34, 2, 15), (34, 4, 15))
    _door(t, 34, 2, 15, "south")
    t.fill((30, 3, 15), (33, 5, 15), "create:framed_glass")
    t.fill((36, 3, 15), (40, 5, 15), "create:framed_glass")

    t.fill((17, 2, 16), (17, 7, 32), "tfmg:cinder_block")
    t.clear((17, 2, 20), (17, 4, 20))
    _door(t, 17, 2, 20, "east")
    t.clear((17, 2, 28), (17, 4, 28))
    _door(t, 17, 2, 28, "east")
    t.fill((5, 2, 25), (16, 7, 25), "tfmg:cinder_block")
    t.clear((15, 2, 25), (15, 4, 25))
    _door(t, 15, 2, 25, "south")
    t.fill((6, 2, 18), (11, 2, 18), "zvhouses:stone_brick_countertop")
    t.set(7, 3, 18, "the_wasteland_reworked:radio")
    t.set(10, 3, 18, "minecraft:lectern")
    t.fill((6, 2, 22), (9, 3, 23), "minecraft:bookshelf")
    t.fill((6, 2, 28), (10, 3, 30), "immersiveengineering:crate")
    t.fill((12, 2, 28), (15, 2, 30), "minecraft:barrel")

    for z in (18, 23, 31, 38):
        for x in (23, 45):
            t.fill((x, 2, z), (x, 14, z), "tfmg:steel_block")
        t.fill((23, 14, z), (45, 14, z), "tfmg:steel_block")
    t.fill((27, 17, 21), (40, 17, 21), "tfmg:steel_block")
    t.fill((27, 17, 34), (40, 17, 34), "tfmg:steel_block")
    t.fill((27, 17, 21), (27, 17, 34), "tfmg:steel_block")
    t.fill((40, 17, 21), (40, 17, 34), "tfmg:steel_block")

    t.fill((23, 1, 16), (45, 1, 40), "minecraft:smooth_stone")
    _rack_bank(t, 24, 26)
    _rack_bank(t, 30, 32)
    _rack_bank(t, 36, 38)

    t.fill((42, 3, 18), (42, 11, 18), "create:fluid_pipe")
    t.set(43, 2, 18, "create:mechanical_pump", facing="west")
    t.set(44, 2, 18, "minecraft:water_cauldron", level="3")
    t.set(45, 2, 18, "minecraft:barrel")
    t.fill((42, 11, 18), (42, 11, 36), "create:fluid_pipe")
    for z in (20, 25, 30):
        t.fill((24, 11, z), (42, 11, z), "create:fluid_pipe")
    for x in (28, 34, 40):
        for z in (20, 26, 30):
            _light(t, x, 12, z)

    t.clear((46, 2, 24), (46, 4, 25))
    _door(t, 46, 2, 24, "west", hinge="left")
    _door(t, 46, 2, 25, "west", hinge="right")
    t.fill((42, 2, 27), (45, 2, 27), "zvhouses:stone_brick_countertop")
    t.set(43, 3, 27, "create:depot")
    t.fill((43, 2, 26), (45, 3, 26), "jaffabricate:pallet_full")
    t.set(43, 2, 21, "oritech:cooler_block")
    t.set(45, 2, 21, "oritech:cooler_block")
    t.fill((43, 2, 20), (45, 3, 20), "immersiveengineering:crate")
    t.fill((42, 1, 29), (45, 1, 30), "minecraft:yellow_concrete")
    t.set(43, 2, 29, "immersiveengineering:crate")
    t.set(45, 2, 29, "minecraft:barrel")

    for z1, z2 in ((34, 36), (39, 40)):
        t.clear((21, 2, z1), (22, 4, z2))
        t.fill((21, 5, z1), (22, 5, z2), "tfmg:steel_block")

    t.fill((5, 1, 34), (20, 1, 40), "minecraft:white_concrete")
    t.fill((6, 2, 35), (15, 2, 35), "zvhouses:stone_brick_countertop")
    for x in (7, 10, 13):
        t.set(x, 2, 38, "minecraft:water_cauldron", level="3")
    t.fill((6, 3, 40), (15, 3, 40), "create:fluid_pipe")
    t.set(16, 2, 38, "create:depot")
    t.set(16, 2, 40, "create:depot")
    for x in (7, 12, 17):
        _light(t, x, 8, 37)

    t.fill((23, 1, 34), (45, 1, 40), "tfmg:factory_floor")
    t.fill((23, 2, 37), (27, 2, 38), "zvhouses:stone_brick_countertop")
    t.fill((34, 2, 35), (38, 2, 38), "zvhouses:stone_brick_countertop")
    t.fill((40, 2, 35), (43, 3, 36), "immersiveengineering:crate")
    t.fill((40, 2, 39), (43, 2, 39), "jaffabricate:pallet_full")
    t.fill((29, 1, 34), (32, 1, 40), "minecraft:yellow_concrete")
    t.clear((29, 2, 34), (32, 4, 40))
    t.clear((30, 2, 41), (31, 4, 41))
    _door(t, 30, 2, 41, "north", hinge="left")
    _door(t, 31, 2, 41, "north", hinge="right")

    t.fill((44, 2, 38), (44, 18, 38), "minecraft:ladder", facing="west", waterlogged="false")
    t.set(44, 19, 38, "minecraft:iron_trapdoor", facing="north", half="bottom", open="false", powered="false", waterlogged="false")

    _articulate_intact_exterior(t)
    t.fill((23, 11, 36), (42, 11, 36), "create:fluid_pipe")

    _sign_on_wall(t, 21, 8, 4, "north", "VERDANT", "CONTINUUM", "FOODS")
    _sign_on_wall(t, 27, 8, 4, "north", "EMERGENCY", "COMMUNITY", "GROW HALL")
    _sign_on_wall(t, 20, 6, 13, "north", "EMERGENCY", "REGISTRATION", "AUTHORIZATION")
    _sign_on_wall(t, 34, 6, 13, "north", "CULTURE KIT", "RELIEF ISSUE")
    _sign_on_wall(t, 34, 8, 15, "north", "STAFF ONLY", "GROW OPERATIONS")
    _sign_on_wall(t, 46, 6, 22, "east", "RECEIVING", "BATCH CHECK")
    _sign_on_wall(t, 46, 6, 20, "west", "CLEAN CULTURE", "STOCK")
    _sign_on_wall(t, 46, 6, 17, "west", "NUTRIENT", "IRRIGATION")
    _sign_on_wall(t, 46, 6, 29, "west", "QUALITY HOLD")
    _sign_on_wall(t, 21, 6, 34, "west", "HARVEST", "WASH / CHECK")
    _sign_on_wall(t, 24, 6, 41, "north", "PACKING", "RELIEF STAGING")
    _sign_on_wall(t, 33, 6, 41, "south", "RELIEF", "DISPATCH")
    _sign_on_wall(t, 46, 11, 20, "east", "EVERCROP", "CULTIVATION")
    _sign_on_wall(t, 38, 11, 41, "south", "VCF", "RELIEF GROW")
    return t


def _apply_d1(t: base.Template) -> None:
    t.fill((19, 2, 7), (21, 3, 8), "immersiveengineering:crate")
    t.set(20, 2, 9, "minecraft:barrel")
    t.fill((48, 1, 26), (49, 2, 27), "jaffabricate:pallet_full")
    t.set(45, 3, 28, "immersiveengineering:crate")
    t.fill((24, 2, 34), (26, 3, 35), "immersiveengineering:crate")
    t.fill((35, 2, 39), (37, 2, 40), "jaffabricate:pallet_full")
    t.fill((36, 1, 27), (38, 1, 30), "minecraft:yellow_concrete")
    for y in (3, 8):
        t.clear((36, y, 28), (38, y, 30))
    t.fill((36, 10, 28), (38, 10, 30), "minecraft:yellow_concrete")
    t.set(38, 9, 29, "minecraft:yellow_concrete")
    t.set(43, 2, 31, "immersiveengineering:crate")
    t.set(45, 2, 31, "minecraft:barrel")
    t.set(37, 9, 28, "minecraft:white_concrete")
    base.wall_sign(t, 37, 9, 27, "north", "RACK 3", "QUALITY HOLD")


def _apply_d3_r1(t: base.Template) -> None:
    t.clear((28, 19, 22), (31, 20, 25))
    t.clear((37, 18, 30), (40, 20, 33))
    t.set(29, 18, 24, "minecraft:cobweb")
    t.set(39, 18, 31, "minecraft:cobweb")
    t.clear((16, 11, 35), (19, 12, 38))
    t.fill((15, 10, 35), (18, 10, 38), "minecraft:mossy_stone_bricks")
    t.fill((18, 10, 34), (20, 10, 35), "minecraft:cracked_stone_bricks")
    t.clear((36, 2, 27), (38, 8, 30))
    t.fill((36, 1, 27), (38, 1, 30), "minecraft:coarse_dirt")
    t.fill((36, 1, 29), (38, 1, 30), "minecraft:moss_block")
    t.set(36, 2, 29, "minecraft:gravel")
    t.set(38, 2, 28, "minecraft:gravel")
    t.clear((36, 11, 30), (41, 11, 30))
    t.set(39, 10, 30, "minecraft:cobweb")
    t.clear((8, 11, 35), (11, 11, 38))
    t.fill((7, 1, 36), (11, 1, 40), "minecraft:mossy_stone_bricks")
    t.fill((12, 1, 38), (15, 1, 40), "minecraft:coarse_dirt")
    t.set(8, 2, 39, "minecraft:cobweb")
    t.set(14, 3, 39, "minecraft:cobweb")
    t.set(49, 0, 24, "minecraft:gravel")
    t.set(50, 0, 25, "minecraft:coarse_dirt")
    t.clear((46, 9, 26), (46, 10, 27))
    t.set(49, 1, 27, "minecraft:air")
    t.clear((34, 7, 43), (35, 7, 45))
    t.fill((36, 0, 43), (38, 0, 46), "minecraft:gravel")
    t.set(37, 1, 44, "minecraft:coarse_dirt")
    for pos in ((20, 3, 4), (20, 4, 4), (29, 2, 4), (30, 4, 4), (34, 5, 7)):
        t.set(*pos, "minecraft:air")
    for pos in ((37, 2, 27), (38, 2, 30), (10, 2, 37), (12, 2, 40)):
        if _block_name(t, *pos) in AIR:
            t.set(*pos, "minecraft:dead_bush")
    t.spawner(37, 2, 29, "minecraft:zombie", count=1, nearby=4)
    t.spawner(8, 2, 29, "minecraft:spider", count=1, nearby=3)
    t.set(23, 3, 14, "minecraft:air")
    t.chest(*PROOF_POS, PROOF_LOOT_TABLE, facing="east")


def _apply_d3_r2(t: base.Template) -> None:
    t.clear((8, 11, 29), (11, 11, 32))
    t.clear((12, 11, 33), (14, 11, 35))
    t.clear((6, 11, 36), (8, 11, 39))
    t.fill((9, 10, 30), (12, 10, 33), "minecraft:mossy_stone_bricks")
    t.fill((13, 10, 34), (15, 10, 36), "minecraft:cracked_stone_bricks")
    t.clear((4, 7, 31), (4, 9, 34))
    t.clear((4, 4, 36), (4, 6, 38))
    t.fill((4, 2, 30), (4, 3, 32), "minecraft:mossy_stone_bricks")
    t.fill((4, 2, 39), (4, 4, 40), "minecraft:cracked_stone_bricks")
    t.clear((46, 8, 19), (46, 10, 20))
    t.clear((46, 4, 33), (46, 6, 35))
    t.fill((46, 5, 19), (46, 7, 20), "minecraft:cracked_stone_bricks")
    t.fill((46, 3, 34), (46, 4, 35), "minecraft:mossy_stone_bricks")
    t.clear((22, 12, 19), (22, 14, 20))
    t.clear((22, 12, 33), (22, 13, 34))
    t.set(22, 14, 24, "minecraft:cracked_stone_bricks")
    t.set(22, 14, 35, "minecraft:mossy_stone_bricks")
    t.clear((36, 8, 41), (37, 10, 41))
    t.clear((42, 4, 41), (43, 6, 41))
    t.fill((41, 5, 41), (41, 7, 41), "minecraft:cracked_stone_bricks")
    for pos, block in {
        (47, 0, 22): "minecraft:gravel",
        (48, 0, 22): "minecraft:coarse_dirt",
        (49, 0, 23): "minecraft:gravel",
        (50, 0, 23): "minecraft:coarse_dirt",
        (47, 0, 28): "minecraft:moss_block",
        (48, 0, 29): "minecraft:gravel",
        (49, 0, 29): "minecraft:coarse_dirt",
    }.items():
        t.set(*pos, block)
    t.clear((49, 7, 27), (50, 7, 29))
    t.set(48, 7, 29, "minecraft:cracked_stone_bricks")
    t.clear((27, 7, 43), (28, 7, 45))
    t.clear((34, 7, 44), (35, 7, 45))
    for pos, block in {
        (23, 0, 43): "minecraft:gravel",
        (24, 0, 44): "minecraft:coarse_dirt",
        (25, 0, 45): "minecraft:gravel",
        (37, 0, 42): "minecraft:coarse_dirt",
        (38, 0, 43): "minecraft:moss_block",
        (38, 0, 45): "minecraft:gravel",
    }.items():
        t.set(*pos, block)
    for pos, block in {
        (5, 1, 33): "minecraft:gravel",
        (7, 1, 38): "minecraft:gravel",
        (45, 1, 34): "minecraft:gravel",
        (44, 1, 35): "minecraft:coarse_dirt",
        (37, 1, 40): "minecraft:gravel",
    }.items():
        t.set(*pos, block)


def _apply_microdetail(t: base.Template) -> None:
    # Service hangers below/around already-approved overhead irrigation runs.
    for pos in ((24, 12, 20), (30, 12, 25), (36, 12, 30)):
        if _block_name(t, *pos) in AIR:
            t.set(*pos, "minecraft:iron_bars")

    # Small maintenance-parts cluster beside the east irrigation service side.
    t.set(43, 2, 17, "create:andesite_casing")
    t.set(45, 2, 17, "immersiveengineering:metal_barrel")

    # Harvest/cleanup props in non-route corners of the converted wet-service room.
    t.set(18, 2, 37, "minecraft:composter")
    t.set(6, 2, 36, "minecraft:barrel")

    # Sparse debris/webbing directly beneath already-approved failure zones.
    for pos in ((10, 10, 31), (22, 13, 20), (46, 7, 34)):
        if _block_name(t, *pos) in AIR:
            t.set(*pos, "minecraft:cobweb")


def _assert_proof_chest(t: base.Template) -> None:
    row = t.blocks.get(PROOF_POS)
    if row is None:
        raise AssertionError("OWS-002 final proof chest is missing")
    state, nbt = row
    if t.palette[state]["Name"] != "minecraft:chest":
        raise AssertionError("OWS-002 final proof coordinate is not a chest")
    if not nbt or nbt.get("LootTable") != PROOF_LOOT_TABLE:
        raise AssertionError(f"OWS-002 final proof chest has wrong loot table: {None if not nbt else nbt.get('LootTable')}")
    if _block_name(t, PROOF_POS[0], PROOF_POS[1] + 1, PROOF_POS[2]) not in AIR:
        raise AssertionError("OWS-002 final proof chest cannot open")
    matches = sum(1 for _, (_, nbt_row) in t.blocks.items() if nbt_row and nbt_row.get("LootTable") == PROOF_LOOT_TABLE)
    if matches != 1:
        raise AssertionError(f"OWS-002 final structure must contain exactly one canonical proof container; found {matches}")


def _assert_final(t: base.Template) -> None:
    if tuple(t.size) != (51, 21, 47):
        raise AssertionError(f"OWS-002 final dimensions changed: {t.size}")

    _assert_door(t, 24, 2, 4, "public entrance west leaf", block_name="minecraft:dark_oak_door")
    _assert_door(t, 25, 2, 4, "public entrance east leaf", block_name="minecraft:dark_oak_door")
    _assert_clear(t, (24, 2, 5), (26, 4, 12), "public queue")
    _assert_door(t, 28, 2, 13, "records control")
    _assert_clear(t, (24, 2, 14), (28, 3, 14), "records/proof approach")
    _assert_clear(t, (27, 2, 18), (29, 4, 33), "grow aisle A")
    _assert_clear(t, (33, 2, 18), (35, 4, 33), "grow aisle B")
    _assert_clear(t, (18, 2, 34), (22, 4, 36), "raw harvest transfer")
    _assert_clear(t, (18, 2, 39), (28, 4, 40), "checked harvest return")
    _assert_clear(t, (29, 2, 34), (32, 4, 40), "relief dispatch lane")
    _assert_door(t, 30, 2, 41, "south dispatch west leaf")
    _assert_door(t, 31, 2, 41, "south dispatch east leaf")
    _assert_door(t, 46, 2, 24, "east receiving west leaf")
    _assert_door(t, 46, 2, 25, "east receiving east leaf")
    _assert_block(t, 44, 18, 38, "minecraft:ladder", "roof ladder top")
    _assert_block(t, 44, 19, 38, "minecraft:iron_trapdoor", "roof landing")
    _assert_proof_chest(t)

    if _block_name(t, 21, 8, 3) != "minecraft:oak_wall_sign":
        raise AssertionError("OWS-002 final structure lost primary VCF identity")
    if _block_name(t, 27, 8, 3) != "minecraft:oak_wall_sign":
        raise AssertionError("OWS-002 final structure lost facility identity")

    wheat = sum(1 for pos in t.blocks if _block_name(t, *pos) == "minecraft:wheat")
    pipes = sum(1 for pos in t.blocks if _block_name(t, *pos) == "create:fluid_pipe")
    spawners = sum(1 for pos in t.blocks if _block_name(t, *pos) == "minecraft:spawner")
    if wheat < 150:
        raise AssertionError(f"OWS-002 final structure preserves too little cultivation evidence: wheat={wheat}")
    if pipes < 70:
        raise AssertionError(f"OWS-002 final structure preserves too little irrigation evidence: pipes={pipes}")
    if spawners != 2:
        raise AssertionError(f"OWS-002 final structure requires exactly two encounter spawners; found {spawners}")


def build_002() -> base.Template:
    t = _build_d0()
    _apply_d1(t)
    _apply_d3_r1(t)
    _apply_d3_r2(t)
    _apply_microdetail(t)
    _assert_final(t)
    return t
