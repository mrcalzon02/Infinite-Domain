#!/usr/bin/env python3
"""Build and render the review-only OWS-009 Gate-A r1 massing study."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path

import generate_wasteland_sites as base


ROOT = Path(__file__).resolve().parents[1]
TARGET = "OWS-009"
SOURCE_PATH = ROOT / "kubejs/data/infinite_domain/structure/wasteland/old_world/ows_009_atlas_roadside_repair_depot.nbt"
FROZEN_SOURCE_SHA256 = "d80dfca574d8f96eca633ac515e810f02f52e7eab2f36195977b42708068fe0d"
FROZEN_SOURCE_BLOB = "4b2df6f6d8bcb5a58511318f0fe78f9f5fc1d44a"
TEMP_NAME = "_heavy_review_ows009_gate_a_massing_r1"
TEMP_NBT = ROOT / "kubejs/data/infinite_domain/structure/wasteland" / f"{TEMP_NAME}.nbt"
OUTPUT_DIR = ROOT / "old_world_narrative/reviews/heavy_rebuild/visual/OWS-009/gate_a_massing/r1"
REQUIRED_RECORDS = (
    "OWS-009_PHASE0_BASELINE_REVIEW.md",
    "OWS-009_PASS2_FUNCTIONAL_DEFINITION.md",
    "OWS-009_PASS3_PRECEDENT_RESEARCH.md",
    "OWS-009_PASS4_PROGRAM_ADJACENCY.md",
    "OWS-009_PASS5_SCALE_TRANSLATION.md",
)
AIR = {None, "minecraft:air", "minecraft:cave_air", "minecraft:void_air", "minecraft:structure_void"}


def _name(t: base.Template, pos: tuple[int, int, int]) -> str | None:
    row = t.blocks.get(pos)
    return None if row is None else t.palette[row[0]]["Name"]


def _shell(t: base.Template, a: tuple[int, int, int], b: tuple[int, int, int], wall: str, roof: str) -> None:
    base.shell(t, a, b, wall, "tfmg:factory_floor", roof)


def _site_and_thresholds(t: base.Template) -> None:
    t.fill((0, 0, 0), (48, 0, 40), "minecraft:grass_block")

    # Road-facing recovery apron and three unmistakable service approaches.
    t.fill((1, 0, 0), (35, 0, 7), "tfmg:asphalt")
    for x1, x2 in ((5, 13), (15, 24), (26, 34)):
        t.fill((x1, 0, 1), (x2, 0, 6), "minecraft:light_gray_concrete")
        t.fill((x1, 0, 3), (x2, 0, 3), "minecraft:yellow_concrete")

    # Customer walk stays outside the recovery field.
    t.fill((36, 0, 0), (47, 0, 19), "minecraft:smooth_stone")
    t.fill((39, 0, 0), (44, 0, 7), "minecraft:white_concrete")

    # Parts delivery and removed-core collection use the east/rear edge.
    t.fill((45, 0, 18), (48, 0, 39), "tfmg:asphalt")
    t.fill((36, 0, 35), (44, 0, 39), "minecraft:coarse_dirt")
    t.fill((36, 0, 35), (44, 0, 35), "minecraft:yellow_concrete")


def _three_cell_hall(t: base.Template) -> None:
    # Three stepped service volumes keep the donor's bay count while replacing
    # the single featureless box with a functional Atlas roof hierarchy.
    _shell(t, (3, 1, 7), (14, 11, 34), "tfmg:cinder_block", "minecraft:smooth_stone")
    _shell(t, (14, 1, 7), (25, 13, 34), "minecraft:light_gray_concrete", "minecraft:smooth_stone")
    _shell(t, (25, 1, 7), (35, 12, 34), "tfmg:cinder_block", "minecraft:smooth_stone")

    # Remove shared shell walls to recover one clear-span operational hall.
    t.clear((14, 2, 8), (14, 9, 31))
    t.clear((25, 2, 8), (25, 9, 31))

    # Broad north thresholds, each framed by real depth and distinct head height.
    for x1, x2, top in ((5, 12, 6), (16, 23, 7), (27, 33, 6)):
        t.clear((x1, 2, 7), (x2, top, 8))
        t.fill((x1 - 1, 1, 6), (x1 - 1, top + 2, 8), "tfmg:steel_block")
        t.fill((x2 + 1, 1, 6), (x2 + 1, top + 2, 8), "tfmg:steel_block")
        t.fill((x1 - 1, top + 1, 6), (x2 + 1, top + 2, 8), "minecraft:orange_concrete")

    # Coarse D0 floor zoning proves cells, a shared transverse movement field,
    # and the rear technician spine without adding operational machinery.
    for x1, x2 in ((5, 13), (15, 24), (26, 34)):
        t.fill((x1, 1, 9), (x2, 1, 23), "minecraft:smooth_stone")
        t.fill((x1, 1, 9), (x1, 1, 23), "minecraft:orange_concrete")
        t.fill((x2, 1, 9), (x2, 1, 23), "minecraft:orange_concrete")
    t.fill((4, 1, 24), (35, 1, 27), "minecraft:light_gray_concrete")
    t.fill((4, 1, 28), (35, 1, 31), "minecraft:polished_blackstone")

    # High clerestory slots follow each work volume rather than repeating the
    # donor's blank walls. They remain massing-scale openings only.
    t.fill((3, 7, 10), (3, 9, 25), "create:framed_glass")
    t.fill((35, 8, 10), (35, 10, 25), "create:framed_glass")
    t.fill((16, 10, 7), (23, 11, 7), "create:framed_glass")
    for x1, x2, y in ((6, 12, 8), (17, 23, 10), (28, 33, 9)):
        t.fill((x1, y, 34), (x2, y + 1, 34), "create:framed_glass")


def _customer_and_support_bars(t: base.Template) -> None:
    # Lower public/service bar establishes a human threshold beside, never in,
    # the recovery lanes.
    _shell(t, (36, 1, 7), (44, 9, 19), "minecraft:white_concrete", "minecraft:light_gray_concrete")
    t.fill((37, 3, 7), (43, 6, 7), "create:framed_glass")
    t.fill((36, 3, 9), (36, 6, 17), "create:framed_glass")
    t.clear((39, 2, 7), (42, 5, 8))
    t.fill((38, 7, 6), (44, 8, 8), "minecraft:orange_concrete")

    # Parts receive/issue and the secure calibrator-records/proof adjacency use
    # one stepped support bar. Their different roof heights preserve legibility.
    _shell(t, (36, 1, 20), (44, 10, 27), "immersiveengineering:sheetmetal_steel", "tfmg:steel_block")
    _shell(t, (36, 1, 27), (44, 11, 34), "minecraft:polished_blackstone_bricks", "tfmg:steel_block")
    t.clear((44, 2, 22), (44, 6, 26))
    t.fill((44, 1, 21), (44, 8, 21), "minecraft:orange_concrete")
    t.fill((44, 1, 27), (44, 8, 27), "minecraft:orange_concrete")
    t.fill((37, 7, 28), (43, 9, 28), "create:framed_glass")

    # Controlled internal thresholds connect service bar, support bar and spine.
    t.clear((35, 2, 12), (36, 4, 14))
    t.clear((35, 2, 23), (36, 5, 25))
    t.clear((35, 2, 29), (36, 5, 31))


def _roof_service_anatomy(t: base.Template) -> None:
    # Three plant housings align to the three cells and physically sit on the
    # rear service spine; a longitudinal header connects them.
    for x1, x2, floor_y, top_y in ((6, 12, 11, 15), (17, 23, 13, 17), (28, 34, 12, 16)):
        _shell(
            t,
            (x1, floor_y, 28),
            (x2, top_y, 33),
            "immersiveengineering:sheetmetal_steel",
            "tfmg:steel_block",
        )
        t.fill((x1 + 1, floor_y + 1, 27), (x2 - 1, top_y - 1, 27), "create:framed_glass")
    t.fill((8, 14, 32), (32, 15, 33), "minecraft:orange_concrete")

    # Integrated roadside blade grows from the tall center cell and front frame.
    t.fill((12, 12, 6), (29, 14, 7), "tfmg:steel_block")
    t.fill((14, 13, 5), (27, 16, 6), "minecraft:orange_concrete")
    t.fill((18, 14, 4), (23, 16, 5), "minecraft:polished_blackstone")


def build_gate_a_massing() -> base.Template:
    t = base.Template((49, 18, 41))
    _site_and_thresholds(t)
    _three_cell_hall(t)
    _customer_and_support_bars(t)
    _roof_service_anatomy(t)
    return t


def _assert_contracts(t: base.Template) -> None:
    if tuple(t.size) != (49, 18, 41):
        raise AssertionError(f"OWS-009 Gate-A dimensions drifted: {t.size}")

    # Each front threshold must retain a five-plus-block clear opening.
    for x1, x2, top in ((5, 12, 6), (16, 23, 7), (27, 33, 6)):
        for x in range(x1, x2 + 1):
            for y in range(2, top + 1):
                if _name(t, (x, y, 7)) not in AIR:
                    raise AssertionError(f"service threshold obstruction at {(x, y, 7)}")

    # Protected movement and technician fields remain open at player height.
    for x1, x2, z1, z2, label in (
        (4, 34, 24, 27, "transverse movement field"),
        (4, 34, 28, 31, "rear technician spine"),
    ):
        for x in range(x1, x2 + 1):
            for z in range(z1, z2 + 1):
                for y in (2, 3):
                    if _name(t, (x, y, z)) not in AIR:
                        raise AssertionError(f"{label} obstruction at {(x, y, z)}")

    frozen = {
        (5, 0, 3): "minecraft:yellow_concrete",          # recovery lane
        (4, 7, 7): "minecraft:orange_concrete",          # Cell 01 frame
        (15, 8, 7): "minecraft:orange_concrete",         # Cell 02 frame
        (26, 7, 7): "minecraft:orange_concrete",         # Cell 03 frame
        (38, 4, 7): "create:framed_glass",               # customer bar
        (44, 4, 23): "minecraft:air",                    # parts receiving threshold
        (40, 8, 28): "create:framed_glass",              # records/proof adjacency
        (20, 14, 32): "minecraft:orange_concrete",       # connected plant header
        (20, 15, 5): "minecraft:polished_blackstone",    # integrated Atlas blade
    }
    for pos, expected in frozen.items():
        actual = _name(t, pos)
        if actual != expected:
            raise AssertionError(f"OWS-009 Gate-A aspect drift at {pos}: {actual} != {expected}")

    names = [_name(t, pos) for pos in t.blocks]
    forbidden = {"minecraft:chest", "minecraft:trapped_chest", "minecraft:spawner", "create:mechanical_press", "create:depot"}
    if forbidden.intersection(names):
        raise AssertionError("OWS-009 Gate-A contains deferred gameplay/operational blocks")


def _git_blob(path: Path) -> str:
    return subprocess.run(
        ["git", "hash-object", str(path.relative_to(ROOT))],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def main() -> None:
    from render_old_world_heavy_rebuild_review import render_review_set
    from render_structure_review import unpack_structure

    review_dir = ROOT / "old_world_narrative/reviews/heavy_rebuild"
    missing = [name for name in REQUIRED_RECORDS if not (review_dir / name).is_file()]
    if missing:
        raise AssertionError(f"OWS-009 Gate-A prerequisites missing: {missing}")
    baseline_review = (review_dir / "OWS-009_PHASE0_BASELINE_REVIEW.md").read_text(encoding="utf-8")
    if "BASELINE SUFFICIENT. REBUILD REQUIRED." not in baseline_review:
        raise AssertionError("OWS-009 independent Phase-0 disposition is missing")

    source_bytes = SOURCE_PATH.read_bytes()
    if hashlib.sha256(source_bytes).hexdigest() != FROZEN_SOURCE_SHA256:
        raise AssertionError("OWS-009 shipping NBT changed during Gate-A authoring")
    if _git_blob(SOURCE_PATH) != FROZEN_SOURCE_BLOB:
        raise AssertionError("OWS-009 shipping Git provenance drifted")

    t = build_gate_a_massing()
    _assert_contracts(t)
    t.save(TEMP_NAME)
    try:
        model_bytes = TEMP_NBT.read_bytes()
        size, blocks = unpack_structure(TEMP_NBT)
        revision = os.environ.get("GITHUB_SHA", "local")[:8]
        manifest = render_review_set(
            target=TARGET,
            gate="gate_a_massing",
            revision=f"massing-r1@{revision}",
            damage_state="D0 intact massing only",
            source_commit=os.environ.get("GITHUB_SHA", "working-tree"),
            source_path="review-only:render_ows009_gate_a_massing.build_gate_a_massing()",
            size=size,
            blocks=blocks,
            output_dir=OUTPUT_DIR,
            camera_set="ows009_fixed_v1",
        )
        manifest.update({
            "review_model_nbt_sha256": hashlib.sha256(model_bytes).hexdigest(),
            "review_builder_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "phase0_source_sha256": FROZEN_SOURCE_SHA256,
            "phase0_source_git_blob": FROZEN_SOURCE_BLOB,
            "phase0_shipping_untouched": SOURCE_PATH.read_bytes() == source_bytes,
            "programmed_massing_aspects_asserted": 9,
            "pass7_plus_content_present": False,
            "visual_review_status": "rendered_pending_independent_review",
            "authoritative_shipping_modified": False,
        })
        (OUTPUT_DIR / "review_manifest.json").write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n"
        )
    finally:
        TEMP_NBT.unlink(missing_ok=True)

    if SOURCE_PATH.read_bytes() != source_bytes:
        raise AssertionError("OWS-009 shipping changed while rendering Gate A")
    print(
        f"Rendered OWS-009 Gate-A r1 at {manifest['dimensions']} with "
        f"{manifest['fixed_camera_set']}; independent review required."
    )


if __name__ == "__main__":
    main()
