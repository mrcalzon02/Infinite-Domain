#!/usr/bin/env python3
"""[SYSTEM REPORT] Build and render OWS-001 Gate-B intact/operational D0 review.

This is a review-only historical interpretation. It is deliberately NOT the
shipping D3 worldgen NBT. It integrates the Gate-A-approved massing with the
Pass-7 through Pass-12 structural, circulation, exterior, interior, operational,
and Verdant Continuum Foods identity decisions. Damage and long-term decay are
for later gates.
"""
from __future__ import annotations

import json
import os

import generate_wasteland_sites as base
from render_old_world_heavy_rebuild_review import OUTPUT_ROOT, ROOT, render_review_set
from render_ows001_gate_a_massing import build_gate_a_massing
from render_structure_review import unpack_structure


STATE_PATH = ROOT / "old_world_narrative" / "registry" / "heavy_rebuild_state.json"
TEMP_NAME = "_heavy_review_ows001_gate_b_intact_r1"
TEMP_NBT = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{TEMP_NAME}.nbt"
OUTPUT_DIR = OUTPUT_ROOT / "OWS-001" / "gate_b_intact" / "r1"


def _door(t: base.Template, x: int, y: int, z: int, facing: str, *, hinge: str = "left") -> None:
    base.door(t, x, y, z, facing=facing, material="iron", hinge=hinge)


def _light(t: base.Template, x: int, y: int, z: int) -> None:
    t.set(x, y, z, "minecraft:sea_lantern")


