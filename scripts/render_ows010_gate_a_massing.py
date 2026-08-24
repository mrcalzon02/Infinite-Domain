#!/usr/bin/env python3
"""Build and render the review-only OWS-010 Gate-A r1 massing candidate.

The model proves the dock/transfer/control/service hierarchy before detailed
structure, circulation, equipment, proof, history, damage, encounters, or
microdetail. It never writes shared state or authoritative shipping NBT.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import generate_wasteland_sites as base
from render_old_world_heavy_rebuild_review import OUTPUT_ROOT, ROOT, render_review_set
from render_structure_review import unpack_structure


TARGET = "OWS-010"
SIZE = (49, 16, 43)
CAMERA_SET = "ows010_fixed_v1"
FROZEN_BASELINE_COMMIT = "e14b3f35306fc313e7ea9a114f2384696864533a"
FROZEN_BASELINE_BLOB = "be2ab341c2d252c975711caa93e92c965f943007"
TEMP_NAME = "_heavy_review_ows010_gate_a_massing_r1"
TEMP_NBT = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{TEMP_NAME}.nbt"
OUTPUT_DIR = OUTPUT_ROOT / TARGET / "gate_a_massing" / "r1"
SHIPPING_RELATIVE = Path(
    "kubejs/data/infinite_domain/structure/wasteland/old_world/"
    "ows_010_atlas_conveyor_transfer_hall.nbt"
)
SHIPPING_PATH = ROOT / SHIPPING_RELATIVE
PLANNING_INPUTS = (
    Path("old_world_narrative/reviews/heavy_rebuild/OWS-010_PHASE0_BASELINE_REVIEW.md"),
    Path("old_world_narrative/reviews/heavy_rebuild/OWS-010_PASS2_FUNCTIONAL_DEFINITION.md"),
    Path("old_world_narrative/reviews/heavy_rebuild/OWS-010_PASS3_PRECEDENT_RESEARCH.md"),
    Path("old_world_narrative/reviews/heavy_rebuild/OWS-010_PASS4_PROGRAM_ADJACENCY.md"),
    Path("old_world_narrative/reviews/heavy_rebuild/OWS-010_PASS5_SCALE_TRANSLATION.md"),
)


def _site_and_courts(t: base.Template) -> None:
    """Retain separate north staff, south truck, and east service approaches."""
    t.fill((0, 0, 0), (48, 0, 42), "minecraft:grass_block")

    # North staff/security approach remains human-scaled and separate from freight.
    t.fill((2, 0, 0), (18, 0, 8), "minecraft:smooth_stone")
    t.fill((7, 0, 0), (12, 0, 10), "minecraft:orange_concrete")

    # South truck court serves four dock portals; dark centerlines reserve
    # vehicle lanes while orange shoulders belong to the building hierarchy.
    t.fill((14, 0, 35), (48, 0, 42), "tfmg:asphalt")
    for x in (20, 27, 34, 41):
        t.fill((x, 0, 38), (x, 0, 42), "minecraft:light_gray_concrete")

    # East service approach never crosses the north staff threshold.
    t.fill((45, 0, 8), (48, 0, 36), "tfmg:asphalt")
    t.fill((46, 0, 14), (48, 0, 26), "minecraft:yellow_concrete")


def _support_and_control_annex(t: base.Template) -> None:
    """Preserve the donor's low support annex and add a process-facing control crown."""
    base.shell(
        t,
        (3, 1, 4),
        (17, 9, 22),
        "minecraft:light_gray_concrete",
        "minecraft:smooth_stone",
        "tfmg:steel_block",
    )

    # Recessed north staff entrance and supported Atlas-orange canopy.
    t.clear((7, 2, 4), (12, 6, 4))
    t.fill((5, 8, 1), (14, 8, 6), "minecraft:orange_concrete")
    for x in (5, 14):
        t.fill((x, 1, 2), (x, 7, 2), "tfmg:steel_block")

    # Raised control/quality/records volume overlooks lane induction and output.
    # Its west portion reserves maintenance records and a non-loot LOR shelf;
    # no proof or manual item is placed in this massing model.
    base.shell(
        t,
        (8, 9, 8),
        (18, 13, 19),
        "minecraft:orange_concrete",
        "tfmg:steel_block",
        "minecraft:light_gray_concrete",
    )
    t.fill((18, 10, 10), (18, 12, 17), "create:framed_glass")
    t.fill((10, 10, 19), (17, 12, 19), "create:framed_glass")


