#!/usr/bin/env python3
"""[SYSTEM REPORT] OWS-004 Gate-B intact review revision r4.

r3 added the missing principal staff/player switchback stair but failed before
rendering because its assertion classified an intentional flat dogleg landing as
a missing stair tread. r4 preserves the r3 geometry and corrects only that
mechanical contract: actual treads remain mandatory, intentional polished-andesite
turning landings are validated separately, and all r3 door/headroom/egress/freight/
utility checks still run.
"""
from __future__ import annotations

import json
import os

import generate_wasteland_sites as base
import render_ows004_gate_b_intact as r1
import render_ows004_gate_b_intact_r2 as r2
import render_ows004_gate_b_intact_r3 as r3
from render_old_world_heavy_rebuild_review import OUTPUT_ROOT, ROOT, render_review_set
from render_structure_review import unpack_structure

STATE_PATH = ROOT / "old_world_narrative" / "registry" / "heavy_rebuild_state.json"
TEMP_NAME = "_heavy_review_ows004_gate_b_intact_r4"
TEMP_NBT = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{TEMP_NAME}.nbt"
OUTPUT_DIR = OUTPUT_ROOT / "OWS-004" / "gate_b_intact" / "r4"


def build_gate_b_intact_r4():
    t = r2.build_gate_b_intact_r2()
    raw_expected = r3._install_primary_staff_stair(t)

    # Long first flights terminate onto a flat transverse landing; those landing
    # coordinates replace the conceptual final tread and are valid route geometry.
    landing_points = [point for point in raw_expected if r3._name(t, *point) == "minecraft:polished_andesite"]
    expected_treads = [point for point in raw_expected if r3._name(t, *point) == "minecraft:stone_brick_stairs"]
    unexpected = [
        (point, r3._name(t, *point))
        for point in raw_expected
        if r3._name(t, *point) not in {"minecraft:polished_andesite", "minecraft:stone_brick_stairs"}
    ]
    if unexpected:
        raise AssertionError(f"OWS-004 r4 stair path contains unexpected substitutions: {unexpected}")
    if landing_points != [(40, 6, 22), (40, 35, 22)]:
        raise AssertionError(f"OWS-004 r4 unexpected dogleg landing substitutions: {landing_points}")
    for x, y, z in landing_points:
        if r3._name(t, x, y, z) != "minecraft:polished_andesite":
            raise AssertionError(f"OWS-004 r4 dogleg landing missing at {(x, y, z)}")
        for head_y in (y + 1, y + 2):
            if r3._name(t, x, head_y, z) not in r3.AIR:
                raise AssertionError(f"OWS-004 r4 landing headroom blocked at {(x, head_y, z)}")

    # Keep every accepted r2 contract and every r3 circulation/service assertion.
    r1._assert_intact_contracts(t)
    r3._assert_staff_stair(t, expected_treads)
    return t, expected_treads, landing_points


def _assert_r4(t, expected_treads, landing_points) -> None:
    if len(expected_treads) < 40:
        raise AssertionError(f"OWS-004 r4 principal staff route too short: {len(expected_treads)} stair treads")
    if len(landing_points) != 2:
        raise AssertionError(f"OWS-004 r4 expected two long-flight landing transitions; found {landing_points}")
    r1._assert_intact_contracts(t)
    r3._assert_staff_stair(t, expected_treads)


def main() -> None:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if state.get("active_target") != "OWS-004":
        print(f"Gate-B OWS-004 r4 renderer skipped: active target is {state.get('active_target')}")
        return

    gate = state.get("visual_review_gates", {}).get("gate_b_intact_state", {})
    status = gate.get("status", "not_started")
    if status not in {
        "ready_for_intact_implementation",
        "ready_to_render",
        "rerender_required",
        "r2_rendered_pending_manual_review",
    }:
        print(f"Gate-B OWS-004 r4 renderer skipped: status={status}")
        return

    t, expected_treads, landing_points = build_gate_b_intact_r4()
    _assert_r4(t, expected_treads, landing_points)
    base.stabilize_door_pairs(t)
    _assert_r4(t, expected_treads, landing_points)
    if tuple(t.size) != (51, 47, 47):
        raise AssertionError(f"OWS-004 Gate-B r4 dimensions changed unexpectedly: {t.size}")

    t.save(TEMP_NAME)
    try:
        size, blocks = unpack_structure(TEMP_NBT)
        revision = os.environ.get("GITHUB_SHA", "local")[:8]
        manifest = render_review_set(
            target="OWS-004",
            gate="gate_b_intact",
            revision=f"intact-r4@{revision}",
            damage_state="D0 intact / operational",
            source_commit=os.environ.get("GITHUB_SHA", "working-tree"),
            source_path="review-only:render_ows004_gate_b_intact_r4.build_gate_b_intact_r4()",
            size=size,
            blocks=blocks,
            output_dir=OUTPUT_DIR,
            camera_set=gate.get("fixed_camera_set", "ows004_fixed_v1"),
        )
    finally:
        TEMP_NBT.unlink(missing_ok=True)

    state["active_status"] = "gate_b_r4_intact_rendered_pending_review"
    for key in (
        "structural_system",
        "circulation_and_access",
        "exterior_architecture",
        "interior_architecture",
        "operational_systems",
        "institutional_identity",
    ):
        state["active_target_passes"][key] = "implemented_gate_b_r4_pending_review"
    state["active_target_passes"]["visual_gate_b_intact_state"] = "r4_rendered_pending_manual_review"
    gate["status"] = "r4_rendered_pending_manual_review"
    gate["r2_review_record"] = "old_world_narrative/reviews/heavy_rebuild/OWS-004_GATE_B_R2_REVIEW.md"
    gate["r2_decision"] = "REVISION REQUIRED"
    gate["r2_implementation_failure"] = "intact model lacked the required principal staff/player stair system"
    gate["r3_implementation_failure"] = "staff-stair assertion treated intentional dogleg landing at (40,6,22) as a missing tread before rendering"
    gate["r4_artifact_manifest"] = str((OUTPUT_DIR / "review_manifest.json").relative_to(ROOT)).replace("\\", "/")
    gate["review_stage_source"] = "scripts/render_ows004_gate_b_intact_r4.py"
    gate["review_only"] = True
    state["visual_review_gates"]["gate_b_intact_state"] = gate
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")

    print(
        f"Rendered OWS-004 Gate B r4 intact review at {manifest['dimensions']} using "
        f"{manifest['fixed_camera_set']}; manual intact-state approval remains pending."
    )


if __name__ == "__main__":
    main()
