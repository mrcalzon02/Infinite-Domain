#!/usr/bin/env python3
"""[SYSTEM REPORT] OWS-004 Gate-C damage-state review revision r2.

r1 was rejected before rendering because its vertical-route assertion checked the
obsolete pre-r4 environmental-riser coordinate inside the new staff-stair core.
r2 preserves the authored D0/D1/D3 history and damage model, but validates the
actual Gate-B r4 service anatomy: freight remains south in the east core and the
rerouted environmental riser remains on the protected far-east x44/z18 edge.
"""
from __future__ import annotations

import json
import os

import generate_wasteland_sites as base
import render_ows004_gate_b_intact as gate_b_base
import render_ows004_gate_b_intact_r4 as gate_b
import render_ows004_gate_c_damage_states as r1
from render_old_world_heavy_rebuild_review import OUTPUT_ROOT, ROOT, render_review_set
from render_structure_review import unpack_structure

STATE_PATH = ROOT / "old_world_narrative" / "registry" / "heavy_rebuild_state.json"
OUTPUT_DIR = OUTPUT_ROOT / "OWS-004" / "gate_c_damage_states" / "r2"
AIR = r1.AIR


def _assert_vertical_routes_r4(t: base.Template) -> None:
    # West secondary egress remains continuous.
    for y in range(9, 39):
        if r1._name(t, (8, y, 30)) != "minecraft:ladder":
            raise AssertionError(f"OWS-004 west secondary-egress ladder gap at y={y}")

    # Preserve every accepted primary-stair tread and intentional dogleg landing.
    _d0, expected_treads, landing_points = gate_b.build_gate_b_intact_r4()
    for point in expected_treads:
        if r1._name(t, point) != "minecraft:stone_brick_stairs":
            raise AssertionError(f"OWS-004 staff stair lost tread at {point}: {r1._name(t, point)}")
        x, y, z = point
        for head_y in (y + 1, y + 2):
            if r1._name(t, (x, head_y, z)) not in AIR:
                raise AssertionError(f"OWS-004 staff stair headroom blocked at {(x, head_y, z)}")
    for point in landing_points:
        if r1._name(t, point) != "minecraft:polished_andesite":
            raise AssertionError(f"OWS-004 staff stair dogleg landing lost at {point}")

    # Freight/material transfer stays in the south half of the east core.
    for level in gate_b_base.LEVELS:
        if r1._name(t, (42, level + 1, 27)) != "create:andesite_casing":
            raise AssertionError(f"OWS-004 freight/material core lost at level {level}")

    # Gate-B r4 rerouted the environmental riser around the new staff stair to
    # x44/z18. D3 may break an upper branch downstream, but this main riser line
    # must remain readable at every production-floor elevation.
    for level in gate_b_base.LEVELS:
        if r1._name(t, (44, level, 18)) != "create:fluid_pipe":
            raise AssertionError(
                f"OWS-004 r4 environmental riser lost at production level {level}: "
                f"{r1._name(t, (44, level, 18))}"
            )


def _assert_proof_access(t: base.Template) -> None:
    # The front double doors survive D3.
    for x in (20, 21):
        if r1._name(t, (x, 2, 6)) != "minecraft:iron_door":
            raise AssertionError(f"OWS-004 D3 front public entrance lost at {(x, 2, 6)}")

    # Records-room partition door from the intact podium remains usable.
    if r1._name(t, (29, 2, 11)) != "minecraft:spruce_door":
        raise AssertionError("OWS-004 D3 staff-control records doorway was lost")

    # Keep a broad approach from the public hall to the records doorway. The
    # proof chest is beyond this threshold at the normal staff-control node.
    for x in range(22, 29):
        for z in (11, 12):
            for y in (2, 3):
                if r1._name(t, (x, y, z)) not in AIR:
                    raise AssertionError(
                        f"OWS-004 D3 proof approach blocked at {(x, y, z)} by {r1._name(t, (x, y, z))}"
                    )


