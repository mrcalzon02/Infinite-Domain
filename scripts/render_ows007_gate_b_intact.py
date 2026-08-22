#!/usr/bin/env python3
"""Build and render the OWS-007 Gate-B r1 intact operating candidate.

The review model begins with the independently accepted Gate-A r1 massing and
adds Passes 7-12 only. It contains no history, damage, encounter architecture,
loot, proof chest, or final microdetail and never writes the shipping structure.
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
from render_ows007_gate_a_massing import build_gate_a_massing
from render_structure_review import unpack_structure


TEMP_NAME = "_heavy_review_ows007_gate_b_intact_r1"
TEMP_NBT = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{TEMP_NAME}.nbt"
OUTPUT_DIR = OUTPUT_ROOT / "OWS-007" / "gate_b_intact" / "r1"
SHIPPING_PATH = (
    ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" /
    "old_world" / "ows_007_vcf_ep7_agricultural_development_laboratory.nbt"
)
GATE_A_MODEL_SHA256 = "4a4be19f241afed420335f5b344162eaf2ab1577ae9e041a6ad198ba84d6c111"


def _pass7_structural_system(t: base.Template) -> None:
    """Give every accepted mass a legible, repeated load-bearing system."""
    # Room-aligned public facade bays divide the accepted cyan-glass frontage.
    for x in (11, 16, 21, 28, 33, 39):
        t.fill((x, 1, 5), (x, 8, 5), "minecraft:light_gray_concrete")
        t.fill((x, 8, 5), (x, 9, 15), "minecraft:light_gray_concrete")

    # Repeated transverse frames distinguish the three stepped chamber volumes.
    chambers = ((5, 17, 15, 44, 15), (17, 30, 13, 46, 18), (30, 42, 16, 43, 16))
    for x1, x2, z1, z2, roof_y in chambers:
        for z in (z1, (z1 + z2) // 2, z2):
            for x in (x1, x2):
                t.fill((x, 1, z), (x, roof_y, z), "tfmg:steel_block")
            t.fill((x1, roof_y - 1, z), (x2, roof_y, z), "tfmg:steel_block")

    # Phenotyping hinge and south service bar use shorter clean industrial bays.
    for x in (7, 14, 22, 30, 38, 44):
        t.fill((x, 1, 40), (x, 12, 40), "minecraft:light_gray_concrete")
        t.fill((x, 11, 40), (x, 12, 52), "minecraft:light_gray_concrete")
    for x in (3, 11, 20, 29, 38, 46):
        t.fill((x, 1, 50), (x, 9, 50), "tfmg:steel_block")
        t.fill((x, 8, 50), (x, 9, 59), "tfmg:steel_block")

    # The bridge receives explicit edge girders; rotunda radial ribs are tied to
    # an annular upper ring without changing its accepted flat crown.
    t.fill((38, 7, 29), (48, 8, 29), "tfmg:steel_block")
    t.fill((38, 7, 41), (48, 8, 41), "tfmg:steel_block")
    cx, cz = 57, 35
    for angle in range(0, 360, 45):
        radians = math.radians(angle)
        for radius in range(6, 13):
            x = cx + round(math.cos(radians) * radius)
            z = cz + round(math.sin(radians) * radius)
            t.set(x, 12, z, "tfmg:steel_block")

    # West environmental spine carries a continuous supported service header.
    t.fill((3, 18, 20), (6, 19, 51), "tfmg:steel_block")
    for z in (22, 30, 38, 46, 51):
        t.fill((2, 1, z), (7, 21, z), "minecraft:light_gray_concrete")


def _pass8_circulation_and_access(t: base.Template) -> None:
    """Separate visitor, staff, sample, waste, maintenance and test routes."""
    # Human-scaled visitor threshold and a protected observation promenade.
    t.clear((23, 2, 5), (26, 5, 6))
    base.double_door(t, 24, 2, 5, "north", "iron")
    t.fill((22, 1, 6), (28, 1, 14), "minecraft:quartz_block")
    t.fill((8, 1, 12), (42, 1, 15), "minecraft:smooth_quartz")

    # Staff badge threshold enters west prep without crossing visitor flow.
    t.clear((8, 2, 14), (10, 5, 16))
    base.double_door(t, 9, 2, 15, "south", "iron")

    # Chamber vestibules face the observation/control edge; rear doors return to
    # phenotyping and service. Each threshold is a full double door.
    for x, z, facing in (
        (11, 15, "south"), (22, 13, "south"), (35, 16, "south"),
        (11, 43, "north"), (22, 45, "north"), (35, 42, "north"),
    ):
        t.clear((x, 2, z), (x + 1, 4, z))
        base.double_door(t, x, 2, z, facing, "iron")

    # Receiving and waste thresholds remain separate on the accepted rear face.
    for x, label_facing in ((11, "south"), (35, "south")):
        t.fill((x - 2, 2, 59), (x + 3, 6, 59), "minecraft:light_gray_concrete")
        t.clear((x, 2, 59), (x + 1, 4, 59))
        base.double_door(t, x, 2, 59, label_facing, "iron")

    # Controlled service transfers close the accession-to-trial loop.
    for x in (12, 24, 36):
        t.clear((x, 2, 50), (x + 1, 4, 50))
        base.double_door(t, x, 2, 50, "north", "iron")

    # Two-wide staff stair reaches bridge level from phenotyping; a short east
    # stair completes the rise from bridge floor to the rotunda annulus.
    for x in (40, 41):
        base.stair_flight(t, x, 2, 49, 7, "north", "minecraft:smooth_quartz_stairs")
    t.fill((39, 8, 39), (42, 8, 44), "minecraft:smooth_stone")
    t.clear((39, 9, 39), (42, 12, 41))
    for step in range(4):
        for z in (34, 35):
            t.set(43 + step, 9 + step, z, "minecraft:smooth_quartz_stairs", facing="west", half="bottom", shape="straight", waterlogged="false")

    # Protected maintenance ladder remains wholly inside the west spine.
    t.clear((3, 2, 24), (5, 20, 26))
    for y in range(2, 21):
        t.set(3, y, 25, "minecraft:ladder", facing="east", waterlogged="false")
    t.fill((3, 21, 24), (7, 21, 28), "minecraft:oxidized_copper_grate")


def _pass9_exterior_architecture(t: base.Template) -> None:
    """Align glazing and thresholds to rooms while preserving Gate-A form."""
    # Supported public glazing becomes reception, exhibit and admin bays.
    for x1, x2 in ((12, 15), (17, 20), (29, 32), (34, 38)):
        t.fill((x1, 3, 5), (x2, 7, 5), "create:framed_glass")

    # Chamber observation windows stop at structure and correspond to modules.
    for x1, x2, z in ((7, 10, 14), (13, 16, 14), (19, 22, 12), (25, 28, 12), (32, 35, 15), (38, 40, 15)):
        t.fill((x1, 4, z), (x2, 8, z), "create:framed_glass")

    # Rear thresholds receive washable drains and explicit clean/waste aprons.
    t.fill((6, 0, 57), (19, 0, 57), "minecraft:oxidized_copper_grate")
    t.fill((29, 0, 57), (42, 0, 57), "minecraft:oxidized_copper_grate")
    t.fill((7, 0, 60), (18, 0, 61), "minecraft:white_concrete")
    t.fill((31, 0, 60), (40, 0, 61), "minecraft:gray_concrete")

    # Functional roof datum: monitor vents, environmental branch panels and
    # rotunda conditioning intake remain grouped rather than decorative clutter.
    for x, y, z in ((11, 20, 29), (24, 24, 29), (36, 22, 29)):
        t.fill((x - 2, y, z - 2), (x + 2, y + 1, z + 2), "minecraft:oxidized_copper_grate")
    t.fill((53, 26, 29), (61, 28, 29), "minecraft:cyan_concrete")


def _pass10_interior_architecture(t: base.Template) -> None:
    """Build legitimate rooms, boundaries and clear operational aisles."""
    # Public bar: exhibit, reception/security, staff threshold and admin review.
    t.fill((8, 1, 7), (42, 1, 15), "minecraft:quartz_block")
    base.partition_x(t, 18, 2, 7, 15, "minecraft:white_concrete", doorway_z=10)
    base.partition_x(t, 30, 2, 7, 15, "minecraft:white_concrete", doorway_z=10)
    t.fill((8, 2, 11), (42, 6, 11), "create:framed_glass")
    t.clear((23, 2, 11), (26, 4, 11))
    base.double_door(t, 24, 2, 11, "south", "iron")

    # Three independent controlled chambers retain two-block center aisles.
    for x1, x2, z1, z2 in ((6, 16, 16, 43), (18, 29, 14, 45), (31, 41, 17, 42)):
        t.fill((x1, 1, z1), (x2, 1, z2), "minecraft:smooth_stone")
    base.partition_z(t, 29, 2, 6, 16, "minecraft:white_concrete", doorways=(11,))
    base.partition_z(t, 31, 2, 18, 29, "minecraft:white_concrete", doorways=(23,))
    base.partition_z(t, 30, 2, 31, 41, "minecraft:cyan_concrete", doorways=(36,))
    for x, z in ((11, 29), (23, 31), (36, 30)):
        t.clear((x, 2, z), (x + 1, 4, z))
        base.double_door(t, x, 2, z, "south", "iron")

    # Phenotyping/reseeding hinge: scan hall, germination, food-quality review.
    t.fill((8, 1, 41), (43, 1, 51), "tfmg:factory_floor")
    base.partition_x(t, 27, 2, 41, 51, "minecraft:white_concrete", doorway_z=46)
    base.partition_x(t, 37, 2, 41, 51, "minecraft:white_concrete", doorway_z=46)
    t.fill((14, 2, 41), (26, 6, 41), "create:framed_glass")
    t.clear((11, 2, 40), (12, 4, 42))
    t.clear((22, 2, 40), (24, 4, 44))
    t.clear((35, 2, 40), (37, 4, 41))

    # South bar follows receipt -> accession/hold -> clean prep -> wash/waste -> records.
    t.fill((4, 1, 51), (45, 1, 58), "tfmg:factory_floor")
    for x in (17, 29, 39):
        base.partition_x(t, x, 2, 51, 58, "minecraft:light_gray_concrete", doorway_z=54)
        t.clear((x, 2, 56), (x, 4, 57))
        base.double_door(t, x, 2, 56, "east", "iron")
    t.fill((18, 1, 51), (28, 1, 58), "minecraft:smooth_stone")
    t.fill((40, 1, 51), (45, 1, 58), "minecraft:quartz_block")

    # Upper rotunda annulus receives a protected inner railing and lower test
    # floor is divided into four readable, reversible durability sectors.
    cx, cz = 57, 35
    for angle in range(0, 360, 15):
        radians = math.radians(angle)
        x = cx + round(math.cos(radians) * 6)
        z = cz + round(math.sin(radians) * 6)
        t.set(x, 13, z, "minecraft:iron_bars")
    t.fill((56, 1, 24), (58, 1, 46), "minecraft:smooth_quartz")
    t.fill((46, 1, 34), (68, 1, 36), "minecraft:smooth_quartz")


def _crop_bank(t: base.Template, x1: int, x2: int, z: int, crop: str) -> None:
    t.fill((x1, 2, z), (x2, 2, z + 1), "farmersdelight:rich_soil")
    for x in range(x1, x2 + 1, 2):
        t.set(x, 3, z, crop)
    t.fill((x1, 5, z), (x2, 5, z + 1), "create:fluid_pipe")


def _pass11_operational_systems(t: base.Template) -> None:
    """Install the intact lot-to-release durability-validation workflow."""
    # Receiving/accession, archive, cold hold, clean prep, wash and records.
    for x in (5, 10, 14):
        t.fill((x, 2, 53), (x + 2, 3, 55), "immersiveengineering:crate")
    base.desk(t, 13, 2, 52)
    t.fill((19, 2, 52), (21, 5, 54), "oritech:cooler_block")
    t.fill((24, 2, 52), (27, 4, 54), "minecraft:barrel", facing="up", open="false")
    t.set(25, 2, 55, "minecraft:brewing_stand", has_bottle_0="false", has_bottle_1="false", has_bottle_2="false")
    t.fill((30, 2, 52), (33, 5, 54), "create:fluid_tank")
    t.set(36, 2, 53, "minecraft:cauldron")
    t.fill((40, 2, 52), (45, 5, 53), "minecraft:bookshelf")
    base.desk(t, 40, 2, 54)

    # Chamber A: reference cultivation and baseline archive comparison.
    for z in (20, 26, 35, 40):
        _crop_bank(t, 7, 10, z, "minecraft:wheat")
        _crop_bank(t, 13, 15, z, "minecraft:carrots")
    t.fill((6, 11, 20), (16, 11, 40), "create:fluid_pipe")
    t.set(11, 12, 31, "create:encased_fan", facing="south")

    # Chamber B: dry-age, cold-soak and accelerated environmental stress racks.
    for z in (18, 24, 36, 42):
        t.fill((19, 2, z), (21, 5, z + 2), "minecraft:barrel", facing="up", open="false")
        t.fill((26, 2, z), (28, 5, z + 2), "oritech:cooler_block")
    t.fill((18, 14, 18), (29, 14, 42), "create:fluid_pipe")
    for x in (20, 27):
        t.set(x, 15, 30, "create:encased_fan", facing="south")

    # Chamber C: germination/reseeding and a bounded spore-survival suite.
    for z in (20, 26, 35, 39):
        _crop_bank(t, 32, 34, z, "minecraft:beetroots")
        _crop_bank(t, 38, 40, z, "minecraft:wheat")
    t.fill((32, 2, 31), (35, 4, 32), "create:framed_glass")
    for x in (33, 36, 39):
        t.set(x, 12, 28, "minecraft:brewing_stand", has_bottle_0="false", has_bottle_1="false", has_bottle_2="false")

    # Phenotyping scan line, reseeding bench and food-quality release review.
    t.fill((9, 2, 45), (24, 2, 46), "create:depot")
    for x in (10, 14, 18, 22):
        t.set(x, 3, 45, "ae2:terminal")
    for z in (44, 48):
        _crop_bank(t, 29, 34, z, "minecraft:wheat")
    base.desk(t, 38, 2, 44)
    base.desk(t, 38, 2, 48)

    # Connected environmental manifold runs from west plant to every chamber,
    # the phenotyping hinge and the rotunda conditioning cap.
    t.fill((4, 16, 24), (4, 16, 51), "create:fluid_pipe")
    t.fill((4, 10, 38), (58, 10, 38), "create:fluid_pipe")
    for x, top in ((11, 18), (24, 22), (36, 20), (43, 15), (57, 28)):
        t.fill((x, 10, 38), (x, top, 38), "create:fluid_pipe")
        t.set(x, 11, 39, "create:mechanical_pump", facing="south")

    # Rotunda lower sectors execute heat/dry, cold/soak, humidity and reseeding
    # comparisons around a shared environmental control node.
    for x, z, block in (
        (51, 29, "minecraft:barrel"), (62, 29, "oritech:cooler_block"),
        (51, 40, "create:fluid_tank"), (62, 40, "farmersdelight:rich_soil"),
    ):
        t.fill((x, 2, z), (x + 3, 5, z + 3), block)
    t.fill((55, 2, 33), (59, 6, 37), "immersiveengineering:sheetmetal_steel")
    for x, z in ((57, 29), (63, 35), (57, 41), (51, 35)):
        t.fill((x, 7, z), (57, 7, 35), "create:fluid_pipe")
    for x, z in ((50, 28), (64, 28), (50, 42), (64, 42)):
        t.set(x, 6, z, "create:encased_fan", facing="south")


def _pass12_institutional_identity(t: base.Template) -> None:
    """Apply restrained VCF identity and operational wayfinding."""
    base.wall_sign(t, 12, 7, 5, "north", "VERDANT CONTINUUM", "FOODS")
    base.wall_sign(t, 29, 7, 5, "north", "EP-7 AGRICULTURAL", "DEVELOPMENT LAB")
    base.wall_sign(t, 22, 5, 7, "south", "VISITOR RECEPTION", "OBSERVATION TOURS")
    base.wall_sign(t, 8, 5, 14, "south", "STAFF BADGE", "CONTROLLED ENTRY")
    base.wall_sign(t, 10, 6, 14, "north", "CHAMBER A", "REFERENCE CULTURE")
    base.wall_sign(t, 21, 6, 12, "north", "CHAMBER B", "DURABILITY STRESS")
    base.wall_sign(t, 34, 6, 15, "north", "CHAMBER C", "GERMINATION / RESEED")
    base.wall_sign(t, 8, 6, 51, "south", "SAMPLE RECEIVING", "LOT / ACCESSION")
    base.wall_sign(t, 19, 6, 51, "south", "ARCHIVE & HOLD", "COLD / DRY")
    base.wall_sign(t, 24, 6, 51, "south", "CLEAN PREPARATION", "BASELINE SAMPLE")
    base.wall_sign(t, 31, 6, 51, "south", "WASH / DECON", "SERVICE RETURN")
    base.wall_sign(t, 40, 6, 51, "south", "SECURE RECORDS", "RELEASE REVIEW")
    base.wall_sign(t, 10, 6, 40, "north", "PHENOTYPING", "SCAN / COMPARE")
    base.wall_sign(t, 28, 6, 40, "north", "RESEEDING", "GERMINATION LOOP")
    base.wall_sign(t, 38, 6, 40, "north", "FOOD QUALITY", "RELEASE DECISION")
    base.wall_sign(t, 41, 11, 29, "north", "DURABILITY ROTUNDA", "OBSERVATION BRIDGE")
    base.wall_sign(t, 49, 9, 35, "west", "ACCELERATED", "DURABILITY TESTS")
    base.wall_sign(t, 55, 8, 29, "north", "HEAT / DRY", "SECTOR A")
    base.wall_sign(t, 62, 8, 35, "east", "COLD / SOAK", "SECTOR B")
    base.wall_sign(t, 55, 14, 35, "west", "ANNULAR OVERLOOK", "AUTHORIZED STAFF")
    base.wall_sign(t, 3, 17, 28, "east", "ENVIRONMENTAL PLANT", "MAINTENANCE ONLY")
    base.wall_sign(t, 35, 7, 58, "south", "WASTE RETURN", "SEPARATE THRESHOLD")


def build_gate_b_intact() -> base.Template:
    t = build_gate_a_massing()
    _pass7_structural_system(t)
    _pass8_circulation_and_access(t)
    _pass9_exterior_architecture(t)
    _pass10_interior_architecture(t)
    _pass11_operational_systems(t)
    _pass12_institutional_identity(t)
    return t


def _name_at(t: base.Template, pos: tuple[int, int, int]) -> str | None:
    entry = t.blocks.get(pos)
    return None if entry is None else t.palette[entry[0]]["Name"]


def _assert_intact_contracts(t: base.Template) -> None:
    if tuple(t.size) != (73, 33, 63):
        raise AssertionError(f"OWS-007 Gate-B r1 dimensions changed unexpectedly: {t.size}")
    if any(not (0 <= x < 73 and 0 <= y < 33 and 0 <= z < 63) for x, y, z in t.blocks):
        raise AssertionError("OWS-007 Gate-B model exceeds the accepted envelope")

    # Representative points freeze all ten accepted Gate-A macro aspects.
    frozen = {
        (22, 0, 1): "minecraft:white_concrete",
        (16, 9, 2): "minecraft:white_concrete",
        (8, 19, 21): "minecraft:white_concrete",
        (20, 23, 19): "minecraft:white_concrete",
        (32, 21, 21): "minecraft:white_concrete",
        (13, 16, 43): "immersiveengineering:sheetmetal_steel",
        (25, 8, 59): "minecraft:light_gray_concrete",
        (2, 20, 32): "minecraft:light_gray_concrete",
        (40, 12, 28): "create:framed_glass",
        (57, 23, 24): "create:framed_glass",
        (52, 29, 30): "minecraft:white_concrete",
    }
    for pos, expected in frozen.items():
        actual = _name_at(t, pos)
        if actual != expected:
            raise AssertionError(f"Gate-A frozen aspect changed at {pos}: {actual} != {expected}")

    # Key controlled thresholds must contain complete two-block-high door pairs.
    for x, z in ((24, 5), (24, 11), (9, 15), (11, 15), (22, 13), (35, 16), (11, 59), (35, 59)):
        for dx in (0, 1):
            for y in (2, 3):
                if _name_at(t, (x + dx, y, z)) != "minecraft:iron_door":
                    raise AssertionError(f"Controlled door missing at {(x + dx, y, z)}")

    # Main visitor, chamber and service aisles remain clear at head height.
    protected = (
        ((23, 2, 7), (26, 3, 10)),
        ((11, 2, 17), (12, 3, 42)),
        ((23, 2, 16), (24, 3, 44)),
        ((36, 2, 18), (37, 3, 26)),
        ((36, 2, 31), (37, 3, 41)),
        ((8, 2, 47), (26, 3, 48)),
        ((5, 2, 56), (44, 3, 57)),
    )
    for low, high in protected:
        for x in range(low[0], high[0] + 1):
            for y in range(low[1], high[1] + 1):
                for z in range(low[2], high[2] + 1):
                    name = _name_at(t, (x, y, z))
                    if name not in {None, "minecraft:air"} and not name.endswith("_door"):
                        raise AssertionError(f"Protected circulation obstruction at {(x, y, z)}: {name}")

    names = [t.palette[entry[0]]["Name"] for entry in t.blocks.values()]
    forbidden = {"minecraft:chest", "minecraft:trapped_chest", "minecraft:spawner"}
    if forbidden.intersection(names):
        raise AssertionError("Gate-B contains deferred proof, loot, or encounter blocks")
    if sum(name.endswith("_wall_sign") for name in names) < 22:
        raise AssertionError("VCF/EP-7 wayfinding is unexpectedly sparse")
    if names.count("farmersdelight:rich_soil") < 70:
        raise AssertionError("Agricultural research program is unexpectedly sparse")
    if names.count("create:fluid_pipe") < 180:
        raise AssertionError("Environmental-service connectivity is unexpectedly sparse")


def git_hash_object(path: Path) -> str:
    result = subprocess.run(
        ["git", "hash-object", str(path.relative_to(ROOT))], cwd=ROOT, check=True,
        capture_output=True, text=True,
    )
    return result.stdout.strip()


def main() -> None:
    shipping_before = git_hash_object(SHIPPING_PATH)
    t = build_gate_b_intact()
    _assert_intact_contracts(t)
    t.save(TEMP_NAME)
    try:
        model_bytes = TEMP_NBT.read_bytes()
        size, blocks = unpack_structure(TEMP_NBT)
        if len(blocks) < 19000:
            raise AssertionError(f"Gate-B r1 intact model is unexpectedly sparse: {len(blocks)}")
        revision = os.environ.get("GITHUB_SHA", "local")[:8]
        manifest = render_review_set(
            target="OWS-007", gate="gate_b_intact", revision=f"intact-r1@{revision}",
            damage_state="D0 intact / operational", source_commit=os.environ.get("GITHUB_SHA", "working-tree"),
            source_path="review-only:render_ows007_gate_b_intact.build_gate_b_intact()",
            size=size, blocks=blocks, output_dir=OUTPUT_DIR, camera_set="ows007_fixed_v1",
        )
        manifest["review_model_nbt_sha256"] = hashlib.sha256(model_bytes).hexdigest()
        manifest["review_builder_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        manifest["gate_a_model_sha256"] = GATE_A_MODEL_SHA256
        manifest["placed_positions"] = len(blocks)
        manifest["gate_a_frozen_aspects_asserted"] = 10
        manifest["gate_b_obligations_implemented"] = 6
        manifest["proof_encounters_damage_present"] = False
        manifest["authoritative_shipping_modified"] = False
        manifest["shipping_nbt_git_blob_before"] = shipping_before
        manifest["shipping_nbt_git_blob_after"] = git_hash_object(SHIPPING_PATH)
        if manifest["shipping_nbt_git_blob_after"] != shipping_before:
            raise AssertionError("OWS-007 shipping NBT changed during review-only rendering")
        (OUTPUT_DIR / "review_manifest.json").write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n"
        )
    finally:
        TEMP_NBT.unlink(missing_ok=True)

    print(
        f"Rendered OWS-007 Gate B r1 intact review at {manifest['dimensions']} using "
        f"{manifest['fixed_camera_set']}; independent visual approval remains pending."
    )


if __name__ == "__main__":
    main()
