#!/usr/bin/env python3
"""[SYSTEM REPORT] OWS-004 Gate-B intact review revision r3.

r2 proved the intact agricultural program but failed Gate B because the only
human vertical route was the west emergency/secondary egress ladder. r3 preserves
all accepted r2 production architecture and installs a distinct protected primary
staff/player switchback stair in the north half of the east service/core mass.
The freight casing remains in the south half, the west ladder remains continuous,
and displaced environmental risers are rerouted around the stair and reconnected
to each cultivation-floor header.
"""
from __future__ import annotations

import json
import os

import generate_wasteland_sites as base
import render_ows004_gate_b_intact as r1
import render_ows004_gate_b_intact_r2 as r2
from render_old_world_heavy_rebuild_review import OUTPUT_ROOT, ROOT, render_review_set
from render_structure_review import unpack_structure

STATE_PATH = ROOT / "dev/old_world_narrative" / "registry" / "heavy_rebuild_state.json"
TEMP_NAME = "_heavy_review_ows004_gate_b_intact_r3"
TEMP_NBT = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{TEMP_NAME}.nbt"
OUTPUT_DIR = OUTPUT_ROOT / "OWS-004" / "gate_b_intact" / "r3"
AIR = {"minecraft:air", "minecraft:cave_air", "minecraft:void_air", "minecraft:structure_void"}


def _name(t: base.Template, x: int, y: int, z: int) -> str:
    row = t.blocks.get((x, y, z))
    if row is None:
        return "minecraft:air"
    return t.palette[row[0]]["Name"]


def _staff_door(t: base.Template, floor_y: int, *, ground: bool = False, crown: bool = False) -> None:
    """Open a staff-only threshold from the production/podium side into the stair."""
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
    """Build one protected switchback stair between two finished floor levels."""
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

    # North-to-south first flight, small transverse landing, then return north.
    base.stair_flight(t, 40, first_y, 18, first_rise, "south", "minecraft:stone_brick_stairs")
    t.fill((40, mid_y, 22), (42, mid_y, 23), "minecraft:polished_andesite")
    base.stair_flight(t, 42, mid_y, 22, second_rise, "north", "minecraft:stone_brick_stairs")

    expected: list[tuple[int, int, int]] = []
    for step in range(first_rise):
        expected.append((40, first_y + step, 18 + step))
    for step in range(second_rise):
        expected.append((42, mid_y + step, 22 - step))
    return expected


def _install_primary_staff_stair(t: base.Template) -> list[tuple[int, int, int]]:
    """Carve and build the primary people route without consuming freight/egress."""
    # The north half of the east core is reserved for people; freight remains
    # south at z25-29. Clear only the staff-stair zone and leave the freight
    # doors/casing untouched.
    t.clear((40, 2, 18), (43, 39, 23))

    # Ground and production/crown landings are rebuilt before stair flights so
    # stair treads can cut their own headroom/openings through each plate.
    t.fill((40, 1, 18), (43, 1, 23), "tfmg:factory_floor")
    for y in (9, 16, 23, 30, 39):
        t.fill((40, y, 18), (43, y, 23), "minecraft:smooth_stone")

    expected: list[tuple[int, int, int]] = []
    expected.extend(_dogleg(t, 1, 9))
    expected.extend(_dogleg(t, 9, 16))
    expected.extend(_dogleg(t, 16, 23))
    expected.extend(_dogleg(t, 23, 30))
    expected.extend(_dogleg(t, 30, 39))

    # Controlled staff thresholds are intentionally separate from the freight
    # threshold at z24 and the west emergency ladder.
    _staff_door(t, 1, ground=True)
    for y in (9, 16, 23, 30):
        _staff_door(t, y)
    _staff_door(t, 39, crown=True)

    # Restore/reroute the environmental riser to the far east side of the core,
    # then connect it around the stair at z23 to the already-accepted floor
    # headers. This avoids "fixing" circulation by deleting the service anatomy.
    t.fill((44, 9, 18), (44, 44, 18), "create:fluid_pipe")
    t.fill((44, 9, 20), (44, 44, 20), "tfmg:steel_block")
    for level in r1.LEVELS:
        branch_y = level + 4
        service_x = 37 if level < 23 else 35
        header_z = 14 if level < 23 else 16
        t.fill((44, branch_y, 18), (44, branch_y, 23), "create:fluid_pipe")
        t.fill((service_x, branch_y, 23), (44, branch_y, 23), "create:fluid_pipe")
        t.fill((service_x, branch_y, header_z), (service_x, branch_y, 23), "create:fluid_pipe")
        t.set(44, branch_y, 21, "create:mechanical_pump", facing="south")

    # Relocate the small amount of clean-intake stock displaced by the ground
    # stair footprint rather than silently reducing the receiving program.
    t.fill((36, 2, 20), (38, 3, 21), "immersiveengineering:crate")

    # Permanent D0 wayfinding distinguishes ordinary staff circulation from the
    # freight/service shaft and from emergency egress.
    base.wall_sign(t, 40, 6, 17, "north", "STAFF STAIRS", "PRODUCTION / CROWN")
    base.wall_sign(t, 43, 12, 17, "north", "STAFF CORE", "LEVEL 01-02")
    base.wall_sign(t, 43, 26, 17, "north", "STAFF CORE", "LEVEL 03-04")
    base.wall_sign(t, 43, 38, 17, "north", "ROOF / PLANT", "STAFF ACCESS")

    return expected


