#!/usr/bin/env python3
"""[SYSTEM REPORT] Build and render OWS-001 Gate-B intact/operational D0 review.

This is a review-only historical interpretation. It is deliberately NOT the
shipping D3 worldgen NBT. Revision r2 corrects the blocking findings from the
recorded Gate-B r1 review: locker-service clearance, receiving/staff circulation,
real roof maintenance access, and physically supported purpose-driven signage.
Damage and long-term decay remain forbidden until Gate B passes.
"""
from __future__ import annotations

import json
import os

import generate_wasteland_sites as base
from render_old_world_heavy_rebuild_review import OUTPUT_ROOT, ROOT, render_review_set
from render_ows001_gate_a_massing import build_gate_a_massing
from render_structure_review import unpack_structure


STATE_PATH = ROOT / "old_world_narrative" / "registry" / "heavy_rebuild_state.json"
TEMP_NAME = "_heavy_review_ows001_gate_b_intact_r2"
TEMP_NBT = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{TEMP_NAME}.nbt"
OUTPUT_DIR = OUTPUT_ROOT / "OWS-001" / "gate_b_intact" / "r2"
AIR = {"minecraft:air", "minecraft:cave_air", "minecraft:void_air", "minecraft:structure_void"}


def _door(t: base.Template, x: int, y: int, z: int, facing: str, *, hinge: str = "left") -> None:
    base.door(t, x, y, z, facing=facing, material="iron", hinge=hinge)


def _light(t: base.Template, x: int, y: int, z: int) -> None:
    t.set(x, y, z, "minecraft:sea_lantern")


def _block_name(t: base.Template, x: int, y: int, z: int) -> str:
    row = t.blocks.get((x, y, z))
    if row is None:
        return "minecraft:air"
    state, _ = row
    return t.palette[state]["Name"]


def _assert_clear(
    t: base.Template,
    a: tuple[int, int, int],
    b: tuple[int, int, int],
    label: str,
) -> None:
    """Fail the review build if a promised circulation volume is obstructed."""
    for x in range(min(a[0], b[0]), max(a[0], b[0]) + 1):
        for y in range(min(a[1], b[1]), max(a[1], b[1]) + 1):
            for z in range(min(a[2], b[2]), max(a[2], b[2]) + 1):
                name = _block_name(t, x, y, z)
                if name not in AIR:
                    raise AssertionError(f"{label} obstructed at {(x, y, z)} by {name}")


def _sign_on_wall(
    t: base.Template,
    wall_x: int,
    wall_y: int,
    wall_z: int,
    facing: str,
    *lines: str,
) -> None:
    """Mount a wall sign one block off a verified supporting wall face.

    `facing` is the direction the sign front faces. The supporting wall therefore
    sits one block behind it. This prevents the r1 error where signs replaced the
    very wall block that was supposed to support them.
    """
    offsets = {
        "north": (0, 0, -1),
        "south": (0, 0, 1),
        "west": (-1, 0, 0),
        "east": (1, 0, 0),
    }
    if facing not in offsets:
        raise ValueError(f"Unsupported wall-sign facing: {facing}")
    support = _block_name(t, wall_x, wall_y, wall_z)
    if support in AIR:
        raise AssertionError(
            f"Cannot mount {' / '.join(lines)}: support {(wall_x, wall_y, wall_z)} is {support}"
        )
    dx, dy, dz = offsets[facing]
    sx, sy, sz = wall_x + dx, wall_y + dy, wall_z + dz
    occupied = _block_name(t, sx, sy, sz)
    if occupied not in AIR:
        raise AssertionError(
            f"Cannot mount {' / '.join(lines)} at {(sx, sy, sz)}: occupied by {occupied}"
        )
    base.wall_sign(t, sx, sy, sz, facing, *lines)


