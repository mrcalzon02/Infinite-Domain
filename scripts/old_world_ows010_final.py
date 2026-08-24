#!/usr/bin/env python3
"""Pure side-effect-free authoritative OWS-010 production builder.

This module reconstructs the independently accepted Gate-C r1 D3 model and
adds only a restrained vanilla-first Pass-19 overlay. It performs no rendering,
serialization, filesystem access, shared registry mutation, shipping write, or
gate decision. The coordinator may import build_010 for generation.
"""
from __future__ import annotations

import generate_wasteland_sites as base


SIZE = (49, 16, 43)
ACCEPTED_GATE_C_D3_SHA256 = "29b9efa13b9ae71cf210aa3630cba224c31d4410d3aea5a4a97d772aa8ef5fc8"
PROOF_LOOT_TABLE = "infinite_domain:chests/old_world/ows_010_atlas_conveyor_transfer_hall"
PROOF_POS = (9, 11, 17)
LOR_ITEM = "kubejs:atlas_transfer_maintenance_manual"
LOR_SHELVES = ((9, 10, 16), (10, 10, 16))
SPAWNERS = {
    (23, 2, 33): "minecraft:zombie",
    (35, 2, 26): "minecraft:zombie",
    (45, 2, 26): "minecraft:cave_spider",
}
AIR = {None, "minecraft:air", "minecraft:cave_air", "minecraft:void_air", "minecraft:structure_void"}
PRODUCTION_REQUIRED_BLOCKS = (
    "minecraft:orange_concrete",
    "create:depot",
    "create:mechanical_press",
    "create:andesite_casing",
)
PASS19_MICRODETAIL = {
    (39, 3, 24): "minecraft:cobweb",
    (45, 2, 29): "minecraft:cobweb",
    (45, 3, 31): "minecraft:cobweb",
    (48, 1, 31): "minecraft:brown_mushroom",
    (40, 1, 38): "minecraft:brown_mushroom",
    (42, 1, 39): "minecraft:red_mushroom",
    (44, 1, 40): "minecraft:brown_mushroom",
    (39, 1, 40): "minecraft:brown_mushroom",
}


def _name(t: base.Template, pos: tuple[int, int, int]) -> str | None:
    row = t.blocks.get(pos)
    return None if row is None else t.palette[row[0]]["Name"]


def _count(t: base.Template, block: str) -> int:
    return sum(_name(t, pos) == block for pos in t.blocks)

def _site_and_courts(t: base.Template) -> None:
    """Retain separate north staff, south truck, and east service approaches."""
    t.fill((0, 0, 0), (48, 0, 42), "minecraft:grass_block")

    # North staff/security approach remains human-scaled and separate from freight.
    t.fill((2, 0, 0), (18, 0, 8), "minecraft:smooth_stone")
    t.fill((7, 0, 0), (12, 0, 10), "minecraft:orange_concrete")

    # South truck court serves four dock portals; dark centerlines reserve
    # vehicle lanes while orange shoulders belong to the building hierarchy.
    t.fill((14, 0, 35), (48, 0, 42), "tfmg:asphalt")
    for x in (20, 27, 34, 41):
        t.fill((x, 0, 38), (x, 0, 42), "minecraft:light_gray_concrete")

    # East service approach never crosses the north staff threshold.
    t.fill((45, 0, 8), (48, 0, 36), "tfmg:asphalt")
    t.fill((46, 0, 14), (48, 0, 26), "minecraft:yellow_concrete")

