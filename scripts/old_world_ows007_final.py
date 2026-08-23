#!/usr/bin/env python3
"""Pure side-effect-free authoritative OWS-007 production builder.

The module reconstructs the independently accepted Gate-C r1 D3 geometry from
target-local code and adds only the Pass-19 microdetail overlay. It performs no
rendering, serialization, registry mutation or gate decision.
"""
from __future__ import annotations

import math

import generate_wasteland_sites as base


ACCEPTED_GATE_C_D3_SHA256 = "62b146b0cb46af49ceaf6fced34785b32c9c9278ae482a5af8ca54513928f54c"
PROOF_LOOT_TABLE = "infinite_domain:chests/old_world/ows_007_vcf_ep7_agricultural_development_laboratory"
PROOF_POS = (43, 2, 55)
SPAWNER_POSITIONS = ((5, 2, 36), (20, 2, 39), (63, 2, 30))
AIR = {None, "minecraft:air", "minecraft:cave_air", "minecraft:void_air", "minecraft:structure_void"}

PASS19_MICRODETAIL = {
    (5, 3, 45): "minecraft:cobweb",
    (6, 2, 42): "minecraft:brown_mushroom",
    (18, 3, 42): "minecraft:cobweb",
    (18, 2, 43): "minecraft:brown_mushroom",
    (31, 3, 55): "minecraft:cobweb",
    (34, 2, 54): "minecraft:brown_mushroom",
    (59, 4, 40): "minecraft:cobweb",
    (59, 2, 42): "minecraft:brown_mushroom",
}

# One grounded replacement at the accepted rotunda humidity/wet-damage edge
# satisfies the declared OWS-007 mycelial-test material contract without
# changing the accepted damage footprint or any route/gameplay node.
PASS19_REPLACEMENTS = {
    (61, 1, 42): ("minecraft:mossy_stone_bricks", "minecraft:mycelium"),
}


def _name(t: base.Template, pos: tuple[int, int, int]) -> str | None:
    entry = t.blocks.get(pos)
    return None if entry is None else t.palette[entry[0]]["Name"]


def _count_block(t: base.Template, block: str) -> int:
    return sum(1 for pos in t.blocks if _name(t, pos) == block)


def _site_and_public_threshold(t: base.Template) -> None:
    t.fill((1, 0, 1), (71, 0, 61), "minecraft:grass_block")
    t.fill((8, 0, 1), (46, 0, 10), "minecraft:smooth_stone")
    t.fill((22, 0, 0), (29, 0, 13), "minecraft:white_concrete")
    for x in (10, 44):
        t.fill((x, 0, 2), (x, 0, 9), "minecraft:lime_concrete")
    t.fill((2, 0, 52), (48, 0, 61), "tfmg:asphalt")
    t.fill((49, 0, 49), (71, 0, 61), "minecraft:light_gray_concrete")
    for x in (7, 18, 31, 42, 55, 66):
        t.fill((x, 0, 56), (x, 0, 61), "minecraft:white_concrete")
    base.shell(t, (7, 1, 6), (43, 9, 16), "minecraft:white_concrete", "minecraft:smooth_stone", "minecraft:light_gray_concrete")
    t.fill((11, 2, 5), (39, 7, 5), "create:framed_glass")
    t.clear((21, 2, 5), (28, 6, 6))
    t.fill((12, 8, 5), (38, 9, 5), "minecraft:lime_concrete")
    t.fill((16, 9, 1), (34, 9, 7), "minecraft:white_concrete")
    for x in (16, 34):
        t.fill((x, 1, 2), (x, 8, 2), "minecraft:light_gray_concrete")
    base.shell(t, (15, 9, 8), (36, 13, 15), "create:framed_glass", "minecraft:light_gray_concrete", "minecraft:white_concrete")


