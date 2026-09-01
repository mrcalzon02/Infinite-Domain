#!/usr/bin/env python3
"""Build and render the narrow OWS-010 Gate-A r2 massing correction."""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import generate_wasteland_sites as base
import render_ows010_gate_a_massing as r1
from render_old_world_heavy_rebuild_review import render_review_set
from render_structure_review import unpack_structure


ROOT = Path(__file__).resolve().parents[1]
TARGET = "OWS-010"
SIZE = (49, 16, 43)
CAMERA_SET = "ows010_fixed_v1"
SOURCE_PATH = r1.SHIPPING_PATH
FROZEN_SOURCE_BLOB = r1.FROZEN_BASELINE_BLOB
TEMP_NAME = "_heavy_review_ows010_gate_a_massing_r2"
TEMP_NBT = ROOT / "kubejs/data/infinite_domain/structure/wasteland" / f"{TEMP_NAME}.nbt"
OUTPUT_DIR = ROOT / "old_world_narrative/reviews/heavy_rebuild/visual/OWS-010/gate_a_massing/r2"
REVIEW_RECORD = ROOT / "old_world_narrative/reviews/heavy_rebuild/OWS-010_GATE_A_R1_REVIEW.md"
R1_MODEL_SHA256 = "f0296bc3de982f3cde027e9f87221be3e07add11cd073377f0b7664aa61165c7"


def _name(t: base.Template, pos: tuple[int, int, int]) -> str | None:
    row = t.blocks.get(pos)
    return None if row is None else t.palette[row[0]]["Name"]


