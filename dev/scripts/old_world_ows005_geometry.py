#!/usr/bin/env python3
"""Pure accepted OWS-005 Gate-A/B/C geometry and mechanical contracts.

This production component performs no rendering, file I/O, registry mutation,
or gate decision. Review tools and the authoritative final builder both consume
these exact functions so accepted geometry has one target-local source.
"""
from __future__ import annotations

import generate_wasteland_sites as base


ACCEPTED_GATE_B_SHA256 = "448f37b09e42076283d8e83f0f70d7fa5433d59af82c773b48a820ce27535f5a"
PROOF_LOOT_TABLE = "infinite_domain:chests/old_world/ows_005_vcf_harvest_packaging_annex"
PROOF_POS = (33, 2, 40)
AIR = {None, "minecraft:air", "minecraft:cave_air", "minecraft:void_air", "minecraft:structure_void"}


def _site_and_thresholds(t: base.Template) -> None:
    t.fill((1, 0, 1), (57, 0, 49), "minecraft:grass_block")

    # West/raw and east/finished aprons make the one-direction material flow
    # legible before line machinery exists.
    t.fill((1, 0, 13), (15, 0, 46), "tfmg:asphalt")
    t.fill((48, 0, 29), (57, 0, 48), "tfmg:asphalt")
    for z in (16, 25, 34, 43):
        t.fill((1, 0, z), (14, 0, z), "minecraft:light_gray_concrete")
    for z in (32, 40, 47):
        t.fill((49, 0, z), (57, 0, z), "minecraft:white_concrete")

    # Covered raw receiving is low, porous and unmistakably separate from the
    # enclosed clean-side dispatch dock.
    t.fill((3, 8, 14), (15, 8, 43), "immersiveengineering:sheetmetal_steel")
    for x in (3, 9, 15):
        for z in (14, 24, 34, 43):
            t.fill((x, 1, z), (x, 7, z), "tfmg:steel_block")
    t.fill((2, 8, 13), (16, 9, 14), "minecraft:lime_concrete")

    # Distinct clean-side dispatch canopy and dock frame.
    t.fill((48, 9, 30), (57, 9, 47), "minecraft:white_concrete")
    for z in (30, 38, 47):
        t.fill((56, 1, z), (56, 8, z), "tfmg:steel_block")
    t.fill((54, 2, 31), (54, 7, 46), "minecraft:light_gray_concrete")
    for z1 in (32, 40):
        t.clear((54, 2, z1), (54, 6, z1 + 5))


def _raw_and_wet_halls(t: base.Template) -> None:
    # Receiving/intake block retains a controlled amount of brick as donor
    # industrial memory, but new structure and glazing establish VCF conversion.
    base.shell(
        t,
        (12, 1, 12),
        (24, 10, 44),
        "minecraft:bricks",
        "tfmg:factory_floor",
        "minecraft:light_gray_concrete",
    )
    t.clear((12, 2, 17), (12, 7, 23))
    t.clear((12, 2, 32), (12, 7, 38))
    for z in (13, 21, 29, 37, 44):
        t.fill((11, 1, z), (11, 10, z), "tfmg:steel_block")

    # Wet sanitation/inspection hall steps taller and changes material at the
    # raw-to-clean boundary.
    base.shell(
        t,
        (23, 1, 10),
        (37, 13, 44),
        "minecraft:white_concrete",
        "tfmg:factory_floor",
        "minecraft:light_gray_concrete",
    )
    t.fill((23, 3, 9), (37, 7, 9), "create:framed_glass")
    for z in (13, 21, 29, 37, 44):
        t.fill((22, 1, z), (22, 13, z), "minecraft:light_gray_concrete")

    # Cyan hygiene/service datum has real thickness and a roof connection; it
    # reserves the sanitation spine rather than acting as floor paint.
    t.fill((21, 1, 10), (23, 13, 44), "minecraft:light_blue_concrete")
    t.fill((22, 13, 15), (25, 17, 20), "immersiveengineering:sheetmetal_steel")
    t.fill((22, 13, 33), (25, 17, 38), "immersiveengineering:sheetmetal_steel")


