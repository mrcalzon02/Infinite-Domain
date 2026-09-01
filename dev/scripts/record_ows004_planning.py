#!/usr/bin/env python3
"""[SYSTEM REPORT] Guard and record OWS-004 heavy-rebuild planning state.

This recorder mirrors already-authored planning documents into the active heavy-
rebuild registry. It never renders or approves a visual gate. All transitions are
monotonic: rerunning planning after Gate B/Gate C has advanced may refresh record
paths, but may not roll the target backward.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STATE_PATH = ROOT / "dev/old_world_narrative" / "registry" / "heavy_rebuild_state.json"
REVIEW_ROOT = ROOT / "dev/old_world_narrative" / "reviews" / "heavy_rebuild"

EARLY_REQUIRED = {
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

HISTORY_FILES = {
    "historical_layering": (
        "OWS-004_PASS13_HISTORICAL_LAYERING.md",
        "HISTORICAL LAYERING: COMPLETE FOR GATE-C IMPLEMENTATION",
    ),
    "environmental_narrative": (
        "OWS-004_PASS14_ENVIRONMENTAL_NARRATIVE.md",
        "ENVIRONMENTAL NARRATIVE: COMPLETE FOR GATE-C IMPLEMENTATION",
    ),
    "encounter_architecture": (
        "OWS-004_PASS15_ENCOUNTER_ARCHITECTURE.md",
        "ENCOUNTER ARCHITECTURE: COMPLETE FOR GATE-C IMPLEMENTATION",
    ),
    "loot_architecture": (
        "OWS-004_PASS16_LOOT_ARCHITECTURE.md",
        "LOOT ARCHITECTURE: COMPLETE FOR GATE-C IMPLEMENTATION",
    ),
    "quest_proof": (
        "OWS-004_PASS17_QUEST_PROOF_ARCHITECTURE.md",
        "QUEST-PROOF ARCHITECTURE: COMPLETE FOR GATE-C IMPLEMENTATION",
    ),
    "damage_and_decay": (
        "OWS-004_PASS18_DAMAGE_AND_DECAY.md",
        "DAMAGE AND DECAY: COMPLETE FOR GATE-C IMPLEMENTATION",
    ),
}

GATE_C_OPENABLE = {
    "blocked_by_gate_b_and_history_passes",
    "pending",
    "ready",
    "ready_to_render",
}


def _read(name: str) -> str:
    path = REVIEW_ROOT / name
    if not path.is_file():
        raise AssertionError(f"OWS-004 planning recorder missing required record: {path}")
    return path.read_text(encoding="utf-8")


def _intact_records_present() -> bool:
    return all((REVIEW_ROOT / name).is_file() for name in INTACT_FILES)


def _history_records_complete() -> bool:
    for filename, marker in HISTORY_FILES.values():
        path = REVIEW_ROOT / filename
        if not path.is_file() or marker not in path.read_text(encoding="utf-8"):
            return False
    return True


def _advanced_active_status(value: str) -> bool:
    value = str(value or "")
    return value.startswith(("gate_b_r", "gate_c_", "gate_d_", "peak_quality_", "static_"))


def _record_history_if_authorized(state: dict) -> bool:
    gate_b = state.get("visual_review_gates", {}).get("gate_b_intact_state", {})
    gate_b_passed = str(gate_b.get("status", "")).startswith("passed") and gate_b.get("decision") == "PASSED"
    if not gate_b_passed or not _history_records_complete():
        return False

    passes = state.setdefault("active_target_passes", {})
    records = state.setdefault("planning_records", {})
    gate_c = state.setdefault("visual_review_gates", {}).setdefault("gate_c_damage_states", {})
    gate_c_status = str(gate_c.get("status", ""))

    # A passed Gate C proves that Passes 13-18 were not merely planned: they were
    # implemented in, rendered with, and accepted as part of that exact revision.
    # Recover that stronger state when a generic planning workflow reruns later.
    if gate_c_status.startswith("passed_r"):
        revision = gate_c_status.removeprefix("passed_")
        history_status = f"complete_gate_c_{revision}"
    else:
        history_status = "complete_for_gate_c_implementation"

    for pass_key, (filename, _marker) in HISTORY_FILES.items():
        current = str(passes.get(pass_key, ""))
        if gate_c_status.startswith("passed_r"):
            passes[pass_key] = history_status
        elif not current.startswith(("implemented_gate_c_", "complete_gate_c_", "complete_gate_d_", "peak_quality_", "static_")):
            passes[pass_key] = history_status
        records[pass_key] = f"old_world_narrative/reviews/heavy_rebuild/{filename}"

    if gate_c_status in GATE_C_OPENABLE:
        gate_c["status"] = "ready_to_render"
        gate_c["history_planning_complete"] = True
        gate_c["required_history_documents"] = [
            f"old_world_narrative/reviews/heavy_rebuild/{filename}"
            for filename, _marker in HISTORY_FILES.values()
        ]
        gate_c["review_only"] = True
        gate_c["fixed_camera_set"] = gate_c.get("fixed_camera_set", "ows004_fixed_v1")
        passes["visual_gate_c_damage_states"] = "ready_to_render"
        if not _advanced_active_status(state.get("active_status", "")):
            state["active_status"] = "gate_c_damage_states_ready_to_render"
    return True


def main() -> None:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if state.get("active_target") != "OWS-004":
        print(f"OWS-004 planning recorder skipped: active target is {state.get('active_target')}")
        return

    baseline = state.get("visual_review_gates", {}).get("baseline", {})
    if baseline.get("status") != "reviewed_rebuild_required" or baseline.get("decision") != "REBUILD REQUIRED":
        raise AssertionError(
            "OWS-004 planning cannot advance until the exact baseline is explicitly reviewed REBUILD REQUIRED"
        )

    phase0 = _read(EARLY_REQUIRED["phase_0_baseline_review"])
    if "**REBUILD REQUIRED**" not in phase0 or "BASELINE VISUAL REVIEW: COMPLETE" not in phase0:
        raise AssertionError("OWS-004 Phase-0 review lacks the explicit rebuild-required decision")

    pass2 = _read(EARLY_REQUIRED["functional_definition"])
    pass3 = _read(EARLY_REQUIRED["precedent_research"])
    pass4 = _read(EARLY_REQUIRED["program_and_adjacency"])
    pass5 = _read(EARLY_REQUIRED["scale_translation"])
    for label, text in (("Pass 2", pass2), ("Pass 3", pass3), ("Pass 4", pass4), ("Pass 5", pass5)):
        if "**Status:** COMPLETE" not in text:
            raise AssertionError(f"OWS-004 {label} is not explicitly COMPLETE")
    if "Retain the current **51 x 47 x 47** envelope" not in pass5:
        raise AssertionError("OWS-004 Gate-A scale contract changed unexpectedly")

    passes = state.setdefault("active_target_passes", {})
    passes["donor_audit"] = "complete"
    passes["baseline_3d_review"] = "reviewed_rebuild_required"
    passes["functional_definition"] = "complete"
    passes["precedent_research"] = "complete"
    passes["program_and_adjacency"] = "complete"
    passes["scale_translation"] = "complete_for_gate_a_study"

    planning = state.setdefault("planning_records", {})
    for key, filename in EARLY_REQUIRED.items():
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
        if not _advanced_active_status(state.get("active_status", "")):
            state["active_status"] = "gate_a_ready_for_massing_implementation"
        STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")
        print("OWS-004 Phase-0 and Passes 2-5 recorded; Gate A remains unresolved.")
        return

    if passes.get("structural_system") in {None, "pending"}:
        passes["structural_system"] = "ready"

    # First preserve/record intact planning without allowing it to downgrade an
    # advanced Gate-B state. The generic recorder is itself monotonic.
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")
    if _intact_records_present():
        sys.path.insert(0, str(ROOT / "dev/scripts"))
        import record_old_world_intact_planning_passes
        record_old_world_intact_planning_passes.main()
        state = json.loads(STATE_PATH.read_text(encoding="utf-8"))

    if _record_history_if_authorized(state):
        STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")
        gate_c_status = state["visual_review_gates"]["gate_c_damage_states"].get("status")
        print(f"OWS-004 Passes 13-18 recorded monotonically; Gate-C state preserved/advanced as {gate_c_status!r}.")
        return

    if not _advanced_active_status(state.get("active_status", "")):
        gate_b_status = str(state.get("visual_review_gates", {}).get("gate_b_intact_state", {}).get("status", ""))
        if gate_b_status.startswith("passed"):
            state["active_status"] = "gate_b_r4_passed_history_ready"
        else:
            state["active_status"] = "gate_b_intact_ready_to_implement"
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")
    print("OWS-004 planning records refreshed without regressing advanced gate state.")


if __name__ == "__main__":
    main()
