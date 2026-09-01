#!/usr/bin/env python3
"""[SYSTEM REPORT] OWS-003 Gate-B intact review revision r5.

r4 repaired the cold-vault transfer frame and then exposed a program contradiction:
all three nursery cells claimed broad inspection/service aisles while their support
crate stacks occupied those same floor zones. r5 preserves the accepted massing
and all earlier repairs, relocates the nursery support crates onto the east-side
cooler/equipment bank, and proves every nursery service area remains clear.
It remains review-only and introduces no historical damage, encounters or proof.
"""
from __future__ import annotations

import json
import os

import generate_wasteland_sites as base
import render_ows003_gate_b_intact as r1
import render_ows003_gate_b_intact_r4 as r4
from render_old_world_heavy_rebuild_review import OUTPUT_ROOT, ROOT, render_review_set
from render_structure_review import unpack_structure

STATE_PATH = ROOT / "old_world_narrative" / "registry" / "heavy_rebuild_state.json"
TEMP_NAME = "_heavy_review_ows003_gate_b_intact_r5"
TEMP_NBT = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{TEMP_NAME}.nbt"
OUTPUT_DIR = OUTPUT_ROOT / "OWS-003" / "gate_b_intact" / "r5"


def _repair_nursery_service_aisles(t: base.Template) -> None:
    """Move cell support stock out of the protected west-side service floors."""
    for z1 in (22, 27, 32):
        t.clear((41, 2, z1 + 1), (42, 3, z1 + 2))
        t.fill((45, 3, z1 + 1), (46, 4, z1 + 2), "immersiveengineering:crate")


def build_gate_b_intact_r5() -> base.Template:
    t = r4.build_gate_b_intact_r4()
    _repair_nursery_service_aisles(t)
    return t


def _assert_r5_repairs(t: base.Template) -> None:
    r4._assert_r4_repairs(t)
    for label, a, b in (
        ("nursery 1 service area", (40, 2, 22), (44, 4, 25)),
        ("nursery 2 service area", (40, 2, 27), (44, 4, 30)),
        ("nursery 3 service area", (40, 2, 32), (44, 4, 35)),
    ):
        r1._assert_clear(t, a, b, f"r5 {label}")
    for z1 in (22, 27, 32):
        r1._assert_block(t, 45, 3, z1 + 1, "immersiveengineering:crate", f"nursery support stock z={z1}")


def main() -> None:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if state.get("active_target") != "OWS-003":
        print(f"Gate-B OWS-003 r5 renderer skipped: active target is {state.get('active_target')}")
        return

    gate = state.get("visual_review_gates", {}).get("gate_b_intact_state", {})
    status = gate.get("status", "not_started")
    if status not in {"ready_for_intact_implementation", "ready_to_render", "rerender_required"}:
        print(f"Gate-B OWS-003 r5 renderer skipped: status={status}")
        return

    t = build_gate_b_intact_r5()
    r1._assert_intact_contracts(t)
    _assert_r5_repairs(t)
    base.stabilize_door_pairs(t)
    r1._assert_intact_contracts(t)
    _assert_r5_repairs(t)

    t.save(TEMP_NAME)
    try:
        size, blocks = unpack_structure(TEMP_NBT)
        revision = os.environ.get("GITHUB_SHA", "local")[:8]
        manifest = render_review_set(
            target="OWS-003",
            gate="gate_b_intact",
            revision=f"intact-r5@{revision}",
            damage_state="D0 intact / operational",
            source_commit=os.environ.get("GITHUB_SHA", "working-tree"),
            source_path="review-only:render_ows003_gate_b_intact_r5.build_gate_b_intact_r5()",
            size=size,
            blocks=blocks,
            output_dir=OUTPUT_DIR,
            camera_set=gate.get("fixed_camera_set", "ows003_fixed_v1"),
        )
    finally:
        TEMP_NBT.unlink(missing_ok=True)

    failure_path = ROOT / "old_world_narrative" / "reviews" / "heavy_rebuild" / "OWS-003_GATE_B_FAILURE.log"
    failure_path.unlink(missing_ok=True)

    state["active_status"] = "gate_b_r5_intact_rendered_pending_review"
    for key in (
        "structural_system",
        "circulation_and_access",
        "exterior_architecture",
        "interior_architecture",
        "operational_systems",
        "institutional_identity",
    ):
        state["active_target_passes"][key] = "r5_implemented_pending_gate_b_review"
    state["active_target_passes"]["visual_gate_b_intact_state"] = "r5_rendered_pending_manual_review"
    gate["status"] = "r5_rendered_pending_manual_review"
    gate["r1_implementation_failure"] = "missing controlled boundaries/support walls at release, packing and outbound staging"
    gate["r2_implementation_failure"] = "maintenance plant-access sign had no physical support wall above the service entrance"
    gate["r3_implementation_failure"] = "retained cannery steel posts obstructed the protected cold-vault center aisle"
    gate["r4_implementation_failure"] = "nursery support crate stacks obstructed the protected inspection/service floors"
    gate["r5_artifact_manifest"] = str((OUTPUT_DIR / "review_manifest.json").relative_to(ROOT)).replace("\\", "/")
    gate["review_stage_source"] = "scripts/render_ows003_gate_b_intact_r5.py"
    gate["review_only"] = True
    state["visual_review_gates"]["gate_b_intact_state"] = gate
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")

    print(
        f"Rendered OWS-003 Gate B r5 intact review at {manifest['dimensions']} using "
        f"{manifest['fixed_camera_set']}; manual intact-state approval remains pending."
    )


if __name__ == "__main__":
    main()
