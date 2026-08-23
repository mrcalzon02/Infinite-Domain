#!/usr/bin/env python3
"""Pure side-effect-free authoritative OWS-009 production builder.

This module reconstructs the independently accepted Gate-C r1 D3 model and
adds only the restrained Pass-19 overlay. It performs no rendering,
serialization, filesystem access, registry mutation, shipping write, or gate
decision. The shared coordinator may import ``build_009`` for generation.
"""
from __future__ import annotations

import generate_wasteland_sites as base


SIZE = (49, 18, 41)
ACCEPTED_GATE_C_D3_SHA256 = "42835cb4b926a8445b66016fa5d21f5219ec38386bc4dc2b941585ab5924b578"
PROOF_LOOT_TABLE = "infinite_domain:chests/old_world/ows_009_atlas_roadside_repair_depot"
PROOF_POS = (37, 2, 29)
SPAWNERS = {
    (6, 2, 21): "minecraft:zombie",
    (23, 2, 21): "minecraft:zombie",
    (43, 2, 33): "minecraft:cave_spider",
}
AIR = {None, "minecraft:air", "minecraft:cave_air", "minecraft:void_air", "minecraft:structure_void"}
REQUIRED_BLOCKS = (
    "tfmg:steel_block",
    "create:framed_glass",
    "create:fluid_pipe",
    "minecraft:oxidized_copper_grate",
    "minecraft:moss_block",
    "minecraft:weathered_cut_copper",
)
PRODUCTION_REQUIRED_BLOCKS = ("create:andesite_casing",) + REQUIRED_BLOCKS
PASS19_MICRODETAIL = {
    (34, 2, 28): "create:andesite_casing",
    (32, 3, 33): "minecraft:cobweb",
    (34, 3, 26): "minecraft:cobweb",
    (41, 3, 33): "minecraft:cobweb",
    (37, 1, 37): "minecraft:red_mushroom",
    (40, 1, 38): "minecraft:brown_mushroom",
    (41, 1, 37): "minecraft:brown_mushroom",
    (44, 1, 36): "minecraft:red_mushroom",
    (46, 1, 28): "minecraft:brown_mushroom",
}


def _name(t: base.Template, pos: tuple[int, int, int]) -> str | None:
    row = t.blocks.get(pos)
    return None if row is None else t.palette[row[0]]["Name"]


def _count(t: base.Template, block: str) -> int:
    return sum(_name(t, pos) == block for pos in t.blocks)


def _shell(t: base.Template, a: tuple[int, int, int], b: tuple[int, int, int], wall: str, roof: str) -> None:
    base.shell(t, a, b, wall, "tfmg:factory_floor", roof)


def _double_door_z(t: base.Template, x: int, y: int, z: int, facing: str) -> None:
    t.clear((x, y, z), (x + 1, y + 2, z)); base.double_door(t, x, y, z, facing, "iron")


def _double_door_x(t: base.Template, x: int, y: int, z: int, facing: str) -> None:
    t.clear((x, y, z), (x, y + 2, z + 1))
    base.door(t, x, y, z, facing, "iron", "left"); base.door(t, x, y, z + 1, facing, "iron", "right")


