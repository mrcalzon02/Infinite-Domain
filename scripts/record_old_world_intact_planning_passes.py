#!/usr/bin/env python3
"""[SYSTEM REPORT] Record completed Old World Passes 7-12 and open Gate B.

This utility does no visual approval. It verifies that Gate A is already passed and
that the active target has explicit completed Pass 7-12 records, then marks those
planning passes complete and opens intact-state implementation.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "old_world_narrative" / "registry" / "heavy_rebuild_state.json"

PASS_FILES = {
    "structural_system": ("PASS7_STRUCTURAL_SYSTEM", "**STRUCTURAL SYSTEM: COMPLETE.**"),
    "circulation_and_access": ("PASS8_CIRCULATION_ACCESS", "**CIRCULATION AND ACCESS: COMPLETE.**"),
    "exterior_architecture": ("PASS9_EXTERIOR_ARCHITECTURE", "**EXTERIOR ARCHITECTURE: COMPLETE.**"),
    "interior_architecture": ("PASS10_INTERIOR_ARCHITECTURE", "**INTERIOR ARCHITECTURE: COMPLETE.**"),
    "operational_systems": ("PASS11_OPERATIONAL_SYSTEMS", "**OPERATIONAL SYSTEMS: COMPLETE.**"),
    "institutional_identity": ("PASS12_VCF_IDENTITY", "**VCF INSTITUTIONAL IDENTITY: COMPLETE.**"),
}


def main() -> None:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    target = state.get("active_target")
    if not target:
        raise AssertionError("Heavy-rebuild state has no active target")

    gate_a = state.get("visual_review_gates", {}).get("gate_a_massing", {})
    if not str(gate_a.get("status", "")).startswith("passed_"):
        raise AssertionError(f"{target} Passes 7-12 cannot advance before Gate A passes")

    records = state.setdefault("planning_records", {})
    for pass_key, (stem, marker) in PASS_FILES.items():
        rel = f"old_world_narrative/reviews/heavy_rebuild/{target}_{stem}.md"
        path = ROOT / rel
        if not path.is_file():
            raise AssertionError(f"Missing {target} intact-planning record: {rel}")
        text = path.read_text(encoding="utf-8")
        if marker not in text:
            raise AssertionError(f"{target} intact-planning record lacks marker {marker}: {rel}")
        records[pass_key] = rel

    passes = state["active_target_passes"]
    for pass_key in PASS_FILES:
        passes[pass_key] = "defined_ready_for_gate_b_implementation"
    passes["visual_gate_b_intact_state"] = "ready_for_intact_implementation"

    gate_b = state["visual_review_gates"]["gate_b_intact_state"]
    gate_b["status"] = "ready_for_intact_implementation"
    gate_b["rule"] = (
        "D0 must prove the retained cannery frame, inserted cold rooms, receiving/intake/pre-cool, vault/nursery, "
        "quality hold, release/licensing, packing/dispatch, refrigeration plant and usable maintenance route before history begins."
    )
    state["visual_review_gates"]["gate_b_intact_state"] = gate_b
    state["active_status"] = "gate_b_intact_ready_to_implement"

    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Recorded {target} Passes 7-12 complete; Gate-B intact implementation is ready.")


if __name__ == "__main__":
    main()
