#!/usr/bin/env python3
"""[SYSTEM REPORT] Guarded bookkeeping for an already-reviewed OWS-003 Gate-C r3.

This script does NOT decide visual quality. It advances the heavy-rebuild state
only after exact r3 artifacts, image QA, and an explicit human-authored PASSED
review record already exist.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "old_world_narrative" / "registry" / "heavy_rebuild_state.json"
REVIEW_ROOT = ROOT / "old_world_narrative" / "reviews" / "heavy_rebuild"
R3_ROOT = REVIEW_ROOT / "visual" / "OWS-003" / "gate_c_damage_states" / "r3"
MANIFEST_PATH = R3_ROOT / "gate_c_manifest.json"
METRICS_PATH = R3_ROOT / "visual_metrics.json"
REVIEW_PATH = REVIEW_ROOT / "OWS-003_GATE_C_R3_REVIEW.md"


def main() -> None:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if state.get("active_target") != "OWS-003":
        raise SystemExit(f"Refused: active target is {state.get('active_target')}")
    if not MANIFEST_PATH.is_file():
        raise SystemExit("Refused: exact OWS-003 Gate-C r3 manifest is absent")
    if not METRICS_PATH.is_file():
        raise SystemExit("Refused: OWS-003 Gate-C r3 image metrics are absent")
    if not REVIEW_PATH.is_file():
        raise SystemExit("Refused: explicit OWS-003 Gate-C r3 visual review is absent")

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    review = REVIEW_PATH.read_text(encoding="utf-8")

    if not str(manifest.get("revision", "")).startswith("gate-c-r3@"):
        raise SystemExit(f"Refused: manifest is not r3: {manifest.get('revision')!r}")
    if manifest.get("d1_changed_positions_from_d0") != 19:
        raise SystemExit("Refused: accepted D1 delta changed from 19")
    if int(manifest.get("d3_changed_positions_from_d0", 0)) < 550:
        raise SystemExit("Refused: r3 D3 does not meet strengthened change floor")
    if manifest.get("deterministic_spawners_d3") != 2:
        raise SystemExit("Refused: r3 does not preserve exactly two deterministic D3 spawners")
    if manifest.get("darknet_return_hook") != "reserved_not_activated":
        raise SystemExit("Refused: OWS-003 reserved Darknet hook was activated or lost")

    if metrics.get("decision") != "IMAGE_LEVEL_CHECKS_PASSED_PENDING_MANUAL_REVIEW":
        raise SystemExit("Refused: r3 image-level safeguards did not pass")
    required_checks = (
        "d1_visibly_present_in_internal_review",
        "d1_restrained",
        "d3_visibly_stronger_than_d1",
        "d3_visible_from_multiple_exterior_cameras",
        "d1_exterior_silhouette_retained",
        "d3_exterior_silhouette_retained",
    )
    checks = metrics.get("checks", {})
    if not all(checks.get(key) is True for key in required_checks):
        raise SystemExit(f"Refused: incomplete r3 image safeguards: {checks}")

    normalized = review.upper()
    if "DECISION:" not in normalized or "PASSED" not in normalized:
        raise SystemExit("Refused: explicit r3 visual review does not contain a PASSED decision")
    if "REVISION REQUIRED" in normalized:
        raise SystemExit("Refused: r3 visual review still contains REVISION REQUIRED")

    state["active_status"] = "gate_c_r3_passed_ready_for_micro_detail"
    for key in (
        "historical_layering",
        "environmental_narrative",
        "encounter_architecture",
        "loot_architecture",
        "quest_proof",
        "damage_and_decay",
    ):
        state["active_target_passes"][key] = "complete_gate_c_r3"
    state["active_target_passes"]["visual_gate_c_damage_states"] = "passed_r3"
    state["active_target_passes"]["micro_detail"] = "ready"

    gate = state["visual_review_gates"]["gate_c_damage_states"]
    gate["status"] = "passed_r3"
    gate["decision"] = "PASSED"
    gate["r3_artifact_manifest"] = str(MANIFEST_PATH.relative_to(ROOT)).replace("\\", "/")
    gate["r3_visual_metrics"] = str(METRICS_PATH.relative_to(ROOT)).replace("\\", "/")
    gate["r3_review_record"] = str(REVIEW_PATH.relative_to(ROOT)).replace("\\", "/")
    gate["r3_d1_changed_positions_from_d0"] = manifest["d1_changed_positions_from_d0"]
    gate["r3_d3_changed_positions_from_d0"] = manifest["d3_changed_positions_from_d0"]
    gate["significant_findings_corrected_or_justified"] = True
    state["visual_review_gates"]["gate_c_damage_states"] = gate

    state.setdefault("planning_records", {})["gate_c_r3_review"] = str(REVIEW_PATH.relative_to(ROOT)).replace("\\", "/")
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(
        "Recorded OWS-003 Gate C r3 PASSED after exact artifact + image QA + explicit visual review; "
        "Pass 19 is now ready."
    )


if __name__ == "__main__":
    main()
