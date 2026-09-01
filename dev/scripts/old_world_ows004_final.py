#!/usr/bin/env python3
"""[SYSTEM REPORT] Final authoritative OWS-004 heavy-rebuild geometry.

`build_004()` reproduces the manually approved Gate-B r4 intact Mycological
Vertical Farm Tower, the Gate-C r4 D1/D3 history, and restrained Pass-19
microdetail. This module is side-effect-free and imports no review/rendering
machinery. Production Old World generation and Gate D must consume this exact
builder.
"""
from __future__ import annotations

import generate_wasteland_sites as base

PROOF_LOOT_TABLE = "infinite_domain:chests/old_world/ows_004_vcf_mycological_vertical_farm_tower"
PROOF_POS = (32, 2, 12)
LEVELS = (9, 16, 23, 30)
AIR = {"minecraft:air", "minecraft:cave_air", "minecraft:void_air", "minecraft:structure_void"}


def _name(t: base.Template, pos: tuple[int, int, int]) -> str:
    row = t.blocks.get(pos)
    if row is None:
        return "minecraft:air"
    return t.palette[row[0]]["Name"]


def _count(t: base.Template, name: str) -> int:
    return sum(1 for pos in t.blocks if _name(t, pos) == name)


# ---------------------------------------------------------------------------
# Gate-A r1 approved massing.
# ---------------------------------------------------------------------------

def _site_and_podium(t: base.Template) -> None:
    t.fill((1, 0, 1), (49, 0, 45), "minecraft:grass_block")
    t.fill((7, 0, 1), (34, 0, 10), "minecraft:smooth_stone")
    base.shell(t, (6, 1, 6), (35, 8, 17), "minecraft:white_concrete", "minecraft:smooth_stone", "minecraft:light_gray_concrete")
    t.fill((10, 2, 5), (30, 6, 5), "create:framed_glass")
    t.clear((18, 2, 5), (22, 5, 6))
    t.fill((11, 7, 5), (29, 8, 5), "minecraft:lime_concrete")
    t.fill((12, 8, 2), (28, 8, 6), "minecraft:white_concrete")
    for x in (12, 28):
        t.fill((x, 1, 3), (x, 7, 3), "minecraft:light_gray_concrete")

    base.shell(t, (34, 1, 13), (48, 10, 32), "minecraft:light_gray_concrete", "tfmg:factory_floor", "minecraft:smooth_stone")
    t.fill((48, 2, 17), (48, 7, 27), "minecraft:white_concrete")
    t.clear((48, 2, 19), (48, 6, 24))
    t.fill((49, 0, 16), (50, 0, 28), "tfmg:factory_floor")
    t.fill((48, 8, 16), (50, 8, 28), "tfmg:steel_block")
    for z in (16, 28):
        t.fill((50, 1, z), (50, 8, z), "tfmg:steel_block")

    base.shell(t, (24, 1, 31), (47, 8, 43), "minecraft:white_concrete", "tfmg:factory_floor", "minecraft:light_gray_concrete")
    t.clear((31, 2, 43), (39, 6, 43))
    t.fill((28, 0, 43), (44, 0, 46), "tfmg:asphalt")
    t.fill((29, 8, 40), (43, 8, 45), "minecraft:light_gray_concrete")
    for x in (29, 43):
        t.fill((x, 1, 44), (x, 8, 44), "tfmg:steel_block")


