#!/usr/bin/env python3
"""[SYSTEM REPORT] OWS-003 Gate-C review revision r3.

Gate-C r2 accepted D0 and D1 but rejected D3 as visually too pristine after
centuries of abandonment. r3 freezes D0/D1 and strengthens D3 only through causal
roof-service, receiving, dispatch and wet-zone decay. It preserves the proof route,
major circulation, cold-chain evidence and overall silhouette. Review-only.
"""
from __future__ import annotations

import json
import os

import render_ows003_gate_c_damage_states_r2 as r2
from render_old_world_heavy_rebuild_review import OUTPUT_ROOT, ROOT

r1 = r2.r1
OUTPUT_DIR = OUTPUT_ROOT / "OWS-003" / "gate_c_damage_states" / "r3"
STATE_PATH = ROOT / "dev/old_world_narrative" / "registry" / "heavy_rebuild_state.json"


def build_d3_r3():
    # Preserve the r2 proof-route correction while using the already-accepted r2
    # D3 geometry as the starting point.
    r1._assert_d3_routes = r2._assert_d3_routes_r2
    t = r1.build_d3()

    # ------------------------------------------------------------------
    # East receiving: prolonged weather exposure at the upper service facade.
    # Keep the two working freight doors and floor route completely intact.
    # ------------------------------------------------------------------
    t.clear((55, 9, 27), (55, 12, 29))
    t.fill((55, 8, 26), (55, 8, 30), "minecraft:cracked_stone_bricks")
    t.set(55, 7, 29, "minecraft:mossy_stone_bricks")
    t.set(56, 1, 29, "minecraft:gravel")
    t.set(57, 1, 30, "minecraft:coarse_dirt")

    # ------------------------------------------------------------------
    # South dispatch: canopy and upper wall decay around, not through, the doors.
    # ------------------------------------------------------------------
    t.clear((49, 6, 43), (52, 8, 43))
    t.clear((50, 8, 44), (52, 8, 47))
    t.fill((48, 5, 43), (48, 8, 43), "minecraft:cracked_stone_bricks")
    t.set(53, 6, 43, "minecraft:mossy_stone_bricks")
    t.fill((49, 1, 39), (53, 1, 42), "minecraft:cracked_stone_bricks")

    # ------------------------------------------------------------------
    # Roof refrigeration deck: a second localized edge failure makes the plant
    # read as abandoned infrastructure rather than simply missing machinery.
    # ------------------------------------------------------------------
    t.clear((32, 18, 24), (35, 18, 26))
    t.clear((36, 19, 30), (39, 19, 30))
    t.clear((45, 18, 31), (45, 20, 34))
    t.set(34, 17, 25, "minecraft:gravel")
    t.set(35, 17, 26, "minecraft:mossy_stone_bricks")
    t.set(45, 17, 33, "minecraft:cobweb")

    # A further coherent roof-light failure patch ties the roof chronology to
    # interior wet zones while leaving most of all three strips readable.
    t.clear((28, 17, 25), (30, 17, 29))
    t.clear((37, 17, 22), (39, 17, 24))

    # ------------------------------------------------------------------
    # Wet brick/service bays below the failed roof systems. These are selective
    # material substitutions/holes, not random checkerboard ruin.
    # ------------------------------------------------------------------
    for y in range(9, 13):
        t.set(56, y, 32, "minecraft:cracked_stone_bricks")
        if y in (10, 11):
            t.set(56, y, 38, "minecraft:mossy_stone_bricks")
    t.clear((56, 12, 33), (56, 14, 35))
    t.fill((39, 1, 34), (43, 1, 37), "minecraft:mossy_stone_bricks")
    t.fill((28, 1, 24), (31, 1, 29), "minecraft:cracked_stone_bricks")

    # A small rear wall service breach makes long abandonment visible from the
    # rear-right camera while preserving the dispatch opening and hall frame.
    t.clear((41, 10, 43), (43, 12, 43))
    t.set(40, 10, 43, "minecraft:cracked_stone_bricks")
    t.set(44, 11, 43, "minecraft:mossy_stone_bricks")

    # Re-run all protected mechanics after the stronger decay layer.
    r2._assert_d3_routes_r2(t)
    r1._assert_identity(t)
    r1._assert_proof_chest(t)
    if r1._count_block(t, "minecraft:spawner") != 2:
        raise AssertionError("r3 must preserve exactly two optional D3 spawners")
    if r1._count_block(t, "oritech:cooler_block") < 90:
        raise AssertionError("r3 removed too much surviving cold-chain equipment")
    if r1._count_block(t, "create:fluid_pipe") < 55:
        raise AssertionError("r3 removed too much surviving service-pipe evidence")
    return t


