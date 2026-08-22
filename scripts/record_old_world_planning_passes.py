#!/usr/bin/env python3
"""[SYSTEM REPORT] Record completed Old World planning passes through Gate-A readiness.

The script is deliberately mechanical. It does not perform design review. It only
verifies that the active target has a reviewed Phase-0 baseline and explicit Pass
2-5 records with their completion markers, then opens the Gate-A massing stage.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "old_world_narrative" / "registry" / "heavy_rebuild_state.json"

PASS_FILES = {
    "functional_definition": ("PASS2_FUNCTIONAL_DEFINITION", "**FUNCTIONAL DEFINITION: COMPLETE.**"),
    "precedent_research": ("PASS3_PRECEDENT_RESEARCH", "**PRECEDENT RESEARCH: COMPLETE.**"),
    "program_and_adjacency": ("PASS4_PROGRAM_ADJACENCY", "**PROGRAM AND ADJACENCY: COMPLETE.**"),
    "scale_translation": ("PASS5_SCALE_TRANSLATION", "**SCALE TRANSLATION: COMPLETE FOR GATE-A STUDY.**"),
}


def main() -> None:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    target = state.get("active_target")
    if not target:
        raise AssertionError("Heavy-rebuild state has no active target")

    baseline = state.get("visual_review_gates", {}).get("baseline", {})
    if baseline.get("status") != "reviewed_rebuild_required":
        raise AssertionError(
            f"{target} planning cannot advance before Phase-0 REBUILD REQUIRED is recorded; "
            f"baseline={baseline.get('status')}"
        )

    records = state.setdefault("planning_records", {})
    for pass_key, (stem, marker) in PASS_FILES.items():
        rel = f"old_world_narrative/reviews/heavy_rebuild/{target}_{stem}.md"
        path = ROOT / rel
        if not path.is_file():
            raise AssertionError(f"Missing {target} planning record: {rel}")
        text = path.read_text(encoding="utf-8")
        if marker not in text:
            raise AssertionError(f"{target} planning record lacks completion marker {marker}: {rel}")
        records[pass_key] = rel

    passes = state["active_target_passes"]
    passes["functional_definition"] = "complete"
    passes["precedent_research"] = "complete"
    passes["program_and_adjacency"] = "complete"
    passes["scale_translation"] = "complete_for_gate_a_study"
    passes["massing"] = "ready_for_implementation"
    passes["visual_gate_a_massing"] = "ready_for_massing_implementation"

    gate_a = state["visual_review_gates"]["gate_a_massing"]
    gate_a["status"] = "ready_for_massing_implementation"
    gate_a["rule"] = (
        "Prove the active target's approved macro program, institutional hierarchy, functional thresholds, "
        "service/maintenance anatomy and site relationship at massing scale before operational detail, damage, "
        "loot, encounters or microdetail may hide architectural defects."
    )
    state["visual_review_gates"]["gate_a_massing"] = gate_a
    state["active_status"] = "gate_a_massing_ready_to_implement"

    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Recorded {target} Passes 2-5 complete; Gate-A massing implementation is ready.")


if __name__ == "__main__":
    main()
