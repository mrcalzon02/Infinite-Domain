#!/usr/bin/env python3
"""[SYSTEM REPORT] Build and render OWS-002 Gate-A D0 massing review.

This module is review-only. It deliberately contains no crop racks, relief stock,
final signage, crisis isolation, ruin damage, quest loot, or microdetail. Its job
is to prove that the retained community-center mass can read as a believable
municipal emergency grow-hall conversion before later passes are allowed to hide
weak macro architecture.

Revision r2 responds directly to the recorded r1 rejection: the lower civic mass
is split into a lower west support wing and a north public/administrative bar, the
grow hall and lantern become the dominant volume, receiving/dispatch receive
complete opening-tied frames, and the roof service cluster becomes legible against
the lowered civic roof.
"""
from __future__ import annotations

import json
import os

import generate_wasteland_sites as base
from render_old_world_heavy_rebuild_review import OUTPUT_ROOT, ROOT, render_review_set
from render_structure_review import unpack_structure


STATE_PATH = ROOT / "dev/old_world_narrative" / "registry" / "heavy_rebuild_state.json"
TEMP_NAME = "_heavy_review_ows002_gate_a_massing_r2"
TEMP_NBT = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{TEMP_NAME}.nbt"
OUTPUT_DIR = OUTPUT_ROOT / "OWS-002" / "gate_a_massing" / "r2"


def _public_canopy(t: base.Template) -> None:
    """Restrained emergency canopy at the retained north civic lobby."""
    t.fill((21, 7, 1), (29, 7, 5), "minecraft:white_concrete")
    for x in (21, 29):
        t.fill((x, 1, 2), (x, 6, 2), "minecraft:polished_blackstone_bricks")
    # Macro identity masses only. Readable signs belong to the intact-state pass.
    t.fill((22, 8, 4), (28, 9, 4), "minecraft:lime_concrete")
    t.fill((18, 8, 5), (19, 11, 5), "minecraft:yellow_concrete")


def _east_receiving(t: base.Template) -> None:
    """Complete civic-scale receiving bay tied to the real east hall threshold."""
    t.fill((46, 0, 18), (50, 0, 31), "tfmg:factory_floor")

    # Recess the receiving face before adding the exterior frame. This makes the
    # bay a real threshold instead of a thin canopy pasted onto the hall wall.
    t.fill((46, 2, 22), (46, 6, 28), "minecraft:gray_concrete")
    t.clear((46, 2, 24), (46, 5, 26))

    for z in (21, 29):
        t.fill((48, 1, z), (48, 7, z), "tfmg:steel_block")
    t.fill((48, 8, 21), (48, 8, 29), "tfmg:steel_block")
    t.fill((46, 7, 21), (50, 7, 29), "minecraft:light_gray_concrete")

    # One restrained vertical VCF service mark differentiates the inbound side
    # without turning the retrofit into a corporate warehouse dock.
    t.fill((47, 2, 21), (47, 6, 21), "minecraft:lime_concrete")


def _south_dispatch(t: base.Template) -> None:
    """Opening-tied relief dispatch frame and apron at the retained south exit."""
    t.fill((23, 0, 41), (38, 0, 46), "tfmg:asphalt")
    t.clear((29, 2, 41), (32, 5, 41))

    # r2 narrows the canopy to the actual handoff bay and adds a complete frame.
    t.fill((27, 7, 39), (35, 7, 45), "minecraft:light_gray_concrete")
    for x in (27, 35):
        t.fill((x, 1, 44), (x, 7, 44), "tfmg:steel_block")
    t.fill((27, 8, 42), (35, 8, 42), "tfmg:steel_block")
    # Yellow is macro emergency routing, not D1 overflow or final sign text.
    t.fill((28, 8, 40), (34, 8, 40), "minecraft:yellow_concrete")


def _roof_service(t: base.Template) -> None:
    """Separated grow-service units on the lower west/rear civic roof."""
    t.fill((10, 12, 32), (19, 12, 40), "minecraft:smooth_stone")
    equipment = (
        ((10, 13, 33), (12, 15, 35)),
        ((14, 13, 33), (16, 16, 35)),
        ((11, 13, 37), (13, 15, 39)),
        ((16, 13, 37), (18, 16, 39)),
    )
    for a, b in equipment:
        t.fill(a, b, "immersiveengineering:sheetmetal_steel")
    t.fill((12, 13, 36), (17, 13, 36), "tfmg:steel_block")


