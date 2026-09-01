#!/usr/bin/env python3
"""[SYSTEM REPORT] Build and render OWS-004 Gate-A D0 massing review.

Review-only model. It proves the macro hierarchy of the VCF mycological vertical
farm tower before cultivation racks, operational machinery, proof loot,
containment history, encounters, damage or microdetail can hide architectural
failures.
"""
from __future__ import annotations

import json
import os

import generate_wasteland_sites as base
from render_old_world_heavy_rebuild_review import OUTPUT_ROOT, ROOT, render_review_set
from render_structure_review import unpack_structure

STATE_PATH = ROOT / "dev/old_world_narrative" / "registry" / "heavy_rebuild_state.json"
TEMP_NAME = "_heavy_review_ows004_gate_a_massing_r1"
TEMP_NBT = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{TEMP_NAME}.nbt"
OUTPUT_DIR = OUTPUT_ROOT / "OWS-004" / "gate_a_massing" / "r1"


def _site_and_podium(t: base.Template) -> None:
    """Create an optimistic public face and separate industrial logistics base."""
    t.fill((1, 0, 1), (49, 0, 45), "minecraft:grass_block")

    # Public/demo forecourt and stepped front podium.
    t.fill((7, 0, 1), (34, 0, 10), "minecraft:smooth_stone")
    base.shell(
        t,
        (6, 1, 6),
        (35, 8, 17),
        "minecraft:white_concrete",
        "minecraft:smooth_stone",
        "minecraft:light_gray_concrete",
    )
    # Transparent public demonstration frontage; this is macro glazing only.
    t.fill((10, 2, 5), (30, 6, 5), "create:framed_glass")
    t.clear((18, 2, 5), (22, 5, 6))
    t.fill((11, 7, 5), (29, 8, 5), "minecraft:lime_concrete")
    # Supported public canopy and entry frame.
    t.fill((12, 8, 2), (28, 8, 6), "minecraft:white_concrete")
    for x in (12, 28):
        t.fill((x, 1, 3), (x, 7, 3), "minecraft:light_gray_concrete")

    # East service/receiving podium deliberately heavier than the public face.
    base.shell(
        t,
        (34, 1, 13),
        (48, 10, 32),
        "minecraft:light_gray_concrete",
        "tfmg:factory_floor",
        "minecraft:smooth_stone",
    )
    t.fill((48, 2, 17), (48, 7, 27), "minecraft:white_concrete")
    t.clear((48, 2, 19), (48, 6, 24))
    t.fill((49, 0, 16), (50, 0, 28), "tfmg:factory_floor")
    t.fill((48, 8, 16), (50, 8, 28), "tfmg:steel_block")
    for z in (16, 28):
        t.fill((50, 1, z), (50, 8, z), "tfmg:steel_block")

    # Rear harvest/packing/dispatch base, separate from receiving and public entry.
    base.shell(
        t,
        (24, 1, 31),
        (47, 8, 43),
        "minecraft:white_concrete",
        "tfmg:factory_floor",
        "minecraft:light_gray_concrete",
    )
    t.clear((31, 2, 43), (39, 6, 43))
    t.fill((28, 0, 43), (44, 0, 46), "tfmg:asphalt")
    t.fill((29, 8, 40), (43, 8, 45), "minecraft:light_gray_concrete")
    for x in (29, 43):
        t.fill((x, 1, 44), (x, 8, 44), "tfmg:steel_block")


def _production_tower(t: base.Template) -> None:
    """Express repeated controlled-environment production modules at macro scale."""
    # Lower two modules retain a slightly broader converted-office footprint.
    base.shell(
        t,
        (10, 8, 12),
        (40, 23, 37),
        "minecraft:white_concrete",
        "minecraft:smooth_stone",
        "minecraft:light_gray_concrete",
    )
    # Upper two modules step inward so the tower is no longer one blunt extrusion.
    base.shell(
        t,
        (12, 23, 14),
        (38, 39, 35),
        "minecraft:white_concrete",
        "minecraft:smooth_stone",
        "minecraft:light_gray_concrete",
    )

    # Four production-module bands. These are architectural service belts, not
    # crop rows or operational equipment.
    module_bands = ((14, 15), (21, 22), (28, 29), (35, 36))
    for y1, y2 in module_bands:
        x1, x2, z1, z2 = (10, 40, 12, 37) if y1 < 23 else (12, 38, 14, 35)
        t.fill((x1, y1, z1 - 1), (x2, y2, z1 - 1), "minecraft:lime_concrete")
        t.fill((x1, y1, z2 + 1), (x2, y2, z2 + 1), "minecraft:lime_concrete")
        # Long controlled glazing strips align to production-floor modules rather
        # than office windows.
        t.fill((x1 + 4, y1 - 3, z1 - 1), (x2 - 4, y1 - 1, z1 - 1), "create:framed_glass")
        t.fill((x1 + 4, y1 - 3, z2 + 1), (x2 - 4, y1 - 1, z2 + 1), "create:framed_glass")

    # Vertical structural ribs break the long faces into cultivation bays.
    for x in (14, 20, 26, 32, 38):
        if x <= 38:
            t.fill((x, 9, 11), (x, 22, 11), "minecraft:light_gray_concrete")
            t.fill((x, 9, 38), (x, 22, 38), "minecraft:light_gray_concrete")
    for x in (16, 22, 28, 34):
        t.fill((x, 24, 13), (x, 38, 13), "minecraft:light_gray_concrete")
        t.fill((x, 24, 36), (x, 38, 36), "minecraft:light_gray_concrete")