def _build_gate_a_r1() -> base.Template:
    t = base.Template(SIZE)
    t.fill((0, 0, 0), (48, 0, 40), "minecraft:grass_block")
    t.fill((1, 0, 0), (35, 0, 7), "tfmg:asphalt")
    for x1, x2 in ((5, 13), (15, 24), (26, 34)):
        t.fill((x1, 0, 1), (x2, 0, 6), "minecraft:light_gray_concrete")
        t.fill((x1, 0, 3), (x2, 0, 3), "minecraft:yellow_concrete")
    t.fill((36, 0, 0), (47, 0, 19), "minecraft:smooth_stone")
    t.fill((39, 0, 0), (44, 0, 7), "minecraft:white_concrete")
    t.fill((45, 0, 18), (48, 0, 39), "tfmg:asphalt")
    t.fill((36, 0, 35), (44, 0, 39), "minecraft:coarse_dirt")
    t.fill((36, 0, 35), (44, 0, 35), "minecraft:yellow_concrete")

    _shell(t, (3, 1, 7), (14, 11, 34), "tfmg:cinder_block", "minecraft:smooth_stone")
    _shell(t, (14, 1, 7), (25, 13, 34), "minecraft:light_gray_concrete", "minecraft:smooth_stone")
    _shell(t, (25, 1, 7), (35, 12, 34), "tfmg:cinder_block", "minecraft:smooth_stone")
    t.clear((14, 2, 8), (14, 9, 31)); t.clear((25, 2, 8), (25, 9, 31))
    for x1, x2, top in ((5, 12, 6), (16, 23, 7), (27, 33, 6)):
        t.clear((x1, 2, 7), (x2, top, 8))
        t.fill((x1 - 1, 1, 6), (x1 - 1, top + 2, 8), "tfmg:steel_block")
        t.fill((x2 + 1, 1, 6), (x2 + 1, top + 2, 8), "tfmg:steel_block")
        t.fill((x1 - 1, top + 1, 6), (x2 + 1, top + 2, 8), "minecraft:orange_concrete")
    for x1, x2 in ((5, 13), (15, 24), (26, 34)):
        t.fill((x1, 1, 9), (x2, 1, 23), "minecraft:smooth_stone")
        t.fill((x1, 1, 9), (x1, 1, 23), "minecraft:orange_concrete")
        t.fill((x2, 1, 9), (x2, 1, 23), "minecraft:orange_concrete")
    t.fill((4, 1, 24), (35, 1, 27), "minecraft:light_gray_concrete")
    t.fill((4, 1, 28), (35, 1, 31), "minecraft:polished_blackstone")
    t.fill((3, 7, 10), (3, 9, 25), "create:framed_glass")
    t.fill((35, 8, 10), (35, 10, 25), "create:framed_glass")
    t.fill((16, 10, 7), (23, 11, 7), "create:framed_glass")
    for x1, x2, y in ((6, 12, 8), (17, 23, 10), (28, 33, 9)):
        t.fill((x1, y, 34), (x2, y + 1, 34), "create:framed_glass")

    _shell(t, (36, 1, 7), (44, 9, 19), "minecraft:white_concrete", "minecraft:light_gray_concrete")
    t.fill((37, 3, 7), (43, 6, 7), "create:framed_glass")
    t.fill((36, 3, 9), (36, 6, 17), "create:framed_glass")
    t.clear((39, 2, 7), (42, 5, 8)); t.fill((38, 7, 6), (44, 8, 8), "minecraft:orange_concrete")
    _shell(t, (36, 1, 20), (44, 10, 27), "immersiveengineering:sheetmetal_steel", "tfmg:steel_block")
    _shell(t, (36, 1, 27), (44, 11, 34), "minecraft:polished_blackstone_bricks", "tfmg:steel_block")
    t.clear((44, 2, 22), (44, 6, 26))
    t.fill((44, 1, 21), (44, 8, 21), "minecraft:orange_concrete")
    t.fill((44, 1, 27), (44, 8, 27), "minecraft:orange_concrete")
    t.fill((37, 7, 28), (43, 9, 28), "create:framed_glass")
    t.clear((35, 2, 12), (36, 4, 14)); t.clear((35, 2, 23), (36, 5, 25)); t.clear((35, 2, 29), (36, 5, 31))

    for x1, x2, floor_y, top_y in ((6, 12, 11, 15), (17, 23, 13, 17), (28, 34, 12, 16)):
        _shell(t, (x1, floor_y, 28), (x2, top_y, 33), "immersiveengineering:sheetmetal_steel", "tfmg:steel_block")
        t.fill((x1 + 1, floor_y + 1, 27), (x2 - 1, top_y - 1, 27), "create:framed_glass")
    t.fill((8, 14, 32), (32, 15, 33), "minecraft:orange_concrete")
    t.fill((12, 12, 6), (29, 14, 7), "tfmg:steel_block")
    t.fill((14, 13, 5), (27, 16, 6), "minecraft:orange_concrete")
    t.fill((18, 14, 4), (23, 16, 5), "minecraft:polished_blackstone")
    return t


