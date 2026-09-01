#!/usr/bin/env python3
"""Build and render the OWS-006 Gate-B r1 intact operating candidate.

The model starts from the independently accepted Gate-A r1 massing and adds
Passes 7-12 only. It contains no proof loot, encounters, anomaly history,
damage, or final microdetail, and never writes shared state or shipping NBT.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path

import generate_wasteland_sites as base
from render_old_world_heavy_rebuild_review import OUTPUT_ROOT, ROOT, render_review_set
from render_ows006_gate_a_massing import build_gate_a_massing
from render_structure_review import unpack_structure


TEMP_NAME = "_heavy_review_ows006_gate_b_intact_r1"
TEMP_NBT = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{TEMP_NAME}.nbt"
OUTPUT_DIR = OUTPUT_ROOT / "OWS-006" / "gate_b_intact" / "r1"
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
GATE_A_MODEL_SHA256 = "76c05221b6f837f6aef074867387c028d63dc9bd90649e864062509882988a88"


def _pass7_structural_system(t: base.Template) -> None:
    """Resolve the accepted study masses as one supported laboratory frame."""
    # Public bar and observation gallery use a regular institutional bay grid.
    for x in (9, 19, 29, 39, 49):
        t.fill((x, 1, 6), (x, 8, 6), "minecraft:light_gray_concrete")
        t.fill((x, 8, 6), (x, 9, 16), "minecraft:light_gray_concrete")
    for x in (11, 24, 37, 50):
        t.fill((x, 1, 13), (x, 9, 13), "tfmg:steel_block")
        t.fill((x, 8, 13), (x, 9, 22), "tfmg:steel_block")

    # Each chamber receives front/rear frames and roof beams aligned with its
    # accepted footprint and monitor rather than an unsupported flat shell.
    chambers = (
        (12, 24, 21, 40, 15),
        (24, 37, 20, 41, 18),
        (37, 49, 22, 40, 16),
    )
    for x1, x2, z1, z2, roof_y in chambers:
        for z in (z1, (z1 + z2) // 2, z2):
            t.fill((x1, 1, z), (x1, roof_y, z), "tfmg:steel_block")
            t.fill((x2, 1, z), (x2, roof_y, z), "tfmg:steel_block")
            t.fill((x1, roof_y - 1, z), (x2, roof_y, z), "tfmg:steel_block")

    # Support wings gain shorter frames tied into the chamber and service grid.
    for z in (14, 23, 32, 41, 43):
        t.fill((2, 1, z), (2, 11, z), "minecraft:light_gray_concrete")
        t.fill((13, 1, z), (13, 11, z), "minecraft:light_gray_concrete")
    for z in (13, 22, 31, 40, 42):
        t.fill((48, 1, z), (48, 13, z), "tfmg:steel_block")
        t.fill((56, 1, z), (56, 13, z), "tfmg:steel_block")

    # Rear plant deck and service spine have explicit support under branch
    # plenums and the accepted east maintenance core.
    for x in (10, 21, 32, 43, 51):
        t.fill((x, 1, 39), (x, 15, 39), "tfmg:steel_block")
        t.fill((x, 9, 39), (x, 10, 48), "tfmg:steel_block")
    t.fill((13, 15, 40), (48, 16, 48), "tfmg:steel_block")

    # Roof drainage follows real volumes rather than becoming random pipe noise.
    for x, z, top in ((9, 6, 8), (49, 16, 8), (12, 40, 15), (49, 40, 16), (56, 42, 21)):
        t.fill((x, 1, z), (x, top, z), "create:fluid_pipe")


def _double_iron_door_z(t: base.Template, x: int, z: int, facing: str = "south") -> None:
    t.clear((x, 2, z), (x + 1, 4, z))
    base.double_door(t, x, 2, z, facing, "iron")


def _pass8_circulation_and_access(t: base.Template) -> None:
    """Create public, staff, sample, waste, maintenance and chamber routes."""
    # Principal public threshold and direct, wide route to observation.
    t.clear((27, 2, 6), (31, 5, 6))
    base.double_door(t, 28, 2, 6, "north", "iron")
    t.fill((26, 1, 6), (32, 1, 19), "minecraft:quartz_block")
    t.clear((27, 2, 13), (31, 5, 16))
    base.double_door(t, 28, 2, 16, "south", "iron")

    # Staff badge route leaves the public bar for west preparation.
    t.clear((10, 2, 14), (13, 5, 16))
    base.double_door(t, 12, 2, 15, "west", "iron")
    t.fill((7, 1, 15), (12, 1, 20), "minecraft:smooth_stone")

    # Controlled chamber vestibules open from the gallery/control edge. Their
    # positions preserve a continuous visitor overlook between entries.
    for x, z in ((17, 21), (29, 20), (42, 22)):
        _double_iron_door_z(t, x, z, "south")

    # Chamber maintenance doors open to the rear service spine.
    for x, z in ((17, 39), (29, 39), (42, 39)):
        _double_iron_door_z(t, x, z, "north")

    # East analysis wing has a controlled gallery connection and an independent
    # records/service connection at the rear.
    t.clear((48, 2, 16), (50, 5, 18))
    base.double_door(t, 49, 2, 17, "east", "iron")
    t.clear((48, 2, 36), (50, 5, 38))
    base.double_door(t, 49, 2, 37, "east", "iron")

    # Separate rear thresholds for sample/reagent receipt and controlled waste.
    for x in (14, 40):
        t.clear((x, 2, 48), (x + 3, 6, 48))
        base.double_door(t, x + 1, 2, 48, "south", "iron")

    # Two-wide dogleg staff stair inside the accepted east maintenance core.
    for x in (52, 53):
        base.stair_flight(t, x, 2, 38, 5, "south", "minecraft:smooth_quartz_stairs")
    t.fill((51, 6, 42), (54, 6, 45), "minecraft:smooth_stone")
    for x in (53, 54):
        base.stair_flight(t, x, 7, 44, 5, "north", "minecraft:smooth_quartz_stairs")
    t.fill((51, 11, 39), (55, 11, 42), "minecraft:smooth_stone")
    for x in (52, 53):
        base.stair_flight(t, x, 12, 40, 5, "south", "minecraft:smooth_quartz_stairs")
    t.fill((51, 16, 43), (55, 16, 47), "minecraft:smooth_stone")
    t.clear((50, 17, 43), (51, 19, 45))
    base.double_door(t, 50, 17, 43, "west", "iron")


def _pass9_exterior_architecture(t: base.Template) -> None:
    """Align glazing, service openings and site work with interior function."""
    # Reception and public interpretation receive controlled front glazing.
    t.fill((12, 3, 5), (23, 6, 5), "create:framed_glass")
    t.fill((35, 3, 5), (46, 6, 5), "create:framed_glass")
    for x in (9, 19, 29, 39, 49):
        t.fill((x, 1, 4), (x, 8, 5), "minecraft:light_gray_concrete")

    # West clean receiving gets a covered transfer frame and washable drain.
    t.fill((0, 9, 18), (5, 9, 29), "minecraft:white_concrete")
    for z in (18, 29):
        t.fill((1, 1, z), (1, 8, z), "tfmg:steel_block")
    t.fill((1, 0, 18), (1, 0, 29), "minecraft:oxidized_copper_grate")

    # East analysis glazing corresponds to staff work/records, while the amber
    # polymer suite remains window-controlled rather than fully transparent.
    t.fill((57, 4, 16), (57, 8, 24), "create:framed_glass")
    t.fill((57, 4, 34), (57, 8, 40), "create:framed_glass")
    t.fill((56, 11, 28), (57, 13, 37), "minecraft:yellow_concrete")

    # Rear service face receives intake/exhaust grilles and threshold drains.
    for x1, x2 in ((11, 19), (24, 35), (40, 49)):
        t.fill((x1, 7, 49), (x2, 9, 49), "minecraft:oxidized_copper_grate")
    t.fill((10, 0, 47), (51, 0, 47), "minecraft:oxidized_copper_grate")

    # Chamber facade belts terminate at real frames and roof monitors.
    for x1, x2, z, y in ((13, 23, 20, 12), (25, 36, 19, 15), (38, 48, 21, 13)):
        t.fill((x1, y, z), (x2, y + 1, z), "minecraft:cyan_concrete")


def _pass10_interior_architecture(t: base.Template) -> None:
    """Establish legitimate rooms, controlled boundaries and clear aisles."""
    # Public bar: interpretation west, reception center, staff/admin east.
    t.fill((10, 1, 7), (48, 1, 15), "minecraft:quartz_block")
    base.partition_x(t, 23, 2, 7, 15, "minecraft:white_concrete", doorway_z=11)
    base.partition_x(t, 35, 2, 7, 15, "minecraft:white_concrete", doorway_z=11)
    t.fill((15, 2, 15), (22, 6, 15), "create:framed_glass")
    t.fill((36, 2, 15), (46, 6, 15), "create:framed_glass")

    # Observation/control gallery has one continuous white floor datum.
    t.fill((12, 1, 16), (49, 1, 21), "minecraft:smooth_quartz")
    for x1, x2 in ((13, 27), (31, 40), (44, 48)):
        t.fill((x1, 2, 20), (x2, 3, 20), "minecraft:light_gray_concrete")

    # West wing: receiving/accession, clean hold/prep, wash/decon and waste link.
    t.fill((3, 1, 15), (12, 1, 42), "tfmg:factory_floor")
    base.partition_z(t, 22, 2, 3, 12, "minecraft:white_concrete", doorways=(7,))
    base.partition_z(t, 31, 2, 3, 12, "minecraft:white_concrete", doorways=(7,))
    base.partition_z(t, 38, 2, 3, 12, "minecraft:light_gray_concrete", doorways=(7,))
    for z in (22, 31, 38):
        t.clear((7, 2, z), (8, 4, z))
        base.double_door(t, 7, 2, z, "south", "iron")

    # Reinforce chamber separation after overlapping Gate-A study shells.
    t.fill((24, 2, 23), (24, 13, 38), "minecraft:white_concrete")
    t.fill((37, 2, 23), (37, 14, 38), "minecraft:white_concrete")
    # Controlled internal floors and clear center aisles.
    for x1, x2, z1, z2 in ((13, 23, 22, 39), (25, 36, 21, 40), (38, 48, 23, 39)):
        t.fill((x1, 1, z1), (x2, 1, z2), "minecraft:smooth_stone")

    # East wing: bacterial controls, coupon preparation, polymer observation,
    # principal investigator review and secure-record reservation.
    t.fill((49, 1, 14), (55, 1, 41), "minecraft:quartz_block")
    base.partition_z(t, 23, 2, 49, 55, "minecraft:white_concrete", doorways=(52,))
    base.partition_z(t, 32, 2, 49, 55, "minecraft:yellow_concrete", doorways=(52,))
    base.partition_z(t, 38, 2, 49, 55, "minecraft:light_gray_concrete", doorways=(52,))
    # Upper records/data mezzanine occupies the accepted taller east mass.
    t.fill((49, 10, 24), (55, 10, 41), "minecraft:smooth_stone")
    t.fill((49, 11, 24), (49, 12, 40), "create:framed_glass")

    # Rear service spine: clean plant control, branch manifold and waste hold.
    t.fill((11, 1, 40), (50, 1, 47), "tfmg:factory_floor")
    base.partition_x(t, 22, 2, 40, 47, "minecraft:light_gray_concrete")
    base.partition_x(t, 38, 2, 40, 47, "minecraft:light_gray_concrete")
    for x in (22, 38):
        t.clear((x, 2, 42), (x, 4, 43))
        base.door(t, x, 2, 42, "east", "iron", "left")
        base.door(t, x, 2, 43, "east", "iron", "right")


def _culture_bank(t: base.Template, x1: int, x2: int, z: int, *, healthy: bool) -> None:
    t.fill((x1, 2, z), (x2, 2, z + 1), "farmersdelight:rich_soil")
    for x in range(x1, x2 + 1, 2):
        t.set(x, 3, z, "minecraft:brown_mushroom" if healthy else "minecraft:red_mushroom")
    t.fill((x1, 5, z), (x2, 5, z + 1), "create:fluid_pipe")


def _pass11_operational_systems(t: base.Template) -> None:
    """Install the complete D0 sample-to-report experimental workflow."""
    # Receiving/accession and cold/clean hold in the west wing.
    t.fill((4, 2, 17), (6, 3, 19), "immersiveengineering:crate")
    t.fill((9, 2, 17), (11, 4, 19), "oritech:cooler_block")
    base.desk(t, 4, 2, 20)
    t.fill((4, 2, 24), (6, 3, 25), "minecraft:barrel", facing="up", open="false")
    for x in (4, 9):
        t.set(x, 2, 28, "minecraft:brewing_stand", has_bottle_0="false", has_bottle_1="false", has_bottle_2="false")
    t.set(10, 2, 34, "minecraft:cauldron")
    t.fill((4, 2, 34), (6, 4, 36), "create:fluid_tank")
    t.fill((4, 6, 35), (11, 6, 35), "create:fluid_pipe")

    # Chamber A: EP-7 reference with modest control culture banks.
    for z in (25, 33):
        _culture_bank(t, 14, 17, z, healthy=False)
        _culture_bank(t, 20, 22, z, healthy=False)
    t.fill((13, 11, 25), (23, 11, 36), "create:fluid_pipe")
    t.set(15, 12, 30, "create:encased_fan", facing="south")
    t.fill((14, 2, 23), (16, 3, 23), "create:depot")

    # Chamber B: dominant EP-7/PT-9 symbiosis trial, visibly productive but
    # maintaining a three-block central service aisle.
    for z in (24, 31, 37):
        _culture_bank(t, 26, 29, z, healthy=True)
        _culture_bank(t, 33, 35, z, healthy=True)
    t.fill((25, 14, 24), (36, 14, 38), "create:fluid_pipe")
    for x in (27, 34):
        t.fill((x, 2, 22), (x + 1, 5, 23), "create:fluid_tank")
    t.set(30, 15, 30, "create:encased_fan", facing="south")
    t.set(31, 15, 30, "create:encased_fan", facing="south")

    # Chamber C: stress/recovery trial with isolated environmental banks.
    for z in (26, 34):
        _culture_bank(t, 39, 41, z, healthy=True)
        _culture_bank(t, 45, 47, z, healthy=False)
    t.fill((38, 12, 25), (48, 12, 37), "create:fluid_pipe")
    t.fill((39, 2, 24), (41, 5, 24), "create:fluid_tank")
    t.set(46, 13, 30, "create:encased_fan", facing="south")

    # Gallery control stations align one-for-one with chamber observation.
    for x in (15, 32, 41):
        t.fill((x, 2, 18), (x + 3, 2, 18), "create:depot")
        t.fill((x + 1, 3, 19), (x + 2, 4, 19), "ae2:terminal")

    # East bacterial controls and polymer coupon preparation/observation.
    for z in (17, 20):
        t.set(51, 2, z, "minecraft:brewing_stand", has_bottle_0="false", has_bottle_1="false", has_bottle_2="false")
        t.fill((54, 2, z), (55, 3, z), "create:framed_glass")
    t.fill((50, 2, 25), (55, 2, 26), "tfmg:plastic_block")
    t.fill((50, 2, 29), (55, 4, 30), "create:framed_glass")
    t.fill((50, 2, 33), (51, 4, 36), "tfmg:plastic_block")
    t.fill((54, 2, 33), (55, 4, 36), "minecraft:yellow_concrete")
    base.desk(t, 50, 2, 40)
    t.fill((54, 2, 39), (55, 6, 41), "minecraft:bookshelf")

    # Shared environmental manifold connects roof plant to all three chambers.
    t.fill((12, 7, 43), (49, 7, 43), "create:fluid_pipe")
    for x, top in ((18, 18), (30, 22), (43, 20)):
        t.fill((x, 7, 40), (x, top, 43), "create:fluid_pipe")
        t.set(x, 8, 44, "create:mechanical_pump", facing="south")
    for x in (16, 28, 41):
        t.fill((x, 2, 45), (x + 3, 5, 46), "immersiveengineering:sheetmetal_steel")
    t.fill((40, 2, 44), (47, 4, 46), "immersiveengineering:crate")

    # Lighting tracks preserve the gallery and chamber center aisles.
    for x in (15, 21, 28, 34, 41, 47):
        t.set(x, 7, 18, "minecraft:sea_lantern")
    for x, z, y in ((18, 30, 10), (30, 30, 13), (43, 30, 11)):
        t.fill((x, y, z - 3), (x, y, z + 3), "minecraft:sea_lantern")


def _pass12_institutional_identity(t: base.Template) -> None:
    """Apply VCF/PT-9 identity as purposeful wayfinding and test language."""
    base.wall_sign(t, 25, 7, 5, "north", "VERDANT CONTINUUM", "FOODS")
    base.wall_sign(t, 33, 7, 5, "north", "PT-9 SYMBIOSIS", "PILOT LABORATORY")
    base.wall_sign(t, 27, 5, 7, "south", "VISITOR RECEPTION", "AUTHORIZED TOURS")
    base.wall_sign(t, 13, 5, 15, "south", "CONTROLLED ENTRY", "STAFF BADGE")
    base.wall_sign(t, 14, 6, 20, "north", "CHAMBER A", "EP-7 REFERENCE")
    base.wall_sign(t, 27, 6, 19, "north", "CHAMBER B", "EP-7 + PT-9")
    base.wall_sign(t, 40, 6, 21, "north", "CHAMBER C", "STRESS RECOVERY")
    base.wall_sign(t, 14, 5, 17, "south", "COMPARATIVE", "OBSERVATION")
    base.wall_sign(t, 4, 6, 21, "north", "SAMPLE ACCESSION", "LOT / CHAIN")
    base.wall_sign(t, 4, 6, 30, "north", "MEDIA & REAGENT", "CLEAN PREP")
    base.wall_sign(t, 4, 6, 37, "north", "WASH / DECON", "SERVICE RETURN")
    base.wall_sign(t, 50, 6, 22, "north", "BACTERIAL CONTROL", "REFERENCE BENCH")
    base.wall_sign(t, 50, 6, 31, "north", "POLYMER COUPONS", "CLEAN / EXPOSED")
    base.wall_sign(t, 50, 6, 37, "north", "MATERIAL HOLD", "PT-9 OBSERVATION")
    base.wall_sign(t, 50, 6, 40, "south", "SECURE RECORDS", "PRINCIPAL REVIEW")
    base.wall_sign(t, 15, 6, 47, "south", "CONTROLLED RECEIVING", "SAMPLES / REAGENTS")
    base.wall_sign(t, 41, 6, 47, "south", "DECON WASTE", "AUTHORIZED REMOVAL")
    base.wall_sign(t, 24, 6, 42, "south", "ENVIRONMENTAL", "BRANCH MANIFOLD")
    base.wall_sign(t, 50, 18, 42, "west", "ROOF PLANT", "MAINTENANCE ACCESS")


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
    if tuple(t.size) != (59, 26, 51):
        raise AssertionError(f"OWS-006 Gate-B r1 dimensions changed unexpectedly: {t.size}")

    # Representative points freeze all ten accepted Gate-A macro aspects.
    frozen = {
        (20, 8, 1): "minecraft:white_concrete",
        (10, 0, 2): "minecraft:smooth_stone",
        (20, 9, 14): "minecraft:light_gray_concrete",
        (15, 15, 26): "minecraft:light_gray_concrete",
        (28, 18, 25): "minecraft:light_gray_concrete",
        (40, 16, 27): "minecraft:light_gray_concrete",
        (2, 5, 30): "minecraft:light_gray_concrete",
        (56, 11, 30): "minecraft:yellow_concrete",
        (25, 10, 48): "minecraft:white_concrete",
        (30, 15, 44): "tfmg:steel_block",
        (50, 10, 45): "minecraft:light_gray_concrete",
    }
    for pos, expected in frozen.items():
        actual = _name_at(t, pos)
        if actual != expected:
            raise AssertionError(f"Gate-A frozen aspect changed at {pos}: {actual} != {expected}")

    # Principal and controlled transfer doors must have complete halves.
    for x, z in ((28, 6), (28, 16), (12, 15), (17, 21), (29, 20), (42, 22), (49, 17)):
        for dx in (0, 1):
            for y in (2, 3):
                if _name_at(t, (x + dx, y, z)) != "minecraft:iron_door":
                    raise AssertionError(f"Controlled door missing at {(x + dx, y, z)}")

    # Main public/gallery and chamber aisles remain two blocks high and clear.
    protected = (
        ((29, 2, 7), (30, 3, 12)),
        ((29, 2, 17), (30, 3, 19)),
        ((18, 2, 24), (19, 3, 38)),
        ((30, 2, 23), (32, 3, 38)),
        ((42, 2, 24), (44, 3, 38)),
        ((7, 2, 16), (8, 3, 41)),
        ((12, 2, 42), (47, 3, 42)),
    )
    for low, high in protected:
        for x in range(low[0], high[0] + 1):
            for y in range(low[1], high[1] + 1):
                for z in range(low[2], high[2] + 1):
                    name = _name_at(t, (x, y, z))
                    if name not in {None, "minecraft:air", "minecraft:iron_door"}:
                        raise AssertionError(f"Protected circulation obstruction at {(x, y, z)}: {name}")

    names = [t.palette[entry[0]]["Name"] for entry in t.blocks.values()]
    forbidden = {"minecraft:chest", "minecraft:trapped_chest", "minecraft:spawner"}
    present_forbidden = forbidden.intersection(names)
    if present_forbidden:
        raise AssertionError(f"Gate-B contains deferred proof/encounter blocks: {sorted(present_forbidden)}")
    if sum(name.endswith("_wall_sign") for name in names) < 19:
        raise AssertionError("VCF/PT-9 intact-state wayfinding is unexpectedly sparse")
    if names.count("farmersdelight:rich_soil") < 40:
        raise AssertionError("Comparative culture program is unexpectedly sparse")
    if names.count("create:fluid_pipe") < 100:
        raise AssertionError("Environmental-service connectivity is unexpectedly sparse")


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
    t = build_gate_b_intact()
    _assert_intact_contracts(t)

    t.save(TEMP_NAME)
    try:
        model_bytes = TEMP_NBT.read_bytes()
        size, blocks = unpack_structure(TEMP_NBT)
        if len(blocks) < 16000:
            raise AssertionError(f"Gate-B r1 intact model is unexpectedly sparse: {len(blocks)}")
        revision = os.environ.get("GITHUB_SHA", "local")[:8]
        manifest = render_review_set(
            target="OWS-006",
            gate="gate_b_intact",
            revision=f"intact-r1@{revision}",
            damage_state="D0 intact / operational",
            source_commit=os.environ.get("GITHUB_SHA", "working-tree"),
            source_path="review-only:render_ows006_gate_b_intact.build_gate_b_intact()",
            size=size,
            blocks=blocks,
            output_dir=OUTPUT_DIR,
            camera_set="ows006_fixed_v1",
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
            raise AssertionError("OWS-006 shipping NBT changed during review-only rendering")
        (OUTPUT_DIR / "review_manifest.json").write_text(
            json.dumps(manifest, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    finally:
        TEMP_NBT.unlink(missing_ok=True)

    print(
        f"Rendered OWS-006 Gate B r1 intact review at {manifest['dimensions']} using "
        f"{manifest['fixed_camera_set']}; independent visual approval remains pending."
    )


if __name__ == "__main__":
    main()
