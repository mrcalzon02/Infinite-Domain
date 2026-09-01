#!/usr/bin/env python3
"""Build and render the narrow OWS-008 Gate-A r2 massing correction.

R2 freezes the accepted r1 command, analysis, stepped composition, hero hall,
cyan treatment language, and upper connector. It revises only treatment roof
profiles, service-joint expression, rear plant, intake/exhaust, and threshold
architecture. It never writes shared state or authoritative shipping NBT.
"""
from __future__ import annotations

import gzip
import hashlib
import json
import os
import subprocess
from pathlib import Path

import generate_wasteland_sites as base
import render_ows008_gate_a_massing as r1
from render_old_world_heavy_rebuild_review import OUTPUT_ROOT, ROOT, render_review_set
from render_structure_review import unpack_structure


TEMP_NAME = "_heavy_review_ows008_gate_a_massing_r2"
TEMP_NBT = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{TEMP_NAME}.nbt"
OUTPUT_DIR = OUTPUT_ROOT / "OWS-008" / "gate_a_massing" / "r2"
SHIPPING_PATH = (
    ROOT
    / "kubejs"
    / "data"
    / "infinite_domain"
    / "structure"
    / "wasteland"
    / "old_world"
    / "ows_008_vcf_emergency_persistence_investigation_lab.nbt"
)
R1_BUILDER_PATH = ROOT / "dev/scripts" / "render_ows008_gate_a_massing.py"
R1_BUILDER_SHA256 = "252a7898afba6d8cd6cfe76aa84ef398765e1c612ea8f3112aa62f27bbe20d81"
R1_MODEL_SHA256 = "23d7bc96c3f3ade8566aedad0c7d3a731cf4eeac55c9adcd365ed295ca59f361"


def _treatment_and_verification_array_r2(t: base.Template) -> None:
    """Keep the r1 family while giving each revision a causal roof profile."""
    modules = (
        # wash/chemical cell: broad, low cycle hood
        ((20, 1, 11), (32, 10, 22), 7, "minecraft:cyan_concrete"),
        # heat/steam cell: thicker, taller chamber
        ((31, 1, 12), (44, 12, 23), 9, "minecraft:cyan_concrete"),
        # air/filter intervention: long horizontal environmental cell
        ((22, 1, 21), (35, 11, 32), 8, "minecraft:cyan_concrete"),
        # combined-procedure revision: largest emergency retrofit
        ((34, 1, 22), (50, 13, 35), 10, "minecraft:cyan_concrete"),
    )

    for lo, hi, datum_y, datum_block in modules:
        base.shell(
            t,
            lo,
            hi,
            "minecraft:white_concrete",
            "minecraft:smooth_stone",
            "minecraft:light_gray_concrete",
        )
        x1, _, z1 = lo
        x2, _, z2 = hi
        t.fill((x1, 3, z1 + 2), (x1, min(datum_y, hi[1] - 2), z2 - 2), "create:framed_glass")
        t.fill((x1, datum_y, z1), (x2, datum_y + 1, z1), datum_block)

    # Freeze the broad upper observation connector and cyan family language.
    base.shell(
        t,
        (17, 7, 15),
        (25, 13, 35),
        "minecraft:white_concrete",
        "minecraft:smooth_stone",
        "minecraft:light_gray_concrete",
    )
    t.fill((25, 8, 17), (25, 11, 33), "create:framed_glass")
    t.fill((18, 8, 14), (24, 11, 14), "create:framed_glass")

    # Wash/chemical: a low set-back hood with a visible rear service shoulder.
    base.shell(
        t,
        (22, 10, 13),
        (29, 13, 20),
        "minecraft:white_concrete",
        "minecraft:smooth_stone",
        "minecraft:light_gray_concrete",
    )
    t.fill((23, 12, 12), (28, 13, 12), "minecraft:cyan_concrete")
    t.fill((28, 11, 20), (31, 13, 22), "immersiveengineering:sheetmetal_steel")

    # Heat/steam: a tall, compact plenum supported directly by the chamber.
    base.shell(
        t,
        (34, 12, 14),
        (41, 17, 21),
        "immersiveengineering:sheetmetal_steel",
        "minecraft:smooth_stone",
        "minecraft:light_gray_concrete",
    )
    for x in (34, 41):
        t.fill((x, 10, 15), (x, 16, 20), "minecraft:white_concrete")

    # Air/filter: a wide horizontal plenum and smaller raised filter monitor.
    base.shell(
        t,
        (24, 11, 23),
        (33, 14, 31),
        "minecraft:white_concrete",
        "minecraft:smooth_stone",
        "minecraft:light_gray_concrete",
    )
    base.shell(
        t,
        (27, 14, 25),
        (33, 16, 29),
        "create:framed_glass",
        "minecraft:smooth_stone",
        "minecraft:white_concrete",
    )
    t.fill((23, 12, 24), (23, 13, 30), "minecraft:cyan_concrete")

    # Combined revision: a two-tier retrofit aligned to the final treatment
    # volume and connected toward the supported controlled-exhaust tower.
    base.shell(
        t,
        (38, 13, 25),
        (48, 17, 34),
        "immersiveengineering:sheetmetal_steel",
        "minecraft:smooth_stone",
        "minecraft:light_gray_concrete",
    )
    base.shell(
        t,
        (41, 17, 27),
        (47, 19, 33),
        "minecraft:white_concrete",
        "minecraft:smooth_stone",
        "minecraft:light_gray_concrete",
    )
    t.fill((46, 15, 32), (51, 17, 35), "immersiveengineering:sheetmetal_steel")


