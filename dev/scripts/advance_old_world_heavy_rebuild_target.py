#!/usr/bin/env python3
"""[SYSTEM REPORT] Advance the heavy-rebuild queue one completed target at a time.

This utility is intentionally conservative. It advances only when the current
active target is already listed in `completed`, selects the first incomplete
queue entry, snapshots the current source revision as that target's immutable
Phase-0 baseline commit, and resets only the active-target pass/gate workspace.
It never marks a pass complete and never advances past an unfinished target.

Queue trigger marker: OWS-004 synchronized Gate-D/static promotion completed.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "old_world_narrative" / "registry" / "heavy_rebuild_state.json"

INSTITUTIONS = {
    "vcf": "Verdant Continuum Foods",
    "atlas": "Atlas Kinetic Industries",
    "polycore": "PolyCore",
    "pleroma": "Pleroma Logistics",
    "aevum": "Aevum",
    "helion": "Helion",
    "blackglass": "Blackglass",
    "asterion": "Asterion",
    "continuity": "Continuity",
}


def _display_name(target: str) -> tuple[str, str]:
    # Import lazily so the transition tool does not participate in normal worldgen.
    import sys
    sys.path.insert(0, str(ROOT / "scripts"))
    import old_world_narrative_core as core

    spec = next((row for row in core.SPECS if row.target == target), None)
    if spec is None:
        raise AssertionError(f"No Old World Spec exists for {target}")
    prefix = f"{target.lower().replace('-', '_')}_"
    remainder = spec.name[len(prefix):] if spec.name.startswith(prefix) else spec.name
    parts = remainder.split("_")
    institution_key = parts[0] if parts and parts[0] in INSTITUTIONS else ""
    if institution_key:
        parts = parts[1:]
    name = " ".join(word.capitalize() for word in parts)
    institution = INSTITUTIONS.get(institution_key, "Old World")
    return name, institution


def _fresh_pass_state(pass_order: list[str]) -> dict[str, str]:
    state = {key: "pending" for key in pass_order}
    state["donor_audit"] = "ready"
    state["baseline_3d_review"] = "pending_render"
    return state


def _fresh_visual_gates(target: str) -> dict:
    camera_set = f"{target.lower().replace('-', '')}_fixed_v1"
    return {
        "baseline": {
            "status": "pending_render",
            "required": True,
            "source": f"untouched {target} functional shipping geometry at baseline_source_commit",
            "minimum_views": [
                "front_left",
                "front_right",
                "rear_right",
                "rear_left",
                "roof_top_oblique",
                "interior_or_cutaway",
            ],
            "contact_sheet": True,
            "fixed_camera_set": camera_set,
        },
        "gate_a_massing": {
            "status": "blocked_by_phase_0_and_planning",
            "required": True,
            "damage_state": "D0 intact massing",
            "fixed_camera_set": camera_set,
            "review_only": True,
        },
        "gate_b_intact_state": {
            "status": "blocked_by_gate_a",
            "required": True,
            "damage_state": "D0 intact / operational",
            "fixed_camera_set": camera_set,
            "review_only": True,
        },
        "gate_c_damage_states": {
            "status": "blocked_by_gate_b_and_history_passes",
            "required": True,
            "minimum_states": ["D0", "D1", "D3"],
            "fixed_camera_set": camera_set,
            "review_only": True,
        },
        "gate_d_final_multi_angle": {
            "status": "blocked_by_gate_c_micro_detail_and_authoritative_sync",
            "required": True,
            "damage_state": "D3 authoritative worldgen state",
            "fixed_camera_set": camera_set,
        },
    }


def main() -> None:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    active = state.get("active_target")
    completed = list(state.get("completed", []))

    if active not in completed:
        print(f"Heavy-rebuild advancement skipped: active target {active} is not completed.")
        return

    queue = list(state.get("queue", []))
    next_target = next((target for target in queue if target not in completed), None)
    if next_target is None:
        print("Heavy-rebuild advancement skipped: all queued targets are completed.")
        return

    name, institution = _display_name(next_target)
    baseline_commit = os.environ.get("GITHUB_SHA") or os.environ.get("HEAVY_REBUILD_BASELINE_SHA")
    if not baseline_commit:
        raise AssertionError("Advancing a target requires GITHUB_SHA or HEAVY_REBUILD_BASELINE_SHA")

    state["baseline_source_commit"] = baseline_commit
    state["active_target"] = next_target
    state["active_target_name"] = name
    state["active_institution"] = institution
    state["active_status"] = "phase_0_donor_audit_ready_baseline_pending_render"
    state["active_dossier"] = f"old_world_narrative/reviews/heavy_rebuild/{next_target}_RESTART_DOSSIER.md"
    state["active_target_passes"] = _fresh_pass_state(list(state["pass_order"]))
    state["planning_records"] = {
        "restart_dossier": state["active_dossier"],
    }
    state["visual_review_gates"] = _fresh_visual_gates(next_target)

    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(
        f"Advanced heavy rebuild from completed {active} to {next_target} — {name}; "
        f"Phase-0 baseline frozen at {baseline_commit}."
    )


if __name__ == "__main__":
    main()