def _support_and_control_annex(t: base.Template) -> None:
    """Preserve the donor's low support annex and add a process-facing control crown."""
    base.shell(
        t,
        (3, 1, 4),
        (17, 9, 22),
        "minecraft:light_gray_concrete",
        "minecraft:smooth_stone",
        "tfmg:steel_block",
    )

    # Recessed north staff entrance and supported Atlas-orange canopy.
    t.clear((7, 2, 4), (12, 6, 4))
    t.fill((5, 8, 1), (14, 8, 6), "minecraft:orange_concrete")
    for x in (5, 14):
        t.fill((x, 1, 2), (x, 7, 2), "tfmg:steel_block")

    # Raised control/quality/records volume overlooks lane induction and output.
    # Its west portion reserves maintenance records and a non-loot LOR shelf;
    # no proof or manual item is placed in this massing model.
    base.shell(
        t,
        (8, 9, 8),
        (18, 13, 19),
        "minecraft:orange_concrete",
        "tfmg:steel_block",
        "minecraft:light_gray_concrete",
    )
    t.fill((18, 10, 10), (18, 12, 17), "create:framed_glass")
    t.fill((10, 10, 19), (17, 12, 19), "create:framed_glass")

def _high_bay_shell_and_docks(t: base.Template) -> None:
    """Create a four-bay Atlas transfer hall with paired dock hierarchy."""
    base.shell(
        t,
        (15, 1, 7),
        (46, 12, 37),
        "minecraft:light_gray_concrete",
        "tfmg:factory_floor",
        "tfmg:steel_block",
    )

    dock_bays = ((18, 22), (25, 29), (32, 36), (39, 43))
    for index, (x1, x2) in enumerate(dock_bays, 1):
        # Full freight portals and deep structural frames correspond to lanes.
        t.clear((x1, 2, 37), (x2, 7, 37))
        t.fill((x1 - 1, 1, 36), (x1 - 1, 10, 38), "tfmg:steel_block")
        t.fill((x2 + 1, 1, 36), (x2 + 1, 10, 38), "tfmg:steel_block")
        crown = "minecraft:orange_concrete" if index <= 2 else "minecraft:black_concrete"
        t.fill((x1 - 1, 8, 35), (x2 + 1, 11, 38), crown)
        # Orange inset retains one Atlas family across inbound/outbound pairs.
        t.fill((x1, 9, 34), (x2, 10, 35), "minecraft:orange_concrete")

    # Repeated road-facing piers make the lane rhythm architectural.
    for x in (15, 17, 24, 31, 38, 45, 46):
        t.fill((x, 1, 35), (x, 12, 37), "tfmg:steel_block")

def _transfer_process_massing(t: base.Template) -> None:
    """Reserve continuous inbound, four-lane, trunk, and outbound-return volumes."""
    lane_ranges = ((18, 20), (24, 26), (30, 32), (36, 38))

    # Two inbound dock tongues feed a shared south induction/crossfeed.
    for x1, x2 in ((19, 21), (26, 28)):
        t.fill((x1, 2, 31), (x2, 3, 37), "minecraft:black_concrete")
    t.fill((18, 2, 28), (40, 3, 31), "minecraft:black_concrete")
    t.fill((18, 4, 29), (40, 5, 30), "minecraft:orange_concrete")

    # Four uninterrupted process lanes rise enough to read in cutaway while
    # leaving a full player-scale clear zone beneath the future catwalk.
    for index, (x1, x2) in enumerate(lane_ranges, 1):
        t.fill((x1, 2, 12), (x2, 3, 28), "minecraft:black_concrete")
        t.fill((x1, 4, 14), (x2, 4, 16), "minecraft:orange_concrete")
        t.fill((x1, 4, 24), (x2, 4, 26), "minecraft:orange_concrete")
        # Lane-local service shoulders reserve reachable drive/isolation faces.
        shoulder = x2 + 1 if index < 4 else x1 - 1
        t.fill((shoulder, 1, 13), (shoulder, 1, 27), "minecraft:yellow_concrete")

    # Common north destination trunk receives every lane output.
    t.fill((18, 2, 9), (42, 3, 12), "minecraft:black_concrete")
    t.fill((18, 4, 9), (42, 5, 10), "minecraft:orange_concrete")

    # Elevated east return/drop keeps outbound freight separate from inbound
    # crossfeed before descending into Dock 03 and Dock 04 tongues.
    t.fill((40, 4, 9), (43, 5, 32), "minecraft:black_concrete")
    t.fill((40, 6, 11), (43, 6, 29), "minecraft:orange_concrete")
    for x1, x2 in ((33, 35), (40, 42)):
        t.fill((x1, 2, 31), (x2, 3, 37), "minecraft:black_concrete")

