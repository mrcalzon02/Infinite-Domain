#!/usr/bin/env python3
"""[SYSTEM REPORT] Build and render OWS-002 Gate-B intact/operational D0 review.

Revision r2 preserves the mechanically successful r1 program and corrects the
recorded intact-state visual failure. The high grow-hall facade now exposes the
interior structural bay rhythm, clerestory glazing and VCF conversion layer;
receiving and dispatch become complete service portals; and the lower-roof plant
is physically connected to the hall irrigation trunk. This remains review-only:
no historical anomaly, collapse, quest-proof loot, rubble or long-term decay is
introduced before Gate B passes.
"""
from __future__ import annotations

import json
import os

import generate_wasteland_sites as base
from render_old_world_heavy_rebuild_review import OUTPUT_ROOT, ROOT, render_review_set
from render_ows002_gate_a_massing import build_gate_a_massing
from render_structure_review import unpack_structure


STATE_PATH = ROOT / "old_world_narrative" / "registry" / "heavy_rebuild_state.json"
TEMP_NAME = "_heavy_review_ows002_gate_b_intact_r2"
TEMP_NBT = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{TEMP_NAME}.nbt"
OUTPUT_DIR = OUTPUT_ROOT / "OWS-002" / "gate_b_intact" / "r2"
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
    if facing not in offsets:
        raise ValueError(f"Unsupported sign facing: {facing}")
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
    """Two-tier emergency cultivation rack with aisle-facing service access."""
    for y in (2, 7):
        t.fill((x1, y, z1), (x2, y, z2), "farmersdelight:rich_soil")
        t.fill((x1, y + 1, z1), (x2, y + 1, z2), "minecraft:wheat", age="7")
    for x in (x1, x2):
        for z in (z1, 24, z2):
            t.fill((x, 2, z), (x, 6, z), "minecraft:scaffolding")
    t.fill((x1, 5, z2), (x2, 6, z2), "minecraft:scaffolding")


def _articulate_intact_exterior_r2(t: base.Template) -> None:
    """Make the operating conversion legible without facade garnish for its own sake."""
    # North public/admin bar: retained civic glazing plus a clean VCF retrofit band.
    for x in (33, 40, 46):
        t.fill((x, 2, 7), (x, 10, 7), "minecraft:light_gray_concrete")
    t.fill((33, 9, 7), (45, 10, 7), "minecraft:lime_concrete")
    # Reassert the two donor-derived window groups below the retrofit band.
    for x1, x2 in ((34, 38), (41, 45)):
        t.fill((x1, 4, 7), (x2, 7, 7), "create:framed_glass")

    # East grow-hall wall: exterior pilasters align with interior portal frames.
    # Clerestories reveal the high-volume cultivation use without turning the
    # emergency conversion into a purpose-built greenhouse shell.
    for z in (18, 23, 31, 38):
        t.fill((46, 2, z), (46, 14, z), "minecraft:light_gray_concrete")
    for z1, z2 in ((19, 21), (24, 28), (32, 36)):
        t.fill((46, 8, z1), (46, 10, z2), "create:framed_glass")
    t.fill((46, 12, 18), (46, 13, 38), "minecraft:lime_concrete")
    # Reassert pilasters through the identity band so structure, not a stripe,
    # remains the organizing facade grammar.
    for z in (18, 23, 31, 38):
        t.fill((46, 2, z), (46, 14, z), "minecraft:light_gray_concrete")

    # Complete east receiving portal around the working two-leaf service door.
    for z in (23, 26):
        t.fill((46, 2, z), (46, 7, z), "minecraft:white_concrete")
    t.fill((46, 7, 23), (46, 7, 26), "tfmg:steel_block")
    t.fill((46, 5, 27), (46, 6, 28), "create:framed_glass")
    t.fill((47, 0, 24), (50, 0, 25), "minecraft:yellow_concrete")
    t.set(49, 1, 27, "jaffabricate:pallet_full")

    # South dispatch face: the wall frame, canopy frame and painted lane now form
    # one architectural handoff rather than a canopy floating in front of doors.
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

    # High west hall wall rises above the lower civic support roof. Three
    # clerestory groups expose the internal bay rhythm from the service side.
    for z1, z2 in ((18, 21), (24, 28), (32, 35)):
        t.fill((22, 12, z1), (22, 14, z2), "create:framed_glass")
    t.fill((22, 15, 18), (22, 15, 38), "minecraft:lime_concrete")

    # Physically connect the visible lower-roof plant to the hall irrigation
    # system instead of leaving two unrelated sets of pipes/equipment.
    t.fill((18, 13, 36), (22, 13, 36), "create:fluid_pipe")
    t.fill((23, 11, 36), (23, 13, 36), "create:fluid_pipe")
    t.set(22, 13, 36, "create:fluid_pipe")