def _persistence_hall_and_joint_gallery_r2(t: base.Template) -> None:
    """Freeze the hero hall and project one continuous technical gallery."""
    base.shell(
        t,
        (20, 1, 29),
        (45, 17, 43),
        "minecraft:white_concrete",
        "minecraft:smooth_stone",
        "minecraft:light_gray_concrete",
    )
    t.fill((23, 5, 28), (40, 12, 28), "create:framed_glass")
    t.fill((19, 4, 32), (19, 12, 39), "create:framed_glass")

    base.shell(
        t,
        (24, 17, 32),
        (40, 20, 40),
        "create:framed_glass",
        "minecraft:light_gray_concrete",
        "minecraft:white_concrete",
    )

    # The service-joint gallery now reads as one projected technical bar from
    # the final treatment revision through the challenge hall into rear plant.
    base.shell(
        t,
        (43, 1, 26),
        (52, 12, 44),
        "immersiveengineering:sheetmetal_steel",
        "minecraft:smooth_stone",
        "minecraft:light_gray_concrete",
    )
    for z in (27, 33, 39, 44):
        t.fill((42, 1, z), (43, 13, z), "minecraft:white_concrete")
    t.fill((42, 7, 27), (42, 9, 43), "minecraft:cyan_concrete")


def _rear_plant_and_thresholds_r2(t: base.Template) -> None:
    """Consolidate plant and distinguish all technical thresholds by form."""
    # One continuous rear technical backbone ties plant, gallery, maintenance,
    # waste and the exhaust base into a single supported composition.
    base.shell(
        t,
        (3, 1, 38),
        (52, 10, 47),
        "minecraft:light_gray_concrete",
        "tfmg:factory_floor",
        "minecraft:white_concrete",
    )

    # Main plant and lower transfer plenum share a roof datum and overlap in a
    # deliberate hinge, replacing r1's scattered cap-like boxes.
    base.shell(
        t,
        (8, 10, 39),
        (30, 16, 47),
        "immersiveengineering:sheetmetal_steel",
        "minecraft:smooth_stone",
        "minecraft:light_gray_concrete",
    )
    base.shell(
        t,
        (28, 10, 40),
        (43, 13, 46),
        "immersiveengineering:sheetmetal_steel",
        "minecraft:smooth_stone",
        "minecraft:light_gray_concrete",
    )

    # Low west clean-air intake: broad, horizontal and visibly connected to
    # the rear plant, with no silhouette resemblance to the tall exhaust.
    base.shell(
        t,
        (2, 7, 33),
        (10, 13, 41),
        "minecraft:white_concrete",
        "minecraft:smooth_stone",
        "minecraft:light_gray_concrete",
    )
    t.fill((1, 9, 35), (1, 12, 39), "create:framed_glass")
    t.fill((3, 12, 32), (9, 13, 32), "minecraft:cyan_concrete")

    # Tall controlled exhaust is now a fully supported shaft growing from the
    # continuous gallery/rear-plant base. The r1 floating cap is removed.
    base.shell(
        t,
        (44, 10, 37),
        (51, 15, 44),
        "tfmg:steel_block",
        "minecraft:smooth_stone",
        "immersiveengineering:sheetmetal_steel",
    )
    base.shell(
        t,
        (46, 15, 39),
        (49, 21, 42),
        "tfmg:steel_block",
        "minecraft:smooth_stone",
        "immersiveengineering:sheetmetal_steel",
    )

    # East sealed-specimen sidecar: deep recess, projected canopy and paired
    # supports distinguish it from all south-facing service thresholds.
    base.shell(
        t,
        (47, 1, 8),
        (53, 8, 20),
        "minecraft:white_concrete",
        "minecraft:smooth_stone",
        "minecraft:light_gray_concrete",
    )
    t.clear((51, 2, 12), (53, 6, 16))
    t.fill((50, 7, 10), (54, 9, 18), "tfmg:steel_block")
    for z in (10, 18):
        t.fill((53, 1, z), (53, 7, z), "minecraft:white_concrete")

    # West maintenance recess: wide protected cart threshold with a supported
    # south canopy directly below the principal plant mass.
    t.clear((7, 2, 45), (15, 7, 47))
    t.fill((6, 8, 45), (16, 10, 48), "tfmg:steel_block")
    for x in (6, 16):
        t.fill((x, 1, 48), (x, 8, 48), "minecraft:light_gray_concrete")

    # Treated-waste sidecar: lower and broader than specimen receipt, with a
    # separate deep recess and apron-facing canopy on the east rear court.
    base.shell(
        t,
        (32, 1, 41),
        (45, 9, 47),
        "minecraft:light_gray_concrete",
        "tfmg:factory_floor",
        "minecraft:white_concrete",
    )
    t.clear((35, 2, 45), (42, 6, 47))
    t.fill((34, 7, 45), (43, 9, 48), "minecraft:white_concrete")
    for x in (34, 43):
        t.fill((x, 1, 48), (x, 7, 48), "tfmg:steel_block")

    # Independent west emergency-egress sidecar uses a small human-scale
    # recess and lateral canopy, physically unlike cart or waste openings.
    base.shell(
        t,
        (1, 1, 30),
        (8, 7, 38),
        "minecraft:white_concrete",
        "minecraft:smooth_stone",
        "minecraft:light_gray_concrete",
    )
    t.clear((1, 2, 33), (2, 5, 35))
    t.fill((0, 6, 31), (3, 8, 37), "minecraft:white_concrete")
    for z in (31, 37):
        t.fill((0, 1, z), (0, 6, z), "minecraft:light_gray_concrete")
    t.fill((0, 0, 32), (3, 0, 36), "minecraft:smooth_stone")