def _high_bay_shell_and_docks(t: base.Template) -> None:
    """Create a four-bay Atlas transfer hall with paired dock hierarchy."""
    base.shell(
        t,
        (15, 1, 7),
        (46, 12, 37),
        "minecraft:light_gray_concrete",
        "tfmg:factory_floor",
        "tfmg:steel_block",
    )

    dock_bays = ((18, 22), (25, 29), (32, 36), (39, 43))
    for index, (x1, x2) in enumerate(dock_bays, 1):
        # Full freight portals and deep structural frames correspond to lanes.
        t.clear((x1, 2, 37), (x2, 7, 37))
        t.fill((x1 - 1, 1, 36), (x1 - 1, 10, 38), "tfmg:steel_block")
        t.fill((x2 + 1, 1, 36), (x2 + 1, 10, 38), "tfmg:steel_block")
        crown = "minecraft:orange_concrete" if index <= 2 else "minecraft:black_concrete"
        t.fill((x1 - 1, 8, 35), (x2 + 1, 11, 38), crown)
        # Orange inset retains one Atlas family across inbound/outbound pairs.
        t.fill((x1, 9, 34), (x2, 10, 35), "minecraft:orange_concrete")

    # Repeated road-facing piers make the lane rhythm architectural.
    for x in (15, 17, 24, 31, 38, 45, 46):
        t.fill((x, 1, 35), (x, 12, 37), "tfmg:steel_block")


def _transfer_process_massing(t: base.Template) -> None:
    """Reserve continuous inbound, four-lane, trunk, and outbound-return volumes."""
    lane_ranges = ((18, 20), (24, 26), (30, 32), (36, 38))

    # Two inbound dock tongues feed a shared south induction/crossfeed.
    for x1, x2 in ((19, 21), (26, 28)):
        t.fill((x1, 2, 31), (x2, 3, 37), "minecraft:black_concrete")
    t.fill((18, 2, 28), (40, 3, 31), "minecraft:black_concrete")
    t.fill((18, 4, 29), (40, 5, 30), "minecraft:orange_concrete")

    # Four uninterrupted process lanes rise enough to read in cutaway while
    # leaving a full player-scale clear zone beneath the future catwalk.
    for index, (x1, x2) in enumerate(lane_ranges, 1):
        t.fill((x1, 2, 12), (x2, 3, 28), "minecraft:black_concrete")
        t.fill((x1, 4, 14), (x2, 4, 16), "minecraft:orange_concrete")
        t.fill((x1, 4, 24), (x2, 4, 26), "minecraft:orange_concrete")
        # Lane-local service shoulders reserve reachable drive/isolation faces.
        shoulder = x2 + 1 if index < 4 else x1 - 1
        t.fill((shoulder, 1, 13), (shoulder, 1, 27), "minecraft:yellow_concrete")

    # Common north destination trunk receives every lane output.
    t.fill((18, 2, 9), (42, 3, 12), "minecraft:black_concrete")
    t.fill((18, 4, 9), (42, 5, 10), "minecraft:orange_concrete")

    # Elevated east return/drop keeps outbound freight separate from inbound
    # crossfeed before descending into Dock 03 and Dock 04 tongues.
    t.fill((40, 4, 9), (43, 5, 32), "minecraft:black_concrete")
    t.fill((40, 6, 11), (43, 6, 29), "minecraft:orange_concrete")
    for x1, x2 in ((33, 35), (40, 42)):
        t.fill((x1, 2, 31), (x2, 3, 37), "minecraft:black_concrete")