def build_gate_b_intact() -> base.Template:
    """Integrate the D0 operating program into Gate-A-approved r2 massing."""
    t = build_gate_a_massing()

    # Rationalize overlapping Gate-A shells into usable volumes while preserving
    # the accepted exterior massing and roof hierarchy.
    t.clear((19, 2, 5), (31, 7, 8))
    t.clear((19, 2, 8), (45, 11, 14))
    t.clear((5, 2, 8), (20, 10, 40))
    t.clear((23, 2, 16), (45, 17, 40))

    # Public entrance, queue and workstations.
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

    # Public/staff boundary and controlled operations sequence.
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
    # Observation glass lets the emergency allocation zone visually connect to
    # the cultivation hero space without making it publicly traversable.
    t.fill((30, 3, 15), (33, 5, 15), "create:framed_glass")
    t.fill((36, 3, 15), (40, 5, 15), "create:framed_glass")

    # West civic/support wing and staff corridor.
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

    # Clear-span hall structure.
    for z in (18, 23, 31, 38):
        for x in (23, 45):
            t.fill((x, 2, z), (x, 14, z), "tfmg:steel_block")
        t.fill((23, 14, z), (45, 14, z), "tfmg:steel_block")
    t.fill((27, 17, 21), (40, 17, 21), "tfmg:steel_block")
    t.fill((27, 17, 34), (40, 17, 34), "tfmg:steel_block")
    t.fill((27, 17, 21), (27, 17, 34), "tfmg:steel_block")
    t.fill((40, 17, 21), (40, 17, 34), "tfmg:steel_block")

    # Cultivation floor and three repeated two-tier banks.
    t.fill((23, 1, 16), (45, 1, 40), "minecraft:smooth_stone")
    _rack_bank(t, 24, 26)
    _rack_bank(t, 30, 32)
    _rack_bank(t, 36, 38)

    # Irrigation/nutrient system. r2 extends the east riser to the roof-plant
    # cross-connection at z=36, creating one physically continuous service path.
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

    # East receiving / batch check and clean stock.
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

    # Raw and checked harvest portals through the hall/support boundary.
    for z1, z2 in ((34, 36), (39, 40)):
        t.clear((21, 2, z1), (22, 4, z2))
        t.fill((21, 5, z1), (22, 5, z2), "tfmg:steel_block")

    # Former kitchen becomes harvest wash/check.
    t.fill((5, 1, 34), (20, 1, 40), "minecraft:white_concrete")
    t.fill((6, 2, 35), (15, 2, 35), "zvhouses:stone_brick_countertop")
    for x in (7, 10, 13):
        t.set(x, 2, 38, "minecraft:water_cauldron", level="3")
    t.fill((6, 3, 40), (15, 3, 40), "create:fluid_pipe")
    t.set(16, 2, 38, "create:depot")
    t.set(16, 2, 40, "create:depot")
    for x in (7, 12, 17):
        _light(t, x, 8, 37)

    # South packing/relief staging and clear dispatch lane.
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

    # Retained donor roof access.
    t.fill((44, 2, 38), (44, 18, 38), "minecraft:ladder", facing="west", waterlogged="false")
    t.set(
        44,
        19,
        38,
        "minecraft:iron_trapdoor",
        facing="north",
        half="bottom",
        open="false",
        powered="false",
        waterlogged="false",
    )

    # Apply r2 intact-state exterior/service corrections after all route geometry.
    _articulate_intact_exterior_r2(t)
    # Complete the interior side of the roof-plant connection after facade work.
    t.fill((23, 11, 36), (42, 11, 36), "create:fluid_pipe")

    # Purpose-driven, support-verified institutional signage.
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


