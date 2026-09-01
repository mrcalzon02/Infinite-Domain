#!/usr/bin/env python3
"""[SYSTEM REPORT] Build and render OWS-003 Gate-B intact/operational D0 review.

This is a review-only D0 model derived from the Gate-A-approved r1 massing. It
implements the retained cannery frame, inserted cold-vault/nursery rooms, separate
receiving and dispatch streams, normal quality hold, batch/licensing control,
connected refrigeration plant and usable maintenance access. No historical
anomaly, quest-proof chest, encounters, ruin damage or centuries-later decay is
introduced before Gate B passes.
"""
from __future__ import annotations

import json
import os

import generate_wasteland_sites as base
from render_old_world_heavy_rebuild_review import OUTPUT_ROOT, ROOT, render_review_set
from render_ows003_gate_a_massing import build_gate_a_massing
from render_structure_review import unpack_structure

STATE_PATH = ROOT / "dev/old_world_narrative" / "registry" / "heavy_rebuild_state.json"
TEMP_NAME = "_heavy_review_ows003_gate_b_intact_r1"
TEMP_NBT = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{TEMP_NAME}.nbt"
OUTPUT_DIR = OUTPUT_ROOT / "OWS-003" / "gate_b_intact" / "r1"
AIR = {"minecraft:air", "minecraft:cave_air", "minecraft:void_air", "minecraft:structure_void"}


def _block_name(t: base.Template, x: int, y: int, z: int) -> str:
    row = t.blocks.get((x, y, z))
    if row is None:
        return "minecraft:air"
    state, _ = row
    return t.palette[state]["Name"]


def _door(t: base.Template, x: int, y: int, z: int, facing: str, *, material: str = "iron", hinge: str = "left") -> None:
    base.door(t, x, y, z, facing=facing, material=material, hinge=hinge)


def _assert_clear(t: base.Template, a: tuple[int, int, int], b: tuple[int, int, int], label: str) -> None:
    for x in range(min(a[0], b[0]), max(a[0], b[0]) + 1):
        for y in range(min(a[1], b[1]), max(a[1], b[1]) + 1):
            for z in range(min(a[2], b[2]), max(a[2], b[2]) + 1):
                name = _block_name(t, x, y, z)
                if name not in AIR:
                    raise AssertionError(f"{label} obstructed at {(x, y, z)} by {name}")


def _assert_door(t: base.Template, x: int, y: int, z: int, label: str, *, block_name: str = "minecraft:iron_door") -> None:
    for yy in (y, y + 1):
        actual = _block_name(t, x, yy, z)
        if actual != block_name:
            raise AssertionError(f"{label} missing {block_name} at {(x, yy, z)}; found {actual}")


def _assert_block(t: base.Template, x: int, y: int, z: int, name: str, label: str) -> None:
    actual = _block_name(t, x, y, z)
    if actual != name:
        raise AssertionError(f"{label} expected {name} at {(x, y, z)}; found {actual}")


def _count(t: base.Template, name: str) -> int:
    return sum(1 for pos in t.blocks if _block_name(t, *pos) == name)


def _sign_on_wall(t: base.Template, wall_x: int, wall_y: int, wall_z: int, facing: str, *lines: str) -> None:
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


def _light(t: base.Template, x: int, y: int, z: int) -> None:
    t.set(x, y, z, "minecraft:sea_lantern")


