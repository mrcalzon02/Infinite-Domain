#!/usr/bin/env python3
"""[SYSTEM REPORT] Record OWS-002 peak-quality static completion after Gate D.

This script does not perform visual review or invent a quality score. It mirrors
the explicit final Gate-D review and final rebuild report into the authoritative
state only when the persisted synchronization, image-regression and generated
structural-lint records still match the reviewed result.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STATE_PATH = ROOT / "dev/old_world_narrative" / "registry" / "heavy_rebuild_state.json"
GATE_D_REVIEW = ROOT / "dev/old_world_narrative" / "reviews" / "heavy_rebuild" / "OWS-002_GATE_D_R1_REVIEW.md"
FINAL_REPORT = ROOT / "dev/old_world_narrative" / "reviews" / "heavy_rebuild" / "OWS-002_FINAL_REBUILD_REPORT.md"
SYNC_PATH = ROOT / "dev/old_world_narrative" / "reviews" / "heavy_rebuild" / "visual" / "OWS-002" / "gate_d_final" / "r1" / "authoritative_sync.json"
METRICS_PATH = ROOT / "dev/old_world_narrative" / "reviews" / "heavy_rebuild" / "visual" / "OWS-002" / "gate_d_final" / "r1" / "visual_regression_metrics.json"
STRUCTURE_RECORD = ROOT / "dev/old_world_narrative" / "structures" / "ows-002-vcf-emergency-community-grow-hall.json"
FAILURE_LOG = ROOT / "dev/old_world_narrative" / "reviews" / "static-build-failure.log"
EXPECTED_HASH = "e6dd44528061f617a4259e8cb123afaa88451a16dd81cdf876475383f8d21548"
EXPECTED_BYTES = 907995
EXPECTED_SCORE = 94


def main() -> None:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if state.get("active_target") != "OWS-002":
        print(f"OWS-002 final-quality recorder skipped: active target is {state.get('active_target')}")
        return

    if "OWS-002" in state.get("completed", []):
        print("OWS-002 is already recorded as completed")
        return

    gate_c = state.get("visual_review_gates", {}).get("gate_c_damage_states", {})
    if gate_c.get("status") != "passed_r2":
        raise AssertionError(f"OWS-002 final promotion requires Gate C passed_r2; got {gate_c.get('status')}")

    gate_d = state.get("visual_review_gates", {}).get("gate_d_final_multi_angle", {})
    if gate_d.get("status") not in {
        "r1_image_checks_passed_pending_manual_review",
        "r1_image_checks_passed_authoritative_sync_verified_pending_manual_review",
    }:
        raise AssertionError(f"OWS-002 final promotion requires reviewed Gate-D artifact state; got {gate_d.get('status')}")

    for path in (GATE_D_REVIEW, FINAL_REPORT, SYNC_PATH, METRICS_PATH, STRUCTURE_RECORD):
        if not path.is_file():
            raise AssertionError(f"OWS-002 final promotion is missing required record: {path}")

    review = GATE_D_REVIEW.read_text(encoding="utf-8")
    if "**PASSED.**" not in review or "**OWS-002 GATE D r1: PASSED" not in review:
        raise AssertionError("OWS-002 Gate-D review does not contain the explicit inspected pass decision")

    report = FINAL_REPORT.read_text(encoding="utf-8")
    if f"**{EXPECTED_SCORE} / 100 — PASSED**" not in report:
        raise AssertionError("OWS-002 final report no longer contains the reviewed 94/100 score")
    if "**OWS-002 HEAVY SCHEMATIC REBUILD: PEAK-QUALITY STATIC APPROVED.**" not in report:
        raise AssertionError("OWS-002 final report lacks explicit peak-quality static approval")

    sync = json.loads(SYNC_PATH.read_text(encoding="utf-8"))
    if sync.get("authoritative_builder") != "old_world_ows002_final.build_002":
        raise AssertionError("OWS-002 Gate-D sync no longer points to the final builder")
    if sync.get("render_source") != "shipping_nbt" or not sync.get("exact_decompressed_nbt_match"):
        raise AssertionError("OWS-002 Gate-D synchronization is not exact shipping-NBT synchronization")
    if sync.get("decompressed_nbt_bytes") != EXPECTED_BYTES:
        raise AssertionError(f"OWS-002 reviewed NBT byte count changed: {sync.get('decompressed_nbt_bytes')}")
    if sync.get("builder_serialization_sha256") != EXPECTED_HASH or sync.get("shipping_nbt_sha256") != EXPECTED_HASH:
        raise AssertionError("OWS-002 reviewed builder/shipping SHA-256 no longer matches")

    metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    if metrics.get("decision") != "IMAGE_LEVEL_REGRESSION_CHECKS_PASSED_PENDING_MANUAL_REVIEW":
        raise AssertionError("OWS-002 Gate-D image regression has not passed")
    if metrics.get("foreground_silhouette_ratio_from_gate_c_r2_d3") and any(
        abs(float(value) - 1.0) > 0.05
        for value in metrics["foreground_silhouette_ratio_from_gate_c_r2_d3"].values()
    ):
        raise AssertionError("OWS-002 Gate-D silhouette no longer matches the reviewed result")

    structure = json.loads(STRUCTURE_RECORD.read_text(encoding="utf-8"))
    lint = structure.get("structural_lint", {})
    stats = structure.get("statistics", {})
    if structure.get("target_id") != "OWS-002":
        raise AssertionError("OWS-002 generated structure record identity mismatch")
    if stats.get("size") != [51, 21, 47] or stats.get("spawners") != 2:
        raise AssertionError(f"OWS-002 generated structure statistics changed: {stats}")
    if not lint.get("structural_lint_passed") or lint.get("issues"):
        raise AssertionError(f"OWS-002 generated structural lint is not clean: {lint}")
    if lint.get("orphan_door_halves") != 0:
        raise AssertionError("OWS-002 generated structure has orphan door halves")

    if FAILURE_LOG.exists():
        raise AssertionError("A static-build failure diagnostic exists; refuse OWS-002 quality promotion")

    state.setdefault("completed", []).append("OWS-002")
    state["completed"] = list(dict.fromkeys(state["completed"]))
    state.setdefault("static_review_passed", []).append("OWS-002")
    state["static_review_passed"] = list(dict.fromkeys(state["static_review_passed"]))
    # Runtime quality approval remains deliberately untouched.

    state.setdefault("completed_records", {})["OWS-002"] = {
        "quality_score": EXPECTED_SCORE,
        "quality_status": "peak_quality_static_approved",
        "final_report": "old_world_narrative/reviews/heavy_rebuild/OWS-002_FINAL_REBUILD_REPORT.md",
        "runtime_validation": "deferred",
    }

    state["active_status"] = "peak_quality_static_approved_runtime_validation_deferred"
    state["active_target_passes"]["micro_detail"] = "complete"
    state["active_target_passes"]["visual_gate_d_final_multi_angle"] = "passed_r1"
    state["active_target_passes"]["static_validation"] = "passed"
    state["active_target_passes"]["quality_status_promotion"] = "passed_94_of_100"
    gate_d["status"] = "passed_r1"
    gate_d["decision"] = "PASSED"
    gate_d["r1_review_record"] = "old_world_narrative/reviews/heavy_rebuild/OWS-002_GATE_D_R1_REVIEW.md"
    gate_d["significant_findings_corrected_or_justified"] = True
    state["visual_review_gates"]["gate_d_final_multi_angle"] = gate_d
    state.setdefault("planning_records", {})["gate_d_r1_review"] = (
        "old_world_narrative/reviews/heavy_rebuild/OWS-002_GATE_D_R1_REVIEW.md"
    )
    state["planning_records"]["final_rebuild_report"] = (
        "old_world_narrative/reviews/heavy_rebuild/OWS-002_FINAL_REBUILD_REPORT.md"
    )

    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")
    print("Recorded OWS-002 peak-quality static approval at 94/100; runtime validation remains deferred.")


if __name__ == "__main__":
    main()