def _apply_gate_a_r2(t: base.Template) -> None:
    steel = "tfmg:steel_block"
    for z, top in ((7, 11), (15, 11), (24, 11), (31, 11), (34, 11)):
        t.fill((2, 1, z), (3, top, min(z + 1, 34)), steel)
    for z1, z2 in ((9, 14), (17, 23), (26, 30)):
        t.fill((3, 2, z1), (3, 5, z2), "minecraft:light_gray_concrete")
    t.fill((2, 6, 9), (2, 6, 30), "minecraft:orange_concrete"); t.fill((2, 10, 25), (3, 11, 33), steel)
    for x, top in ((3, 11), (14, 12), (25, 12), (35, 12)):
        t.fill((x, 1, 34), (min(x + 1, 35), top, 35), steel)
    t.fill((4, 10, 35), (34, 11, 36), steel); t.fill((5, 12, 35), (33, 12, 35), "minecraft:orange_concrete")
    for x1, x2, y in ((6, 12, 8), (17, 23, 10), (28, 33, 9)):
        t.fill((x1 - 1, y - 1, 35), (x2 + 1, y + 2, 35), steel)
        t.fill((x1, y, 34), (x2, y + 1, 34), "create:framed_glass")
    t.fill((5, 12, 35), (33, 12, 35), "minecraft:orange_concrete")

    t.fill((4, 8, 5), (13, 9, 6), steel); t.fill((5, 8, 4), (12, 8, 5), "minecraft:orange_concrete")
    _shell(t, (6, 11, 13), (12, 13, 22), steel, "minecraft:light_gray_concrete"); t.fill((7, 12, 12), (11, 12, 12), "create:framed_glass")
    t.fill((15, 9, 5), (24, 10, 6), steel); t.fill((16, 9, 4), (23, 9, 5), "minecraft:orange_concrete")
    _shell(t, (17, 13, 11), (23, 16, 23), steel, "minecraft:light_gray_concrete"); t.fill((18, 14, 10), (22, 15, 10), "create:framed_glass")
    t.fill((19, 16, 8), (21, 17, 12), "minecraft:orange_concrete")
    t.fill((26, 7, 5), (34, 8, 6), steel); t.fill((27, 7, 4), (34, 7, 5), "minecraft:orange_concrete")
    _shell(t, (29, 12, 15), (34, 14, 25), steel, "minecraft:light_gray_concrete"); t.fill((28, 12, 17), (28, 13, 23), "create:framed_glass")

    t.fill((44, 1, 21), (45, 8, 22), steel); t.fill((44, 1, 26), (45, 8, 27), steel)
    t.fill((44, 7, 21), (46, 8, 27), steel); t.fill((45, 8, 22), (46, 8, 26), "minecraft:orange_concrete")
    t.clear((44, 2, 23), (45, 6, 25))
    t.clear((37, 2, 34), (42, 5, 35)); t.fill((36, 1, 33), (37, 7, 36), "minecraft:polished_blackstone")
    t.fill((42, 1, 33), (43, 7, 36), "minecraft:polished_blackstone"); t.fill((36, 6, 33), (43, 7, 36), steel)
    t.fill((38, 7, 35), (41, 7, 36), "minecraft:orange_concrete")


def build_gate_a() -> base.Template:
    t = _build_gate_a_r1(); _apply_gate_a_r2(t); return t


def _pass7_structural_system(t: base.Template) -> None:
    for x, roof_y in ((4, 9), (14, 10), (25, 10), (35, 9)):
        for z in (9, 16, 23, 32): t.fill((x, 1, z), (x, roof_y, z), "tfmg:steel_block")
    for x1, x2, beam_y in ((4, 14, 9), (14, 25, 10), (25, 35, 9)):
        for z in (10, 16, 23, 32): t.fill((x1, beam_y, z), (x2, beam_y + 1, z), "tfmg:steel_block")
    for x1, x2, y, z1, z2 in ((6, 12, 10, 12, 23), (17, 23, 12, 10, 25), (28, 34, 11, 14, 27)):
        t.fill((x1, y, z1), (x1, y, z2), "tfmg:steel_block"); t.fill((x2, y, z1), (x2, y, z2), "tfmg:steel_block")
    for z, top in ((8, 8), (19, 8), (20, 9), (27, 10), (34, 10)):
        t.fill((36, 1, z), (36, top, z), "tfmg:steel_block"); t.fill((44, 1, z), (44, top, z), "tfmg:steel_block")
        t.fill((36, top, z), (44, top, z), "tfmg:steel_block")