def _operator_and_maintenance_access(t: base.Template) -> None:
    """Reserve broad, protected routes rather than decorative scaffolding."""
    # West operator gallery joins the annex to lane starts and outputs.
    base.shell(
        t,
        (13, 1, 10),
        (17, 8, 31),
        "minecraft:light_gray_concrete",
        "minecraft:smooth_stone",
        "tfmg:steel_block",
    )
    t.fill((17, 3, 12), (17, 7, 29), "create:framed_glass")

    # Guarded cross-aisle bridge reserves safe operator transfer above all lanes.
    t.fill((16, 7, 19), (43, 8, 22), "minecraft:light_gray_concrete")
    t.fill((16, 9, 19), (43, 9, 19), "minecraft:orange_concrete")
    t.fill((16, 9, 22), (43, 9, 22), "minecraft:orange_concrete")

    # East service core and long maintenance face connect floor, bridge, roof,
    # parts issue, lockout and output return without entering operator space.
    base.shell(
        t,
        (43, 1, 15),
        (48, 14, 28),
        "tfmg:steel_block",
        "minecraft:smooth_stone",
        "minecraft:orange_concrete",
    )
    t.fill((42, 2, 13), (44, 3, 31), "minecraft:light_gray_concrete")
    t.fill((42, 4, 14), (42, 8, 29), "create:framed_glass")
    t.fill((42, 7, 20), (47, 8, 22), "minecraft:light_gray_concrete")

def _roof_process_system(t: base.Template) -> None:
    """Align four lane monitors with one connected transfer/service crown."""
    lane_ranges = ((18, 20), (24, 26), (30, 32), (36, 38))
    for x1, x2 in lane_ranges:
        base.shell(
            t,
            (x1, 12, 13),
            (x2, 15, 27),
            "create:framed_glass",
            "tfmg:steel_block",
            "minecraft:orange_concrete",
        )

    # North transfer crown ties all lane monitors to the destination trunk.
    base.shell(
        t,
        (16, 12, 7),
        (43, 15, 13),
        "tfmg:steel_block",
        "minecraft:light_gray_concrete",
        "minecraft:orange_concrete",
    )
    t.fill((18, 13, 6), (40, 15, 6), "minecraft:orange_concrete")

    # East roof-service bar terminates at the maintenance core and aligns with
    # the outbound return instead of becoming arbitrary roof clutter.
    base.shell(
        t,
        (40, 10, 10),
        (47, 14, 31),
        "immersiveengineering:sheetmetal_steel",
        "tfmg:steel_block",
        "minecraft:orange_concrete",
    )

def build_gate_a_massing() -> base.Template:
    t = base.Template(SIZE)
    _site_and_courts(t)
    _support_and_control_annex(t)
    _high_bay_shell_and_docks(t)
    _transfer_process_massing(t)
    _operator_and_maintenance_access(t)
    _roof_process_system(t)
    return t

def _split_dock_crowns(t: base.Template) -> None:
    """Make inbound and outbound dock pairs distinct without moving portals."""
    # Inbound 01–02: one higher, forward orange gantry with two dark inset hoods.
    t.fill((17, 10, 33), (30, 12, 36), "minecraft:orange_concrete")
    for x1, x2 in ((18, 22), (25, 29)):
        t.fill((x1, 8, 33), (x2, 10, 35), "tfmg:steel_block")
        t.fill((x1 + 1, 8, 32), (x2 - 1, 9, 33), "minecraft:black_concrete")

    # The pair break is a tall steel fin aligned with the frozen center frames.
    t.fill((30, 8, 32), (31, 14, 38), "tfmg:steel_block")
    t.fill((30, 12, 32), (31, 14, 34), "minecraft:orange_concrete")

    # Outbound 03–04: a lower, recessed charcoal assembly under an orange cap.
    t.fill((32, 8, 35), (44, 10, 38), "minecraft:black_concrete")
    t.fill((32, 11, 35), (44, 12, 37), "minecraft:orange_concrete")
    for x1, x2 in ((32, 36), (39, 43)):
        t.fill((x1, 8, 34), (x2, 9, 35), "immersiveengineering:sheetmetal_steel")