def _clean_pack_and_cold_chain(t: base.Template) -> None:
    # Tall clean packing high bay; clerestories correspond to the production
    # volume and repeated piers make the span structurally legible.
    base.shell(
        t,
        (35, 1, 12),
        (49, 18, 46),
        "minecraft:white_concrete",
        "tfmg:factory_floor",
        "minecraft:light_gray_concrete",
    )
    t.fill((35, 11, 11), (49, 15, 11), "create:framed_glass")
    for x in (36, 42, 48):
        t.fill((x, 1, 11), (x, 18, 11), "tfmg:steel_block")
        t.fill((x, 1, 47), (x, 18, 47), "tfmg:steel_block")

    # Two raised roof monitors create a packaging-hall silhouette without
    # populating operational detail prematurely.
    for x1, x2 in ((37, 41), (44, 48)):
        base.shell(
            t,
            (x1, 18, 16),
            (x2, 21, 41),
            "create:framed_glass",
            "minecraft:light_gray_concrete",
            "minecraft:white_concrete",
        )

    # Window-poor insulated cold block projects from the clean hall and meets
    # dispatch directly. Its mechanical crown is attached to the cold mass.
    base.shell(
        t,
        (46, 1, 5),
        (57, 14, 30),
        "minecraft:light_gray_concrete",
        "tfmg:factory_floor",
        "minecraft:white_concrete",
    )
    t.fill((45, 2, 8), (45, 11, 27), "minecraft:cyan_concrete")
    t.fill((49, 14, 8), (56, 19, 27), "immersiveengineering:sheetmetal_steel")
    t.fill((51, 19, 10), (54, 22, 13), "tfmg:steel_block")
    t.fill((51, 19, 22), (54, 22, 25), "tfmg:steel_block")


def _public_qa_front(t: base.Template) -> None:
    # Clean QA/visitor pavilion faces the approach and remains spatially distinct
    # from both truck aprons.
    base.shell(
        t,
        (20, 1, 2),
        (42, 8, 12),
        "minecraft:white_concrete",
        "minecraft:smooth_stone",
        "minecraft:light_gray_concrete",
    )
    t.fill((23, 2, 1), (39, 6, 1), "create:framed_glass")
    t.clear((29, 2, 1), (33, 5, 2))
    t.fill((23, 7, 1), (39, 8, 1), "minecraft:lime_concrete")
    t.fill((25, 8, 0), (37, 8, 4), "minecraft:white_concrete")
    for x in (25, 37):
        t.fill((x, 1, 1), (x, 7, 1), "minecraft:light_gray_concrete")


def build_gate_a_massing() -> base.Template:
    t = base.Template((59, 24, 51))
    _site_and_thresholds(t)
    _raw_and_wet_halls(t)
    _clean_pack_and_cold_chain(t)
    _public_qa_front(t)
    return t


def _pass7_structural_system(t: base.Template) -> None:
    """Resolve the overlapping study shells as one repeated industrial frame."""
    # Raw receiving frame and supported low roof.
    for z in (14, 22, 30, 38, 44):
        t.fill((12, 8, z), (24, 9, z), "tfmg:steel_block")
        for x in (12, 24):
            t.fill((x, 1, z), (x, 8, z), "tfmg:steel_block")

    # Wet hall beams align the sanitation spine with the main building frame.
    for z in (10, 18, 26, 34, 42, 44):
        t.fill((23, 11, z), (37, 12, z), "minecraft:light_gray_concrete")
        for x in (23, 37):
            t.fill((x, 1, z), (x, 11, z), "minecraft:light_gray_concrete")

    # Packing high-bay frames support the accepted height and roof monitors.
    for z in (12, 19, 26, 33, 40, 46):
        t.fill((35, 15, z), (49, 17, z), "tfmg:steel_block")
        for x in (35, 49):
            t.fill((x, 1, z), (x, 15, z), "tfmg:steel_block")

    # Cold-block insulation frame and plant deck remain on the accepted mass.
    for z in (5, 13, 21, 29):
        t.fill((46, 12, z), (57, 13, z), "minecraft:light_gray_concrete")
    t.fill((48, 14, 7), (57, 14, 28), "tfmg:steel_block")

    # Roof gutters/downpipes resolve broad planes without changing hierarchy.
    t.fill((12, 10, 11), (24, 10, 11), "minecraft:weathered_cut_copper")
    t.fill((23, 13, 45), (37, 13, 45), "minecraft:weathered_cut_copper")
    t.fill((34, 18, 12), (34, 18, 46), "minecraft:weathered_cut_copper")
    for x, z, top in ((12, 12, 10), (24, 44, 10), (23, 44, 13), (35, 46, 18), (57, 29, 14)):
        t.fill((x, 1, z), (x, top, z), "create:fluid_pipe")