def _pass8_circulation_and_access(t: base.Template) -> None:
    for x1, x2, color in ((7, 11, "minecraft:cyan_concrete"), (18, 22, "minecraft:orange_concrete"), (28, 32, "minecraft:white_concrete")):
        t.fill((x1, 1, 8), (x2, 1, 23), "minecraft:smooth_stone")
        t.fill((x1, 1, 9), (x1, 1, 22), color); t.fill((x2, 1, 9), (x2, 1, 22), color)
    t.fill((4, 1, 24), (34, 1, 27), "minecraft:light_gray_concrete"); t.fill((4, 1, 25), (34, 1, 26), "minecraft:yellow_concrete")
    t.fill((4, 1, 28), (34, 1, 31), "minecraft:polished_blackstone"); t.fill((4, 1, 29), (34, 1, 30), "tfmg:factory_floor")
    _double_door_z(t, 40, 2, 7, "north"); _double_door_x(t, 35, 2, 13, "east")
    _double_door_x(t, 35, 2, 23, "east"); _double_door_x(t, 35, 2, 29, "east")
    _double_door_x(t, 44, 2, 23, "east"); _double_door_z(t, 39, 2, 34, "south")
    t.fill((39, 1, 8), (42, 1, 13), "minecraft:white_concrete"); t.fill((37, 1, 13), (42, 1, 14), "minecraft:cyan_concrete")
    t.fill((37, 1, 23), (43, 1, 25), "minecraft:orange_concrete"); t.fill((39, 1, 29), (40, 1, 33), "minecraft:yellow_concrete")


def _pass9_exterior_architecture(t: base.Template) -> None:
    t.fill((3, 6, 11), (3, 8, 14), "create:framed_glass"); t.fill((3, 6, 18), (3, 8, 21), "create:framed_glass")
    t.fill((15, 9, 7), (23, 11, 7), "create:framed_glass"); t.fill((35, 7, 12), (35, 9, 16), "create:framed_glass")
    t.fill((35, 7, 19), (35, 9, 22), "create:framed_glass")
    for x, z, top in ((3, 10, 10), (3, 27, 10), (14, 33, 11), (25, 33, 11), (35, 18, 11), (44, 18, 8), (44, 29, 10)):
        t.fill((x, 1, z), (x, top, z), "create:fluid_pipe")
    t.fill((4, 0, 33), (34, 0, 33), "minecraft:oxidized_copper_grate"); t.fill((45, 0, 22), (48, 0, 22), "minecraft:oxidized_copper_grate")
    for x, y, z in ((5, 7, 6), (13, 7, 6), (16, 8, 6), (23, 8, 6), (27, 7, 6), (34, 7, 6), (39, 7, 7), (43, 7, 7), (45, 7, 22), (45, 7, 26), (38, 6, 34), (42, 6, 34)):
        t.set(x, y, z, "minecraft:redstone_lamp", lit="true")


def _pass10_interior_architecture(t: base.Template) -> None:
    t.fill((37, 1, 8), (43, 1, 18), "minecraft:smooth_quartz"); base.partition_z(t, 15, 2, 37, 43, "minecraft:white_concrete")
    _double_door_z(t, 40, 2, 15, "south"); t.fill((37, 2, 15), (39, 5, 15), "create:framed_glass"); t.fill((42, 2, 15), (43, 5, 15), "create:framed_glass")
    t.fill((37, 1, 21), (43, 1, 26), "tfmg:factory_floor"); base.partition_x(t, 40, 2, 21, 26, "minecraft:light_gray_concrete")
    _double_door_x(t, 40, 2, 23, "west")
    t.fill((37, 1, 28), (43, 1, 33), "minecraft:polished_blackstone"); base.partition_z(t, 31, 2, 37, 43, "minecraft:light_gray_concrete")
    _double_door_z(t, 39, 2, 31, "south"); base.partition_x(t, 41, 2, 28, 30, "minecraft:polished_blackstone_bricks", doorway_z=29)
    base.door(t, 41, 2, 29, "east", "iron", "left")
    for x, z1, z2 in ((5, 11, 22), (13, 11, 22), (16, 11, 22), (24, 11, 22), (27, 11, 22), (34, 11, 22)):
        t.fill((x, 2, z1), (x, 4, z1 + 1), "create:framed_glass"); t.fill((x, 2, z2 - 1), (x, 4, z2), "create:framed_glass")