def _production_tower(t: base.Template) -> None:
    base.shell(t, (10, 8, 12), (40, 23, 37), "minecraft:white_concrete", "minecraft:smooth_stone", "minecraft:light_gray_concrete")
    base.shell(t, (12, 23, 14), (38, 39, 35), "minecraft:white_concrete", "minecraft:smooth_stone", "minecraft:light_gray_concrete")
    for y1, y2 in ((14, 15), (21, 22), (28, 29), (35, 36)):
        x1, x2, z1, z2 = (10, 40, 12, 37) if y1 < 23 else (12, 38, 14, 35)
        t.fill((x1, y1, z1 - 1), (x2, y2, z1 - 1), "minecraft:lime_concrete")
        t.fill((x1, y1, z2 + 1), (x2, y2, z2 + 1), "minecraft:lime_concrete")
        t.fill((x1 + 4, y1 - 3, z1 - 1), (x2 - 4, y1 - 1, z1 - 1), "create:framed_glass")
        t.fill((x1 + 4, y1 - 3, z2 + 1), (x2 - 4, y1 - 1, z2 + 1), "create:framed_glass")
    for x in (14, 20, 26, 32, 38):
        t.fill((x, 9, 11), (x, 22, 11), "minecraft:light_gray_concrete")
        t.fill((x, 9, 38), (x, 22, 38), "minecraft:light_gray_concrete")
    for x in (16, 22, 28, 34):
        t.fill((x, 24, 13), (x, 38, 13), "minecraft:light_gray_concrete")
        t.fill((x, 24, 36), (x, 38, 36), "minecraft:light_gray_concrete")


def _vertical_service_spine(t: base.Template) -> None:
    base.shell(t, (39, 8, 17), (45, 42, 31), "minecraft:light_gray_concrete", "minecraft:smooth_stone", "minecraft:white_concrete")
    for y in (13, 20, 27, 34):
        t.fill((39, y, 16), (45, y + 1, 16), "tfmg:steel_block")
        t.fill((39, y, 32), (45, y + 1, 32), "tfmg:steel_block")
    t.fill((45, 11, 20), (45, 39, 27), "create:framed_glass")
    base.shell(t, (6, 8, 24), (10, 39, 33), "minecraft:light_gray_concrete", "minecraft:smooth_stone", "minecraft:white_concrete")


def _roof_crown(t: base.Template) -> None:
    base.shell(t, (14, 39, 15), (36, 45, 34), "create:framed_glass", "minecraft:smooth_stone", "create:framed_glass")
    for x in (14, 25, 36):
        t.fill((x, 39, 14), (x, 46, 14), "minecraft:white_concrete")
        t.fill((x, 39, 35), (x, 46, 35), "minecraft:white_concrete")
    t.fill((14, 45, 14), (36, 46, 14), "minecraft:lime_concrete")
    t.fill((14, 45, 35), (36, 46, 35), "minecraft:lime_concrete")
    t.fill((37, 40, 18), (44, 45, 30), "immersiveengineering:sheetmetal_steel")
    t.fill((39, 42, 16), (42, 45, 17), "tfmg:steel_block")
    t.fill((39, 42, 31), (42, 45, 32), "tfmg:steel_block")


def _gate_a_massing() -> base.Template:
    t = base.Template((51, 47, 47))
    _site_and_podium(t)
    _production_tower(t)
    _vertical_service_spine(t)
    _roof_crown(t)
    return t


# ---------------------------------------------------------------------------
# Gate-B r4 approved intact operating architecture.
# ---------------------------------------------------------------------------

