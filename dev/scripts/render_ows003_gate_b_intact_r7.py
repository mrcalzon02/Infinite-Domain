#!/usr/bin/env python3
"""[SYSTEM REPORT] OWS-003 Gate-B intact review revision r7.

r5 cleared the nursery support-stock aisles and exposed one remaining inherited
frame post at x=43,z=32 inside nursery 3. r6 already addresses the analogous
receiving-lane post at x=49,z=26. r7 composes all previous repairs and transfers
the nursery-3 post above the cold-room envelope as well, leaving every protected
D0 operations route clear while retaining the old cannery frame overhead.
It remains review-only and introduces no historical damage, encounters or proof.
"""
from __future__ import annotations

import json
import os

import generate_wasteland_sites as base
import render_ows003_gate_b_intact as r1
import render_ows003_gate_b_intact_r6 as r6
from render_old_world_heavy_rebuild_review import OUTPUT_ROOT, ROOT, render_review_set
from render_structure_review import unpack_structure

STATE_PATH = ROOT / "dev/old_world_narrative" / "registry" / "heavy_rebuild_state.json"
TEMP_NAME = "_heavy_review_ows003_gate_b_intact_r7"
TEMP_NBT = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{TEMP_NAME}.nbt"
OUTPUT_DIR = OUTPUT_ROOT / "OWS-003" / "gate_b_intact" / "r7"


def _repair_nursery3_frame(t: base.Template) -> None:
    """Transfer the inherited x=43,z=32 post above dormancy nursery 3."""
    t.clear((43, 2, 32), (43, 8, 32))
    t.fill((39, 9, 32), (47, 9, 32), "tfmg:steel_block")
    t.fill((39, 2, 32), (39, 9, 32), "tfmg:steel_block")
    t.fill((47, 2, 32), (47, 9, 32), "tfmg:steel_block")


def build_gate_b_intact_r7() -> base.Template:
    t = r6.build_gate_b_intact_r6()
    _repair_nursery3_frame(t)
    return t


def _assert_r7_repairs(t: base.Template) -> None:
    r6._assert_r6_repairs(t)
    r1._assert_clear(t, (40, 2, 32), (44, 4, 35), "r7 nursery 3 service area")
    r1._assert_block(t, 43, 9, 32, "tfmg:steel_block", "nursery-3 transfer header")
    r1._assert_block(t, 39, 9, 32, "tfmg:steel_block", "nursery-3 west transfer jamb")
    r1._assert_block(t, 47, 9, 32, "tfmg:steel_block", "nursery-3 east transfer jamb")


def main() -> None:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if state.get("active_target") != "OWS-003":
        print(f"Gate-B OWS-003 r7 renderer skipped: active target is {state.get('active_target')}")
        return

    gate = state.get("visual_review_gates", {}).get("gate_b_intact_state", {})
    status = gate.get("status", "not_started")
    if status not in {"ready_for_intact_implementation", "ready_to_render", "rerender_required"}:
        print(f"Gate-B OWS-003 r7 renderer skipped: status={status}")
        return

    t = build_gate_b_intact_r7()
    r1._assert_intact_contracts(t)
    _assert_r7_repairs(t)
    base.stabilize_door_pairs(t)
    r1._assert_intact_contracts(t)
    _assert_r7_repairs(t)

    t.save(TEMP_NAME)
    try:
        size, blocks = unpack_structure(TEMP_NBT)
        revision = os.environ.get("GITHUB_SHA", "local")[:8]
        manifest = render_review_set(
            target="OWS-003",
            gate="gate_b_intact",
            revision=f"intact-r7@{revision}",
            damage_state="D0 intact / operational",
            source_commit=os.environ.get("GITHUB_SHA", "working-tree"),
            source_path="review-only:render_ows003_gate_b_intact_r7.build_gate_b_intact_r7()",
            size=size,
            blocks=blocks,
            output_dir=OUTPUT_DIR,
            camera_set=gate.get("fixed_camera_set", "ows003_fixed_v1"),
        )
    finally:
        TEMP_NBT.unlink(missing_ok=True)

    failure_path = ROOT / "dev/old_world_narrative" / "reviews" / "heavy_rebuild" / "OWS-003_GATE_B_FAILURE.log"
    failure_path.unlink(missing_ok=True)

    state["active_status"] = "gate_b_r7_intact_rendered_pending_review"
    for key in (
        "structural_system",
        "circulation_and_access",
        "exterior_architecture",
        "interior_architecture",
        "operational_systems",
        "institutional_identity",
    ):
        state["active_target_passes"][key] = "r7_implemented_pending_gate_b_review"
    state["active_target_passes"]["visual_gate_b_intact_state"] = "r7_rendered_pending_manual_review"
    gate["status"] = "r7_rendered_pending_manual_review"
    gate["r1_implementation_failure"] = "missing controlled boundaries/support walls at release, packing and outbound staging"
    gate["r2_implementation_failure"] = "maintenance plant-access sign had no physical support wall above the service entrance"
    gate["r3_implementation_failure"] = "retained cannery steel posts obstructed the protected cold-vault center aisle"
    gate["r4_implementation_failure"] = "nursery support crate stacks obstructed the protected inspection/service floors"
    gate["r5_implementation_failure"] = "retained x=43,z=32 cannery post obstructed nursery-3 service floor"
    gate["r6_source_audit_finding"] = "retained x=49,z=26 cannery post occupied the conditioned receiving freight lane"
    gate["r7_artifact_manifest"] = str((OUTPUT_DIR / "review_manifest.json").relative_to(ROOT)).replace("\\", "/")
    gate["review_stage_source"] = "scripts/render_ows003_gate_b_intact_r7.py"
    gate["review_only"] = True
    state["visual_review_gates"]["gate_b_intact_state"] = gate
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")

    print(
        f"Rendered OWS-003 Gate B r7 intact review at {manifest['dimensions']} using "
        f"{manifest['fixed_camera_set']}; manual intact-state approval remains pending."
    )


if __name__ == "__main__":
    main()
