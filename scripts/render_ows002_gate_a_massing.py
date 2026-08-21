#!/usr/bin/env python3
"""[SYSTEM REPORT] Build and render OWS-002 Gate-A D0 massing review.

This module is review-only. It deliberately contains no crop racks, relief stock,
final signage, crisis isolation, ruin damage, quest loot, or microdetail. Its job
is to prove that the retained community-center mass can read as a believable
municipal emergency grow-hall conversion before later passes are allowed to hide
weak macro architecture.
"""
from __future__ import annotations

import json
import os

import generate_wasteland_sites as base
from render_old_world_heavy_rebuild_review import OUTPUT_ROOT, ROOT, render_review_set
from render_structure_review import unpack_structure


STATE_PATH = ROOT / "old_world_narrative" / "registry" / "heavy_rebuild_state.json"
TEMP_NAME = "_heavy_review_ows002_gate_a_massing_r1"
TEMP_NBT = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{TEMP_NAME}.nbt"
OUTPUT_DIR = OUTPUT_ROOT / "OWS-002" / "gate_a_massing" / "r1"


def _public_canopy(t: base.Template) -> None:
    """A restrained civic-emergency canopy tied to the existing north doors."""
    # Existing projecting lobby remains the architectural anchor. The canopy is
    # intentionally narrower than the lobby so it reads as a retrofit, not a new
    # monumental facade pasted over the community center.
    t.fill((20, 7, 1), (30, 7, 5), "minecraft:white_concrete")
    for x in (20, 30):
        t.fill((x, 1, 2), (x, 6, 2), "minecraft:polished_blackstone_bricks")
    # Emergency/VCF identity masses only; final readable signs belong to Pass 12.
    t.fill((21, 8, 4), (29, 9, 4), "minecraft:lime_concrete")
    t.fill((18, 8, 5), (19, 11, 5), "minecraft:yellow_concrete")


def _east_receiving(t: base.Template) -> None:
    """Compact clean-stock receiving frame at the donor east hall threshold."""
    # Service apron fits inside the existing 51-block template rather than
    # pretending this neighborhood civic site suddenly owns a warehouse truck court.
    t.fill((46, 0, 18), (50, 0, 31), "tfmg:factory_floor")
    for z in (21, 29):
        t.fill((48, 1, z), (48, 6, z), "tfmg:steel_block")
    t.fill((46, 7, 21), (50, 7, 29), "minecraft:light_gray_concrete")
    t.fill((48, 7, 21), (48, 8, 29), "minecraft:lime_concrete")
    # A recessed service threshold makes the receiving side distinct from the
    # public north face even before doors and operational signage are detailed.
    t.fill((46, 2, 22), (46, 6, 28), "minecraft:gray_concrete")
    t.clear((46, 2, 24), (46, 5, 26))


def _south_dispatch(t: base.Template) -> None:
    """Emergency relief handoff tied to the real south hall exit."""
    t.fill((23, 0, 41), (38, 0, 46), "tfmg:asphalt")
    t.fill((26, 7, 39), (36, 7, 45), "minecraft:light_gray_concrete")
    for x in (26, 36):
        t.fill((x, 1, 44), (x, 6, 44), "tfmg:steel_block")
    # Yellow relief band is architectural routing at this stage, not D1 overflow.
    t.fill((27, 8, 40), (35, 8, 40), "minecraft:yellow_concrete")
    t.clear((29, 2, 41), (32, 5, 41))


def _roof_service(t: base.Template) -> None:
    """Clustered grow-service plant that remains subordinate to the roof lantern."""
    # Preserve the donor west/rear service-volume position but articulate it into
    # serviceable equipment masses with gaps instead of one unbroken rooftop cube.
    t.fill((12, 14, 33), (18, 14, 39), "minecraft:smooth_stone")
    equipment = (
        ((12, 15, 34), (13, 17, 36)),
        ((15, 15, 34), (16, 18, 36)),
        ((12, 15, 38), (14, 17, 39)),
        ((17, 15, 37), (18, 18, 39)),
    )
    for a, b in equipment:
        t.fill(a, b, "immersiveengineering:sheetmetal_steel")
    t.fill((13, 15, 37), (17, 15, 37), "tfmg:steel_block")


