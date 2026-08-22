#!/usr/bin/env python3
"""Build and render the review-only OWS-006 Gate-A r1 massing candidate.

The model proves the public/chamber/support/service hierarchy before laboratory
equipment, proof loot, history, encounters, damage, or microdetail are added.
It never writes shared heavy-rebuild state or authoritative shipping NBT.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path

import generate_wasteland_sites as base
from render_old_world_heavy_rebuild_review import OUTPUT_ROOT, ROOT, render_review_set
from render_structure_review import unpack_structure


TEMP_NAME = "_heavy_review_ows006_gate_a_massing_r1"
TEMP_NBT = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{TEMP_NAME}.nbt"
OUTPUT_DIR = OUTPUT_ROOT / "OWS-006" / "gate_a_massing" / "r1"
SHIPPING_PATH = (
    ROOT
    / "kubejs"
    / "data"
    / "infinite_domain"
    / "structure"
    / "wasteland"
    / "old_world"
    / "ows_006_vcf_pt9_symbiosis_pilot_laboratory.nbt"
)


def _site_and_public_threshold(t: base.Template) -> None:
    """Establish a clean visitor front and physically separate service access."""
    t.fill((1, 0, 1), (57, 0, 49), "minecraft:grass_block")

    # Public forecourt and central arrival axis.
    t.fill((10, 0, 1), (48, 0, 12), "minecraft:smooth_stone")
    t.fill((26, 0, 0), (32, 0, 15), "minecraft:white_concrete")
    for x in (12, 46):
        t.fill((x, 0, 2), (x, 0, 10), "minecraft:lime_concrete")

    # Low public/reception bar: transparent and optimistic, but clearly a
    # controlled threshold rather than a door cut into a research hall.
    base.shell(
        t,
        (9, 1, 6),
        (49, 8, 16),
        "minecraft:white_concrete",
        "minecraft:smooth_stone",
        "minecraft:light_gray_concrete",
    )
    t.fill((13, 2, 5), (45, 6, 5), "create:framed_glass")
    t.clear((26, 2, 5), (32, 5, 6))
    t.fill((14, 7, 5), (44, 8, 5), "minecraft:lime_concrete")

    # Deep, supported entrance canopy scaled to the public institution.
    t.fill((20, 8, 1), (38, 8, 7), "minecraft:white_concrete")
    for x in (20, 38):
        t.fill((x, 1, 2), (x, 7, 2), "minecraft:light_gray_concrete")

    # Rear service apron is displaced from the public front and feeds both
    # support wings without crossing the observation route.
    t.fill((5, 0, 40), (55, 0, 49), "tfmg:asphalt")
    for x in (8, 18, 28, 38, 48):
        t.fill((x, 0, 44), (x, 0, 49), "minecraft:light_gray_concrete")


def _observation_gallery(t: base.Template) -> None:
    """Make the three comparative chambers readable from one hero threshold."""
    base.shell(
        t,
        (11, 1, 13),
        (50, 9, 22),
        "minecraft:white_concrete",
        "minecraft:smooth_stone",
        "minecraft:light_gray_concrete",
    )
    # Continuous controlled glazing faces the chamber pods. It is macro
    # architecture here, not a finished interior observation system.
    t.fill((13, 3, 22), (48, 7, 22), "create:framed_glass")
    for x in (13, 24, 36, 48):
        t.fill((x, 1, 21), (x, 9, 22), "minecraft:light_gray_concrete")
    # A shallow glazed lantern announces the comparison gallery in section.
    base.shell(
        t,
        (20, 9, 14),
        (41, 12, 20),
        "create:framed_glass",
        "minecraft:light_gray_concrete",
        "minecraft:white_concrete",
    )


def _comparative_chambers(t: base.Template) -> None:
    """Express A/B/C as related but distinct controlled research volumes."""
    chambers = (
        ((12, 1, 21), (24, 15, 40), 15),
        ((24, 1, 20), (37, 18, 41), 18),
        ((37, 1, 22), (49, 16, 40), 16),
    )
    for index, (lo, hi, roof_y) in enumerate(chambers):
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
        # Controlled observation faces are concentrated toward the gallery.
        t.fill((x1 + 2, 4, z1 - 1), (x2 - 2, 10, z1 - 1), "create:framed_glass")
        # A real service belt runs across each rear chamber face.
        t.fill((x1, roof_y - 4, z2 + 1), (x2, roof_y - 2, z2 + 1), "minecraft:cyan_concrete")
        for x in (x1, x2):
            t.fill((x, 1, z1 - 1), (x, roof_y, z1 - 1), "minecraft:light_gray_concrete")

    # Raised chamber monitors give each trial volume environmental identity and
    # tie the stepped silhouette to the shared service spine.
    monitors = (
        ((15, 15, 26), (21, 18, 36)),
        ((28, 18, 25), (34, 22, 37)),
        ((40, 16, 27), (46, 20, 36)),
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


def _support_wings(t: base.Template) -> None:
    """Reserve distinct preparation and analysis masses around the chambers."""
    # West preparation/receiving wing: low, serviceable and connected to the
    # clean chamber-transfer side rather than the public lobby.
    base.shell(
        t,
        (2, 1, 14),
        (13, 11, 43),
        "minecraft:light_gray_concrete",
        "tfmg:factory_floor",
        "minecraft:white_concrete",
    )
    t.fill((1, 3, 19), (1, 8, 28), "minecraft:white_concrete")
    t.clear((1, 3, 21), (2, 7, 26))
    t.fill((2, 8, 17), (5, 11, 40), "minecraft:cyan_concrete")

    # East analysis/polymer wing: taller at the records end, asymmetrical and
    # deliberately separate from clean preparation.
    base.shell(
        t,
        (48, 1, 13),
        (56, 13, 42),
        "minecraft:white_concrete",
        "minecraft:smooth_stone",
        "minecraft:light_gray_concrete",
    )
    t.fill((56, 4, 18), (56, 9, 36), "create:framed_glass")
    for z in (16, 25, 34, 42):
        t.fill((57, 1, z), (57, 13, z), "minecraft:light_gray_concrete")
    # One restrained amber mass reserves the polymer-observation suite without
    # substituting hazard color for later operational architecture.
    t.fill((52, 11, 27), (56, 14, 38), "minecraft:yellow_concrete")


def _rear_service_spine_and_plant(t: base.Template) -> None:
    """Connect all chamber branches to one maintainable environmental system."""
    base.shell(
        t,
        (10, 1, 39),
        (51, 10, 48),
        "minecraft:light_gray_concrete",
        "tfmg:factory_floor",
        "minecraft:white_concrete",
    )
    # Rear loading/waste thresholds remain distinct at the massing scale.
    for x1, x2 in ((14, 20), (40, 46)):
        t.clear((x1, 2, 48), (x2, 7, 48))
        t.fill((x1 - 1, 8, 47), (x2 + 1, 10, 49), "tfmg:steel_block")

    # Shared rooftop environmental plant with three chamber branch plenums.
    t.fill((14, 10, 41), (47, 15, 47), "immersiveengineering:sheetmetal_steel")
    for x1, x2, top in ((15, 21, 20), (27, 34, 24), (40, 46, 21)):
        t.fill((x1, 15, 42), (x2, top, 46), "tfmg:steel_block")
        t.fill((x1 + 2, top, 43), (x2 - 2, min(25, top + 2), 45), "minecraft:light_gray_concrete")

    # East maintenance core carries service access to the high central plant.
    base.shell(
        t,
        (50, 1, 35),
        (56, 21, 47),
        "minecraft:light_gray_concrete",
        "minecraft:smooth_stone",
        "minecraft:white_concrete",
    )
    t.fill((56, 4, 38), (56, 18, 44), "create:framed_glass")


def build_gate_a_massing() -> base.Template:
    t = base.Template((59, 26, 51))
    _site_and_public_threshold(t)
    _observation_gallery(t)
    _comparative_chambers(t)
    _support_wings(t)
    _rear_service_spine_and_plant(t)
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
    if tuple(t.size) != (59, 26, 51):
        raise AssertionError(f"OWS-006 Gate-A r1 dimensions changed unexpectedly: {t.size}")
    if len(t.blocks) < 15000:
        raise AssertionError("Gate-A r1 massing is unexpectedly sparse")
    if any(not (0 <= x < 59 and 0 <= y < 26 and 0 <= z < 51) for x, y, z in t.blocks):
        raise AssertionError("Gate-A r1 massing exceeds the retained review envelope")

    t.save(TEMP_NAME)
    try:
        model_bytes = TEMP_NBT.read_bytes()
        size, blocks = unpack_structure(TEMP_NBT)
        revision = os.environ.get("GITHUB_SHA", "local")[:8]
        manifest = render_review_set(
            target="OWS-006",
            gate="gate_a_massing",
            revision=f"massing-r1@{revision}",
            damage_state="D0 intact massing only",
            source_commit=os.environ.get("GITHUB_SHA", "working-tree"),
            source_path="review-only:render_ows006_gate_a_massing.build_gate_a_massing()",
            size=size,
            blocks=blocks,
            output_dir=OUTPUT_DIR,
            camera_set="ows006_fixed_v1",
        )
        manifest["review_model_nbt_sha256"] = hashlib.sha256(model_bytes).hexdigest()
        manifest["review_builder_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        manifest["authoritative_shipping_modified"] = False
        manifest["shipping_nbt_git_blob_before"] = shipping_before
        manifest["shipping_nbt_git_blob_after"] = git_hash_object(SHIPPING_PATH)
        if manifest["shipping_nbt_git_blob_after"] != shipping_before:
            raise AssertionError("OWS-006 shipping NBT changed during review-only rendering")
        (OUTPUT_DIR / "review_manifest.json").write_text(
            json.dumps(manifest, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    finally:
        TEMP_NBT.unlink(missing_ok=True)

    print(
        f"Rendered OWS-006 Gate A r1 massing review at {manifest['dimensions']} using "
        f"{manifest['fixed_camera_set']}; independent visual approval remains pending."
    )


if __name__ == "__main__":
    main()