def _pass11_operational_systems(t: base.Template) -> None:
    for z in (12, 19):
        t.fill((5, 2, z), (5, 6, z), "tfmg:steel_block"); t.fill((13, 2, z), (13, 6, z), "tfmg:steel_block")
        t.fill((5, 6, z), (13, 7, z), "minecraft:cyan_concrete")
        t.set(6, 5, z, "minecraft:observer", facing="east"); t.set(12, 5, z, "minecraft:observer", facing="west")
    for z in (13, 16, 20):
        t.set(7, 1, z, "create:depot"); t.set(11, 1, z, "create:depot")
    t.fill((5, 2, 15), (5, 3, 17), "ae2:drive"); t.set(6, 2, 16, "ae2:terminal")
    t.fill((12, 2, 15), (13, 3, 17), "immersiveengineering:sheetmetal_steel")
    t.fill((18, 0, 13), (22, 0, 20), "minecraft:polished_blackstone"); t.fill((18, 1, 13), (22, 1, 20), "minecraft:oxidized_copper_grate")
    for x in (16, 24):
        for z in (12, 20):
            t.fill((x, 2, z), (x, 6, z), "tfmg:steel_block"); t.set(x, 3, z, "create:mechanical_pump", facing="up")
    t.fill((16, 8, 16), (24, 9, 16), "tfmg:steel_block")
    for x in (18, 21):
        t.fill((x, 6, 16), (x, 8, 16), "minecraft:chain"); t.set(x, 5, 16, "create:depot")
    for z in (11, 14, 19, 22):
        t.set(16, 2, z, "create:depot"); t.set(24, 2, z, "create:depot")
    t.set(16, 3, 17, "create:mechanical_press", facing="east"); t.set(24, 3, 17, "create:mechanical_press", facing="west")
    for z in (13, 16, 19): t.fill((28, 1, z), (32, 1, z), "create:shaft")
    t.fill((27, 2, 20), (27, 6, 20), "tfmg:steel_block"); t.fill((34, 2, 20), (34, 6, 20), "tfmg:steel_block")
    t.fill((27, 6, 20), (34, 7, 20), "minecraft:orange_concrete")
    for x in (28, 33):
        t.set(x, 5, 20, "minecraft:observer", facing="south"); t.set(x, 2, 22, "ae2:terminal")
    t.fill((33, 2, 12), (34, 4, 16), "immersiveengineering:capacitor_mv"); t.set(33, 2, 18, "create:mechanical_pump", facing="west")
    t.fill((37, 2, 21), (39, 4, 22), "immersiveengineering:crate"); t.fill((37, 2, 25), (39, 3, 26), "immersiveengineering:crate")
    for z in (21, 26): t.set(42, 2, z, "create:depot")
    t.set(42, 4, 24, "ae2:terminal"); t.fill((42, 2, 28), (43, 4, 30), "ae2:drive"); t.set(41, 2, 28, "ae2:terminal")
    t.fill((37, 2, 32), (38, 4, 33), "immersiveengineering:sheetmetal_steel"); t.fill((42, 2, 32), (43, 4, 33), "immersiveengineering:sheetmetal_steel")
    base.desk(t, 37, 2, 13, "north"); t.set(38, 3, 13, "ae2:terminal")
    for x in (37, 43):
        t.fill((x, 2, 9), (x, 2, 11), "minecraft:smooth_quartz_stairs", facing="east" if x == 37 else "west", half="bottom", shape="straight", waterlogged="false")
    t.fill((5, 7, 30), (34, 7, 30), "create:fluid_pipe"); t.fill((5, 8, 32), (34, 8, 32), "immersiveengineering:sheetmetal_steel")
    for x, top in ((9, 14), (20, 16), (31, 15)):
        t.fill((x, 7, 15), (x, 7, 30), "create:fluid_pipe"); t.fill((x, 7, 30), (x, top, 30), "create:fluid_pipe")
        t.set(x, 8, 27, "create:mechanical_pump", facing="south"); t.set(x, top - 1, 29, "create:encased_fan", facing="south")
    for x in (6, 17, 28):
        t.fill((x, 2, 32), (x + 2, 4, 33), "immersiveengineering:capacitor_mv"); t.set(x + 1, 5, 32, "immersiveengineering:connector_lv", facing="up")
    for x in (6, 13, 17, 24, 27, 33):
        t.fill((x, 1, 10), (x, 1, 23), "minecraft:oxidized_copper_grate"); t.fill((x, 1, 23), (x, 1, 28), "minecraft:oxidized_copper_grate")
    for x in (6, 10, 18, 22, 28, 32):
        t.set(x, 8, 14, "minecraft:sea_lantern"); t.set(x, 8, 21, "minecraft:sea_lantern")
    for x in (7, 13, 19, 25, 31): t.set(x, 7, 29, "minecraft:sea_lantern")


