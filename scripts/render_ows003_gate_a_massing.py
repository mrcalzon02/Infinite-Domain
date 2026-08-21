#!/usr/bin/env python3
"""[SYSTEM REPORT] Build and render OWS-003 Gate-A D0 massing review.

This module is review-only. It preserves useful orchard-cannery site history but
contains no final cold-vault racks, nursery cells, proof loot, anomaly layer,
encounters, damage or microdetail. Its only job is to prove the adaptive-reuse
massing, cold-chain site hierarchy, loading thresholds, roof plant reservation and
maintenance-access composition before detailed operations can hide macro defects.
"""
from __future__ import annotations

import json
import os

import generate_wasteland_sites as base
from render_old_world_heavy_rebuild_review import OUTPUT_ROOT, ROOT, render_review_set
from render_structure_review import unpack_structure

STATE_PATH = ROOT / "old_world_narrative" / "registry" / "heavy_rebuild_state.json"
TEMP_NAME = "_heavy_review_ows003_gate_a_massing_r1"
TEMP_NBT = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{TEMP_NAME}.nbt"
OUTPUT_DIR = OUTPUT_ROOT / "OWS-003" / "gate_a_massing" / "r1"


def _orchard_context(t: base.Template) -> None:
    """Retain legible orchard history without letting foliage become the hero mass."""
    # Four interrupted rows preserve the former agricultural property. Canopy gaps
    # keep the converted plant visible from every review angle.
    for x in (5, 10, 15, 20):
        for z in (10, 17, 24, 31, 38, 45):
            t.fill((x, 1, z), (x, 4, z), "minecraft:oak_log", axis="y")
            t.fill((x - 2, 4, z - 2), (x + 2, 6, z + 2), "minecraft:oak_leaves", persistent="true")
    # Old orchard service strip against the plant edge.
    t.fill((21, 0, 8), (23, 0, 45), "minecraft:coarse_dirt")


def _front_admin(t: base.Template) -> None:
    """Lower retained cannery annex converted into the controlled staff/records face."""
    base.shell(
        t,
        (24, 1, 5),
        (55, 9, 18),
        "minecraft:bricks",
        "minecraft:polished_andesite",
        "minecraft:smooth_stone",
    )
    # Later clean VCF retrofit projects from, rather than recolors, the old brick.
    t.fill((31, 2, 4), (48, 7, 4), "minecraft:white_concrete")
    t.fill((35, 3, 3), (44, 6, 3), "create:framed_glass")
    t.clear((39, 2, 3), (40, 5, 4))
    t.fill((34, 8, 4), (46, 9, 4), "minecraft:white_concrete")
    t.fill((37, 9, 3), (43, 11, 3), "minecraft:lime_concrete")
    # Restrained supported arrival canopy.
    t.fill((34, 8, 1), (46, 8, 4), "minecraft:white_concrete")
    for x in (34, 46):
        t.fill((x, 1, 2), (x, 7, 2), "minecraft:light_gray_concrete")


def _main_cold_hall(t: base.Template) -> None:
    """Retained high cannery process hall becomes the dominant cold-chain mass."""
    base.shell(
        t,
        (24, 1, 17),
        (55, 17, 43),
        "minecraft:bricks",
        "tfmg:factory_floor",
        "minecraft:smooth_stone",
    )

    # Industrial bay rhythm. These are macro pilasters/frames only; detailed
    # structure and room openings belong after Gate A.
    for z in (20, 26, 32, 38, 43):
        t.fill((23, 1, z), (23, 16, z), "minecraft:light_gray_concrete")
        t.fill((56, 1, z), (56, 16, z), "minecraft:light_gray_concrete")
    for x in (28, 35, 42, 49, 55):
        t.fill((x, 1, 16), (x, 16, 16), "minecraft:light_gray_concrete")
        t.fill((x, 1, 44), (x, 16, 44), "minecraft:light_gray_concrete")

    # Reinterpret the donor's long roof-light rhythm as three bay-aligned strips.
    for x1, x2 in ((28, 30), (37, 39), (46, 48)):
        t.fill((x1, 17, 20), (x2, 17, 39), "create:framed_glass")
        t.fill((x1 - 1, 17, 20), (x1 - 1, 18, 39), "tfmg:steel_block")
        t.fill((x2 + 1, 17, 20), (x2 + 1, 18, 39), "tfmg:steel_block")

    # Cold-chain conversion band is discontinuous and tied to structure rather
    # than wrapping the entire donor in a corporate stripe.
    t.fill((31, 13, 16), (39, 14, 16), "minecraft:white_concrete")
    t.fill((40, 13, 16), (48, 14, 16), "minecraft:lime_concrete")


def _east_receiving(t: base.Template) -> None:
    """Complete inbound cold-chain threshold on the east service face."""
    t.fill((55, 0, 20), (58, 0, 31), "tfmg:factory_floor")
    # Recessed portal body and complete exterior frame.
    t.fill((55, 2, 21), (55, 8, 30), "minecraft:white_concrete")
    t.clear((55, 2, 23), (55, 6, 27))
    for z in (21, 30):
        t.fill((57, 1, z), (57, 8, z), "tfmg:steel_block")
    t.fill((57, 8, 21), (57, 8, 30), "tfmg:steel_block")
    t.fill((55, 8, 21), (58, 8, 30), "minecraft:light_gray_concrete")
    # Cyan is reserved for temperature-controlled logistics routing.
    t.fill((56, 2, 21), (56, 7, 21), "minecraft:light_blue_concrete")