def build_gate_a_massing() -> base.Template:
    """Return OWS-002 r2 macro geometry only."""
    t = base.Template((51, 21, 47))

    # Differentiated civic site. Hardscape exists only where public or service
    # throughput needs it, leaving a visible soft perimeter around the conversion.
    t.fill((1, 0, 1), (49, 0, 45), "minecraft:grass_block")
    t.fill((18, 0, 0), (32, 0, 7), "minecraft:smooth_stone")
    t.fill((3, 0, 7), (6, 0, 41), "minecraft:smooth_stone")
    t.fill((46, 0, 18), (50, 0, 31), "tfmg:factory_floor")
    t.fill((23, 0, 41), (38, 0, 46), "tfmg:asphalt")

    # r2 turns the oversized r1 lower box into an explicit civic L-shaped wrap:
    # a low west/rear support wing plus a slightly taller north public/admin bar.
    # The original community-center reading survives, but neither element can
    # compete with the converted multipurpose/grow hall for skyline dominance.
    base.shell(
        t,
        (4, 1, 7),
        (21, 11, 41),
        "minecraft:mud_bricks",
        "tfmg:factory_floor",
        "minecraft:smooth_stone",
    )
    base.shell(
        t,
        (18, 1, 7),
        (46, 12, 15),
        "minecraft:smooth_stone",
        "minecraft:polished_andesite",
        "minecraft:smooth_stone",
    )

    # The retained multipurpose hall is now unambiguously the hero volume. Its
    # dimensions remain compatible with the donor and the accepted Pass-5 scale.
    base.shell(
        t,
        (22, 1, 15),
        (46, 18, 41),
        "minecraft:bricks",
        "minecraft:smooth_stone",
        "minecraft:weathered_cut_copper",
    )

    # Retained projecting civic lobby.
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

    # Simplified civic glazing protects the adaptive-reuse reading without
    # prematurely performing the Pass-9 facade-detail pass.
    for z1, z2 in ((11, 15), (20, 24), (31, 35)):
        t.fill((4, 3, z1), (4, 6, z2), "create:framed_glass")
    for x1, x2 in ((34, 38), (41, 45)):
        t.fill((x1, 4, 7), (x2, 7, 7), "create:framed_glass")

    # Preserve the hall lantern as the clear topmost civic/agricultural feature.
    t.fill((27, 18, 21), (40, 20, 34), "create:framed_glass")

    _public_canopy(t)
    _east_receiving(t)
    _south_dispatch(t)
    _roof_service(t)

    # Preserve the authoritative donor's east/rear maintenance route. r2 does not
    # relocate this ladder merely to make the roof plant composition easier.
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

    # A restrained hall crown signals the VCF conversion at macro scale while the
    # original brick civic hall remains the dominant architectural material.
    t.fill((25, 13, 14), (43, 14, 14), "minecraft:lime_concrete")

    return t


def main() -> None:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if state.get("active_target") != "OWS-002":
        print(f"Gate-A OWS-002 renderer skipped: active target is {state.get('active_target')}")
        return

    gate = state.get("visual_review_gates", {}).get("gate_a_massing", {})
    status = gate.get("status", "not_started")
    if status not in {"ready_for_massing_implementation", "ready_to_render", "rerender_required"}:
        print(f"Gate-A OWS-002 renderer skipped: status={status}")
        return

    t = build_gate_a_massing()
    if tuple(t.size) != (51, 21, 47):
        raise AssertionError(f"OWS-002 Gate-A r2 dimensions changed unexpectedly: {t.size}")

    t.save(TEMP_NAME)
    try:
        size, blocks = unpack_structure(TEMP_NBT)
        revision = os.environ.get("GITHUB_SHA", "local")[:8]
        manifest = render_review_set(
            target="OWS-002",
            gate="gate_a_massing",
            revision=f"massing-r2@{revision}",
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

    state["active_status"] = "gate_a_r2_massing_rendered_pending_review"
    state["active_target_passes"]["massing"] = "r2_implemented_pending_gate_a_review"
    state["active_target_passes"]["visual_gate_a_massing"] = "r2_rendered_pending_manual_review"
    gate["status"] = "r2_rendered_pending_manual_review"
    gate["r2_artifact_manifest"] = str((OUTPUT_DIR / "review_manifest.json").relative_to(ROOT)).replace("\\", "/")
    gate["review_stage_source"] = "scripts/render_ows002_gate_a_massing.py"
    gate["review_only"] = True
    state["visual_review_gates"]["gate_a_massing"] = gate
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")

    print(
        f"Rendered OWS-002 Gate A r2 massing review at {manifest['dimensions']} using "
        f"{manifest['fixed_camera_set']}; manual massing approval remains pending."
    )


if __name__ == "__main__":
    main()