def _pass12_atlas_identity(t: base.Template) -> None:
    for x1, x2, y in ((5, 13, 7), (16, 24, 8), (27, 34, 7)):
        t.fill((x1, y, 9), (x2, y + 1, 9), "minecraft:polished_blackstone")
        t.fill((x1 + 1, y, 10), (x2 - 1, y, 10), "minecraft:orange_concrete")
    t.fill((4, 4, 28), (34, 5, 28), "minecraft:orange_concrete")
    signs = (
        (6, 6, 7, "north", "ATLAS SERVICE", "DIAGNOSTICS / 01"),
        (17, 7, 7, "north", "ATLAS SERVICE", "HEAVY REPAIR / 02"),
        (28, 6, 7, "north", "ATLAS SERVICE", "CALIBRATE / 03"),
        (38, 6, 7, "north", "CUSTOMER SERVICE", "CHECK-IN"),
        (35, 5, 13, "west", "SERVICE HANDOFF", "STAFF CONTROL"),
        (44, 6, 23, "west", "PARTS RECEIVE", "DELIVERY CONTROL"),
        (36, 5, 23, "east", "PARTS ISSUE", "TECHNICIANS"),
        (36, 5, 29, "east", "SERVICE RECORDS", "CONTROLLED"),
        (42, 5, 28, "west", "PROOF NODE", "RECORDS ADJACENT"),
        (39, 5, 34, "north", "CORE / REWORK", "QUARANTINE RETURN"),
        (7, 6, 23, "south", "TRANSVERSE FIELD", "KEEP CLEAR"),
        (7, 6, 31, "south", "TECHNICIAN SPINE", "AIR / POWER / DATA"),
        (18, 6, 20, "north", "INSPECTION PIT", "LIFT LOCKOUT"),
        (28, 6, 20, "north", "LOAD TEST", "CALIBRATION"),
    )
    for args in signs: base.wall_sign(t, *args)


def build_d0() -> base.Template:
    t = build_gate_a()
    _pass7_structural_system(t); _pass8_circulation_and_access(t); _pass9_exterior_architecture(t)
    _pass10_interior_architecture(t); _pass11_operational_systems(t); _pass12_atlas_identity(t)
    return t


def build_d1() -> base.Template:
    t = build_d0()
    for x1, x2, color in ((5, 13, "minecraft:cyan_concrete"), (16, 24, "minecraft:orange_concrete"), (27, 34, "minecraft:yellow_concrete")):
        t.fill((x1, 1, 22), (x2, 1, 23), color)
    for x, color in ((9, "minecraft:cyan_concrete"), (20, "minecraft:orange_concrete"), (31, "minecraft:yellow_concrete")):
        t.fill((x - 2, 2, 32), (x - 2, 5, 32), "tfmg:steel_block"); t.fill((x + 2, 2, 32), (x + 2, 5, 32), "tfmg:steel_block")
        t.fill((x - 2, 5, 32), (x + 2, 5, 32), color); t.fill((x - 1, 2, 32), (x + 1, 3, 32), "create:framed_glass")
        t.set(x, 4, 32, "ae2:terminal")
    t.fill((5, 6, 33), (34, 6, 33), "create:fluid_pipe")
    for x, top in ((9, 14), (20, 16), (31, 15)):
        t.fill((x, 6, 24), (x, 6, 33), "create:fluid_pipe"); t.set(x, 6, 27, "create:mechanical_pump", facing="south")
        t.fill((x + 1, 7, 33), (x + 1, top, 33), "create:fluid_pipe"); t.set(x + 1, top - 1, 32, "create:encased_fan", facing="south")
    for x, color in ((6, "minecraft:cyan_concrete"), (17, "minecraft:orange_concrete"), (27, "minecraft:yellow_concrete")):
        t.fill((x, 2, 23), (x + 1, 2, 23), "create:depot")
        t.set(x, 3, 23, "minecraft:brewing_stand", has_bottle_0="false", has_bottle_1="false", has_bottle_2="false")
        t.fill((x, 1, 21), (x + 1, 1, 21), color)
    t.fill((37, 5, 21), (39, 6, 22), "immersiveengineering:crate"); t.fill((37, 4, 25), (39, 5, 26), "immersiveengineering:crate")
    t.fill((37, 2, 32), (38, 5, 33), "minecraft:weathered_copper"); t.fill((42, 2, 32), (43, 5, 33), "minecraft:weathered_copper")
    t.fill((32, 14, 21), (34, 14, 24), "minecraft:weathered_cut_copper"); t.fill((41, 10, 24), (43, 10, 26), "minecraft:weathered_cut_copper")
    signs = (
        (6, 5, 23, "south", "DIAGNOSTIC RECHECK", "SERVICE BULLETIN 6"),
        (17, 5, 23, "south", "LIFT DATUM", "VERIFY AFTER LOAD"),
        (27, 5, 23, "south", "CALIBRATION HOLD", "REPEAT TEST"),
        (7, 5, 32, "south", "DRAIN COLLAR 01", "INSPECT WEEKLY"),
        (18, 5, 32, "south", "DRAIN COLLAR 02", "SEEPAGE MONITOR"),
        (29, 5, 32, "south", "DRAIN COLLAR 03", "FLASHING WATCH"),
        (37, 6, 21, "east", "RECHECK PARTS", "PRIORITY ISSUE"),
        (37, 6, 32, "east", "REMOVED CORES", "RETURN BACKLOG"),
    )
    for args in signs: base.wall_sign(t, *args)
    return t


