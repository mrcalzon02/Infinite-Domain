#!/usr/bin/env python3
"""Build and render the review-only OWS-009 Gate-A r2 massing study."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path

import generate_wasteland_sites as base


ROOT = Path(__file__).resolve().parents[2]
TARGET = "OWS-009"
SOURCE_PATH = ROOT / "kubejs/data/infinite_domain/structure/wasteland/old_world/ows_009_atlas_roadside_repair_depot.nbt"
FROZEN_SOURCE_SHA256 = "d80dfca574d8f96eca633ac515e810f02f52e7eab2f36195977b42708068fe0d"
FROZEN_SOURCE_BLOB = "4b2df6f6d8bcb5a58511318f0fe78f9f5fc1d44a"
TEMP_NAME = "_heavy_review_ows009_gate_a_massing_r2"
TEMP_NBT = ROOT / "kubejs/data/infinite_domain/structure/wasteland" / f"{TEMP_NAME}.nbt"
OUTPUT_DIR = ROOT / "dev/old_world_narrative/reviews/heavy_rebuild/visual/OWS-009/gate_a_massing/r2"
REQUIRED_RECORDS = (
    "OWS-009_PHASE0_BASELINE_REVIEW.md",
    "OWS-009_PASS2_FUNCTIONAL_DEFINITION.md",
    "OWS-009_PASS3_PRECEDENT_RESEARCH.md",
    "OWS-009_PASS4_PROGRAM_ADJACENCY.md",
    "OWS-009_PASS5_SCALE_TRANSLATION.md",
    "OWS-009_GATE_A_R1_REVIEW.md",
)
AIR = {None, "minecraft:air", "minecraft:cave_air", "minecraft:void_air", "minecraft:structure_void"}
HARDSCAPE = {
    "tfmg:asphalt",
    "minecraft:light_gray_concrete",
    "minecraft:white_concrete",
    "minecraft:yellow_concrete",
    "minecraft:smooth_stone",
}


def _name(t: base.Template, pos: tuple[int, int, int]) -> str | None:
    row = t.blocks.get(pos)
    return None if row is None else t.palette[row[0]]["Name"]


def _shell(t: base.Template, a: tuple[int, int, int], b: tuple[int, int, int], wall: str, roof: str) -> None:
    base.shell(t, a, b, wall, "tfmg:factory_floor", roof)


def _site_and_thresholds(t: base.Template) -> None:
    # The outermost north/east/rear cells are deliberately retained as natural
    # transition capacity. They are not decorative margins: later placement
    # work may consume them for bounded drainage, ramps or retaining treatment.
    t.fill((0, 0, 0), (48, 0, 40), "minecraft:grass_block")

    # Road-facing recovery apron. Z0 remains a protected transition edge; the
    # two-block Z0-1 band can absorb grade/drainage without cutting service lanes.
    t.fill((1, 0, 2), (35, 0, 7), "tfmg:asphalt")
    for x1, x2 in ((5, 13), (15, 24), (26, 34)):
        t.fill((x1, 0, 2), (x2, 0, 6), "minecraft:light_gray_concrete")
        t.fill((x1, 0, 4), (x2, 0, 4), "minecraft:yellow_concrete")

    # Public circulation is separated from recovery traffic and also stops
    # short of the protected north edge.
    t.fill((36, 0, 2), (43, 0, 19), "minecraft:smooth_stone")
    t.fill((38, 0, 2), (42, 0, 7), "minecraft:white_concrete")

    # Parts-delivery / core-return maneuvering runs along the east side but
    # retains X48 as a seam-control strip and Z40 as rear transition capacity.
    t.fill((44, 0, 18), (47, 0, 39), "tfmg:asphalt")
    t.fill((36, 0, 35), (43, 0, 39), "minecraft:coarse_dirt")
    t.fill((36, 0, 35), (43, 0, 35), "minecraft:yellow_concrete")


def _three_cell_hall(t: base.Template) -> None:
    # Three visibly different repair cells preserve the original program while
    # replacing the donor-garage silhouette with an Atlas industrial hierarchy.
    _shell(t, (3, 1, 7), (14, 11, 34), "tfmg:cinder_block", "minecraft:smooth_stone")
    _shell(t, (14, 1, 7), (25, 13, 34), "minecraft:light_gray_concrete", "minecraft:smooth_stone")
    _shell(t, (25, 1, 7), (35, 12, 34), "tfmg:cinder_block", "minecraft:smooth_stone")

    # Shared shell walls are opened to one operational hall; structural piers
    # remain at the cell lines rather than leaving unsupported clear spans.
    t.clear((14, 2, 9), (14, 9, 31))
    t.clear((25, 2, 9), (25, 9, 31))
    for x in (14, 25):
        t.fill((x, 1, 8), (x, 10, 9), "tfmg:steel_block")
        t.fill((x, 1, 31), (x, 10, 33), "tfmg:steel_block")

    # Distinct service thresholds: diagnostic cell is lower and recessed,
    # heavy intervention is tallest/deepest, recommissioning has a projecting
    # canopy. The three frames no longer read as copied garage doors.
    thresholds = (
        (5, 12, 6, 6, 8),
        (16, 23, 8, 5, 8),
        (27, 33, 7, 6, 9),
    )
    for x1, x2, top, frame_z1, frame_z2 in thresholds:
        t.clear((x1, 2, 7), (x2, top, 8))
        t.fill((x1 - 1, 1, frame_z1), (x1 - 1, top + 2, frame_z2), "tfmg:steel_block")
        t.fill((x2 + 1, 1, frame_z1), (x2 + 1, top + 2, frame_z2), "tfmg:steel_block")
        t.fill((x1 - 1, top + 1, frame_z1), (x2 + 1, top + 2, frame_z2), "minecraft:orange_concrete")
    t.fill((26, 8, 5), (34, 9, 6), "tfmg:steel_block")
    t.fill((28, 9, 4), (32, 9, 6), "minecraft:orange_concrete")

    # Cell floor zoning, transverse movement field and rear technician spine.
    for x1, x2 in ((5, 13), (15, 24), (26, 34)):
        t.fill((x1, 1, 9), (x2, 1, 23), "minecraft:smooth_stone")
        t.fill((x1, 1, 9), (x1, 1, 23), "minecraft:orange_concrete")
        t.fill((x2, 1, 9), (x2, 1, 23), "minecraft:orange_concrete")
    t.fill((4, 1, 24), (35, 1, 27), "minecraft:light_gray_concrete")
    t.fill((4, 1, 28), (35, 1, 31), "minecraft:polished_blackstone")

    # Bay-aligned facade depth breaks the long side and rear planes into
    # credible structural modules. Nothing here is Pass-7 machinery/detail.
    for z in (10, 17, 24, 31):
        t.fill((2, 1, z), (3, 8, z + 1), "tfmg:steel_block")
        t.fill((35, 1, z), (36, 8, z + 1), "tfmg:steel_block")
    for x in (5, 13, 17, 23, 28, 34):
        t.fill((x, 1, 34), (x + 1, 7, 35), "tfmg:steel_block")

    # Clerestories are separated into modules instead of continuous glass bands.
    for z1, z2 in ((10, 14), (18, 22)):
        t.fill((3, 7, z1), (3, 9, z2), "create:framed_glass")
        t.fill((35, 8, z1), (35, 10, z2), "create:framed_glass")
    t.fill((17, 10, 7), (22, 11, 7), "create:framed_glass")
    for x1, x2, y in ((6, 11, 8), (17, 22, 10), (28, 32, 9)):
        t.fill((x1, y, 34), (x2, y + 1, 34), "create:framed_glass")

    # Roof monitors reinforce three different work-cell profiles and create
    # construction-readable roof anatomy rather than a flat stepped lid.
    _shell(t, (6, 11, 15), (12, 14, 26), "immersiveengineering:sheetmetal_steel", "tfmg:steel_block")
    _shell(t, (17, 13, 13), (23, 17, 27), "immersiveengineering:sheetmetal_steel", "tfmg:steel_block")
    _shell(t, (28, 12, 16), (33, 15, 25), "immersiveengineering:sheetmetal_steel", "tfmg:steel_block")
    t.fill((7, 12, 15), (11, 13, 15), "create:framed_glass")
    t.fill((18, 14, 13), (22, 16, 13), "create:framed_glass")
    t.fill((29, 13, 16), (32, 14, 16), "create:framed_glass")


def _customer_and_support_bars(t: base.Template) -> None:
    # Human-scale public/service bar remains distinct from vehicle recovery.
    _shell(t, (36, 1, 7), (43, 9, 19), "minecraft:white_concrete", "minecraft:light_gray_concrete")
    t.fill((37, 3, 7), (42, 6, 7), "create:framed_glass")
    t.fill((36, 3, 9), (36, 6, 17), "create:framed_glass")
    t.clear((38, 2, 7), (41, 5, 8))
    t.fill((37, 7, 6), (43, 8, 8), "minecraft:orange_concrete")

    # Parts receive/issue and secure calibrator-records functions are stepped
    # westward one block to preserve a four-block east maneuvering lane plus
    # the protected X48 terrain seam.
    _shell(t, (36, 1, 20), (43, 10, 27), "immersiveengineering:sheetmetal_steel", "tfmg:steel_block")
    _shell(t, (36, 1, 27), (43, 11, 34), "minecraft:polished_blackstone_bricks", "tfmg:steel_block")
    t.clear((43, 2, 22), (43, 6, 25))
    t.fill((43, 1, 21), (43, 8, 21), "minecraft:orange_concrete")
    t.fill((43, 1, 27), (43, 8, 27), "minecraft:orange_concrete")
    t.fill((37, 7, 28), (42, 9, 28), "create:framed_glass")

    # Core/rework return gets a distinct rear threshold and canopy so it cannot
    # be mistaken for incoming parts-delivery circulation.
    t.clear((38, 2, 34), (41, 5, 34))
    t.fill((37, 6, 34), (42, 7, 36), "tfmg:steel_block")
    t.fill((38, 7, 35), (41, 7, 36), "minecraft:orange_concrete")

    # Controlled internal thresholds connect service/support bars to the spine.
    t.clear((35, 2, 12), (36, 4, 14))
    t.clear((35, 2, 23), (36, 5, 25))
    t.clear((35, 2, 29), (36, 5, 31))


def _roof_service_anatomy(t: base.Template) -> None:
    # Cell-aligned plant housings sit over the technician/service zone and are
    # connected by a physical header. Differing heights echo the work-cell roof
    # hierarchy rather than repeating identical rooftop boxes.
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

    # Atlas identity is architectural: a load-bearing-looking charcoal/orange
    # blade is tied into the center cell and frame rather than applied as signage.
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

    # Protected terrain/seam edges may not contain hardscape. These assertions
    # make the r1 boundary-touching defect mechanically non-regressible.
    for x in range(49):
        if _name(t, (x, 0, 0)) in HARDSCAPE:
            raise AssertionError(f"north terrain-transition edge paved at {(x, 0, 0)}")
    for z in range(41):
        if _name(t, (48, 0, z)) in HARDSCAPE:
            raise AssertionError(f"east terrain-transition edge paved at {(48, 0, z)}")
    for x in range(49):
        if _name(t, (x, 0, 40)) in HARDSCAPE:
            raise AssertionError(f"rear terrain-transition edge paved at {(x, 0, 40)}")

    # Four-block east service maneuvering corridor must survive between annex
    # wall and protected terrain edge.
    for x in range(44, 48):
        for z in range(18, 40):
            if _name(t, (x, 0, z)) != "tfmg:asphalt":
                raise AssertionError(f"east service maneuvering lane discontinuity at {(x, 0, z)}")

    # Each vehicle threshold must retain its specified clear opening.
    for x1, x2, top in ((5, 12, 6), (16, 23, 8), (27, 33, 7)):
        for x in range(x1, x2 + 1):
            for y in range(2, top + 1):
                if _name(t, (x, y, 7)) not in AIR:
                    raise AssertionError(f"service threshold obstruction at {(x, y, 7)}")

    # Protected transverse movement and technician fields remain open at player height.
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
        (5, 0, 4): "minecraft:yellow_concrete",          # recovery lane
        (4, 7, 7): "minecraft:orange_concrete",          # Cell 01 frame
        (15, 9, 7): "minecraft:orange_concrete",         # Cell 02 frame
        (26, 8, 7): "minecraft:orange_concrete",         # Cell 03 frame
        (38, 4, 7): "create:framed_glass",               # customer bar
        (43, 4, 23): "minecraft:air",                    # parts receiving threshold
        (40, 8, 28): "create:framed_glass",              # records/proof adjacency
        (39, 4, 34): "minecraft:air",                    # distinct core-return threshold
        (20, 14, 32): "minecraft:orange_concrete",       # connected plant header
        (20, 15, 5): "minecraft:polished_blackstone",    # integrated Atlas blade
        (48, 0, 25): "minecraft:grass_block",            # east seam-control strip
        (20, 0, 0): "minecraft:grass_block",             # north transition strip
    }
    for pos, expected in frozen.items():
        actual = _name(t, pos)
        if actual != expected:
            raise AssertionError(f"OWS-009 Gate-A aspect drift at {pos}: {actual} != {expected}")

    names = [_name(t, pos) for pos in t.blocks]
    forbidden = {
        "minecraft:chest",
        "minecraft:trapped_chest",
        "minecraft:spawner",
        "create:mechanical_press",
        "create:depot",
    }
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

    review_dir = ROOT / "dev/old_world_narrative/reviews/heavy_rebuild"
    missing = [name for name in REQUIRED_RECORDS if not (review_dir / name).is_file()]
    if missing:
        raise AssertionError(f"OWS-009 Gate-A prerequisites missing: {missing}")
    baseline_review = (review_dir / "OWS-009_PHASE0_BASELINE_REVIEW.md").read_text(encoding="utf-8")
    if "BASELINE SUFFICIENT. REBUILD REQUIRED." not in baseline_review:
        raise AssertionError("OWS-009 independent Phase-0 disposition is missing")
    r1_review = (review_dir / "OWS-009_GATE_A_R1_REVIEW.md").read_text(encoding="utf-8")
    if "OWS-009 GATE A r1: REVISION REQUIRED." not in r1_review:
        raise AssertionError("OWS-009 Gate-A r1 rejection is missing")

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
            revision=f"massing-r2@{revision}",
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
            "programmed_massing_aspects_asserted": 12,
            "protected_transition_edges_asserted": ["north_z0", "east_x48", "rear_z40"],
            "east_service_lane_width_blocks": 4,
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
        f"Rendered OWS-009 Gate-A r2 at {manifest['dimensions']} with "
        f"{manifest['fixed_camera_set']}; independent review required."
    )


if __name__ == "__main__":
    main()