def _south_dispatch(t: base.Template) -> None:
    """Distinct outbound threshold and dispatch apron on the south/rear face."""
    t.fill((39, 0, 43), (56, 0, 50), "tfmg:asphalt")
    t.clear((44, 2, 43), (49, 6, 44))
    t.fill((42, 8, 42), (52, 8, 48), "minecraft:light_gray_concrete")
    for x in (42, 52):
        t.fill((x, 1, 47), (x, 8, 47), "tfmg:steel_block")
    t.fill((42, 9, 44), (52, 9, 44), "tfmg:steel_block")
    # Yellow remains outbound routing/emergency visibility rather than identity.
    t.fill((44, 0, 44), (49, 0, 50), "minecraft:yellow_concrete")


def _roof_plant_and_access(t: base.Template) -> None:
    """Reserve proportional refrigeration plant and a maintainable access mass."""
    # Plant deck positioned over conditioned hall zones.
    t.fill((32, 18, 24), (49, 18, 37), "minecraft:smooth_stone")
    equipment = (
        ((33, 19, 25), (36, 21, 29)),
        ((38, 19, 25), (41, 22, 29)),
        ((33, 19, 32), (37, 21, 36)),
        ((40, 19, 32), (44, 22, 36)),
        ((46, 19, 27), (49, 21, 34)),
    )
    for a, b in equipment:
        t.fill(a, b, "immersiveengineering:sheetmetal_steel")
    # Service gaps/trunks remain visible between equipment masses.
    t.fill((36, 19, 30), (48, 19, 30), "tfmg:steel_block")
    t.fill((45, 18, 30), (45, 20, 38), "tfmg:steel_block")

    # Projecting maintenance stair/access tower. Actual stairs/ladder come later;
    # Gate A only protects the mass and roof landing relationship.
    base.shell(
        t,
        (50, 1, 31),
        (55, 20, 38),
        "minecraft:light_gray_concrete",
        "minecraft:smooth_stone",
        "minecraft:white_concrete",
    )
    t.fill((51, 18, 30), (54, 20, 31), "minecraft:white_concrete")


def build_gate_a_massing() -> base.Template:
    """Return OWS-003 r1 macro geometry only."""
    t = base.Template((59, 24, 51))

    # Site pad remains mostly soft. Hardscape is split by actual operational role.
    t.fill((1, 0, 1), (57, 0, 49), "minecraft:grass_block")
    t.fill((29, 0, 1), (50, 0, 7), "minecraft:smooth_stone")
    t.fill((55, 0, 20), (58, 0, 31), "tfmg:factory_floor")
    t.fill((39, 0, 43), (56, 0, 50), "tfmg:asphalt")

    _orchard_context(t)
    _front_admin(t)
    _main_cold_hall(t)
    _east_receiving(t)
    _south_dispatch(t)
    _roof_plant_and_access(t)

    return t


def main() -> None:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if state.get("active_target") != "OWS-003":
        print(f"Gate-A OWS-003 renderer skipped: active target is {state.get('active_target')}")
        return

    gate = state.get("visual_review_gates", {}).get("gate_a_massing", {})
    status = gate.get("status", "not_started")
    if status not in {"ready_for_massing_implementation", "ready_to_render", "rerender_required"}:
        print(f"Gate-A OWS-003 renderer skipped: status={status}")
        return

    t = build_gate_a_massing()
    if tuple(t.size) != (59, 24, 51):
        raise AssertionError(f"OWS-003 Gate-A r1 dimensions changed unexpectedly: {t.size}")

    t.save(TEMP_NAME)
    try:
        size, blocks = unpack_structure(TEMP_NBT)
        revision = os.environ.get("GITHUB_SHA", "local")[:8]
        manifest = render_review_set(
            target="OWS-003",
            gate="gate_a_massing",
            revision=f"massing-r1@{revision}",
            damage_state="D0 intact massing only",
            source_commit=os.environ.get("GITHUB_SHA", "working-tree"),
            source_path="review-only:render_ows003_gate_a_massing.build_gate_a_massing()",
            size=size,
            blocks=blocks,
            output_dir=OUTPUT_DIR,
            camera_set=gate.get("fixed_camera_set", "ows003_fixed_v1"),
        )
    finally:
        TEMP_NBT.unlink(missing_ok=True)

    state["active_status"] = "gate_a_r1_massing_rendered_pending_review"
    state["active_target_passes"]["massing"] = "r1_implemented_pending_gate_a_review"
    state["active_target_passes"]["visual_gate_a_massing"] = "r1_rendered_pending_manual_review"
    gate["status"] = "r1_rendered_pending_manual_review"
    gate["r1_artifact_manifest"] = str((OUTPUT_DIR / "review_manifest.json").relative_to(ROOT)).replace("\\", "/")
    gate["review_stage_source"] = "scripts/render_ows003_gate_a_massing.py"
    gate["review_only"] = True
    state["visual_review_gates"]["gate_a_massing"] = gate
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")

    print(
        f"Rendered OWS-003 Gate A r1 massing review at {manifest['dimensions']} using "
        f"{manifest['fixed_camera_set']}; manual massing approval remains pending."
    )


if __name__ == "__main__":
    main()
