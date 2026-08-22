#!/usr/bin/env python3
"""Side-effect-free authoritative OWS-006 production builder.

The accepted Gate-C r2 D3 model is reconstructed entirely from production-safe
target-local functions. This module adds only the localized Pass-19 overlay.
It imports no review/render module, performs no I/O, and mutates no registry.
"""
from __future__ import annotations

import generate_wasteland_sites as base


ACCEPTED_GATE_C_D3_SHA256 = "8c9d3e31c0d3cdfcee0a45bdc7bf5156184a05521babdd8665f47e6d6e5f6e09"
PROOF_LOOT_TABLE = "infinite_domain:chests/old_world/ows_006_vcf_pt9_symbiosis_pilot_laboratory"
PROOF_POS = (54, 2, 40)
AIR = {None, "minecraft:air", "minecraft:cave_air", "minecraft:void_air", "minecraft:structure_void"}


def _name(t: base.Template, pos: tuple[int, int, int]) -> str | None:
    entry = t.blocks.get(pos)
    return None if entry is None else t.palette[entry[0]]["Name"]


def _count_block(t: base.Template, name: str) -> int:
    return sum(1 for pos in t.blocks if _name(t, pos) == name)


def build_d0() -> base.Template:
    """Return the accepted Gate-B intact model."""
    t = build_gate_b_intact()
    _assert_intact_contracts(t)
    return t


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


def build_d1() -> base.Template:
    """Localized early intervention where PT-9 attacks polymer interfaces."""
    t = build_d0()

    # The pre-existing yellow polymer suite expands into a controlled integrity
    # hold. Floor-only zoning keeps the east-wing route and room anatomy intact.
    t.fill((49, 1, 24), (55, 1, 37), "minecraft:yellow_concrete")
    t.fill((50, 1, 28), (53, 1, 31), "minecraft:smooth_stone")
    t.fill((25, 1, 24), (29, 1, 38), "minecraft:yellow_concrete")
    t.fill((33, 1, 24), (36, 1, 38), "minecraft:yellow_concrete")

    # A traversable polymer-integrity vestibule marks the observed-material hold.
    t.fill((49, 2, 32), (51, 5, 32), "minecraft:white_concrete")
    t.fill((53, 2, 32), (55, 5, 32), "minecraft:white_concrete")
    base.door(t, 52, 2, 32, "south", "iron")
    t.fill((49, 5, 32), (55, 5, 32), "minecraft:yellow_concrete")

    # Failed coupons, replacement filter media and the temporary Chamber-B
    # bypass make the response operational rather than decorative.
    t.fill((50, 2, 34), (53, 3, 36), "tfmg:plastic_block")
    t.fill((49, 2, 28), (51, 3, 30), "immersiveengineering:crate")
    t.fill((33, 6, 33), (36, 6, 37), "create:fluid_pipe")
    t.set(34, 6, 35, "create:mechanical_pump", facing="north")
    t.fill((32, 6, 39), (35, 8, 40), "immersiveengineering:sheetmetal_steel")

    base.wall_sign(t, 50, 6, 32, "north", "POLYMER HOLD", "SEAL INTEGRITY")
    base.wall_sign(t, 33, 7, 39, "north", "CHAMBER B BYPASS", "FILTER WATCH")
    base.wall_sign(t, 50, 6, 28, "south", "FAILED COUPONS", "MATERIAL REVIEW")

    # D1 remains an intact, localized intervention with every accepted route.
    _assert_intact_contracts(t)
    return t


