#!/usr/bin/env python3
"""[SYSTEM REPORT] Build and render OWS-001 Gate-A D0 massing review.

This is a review-only intermediate. It does not replace the authoritative OWS-001
builder and it is never placed in worldgen. The purpose is to test the rebuilt
shell, site occupation, entrance hierarchy, service massing, and roof composition
before expensive interior work begins.

Revision r2 addresses every blocking finding from the recorded r1 Gate-A review:
smaller purpose-tied canopies, a stepped central workplace mass, stronger service
bay rhythm, a broken-up cold-chain roof plant, partial mechanical screens, and a
site plan composed from separate public/service hardscape zones rather than one
continuous asphalt rectangle.
"""
from __future__ import annotations

import json
import os

import generate_wasteland_sites as base
from render_old_world_heavy_rebuild_review import OUTPUT_ROOT, ROOT, render_review_set
from render_structure_review import unpack_structure


STATE_PATH = ROOT / "dev/old_world_narrative" / "registry" / "heavy_rebuild_state.json"
TEMP_NAME = "_heavy_review_ows001_gate_a_massing_r2"
TEMP_NBT = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{TEMP_NAME}.nbt"
OUTPUT_DIR = OUTPUT_ROOT / "OWS-001" / "gate_a_massing" / "r2"


def _service_frame(
    t: base.Template,
    *,
    x: int,
    z1: int,
    z2: int,
    outward_x: int,
    top_y: int,
) -> None:
    """Add one large external service-bay frame, not facade microdetail."""
    for z in (z1, z2):
        t.fill((outward_x, 1, z), (outward_x, top_y, z), "tfmg:steel_block")
    t.fill((outward_x, top_y, z1), (outward_x, top_y, z2), "tfmg:steel_block")
    # Recess the wall inside the frame so it reads as a real service bay.
    inner_x = x
    t.fill((inner_x, 2, z1 + 1), (inner_x, top_y - 1, z2 - 1), "minecraft:gray_concrete")