def _public_and_podium(t: base.Template) -> None:
    base.double_door(t, 20, 2, 6, "north", "iron")
    t.fill((8, 1, 7), (33, 1, 15), "minecraft:quartz_block")
    t.fill((10, 2, 15), (27, 6, 15), "create:framed_glass")
    base.partition_x(t, 29, 2, 7, 15, "minecraft:white_concrete", doorway_z=11)
    t.fill((30, 2, 8), (33, 3, 10), "minecraft:bookshelf")
    t.fill((30, 2, 13), (33, 2, 14), "create:depot")

    base.partition_z(t, 23, 2, 35, 47, "minecraft:light_gray_concrete", doorways=(40,))
    t.fill((35, 1, 15), (47, 1, 22), "tfmg:factory_floor")
    t.fill((35, 1, 24), (47, 1, 30), "minecraft:polished_blackstone")
    for x in (36, 40, 44):
        t.fill((x, 2, 16), (x + 1, 3, 18), "immersiveengineering:crate")
    for x in (36, 41, 45):
        t.fill((x, 2, 26), (x, 3, 28), "create:cardboard_block")
    base.door(t, 48, 2, 20, "east", "iron", "left")
    base.door(t, 48, 2, 21, "east", "iron", "right")
    base.door(t, 48, 2, 27, "east", "iron", "left")

    base.partition_x(t, 31, 2, 32, 42, "minecraft:white_concrete", doorway_z=37)
    base.partition_x(t, 39, 2, 32, 42, "minecraft:white_concrete", doorway_z=37)
    for x in (26, 28):
        t.set(x, 2, 34, "create:depot")
        t.set(x, 3, 34, "create:mechanical_press", facing="north")
    t.fill((33, 2, 34), (37, 3, 36), "create:cardboard_block")
    t.fill((41, 2, 34), (45, 4, 39), "immersiveengineering:crate")
    base.door(t, 34, 2, 43, "south", "iron", "left")
    base.door(t, 35, 2, 43, "south", "iron", "right")

    base.wall_sign(t, 18, 6, 5, "north", "VERDANT CONTINUUM", "FOODS")
    base.wall_sign(t, 22, 6, 5, "north", "MYCOLOGICAL", "VERTICAL FARM")
    base.wall_sign(t, 28, 4, 7, "west", "PUBLIC DEMO", "PRODUCTION VIEW")
    base.wall_sign(t, 35, 5, 13, "north", "CLEAN RECEIVING", "BATCH INTAKE")
    base.wall_sign(t, 47, 5, 25, "west", "SPENT RETURN", "SERVICE ONLY")
    base.wall_sign(t, 25, 5, 42, "south", "HARVEST CHECK", "GRADE / RELEASE")
    base.wall_sign(t, 33, 5, 42, "south", "PACKING")
    base.wall_sign(t, 41, 5, 42, "south", "OUTBOUND", "DISPATCH")


def _production_floor_plate(t: base.Template, y: int, upper: bool) -> None:
    x1, x2, z1, z2 = (13, 37, 15, 34) if upper else (11, 39, 13, 36)
    t.fill((x1, y, z1), (x2, y, z2), "tfmg:factory_floor")
    aisle_x1, aisle_x2 = 23, 27
    t.fill((aisle_x1, y, z1 + 2), (aisle_x2, y, z2 - 2), "minecraft:smooth_stone")
    left_x = range(x1 + 2, min(aisle_x1 - 1, x1 + 8), 3)
    right_start = max(aisle_x2 + 2, x2 - 8)
    right_x = range(right_start, x2 - 1, 3)
    for x in (*left_x, *right_x):
        for z in range(z1 + 3, z2 - 2, 5):
            t.fill((x, y + 1, z), (x + 1, y + 1, z + 2), "minecraft:mycelium")
            t.fill((x, y + 2, z), (x + 1, y + 2, z + 2), "minecraft:scaffolding")
            t.set(x, y + 3, z + 1, "minecraft:brown_mushroom")
            t.set(x + 1, y + 3, z + 1, "minecraft:red_mushroom")
    t.fill((x2 - 5, y + 1, z2 - 4), (x2 - 2, y + 1, z2 - 3), "create:depot")
    t.set(x2 - 4, y + 2, z2 - 3, "minecraft:cauldron")
    service_z = z1 + 1
    t.fill((x1 + 2, y + 4, service_z), (x2 - 2, y + 4, service_z), "create:fluid_pipe")
    for x in (x1 + 4, x1 + 10, x2 - 10, x2 - 4):
        t.set(x, y + 4, service_z + 1, "create:encased_fan", facing="south")
    t.fill((x1 + 1, y + 1, z2 - 5), (x1 + 2, y + 3, z2 - 4), "create:fluid_tank")
    t.fill((x1 + 3, y + 2, z2 - 4), (aisle_x1 - 1, y + 2, z2 - 4), "create:fluid_pipe")
    level_index = LEVELS.index(y) + 1
    base.wall_sign(t, aisle_x1 - 1, y + 3, z1 + 1, "south", f"CULTIVATION {level_index}", "CONTROLLED ZONE")
    base.wall_sign(t, x2 - 2, y + 3, z2 - 1, "north", "HARVEST HANDOFF", f"LEVEL {level_index}")