def _build_admin_and_records(t: base.Template) -> None:
    # Rationalize the lower annex and guarantee a clean staff entry through the
    # Gate-A facade projection into a batch/licensing control environment.
    t.clear((25, 2, 6), (54, 8, 16))
    t.fill((25, 1, 6), (54, 1, 16), "minecraft:polished_andesite")

    # Restore front facade after the interior clear.
    t.fill((31, 2, 4), (48, 7, 4), "minecraft:white_concrete")
    t.fill((35, 3, 3), (44, 6, 3), "create:framed_glass")
    t.clear((39, 2, 3), (40, 5, 5))
    _door(t, 39, 2, 4, "south", material="dark_oak", hinge="left")
    _door(t, 40, 2, 4, "south", material="dark_oak", hinge="right")

    # Central staff corridor with west support and east batch/licensing rooms.
    t.fill((35, 2, 6), (35, 7, 16), "minecraft:bricks")
    t.clear((35, 2, 10), (35, 4, 10))
    _door(t, 35, 2, 10, "east")
    t.fill((43, 2, 6), (43, 7, 16), "minecraft:white_concrete")
    t.clear((43, 2, 10), (43, 4, 10))
    _door(t, 43, 2, 10, "west")

    # West staff/support room.
    t.fill((26, 2, 8), (32, 2, 9), "zvhouses:stone_brick_countertop")
    t.set(27, 3, 8, "the_wasteland_reworked:radio")
    t.fill((26, 2, 13), (31, 3, 14), "minecraft:barrel")

    # Batch registration and licensing/release-control records.
    t.fill((44, 2, 8), (52, 2, 9), "zvhouses:stone_brick_countertop")
    t.set(45, 3, 8, "minecraft:lectern")
    t.set(47, 3, 8, "create:depot")
    t.set(51, 3, 8, "the_wasteland_reworked:radio")
    t.fill((46, 2, 13), (53, 4, 15), "minecraft:bookshelf")
    t.set(49, 2, 12, "minecraft:lectern")

    # Controlled operations crossings through the retained annex/hall boundary.
    t.clear((37, 2, 17), (38, 4, 17))
    _door(t, 37, 2, 17, "north", hinge="left")
    _door(t, 38, 2, 17, "north", hinge="right")
    t.clear((50, 2, 17), (50, 4, 17))
    _door(t, 50, 2, 17, "north")


def _build_hall_structure(t: base.Template) -> None:
    # Clear the high hall interior while preserving Gate-A exterior shell/roof.
    t.clear((25, 2, 18), (54, 16, 42))
    t.fill((25, 1, 18), (54, 1, 42), "tfmg:factory_floor")

    # Repeated old-cannery frame inside the shell.
    for z in (20, 26, 32, 38):
        for x in (25, 31, 37, 43, 49, 54):
            t.fill((x, 2, z), (x, 15, z), "tfmg:steel_block")
        t.fill((25, 15, z), (54, 15, z), "tfmg:steel_block")

    # Rebuild roof lights and their transverse support after the interior clear.
    for x1, x2 in ((28, 30), (37, 39), (46, 48)):
        t.fill((x1, 17, 20), (x2, 17, 39), "create:framed_glass")
        for z in (20, 26, 32, 38):
            t.fill((x1 - 1, 16, z), (x2 + 1, 16, z), "tfmg:steel_block")


def _build_cold_vault(t: base.Template) -> None:
    # Inserted cold vault in the west half of the old hall.
    t.fill((25, 1, 19), (35, 1, 35), "minecraft:light_gray_concrete")
    t.fill((35, 2, 19), (35, 8, 35), "minecraft:white_concrete")
    t.fill((25, 2, 19), (35, 8, 19), "minecraft:white_concrete")
    t.fill((25, 2, 35), (35, 8, 35), "minecraft:white_concrete")
    for z in (22, 31):
        t.clear((35, 2, z), (35, 4, z))
        _door(t, 35, 2, z, "east")
    # Monitoring glazing at aisle ends.
    t.fill((35, 3, 24), (35, 5, 28), "create:framed_glass")

    # Two dense refrigerated banks with a protected three-block center aisle.
    t.fill((26, 2, 20), (28, 2, 34), "oritech:cooler_block")
    t.fill((32, 2, 20), (34, 2, 34), "oritech:cooler_block")
    for z in (21, 25, 29, 33):
        t.fill((26, 3, z), (28, 3, z), "immersiveengineering:crate")
        t.fill((32, 3, z), (34, 3, z), "minecraft:barrel")
    # Batch end markers.
    t.fill((26, 4, 20), (28, 4, 20), "minecraft:lime_concrete")
    t.fill((32, 4, 20), (34, 4, 20), "minecraft:light_blue_concrete")


