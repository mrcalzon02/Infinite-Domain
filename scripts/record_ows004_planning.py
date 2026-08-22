#!/usr/bin/env python3
"""[SYSTEM REPORT] Guard OWS-004 planning completion across Gate A / Gate B planning.

This recorder does not render or approve a visual gate. It mirrors the already-
authored Phase-0 / Passes 2-5 planning into state, preserves an already-passed
Gate A, and when all explicit Passes 7-12 records exist delegates to the generic
intact-planning recorder. Visual Gate B remains a separate manual review.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "old_world_narrative" / "registry" / "heavy_rebuild_state.json"
REVIEW_ROOT = ROOT / "old_world_narrative" / "reviews" / "heavy_rebuild"

REQUIRED = {
    "phase_0_baseline_review": "OWS-004_PHASE0_BASELINE_REVIEW.md",
    "functional_definition": "OWS-004_PASS2_FUNCTIONAL_DEFINITION.md",
    "precedent_research": "OWS-004_PASS3_PRECEDENT_RESEARCH.md",
    "program_and_adjacency": "OWS-004_PASS4_PROGRAM_ADJACENCY.md",
    "scale_translation": "OWS-004_PASS5_SCALE_TRANSLATION.md",
}

INTACT_FILES = (
    "OWS-004_PASS7_STRUCTURAL_SYSTEM.md",
    "OWS-004_PASS8_CIRCULATION_ACCESS.md",
    "OWS-004_PASS9_EXTERIOR_ARCHITECTURE.md",
    "OWS-004_PASS10_INTERIOR_ARCHITECTURE.md",
    "OWS-004_PASS11_OPERATIONAL_SYSTEMS.md",
    "OWS-004_PASS12_VCF_IDENTITY.md",
)


def _read(name: str) -> str:
    path = REVIEW_ROOT / name
    if not path.is_file():
        raise AssertionError(f"OWS-004 planning recorder missing required record: {path}")
    return path.read_text(encoding="utf-8")


def _intact_records_present() -> bool:
    return all((REVIEW_ROOT / name).is_file() for name in INTACT_FILES)


def main() -> None:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if state.get("active_target") != "OWS-004":
        print(f"OWS-004 planning recorder skipped: active target is {state.get('active_target')}")
        return

    baseline = state.get("visual_review_gates", {}).get("baseline", {})
    if baseline.get("status") != "reviewed_rebuild_required" or baseline.get("decision") != "REBUILD REQUIRED":
        raise AssertionError(
            "OWS-004 planning cannot unlock Gate A until the exact baseline is explicitly reviewed REBUILD REQUIRED"
        )

    phase0 = _read(REQUIRED["phase_0_baseline_review"])
    if "**REBUILD REQUIRED**" not in phase0 or "BASELINE VISUAL REVIEW: COMPLETE" not in phase0:
        raise AssertionError("OWS-004 Phase-0 review lacks the explicit rebuild-required decision")

    pass2 = _read(REQUIRED["functional_definition"])
    pass3 = _read(REQUIRED["precedent_research"])
    pass4 = _read(REQUIRED["program_and_adjacency"])
    pass5 = _read(REQUIRED["scale_translation"])
    for label, text in (("Pass 2", pass2), ("Pass 3", pass3), ("Pass 4", pass4), ("Pass 5", pass5)):
        if "**Status:** COMPLETE" not in text:
            raise AssertionError(f"OWS-004 {label} is not explicitly COMPLETE")
    if "Retain the current **51 x 47 x 47** envelope" not in pass5:
        raise AssertionError("OWS-004 Gate-A scale contract changed unexpectedly")

    passes = state["active_target_passes"]
    passes["donor_audit"] = "complete"
    passes["baseline_3d_review"] = "reviewed_rebuild_required"
    passes["functional_definition"] = "complete"
    passes["precedent_research"] = "complete"
    passes["program_and_adjacency"] = "complete"
    passes["scale_translation"] = "complete_for_gate_a_study"

    planning = state.setdefault("planning_records", {})
    for key, filename in REQUIRED.items():
        planning[key] = f"old_world_narrative/reviews/heavy_rebuild/{filename}"

    gate_a = state["visual_review_gates"]["gate_a_massing"]
    gate_a_passed = str(gate_a.get("status", "")).startswith("passed")
    if not gate_a_passed:
        if passes.get("massing") in {None, "pending"}:
            passes["massing"] = "ready_for_implementation"
        if passes.get("visual_gate_a_massing") in {None, "pending"}:
            passes["visual_gate_a_massing"] = "ready_to_render"
        gate_a["status"] = "ready_for_massing_implementation"
        gate_a["review_only"] = True
        gate_a["rule"] = (
            "Prove public/industrial podium hierarchy, four cultivation-module bands, a real vertical "
            "service/core expression, distinct receiving/dispatch thresholds and a greenhouse/environmental "
            "crown inside the retained 51x47x47 envelope before operational detail."
        )
        state["active_status"] = "gate_a_ready_for_massing_implementation"
    else:
        # Never regress an already-reviewed Gate A to an earlier planning status.
        if passes.get("structural_system") in {None, "pending"}:
            passes["structural_system"] = "ready"
        state["active_status"] = "gate_a_r1_passed_pass_7_structural_system_ready"

    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")

    if gate_a_passed and _intact_records_present():
        sys.path.insert(0, str(ROOT / "scripts"))
        import record_old_world_intact_planning_passes
        record_old_world_intact_planning_passes.main()
        print("OWS-004 Passes 7-12 records detected; Gate-B intact implementation opened.")
    else:
        print("OWS-004 Phase-0 and Passes 2-5 recorded; waiting on Gate A or complete Passes 7-12 records.")


if __name__ == "__main__":
    main()