def _controlled_trial_wing(t: base.Template) -> None:
    chambers = (
        ((5, 1, 15), (17, 15, 44), 15, 10),
        ((17, 1, 13), (30, 18, 46), 18, 12),
        ((30, 1, 16), (42, 16, 43), 16, 11),
    )
    for lo, hi, roof_y, band_y in chambers:
        base.shell(t, lo, hi, "minecraft:white_concrete", "minecraft:smooth_stone", "minecraft:light_gray_concrete")
        x1, _, z1 = lo
        x2, _, z2 = hi
        t.fill((x1 + 2, 4, z1 - 1), (x2 - 2, 9, z1 - 1), "create:framed_glass")
        t.fill((x1, band_y, z2 + 1), (x2, band_y + 1, z2 + 1), "minecraft:cyan_concrete")
        for x in (x1, x2):
            t.fill((x, 1, z1 - 1), (x, roof_y, z1 - 1), "minecraft:light_gray_concrete")
    monitors = (
        ((8, 15, 21), (15, 19, 38)),
        ((20, 18, 19), (28, 23, 40)),
        ((32, 16, 21), (40, 21, 37)),
    )
    for lo, hi in monitors:
        base.shell(t, lo, hi, "create:framed_glass", "minecraft:light_gray_concrete", "minecraft:white_concrete")
        x1, y1, z1 = lo
        x2, y2, z2 = hi
        t.fill((x1, y2, z1 - 1), (x2, y2, z1 - 1), "minecraft:lime_concrete")
        t.fill((x1, y1, z2 + 1), (x2, y1 + 1, z2 + 1), "minecraft:cyan_concrete")


def _phenotyping_and_service_hinge(t: base.Template) -> None:
    base.shell(t, (7, 1, 40), (44, 12, 52), "minecraft:white_concrete", "tfmg:factory_floor", "minecraft:light_gray_concrete")
    t.fill((11, 4, 39), (40, 9, 39), "create:framed_glass")
    base.shell(t, (13, 12, 43), (39, 16, 50), "create:framed_glass", "minecraft:light_gray_concrete", "minecraft:white_concrete")
    base.shell(t, (3, 1, 50), (46, 9, 59), "minecraft:light_gray_concrete", "tfmg:factory_floor", "minecraft:white_concrete")
    for x1, x2 in ((7, 17), (31, 39)):
        t.clear((x1, 2, 59), (x2, 7, 59))
        t.fill((x1 - 1, 8, 58), (x2 + 1, 10, 60), "tfmg:steel_block")
    base.shell(t, (2, 1, 18), (7, 22, 53), "minecraft:light_gray_concrete", "minecraft:smooth_stone", "minecraft:white_concrete")
    t.fill((1, 4, 22), (1, 19, 48), "create:framed_glass")
    t.fill((4, 12, 42), (15, 21, 52), "immersiveengineering:sheetmetal_steel")
    t.fill((7, 17, 45), (13, 25, 50), "tfmg:steel_block")


def _set_disk(t: base.Template, cx: int, y: int, cz: int, radius: int, block: str, *, inner_radius: int = -1) -> None:
    for dx in range(-radius, radius + 1):
        for dz in range(-radius, radius + 1):
            d2 = dx * dx + dz * dz
            if d2 <= radius * radius and d2 > inner_radius * inner_radius:
                t.set(cx + dx, y, cz + dz, block)


def _durability_rotunda(t: base.Template) -> None:
    cx, cz, radius = 57, 35, 13
    inner = radius - 2
    _set_disk(t, cx, 1, cz, radius - 1, "minecraft:smooth_stone")
    _set_disk(t, cx, 12, cz, radius - 1, "minecraft:smooth_stone", inner_radius=5)
    for y in range(1, 23):
        for dx in range(-radius, radius + 1):
            for dz in range(-radius, radius + 1):
                d2 = dx * dx + dz * dz
                if not (inner * inner <= d2 <= radius * radius):
                    continue
                structural_rib = abs(dx) <= 1 or abs(dz) <= 1 or abs(abs(dx) - abs(dz)) <= 1
                if y <= 4:
                    block = "minecraft:light_gray_concrete"
                elif y in (10, 11):
                    block = "minecraft:lime_concrete"
                elif structural_rib:
                    block = "minecraft:white_concrete"
                elif y >= 19:
                    block = "minecraft:light_gray_concrete"
                else:
                    block = "create:framed_glass"
                t.set(cx + dx, y, cz + dz, block)
    base.shell(t, (38, 8, 29), (48, 13, 41), "minecraft:white_concrete", "minecraft:smooth_stone", "minecraft:light_gray_concrete")
    t.fill((39, 9, 28), (47, 12, 28), "create:framed_glass")
    t.fill((39, 9, 42), (47, 12, 42), "create:framed_glass")
    _set_disk(t, cx, 23, cz, radius - 1, "create:framed_glass", inner_radius=4)
    for angle in range(0, 360, 45):
        radians = math.radians(angle)
        for step in range(5, radius):
            x = cx + round(math.cos(radians) * step)
            z = cz + round(math.sin(radians) * step)
            t.set(x, 24, z, "minecraft:white_concrete")
    base.shell(t, (52, 23, 30), (62, 29, 40), "immersiveengineering:sheetmetal_steel", "minecraft:smooth_stone", "minecraft:white_concrete")
    t.fill((54, 26, 29), (60, 29, 29), "minecraft:cyan_concrete")
    t.fill((51, 25, 32), (51, 28, 38), "create:framed_glass")
    t.fill((63, 24, 33), (66, 27, 37), "tfmg:steel_block")