def _vertical_service_spine(t: base.Template) -> None:
    """Reserve a substantial environmental/freight service spine and roof access."""
    base.shell(
        t,
        (39, 8, 17),
        (45, 42, 31),
        "minecraft:light_gray_concrete",
        "minecraft:smooth_stone",
        "minecraft:white_concrete",
    )
    # Projecting steel service bands communicate floor connections without yet
    # placing actual ducts, pipes, lifts or machinery.
    for y in (13, 20, 27, 34):
        t.fill((39, y, 16), (45, y + 1, 16), "tfmg:steel_block")
        t.fill((39, y, 32), (45, y + 1, 32), "tfmg:steel_block")
    # Narrow controlled-glass maintenance face makes the spine visually distinct.
    t.fill((45, 11, 20), (45, 39, 27), "create:framed_glass")

    # Secondary stair/egress mass on the opposite side: integrated, not dangling
    # exterior stair flights from the office donor.
    base.shell(
        t,
        (6, 8, 24),
        (10, 39, 33),
        "minecraft:light_gray_concrete",
        "minecraft:smooth_stone",
        "minecraft:white_concrete",
    )


def _roof_crown(t: base.Template) -> None:
    """Build a readable greenhouse/environmental crown tied to the service spine."""
    # Glazed cultivation/showcase crown.
    base.shell(
        t,
        (14, 39, 15),
        (36, 45, 34),
        "create:framed_glass",
        "minecraft:smooth_stone",
        "create:framed_glass",
    )
    # Strong white/lime frame gives the glass volume an intentional silhouette.
    for x in (14, 25, 36):
        t.fill((x, 39, 14), (x, 46, 14), "minecraft:white_concrete")
        t.fill((x, 39, 35), (x, 46, 35), "minecraft:white_concrete")
    t.fill((14, 45, 14), (36, 46, 14), "minecraft:lime_concrete")
    t.fill((14, 45, 35), (36, 46, 35), "minecraft:lime_concrete")

    # Environmental plant block adjacent to, not replacing, the greenhouse.
    t.fill((37, 40, 18), (44, 45, 30), "immersiveengineering:sheetmetal_steel")
    t.fill((39, 42, 16), (42, 45, 17), "tfmg:steel_block")
    t.fill((39, 42, 31), (42, 45, 32), "tfmg:steel_block")


def build_gate_a_massing() -> base.Template:
    t = base.Template((51, 47, 47))
    _site_and_podium(t)
    _production_tower(t)
    _vertical_service_spine(t)
    _roof_crown(t)
    return t


def main() -> None:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if state.get("active_target") != "OWS-004":
        print(f"Gate-A OWS-004 renderer skipped: active target is {state.get('active_target')}")
        return

    gate = state.get("visual_review_gates", {}).get("gate_a_massing", {})
    status = gate.get("status", "not_started")
    if status not in {"ready_for_massing_implementation", "ready_to_render", "rerender_required"}:
        print(f"Gate-A OWS-004 renderer skipped: status={status}")
        return

    t = build_gate_a_massing()
    if tuple(t.size) != (51, 47, 47):
        raise AssertionError(f"OWS-004 Gate-A r1 dimensions changed unexpectedly: {t.size}")

    t.save(TEMP_NAME)
    try:
        size, blocks = unpack_structure(TEMP_NBT)
        revision = os.environ.get("GITHUB_SHA", "local")[:8]
        manifest = render_review_set(
            target="OWS-004",
            gate="gate_a_massing",
            revision=f"massing-r1@{revision}",
            damage_state="D0 intact massing only",
            source_commit=os.environ.get("GITHUB_SHA", "working-tree"),
            source_path="review-only:render_ows004_gate_a_massing.build_gate_a_massing()",
            size=size,
            blocks=blocks,
            output_dir=OUTPUT_DIR,
            camera_set=gate.get("fixed_camera_set", "ows004_fixed_v1"),
        )
    finally:
        TEMP_NBT.unlink(missing_ok=True)

    state["active_status"] = "gate_a_r1_massing_rendered_pending_review"
    state["active_target_passes"]["massing"] = "r1_implemented_pending_gate_a_review"
    state["active_target_passes"]["visual_gate_a_massing"] = "r1_rendered_pending_manual_review"
    gate["status"] = "r1_rendered_pending_manual_review"
    gate["r1_artifact_manifest"] = str((OUTPUT_DIR / "review_manifest.json").relative_to(ROOT)).replace("\\", "/")
    gate["review_stage_source"] = "scripts/render_ows004_gate_a_massing.py"
    gate["review_only"] = True
    state["visual_review_gates"]["gate_a_massing"] = gate
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")

    print(
        f"Rendered OWS-004 Gate A r1 massing review at {manifest['dimensions']} using "
        f"{manifest['fixed_camera_set']}; manual massing approval remains pending."
    )


if __name__ == "__main__":
    main()