def _vertical_cores_and_services(t: base.Template) -> None:
    t.fill((7, 9, 27), (9, 38, 31), "minecraft:smooth_stone")
    t.clear((8, 9, 28), (8, 38, 30))
    for level in LEVELS:
        landing_x2 = 12 if level < 23 else 14
        t.fill((8, level, 29), (landing_x2, level, 31), "minecraft:smooth_stone")
        t.clear((10 if level < 23 else 12, level + 1, 30), (landing_x2, level + 3, 31))
    for y in range(9, 39):
        t.set(8, y, 30, "minecraft:ladder", facing="north", waterlogged="false")

    for level in LEVELS:
        t.fill((40, level, 18), (44, level, 30), "tfmg:factory_floor")
        t.fill((40, level + 1, 25), (44, level + 3, 29), "create:andesite_casing")
        t.clear((39 if level < 23 else 38, level + 1, 23), (40, level + 2, 25))
        base.door(t, 39 if level < 23 else 38, level + 1, 24, "west", "iron")

    t.fill((42, 9, 19), (42, 41, 19), "create:fluid_pipe")
    t.fill((43, 9, 20), (43, 41, 20), "tfmg:steel_block")
    for level in LEVELS:
        wall_x = 39 if level < 23 else 38
        t.fill((wall_x - 3, level + 4, 19), (42, level + 4, 19), "create:fluid_pipe")
        t.set(41, level + 2, 21, "create:mechanical_pump", facing="west")

    t.fill((40, 39, 19), (44, 39, 31), "minecraft:smooth_stone")
    t.clear((39, 40, 23), (40, 42, 25))
    base.door(t, 39, 40, 24, "west", "iron")


def _upper_isolation_readiness(t: base.Template) -> None:
    y = 30
    t.fill((33, y + 1, 21), (37, y + 4, 27), "minecraft:white_concrete")
    t.clear((34, y + 1, 22), (36, y + 3, 26))
    base.door(t, 33, y + 1, 24, "east", "iron")
    base.door(t, 37, y + 1, 24, "west", "iron")
    t.set(35, y + 2, 22, "create:mechanical_pump", facing="west")
    t.fill((34, y + 2, 26), (36, y + 2, 26), "create:depot")
    base.wall_sign(t, 34, y + 4, 23, "south", "ENV BRANCH 04", "CONTROL / SHUTOFF")
    base.wall_sign(t, 36, y + 4, 25, "north", "QUALITY HOLD", "AUTHORIZED STAFF")


def _roof_crown_operations(t: base.Template) -> None:
    t.fill((23, 39, 17), (27, 39, 32), "minecraft:smooth_stone")
    for x in (17, 20, 30, 33):
        for z in (19, 24, 29):
            t.fill((x, 40, z), (x + 1, 40, z + 2), "minecraft:mycelium")
            t.fill((x, 41, z), (x + 1, 42, z + 2), "minecraft:scaffolding")
            t.set(x, 43, z + 1, "minecraft:brown_mushroom")
    t.fill((16, 44, 17), (35, 44, 17), "create:fluid_pipe")
    t.fill((35, 44, 17), (42, 44, 19), "create:fluid_pipe")
    for x in (18, 24, 30, 34):
        t.set(x, 44, 19, "create:encased_fan", facing="south")
    t.fill((37, 40, 32), (39, 43, 34), "create:fluid_tank")
    base.wall_sign(t, 23, 43, 15, "north", "ROOFTOP SHOWCASE", "CONTROLLED CULTIVATION")
    base.wall_sign(t, 40, 42, 31, "north", "ENVIRONMENTAL PLANT", "MAINTENANCE")


