#!/usr/bin/env python3
"""[SYSTEM REPORT] Record an already-completed Old World Gate-A visual decision.

This script performs no visual review. It requires the active target's persisted
Gate-A r1 render manifest and an explicit human-authored PASSED review record,
then records the massing pass and opens Pass 7 structural-system work.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STATE_PATH = ROOT / "dev/old_world_narrative" / "registry" / "heavy_rebuild_state.json"


def main() -> None:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    target = state.get("active_target")
    if not target:
        raise AssertionError("Heavy-rebuild state has no active target")

    gate = state.get("visual_review_gates", {}).get("gate_a_massing", {})
    if gate.get("status") == "passed_r1":
        print(f"{target} Gate A r1 is already recorded as passed.")
        return
    if gate.get("status") != "r1_rendered_pending_manual_review":
        raise AssertionError(f"{target} Gate A is not ready for r1 decision recording: {gate.get('status')}")

    manifest_rel = gate.get("r1_artifact_manifest")
    if not manifest_rel:
        raise AssertionError(f"{target} Gate-A state lacks r1 artifact manifest")
    manifest_path = ROOT / manifest_rel
    if not manifest_path.is_file():
        raise AssertionError(f"{target} Gate-A r1 manifest is missing: {manifest_rel}")

    review_rel = f"old_world_narrative/reviews/heavy_rebuild/{target}_GATE_A_R1_REVIEW.md"
    review_path = ROOT / review_rel
    if not review_path.is_file():
        raise AssertionError(f"{target} Gate-A r1 review is missing: {review_rel}")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("target") != target or manifest.get("gate") != "gate_a_massing":
        raise AssertionError("Gate-A r1 manifest identity mismatch")
    if manifest.get("fixed_camera_set") != gate.get("fixed_camera_set"):
        raise AssertionError("Gate-A r1 fixed-camera set mismatch")
    if manifest.get("visual_review_status") != "rendered_pending_manual_review":
        raise AssertionError("Gate-A r1 manifest is not a pending-review render set")

    review = review_path.read_text(encoding="utf-8")
    if "**Decision:** **PASSED**" not in review:
        raise AssertionError("Gate-A r1 review lacks explicit PASSED decision")
    accepted_pass_markers = (
        "**GATE A r1: PASSED.**",
        f"**{target} GATE A r1: PASSED.**",
    )
    if not any(marker in review for marker in accepted_pass_markers):
        raise AssertionError(
            f"Gate-A r1 review lacks explicit pass marker; expected one of {accepted_pass_markers}"
        )

    passes = state["active_target_passes"]
    passes["massing"] = "complete_gate_a_r1"
    passes["visual_gate_a_massing"] = "passed_r1"
    passes["structural_system"] = "ready"

    gate["status"] = "passed_r1"
    gate["decision"] = "PASSED"
    gate["r1_review_record"] = review_rel
    gate["significant_findings_corrected_or_justified"] = True
    state["visual_review_gates"]["gate_a_massing"] = gate

    gate_b = state["visual_review_gates"]["gate_b_intact_state"]
    gate_b["status"] = "blocked_by_passes_7_12"
    state["visual_review_gates"]["gate_b_intact_state"] = gate_b

    state.setdefault("planning_records", {})["gate_a_r1_review"] = review_rel
    state["active_status"] = "gate_a_r1_passed_pass_7_structural_system_ready"

    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Recorded {target} Gate A r1 PASSED; Pass 7 structural-system work is ready.")


if __name__ == "__main__":
    main()
