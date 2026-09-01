#!/usr/bin/env python3
"""Pure side-effect-free authoritative OWS-008 production builder.

The module reconstructs the independently accepted Gate-C r1 D3 geometry and
adds only the restrained Pass-19 overlay. It performs no rendering,
serialization, registry mutation, shipping write, or gate decision.
"""
from __future__ import annotations

import generate_wasteland_sites as base


SIZE = (55, 22, 49)
ACCEPTED_GATE_C_D3_SHA256 = "6de9ee39cde02c1ea298a7352c9b4eb6502a21ff6696b6c972795769efc33f36"
PROOF_LOOT_TABLE = "infinite_domain:chests/old_world/ows_008_vcf_emergency_persistence_investigation_lab"
PROOF_POS = (12, 14, 29)
SPAWNERS = {
    (51, 2, 24): "minecraft:zombie",
    (14, 2, 34): "minecraft:cave_spider",
    (14, 2, 41): "minecraft:spider",
}
AIR = {None, "minecraft:air", "minecraft:cave_air", "minecraft:void_air", "minecraft:structure_void"}
REQUIRED_BLOCKS = (
    "minecraft:lime_concrete",
    "minecraft:yellow_concrete",
    "create:framed_glass",
    "create:fluid_pipe",
    "minecraft:mycelium",
    "minecraft:brown_mushroom",
)
PASS19_MICRODETAIL = {
    (7, 3, 38): "minecraft:cobweb",
    (9, 2, 38): "minecraft:brown_mushroom",
    (18, 2, 42): "minecraft:red_mushroom",
    (28, 3, 41): "minecraft:cobweb",
    (36, 2, 42): "minecraft:brown_mushroom",
    (48, 2, 40): "minecraft:red_mushroom",
    (49, 3, 36): "minecraft:cobweb",
    (50, 2, 40): "minecraft:brown_mushroom",
}
WEST_COMMAND_STAIR_FLIGHTS = (
    (4, 2, 19, 5, "south"),
    (5, 2, 19, 5, "south"),
    (4, 8, 27, 5, "north"),
    (5, 8, 27, 5, "north"),
)
UPPER_PROOF_ROUTE = (
    (4, 2, 18),
    (4, 3, 19), (4, 4, 20), (4, 5, 21), (4, 6, 22), (4, 7, 23),
    (4, 8, 24), (3, 8, 24), (3, 8, 25), (3, 8, 26), (3, 8, 27),
    (3, 8, 28), (4, 8, 28),
    (4, 9, 27), (4, 10, 26), (4, 11, 25), (4, 12, 24), (4, 13, 23),
    (3, 14, 23), (3, 14, 24), (3, 14, 25), (4, 14, 25),
    (5, 14, 25), (6, 14, 25), (7, 14, 25), (8, 14, 25),
    (9, 14, 25), (10, 14, 25), (11, 14, 25), (12, 14, 25),
    (12, 14, 26), (12, 14, 27), (12, 14, 28),
)


def _name(t: base.Template, pos: tuple[int, int, int]) -> str | None:
    row = t.blocks.get(pos)
    return None if row is None else t.palette[row[0]]["Name"]


def _count(t: base.Template, block: str) -> int:
    return sum(_name(t, pos) == block for pos in t.blocks)


def _double_iron_door_z(t: base.Template, x: int, y: int, z: int, facing: str) -> None:
    t.clear((x, y, z), (x + 1, y + 2, z))
    base.double_door(t, x, y, z, facing, "iron")


def _double_iron_door_x(t: base.Template, x: int, y: int, z: int, facing: str) -> None:
    t.clear((x, y, z), (x, y + 2, z + 1))
    base.door(t, x, y, z, facing, "iron", "left")
    base.door(t, x, y, z + 1, facing, "iron", "right")