def _build_d3_r1() -> base.Template:
    """Reconstruct the rejected r1 D3 exactly as the narrow-r2 baseline."""
    t = build_d1()

    # The east material-hold envelope fails first around degraded seals. The
    # stair and secure-record approach farther south remain traversable.
    t.clear((52, 10, 33), (55, 14, 36))
    t.clear((55, 5, 33), (57, 10, 36))
    t.clear((50, 2, 34), (53, 3, 36))
    t.fill((50, 1, 33), (55, 1, 37), "minecraft:mossy_stone_bricks")
    t.fill((51, 2, 34), (53, 3, 36), "minecraft:gravel")
    t.set(50, 3, 35, "minecraft:cobweb")
    t.set(55, 2, 36, "minecraft:brown_mushroom")

    # Chamber B's bypass and environmental monitor fail next. Damage stays off
    # the accepted three-wide center aisle and leaves A/C as readable controls.
    t.clear((33, 14, 32), (36, 18, 38))
    t.clear((34, 8, 34), (36, 13, 38))
    t.fill((33, 1, 33), (36, 1, 38), "minecraft:cracked_stone_bricks")
    t.fill((34, 2, 35), (36, 3, 38), "minecraft:gravel")
    t.set(33, 3, 36, "minecraft:cobweb")
    t.set(35, 2, 38, "minecraft:brown_mushroom")

    # The matching rear manifold branch and local roof service deck weather in
    # the same causal line. The accepted manifold datum at y15 is not touched.
    t.clear((27, 17, 42), (34, 24, 46))
    t.clear((32, 8, 44), (35, 13, 46))
    t.fill((31, 1, 44), (36, 1, 47), "minecraft:mossy_stone_bricks")
    t.fill((33, 2, 44), (36, 3, 46), "minecraft:gravel")
    t.set(32, 3, 45, "minecraft:cobweb")

    # A restrained water path links the failed east envelope to the service
    # yard without inventing an explosion or generalized destruction.
    t.fill((51, 0, 42), (55, 0, 47), "minecraft:coarse_dirt")
    t.fill((48, 1, 44), (52, 1, 47), "minecraft:mossy_stone_bricks")
    t.set(50, 2, 46, "minecraft:brown_mushroom")

    # Prove accepted D0 architecture and circulation before adding deferred
    # gameplay blocks forbidden by Gate B.
    _assert_intact_contracts(t)

    # Secure principal-review records carry exactly one canonical proof chest.
    t.clear((53, 2, 39), (55, 4, 41))
    t.set(PROOF_POS[0], PROOF_POS[1] + 1, PROOF_POS[2], "minecraft:air")
    t.chest(*PROOF_POS, PROOF_LOOT_TABLE, facing="west")

    # Three restrained vanilla encounters track the same failure path and stay
    # away from public/chamber center aisles and the proof container.
    t.clear((53, 2, 33), (55, 3, 35))
    t.spawner(54, 2, 34, "minecraft:spider", count=1, nearby=3)
    t.clear((33, 2, 35), (35, 3, 37))
    t.spawner(34, 2, 36, "minecraft:zombie", count=1, nearby=4)
    t.clear((44, 2, 44), (46, 3, 46))
    t.spawner(45, 2, 45, "minecraft:skeleton", count=1, nearby=3)

    _assert_d3_contracts(t)
    return t


def build_d3() -> base.Template:
    """Narrow r2: remove only the unsupported rear cap and land its debris."""
    t = _build_d3_r1()

    # Independent r1 review identified this 4x3 cap as floating after its tower
    # was removed. Remove exactly that detached remnant and land a restrained
    # five-block debris scatter on the surviving service deck directly below.
    t.clear((29, 25, 43), (32, 25, 45))
    for pos in ((29, 17, 43), (30, 17, 44), (31, 17, 45), (32, 17, 44), (31, 18, 44)):
        t.set(*pos, "minecraft:light_gray_concrete")

    _assert_d3_contracts(t)
    return t


def _assert_proof(t: base.Template) -> None:
    row = t.blocks.get(PROOF_POS)
    if row is None:
        raise AssertionError("OWS-006 D3 proof chest is missing")
    state_id, nbt = row
    if t.palette[state_id]["Name"] != "minecraft:chest":
        raise AssertionError(f"OWS-006 proof position contains {t.palette[state_id]['Name']}")
    if not nbt or nbt.get("LootTable") != PROOF_LOOT_TABLE:
        raise AssertionError(f"OWS-006 proof chest has wrong loot table: {None if not nbt else nbt.get('LootTable')}")
    if _name(t, (PROOF_POS[0], PROOF_POS[1] + 1, PROOF_POS[2])) not in AIR:
        raise AssertionError("OWS-006 proof chest has no clear block above")
    matching = sum(1 for _, block_nbt in t.blocks.values() if block_nbt and block_nbt.get("LootTable") == PROOF_LOOT_TABLE)
    if matching != 1:
        raise AssertionError(f"OWS-006 must contain exactly one canonical proof container; found {matching}")