def _git_blob(path: Path) -> str:
    return subprocess.run(
        ["git", "hash-object", str(path.relative_to(ROOT))],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _git_head() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _split_dock_crowns(t: base.Template) -> None:
    """Make inbound and outbound dock pairs distinct without moving portals."""
    # Inbound 01–02: one higher, forward orange gantry with two dark inset hoods.
    t.fill((17, 10, 33), (30, 12, 36), "minecraft:orange_concrete")
    for x1, x2 in ((18, 22), (25, 29)):
        t.fill((x1, 8, 33), (x2, 10, 35), "tfmg:steel_block")
        t.fill((x1 + 1, 8, 32), (x2 - 1, 9, 33), "minecraft:black_concrete")

    # The pair break is a tall steel fin aligned with the frozen center frames.
    t.fill((30, 8, 32), (31, 14, 38), "tfmg:steel_block")
    t.fill((30, 12, 32), (31, 14, 34), "minecraft:orange_concrete")

    # Outbound 03–04: a lower, recessed charcoal assembly under an orange cap.
    t.fill((32, 8, 35), (44, 10, 38), "minecraft:black_concrete")
    t.fill((32, 11, 35), (44, 12, 37), "minecraft:orange_concrete")
    for x1, x2 in ((32, 36), (39, 43)):
        t.fill((x1, 8, 34), (x2, 9, 35), "immersiveengineering:sheetmetal_steel")


def _articulate_long_elevations(t: base.Template) -> None:
    """Replace flush side planes with truss-aligned piers and recessed bands."""
    # West operator-gallery elevation: projected steel piers, recessed glazing,
    # and an orange clerestory header express a supervised personnel edge.
    for z in (10, 15, 20, 25, 30):
        t.fill((12, 2, z), (12, 9, z + 1), "tfmg:steel_block")
        t.fill((12, 8, z), (13, 9, z + 1), "minecraft:orange_concrete")
    for z1, z2 in ((12, 14), (17, 19), (22, 24), (27, 29)):
        t.clear((13, 3, z1), (13, 6, z2))
        t.fill((14, 3, z1), (14, 6, z2), "create:framed_glass")
    t.fill((12, 7, 11), (12, 8, 29), "minecraft:orange_concrete")

    # Gallery/service threshold at the south end is a deep massing recess, not
    # a detailed door. It aligns to the existing protected operator route.
    t.clear((13, 3, 29), (13, 6, 31))
    t.fill((12, 1, 28), (12, 8, 29), "tfmg:steel_block")
    t.fill((13, 3, 28), (13, 8, 29), "tfmg:steel_block")
    t.fill((12, 1, 31), (12, 8, 32), "tfmg:steel_block")
    t.fill((13, 3, 31), (13, 8, 32), "tfmg:steel_block")
    t.fill((11, 7, 28), (13, 9, 32), "minecraft:orange_concrete")

    # East hall elevation: exposed segments north and south of the maintenance
    # core receive projected lane/truss piers and deeply recessed clerestories.
    for z in (7, 13, 29, 35):
        t.fill((47, 1, z), (48, 12, z + 1), "tfmg:steel_block")
        t.fill((47, 9, z), (48, 11, z + 1), "minecraft:orange_concrete")
    for z1, z2 in ((9, 12), (31, 34)):
        t.clear((46, 4, z1), (46, 8, z2))
        t.fill((45, 4, z1), (45, 8, z2), "create:framed_glass")
        t.fill((47, 9, z1), (47, 10, z2), "minecraft:orange_concrete")

    # North transfer elevation: lane/truss-aligned piers and four recessed
    # clerestory bays reveal the destination-trunk rhythm on the blank rear view.
    for x in (16, 22, 28, 34, 40, 46):
        t.fill((x, 2, 5), (x + 1, 12, 6), "tfmg:steel_block")
        t.fill((x, 9, 5), (x + 1, 11, 7), "minecraft:orange_concrete")
    for x1, x2 in ((18, 21), (24, 27), (30, 33), (36, 39)):
        t.clear((x1, 5, 7), (x2, 9, 7))
        t.fill((x1, 5, 8), (x2, 9, 8), "create:framed_glass")
        t.fill((x1, 10, 6), (x2, 11, 7), "minecraft:orange_concrete")


def _strengthen_control_oversight(t: base.Template) -> None:
    """Make the accepted crown read as a hall-facing control/records lantern."""
    # Reprofile within the accepted crown footprint with a stronger glazed east
    # face, darker datum, and a raised orange cap distinguishable from hall roof.
    t.fill((8, 9, 8), (17, 10, 19), "tfmg:steel_block")
    t.fill((17, 10, 9), (17, 13, 18), "create:framed_glass")
    t.fill((18, 10, 9), (18, 11, 18), "create:framed_glass")
    t.fill((17, 9, 9), (18, 14, 9), "tfmg:steel_block")
    for z in (13, 18):
        t.fill((17, 9, z), (17, 14, z), "tfmg:steel_block")
    t.fill((7, 14, 7), (17, 15, 20), "minecraft:orange_concrete")
    t.fill((10, 14, 20), (17, 15, 21), "tfmg:steel_block")

    # Two supports and an underslung orange datum visibly connect oversight to
    # the operator gallery while remaining below the frozen roof monitors.
    for z in (10, 17):
        t.fill((17, 6, z), (18, 9, z + 1), "tfmg:steel_block")
    t.fill((16, 8, 10), (18, 9, 17), "minecraft:orange_concrete")


def _clarify_maintenance_core(t: base.Template) -> None:
    """Tie the east service threshold, cross bridge, and roof bar into one core."""
    # A recessed base threshold and tall paired piers create a real service entry.
    t.clear((48, 2, 20), (48, 6, 23))
    t.fill((47, 2, 20), (47, 6, 23), "minecraft:black_concrete")
    for z1, z2 in ((18, 19), (24, 25)):
        t.fill((47, 2, z1), (48, 15, z2), "tfmg:steel_block")
        t.fill((48, 8, z1), (48, 14, z2), "minecraft:orange_concrete")

    # The accepted bridge footprint stays fixed at Y7–8; r2 adds a visible
    # orange/steel hood above it and continues that datum into the roof cap.
    t.fill((40, 9, 19), (48, 10, 19), "minecraft:orange_concrete")
    t.fill((40, 9, 23), (48, 10, 23), "minecraft:orange_concrete")
    t.fill((46, 9, 20), (48, 10, 22), "tfmg:steel_block")
    t.fill((43, 14, 15), (48, 15, 28), "immersiveengineering:sheetmetal_steel")
    t.fill((47, 14, 17), (48, 15, 26), "minecraft:orange_concrete")


def build_gate_a_massing_r2() -> base.Template:
    t = r1.build_gate_a_massing()
    _split_dock_crowns(t)
    _articulate_long_elevations(t)
    _strengthen_control_oversight(t)
    _clarify_maintenance_core(t)
    return t


def _assert_same_region(
    r1_model: base.Template,
    r2_model: base.Template,
    a: tuple[int, int, int],
    b: tuple[int, int, int],
    label: str,
) -> None:
    for x in range(a[0], b[0] + 1):
        for y in range(a[1], b[1] + 1):
            for z in range(a[2], b[2] + 1):
                pos = (x, y, z)
                if _name(r1_model, pos) != _name(r2_model, pos):
                    raise AssertionError(f"r2 changed frozen {label} at {pos}")


def _assert_r2_scope(r1_model: base.Template, r2_model: base.Template) -> int:
    if tuple(r2_model.size) != SIZE:
        raise AssertionError(f"OWS-010 Gate-A r2 dimensions drifted: {r2_model.size}")
    if any(not (0 <= x < SIZE[0] and 0 <= y < SIZE[1] and 0 <= z < SIZE[2]) for x, y, z in r2_model.blocks):
        raise AssertionError("OWS-010 Gate-A r2 exceeds the frozen envelope")

    # Four dock openings and their deep structural frames are exact frozen facts.
    for x1, x2 in ((18, 22), (25, 29), (32, 36), (39, 43)):
        _assert_same_region(r1_model, r2_model, (x1, 2, 37), (x2, 7, 37), "dock portal")
    for x in (17, 23, 24, 30, 31, 37, 38, 44):
        _assert_same_region(r1_model, r2_model, (x, 1, 36), (x, 7, 38), "dock frame")

    # The complete U-flow material contract remains exact below facade scope.
    frozen_process_regions = (
        ((19, 2, 31), (21, 3, 37), "inbound tongue 01"),
        ((26, 2, 31), (28, 3, 37), "inbound tongue 02"),
        ((18, 2, 28), (40, 5, 31), "induction crossfeed"),
        ((18, 2, 12), (20, 4, 28), "lane 01"),
        ((24, 2, 12), (26, 4, 28), "lane 02"),
        ((30, 2, 12), (32, 4, 28), "lane 03"),
        ((36, 2, 12), (38, 4, 28), "lane 04"),
        ((18, 2, 9), (42, 5, 12), "destination trunk"),
        ((40, 4, 9), (43, 6, 32), "east return"),
        ((33, 2, 31), (35, 3, 37), "outbound tongue 03"),
        ((40, 2, 31), (42, 3, 37), "outbound tongue 04"),
    )
    for a, b, label in frozen_process_regions:
        _assert_same_region(r1_model, r2_model, a, b, label)

    # Gallery/cross-aisle route floors, annex/core footprints and monitor
    # alignment remain exact even though their exterior profiles are corrected.
    _assert_same_region(r1_model, r2_model, (13, 1, 10), (17, 2, 31), "operator-gallery floor")
    _assert_same_region(r1_model, r2_model, (16, 7, 19), (43, 8, 22), "cross-aisle reservation")
    _assert_same_region(r1_model, r2_model, (3, 1, 4), (17, 1, 22), "annex footprint")
    _assert_same_region(r1_model, r2_model, (43, 1, 15), (48, 1, 28), "maintenance-core footprint")
    for x1, x2 in ((18, 20), (24, 26), (30, 32), (36, 38)):
        _assert_same_region(r1_model, r2_model, (x1, 12, 13), (x2, 15, 27), "lane-monitor alignment")

    positions = set(r1_model.blocks) | set(r2_model.blocks)
    changed = sum(_name(r1_model, pos) != _name(r2_model, pos) for pos in positions)
    if not 700 <= changed <= 3000:
        raise AssertionError(f"OWS-010 Gate-A r2 correction scope unexpected: {changed} positions")

    names = {_name(r2_model, pos) for pos in r2_model.blocks}
    forbidden = {
        "minecraft:chest",
        "minecraft:trapped_chest",
        "minecraft:spawner",
        "minecraft:lectern",
        "create:mechanical_press",
        "create:depot",
        "create:mechanical_belt",
        "create:shaft",
        "create:cogwheel",
        "immersiveengineering:crate",
    }
    found = forbidden.intersection(names)
    if found:
        raise AssertionError(f"OWS-010 Gate-A r2 contains deferred Pass-7+ content: {sorted(found)}")
    return changed


def main() -> None:
    review_text = REVIEW_RECORD.read_text(encoding="utf-8")
    if "**Decision:** **REVISION REQUIRED**" not in review_text:
        raise AssertionError("OWS-010 Gate-A r1 revision authority is missing")
    if "Pass 6 is reopened only for the narrow scope above" not in review_text:
        raise AssertionError("OWS-010 Gate-A r2 scope authority is missing")

    source_bytes = SOURCE_PATH.read_bytes()
    source_sha256 = hashlib.sha256(source_bytes).hexdigest()
    if _git_blob(SOURCE_PATH) != FROZEN_SOURCE_BLOB:
        raise AssertionError("OWS-010 shipping Git provenance drifted")

    r1_model = r1.build_gate_a_massing()
    model = build_gate_a_massing_r2()
    changed_positions = _assert_r2_scope(r1_model, model)
    model.save(TEMP_NAME)
    try:
        model_bytes = TEMP_NBT.read_bytes()
        size, blocks = unpack_structure(TEMP_NBT)
        occupied_min = [min(point[axis] for point in blocks) for axis in range(3)]
        occupied_max = [max(point[axis] for point in blocks) for axis in range(3)]
        head = _git_head()
        manifest = render_review_set(
            target=TARGET,
            gate="gate_a_massing",
            revision=f"massing-r2@{head[:8]}",
            damage_state="D0 intact massing only",
            source_commit=head,
            source_path="review-only:render_ows010_gate_a_massing_r2.build_gate_a_massing_r2()",
            size=size,
            blocks=blocks,
            output_dir=OUTPUT_DIR,
            camera_set=CAMERA_SET,
        )
        manifest.update({
            "review_model_nbt_sha256": hashlib.sha256(model_bytes).hexdigest(),
            "review_builder_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "review_model_non_air_blocks": len(blocks),
            "review_model_occupied_bounds": {"min": occupied_min, "max": occupied_max},
            "r1_review_model_nbt_sha256": R1_MODEL_SHA256,
            "phase0_source_sha256": source_sha256,
            "phase0_source_git_blob": FROZEN_SOURCE_BLOB,
            "phase0_shipping_untouched": SOURCE_PATH.read_bytes() == source_bytes,
            "shipping_nbt_git_blob_before": FROZEN_SOURCE_BLOB,
            "shipping_nbt_git_blob_after": _git_blob(SOURCE_PATH),
            "r1_accepted_aspects_frozen": 9,
            "r2_changed_positions": changed_positions,
            "r2_scope": [
                "distinct projected inbound 01-02 and recessed outbound 03-04 dock-crown assemblies",
                "lane/truss-aligned north/side piers, deep gallery/clerestory recesses and service thresholds",
                "raised hall-facing control/records lantern profile",
                "east maintenance base threshold, bridge hood, vertical piers and roof cap",
            ],
            "pass7_plus_content_present": False,
            "lor_006_manual_placed": False,
            "canonical_proof_placed": False,
            "visual_review_status": "rendered_pending_independent_review",
            "authoritative_shipping_modified": False,
        })
        (OUTPUT_DIR / "review_manifest.json").write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n"
        )
    finally:
        TEMP_NBT.unlink(missing_ok=True)

    if SOURCE_PATH.read_bytes() != source_bytes:
        raise AssertionError("OWS-010 shipping changed while rendering Gate-A r2")
    print(
        f"Rendered OWS-010 Gate-A r2 at {manifest['dimensions']} with "
        f"{manifest['fixed_camera_set']}; {changed_positions} scoped changes; independent review required."
    )


if __name__ == "__main__":
    main()
