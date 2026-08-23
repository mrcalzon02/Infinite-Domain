#!/usr/bin/env python3
"""Build and render the review-only OWS-009 Gate-A r2 massing revision."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path

import generate_wasteland_sites as base
import render_ows009_gate_a_massing as r1


ROOT = Path(__file__).resolve().parents[1]
TARGET = "OWS-009"
SOURCE_PATH = r1.SOURCE_PATH
FROZEN_SOURCE_SHA256 = r1.FROZEN_SOURCE_SHA256
FROZEN_SOURCE_BLOB = r1.FROZEN_SOURCE_BLOB
TEMP_NAME = "_heavy_review_ows009_gate_a_massing_r2"
TEMP_NBT = ROOT / "kubejs/data/infinite_domain/structure/wasteland" / f"{TEMP_NAME}.nbt"
OUTPUT_DIR = ROOT / "old_world_narrative/reviews/heavy_rebuild/visual/OWS-009/gate_a_massing/r2"
R1_REVIEW = ROOT / "old_world_narrative/reviews/heavy_rebuild/OWS-009_GATE_A_R1_REVIEW.md"
AIR = r1.AIR


def _project_side_and_rear_structure(t: base.Template) -> None:
    """Replace flush wall dominance with cell- and spine-aligned deep bays."""
    steel = "tfmg:steel_block"

    # West service elevation: five deep projected frames separate intake,
    # working-cell and technician-spine panels. Lower inset panels stop the
    # long cinder-block wall from reading as one applied-color plane.
    for z, top in ((7, 11), (15, 11), (24, 11), (31, 11), (34, 11)):
        t.fill((2, 1, z), (3, top, min(z + 1, 34)), steel)
    for z1, z2 in ((9, 14), (17, 23), (26, 30)):
        t.fill((3, 2, z1), (3, 5, z2), "minecraft:light_gray_concrete")
    t.fill((2, 6, 9), (2, 6, 30), "minecraft:orange_concrete")
    t.fill((2, 10, 25), (3, 11, 33), steel)

    # Rear elevation: the three cell widths and east support bar receive
    # independent projected piers, with a real steel/orange service header
    # attached to the rear technician spine rather than a decorative stripe.
    for x, top in ((3, 11), (14, 12), (25, 12), (35, 12)):
        t.fill((x, 1, 34), (min(x + 1, 35), top, 35), steel)
    t.fill((4, 10, 35), (34, 11, 36), steel)
    t.fill((5, 12, 35), (33, 12, 35), "minecraft:orange_concrete")
    for x1, x2, y in ((6, 12, 8), (17, 23, 10), (28, 33, 9)):
        t.fill((x1 - 1, y - 1, 35), (x2 + 1, y + 2, 35), steel)
        t.fill((x1, y, 34), (x2, y + 1, 34), "create:framed_glass")
    t.fill((5, 12, 35), (33, 12, 35), "minecraft:orange_concrete")


def _differentiate_cell_profiles(t: base.Template) -> None:
    """Give all three repair cells distinct roof and threshold silhouettes."""
    steel = "tfmg:steel_block"

    # Cell 01: low diagnostic hood and a shallow roof monitor.
    t.fill((4, 8, 5), (13, 9, 6), steel)
    t.fill((5, 8, 4), (12, 8, 5), "minecraft:orange_concrete")
    r1._shell(t, (6, 11, 13), (12, 13, 22), steel, "minecraft:light_gray_concrete")
    t.fill((7, 12, 12), (11, 12, 12), "create:framed_glass")

    # Cell 02: tallest portal and transverse exchange monitor, tied directly
    # into the retained roadside blade.
    t.fill((15, 9, 5), (24, 10, 6), steel)
    t.fill((16, 9, 4), (23, 9, 5), "minecraft:orange_concrete")
    r1._shell(t, (17, 13, 11), (23, 16, 23), steel, "minecraft:light_gray_concrete")
    t.fill((18, 14, 10), (22, 15, 10), "create:framed_glass")
    t.fill((19, 16, 8), (21, 17, 12), "minecraft:orange_concrete")

    # Cell 03: offset calibration/release monitor and a lower, wider release
    # canopy so it cannot be mistaken for Cell 01's diagnostic threshold.
    t.fill((26, 7, 5), (34, 8, 6), steel)
    t.fill((27, 7, 4), (34, 7, 5), "minecraft:orange_concrete")
    r1._shell(t, (29, 12, 15), (34, 14, 25), steel, "minecraft:light_gray_concrete")
    t.fill((28, 12, 17), (28, 13, 23), "create:framed_glass")


def _differentiate_support_thresholds(t: base.Template) -> None:
    """Make clean parts receiving and dirty core return readable separately."""
    steel = "tfmg:steel_block"

    # East-facing parts receiving portal: orange service frame and a shallow
    # canopy connected to the paved delivery strip.
    t.fill((44, 1, 21), (45, 8, 22), steel)
    t.fill((44, 1, 26), (45, 8, 27), steel)
    t.fill((44, 7, 21), (46, 8, 27), steel)
    t.fill((45, 8, 22), (46, 8, 26), "minecraft:orange_concrete")
    t.clear((44, 2, 23), (45, 6, 25))

    # South-facing removed-core/rework portal: charcoal return frame opening
    # directly onto the isolated coarse-dirt collection yard.
    t.clear((37, 2, 34), (42, 5, 35))
    t.fill((36, 1, 33), (37, 7, 36), "minecraft:polished_blackstone")
    t.fill((42, 1, 33), (43, 7, 36), "minecraft:polished_blackstone")
    t.fill((36, 6, 33), (43, 7, 36), steel)
    t.fill((38, 7, 35), (41, 7, 36), "minecraft:orange_concrete")


def build_gate_a_massing_r2() -> base.Template:
    t = r1.build_gate_a_massing()
    _project_side_and_rear_structure(t)
    _differentiate_cell_profiles(t)
    _differentiate_support_thresholds(t)
    return t


def _name(t: base.Template, pos: tuple[int, int, int]) -> str | None:
    return r1._name(t, pos)


def _changed_positions(a: base.Template, b: base.Template) -> int:
    positions = set(a.blocks) | set(b.blocks)
    return sum(_name(a, pos) != _name(b, pos) for pos in positions)


def _assert_r2_contracts(t: base.Template) -> int:
    r1._assert_contracts(t)
    changed = _changed_positions(r1.build_gate_a_massing(), t)
    if changed < 500:
        raise AssertionError(f"OWS-009 Gate-A r2 revision too small: {changed} changed positions")

    required = {
        (2, 5, 15): "tfmg:steel_block",                # west projected bay pier
        (2, 6, 20): "minecraft:orange_concrete",       # west service datum
        (10, 11, 36): "tfmg:steel_block",              # rear service header
        (20, 12, 35): "minecraft:orange_concrete",     # rear Atlas header
        (8, 12, 12): "create:framed_glass",            # Cell 01 monitor
        (20, 15, 10): "create:framed_glass",           # Cell 02 monitor
        (28, 13, 20): "create:framed_glass",           # Cell 03 offset monitor
        (45, 8, 24): "minecraft:orange_concrete",      # parts portal canopy
        (39, 7, 36): "minecraft:orange_concrete",      # core-return portal
    }
    for pos, expected in required.items():
        actual = _name(t, pos)
        if actual != expected:
            raise AssertionError(f"OWS-009 Gate-A r2 aspect drift at {pos}: {actual} != {expected}")

    # Parts and core thresholds must remain separately traversable.
    for pos in ((44, 3, 24), (39, 3, 34)):
        if _name(t, pos) not in AIR:
            raise AssertionError(f"OWS-009 Gate-A r2 service threshold blocked at {pos}")
    return changed


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

    if "OWS-009 GATE A r1: REVISION REQUIRED." not in R1_REVIEW.read_text(encoding="utf-8"):
        raise AssertionError("OWS-009 Gate-A r1 revision decision missing")

    source_bytes = SOURCE_PATH.read_bytes()
    if hashlib.sha256(source_bytes).hexdigest() != FROZEN_SOURCE_SHA256:
        raise AssertionError("OWS-009 shipping NBT changed during Gate-A r2 authoring")
    if _git_blob(SOURCE_PATH) != FROZEN_SOURCE_BLOB:
        raise AssertionError("OWS-009 shipping Git provenance drifted")

    t = build_gate_a_massing_r2()
    changed = _assert_r2_contracts(t)
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
            source_path="review-only:render_ows009_gate_a_massing_r2.build_gate_a_massing_r2()",
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
            "gate_a_r1_decision": "REVISION REQUIRED",
            "changed_positions_from_r1": changed,
            "r2_massing_aspects_asserted": 9,
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
        raise AssertionError("OWS-009 shipping changed while rendering Gate A r2")
    print(
        f"Rendered OWS-009 Gate-A r2 at {manifest['dimensions']} with "
        f"{changed} changed positions from r1; independent review required."
    )


if __name__ == "__main__":
    main()
