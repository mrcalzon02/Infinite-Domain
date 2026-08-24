from __future__ import annotations
from typing import Any

A: Any = None


def configure(api: Any) -> None:
    global A
    A = api


def site(size, road=None):
    t = A.Template(size); A.roadside_apron(t, road=road); return t


def abandoned_orchard_cannery_clean_master():
    t = site((59, 24, 51), road=(20, 0, 38, 6))
    # Orchard rows feed a receiving dock, wash/sort line, cook hall, canning line and dispatch store.
    for x in range(4, 24, 5):
        for z in range(10, 47, 6):
            t.fill((x, 1, z), (x, 5, z), "minecraft:dark_oak_log", axis="y")
            t.fill((x - 2, 5, z - 2), (x + 2, 8, z + 2), "minecraft:oak_leaves", persistent="true", distance="1")
    # Three stepped departments prevent the factory from reading as one large
    # cube: low receiving/administration, tall cook hall and rear dispatch.
    A.shell(t, (26, 1, 8), (42, 11, 23), "minecraft:bricks", "tfmg:factory_floor", "minecraft:weathered_cut_copper")
    A.shell(t, (26, 1, 22), (55, 16, 46), "minecraft:bricks", "tfmg:factory_floor", "minecraft:weathered_cut_copper")
    A.shell(t, (43, 1, 10), (55, 12, 23), "minecraft:bricks", "tfmg:factory_floor", "minecraft:smooth_stone")
    t.clear((29, 2, 22), (39, 7, 23))
    # The breach into the dispatch office wing only opened that wing's own
    # west wall (x=43); the receiving wing's east wall (x=42) right next to
    # it was never cleared, so the office (desk + radio) stayed sealed
    # behind a solid wall with zero doors anywhere. Clear both wall layers
    # so the breach actually connects through to receiving's front door.
    t.clear((42, 2, 14), (44, 7, 20))
    A.double_door(t, 30, 2, 8, "north", "iron")
    A.partition_x(t, 34, 2, 9, 21, "tfmg:cinder_block", 15)
    A.partition_z(t, 31, 2, 27, 54, "tfmg:cinder_block", (32, 41, 50))
    A.partition_x(t, 46, 2, 32, 45, "tfmg:cinder_block", 38)
    # Intake crates -> wash trough -> cook vats -> packing shelves.
    t.fill((27, 2, 11), (31, 4, 16), "quark:apple_crate")
    for x in (29, 34, 39, 44, 49):
        t.set(x, 2, 21, "minecraft:water_cauldron", level="3")
        t.set(x, 2, 26, "minecraft:smoker", facing="south", lit="false")
        t.set(x, 2, 34, "create:mechanical_press")
        t.fill((x, 2, 38), (x, 4, 43), "minecraft:scaffolding")
    t.fill((48, 2, 33), (53, 5, 44), "minecraft:scaffolding")
    A.desk(t, 46, 2, 13)
    t.set(52, 2, 13, "the_wasteland_reworked:radio")
    A.double_door(t, 49, 2, 46, "south", "iron")
    t.fill((45, 8, 44), (57, 8, 50), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
    for x in (45, 57): t.fill((x, 1, 49), (x, 7, 49), "minecraft:polished_blackstone_bricks")
    for z in (13, 24, 37): A.window(t, 55, 5, z, axis="z")
    for x in (29, 36, 47, 52): A.window(t, x, 5, 8)
    # Three narrow sawtooth monitors and an offset boiler stack make the roof
    # line legible from a distance.
    for z in (25, 33, 41):
        t.fill((29, 16, z), (51, 18, z + 2), "create:framed_glass")
        t.fill((29, 19, z), (51, 19, z + 3), "minecraft:weathered_cut_copper_slab", type="bottom", waterlogged="false")
    t.fill((52, 1, 25), (55, 22, 28), "minecraft:bricks")
    t.clear((53, 2, 26), (54, 21, 27))
    return t


def abandoned_orchard_cannery():
    t = abandoned_orchard_cannery_clean_master(); t.clear((42, 10, 27), (58, 23, 50)); t.fill((44, 1, 29), (58, 4, 50), "minecraft:gravel"); t.fill((48, 5, 34), (58, 7, 43), "minecraft:gravel"); t.spawner(34, 2, 28, "minecraft:zombie", count=2, nearby=6); return t


def ruined_grain_elevator_clean_master():
    t = site((55, 35, 49), road=(18, 0, 36, 6))
    # Truck scale/intake pit, headhouse, four silos, cleaner, bagging and rail dispatch.
    t.fill((5, 1, 8), (24, 2, 16), "minecraft:smooth_stone")
    t.fill((9, 2, 10), (20, 3, 14), "minecraft:polished_blackstone")
    A.shell(t, (5, 1, 19), (24, 18, 44), "minecraft:bricks", "tfmg:factory_floor", "minecraft:smooth_stone")
    # Narrow elevator leg and four genuinely rounded storage bins. Their
    # circular plans distinguish them from generic towers at every angle.
    A.shell(t, (20, 1, 18), (30, 32, 39), "minecraft:light_gray_concrete", "minecraft:smooth_stone", "minecraft:smooth_stone")

    def silo(cx, cz):
        radius = 5
        for y in range(1, 27):
            for dx in range(-radius, radius + 1):
                for dz in range(-radius, radius + 1):
                    d2 = dx * dx + dz * dz
                    if d2 <= radius * radius and (y == 1 or d2 >= (radius - 1) * (radius - 1)):
                        t.set(cx + dx, y, cz + dz, "minecraft:light_gray_concrete")
        for rise, roof_radius in enumerate((5, 4, 3, 2, 1)):
            y = 27 + rise
            for dx in range(-roof_radius, roof_radius + 1):
                for dz in range(-roof_radius, roof_radius + 1):
                    if dx * dx + dz * dz <= roof_radius * roof_radius:
                        t.set(cx + dx, y, cz + dz, "minecraft:smooth_stone")

    for center in ((37, 12), (48, 12), (37, 29), (48, 29)):
        silo(*center)
    # Cleaner and bagging line: isolated machines remain readable instead of
    # becoming an implausible solid mass of processing blocks.
    t.fill((11, 2, 22), (21, 2, 22), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
    for x in (12, 16, 20):
        t.set(x, 3, 22, "create:mechanical_press")
        t.fill((x, 2, 25), (x, 3, 28), "minecraft:brown_wool")
    t.fill((7, 2, 32), (16, 5, 41), "minecraft:scaffolding")
    A.desk(t, 18, 2, 34)
    t.set(22, 2, 34, "the_wasteland_reworked:radio")
    A.stair_flight(t, 19, 2, 22, 15, "south", "minecraft:stone_brick_stairs")
    # The elevator leg tower (radio inside) is its own fully-walled box
    # (west wall at x=20) with no door anywhere, distinct from the headhouse
    # next door even though their footprints overlap. Cut a real doorway
    # through the shared wall so the headhouse's own front door actually
    # reaches the tower interior.
    t.clear((20, 2, 25), (20, 3, 25))
    A.door(t, 20, 2, 25, "east", "iron")
    t.fill((23, 28, 9), (49, 31, 33), "immersiveengineering:sheetmetal_steel")
    t.clear((25, 29, 11), (47, 30, 31))
    for x in range(4, 52):
        t.set(x, 1, 46, "minecraft:rail", shape="east_west", waterlogged="false")
    t.fill((5, 8, 40), (25, 8, 48), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
    A.double_door(t, 10, 2, 44, "south", "iron")
    t.fill((24, 32, 19), (48, 34, 22), "tfmg:steel_block")
    return t


def ruined_grain_elevator():
    t = ruined_grain_elevator_clean_master(); t.clear((42, 18, 4), (54, 34, 27)); t.fill((43, 1, 7), (54, 5, 27), "minecraft:gravel"); t.fill((47, 6, 11), (54, 10, 20), "minecraft:gravel"); t.spawner(17, 2, 37, "minecraft:pillager", count=2, nearby=6); return t


def shattered_greenhouse_nursery_clean_master():
    t = site((61, 21, 49), road=(21, 0, 39, 6))
    # Retail/office headhouse feeds propagation, potting, hardening and dispatch houses.
    A.shell(t, (20, 1, 7), (40, 12, 20), "minecraft:bricks", "tfmg:factory_floor", "minecraft:smooth_stone")
    A.double_door(t, 29, 2, 7, "north", "dark_oak")
    A.partition_x(t, 31, 2, 8, 19, "tfmg:cinder_block", 13)
    A.desk(t, 22, 2, 10); t.set(26, 2, 10, "the_wasteland_reworked:radio")
    t.fill((33, 2, 10), (38, 5, 17), "minecraft:scaffolding")
    def greenhouse_bay(x1, x2):
        z1, z2, eave = 21, 45, 10
        t.fill((x1, 1, z1), (x2, 1, z2), "minecraft:coarse_dirt")
        t.fill((x1, 2, z1), (x2, 2, z1), "minecraft:bricks")
        t.fill((x1, 2, z2), (x2, 2, z2), "minecraft:bricks")
        t.fill((x1, 2, z1), (x1, 2, z2), "minecraft:bricks")
        t.fill((x2, 2, z1), (x2, 2, z2), "minecraft:bricks")
        t.fill((x1, 3, z1), (x2, eave - 1, z1), "create:framed_glass")
        t.fill((x1, 3, z2), (x2, eave - 1, z2), "create:framed_glass")
        t.fill((x1, 3, z1), (x1, eave - 1, z2), "create:framed_glass")
        t.fill((x2, 3, z1), (x2, eave - 1, z2), "create:framed_glass")
        for x in range(x1, x2 + 1, 5):
            t.fill((x, 2, z1), (x, eave, z1), "minecraft:stripped_dark_oak_log", axis="y")
            t.fill((x, 2, z2), (x, eave, z2), "minecraft:stripped_dark_oak_log", axis="y")
        for z in range(z1, z2 + 1, 6):
            t.fill((x1, 2, z), (x1, eave, z), "minecraft:stripped_dark_oak_log", axis="y")
            t.fill((x2, 2, z), (x2, eave, z), "minecraft:stripped_dark_oak_log", axis="y")
        rises = (x2 - x1) // 2
        for rise in range(rises + 1):
            left, right, y = x1 + rise, x2 - rise, eave + rise
            t.fill((left, y, z1), (left, y, z2), "create:framed_glass")
            t.fill((right, y, z1), (right, y, z2), "create:framed_glass")
            t.fill((left, y, z1), (right, y, z1), "create:framed_glass")
            t.fill((left, y, z2), (right, y, z2), "create:framed_glass")

    for x1, x2 in ((3, 17), (21, 39), (43, 57)):
        greenhouse_bay(x1, x2)
        for x in range(x1 + 2, x2 - 1, 4):
            t.fill((x, 2, 24), (x, 2, 42), "minecraft:farmland", moisture="7")
            for z in range(25, 42, 4): t.set(x, 3, z, "minecraft:flower_pot")
        # The east and west bays were fully enclosed glass boxes with no
        # door on any side (only the middle bay got one, below). Give each
        # its own south-wall door, seated next to the nearest structural
        # post (x1 + 5) rather than in open glazing, so it is actually
        # framed instead of floating in an unwalled window run.
        if x1 != 21:
            A.door(t, x1 + 6, 2, 45, "south", "iron")
    # Potting line, irrigation tanks and exterior tree/shrub yard.
    t.fill((22, 2, 24), (38, 3, 27), "minecraft:spruce_planks")
    for x in (24, 29, 34): t.set(x, 3, 25, "minecraft:composter", level="5")
    for x in (5, 12, 45, 52): t.fill((x, 2, 42), (x + 2, 2, 44), "minecraft:water_cauldron", level="3")
    for x in range(4, 58, 6):
        t.fill((x, 1, 17), (x, 4, 17), "minecraft:spruce_log", axis="y"); t.fill((x - 1, 4, 16), (x + 1, 6, 18), "minecraft:spruce_leaves", persistent="true", distance="1")
    # Seated next to the post at x=26 (was mid-glazing at x=28, which left
    # the door itself unframed on both axes — a pre-existing opening-coupling
    # bug caught incidentally while fixing the other two bays' missing doors).
    A.door(t, 27, 2, 45, "south", "iron")
    return t


def shattered_greenhouse_nursery():
    t = shattered_greenhouse_nursery_clean_master(); t.clear((40, 7, 18), (60, 20, 48)); t.fill((44, 1, 24), (59, 3, 46), "minecraft:gravel"); t.fill((50, 4, 30), (59, 6, 43), "minecraft:gravel"); t.spawner(29, 2, 34, "minecraft:zombie", count=2, nearby=6); return t


def remote_sawmill_clean_master():
    t = site((63, 32, 53), road=(0, 0, 62, 7))
    # Log yard -> debarker/saw hall -> sorting shed -> drying racks -> dispatch.
    for x in (4, 9, 14):
        for z in range(13, 47, 5): t.fill((x, 1, z), (x + 2, 4, z), "minecraft:spruce_log", axis="x")
    A.shell(t, (19, 1, 9), (45, 17, 43), "minecraft:stripped_spruce_log", "tfmg:factory_floor", "minecraft:dark_oak_planks")
    A.gable_roof_x(t, 19, 45, 9, 43, 17, "minecraft:stripped_spruce_log", "minecraft:dark_oak_stairs", "minecraft:stripped_dark_oak_log")
    t.clear((24, 2, 9), (40, 8, 9)); t.clear((24, 2, 43), (40, 8, 43))
    for z in (13, 21, 31, 39):
        A.window(t, 19, 9, z, axis="z")
        A.window(t, 45, 9, z, axis="z")
    for x in (23, 29, 35, 41):
        t.set(x, 2, 16, "create:mechanical_saw"); t.fill((x, 2, 20), (x, 3, 35), "minecraft:stripped_spruce_log", axis="z")
    A.shell(t, (47, 1, 12), (59, 12, 30), "minecraft:bricks", "minecraft:smooth_stone", "minecraft:weathered_cut_copper")
    A.gable_roof_x(t, 47, 59, 12, 30, 12, "minecraft:bricks", "minecraft:weathered_cut_copper_stairs", "minecraft:weathered_cut_copper")
    A.door(t, 52, 2, 12, "north", "iron"); A.desk(t, 49, 2, 16); t.set(56, 2, 16, "the_wasteland_reworked:radio")
    t.fill((48, 2, 22), (57, 5, 28), "minecraft:scaffolding")
    for x in (47, 52, 57):
        for px in (x, x + 3):
            for pz in (34, 48):
                t.fill((px, 1, pz), (px, 6, pz), "minecraft:stripped_spruce_log", axis="y")
        t.fill((x, 6, 34), (x + 3, 6, 48), "minecraft:spruce_slab", type="bottom", waterlogged="false")
        for z in (36, 40, 44):
            t.fill((x, 2, z), (x + 3, 2, z), "minecraft:spruce_planks")
    t.fill((18, 8, 40), (46, 8, 49), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
    return t


def remote_sawmill():
    t = remote_sawmill_clean_master()
    t.clear((34, 12, 30), (62, 31, 52))
    # Stepped roof and rack debris, not a single rectangular rubble volume.
    t.fill((36, 1, 34), (46, 3, 42), "minecraft:gravel")
    t.fill((42, 1, 39), (53, 5, 48), "minecraft:gravel")
    t.fill((51, 1, 45), (62, 2, 52), "minecraft:gravel")
    t.fill((39, 4, 37), (48, 4, 38), "minecraft:stripped_spruce_log", axis="x")
    t.fill((48, 6, 42), (58, 6, 43), "minecraft:stripped_spruce_log", axis="x")
    t.spawner(27, 2, 31, "minecraft:pillager", count=2, nearby=6)
    return t