def _build_gate_a() -> base.Template:
    t = base.Template(SIZE)

    t.fill((0, 0, 0), (54, 0, 48), "minecraft:grass_block")
    t.fill((10, 0, 0), (43, 0, 12), "minecraft:smooth_stone")
    t.fill((24, 0, 0), (30, 0, 15), "minecraft:white_concrete")
    for x in (12, 41):
        t.fill((x, 0, 2), (x, 0, 10), "minecraft:lime_concrete")
    t.fill((47, 0, 9), (54, 0, 47), "tfmg:asphalt")
    t.fill((34, 0, 39), (54, 0, 48), "tfmg:asphalt")
    t.fill((51, 0, 12), (54, 0, 30), "minecraft:yellow_concrete")
    t.fill((0, 0, 13), (7, 0, 32), "minecraft:smooth_stone")
    t.fill((0, 0, 16), (4, 0, 20), "minecraft:lime_concrete")

    base.shell(t, (13, 1, 4), (41, 8, 14), "minecraft:white_concrete", "minecraft:smooth_stone", "minecraft:light_gray_concrete")
    t.fill((16, 2, 3), (38, 6, 3), "create:framed_glass")
    t.clear((24, 2, 3), (30, 5, 4))
    t.fill((17, 7, 3), (37, 8, 3), "minecraft:lime_concrete")
    t.fill((19, 8, 0), (35, 8, 6), "minecraft:white_concrete")
    for x in (19, 35):
        t.fill((x, 1, 1), (x, 7, 1), "minecraft:light_gray_concrete")
    base.shell(t, (7, 1, 12), (47, 9, 22), "minecraft:white_concrete", "minecraft:smooth_stone", "minecraft:light_gray_concrete")
    t.fill((10, 3, 22), (44, 7, 22), "create:framed_glass")
    for x in (10, 19, 29, 39, 44):
        t.fill((x, 1, 21), (x, 9, 22), "minecraft:light_gray_concrete")
    base.shell(t, (8, 9, 13), (21, 14, 21), "create:framed_glass", "minecraft:light_gray_concrete", "minecraft:white_concrete")

    cells = (
        ((6, 1, 24), (16, 14, 39), "minecraft:lime_concrete"),
        ((17, 1, 22), (27, 11, 37), "minecraft:white_concrete"),
        ((28, 1, 20), (39, 16, 36), "minecraft:yellow_concrete"),
        ((40, 1, 18), (50, 12, 34), "minecraft:cyan_concrete"),
    )
    for lo, hi, accent in cells:
        base.shell(t, lo, hi, "minecraft:white_concrete", "minecraft:smooth_stone", "minecraft:light_gray_concrete")
        x1, _, z1 = lo
        x2, y2, z2 = hi
        t.fill((x1 + 2, 3, z1 - 1), (x2 - 2, min(8, y2 - 2), z1 - 1), "create:framed_glass")
        for x in (x1, x2):
            t.fill((x, 1, z1 - 1), (x, y2, z1 - 1), "minecraft:light_gray_concrete")
        t.fill((x1 + 1, max(6, y2 - 3), z2), (x2 - 1, y2 - 1, z2), accent)
    base.shell(t, (8, 14, 28), (14, 18, 35), "create:framed_glass", "minecraft:light_gray_concrete", "minecraft:lime_concrete")
    base.shell(t, (19, 11, 26), (25, 15, 33), "minecraft:white_concrete", "minecraft:light_gray_concrete", "minecraft:white_concrete")
    base.shell(t, (30, 16, 24), (37, 20, 32), "immersiveengineering:sheetmetal_steel", "minecraft:light_gray_concrete", "minecraft:yellow_concrete")
    base.shell(t, (42, 12, 22), (48, 17, 29), "tfmg:steel_block", "minecraft:light_gray_concrete", "minecraft:cyan_concrete")

    base.shell(t, (2, 1, 12), (9, 12, 43), "minecraft:white_concrete", "minecraft:smooth_stone", "minecraft:light_gray_concrete")
    t.fill((1, 3, 16), (1, 8, 28), "create:framed_glass")
    for z in (15, 24, 33, 41):
        t.fill((1, 1, z), (2, 12, z), "minecraft:light_gray_concrete")
    base.shell(t, (2, 12, 17), (15, 17, 33), "minecraft:white_concrete", "minecraft:light_gray_concrete", "minecraft:lime_concrete")
    t.fill((15, 13, 20), (15, 16, 30), "create:framed_glass")
    base.shell(t, (48, 1, 10), (53, 10, 41), "minecraft:light_gray_concrete", "tfmg:factory_floor", "minecraft:white_concrete")
    t.clear((52, 2, 14), (53, 7, 21))
    t.fill((49, 8, 12), (54, 10, 23), "minecraft:yellow_concrete")
    t.fill((53, 3, 27), (53, 7, 36), "create:framed_glass")

    base.shell(t, (5, 1, 37), (51, 9, 46), "minecraft:light_gray_concrete", "tfmg:factory_floor", "minecraft:white_concrete")
    t.clear((5, 2, 40), (6, 6, 44))
    t.fill((3, 7, 39), (8, 9, 45), "minecraft:lime_concrete")
    t.clear((46, 2, 45), (51, 6, 46))
    t.fill((44, 7, 44), (52, 9, 47), "minecraft:yellow_concrete")
    base.shell(t, (8, 9, 39), (45, 12, 44), "immersiveengineering:sheetmetal_steel", "minecraft:light_gray_concrete", "minecraft:white_concrete")
    for x in (11, 22, 33, 43):
        t.fill((x, 12, 39), (x + 2, 15, 43), "tfmg:steel_block")
    base.shell(t, (46, 1, 34), (52, 18, 46), "minecraft:light_gray_concrete", "minecraft:smooth_stone", "minecraft:white_concrete")
    t.fill((45, 4, 37), (45, 15, 43), "create:framed_glass")
    return t


