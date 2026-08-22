#!/usr/bin/env python3
"""[SYSTEM REPORT] OWS-004 Gate-C damage-state review revision r4.

Manual review accepted r2 D0 and D1 but rejected D3 as visually too pristine for
a centuries-later ruin. r4 freezes D0/D1 and strengthens D3 only. The added decay
is deliberately top-heavy and causal: larger greenhouse/crown failures, visible
upper containment/service breaches, stronger fourth-floor grow-bank loss and a
smaller third-floor wet-service consequence. Protected staff/freight/egress/proof
systems remain intact. Review-only; no visual approval is implied.
"""
from __future__ import annotations

import json
import os

import render_ows004_gate_c_damage_states as r1
import render_ows004_gate_c_damage_states_r3 as r3
from render_old_world_heavy_rebuild_review import OUTPUT_ROOT, ROOT

STATE_PATH = ROOT / "old_world_narrative" / "registry" / "heavy_rebuild_state.json"
OUTPUT_DIR = OUTPUT_ROOT / "OWS-004" / "gate_c_damage_states" / "r4"


def build_d0():
    return r3.build_d0()


def build_d1():
    return r3.build_d1()


def build_d3_r4():
    t = r3.build_d3()

    # ------------------------------------------------------------------
    # Environmental crown: convert the near-continuous cyan cap into clearly
    # surviving and failed greenhouse zones. These are broad coherent failures,
    # not checkerboard erosion.
    # ------------------------------------------------------------------
    # Northwest crown corner / roof skin failure.
    t.clear((13, 44, 17), (20, 46, 24))
    # Southeast crown roof and upper glazing failure.
    t.clear((28, 44, 26), (36, 46, 34))
    # Mid-west roof break creates a second visible weather path into Level 4.
    t.clear((20, 46, 23), (25, 46, 29))

    # Retain fractured edge traces so the original crown envelope remains readable.
    t.fill((13, 43, 17), (18, 43, 17), "minecraft:cracked_stone_bricks")
    t.fill((28, 43, 34), (34, 43, 34), "minecraft:cracked_stone_bricks")
    t.set(20, 43, 18, "minecraft:mossy_stone_bricks")
    t.set(33, 43, 33, "minecraft:mossy_stone_bricks")

    # Exposed crown-service plant: remove a coherent section of header/equipment
    # adjacent to the failed glazing while preserving the main riser history.
    t.clear((16, 44, 17), (25, 44, 19))
    t.clear((30, 44, 17), (36, 44, 19))
    t.clear((37, 40, 32), (39, 43, 34))
    t.set(24, 43, 19, "minecraft:cobweb")
    t.set(35, 42, 19, "minecraft:cobweb")
    t.set(38, 39, 33, "minecraft:gravel")

    # ------------------------------------------------------------------
    # Level 4 containment failure: visible facade/service breaches tie exterior
    # damage directly to the D1 quarantine zone rather than random ruin.
    # ------------------------------------------------------------------
    # North/front upper cultivation facade breach, west of the protected east core.
    t.clear((12, 33, 14), (18, 38, 14))
    t.fill((12, 32, 14), (18, 32, 14), "minecraft:cracked_stone_bricks")
    t.set(13, 33, 15, "minecraft:cobweb")
    t.set(17, 34, 15, "minecraft:mossy_stone_bricks")

    # South/rear upper facade breach around failed environmental branch, still west
    # of the staff/freight core.
    t.clear((30, 33, 36), (37, 38, 36))
    t.fill((30, 32, 36), (37, 32, 36), "minecraft:cracked_stone_bricks")
    t.set(32, 33, 35, "minecraft:cobweb")
    t.set(36, 34, 35, "minecraft:mossy_stone_bricks")

    # Stronger Level-4 rack collapse/spill beneath the crown failures. Preserve the
    # central aisle and eastern people/freight/service core.
    t.clear((14, 31, 18), (20, 34, 24))
    t.fill((14, 30, 18), (20, 30, 24), "minecraft:coarse_dirt")
    for pos in ((15, 31, 19), (17, 31, 21), (19, 31, 23)):
        t.set(*pos, "minecraft:brown_mushroom")
    t.set(18, 31, 20, "minecraft:red_mushroom")
    t.set(20, 31, 24, "minecraft:cobweb")

    # A second failed bank on the rear-west side makes the containment collapse read
    # across multiple floor-slice and exterior cameras without consuming the aisle.
    t.clear((31, 31, 29), (35, 34, 33))
    t.fill((31, 30, 29), (35, 30, 33), "minecraft:mossy_stone_bricks")
    t.set(32, 31, 30, "minecraft:brown_mushroom")
    t.set(34, 31, 32, "minecraft:cobweb")

    # ------------------------------------------------------------------
    # Level 3 consequence: smaller wet/service failure below the upper breach.
    # Lower Levels 1-2 remain comparatively intact to preserve the vertical gradient.
    # ------------------------------------------------------------------
    t.clear((30, 24, 30), (33, 26, 33))
    t.fill((30, 23, 30), (34, 23, 34), "minecraft:mossy_stone_bricks")
    t.set(31, 24, 31, "minecraft:cobweb")
    t.set(33, 24, 33, "minecraft:brown_mushroom")

    # Scars directly beneath failed crown penetrations; sparse and causal.
    t.fill((14, 30, 15), (18, 30, 17), "minecraft:cracked_stone_bricks")
    t.fill((30, 30, 34), (36, 30, 35), "minecraft:mossy_stone_bricks")

    # Reassert all protected mechanics after the stronger D3 layer.
    r3._assert_vertical_routes_r3(t)
    r1._assert_identity(t)
    r1._assert_proof_chest(t)
    r3.r2._assert_proof_access(t)
    if r1._count_block(t, "minecraft:spawner") != 2:
        raise AssertionError("OWS-004 r4 must preserve exactly two optional D3 spawners")
    if r1._count_block(t, "minecraft:mycelium") < 70:
        raise AssertionError("OWS-004 r4 removed too much surviving cultivation evidence")
    if r1._count_block(t, "create:fluid_pipe") < 55:
        raise AssertionError("OWS-004 r4 removed too much surviving environmental-service evidence")
    return t