def _staff_door(t: base.Template, floor_y: int, *, ground: bool = False, crown: bool = False) -> None:
    if ground:
        wall_x, door_y = 39, 2
    elif crown:
        wall_x, door_y = 39, 40
    else:
        wall_x, door_y = (39 if floor_y < 23 else 38), floor_y + 1
    z = 22
    t.clear((wall_x, door_y, z), (40, door_y + 2, z))
    base.door(t, wall_x, door_y, z, "west", "iron")


def _dogleg(t: base.Template, floor_y: int, target_y: int) -> list[tuple[int, int, int]]:
    delta = target_y - floor_y
    if delta == 7:
        first_rise, second_rise = 4, 4
    elif delta == 8:
        first_rise, second_rise = 5, 4
    elif delta == 9:
        first_rise, second_rise = 5, 5
    else:
        raise ValueError(f"Unsupported staff-stair floor interval: {floor_y}->{target_y}")
    first_y = floor_y + 1
    mid_y = first_y + first_rise - 1
    base.stair_flight(t, 40, first_y, 18, first_rise, "south", "minecraft:stone_brick_stairs")
    t.fill((40, mid_y, 22), (42, mid_y, 23), "minecraft:polished_andesite")
    base.stair_flight(t, 42, mid_y, 22, second_rise, "north", "minecraft:stone_brick_stairs")
    expected: list[tuple[int, int, int]] = []
    for step in range(first_rise):
        expected.append((40, first_y + step, 18 + step))
    for step in range(second_rise):
        expected.append((42, mid_y + step, 22 - step))
    return expected


def _install_primary_staff_stair(t: base.Template) -> tuple[list[tuple[int, int, int]], list[tuple[int, int, int]]]:
    t.clear((40, 2, 18), (43, 39, 23))
    t.fill((40, 1, 18), (43, 1, 23), "tfmg:factory_floor")
    for y in (9, 16, 23, 30, 39):
        t.fill((40, y, 18), (43, y, 23), "minecraft:smooth_stone")
    raw_expected: list[tuple[int, int, int]] = []
    raw_expected.extend(_dogleg(t, 1, 9))
    raw_expected.extend(_dogleg(t, 9, 16))
    raw_expected.extend(_dogleg(t, 16, 23))
    raw_expected.extend(_dogleg(t, 23, 30))
    raw_expected.extend(_dogleg(t, 30, 39))

    _staff_door(t, 1, ground=True)
    for y in (9, 16, 23, 30):
        _staff_door(t, y)
    _staff_door(t, 39, crown=True)

    t.fill((44, 9, 18), (44, 44, 18), "create:fluid_pipe")
    t.fill((44, 9, 20), (44, 44, 20), "tfmg:steel_block")
    for level in LEVELS:
        branch_y = level + 4
        service_x = 37 if level < 23 else 35
        header_z = 14 if level < 23 else 16
        t.fill((44, branch_y, 18), (44, branch_y, 23), "create:fluid_pipe")
        t.fill((service_x, branch_y, 23), (44, branch_y, 23), "create:fluid_pipe")
        t.fill((service_x, branch_y, header_z), (service_x, branch_y, 23), "create:fluid_pipe")
        t.set(44, branch_y, 21, "create:mechanical_pump", facing="south")

    t.fill((36, 2, 20), (38, 3, 21), "immersiveengineering:crate")
    base.wall_sign(t, 40, 6, 17, "north", "STAFF STAIRS", "PRODUCTION / CROWN")
    base.wall_sign(t, 43, 12, 17, "north", "STAFF CORE", "LEVEL 01-02")
    base.wall_sign(t, 43, 26, 17, "north", "STAFF CORE", "LEVEL 03-04")
    base.wall_sign(t, 43, 38, 17, "north", "ROOF / PLANT", "STAFF ACCESS")

    landing_points = [point for point in raw_expected if _name(t, point) == "minecraft:polished_andesite"]
    expected_treads = [point for point in raw_expected if _name(t, point) == "minecraft:stone_brick_stairs"]
    unexpected = [(point, _name(t, point)) for point in raw_expected if _name(t, point) not in {"minecraft:polished_andesite", "minecraft:stone_brick_stairs"}]
    if unexpected:
        raise AssertionError(f"OWS-004 stair path contains unexpected substitutions: {unexpected}")
    if landing_points != [(40, 6, 22), (40, 35, 22)]:
        raise AssertionError(f"OWS-004 unexpected dogleg landing substitutions: {landing_points}")
    return expected_treads, landing_points


