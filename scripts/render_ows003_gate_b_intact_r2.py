#!/usr/bin/env python3
"""[SYSTEM REPORT] OWS-003 Gate-B intact review revision r2.

r1 failed before rendering because release inspection, packing and outbound cold
staging were equipped zones without complete controlled boundary walls. This r2
reuses the accepted Gate-A massing and r1 component builders, inserts those three
missing boundaries/crossings, then applies the same signage and mechanical route
assertions. It remains review-only and introduces no historical damage or proof.
"""
from __future__ import annotations

import json
import os

import generate_wasteland_sites as base
import render_ows003_gate_b_intact as r1
from render_old_world_heavy_rebuild_review import OUTPUT_ROOT, ROOT, render_review_set
from render_structure_review import unpack_structure

STATE_PATH = ROOT / "old_world_narrative" / "registry" / "heavy_rebuild_state.json"
TEMP_NAME = "_heavy_review_ows003_gate_b_intact_r2"
TEMP_NBT = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{TEMP_NAME}.nbt"
OUTPUT_DIR = OUTPUT_ROOT / "OWS-003" / "gate_b_intact" / "r2"


def _add_missing_process_boundaries(t: base.Template) -> None:
    """Give release, packing and outbound staging actual controlled architecture."""
    # Release inspection: west/rear room separated from the operations spine.
    t.fill((35, 2, 36), (35, 7, 42), "minecraft:white_concrete")
    t.clear((35, 2, 40), (35, 4, 40))
    r1._door(t, 35, 2, 40, "east")

    # Conditioned packing: later clean insert east of the operations spine.
    t.fill((39, 2, 37), (39, 7, 42), "minecraft:white_concrete")
    t.clear((39, 2, 40), (39, 4, 40))
    r1._door(t, 39, 2, 40, "east")

    # Outbound cold staging: separate conditioned buffer before dispatch.
    t.fill((48, 2, 38), (48, 7, 42), "minecraft:white_concrete")
    t.clear((48, 2, 40), (48, 4, 40))
    r1._door(t, 48, 2, 40, "east")


def build_gate_b_intact_r2() -> base.Template:
    t = r1.build_gate_a_massing()
    r1._build_admin_and_records(t)
    r1._build_hall_structure(t)
    r1._build_cold_vault(t)
    r1._build_nursery_cells(t)
    r1._build_receiving_quality_and_outbound(t)
    _add_missing_process_boundaries(t)
    r1._build_operations_spine(t)
    r1._build_plant_and_maintenance(t)
    r1._articulate_exterior(t)
    r1._add_identity_and_wayfinding(t)
    return t


def _assert_r2_process_boundaries(t: base.Template) -> None:
    r1._assert_door(t, 35, 2, 40, "release-to-operations control door")
    r1._assert_door(t, 39, 2, 40, "operations-to-packing control door")
    r1._assert_door(t, 48, 2, 40, "packing-to-outbound-cold control door")
    # The original protected center spine must remain intact after adding walls.
    r1._assert_clear(t, (36, 2, 18), (38, 4, 42), "r2 protected operations spine")
    # Release and packing each keep usable work area behind their new walls.
    r1._assert_clear(t, (29, 3, 40), (34, 4, 42), "release-inspection working aisle")
    r1._assert_clear(t, (40, 4, 40), (47, 5, 42), "conditioned-packing working aisle")


def main() -> None:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if state.get("active_target") != "OWS-003":
        print(f"Gate-B OWS-003 r2 renderer skipped: active target is {state.get('active_target')}")
        return

    gate = state.get("visual_review_gates", {}).get("gate_b_intact_state", {})
    status = gate.get("status", "not_started")
    if status not in {"ready_for_intact_implementation", "ready_to_render", "rerender_required"}:
        print(f"Gate-B OWS-003 r2 renderer skipped: status={status}")
        return

    t = build_gate_b_intact_r2()
    r1._assert_intact_contracts(t)
    _assert_r2_process_boundaries(t)
    base.stabilize_door_pairs(t)
    r1._assert_intact_contracts(t)
    _assert_r2_process_boundaries(t)

    t.save(TEMP_NAME)
    try:
        size, blocks = unpack_structure(TEMP_NBT)
        revision = os.environ.get("GITHUB_SHA", "local")[:8]
        manifest = render_review_set(
            target="OWS-003",
            gate="gate_b_intact",
            revision=f"intact-r2@{revision}",
            damage_state="D0 intact / operational",
            source_commit=os.environ.get("GITHUB_SHA", "working-tree"),
            source_path="review-only:render_ows003_gate_b_intact_r2.build_gate_b_intact_r2()",
            size=size,
            blocks=blocks,
            output_dir=OUTPUT_DIR,
            camera_set=gate.get("fixed_camera_set", "ows003_fixed_v1"),
        )
    finally:
        TEMP_NBT.unlink(missing_ok=True)

    # Clear the stale r1 failure diagnostic only after r2 reaches rendered state.
    failure_path = ROOT / "old_world_narrative" / "reviews" / "heavy_rebuild" / "OWS-003_GATE_B_FAILURE.log"
    failure_path.unlink(missing_ok=True)

    state["active_status"] = "gate_b_r2_intact_rendered_pending_review"
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
    gate["r1_implementation_failure"] = "missing controlled boundaries/support walls at release, packing and outbound staging"
    gate["r2_artifact_manifest"] = str((OUTPUT_DIR / "review_manifest.json").relative_to(ROOT)).replace("\\", "/")
    gate["review_stage_source"] = "scripts/render_ows003_gate_b_intact_r2.py"
    gate["review_only"] = True
    state["visual_review_gates"]["gate_b_intact_state"] = gate
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")

    print(
        f"Rendered OWS-003 Gate B r2 intact review at {manifest['dimensions']} using "
        f"{manifest['fixed_camera_set']}; manual intact-state approval remains pending."
    )


if __name__ == "__main__":
    main()