def main() -> None:
    r1._assert_history_authorized()
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if state.get("active_target") != "OWS-004":
        print(f"Gate-C OWS-004 r4 renderer skipped: active target is {state.get('active_target')}")
        return
    gate = state.get("visual_review_gates", {}).get("gate_c_damage_states", {})
    if gate.get("status") not in {
        "ready_for_damage_implementation",
        "ready_to_render",
        "rerender_required",
        "r2_rendered_pending_manual_review",
        "r3_rendered_pending_manual_review",
    }:
        print(f"Gate-C OWS-004 r4 renderer skipped: status={gate.get('status')}")
        return

    # Freeze accepted D0/D1 exactly from the reviewed r2/r3 geometry.
    d0 = build_d0()
    d1 = build_d1()
    d3 = build_d3_r4()
    d1_changes = r1._diff_count(d0, d1)
    d3_changes = r1._diff_count(d0, d3)
    if d1_changes != 112:
        raise AssertionError(f"OWS-004 r4 must freeze accepted D1 exactly; changed_positions={d1_changes}")
    if d3_changes < 500:
        raise AssertionError(f"OWS-004 r4 D3 remains too weak by change-density guard: {d3_changes}")
    if d3_changes <= d1_changes * 4:
        raise AssertionError(f"OWS-004 r4 D3 must be materially stronger than D1: D1={d1_changes}, D3={d3_changes}")

    revision = os.environ.get("GITHUB_SHA", "local")[:8]
    camera_set = gate.get("fixed_camera_set", "ows004_fixed_v1")
    # Use r2's rendering helper but direct it to r4 output.
    r3.r2.OUTPUT_DIR = OUTPUT_DIR
    manifests = {
        "D0": r3.r2._render_state("d0", "D0 intact / normal industrial agriculture", d0, f"gate-c-r4@{revision}", camera_set),
        "D1": r3.r2._render_state("d1", "D1 localized active containment", d1, f"gate-c-r4@{revision}", camera_set),
        "D3": r3.r2._render_state("d3", "D3 centuries-later causal ruin r4", d3, f"gate-c-r4@{revision}", camera_set),
    }

    gate_manifest = {
        "target": "OWS-004",
        "gate": "gate_c_damage_states",
        "revision": f"gate-c-r4@{revision}",
        "fixed_camera_set": camera_set,
        "source_d0": "render_ows004_gate_b_intact_r4.build_gate_b_intact_r4",
        "d0_d1_status": "frozen_from_accepted_r2_visual_review",
        "d3_revision_basis": "OWS-004_GATE_C_R2_REVIEW.md",
        "d1_changed_positions_from_d0": d1_changes,
        "d3_changed_positions_from_d0": d3_changes,
        "proof_position": list(r1.PROOF_POS),
        "proof_loot_table": r1.PROOF_LOOT_TABLE,
        "deterministic_spawners_d3": 2,
        "visual_review_status": "rendered_pending_manual_review",
        "states": {key: value["views"] for key, value in manifests.items()},
    }
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "gate_c_manifest.json").write_text(json.dumps(gate_manifest, indent=2) + "\n", encoding="utf-8")

    state["active_status"] = "gate_c_r4_rendered_pending_review"
    for key in ("historical_layering", "environmental_narrative", "encounter_architecture", "loot_architecture", "quest_proof", "damage_and_decay"):
        state["active_target_passes"][key] = "implemented_gate_c_r4_pending_review"
    state["active_target_passes"]["visual_gate_c_damage_states"] = "r4_rendered_pending_manual_review"
    gate["status"] = "r4_rendered_pending_manual_review"
    gate["r2_review_record"] = "old_world_narrative/reviews/heavy_rebuild/OWS-004_GATE_C_R2_REVIEW.md"
    gate["r2_decision"] = "REVISION REQUIRED"
    gate["r4_artifact_manifest"] = str((OUTPUT_DIR / "gate_c_manifest.json").relative_to(ROOT)).replace("\\", "/")
    gate["review_stage_source"] = "scripts/render_ows004_gate_c_damage_states_r4.py"
    gate["review_only"] = True
    state["visual_review_gates"]["gate_c_damage_states"] = gate
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Rendered OWS-004 Gate C r4: D1 changes={d1_changes}, D3 changes={d3_changes}; manual visual review remains pending.")


if __name__ == "__main__":
    main()