def _assert_d3_contracts(t: base.Template) -> None:
    _assert_proof(t)
    if _count_block(t, "minecraft:spawner") != 3:
        raise AssertionError("OWS-006 D3 requires exactly three deliberate encounter spawners")
    for x, z in ((28, 6), (28, 16), (12, 15), (17, 21), (29, 20), (42, 22), (49, 17)):
        for dx in (0, 1):
            if _name(t, (x + dx, 2, z)) != "minecraft:iron_door":
                raise AssertionError(f"OWS-006 D3 route lost controlled door at {(x + dx, 2, z)}")
    if _name(t, (53, 2, 40)) not in AIR:
        raise AssertionError("OWS-006 D3 proof approach is obstructed")
    sign_count = sum((_name(t, pos) or "").endswith("_wall_sign") for pos in t.blocks)
    if sign_count < 19:
        raise AssertionError(f"OWS-006 D3 preserves too little institutional identity: {sign_count} signs")
    for pos in ((25, 7, 5), (33, 7, 5)):
        if not (_name(t, pos) or "").endswith("_wall_sign"):
            raise AssertionError(f"OWS-006 D3 lost primary VCF identity at {pos}")
    if _count_block(t, "create:fluid_pipe") < 90:
        raise AssertionError("OWS-006 D3 removed too much environmental-service anatomy")
    if _count_block(t, "farmersdelight:rich_soil") < 40:
        raise AssertionError("OWS-006 D3 removed too much comparative culture evidence")
    for pos in ((54, 2, 34), (34, 2, 36), (45, 2, 45)):
        if sum(abs(a - b) for a, b in zip(pos, PROOF_POS)) < 6:
            raise AssertionError(f"OWS-006 encounter is too close to proof at {pos}")

# Every Pass-19 mutation remains inside an accepted r2 D3 weather/damage zone.
PASS19_MICRODETAIL = {
    (52, 4, 34): "minecraft:cobweb",
    (53, 4, 36): "minecraft:cobweb",
    (36, 4, 37): "minecraft:cobweb",
    (35, 2, 34): "minecraft:brown_mushroom",
    (29, 18, 43): "minecraft:cobweb",
    (32, 17, 45): "minecraft:cobweb",
    (49, 2, 45): "minecraft:brown_mushroom",
    (51, 2, 46): "minecraft:brown_mushroom",
}


def build_accepted_d3() -> base.Template:
    """Return the independently accepted Gate-C r2 D3 model."""
    return build_d3()


def _apply_pass19_microdetail(t: base.Template) -> None:
    for pos, block in PASS19_MICRODETAIL.items():
        if _name(t, pos) not in AIR:
            raise AssertionError(f"OWS-006 Pass-19 position was not empty at {pos}: {_name(t, pos)}")
        t.set(*pos, block)


def _assert_final_contracts(t: base.Template) -> None:
    _assert_d3_contracts(t)
    if tuple(t.size) != (59, 26, 51):
        raise AssertionError(f"OWS-006 final dimensions changed: {t.size}")
    for pos, expected in PASS19_MICRODETAIL.items():
        actual = _name(t, pos)
        if actual != expected:
            raise AssertionError(f"OWS-006 Pass-19 detail drift at {pos}: {actual} != {expected}")
    if _name(t, (53, 2, 40)) not in AIR:
        raise AssertionError("OWS-006 Pass-19 detail obstructed the secure-records proof approach")


def build_006() -> base.Template:
    """Build accepted r2 D3 plus localized Pass-19 detail, without I/O."""
    t = build_accepted_d3()
    _apply_pass19_microdetail(t)
    _assert_final_contracts(t)
    return t


if __name__ == "__main__":
    raise SystemExit("Import build_006 from the authoritative generator; this module performs no writes.")