def _operator_and_maintenance_access(t: base.Template) -> None:
    """Reserve broad, protected routes rather than decorative scaffolding."""
    # West operator gallery joins the annex to lane starts and outputs.
    base.shell(
        t,
        (13, 1, 10),
        (17, 8, 31),
        "minecraft:light_gray_concrete",
        "minecraft:smooth_stone",
        "tfmg:steel_block",
    )
    t.fill((17, 3, 12), (17, 7, 29), "create:framed_glass")

    # Guarded cross-aisle bridge reserves safe operator transfer above all lanes.
    t.fill((16, 7, 19), (43, 8, 22), "minecraft:light_gray_concrete")
    t.fill((16, 9, 19), (43, 9, 19), "minecraft:orange_concrete")
    t.fill((16, 9, 22), (43, 9, 22), "minecraft:orange_concrete")

    # East service core and long maintenance face connect floor, bridge, roof,
    # parts issue, lockout and output return without entering operator space.
    base.shell(
        t,
        (43, 1, 15),
        (48, 14, 28),
        "tfmg:steel_block",
        "minecraft:smooth_stone",
        "minecraft:orange_concrete",
    )
    t.fill((42, 2, 13), (44, 3, 31), "minecraft:light_gray_concrete")
    t.fill((42, 4, 14), (42, 8, 29), "create:framed_glass")
    t.fill((42, 7, 20), (47, 8, 22), "minecraft:light_gray_concrete")


def _roof_process_system(t: base.Template) -> None:
    """Align four lane monitors with one connected transfer/service crown."""
    lane_ranges = ((18, 20), (24, 26), (30, 32), (36, 38))
    for x1, x2 in lane_ranges:
        base.shell(
            t,
            (x1, 12, 13),
            (x2, 15, 27),
            "create:framed_glass",
            "tfmg:steel_block",
            "minecraft:orange_concrete",
        )

    # North transfer crown ties all lane monitors to the destination trunk.
    base.shell(
        t,
        (16, 12, 7),
        (43, 15, 13),
        "tfmg:steel_block",
        "minecraft:light_gray_concrete",
        "minecraft:orange_concrete",
    )
    t.fill((18, 13, 6), (40, 15, 6), "minecraft:orange_concrete")

    # East roof-service bar terminates at the maintenance core and aligns with
    # the outbound return instead of becoming arbitrary roof clutter.
    base.shell(
        t,
        (40, 10, 10),
        (47, 14, 31),
        "immersiveengineering:sheetmetal_steel",
        "tfmg:steel_block",
        "minecraft:orange_concrete",
    )


def build_gate_a_massing() -> base.Template:
    t = base.Template(SIZE)
    _site_and_courts(t)
    _support_and_control_annex(t)
    _high_bay_shell_and_docks(t)
    _transfer_process_massing(t)
    _operator_and_maintenance_access(t)
    _roof_process_system(t)
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


