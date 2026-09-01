#!/usr/bin/env python3
"""[SYSTEM REPORT] OWS-003 Gate-C review revision r2.

r1 correctly rejected its own proof-route check because the asserted rectangular
clear volume included the legitimate batch-record lectern at x=49,z=12. The real
proof route is a clear office aisle along z=11 followed by a short approach from
x=52 to the west-facing chest at x=53,z=12. r2 preserves all r1 D0/D1/D3 geometry
and changes only that review assertion. It remains review-only.
"""
from __future__ import annotations

import json
import os

import render_ows003_gate_c_damage_states as r1
from render_old_world_heavy_rebuild_review import OUTPUT_ROOT, ROOT

OUTPUT_DIR = OUTPUT_ROOT / "OWS-003" / "gate_c_damage_states" / "r2"
STATE_PATH = ROOT / "dev/old_world_narrative" / "registry" / "heavy_rebuild_state.json"


def _assert_d3_routes_r2(t) -> None:
    b = r1.gate_b_base
    b._assert_door(t, 39, 2, 4, "D3 front staff entrance west leaf", block_name="minecraft:dark_oak_door")
    b._assert_door(t, 40, 2, 4, "D3 front staff entrance east leaf", block_name="minecraft:dark_oak_door")
    b._assert_door(t, 43, 2, 10, "D3 batch/licensing office door")
    # Real approach: enter the records office, follow the clear z=11 aisle past
    # the legitimate batch lectern at x=49,z=12, then turn one block south at x=52.
    b._assert_clear(t, (44, 2, 11), (53, 3, 11), "D3 batch/licensing office aisle")
    b._assert_clear(t, (50, 2, 12), (52, 3, 12), "D3 final proof-chest approach")
    b._assert_clear(t, (36, 2, 18), (38, 4, 42), "D3 conditioned operations spine")
    b._assert_clear(t, (29, 2, 21), (31, 4, 33), "D3 cold-vault center aisle")
    b._assert_clear(t, (40, 2, 22), (44, 4, 25), "D3 nursery-1 service area")
    b._assert_clear(t, (40, 2, 27), (44, 4, 30), "D3 nursery-2 service area")
    b._assert_clear(t, (49, 2, 23), (53, 4, 27), "D3 receiving freight lane")
    b._assert_clear(t, (44, 2, 40), (47, 4, 42), "D3 packing-to-dispatch transfer")
    b._assert_door(t, 55, 2, 24, "D3 receiving west leaf")
    b._assert_door(t, 55, 2, 25, "D3 receiving east leaf")
    b._assert_door(t, 46, 2, 43, "D3 dispatch west leaf")
    b._assert_door(t, 47, 2, 43, "D3 dispatch east leaf")
    b._assert_block(t, 54, 18, 36, "minecraft:ladder", "D3 maintenance ladder top")


