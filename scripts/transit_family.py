from __future__ import annotations

from typing import Any

A: Any = None


def configure(api: Any) -> None:
    global A
    A = api


def site(size, road=None):
    t = A.Template(size)
    A.roadside_apron(t, road=road)
    return t


def collapsed_subway_station_clean_master():
    t = A.Template((63, 24, 45))
    # Excavated station box: twin tracks, island platforms, concourse and two exits.
    t.clear((2, 1, 3), (60, 21, 41))
    t.fill((2, 0, 3), (60, 0, 41), "immersiveengineering:concrete_reinforced")
    for x in range(2, 61):
        t.fill((x, 1, 3), (x, 21, 3), "immersiveengineering:concrete_reinforced")
        t.fill((x, 1, 41), (x, 21, 41), "immersiveengineering:concrete_reinforced")
    for z in range(4, 41):
        t.fill((2, 1, z), (2, 21, z), "immersiveengineering:concrete_reinforced")
        t.fill((60, 1, z), (60, 21, z), "immersiveengineering:concrete_reinforced")
    t.fill((2, 21, 3), (60, 21, 41), "immersiveengineering:concrete_reinforced")
    # Track beds and two island platforms with shelter columns and signage.
    for z in (9, 35):
        t.fill((4, 1, z - 2), (58, 1, z + 2), "minecraft:deepslate_tiles")
        for x in range(5, 58):
            t.set(x, 2, z, "minecraft:rail", shape="east_west", waterlogged="false")
    t.fill((5, 2, 14), (57, 3, 19), "minecraft:smooth_stone")
    t.fill((5, 2, 25), (57, 3, 30), "minecraft:smooth_stone")
    for x in range(8, 57, 8):
        for z in (15, 29):
            t.fill((x, 4, z), (x, 9, z), "minecraft:polished_blackstone_bricks")
            t.fill((x - 2, 9, z - 1), (x + 2, 9, z + 1), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
            t.set(x, 6, z, "create:red_nixie_tube")
    # Mezzanine concourse, ticketing, toilets, staff and maintenance rooms.
    t.fill((4, 11, 6), (58, 12, 38), "minecraft:smooth_stone")
    t.clear((19, 11, 13), (43, 12, 31))
    A.stair_flight(t, 10, 3, 15, 9, "south", "minecraft:stone_brick_stairs")
    A.stair_flight(t, 47, 3, 26, 9, "north", "minecraft:stone_brick_stairs")
    t.fill((8, 13, 8), (24, 13, 10), "zvhouses:stone_brick_countertop")
    for x in (10, 14, 18, 22):
        t.set(x, 14, 10, "minecraft:iron_trapdoor", facing="south", half="top", open="false", powered="false", waterlogged="false")
    A.partition_x(t, 43, 13, 7, 18, "tfmg:cinder_block", 12)
    A.partition_x(t, 51, 13, 7, 18, "tfmg:cinder_block", 12)
    A.door(t, 43, 13, 14, "east", "iron")
    A.door(t, 51, 13, 14, "east", "iron")
    t.fill((45, 13, 8), (49, 16, 10), "minecraft:scaffolding")
    t.set(53, 13, 9, "minecraft:water_cauldron", level="1")
    t.set(56, 13, 9, "minecraft:quartz_stairs", facing="west", half="bottom", shape="straight", waterlogged="false")
    # Independent street stairs terminate in glazed entrance pavilions.
    A.stair_flight(t, 7, 12, 31, 9, "south", "minecraft:stone_brick_stairs")
    A.stair_flight(t, 50, 12, 7, 9, "south", "minecraft:stone_brick_stairs")
    A.shell(t, (4, 20, 30), (16, 23, 40), "create:framed_glass", "minecraft:smooth_stone", "minecraft:smooth_stone_slab")
    A.shell(t, (47, 20, 4), (59, 23, 14), "create:framed_glass", "minecraft:smooth_stone", "minecraft:smooth_stone_slab")
    return t


def collapsed_subway_station():
    t = collapsed_subway_station_clean_master()
    t.clear((39, 8, 22), (62, 23, 44))
    t.fill((41, 1, 23), (62, 10, 44), "minecraft:gravel")
    t.clear((1, 15, 2), (18, 23, 17))
    t.spawner(28, 3, 17, "minecraft:zombie", count=3, nearby=8)
    return t


def ruined_bus_terminal_clean_master():
    t = site((61, 24, 51), road=(0, 0, 60, 8))
    A.shell(t, (5, 1, 8), (40, 16, 43), "minecraft:bricks", "tfmg:factory_floor", "minecraft:smooth_stone")
    A.shell(t, (13, 1, 5), (31, 9, 10), "minecraft:smooth_stone", "minecraft:polished_andesite", "minecraft:smooth_stone_slab")
    A.double_door(t, 21, 2, 5, "north", "dark_oak")
    A.double_door(t, 21, 2, 10, "south", "dark_oak")
    # Ticket lobby, waiting hall, café, toilets, baggage and staff offices.
    t.fill((9, 2, 13), (23, 2, 15), "zvhouses:spruce_countertop")
    for x in range(10, 24, 4):
        t.set(x, 3, 15, "minecraft:iron_trapdoor", facing="south", half="top", open="false", powered="false", waterlogged="false")
    for x in (9, 15, 23, 29):
        for z in (21, 27):
            t.fill((x, 2, z), (x + 3, 2, z), "minecraft:dark_oak_stairs", facing="south", half="bottom", shape="straight", waterlogged="false")
    A.partition_z(t, 33, 2, 6, 39, "tfmg:cinder_block", (10, 18, 27, 36))
    A.partition_x(t, 16, 2, 34, 42, "tfmg:cinder_block", 37)
    A.partition_x(t, 29, 2, 34, 42, "tfmg:cinder_block", 37)
    t.set(8, 2, 36, "minecraft:smoker", facing="south", lit="false")
    t.set(11, 2, 36, "minecraft:water_cauldron", level="1")
    t.fill((18, 2, 35), (26, 5, 40), "minecraft:scaffolding")
    A.desk(t, 31, 2, 35)
    t.set(37, 2, 36, "the_wasteland_reworked:radio")
    # Six sawtooth bus bays with covered boarding islands and maintenance shed.
    for z in (10, 17, 24, 31, 38, 45):
        t.fill((42, 0, z), (60, 0, min(49, z + 4)), "tfmg:asphalt")
        t.fill((42, 1, z), (54, 1, z), "minecraft:white_concrete")
        t.fill((41, 7, z), (56, 7, min(49, z + 3)), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
        t.fill((42, 1, z + 1), (42, 6, z + 1), "minecraft:polished_blackstone_bricks")
    A.shell(t, (43, 1, 39), (58, 12, 49), "tfmg:cinder_block", "minecraft:smooth_stone", "minecraft:weathered_cut_copper")
    t.clear((46, 2, 39), (54, 7, 39))
    t.fill((47, 2, 45), (55, 5, 47), "minecraft:scaffolding")
    for x in (8, 15, 28, 36):
        A.window(t, x, 4, 8)
    t.fill((4, 12, 36), (24, 12, 47), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
    t.fill((38, 2, 39), (38, 16, 39), "minecraft:ladder", facing="west", waterlogged="false")
    t.set(38, 17, 39, "minecraft:iron_trapdoor", facing="north", half="bottom", open="false", powered="false", waterlogged="false")
    return t


def ruined_bus_terminal():
    t = ruined_bus_terminal_clean_master()
    t.clear((37, 9, 26), (60, 23, 50))
    t.fill((40, 1, 28), (60, 7, 50), "minecraft:gravel")
    t.spawner(22, 2, 25, "minecraft:zombie", count=2, nearby=7)
    return t


def elevated_rail_collapse_clean_master():
    t = site((67, 30, 39), road=(0, 13, 66, 25))
    # Four-pier viaduct carries twin tracks and an elevated side-platform stop.
    for x in (6, 24, 42, 60):
        t.fill((x, 1, 8), (x + 3, 17, 11), "immersiveengineering:concrete_reinforced")
        t.fill((x, 1, 27), (x + 3, 17, 30), "immersiveengineering:concrete_reinforced")
    t.fill((2, 17, 6), (64, 20, 32), "immersiveengineering:concrete_reinforced")
    for x in range(3, 64):
        t.set(x, 21, 13, "minecraft:rail", shape="east_west", waterlogged="false")
        t.set(x, 21, 25, "minecraft:rail", shape="east_west", waterlogged="false")
    t.fill((15, 21, 7), (51, 22, 11), "minecraft:smooth_stone")
    t.fill((15, 21, 27), (51, 22, 31), "minecraft:smooth_stone")
    for x in (17, 27, 39, 49):
        t.fill((x, 23, 8), (x, 28, 10), "minecraft:polished_blackstone_bricks")
        t.fill((x - 2, 28, 7), (x + 2, 28, 11), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
    # Street ticket house and two enclosed stairs reach both platforms.
    A.shell(t, (25, 1, 13), (41, 10, 25), "minecraft:bricks", "tfmg:factory_floor", "minecraft:smooth_stone")
    A.double_door(t, 32, 2, 13, "north", "iron")
    t.fill((28, 2, 17), (38, 2, 19), "zvhouses:stone_brick_countertop")
    t.set(38, 2, 22, "the_wasteland_reworked:radio")
    A.stair_flight(t, 17, 3, 12, 18, "south", "minecraft:stone_brick_stairs")
    A.stair_flight(t, 47, 3, 9, 18, "south", "minecraft:stone_brick_stairs")
    return t


def elevated_rail_collapse():
    t = elevated_rail_collapse_clean_master()
    t.clear((35, 14, 4), (57, 29, 35))
    t.fill((38, 1, 9), (58, 13, 35), "minecraft:gravel")
    t.fill((41, 5, 12), (60, 8, 29), "immersiveengineering:concrete_reinforced")
    t.spawner(31, 2, 22, "minecraft:pillager", count=2, nearby=6)
    return t


def sunken_highway_interchange_clean_master():
    t = site((73, 25, 73))
    # Excavated east-west mainline, grade-separated crossing and four curved-ish ramps.
    t.fill((0, 0, 27), (72, 0, 45), "tfmg:asphalt")
    t.fill((27, 8, 0), (45, 11, 72), "immersiveengineering:concrete_reinforced")
    t.fill((31, 12, 0), (41, 12, 72), "tfmg:asphalt")
    for x in (13, 58):
        t.fill((x, 1, 27), (x + 3, 10, 45), "immersiveengineering:concrete_reinforced")
    for i in range(24):
        # Broad stepped ramps feather into both road levels without fragile diagonals.
        y = min(8, i // 3)
        for x, z in ((3 + i, 22 - i // 2), (46 + i, 50 + i // 2), (22 - i // 2, 46 + i), (50 + i // 2, 3 + i)):
            t.fill((max(0, x), y, max(0, z)), (min(72, x + 6), y + 1, min(72, z + 5)), "tfmg:asphalt")
    # Retaining walls, underpass service refuge and directional gantries.
    for x in range(73):
        t.fill((x, 1, 24), (x, 8, 26), "minecraft:stone_bricks")
        t.fill((x, 1, 46), (x, 8, 48), "minecraft:stone_bricks")
    A.shell(t, (3, 1, 30), (16, 8, 42), "tfmg:cinder_block", "minecraft:smooth_stone", "minecraft:smooth_stone")
    A.door(t, 9, 2, 30, "north", "iron")
    t.fill((5, 2, 35), (13, 5, 40), "minecraft:scaffolding")
    t.set(13, 2, 32, "the_wasteland_reworked:radio")
    for x in (20, 52):
        t.fill((x, 12, 29), (x + 2, 20, 31), "minecraft:polished_blackstone_bricks")
        t.fill((x, 20, 29), (x + 16, 22, 31), "minecraft:polished_blackstone_bricks")
        t.fill((x + 4, 19, 28), (x + 12, 21, 28), "minecraft:yellow_concrete")
    return t


def sunken_highway_interchange():
    t = sunken_highway_interchange_clean_master()
    t.clear((37, 7, 34), (64, 24, 65))
    t.fill((39, 1, 36), (66, 12, 67), "minecraft:gravel")
    t.clear((13, 9, 0), (33, 24, 27))
    t.spawner(9, 2, 36, "minecraft:zombie", count=2, nearby=6)
    return t


def collapsed_airship_terminal_clean_master():
    t = site((67, 35, 57), road=(20, 0, 46, 6))
    # Passenger terminal, high departure hall, baggage/service wing and two berths.
    A.shell(t, (5, 1, 7), (45, 22, 49), "minecraft:bricks", "tfmg:factory_floor", "minecraft:smooth_stone")
    A.shell(t, (15, 1, 4), (35, 10, 9), "minecraft:smooth_stone", "minecraft:polished_andesite", "minecraft:smooth_stone_slab")
    A.double_door(t, 24, 2, 4, "north", "iron")
    A.double_door(t, 24, 2, 9, "south", "iron")
    t.fill((8, 2, 13), (26, 2, 15), "zvhouses:stone_brick_countertop")
    for x in (9, 14, 19, 24):
        t.set(x, 3, 15, "minecraft:iron_trapdoor", facing="south", half="top", open="false", powered="false", waterlogged="false")
    for x in (10, 18, 29, 37):
        for z in (22, 29):
            t.fill((x, 2, z), (x + 4, 2, z), "minecraft:dark_oak_stairs", facing="south", half="bottom", shape="straight", waterlogged="false")
    A.partition_z(t, 36, 2, 6, 44, "tfmg:cinder_block", (10, 21, 33, 40))
    t.fill((7, 2, 39), (21, 5, 46), "minecraft:scaffolding")
    A.desk(t, 27, 2, 39)
    t.set(33, 2, 40, "the_wasteland_reworked:radio")
    t.set(30, 2, 40, "minecraft:barrel", facing="up", open="false")
    # Elevated boarding galleries lead to two armored mooring towers.
    t.fill((39, 12, 13), (61, 15, 20), "immersiveengineering:sheetmetal_steel")
    t.fill((39, 12, 34), (61, 15, 41), "immersiveengineering:sheetmetal_steel")
    for z in (13, 34):
        A.shell(t, (56, 1, z), (64, 31, z + 7), "minecraft:polished_blackstone_bricks", "minecraft:smooth_stone", "minecraft:smooth_stone")
        t.clear((57, 12, z + 1), (63, 20, z + 6))
        A.stair_flight(t, 57, 2, z + 1, 13, "south", "minecraft:stone_brick_stairs")
        # The 13-step flight climbs 6 steps past the tower shell's far wall
        # (z + 7), so those upper treads had no backing at all and floated
        # in open air. A real exterior maintenance-stair wall picks up where
        # the tower shell leaves off, backing every step through the top.
        t.fill((56, 9, z + 8), (56, 14, z + 13), "minecraft:polished_blackstone_bricks")
    t.fill((10, 22, 16), (38, 30, 39), "create:framed_glass")
    t.fill((6, 22, 40), (23, 27, 49), "immersiveengineering:sheetmetal_steel")
    return t


def collapsed_airship_terminal():
    t = collapsed_airship_terminal_clean_master()
    t.clear((38, 13, 24), (66, 34, 56))
    t.fill((40, 1, 27), (66, 12, 56), "minecraft:gravel")
    t.clear((3, 18, 5), (22, 34, 27))
    t.spawner(25, 2, 28, "minecraft:pillager", count=3, nearby=8)
    return t


def crashed_cargo_airship_clean_master():
    t = site((71, 29, 39))
    # Tapered rigid hull with command bow, cargo spine, engine rooms and tail.
    for x in range(5, 66):
        taper = min(9, 2 + min(x - 5, 65 - x) // 3)
        t.fill((x, 8 - taper // 3, 19 - taper), (x, 12 + taper // 3, 19 + taper), "minecraft:oxidized_copper")
    t.clear((8, 7, 12), (62, 14, 26))
    t.fill((7, 7, 10), (63, 7, 28), "immersiveengineering:sheetmetal_steel")
    t.fill((7, 14, 10), (63, 14, 28), "immersiveengineering:sheetmetal_steel")
    # Command deck, crew/service, three cargo holds and engine compartments.
    A.partition_x(t, 17, 8, 11, 27, "immersiveengineering:sheetmetal_steel", 19)
    A.partition_x(t, 27, 8, 11, 27, "immersiveengineering:sheetmetal_steel", 19)
    A.partition_x(t, 44, 8, 11, 27, "immersiveengineering:sheetmetal_steel", 19)
    A.partition_x(t, 55, 8, 11, 27, "immersiveengineering:sheetmetal_steel", 19)
    A.desk(t, 9, 8, 16)
    t.set(13, 8, 16, "the_wasteland_reworked:radio")
    for x in (20, 31, 38, 47):
        t.fill((x, 8, 13), (x + 4, 11, 25), "jaffabricate:pallet_full")
    for x in (57, 61):
        t.set(x, 8, 14, "create:mechanical_press")
        t.set(x, 8, 24, "minecraft:blast_furnace", facing="west", lit="false")
    A.bed(t, 20, 8, 12, "north", "gray")
    A.bed(t, 24, 8, 12, "north", "gray")
    # Keel, stabilizers, engine pods and tailplanes define the vehicle silhouette.
    t.fill((12, 3, 18), (59, 6, 20), "minecraft:polished_blackstone_bricks")
    t.fill((25, 10, 0), (43, 13, 38), "immersiveengineering:sheetmetal_steel")
    t.clear((26, 11, 10), (42, 13, 28))
    for z in (4, 31):
        t.fill((48, 5, z), (57, 10, z + 3), "tfmg:steel_block")
    t.fill((58, 15, 9), (68, 19, 29), "minecraft:oxidized_copper")
    t.fill((62, 19, 4), (69, 24, 34), "immersiveengineering:sheetmetal_steel")
    return t


def crashed_cargo_airship():
    t = crashed_cargo_airship_clean_master()
    t.clear((3, 10, 0), (29, 28, 24))
    t.fill((4, 1, 3), (31, 9, 27), "minecraft:gravel")
    t.clear((47, 13, 20), (70, 28, 38))
    t.spawner(35, 8, 21, "minecraft:zombie", count=2, nearby=7)
    return t