def _build_nursery_cells(t: base.Template) -> None:
    # Three standardized but individually accessible dormancy cells east of the
    # protected main operations spine.
    t.fill((39, 2, 21), (39, 8, 36), "minecraft:white_concrete")
    for z in (21, 26, 31, 36):
        t.fill((39, 2, z), (47, 8, z), "minecraft:white_concrete")
    for z in (23, 28, 33):
        t.clear((39, 2, z), (39, 4, z))
        _door(t, 39, 2, z, "east")
        # observation glass beside each controlled threshold
        t.fill((39, 3, z - 1), (39, 5, z - 1), "create:framed_glass")
        t.fill((39, 3, z + 1), (39, 5, z + 1), "create:framed_glass")

    # Cell-specific storage/culture positions. Wide west side remains clear for
    # inspection and service rather than squeezing aisles to one block.
    for z1, z2 in ((22, 25), (27, 30), (32, 35)):
        t.fill((45, 2, z1), (47, 2, z2), "oritech:cooler_block")
        t.fill((41, 2, z1 + 1), (42, 3, z1 + 2), "immersiveengineering:crate")


def _build_receiving_quality_and_outbound(t: base.Template) -> None:
    # East receiving vestibule behind the actual exterior loading portal.
    t.fill((48, 1, 18), (54, 1, 28), "minecraft:white_concrete")
    t.fill((48, 2, 18), (48, 7, 28), "minecraft:white_concrete")
    t.fill((48, 2, 18), (54, 7, 18), "minecraft:white_concrete")
    t.fill((48, 2, 28), (54, 7, 28), "minecraft:white_concrete")

    # Restore receiving face and make the actual conditioned freight threshold.
    t.fill((55, 2, 21), (55, 8, 30), "minecraft:white_concrete")
    t.clear((55, 2, 23), (55, 5, 27))
    for z, hinge in ((24, "left"), (25, "right")):
        _door(t, 55, 2, z, "west", hinge=hinge)
    t.fill((55, 6, 23), (55, 7, 27), "tfmg:steel_block")

    # Intake/check and receiving hold equipment; through-lane remains open.
    t.fill((49, 2, 19), (53, 2, 20), "zvhouses:stone_brick_countertop")
    t.set(50, 3, 19, "create:depot")
    t.set(52, 3, 19, "minecraft:lectern")
    t.fill((49, 2, 21), (50, 2, 22), "oritech:cooler_block")
    t.fill((53, 2, 21), (54, 2, 22), "oritech:cooler_block")
    t.set(54, 3, 27, "jaffabricate:pallet_full")

    # Controlled transfer from receiving into operations spine/nursery side.
    t.clear((48, 2, 22), (48, 4, 23))
    _door(t, 48, 2, 22, "west", hinge="left")
    _door(t, 48, 2, 23, "west", hinge="right")

    # Normal D0 quality hold / seal-repack zone, just north of maintenance tower.
    t.fill((48, 1, 29), (54, 1, 31), "minecraft:yellow_concrete")
    t.fill((48, 2, 29), (48, 7, 31), "minecraft:white_concrete")
    t.clear((48, 2, 30), (48, 4, 30))
    _door(t, 48, 2, 30, "west")
    t.fill((50, 2, 29), (54, 2, 29), "zvhouses:stone_brick_countertop")
    t.set(51, 3, 29, "oritech:cooler_block")
    t.set(53, 3, 29, "immersiveengineering:crate")
    t.set(54, 3, 30, "minecraft:barrel")

    # Release inspection and conditioned packing across the rear of the hall.
    t.fill((25, 1, 36), (35, 1, 42), "minecraft:white_concrete")
    t.fill((26, 2, 37), (33, 2, 38), "zvhouses:stone_brick_countertop")
    t.set(28, 3, 37, "create:depot")
    t.set(31, 3, 37, "minecraft:lectern")

    t.fill((39, 1, 37), (47, 1, 42), "minecraft:light_gray_concrete")
    t.fill((40, 2, 38), (43, 2, 39), "zvhouses:stone_brick_countertop")
    t.fill((45, 2, 38), (47, 3, 39), "immersiveengineering:crate")
    t.set(41, 3, 41, "jaffabricate:pallet_full")

    # Outbound cold staging east of packing and south of the maintenance tower.
    t.fill((48, 1, 38), (54, 1, 42), "minecraft:light_blue_concrete")
    t.fill((49, 2, 39), (50, 2, 41), "oritech:cooler_block")
    t.fill((53, 2, 39), (54, 2, 41), "oritech:cooler_block")

    # Restore south dispatch face with a centered working two-leaf door pair and
    # preserve the Gate-A external yellow dispatch lane.
    t.fill((24, 2, 43), (55, 16, 43), "minecraft:bricks")
    for x in (25, 31, 37, 43, 49, 54):
        t.fill((x, 2, 43), (x, 15, 43), "minecraft:light_gray_concrete")
    t.clear((44, 2, 43), (49, 5, 43))
    _door(t, 46, 2, 43, "north", hinge="left")
    _door(t, 47, 2, 43, "north", hinge="right")
    t.fill((44, 6, 43), (49, 7, 43), "tfmg:steel_block")
    t.fill((44, 0, 44), (49, 0, 50), "minecraft:yellow_concrete")