def build_accepted_d3() -> base.Template:
    t = build_d1()
    for x1, x2 in ((24, 27), (29, 34)): t.fill((x1, 1, 32), (x2, 1, 34), "minecraft:mossy_stone_bricks")
    t.fill((31, 1, 22), (34, 1, 28), "minecraft:moss_block"); t.fill((36, 1, 31), (44, 1, 34), "minecraft:coarse_dirt")
    for pos in ((25, 2, 33), (29, 2, 32), (33, 2, 34), (34, 2, 25), (38, 2, 33), (41, 2, 32)): t.set(*pos, "minecraft:brown_mushroom")
    for pos in ((28, 4, 32), (32, 4, 32), (35, 4, 31), (43, 4, 31)):
        t.set(*pos, "minecraft:vine", north="false", east="true", south="false", west="false", up="false")
    t.clear((32, 14, 22), (34, 14, 24)); t.fill((31, 13, 22), (34, 13, 24), "minecraft:weathered_cut_copper")
    for pos in ((32, 2, 22), (33, 2, 23), (34, 2, 24), (34, 1, 25)): t.set(*pos, "minecraft:gravel")
    t.clear((41, 10, 24), (43, 10, 26)); t.fill((40, 9, 24), (43, 9, 26), "minecraft:weathered_cut_copper")
    for pos in ((42, 6, 25), (44, 2, 26), (45, 1, 25), (46, 1, 26)): t.set(*pos, "minecraft:gravel")
    t.clear((41, 6, 35), (43, 7, 36)); t.fill((40, 5, 35), (43, 5, 36), "minecraft:weathered_cut_copper")
    for pos in ((41, 1, 36), (42, 1, 37), (43, 1, 38), (44, 1, 37)): t.set(*pos, "minecraft:gravel")
    t.fill((36, 0, 35), (44, 0, 39), "minecraft:mossy_cobblestone"); t.fill((45, 0, 23), (48, 0, 29), "minecraft:cracked_stone_bricks")
    for pos in ((30, 2, 33), (34, 2, 27), (38, 2, 33), (43, 2, 30), (44, 3, 28)): t.set(*pos, "minecraft:cobweb")
    t.chest(*PROOF_POS, PROOF_LOOT_TABLE, facing="east")
    for (x, y, z), mob in SPAWNERS.items():
        if (x, y, z) == (43, 2, 33): t.clear((43, 2, 33), (43, 3, 33))
        t.spawner(x, y, z, mob, count=1, nearby=3)
    _assert_d3_contracts(t)
    return t


def _assert_clear(t: base.Template, low: tuple[int, int, int], high: tuple[int, int, int], label: str) -> None:
    for x in range(low[0], high[0] + 1):
        for y in range(low[1], high[1] + 1):
            for z in range(low[2], high[2] + 1):
                name = _name(t, (x, y, z))
                if name not in AIR | {"minecraft:iron_door"}: raise AssertionError(f"OWS-009 {label} obstructed at {(x, y, z)}: {name}")


def _assert_proof(t: base.Template) -> None:
    row = t.blocks.get(PROOF_POS)
    if row is None or t.palette[row[0]]["Name"] != "minecraft:chest": raise AssertionError("OWS-009 canonical proof chest missing")
    if not row[1] or row[1].get("LootTable") != PROOF_LOOT_TABLE: raise AssertionError("OWS-009 proof chest uses wrong loot table")
    if _name(t, (37, 3, 29)) not in AIR or _name(t, (38, 2, 29)) not in AIR: raise AssertionError("OWS-009 proof approach obstructed")
    matches = sum(1 for _, nbt in t.blocks.values() if nbt and nbt.get("LootTable") == PROOF_LOOT_TABLE)
    if matches != 1: raise AssertionError(f"OWS-009 requires exactly one proof node; found {matches}")


