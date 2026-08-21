#!/usr/bin/env python3
"""[SYSTEM REPORT] Build and render OWS-001 Gate-A D0 massing review.

This is a review-only intermediate. It does not replace the authoritative OWS-001
builder and it is never placed in worldgen. The purpose is to test the rebuilt
shell, site occupation, entrance hierarchy, service massing, and roof composition
before expensive interior work begins.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import generate_wasteland_sites as base
from render_old_world_heavy_rebuild_review import OUTPUT_ROOT, ROOT, render_review_set
from render_structure_review import unpack_structure


STATE_PATH = ROOT / "old_world_narrative" / "registry" / "heavy_rebuild_state.json"
TEMP_NAME = "_heavy_review_ows001_gate_a_massing_r1"
TEMP_NBT = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{TEMP_NAME}.nbt"
OUTPUT_DIR = OUTPUT_ROOT / "OWS-001" / "gate_a_massing" / "r1"


def build_gate_a_massing() -> base.Template:
    """Construct only the D0 architectural/site masses needed for Gate A."""
    t = base.Template((39, 13, 33))

    # D0 site datum. Keep a compact neighborhood service lot instead of letting
    # the building float in review space. This is deliberately clean/intact.
    t.fill((1, 0, 1), (37, 0, 31), "tfmg:asphalt")
    t.fill((9, 0, 1), (29, 0, 7), "minecraft:smooth_stone")
    t.fill((7, 0, 30), (31, 0, 32), "minecraft:smooth_stone")

    # Central workplace body: ordinary durable neighborhood construction.
    # It remains lower than an institutional campus and acts as the shared
    # circulation/workplace core between the specialized side volumes.
    base.shell(
        t,
        (8, 1, 8),
        (31, 8, 28),
        "minecraft:stone_bricks",
        "minecraft:smooth_stone",
        "minecraft:light_gray_concrete",
    )

    # West returns/sanitation annex: intentionally lower and slightly offset.
    # This gives the dirty-return process its own architectural address so the
    # later D1 quality-hold retrofit can stay local rather than infecting the
    # visual language of the whole building.
    base.shell(
        t,
        (3, 1, 11),
        (12, 7, 24),
        "minecraft:light_gray_concrete",
        "minecraft:smooth_stone",
        "minecraft:white_concrete",
    )

    # East clean cold-chain block: taller service volume under the roof plant.
    # Its extra height is functional rather than monumental and creates a clear
    # clean-vs-return asymmetry in the silhouette.
    base.shell(
        t,
        (27, 1, 10),
        (35, 9, 25),
        "minecraft:white_concrete",
        "minecraft:smooth_stone",
        "minecraft:light_gray_concrete",
    )

    # Public entrance pavilion projects toward the street. The clean white mass
    # and glazed opening will later carry full VCF identity, but Gate A judges
    # the entrance by shape and hierarchy rather than readable signage.
    base.shell(
        t,
        (11, 1, 3),
        (27, 7, 11),
        "minecraft:white_concrete",
        "minecraft:smooth_stone",
        "minecraft:white_concrete",
    )
    t.fill((13, 2, 3), (25, 5, 3), "create:framed_glass")
    t.clear((18, 2, 3), (20, 4, 3))
    base.door(t, 18, 2, 3, facing="south", material="iron", hinge="left")
    base.door(t, 19, 2, 3, facing="south", material="iron", hinge="right")

    # Public canopy / institutional blade. Green is used as a restrained VCF
    # massing accent, not as a substitute for architecture or final signage.
    t.fill((9, 6, 1), (29, 6, 5), "minecraft:white_concrete")
    t.fill((11, 7, 4), (27, 8, 4), "minecraft:lime_concrete")
    t.fill((12, 8, 5), (14, 10, 5), "minecraft:lime_concrete")

    # Rear receiving/dispatch volume and service canopy. The freight side is
    # intentionally different from the customer facade even before signs exist.
    base.shell(
        t,
        (12, 1, 24),
        (29, 7, 31),
        "tfmg:cinder_block",
        "tfmg:factory_floor",
        "minecraft:light_gray_concrete",
    )
    t.clear((16, 2, 31), (20, 5, 31))
    t.fill((14, 6, 29), (24, 6, 32), "tfmg:steel_block")
    t.fill((8, 0, 28), (30, 0, 32), "tfmg:factory_floor")

    # Minimal side/service thresholds used only to prove that the planned
    # circulation can enter the correct masses. Interior planning comes later.
    t.clear((3, 2, 16), (3, 4, 18))
    t.clear((35, 2, 17), (35, 4, 18))
    t.clear((11, 2, 28), (12, 4, 28))

    # Cold-chain roof plant: two equipment masses, a connecting service bridge,
    # and a raised screen. No micro-machinery is placed at Gate A.
    t.fill((17, 9, 13), (21, 11, 18), "immersiveengineering:sheetmetal_steel")
    t.fill((24, 10, 14), (29, 12, 20), "immersiveengineering:sheetmetal_steel")
    t.fill((21, 10, 15), (24, 10, 17), "tfmg:steel_block")
    t.fill((16, 9, 12), (30, 9, 12), "minecraft:white_concrete")
    t.fill((16, 9, 21), (30, 9, 21), "minecraft:white_concrete")

    # A few large facade openings establish public-vs-workplace rhythm without
    # pretending the intact interior or final fenestration has been designed.
    t.fill((9, 3, 8), (12, 5, 8), "create:framed_glass")
    t.fill((26, 3, 8), (29, 5, 8), "create:framed_glass")
    t.fill((8, 3, 12), (8, 5, 15), "create:framed_glass")

    return t


def main() -> None:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if state.get("active_target") != "OWS-001":
        print(f"Gate-A OWS-001 renderer skipped: active target is {state.get('active_target')}")
        return

    gate = state.get("visual_review_gates", {}).get("gate_a_massing", {})
    status = gate.get("status", "not_started")
    if status not in {"designing_massing_review", "ready_to_render", "rerender_required"}:
        print(f"Gate-A OWS-001 renderer skipped: status={status}")
        return

    t = build_gate_a_massing()
    t.save(TEMP_NAME)
    try:
        size, blocks = unpack_structure(TEMP_NBT)
        revision = os.environ.get("GITHUB_SHA", "local")[:8]
        manifest = render_review_set(
            target="OWS-001",
            gate="gate_a_massing",
            revision=f"massing-r1@{revision}",
            damage_state="D0 intact massing only",
            source_commit=os.environ.get("GITHUB_SHA", "working-tree"),
            source_path="review-only:build_gate_a_massing()",
            size=size,
            blocks=blocks,
            output_dir=OUTPUT_DIR,
            camera_set=gate.get("fixed_camera_set", "ows001_fixed_v1"),
        )
    finally:
        TEMP_NBT.unlink(missing_ok=True)

    state["active_status"] = "gate_a_massing_rendered_pending_review"
    state["active_target_passes"]["massing"] = "implemented_pending_gate_a_review"
    state["active_target_passes"]["visual_gate_a_massing"] = "rendered_pending_manual_review"
    gate["status"] = "rendered_pending_manual_review"
    gate["artifact_manifest"] = str((OUTPUT_DIR / "review_manifest.json").relative_to(ROOT)).replace("\\", "/")
    gate["review_stage_source"] = "scripts/render_ows001_gate_a_massing.py"
    gate["review_only"] = True
    state["visual_review_gates"]["gate_a_massing"] = gate
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")

    print(
        f"Rendered OWS-001 Gate A massing review at {manifest['dimensions']} using "
        f"{manifest['fixed_camera_set']}; manual massing approval remains pending."
    )


if __name__ == "__main__":
    main()