def _build_operations_spine(t: base.Template) -> None:
    # Clear and reassert the protected 3-block operations spine after adjacent
    # rooms are built. Fixed columns at z=20/26/32/38 remain visible overhead but
    # floor-level circulation is unobstructed.
    t.fill((36, 1, 18), (38, 1, 42), "minecraft:light_gray_concrete")
    t.clear((36, 2, 18), (38, 4, 42))


def _build_plant_and_maintenance(t: base.Template) -> None:
    # Turn Gate-A mechanical masses into an integrated refrigeration system.
    for pos in ((34, 22, 27), (40, 23, 27), (35, 22, 34), (42, 23, 34), (48, 22, 30)):
        t.set(*pos, "oritech:cooler_block")

    # Roof plant header and two vertical risers.
    t.fill((32, 18, 23), (49, 18, 23), "create:fluid_pipe")
    t.fill((45, 12, 23), (45, 18, 23), "create:fluid_pipe")
    t.fill((52, 12, 31), (52, 18, 31), "create:fluid_pipe")
    # Interior high service trunk follows the hall frame and branches toward
    # vault/nursery/receiving rather than wandering decoratively.
    t.fill((28, 12, 23), (52, 12, 23), "create:fluid_pipe")
    t.fill((28, 12, 30), (52, 12, 30), "create:fluid_pipe")
    for x in (28, 34, 42, 47, 52):
        t.fill((x, 8, 23), (x, 12, 23), "create:fluid_pipe")
    for z in (23, 30):
        t.fill((34, 8, z), (34, 12, z), "create:fluid_pipe")
        t.fill((47, 8, z), (47, 12, z), "create:fluid_pipe")

    # Service/aisle lighting aligned to operational zones.
    for x, z in ((30, 22), (30, 28), (30, 33), (37, 22), (37, 28), (37, 34), (43, 23), (43, 28), (43, 33), (51, 22), (51, 27), (30, 39), (43, 40), (51, 40)):
        _light(t, x, 14 if z < 36 else 8, z)

    # Real maintenance tower vertical route and roof-plant landing.
    t.clear((51, 2, 32), (54, 19, 37))
    t.fill((54, 2, 36), (54, 18, 36), "minecraft:ladder", facing="west", waterlogged="false")
    t.fill((51, 18, 32), (54, 18, 37), "minecraft:light_gray_concrete")
    t.set(54, 18, 36, "minecraft:ladder", facing="west", waterlogged="false")
    t.clear((50, 2, 36), (50, 4, 36))
    _door(t, 50, 2, 36, "west")
    t.clear((50, 18, 35), (50, 19, 35))
    _door(t, 50, 18, 35, "west")
    t.fill((45, 18, 35), (49, 18, 35), "tfmg:steel_block")


