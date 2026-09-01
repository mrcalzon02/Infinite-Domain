#!/usr/bin/env python3
"""[SYSTEM REPORT] Guarded bookkeeping for an already-reviewed OWS-004 Gate-C r4.

This script does NOT decide visual quality. It mirrors the explicit human-authored
r4 PASSED decision into heavy_rebuild_state.json only after rechecking the exact
persisted r4 manifest and the mechanical invariants that were successfully
rendered. It opens Pass 19 only; Gate D and static promotion remain blocked.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "old_world_narrative" / "registry" / "heavy_rebuild_state.json"
REVIEW_ROOT = ROOT / "old_world_narrative" / "reviews" / "heavy_rebuild"
R4_ROOT = REVIEW_ROOT / "visual" / "OWS-004" / "gate_c_damage_states" / "r4"
MANIFEST_PATH = R4_ROOT / "gate_c_manifest.json"
REVIEW_PATH = REVIEW_ROOT / "OWS-004_GATE_C_R4_REVIEW.md"
R2_REVIEW_PATH = REVIEW_ROOT / "OWS-004_GATE_C_R2_REVIEW.md"

EXPECTED_PROOF_POS = [32, 2, 12]
EXPECTED_PROOF_TABLE = "infinite_domain:chests/old_world/ows_004_vcf_mycological_vertical_farm_tower"


def main() -> None:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if state.get("active_target") != "OWS-004":
        raise SystemExit(f"Refused: active target is {state.get('active_target')}")
    if not MANIFEST_PATH.is_file():
        raise SystemExit("Refused: exact OWS-004 Gate-C r4 manifest is absent")
    if not REVIEW_PATH.is_file():
        raise SystemExit("Refused: explicit OWS-004 Gate-C r4 visual review is absent")
    if not R2_REVIEW_PATH.is_file():
        raise SystemExit("Refused: prior rejected OWS-004 Gate-C r2 review is absent")

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    review = REVIEW_PATH.read_text(encoding="utf-8")
    r2_review = R2_REVIEW_PATH.read_text(encoding="utf-8")

    if not str(manifest.get("revision", "")).startswith("gate-c-r4@36fbf22b"):
        raise SystemExit(f"Refused: manifest is not the reviewed r4 revision: {manifest.get('revision')!r}")
    if manifest.get("d0_d1_status") != "frozen_from_accepted_r2_visual_review":
        raise SystemExit("Refused: r4 does not attest frozen reviewed D0/D1")
    if manifest.get("d1_changed_positions_from_d0") != 112:
        raise SystemExit("Refused: accepted D1 delta changed from 112")
    if manifest.get("d3_changed_positions_from_d0") != 727:
        raise SystemExit(
            f"Refused: reviewed r4 D3 delta changed from 727: {manifest.get('d3_changed_positions_from_d0')}"
        )
    if manifest.get("deterministic_spawners_d3") != 2:
        raise SystemExit("Refused: r4 does not preserve exactly two D3 encounter spawners")
    if manifest.get("proof_position") != EXPECTED_PROOF_POS:
        raise SystemExit(f"Refused: proof coordinate changed: {manifest.get('proof_position')}")
    if manifest.get("proof_loot_table") != EXPECTED_PROOF_TABLE:
        raise SystemExit(f"Refused: proof loot table changed: {manifest.get('proof_loot_table')}")
    if manifest.get("d3_revision_basis") != "OWS-004_GATE_C_R2_REVIEW.md":
        raise SystemExit("Refused: r4 no longer records the rejected r2 visual basis")

    normalized = review.upper()
    if "DECISION:" not in normalized or "PASSED" not in normalized:
        raise SystemExit("Refused: explicit r4 visual review does not contain a PASSED decision")
    if "OWS-004 GATE C R4: PASSED" not in normalized:
        raise SystemExit("Refused: explicit r4 gate decision line is missing")
    if "REVISION REQUIRED" in normalized:
        raise SystemExit("Refused: r4 review still contains REVISION REQUIRED")
    if "REVISION REQUIRED" not in r2_review.upper():
        raise SystemExit("Refused: prior r2 review no longer records its rejection")

    state["active_status"] = "gate_c_r4_passed_ready_for_micro_detail"
    for key in (
        "historical_layering",
        "environmental_narrative",
        "encounter_architecture",
        "loot_architecture",
        "quest_proof",
        "damage_and_decay",
    ):
        state["active_target_passes"][key] = "complete_gate_c_r4"
    state["active_target_passes"]["visual_gate_c_damage_states"] = "passed_r4"
    state["active_target_passes"]["micro_detail"] = "ready"

    gate = state["visual_review_gates"]["gate_c_damage_states"]
    gate["status"] = "passed_r4"
    gate["decision"] = "PASSED"
    gate["r2_review_record"] = str(R2_REVIEW_PATH.relative_to(ROOT)).replace("\\", "/")
    gate["r2_decision"] = "REVISION REQUIRED"
    gate["r4_artifact_manifest"] = str(MANIFEST_PATH.relative_to(ROOT)).replace("\\", "/")
    gate["r4_review_record"] = str(REVIEW_PATH.relative_to(ROOT)).replace("\\", "/")
    gate["r4_d1_changed_positions_from_d0"] = 112
    gate["r4_d3_changed_positions_from_d0"] = 727
    gate["significant_findings_corrected_or_justified"] = True
    state["visual_review_gates"]["gate_c_damage_states"] = gate

    state.setdefault("planning_records", {})["gate_c_r4_review"] = str(REVIEW_PATH.relative_to(ROOT)).replace("\\", "/")
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")
    print("Recorded OWS-004 Gate C r4 PASSED after exact artifact + explicit visual review; Pass 19 is ready.")


if __name__ == "__main__":
    main()