def build_gate_a_massing() -> base.Template:
    """Construct only the D0 architectural/site masses needed for Gate A."""
    t = base.Template((39, 13, 33))

    # D0 site composition. A soft perimeter keeps this from reading as a diagram
    # on one giant asphalt card. Hardscape exists only where people/freight need it.
    t.fill((1, 0, 1), (37, 0, 31), "minecraft:grass_block")
    t.fill((9, 0, 1), (29, 0, 8), "minecraft:smooth_stone")   # public arrival
    t.fill((6, 0, 7), (32, 0, 28), "tfmg:asphalt")            # building/service walk
    t.fill((10, 0, 27), (30, 0, 32), "tfmg:factory_floor")    # rear freight apron
    t.fill((3, 0, 12), (6, 0, 24), "minecraft:smooth_stone")  # returns/service strip
    t.fill((33, 0, 13), (36, 0, 24), "minecraft:smooth_stone")  # cold plant service strip

    # r2 central massing is deliberately stepped rather than one 24x21 donor-like
    # box. The front workplace block and lower rear process block overlap just
    # enough to form a coherent building while producing a real roof/setback break.
    base.shell(
        t,
        (8, 1, 8),
        (26, 8, 20),
        "minecraft:stone_bricks",
        "minecraft:smooth_stone",
        "minecraft:light_gray_concrete",
    )
    base.shell(
        t,
        (10, 1, 18),
        (29, 7, 27),
        "minecraft:stone_bricks",
        "minecraft:smooth_stone",
        "minecraft:white_concrete",
    )

    # West returns/sanitation annex: lower, offset, and visually service-oriented.
    # It has its own large bay frame so the side elevation already implies a real
    # dirty-return/service function before any signage or fixtures are installed.
    base.shell(
        t,
        (3, 1, 12),
        (12, 7, 24),
        "minecraft:light_gray_concrete",
        "minecraft:smooth_stone",
        "minecraft:white_concrete",
    )
    _service_frame(t, x=3, z1=15, z2=20, outward_x=2, top_y=6)
    t.clear((3, 2, 17), (3, 4, 18))

    # East clean cold-chain block: the tallest inhabited/service mass, directly
    # beneath the roof refrigeration plant. A second major service frame makes
    # its maintenance role legible from the opposing side camera.
    base.shell(
        t,
        (26, 1, 10),
        (35, 9, 25),
        "minecraft:white_concrete",
        "minecraft:smooth_stone",
        "minecraft:light_gray_concrete",
    )
    _service_frame(t, x=35, z1=14, z2=21, outward_x=36, top_y=7)
    t.clear((35, 2, 17), (35, 4, 18))

    # Public entrance pavilion: still distinct, but narrower than r1 and tied to
    # a clear central threshold. It is intentionally not a monumental lobby.
    base.shell(
        t,
        (12, 1, 3),
        (26, 7, 12),
        "minecraft:white_concrete",
        "minecraft:smooth_stone",
        "minecraft:white_concrete",
    )
    t.fill((14, 2, 3), (24, 5, 3), "create:framed_glass")
    t.clear((18, 2, 3), (20, 4, 3))
    base.door(t, 18, 2, 3, facing="south", material="iron", hinge="left")
    base.door(t, 19, 2, 3, facing="south", material="iron", hinge="right")

    # r2 public canopy is sized to the actual entrance and supported at its edges.
    # The smaller canopy lets the pavilion itself, not a floating slab, establish
    # arrival hierarchy.
    t.fill((14, 6, 1), (24, 6, 5), "minecraft:white_concrete")
    t.fill((14, 2, 2), (14, 5, 2), "minecraft:white_concrete")
    t.fill((24, 2, 2), (24, 5, 2), "minecraft:white_concrete")
    t.fill((15, 7, 4), (23, 8, 4), "minecraft:lime_concrete")
    t.fill((12, 7, 6), (13, 9, 6), "minecraft:lime_concrete")

    # Rear receiving/dispatch volume. The freight opening and canopy now form one
    # aligned service bay instead of the r1 broad generic rear slab.
    base.shell(
        t,
        (12, 1, 23),
        (29, 7, 31),
        "tfmg:cinder_block",
        "tfmg:factory_floor",
        "minecraft:light_gray_concrete",
    )
    t.clear((17, 2, 31), (20, 5, 31))
    t.fill((16, 6, 29), (21, 6, 32), "tfmg:steel_block")
    t.fill((16, 2, 30), (16, 5, 30), "tfmg:steel_block")
    t.fill((21, 2, 30), (21, 5, 30), "tfmg:steel_block")
    t.fill((16, 5, 30), (21, 5, 30), "tfmg:steel_block")

    # A shallow rear records/service bump-out prevents the back elevation from
    # becoming one uninterrupted loading wall and reserves believable workplace
    # volume without designing the interior yet.
    base.shell(
        t,
        (24, 1, 25),
        (33, 6, 29),
        "minecraft:stone_bricks",
        "minecraft:smooth_stone",
        "minecraft:white_concrete",
    )
    t.fill((27, 3, 29), (30, 4, 29), "create:framed_glass")

    # Cold-chain roof plant r2: four separated equipment masses with a service
    # spine and open maintenance gaps. They are big enough to read in primitive
    # review, but no longer resemble two solid rooftop bunkers.
    equipment = (
        ((17, 9, 14), (18, 10, 16)),
        ((20, 9, 14), (21, 11, 16)),
        ((24, 10, 15), (25, 11, 18)),
        ((28, 10, 15), (29, 12, 18)),
    )
    for a, b in equipment:
        t.fill(a, b, "immersiveengineering:sheetmetal_steel")
    t.fill((17, 9, 18), (29, 9, 19), "minecraft:smooth_stone")
    for x in (16, 23, 30):
        t.fill((x, 9, 13), (x, 11, 13), "tfmg:steel_block")
        t.fill((x, 9, 20), (x, 11, 20), "tfmg:steel_block")
    t.fill((16, 11, 13), (22, 11, 13), "minecraft:white_concrete")
    t.fill((24, 11, 20), (30, 11, 20), "minecraft:white_concrete")

    # Large facade openings establish structural/public rhythm, not final window
    # detailing. They line up with the stepped masses and leave solid wall bays.
    t.fill((9, 3, 8), (12, 5, 8), "create:framed_glass")
    t.fill((22, 3, 8), (25, 5, 8), "create:framed_glass")
    t.fill((8, 3, 12), (8, 5, 15), "create:framed_glass")
    t.fill((10, 3, 20), (10, 5, 23), "create:framed_glass")

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
            revision=f"massing-r2@{revision}",
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

    state["active_status"] = "gate_a_r2_massing_rendered_pending_review"
    state["active_target_passes"]["massing"] = "r2_implemented_pending_gate_a_review"
    state["active_target_passes"]["visual_gate_a_massing"] = "r2_rendered_pending_manual_review"
    gate["status"] = "r2_rendered_pending_manual_review"
    gate["r2_artifact_manifest"] = str((OUTPUT_DIR / "review_manifest.json").relative_to(ROOT)).replace("\\", "/")
    gate["review_stage_source"] = "scripts/render_ows001_gate_a_massing.py"
    gate["review_only"] = True
    state["visual_review_gates"]["gate_a_massing"] = gate
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")

    print(
        f"Rendered OWS-001 Gate A r2 massing review at {manifest['dimensions']} using "
        f"{manifest['fixed_camera_set']}; manual massing approval remains pending."
    )


if __name__ == "__main__":
    main()