def _build_d0() -> tuple[base.Template, list[tuple[int, int, int]], list[tuple[int, int, int]]]:
    t = _gate_a_massing()
    _public_and_podium(t)
    for y in LEVELS:
        _production_floor_plate(t, y, upper=y >= 23)
    _vertical_cores_and_services(t)
    _upper_isolation_readiness(t)
    _roof_crown_operations(t)
    # r2's sequencing repair is intentionally preserved even though the current
    # r1 review builder now also installs the ladder after its landings.
    for y in range(9, 39):
        t.set(8, y, 30, "minecraft:ladder", facing="north", waterlogged="false")
    expected_treads, landing_points = _install_primary_staff_stair(t)
    return t, expected_treads, landing_points


# ---------------------------------------------------------------------------
# Gate-C approved D1/D3 history.
# ---------------------------------------------------------------------------

def _apply_d1(t: base.Template) -> None:
    y = 30
    t.fill((28, y, 17), (37, y, 18), "minecraft:yellow_concrete")
    t.fill((28, y, 28), (37, y, 29), "minecraft:yellow_concrete")
    t.fill((28, y, 18), (29, y, 29), "minecraft:yellow_concrete")
    t.fill((29, y + 1, 20), (29, y + 4, 27), "minecraft:white_concrete")
    t.clear((29, y + 1, 23), (29, y + 3, 24))
    base.door(t, 29, y + 1, 24, "west", "iron")
    t.clear((31, y + 1, 20), (32, y + 3, 22))
    t.fill((31, y + 1, 20), (32, y + 1, 22), "minecraft:yellow_concrete")
    t.clear((32, y + 4, 16), (34, y + 4, 16))
    t.fill((32, y + 4, 16), (33, y + 4, 16), "minecraft:yellow_concrete")
    t.set(34, y + 4, 16, "create:fluid_pipe")
    t.fill((35, y + 1, 29), (37, y + 2, 30), "immersiveengineering:crate")
    t.set(36, y + 3, 29, "minecraft:barrel")
    base.wall_sign(t, 36, y + 4, 30, "north", "QUALITY HOLD", "LEVEL 4")


def _apply_d3_base(t: base.Template) -> None:
    t.clear((14, 46, 17), (20, 46, 24))
    t.clear((29, 46, 25), (36, 46, 34))
    t.clear((34, 43, 17), (39, 45, 19))
    t.clear((33, 44, 17), (37, 44, 19))
    t.set(34, 43, 18, "minecraft:cobweb")
    t.set(36, 42, 19, "minecraft:cobweb")

    t.clear((29, 32, 20), (29, 34, 22))
    t.clear((29, 33, 26), (29, 34, 27))
    t.fill((29, 31, 20), (29, 31, 22), "minecraft:cracked_stone_bricks")
    t.clear((14, 31, 18), (16, 33, 22))
    t.fill((14, 30, 18), (17, 30, 23), "minecraft:coarse_dirt")
    t.set(16, 31, 21, "minecraft:brown_mushroom")
    t.set(17, 31, 22, "minecraft:red_mushroom")
    t.set(18, 31, 23, "minecraft:cobweb")

    t.clear((34, 34, 19), (37, 34, 19))
    t.set(35, 34, 19, "minecraft:cracked_stone_bricks")
    t.set(37, 33, 20, "minecraft:cobweb")
    t.clear((14, 24, 19), (15, 26, 21))
    t.fill((14, 23, 19), (17, 23, 22), "minecraft:mossy_stone_bricks")
    t.set(17, 24, 20, "minecraft:cobweb")
    t.fill((11, 9, 34), (14, 9, 36), "minecraft:cracked_stone_bricks")
    t.fill((13, 16, 34), (16, 16, 36), "minecraft:mossy_stone_bricks")
    t.clear((38, 35, 36), (40, 38, 36))
    t.clear((10, 36, 14), (12, 38, 14))
    t.set(39, 34, 36, "minecraft:cracked_stone_bricks")
    t.set(11, 35, 14, "minecraft:mossy_stone_bricks")

    t.spawner(18, 31, 26, "minecraft:zombie", count=1, nearby=4)
    t.spawner(34, 24, 32, "minecraft:spider", count=1, nearby=3)
    t.set(PROOF_POS[0], PROOF_POS[1] + 1, PROOF_POS[2], "minecraft:air")
    t.chest(*PROOF_POS, PROOF_LOOT_TABLE, facing="west")