def _articulate_exterior(t: base.Template) -> None:
    # Controlled clerestory/service openings aligned to actual high-hall use.
    for z1, z2 in ((21, 24), (27, 30), (33, 36)):
        t.fill((24, 10, z1), (24, 12, z2), "create:framed_glass")
    for z1, z2 in ((19, 21), (33, 35), (39, 41)):
        t.fill((55, 10, z1), (55, 12, z2), "create:framed_glass")
    for x1, x2 in ((26, 29), (32, 35), (40, 43), (50, 53)):
        t.fill((x1, 10, 43), (x2, 12, 43), "create:framed_glass")

    # Reassert structural pilasters through glazing groups.
    for z in (20, 26, 32, 38, 43):
        t.fill((23, 1, z), (23, 16, z), "minecraft:light_gray_concrete")
        t.fill((56, 1, z), (56, 16, z), "minecraft:light_gray_concrete")


def _add_identity_and_wayfinding(t: base.Template) -> None:
    # Exterior institutional identity.
    _sign_on_wall(t, 32, 6, 4, "north", "VERDANT", "CONTINUUM", "FOODS")
    _sign_on_wall(t, 46, 6, 4, "north", "COLD-CHAIN", "CULTURE", "NURSERY")
    _sign_on_wall(t, 55, 7, 22, "east", "RECEIVING", "COLD CHAIN")
    _sign_on_wall(t, 54, 7, 43, "south", "OUTBOUND", "CULTURES")

    # Permanent D0 internal wayfinding.
    _sign_on_wall(t, 43, 6, 8, "west", "BATCH", "REGISTRATION")
    _sign_on_wall(t, 43, 6, 13, "west", "LICENSE", "ROUTING")
    _sign_on_wall(t, 35, 6, 14, "east", "AUTHORIZED", "OPERATIONS")
    _sign_on_wall(t, 48, 6, 19, "east", "CONDITION", "CHECK")
    _sign_on_wall(t, 48, 6, 27, "east", "RECEIVING", "HOLD / PRE-COOL")
    _sign_on_wall(t, 35, 6, 20, "east", "COLD VAULT", "A")
    _sign_on_wall(t, 39, 6, 22, "west", "DORMANCY", "NURSERY 1")
    _sign_on_wall(t, 39, 6, 27, "west", "DORMANCY", "NURSERY 2")
    _sign_on_wall(t, 39, 6, 32, "west", "DORMANCY", "NURSERY 3")
    _sign_on_wall(t, 48, 6, 29, "west", "QUALITY HOLD", "SEAL INSPECTION")
    _sign_on_wall(t, 35, 6, 38, "east", "RELEASE", "INSPECTION")
    _sign_on_wall(t, 39, 6, 38, "west", "CONDITIONED", "PACKING")
    _sign_on_wall(t, 48, 6, 39, "west", "OUTBOUND", "COLD STAGING")
    _sign_on_wall(t, 50, 6, 36, "west", "PLANT ACCESS", "STAFF ONLY")


def build_gate_b_intact() -> base.Template:
    """Return the complete D0 operating interpretation for Gate-B review."""
    t = build_gate_a_massing()
    _build_admin_and_records(t)
    _build_hall_structure(t)
    _build_cold_vault(t)
    _build_nursery_cells(t)
    _build_receiving_quality_and_outbound(t)
    _build_operations_spine(t)
    _build_plant_and_maintenance(t)
    _articulate_exterior(t)
    _add_identity_and_wayfinding(t)
    return t