def _framed_loading_opening_x(t: base.Template, x: int, z1: int, z2: int, height: int) -> None:
    t.clear((x, 2, z1), (x, height - 1, z2))
    t.fill((x, 1, z1 - 1), (x, height, z1 - 1), "tfmg:steel_block")
    t.fill((x, 1, z2 + 1), (x, height, z2 + 1), "tfmg:steel_block")
    t.fill((x, height, z1 - 1), (x, height, z2 + 1), "tfmg:steel_block")


def _pass8_circulation_and_access(t: base.Template) -> None:
    """Create distinct visitor, staff, product, reject and maintenance routes."""
    # Public approach and entrance at the accepted pavilion.
    t.fill((27, 0, 0), (35, 0, 3), "minecraft:smooth_stone")
    t.clear((29, 2, 2), (33, 5, 3))
    base.double_door(t, 30, 2, 2, "north", "iron")
    t.fill((28, 1, 3), (34, 1, 11), "minecraft:quartz_block")

    # Glazed process overlook with a controlled staff transition.
    t.fill((22, 2, 12), (41, 6, 12), "create:framed_glass")
    t.clear((30, 2, 12), (33, 4, 12))
    base.double_door(t, 31, 2, 12, "south", "iron")
    base.partition_x(t, 27, 2, 3, 11, "minecraft:white_concrete", doorway_z=7)
    t.clear((20, 2, 6), (20, 4, 8))
    base.double_door(t, 20, 2, 6, "west", "iron")

    # Two framed raw receiving bays beneath the west canopy.
    _framed_loading_opening_x(t, 12, 17, 22, 8)
    _framed_loading_opening_x(t, 12, 32, 37, 8)

    # Controlled raw-to-wet transfers through the sanitation spine.
    for z1 in (19, 32):
        t.clear((21, 2, z1), (24, 5, z1 + 2))
        base.door(t, 23, 2, z1, "east", "iron", "left")
        base.door(t, 23, 2, z1 + 1, "east", "iron", "right")

    # Wet-to-clean packing transfers.
    for z1 in (19, 33):
        t.clear((35, 2, z1), (35, 5, z1 + 2))
        base.door(t, 35, 2, z1, "east", "iron", "left")
        base.door(t, 35, 2, z1 + 1, "east", "iron", "right")

    # Packing-to-cold transfer; cold rooms are divided and independently gated.
    for z1 in (12, 23):
        t.clear((46, 2, z1), (46, 5, z1 + 2))
        base.door(t, 46, 2, z1, "east", "iron", "left")
        base.door(t, 46, 2, z1 + 1, "east", "iron", "right")
    base.partition_z(t, 18, 2, 47, 56, "minecraft:white_concrete", doorways=(51, 54))

    # Refrigerated dispatch opens from cold hold into the accepted east canopy.
    t.clear((49, 2, 30), (55, 7, 30))
    for x in (49, 52):
        base.double_door(t, x, 2, 30, "south", "iron")
    t.fill((49, 1, 29), (55, 1, 34), "minecraft:polished_blackstone")

    # QA reject/waste route exits separately at the rear of wet processing.
    t.clear((27, 2, 44), (30, 5, 44))
    base.double_door(t, 28, 2, 44, "south", "iron")
    t.fill((26, 0, 45), (31, 0, 49), "tfmg:asphalt")

    # Protected maintenance ladder and roof landing reach cold/refrigeration plant.
    t.fill((46, 1, 7), (49, 15, 10), "minecraft:smooth_stone")
    t.clear((47, 2, 8), (48, 15, 9))
    t.fill((47, 14, 7), (50, 14, 12), "minecraft:oxidized_copper_grate")
    t.clear((48, 15, 10), (50, 17, 12))
    for y in range(2, 15):
        t.set(47, y, 8, "minecraft:ladder", facing="west", waterlogged="false")


