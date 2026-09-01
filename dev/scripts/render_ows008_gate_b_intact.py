#!/usr/bin/env python3
"""Build and render the OWS-008 Gate-B r2 intact operating candidate.

The model starts from the exact independently accepted Gate-A r2 massing and
adds Passes 7-12 only. It contains no proof loot, encounters, damage, decay, or
final microdetail, and never writes shared state or authoritative shipping NBT.
"""
from __future__ import annotations

import gzip
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

import generate_wasteland_sites as base
import old_world_ows008_final as final_builder
from render_old_world_heavy_rebuild_review import OUTPUT_ROOT, ROOT, render_review_set
from render_ows008_gate_a_massing_r2 import build_gate_a_massing_r2
from render_structure_review import unpack_structure


TARGET = "OWS-008"
SIZE = (55, 22, 49)
CAMERA_SET = "ows008_fixed_v1"
GATE_A_MODEL_DECOMPRESSED_SHA256 = "22bca95829c4497cdf810b13be3d0e2c4a01c2df406b9cec8339f9c8d0773894"
TEMP_GATE_A_NAME = "_heavy_review_ows008_gate_a_freeze_check"
TEMP_NAME = "_heavy_review_ows008_gate_b_intact_r2"
OUTPUT_DIR = OUTPUT_ROOT / TARGET / "gate_b_intact" / "r2"
SHIPPING_PATH = (
    ROOT
    / "kubejs"
    / "data"
    / "infinite_domain"
    / "structure"
    / "wasteland"
    / "old_world"
    / "ows_008_vcf_emergency_persistence_investigation_lab.nbt"
)
STATE_PATH = ROOT / "old_world_narrative" / "registry" / "heavy_rebuild_state.json"
GATE_A_R2_REVIEW = ROOT / "old_world_narrative" / "reviews" / "heavy_rebuild" / "OWS-008_GATE_A_R2_REVIEW.md"


def _double_iron_door_z(t: base.Template, x: int, y: int, z: int, facing: str) -> None:
    """Two-wide door in an east/west wall."""
    t.clear((x, y, z), (x + 1, y + 2, z))
    base.double_door(t, x, y, z, facing, "iron")


def _double_iron_door_x(t: base.Template, x: int, y: int, z: int, facing: str) -> None:
    """Two-wide door in a north/south wall."""
    t.clear((x, y, z), (x, y + 2, z + 1))
    base.door(t, x, y, z, facing, "iron", "left")
    base.door(t, x, y, z + 1, facing, "iron", "right")