def _assert_d3_contracts(t: base.Template) -> None:
    if tuple(t.size) != SIZE: raise AssertionError(f"OWS-009 dimensions changed: {t.size}")
    if any(not (0 <= x < 49 and 0 <= y < 18 and 0 <= z < 41) for x, y, z in t.blocks): raise AssertionError("OWS-009 exceeds accepted bounds")
    _assert_proof(t)
    if _count(t, "minecraft:spawner") != 3: raise AssertionError("OWS-009 requires three bounded spawners")
    for pos in SPAWNERS:
        if _name(t, pos) != "minecraft:spawner": raise AssertionError(f"OWS-009 spawner missing at {pos}")
        if sum(abs(a - b) for a, b in zip(pos, PROOF_POS)) < 9: raise AssertionError(f"OWS-009 spawner too close to proof at {pos}")
    for x, z in ((40, 7), (40, 15), (39, 31), (39, 34)):
        for dx in (0, 1):
            for y in (2, 3):
                if _name(t, (x + dx, y, z)) != "minecraft:iron_door": raise AssertionError(f"OWS-009 lost door at {(x + dx, y, z)}")
    for x, z in ((35, 13), (35, 23), (35, 29), (40, 23), (44, 23)):
        for dz in (0, 1):
            for y in (2, 3):
                if _name(t, (x, y, z + dz)) != "minecraft:iron_door": raise AssertionError(f"OWS-009 lost door at {(x, y, z + dz)}")
    for low, high, label in (
        ((8, 2, 8), (10, 4, 22), "Bay-01 vehicle lane"), ((19, 2, 8), (21, 4, 22), "Bay-02 vehicle lane"),
        ((29, 2, 8), (31, 4, 22), "Bay-03 vehicle lane"), ((5, 2, 24), (33, 3, 27), "transverse field"),
        ((5, 2, 28), (33, 3, 31), "technician spine"), ((39, 2, 8), (42, 3, 14), "customer route"),
        ((41, 2, 23), (43, 3, 25), "parts route"), ((39, 2, 29), (40, 3, 34), "records/core route"),
    ): _assert_clear(t, low, high, label)
    if _count(t, "create:fluid_pipe") < 150: raise AssertionError("OWS-009 lost connected utility anatomy")
    if _count(t, "tfmg:steel_block") < 700: raise AssertionError("OWS-009 lost primary structure")
    if sum((_name(t, pos) or "").endswith("_wall_sign") for pos in t.blocks) < 20: raise AssertionError("OWS-009 lost Atlas identity")
    for block in REQUIRED_BLOCKS:
        if _count(t, block) < 1: raise AssertionError(f"OWS-009 lacks required block {block}")


def _apply_pass19_microdetail(t: base.Template) -> None:
    for pos, block in PASS19_MICRODETAIL.items():
        if _name(t, pos) not in AIR: raise AssertionError(f"OWS-009 Pass-19 detail would overwrite accepted D3 at {pos}: {_name(t, pos)}")
        t.set(*pos, block)


def _assert_final_contracts(t: base.Template) -> None:
    _assert_d3_contracts(t)
    for pos, expected in PASS19_MICRODETAIL.items():
        if _name(t, pos) != expected: raise AssertionError(f"OWS-009 Pass-19 detail drift at {pos}")
    casing = (34, 2, 28)
    if _name(t, (34, 1, 28)) in AIR: raise AssertionError("OWS-009 Pass-19 casing is not grounded")
    if all(_name(t, pos) in AIR for pos in ((33, 2, 28), (35, 2, 28), (34, 2, 27), (34, 2, 29))):
        raise AssertionError(f"OWS-009 Pass-19 casing is not connected at {casing}")
    if _count(t, "create:andesite_casing") != 1: raise AssertionError("OWS-009 requires exactly one serialized andesite casing")


def build_009() -> base.Template:
    """Return accepted OWS-009 D3 plus nine localized Pass-19 details."""
    t = build_accepted_d3(); _apply_pass19_microdetail(t); _assert_final_contracts(t); return t


if __name__ == "__main__":
    raise SystemExit("Import build_009 from the authoritative generator; this module performs no writes.")