def _pass9_exterior_architecture(t: base.Template) -> None:
    """Differentiate clean public, dirty receiving and cold dispatch elevations."""
    # Receiving apron has raw-lot lanes and a washable trench.
    for z in (18, 21, 33, 36):
        t.fill((2, 0, z), (11, 0, z), "minecraft:yellow_concrete")
    t.fill((10, 0, 14), (10, 0, 43), "minecraft:oxidized_copper_grate")

    # Refrigerated dispatch gets insulated dock seals and a separate drain.
    for x in (48, 51, 54, 57):
        t.fill((x, 1, 30), (x, 8, 30), "minecraft:cyan_concrete")
    t.fill((48, 0, 31), (57, 0, 31), "minecraft:oxidized_copper_grate")

    # Pavilion glazing is tied to reception, QA and the process overlook.
    t.fill((22, 3, 2), (27, 6, 2), "create:framed_glass")
    t.fill((35, 3, 2), (40, 6, 2), "create:framed_glass")
    t.fill((20, 3, 4), (20, 6, 10), "create:framed_glass")

    # Restrained VCF material panels follow actual sanitary/clean zones.
    t.fill((24, 8, 9), (34, 10, 9), "minecraft:lime_concrete")
    t.fill((36, 9, 11), (48, 10, 11), "minecraft:white_concrete")
    t.fill((46, 8, 4), (57, 10, 4), "minecraft:light_gray_concrete")


def _pass10_interior_architecture(t: base.Template) -> None:
    """Establish rooms and sanitary boundaries before adding equipment."""
    # Raw lot lanes and intake-control room.
    t.fill((13, 1, 13), (22, 1, 43), "tfmg:factory_floor")
    base.partition_z(t, 27, 2, 13, 22, "minecraft:bricks", doorways=(17, 20))
    base.partition_z(t, 15, 2, 13, 22, "minecraft:light_gray_concrete", doorways=(18,))

    # Wet processing: two lanes separated by a drain/service aisle, plus QA hold.
    t.fill((24, 1, 11), (34, 1, 43), "minecraft:light_blue_concrete")
    t.fill((24, 1, 26), (34, 1, 28), "minecraft:oxidized_copper_grate")
    base.partition_z(t, 38, 2, 24, 34, "minecraft:white_concrete", doorways=(27, 32))

    # Clean packing floor and dry packaging store.
    t.fill((36, 1, 13), (48, 1, 45), "minecraft:smooth_stone")
    base.partition_z(t, 39, 2, 36, 48, "minecraft:white_concrete", doorways=(40, 45))

    # Two insulated cold compartments with an uncluttered transfer aisle.
    t.fill((47, 1, 6), (56, 1, 29), "minecraft:polished_blackstone")
    t.fill((50, 1, 6), (52, 1, 29), "minecraft:smooth_stone")

    # Pavilion: staff hygiene west, visitor/reception center, QA records east.
    t.fill((21, 1, 3), (41, 1, 11), "minecraft:quartz_block")
    base.partition_x(t, 35, 2, 3, 11, "minecraft:white_concrete", doorway_z=7)
    t.fill((28, 2, 10), (34, 5, 10), "create:framed_glass")


