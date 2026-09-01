#!/usr/bin/env python3
"""Build and render the review-only OWS-007 Gate-A r1 massing candidate.

The model proves the public/trial/service/rotunda hierarchy before structure,
circulation, operational equipment, proof loot, history, damage, encounters, or
microdetail are added. It never writes shared state or authoritative shipping NBT.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import subprocess
from pathlib import Path

import generate_wasteland_sites as base
from render_old_world_heavy_rebuild_review import OUTPUT_ROOT, ROOT, render_review_set
from render_structure_review import unpack_structure


TEMP_NAME = "_heavy_review_ows007_gate_a_massing_r1"
TEMP_NBT = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{TEMP_NAME}.nbt"
OUTPUT_DIR = OUTPUT_ROOT / "OWS-007" / "gate_a_massing" / "r1"
SHIPPING_PATH = (
    ROOT
    / "kubejs"
    / "data"
    / "infinite_domain"
    / "structure"
    / "wasteland"
    / "old_world"
    / "ows_007_vcf_ep7_agricultural_development_laboratory.nbt"
)


def _site_and_public_threshold(t: base.Template) -> None:
    """Establish a public north face and a separate south service court."""
    t.fill((1, 0, 1), (71, 0, 61), "minecraft:grass_block")

    # Public forecourt and arrival axis remain separate from all vehicle/service
    # surfaces. Lime strips are site-scale identity, not detailed signage.
    t.fill((8, 0, 1), (46, 0, 10), "minecraft:smooth_stone")
    t.fill((22, 0, 0), (29, 0, 13), "minecraft:white_concrete")
    for x in (10, 44):
        t.fill((x, 0, 2), (x, 0, 9), "minecraft:lime_concrete")

    # Rear sample/service court reserves distinct clean receiving and waste
    # thresholds without entering downstream room design.
    t.fill((2, 0, 52), (48, 0, 61), "tfmg:asphalt")
    t.fill((49, 0, 49), (71, 0, 61), "minecraft:light_gray_concrete")
    for x in (7, 18, 31, 42, 55, 66):
        t.fill((x, 0, 56), (x, 0, 61), "minecraft:white_concrete")

    # Transparent, human-scaled public/research bar.
    base.shell(
        t,
        (7, 1, 6),
        (43, 9, 16),
        "minecraft:white_concrete",
        "minecraft:smooth_stone",
        "minecraft:light_gray_concrete",
    )
    t.fill((11, 2, 5), (39, 7, 5), "create:framed_glass")
    t.clear((21, 2, 5), (28, 6, 6))
    t.fill((12, 8, 5), (38, 9, 5), "minecraft:lime_concrete")

    # Supported institutional canopy and raised public observation lantern.
    t.fill((16, 9, 1), (34, 9, 7), "minecraft:white_concrete")
    for x in (16, 34):
        t.fill((x, 1, 2), (x, 8, 2), "minecraft:light_gray_concrete")
    base.shell(
        t,
        (15, 9, 8),
        (36, 13, 15),
        "create:framed_glass",
        "minecraft:light_gray_concrete",
        "minecraft:white_concrete",
    )


def _controlled_trial_wing(t: base.Template) -> None:
    """Create a repeatable but stepped reference/stress chamber family."""
    chambers = (
        ((5, 1, 15), (17, 15, 44), 15, 10),
        ((17, 1, 13), (30, 18, 46), 18, 12),
        ((30, 1, 16), (42, 16, 43), 16, 11),
    )
    for lo, hi, roof_y, band_y in chambers:
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

        # North observation glazing and south technical belt correspond to real
        # chamber faces; neither wraps indiscriminately around the building.
        t.fill((x1 + 2, 4, z1 - 1), (x2 - 2, 9, z1 - 1), "create:framed_glass")
        t.fill((x1, band_y, z2 + 1), (x2, band_y + 1, z2 + 1), "minecraft:cyan_concrete")
        for x in (x1, x2):
            t.fill((x, 1, z1 - 1), (x, roof_y, z1 - 1), "minecraft:light_gray_concrete")

    # Greenhouse/climate monitors give each chamber a controlled-environment
    # identity and replace the donor's anonymous flat roof strips.
    monitors = (
        ((8, 15, 21), (15, 19, 38)),
        ((20, 18, 19), (28, 23, 40)),
        ((32, 16, 21), (40, 21, 37)),
    )
    for lo, hi in monitors:
        base.shell(
            t,
            lo,
            hi,
            "create:framed_glass",
            "minecraft:light_gray_concrete",
            "minecraft:white_concrete",
        )
        x1, y1, z1 = lo
        x2, y2, z2 = hi
        t.fill((x1, y2, z1 - 1), (x2, y2, z1 - 1), "minecraft:lime_concrete")
        t.fill((x1, y1, z2 + 1), (x2, y1 + 1, z2 + 1), "minecraft:cyan_concrete")


def _phenotyping_and_service_hinge(t: base.Template) -> None:
    """Link trial chambers to reseeding, receiving, and environmental plant."""
    # Transverse phenotyping/reseeding hall closes the experimental loop and
    # forms a deliberate hinge between rectangular chambers and the rotunda.
    base.shell(
        t,
        (7, 1, 40),
        (44, 12, 52),
        "minecraft:white_concrete",
        "tfmg:factory_floor",
        "minecraft:light_gray_concrete",
    )
    t.fill((11, 4, 39), (40, 9, 39), "create:framed_glass")
    base.shell(
        t,
        (13, 12, 43),
        (39, 16, 50),
        "create:framed_glass",
        "minecraft:light_gray_concrete",
        "minecraft:white_concrete",
    )

    # Low south accession/service bar with two distinct large thresholds.
    base.shell(
        t,
        (3, 1, 50),
        (46, 9, 59),
        "minecraft:light_gray_concrete",
        "tfmg:factory_floor",
        "minecraft:white_concrete",
    )
    for x1, x2 in ((7, 17), (31, 39)):
        t.clear((x1, 2, 59), (x2, 7, 59))
        t.fill((x1 - 1, 8, 58), (x2 + 1, 10, 60), "tfmg:steel_block")

    # Continuous west maintenance spine and one coherent roof plant mass.
    base.shell(
        t,
        (2, 1, 18),
        (7, 22, 53),
        "minecraft:light_gray_concrete",
        "minecraft:smooth_stone",
        "minecraft:white_concrete",
    )
    t.fill((1, 4, 22), (1, 19, 48), "create:framed_glass")
    t.fill((4, 12, 42), (15, 21, 52), "immersiveengineering:sheetmetal_steel")
    t.fill((7, 17, 45), (13, 25, 50), "tfmg:steel_block")


def _set_disk(
    t: base.Template,
    cx: int,
    y: int,
    cz: int,
    radius: int,
    block: str,
    *,
    inner_radius: int = -1,
) -> None:
    for dx in range(-radius, radius + 1):
        for dz in range(-radius, radius + 1):
            d2 = dx * dx + dz * dz
            if d2 <= radius * radius and d2 > inner_radius * inner_radius:
                t.set(cx + dx, y, cz + dz, block)


def _durability_rotunda(t: base.Template) -> None:
    """Replace the reactor reading with a glazed agricultural test instrument."""
    cx, cz, radius = 57, 35, 13
    inner = radius - 2

    # Floor and annular observation/mezzanine plates establish usable layers.
    _set_disk(t, cx, 1, cz, radius - 1, "minecraft:smooth_stone")
    _set_disk(t, cx, 12, cz, radius - 1, "minecraft:smooth_stone", inner_radius=5)

    for y in range(1, 23):
        for dx in range(-radius, radius + 1):
            for dz in range(-radius, radius + 1):
                d2 = dx * dx + dz * dz
                if not (inner * inner <= d2 <= radius * radius):
                    continue
                structural_rib = (
                    abs(dx) <= 1
                    or abs(dz) <= 1
                    or abs(abs(dx) - abs(dz)) <= 1
                )
                if y <= 4:
                    block = "minecraft:light_gray_concrete"
                elif y in (10, 11):
                    block = "minecraft:lime_concrete"
                elif structural_rib:
                    block = "minecraft:white_concrete"
                elif y >= 19:
                    block = "minecraft:light_gray_concrete"
                else:
                    block = "create:framed_glass"
                t.set(cx + dx, y, cz + dz, block)

    # Broad observation bridge enters the annular upper level from the trial
    # wing. It is a building volume, not a decorative one-block catwalk.
    base.shell(
        t,
        (38, 8, 29),
        (48, 13, 41),
        "minecraft:white_concrete",
        "minecraft:smooth_stone",
        "minecraft:light_gray_concrete",
    )
    t.fill((39, 9, 28), (47, 12, 28), "create:framed_glass")
    t.fill((39, 9, 42), (47, 12, 42), "create:framed_glass")

    # A flat glazed research crown and asymmetric conditioning cap eliminate
    # the inherited reactor dome while preserving the landmark circular mass.
    _set_disk(t, cx, 23, cz, radius - 1, "create:framed_glass", inner_radius=4)
    for angle in range(0, 360, 45):
        radians = math.radians(angle)
        for step in range(5, radius):
            x = cx + round(math.cos(radians) * step)
            z = cz + round(math.sin(radians) * step)
            t.set(x, 24, z, "minecraft:white_concrete")

    base.shell(
        t,
        (52, 23, 30),
        (62, 29, 40),
        "immersiveengineering:sheetmetal_steel",
        "minecraft:smooth_stone",
        "minecraft:white_concrete",
    )
    t.fill((54, 26, 29), (60, 29, 29), "minecraft:cyan_concrete")
    t.fill((51, 25, 32), (51, 28, 38), "create:framed_glass")
    t.fill((63, 24, 33), (66, 27, 37), "tfmg:steel_block")


def build_gate_a_massing() -> base.Template:
    t = base.Template((73, 33, 63))
    _site_and_public_threshold(t)
    _controlled_trial_wing(t)
    _phenotyping_and_service_hinge(t)
    _durability_rotunda(t)
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
    shipping_before = git_hash_object(SHIPPING_PATH)
    t = build_gate_a_massing()
    if tuple(t.size) != (73, 33, 63):
        raise AssertionError(f"OWS-007 Gate-A r1 dimensions changed unexpectedly: {t.size}")
    if len(t.blocks) < 17000:
        raise AssertionError("Gate-A r1 massing is unexpectedly sparse")
    if any(not (0 <= x < 73 and 0 <= y < 33 and 0 <= z < 63) for x, y, z in t.blocks):
        raise AssertionError("Gate-A r1 massing exceeds the retained review envelope")

    t.save(TEMP_NAME)
    try:
        model_bytes = TEMP_NBT.read_bytes()
        size, blocks = unpack_structure(TEMP_NBT)
        revision = os.environ.get("GITHUB_SHA", "local")[:8]
        manifest = render_review_set(
            target="OWS-007",
            gate="gate_a_massing",
            revision=f"massing-r1@{revision}",
            damage_state="D0 intact massing only",
            source_commit=os.environ.get("GITHUB_SHA", "working-tree"),
            source_path="review-only:render_ows007_gate_a_massing.build_gate_a_massing()",
            size=size,
            blocks=blocks,
            output_dir=OUTPUT_DIR,
            camera_set="ows007_fixed_v1",
        )
        manifest["review_model_nbt_sha256"] = hashlib.sha256(model_bytes).hexdigest()
        manifest["review_builder_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        manifest["authoritative_shipping_modified"] = False
        manifest["shipping_nbt_git_blob_before"] = shipping_before
        manifest["shipping_nbt_git_blob_after"] = git_hash_object(SHIPPING_PATH)
        if manifest["shipping_nbt_git_blob_after"] != shipping_before:
            raise AssertionError("OWS-007 shipping NBT changed during review-only rendering")
        (OUTPUT_DIR / "review_manifest.json").write_text(
            json.dumps(manifest, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    finally:
        TEMP_NBT.unlink(missing_ok=True)

    print(
        f"Rendered OWS-007 Gate A r1 massing review at {manifest['dimensions']} using "
        f"{manifest['fixed_camera_set']}; independent visual approval remains pending."
    )


if __name__ == "__main__":
    main()