def _apply_gate_b(t: base.Template) -> None:
    for x in (13, 20, 27, 34, 41):
        t.fill((x, 1, 4), (x, 8, 4), "minecraft:light_gray_concrete")
        t.fill((x, 8, 4), (x, 8, 14), "minecraft:light_gray_concrete")
    for x in (7, 17, 27, 37, 47):
        t.fill((x, 1, 12), (x, 9, 12), "tfmg:steel_block")
        t.fill((x, 8, 12), (x, 9, 22), "tfmg:steel_block")
    for x1, x2, z1, z2, roof_y in ((6, 16, 24, 39, 14), (17, 27, 22, 37, 11), (28, 39, 20, 36, 16), (40, 50, 18, 34, 12)):
        for z in (z1, (z1 + z2) // 2, z2):
            t.fill((x1, 1, z), (x1, roof_y, z), "tfmg:steel_block")
            t.fill((x2, 1, z), (x2, roof_y, z), "tfmg:steel_block")
            t.fill((x1, roof_y - 1, z), (x2, roof_y, z), "tfmg:steel_block")
    for z in (12, 20, 28, 36, 43):
        t.fill((2, 1, z), (2, 12, z), "minecraft:light_gray_concrete")
        t.fill((9, 1, z), (9, 12, z), "minecraft:light_gray_concrete")
    for z in (10, 18, 26, 34, 41):
        t.fill((48, 1, z), (48, 10, z), "tfmg:steel_block")
        t.fill((53, 1, z), (53, 10, z), "tfmg:steel_block")
    for x in (5, 16, 27, 38, 51):
        t.fill((x, 1, 37), (x, 12, 37), "tfmg:steel_block")
        t.fill((x, 8, 37), (x, 9, 46), "tfmg:steel_block")
    t.fill((7, 11, 38), (46, 11, 45), "tfmg:steel_block")
    for z in (34, 40, 46):
        t.fill((46, 1, z), (46, 18, z), "tfmg:steel_block")
        t.fill((52, 1, z), (52, 18, z), "tfmg:steel_block")
    for x, z, top in ((13, 4, 8), (41, 4, 8), (6, 39, 14), (39, 36, 16), (50, 34, 12), (52, 44, 18)):
        t.fill((x, 1, z), (x, top, z), "create:fluid_pipe")

    t.clear((24, 2, 3), (30, 5, 4)); _double_iron_door_z(t, 26, 2, 4, "north")
    t.fill((24, 1, 4), (30, 1, 18), "minecraft:quartz_block")
    t.clear((24, 2, 12), (30, 5, 14)); _double_iron_door_z(t, 26, 2, 13, "south")
    t.clear((1, 2, 16), (2, 5, 20)); _double_iron_door_x(t, 2, 2, 18, "west")
    t.fill((3, 1, 14), (8, 1, 22), "minecraft:smooth_quartz")
    t.clear((52, 2, 13), (53, 6, 20)); _double_iron_door_x(t, 53, 2, 16, "east")
    t.clear((52, 2, 34), (53, 6, 39)); _double_iron_door_x(t, 53, 2, 36, "east")
    for x, front_z, inner_z in ((11, 24, 28), (22, 22, 26), (33, 20, 24), (45, 18, 22)):
        _double_iron_door_z(t, x, 2, front_z, "south"); _double_iron_door_z(t, x, 2, inner_z, "south")
    for x, z in ((39, 26), (27, 29), (16, 31)):
        _double_iron_door_x(t, x, 2, z, "west")
    _double_iron_door_x(t, 50, 2, 28, "east")
    for x, z in ((32, 36), (21, 37), (10, 39)):
        _double_iron_door_z(t, x, 2, z, "north")
    _double_iron_door_x(t, 5, 2, 41, "west"); _double_iron_door_z(t, 47, 2, 46, "south")
    for x in (4, 5): base.stair_flight(t, x, 2, 19, 5, "south", "minecraft:smooth_quartz_stairs")
    t.fill((3, 7, 23), (7, 7, 28), "minecraft:smooth_stone"); t.clear((3, 8, 22), (7, 13, 28))
    for x in (4, 5): base.stair_flight(t, x, 8, 27, 5, "north", "minecraft:smooth_quartz_stairs")
    t.fill((3, 13, 21), (7, 13, 24), "minecraft:smooth_stone")
    for x in (48, 49): base.stair_flight(t, x, 2, 36, 4, "south", "minecraft:smooth_quartz_stairs")
    t.fill((47, 6, 39), (51, 6, 43), "minecraft:smooth_stone")
    for x in (48, 49): base.stair_flight(t, x, 7, 42, 4, "north", "minecraft:smooth_quartz_stairs")
    t.fill((47, 11, 36), (51, 11, 40), "minecraft:smooth_stone")
    for x in (48, 49): base.stair_flight(t, x, 12, 37, 4, "south", "minecraft:smooth_quartz_stairs")
    t.fill((47, 16, 40), (51, 16, 44), "minecraft:smooth_stone"); _double_iron_door_x(t, 46, 16, 41, "west")

    t.fill((14, 3, 3), (23, 6, 3), "create:framed_glass"); t.fill((31, 3, 3), (40, 6, 3), "create:framed_glass")
    for x in (13, 20, 24, 31, 34, 41): t.fill((x, 1, 3), (x, 8, 4), "minecraft:light_gray_concrete")
    t.fill((0, 9, 15), (5, 9, 23), "minecraft:white_concrete")
    for z in (15, 23): t.fill((1, 1, z), (1, 8, z), "tfmg:steel_block")
    t.fill((0, 0, 15), (0, 0, 23), "minecraft:oxidized_copper_grate")
    t.fill((49, 9, 12), (54, 10, 23), "minecraft:yellow_concrete")
    t.fill((54, 0, 12), (54, 0, 23), "minecraft:oxidized_copper_grate")
    t.fill((53, 3, 27), (53, 7, 33), "create:framed_glass")
    for x1, x2 in ((7, 15), (19, 27), (31, 39), (43, 50)): t.fill((x1, 7, 47), (x2, 9, 47), "minecraft:oxidized_copper_grate")
    t.fill((6, 0, 46), (51, 0, 46), "minecraft:oxidized_copper_grate")
    for x1, x2, z, y, color in ((7, 15, 23, 10, "minecraft:lime_concrete"), (18, 26, 21, 7, "minecraft:white_concrete"), (29, 38, 19, 12, "minecraft:yellow_concrete"), (41, 49, 17, 8, "minecraft:cyan_concrete")):
        t.fill((x1, y, z), (x2, y + 1, z), color)

    t.fill((14, 1, 5), (40, 1, 13), "minecraft:quartz_block")
    base.partition_x(t, 23, 2, 5, 12, "minecraft:white_concrete", doorway_z=9)
    base.partition_x(t, 31, 2, 5, 12, "minecraft:white_concrete", doorway_z=9)
    t.fill((14, 2, 12), (22, 6, 12), "create:framed_glass"); t.fill((32, 2, 12), (40, 6, 12), "create:framed_glass")
    t.fill((8, 1, 14), (46, 1, 21), "minecraft:smooth_quartz"); t.fill((8, 1, 19), (46, 1, 20), "minecraft:lime_concrete")
    t.fill((3, 1, 13), (8, 1, 42), "minecraft:quartz_block")
    for z in (21, 29, 36): base.partition_z(t, z, 2, 3, 8, "minecraft:white_concrete", doorways=(6,))
    t.fill((3, 13, 18), (14, 13, 32), "minecraft:smooth_quartz")
    base.partition_x(t, 8, 14, 18, 32, "minecraft:white_concrete", doorway_z=25)
    # Restore the accepted west command/archive stair after its partitions and
    # landing slabs are resolved. Those later writes otherwise replace the
    # z=21 lower treads and the top headroom of both flights.
    for x, y, z, rise, facing in WEST_COMMAND_STAIR_FLIGHTS:
        base.stair_flight(t, x, y, z, rise, facing, "minecraft:smooth_quartz_stairs")
    t.fill((49, 1, 11), (52, 1, 40), "tfmg:factory_floor")
    for z in (21, 29, 35): base.partition_z(t, z, 2, 49, 52, "minecraft:light_gray_concrete", doorways=(51,))
    for x1, x2, z1, z2, partition_z, datum in ((6, 16, 24, 39, 28, "minecraft:lime_concrete"), (17, 27, 22, 37, 26, "minecraft:white_concrete"), (28, 39, 20, 36, 24, "minecraft:yellow_concrete"), (40, 50, 18, 34, 22, "minecraft:cyan_concrete")):
        t.fill((x1 + 1, 1, z1 + 1), (x2 - 1, 1, z2 - 1), "minecraft:smooth_quartz")
        t.fill((x1 + 1, 1, z1 + 1), (x2 - 1, 1, partition_z - 1), datum)
        base.partition_z(t, partition_z, 2, x1 + 1, x2 - 1, "minecraft:white_concrete")
        center = (x1 + x2) // 2
        t.clear((center, 2, partition_z), (center + 1, 4, partition_z)); base.double_door(t, center, 2, partition_z, "south", "iron")
    _double_iron_door_x(t, 50, 2, 28, "east")
    t.fill((6, 1, 38), (50, 1, 45), "tfmg:factory_floor")
    base.partition_x(t, 16, 2, 38, 45, "minecraft:light_gray_concrete"); base.partition_x(t, 39, 2, 38, 45, "minecraft:light_gray_concrete")
    for x in (16, 39): _double_iron_door_x(t, x, 2, 43, "east")

    t.fill((49, 2, 13), (51, 3, 15), "immersiveengineering:crate"); base.desk(t, 49, 2, 19, "north")
    for z in (23, 26):
        t.set(49, 2, z, "minecraft:brewing_stand", has_bottle_0="false", has_bottle_1="false", has_bottle_2="false")
        t.fill((51, 2, z), (52, 3, z), "create:framed_glass")
    t.fill((49, 2, 31), (51, 4, 33), "create:fluid_tank"); t.set(52, 2, 31, "minecraft:water_cauldron", level="3")
    t.fill((49, 2, 37), (52, 4, 39), "immersiveengineering:sheetmetal_steel")
    for x in (42, 47):
        t.fill((x, 2, 24), (x + 1, 5, 26), "create:fluid_tank"); t.set(x, 2, 29, "minecraft:water_cauldron", level="3")
    t.fill((41, 1, 31), (49, 1, 31), "minecraft:oxidized_copper_grate"); t.fill((41, 9, 24), (49, 9, 32), "create:fluid_pipe")
    t.set(44, 10, 28, "create:encased_fan", facing="south"); t.set(47, 10, 28, "create:encased_fan", facing="south")
    t.fill((30, 2, 27), (37, 7, 31), "create:framed_glass"); t.clear((31, 3, 28), (36, 6, 30)); t.clear((33, 2, 27), (34, 4, 31))
    for x in (30, 37): t.fill((x, 2, 32), (x + (1 if x == 30 else 0), 5, 34), "create:fluid_tank")
    t.fill((29, 12, 27), (38, 12, 34), "create:fluid_pipe"); t.set(33, 13, 30, "create:encased_fan", facing="south"); t.set(35, 13, 30, "create:encased_fan", facing="south")
    for x in (19, 23):
        t.fill((x, 2, 29), (x + 2, 4, 31), "oritech:cooler_block"); t.fill((x, 2, 34), (x + 2, 3, 35), "minecraft:smooth_quartz")
    t.fill((18, 8, 29), (26, 8, 35), "create:fluid_pipe"); t.set(21, 9, 32, "create:encased_fan", facing="south")
    t.fill((19, 2, 27), (21, 2, 27), "create:depot"); t.fill((23, 2, 27), (25, 2, 27), "create:depot")
    for z in (31, 35):
        t.fill((8, 2, z), (10, 2, z + 1), "farmersdelight:rich_soil"); t.fill((13, 2, z), (15, 2, z + 1), "farmersdelight:rich_soil")
        for x in (8, 10, 13, 15): t.set(x, 3, z, "minecraft:brown_mushroom")
    t.fill((7, 10, 30), (15, 10, 37), "create:fluid_pipe"); t.set(10, 11, 34, "create:encased_fan", facing="south"); t.fill((7, 4, 37), (15, 7, 37), "create:framed_glass")
    for x in (9, 20, 32, 41):
        t.fill((x, 2, 18), (x + 2, 2, 18), "create:depot"); t.set(x + 1, 3, 19, "ae2:terminal")
    for z in (23, 26):
        t.set(4, 2, z, "minecraft:brewing_stand", has_bottle_0="false", has_bottle_1="false", has_bottle_2="false"); t.set(7, 2, z, "ae2:terminal")
    t.fill((3, 2, 31), (5, 4, 34), "oritech:cooler_block"); t.fill((7, 2, 31), (8, 5, 34), "minecraft:bookshelf")
    for x, z in ((3, 20), (9, 20), (3, 28), (9, 28)): base.desk(t, x, 14, z, "north")
    t.fill((4, 14, 31), (7, 16, 32), "ae2:drive"); t.fill((10, 14, 31), (13, 16, 32), "minecraft:bookshelf")
    t.fill((7, 1, 40), (45, 1, 40), "minecraft:oxidized_copper_grate"); t.fill((7, 6, 41), (45, 6, 41), "create:fluid_pipe"); t.fill((7, 8, 44), (45, 8, 44), "create:fluid_pipe")
    for x in (13, 22, 33, 44):
        t.fill((x, 2, 39), (x + 1, 5, 39), "tfmg:steel_block"); t.fill((x, 4, 40), (x, 6, 44), "create:fluid_pipe")
        t.set(x + 1, 2, 42, "minecraft:lever", face="wall", facing="south", powered="false"); t.fill((x, 9, 40), (x + 2, 11, 43), "immersiveengineering:sheetmetal_steel")
    t.fill((7, 2, 44), (14, 4, 45), "create:fluid_tank"); t.fill((41, 2, 44), (49, 4, 45), "immersiveengineering:sheetmetal_steel")
    for x, top, z in ((11, 18, 39), (22, 15, 37), (33, 20, 36), (45, 17, 34)):
        t.fill((x, 6, z), (x, top, z), "create:fluid_pipe"); t.set(x, 7, min(44, z + 2), "create:mechanical_pump", facing="south")
    for x in (10, 16, 22, 28, 34, 40, 46): t.set(x, 7, 17, "minecraft:sea_lantern")
    for x, y, z in ((11, 11, 34), (22, 8, 32), (33, 13, 30), (45, 10, 28)): t.fill((x, y, z - 2), (x, y, z + 2), "minecraft:sea_lantern")

    t.fill((14, 7, 3), (40, 8, 3), "minecraft:lime_concrete"); t.fill((3, 1, 14), (8, 1, 16), "minecraft:lime_concrete"); t.fill((49, 1, 12), (52, 1, 20), "minecraft:yellow_concrete")
    for x, z, color in ((10, 24, "minecraft:lime_concrete"), (21, 22, "minecraft:white_concrete"), (33, 20, "minecraft:yellow_concrete"), (45, 18, "minecraft:cyan_concrete")):
        t.fill((x - 2, 1, z), (x + 3, 1, z + 2), color)
    signs = (
        (20, 7, 4, "north", "VERDANT CONTINUUM", "FOODS"), (33, 7, 4, "north", "PERSISTENCE", "INCIDENT LAB"),
        (24, 5, 6, "south", "INCIDENT LIAISON", "PUBLIC CHECK-IN"), (3, 6, 18, "east", "STAFF CLEAN ENTRY", "CHANGE / GOWN"),
        (51, 7, 16, "west", "INCIDENT RECEIVING", "SEALED MATERIAL"), (49, 6, 27, "north", "DIRTY EXAM", "CUSTODY ACTIVE"),
        (49, 6, 34, "north", "WASH / RETURN", "DIRTY SIDE"), (42, 6, 17, "north", "CELL A", "WET / THERMAL"),
        (30, 6, 19, "north", "CELL B", "VAPOR CYCLE"), (19, 6, 21, "north", "CELL C", "CLEAN HOLD"),
        (8, 6, 23, "north", "CELL D", "PERSISTENCE"), (9, 5, 16, "south", "VALIDATION GALLERY", "CYCLES A-D"),
        (4, 6, 20, "north", "CLEAN CHANGE", "STAFF ONLY"), (4, 6, 28, "north", "COMPARATIVE", "ANALYSIS"),
        (4, 6, 35, "north", "RETAINED SAMPLES", "CONTROLLED HOLD"), (3, 16, 18, "south", "INCIDENT COMMAND", "ACTIVE REVIEW"),
        (10, 16, 32, "north", "SECURE ARCHIVE", "AUTHORIZED DATA"), (18, 5, 38, "south", "JOINT INSPECTION", "SERVICE SPINE"),
        (31, 5, 38, "south", "PENETRATION TEST", "DRAIN / AIR / DATA"), (8, 5, 45, "south", "CLEAN SERVICES", "SUPPLY / WASH"),
        (42, 5, 45, "south", "DECON WASTE", "AUTHORIZED REMOVAL"), (46, 16, 40, "west", "ROOF PLANT", "MAINTENANCE ACCESS"),
    )
    for args in signs: base.wall_sign(t, *args)


def build_d0() -> base.Template:
    t = _build_gate_a()
    _apply_gate_b(t)
    return t


def build_d1() -> base.Template:
    t = build_d0()
    for x1, x2, color in ((7, 15, "minecraft:lime_concrete"), (18, 26, "minecraft:white_concrete"), (29, 38, "minecraft:yellow_concrete"), (41, 49, "minecraft:cyan_concrete")):
        t.fill((x1, 1, 38), (x2, 1, 40), color)
    for x, seal in ((13, "minecraft:lime_concrete"), (22, "minecraft:white_concrete"), (33, "minecraft:yellow_concrete"), (44, "minecraft:cyan_concrete")):
        t.fill((x - 2, 2, 40), (x - 2, 5, 40), "tfmg:steel_block"); t.fill((x + 2, 2, 40), (x + 2, 5, 40), "tfmg:steel_block")
        t.fill((x - 2, 5, 40), (x + 2, 5, 40), seal); t.fill((x - 1, 2, 40), (x + 1, 3, 40), "create:framed_glass"); t.set(x, 3, 40, "ae2:terminal")
    t.fill((8, 7, 42), (46, 7, 42), "create:fluid_pipe")
    for x in (11, 22, 33, 45):
        t.fill((x, 7, 39), (x, 7, 42), "create:fluid_pipe"); t.set(x, 7, 41, "create:mechanical_pump", facing="south")
    for x1, x2 in ((7, 10), (19, 21), (30, 32), (41, 43)):
        t.fill((x1, 2, 45), (x2, 4, 45), "immersiveengineering:sheetmetal_steel"); t.set(x2, 5, 45, "create:encased_fan", facing="south")
    t.fill((8, 12, 44), (45, 12, 44), "create:fluid_pipe")
    for x in (11, 22, 33, 45):
        t.fill((x, 8, 44), (x, 12, 44), "create:fluid_pipe"); t.set(x, 12, 44, "create:mechanical_pump", facing="east")
    for x in (9, 20, 31, 42):
        t.fill((x, 2, 41), (x + 1, 2, 41), "create:depot"); t.set(x, 3, 41, "minecraft:brewing_stand", has_bottle_0="false", has_bottle_1="false", has_bottle_2="false")
    for args in (
        (7, 5, 38, "south", "JOINT SAMPLE D", "SEAL GENERATION 4"), (18, 5, 38, "south", "JOINT SAMPLE C", "SURFACE NEGATIVE"),
        (29, 5, 38, "south", "JOINT SAMPLE B", "HIDDEN POSITIVE"), (41, 5, 38, "south", "JOINT SAMPLE A", "RETEST REQUIRED"),
        (31, 6, 45, "south", "BYPASS FILTRATION", "CONTINUOUS WATCH"), (3, 16, 27, "east", "INCIDENT STATUS", "CONTAINMENT HOLD"),
    ): base.wall_sign(t, *args)
    return t


def build_accepted_d3() -> base.Template:
    t = build_d1()
    for x1, x2 in ((7, 11), (14, 19), (24, 29), (35, 41), (45, 48)): t.fill((x1, 1, 40), (x2, 1, 42), "minecraft:mycelium")
    for pos in ((8, 2, 40), (10, 2, 42), (16, 2, 41), (27, 2, 40), (37, 2, 41), (41, 2, 40), (47, 2, 42)): t.set(*pos, "minecraft:brown_mushroom")
    for pos in ((12, 4, 40), (23, 4, 40), (34, 4, 40), (45, 4, 40)): t.set(*pos, "minecraft:vine", north="false", east="true", south="false", west="false", up="false")
    t.fill((41, 1, 32), (49, 1, 34), "minecraft:mossy_stone_bricks"); t.fill((48, 1, 29), (52, 1, 35), "minecraft:coarse_dirt"); t.fill((49, 1, 36), (52, 1, 40), "minecraft:moss_block")
    for pos in ((43, 2, 33), (48, 2, 34), (50, 2, 38), (52, 3, 37)): t.set(*pos, "minecraft:cobweb")
    t.clear((41, 11, 42), (45, 11, 45)); t.clear((46, 9, 42), (48, 10, 45)); t.fill((41, 10, 42), (45, 10, 45), "minecraft:weathered_cut_copper")
    for pos in ((42, 2, 42), (44, 2, 43), (46, 2, 44), (48, 2, 43), (49, 2, 45), (51, 1, 45)): t.set(*pos, "minecraft:gravel")
    t.clear((51, 9, 20), (53, 10, 22)); t.fill((50, 8, 20), (53, 8, 22), "minecraft:weathered_cut_copper")
    t.clear((47, 18, 43), (49, 18, 45)); t.fill((47, 17, 43), (49, 17, 45), "minecraft:weathered_cut_copper")
    for pos in ((52, 1, 20), (54, 1, 21), (53, 2, 22), (52, 11, 43), (53, 11, 44), (54, 11, 45)): t.set(*pos, "minecraft:gravel")
    t.clear((7, 6, 37), (9, 7, 37)); t.fill((7, 5, 38), (9, 5, 39), "minecraft:cracked_stone_bricks")
    for pos in ((7, 2, 38), (8, 2, 39), (15, 2, 38)): t.set(*pos, "minecraft:gravel")
    t.fill((41, 0, 43), (54, 0, 46), "minecraft:mossy_cobblestone"); t.fill((7, 0, 46), (15, 0, 47), "minecraft:mossy_cobblestone"); t.fill((28, 0, 46), (38, 0, 47), "minecraft:cracked_stone_bricks")
    t.chest(*PROOF_POS, PROOF_LOOT_TABLE, facing="north")
    for (x, y, z), mob in SPAWNERS.items(): t.spawner(x, y, z, mob, count=1, nearby=3 if "spider" in mob else 4)
    _assert_d3_contracts(t)
    return t


def _assert_proof(t: base.Template) -> None:
    row = t.blocks.get(PROOF_POS)
    if row is None or t.palette[row[0]]["Name"] != "minecraft:chest": raise AssertionError("OWS-008 canonical proof chest is missing")
    if not row[1] or row[1].get("LootTable") != PROOF_LOOT_TABLE: raise AssertionError("OWS-008 proof chest has the wrong loot table")
    if _name(t, (12, 15, 29)) not in AIR or _name(t, (12, 14, 28)) not in AIR: raise AssertionError("OWS-008 proof route is obstructed")
    matching = sum(1 for _, nbt in t.blocks.values() if nbt and nbt.get("LootTable") == PROOF_LOOT_TABLE)
    if matching != 1: raise AssertionError(f"OWS-008 requires one proof node; found {matching}")


def _assert_upper_proof_route(t: base.Template) -> None:
    expected_approach = (PROOF_POS[0], PROOF_POS[1], PROOF_POS[2] - 1)
    if UPPER_PROOF_ROUTE[0] != (4, 2, 18) or UPPER_PROOF_ROUTE[-1] != expected_approach:
        raise AssertionError("OWS-008 upper-proof route endpoints changed")
    for x, y, z, rise, facing in WEST_COMMAND_STAIR_FLIGHTS:
        dx, dz = {"south": (0, 1), "north": (0, -1)}[facing]
        for step in range(rise):
            tread = (x + dx * step, y + step, z + dz * step)
            if _name(t, tread) != "minecraft:smooth_quartz_stairs":
                raise AssertionError(f"OWS-008 west command stair tread changed at {tread}: {_name(t, tread)}")
            for head_y in (tread[1] + 1, tread[1] + 2):
                head = (tread[0], head_y, tread[2])
                if _name(t, head) not in AIR:
                    raise AssertionError(f"OWS-008 west command stair headroom obstructed at {head}: {_name(t, head)}")

    for previous, current in zip(UPPER_PROOF_ROUTE, UPPER_PROOF_ROUTE[1:]):
        horizontal = abs(current[0] - previous[0]) + abs(current[2] - previous[2])
        if horizontal != 1 or abs(current[1] - previous[1]) > 1:
            raise AssertionError(f"OWS-008 upper-proof route has an invalid step: {previous} -> {current}")
    for feet in UPPER_PROOF_ROUTE:
        feet_name = _name(t, feet)
        head = (feet[0], feet[1] + 1, feet[2])
        head_name = _name(t, head)
        if feet_name not in AIR and not (feet_name or "").endswith("_door"):
            raise AssertionError(f"OWS-008 upper-proof route feet obstructed at {feet}: {feet_name}")
        if head_name not in AIR and not (head_name or "").endswith("_door"):
            raise AssertionError(f"OWS-008 upper-proof route head obstructed at {head}: {head_name}")
        support = (feet[0], feet[1] - 1, feet[2])
        if _name(t, support) in AIR:
            raise AssertionError(f"OWS-008 upper-proof route lacks support below {feet}")


def _assert_d3_contracts(t: base.Template) -> None:
    if tuple(t.size) != SIZE: raise AssertionError(f"OWS-008 dimensions changed: {t.size}")
    if any(not (0 <= x < 55 and 0 <= y < 22 and 0 <= z < 49) for x, y, z in t.blocks): raise AssertionError("OWS-008 exceeds accepted bounds")
    _assert_proof(t)
    _assert_upper_proof_route(t)
    if _count(t, "minecraft:spawner") != 3: raise AssertionError("OWS-008 requires three bounded spawners")
    for pos in SPAWNERS:
        row = t.blocks.get(pos)
        if row is None or t.palette[row[0]]["Name"] != "minecraft:spawner": raise AssertionError(f"OWS-008 spawner missing at {pos}")
        if sum(abs(a - b) for a, b in zip(pos, PROOF_POS)) < 12: raise AssertionError(f"OWS-008 spawner too close to proof at {pos}")
    for x, z in ((26, 4), (26, 13), (11, 24), (11, 28), (22, 22), (22, 26), (33, 20), (33, 24), (45, 18), (45, 22), (32, 36), (21, 37), (10, 39), (47, 46)):
        for dx in (0, 1):
            for y in (2, 3):
                if _name(t, (x + dx, y, z)) != "minecraft:iron_door": raise AssertionError(f"OWS-008 lost door at {(x + dx, y, z)}")
    for x, z in ((2, 18), (53, 16), (53, 36), (39, 26), (27, 29), (16, 31), (50, 28), (5, 41), (16, 43), (39, 43)):
        for dz in (0, 1):
            for y in (2, 3):
                if _name(t, (x, y, z + dz)) != "minecraft:iron_door": raise AssertionError(f"OWS-008 lost door at {(x, y, z + dz)}")
    if _count(t, "create:fluid_pipe") < 480 or _count(t, "create:fluid_tank") < 140: raise AssertionError("OWS-008 lost required service systems")
    if _count(t, "minecraft:smooth_quartz_stairs") < 36: raise AssertionError("OWS-008 lost vertical circulation")
    if sum((_name(t, pos) or "").endswith("_wall_sign") for pos in t.blocks) < 24: raise AssertionError("OWS-008 lost institutional signs")
    for block in REQUIRED_BLOCKS:
        if _count(t, block) < 1: raise AssertionError(f"OWS-008 lacks required block {block}")


def _apply_pass19_microdetail(t: base.Template) -> None:
    for pos, block in PASS19_MICRODETAIL.items():
        if _name(t, pos) not in AIR: raise AssertionError(f"OWS-008 Pass-19 detail would overwrite D3 at {pos}: {_name(t, pos)}")
        t.set(*pos, block)


def _assert_final_contracts(t: base.Template) -> None:
    _assert_d3_contracts(t)
    for pos, expected in PASS19_MICRODETAIL.items():
        if _name(t, pos) != expected: raise AssertionError(f"OWS-008 Pass-19 drift at {pos}")
    protected = ((25, 2, 5), (27, 2, 15), (11, 2, 30), (22, 2, 29), (33, 2, 27), (45, 2, 25), (28, 2, 44), (12, 14, 28))
    for pos in protected:
        if _name(t, pos) not in AIR and _name(t, pos) != "minecraft:iron_door": raise AssertionError(f"OWS-008 protected route obstructed at {pos}")


def build_008() -> base.Template:
    """Return accepted D3 plus eight localized Pass-19 details, without I/O."""
    t = build_accepted_d3()
    _apply_pass19_microdetail(t)
    _assert_final_contracts(t)
    return t


if __name__ == "__main__":
    raise SystemExit("Import build_008 from the authoritative generator; this module performs no writes.")