def _assert_intact_contracts(t: base.Template) -> None:
    # Exterior thresholds.
    _assert_door(t, 24, 2, 4, "north public entrance west leaf", block_name="minecraft:dark_oak_door")
    _assert_door(t, 25, 2, 4, "north public entrance east leaf", block_name="minecraft:dark_oak_door")
    _assert_door(t, 46, 2, 24, "east receiving west leaf")
    _assert_door(t, 46, 2, 25, "east receiving east leaf")
    _assert_door(t, 30, 2, 41, "south dispatch west leaf")
    _assert_door(t, 31, 2, 41, "south dispatch east leaf")

    # Public and controlled staff routes.
    _assert_clear(t, (24, 2, 5), (26, 4, 12), "three-block public queue/lobby route")
    _assert_door(t, 28, 2, 13, "public-to-staff control door")
    _assert_door(t, 34, 2, 15, "staff-to-grow-operations door")

    # Production circulation.
    _assert_clear(t, (24, 2, 16), (41, 4, 17), "north grow-hall cross-aisle")
    _assert_clear(t, (27, 2, 18), (29, 4, 33), "grow aisle A")
    _assert_clear(t, (33, 2, 18), (35, 4, 33), "grow aisle B")
    _assert_clear(t, (39, 2, 18), (41, 4, 31), "east grow-service strip")
    _assert_clear(t, (24, 2, 31), (41, 4, 33), "south harvest cross-aisle")

    # Harvest and dispatch continuity.
    _assert_clear(t, (18, 2, 34), (22, 4, 36), "raw-harvest west transfer")
    _assert_clear(t, (18, 2, 39), (28, 4, 40), "checked-harvest return to packing")
    _assert_clear(t, (29, 2, 34), (32, 4, 40), "four-block relief dispatch lane")

    # Roof maintenance route.
    _assert_block(t, 44, 18, 38, "minecraft:ladder", "roof ladder top")
    _assert_block(t, 44, 19, 38, "minecraft:iron_trapdoor", "roof ladder landing")

    # r2 visual-architecture contracts: facade rhythm and service integration must
    # survive future edits rather than regressing to sign-only identity.
    _assert_block(t, 46, 9, 20, "create:framed_glass", "east hall clerestory")
    _assert_block(t, 46, 12, 25, "minecraft:lime_concrete", "east VCF service band")
    _assert_block(t, 22, 13, 25, "create:framed_glass", "west hall clerestory")
    _assert_block(t, 37, 9, 41, "create:framed_glass", "south hall clerestory")
    _assert_block(t, 46, 7, 24, "tfmg:steel_block", "receiving portal header")
    _assert_block(t, 30, 6, 41, "tfmg:steel_block", "dispatch portal header")
    _assert_block(t, 30, 0, 44, "minecraft:yellow_concrete", "external relief lane")
    _assert_block(t, 20, 13, 36, "create:fluid_pipe", "roof plant bridge")
    _assert_block(t, 30, 11, 36, "create:fluid_pipe", "roof-to-hall service trunk")
    _assert_block(t, 42, 11, 36, "create:fluid_pipe", "service trunk tie-in")

    # Operational-density checks catch accidental simplification.
    wheat = sum(1 for pos in t.blocks if _block_name(t, *pos) == "minecraft:wheat")
    pipes = sum(1 for pos in t.blocks if _block_name(t, *pos) == "create:fluid_pipe")
    signs = sum(1 for pos in t.blocks if _block_name(t, *pos) == "minecraft:oak_wall_sign")
    if wheat < 180:
        raise AssertionError(f"intact grow hall has too little two-tier crop evidence: wheat={wheat}")
    if pipes < 90:
        raise AssertionError(f"intact grow hall has too little connected irrigation/service infrastructure: pipes={pipes}")
    if signs < 14:
        raise AssertionError(f"intact grow hall has insufficient purposeful signage: signs={signs}")


def main() -> None:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if state.get("active_target") != "OWS-002":
        print(f"Gate-B OWS-002 renderer skipped: active target is {state.get('active_target')}")
        return

    gate = state.get("visual_review_gates", {}).get("gate_b_intact_state", {})
    status = gate.get("status", "not_started")
    if status not in {"ready_for_intact_implementation", "ready_to_render", "rerender_required"}:
        print(f"Gate-B OWS-002 renderer skipped: status={status}")
        return

    t = build_gate_b_intact()
    _assert_intact_contracts(t)
    base.stabilize_door_pairs(t)
    _assert_intact_contracts(t)

    t.save(TEMP_NAME)
    try:
        size, blocks = unpack_structure(TEMP_NBT)
        revision = os.environ.get("GITHUB_SHA", "local")[:8]
        manifest = render_review_set(
            target="OWS-002",
            gate="gate_b_intact",
            revision=f"intact-r2@{revision}",
            damage_state="D0 intact / operational",
            source_commit=os.environ.get("GITHUB_SHA", "working-tree"),
            source_path="review-only:render_ows002_gate_b_intact.build_gate_b_intact()",
            size=size,
            blocks=blocks,
            output_dir=OUTPUT_DIR,
            camera_set=gate.get("fixed_camera_set", "ows002_fixed_v1"),
        )
    finally:
        TEMP_NBT.unlink(missing_ok=True)

    state["active_status"] = "gate_b_r2_intact_rendered_pending_review"
    for key in (
        "structural_system",
        "circulation_and_access",
        "exterior_architecture",
        "interior_architecture",
        "operational_systems",
        "institutional_identity",
    ):
        state["active_target_passes"][key] = "implemented_gate_b_r2_pending_review"
    state["active_target_passes"]["visual_gate_b_intact_state"] = "r2_rendered_pending_manual_review"
    gate["status"] = "r2_rendered_pending_manual_review"
    gate["r2_artifact_manifest"] = str((OUTPUT_DIR / "review_manifest.json").relative_to(ROOT)).replace("\\", "/")
    gate["review_stage_source"] = "scripts/render_ows002_gate_b_intact.py"
    gate["review_only"] = True
    state["visual_review_gates"]["gate_b_intact_state"] = gate
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")

    print(
        f"Rendered OWS-002 Gate B r2 intact review at {manifest['dimensions']} using "
        f"{manifest['fixed_camera_set']}; manual intact-state approval remains pending."
    )


if __name__ == "__main__":
    main()