def _pass11_operational_systems(t: base.Template) -> None:
    """Install connected material, sanitation, packing and refrigeration systems."""
    # Receiving lot check and raw pallet staging.
    for z in (18, 21, 33, 36):
        t.fill((14, 2, z), (17, 3, z + 1), "jaffabricate:pallet_full")
    for z in (18, 33):
        t.fill((19, 2, z), (21, 2, z + 2), "create:depot")
    t.fill((14, 2, 13), (16, 3, 14), "immersiveengineering:crate")

    # Two PT-9 wash/sanitation lanes with header, pumps, tanks and drains.
    for z in (20, 33):
        t.fill((25, 2, z), (33, 2, z), "create:depot")
        t.fill((25, 4, z - 1), (33, 4, z - 1), "create:fluid_pipe")
        for x in (26, 30, 33):
            t.set(x, 3, z, "create:encased_fan", facing="east")
        t.set(27, 4, z - 1, "create:mechanical_pump", facing="east")
    t.fill((24, 2, 15), (26, 6, 17), "create:fluid_tank")
    t.fill((22, 7, 16), (24, 7, 35), "create:fluid_pipe")
    t.fill((23, 4, 16), (23, 7, 16), "create:fluid_pipe")
    t.fill((23, 4, 35), (23, 7, 35), "create:fluid_pipe")

    # Inspection and normal rejected-lot holding remain bounded in D0.
    for x in (26, 30):
        t.fill((x, 2, 40), (x + 2, 2, 41), "create:depot")
    t.fill((32, 2, 39), (34, 4, 42), "immersiveengineering:crate")

    # Parallel clean packing/coding lines and dry case stock.
    for z in (21, 33):
        for x in (37, 41, 45):
            t.set(x, 2, z, "create:depot")
            t.set(x, 3, z, "create:mechanical_press", facing="east")
        t.fill((37, 5, z - 1), (47, 5, z - 1), "tfmg:steel_block")
    t.fill((37, 2, 41), (42, 4, 44), "create:cardboard_block")
    t.fill((44, 2, 41), (47, 4, 44), "immersiveengineering:crate")

    # Cold compartments: cooler walls, finished pallets and clear center aisle.
    for z in (8, 12, 21, 25):
        t.fill((48, 2, z), (49, 6, z + 2), "oritech:cooler_block")
        t.fill((53, 2, z), (55, 4, z + 2), "jaffabricate:pallet_full")
    t.fill((55, 5, 7), (55, 12, 27), "create:fluid_pipe")

    # Roof refrigeration banks and cold-room connection occupy the accepted crown.
    t.clear((50, 15, 9), (55, 18, 26))
    for z1 in (9, 22):
        t.fill((50, 15, z1), (55, 18, z1 + 3), "oritech:cooler_block")
    t.fill((52, 19, 9), (52, 19, 25), "create:fluid_pipe")
    t.fill((55, 13, 25), (55, 19, 25), "create:fluid_pipe")
    t.fill((49, 14, 15), (55, 14, 20), "minecraft:oxidized_copper_grate")

    # Wet-hall roof sanitation/ventilation plant connects to the cyan spine.
    for x, z in ((22, 16), (22, 35)):
        t.fill((x, 14, z), (x + 2, 16, z + 2), "create:fluid_tank")
        t.fill((x + 1, 7, z + 1), (x + 1, 14, z + 1), "create:fluid_pipe")
    for x in (26, 31, 36):
        t.set(x, 14, 26, "create:encased_fan", facing="east")

    # Staff hygiene fixtures and QA work/records surfaces.
    t.fill((22, 2, 4), (24, 2, 4), "minecraft:barrel", facing="up", open="false")
    t.set(24, 2, 9, "minecraft:cauldron")
    base.desk(t, 37, 2, 5)
    base.desk(t, 37, 2, 8)
    t.fill((40, 2, 4), (40, 4, 9), "minecraft:bookshelf")