def _articulate_long_elevations(t: base.Template) -> None:
    """Replace flush side planes with truss-aligned piers and recessed bands."""
    # West operator-gallery elevation: projected steel piers, recessed glazing,
    # and an orange clerestory header express a supervised personnel edge.
    for z in (10, 15, 20, 25, 30):
        t.fill((12, 2, z), (12, 9, z + 1), "tfmg:steel_block")
        t.fill((12, 8, z), (13, 9, z + 1), "minecraft:orange_concrete")
    for z1, z2 in ((12, 14), (17, 19), (22, 24), (27, 29)):
        t.clear((13, 3, z1), (13, 6, z2))
        t.fill((14, 3, z1), (14, 6, z2), "create:framed_glass")
    t.fill((12, 7, 11), (12, 8, 29), "minecraft:orange_concrete")

    # Gallery/service threshold at the south end is a deep massing recess, not
    # a detailed door. It aligns to the existing protected operator route.
    t.clear((13, 3, 29), (13, 6, 31))
    t.fill((12, 1, 28), (12, 8, 29), "tfmg:steel_block")
    t.fill((13, 3, 28), (13, 8, 29), "tfmg:steel_block")
    t.fill((12, 1, 31), (12, 8, 32), "tfmg:steel_block")
    t.fill((13, 3, 31), (13, 8, 32), "tfmg:steel_block")
    t.fill((11, 7, 28), (13, 9, 32), "minecraft:orange_concrete")

    # East hall elevation: exposed segments north and south of the maintenance
    # core receive projected lane/truss piers and deeply recessed clerestories.
    for z in (7, 13, 29, 35):
        t.fill((47, 1, z), (48, 12, z + 1), "tfmg:steel_block")
        t.fill((47, 9, z), (48, 11, z + 1), "minecraft:orange_concrete")
    for z1, z2 in ((9, 12), (31, 34)):
        t.clear((46, 4, z1), (46, 8, z2))
        t.fill((45, 4, z1), (45, 8, z2), "create:framed_glass")
        t.fill((47, 9, z1), (47, 10, z2), "minecraft:orange_concrete")

    # North transfer elevation: lane/truss-aligned piers and four recessed
    # clerestory bays reveal the destination-trunk rhythm on the blank rear view.
    for x in (16, 22, 28, 34, 40, 46):
        t.fill((x, 2, 5), (x + 1, 12, 6), "tfmg:steel_block")
        t.fill((x, 9, 5), (x + 1, 11, 7), "minecraft:orange_concrete")
    for x1, x2 in ((18, 21), (24, 27), (30, 33), (36, 39)):
        t.clear((x1, 5, 7), (x2, 9, 7))
        t.fill((x1, 5, 8), (x2, 9, 8), "create:framed_glass")
        t.fill((x1, 10, 6), (x2, 11, 7), "minecraft:orange_concrete")

def _strengthen_control_oversight(t: base.Template) -> None:
    """Make the accepted crown read as a hall-facing control/records lantern."""
    # Reprofile within the accepted crown footprint with a stronger glazed east
    # face, darker datum, and a raised orange cap distinguishable from hall roof.
    t.fill((8, 9, 8), (17, 10, 19), "tfmg:steel_block")
    t.fill((17, 10, 9), (17, 13, 18), "create:framed_glass")
    t.fill((18, 10, 9), (18, 11, 18), "create:framed_glass")
    t.fill((17, 9, 9), (18, 14, 9), "tfmg:steel_block")
    for z in (13, 18):
        t.fill((17, 9, z), (17, 14, z), "tfmg:steel_block")
    t.fill((7, 14, 7), (17, 15, 20), "minecraft:orange_concrete")
    t.fill((10, 14, 20), (17, 15, 21), "tfmg:steel_block")

    # Two supports and an underslung orange datum visibly connect oversight to
    # the operator gallery while remaining below the frozen roof monitors.
    for z in (10, 17):
        t.fill((17, 6, z), (18, 9, z + 1), "tfmg:steel_block")
    t.fill((16, 8, 10), (18, 9, 17), "minecraft:orange_concrete")