def _apply_d3_r4(t: base.Template) -> None:
    t.clear((13, 44, 17), (20, 46, 24))
    t.clear((28, 44, 26), (36, 46, 34))
    t.clear((20, 46, 23), (25, 46, 29))
    t.fill((13, 43, 17), (18, 43, 17), "minecraft:cracked_stone_bricks")
    t.fill((28, 43, 34), (34, 43, 34), "minecraft:cracked_stone_bricks")
    t.set(20, 43, 18, "minecraft:mossy_stone_bricks")
    t.set(33, 43, 33, "minecraft:mossy_stone_bricks")
    t.clear((16, 44, 17), (25, 44, 19))
    t.clear((30, 44, 17), (36, 44, 19))
    t.clear((37, 40, 32), (39, 43, 34))
    t.set(24, 43, 19, "minecraft:cobweb")
    t.set(35, 42, 19, "minecraft:cobweb")
    t.set(38, 39, 33, "minecraft:gravel")

    t.clear((12, 33, 14), (18, 38, 14))
    t.fill((12, 32, 14), (18, 32, 14), "minecraft:cracked_stone_bricks")
    t.set(13, 33, 15, "minecraft:cobweb")
    t.set(17, 34, 15, "minecraft:mossy_stone_bricks")
    t.clear((30, 33, 36), (37, 38, 36))
    t.fill((30, 32, 36), (37, 32, 36), "minecraft:cracked_stone_bricks")
    t.set(32, 33, 35, "minecraft:cobweb")
    t.set(36, 34, 35, "minecraft:mossy_stone_bricks")

    t.clear((14, 31, 18), (20, 34, 24))
    t.fill((14, 30, 18), (20, 30, 24), "minecraft:coarse_dirt")
    for pos in ((15, 31, 19), (17, 31, 21), (19, 31, 23)):
        t.set(*pos, "minecraft:brown_mushroom")
    t.set(18, 31, 20, "minecraft:red_mushroom")
    t.set(20, 31, 24, "minecraft:cobweb")
    t.clear((31, 31, 29), (35, 34, 33))
    t.fill((31, 30, 29), (35, 30, 33), "minecraft:mossy_stone_bricks")
    t.set(32, 31, 30, "minecraft:brown_mushroom")
    t.set(34, 31, 32, "minecraft:cobweb")

    t.clear((30, 24, 30), (33, 26, 33))
    t.fill((30, 23, 30), (34, 23, 34), "minecraft:mossy_stone_bricks")
    t.set(31, 24, 31, "minecraft:cobweb")
    t.set(33, 24, 33, "minecraft:brown_mushroom")
    t.fill((14, 30, 15), (18, 30, 17), "minecraft:cracked_stone_bricks")
    t.fill((30, 30, 34), (36, 30, 35), "minecraft:mossy_stone_bricks")