def _assert_intact_contracts(t: base.Template) -> None:
    # Staff/admin thresholds.
    _assert_door(t, 39, 2, 4, "front staff entrance west leaf", block_name="minecraft:dark_oak_door")
    _assert_door(t, 40, 2, 4, "front staff entrance east leaf", block_name="minecraft:dark_oak_door")
    _assert_door(t, 37, 2, 17, "admin-to-operations west leaf")
    _assert_door(t, 38, 2, 17, "admin-to-operations east leaf")

    # Exterior logistics thresholds.
    _assert_door(t, 55, 2, 24, "receiving west leaf")
    _assert_door(t, 55, 2, 25, "receiving east leaf")
    _assert_door(t, 46, 2, 43, "dispatch west leaf")
    _assert_door(t, 47, 2, 43, "dispatch east leaf")

    # Protected main circulation.
    _assert_clear(t, (36, 2, 18), (38, 4, 42), "three-block conditioned operations spine")
    _assert_clear(t, (29, 2, 21), (31, 4, 33), "cold-vault center aisle")
    _assert_clear(t, (40, 2, 22), (44, 4, 25), "nursery 1 service area")
    _assert_clear(t, (40, 2, 27), (44, 4, 30), "nursery 2 service area")
    _assert_clear(t, (40, 2, 32), (44, 4, 35), "nursery 3 service area")
    _assert_clear(t, (49, 2, 23), (53, 4, 27), "receiving freight lane")
    _assert_clear(t, (44, 2, 40), (47, 4, 42), "packing-to-dispatch transfer")

    # Maintenance access really spans the tall building.
    _assert_door(t, 50, 2, 36, "maintenance tower ground door")
    _assert_door(t, 50, 18, 35, "maintenance tower roof door")
    _assert_block(t, 54, 18, 36, "minecraft:ladder", "maintenance ladder top")
    _assert_block(t, 45, 18, 35, "tfmg:steel_block", "roof plant access bridge")

    # Mechanical integration and density guards.
    coolers = _count(t, "oritech:cooler_block")
    pipes = _count(t, "create:fluid_pipe")
    signs = _count(t, "minecraft:oak_wall_sign")
    if coolers < 120:
        raise AssertionError(f"OWS-003 D0 has too little refrigerated/nursery evidence: cooler_blocks={coolers}")
    if pipes < 90:
        raise AssertionError(f"OWS-003 D0 refrigeration/service network is too sparse: pipes={pipes}")
    if signs < 18:
        raise AssertionError(f"OWS-003 D0 has insufficient purposeful wayfinding: signs={signs}")


def main() -> None:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if state.get("active_target") != "OWS-003":
        print(f"Gate-B OWS-003 renderer skipped: active target is {state.get('active_target')}")
        return

    gate = state.get("visual_review_gates", {}).get("gate_b_intact_state", {})
    status = gate.get("status", "not_started")
    if status not in {"ready_for_intact_implementation", "ready_to_render", "rerender_required"}:
        print(f"Gate-B OWS-003 renderer skipped: status={status}")
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
            target="OWS-003",
            gate="gate_b_intact",
            revision=f"intact-r1@{revision}",
            damage_state="D0 intact / operational",
            source_commit=os.environ.get("GITHUB_SHA", "working-tree"),
            source_path="review-only:render_ows003_gate_b_intact.build_gate_b_intact()",
            size=size,
            blocks=blocks,
            output_dir=OUTPUT_DIR,
            camera_set=gate.get("fixed_camera_set", "ows003_fixed_v1"),
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
        state["active_target_passes"][key] = "implemented_pending_gate_b_review"
    state["active_target_passes"]["visual_gate_b_intact_state"] = "r1_rendered_pending_manual_review"
    gate["status"] = "r1_rendered_pending_manual_review"
    gate["r1_artifact_manifest"] = str((OUTPUT_DIR / "review_manifest.json").relative_to(ROOT)).replace("\\", "/")
    gate["review_stage_source"] = "scripts/render_ows003_gate_b_intact.py"
    gate["review_only"] = True
    state["visual_review_gates"]["gate_b_intact_state"] = gate
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")

    print(
        f"Rendered OWS-003 Gate B r1 intact review at {manifest['dimensions']} using "
        f"{manifest['fixed_camera_set']}; manual intact-state approval remains pending."
    )


if __name__ == "__main__":
    main()
