#!/usr/bin/env python3
"""[SYSTEM REPORT] OWS-003 Gate-B intact review revision r4.

r3 repaired the maintenance-sign support and then exposed a deeper intact-state
conflict: retained cannery steel posts at x=31,z=26/32 occupied the cold-vault
center aisle. r4 preserves the accepted Gate-A shell, r2 process boundaries and
r3 plant-access repair, but converts those two low steel posts into transfer
frames above the inserted cold room so the three-block service aisle is real.
It remains review-only and introduces no historical damage, encounters or proof.
"""
from __future__ import annotations

import json
import os

import generate_wasteland_sites as base
import render_ows003_gate_b_intact as r1
import render_ows003_gate_b_intact_r2 as r2
import render_ows003_gate_b_intact_r3 as r3
from render_old_world_heavy_rebuild_review import OUTPUT_ROOT, ROOT, render_review_set
from render_structure_review import unpack_structure

STATE_PATH = ROOT / "old_world_narrative" / "registry" / "heavy_rebuild_state.json"
TEMP_NAME = "_heavy_review_ows003_gate_b_intact_r4"
TEMP_NBT = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{TEMP_NAME}.nbt"
OUTPUT_DIR = OUTPUT_ROOT / "OWS-003" / "gate_b_intact" / "r4"


def _repair_cold_vault_structural_aisle(t: base.Template) -> None:
    """Transfer retained cannery frame loads around the inserted vault aisle."""
    for z in (26, 32):
        # Remove only the lower portion of the inherited x=31 post that occupies
        # the protected center aisle. Upper roof framing remains intact.
        t.clear((31, 2, z), (31, 8, z))
        # Express a transfer frame at the top of the inserted cold-room envelope.
        # Side jambs align to the room edges and the header bridges the clear aisle.
        t.fill((25, 2, z), (25, 9, z), "tfmg:steel_block")
        t.fill((35, 2, z), (35, 9, z), "tfmg:steel_block")
        t.fill((25, 9, z), (35, 9, z), "tfmg:steel_block")


def build_gate_b_intact_r4() -> base.Template:
    t = r3.build_gate_b_intact_r3()
    _repair_cold_vault_structural_aisle(t)
    return t


def _assert_r4_repairs(t: base.Template) -> None:
    r3._assert_r3_repairs(t)
    r1._assert_clear(t, (29, 2, 21), (31, 4, 33), "r4 cold-vault center aisle")
    for z in (26, 32):
        r1._assert_block(t, 31, 9, z, "tfmg:steel_block", f"cold-vault transfer header z={z}")
        r1._assert_block(t, 25, 9, z, "tfmg:steel_block", f"cold-vault transfer west jamb z={z}")
        r1._assert_block(t, 35, 9, z, "tfmg:steel_block", f"cold-vault transfer east jamb z={z}")


def main() -> None:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if state.get("active_target") != "OWS-003":
        print(f"Gate-B OWS-003 r4 renderer skipped: active target is {state.get('active_target')}")
        return

    gate = state.get("visual_review_gates", {}).get("gate_b_intact_state", {})
    status = gate.get("status", "not_started")
    if status not in {"ready_for_intact_implementation", "ready_to_render", "rerender_required"}:
        print(f"Gate-B OWS-003 r4 renderer skipped: status={status}")
        return

    t = build_gate_b_intact_r4()
    r1._assert_intact_contracts(t)
    _assert_r4_repairs(t)
    base.stabilize_door_pairs(t)
    r1._assert_intact_contracts(t)
    _assert_r4_repairs(t)

    t.save(TEMP_NAME)
    try:
        size, blocks = unpack_structure(TEMP_NBT)
        revision = os.environ.get("GITHUB_SHA", "local")[:8]
        manifest = render_review_set(
            target="OWS-003",
            gate="gate_b_intact",
            revision=f"intact-r4@{revision}",
            damage_state="D0 intact / operational",
            source_commit=os.environ.get("GITHUB_SHA", "working-tree"),
            source_path="review-only:render_ows003_gate_b_intact_r4.build_gate_b_intact_r4()",
            size=size,
            blocks=blocks,
            output_dir=OUTPUT_DIR,
            camera_set=gate.get("fixed_camera_set", "ows003_fixed_v1"),
        )
    finally:
        TEMP_NBT.unlink(missing_ok=True)

    failure_path = ROOT / "old_world_narrative" / "reviews" / "heavy_rebuild" / "OWS-003_GATE_B_FAILURE.log"
    failure_path.unlink(missing_ok=True)

    state["active_status"] = "gate_b_r4_intact_rendered_pending_review"
    for key in (
        "structural_system",
        "circulation_and_access",
        "exterior_architecture",
        "interior_architecture",
        "operational_systems",
        "institutional_identity",
    ):
        state["active_target_passes"][key] = "r4_implemented_pending_gate_b_review"
    state["active_target_passes"]["visual_gate_b_intact_state"] = "r4_rendered_pending_manual_review"
    gate["status"] = "r4_rendered_pending_manual_review"
    gate["r1_implementation_failure"] = "missing controlled boundaries/support walls at release, packing and outbound staging"
    gate["r2_implementation_failure"] = "maintenance plant-access sign had no physical support wall above the service entrance"
    gate["r3_implementation_failure"] = "retained cannery steel posts obstructed the protected cold-vault center aisle"
    gate["r4_artifact_manifest"] = str((OUTPUT_DIR / "review_manifest.json").relative_to(ROOT)).replace("\\", "/")
    gate["review_stage_source"] = "scripts/render_ows003_gate_b_intact_r4.py"
    gate["review_only"] = True
    state["visual_review_gates"]["gate_b_intact_state"] = gate
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")

    print(
        f"Rendered OWS-003 Gate B r4 intact review at {manifest['dimensions']} using "
        f"{manifest['fixed_camera_set']}; manual intact-state approval remains pending."
    )


if __name__ == "__main__":
    main()