def _clarify_maintenance_core(t: base.Template) -> None:
    """Tie the east service threshold, cross bridge, and roof bar into one core."""
    # A recessed base threshold and tall paired piers create a real service entry.
    t.clear((48, 2, 20), (48, 6, 23))
    t.fill((47, 2, 20), (47, 6, 23), "minecraft:black_concrete")
    for z1, z2 in ((18, 19), (24, 25)):
        t.fill((47, 2, z1), (48, 15, z2), "tfmg:steel_block")
        t.fill((48, 8, z1), (48, 14, z2), "minecraft:orange_concrete")

    # The accepted bridge footprint stays fixed at Y7–8; r2 adds a visible
    # orange/steel hood above it and continues that datum into the roof cap.
    t.fill((40, 9, 19), (48, 10, 19), "minecraft:orange_concrete")
    t.fill((40, 9, 23), (48, 10, 23), "minecraft:orange_concrete")
    t.fill((46, 9, 20), (48, 10, 22), "tfmg:steel_block")
    t.fill((43, 14, 15), (48, 15, 28), "immersiveengineering:sheetmetal_steel")
    t.fill((47, 14, 17), (48, 15, 26), "minecraft:orange_concrete")

def build_gate_a_massing_r2() -> base.Template:
    t = build_gate_a_massing()
    _split_dock_crowns(t)
    _articulate_long_elevations(t)
    _strengthen_control_oversight(t)
    _clarify_maintenance_core(t)
    return t

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

def build_d0() -> base.Template:
    return build_gate_b_intact()

