#!/usr/bin/env python3
"""[SYSTEM REPORT] Build and render OWS-002 Gate-B intact/operational D0 review.

This review-only model consumes the Gate-A-approved r2 massing and implements the
intact emergency grow-hall program. It contains no historical anomaly, collapse,
quest-proof loot, rubble, or centuries-later damage. Executable assertions enforce
the circulation, signage, cultivation, utility and roof-access contracts before a
render can be persisted for manual Gate-B review.
"""
from __future__ import annotations

import json
import os

import generate_wasteland_sites as base
from render_old_world_heavy_rebuild_review import OUTPUT_ROOT, ROOT, render_review_set
from render_ows002_gate_a_massing import build_gate_a_massing
from render_structure_review import unpack_structure


STATE_PATH = ROOT / "old_world_narrative" / "registry" / "heavy_rebuild_state.json"
TEMP_NAME = "_heavy_review_ows002_gate_b_intact_r1"
TEMP_NBT = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{TEMP_NAME}.nbt"
OUTPUT_DIR = OUTPUT_ROOT / "OWS-002" / "gate_b_intact" / "r1"
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
    """Two-tier emergency cultivation rack with open aisle-facing service access."""
    for y in (2, 7):
        t.fill((x1, y, z1), (x2, y, z2), "farmersdelight:rich_soil")
        t.fill((x1, y + 1, z1), (x2, y + 1, z2), "minecraft:wheat", age="7")
    for x in (x1, x2):
        for z in (z1, 24, z2):
            t.fill((x, 2, z), (x, 6, z), "minecraft:scaffolding")
    # End service platform/upright remains inside the rack footprint, not the aisle.
    t.fill((x1, 5, z2), (x2, 6, z2), "minecraft:scaffolding")