def build_d0() -> base.Template:
    return r1.build_d0()


def build_d1() -> base.Template:
    # Replace only the stale r1 assertion; the D1 implementation itself remains
    # exactly the authored localized Cultivation-04 containment state.
    original = r1._assert_vertical_routes
    r1._assert_vertical_routes = _assert_vertical_routes_r4
    try:
        return r1.build_d1()
    finally:
        r1._assert_vertical_routes = original


def build_d3() -> base.Template:
    original = r1._assert_vertical_routes
    r1._assert_vertical_routes = _assert_vertical_routes_r4
    try:
        t = r1.build_d3()
    finally:
        r1._assert_vertical_routes = original
    _assert_proof_access(t)
    return t


def _render_state(label: str, damage_state: str, t: base.Template, revision: str, camera_set: str) -> dict:
    temp_name = f"_heavy_review_ows004_gate_c_{label}_r2"
    temp_nbt = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{temp_name}.nbt"
    t.save(temp_name)
    try:
        size, blocks = unpack_structure(temp_nbt)
        return render_review_set(
            target="OWS-004",
            gate="gate_c_damage_states",
            revision=revision,
            damage_state=damage_state,
            source_commit=os.environ.get("GITHUB_SHA", "working-tree"),
            source_path=f"review-only:render_ows004_gate_c_damage_states_r2.build_{label}()",
            size=size,
            blocks=blocks,
            output_dir=OUTPUT_DIR / label,
            camera_set=camera_set,
        )
    finally:
        temp_nbt.unlink(missing_ok=True)


def main() -> None:
    r1._assert_history_authorized()
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if state.get("active_target") != "OWS-004":
        print(f"Gate-C OWS-004 r2 renderer skipped: active target is {state.get('active_target')}")
        return
    gate = state.get("visual_review_gates", {}).get("gate_c_damage_states", {})
    if gate.get("status") not in {
        "ready_for_damage_implementation",
        "ready_to_render",
        "rerender_required",
    }:
        print(f"Gate-C OWS-004 r2 renderer skipped: status={gate.get('status')}")
        return

    d0 = build_d0()
    d1 = build_d1()
    d3 = build_d3()
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
        "D0": _render_state("d0", "D0 intact / normal industrial agriculture", d0, f"gate-c-r2@{revision}", camera_set),
        "D1": _render_state("d1", "D1 localized active containment", d1, f"gate-c-r2@{revision}", camera_set),
        "D3": _render_state("d3", "D3 centuries-later causal ruin", d3, f"gate-c-r2@{revision}", camera_set),
    }

    gate_manifest = {
        "target": "OWS-004",
        "gate": "gate_c_damage_states",
        "revision": f"gate-c-r2@{revision}",
        "fixed_camera_set": camera_set,
        "source_d0": "render_ows004_gate_b_intact_r4.build_gate_b_intact_r4",
        "r1_implementation_failure": "vertical-route assertion checked obsolete pre-r4 environmental-riser coordinate x42/z19 inside the new staff stair",
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
    state["active_target_passes"]["visual_gate_c_damage_states"] = "r2_rendered_pending_manual_review"
    gate["status"] = "r2_rendered_pending_manual_review"
    gate["r1_implementation_failure"] = gate_manifest["r1_implementation_failure"]
    gate["r2_artifact_manifest"] = str((OUTPUT_DIR / "gate_c_manifest.json").relative_to(ROOT)).replace("\\", "/")
    gate["review_stage_source"] = "scripts/render_ows004_gate_c_damage_states_r2.py"
    gate["review_only"] = True
    state["visual_review_gates"]["gate_c_damage_states"] = gate
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Rendered OWS-004 Gate C r2: D1 changes={d1_changes}, D3 changes={d3_changes}; manual visual review remains pending.")


if __name__ == "__main__":
    main()