def build_d1() -> base.Template:
    """Show competent Lane-04 cannibalization while three lines stay live."""
    t = build_d0()

    # Lockout datum encloses the complete original Lane-04 bed without moving
    # its input/output or structural bay. Yellow is used only at isolation.
    t.fill((35, 1, 13), (35, 1, 27), "minecraft:yellow_concrete")
    t.fill((36, 1, 12), (38, 1, 12), "minecraft:yellow_concrete")
    t.fill((36, 1, 28), (38, 1, 28), "minecraft:yellow_concrete")

    # Four replaceable roller/depot modules and both drive clusters are removed.
    # The casing bed and lane endpoints survive so original function is legible.
    for z in (16, 17, 24, 25):
        t.clear((36, 3, z), (38, 3, z))
        t.fill((36, 2, z), (38, 2, z), "minecraft:weathered_copper")
    for z in (16, 24):
        t.clear((39, 2, z), (39, 4, z))
        t.fill((39, 1, z), (39, 2, z), "minecraft:oxidized_copper_grate")

    # Removed standardized modules are staged at east parts issue in the same
    # positional grammar as the missing Lane-04 rollers and drive assemblies.
    for z in (24, 25, 27, 28):
        t.set(45, 2, z, "create:shaft", axis="x")
        t.set(46, 2, z, "create:depot")
        t.set(47, 2, z, "create:andesite_casing")
    t.set(45, 3, 24, "create:large_cogwheel", axis="x")
    t.set(47, 3, 24, "create:large_cogwheel", axis="x")
    t.set(45, 3, 28, "immersiveengineering:connector_lv", facing="up")
    t.set(47, 3, 28, "immersiveengineering:connector_lv", facing="up")

    # Lanes 01-03 receive the best salvaged spares at their existing service
    # faces; these are added modules, not relocated lane geometry.
    for x in (21, 27, 33):
        t.set(x, 2, 18, "create:large_cogwheel", axis="x")
        t.set(x, 3, 18, "create:shaft", axis="x")
        t.set(x, 4, 18, "immersiveengineering:connector_lv", facing="up")
        t.set(x, 2, 26, "create:brass_casing")
        t.set(x, 3, 26, "create:mechanical_pump", facing="south")

    # A temporary overhead drive/service bypass crosses all four lanes, ties
    # into existing branches, and is visibly patched at the dead fourth line.
    t.fill((19, 7, 24), (39, 7, 24), "create:fluid_pipe")
    for x in (19, 25, 31, 37):
        t.set(x, 7, 24, "create:mechanical_pump", facing="east")
    t.fill((36, 8, 24), (39, 8, 24), "minecraft:weathered_cut_copper")

    # Shrinking stores and tagged removed modules accumulate at real issue and
    # rework positions while circulation and proof/LOR reservations stay clear.
    t.fill((44, 5, 24), (44, 6, 28), "immersiveengineering:crate")
    t.fill((14, 2, 24), (14, 4, 26), "minecraft:weathered_copper")
    t.set(16, 3, 28, "minecraft:yellow_concrete")
    t.fill((9, 10, 14), (10, 10, 15), "minecraft:weathered_cut_copper")

    # The component-starved monitor receives a temporary intact patch. D3 will
    # fail only this documented intervention and the connected east service edge.
    t.fill((36, 14, 24), (38, 14, 26), "minecraft:weathered_cut_copper")
    t.fill((46, 10, 29), (47, 10, 33), "minecraft:weathered_cut_copper")

    base.wall_sign(t, 36, 5, 13, "north", "LANE 04 LOCKOUT", "PARTS TRANSFER")
    base.wall_sign(t, 36, 5, 27, "south", "LANE 04 INACTIVE", "BED RETAINED")
    base.wall_sign(t, 35, 5, 18, "east", "MODULES REMOVED", "WORK ORDER 4-17")
    base.wall_sign(t, 35, 5, 25, "east", "DRIVES REMOVED", "ISSUE TO 01-03")
    base.wall_sign(t, 45, 4, 24, "west", "SALVAGED MODULES", "INSPECT BEFORE USE")
    base.wall_sign(t, 45, 4, 28, "west", "STOCK CRITICAL", "NO NEW DRIVES")
    base.wall_sign(t, 19, 8, 24, "south", "TEMP SERVICE BUS", "LINES 01-03 PRIORITY")
    base.wall_sign(t, 9, 12, 14, "east", "MAINT. SHORTAGE", "TRANSFER AUTHORIZED")

    return t

def _place_proof_and_encounters(t: base.Template) -> None:
    if _name(t, PROOF_POS) not in AIR or _name(t, (9, 12, 17)) not in AIR or _name(t, (10, 11, 17)) not in AIR:
        raise AssertionError("OWS-010 records proof position, headroom or east approach is obstructed")
    t.chest(*PROOF_POS, PROOF_LOOT_TABLE, facing="east")

    for (x, y, z), mob in SPAWNERS.items():
        if _name(t, (x, y, z)) not in AIR or _name(t, (x, y + 1, z)) not in AIR:
            raise AssertionError(f"OWS-010 spawner position obstructed at {(x, y, z)}")
        t.spawner(x, y, z, mob, count=1, nearby=3)