def build_gate_a_massing() -> base.Template:
    """Return OWS-002 r1 macro geometry only."""
    t = base.Template((51, 21, 47))

    # Site composition. Separate public, receiving and dispatch hardscape avoids
    # the giant-universal-asphalt-card failure mode while retaining civic context.
    t.fill((1, 0, 1), (49, 0, 45), "minecraft:grass_block")
    t.fill((18, 0, 0), (32, 0, 9), "minecraft:smooth_stone")
    t.fill((4, 0, 7), (46, 0, 41), "tfmg:asphalt")
    # Break the hardscape back around the civic perimeter so the building does not
    # sit on one undifferentiated rectangle.
    t.fill((5, 0, 8), (17, 0, 33), "minecraft:smooth_stone")
    t.fill((6, 0, 34), (20, 0, 40), "minecraft:smooth_stone")
    t.fill((23, 0, 16), (45, 0, 40), "tfmg:factory_floor")

    # Retained civic/community-center body. Gate A tests conversion of this mass,
    # not replacement with a generic green industrial box.
    base.shell(
        t,
        (4, 1, 7),
        (46, 14, 41),
        "minecraft:mud_bricks",
        "tfmg:factory_floor",
        "minecraft:smooth_stone",
    )

    # Taller multipurpose-hall volume remains the future cultivation hero space.
    base.shell(
        t,
        (22, 1, 15),
        (46, 18, 41),
        "minecraft:bricks",
        "minecraft:smooth_stone",
        "minecraft:weathered_cut_copper",
    )

    # Projecting public lobby preserves familiar civic arrival hierarchy.
    base.shell(
        t,
        (18, 1, 4),
        (32, 8, 9),
        "minecraft:smooth_stone",
        "minecraft:polished_andesite",
        "minecraft:smooth_stone_slab",
    )
    t.fill((20, 2, 4), (30, 5, 4), "create:framed_glass")
    t.clear((24, 2, 4), (25, 4, 4))
    base.door(t, 24, 2, 4, facing="south", material="dark_oak", hinge="left")
    base.door(t, 25, 2, 4, facing="south", material="dark_oak", hinge="right")

    # Macro facade rhythm retained from the donor in simplified form. These broad
    # openings protect the civic reading without entering Pass-9 facade detailing.
    for x1, x2 in ((6, 10), (13, 17), (35, 39), (42, 45)):
        t.fill((x1, 4, 7), (x2, 7, 7), "create:framed_glass")
    for z1, z2 in ((11, 15), (20, 24), (31, 35)):
        t.fill((4, 4, z1), (4, 7, z2), "create:framed_glass")

    # Preserve the hall lantern as the tallest and most memorable civic/agricultural
    # feature. It is intentionally more important than the retrofit service plant.
    t.fill((27, 18, 21), (40, 20, 34), "create:framed_glass")

    _public_canopy(t)
    _east_receiving(t)
    _south_dispatch(t)
    _roof_service(t)

    # Protect the donor maintenance concept at massing level: visible east-rear
    # vertical access leading to a roof landing. Final hatch/door correctness is
    # a Gate-B contract, not a Gate-A detail requirement.
    t.fill((44, 2, 38), (44, 18, 38), "minecraft:ladder", facing="west", waterlogged="false")
    t.set(
        44,
        19,
        38,
        "minecraft:iron_trapdoor",
        facing="north",
        half="bottom",
        open="false",
        powered="false",
        waterlogged="false",
    )

    # Emergency conversion massing markers: a restrained VCF crown on the hall's
    # public edge and municipal yellow routing at the three actual thresholds.
    t.fill((22, 14, 14), (46, 15, 14), "minecraft:lime_concrete")
    t.fill((18, 9, 6), (19, 11, 6), "minecraft:yellow_concrete")
    t.fill((46, 7, 22), (46, 8, 28), "minecraft:lime_concrete")
    t.fill((27, 8, 40), (35, 8, 40), "minecraft:yellow_concrete")

    return t


def main() -> None:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if state.get("active_target") != "OWS-002":
        print(f"Gate-A OWS-002 renderer skipped: active target is {state.get('active_target')}")
        return

    gate = state.get("visual_review_gates", {}).get("gate_a_massing", {})
    status = gate.get("status", "not_started")
    allowed = {
        "ready_for_massing_implementation",
        "ready_to_render",
        "rerender_required",
    }
    if status not in allowed:
        print(f"Gate-A OWS-002 renderer skipped: status={status}")
        return

    t = build_gate_a_massing()
    if tuple(t.size) != (51, 21, 47):
        raise AssertionError(f"OWS-002 Gate-A r1 dimensions changed unexpectedly: {t.size}")

    t.save(TEMP_NAME)
    try:
        size, blocks = unpack_structure(TEMP_NBT)
        revision = os.environ.get("GITHUB_SHA", "local")[:8]
        manifest = render_review_set(
            target="OWS-002",
            gate="gate_a_massing",
            revision=f"massing-r1@{revision}",
            damage_state="D0 intact massing only",
            source_commit=os.environ.get("GITHUB_SHA", "working-tree"),
            source_path="review-only:render_ows002_gate_a_massing.build_gate_a_massing()",
            size=size,
            blocks=blocks,
            output_dir=OUTPUT_DIR,
            camera_set=gate.get("fixed_camera_set", "ows002_fixed_v1"),
        )
    finally:
        TEMP_NBT.unlink(missing_ok=True)

    state["active_status"] = "gate_a_r1_massing_rendered_pending_review"
    state["active_target_passes"]["massing"] = "r1_implemented_pending_gate_a_review"
    state["active_target_passes"]["visual_gate_a_massing"] = "r1_rendered_pending_manual_review"
    gate["status"] = "r1_rendered_pending_manual_review"
    gate["r1_artifact_manifest"] = str((OUTPUT_DIR / "review_manifest.json").relative_to(ROOT)).replace("\\", "/")
    gate["review_stage_source"] = "scripts/render_ows002_gate_a_massing.py"
    gate["review_only"] = True
    state["visual_review_gates"]["gate_a_massing"] = gate
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")

    print(
        f"Rendered OWS-002 Gate A r1 massing review at {manifest['dimensions']} using "
        f"{manifest['fixed_camera_set']}; manual massing approval remains pending."
    )


if __name__ == "__main__":
    main()