def build_gate_b_intact() -> base.Template:
    """Integrate the D0 building program into the Gate-A-approved r2 massing."""
    t = build_gate_a_massing()

    # ---------------------------------------------------------------------
    # Pass 7: rationalize the overlapping review shells into usable volumes.
    # Exterior roof/wall planes remain; internal overlap walls are cleared and
    # replaced below with partitions aligned to the real program.
    # ---------------------------------------------------------------------
    t.clear((13, 2, 4), (25, 6, 11))      # public pavilion interior
    t.clear((9, 2, 9), (25, 7, 19))       # front workplace interior
    t.clear((11, 2, 19), (28, 6, 26))     # rear process interior
    t.clear((4, 2, 13), (11, 6, 23))      # west returns annex interior
    t.clear((27, 2, 11), (34, 8, 24))     # east clean cold-chain interior
    t.clear((13, 2, 24), (28, 6, 30))     # rear receiving interior
    t.clear((25, 2, 26), (32, 5, 28))     # supervisor bump-out interior

    # Restore the front public wall/glazing and principal double entrance after
    # interior clearing reaches the pavilion edge.
    t.fill((14, 2, 3), (24, 5, 3), "create:framed_glass")
    t.clear((18, 2, 3), (19, 4, 3))
    _door(t, 18, 2, 3, "south", hinge="left")
    _door(t, 19, 2, 3, "south", hinge="right")

    # Structural rhythm: two internal workplace posts, cold-chain support lines,
    # and the already approved service frames. These are intentionally sparse;
    # the one-storey depot does not need a forest of columns.
    for x in (14, 20):
        t.fill((x, 2, 14), (x, 7, 14), "tfmg:steel_block")
    for x in (28, 33):
        for z in (12, 23):
            t.fill((x, 2, z), (x, 8, z), "tfmg:steel_block")

    # Service/ceiling beams align the broad workplace and cold-chain roof zones.
    t.fill((9, 7, 14), (25, 7, 14), "tfmg:steel_block")
    t.fill((27, 8, 17), (34, 8, 17), "tfmg:steel_block")

    # ---------------------------------------------------------------------
    # Pass 8/10: circulation + interior partitions.
    # ---------------------------------------------------------------------

    # Public pavilion floor and central orientation zone.
    t.fill((13, 1, 4), (25, 1, 11), "minecraft:smooth_stone")
    t.fill((17, 1, 4), (20, 1, 8), "minecraft:white_concrete")

    # Return counter (west) and issue counter (east). Staff space remains behind.
    t.fill((13, 2, 9), (16, 2, 10), "zvhouses:stone_brick_countertop")
    t.fill((20, 2, 9), (24, 2, 10), "zvhouses:stone_brick_countertop")
    t.fill((13, 3, 10), (16, 3, 10), "minecraft:light_gray_concrete")
    t.fill((20, 3, 10), (24, 3, 10), "minecraft:lime_concrete")

    # Controlled public/back-of-house divider, with two staff openings behind
    # return and issue service. It prevents the pavilion becoming an open lobby.
    t.fill((12, 2, 11), (26, 6, 11), "minecraft:white_concrete")
    t.fill((14, 3, 11), (16, 5, 11), "create:framed_glass")
    t.fill((21, 3, 11), (24, 5, 11), "create:framed_glass")
    t.clear((17, 2, 11), (17, 4, 11))
    t.clear((25, 2, 11), (25, 4, 11))
    _door(t, 17, 2, 11, "north")
    _door(t, 25, 2, 11, "north")

    # Central staff spine: keep a 3-block clear north-south route.
    t.fill((17, 1, 12), (19, 1, 27), "minecraft:light_gray_concrete")
    t.clear((17, 2, 12), (19, 6, 27))

    # West return-processing boundary. Openings connect return handoff to
    # sanitation and accepted-return handling without leaking into clean stock.
    t.fill((12, 2, 12), (12, 6, 24), "minecraft:white_concrete")
    t.clear((12, 2, 14), (12, 4, 15))
    _door(t, 12, 2, 14, "west")
    t.clear((12, 2, 22), (12, 4, 22))
    _door(t, 12, 2, 22, "west")

    # Sanitation / quality-hold split in west annex.
    t.fill((4, 1, 13), (11, 1, 23), "minecraft:white_concrete")
    t.fill((4, 2, 20), (11, 6, 20), "tfmg:cinder_block")
    t.clear((9, 2, 20), (9, 4, 20))
    _door(t, 9, 2, 20, "south")

    # Clean-side boundary into east cold block; one issue-service opening and one
    # rear clean-stock opening are enough for D0 staff circulation.
    t.fill((26, 2, 11), (26, 8, 25), "minecraft:white_concrete")
    t.clear((26, 2, 15), (26, 4, 16))
    _door(t, 26, 2, 15, "east")
    t.clear((26, 2, 22), (26, 4, 22))
    _door(t, 26, 2, 22, "east")

    # Rear receiving zone remains open around the freight path but is separated
    # from return crates on west and clean stock on east by real room boundaries.
    t.fill((10, 2, 21), (16, 6, 21), "tfmg:cinder_block")
    t.clear((14, 2, 21), (14, 4, 21))
    _door(t, 14, 2, 21, "north")
    t.fill((23, 2, 21), (23, 6, 27), "minecraft:white_concrete")
    t.clear((23, 2, 24), (23, 4, 24))
    _door(t, 23, 2, 24, "east")

    # Restore/strengthen rear freight opening and frame after interior clearing.
    t.clear((17, 2, 31), (20, 5, 31))
    for x in (16, 21):
        t.fill((x, 1, 30), (x, 6, 31), "tfmg:steel_block")
    t.fill((16, 6, 30), (21, 6, 31), "tfmg:steel_block")

    # Supervisor/records room enclosure and staff doorway.
    t.fill((24, 2, 25), (24, 5, 29), "minecraft:stone_bricks")
    t.clear((24, 2, 27), (24, 4, 27))
    _door(t, 24, 2, 27, "east")

    # ---------------------------------------------------------------------
    # Pass 10/11: room-scale operational systems.
    # ---------------------------------------------------------------------

    # Primary culture-locker / issue hero space. Repeated banks occupy the clean
    # east/front zone with a clear three-block service lane between the rows.
    t.fill((20, 1, 12), (25, 1, 19), "minecraft:light_gray_concrete")
    for z in (13, 15, 17, 19):
        t.fill((21, 2, z), (22, 3, z), "oritech:cooler_block")
        t.fill((24, 2, z), (25, 3, z), "oritech:cooler_block")
    t.fill((20, 2, 12), (25, 2, 12), "minecraft:lime_concrete")
    for x in (20, 22, 24):
        t.set(x, 2, 18, "create:depot")

    # East clean cold holding: denser staff-only storage tied to roof plant.
    t.fill((27, 1, 11), (34, 1, 24), "minecraft:light_gray_concrete")
    for x in (28, 31, 34):
        for z in (13, 17, 21):
            t.set(x, 2, z, "oritech:cooler_block")
            t.set(x, 3, z, "oritech:cooler_block")
    t.fill((28, 2, 23), (33, 3, 24), "immersiveengineering:crate")

    # Return sanitation: wet line, pipe service and inspection counter. The room
    # remains clean and professional in D0; there is no emergency yellow overlay.
    t.fill((5, 2, 16), (10, 2, 16), "create:fluid_pipe")
    t.set(6, 2, 18, "minecraft:water_cauldron", level="3")
    t.set(9, 2, 18, "minecraft:water_cauldron", level="3")
    t.fill((5, 2, 14), (10, 2, 14), "zvhouses:stone_brick_countertop")
    t.fill((5, 2, 19), (7, 3, 19), "immersiveengineering:crate")

    # D0 quality hold: a normal controlled contingency room with sparse capacity.
    t.fill((5, 2, 21), (7, 3, 23), "immersiveengineering:crate")
    t.fill((9, 2, 22), (10, 3, 23), "minecraft:barrel")

    # Returned-crate consolidation on the west/rear service side.
    t.fill((11, 1, 22), (16, 1, 27), "tfmg:factory_floor")
    t.fill((11, 2, 23), (14, 3, 25), "immersiveengineering:crate")
    t.fill((12, 2, 26), (15, 2, 26), "jaffabricate:pallet_full")

    # Receiving and batch/temperature check. Staged inbound product must pass the
    # check station before its route reaches the clean-stock door.
    t.fill((13, 1, 24), (22, 1, 30), "tfmg:factory_floor")
    t.fill((14, 2, 27), (16, 3, 29), "jaffabricate:pallet_full")
    t.fill((18, 2, 27), (20, 3, 29), "immersiveengineering:crate")
    t.fill((20, 2, 24), (22, 2, 25), "zvhouses:stone_brick_countertop")
    t.set(21, 3, 25, "create:depot")

    # Supervisor/batch-record station. The shipping D3 builder will later use the
    # deterministic loot table here; this D0 review uses only operational props.
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

    # Maintenance ladder inside east service zone reaches the roof plant without
    # crossing customer or dirty-return circulation.
    t.fill((34, 2, 23), (34, 8, 23), "minecraft:ladder", facing="west", waterlogged="false")

    # Turn Gate-A equipment masses into recognizable D0 refrigeration plant while
    # preserving open service gaps and the accepted roof silhouette.
    for x, z in ((17, 14), (20, 14), (24, 15), (28, 15)):
        t.set(x, 10, z, "oritech:cooler_block")
    t.fill((18, 10, 18), (29, 10, 18), "create:fluid_pipe")
    t.fill((34, 3, 18), (34, 10, 18), "create:fluid_pipe")
    t.fill((29, 10, 18), (34, 10, 18), "create:fluid_pipe")

    # ---------------------------------------------------------------------
    # Pass 9/12: exterior/identity and purpose-driven D0 signage.
    # ---------------------------------------------------------------------

    # Public facade identity. Multiple signs form one coordinated installation so
    # the exact full company/facility names are present without unreadable text.
    base.wall_sign(t, 15, 6, 3, "north", "VERDANT", "CONTINUUM", "FOODS")
    base.wall_sign(t, 22, 6, 3, "north", "NEIGHBORHOOD", "CULTURE SERVICE", "DEPOT")

    # Customer wayfinding at the actual handoff points.
    base.wall_sign(t, 14, 4, 10, "south", "RETURN", "CULTURES")
    base.wall_sign(t, 22, 4, 10, "south", "CULTURE", "ISSUE")

    # Staff/operational labels follow the workflow instead of filling blank walls.
    base.wall_sign(t, 22, 4, 12, "north", "COLD LOCKERS", "AUTHORIZED STAFF")
    base.wall_sign(t, 7, 4, 13, "north", "SANITATION", "RETURNS ONLY")
    base.wall_sign(t, 7, 4, 20, "north", "QUALITY HOLD", "STAFF ONLY")
    base.wall_sign(t, 15, 4, 22, "north", "RETURN CRATES", "SERVICE DISPATCH")
    base.wall_sign(t, 18, 4, 30, "south", "RECEIVING", "BATCH CHECK")
    base.wall_sign(t, 27, 4, 22, "north", "CLEAN STOCK", "COLD HOLD")
    base.wall_sign(t, 28, 4, 25, "north", "SUPERVISOR", "BATCH RECORDS")
    base.wall_sign(t, 34, 5, 18, "west", "COLD PLANT", "STAFF ONLY")

    # Small rear service identity differentiates the freight side without turning
    # it into a second corporate billboard.
    base.wall_sign(t, 22, 5, 31, "south", "VCF SERVICE", "RECEIVING")

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
            revision=f"intact-r1@{revision}",
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

    state["active_status"] = "gate_b_intact_r1_rendered_pending_review"
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
    gate["review_stage_source"] = "scripts/render_ows001_gate_b_intact.py"
    gate["review_only"] = True
    state["visual_review_gates"]["gate_b_intact_state"] = gate
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")

    print(
        f"Rendered OWS-001 Gate B intact r1 at {manifest['dimensions']} using "
        f"{manifest['fixed_camera_set']}; visual approval remains pending."
    )


if __name__ == "__main__":
    main()