def main() -> None:
    r1._assert_history_authorized()
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if state.get("active_target") != "OWS-003":
        print(f"Gate-C OWS-003 r2 renderer skipped: active target is {state.get('active_target')}")
        return

    # Review-only assertion repair. Geometry remains exactly r1.
    r1._assert_d3_routes = _assert_d3_routes_r2
    r1.OUTPUT_DIR = OUTPUT_DIR

    d0 = r1.build_d0()
    d1 = r1.build_d1()
    d3 = r1.build_d3()
    d1_changes = r1._diff_count(d0, d1)
    d3_changes = r1._diff_count(d0, d3)
    if not (10 <= d1_changes <= 120):
        raise AssertionError(f"D1 must remain a bounded early anomaly; changed_positions={d1_changes}")
    if d3_changes < 180:
        raise AssertionError(f"D3 is too visually/structurally close to D0; changed_positions={d3_changes}")
    if d3_changes <= d1_changes * 2:
        raise AssertionError(f"D3 must be materially stronger than D1: D1={d1_changes}, D3={d3_changes}")

    revision = os.environ.get("GITHUB_SHA", "local")[:8]
    camera_set = state.get("visual_review_gates", {}).get("gate_c_damage_states", {}).get("fixed_camera_set", "ows003_fixed_v1")
    manifests = {
        "D0": r1._render_state("d0", "D0 intact / normal operation", d0, f"gate-c-r2@{revision}", camera_set),
        "D1": r1._render_state("d1", "D1 early seal/gasket anomaly", d1, f"gate-c-r2@{revision}", camera_set),
        "D3": r1._render_state("d3", "D3 centuries-later causal ruin", d3, f"gate-c-r2@{revision}", camera_set),
    }

    gate_manifest = {
        "target": "OWS-003",
        "gate": "gate_c_damage_states",
        "revision": f"gate-c-r2@{revision}",
        "fixed_camera_set": camera_set,
        "source_d0": "render_ows003_gate_b_intact_r7.build_gate_b_intact_r7",
        "geometry_source": "r1 D0/D1/D3 geometry; r2 corrects proof-route assertion only",
        "d1_changed_positions_from_d0": d1_changes,
        "d3_changed_positions_from_d0": d3_changes,
        "proof_position": list(r1.PROOF_POS),
        "proof_loot_table": r1.PROOF_LOOT_TABLE,
        "deterministic_spawners_d3": 2,
        "darknet_return_hook": "reserved_not_activated",
        "visual_review_status": "rendered_pending_manual_review",
        "states": {key: value["views"] for key, value in manifests.items()},
    }
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "gate_c_manifest.json").write_text(json.dumps(gate_manifest, indent=2) + "\n", encoding="utf-8")

    state["active_status"] = "gate_c_r2_rendered_pending_review"
    for key in (
        "historical_layering",
        "environmental_narrative",
        "encounter_architecture",
        "loot_architecture",
        "quest_proof",
        "damage_and_decay",
    ):
        state["active_target_passes"][key] = "implemented_gate_c_r2_pending_review"
    state["active_target_passes"]["visual_gate_b_intact_state"] = "passed_r7"
    for key in (
        "structural_system",
        "circulation_and_access",
        "exterior_architecture",
        "interior_architecture",
        "operational_systems",
        "institutional_identity",
    ):
        state["active_target_passes"][key] = "complete_gate_b_r7"
    state["active_target_passes"]["visual_gate_c_damage_states"] = "r2_rendered_pending_manual_review"

    gate_b_state = state["visual_review_gates"]["gate_b_intact_state"]
    gate_b_state["status"] = "passed_r7"
    gate_b_state["decision"] = "PASSED"
    gate_b_state["review_record"] = "old_world_narrative/reviews/heavy_rebuild/OWS-003_GATE_B_R7_REVIEW.md"
    gate_b_state["significant_findings_corrected_or_justified"] = True

    gate = state["visual_review_gates"]["gate_c_damage_states"]
    gate["status"] = "r2_rendered_pending_manual_review"
    gate["r1_implementation_failure"] = "proof-office rectangular clearance assertion incorrectly included legitimate batch lectern at x=49,z=12"
    gate["r2_artifact_manifest"] = str((OUTPUT_DIR / "gate_c_manifest.json").relative_to(ROOT)).replace("\\", "/")
    gate["review_stage_source"] = "scripts/render_ows003_gate_c_damage_states_r2.py"
    gate["review_only"] = True
    state["visual_review_gates"]["gate_c_damage_states"] = gate
    state.setdefault("planning_records", {}).update({
        "gate_b_r7_review": "old_world_narrative/reviews/heavy_rebuild/OWS-003_GATE_B_R7_REVIEW.md",
        "pass_13_historical_layering": "old_world_narrative/reviews/heavy_rebuild/OWS-003_PASS13_HISTORICAL_LAYERING.md",
        "pass_14_environmental_narrative": "old_world_narrative/reviews/heavy_rebuild/OWS-003_PASS14_ENVIRONMENTAL_NARRATIVE.md",
        "pass_15_encounter_architecture": "old_world_narrative/reviews/heavy_rebuild/OWS-003_PASS15_ENCOUNTER_ARCHITECTURE.md",
        "pass_16_loot_architecture": "old_world_narrative/reviews/heavy_rebuild/OWS-003_PASS16_LOOT_ARCHITECTURE.md",
        "pass_17_quest_proof": "old_world_narrative/reviews/heavy_rebuild/OWS-003_PASS17_QUEST_PROOF_ARCHITECTURE.md",
        "pass_18_damage_and_decay": "old_world_narrative/reviews/heavy_rebuild/OWS-003_PASS18_DAMAGE_AND_DECAY.md",
    })
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Rendered OWS-003 Gate C r2: D1 changes={d1_changes}, D3 changes={d3_changes}; manual review remains pending.")


if __name__ == "__main__":
    main()