def main() -> None:
    r1._assert_history_authorized()
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if state.get("active_target") != "OWS-003":
        print(f"Gate-C OWS-003 r3 renderer skipped: active target is {state.get('active_target')}")
        return

    r1._assert_d3_routes = r2._assert_d3_routes_r2
    r1.OUTPUT_DIR = OUTPUT_DIR
    d0 = r1.build_d0()
    d1 = r1.build_d1()
    d3 = build_d3_r3()
    d1_changes = r1._diff_count(d0, d1)
    d3_changes = r1._diff_count(d0, d3)
    if d1_changes != 19:
        raise AssertionError(f"r3 must preserve accepted D1 exactly; changed_positions={d1_changes}")
    if d3_changes < 550:
        raise AssertionError(f"r3 D3 decay remains too weak by change-density guard: {d3_changes}")
    if d3_changes <= d1_changes * 10:
        raise AssertionError(f"r3 D3 must remain materially stronger than D1: D1={d1_changes}, D3={d3_changes}")

    revision = os.environ.get("GITHUB_SHA", "local")[:8]
    camera_set = state.get("visual_review_gates", {}).get("gate_c_damage_states", {}).get("fixed_camera_set", "ows003_fixed_v1")
    manifests = {
        "D0": r1._render_state("d0", "D0 intact / normal operation", d0, f"gate-c-r3@{revision}", camera_set),
        "D1": r1._render_state("d1", "D1 early seal/gasket anomaly", d1, f"gate-c-r3@{revision}", camera_set),
        "D3": r1._render_state("d3", "D3 centuries-later causal ruin r3", d3, f"gate-c-r3@{revision}", camera_set),
    }

    gate_manifest = {
        "target": "OWS-003",
        "gate": "gate_c_damage_states",
        "revision": f"gate-c-r3@{revision}",
        "fixed_camera_set": camera_set,
        "source_d0": "render_ows003_gate_b_intact_r7.build_gate_b_intact_r7",
        "d0_d1_status": "frozen_from_accepted_r2_inputs",
        "d3_revision_basis": "OWS-003_GATE_C_R2_REVIEW.md",
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

    state["active_status"] = "gate_c_r3_rendered_pending_review"
    for key in (
        "historical_layering",
        "environmental_narrative",
        "encounter_architecture",
        "loot_architecture",
        "quest_proof",
        "damage_and_decay",
    ):
        state["active_target_passes"][key] = "implemented_gate_c_r3_pending_review"
    state["active_target_passes"]["visual_gate_b_intact_state"] = "passed_r7"
    state["active_target_passes"]["visual_gate_c_damage_states"] = "r3_rendered_pending_manual_review"
    gate_b_state = state["visual_review_gates"]["gate_b_intact_state"]
    gate_b_state["status"] = "passed_r7"
    gate_b_state["decision"] = "PASSED"
    gate_b_state["review_record"] = "old_world_narrative/reviews/heavy_rebuild/OWS-003_GATE_B_R7_REVIEW.md"
    gate = state["visual_review_gates"]["gate_c_damage_states"]
    gate["status"] = "r3_rendered_pending_manual_review"
    gate["r2_review_record"] = "old_world_narrative/reviews/heavy_rebuild/OWS-003_GATE_C_R2_REVIEW.md"
    gate["r2_decision"] = "REVISION REQUIRED"
    gate["r3_artifact_manifest"] = str((OUTPUT_DIR / "gate_c_manifest.json").relative_to(ROOT)).replace("\\", "/")
    gate["review_stage_source"] = "scripts/render_ows003_gate_c_damage_states_r3.py"
    gate["review_only"] = True
    state["visual_review_gates"]["gate_c_damage_states"] = gate
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Rendered OWS-003 Gate C r3: D1 changes={d1_changes}, D3 changes={d3_changes}; manual review remains pending.")


if __name__ == "__main__":
    main()
