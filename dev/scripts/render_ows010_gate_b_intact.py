#!/usr/bin/env python3
"""Build and render OWS-010 Gate-B r1 intact operating candidate.

The review model begins with the exact independently accepted Gate-A r2
massing and adds doctrine Passes 7-12 only. It is target-local and never
writes shared state, production dispatch, registries, or shipping NBT.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import generate_wasteland_sites as base
from render_old_world_heavy_rebuild_review import OUTPUT_ROOT, ROOT, render_review_set
from render_ows010_gate_a_massing_r2 import build_gate_a_massing_r2
from render_structure_review import unpack_structure


TARGET = "OWS-010"
SIZE = (49, 16, 43)
CAMERA_SET = "ows010_fixed_v1"
GATE_A_MODEL_SHA256 = "784e37d03c8f8eea79ca57db14b85ca70e0c517a3e25e506d073a34dd9f1573d"
FROZEN_SHIPPING_SHA256 = "5e9390d3d41663f1baef6ad017e941dbf6153d168bb9100a8a5fd46193d9035a"
FROZEN_SHIPPING_BLOB = "be2ab341c2d252c975711caa93e92c965f943007"
TEMP_GATE_A_NAME = "_heavy_review_ows010_gate_a_freeze_check"
TEMP_GATE_A_NBT = ROOT / "kubejs/data/infinite_domain/structure/wasteland" / f"{TEMP_GATE_A_NAME}.nbt"
TEMP_NAME = "_heavy_review_ows010_gate_b_intact_r1"
TEMP_NBT = ROOT / "kubejs/data/infinite_domain/structure/wasteland" / f"{TEMP_NAME}.nbt"
OUTPUT_DIR = OUTPUT_ROOT / TARGET / "gate_b_intact" / "r1"
SHIPPING_PATH = ROOT / (
    "kubejs/data/infinite_domain/structure/wasteland/old_world/"
    "ows_010_atlas_conveyor_transfer_hall.nbt"
)
GATE_A_REVIEW = ROOT / "old_world_narrative/reviews/heavy_rebuild/OWS-010_GATE_A_R2_REVIEW.md"
AIR = {None, "minecraft:air", "minecraft:cave_air", "minecraft:void_air", "minecraft:structure_void"}


def _name(t: base.Template, pos: tuple[int, int, int]) -> str | None:
    entry = t.blocks.get(pos)
    return None if entry is None else t.palette[entry[0]]["Name"]


def _double_door_z(t: base.Template, x: int, y: int, z: int, facing: str) -> None:
    t.clear((x, y, z), (x + 1, y + 2, z))
    base.double_door(t, x, y, z, facing, "iron")


def _double_door_x(t: base.Template, x: int, y: int, z: int, facing: str) -> None:
    t.clear((x, y, z), (x, y + 2, z + 1))
    base.door(t, x, y, z, facing, "iron", "left")
    base.door(t, x, y, z + 1, facing, "iron", "right")


def _two_wide_stair(
    t: base.Template,
    x: int,
    y: int,
    z: int,
    rise: int,
    facing: str,
    axis: str,
) -> None:
    """Place paired playable stairs with three-block headroom."""
    base.stair_flight(t, x, y, z, rise, facing, "minecraft:smooth_stone_stairs")
    if axis == "x":
        base.stair_flight(t, x + 1, y, z, rise, facing, "minecraft:smooth_stone_stairs")
    else:
        base.stair_flight(t, x, y, z + 1, rise, facing, "minecraft:smooth_stone_stairs")


def _pass7_structural_system(t: base.Template) -> None:
    """Resolve the accepted hall into a lane-indexed steel frame and truss grid."""
    # Primary columns sit on lane boundaries and on the protected bridge edges.
    # They never occupy a conveyor bed, dock tongue, or playable bridge surface.
    for x in (16, 22, 28, 34, 40, 45):
        for z in (11, 19, 22, 28):
            t.fill((x, 2, z), (x, 10, z), "tfmg:steel_block")

    # Four transverse trusses describe the real clear span beneath the accepted
    # lane monitors. Orange chords identify load-transfer and service datums.
    for z in (11, 19, 22, 28):
        t.fill((16, 10, z), (45, 10, z), "tfmg:steel_block")
        for x in (19, 25, 31, 37, 43):
            t.set(x, 9, z, "minecraft:orange_concrete")
    for x in (16, 22, 28, 34, 40, 45):
        t.fill((x, 10, 11), (x, 10, 28), "tfmg:steel_block")

    # Each monitor bears on paired longitudinal rails and short transfer posts.
    for x1, x2 in ((18, 20), (24, 26), (30, 32), (36, 38)):
        t.fill((x1, 11, 13), (x1, 11, 27), "tfmg:steel_block")
        t.fill((x2, 11, 13), (x2, 11, 27), "tfmg:steel_block")
        for z in (13, 27):
            t.fill((x1, 11, z), (x1, 13, z), "tfmg:steel_block")
            t.fill((x2, 11, z), (x2, 13, z), "tfmg:steel_block")

    # Annex and maintenance frames connect the low occupied volumes to the
    # accepted oversight crown and east roof-service spine.
    for x in (4, 10, 17):
        for z in (5, 11, 21):
            t.fill((x, 2, z), (x, 8, z), "tfmg:steel_block")
    for z in (15, 22, 28):
        t.fill((43, 7, z), (48, 7, z), "tfmg:steel_block")


def _pass8_circulation_and_access(t: base.Template) -> None:
    """Build distinct staff, operator, catwalk, dock and maintenance routes."""
    # North staff threshold and protected annex spine remain independent of the
    # south freight court. The orange strip terminates at access control.
    _double_door_z(t, 9, 2, 4, "north")
    t.fill((8, 1, 5), (11, 1, 20), "minecraft:smooth_stone")
    t.fill((9, 1, 5), (10, 1, 20), "minecraft:orange_concrete")

    # Ground operator gallery is three blocks clear and connects quality/rework
    # to both lane ends without entering the induction crossfeed.
    t.fill((14, 1, 11), (16, 1, 30), "minecraft:smooth_stone")
    t.fill((16, 1, 11), (16, 1, 30), "minecraft:orange_concrete")
    # Keep the accepted recessed west glazing at X14; the two-wide clear route
    # uses X15-16 immediately behind it.
    t.clear((15, 2, 11), (16, 5, 30))
    _double_door_x(t, 17, 2, 14, "east")
    _double_door_x(t, 17, 2, 26, "east")

    # A two-wide annex stair reaches a full upper landing, control room, and the
    # lane-spanning catwalk. The lower operator route remains clear to its east.
    _two_wide_stair(t, 10, 2, 12, 6, "south", "x")
    t.fill((10, 7, 17), (16, 7, 21), "minecraft:smooth_stone")
    t.clear((10, 8, 17), (16, 10, 21))

    # The accepted cross-aisle reservation becomes a playable two-wide bridge.
    t.fill((16, 7, 20), (43, 7, 21), "minecraft:smooth_stone")
    t.clear((16, 8, 20), (43, 9, 21))
    t.fill((16, 8, 19), (43, 9, 19), "minecraft:iron_bars")
    t.fill((16, 8, 22), (43, 9, 22), "minecraft:iron_bars")
    for x in (16, 22, 28, 34, 40, 43):
        t.set(x, 7, 20, "minecraft:yellow_concrete")
        t.set(x, 7, 21, "minecraft:yellow_concrete")

    # The east core provides a second full stair from grade to bridge and a
    # paired continuation to roof-service level; neither is a decorative ladder.
    _two_wide_stair(t, 45, 2, 16, 6, "south", "x")
    t.fill((43, 7, 20), (47, 7, 23), "minecraft:smooth_stone")
    t.clear((43, 8, 20), (47, 9, 23))
    _two_wide_stair(t, 45, 8, 23, 5, "south", "x")
    t.fill((44, 12, 27), (47, 12, 28), "minecraft:smooth_stone")
    t.clear((44, 13, 27), (47, 14, 28))

    # A depressed, guarded drive trench parallels every lane beneath the raised
    # east return. Its north and south ramps meet the maintenance core route.
    t.fill((40, 0, 13), (41, 0, 28), "minecraft:oxidized_copper_grate")
    t.clear((40, 1, 13), (41, 3, 28))
    t.fill((39, 1, 13), (39, 2, 28), "minecraft:iron_bars")
    t.set(40, 0, 13, "minecraft:smooth_stone_stairs", facing="north", half="bottom", shape="straight", waterlogged="false")
    t.set(41, 0, 28, "minecraft:smooth_stone_stairs", facing="south", half="bottom", shape="straight", waterlogged="false")

    # Independent east service entry and hall emergency egress remain outside
    # truck swing paths. Four freight portals remain untouched and usable.
    _double_door_x(t, 48, 2, 20, "east")
    _double_door_x(t, 46, 2, 9, "east")
    t.fill((42, 1, 12), (44, 1, 31), "minecraft:light_gray_concrete")
    t.clear((42, 2, 12), (44, 3, 31))


def _pass9_exterior_architecture(t: base.Template) -> None:
    """Add room-aligned thresholds, drainage, court safety, and work lighting."""
    # Lamps identify staff, freight, emergency and service thresholds while the
    # accepted facade/crown geometry remains untouched.
    for x, y, z in (
        (7, 7, 4), (12, 7, 4),
        (19, 7, 36), (26, 7, 36), (33, 7, 36), (40, 7, 36),
        (47, 7, 10), (47, 7, 27),
    ):
        t.set(x, y, z, "minecraft:redstone_lamp", lit="true")

    # Dock-pair bollards and drainage reinforce the accepted inbound/outbound
    # assemblies without moving a frame, portal, crown, or truck coordinate.
    for x in (17, 23, 24, 30, 31, 37, 38, 44):
        t.fill((x, 1, 39), (x, 2, 39), "minecraft:yellow_concrete")
    t.fill((15, 0, 34), (45, 0, 34), "minecraft:oxidized_copper_grate")
    t.fill((45, 0, 8), (45, 0, 33), "minecraft:oxidized_copper_grate")

    # Roof-edge downpipes terminate at those site drains and align with real
    # hall/annex bay lines rather than decorating blank wall areas.
    for x, z, top in ((15, 8, 11), (15, 33, 11), (46, 8, 11), (46, 33, 11), (3, 7, 8), (3, 20, 8)):
        t.fill((x, 1, z), (x, top, z), "create:fluid_pipe")


def _pass10_interior_architecture(t: base.Template) -> None:
    """Create legitimate support, quality, control, records and service rooms."""
    # Ground annex: security/dispatch north, lockers/break west, quality/rework
    # east/south. Every partition has a real controlled threshold.
    t.fill((4, 1, 5), (16, 1, 21), "minecraft:smooth_stone")
    base.partition_z(t, 11, 2, 4, 16, "minecraft:light_gray_concrete", (7, 13))
    base.partition_x(t, 10, 2, 5, 10, "minecraft:light_gray_concrete", 8)
    base.partition_x(t, 9, 2, 12, 21, "minecraft:light_gray_concrete", 18)
    base.desk(t, 5, 2, 7, "north")
    base.desk(t, 13, 2, 7, "north")
    t.fill((4, 2, 13), (5, 3, 18), "minecraft:light_gray_concrete")
    t.set(6, 2, 18, "minecraft:crafting_table")
    t.set(7, 2, 18, "minecraft:blast_furnace", facing="north", lit="false")

    # Upper oversight volume separates live control from maintenance records.
    t.fill((9, 9, 9), (17, 9, 18), "tfmg:factory_floor")
    base.partition_x(t, 12, 10, 10, 18, "minecraft:light_gray_concrete", 14)
    _double_door_z(t, 10, 10, 9, "north")
    t.fill((13, 10, 10), (16, 10, 17), "minecraft:smooth_stone")
    t.fill((9, 10, 10), (11, 10, 17), "minecraft:polished_blackstone")
    base.desk(t, 14, 10, 12, "south")
    base.desk(t, 14, 10, 16, "north")

    # The south gallery end is manual inspection/rework, physically adjacent to
    # induction but behind glazing and a controlled two-wide opening.
    t.fill((14, 1, 24), (16, 1, 30), "tfmg:factory_floor")
    t.fill((14, 2, 24), (14, 5, 24), "create:framed_glass")
    t.fill((14, 2, 30), (14, 5, 30), "create:framed_glass")
    t.fill((15, 2, 29), (16, 3, 30), "immersiveengineering:sheetmetal_steel")

    # East core makes parts issue, isolation and repair/calibration visible from
    # the service route while preserving both stair flights and bridge landing.
    t.fill((44, 1, 15), (47, 1, 28), "tfmg:factory_floor")
    t.fill((44, 2, 24), (44, 5, 28), "immersiveengineering:sheetmetal_steel")
    t.fill((47, 2, 15), (47, 5, 18), "immersiveengineering:sheetmetal_steel")
    t.fill((44, 2, 15), (44, 4, 18), "create:framed_glass")


def _lane_conveyor(t: base.Template, x1: int, x2: int, lane: int) -> None:
    center = (x1 + x2) // 2
    # Continuous roller/depot surface; brass checkpoints break the long run at
    # metering and destination zones without interrupting material continuity.
    for z in range(12, 29):
        casing = "create:brass_casing" if z in {12, 16, 24, 28} else "create:andesite_casing"
        t.fill((x1, 2, z), (x2, 2, z), casing)
        t.set(center, 3, z, "create:depot")
        t.set(x1, 3, z, "create:shaft", axis="x")
        t.set(x2, 3, z, "create:shaft", axis="x")

    # Two process arches provide identification, sorting and exit verification.
    for z in (14, 25):
        t.fill((x1 - 1, 4, z), (x1 - 1, 6, z), "tfmg:steel_block")
        t.fill((x2 + 1, 4, z), (x2 + 1, 6, z), "tfmg:steel_block")
        t.fill((x1 - 1, 6, z), (x2 + 1, 6, z), "minecraft:orange_concrete")
        t.set(x1, 5, z, "minecraft:observer", facing="east")
        t.set(x2, 5, z, "minecraft:observer", facing="west")

    # Lane-local drive and lockout faces connect to the east maintenance side.
    drive_x = x2 + 1
    for z in (16, 24):
        t.set(drive_x, 2, z, "create:large_cogwheel", axis="x")
        t.set(drive_x, 3, z, "create:shaft", axis="x")
        t.set(drive_x, 4, z, "immersiveengineering:connector_lv", facing="up")
        t.set(drive_x, 1, z, "minecraft:yellow_concrete")
    t.set(center, 4, 20, "create:brass_funnel", facing="north", powered="false")
    t.set(center, 4, 27, "create:chute")


def _pass11_operational_systems(t: base.Template) -> None:
    """Install the intact dock-to-sort-to-return operating chain and utilities."""
    lane_ranges = ((18, 20), (24, 26), (30, 32), (36, 38))
    for lane, (x1, x2) in enumerate(lane_ranges, 1):
        _lane_conveyor(t, x1, x2, lane)

    # Paired inbound tongues receive two dock streams into inspection and a
    # transverse metering crossfeed that visibly branches to all four lanes.
    for x1, x2 in ((19, 21), (26, 28)):
        center = (x1 + x2) // 2
        for z in range(31, 37):
            t.fill((x1, 2, z), (x2, 2, z), "create:andesite_casing")
            t.set(center, 3, z, "create:depot")
            t.set(x1, 3, z, "create:shaft", axis="x")
            t.set(x2, 3, z, "create:shaft", axis="x")
    for x in range(18, 41):
        t.set(x, 2, 29, "create:brass_casing")
        t.set(x, 3, 29, "create:shaft", axis="z")
        t.set(x, 2, 30, "create:andesite_casing")
        t.set(x, 3, 30, "create:depot")
    for center in (19, 25, 31, 37):
        t.set(center, 4, 29, "create:brass_funnel", facing="north", powered="false")

    # Identification/measurement arch and dock-control pedestals sit between
    # receiving buffers and induction, never in the protected operator route.
    t.fill((18, 5, 31), (29, 6, 31), "tfmg:steel_block")
    for x in (18, 29):
        t.fill((x, 3, 31), (x, 6, 31), "tfmg:steel_block")
    t.set(20, 5, 31, "minecraft:observer", facing="south")
    t.set(27, 5, 31, "minecraft:observer", facing="south")
    for x in (18, 25, 32, 39):
        t.set(x, 2, 33, "ae2:terminal")

    # North destination trunk receives all lane outputs and turns east into the
    # elevated return. Separate drop buffers feed outbound Docks 03 and 04.
    for x in range(18, 43):
        t.set(x, 2, 10, "create:brass_casing")
        t.set(x, 3, 10, "create:shaft", axis="z")
        t.set(x, 2, 11, "create:andesite_casing")
        t.set(x, 3, 11, "create:depot")
    for center in (19, 25, 31, 37):
        t.set(center, 4, 11, "create:brass_funnel", facing="south", powered="false")
    for z in range(12, 32):
        t.set(40, 4, z, "create:shaft", axis="z")
        t.set(41, 4, z, "create:andesite_casing")
        t.set(41, 5, z, "create:depot")
        t.set(42, 4, z, "create:shaft", axis="z")
    for x1, x2 in ((33, 35), (40, 42)):
        center = (x1 + x2) // 2
        for z in range(32, 37):
            t.fill((x1, 2, z), (x2, 2, z), "create:brass_casing")
            t.set(center, 3, z, "create:depot")
            t.set(x1, 3, z, "create:shaft", axis="x")
            t.set(x2, 3, z, "create:shaft", axis="x")

    # Manual exception/rework spur remains outside freight flow with inspection,
    # hold, bench and controlled return to induction.
    for z in range(25, 30):
        t.set(15, 2, z, "create:depot")
        t.set(16, 2, z, "create:andesite_casing")
    t.set(15, 3, 26, "create:mechanical_press", facing="south")
    t.set(16, 3, 28, "ae2:terminal")
    t.fill((14, 2, 24), (14, 4, 26), "immersiveengineering:sheetmetal_steel")

    # Parts issue and critical spares stay next to Lane 04 and the service core.
    t.fill((44, 2, 24), (44, 4, 28), "immersiveengineering:crate")
    t.set(47, 2, 17, "ae2:terminal")
    t.fill((47, 2, 18), (47, 4, 19), "immersiveengineering:capacitor_mv")
    t.set(44, 2, 16, "create:depot")
    t.set(44, 3, 17, "create:mechanical_press", facing="south")

    # Control/records instrumentation provides real oversight while keeping the
    # future proof node and LOR-006 shelf spatial only and empty.
    t.fill((9, 10, 11), (10, 12, 13), "ae2:drive")
    t.set(11, 10, 12, "ae2:terminal")
    t.set(14, 10, 11, "ae2:terminal")
    t.set(16, 10, 11, "ae2:terminal")
    t.set(16, 10, 15, "ae2:terminal")
    t.set(9, 10, 16, "supplementaries:item_shelf")
    t.set(10, 10, 16, "supplementaries:item_shelf")

    # Connected power, drive, extraction and roof-service systems branch from
    # the east core to every lane and rise into all four accepted monitors.
    t.fill((43, 9, 12), (43, 9, 30), "create:fluid_pipe")
    t.fill((17, 9, 27), (43, 9, 27), "create:fluid_pipe")
    for x in (19, 25, 31, 37):
        t.fill((x, 7, 24), (x, 9, 27), "create:fluid_pipe")
        t.fill((x, 9, 13), (x, 13, 13), "create:fluid_pipe")
        t.set(x, 9, 25, "create:mechanical_pump", facing="south")
        t.set(x, 13, 18, "create:encased_fan", facing="south")
        t.set(x, 13, 23, "create:encased_fan", facing="north")
    t.fill((44, 2, 15), (47, 4, 16), "immersiveengineering:capacitor_mv")
    t.fill((44, 6, 15), (44, 9, 30), "immersiveengineering:sheetmetal_steel")
    for x in (21, 27, 33, 39):
        # Lane buses terminate west of the raised return, then rise over it;
        # the material route itself remains physically continuous.
        t.fill((x, 5, 16), (39, 5, 16), "immersiveengineering:sheetmetal_steel")
        t.set(x, 5, 16, "immersiveengineering:connector_lv", facing="up")
    t.fill((39, 6, 16), (39, 8, 16), "immersiveengineering:sheetmetal_steel")
    t.fill((39, 8, 16), (43, 8, 16), "immersiveengineering:sheetmetal_steel")

    # Operational lighting follows lanes, catwalk, gallery, dock buffers and
    # service trench instead of floating arbitrarily in the high bay.
    for x in (19, 25, 31, 37):
        for z in (13, 18, 24, 28):
            t.set(x, 8, z, "minecraft:sea_lantern")
    for x in (18, 24, 30, 36, 42):
        t.set(x, 10, 20, "minecraft:sea_lantern")
    for z in (14, 20, 26):
        t.set(14, 6, z, "minecraft:sea_lantern")
        t.set(41, 3, z, "minecraft:sea_lantern")


def _pass12_atlas_identity(t: base.Template) -> None:
    """Apply Atlas precision through process frames and restrained wayfinding."""
    # Orange/charcoal process crowns tie lane modules to the accepted exterior
    # dock hierarchy. Identity remains architectural rather than logo wallpaper.
    for x1, x2 in ((18, 20), (24, 26), (30, 32), (36, 38)):
        t.fill((x1 - 1, 6, 12), (x2 + 1, 7, 12), "minecraft:polished_blackstone")
        t.fill((x1, 6, 13), (x2, 6, 13), "minecraft:orange_concrete")
        t.fill((x1 - 1, 6, 28), (x2 + 1, 7, 28), "minecraft:polished_blackstone")
        t.fill((x1, 6, 27), (x2, 6, 27), "minecraft:orange_concrete")

    base.wall_sign(t, 6, 6, 4, "north", "ATLAS KINETIC", "TRANSFER HALL")
    base.wall_sign(t, 18, 7, 36, "north", "INBOUND 01", "REGULAR CRATES")
    base.wall_sign(t, 25, 7, 36, "north", "INBOUND 02", "MIXED ASSEMBLY")
    base.wall_sign(t, 32, 7, 36, "north", "OUTBOUND 03", "REGIONAL A")
    base.wall_sign(t, 39, 7, 36, "north", "OUTBOUND 04", "REGIONAL B")
    for lane, x in enumerate((19, 25, 31, 37), 1):
        base.wall_sign(t, x, 6, 12, "north", "ATLAS TRANSFER", f"LANE {lane:02d}")
        base.wall_sign(t, x, 6, 28, "south", "LINE CLEAR", f"LOCKOUT {lane:02d}")
    base.wall_sign(t, 18, 5, 31, "south", "RECEIVING CHECK", "IDENTIFY / METER")
    base.wall_sign(t, 15, 5, 24, "south", "EXCEPTION", "INSPECT / REWORK")
    base.wall_sign(t, 18, 6, 10, "north", "DESTINATION TRUNK", "ROUTE / DIVERT")
    base.wall_sign(t, 42, 6, 28, "east", "OUTBOUND RETURN", "DOCKS 03 / 04")
    base.wall_sign(t, 14, 5, 14, "west", "OPERATOR GALLERY", "GUARDED ACCESS")
    base.wall_sign(t, 21, 9, 19, "north", "CROSS AISLE", "KEEP LINE CLEAR")
    base.wall_sign(t, 44, 5, 24, "west", "PARTS ISSUE", "CRITICAL SPARES")
    base.wall_sign(t, 47, 5, 16, "west", "MASTER ISOLATION", "AUTHORIZED ONLY")
    base.wall_sign(t, 13, 12, 10, "west", "CONTROL / QUALITY", "THROUGHPUT")
    base.wall_sign(t, 11, 12, 16, "east", "MAINT. RECORDS", "PROOF RESERVED")
    base.wall_sign(t, 10, 12, 17, "south", "LOR SHELF", "SPATIAL HOLD ONLY")
    base.wall_sign(t, 39, 2, 14, "west", "DRIVE TRENCH", "LOCKOUT FIRST")


def build_gate_b_intact() -> base.Template:
    t = build_gate_a_massing_r2()
    _pass7_structural_system(t)
    _pass8_circulation_and_access(t)
    _pass9_exterior_architecture(t)
    _pass10_interior_architecture(t)
    _pass11_operational_systems(t)
    _pass12_atlas_identity(t)
    return t


def _assert_gate_a_source_freeze() -> None:
    gate_a = build_gate_a_massing_r2()
    gate_a.save(TEMP_GATE_A_NAME)
    try:
        actual = hashlib.sha256(TEMP_GATE_A_NBT.read_bytes()).hexdigest()
    finally:
        TEMP_GATE_A_NBT.unlink(missing_ok=True)
    if actual != GATE_A_MODEL_SHA256:
        raise AssertionError(f"accepted Gate-A r2 source drifted: {actual} != {GATE_A_MODEL_SHA256}")


def _assert_clear(
    t: base.Template,
    low: tuple[int, int, int],
    high: tuple[int, int, int],
    label: str,
    allowed: set[str] | None = None,
) -> None:
    allowed = allowed or set()
    for x in range(low[0], high[0] + 1):
        for y in range(low[1], high[1] + 1):
            for z in range(low[2], high[2] + 1):
                name = _name(t, (x, y, z))
                if name not in AIR | allowed:
                    raise AssertionError(f"{label} obstruction at {(x, y, z)}: {name}")


def _assert_intact_contracts(t: base.Template) -> None:
    if tuple(t.size) != SIZE:
        raise AssertionError(f"OWS-010 Gate-B dimensions drifted: {t.size}")
    if any(not (0 <= x < SIZE[0] and 0 <= y < SIZE[1] and 0 <= z < SIZE[2]) for x, y, z in t.blocks):
        raise AssertionError("OWS-010 Gate-B exceeds accepted 49x16x43 envelope")

    # Exact exterior anchors freeze the accepted dock hierarchy, facade rhythm,
    # control crown, east service spine, roof monitors and transfer crown.
    frozen = {
        (17, 10, 33): "minecraft:orange_concrete",
        (29, 10, 33): "tfmg:steel_block",
        (30, 13, 33): "minecraft:orange_concrete",
        (33, 9, 35): "immersiveengineering:sheetmetal_steel",
        (41, 11, 36): "minecraft:orange_concrete",
        (12, 8, 15): "minecraft:orange_concrete",
        (14, 4, 17): "create:framed_glass",
        (47, 10, 10): "minecraft:orange_concrete",
        (45, 6, 10): "create:framed_glass",
        (16, 9, 5): "minecraft:orange_concrete",
        (19, 7, 8): "create:framed_glass",
        (7, 15, 7): "minecraft:orange_concrete",
        (17, 12, 15): "create:framed_glass",
        (47, 13, 18): "tfmg:steel_block",
        (48, 14, 18): "minecraft:orange_concrete",
        (18, 15, 18): "minecraft:orange_concrete",
        (24, 15, 18): "minecraft:orange_concrete",
        (30, 15, 18): "minecraft:orange_concrete",
        (36, 15, 18): "minecraft:orange_concrete",
        (28, 15, 7): "minecraft:orange_concrete",
    }
    for pos, expected in frozen.items():
        actual = _name(t, pos)
        if actual != expected:
            raise AssertionError(f"accepted Gate-A r2 aspect changed at {pos}: {actual} != {expected}")

    # Four complete lanes, two inbound feeds, common trunk, return and paired
    # outbound buffers remain continuous in the intact operating state.
    for center in (19, 25, 31, 37):
        for z in range(12, 29):
            if _name(t, (center, 3, z)) != "create:depot":
                raise AssertionError(f"continuous transfer lane missing at {(center, 3, z)}")
    for center in (20, 27):
        for z in range(31, 37):
            if _name(t, (center, 3, z)) != "create:depot":
                raise AssertionError(f"continuous inbound tongue missing at {(center, 3, z)}")
    for x in range(18, 43):
        if _name(t, (x, 3, 11)) != "create:depot":
            raise AssertionError(f"destination trunk missing at {(x, 3, 11)}")
    for z in range(12, 32):
        if _name(t, (41, 5, z)) != "create:depot":
            raise AssertionError(f"outbound return missing at {(41, 5, z)}")
    for center in (34, 41):
        for z in range(32, 37):
            if _name(t, (center, 3, z)) != "create:depot":
                raise AssertionError(f"outbound buffer missing at {(center, 3, z)}")

    # Principal operator/catwalk and maintenance/trench paths retain real
    # playable clearances. Doors and stairs are checked separately.
    _assert_clear(t, (15, 2, 18), (16, 4, 23), "ground operator gallery")
    _assert_clear(t, (17, 8, 20), (42, 9, 21), "guarded cross-aisle bridge")
    _assert_clear(t, (42, 2, 12), (44, 3, 14), "north maintenance route")
    _assert_clear(t, (42, 2, 29), (44, 3, 31), "south maintenance route")
    _assert_clear(t, (40, 1, 14), (41, 2, 27), "drive trench", {"minecraft:sea_lantern"})

    # Both controlled independent thresholds contain complete door halves.
    for x, z in ((9, 4),):
        for dx in (0, 1):
            for y in (2, 3):
                if _name(t, (x + dx, y, z)) != "minecraft:iron_door":
                    raise AssertionError(f"north staff door missing at {(x + dx, y, z)}")
    for x, z in ((48, 20),):
        for dz in (0, 1):
            for y in (2, 3):
                if _name(t, (x, y, z + dz)) != "minecraft:iron_door":
                    raise AssertionError(f"east service door missing at {(x, y, z + dz)}")

    names = [t.palette[entry[0]]["Name"] for entry in t.blocks.values()]
    forbidden = {"minecraft:chest", "minecraft:trapped_chest", "minecraft:spawner", "minecraft:lectern"}
    found = forbidden.intersection(names)
    if found:
        raise AssertionError(f"Gate-B contains deferred history/encounter/loot/proof content: {sorted(found)}")
    requirements = {
        "create:depot": 150,
        "create:shaft": 180,
        "create:fluid_pipe": 100,
        "create:andesite_casing": 150,
        "create:brass_casing": 65,
        "create:large_cogwheel": 8,
        "minecraft:smooth_stone_stairs": 22,
        # Template-safe grates replace connective iron bars at serialization.
        "minecraft:oxidized_copper_grate": 180,
        "tfmg:steel_block": 850,
        "immersiveengineering:capacitor_mv": 12,
        "ae2:terminal": 10,
    }
    for name, minimum in requirements.items():
        if names.count(name) < minimum:
            raise AssertionError(f"intact system coverage sparse for {name}: {names.count(name)} < {minimum}")
    if sum(name.endswith("_wall_sign") for name in names) < 20:
        raise AssertionError("Atlas intact-state wayfinding unexpectedly sparse")


def _git_blob(path: Path) -> str:
    return subprocess.run(
        ["git", "hash-object", str(path.relative_to(ROOT))],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _git_head() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()


def main() -> None:
    review = GATE_A_REVIEW.read_text(encoding="utf-8")
    if "**Decision:** **PASSED**" not in review or GATE_A_MODEL_SHA256 not in review:
        raise AssertionError("OWS-010 accepted Gate-A r2 authority/hash missing")
    shipping_bytes = SHIPPING_PATH.read_bytes()
    if hashlib.sha256(shipping_bytes).hexdigest() != FROZEN_SHIPPING_SHA256:
        raise AssertionError("OWS-010 shipping SHA drifted before Gate-B render")
    if _git_blob(SHIPPING_PATH) != FROZEN_SHIPPING_BLOB:
        raise AssertionError("OWS-010 shipping Git blob drifted before Gate-B render")
    _assert_gate_a_source_freeze()

    model = build_gate_b_intact()
    _assert_intact_contracts(model)
    model.save(TEMP_NAME)
    try:
        model_bytes = TEMP_NBT.read_bytes()
        size, blocks = unpack_structure(TEMP_NBT)
        occupied_min = [min(point[axis] for point in blocks) for axis in range(3)]
        occupied_max = [max(point[axis] for point in blocks) for axis in range(3)]
        head = _git_head()
        manifest = render_review_set(
            target=TARGET,
            gate="gate_b_intact",
            revision=f"intact-r1@{head[:8]}",
            damage_state="D0 intact / operational",
            source_commit=head,
            source_path="review-only:render_ows010_gate_b_intact.build_gate_b_intact()",
            size=size,
            blocks=blocks,
            output_dir=OUTPUT_DIR,
            camera_set=CAMERA_SET,
        )
        manifest.update({
            "review_model_nbt_sha256": hashlib.sha256(model_bytes).hexdigest(),
            "review_builder_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "review_model_non_air_blocks": len(blocks),
            "review_model_occupied_bounds": {"min": occupied_min, "max": occupied_max},
            "gate_a_r2_model_sha256": GATE_A_MODEL_SHA256,
            "gate_a_frozen_aspects_asserted": 20,
            "gate_b_passes_implemented": [7, 8, 9, 10, 11, 12],
            "intact_transfer_lanes": 4,
            "paired_inbound_docks": [1, 2],
            "paired_outbound_docks": [3, 4],
            "history_damage_encounters_loot_proof_present": False,
            "lor_006_manual_placed": False,
            "lor_006_spatial_context_reserved": True,
            "authoritative_shipping_modified": False,
            "shipping_nbt_sha256_before": FROZEN_SHIPPING_SHA256,
            "shipping_nbt_sha256_after": hashlib.sha256(SHIPPING_PATH.read_bytes()).hexdigest(),
            "shipping_nbt_git_blob_before": FROZEN_SHIPPING_BLOB,
            "shipping_nbt_git_blob_after": _git_blob(SHIPPING_PATH),
            "visual_review_status": "rendered_pending_independent_review",
        })
        if manifest["shipping_nbt_sha256_after"] != FROZEN_SHIPPING_SHA256 or manifest["shipping_nbt_git_blob_after"] != FROZEN_SHIPPING_BLOB:
            raise AssertionError("OWS-010 shipping changed during Gate-B render")
        (OUTPUT_DIR / "review_manifest.json").write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n"
        )
    finally:
        TEMP_NBT.unlink(missing_ok=True)

    if SHIPPING_PATH.read_bytes() != shipping_bytes:
        raise AssertionError("OWS-010 shipping bytes changed during Gate-B render")
    print(
        f"Rendered {TARGET} Gate B r1 intact at {manifest['dimensions']} with "
        f"{manifest['review_model_non_air_blocks']} positions; independent review required."
    )


if __name__ == "__main__":
    main()
