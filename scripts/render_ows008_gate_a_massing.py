#!/usr/bin/env python3
"""Build and render the review-only OWS-008 Gate-A r1 massing candidate.

<<<<<<< Updated upstream
The model proves the incident-command, analysis, treatment, verification,
service-joint and plant hierarchy before structure, circulation, operational
equipment, proof loot, history, encounters, damage, or microdetail are added.
It never writes shared state or authoritative shipping NBT.
=======
The model proves the public/dirty/validation/analysis/service hierarchy before
structure, playable circulation, equipment, proof, history, encounters, damage,
or microdetail. It never writes shared state or authoritative shipping NBT.
>>>>>>> Stashed changes
"""
from __future__ import annotations

import hashlib
import json
<<<<<<< Updated upstream
import os
=======
>>>>>>> Stashed changes
import subprocess
from pathlib import Path

import generate_wasteland_sites as base
from render_old_world_heavy_rebuild_review import OUTPUT_ROOT, ROOT, render_review_set
from render_structure_review import unpack_structure


<<<<<<< Updated upstream
TEMP_NAME = "_heavy_review_ows008_gate_a_massing_r1"
TEMP_NBT = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{TEMP_NAME}.nbt"
OUTPUT_DIR = OUTPUT_ROOT / "OWS-008" / "gate_a_massing" / "r1"
SHIPPING_PATH = (
    ROOT
    / "kubejs"
    / "data"
    / "infinite_domain"
    / "structure"
    / "wasteland"
    / "old_world"
    / "ows_008_vcf_emergency_persistence_investigation_lab.nbt"
=======
TARGET = "OWS-008"
SIZE = (55, 22, 49)
CAMERA_SET = "ows008_fixed_v1"
FROZEN_BASELINE_COMMIT = "e14b3f35306fc313e7ea9a114f2384696864533a"
FROZEN_BASELINE_BLOB = "6646d96d5723bb8d1b611de8354dea41396cb6df"
TEMP_NAME = "_heavy_review_ows008_gate_a_massing_r1"
TEMP_NBT = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{TEMP_NAME}.nbt"
OUTPUT_DIR = OUTPUT_ROOT / TARGET / "gate_a_massing" / "r1"
SHIPPING_RELATIVE = Path(
    "kubejs/data/infinite_domain/structure/wasteland/old_world/"
    "ows_008_vcf_emergency_persistence_investigation_lab.nbt"
)
SHIPPING_PATH = ROOT / SHIPPING_RELATIVE
PLANNING_INPUTS = (
    Path("old_world_narrative/reviews/heavy_rebuild/OWS-008_PHASE0_BASELINE_REVIEW.md"),
    Path("old_world_narrative/reviews/heavy_rebuild/OWS-008_PASS2_FUNCTIONAL_DEFINITION.md"),
    Path("old_world_narrative/reviews/heavy_rebuild/OWS-008_PASS3_PRECEDENT_RESEARCH.md"),
    Path("old_world_narrative/reviews/heavy_rebuild/OWS-008_PASS4_PROGRAM_ADJACENCY.md"),
    Path("old_world_narrative/reviews/heavy_rebuild/OWS-008_PASS5_SCALE_TRANSLATION.md"),
>>>>>>> Stashed changes
)


def _site_and_thresholds(t: base.Template) -> None:
<<<<<<< Updated upstream
    """Separate public command, incident receipt, and rear service approaches."""
    t.fill((1, 0, 1), (53, 0, 47), "minecraft:grass_block")

    # North command forecourt: a human-scaled institutional approach rather
    # than a road entering the containment plant.
    t.fill((3, 0, 1), (31, 0, 9), "minecraft:smooth_stone")
    t.fill((12, 0, 0), (20, 0, 12), "minecraft:white_concrete")
    t.fill((5, 0, 2), (5, 0, 8), "minecraft:lime_concrete")
    t.fill((29, 0, 2), (29, 0, 8), "minecraft:lime_concrete")

    # East sealed-specimen apron is intentionally narrow and does not merge
    # with the south maintenance/waste court.
    t.fill((47, 0, 7), (53, 0, 30), "minecraft:light_gray_concrete")
    for z in (10, 18, 26):
        t.fill((50, 0, z), (53, 0, z), "minecraft:yellow_concrete")

    # Rear plant court reserves two independent service thresholds and a
    # central exclusion strip between maintenance and treated-waste handling.
    t.fill((2, 0, 39), (52, 0, 47), "tfmg:asphalt")
    t.fill((24, 0, 40), (28, 0, 47), "minecraft:light_gray_concrete")
    for x in (5, 15, 36, 47):
        t.fill((x, 0, 43), (x, 0, 47), "minecraft:white_concrete")


def _incident_command_threshold(t: base.Template) -> None:
    """Create a low VCF command face with a raised protected overview."""
    base.shell(
        t,
        (4, 1, 5),
        (31, 8, 14),
=======
    """Separate public, incident-receipt, clean-delivery and waste approaches."""
    t.fill((0, 0, 0), (54, 0, 48), "minecraft:grass_block")

    # North public forecourt and institutional arrival axis.
    t.fill((10, 0, 0), (43, 0, 12), "minecraft:smooth_stone")
    t.fill((24, 0, 0), (30, 0, 15), "minecraft:white_concrete")
    for x in (12, 41):
        t.fill((x, 0, 2), (x, 0, 10), "minecraft:lime_concrete")

    # East incident-receipt lane and southeast contaminated-waste apron.
    t.fill((47, 0, 9), (54, 0, 47), "tfmg:asphalt")
    t.fill((34, 0, 39), (54, 0, 48), "tfmg:asphalt")
    t.fill((51, 0, 12), (54, 0, 30), "minecraft:yellow_concrete")

    # West clean-delivery/staff edge remains separate from dirty receiving.
    t.fill((0, 0, 13), (7, 0, 32), "minecraft:smooth_stone")
    t.fill((0, 0, 16), (4, 0, 20), "minecraft:lime_concrete")


def _public_bar_and_gallery(t: base.Template) -> None:
    """Create a human-scaled VCF front and controlled validation overlook."""
    base.shell(
        t,
        (13, 1, 4),
        (41, 8, 14),
>>>>>>> Stashed changes
        "minecraft:white_concrete",
        "minecraft:smooth_stone",
        "minecraft:light_gray_concrete",
    )
<<<<<<< Updated upstream

    # Glazing is confined to the public/command face and corresponds to the
    # future briefing and status functions behind it.
    t.fill((7, 3, 4), (28, 6, 4), "create:framed_glass")
    t.clear((13, 2, 4), (20, 6, 5))
    t.fill((8, 7, 4), (27, 8, 4), "minecraft:lime_concrete")

    # A supported offset canopy makes the incident entrance obvious without
    # increasing the entire facade to prestige-lobby scale.
    t.fill((10, 8, 1), (24, 8, 7), "minecraft:white_concrete")
    for x in (10, 24):
        t.fill((x, 1, 2), (x, 7, 2), "minecraft:light_gray_concrete")

    # Raised command/observation lantern bridges toward the laboratory core.
    base.shell(
        t,
        (9, 8, 10),
        (29, 13, 18),
        "create:framed_glass",
        "minecraft:light_gray_concrete",
        "minecraft:white_concrete",
    )
    t.fill((11, 12, 9), (27, 13, 9), "minecraft:lime_concrete")


def _analysis_wing(t: base.Template) -> None:
    """Establish the stepped west custody, examination, and analysis mass."""
    base.shell(
        t,
        (3, 1, 13),
        (20, 15, 34),
=======
    t.fill((16, 2, 3), (38, 6, 3), "create:framed_glass")
    t.clear((24, 2, 3), (30, 5, 4))
    t.fill((17, 7, 3), (37, 8, 3), "minecraft:lime_concrete")

    # Deep supported canopy makes the north public entrance unambiguous.
    t.fill((19, 8, 0), (35, 8, 6), "minecraft:white_concrete")
    for x in (19, 35):
        t.fill((x, 1, 1), (x, 7, 1), "minecraft:light_gray_concrete")

    # A transverse gallery joins public orientation to the four-stage process.
    base.shell(
        t,
        (7, 1, 12),
        (47, 9, 22),
>>>>>>> Stashed changes
        "minecraft:white_concrete",
        "minecraft:smooth_stone",
        "minecraft:light_gray_concrete",
    )
<<<<<<< Updated upstream

    # A lower southern records/custody shoulder prevents a single tall box and
    # creates a protected hinge toward plant and service access.
    base.shell(
        t,
        (5, 1, 31),
        (23, 11, 41),
        "minecraft:light_gray_concrete",
        "minecraft:smooth_stone",
        "minecraft:white_concrete",
    )

    # Controlled observation strips occur only where upper analysis faces the
    # test array. The window-poor west wall remains appropriate to custody.
    t.fill((19, 8, 17), (20, 12, 29), "create:framed_glass")
    t.fill((8, 5, 12), (16, 8, 12), "create:framed_glass")

    # A raised light/service monitor gives the two-level research wing a roof
    # identity separate from containment stacks and rear plant.
    base.shell(
        t,
        (7, 15, 18),
        (16, 18, 31),
=======
    t.fill((10, 3, 22), (44, 7, 22), "create:framed_glass")
    for x in (10, 19, 29, 39, 44):
        t.fill((x, 1, 21), (x, 9, 22), "minecraft:light_gray_concrete")

    # The west-biased raised lantern reserves incident command/overview without
    # turning the complete site into a uniform second storey.
    base.shell(
        t,
        (8, 9, 13),
        (21, 14, 21),
>>>>>>> Stashed changes
        "create:framed_glass",
        "minecraft:light_gray_concrete",
        "minecraft:white_concrete",
    )


<<<<<<< Updated upstream
def _treatment_and_verification_array(t: base.Template) -> None:
    """Build four related but non-cloned treatment and verification masses."""
    modules = (
        # wash/chemical cell: low, broad and closest to dirty accession
        ((20, 1, 11), (32, 10, 22), 7, "minecraft:cyan_concrete"),
        # heat/steam cell: thicker and taller technical chamber
        ((31, 1, 12), (44, 12, 23), 9, "minecraft:yellow_concrete"),
        # air/filter intervention: stepped southward under a raised plenum
        ((22, 1, 21), (35, 11, 32), 8, "minecraft:cyan_concrete"),
        # combined-procedure revision: largest and latest emergency mass
        ((34, 1, 22), (50, 13, 35), 10, "minecraft:yellow_concrete"),
    )

    for lo, hi, datum_y, datum_block in modules:
=======
def _validation_sequence(t: base.Template) -> None:
    """Express four related but distinct treatment/verification volumes."""
    cells = (
        # name, lower, upper, emergency/service accent
        ("D_persistence", (6, 1, 24), (16, 14, 39), "minecraft:lime_concrete"),
        ("C_clean_hold", (17, 1, 22), (27, 11, 37), "minecraft:white_concrete"),
        ("B_chemical", (28, 1, 20), (39, 16, 36), "minecraft:yellow_concrete"),
        ("A_wet_thermal", (40, 1, 18), (50, 12, 34), "minecraft:cyan_concrete"),
    )
    for _name, lo, hi, accent in cells:
>>>>>>> Stashed changes
        base.shell(
            t,
            lo,
            hi,
            "minecraft:white_concrete",
            "minecraft:smooth_stone",
            "minecraft:light_gray_concrete",
        )
<<<<<<< Updated upstream
        x1, _, z1 = lo
        x2, _, z2 = hi

        # The west/observation face is selectively glazed. Technical east and
        # rear faces retain mass and boundary depth.
        t.fill((x1, 3, z1 + 2), (x1, min(datum_y, hi[1] - 2), z2 - 2), "create:framed_glass")
        t.fill((x1, datum_y, z1), (x2, datum_y + 1, z1), datum_block)

    # A protected upper observation spine joins command, analysis, treatment,
    # and challenge without becoming a decorative one-block catwalk.
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

    # Two coherent treatment plenums align to the modules below; their height
    # and placement distinguish process systems without a random pipe forest.
    base.shell(
        t,
        (33, 12, 14),
        (41, 16, 21),
        "immersiveengineering:sheetmetal_steel",
        "minecraft:smooth_stone",
        "minecraft:light_gray_concrete",
    )
    base.shell(
        t,
        (40, 13, 25),
        (48, 17, 33),
        "immersiveengineering:sheetmetal_steel",
        "minecraft:smooth_stone",
        "minecraft:light_gray_concrete",
    )


def _persistence_hall_and_joint_gallery(t: base.Template) -> None:
    """Reserve the double-height challenge hall and concealed-service anatomy."""
    base.shell(
        t,
        (20, 1, 29),
        (45, 17, 43),
        "minecraft:white_concrete",
        "minecraft:smooth_stone",
        "minecraft:light_gray_concrete",
    )

    # Tall north/west observation faces make the future clean-face versus
    # concealed-joint contradiction visible from approach and section views.
    t.fill((23, 5, 28), (40, 12, 28), "create:framed_glass")
    t.fill((19, 4, 32), (19, 12, 39), "create:framed_glass")

    # The clerestory is smaller than the hall below and preserves a stepped,
    # technically credible silhouette within the retained 22-block height.
    base.shell(
        t,
        (24, 17, 32),
        (40, 20, 40),
        "create:framed_glass",
        "minecraft:light_gray_concrete",
        "minecraft:white_concrete",
    )

    # A narrow, deliberately solid technical bar sits behind the challenge
    # face. Later passes will resolve the 2–3 block gallery and forensic bays.
    base.shell(
        t,
        (44, 1, 29),
        (51, 12, 43),
        "immersiveengineering:sheetmetal_steel",
        "minecraft:smooth_stone",
        "minecraft:light_gray_concrete",
    )
    t.fill((43, 6, 31), (43, 9, 41), "minecraft:yellow_concrete")


def _rear_plant_and_receiving(t: base.Template) -> None:
    """Consolidate the technical plant and keep receipt/waste thresholds apart."""
    # Rear air/wash/sterilant plant occupies one coherent mass linked to the
    # laboratory systems rather than several unrelated roof boxes.
    base.shell(
        t,
        (3, 1, 38),
        (23, 10, 47),
=======
        x1, _y1, z1 = lo
        x2, y2, z2 = hi
        # Observation faces align to the gallery; vertical edge piers prevent
        # the sequence reading as one glass greenhouse wall.
        t.fill((x1 + 2, 3, z1 - 1), (x2 - 2, min(8, y2 - 2), z1 - 1), "create:framed_glass")
        for x in (x1, x2):
            t.fill((x, 1, z1 - 1), (x, y2, z1 - 1), "minecraft:light_gray_concrete")
        # A restrained high service band differentiates the process family.
        t.fill((x1 + 1, max(6, y2 - 3), z2), (x2 - 1, y2 - 1, z2), accent)

    # Distinct service monitors explain the stepped height sequence.
    base.shell(
        t,
        (8, 14, 28),
        (14, 18, 35),
        "create:framed_glass",
        "minecraft:light_gray_concrete",
        "minecraft:lime_concrete",
    )
    base.shell(
        t,
        (19, 11, 26),
        (25, 15, 33),
        "minecraft:white_concrete",
        "minecraft:light_gray_concrete",
        "minecraft:white_concrete",
    )
    base.shell(
        t,
        (30, 16, 24),
        (37, 20, 32),
        "immersiveengineering:sheetmetal_steel",
        "minecraft:light_gray_concrete",
        "minecraft:yellow_concrete",
    )
    base.shell(
        t,
        (42, 12, 22),
        (48, 17, 29),
        "tfmg:steel_block",
        "minecraft:light_gray_concrete",
        "minecraft:cyan_concrete",
    )


def _support_wings(t: base.Template) -> None:
    """Reserve clean analysis/command west and dirty receiving east."""
    base.shell(
        t,
        (2, 1, 12),
        (9, 12, 43),
        "minecraft:white_concrete",
        "minecraft:smooth_stone",
        "minecraft:light_gray_concrete",
    )
    t.fill((1, 3, 16), (1, 8, 28), "create:framed_glass")
    for z in (15, 24, 33, 41):
        t.fill((1, 1, z), (2, 12, z), "minecraft:light_gray_concrete")

    # Upper west command/archive mass supervises the gallery and remains
    # separate from the specimen route.
    base.shell(
        t,
        (2, 12, 17),
        (15, 17, 33),
        "minecraft:white_concrete",
        "minecraft:light_gray_concrete",
        "minecraft:lime_concrete",
    )
    t.fill((15, 13, 20), (15, 16, 30), "create:framed_glass")

    # East dirty receipt is lower and heavier, connected to the asphalt lane.
    base.shell(
        t,
        (48, 1, 10),
        (53, 10, 41),
>>>>>>> Stashed changes
        "minecraft:light_gray_concrete",
        "tfmg:factory_floor",
        "minecraft:white_concrete",
    )
<<<<<<< Updated upstream
    t.clear((6, 2, 47), (13, 7, 47))
    t.fill((5, 8, 46), (14, 10, 48), "tfmg:steel_block")

    # A raised filter/wash plant sits directly above the service bar and below
    # the height of the persistence clerestory.
    base.shell(
        t,
        (7, 10, 39),
        (18, 16, 47),
        "immersiveengineering:sheetmetal_steel",
        "minecraft:smooth_stone",
        "minecraft:light_gray_concrete",
    )

    # Rear treated-waste and maintenance bar forms the second back-of-house
    # threshold; the two openings are visually and spatially separated.
    base.shell(
        t,
        (27, 1, 40),
        (52, 9, 47),
=======
    t.clear((52, 2, 14), (53, 7, 21))
    t.fill((49, 8, 12), (54, 10, 23), "minecraft:yellow_concrete")
    t.fill((53, 3, 27), (53, 7, 36), "create:framed_glass")


def _service_spine_and_plant(t: base.Template) -> None:
    """Tie every process cell to one navigable service/inspection mass."""
    base.shell(
        t,
        (5, 1, 37),
        (51, 9, 46),
>>>>>>> Stashed changes
        "minecraft:light_gray_concrete",
        "tfmg:factory_floor",
        "minecraft:white_concrete",
    )
<<<<<<< Updated upstream
    for x1, x2 in ((31, 37), (43, 49)):
        t.clear((x1, 2, 47), (x2, 6, 47))
        t.fill((x1 - 1, 7, 46), (x2 + 1, 9, 48), "tfmg:steel_block")

    # East sealed-specimen receipt is a low sidecar attached to the dirty end
    # of the array, not a public entrance or general loading dock.
    base.shell(
        t,
        (47, 1, 9),
        (53, 8, 27),
        "minecraft:white_concrete",
        "minecraft:smooth_stone",
        "minecraft:light_gray_concrete",
    )
    t.clear((52, 2, 13), (53, 6, 18))
    t.fill((50, 7, 11), (54, 9, 20), "tfmg:steel_block")

    # One controlled exhaust stack and a separate lower intake housing are
    # traceable to the rear/service and treatment masses below.
    t.fill((46, 13, 35), (48, 21, 37), "tfmg:steel_block")
    t.fill((45, 20, 34), (49, 21, 38), "minecraft:light_gray_concrete")
    base.shell(
        t,
        (2, 9, 31),
        (7, 13, 37),
        "immersiveengineering:sheetmetal_steel",
        "minecraft:smooth_stone",
        "minecraft:white_concrete",
    )


def build_gate_a_massing() -> base.Template:
    t = base.Template((55, 22, 49))
    _site_and_thresholds(t)
    _incident_command_threshold(t)
    _analysis_wing(t)
    _treatment_and_verification_array(t)
    _persistence_hall_and_joint_gallery(t)
    _rear_plant_and_receiving(t)
=======

    # Opposed clean-delivery and contaminated-waste thresholds remain visible.
    t.clear((5, 2, 40), (6, 6, 44))
    t.fill((3, 7, 39), (8, 9, 45), "minecraft:lime_concrete")
    t.clear((46, 2, 45), (51, 6, 46))
    t.fill((44, 7, 44), (52, 9, 47), "minecraft:yellow_concrete")

    # Raised interstitial inspection bar expresses the concealed-joint spine.
    base.shell(
        t,
        (8, 9, 39),
        (45, 12, 44),
        "immersiveengineering:sheetmetal_steel",
        "minecraft:light_gray_concrete",
        "minecraft:white_concrete",
    )
    for x in (11, 22, 33, 43):
        t.fill((x, 12, 39), (x + 2, 15, 43), "tfmg:steel_block")

    # East maintenance core reaches the highest purge monitor and roof service.
    base.shell(
        t,
        (46, 1, 34),
        (52, 18, 46),
        "minecraft:light_gray_concrete",
        "minecraft:smooth_stone",
        "minecraft:white_concrete",
    )
    t.fill((45, 4, 37), (45, 15, 43), "create:framed_glass")


def build_gate_a_massing() -> base.Template:
    t = base.Template(SIZE)
    _site_and_thresholds(t)
    _public_bar_and_gallery(t)
    _validation_sequence(t)
    _support_wings(t)
    _service_spine_and_plant(t)
>>>>>>> Stashed changes
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


<<<<<<< Updated upstream
def main() -> None:
    shipping_before = git_hash_object(SHIPPING_PATH)
    t = build_gate_a_massing()
    if tuple(t.size) != (55, 22, 49):
        raise AssertionError(f"OWS-008 Gate-A r1 dimensions changed unexpectedly: {t.size}")
    if len(t.blocks) < 9000:
        raise AssertionError("OWS-008 Gate-A r1 massing is unexpectedly sparse")
    if any(not (0 <= x < 55 and 0 <= y < 22 and 0 <= z < 49) for x, y, z in t.blocks):
        raise AssertionError("OWS-008 Gate-A r1 massing exceeds the retained review envelope")

    TEMP_NBT.unlink(missing_ok=True)
=======
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
            "OWS-008 shipping NBT no longer matches the independently reviewed Phase-0 blob"
        )

    planning_hashes = {str(path).replace("\\", "/"): sha256(ROOT / path) for path in PLANNING_INPUTS}
    t = build_gate_a_massing()
    if tuple(t.size) != SIZE:
        raise AssertionError(f"OWS-008 Gate-A r1 dimensions changed unexpectedly: {t.size}")
    if len(t.blocks) < 10000:
        raise AssertionError("OWS-008 Gate-A r1 massing is unexpectedly sparse")
    if any(not (0 <= x < SIZE[0] and 0 <= y < SIZE[1] and 0 <= z < SIZE[2]) for x, y, z in t.blocks):
        raise AssertionError("OWS-008 Gate-A r1 massing exceeds the retained review envelope")

    required_mass_points = {
        "public_canopy": (27, 8, 1),
        "west_command": (4, 17, 24),
        "persistence_monitor": (10, 18, 31),
        "chemical_purge_monitor": (33, 20, 28),
        "east_dirty_receipt": (53, 9, 18),
        "joint_inspection_spine": (20, 12, 41),
        "maintenance_core": (50, 18, 40),
    }
    missing = [name for name, point in required_mass_points.items() if point not in t.blocks]
    if missing:
        raise AssertionError(f"OWS-008 Gate-A r1 missing required mass points: {missing}")

>>>>>>> Stashed changes
    t.save(TEMP_NAME)
    try:
        model_bytes = TEMP_NBT.read_bytes()
        size, blocks = unpack_structure(TEMP_NBT)
<<<<<<< Updated upstream
        if tuple(size) != (55, 22, 49):
            raise AssertionError(f"Serialized review model has unexpected size: {size}")
        revision = os.environ.get("GITHUB_SHA", "local")[:8]
        manifest = render_review_set(
            target="OWS-008",
            gate="gate_a_massing",
            revision=f"massing-r1@{revision}",
            damage_state="D0 intact massing only",
            source_commit=os.environ.get("GITHUB_SHA", "working-tree"),
=======
        occupied_min = [min(point[axis] for point in blocks) for axis in range(3)]
        occupied_max = [max(point[axis] for point in blocks) for axis in range(3)]
        head = git_rev_parse("HEAD")
        manifest = render_review_set(
            target=TARGET,
            gate="gate_a_massing",
            revision=f"massing-r1@{head[:8]}",
            damage_state="D0 intact massing only",
            source_commit=head,
>>>>>>> Stashed changes
            source_path="review-only:render_ows008_gate_a_massing.build_gate_a_massing()",
            size=size,
            blocks=blocks,
            output_dir=OUTPUT_DIR,
<<<<<<< Updated upstream
            camera_set="ows008_fixed_v1",
        )
        manifest["review_model_nbt_sha256"] = hashlib.sha256(model_bytes).hexdigest()
        manifest["review_builder_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        manifest["review_model_block_positions"] = len(t.blocks)
        used_names = [t.palette[state_index]["Name"] for state_index, _ in t.blocks.values()]
        manifest["review_model_non_air_positions"] = sum(name != "minecraft:air" for name in used_names)
        manifest["review_model_explicit_air_positions"] = sum(name == "minecraft:air" for name in used_names)
        manifest["review_model_palette_states"] = len(t.palette)
        manifest["review_model_block_entities"] = sum(nbt is not None for _, nbt in t.blocks.values())
        manifest["review_model_entities"] = len(t.entities)
=======
            camera_set=CAMERA_SET,
        )
        manifest["review_model_nbt_sha256"] = hashlib.sha256(model_bytes).hexdigest()
        manifest["review_builder_sha256"] = sha256(Path(__file__))
        manifest["review_model_non_air_blocks"] = len(blocks)
        manifest["review_model_occupied_bounds"] = {"min": occupied_min, "max": occupied_max}
        manifest["planning_input_sha256"] = planning_hashes
        manifest["phase0_baseline_manifest"] = (
            "old_world_narrative/reviews/heavy_rebuild/visual/OWS-008/"
            "baseline/r0_pre_heavy_rebuild/review_manifest.json"
        )
        manifest["frozen_phase0_source_commit"] = FROZEN_BASELINE_COMMIT
        manifest["frozen_phase0_shipping_git_blob"] = FROZEN_BASELINE_BLOB
>>>>>>> Stashed changes
        manifest["authoritative_shipping_modified"] = False
        manifest["shipping_nbt_git_blob_before"] = shipping_before
        manifest["shipping_nbt_git_blob_after"] = git_hash_object(SHIPPING_PATH)
        if manifest["shipping_nbt_git_blob_after"] != shipping_before:
            raise AssertionError("OWS-008 shipping NBT changed during review-only rendering")
        (OUTPUT_DIR / "review_manifest.json").write_text(
            json.dumps(manifest, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    finally:
        TEMP_NBT.unlink(missing_ok=True)

    print(
<<<<<<< Updated upstream
        f"Rendered OWS-008 Gate A r1 massing review at {manifest['dimensions']} using "
=======
        f"Rendered {TARGET} Gate A r1 massing review at {manifest['dimensions']} using "
>>>>>>> Stashed changes
        f"{manifest['fixed_camera_set']}; independent visual approval remains pending."
    )


if __name__ == "__main__":
    main()