def build_gate_b_intact() -> base.Template:
    t = build_gate_a_massing()

    # Rationalize overlapping Gate-A shells into usable volumes while preserving
    # every exterior roof/wall mass accepted by Gate A.
    t.clear((19, 2, 5), (31, 7, 8))       # public lobby
    t.clear((19, 2, 8), (45, 11, 14))     # north public/admin bar
    t.clear((5, 2, 8), (20, 10, 40))      # west civic/support wing
    t.clear((23, 2, 16), (45, 17, 40))    # high grow hall

    # Restore/guarantee the public entrance after volume rationalization.
    t.fill((20, 2, 4), (30, 5, 4), "create:framed_glass")
    t.clear((24, 2, 4), (25, 4, 4))
    _door(t, 24, 2, 4, "south", material="dark_oak", hinge="left")
    _door(t, 25, 2, 4, "south", material="dark_oak", hinge="right")

    # Public floors and primary three-block queue spine.
    t.fill((19, 1, 5), (31, 1, 13), "minecraft:polished_andesite")
    t.fill((24, 1, 5), (26, 1, 12), "minecraft:white_concrete")
    t.clear((24, 2, 5), (26, 4, 12))

    # Registration/authorization and culture/relief issue workstations sit to the
    # sides of the public spine rather than across it.
    t.fill((19, 2, 11), (22, 2, 12), "zvhouses:stone_brick_countertop")
    t.set(20, 3, 11, "minecraft:lectern")
    t.fill((32, 2, 11), (38, 2, 12), "zvhouses:stone_brick_countertop")
    t.set(36, 3, 11, "create:depot")

    # Public/staff divider with glazed counter openings and one controlled staff door.
    t.fill((18, 2, 13), (46, 6, 13), "minecraft:white_concrete")
    t.fill((19, 3, 13), (22, 5, 13), "create:framed_glass")
    t.fill((32, 3, 13), (38, 5, 13), "create:framed_glass")
    t.clear((28, 2, 13), (28, 4, 13))
    _door(t, 28, 2, 13, "north")

    # Staff-side allocation records and small clean issue stock.
    t.fill((19, 1, 14), (24, 1, 14), "minecraft:light_gray_concrete")
    t.fill((19, 2, 14), (22, 2, 14), "zvhouses:stone_brick_countertop")
    t.set(20, 3, 14, "minecraft:bookshelf")
    t.set(22, 3, 14, "the_wasteland_reworked:radio")
    t.fill((38, 1, 14), (44, 1, 14), "minecraft:light_gray_concrete")
    t.set(39, 2, 14, "oritech:cooler_block")
    t.set(41, 2, 14, "immersiveengineering:crate")
    t.set(43, 2, 14, "minecraft:barrel")

    # Controlled operations door through the hall's north wall.
    t.clear((34, 2, 15), (34, 4, 15))
    _door(t, 34, 2, 15, "south")

    # Civic support rooms west of the hall. X=18..20 remains a continuous staff
    # corridor to wet-service, harvest portals and roof/operations access.
    t.fill((17, 2, 16), (17, 7, 32), "tfmg:cinder_block")
    t.clear((17, 2, 20), (17, 4, 20))
    _door(t, 17, 2, 20, "east")
    t.clear((17, 2, 28), (17, 4, 28))
    _door(t, 17, 2, 28, "east")
    t.fill((5, 2, 25), (16, 7, 25), "tfmg:cinder_block")
    t.clear((15, 2, 25), (15, 4, 25))
    _door(t, 15, 2, 25, "south")

    # Emergency coordination / staff support.
    t.fill((6, 2, 18), (11, 2, 18), "zvhouses:stone_brick_countertop")
    t.set(7, 3, 18, "the_wasteland_reworked:radio")
    t.set(10, 3, 18, "minecraft:lectern")
    t.fill((6, 2, 22), (9, 3, 23), "minecraft:bookshelf")

    # Tool/packaging support room.
    t.fill((6, 2, 28), (10, 3, 30), "immersiveengineering:crate")
    t.fill((12, 2, 28), (15, 2, 30), "minecraft:barrel")

    # Structural portal frames preserve the clear-span hall. Posts live on the
    # hall edges; high beams never intersect the guaranteed lower-floor aisles.
    for z in (18, 23, 31, 38):
        for x in (23, 45):
            t.fill((x, 2, z), (x, 14, z), "tfmg:steel_block")
        t.fill((23, 14, z), (45, 14, z), "tfmg:steel_block")

    # High support ring below the existing roof lantern; no vertical post is placed
    # in the primary grow aisles.
    t.fill((27, 17, 21), (40, 17, 21), "tfmg:steel_block")
    t.fill((27, 17, 34), (40, 17, 34), "tfmg:steel_block")
    t.fill((27, 17, 21), (27, 17, 34), "tfmg:steel_block")
    t.fill((40, 17, 21), (40, 17, 34), "tfmg:steel_block")

    # Grow hall floor and repeated two-tier banks. Required three-block aisles are
    # intentionally empty at Y=2..4 and are asserted below.
    t.fill((23, 1, 16), (45, 1, 40), "minecraft:smooth_stone")
    _rack_bank(t, 24, 26)
    _rack_bank(t, 30, 32)
    _rack_bank(t, 36, 38)

    # Nutrient/irrigation service. Main riser lives east of the protected service
    # strip; three overhead branches visibly feed the cultivation banks.
    t.fill((42, 3, 18), (42, 11, 18), "create:fluid_pipe")
    t.set(43, 2, 18, "create:mechanical_pump", facing="west")
    t.set(44, 2, 18, "minecraft:water_cauldron", level="3")
    t.set(45, 2, 18, "minecraft:barrel")
    t.fill((42, 11, 18), (42, 11, 30), "create:fluid_pipe")
    for z in (20, 25, 30):
        t.fill((24, 11, z), (42, 11, z), "create:fluid_pipe")

    # Repeated hall task/grow lighting stays above all player clearances.
    for x in (28, 34, 40):
        for z in (20, 26, 30):
            _light(t, x, 12, z)

    # East receiving / batch check. Exterior threshold becomes a working double
    # iron-door service opening while the three-block internal service strip stays clear.
    t.clear((46, 2, 24), (46, 4, 25))
    _door(t, 46, 2, 24, "west", hinge="left")
    _door(t, 46, 2, 25, "west", hinge="right")
    t.fill((42, 2, 27), (45, 2, 27), "zvhouses:stone_brick_countertop")
    t.set(43, 3, 27, "create:depot")
    t.fill((43, 2, 26), (45, 3, 26), "jaffabricate:pallet_full")

    # Clean culture stock is upstream of cultivation and distinct from nutrient stock.
    t.set(43, 2, 21, "oritech:cooler_block")
    t.set(45, 2, 21, "oritech:cooler_block")
    t.fill((43, 2, 20), (45, 3, 20), "immersiveengineering:crate")

    # Normal D0 quality-hold capacity: marked, local and bypassable.
    t.fill((42, 1, 29), (45, 1, 30), "minecraft:yellow_concrete")
    t.set(43, 2, 29, "immersiveengineering:crate")
    t.set(45, 2, 29, "minecraft:barrel")

    # Deliberate raw and checked-harvest portals through the double mass boundary.
    for z1, z2 in ((34, 36), (39, 40)):
        t.clear((21, 2, z1), (22, 4, z2))
        t.fill((21, 5, z1), (22, 5, z2), "tfmg:steel_block")

    # Harvest wash/check conversion in the former kitchen/wet-service zone.
    t.fill((5, 1, 34), (20, 1, 40), "minecraft:white_concrete")
    t.fill((6, 2, 35), (15, 2, 35), "zvhouses:stone_brick_countertop")
    for x in (7, 10, 13):
        t.set(x, 2, 38, "minecraft:water_cauldron", level="3")
    t.fill((6, 3, 40), (15, 3, 40), "create:fluid_pipe")
    t.set(16, 2, 38, "create:depot")
    t.set(16, 2, 40, "create:depot")
    for x in (7, 12, 17):
        _light(t, x, 8, 37)

    # South packing/relief staging. The central X=29..32 dispatch lane remains
    # empty all the way to the south doors.
    t.fill((23, 1, 34), (45, 1, 40), "tfmg:factory_floor")
    t.fill((23, 2, 37), (27, 2, 38), "zvhouses:stone_brick_countertop")
    t.fill((34, 2, 35), (38, 2, 38), "zvhouses:stone_brick_countertop")
    t.fill((40, 2, 35), (43, 3, 36), "immersiveengineering:crate")
    t.fill((40, 2, 39), (43, 2, 39), "jaffabricate:pallet_full")
    t.fill((29, 1, 34), (32, 1, 40), "minecraft:yellow_concrete")
    t.clear((29, 2, 34), (32, 4, 40))

    # Working south dispatch doors at the accepted Gate-A threshold.
    t.clear((30, 2, 41), (31, 4, 41))
    _door(t, 30, 2, 41, "north", hinge="left")
    _door(t, 31, 2, 41, "north", hinge="right")

    # Reassert donor roof access after all interior work.
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

    # Raw/checked harvest transfer and packing/dispatch continuity.
    _assert_clear(t, (18, 2, 34), (22, 4, 36), "raw-harvest west transfer")
    _assert_clear(t, (18, 2, 39), (28, 4, 40), "checked-harvest return to packing")
    _assert_clear(t, (29, 2, 34), (32, 4, 40), "four-block relief dispatch lane")

    # Roof maintenance route must survive the conversion.
    if _block_name(t, 44, 18, 38) != "minecraft:ladder":
        raise AssertionError("roof ladder does not reach the hall roof plane")
    if _block_name(t, 44, 19, 38) != "minecraft:iron_trapdoor":
        raise AssertionError("roof ladder lacks its retained trapdoor/landing")

    # Operational-density checks catch accidental future simplification.
    wheat = sum(1 for pos in t.blocks if _block_name(t, *pos) == "minecraft:wheat")
    pipes = sum(1 for pos in t.blocks if _block_name(t, *pos) == "create:fluid_pipe")
    signs = sum(1 for pos in t.blocks if _block_name(t, *pos) == "minecraft:oak_wall_sign")
    if wheat < 180:
        raise AssertionError(f"intact grow hall has too little two-tier crop evidence: wheat={wheat}")
    if pipes < 70:
        raise AssertionError(f"intact grow hall has too little connected irrigation service: pipes={pipes}")
    if signs < 12:
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
            revision=f"intact-r1@{revision}",
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

    state["active_status"] = "gate_b_r1_intact_rendered_pending_review"
    for key in (
        "structural_system",
        "circulation_and_access",
        "exterior_architecture",
        "interior_architecture",
        "operational_systems",
        "institutional_identity",
    ):
        state["active_target_passes"][key] = "implemented_gate_b_r1_pending_review"
    state["active_target_passes"]["visual_gate_b_intact_state"] = "r1_rendered_pending_manual_review"
    gate["status"] = "r1_rendered_pending_manual_review"
    gate["r1_artifact_manifest"] = str((OUTPUT_DIR / "review_manifest.json").relative_to(ROOT)).replace("\\", "/")
    gate["review_stage_source"] = "scripts/render_ows002_gate_b_intact.py"
    gate["review_only"] = True
    state["visual_review_gates"]["gate_b_intact_state"] = gate
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")

    print(
        f"Rendered OWS-002 Gate B r1 intact review at {manifest['dimensions']} using "
        f"{manifest['fixed_camera_set']}; manual intact-state approval remains pending."
    )


if __name__ == "__main__":
    main()