def git_rev_parse(spec: str) -> str:
    result = subprocess.run(
        ["git", "rev-parse", spec],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    shipping_before = git_hash_object(SHIPPING_PATH)
    if shipping_before != FROZEN_BASELINE_BLOB:
        raise AssertionError(
            "OWS-010 shipping NBT no longer matches the independently reviewed Phase-0 blob"
        )

    planning_hashes = {str(path).replace("\\", "/"): sha256(ROOT / path) for path in PLANNING_INPUTS}
    t = build_gate_a_massing()
    if tuple(t.size) != SIZE:
        raise AssertionError(f"OWS-010 Gate-A r1 dimensions changed unexpectedly: {t.size}")
    if len(t.blocks) < 7000:
        raise AssertionError("OWS-010 Gate-A r1 massing is unexpectedly sparse")
    if any(not (0 <= x < SIZE[0] and 0 <= y < SIZE[1] and 0 <= z < SIZE[2]) for x, y, z in t.blocks):
        raise AssertionError("OWS-010 Gate-A r1 massing exceeds the frozen review envelope")

    required_mass_points = {
        "north_staff_canopy": (9, 8, 1),
        "control_records_crown": (14, 13, 12),
        "dock_01_crown": (20, 10, 35),
        "dock_04_crown": (41, 10, 35),
        "north_destination_trunk": (28, 3, 10),
        "operator_cross_aisle": (28, 8, 20),
        "east_outbound_return": (42, 5, 25),
        "east_maintenance_core": (47, 14, 22),
        "lane_01_monitor": (19, 15, 18),
        "lane_04_monitor": (37, 15, 18),
    }
    missing = [name for name, point in required_mass_points.items() if point not in t.blocks]
    if missing:
        raise AssertionError(f"OWS-010 Gate-A r1 missing required mass points: {missing}")

    for x in (19, 25, 31, 37):
        if any((x, 2, z) not in t.blocks for z in range(12, 29)):
            raise AssertionError(f"OWS-010 Gate-A r1 lane at X{x} is not continuous")

    t.save(TEMP_NAME)
    try:
        model_bytes = TEMP_NBT.read_bytes()
        size, blocks = unpack_structure(TEMP_NBT)
        occupied_min = [min(point[axis] for point in blocks) for axis in range(3)]
        occupied_max = [max(point[axis] for point in blocks) for axis in range(3)]
        head = git_rev_parse("HEAD")
        manifest = render_review_set(
            target=TARGET,
            gate="gate_a_massing",
            revision=f"massing-r1@{head[:8]}",
            damage_state="D0 intact massing only",
            source_commit=head,
            source_path="review-only:render_ows010_gate_a_massing.build_gate_a_massing()",
            size=size,
            blocks=blocks,
            output_dir=OUTPUT_DIR,
            camera_set=CAMERA_SET,
        )
        manifest["review_model_nbt_sha256"] = hashlib.sha256(model_bytes).hexdigest()
        manifest["review_builder_sha256"] = sha256(Path(__file__))
        manifest["review_model_non_air_blocks"] = len(blocks)
        manifest["review_model_occupied_bounds"] = {"min": occupied_min, "max": occupied_max}
        manifest["planning_input_sha256"] = planning_hashes
        manifest["phase0_baseline_manifest"] = (
            "old_world_narrative/reviews/heavy_rebuild/visual/OWS-010/"
            "baseline/r0_pre_heavy_rebuild/review_manifest.json"
        )
        manifest["frozen_phase0_source_commit"] = FROZEN_BASELINE_COMMIT
        manifest["frozen_phase0_shipping_git_blob"] = FROZEN_BASELINE_BLOB
        manifest["authoritative_shipping_modified"] = False
        manifest["shipping_nbt_git_blob_before"] = shipping_before
        manifest["shipping_nbt_git_blob_after"] = git_hash_object(SHIPPING_PATH)
        manifest["lor_006_manual_placed"] = False
        manifest["canonical_proof_placed"] = False
        manifest["pass_scope"] = "Pass 6 D0 massing only; Passes 7+ omitted"
        if manifest["shipping_nbt_git_blob_after"] != shipping_before:
            raise AssertionError("OWS-010 shipping NBT changed during review-only rendering")
        (OUTPUT_DIR / "review_manifest.json").write_text(
            json.dumps(manifest, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    finally:
        TEMP_NBT.unlink(missing_ok=True)

    print(
        f"Rendered {TARGET} Gate A r1 massing review at {manifest['dimensions']} using "
        f"{manifest['fixed_camera_set']}; independent visual approval remains pending."
    )


if __name__ == "__main__":
    main()