def build_accepted_d3() -> base.Template:
    """Grow restrained long-abandonment damage from the starved Lane-04 system."""
    t = build_d1()

    # The temporary Lane-04 monitor patch opens locally. Primary side rails and
    # neighboring monitor bays survive; weathered edges remain supported.
    t.clear((37, 15, 24), (38, 15, 26))
    t.clear((38, 13, 24), (38, 14, 26))
    t.fill((36, 14, 23), (38, 14, 23), "minecraft:weathered_cut_copper")
    t.fill((36, 14, 27), (38, 14, 27), "minecraft:weathered_cut_copper")
    t.fill((36, 13, 24), (36, 14, 26), "minecraft:weathered_cut_copper")

    # Roof fragments land on the already locked lane and removed-module gaps.
    for pos in ((37, 3, 24), (38, 3, 25), (36, 3, 24), (39, 1, 25)):
        t.set(*pos, "minecraft:gravel")
    t.set(36, 3, 25, "minecraft:weathered_cut_copper")

    # Water follows the opened monitor, Lane-04 service shoulder and depressed
    # drive trench rather than spreading evenly through the facility.
    t.fill((35, 1, 23), (35, 1, 28), "minecraft:moss_block")
    t.fill((36, 1, 26), (39, 1, 28), "minecraft:mossy_stone_bricks")
    t.fill((40, 0, 23), (41, 0, 27), "minecraft:mossy_cobblestone")
    for pos in ((35, 2, 23), (39, 3, 27), (40, 1, 23), (41, 1, 28)):
        t.set(*pos, "minecraft:cobweb")
    for pos in ((35, 2, 27), (39, 2, 28), (41, 1, 24)):
        t.set(*pos, "minecraft:brown_mushroom")

    # Connected east clerestory/service flashing fails locally. Fragments land
    # on the exterior service strip directly below, outside protected routes.
    t.clear((46, 6, 31), (46, 8, 33))
    t.fill((46, 5, 30), (46, 5, 34), "minecraft:weathered_cut_copper")
    t.fill((45, 9, 31), (47, 9, 33), "minecraft:weathered_cut_copper")
    for pos in ((47, 1, 31), (48, 1, 32), (47, 1, 33), (48, 1, 34)):
        t.set(*pos, "minecraft:gravel")
    t.fill((45, 0, 29), (48, 0, 35), "minecraft:cracked_stone_bricks")

    # Dock-04 and east service exposure remain subordinate to the Lane-04 cause.
    t.fill((39, 0, 38), (44, 0, 42), "minecraft:mossy_cobblestone")
    for pos in ((40, 2, 34), (42, 2, 35), (44, 2, 32), (45, 3, 30)):
        t.set(*pos, "minecraft:cobweb")

    # Final gameplay nodes are added after historical and route freeze checks.

    _place_proof_and_encounters(t)

    return t

def _assert_proof_and_gameplay(t: base.Template) -> None:
    row = t.blocks.get(PROOF_POS)
    if row is None or t.palette[row[0]]["Name"] != "minecraft:chest":
        raise AssertionError("OWS-010 canonical proof chest missing")
    if not row[1] or row[1].get("LootTable") != PROOF_LOOT_TABLE:
        raise AssertionError("OWS-010 proof chest uses wrong loot table")
    if _name(t, (9, 12, 17)) not in AIR or _name(t, (10, 11, 17)) not in AIR:
        raise AssertionError("OWS-010 proof approach obstructed")
    matches = sum(1 for _, nbt in t.blocks.values() if nbt and nbt.get("LootTable") == PROOF_LOOT_TABLE)
    if matches != 1 or _count(t, "minecraft:chest") != 1:
        raise AssertionError(f"OWS-010 requires exactly one proof node; found {matches}")
    if _count(t, "minecraft:spawner") != len(SPAWNERS):
        raise AssertionError("OWS-010 requires exactly three bounded spawners")
    for pos, expected in SPAWNERS.items():
        row = t.blocks.get(pos)
        if row is None or t.palette[row[0]]["Name"] != "minecraft:spawner":
            raise AssertionError(f"OWS-010 spawner missing at {pos}")
        mob = (((row[1] or {}).get("SpawnData") or {}).get("entity") or {}).get("id")
        if mob != expected:
            raise AssertionError(f"OWS-010 spawner mob drifted at {pos}: {mob}")
        if sum(abs(a - b) for a, b in zip(pos, PROOF_POS)) < 14:
            raise AssertionError(f"OWS-010 spawner too close to proof at {pos}")