def _assert_staff_stair(t: base.Template, expected: list[tuple[int, int, int]]) -> None:
    if len(expected) < 40:
        raise AssertionError(f"OWS-004 r3 staff stair unexpectedly short: {len(expected)} treads")
    for x, y, z in expected:
        if _name(t, x, y, z) != "minecraft:stone_brick_stairs":
            raise AssertionError(f"OWS-004 r3 missing principal staff stair tread at {(x, y, z)}")
        for head_y in (y + 1, y + 2):
            name = _name(t, x, head_y, z)
            if name not in AIR:
                raise AssertionError(f"OWS-004 r3 staff stair headroom blocked at {(x, head_y, z)} by {name}")

    # Staff thresholds at every occupied production level and crown.
    for wall_x, door_y in ((39, 2), (39, 10), (39, 17), (38, 24), (38, 31), (39, 40)):
        if _name(t, wall_x, door_y, 22) != "minecraft:iron_door":
            raise AssertionError(f"OWS-004 r3 missing staff-core door at {(wall_x, door_y, 22)}")

    # West ladder remains the independent secondary egress.
    for y in range(9, 39):
        if _name(t, 8, y, 30) != "minecraft:ladder":
            raise AssertionError(f"OWS-004 r3 secondary egress ladder gap at y={y}")

    # Freight/service identity remains south of the staff stair.
    for level in r1.LEVELS:
        if _name(t, 44, level + 2, 27) != "create:andesite_casing":
            raise AssertionError(f"OWS-004 r3 freight casing lost at level {level}")

    # Rerouted utility line must actually connect the vertical riser to each
    # production header via the protected edge route.
    for level in r1.LEVELS:
        branch_y = level + 4
        service_x = 37 if level < 23 else 35
        header_z = 14 if level < 23 else 16
        for point in ((44, branch_y, 18), (44, branch_y, 23), (service_x, branch_y, 23), (service_x, branch_y, header_z)):
            if _name(t, *point) not in {"create:fluid_pipe", "create:mechanical_pump"}:
                raise AssertionError(f"OWS-004 r3 disconnected environmental route at {point}: {_name(t, *point)}")


def build_gate_b_intact_r3() -> base.Template:
    t = r2.build_gate_b_intact_r2()
    expected = _install_primary_staff_stair(t)
    # Preserve every accepted r2 invariant as well as the new principal-stair contract.
    r1._assert_intact_contracts(t)
    _assert_staff_stair(t, expected)
    return t


def main() -> None:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if state.get("active_target") != "OWS-004":
        print(f"Gate-B OWS-004 r3 renderer skipped: active target is {state.get('active_target')}")
        return

    gate = state.get("visual_review_gates", {}).get("gate_b_intact_state", {})
    status = gate.get("status", "not_started")
    if status not in {
        "r2_rendered_pending_manual_review",
        "rerender_required",
        "ready_to_render",
        "ready_for_intact_implementation",
    }:
        print(f"Gate-B OWS-004 r3 renderer skipped: status={status}")
        return

    t = build_gate_b_intact_r3()
    if tuple(t.size) != (51, 47, 47):
        raise AssertionError(f"OWS-004 Gate-B r3 dimensions changed unexpectedly: {t.size}")

    t.save(TEMP_NAME)
    try:
        size, blocks = unpack_structure(TEMP_NBT)
        revision = os.environ.get("GITHUB_SHA", "local")[:8]
        manifest = render_review_set(
            target="OWS-004",
            gate="gate_b_intact",
            revision=f"intact-r3@{revision}",
            damage_state="D0 intact / operational",
            source_commit=os.environ.get("GITHUB_SHA", "working-tree"),
            source_path="review-only:render_ows004_gate_b_intact_r3.build_gate_b_intact_r3()",
            size=size,
            blocks=blocks,
            output_dir=OUTPUT_DIR,
            camera_set=gate.get("fixed_camera_set", "ows004_fixed_v1"),
        )
    finally:
        TEMP_NBT.unlink(missing_ok=True)

    state["active_status"] = "gate_b_r3_intact_rendered_pending_review"
    for key in (
        "structural_system",
        "circulation_and_access",
        "exterior_architecture",
        "interior_architecture",
        "operational_systems",
        "institutional_identity",
    ):
        state["active_target_passes"][key] = "implemented_gate_b_r3_pending_review"
    state["active_target_passes"]["visual_gate_b_intact_state"] = "r3_rendered_pending_manual_review"
    gate["status"] = "r3_rendered_pending_manual_review"
    gate["r2_review_record"] = "old_world_narrative/reviews/heavy_rebuild/OWS-004_GATE_B_R2_REVIEW.md"
    gate["r2_decision"] = "REVISION_REQUIRED_MISSING_PRIMARY_STAFF_STAIR"
    gate["r3_artifact_manifest"] = str((OUTPUT_DIR / "review_manifest.json").relative_to(ROOT)).replace("\\", "/")
    gate["review_stage_source"] = "scripts/render_ows004_gate_b_intact_r3.py"
    gate["review_only"] = True
    state["visual_review_gates"]["gate_b_intact_state"] = gate
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")

    print(
        f"Rendered OWS-004 Gate B r3 intact review at {manifest['dimensions']} using "
        f"{manifest['fixed_camera_set']}; manual intact-state approval remains pending."
    )


if __name__ == "__main__":
    main()