def build_gate_a_massing() -> base.Template:
    t = base.Template((73, 33, 63))
    _site_and_public_threshold(t)
    _controlled_trial_wing(t)
    _phenotyping_and_service_hinge(t)
    _durability_rotunda(t)
    return t


def _pass7_structural_system(t: base.Template) -> None:
    for x in (11, 16, 21, 28, 33, 39):
        t.fill((x, 1, 5), (x, 8, 5), "minecraft:light_gray_concrete")
        t.fill((x, 8, 5), (x, 9, 15), "minecraft:light_gray_concrete")
    chambers = ((5, 17, 15, 44, 15), (17, 30, 13, 46, 18), (30, 42, 16, 43, 16))
    for x1, x2, z1, z2, roof_y in chambers:
        for z in (z1, (z1 + z2) // 2, z2):
            for x in (x1, x2):
                t.fill((x, 1, z), (x, roof_y, z), "tfmg:steel_block")
            t.fill((x1, roof_y - 1, z), (x2, roof_y, z), "tfmg:steel_block")
    for x in (7, 14, 22, 30, 38, 44):
        t.fill((x, 1, 40), (x, 12, 40), "minecraft:light_gray_concrete")
        t.fill((x, 11, 40), (x, 12, 52), "minecraft:light_gray_concrete")
    for x in (3, 11, 20, 29, 38, 46):
        t.fill((x, 1, 50), (x, 9, 50), "tfmg:steel_block")
        t.fill((x, 8, 50), (x, 9, 59), "tfmg:steel_block")
    t.fill((38, 7, 29), (48, 8, 29), "tfmg:steel_block")
    t.fill((38, 7, 41), (48, 8, 41), "tfmg:steel_block")
    cx, cz = 57, 35
    for angle in range(0, 360, 45):
        radians = math.radians(angle)
        for radius in range(6, 13):
            x = cx + round(math.cos(radians) * radius)
            z = cz + round(math.sin(radians) * radius)
            t.set(x, 12, z, "tfmg:steel_block")
    t.fill((3, 18, 20), (6, 19, 51), "tfmg:steel_block")
    for z in (22, 30, 38, 46, 51):
        t.fill((2, 1, z), (7, 21, z), "minecraft:light_gray_concrete")


def _pass8_circulation_and_access(t: base.Template) -> None:
    t.clear((23, 2, 5), (26, 5, 6))
    base.double_door(t, 24, 2, 5, "north", "iron")
    t.fill((22, 1, 6), (28, 1, 14), "minecraft:quartz_block")
    t.fill((8, 1, 12), (42, 1, 15), "minecraft:smooth_quartz")
    t.clear((8, 2, 14), (10, 5, 16))
    base.double_door(t, 9, 2, 15, "south", "iron")
    for x, z, facing in (
        (11, 15, "south"), (22, 13, "south"), (35, 16, "south"),
        (11, 43, "north"), (22, 45, "north"), (35, 42, "north"),
    ):
        t.clear((x, 2, z), (x + 1, 4, z))
        base.double_door(t, x, 2, z, facing, "iron")
    for x, label_facing in ((11, "south"), (35, "south")):
        t.fill((x - 2, 2, 59), (x + 3, 6, 59), "minecraft:light_gray_concrete")
        t.clear((x, 2, 59), (x + 1, 4, 59))
        base.double_door(t, x, 2, 59, label_facing, "iron")
    for x in (12, 24, 36):
        t.clear((x, 2, 50), (x + 1, 4, 50))
        base.double_door(t, x, 2, 50, "north", "iron")
    for x in (40, 41):
        base.stair_flight(t, x, 2, 49, 7, "north", "minecraft:smooth_quartz_stairs")
    t.fill((39, 8, 39), (42, 8, 44), "minecraft:smooth_stone")
    t.clear((39, 9, 39), (42, 12, 41))
    for step in range(4):
        for z in (34, 35):
            t.set(43 + step, 9 + step, z, "minecraft:smooth_quartz_stairs", facing="west", half="bottom", shape="straight", waterlogged="false")
    t.clear((3, 2, 24), (5, 20, 26))
    for y in range(2, 21):
        t.set(3, y, 25, "minecraft:ladder", facing="east", waterlogged="false")
    t.fill((3, 21, 24), (7, 21, 28), "minecraft:oxidized_copper_grate")


def _pass9_exterior_architecture(t: base.Template) -> None:
    for x1, x2 in ((12, 15), (17, 20), (29, 32), (34, 38)):
        t.fill((x1, 3, 5), (x2, 7, 5), "create:framed_glass")
    for x1, x2, z in ((7, 10, 14), (13, 16, 14), (19, 22, 12), (25, 28, 12), (32, 35, 15), (38, 40, 15)):
        t.fill((x1, 4, z), (x2, 8, z), "create:framed_glass")
    t.fill((6, 0, 57), (19, 0, 57), "minecraft:oxidized_copper_grate")
    t.fill((29, 0, 57), (42, 0, 57), "minecraft:oxidized_copper_grate")
    t.fill((7, 0, 60), (18, 0, 61), "minecraft:white_concrete")
    t.fill((31, 0, 60), (40, 0, 61), "minecraft:gray_concrete")
    for x, y, z in ((11, 20, 29), (24, 24, 29), (36, 22, 29)):
        t.fill((x - 2, y, z - 2), (x + 2, y + 1, z + 2), "minecraft:oxidized_copper_grate")
    t.fill((53, 26, 29), (61, 28, 29), "minecraft:cyan_concrete")


def _pass10_interior_architecture(t: base.Template) -> None:
    t.fill((8, 1, 7), (42, 1, 15), "minecraft:quartz_block")
    base.partition_x(t, 18, 2, 7, 15, "minecraft:white_concrete", doorway_z=10)
    base.partition_x(t, 30, 2, 7, 15, "minecraft:white_concrete", doorway_z=10)
    t.fill((8, 2, 11), (42, 6, 11), "create:framed_glass")
    t.clear((23, 2, 11), (26, 4, 11))
    base.double_door(t, 24, 2, 11, "south", "iron")
    for x1, x2, z1, z2 in ((6, 16, 16, 43), (18, 29, 14, 45), (31, 41, 17, 42)):
        t.fill((x1, 1, z1), (x2, 1, z2), "minecraft:smooth_stone")
    base.partition_z(t, 29, 2, 6, 16, "minecraft:white_concrete", doorways=(11,))
    base.partition_z(t, 31, 2, 18, 29, "minecraft:white_concrete", doorways=(23,))
    base.partition_z(t, 30, 2, 31, 41, "minecraft:cyan_concrete", doorways=(36,))
    for x, z in ((11, 29), (23, 31), (36, 30)):
        t.clear((x, 2, z), (x + 1, 4, z))
        base.double_door(t, x, 2, z, "south", "iron")
    t.fill((8, 1, 41), (43, 1, 51), "tfmg:factory_floor")
    base.partition_x(t, 27, 2, 41, 51, "minecraft:white_concrete", doorway_z=46)
    base.partition_x(t, 37, 2, 41, 51, "minecraft:white_concrete", doorway_z=46)
    t.fill((14, 2, 41), (26, 6, 41), "create:framed_glass")
    t.clear((11, 2, 40), (12, 4, 42))
    t.clear((22, 2, 40), (24, 4, 44))
    t.clear((35, 2, 40), (37, 4, 41))
    t.fill((4, 1, 51), (45, 1, 58), "tfmg:factory_floor")
    for x in (17, 29, 39):
        base.partition_x(t, x, 2, 51, 58, "minecraft:light_gray_concrete", doorway_z=54)
        t.clear((x, 2, 56), (x, 4, 57))
        base.double_door(t, x, 2, 56, "east", "iron")
    t.fill((18, 1, 51), (28, 1, 58), "minecraft:smooth_stone")
    t.fill((40, 1, 51), (45, 1, 58), "minecraft:quartz_block")
    cx, cz = 57, 35
    for angle in range(0, 360, 15):
        radians = math.radians(angle)
        x = cx + round(math.cos(radians) * 6)
        z = cz + round(math.sin(radians) * 6)
        t.set(x, 13, z, "minecraft:iron_bars")
    t.fill((56, 1, 24), (58, 1, 46), "minecraft:smooth_quartz")
    t.fill((46, 1, 34), (68, 1, 36), "minecraft:smooth_quartz")


def _crop_bank(t: base.Template, x1: int, x2: int, z: int, crop: str) -> None:
    t.fill((x1, 2, z), (x2, 2, z + 1), "farmersdelight:rich_soil")
    for x in range(x1, x2 + 1, 2):
        t.set(x, 3, z, crop)
    t.fill((x1, 5, z), (x2, 5, z + 1), "create:fluid_pipe")


def _pass11_operational_systems(t: base.Template) -> None:
    for x in (5, 10, 14):
        t.fill((x, 2, 53), (x + 2, 3, 55), "immersiveengineering:crate")
    base.desk(t, 13, 2, 52)
    t.fill((19, 2, 52), (21, 5, 54), "oritech:cooler_block")
    t.fill((24, 2, 52), (27, 4, 54), "minecraft:barrel", facing="up", open="false")
    t.set(25, 2, 55, "minecraft:brewing_stand", has_bottle_0="false", has_bottle_1="false", has_bottle_2="false")
    t.fill((30, 2, 52), (33, 5, 54), "create:fluid_tank")
    t.set(36, 2, 53, "minecraft:cauldron")
    t.fill((40, 2, 52), (45, 5, 53), "minecraft:bookshelf")
    base.desk(t, 40, 2, 54)
    for z in (20, 26, 35, 40):
        _crop_bank(t, 7, 10, z, "minecraft:wheat")
        _crop_bank(t, 13, 15, z, "minecraft:carrots")
    t.fill((6, 11, 20), (16, 11, 40), "create:fluid_pipe")
    t.set(11, 12, 31, "create:encased_fan", facing="south")
    for z in (18, 24, 36, 42):
        t.fill((19, 2, z), (21, 5, z + 2), "minecraft:barrel", facing="up", open="false")
        t.fill((26, 2, z), (28, 5, z + 2), "oritech:cooler_block")
    t.fill((18, 14, 18), (29, 14, 42), "create:fluid_pipe")
    for x in (20, 27):
        t.set(x, 15, 30, "create:encased_fan", facing="south")
    for z in (20, 26, 35, 39):
        _crop_bank(t, 32, 34, z, "minecraft:beetroots")
        _crop_bank(t, 38, 40, z, "minecraft:wheat")
    t.fill((32, 2, 31), (35, 4, 32), "create:framed_glass")
    for x in (33, 36, 39):
        t.set(x, 12, 28, "minecraft:brewing_stand", has_bottle_0="false", has_bottle_1="false", has_bottle_2="false")
    t.fill((9, 2, 45), (24, 2, 46), "create:depot")
    for x in (10, 14, 18, 22):
        t.set(x, 3, 45, "ae2:terminal")
    for z in (44, 48):
        _crop_bank(t, 29, 34, z, "minecraft:wheat")
    base.desk(t, 38, 2, 44)
    base.desk(t, 38, 2, 48)
    t.fill((4, 16, 24), (4, 16, 51), "create:fluid_pipe")
    t.fill((4, 10, 38), (58, 10, 38), "create:fluid_pipe")
    for x, top in ((11, 18), (24, 22), (36, 20), (43, 15), (57, 28)):
        t.fill((x, 10, 38), (x, top, 38), "create:fluid_pipe")
        t.set(x, 11, 39, "create:mechanical_pump", facing="south")
    for x, z, block in (
        (51, 29, "minecraft:barrel"), (62, 29, "oritech:cooler_block"),
        (51, 40, "create:fluid_tank"), (62, 40, "farmersdelight:rich_soil"),
    ):
        t.fill((x, 2, z), (x + 3, 5, z + 3), block)
    t.fill((55, 2, 33), (59, 6, 37), "immersiveengineering:sheetmetal_steel")
    for x, z in ((57, 29), (63, 35), (57, 41), (51, 35)):
        t.fill((x, 7, z), (57, 7, 35), "create:fluid_pipe")
    for x, z in ((50, 28), (64, 28), (50, 42), (64, 42)):
        t.set(x, 6, z, "create:encased_fan", facing="south")


def _pass12_institutional_identity(t: base.Template) -> None:
    base.wall_sign(t, 12, 7, 5, "north", "VERDANT CONTINUUM", "FOODS")
    base.wall_sign(t, 29, 7, 5, "north", "EP-7 AGRICULTURAL", "DEVELOPMENT LAB")
    base.wall_sign(t, 22, 5, 7, "south", "VISITOR RECEPTION", "OBSERVATION TOURS")
    base.wall_sign(t, 8, 5, 14, "south", "STAFF BADGE", "CONTROLLED ENTRY")
    base.wall_sign(t, 10, 6, 14, "north", "CHAMBER A", "REFERENCE CULTURE")
    base.wall_sign(t, 21, 6, 12, "north", "CHAMBER B", "DURABILITY STRESS")
    base.wall_sign(t, 34, 6, 15, "north", "CHAMBER C", "GERMINATION / RESEED")
    base.wall_sign(t, 8, 6, 51, "south", "SAMPLE RECEIVING", "LOT / ACCESSION")
    base.wall_sign(t, 19, 6, 51, "south", "ARCHIVE & HOLD", "COLD / DRY")
    base.wall_sign(t, 24, 6, 51, "south", "CLEAN PREPARATION", "BASELINE SAMPLE")
    base.wall_sign(t, 31, 6, 51, "south", "WASH / DECON", "SERVICE RETURN")
    base.wall_sign(t, 40, 6, 51, "south", "SECURE RECORDS", "RELEASE REVIEW")
    base.wall_sign(t, 10, 6, 40, "north", "PHENOTYPING", "SCAN / COMPARE")
    base.wall_sign(t, 28, 6, 40, "north", "RESEEDING", "GERMINATION LOOP")
    base.wall_sign(t, 38, 6, 40, "north", "FOOD QUALITY", "RELEASE DECISION")
    base.wall_sign(t, 41, 11, 29, "north", "DURABILITY ROTUNDA", "OBSERVATION BRIDGE")
    base.wall_sign(t, 49, 9, 35, "west", "ACCELERATED", "DURABILITY TESTS")
    base.wall_sign(t, 55, 8, 29, "north", "HEAT / DRY", "SECTOR A")
    base.wall_sign(t, 62, 8, 35, "east", "COLD / SOAK", "SECTOR B")
    base.wall_sign(t, 55, 14, 35, "west", "ANNULAR OVERLOOK", "AUTHORIZED STAFF")
    base.wall_sign(t, 3, 17, 28, "east", "ENVIRONMENTAL PLANT", "MAINTENANCE ONLY")
    base.wall_sign(t, 35, 7, 58, "south", "WASTE RETURN", "SEPARATE THRESHOLD")


def build_gate_b_r1() -> base.Template:
    t = build_gate_a_massing()
    _pass7_structural_system(t)
    _pass8_circulation_and_access(t)
    _pass9_exterior_architecture(t)
    _pass10_interior_architecture(t)
    _pass11_operational_systems(t)
    _pass12_institutional_identity(t)
    return t


def build_gate_b_r2() -> base.Template:
    t = build_gate_b_r1()
    for z in (22, 30, 38, 46, 48):
        t.fill((1, 4, z), (1, 19, z), "minecraft:white_concrete")
    t.fill((1, 11, 22), (1, 11, 48), "minecraft:light_gray_concrete")
    return t


def build_d1() -> base.Template:
    t = build_gate_b_r2()
    for z1, z2 in ((18, 27), (34, 43)):
        t.fill((18, 1, z1), (21, 1, z2), "minecraft:orange_concrete")
        t.fill((26, 1, z1), (29, 1, z2), "minecraft:yellow_concrete")
    t.fill((50, 1, 28), (54, 1, 32), "minecraft:orange_concrete")
    t.fill((60, 1, 28), (64, 1, 32), "minecraft:light_blue_concrete")
    t.fill((6, 13, 32), (24, 13, 32), "create:fluid_pipe")
    t.fill((24, 13, 32), (24, 17, 38), "create:fluid_pipe")
    t.fill((24, 17, 38), (57, 17, 38), "create:fluid_pipe")
    for x, z, facing in ((8, 32, "east"), (24, 35, "south"), (43, 38, "east")):
        t.set(x, 13 if x != 43 else 17, z, "create:mechanical_pump", facing=facing)
    t.fill((20, 6, 35), (21, 8, 37), "immersiveengineering:sheetmetal_steel")
    t.fill((26, 6, 35), (28, 8, 37), "oritech:cooler_block")
    t.fill((8, 2, 52), (10, 3, 54), "immersiveengineering:crate")
    t.fill((41, 2, 54), (42, 3, 54), "minecraft:barrel", facing="up", open="false")
    base.wall_sign(t, 18, 7, 33, "north", "EXTENDED CYCLE", "HEAT / DRY")
    base.wall_sign(t, 26, 7, 33, "north", "EXTENDED CYCLE", "COLD / SOAK")
    base.wall_sign(t, 41, 6, 54, "south", "PERSISTENCE RELEASE", "STOCK HOLD")
    base.wall_sign(t, 54, 8, 28, "north", "DURABILITY ROTUNDA", "EXTENDED RUN")
    return t


def build_accepted_d3() -> base.Template:
    """Return the independently accepted Gate-C r1 D3 before Pass 19."""
    t = build_d1()
    t.clear((21, 23, 27), (26, 23, 33))
    t.clear((20, 19, 26), (20, 22, 35))
    t.clear((27, 19, 34), (28, 21, 39))
    t.clear((19, 18, 34), (25, 18, 41))
    t.fill((19, 17, 34), (25, 17, 41), "minecraft:cracked_stone_bricks")
    for pos in ((21, 2, 36), (27, 2, 39), (19, 2, 41), (26, 3, 40), (28, 2, 35)):
        t.set(*pos, "minecraft:gravel")
    t.clear((8, 20, 46), (12, 25, 49))
    t.clear((5, 18, 45), (7, 21, 49))
    t.fill((7, 17, 45), (12, 17, 49), "minecraft:weathered_cut_copper")
    t.fill((8, 16, 46), (11, 16, 49), "minecraft:gravel")
    t.fill((5, 1, 38), (7, 1, 47), "minecraft:mossy_stone_bricks")
    for pos in ((6, 2, 39), (7, 2, 43), (5, 3, 46)):
        t.set(*pos, "minecraft:cobweb")
    t.fill((18, 1, 41), (21, 1, 45), "minecraft:mossy_stone_bricks")
    t.fill((26, 1, 40), (29, 1, 45), "minecraft:coarse_dirt")
    t.fill((30, 1, 52), (37, 1, 55), "minecraft:mossy_stone_bricks")
    t.clear((31, 8, 53), (37, 9, 57))
    t.fill((31, 7, 53), (37, 7, 55), "minecraft:cracked_stone_bricks")
    for pos in ((31, 2, 53), (35, 2, 54), (37, 2, 52)):
        t.set(*pos, "minecraft:brown_mushroom")
    t.clear((59, 24, 39), (62, 28, 40))
    t.clear((58, 29, 36), (61, 29, 39))
    t.fill((59, 23, 36), (62, 23, 39), "minecraft:weathered_cut_copper")
    t.fill((61, 1, 39), (65, 1, 43), "minecraft:mossy_stone_bricks")
    t.fill((62, 2, 40), (65, 2, 42), "farmersdelight:rich_soil")
    for pos, crop in (((62, 3, 40), "minecraft:wheat"), ((64, 3, 41), "minecraft:beetroots"), ((65, 3, 42), "minecraft:wheat")):
        t.set(*pos, crop)
    t.fill((20, 1, 42), (20, 1, 45), "minecraft:moss_block")
    t.fill((27, 1, 41), (28, 1, 44), "minecraft:moss_block")
    t.set(21, 3, 43, "minecraft:vine", north="false", east="true", south="false", west="false", up="false")
    t.set(62, 4, 41, "minecraft:vine", north="true", east="false", south="false", west="false", up="false")
    t.clear((42, 2, 55), (44, 4, 55))
    t.chest(*PROOF_POS, PROOF_LOOT_TABLE, facing="south")
    t.clear((4, 2, 35), (6, 3, 37))
    t.spawner(5, 2, 36, "minecraft:spider", count=1, nearby=3)
    t.clear((19, 2, 38), (21, 3, 40))
    t.spawner(20, 2, 39, "minecraft:zombie", count=1, nearby=4)
    t.clear((62, 2, 29), (64, 3, 31))
    t.spawner(63, 2, 30, "minecraft:skeleton", count=1, nearby=3)
    _assert_d3_contracts(t)
    return t


def _assert_corrected_facade(t: base.Template) -> None:
    for z in (22, 30, 38, 46, 48):
        for y in range(4, 20):
            expected = "minecraft:light_gray_concrete" if y == 11 else "minecraft:white_concrete"
            if _name(t, (1, y, z)) != expected:
                raise AssertionError(f"OWS-007 accepted facade lost at {(1, y, z)}")
    for z in range(22, 49):
        if _name(t, (1, 11, z)) != "minecraft:light_gray_concrete":
            raise AssertionError(f"OWS-007 accepted horizontal beam lost at z={z}")


def _assert_proof(t: base.Template) -> None:
    row = t.blocks.get(PROOF_POS)
    if row is None:
        raise AssertionError("OWS-007 canonical proof chest is missing")
    state_id, nbt = row
    if t.palette[state_id]["Name"] != "minecraft:chest":
        raise AssertionError(f"OWS-007 proof position contains {t.palette[state_id]['Name']}")
    if not nbt or nbt.get("LootTable") != PROOF_LOOT_TABLE:
        raise AssertionError("OWS-007 proof chest has the wrong canonical loot table")
    if _name(t, (43, 3, 55)) not in AIR or _name(t, (43, 2, 56)) not in AIR:
        raise AssertionError("OWS-007 proof node or south approach is obstructed")
    matching = sum(1 for _, nbt in t.blocks.values() if nbt and nbt.get("LootTable") == PROOF_LOOT_TABLE)
    if matching != 1:
        raise AssertionError(f"OWS-007 requires exactly one canonical proof node; found {matching}")


def _assert_d3_contracts(t: base.Template) -> None:
    if tuple(t.size) != (73, 33, 63):
        raise AssertionError(f"OWS-007 dimensions changed: {t.size}")
    _assert_proof(t)
    _assert_corrected_facade(t)
    if _count_block(t, "minecraft:spawner") != 3:
        raise AssertionError("OWS-007 requires exactly three bounded spawners")
    for x, z in ((24, 5), (24, 11), (9, 15), (11, 15), (22, 13), (35, 16), (11, 59), (35, 59)):
        for dx in (0, 1):
            for y in (2, 3):
                if _name(t, (x + dx, y, z)) != "minecraft:iron_door":
                    raise AssertionError(f"OWS-007 route lost controlled door at {(x + dx, y, z)}")
    if _count_block(t, "create:fluid_pipe") < 170:
        raise AssertionError("OWS-007 lost too much environmental-system anatomy")
    if _count_block(t, "farmersdelight:rich_soil") < 65:
        raise AssertionError("OWS-007 lost too much agricultural program evidence")
    signs = sum((_name(t, pos) or "").endswith("_wall_sign") for pos in t.blocks)
    if signs < 22:
        raise AssertionError(f"OWS-007 preserves too little identity: {signs} signs")


def _apply_pass19_microdetail(t: base.Template) -> None:
    for pos, block in PASS19_MICRODETAIL.items():
        if _name(t, pos) not in AIR:
            raise AssertionError(f"OWS-007 Pass-19 detail would overwrite accepted D3 at {pos}: {_name(t, pos)}")
        t.set(*pos, block)
    for pos, (before, after) in PASS19_REPLACEMENTS.items():
        if _name(t, pos) != before:
            raise AssertionError(f"OWS-007 Pass-19 replacement drift at {pos}: {_name(t, pos)} != {before}")
        t.set(*pos, after)


def _assert_final_contracts(t: base.Template) -> None:
    _assert_d3_contracts(t)
    for pos, expected in PASS19_MICRODETAIL.items():
        if _name(t, pos) != expected:
            raise AssertionError(f"OWS-007 Pass-19 detail drift at {pos}")
    for pos, (_, expected) in PASS19_REPLACEMENTS.items():
        if _name(t, pos) != expected:
            raise AssertionError(f"OWS-007 Pass-19 replacement drift at {pos}")
    if _count_block(t, "minecraft:mycelium") < 1:
        raise AssertionError("OWS-007 final production builder lacks required minecraft:mycelium")
    for pos in ((43, 2, 56), (23, 2, 42), (24, 2, 42), (36, 2, 56), (37, 2, 56)):
        if _name(t, pos) not in AIR and not (_name(t, pos) or "").endswith("_door"):
            raise AssertionError(f"OWS-007 Pass-19 obstructed protected route at {pos}")


def build_007() -> base.Template:
    """Build accepted D3 plus nine localized Pass-19 details, without I/O."""
    t = build_accepted_d3()
    _apply_pass19_microdetail(t)
    _assert_final_contracts(t)
    return t


if __name__ == "__main__":
    raise SystemExit("Import build_007 from the authoritative generator; this module performs no writes.")