def build_gate_a_massing_r2() -> base.Template:
    t = base.Template((55, 22, 49))
    r1._site_and_thresholds(t)
    r1._incident_command_threshold(t)
    r1._analysis_wing(t)
    _treatment_and_verification_array_r2(t)
    _persistence_hall_and_joint_gallery_r2(t)
    _rear_plant_and_thresholds_r2(t)
    return t


def git_hash_object(path: Path) -> str:
    result = subprocess.run(
        ["git", "hash-object", str(path.relative_to(ROOT))],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def main() -> None:
    r1_builder_hash = hashlib.sha256(R1_BUILDER_PATH.read_bytes()).hexdigest()
    if r1_builder_hash != R1_BUILDER_SHA256:
        raise AssertionError("OWS-008 r1 builder drifted; frozen comparison is no longer reproducible")

    shipping_before = git_hash_object(SHIPPING_PATH)
    t = build_gate_a_massing_r2()
    if tuple(t.size) != (55, 22, 49):
        raise AssertionError(f"OWS-008 Gate-A r2 dimensions changed unexpectedly: {t.size}")
    if len(t.blocks) < 9000:
        raise AssertionError("OWS-008 Gate-A r2 massing is unexpectedly sparse")
    if any(not (0 <= x < 55 and 0 <= y < 22 and 0 <= z < 49) for x, y, z in t.blocks):
        raise AssertionError("OWS-008 Gate-A r2 massing exceeds the retained review envelope")

    TEMP_NBT.unlink(missing_ok=True)
    t.save(TEMP_NAME)
    try:
        model_bytes = TEMP_NBT.read_bytes()
        model_hash = hashlib.sha256(model_bytes).hexdigest()
        model_decompressed_hash = hashlib.sha256(gzip.decompress(model_bytes)).hexdigest()
        if model_hash == R1_MODEL_SHA256:
            raise AssertionError("OWS-008 Gate-A r2 did not change from revision-required r1")
        size, blocks = unpack_structure(TEMP_NBT)
        if tuple(size) != (55, 22, 49):
            raise AssertionError(f"Serialized r2 review model has unexpected size: {size}")

        revision = os.environ.get("GITHUB_SHA", "local")[:8]
        manifest = render_review_set(
            target="OWS-008",
            gate="gate_a_massing",
            revision=f"massing-r2@{revision}",
            damage_state="D0 intact massing only",
            source_commit=os.environ.get("GITHUB_SHA", "working-tree"),
            source_path="review-only:render_ows008_gate_a_massing_r2.build_gate_a_massing_r2()",
            size=size,
            blocks=blocks,
            output_dir=OUTPUT_DIR,
            camera_set="ows008_fixed_v1",
        )
        used_names = [t.palette[state_index]["Name"] for state_index, _ in t.blocks.values()]
        manifest["review_model_nbt_sha256"] = model_hash
        manifest["review_model_decompressed_nbt_sha256"] = model_decompressed_hash
        manifest["review_builder_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        manifest["frozen_r1_builder_sha256"] = r1_builder_hash
        manifest["revision_required_r1_model_sha256"] = R1_MODEL_SHA256
        manifest["review_model_block_positions"] = len(t.blocks)
        manifest["review_model_non_air_positions"] = sum(name != "minecraft:air" for name in used_names)
        manifest["review_model_explicit_air_positions"] = sum(name == "minecraft:air" for name in used_names)
        manifest["review_model_palette_states"] = len(t.palette)
        manifest["review_model_block_entities"] = sum(nbt is not None for _, nbt in t.blocks.values())
        manifest["review_model_entities"] = len(t.entities)
        manifest["authoritative_shipping_modified"] = False
        manifest["shipping_nbt_git_blob_before"] = shipping_before
        manifest["shipping_nbt_git_blob_after"] = git_hash_object(SHIPPING_PATH)
        if manifest["shipping_nbt_git_blob_after"] != shipping_before:
            raise AssertionError("OWS-008 shipping NBT changed during r2 review-only rendering")
        (OUTPUT_DIR / "review_manifest.json").write_text(
            json.dumps(manifest, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    finally:
        TEMP_NBT.unlink(missing_ok=True)

    print(
        f"Rendered OWS-008 Gate A r2 correction at {manifest['dimensions']} using "
        f"{manifest['fixed_camera_set']}; independent visual approval remains pending."
    )


if __name__ == "__main__":
    main()
