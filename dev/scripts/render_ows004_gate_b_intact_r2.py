#!/usr/bin/env python3
"""[SYSTEM REPORT] OWS-004 Gate-B intact review revision r2.

r1 built the intended intact operating tower but its landing slabs overwrote the
continuous west-egress ladder at each production level. CI proved the first gap at
Y9 before rendering. r2 changes only that implementation sequencing: it restores
the ladder/hatch column after all landings are built, then re-runs the complete r1
intact contract. No architecture, history, loot, encounter or damage layer changes.
"""
from __future__ import annotations

import json
import os

import render_ows004_gate_b_intact as r1
from render_old_world_heavy_rebuild_review import OUTPUT_ROOT, ROOT, render_review_set
from render_structure_review import unpack_structure

STATE_PATH = ROOT / "dev/old_world_narrative" / "registry" / "heavy_rebuild_state.json"
TEMP_NAME = "_heavy_review_ows004_gate_b_intact_r2"
TEMP_NBT = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{TEMP_NAME}.nbt"
OUTPUT_DIR = OUTPUT_ROOT / "OWS-004" / "gate_b_intact" / "r2"


def _restore_egress_ladder(t) -> None:
    """Restore the through-floor ladder after r1 creates landing slabs."""
    for y in range(9, 39):
        t.set(8, y, 30, "minecraft:ladder", facing="north", waterlogged="false")


def build_gate_b_intact_r2():
    t = r1.build_gate_b_intact()
    _restore_egress_ladder(t)
    r1._assert_intact_contracts(t)
    return t


def main() -> None:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if state.get("active_target") != "OWS-004":
        print(f"Gate-B OWS-004 r2 renderer skipped: active target is {state.get('active_target')}")
        return

    gate = state.get("visual_review_gates", {}).get("gate_b_intact_state", {})
    status = gate.get("status", "not_started")
    if status not in {"ready_for_intact_implementation", "ready_to_render", "rerender_required"}:
        print(f"Gate-B OWS-004 r2 renderer skipped: status={status}")
        return

    t = build_gate_b_intact_r2()
    if tuple(t.size) != (51, 47, 47):
        raise AssertionError(f"OWS-004 Gate-B r2 dimensions changed unexpectedly: {t.size}")

    t.save(TEMP_NAME)
    try:
        size, blocks = unpack_structure(TEMP_NBT)
        revision = os.environ.get("GITHUB_SHA", "local")[:8]
        manifest = render_review_set(
            target="OWS-004",
            gate="gate_b_intact",
            revision=f"intact-r2@{revision}",
            damage_state="D0 intact / operational",
            source_commit=os.environ.get("GITHUB_SHA", "working-tree"),
            source_path="review-only:render_ows004_gate_b_intact_r2.build_gate_b_intact_r2()",
            size=size,
            blocks=blocks,
            output_dir=OUTPUT_DIR,
            camera_set=gate.get("fixed_camera_set", "ows004_fixed_v1"),
        )
    finally:
        TEMP_NBT.unlink(missing_ok=True)

    state["active_status"] = "gate_b_r2_intact_rendered_pending_review"
    for key in (
        "structural_system",
        "circulation_and_access",
        "exterior_architecture",
        "interior_architecture",
        "operational_systems",
        "institutional_identity",
    ):
        state["active_target_passes"][key] = "implemented_gate_b_r2_pending_review"
    state["active_target_passes"]["visual_gate_b_intact_state"] = "r2_rendered_pending_manual_review"
    gate["status"] = "r2_rendered_pending_manual_review"
    gate["r1_implementation_failure"] = "west egress landing slabs overwrote the continuous ladder at production-floor elevations; first CI failure at y=9"
    gate["r2_artifact_manifest"] = str((OUTPUT_DIR / "review_manifest.json").relative_to(ROOT)).replace("\\", "/")
    gate["review_stage_source"] = "scripts/render_ows004_gate_b_intact_r2.py"
    gate["review_only"] = True
    state["visual_review_gates"]["gate_b_intact_state"] = gate
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")

    print(
        f"Rendered OWS-004 Gate B r2 intact review at {manifest['dimensions']} using "
        f"{manifest['fixed_camera_set']}; manual intact-state approval remains pending."
    )


if __name__ == "__main__":
    main()