def build_gate_b_intact() -> base.Template:
    """Integrate the D0 building program into the Gate-A-approved r2 massing."""
    t = build_gate_a_massing()

    # ---------------------------------------------------------------------
    # Pass 7: rationalize the overlapping review shells into usable volumes.
    # ---------------------------------------------------------------------
    t.clear((13, 2, 4), (25, 6, 11))
    t.clear((9, 2, 9), (25, 7, 19))
    t.clear((11, 2, 19), (28, 6, 26))
    t.clear((4, 2, 13), (11, 6, 23))
    t.clear((27, 2, 11), (34, 8, 24))
    t.clear((13, 2, 24), (28, 6, 30))
    t.clear((25, 2, 26), (32, 5, 28))

    # Front glazing and principal double entrance.
    t.fill((14, 2, 3), (24, 5, 3), "create:framed_glass")
    t.clear((18, 2, 3), (19, 4, 3))
    _door(t, 18, 2, 3, "south", hinge="left")
    _door(t, 19, 2, 3, "south", hinge="right")

    # Sparse rational structural rhythm.
    for x in (14, 20):
        t.fill((x, 2, 14), (x, 7, 14), "tfmg:steel_block")
    for x in (28, 33):
        for z in (12, 23):
            t.fill((x, 2, z), (x, 8, z), "tfmg:steel_block")
    t.fill((9, 7, 14), (25, 7, 14), "tfmg:steel_block")
    t.fill((27, 8, 17), (34, 8, 17), "tfmg:steel_block")

    # ---------------------------------------------------------------------
    # Pass 8/10: circulation + interior partitions.
    # ---------------------------------------------------------------------
    t.fill((13, 1, 4), (25, 1, 11), "minecraft:smooth_stone")
    t.fill((17, 1, 4), (20, 1, 8), "minecraft:white_concrete")

    # Public return and issue counters.
    t.fill((13, 2, 9), (16, 2, 10), "zvhouses:stone_brick_countertop")
    t.fill((20, 2, 9), (24, 2, 10), "zvhouses:stone_brick_countertop")
    t.fill((13, 3, 10), (16, 3, 10), "minecraft:light_gray_concrete")
    t.fill((20, 3, 10), (24, 3, 10), "minecraft:lime_concrete")

    # Controlled public/back-of-house divider.
    t.fill((12, 2, 11), (26, 6, 11), "minecraft:white_concrete")
    t.fill((14, 3, 11), (16, 5, 11), "create:framed_glass")
    t.fill((21, 3, 11), (24, 5, 11), "create:framed_glass")
    t.clear((17, 2, 11), (17, 4, 11))
    t.clear((25, 2, 11), (25, 4, 11))
    _door(t, 17, 2, 11, "north")
    _door(t, 25, 2, 11, "north")

    # Three-block central staff spine, preserved all the way to receiving in r2.
    t.fill((17, 1, 12), (19, 1, 30), "minecraft:light_gray_concrete")
    t.clear((17, 2, 12), (19, 6, 30))

    # West return-processing boundary and sanitation / quality-hold split.
    t.fill((12, 2, 12), (12, 6, 24), "minecraft:white_concrete")
    t.clear((12, 2, 14), (12, 4, 15))
    _door(t, 12, 2, 14, "west")
    t.clear((12, 2, 22), (12, 4, 22))
    _door(t, 12, 2, 22, "west")
    t.fill((4, 1, 13), (11, 1, 23), "minecraft:white_concrete")
    t.fill((4, 2, 20), (11, 6, 20), "tfmg:cinder_block")
    t.clear((9, 2, 20), (9, 4, 20))
    _door(t, 9, 2, 20, "south")

    # Clean-side boundary into east cold block.
    t.fill((26, 2, 11), (26, 8, 25), "minecraft:white_concrete")
    t.clear((26, 2, 15), (26, 4, 16))
    _door(t, 26, 2, 15, "east")
    t.clear((26, 2, 22), (26, 4, 22))
    _door(t, 26, 2, 22, "east")

    # Rear receiving boundaries.
    t.fill((10, 2, 21), (16, 6, 21), "tfmg:cinder_block")
    t.clear((14, 2, 21), (14, 4, 21))
    _door(t, 14, 2, 21, "north")
    t.fill((23, 2, 21), (23, 6, 27), "minecraft:white_concrete")
    t.clear((23, 2, 24), (23, 4, 24))
    _door(t, 23, 2, 24, "east")

    # Rear freight opening/frame.
    t.clear((17, 2, 31), (20, 5, 31))
    for x in (16, 21):
        t.fill((x, 1, 30), (x, 6, 31), "tfmg:steel_block")
    t.fill((16, 6, 30), (21, 6, 31), "tfmg:steel_block")

    # Supervisor/records enclosure.
    t.fill((24, 2, 25), (24, 5, 29), "minecraft:stone_bricks")
    t.clear((24, 2, 27), (24, 4, 27))
    _door(t, 24, 2, 27, "east")

    # ---------------------------------------------------------------------
    # Pass 10/11: room-scale operational systems.
    # ---------------------------------------------------------------------

    # Primary culture-locker hero space. r2 deliberately leaves x=21..23 clear
    # as a full three-block maintenance/issue aisle from z=13..19.
    t.fill((20, 1, 12), (25, 1, 19), "minecraft:light_gray_concrete")
    for z in (13, 15, 17, 19):
        t.fill((20, 2, z), (20, 3, z), "oritech:cooler_block")
        t.fill((24, 2, z), (25, 3, z), "oritech:cooler_block")
    t.fill((20, 2, 12), (25, 2, 12), "minecraft:lime_concrete")
    t.set(20, 2, 18, "create:depot")
    t.set(24, 2, 18, "create:depot")

    # East clean cold holding.
    t.fill((27, 1, 11), (34, 1, 24), "minecraft:light_gray_concrete")
    for x in (28, 31, 34):
        for z in (13, 17, 21):
            t.set(x, 2, z, "oritech:cooler_block")
            t.set(x, 3, z, "oritech:cooler_block")
    t.fill((28, 2, 23), (33, 3, 24), "immersiveengineering:crate")

    # Return sanitation and normal D0 quality hold.
    t.fill((5, 2, 16), (10, 2, 16), "create:fluid_pipe")
    t.set(6, 2, 18, "minecraft:water_cauldron", level="3")
    t.set(9, 2, 18, "minecraft:water_cauldron", level="3")
    t.fill((5, 2, 14), (10, 2, 14), "zvhouses:stone_brick_countertop")
    t.fill((5, 2, 19), (7, 3, 19), "immersiveengineering:crate")
    t.fill((5, 2, 21), (7, 3, 23), "immersiveengineering:crate")
    t.fill((9, 2, 22), (10, 3, 23), "minecraft:barrel")

    # Returned-crate consolidation.
    t.fill((11, 1, 22), (16, 1, 27), "tfmg:factory_floor")
    t.fill((11, 2, 23), (14, 3, 25), "immersiveengineering:crate")
    t.fill((12, 2, 26), (15, 2, 26), "jaffabricate:pallet_full")

    # Receiving and batch/temperature check. r2 moves freight into west/east
    # staging pockets and keeps x=17..19 unobstructed through the full approach.
    t.fill((13, 1, 24), (22, 1, 30), "tfmg:factory_floor")
    t.fill((13, 2, 27), (15, 3, 29), "jaffabricate:pallet_full")
    t.fill((21, 2, 27), (22, 3, 29), "immersiveengineering:crate")
    t.fill((20, 2, 24), (22, 2, 25), "zvhouses:stone_brick_countertop")
    t.set(21, 3, 25, "create:depot")

    # Supervisor/batch-record station.
    t.fill((25, 1, 26), (32, 1, 28), "minecraft:smooth_stone")
    t.fill((26, 2, 27), (30, 2, 27), "zvhouses:stone_brick_countertop")
    t.set(30, 3, 27, "the_wasteland_reworked:radio")
    t.fill((31, 2, 26), (32, 4, 28), "minecraft:bookshelf")
    t.set(27, 2, 28, "minecraft:barrel")

    # ---------------------------------------------------------------------
    # Ceiling, lighting, maintenance and rooftop cold-chain support.
    # ---------------------------------------------------------------------
    for x in (15, 19, 23):
        for z in (5, 8):
            _light(t, x, 6, z)
    for x in (11, 17, 23):
        for z in (13, 18):
            _light(t, x, 7, z)
    for x in (6, 10):
        for z in (15, 22):
            _light(t, x, 6, z)
    for x in (15, 20, 26):
        _light(t, x, 6, 27)

    # r2 roof access: ladder penetrates the y=9 roof plane and opens directly to
    # a durable service landing rather than terminating beneath a solid ceiling.
    t.fill((31, 9, 21), (33, 9, 24), "minecraft:smooth_stone")
    t.fill((34, 2, 23), (34, 9, 23), "minecraft:ladder", facing="west", waterlogged="false")

    # Recognizable refrigeration plant with open service gaps and a real feed.
    for x, z in ((17, 14), (20, 14), (24, 15), (28, 15)):
        t.set(x, 10, z, "oritech:cooler_block")
    t.fill((18, 10, 18), (29, 10, 18), "create:fluid_pipe")
    t.fill((34, 3, 18), (34, 10, 18), "create:fluid_pipe")
    t.fill((29, 10, 18), (34, 10, 18), "create:fluid_pipe")

    # ---------------------------------------------------------------------
    # Pass 9/12: physically supported exterior/identity signage.
    # ---------------------------------------------------------------------

    # Public facade identity: support wall is z=3; signs project to z=2.
    _sign_on_wall(t, 15, 6, 3, "north", "VERDANT", "CONTINUUM", "FOODS")
    _sign_on_wall(t, 22, 6, 3, "north", "NEIGHBORHOOD", "CULTURE SERVICE", "DEPOT")

    # Customer wayfinding on the north/public face of the z=11 divider.
    _sign_on_wall(t, 13, 4, 11, "north", "RETURN", "CULTURES")
    _sign_on_wall(t, 20, 4, 11, "north", "CULTURE", "ISSUE")

    # Staff-side and operational signs use real nearby partitions as supports.
    _sign_on_wall(t, 20, 5, 11, "south", "COLD LOCKERS", "AUTHORIZED STAFF")
    _sign_on_wall(t, 12, 4, 17, "west", "SANITATION", "RETURNS ONLY")
    _sign_on_wall(t, 7, 4, 20, "north", "QUALITY HOLD", "STAFF ONLY")
    _sign_on_wall(t, 15, 4, 21, "south", "RETURN CRATES", "SERVICE DISPATCH")
    _sign_on_wall(t, 18, 6, 31, "north", "RECEIVING", "BATCH CHECK")
    _sign_on_wall(t, 26, 5, 22, "east", "CLEAN STOCK", "COLD HOLD")
    _sign_on_wall(t, 28, 4, 25, "north", "SUPERVISOR", "BATCH RECORDS")
    _sign_on_wall(t, 35, 5, 18, "west", "COLD PLANT", "STAFF ONLY")

    # Rear exterior service identity projects south from the z=31 wall.
    _sign_on_wall(t, 22, 5, 31, "south", "VCF SERVICE", "RECEIVING")

    # ---------------------------------------------------------------------
    # Gate-B r2 invariants. These are intentionally executable quality contracts.
    # ---------------------------------------------------------------------
    _assert_clear(t, (21, 2, 13), (23, 3, 19), "culture-locker three-block service aisle")
    _assert_clear(t, (17, 2, 12), (19, 3, 30), "central three-block staff spine")
    if _block_name(t, 34, 9, 23) != "minecraft:ladder":
        raise AssertionError("roof maintenance ladder does not penetrate the roof plane")

    return t


