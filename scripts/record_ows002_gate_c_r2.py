#!/usr/bin/env python3
"""[SYSTEM REPORT] Record the completed manual OWS-002 Gate-C r2 review.

This script does not perform or infer visual review. It only records the explicit
human/assistant review decision already written in OWS-002_GATE_C_R2_REVIEW.md,
and only when the persisted r2 manifest still matches the reviewed artifact set.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "old_world_narrative" / "registry" / "heavy_rebuild_state.json"
MANIFEST_PATH = (
    ROOT
    / "old_world_narrative"
    / "reviews"
    / "heavy_rebuild"
    / "visual"
    / "OWS-002"
    / "gate_c_damage_states"
    / "r2"
    / "gate_c_manifest.json"
)
REVIEW_PATH = ROOT / "old_world_narrative" / "reviews" / "heavy_rebuild" / "OWS-002_GATE_C_R2_REVIEW.md"


def main() -> None:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if state.get("active_target") != "OWS-002":
        print(f"OWS-002 Gate-C r2 record skipped: active target is {state.get('active_target')}")
        return

    gate = state.get("visual_review_gates", {}).get("gate_c_damage_states", {})
    status = gate.get("status")
    if status == "passed_r2":
        print("OWS-002 Gate C already recorded as passed_r2")
        return
    if status != "r2_rendered_pending_manual_review":
        print(f"OWS-002 Gate-C r2 record skipped: status={status}")
        return

    if not MANIFEST_PATH.exists() or not REVIEW_PATH.exists():
        raise AssertionError("Gate-C r2 record requires the persisted r2 manifest and explicit review record")

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if manifest.get("target") != "OWS-002" or manifest.get("gate") != "gate_c_damage_states":
        raise AssertionError("Gate-C r2 manifest identity mismatch")
    if manifest.get("visual_review_status") != "rendered_pending_manual_review":
        raise AssertionError("Gate-C r2 manifest is not the manually reviewed pending artifact set")
    if manifest.get("accepted_from_r1") != ["D0", "D1"] or manifest.get("revised_in_r2") != ["D3"]:
        raise AssertionError("Gate-C r2 manifest no longer preserves the reviewed D0/D1 -> revised D3 relationship")

    changes = manifest.get("change_counts_from_d0", {})
    if changes.get("d1") != 83 or changes.get("d3") != 520:
        raise AssertionError(f"Gate-C r2 reviewed change counts no longer match: {changes}")

    review_text = REVIEW_PATH.read_text(encoding="utf-8")
    if "**PASSED.**" not in review_text or "**GATE C r2 STATUS: PASSED.**" not in review_text:
        raise AssertionError("Gate-C r2 review record does not contain the explicit reviewed pass decision")

    state["active_status"] = "gate_c_r2_passed_micro_detail_ready"
    for key in (
        "historical_layering",
        "environmental_narrative",
        "encounter_architecture",
        "loot_architecture",
        "quest_proof",
        "damage_and_decay",
    ):
        state["active_target_passes"][key] = "complete_gate_c_r2"
    state["active_target_passes"]["visual_gate_c_damage_states"] = "passed_r2"
    state["active_target_passes"]["micro_detail"] = "implementation_ready"

    gate["status"] = "passed_r2"
    gate["decision"] = "PASSED_R2"
    gate["r1_decision"] = "REVISION REQUIRED"
    gate["r2_decision"] = "PASSED"
    gate["r2_review_record"] = "old_world_narrative/reviews/heavy_rebuild/OWS-002_GATE_C_R2_REVIEW.md"
    gate["significant_findings_corrected_or_justified"] = True
    state["visual_review_gates"]["gate_c_damage_states"] = gate
    state.setdefault("planning_records", {})["gate_c_r2_review"] = (
        "old_world_narrative/reviews/heavy_rebuild/OWS-002_GATE_C_R2_REVIEW.md"
    )

    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")
    print("Recorded manually reviewed OWS-002 Gate C r2 PASSED; Pass 19 micro-detail is now ready.")


if __name__ == "__main__":
    main()