def _apply_pass19_microdetail(t: base.Template) -> None:
    """Restrained close-range detail only; no approved route/massing change."""
    # Abandoned floor-service stock at existing work nodes.
    t.set(13, 10, 31, "minecraft:barrel")
    t.set(14, 17, 31, "immersiveengineering:crate")
    t.set(15, 24, 29, "minecraft:barrel")
    # Broken cultivation remnants remain directly beside the accepted Level-4
    # collapse fields and outside the protected central aisle.
    t.set(16, 31, 24, "immersiveengineering:crate")
    t.set(19, 31, 22, "minecraft:barrel")
    # Sparse weather residue below already-approved crown failures.
    t.set(19, 42, 20, "minecraft:cobweb")
    t.set(30, 42, 30, "minecraft:cobweb")
    t.set(21, 39, 24, "minecraft:gravel")
    # Small wet-service residue at the accepted Level-3 consequence node.
    t.set(30, 24, 34, "minecraft:gravel")
    t.set(34, 24, 30, "minecraft:cobweb")


def _assert_final(t: base.Template, expected_treads: list[tuple[int, int, int]], landing_points: list[tuple[int, int, int]]) -> None:
    if tuple(t.size) != (51, 47, 47):
        raise AssertionError(f"OWS-004 final dimensions changed: {t.size}")
    if len(expected_treads) < 40 or landing_points != [(40, 6, 22), (40, 35, 22)]:
        raise AssertionError("OWS-004 final principal staff stair contract changed")
    for point in expected_treads:
        if _name(t, point) != "minecraft:stone_brick_stairs":
            raise AssertionError(f"OWS-004 final staff stair lost at {point}: {_name(t, point)}")
        x, y, z = point
        for head_y in (y + 1, y + 2):
            if _name(t, (x, head_y, z)) not in AIR:
                raise AssertionError(f"OWS-004 final staff-stair headroom blocked at {(x, head_y, z)}")
    for point in landing_points:
        if _name(t, point) != "minecraft:polished_andesite":
            raise AssertionError(f"OWS-004 final stair landing lost at {point}")
    for y in range(9, 39):
        if _name(t, (8, y, 30)) != "minecraft:ladder":
            raise AssertionError(f"OWS-004 final west egress ladder gap at y={y}")
    for level in LEVELS:
        if _name(t, (44, level + 2, 27)) != "create:andesite_casing":
            raise AssertionError(f"OWS-004 final freight core lost at level {level}")
        if _name(t, (44, level, 18)) != "create:fluid_pipe":
            raise AssertionError(f"OWS-004 final environmental riser lost at level {level}")
    row = t.blocks.get(PROOF_POS)
    if row is None or t.palette[row[0]]["Name"] != "minecraft:chest" or not row[1] or row[1].get("LootTable") != PROOF_LOOT_TABLE:
        raise AssertionError("OWS-004 final canonical proof chest changed")
    if _name(t, (PROOF_POS[0], PROOF_POS[1] + 1, PROOF_POS[2])) not in AIR:
        raise AssertionError("OWS-004 final proof chest is obstructed")
    matching = sum(1 for _, (_, nbt) in t.blocks.items() if nbt and nbt.get("LootTable") == PROOF_LOOT_TABLE)
    if matching != 1:
        raise AssertionError(f"OWS-004 final must contain exactly one canonical proof container; found {matching}")
    if _count(t, "minecraft:spawner") != 2:
        raise AssertionError("OWS-004 final must preserve exactly two optional encounter spawners")
    if _count(t, "minecraft:oak_wall_sign") < 8:
        raise AssertionError("OWS-004 final preserves too little institutional/operational wayfinding")
    if _count(t, "minecraft:mycelium") < 70:
        raise AssertionError("OWS-004 final removed too much surviving cultivation evidence")
    if _count(t, "create:fluid_pipe") < 55:
        raise AssertionError("OWS-004 final removed too much environmental-service evidence")


def build_004() -> base.Template:
    t, expected_treads, landing_points = _build_d0()
    _apply_d1(t)
    _apply_d3_base(t)
    _apply_d3_r4(t)
    _apply_pass19_microdetail(t)
    _assert_final(t, expected_treads, landing_points)
    return t
