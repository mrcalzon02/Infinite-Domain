#!/usr/bin/env python3
"""[SYSTEM REPORT] OWS-004 Gate-C damage-state review revision r3.

r2 correctly moved the environmental-riser guard to the accepted Gate-B r4
x44/z18 service edge, but still checked freight at the obsolete x42 coordinate.
Gate-B r3/r4 explicitly preserve freight casing at x44/z27. r3 changes only this
remaining stale topology assertion; D0/D1/D3 geometry and r2 proof-access checks
are frozen. Manual image review remains mandatory.
"""
from __future__ import annotations

import json
import os

import render_ows004_gate_c_damage_states as r1
import render_ows004_gate_c_damage_states_r2 as r2
from render_old_world_heavy_rebuild_review import OUTPUT_ROOT, ROOT

STATE_PATH = ROOT / "old_world_narrative" / "registry" / "heavy_rebuild_state.json"
OUTPUT_DIR = OUTPUT_ROOT / "OWS-004" / "gate_c_damage_states" / "r3"


def _assert_vertical_routes_r3(t) -> None:
    for y in range(9, 39):
        if r1._name(t, (8, y, 30)) != "minecraft:ladder":
            raise AssertionError(f"OWS-004 west secondary-egress ladder gap at y={y}")

    _d0, expected_treads, landing_points = r1.gate_b.build_gate_b_intact_r4()
    for point in expected_treads:
        if r1._name(t, point) != "minecraft:stone_brick_stairs":
            raise AssertionError(f"OWS-004 staff stair lost tread at {point}: {r1._name(t, point)}")
        x, y, z = point
        for head_y in (y + 1, y + 2):
            if r1._name(t, (x, head_y, z)) not in r1.AIR:
                raise AssertionError(f"OWS-004 staff stair headroom blocked at {(x, head_y, z)}")
    for point in landing_points:
        if r1._name(t, point) != "minecraft:polished_andesite":
            raise AssertionError(f"OWS-004 staff stair dogleg landing lost at {point}")

    for level in r1.LEVELS:
        if r1._name(t, (44, level + 2, 27)) != "create:andesite_casing":
            raise AssertionError(f"OWS-004 freight/material core lost at level {level}")
        if r1._name(t, (44, level, 18)) != "create:fluid_pipe":
            raise AssertionError(
                f"OWS-004 r4 environmental riser lost at production level {level}: "
                f"{r1._name(t, (44, level, 18))}"
            )


def build_d0():
    return r2.build_d0()


def build_d1():
    original = r2._assert_vertical_routes_r4
    r2._assert_vertical_routes_r4 = _assert_vertical_routes_r3
    try:
        return r2.build_d1()
    finally:
        r2._assert_vertical_routes_r4 = original


def build_d3():
    original = r2._assert_vertical_routes_r4
    r2._assert_vertical_routes_r4 = _assert_vertical_routes_r3
    try:
        return r2.build_d3()
    finally:
        r2._assert_vertical_routes_r4 = original


def main() -> None:
    r1._assert_history_authorized()
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if state.get("active_target") != "OWS-004":
        print(f"Gate-C OWS-004 r3 renderer skipped: active target is {state.get('active_target')}")
        return
    gate = state.get("visual_review_gates", {}).get("gate_c_damage_states", {})
    if gate.get("status") not in {"ready_for_damage_implementation", "ready_to_render", "rerender_required"}:
        print(f"Gate-C OWS-004 r3 renderer skipped: status={gate.get('status')}")
        return

    r2.OUTPUT_DIR = OUTPUT_DIR
    d0, d1, d3 = build_d0(), build_d1(), build_d3()
    d1_changes = r1._diff_count(d0, d1)
    d3_changes = r1._diff_count(d0, d3)
    if d1_changes < 35:
        raise AssertionError(f"OWS-004 D1 containment is too weak to review: changed_positions={d1_changes}")
    if d3_changes < 180:
        raise AssertionError(f"OWS-004 D3 long-term ruin is too weak to review: changed_positions={d3_changes}")
    if d3_changes <= d1_changes * 2:
        raise AssertionError(f"OWS-004 D3 must be materially stronger than D1: D1={d1_changes}, D3={d3_changes}")

    revision = os.environ.get("GITHUB_SHA", "local")[:8]
    camera_set = gate.get("fixed_camera_set", "ows004_fixed_v1")
    manifests = {
        "D0": r2._render_state("d0", "D0 intact / normal industrial agriculture", d0, f"gate-c-r3@{revision}", camera_set),
        "D1": r2._render_state("d1", "D1 localized active containment", d1, f"gate-c-r3@{revision}", camera_set),
        "D3": r2._render_state("d3", "D3 centuries-later causal ruin", d3, f"gate-c-r3@{revision}", camera_set),
    }
    gate_manifest = {
        "target": "OWS-004",
        "gate": "gate_c_damage_states",
        "revision": f"gate-c-r3@{revision}",
        "fixed_camera_set": camera_set,
        "source_d0": "render_ows004_gate_b_intact_r4.build_gate_b_intact_r4",
        "r1_implementation_failure": "stale pre-r4 environmental-riser coordinate",
        "r2_implementation_failure": "freight guard still checked obsolete x42 coordinate instead of accepted x44 casing",
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

    state["active_status"] = "gate_c_r3_rendered_pending_review"
    for key in ("historical_layering", "environmental_narrative", "encounter_architecture", "loot_architecture", "quest_proof", "damage_and_decay"):
        state["active_target_passes"][key] = "implemented_gate_c_r3_pending_review"
    state["active_target_passes"]["visual_gate_c_damage_states"] = "r3_rendered_pending_manual_review"
    gate["status"] = "r3_rendered_pending_manual_review"
    gate["r1_implementation_failure"] = gate_manifest["r1_implementation_failure"]
    gate["r2_implementation_failure"] = gate_manifest["r2_implementation_failure"]
    gate["r3_artifact_manifest"] = str((OUTPUT_DIR / "gate_c_manifest.json").relative_to(ROOT)).replace("\\", "/")
    gate["review_stage_source"] = "scripts/render_ows004_gate_c_damage_states_r3.py"
    gate["review_only"] = True
    state["visual_review_gates"]["gate_c_damage_states"] = gate
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Rendered OWS-004 Gate C r3: D1 changes={d1_changes}, D3 changes={d3_changes}; manual visual review remains pending.")


if __name__ == "__main__":
    main()