def _assert_accepted_d3_contracts(t: base.Template) -> None:
    if tuple(t.size) != SIZE:
        raise AssertionError(f"OWS-010 dimensions changed: {t.size}")
    if any(not (0 <= x < 49 and 0 <= y < 16 and 0 <= z < 43) for x, y, z in t.blocks):
        raise AssertionError("OWS-010 exceeds accepted bounds")
    _assert_proof_and_gameplay(t)
    for shelf in LOR_SHELVES:
        if _name(t, shelf) != "supplementaries:item_shelf":
            raise AssertionError(f"OWS-010 empty LOR shelf drifted at {shelf}")
    serialized_nbt = "\n".join(repr(nbt) for _, nbt in t.blocks.values() if nbt)
    if LOR_ITEM in serialized_nbt:
        raise AssertionError("OWS-010 production builder duplicates LOR-006")
    for center in (19, 25, 31):
        for z in range(12, 29):
            if _name(t, (center, 3, z)) != "create:depot":
                raise AssertionError(f"OWS-010 maintained lane drift at {(center, 3, z)}")
    for z in (12, 13, 14, 15, 18, 19, 20, 21, 22, 23, 26, 27, 28):
        if _name(t, (37, 3, z)) != "create:depot":
            raise AssertionError(f"OWS-010 retained Lane-04 anatomy drift at {(37, 3, z)}")
    for center in (20, 27):
        for z in range(31, 37):
            if _name(t, (center, 3, z)) != "create:depot":
                raise AssertionError(f"OWS-010 inbound tongue drift at {(center, 3, z)}")
    for x in range(18, 43):
        if _name(t, (x, 3, 11)) != "create:depot":
            raise AssertionError(f"OWS-010 destination trunk drift at {(x, 3, 11)}")
    for z in range(12, 32):
        if _name(t, (41, 5, z)) != "create:depot":
            raise AssertionError(f"OWS-010 east return drift at {(41, 5, z)}")
    for center in (34, 41):
        for z in range(32, 37):
            if _name(t, (center, 3, z)) != "create:depot":
                raise AssertionError(f"OWS-010 outbound buffer drift at {(center, 3, z)}")
    gate_clear = (
        ((15, 2, 18), (16, 4, 23), "operator gallery"),
        ((17, 8, 20), (42, 9, 21), "cross aisle"),
        ((42, 2, 12), (44, 3, 14), "north maintenance route"),
        ((42, 2, 29), (44, 3, 31), "south maintenance route"),
    )
    for low, high, label in gate_clear:
        for x in range(low[0], high[0] + 1):
            for y in range(low[1], high[1] + 1):
                for z in range(low[2], high[2] + 1):
                    if _name(t, (x, y, z)) not in AIR:
                        raise AssertionError(f"OWS-010 {label} obstructed at {(x, y, z)}")
    if _count(t, "minecraft:smooth_stone_stairs") < 28:
        raise AssertionError("OWS-010 lost a playable stair system")
    if _count(t, "tfmg:steel_block") < 2700 or _count(t, "create:fluid_pipe") < 150:
        raise AssertionError("OWS-010 lost accepted structure or connected service anatomy")
    for block in PRODUCTION_REQUIRED_BLOCKS:
        if _count(t, block) < 1:
            raise AssertionError(f"OWS-010 lacks required production block {block}")


def _apply_pass19_microdetail(t: base.Template) -> None:
    for pos, block in PASS19_MICRODETAIL.items():
        if _name(t, pos) not in AIR:
            raise AssertionError(f"OWS-010 Pass-19 detail would overwrite accepted D3 at {pos}: {_name(t, pos)}")
        t.set(*pos, block)


def _assert_final_contracts(t: base.Template) -> None:
    _assert_accepted_d3_contracts(t)
    for pos, expected in PASS19_MICRODETAIL.items():
        if _name(t, pos) != expected:
            raise AssertionError(f"OWS-010 Pass-19 detail drift at {pos}")
    for pos, block in PASS19_MICRODETAIL.items():
        if block.endswith("_mushroom") and _name(t, (pos[0], pos[1] - 1, pos[2])) in AIR:
            raise AssertionError(f"OWS-010 Pass-19 mushroom is unsupported at {pos}")


def build_010() -> base.Template:
    """Return accepted OWS-010 D3 plus eight localized vanilla details."""
    t = build_accepted_d3()
    _apply_pass19_microdetail(t)
    _assert_final_contracts(t)
    return t


if __name__ == "__main__":
    raise SystemExit("Import build_010 from the authoritative generator; this module performs no writes.")

