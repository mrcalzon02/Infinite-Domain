#!/usr/bin/env python3
"""[SYSTEM REPORT] OWS-003 Gate-B intact review revision r3.

r1 failed before rendering because several process zones lacked complete controlled
boundary walls. r2 repaired those process boundaries but then exposed a second
physical correctness defect: the permanent PLANT ACCESS / STAFF ONLY wall sign
had no supporting wall above the maintenance entrance. r3 preserves the accepted
Gate-A massing and r2 process-boundary repairs, adds a real maintenance-door
header/support frame, and reruns the same intact-state contracts before rendering.
It remains review-only and introduces no historical damage, encounters or proof.
"""
from __future__ import annotations

import json
import os

import generate_wasteland_sites as base
import render_ows003_gate_b_intact as r1
import render_ows003_gate_b_intact_r2 as r2
from render_old_world_heavy_rebuild_review import OUTPUT_ROOT, ROOT, render_review_set
from render_structure_review import unpack_structure

STATE_PATH = ROOT / "dev/old_world_narrative" / "registry" / "heavy_rebuild_state.json"
TEMP_NAME = "_heavy_review_ows003_gate_b_intact_r3"
TEMP_NBT = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{TEMP_NAME}.nbt"
OUTPUT_DIR = OUTPUT_ROOT / "OWS-003" / "gate_b_intact" / "r3"


def _repair_plant_access_support(t: base.Template) -> None:
    """Frame the maintenance entrance so permanent plant-access signage is physical."""
    # The maintenance door occupies y=2..3 at x=50,z=36. The original massing left
    # open air above it, so the D0 PLANT ACCESS sign had no wall to mount to. Give the
    # entrance a real light-gray structural header/upper jamb without narrowing the
    # door or the ladder/service route behind it.
    t.fill((50, 4, 36), (50, 8, 36), "minecraft:light_gray_concrete")


def build_gate_b_intact_r3() -> base.Template:
    t = r1.build_gate_a_massing()
    r1._build_admin_and_records(t)
    r1._build_hall_structure(t)
    r1._build_cold_vault(t)
    r1._build_nursery_cells(t)
    r1._build_receiving_quality_and_outbound(t)
    r2._add_missing_process_boundaries(t)
    r1._build_operations_spine(t)
    r1._build_plant_and_maintenance(t)
    r1._articulate_exterior(t)
    _repair_plant_access_support(t)
    r1._add_identity_and_wayfinding(t)
    return t


def _assert_r3_repairs(t: base.Template) -> None:
    r2._assert_r2_process_boundaries(t)
    r1._assert_block(
        t,
        50,
        6,
        36,
        "minecraft:light_gray_concrete",
        "plant-access signage support",
    )
    r1._assert_door(t, 50, 2, 36, "maintenance-tower ground access door")
    # Ensure the sign itself occupies the intended face rather than floating elsewhere.
    r1._assert_block(t, 49, 6, 36, "minecraft:oak_wall_sign", "plant-access wall sign")


def main() -> None:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if state.get("active_target") != "OWS-003":
        print(f"Gate-B OWS-003 r3 renderer skipped: active target is {state.get('active_target')}")
        return

    gate = state.get("visual_review_gates", {}).get("gate_b_intact_state", {})
    status = gate.get("status", "not_started")
    if status not in {"ready_for_intact_implementation", "ready_to_render", "rerender_required"}:
        print(f"Gate-B OWS-003 r3 renderer skipped: status={status}")
        return

    t = build_gate_b_intact_r3()
    r1._assert_intact_contracts(t)
    _assert_r3_repairs(t)
    base.stabilize_door_pairs(t)
    r1._assert_intact_contracts(t)
    _assert_r3_repairs(t)

    t.save(TEMP_NAME)
    try:
        size, blocks = unpack_structure(TEMP_NBT)
        revision = os.environ.get("GITHUB_SHA", "local")[:8]
        manifest = render_review_set(
            target="OWS-003",
            gate="gate_b_intact",
            revision=f"intact-r3@{revision}",
            damage_state="D0 intact / operational",
            source_commit=os.environ.get("GITHUB_SHA", "working-tree"),
            source_path="review-only:render_ows003_gate_b_intact_r3.build_gate_b_intact_r3()",
            size=size,
            blocks=blocks,
            output_dir=OUTPUT_DIR,
            camera_set=gate.get("fixed_camera_set", "ows003_fixed_v1"),
        )
    finally:
        TEMP_NBT.unlink(missing_ok=True)

    # Clear stale failed-attempt diagnostics only after r3 reaches rendered state.
    failure_path = ROOT / "dev/old_world_narrative" / "reviews" / "heavy_rebuild" / "OWS-003_GATE_B_FAILURE.log"
    failure_path.unlink(missing_ok=True)

    state["active_status"] = "gate_b_r3_intact_rendered_pending_review"
    for key in (
        "structural_system",
        "circulation_and_access",
        "exterior_architecture",
        "interior_architecture",
        "operational_systems",
        "institutional_identity",
    ):
        state["active_target_passes"][key] = "r3_implemented_pending_gate_b_review"
    state["active_target_passes"]["visual_gate_b_intact_state"] = "r3_rendered_pending_manual_review"
    gate["status"] = "r3_rendered_pending_manual_review"
    gate["r1_implementation_failure"] = "missing controlled boundaries/support walls at release, packing and outbound staging"
    gate["r2_implementation_failure"] = "maintenance plant-access sign had no physical support wall above the service entrance"
    gate["r3_artifact_manifest"] = str((OUTPUT_DIR / "review_manifest.json").relative_to(ROOT)).replace("\\", "/")
    gate["review_stage_source"] = "scripts/render_ows003_gate_b_intact_r3.py"
    gate["review_only"] = True
    state["visual_review_gates"]["gate_b_intact_state"] = gate
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")

    print(
        f"Rendered OWS-003 Gate B r3 intact review at {manifest['dimensions']} using "
        f"{manifest['fixed_camera_set']}; manual intact-state approval remains pending."
    )


if __name__ == "__main__":
    main()