def main() -> None:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if state.get("active_target") != "OWS-001":
        print(f"Gate-B OWS-001 renderer skipped: active target is {state.get('active_target')}")
        return

    gate = state.get("visual_review_gates", {}).get("gate_b_intact_state", {})
    status = gate.get("status", "not_started")
    if status not in {"ready_to_render", "rerender_required"}:
        print(f"Gate-B OWS-001 renderer skipped: status={status}")
        return

    t = build_gate_b_intact()
    t.save(TEMP_NAME)
    try:
        size, blocks = unpack_structure(TEMP_NBT)
        revision = os.environ.get("GITHUB_SHA", "local")[:8]
        manifest = render_review_set(
            target="OWS-001",
            gate="gate_b_intact_state",
            revision=f"intact-r2@{revision}",
            damage_state="D0 intact/normal operation",
            source_commit=os.environ.get("GITHUB_SHA", "working-tree"),
            source_path="review-only:build_gate_b_intact()",
            size=size,
            blocks=blocks,
            output_dir=OUTPUT_DIR,
            camera_set=gate.get("fixed_camera_set", "ows001_fixed_v1"),
        )
    finally:
        TEMP_NBT.unlink(missing_ok=True)

    state["active_status"] = "gate_b_intact_r2_rendered_pending_review"
    for key in (
        "structural_system",
        "circulation_and_access",
        "exterior_architecture",
        "interior_architecture",
        "operational_systems",
        "institutional_identity",
    ):
        state["active_target_passes"][key] = "r2_implemented_pending_gate_b_review"
    state["active_target_passes"]["visual_gate_b_intact_state"] = "r2_rendered_pending_manual_review"
    gate["status"] = "r2_rendered_pending_manual_review"
    gate["r2_artifact_manifest"] = str((OUTPUT_DIR / "review_manifest.json").relative_to(ROOT)).replace("\\", "/")
    gate["review_stage_source"] = "scripts/render_ows001_gate_b_intact.py"
    gate["review_only"] = True
    state["visual_review_gates"]["gate_b_intact_state"] = gate
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")

    print(
        f"Rendered OWS-001 Gate B intact r2 at {manifest['dimensions']} using "
        f"{manifest['fixed_camera_set']}; visual approval remains pending."
    )


if __name__ == "__main__":
    main()
