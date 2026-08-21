#!/usr/bin/env python3
"""[SYSTEM REPORT] Promote OWS-002 past Gate C after completed manual visual review.

This script does not perform visual review. It records the already-completed r1
manual decision only when the exact persisted Gate-C manifest and review record
are present and still match the approved chronology.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "old_world_narrative" / "registry" / "heavy_rebuild_state.json"
MANIFEST_PATH = ROOT / "old_world_narrative" / "reviews" / "heavy_rebuild" / "visual" / "OWS-002" / "gate_c_damage_states" / "r1" / "gate_c_manifest.json"
REVIEW_PATH = ROOT / "old_world_narrative" / "reviews" / "heavy_rebuild" / "OWS-002_GATE_C_R1_REVIEW.md"


def main() -> None:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if state.get("active_target") != "OWS-002":
        print(f"OWS-002 Gate-C approval skipped: active target is {state.get('active_target')}")
        return

    gate = state.get("visual_review_gates", {}).get("gate_c_damage_states", {})
    status = gate.get("status")
    if status == "passed_r1":
        print("OWS-002 Gate C already recorded as passed_r1")
        return
    if status != "r1_rendered_pending_manual_review":
        print(f"OWS-002 Gate-C approval skipped: status={status}")
        return

    if not MANIFEST_PATH.exists() or not REVIEW_PATH.exists():
        raise AssertionError("Gate-C approval requires both the persisted r1 manifest and manual review record")

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if manifest.get("target") != "OWS-002" or manifest.get("gate") != "gate_c_damage_states":
        raise AssertionError("Gate-C manifest identity mismatch")
    if manifest.get("visual_review_status") != "rendered_pending_manual_review":
        raise AssertionError("Gate-C manifest is not the reviewed r1 render set")
    changes = manifest.get("change_counts_from_d0", {})
    if changes.get("d1") != 83 or changes.get("d3") != 352:
        raise AssertionError(f"Gate-C reviewed change counts no longer match approval: {changes}")

    review_text = REVIEW_PATH.read_text(encoding="utf-8")
    if "**PASSED.**" not in review_text or "Gate C therefore passes at r1" not in review_text:
        raise AssertionError("Manual Gate-C review record does not contain the approved r1 decision")

    state["active_status"] = "gate_c_r1_passed_micro_detail_ready"
    for key in (
        "historical_layering",
        "environmental_narrative",
        "encounter_architecture",
        "loot_architecture",
        "quest_proof",
        "damage_and_decay",
    ):
        state["active_target_passes"][key] = "complete_gate_c_r1"
    state["active_target_passes"]["visual_gate_c_damage_states"] = "passed_r1"
    state["active_target_passes"]["micro_detail"] = "implementation_ready"

    gate["status"] = "passed_r1"
    gate["decision"] = "PASSED"
    gate["r1_review_record"] = "old_world_narrative/reviews/heavy_rebuild/OWS-002_GATE_C_R1_REVIEW.md"
    gate["significant_findings_corrected_or_justified"] = True
    state["visual_review_gates"]["gate_c_damage_states"] = gate
    state.setdefault("planning_records", {})["gate_c_r1_review"] = "old_world_narrative/reviews/heavy_rebuild/OWS-002_GATE_C_R1_REVIEW.md"

    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")
    print("Recorded OWS-002 Gate C r1 PASSED; Pass 19 micro-detail is now the next valid stage.")


if __name__ == "__main__":
    main()
