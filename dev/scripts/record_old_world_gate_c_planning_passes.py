#!/usr/bin/env python3
"""[SYSTEM REPORT] Verify completed Passes 13-18 and open active Gate C.

This utility does no visual judgment and creates no history itself. It verifies
that Gate B is already passed and that the six narrative/encounter/loot/proof/
damage planning records for the active target contain their explicit completion
markers. It then opens Gate-C implementation only if Gate C has not already
advanced farther. State transitions are monotonic.

When Gate B is still pending, revision-required, or awaiting manual review, this
recorder returns without mutation so the visual-review workflow can proceed to
the unresolved Gate-B renderer instead of failing before that gate is produced.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STATE_PATH = ROOT / "dev/old_world_narrative" / "registry" / "heavy_rebuild_state.json"

PASS_FILES = {
    "historical_layering": ("PASS13_HISTORICAL_LAYERING", "**HISTORICAL LAYERING: COMPLETE FOR GATE-C IMPLEMENTATION.**"),
    "environmental_narrative": ("PASS14_ENVIRONMENTAL_NARRATIVE", "**ENVIRONMENTAL NARRATIVE: COMPLETE FOR GATE-C IMPLEMENTATION.**"),
    "encounter_architecture": ("PASS15_ENCOUNTER_ARCHITECTURE", "**ENCOUNTER ARCHITECTURE: COMPLETE FOR GATE-C IMPLEMENTATION.**"),
    "loot_architecture": ("PASS16_LOOT_ARCHITECTURE", "**LOOT ARCHITECTURE: COMPLETE FOR GATE-C IMPLEMENTATION.**"),
    "quest_proof": ("PASS17_QUEST_PROOF_ARCHITECTURE", "**QUEST-PROOF ARCHITECTURE: COMPLETE FOR GATE-C IMPLEMENTATION.**"),
    "damage_and_decay": ("PASS18_DAMAGE_AND_DECAY", "**DAMAGE AND DECAY: COMPLETE FOR GATE-C IMPLEMENTATION.**"),
}

OPENABLE_GATE_C_STATES = {
    "blocked_by_gate_b_and_history_passes",
    "blocked_by_passes_13_18",
    "pending",
    "ready_for_damage_implementation",
    "ready_to_render",
}


def _resolve_record(target: str, stem: str) -> tuple[str, Path]:
    rel = f"dev/old_world_narrative/reviews/heavy_rebuild/{target}_{stem}.md"
    path = ROOT / rel
    if not path.is_file():
        raise AssertionError(f"Missing {target} Gate-C planning record: {rel}")
    return rel, path


def main() -> None:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    target = state.get("active_target")
    if not target:
        raise AssertionError("Heavy-rebuild state has no active target")

    gate_b = state.get("visual_review_gates", {}).get("gate_b_intact_state", {})
    gate_b_status = str(gate_b.get("status", ""))
    if not gate_b_status.startswith("passed_"):
        print(f"{target} Gate-C planning recorder skipped: Gate B status={gate_b_status!r}")
        return

    records = state.setdefault("planning_records", {})
    for pass_key, (stem, marker) in PASS_FILES.items():
        rel, path = _resolve_record(target, stem)
        text = path.read_text(encoding="utf-8")
        if marker not in text:
            raise AssertionError(f"{target} Gate-C planning record lacks marker {marker}: {rel}")
        records[pass_key] = rel

    gate_c = state["visual_review_gates"]["gate_c_damage_states"]
    current = str(gate_c.get("status", ""))
    if current not in OPENABLE_GATE_C_STATES:
        STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")
        print(f"Verified {target} Passes 13-18; preserved advanced Gate-C state {current!r}.")
        return

    passes = state["active_target_passes"]
    for key in PASS_FILES:
        value = str(passes.get(key, "pending"))
        if value in {"pending", "ready", "defined_ready_for_gate_c_implementation"}:
            passes[key] = "defined_ready_for_gate_c_implementation"
    visual = str(passes.get("visual_gate_c_damage_states", "pending"))
    if visual in {"pending", "ready", "ready_for_damage_implementation"}:
        passes["visual_gate_c_damage_states"] = "ready_for_damage_implementation"

    gate_c["status"] = "ready_for_damage_implementation"
    gate_c["rule"] = (
        "D0 must exactly preserve the accepted intact Gate-B model; D1 must express the approved localized historical intervention; "
        "D3 must express causal long-term ruin while retaining proof, circulation, institutional identity and reconstructable operations."
    )
    state["visual_review_gates"]["gate_c_damage_states"] = gate_c
    if not str(state.get("active_status", "")).startswith(("gate_c_r", "gate_d_", "peak_quality_")):
        state["active_status"] = "gate_c_damage_states_ready_to_implement"

    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Verified {target} Passes 13-18 complete; Gate-C damage-state implementation is ready.")


if __name__ == "__main__":
    main()