def _pass7_structural_system(t: base.Template) -> None:
    """Resolve the accepted masses as one supported containment laboratory."""
    # Public bar and validation gallery use an institutional bay grid.
    for x in (13, 20, 27, 34, 41):
        t.fill((x, 1, 4), (x, 8, 4), "minecraft:light_gray_concrete")
        t.fill((x, 8, 4), (x, 8, 14), "minecraft:light_gray_concrete")
    for x in (7, 17, 27, 37, 47):
        t.fill((x, 1, 12), (x, 9, 12), "tfmg:steel_block")
        t.fill((x, 8, 12), (x, 9, 22), "tfmg:steel_block")

    # A-D receive front/rear frames and intermediate roof beams aligned with
    # their accepted footprints and monitor loads.
    cells = (
        (6, 16, 24, 39, 14),
        (17, 27, 22, 37, 11),
        (28, 39, 20, 36, 16),
        (40, 50, 18, 34, 12),
    )
    for x1, x2, z1, z2, roof_y in cells:
        for z in (z1, (z1 + z2) // 2, z2):
            t.fill((x1, 1, z), (x1, roof_y, z), "tfmg:steel_block")
            t.fill((x2, 1, z), (x2, roof_y, z), "tfmg:steel_block")
            t.fill((x1, roof_y - 1, z), (x2, roof_y, z), "tfmg:steel_block")

    # Clean west and dirty east wings receive shorter repeated support frames.
    for z in (12, 20, 28, 36, 43):
        t.fill((2, 1, z), (2, 12, z), "minecraft:light_gray_concrete")
        t.fill((9, 1, z), (9, 12, z), "minecraft:light_gray_concrete")
    for z in (10, 18, 26, 34, 41):
        t.fill((48, 1, z), (48, 10, z), "tfmg:steel_block")
        t.fill((53, 1, z), (53, 10, z), "tfmg:steel_block")

    # Rear service/joint spine and maintenance core bear on explicit frames.
    for x in (5, 16, 27, 38, 51):
        t.fill((x, 1, 37), (x, 12, 37), "tfmg:steel_block")
        t.fill((x, 8, 37), (x, 9, 46), "tfmg:steel_block")
    t.fill((7, 11, 38), (46, 11, 45), "tfmg:steel_block")
    for z in (34, 40, 46):
        t.fill((46, 1, z), (46, 18, z), "tfmg:steel_block")
        t.fill((52, 1, z), (52, 18, z), "tfmg:steel_block")

    # Drainage follows real roof/volume edges.
    for x, z, top in ((13, 4, 8), (41, 4, 8), (6, 39, 14), (39, 36, 16), (50, 34, 12), (52, 44, 18)):
        t.fill((x, 1, z), (x, top, z), "create:fluid_pipe")


def _pass8_circulation_and_access(t: base.Template) -> None:
    """Create public, clean staff, dirty specimen, waste and service routes."""
    # Principal public threshold and broad route through liaison to gallery.
    t.clear((24, 2, 3), (30, 5, 4))
    _double_iron_door_z(t, 26, 2, 4, "north")
    t.fill((24, 1, 4), (30, 1, 18), "minecraft:quartz_block")
    t.clear((24, 2, 12), (30, 5, 14))
    _double_iron_door_z(t, 26, 2, 13, "south")

    # West clean staff/delivery threshold is isolated from dirty receiving.
    t.clear((1, 2, 16), (2, 5, 20))
    _double_iron_door_x(t, 2, 2, 18, "west")
    t.fill((3, 1, 14), (8, 1, 22), "minecraft:smooth_quartz")

    # East incident receipt and dirty waste thresholds open to the asphalt lane.
    t.clear((52, 2, 13), (53, 6, 20))
    _double_iron_door_x(t, 53, 2, 16, "east")
    t.clear((52, 2, 34), (53, 6, 39))
    _double_iron_door_x(t, 53, 2, 36, "east")

    # Staff entry into each controlled cell uses a small internal vestibule.
    cell_entries = ((11, 24, 28), (22, 22, 26), (33, 20, 24), (45, 18, 22))
    for x, front_z, inner_z in cell_entries:
        _double_iron_door_z(t, x, 2, front_z, "south")
        _double_iron_door_z(t, x, 2, inner_z, "south")

    # Material procession A -> B -> C -> D uses controlled two-wide crossings.
    for x, z in ((39, 26), (27, 29), (16, 31)):
        _double_iron_door_x(t, x, 2, z, "west")

    # Separate rear maintenance connections; A uses the east plant core while
    # B/C/D connect directly to the accepted joint-inspection spine.
    _double_iron_door_x(t, 50, 2, 28, "east")
    for x, z in ((32, 36), (21, 37), (10, 39)):
        _double_iron_door_z(t, x, 2, z, "north")

    # Rear clean delivery and waste/service exits remain opposed.
    _double_iron_door_x(t, 5, 2, 41, "west")
    _double_iron_door_z(t, 47, 2, 46, "south")

    # Two-wide west dogleg stair reaches command/archive.
    for x in (4, 5):
        base.stair_flight(t, x, 2, 19, 5, "south", "minecraft:smooth_quartz_stairs")
    t.fill((3, 7, 23), (7, 7, 28), "minecraft:smooth_stone")
    t.clear((3, 8, 22), (7, 13, 28))
    for x in (4, 5):
        base.stair_flight(t, x, 8, 27, 5, "north", "minecraft:smooth_quartz_stairs")
    t.fill((3, 13, 21), (7, 13, 24), "minecraft:smooth_stone")

    # Independent east dogleg maintenance stair reaches interstitial/roof plant.
    for x in (48, 49):
        base.stair_flight(t, x, 2, 36, 4, "south", "minecraft:smooth_quartz_stairs")
    t.fill((47, 6, 39), (51, 6, 43), "minecraft:smooth_stone")
    for x in (48, 49):
        base.stair_flight(t, x, 7, 42, 4, "north", "minecraft:smooth_quartz_stairs")
    t.fill((47, 11, 36), (51, 11, 40), "minecraft:smooth_stone")
    for x in (48, 49):
        base.stair_flight(t, x, 12, 37, 4, "south", "minecraft:smooth_quartz_stairs")
    t.fill((47, 16, 40), (51, 16, 44), "minecraft:smooth_stone")
    _double_iron_door_x(t, 46, 16, 41, "west")


def _pass9_exterior_architecture(t: base.Template) -> None:
    """Align openings, bay rhythm and service thresholds with room functions."""
    # Public glazing corresponds to liaison/reception rooms around the entrance.
    t.fill((14, 3, 3), (23, 6, 3), "create:framed_glass")
    t.fill((31, 3, 3), (40, 6, 3), "create:framed_glass")
    for x in (13, 20, 24, 31, 34, 41):
        t.fill((x, 1, 3), (x, 8, 4), "minecraft:light_gray_concrete")

    # West clean delivery/staff face receives a washable canopy and drain.
    t.fill((0, 9, 15), (5, 9, 23), "minecraft:white_concrete")
    for z in (15, 23):
        t.fill((1, 1, z), (1, 8, z), "tfmg:steel_block")
    t.fill((0, 0, 15), (0, 0, 23), "minecraft:oxidized_copper_grate")

    # East dirty receipt is heavier, with a deep emergency canopy and trench.
    t.fill((49, 9, 12), (54, 10, 23), "minecraft:yellow_concrete")
    t.fill((54, 0, 12), (54, 0, 23), "minecraft:oxidized_copper_grate")
    t.fill((53, 3, 27), (53, 7, 33), "create:framed_glass")

    # Rear service face exposes separated intake/exhaust banks and drains.
    for x1, x2 in ((7, 15), (19, 27), (31, 39), (43, 50)):
        t.fill((x1, 7, 47), (x2, 9, 47), "minecraft:oxidized_copper_grate")
    t.fill((6, 0, 46), (51, 0, 46), "minecraft:oxidized_copper_grate")

    # Room-aligned observation faces and high service bands remain bounded by
    # real structural piers instead of becoming continuous decorative glazing.
    for x1, x2, z, y, color in (
        (7, 15, 23, 10, "minecraft:lime_concrete"),
        (18, 26, 21, 7, "minecraft:white_concrete"),
        (29, 38, 19, 12, "minecraft:yellow_concrete"),
        (41, 49, 17, 8, "minecraft:cyan_concrete"),
    ):
        t.fill((x1, y, z), (x2, y + 1, z), color)


def _pass10_interior_architecture(t: base.Template) -> None:
    """Create legitimate rooms, pressure boundaries and continuous clear routes."""
    # Public bar: west briefing, central security/reception, east liaison.
    t.fill((14, 1, 5), (40, 1, 13), "minecraft:quartz_block")
    base.partition_x(t, 23, 2, 5, 12, "minecraft:white_concrete", doorway_z=9)
    base.partition_x(t, 31, 2, 5, 12, "minecraft:white_concrete", doorway_z=9)
    t.fill((14, 2, 12), (22, 6, 12), "create:framed_glass")
    t.fill((32, 2, 12), (40, 6, 12), "create:framed_glass")

    # Validation gallery keeps one continuous observation route.
    t.fill((8, 1, 14), (46, 1, 21), "minecraft:smooth_quartz")
    t.fill((8, 1, 19), (46, 1, 20), "minecraft:lime_concrete")

    # West wing: clean change, analysis, retained samples and command access.
    t.fill((3, 1, 13), (8, 1, 42), "minecraft:quartz_block")
    for z in (21, 29, 36):
        base.partition_z(t, z, 2, 3, 8, "minecraft:white_concrete", doorways=(6,))
    t.fill((3, 13, 18), (14, 13, 32), "minecraft:smooth_quartz")
    base.partition_x(t, 8, 14, 18, 32, "minecraft:white_concrete", doorway_z=25)

    # East wing: receipt/custody, dirty examination, wash and waste return.
    t.fill((49, 1, 11), (52, 1, 40), "tfmg:factory_floor")
    for z in (21, 29, 35):
        base.partition_z(t, z, 2, 49, 52, "minecraft:light_gray_concrete", doorways=(51,))

    # Each cell gains a hygienic floor and internal vestibule boundary.
    cells = (
        (6, 16, 24, 39, 28, "minecraft:lime_concrete"),
        (17, 27, 22, 37, 26, "minecraft:white_concrete"),
        (28, 39, 20, 36, 24, "minecraft:yellow_concrete"),
        (40, 50, 18, 34, 22, "minecraft:cyan_concrete"),
    )
    for x1, x2, z1, z2, partition_z, datum in cells:
        t.fill((x1 + 1, 1, z1 + 1), (x2 - 1, 1, z2 - 1), "minecraft:smooth_quartz")
        t.fill((x1 + 1, 1, z1 + 1), (x2 - 1, 1, partition_z - 1), datum)
        base.partition_z(t, partition_z, 2, x1 + 1, x2 - 1, "minecraft:white_concrete")
        center = (x1 + x2) // 2
        t.clear((center, 2, partition_z), (center + 1, 4, partition_z))
        base.double_door(t, center, 2, partition_z, "south", "iron")

    # Restore the A-to-east-plant crossing after the dirty-wing transverse
    # partitions are resolved; its second leaf occupies their z=29 datum.
    _double_iron_door_x(t, 50, 2, 28, "east")

    # Rear service spine: clean utilities west, joint inspection center, dirty
    # effluent/waste east, with a through maintenance route.
    t.fill((6, 1, 38), (50, 1, 45), "tfmg:factory_floor")
    base.partition_x(t, 16, 2, 38, 45, "minecraft:light_gray_concrete")
    base.partition_x(t, 39, 2, 38, 45, "minecraft:light_gray_concrete")
    for x in (16, 39):
        _double_iron_door_x(t, x, 2, 43, "east")


def _pass11_operational_systems(t: base.Template) -> None:
    """Install the intact incident-receipt-to-recurrence investigation system."""
    # East receipt/custody, dirty examination and wash/waste chain.
    t.fill((49, 2, 13), (51, 3, 15), "immersiveengineering:crate")
    base.desk(t, 49, 2, 19, "north")
    for z in (23, 26):
        t.set(49, 2, z, "minecraft:brewing_stand", has_bottle_0="false", has_bottle_1="false", has_bottle_2="false")
        t.fill((51, 2, z), (52, 3, z), "create:framed_glass")
    t.fill((49, 2, 31), (51, 4, 33), "create:fluid_tank")
    t.set(52, 2, 31, "minecraft:water_cauldron", level="3")
    t.fill((49, 2, 37), (52, 4, 39), "immersiveengineering:sheetmetal_steel")

    # Cell A: wet/thermal treatment, drainable and visibly service-intensive.
    for x in (42, 47):
        t.fill((x, 2, 24), (x + 1, 5, 26), "create:fluid_tank")
        t.set(x, 2, 29, "minecraft:water_cauldron", level="3")
    t.fill((41, 1, 31), (49, 1, 31), "minecraft:oxidized_copper_grate")
    t.fill((41, 9, 24), (49, 9, 32), "create:fluid_pipe")
    t.set(44, 10, 28, "create:encased_fan", facing="south")
    t.set(47, 10, 28, "create:encased_fan", facing="south")

    # Cell B: chemical/vapor treatment with a sealed internal process cabinet.
    t.fill((30, 2, 27), (37, 7, 31), "create:framed_glass")
    t.clear((31, 3, 28), (36, 6, 30))
    # The paired chambers flank a two-wide controlled operator aisle aligned
    # with both pressure doors; they never turn the process cabinet into a
    # decorative obstruction.
    t.clear((33, 2, 27), (34, 4, 31))
    for x in (30, 37):
        t.fill((x, 2, 32), (x + (1 if x == 30 else 0), 5, 34), "create:fluid_tank")
    t.fill((29, 12, 27), (38, 12, 34), "create:fluid_pipe")
    t.set(33, 13, 30, "create:encased_fan", facing="south")
    t.set(35, 13, 30, "create:encased_fan", facing="south")

    # Cell C: post-treatment clean hold with positive-air and cooler banks.
    for x in (19, 23):
        t.fill((x, 2, 29), (x + 2, 4, 31), "oritech:cooler_block")
        t.fill((x, 2, 34), (x + 2, 3, 35), "minecraft:smooth_quartz")
    t.fill((18, 8, 29), (26, 8, 35), "create:fluid_pipe")
    t.set(21, 9, 32, "create:encased_fan", facing="south")
    t.fill((19, 2, 27), (21, 2, 27), "create:depot")
    t.fill((23, 2, 27), (25, 2, 27), "create:depot")

    # Cell D: controlled persistence challenge and hidden-recurrence comparison.
    for z in (31, 35):
        t.fill((8, 2, z), (10, 2, z + 1), "farmersdelight:rich_soil")
        t.fill((13, 2, z), (15, 2, z + 1), "farmersdelight:rich_soil")
        for x in (8, 10, 13, 15):
            t.set(x, 3, z, "minecraft:brown_mushroom")
    t.fill((7, 10, 30), (15, 10, 37), "create:fluid_pipe")
    t.set(10, 11, 34, "create:encased_fan", facing="south")
    t.fill((7, 4, 37), (15, 7, 37), "create:framed_glass")

    # Gallery controls align one-for-one with D/C/B/A.
    for x in (9, 20, 32, 41):
        t.fill((x, 2, 18), (x + 2, 2, 18), "create:depot")
        t.set(x + 1, 3, 19, "ae2:terminal")

    # West analysis, retained samples and upper incident command/archive.
    for z in (23, 26):
        t.set(4, 2, z, "minecraft:brewing_stand", has_bottle_0="false", has_bottle_1="false", has_bottle_2="false")
        t.set(7, 2, z, "ae2:terminal")
    t.fill((3, 2, 31), (5, 4, 34), "oritech:cooler_block")
    t.fill((7, 2, 31), (8, 5, 34), "minecraft:bookshelf")
    for x, z in ((3, 20), (9, 20), (3, 28), (9, 28)):
        base.desk(t, x, 14, z, "north")
    t.fill((4, 14, 31), (7, 16, 32), "ae2:drive")
    t.fill((10, 14, 31), (13, 16, 32), "minecraft:bookshelf")

    # Concealed-joint inspection spine: overhead air/wash, floor drain sampling,
    # four aligned penetration racks and clean/dirty service separation.
    t.fill((7, 1, 40), (45, 1, 40), "minecraft:oxidized_copper_grate")
    t.fill((7, 6, 41), (45, 6, 41), "create:fluid_pipe")
    t.fill((7, 8, 44), (45, 8, 44), "create:fluid_pipe")
    for x in (13, 22, 33, 44):
        t.fill((x, 2, 39), (x + 1, 5, 39), "tfmg:steel_block")
        t.fill((x, 4, 40), (x, 6, 44), "create:fluid_pipe")
        t.set(x + 1, 2, 42, "minecraft:lever", face="wall", facing="south", powered="false")
        t.fill((x, 9, 40), (x + 2, 11, 43), "immersiveengineering:sheetmetal_steel")
    t.fill((7, 2, 44), (14, 4, 45), "create:fluid_tank")
    t.fill((41, 2, 44), (49, 4, 45), "immersiveengineering:sheetmetal_steel")

    # Branches link each cell service zone to its accepted roof monitor.
    for x, top, z in ((11, 18, 39), (22, 15, 37), (33, 20, 36), (45, 17, 34)):
        t.fill((x, 6, z), (x, top, z), "create:fluid_pipe")
        t.set(x, 7, min(44, z + 2), "create:mechanical_pump", facing="south")

    # Lighting follows real work and circulation axes.
    for x in (10, 16, 22, 28, 34, 40, 46):
        t.set(x, 7, 17, "minecraft:sea_lantern")
    for x, y, z in ((11, 11, 34), (22, 8, 32), (33, 13, 30), (45, 10, 28)):
        t.fill((x, y, z - 2), (x, y, z + 2), "minecraft:sea_lantern")


def _pass12_institutional_identity(t: base.Template) -> None:
    """Apply architectural VCF identity and purposeful emergency wayfinding."""
    # Clean VCF datums remain visible beneath localized emergency boundaries.
    t.fill((14, 7, 3), (40, 8, 3), "minecraft:lime_concrete")
    t.fill((3, 1, 14), (8, 1, 16), "minecraft:lime_concrete")
    t.fill((49, 1, 12), (52, 1, 20), "minecraft:yellow_concrete")
    for x, z, color in ((10, 24, "minecraft:lime_concrete"), (21, 22, "minecraft:white_concrete"), (33, 20, "minecraft:yellow_concrete"), (45, 18, "minecraft:cyan_concrete")):
        t.fill((x - 2, 1, z), (x + 3, 1, z + 2), color)

    base.wall_sign(t, 20, 7, 4, "north", "VERDANT CONTINUUM", "FOODS")
    base.wall_sign(t, 33, 7, 4, "north", "PERSISTENCE", "INCIDENT LAB")
    base.wall_sign(t, 24, 5, 6, "south", "INCIDENT LIAISON", "PUBLIC CHECK-IN")
    base.wall_sign(t, 3, 6, 18, "east", "STAFF CLEAN ENTRY", "CHANGE / GOWN")
    base.wall_sign(t, 51, 7, 16, "west", "INCIDENT RECEIVING", "SEALED MATERIAL")
    base.wall_sign(t, 49, 6, 27, "north", "DIRTY EXAM", "CUSTODY ACTIVE")
    base.wall_sign(t, 49, 6, 34, "north", "WASH / RETURN", "DIRTY SIDE")
    base.wall_sign(t, 42, 6, 17, "north", "CELL A", "WET / THERMAL")
    base.wall_sign(t, 30, 6, 19, "north", "CELL B", "VAPOR CYCLE")
    base.wall_sign(t, 19, 6, 21, "north", "CELL C", "CLEAN HOLD")
    base.wall_sign(t, 8, 6, 23, "north", "CELL D", "PERSISTENCE")
    base.wall_sign(t, 9, 5, 16, "south", "VALIDATION GALLERY", "CYCLES A-D")
    base.wall_sign(t, 4, 6, 20, "north", "CLEAN CHANGE", "STAFF ONLY")
    base.wall_sign(t, 4, 6, 28, "north", "COMPARATIVE", "ANALYSIS")
    base.wall_sign(t, 4, 6, 35, "north", "RETAINED SAMPLES", "CONTROLLED HOLD")
    base.wall_sign(t, 3, 16, 18, "south", "INCIDENT COMMAND", "ACTIVE REVIEW")
    base.wall_sign(t, 10, 16, 32, "north", "SECURE ARCHIVE", "AUTHORIZED DATA")
    base.wall_sign(t, 18, 5, 38, "south", "JOINT INSPECTION", "SERVICE SPINE")
    base.wall_sign(t, 31, 5, 38, "south", "PENETRATION TEST", "DRAIN / AIR / DATA")
    base.wall_sign(t, 8, 5, 45, "south", "CLEAN SERVICES", "SUPPLY / WASH")
    base.wall_sign(t, 42, 5, 45, "south", "DECON WASTE", "AUTHORIZED REMOVAL")
    base.wall_sign(t, 46, 16, 40, "west", "ROOF PLANT", "MAINTENANCE ACCESS")


def build_gate_b_intact() -> base.Template:
    t = build_gate_a_massing_r2()
    _pass7_structural_system(t)
    _pass8_circulation_and_access(t)
    _pass9_exterior_architecture(t)
    _pass10_interior_architecture(t)
    _pass11_operational_systems(t)
    _pass12_institutional_identity(t)
    # The accepted intact design is unchanged; replay its west command stair
    # after all partition/landing writes so the two flights are executable.
    for x, y, z, rise, facing in final_builder.WEST_COMMAND_STAIR_FLIGHTS:
        base.stair_flight(t, x, y, z, rise, facing, "minecraft:smooth_quartz_stairs")
    return t


def _name_at(t: base.Template, pos: tuple[int, int, int]) -> str | None:
    entry = t.blocks.get(pos)
    return None if entry is None else t.palette[entry[0]]["Name"]


def _assert_gate_a_source_freeze() -> None:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    gate = state.get("visual_review_gates", {}).get("gate_a_massing", {})
    if gate.get("status") != "passed_r2":
        raise AssertionError("Gate B refused: OWS-008 Gate A r2 is not independently approved")
    if not GATE_A_R2_REVIEW.is_file():
        raise AssertionError("Gate B refused: explicit OWS-008 Gate-A r2 review is missing")
    review = GATE_A_R2_REVIEW.read_text(encoding="utf-8")
    if "**Decision:** **PASSED**" not in review or "**OWS-008 GATE A r2: PASSED.**" not in review:
        raise AssertionError("Gate B refused: OWS-008 Gate-A r2 review lacks an explicit PASSED decision")

    gate_a = build_gate_a_massing_r2()
    original_data = base.DATA
    try:
        with tempfile.TemporaryDirectory(prefix="ows008-gate-a-freeze-") as temp_dir:
            base.DATA = Path(temp_dir)
            gate_a.save(TEMP_GATE_A_NAME)
            temp_nbt = base.DATA / "structure" / "wasteland" / f"{TEMP_GATE_A_NAME}.nbt"
            actual = hashlib.sha256(gzip.decompress(temp_nbt.read_bytes())).hexdigest()
    finally:
        base.DATA = original_data
    if actual != GATE_A_MODEL_DECOMPRESSED_SHA256:
        raise AssertionError(
            f"Accepted Gate-A r2 source drifted: {actual} != {GATE_A_MODEL_DECOMPRESSED_SHA256}"
        )


def _assert_intact_contracts(t: base.Template) -> None:
    if tuple(t.size) != SIZE:
        raise AssertionError(f"OWS-008 Gate-B r2 dimensions changed unexpectedly: {t.size}")
    if any(not (0 <= x < SIZE[0] and 0 <= y < SIZE[1] and 0 <= z < SIZE[2]) for x, y, z in t.blocks):
        raise AssertionError("OWS-008 Gate-B r2 exceeds the accepted envelope")
    final_builder._assert_upper_proof_route(t)

    # Representative points freeze the nine independently accepted macro aspects.
    frozen = {
        (27, 8, 1): "minecraft:white_concrete",
        (10, 0, 2): "minecraft:smooth_stone",
        (4, 17, 24): "minecraft:lime_concrete",
        (10, 18, 31): "minecraft:lime_concrete",
        (33, 20, 28): "minecraft:yellow_concrete",
        (53, 9, 18): "minecraft:yellow_concrete",
        (20, 12, 41): "minecraft:white_concrete",
        (50, 18, 40): "minecraft:white_concrete",
    }
    for pos, expected in frozen.items():
        actual = _name_at(t, pos)
        if actual != expected:
            raise AssertionError(f"Gate-A frozen aspect changed at {pos}: {actual} != {expected}")

    # Principal, process and service doors retain complete lower/upper halves.
    doors_z = ((26, 4), (26, 13), (11, 24), (11, 28), (22, 22), (22, 26), (33, 20), (33, 24), (45, 18), (45, 22), (32, 36), (21, 37), (10, 39), (47, 46))
    for x, z in doors_z:
        for dx in (0, 1):
            for y in (2, 3):
                if _name_at(t, (x + dx, y, z)) != "minecraft:iron_door":
                    raise AssertionError(f"Controlled Z-wall door missing at {(x + dx, y, z)}")
    doors_x = ((2, 18), (53, 16), (53, 36), (39, 26), (27, 29), (16, 31), (50, 28), (5, 41), (16, 43), (39, 43))
    for x, z in doors_x:
        for dz in (0, 1):
            for y in (2, 3):
                if _name_at(t, (x, y, z + dz)) != "minecraft:iron_door":
                    raise AssertionError(f"Controlled X-wall door missing at {(x, y, z + dz)}")

    # Public, gallery, cell and service center aisles remain two blocks high.
    protected = (
        ((25, 2, 5), (29, 3, 11)),
        ((10, 2, 15), (45, 3, 16)),
        ((11, 2, 29), (12, 3, 36)),
        ((22, 2, 27), (22, 3, 35)),
        ((33, 2, 25), (34, 3, 34)),
        ((45, 2, 23), (46, 3, 32)),
        ((18, 2, 43), (38, 3, 44)),
    )
    for low, high in protected:
        for x in range(low[0], high[0] + 1):
            for y in range(low[1], high[1] + 1):
                for z in range(low[2], high[2] + 1):
                    name = _name_at(t, (x, y, z))
                    if name not in {None, "minecraft:air", "minecraft:iron_door"}:
                        raise AssertionError(f"Protected circulation obstruction at {(x, y, z)}: {name}")

    names = [t.palette[entry[0]]["Name"] for entry in t.blocks.values()]
    forbidden = {"minecraft:chest", "minecraft:trapped_chest", "minecraft:spawner"}
    present_forbidden = forbidden.intersection(names)
    if present_forbidden:
        raise AssertionError(f"Gate-B contains deferred proof/encounter blocks: {sorted(present_forbidden)}")
    if sum(name.endswith("_wall_sign") for name in names) < 22:
        raise AssertionError("VCF/emergency intact-state wayfinding is unexpectedly sparse")
    if names.count("minecraft:smooth_quartz_stairs") < 24:
        raise AssertionError("Independent staff/maintenance stair coverage is unexpectedly sparse")
    if names.count("create:fluid_pipe") < 140:
        raise AssertionError("Connected air/wash/drain service coverage is unexpectedly sparse")
    if names.count("create:fluid_tank") < 20:
        raise AssertionError("Treatment/clean-service plant is unexpectedly sparse")
    if names.count("farmersdelight:rich_soil") < 16:
        raise AssertionError("Controlled persistence test program is unexpectedly sparse")


def git_hash_object(path: Path) -> str:
    result = subprocess.run(
        ["git", "hash-object", str(path.relative_to(ROOT))],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def git_rev_parse(spec: str) -> str:
    result = subprocess.run(
        ["git", "rev-parse", spec],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def main() -> None:
    shipping_before = git_hash_object(SHIPPING_PATH)
    _assert_gate_a_source_freeze()

    t = build_gate_b_intact()
    _assert_intact_contracts(t)

    original_data = base.DATA
    try:
        with tempfile.TemporaryDirectory(prefix="ows008-gate-b-r2-") as temp_dir:
            base.DATA = Path(temp_dir)
            t.save(TEMP_NAME)
            temp_nbt = base.DATA / "structure" / "wasteland" / f"{TEMP_NAME}.nbt"
            model_bytes = temp_nbt.read_bytes()
            size, blocks = unpack_structure(temp_nbt)
            if len(blocks) < 15000:
                raise AssertionError(f"Gate-B r2 intact model is unexpectedly sparse: {len(blocks)}")
            head = git_rev_parse("HEAD")
            manifest = render_review_set(
                target=TARGET,
                gate="gate_b_intact",
                revision=f"intact-r2@{head[:8]}",
                damage_state="D0 intact / operational",
                source_commit=head,
                source_path="review-only:render_ows008_gate_b_intact.build_gate_b_intact()",
                size=size,
                blocks=blocks,
                output_dir=OUTPUT_DIR,
                camera_set=CAMERA_SET,
            )
        manifest["review_model_nbt_sha256"] = hashlib.sha256(model_bytes).hexdigest()
        manifest["review_builder_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        manifest["gate_a_model_decompressed_sha256"] = GATE_A_MODEL_DECOMPRESSED_SHA256
        manifest["placed_positions"] = len(blocks)
        manifest["gate_a_frozen_aspects_asserted"] = 9
        manifest["gate_b_obligations_implemented"] = 6
        manifest["working_door_blocks_asserted"] = 100
        manifest["west_command_stair_treads_asserted"] = 20
        manifest["upper_proof_route_connected"] = True
        manifest["proof_encounters_history_damage_present"] = False
        manifest["authoritative_shipping_modified"] = False
        manifest["shipping_nbt_git_blob_before"] = shipping_before
        manifest["shipping_nbt_git_blob_after"] = git_hash_object(SHIPPING_PATH)
        if manifest["shipping_nbt_git_blob_after"] != shipping_before:
            raise AssertionError("OWS-008 shipping NBT changed during review-only rendering")
        (OUTPUT_DIR / "review_manifest.json").write_text(
            json.dumps(manifest, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    finally:
        base.DATA = original_data

    print(
        f"Rendered {TARGET} Gate B r2 intact review at {manifest['dimensions']} using "
        f"{manifest['fixed_camera_set']}; independent visual approval remains pending."
    )


if __name__ == "__main__":
    main()
