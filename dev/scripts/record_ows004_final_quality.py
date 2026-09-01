#!/usr/bin/env python3
"""[SYSTEM REPORT] Record OWS-004 peak-quality static completion after Gate D.

This recorder performs no visual review and invents no score. It mirrors the
explicit inspected Gate-D review and final rebuild report into authoritative state
only while the synchronized shipping hash, image-regression result and generated
structural-lint record still match the reviewed artifact.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STATE_PATH = ROOT / "dev/old_world_narrative" / "registry" / "heavy_rebuild_state.json"
GATE_D_REVIEW = ROOT / "dev/old_world_narrative" / "reviews" / "heavy_rebuild" / "OWS-004_GATE_D_R1_REVIEW.md"
FINAL_REPORT = ROOT / "dev/old_world_narrative" / "reviews" / "heavy_rebuild" / "OWS-004_FINAL_REBUILD_REPORT.md"
SYNC_PATH = ROOT / "dev/old_world_narrative" / "reviews" / "heavy_rebuild" / "visual" / "OWS-004" / "gate_d_final" / "r1" / "authoritative_sync.json"
METRICS_PATH = ROOT / "dev/old_world_narrative" / "reviews" / "heavy_rebuild" / "visual" / "OWS-004" / "gate_d_final" / "r1" / "visual_regression_metrics.json"
STRUCTURE_RECORD = ROOT / "dev/old_world_narrative" / "structures" / "ows-004-vcf-mycological-vertical-farm-tower.json"
FAILURE_LOG = ROOT / "dev/old_world_narrative" / "reviews" / "static-build-failure.log"
EXPECTED_HASH = "3c75be18613208a59daa0bb90d5810f10564fa018d77b87870f413d01d890b62"
EXPECTED_BYTES = 1505368
EXPECTED_SCORE = 95


def main() -> None:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if state.get("active_target") != "OWS-004":
        print(f"OWS-004 final-quality recorder skipped: active target is {state.get('active_target')}")
        return
    if "OWS-004" in state.get("completed", []):
        print("OWS-004 is already recorded as completed")
        return

    gate_c = state.get("visual_review_gates", {}).get("gate_c_damage_states", {})
    if gate_c.get("status") != "passed_r4":
        raise AssertionError(f"OWS-004 final promotion requires Gate C passed_r4; got {gate_c.get('status')}")

    for path in (GATE_D_REVIEW, FINAL_REPORT, SYNC_PATH, METRICS_PATH, STRUCTURE_RECORD):
        if not path.is_file():
            raise AssertionError(f"OWS-004 final promotion is missing required record: {path}")

    review = GATE_D_REVIEW.read_text(encoding="utf-8")
    if "**Decision:** **PASSED**" not in review or "**OWS-004 GATE D r1: PASSED.**" not in review:
        raise AssertionError("OWS-004 Gate-D review does not contain the explicit inspected pass decision")

    report = FINAL_REPORT.read_text(encoding="utf-8")
    if f"**{EXPECTED_SCORE} / 100 — PASSED**" not in report:
        raise AssertionError("OWS-004 final report no longer contains the reviewed 95/100 score")
    if "**OWS-004 HEAVY SCHEMATIC REBUILD: PEAK-QUALITY STATIC APPROVED.**" not in report:
        raise AssertionError("OWS-004 final report lacks explicit peak-quality static approval")

    sync = json.loads(SYNC_PATH.read_text(encoding="utf-8"))
    if sync.get("authoritative_builder") != "old_world_ows004_final.build_004":
        raise AssertionError("OWS-004 Gate-D sync no longer points to the final builder")
    if sync.get("render_source") != "shipping_nbt" or not sync.get("exact_decompressed_nbt_match"):
        raise AssertionError("OWS-004 Gate-D synchronization is not exact shipping-NBT synchronization")
    if sync.get("decompressed_nbt_bytes") != EXPECTED_BYTES:
        raise AssertionError(f"OWS-004 reviewed NBT byte count changed: {sync.get('decompressed_nbt_bytes')}")
    if sync.get("builder_serialization_sha256") != EXPECTED_HASH or sync.get("shipping_nbt_sha256") != EXPECTED_HASH:
        raise AssertionError("OWS-004 reviewed builder/shipping SHA-256 no longer matches")

    metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    if metrics.get("decision") != "IMAGE_LEVEL_REGRESSION_CHECKS_PASSED_PENDING_MANUAL_REVIEW":
        raise AssertionError("OWS-004 Gate-D image regression has not passed")
    if metrics.get("authoritative_sync", {}).get("shipping_nbt_sha256") != EXPECTED_HASH:
        raise AssertionError("OWS-004 Gate-D regression metrics reference a different shipping NBT")
    silhouettes = metrics.get("foreground_silhouette_ratio_from_gate_c_r4_d3", {})
    if not silhouettes or any(abs(float(value) - 1.0) > 0.05 for value in silhouettes.values()):
        raise AssertionError("OWS-004 Gate-D silhouette no longer matches the reviewed result")

    structure = json.loads(STRUCTURE_RECORD.read_text(encoding="utf-8"))
    lint = structure.get("structural_lint", {})
    stats = structure.get("statistics", {})
    if structure.get("target_id") != "OWS-004":
        raise AssertionError("OWS-004 generated structure record identity mismatch")
    if stats.get("size") != [51, 47, 47] or stats.get("spawners") != 2:
        raise AssertionError(f"OWS-004 generated structure statistics changed: {stats}")
    if stats.get("placed_blocks") != 41516 or stats.get("palette_states") != 63:
        raise AssertionError(f"OWS-004 reviewed structure statistics changed: {stats}")
    if stats.get("modded_blocks") != 5683:
        raise AssertionError(f"OWS-004 reviewed modded-block count changed: {stats}")
    if not lint.get("structural_lint_passed") or lint.get("issues"):
        raise AssertionError(f"OWS-004 generated structural lint is not clean: {lint}")
    if lint.get("orphan_door_halves") != 0 or lint.get("working_doors") != 24:
        raise AssertionError(f"OWS-004 door contracts changed: {lint}")
    if lint.get("functional_fixtures", 0) < 290 or lint.get("vertical_access_span", 0) < 37:
        raise AssertionError(f"OWS-004 operational/vertical coverage regressed: {lint}")

    if FAILURE_LOG.exists():
        raise AssertionError("A static-build failure diagnostic exists; refuse OWS-004 quality promotion")

    state.setdefault("completed", []).append("OWS-004")
    state["completed"] = list(dict.fromkeys(state["completed"]))
    state.setdefault("static_review_passed", []).append("OWS-004")
    state["static_review_passed"] = list(dict.fromkeys(state["static_review_passed"]))
    state.setdefault("completed_records", {})["OWS-004"] = {
        "quality_score": EXPECTED_SCORE,
        "quality_status": "peak_quality_static_approved",
        "final_report": "old_world_narrative/reviews/heavy_rebuild/OWS-004_FINAL_REBUILD_REPORT.md",
        "runtime_validation": "deferred",
    }

    state["active_status"] = "peak_quality_static_approved_runtime_validation_deferred"
    state["active_target_passes"]["micro_detail"] = "complete"
    state["active_target_passes"]["visual_gate_d_final_multi_angle"] = "passed_r1"
    state["active_target_passes"]["static_validation"] = "passed"
    state["active_target_passes"]["quality_status_promotion"] = "passed_95_of_100"

    gate_d = state.setdefault("visual_review_gates", {}).setdefault("gate_d_final_multi_angle", {})
    gate_d.update({
        "status": "passed_r1",
        "decision": "PASSED",
        "damage_state": "D3 authoritative worldgen state",
        "fixed_camera_set": "ows004_fixed_v1",
        "r1_artifact_manifest": "old_world_narrative/reviews/heavy_rebuild/visual/OWS-004/gate_d_final/r1/review_manifest.json",
        "r1_authoritative_sync": "old_world_narrative/reviews/heavy_rebuild/visual/OWS-004/gate_d_final/r1/authoritative_sync.json",
        "r1_visual_metrics": "old_world_narrative/reviews/heavy_rebuild/visual/OWS-004/gate_d_final/r1/visual_regression_metrics.json",
        "r1_review_record": "old_world_narrative/reviews/heavy_rebuild/OWS-004_GATE_D_R1_REVIEW.md",
        "render_source": "shipping_nbt",
        "exact_authoritative_nbt_match": True,
        "shipping_nbt_sha256": EXPECTED_HASH,
        "significant_findings_corrected_or_justified": True,
    })

    planning = state.setdefault("planning_records", {})
    planning["pass_19_micro_detail"] = "old_world_narrative/reviews/heavy_rebuild/OWS-004_PASS19_MICRODETAIL.md"
    planning["gate_d_r1_review"] = "old_world_narrative/reviews/heavy_rebuild/OWS-004_GATE_D_R1_REVIEW.md"
    planning["final_rebuild_report"] = "old_world_narrative/reviews/heavy_rebuild/OWS-004_FINAL_REBUILD_REPORT.md"

    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")
    print("Recorded OWS-004 peak-quality static approval at 95/100; runtime validation remains deferred.")


if __name__ == "__main__":
    main()