def _pass12_institutional_identity(t: base.Template) -> None:
    """Apply VCF identity through restrained signs aligned with real zones."""
    base.wall_sign(t, 27, 7, 1, "north", "VERDANT CONTINUUM", "FOODS")
    base.wall_sign(t, 34, 7, 1, "north", "HARVEST & PACKAGING", "QUALITY ANNEX")
    base.wall_sign(t, 14, 7, 16, "west", "RAW HARVEST", "LOT INTAKE")
    base.wall_sign(t, 14, 7, 31, "west", "RECEIVING BAY 02", "CHECK / RECORD")
    base.wall_sign(t, 24, 6, 18, "west", "PT-9 SANITATION", "WET LINE 01")
    base.wall_sign(t, 24, 6, 31, "west", "PT-9 SANITATION", "WET LINE 02")
    base.wall_sign(t, 27, 5, 38, "north", "QUALITY INSPECTION", "GRADE / RELEASE")
    base.wall_sign(t, 33, 5, 38, "north", "REJECT DIVERSION", "QA HOLD")
    base.wall_sign(t, 36, 6, 18, "west", "CLEAN PACKING", "CASE CODE 01")
    base.wall_sign(t, 36, 6, 31, "west", "CLEAN PACKING", "CASE CODE 02")
    base.wall_sign(t, 48, 6, 7, "west", "COLD HOLD A", "FINISHED LOTS")
    base.wall_sign(t, 48, 6, 20, "west", "COLD HOLD B", "FINISHED LOTS")
    base.wall_sign(t, 52, 7, 30, "south", "REFRIGERATED", "DISPATCH")
    base.wall_sign(t, 22, 5, 11, "south", "STAFF HYGIENE", "CONTROLLED ENTRY")
    base.wall_sign(t, 37, 5, 11, "south", "QUALITY ASSURANCE", "BATCH RECORDS")
    base.wall_sign(t, 48, 13, 8, "north", "ROOF PLANT", "AUTHORIZED STAFF")


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
    if tuple(t.size) != (59, 24, 51):
        raise AssertionError(f"OWS-005 Gate-B r1 dimensions changed unexpectedly: {t.size}")

    # Freeze representative points from all eight Gate-A accepted aspects.
    frozen = {
        (3, 8, 20): "immersiveengineering:sheetmetal_steel",
        (56, 9, 40): "minecraft:white_concrete",
        (12, 5, 25): "minecraft:bricks",
        (30, 13, 25): "minecraft:light_gray_concrete",
        (40, 18, 16): "minecraft:light_gray_concrete",
        (57, 8, 15): "minecraft:light_gray_concrete",
        (20, 7, 5): "minecraft:white_concrete",
        (55, 14, 8): "tfmg:steel_block",
    }
    for pos, expected in frozen.items():
        actual = _name_at(t, pos)
        if actual != expected:
            raise AssertionError(f"Gate-A frozen aspect changed at {pos}: {actual} != {expected}")

    # Maintenance ladder must remain continuous through the cold-block roof.
    for y in range(2, 15):
        if _name_at(t, (47, y, 8)) != "minecraft:ladder":
            raise AssertionError(f"Maintenance ladder gap at y={y}")

    # Critical material transfers retain two-block-high traversable openings.
    for x, z in ((23, 19), (23, 32), (35, 19), (35, 33), (46, 12), (46, 23)):
        if _name_at(t, (x, 2, z)) != "minecraft:iron_door" or _name_at(t, (x, 3, z)) != "minecraft:iron_door":
            raise AssertionError(f"Controlled transfer door missing at {(x, z)}")

    # Protected center aisles in wet, packing and cold zones stay navigable.
    protected = (
        ((29, 2, 14), (29, 3, 18)),
        ((29, 2, 23), (29, 3, 25)),
        ((29, 2, 29), (29, 3, 31)),
        ((29, 2, 36), (29, 3, 37)),
        ((39, 2, 14), (39, 3, 17)),
        ((39, 2, 24), (39, 3, 31)),
        ((39, 2, 35), (39, 3, 38)),
        ((51, 2, 7), (52, 3, 17)),
        ((51, 2, 19), (52, 3, 28)),
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
        raise AssertionError(f"Gate-B model contains deferred proof/encounter blocks: {sorted(present_forbidden)}")
    sign_count = sum(name.endswith("_wall_sign") for name in names)
    if sign_count < 16:
        raise AssertionError(f"VCF/process wayfinding unexpectedly sparse: {sign_count} signs")


def _name(t: base.Template, pos: tuple[int, int, int]) -> str | None:
    entry = t.blocks.get(pos)
    return None if entry is None else t.palette[entry[0]]["Name"]


def _diff_count(a: base.Template, b: base.Template) -> int:
    positions = set(a.blocks) | set(b.blocks)
    return sum(1 for pos in positions if _name(a, pos) != _name(b, pos))


def _count_block(t: base.Template, name: str) -> int:
    return sum(1 for pos in t.blocks if _name(t, pos) == name)


def build_d0() -> base.Template:
    t = build_gate_b_intact()
    _assert_intact_contracts(t)
    return t


def build_d1() -> base.Template:
    """Localized early-anomaly intervention around line 02 and QA rejection."""
    t = build_d0()

    # Yellow quality-control fields grow from ordinary line/reject boundaries,
    # but stay on floors so the accepted process geometry remains readable.
    t.fill((24, 1, 30), (34, 1, 37), "minecraft:yellow_concrete")
    t.fill((24, 1, 38), (34, 1, 43), "minecraft:yellow_concrete")
    t.fill((47, 1, 19), (56, 1, 29), "minecraft:yellow_concrete")
    t.fill((50, 1, 19), (52, 1, 29), "minecraft:smooth_stone")

    # Temporary controlled bulkhead keeps the wet central aisle usable.
    t.fill((24, 2, 30), (28, 5, 30), "minecraft:white_concrete")
    t.fill((30, 2, 30), (34, 5, 30), "minecraft:white_concrete")
    base.door(t, 29, 2, 30, "south", "iron")
    t.fill((24, 5, 30), (34, 5, 30), "minecraft:yellow_concrete")

    # Line-02 sanitation bypass, replacement media and suspect lot staging.
    t.fill((24, 6, 34), (33, 6, 34), "create:fluid_pipe")
    t.set(27, 6, 34, "create:mechanical_pump", facing="east")
    t.fill((25, 2, 35), (27, 4, 37), "immersiveengineering:crate")
    t.fill((31, 2, 39), (34, 4, 42), "create:cardboard_block")

    # Cold hold B receives segregated finished lots; compartment A stays normal.
    t.fill((53, 2, 21), (55, 5, 27), "create:cardboard_block")
    t.fill((48, 2, 20), (49, 4, 22), "oritech:cooler_block")

    base.wall_sign(t, 27, 5, 30, "north", "LINE 02 HOLD", "SANITATION REVIEW")
    base.wall_sign(t, 32, 5, 38, "north", "PT-9 LOT HOLD", "QA RELEASE ONLY")
    base.wall_sign(t, 48, 6, 20, "west", "COLD HOLD B", "SEGREGATED LOTS")

    # D1 remains an intact local intervention with all accepted routes present.
    _assert_intact_contracts(t)
    return t


def build_d3() -> base.Template:
    """Causal centuries-later ruin derived from the D1 system failures."""
    t = build_d1()

    # Wet line 02: sanitation tank/header and adjacent roof fail together.
    t.clear((22, 14, 35), (24, 16, 37))
    t.clear((24, 13, 32), (30, 13, 39))
    t.clear((24, 11, 34), (28, 12, 34))
    t.fill((24, 1, 33), (28, 1, 38), "minecraft:mossy_stone_bricks")
    t.fill((25, 2, 35), (28, 2, 38), "minecraft:gravel")
    t.set(26, 3, 36, "minecraft:cobweb")
    t.set(28, 2, 34, "minecraft:brown_mushroom")

    # Packing line 02: a coherent rear-monitor weather breach drops debris onto
    # the affected line while preserving the high-bay frame and line 01.
    t.clear((44, 21, 29), (48, 21, 40))
    t.clear((48, 19, 35), (48, 20, 40))
    t.clear((44, 2, 33), (47, 4, 35))
    t.fill((43, 1, 32), (47, 1, 36), "minecraft:cracked_stone_bricks")
    t.fill((44, 2, 34), (47, 3, 37), "minecraft:gravel")
    t.set(43, 3, 35, "minecraft:cobweb")

    # Cold hold B: the matching refrigeration bank and local roof/deck fail.
    t.clear((50, 15, 22), (55, 18, 25))
    t.clear((53, 14, 22), (56, 14, 27))
    t.clear((55, 5, 22), (55, 11, 27))
    t.fill((53, 2, 22), (55, 4, 27), "minecraft:mossy_stone_bricks")
    t.set(54, 5, 24, "minecraft:cobweb")
    t.set(55, 2, 26, "minecraft:brown_mushroom")

    # Receiving bay 02 takes smaller canopy loss; bay 01 and threshold remain.
    t.clear((3, 8, 31), (8, 9, 38))
    t.clear((3, 3, 34), (3, 7, 34))
    t.fill((4, 1, 34), (8, 2, 38), "minecraft:gravel")
    t.set(8, 3, 37, "minecraft:cobweb")

    # Local water-path weathering follows downpipes and the reject exit.
    t.fill((23, 1, 42), (26, 1, 44), "minecraft:mossy_stone_bricks")
    t.fill((26, 0, 45), (29, 0, 48), "minecraft:coarse_dirt")
    t.set(24, 2, 43, "minecraft:cobweb")

    # Prove the accepted architecture/routes before adding deferred gameplay
    # blocks that the Gate-B contract intentionally rejected.
    _assert_intact_contracts(t)

    # Clear a real approach inside the QA hold, then install exactly one proof.
    t.clear((31, 2, 39), (33, 3, 41))
    t.set(PROOF_POS[0], PROOF_POS[1] + 1, PROOF_POS[2], "minecraft:air")
    t.chest(*PROOF_POS, PROOF_LOOT_TABLE, facing="west")

    # Restrained vanilla encounter progression, away from proof and main aisles.
    t.spawner(17, 2, 34, "minecraft:spider", count=1, nearby=3)
    t.spawner(25, 2, 41, "minecraft:zombie", count=1, nearby=4)
    t.spawner(54, 2, 19, "minecraft:skeleton", count=1, nearby=3)

    _assert_d3_contracts(t)
    return t


def _assert_proof(t: base.Template) -> None:
    row = t.blocks.get(PROOF_POS)
    if row is None:
        raise AssertionError("OWS-005 D3 proof chest is missing")
    state_id, nbt = row
    if t.palette[state_id]["Name"] != "minecraft:chest":
        raise AssertionError(f"OWS-005 proof position contains {t.palette[state_id]['Name']}")
    if not nbt or nbt.get("LootTable") != PROOF_LOOT_TABLE:
        raise AssertionError(f"OWS-005 proof chest has wrong loot table: {None if not nbt else nbt.get('LootTable')}")
    if _name(t, (PROOF_POS[0], PROOF_POS[1] + 1, PROOF_POS[2])) not in AIR:
        raise AssertionError("OWS-005 proof chest has no clear block above")
    matching = sum(
        1 for _, block_nbt in t.blocks.values()
        if block_nbt and block_nbt.get("LootTable") == PROOF_LOOT_TABLE
    )
    if matching != 1:
        raise AssertionError(f"OWS-005 must contain exactly one canonical proof container; found {matching}")


def _assert_d3_contracts(t: base.Template) -> None:
    _assert_proof(t)
    if _count_block(t, "minecraft:spawner") != 3:
        raise AssertionError("OWS-005 D3 requires exactly three deliberate encounter spawners")
    for y in range(2, 15):
        if _name(t, (47, y, 8)) != "minecraft:ladder":
            raise AssertionError(f"OWS-005 D3 maintenance ladder gap at y={y}")
    for pos in ((30, 2, 2), (31, 2, 12), (32, 2, 38)):
        if not (_name(t, pos) or "").endswith("_door"):
            raise AssertionError(f"OWS-005 D3 proof route lost controlled door at {pos}")
    if _name(t, (32, 2, 39)) not in AIR:
        raise AssertionError("OWS-005 D3 proof approach is obstructed")
    sign_count = sum((_name(t, pos) or "").endswith("_wall_sign") for pos in t.blocks)
    if sign_count < 12:
        raise AssertionError(f"OWS-005 D3 preserves too little process identity: {sign_count} signs")
    for pos in ((27, 7, 1), (34, 7, 1)):
        if not (_name(t, pos) or "").endswith("_wall_sign"):
            raise AssertionError(f"OWS-005 D3 lost primary VCF identity at {pos}")
    if _count_block(t, "create:fluid_pipe") < 65:
        raise AssertionError("OWS-005 D3 removed too much service anatomy")
    if _count_block(t, "oritech:cooler_block") < 70:
        raise AssertionError("OWS-005 D3 removed too much cold-chain evidence")



