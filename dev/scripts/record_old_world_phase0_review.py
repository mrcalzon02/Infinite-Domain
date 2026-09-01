#!/usr/bin/env python3
"""[SYSTEM REPORT] Record an already-completed Old World Phase-0 visual decision.

This script never performs visual review. It only records a human-authored
REBUILD REQUIRED decision after the exact baseline manifest and matching review
record already exist for the active target.
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

    review_rel = f"old_world_narrative/reviews/heavy_rebuild/{target}_PHASE0_BASELINE_REVIEW.md"
    review_path = ROOT / review_rel
    gate = state.get("visual_review_gates", {}).get("baseline", {})
    manifest_rel = gate.get("artifact_manifest")
    if not manifest_rel:
        raise AssertionError(f"{target} Phase-0 review cannot be recorded without a baseline manifest")
    manifest_path = ROOT / manifest_rel
    if not manifest_path.is_file():
        raise AssertionError(f"{target} baseline manifest is missing: {manifest_rel}")
    if not review_path.is_file():
        raise AssertionError(f"{target} Phase-0 review record is missing: {review_rel}")

    allowed_statuses = {"rendered_pending_manual_review", "reviewed_rebuild_required"}
    if gate.get("status") not in allowed_statuses:
        raise AssertionError(
            f"{target} baseline status is not recordable: {gate.get('status')}"
        )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("target") != target or manifest.get("gate") != "baseline":
        raise AssertionError("Phase-0 manifest identity does not match active target")
    if manifest.get("source_commit") != state.get("baseline_source_commit"):
        raise AssertionError(
            "Phase-0 manifest source commit does not match frozen baseline_source_commit"
        )
    if manifest.get("fixed_camera_set") != gate.get("fixed_camera_set"):
        raise AssertionError("Phase-0 manifest camera set does not match state")

    review = review_path.read_text(encoding="utf-8")
    required_markers = (
        "**Decision:** **REBUILD REQUIRED**",
        "**DONOR AUDIT: COMPLETE.**",
        "**BASELINE VISUAL REVIEW: COMPLETE — REBUILD REQUIRED.**",
    )
    missing = [marker for marker in required_markers if marker not in review]
    if missing:
        raise AssertionError(f"Phase-0 review lacks required decision markers: {missing}")

    state["active_status"] = "phase_0_reviewed_pass_2_functional_definition_ready"
    state["active_target_passes"]["donor_audit"] = "complete"
    state["active_target_passes"]["baseline_3d_review"] = "reviewed_rebuild_required"
    state["active_target_passes"]["functional_definition"] = "ready"
    state.setdefault("planning_records", {})["phase_0_baseline_review"] = review_rel

    gate["status"] = "reviewed_rebuild_required"
    gate["review_record"] = review_rel
    gate["decision"] = "REBUILD REQUIRED"
    gate["significant_findings_corrected_or_justified"] = False
    state["visual_review_gates"]["baseline"] = gate

    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(
        f"Recorded {target} Phase-0 REBUILD REQUIRED; Pass 2 functional definition is now ready."
    )


if __name__ == "__main__":
    main()
