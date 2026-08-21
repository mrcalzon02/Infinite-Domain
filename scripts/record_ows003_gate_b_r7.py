#!/usr/bin/env python3
"""[SYSTEM REPORT] Record the already-reviewed OWS-003 Gate-B r7 decision.

This script does not judge images. It only synchronizes heavy_rebuild_state.json
after a human/assistant visual review has already been committed as PASSED and
the exact r7 render manifest is present.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "old_world_narrative" / "registry" / "heavy_rebuild_state.json"
REVIEW_PATH = ROOT / "old_world_narrative" / "reviews" / "heavy_rebuild" / "OWS-003_GATE_B_R7_REVIEW.md"
MANIFEST_REL = "old_world_narrative/reviews/heavy_rebuild/visual/OWS-003/gate_b_intact/r7/review_manifest.json"
MANIFEST_PATH = ROOT / MANIFEST_REL


def main() -> None:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if state.get("active_target") != "OWS-003":
        raise SystemExit(f"Refused Gate-B recording: active target is {state.get('active_target')}")
    if not REVIEW_PATH.exists():
        raise SystemExit("Refused Gate-B recording: explicit r7 review record is missing")
    review = REVIEW_PATH.read_text(encoding="utf-8")
    if "OWS-003 GATE B r7: PASSED" not in review or "**Decision:** **PASSED**" not in review:
        raise SystemExit("Refused Gate-B recording: r7 review is not explicitly PASSED")
    if not MANIFEST_PATH.exists():
        raise SystemExit("Refused Gate-B recording: persisted r7 artifact manifest is missing")
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if manifest.get("target") != "OWS-003" or manifest.get("gate") != "gate_b_intact":
        raise SystemExit("Refused Gate-B recording: artifact manifest does not describe OWS-003 Gate B")
    if "r7" not in str(manifest.get("revision", "")):
        raise SystemExit(f"Refused Gate-B recording: expected r7 manifest, found {manifest.get('revision')}")

    state["active_status"] = "gate_b_r7_passed_history_planning_ready"
    for key in (
        "structural_system",
        "circulation_and_access",
        "exterior_architecture",
        "interior_architecture",
        "operational_systems",
        "institutional_identity",
    ):
        state["active_target_passes"][key] = "complete_gate_b_r7"
    state["active_target_passes"]["visual_gate_b_intact_state"] = "passed_r7"

    gate = state["visual_review_gates"]["gate_b_intact_state"]
    gate["status"] = "passed_r7"
    gate["decision"] = "PASSED"
    gate["review_record"] = str(REVIEW_PATH.relative_to(ROOT)).replace("\\", "/")
    gate["r7_artifact_manifest"] = MANIFEST_REL
    gate["significant_findings_corrected_or_justified"] = True
    state["visual_review_gates"]["gate_b_intact_state"] = gate

    for key in (
        "historical_layering",
        "environmental_narrative",
        "encounter_architecture",
        "loot_architecture",
        "quest_proof",
        "damage_and_decay",
    ):
        if state["active_target_passes"].get(key) == "pending":
            state["active_target_passes"][key] = "ready_for_planning"

    state.setdefault("planning_records", {})["gate_b_r7_review"] = str(REVIEW_PATH.relative_to(ROOT)).replace("\\", "/")
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")
    print("Recorded explicit OWS-003 Gate-B r7 PASSED decision; historical planning is now unlocked.")


if __name__ == "__main__":
    main()
