from __future__ import annotations

from typing import Any


A: Any = None


def configure(api: Any) -> None:
    global A
    A = api


def site(size: tuple[int, int, int], road: tuple[int, int, int, int] | None = None):
    t = A.Template(size)
    A.roadside_apron(t, road=road)
    return t


def bathroom(t, x: int, y: int, z: int, facing: str = "north") -> None:
    t.set(x, y, z, "minecraft:water_cauldron", level="2")
    t.set(x + 2, y, z, "minecraft:quartz_stairs", facing=facing, half="bottom", shape="straight", waterlogged="false")
    t.set(x + 2, y + 1, z + 1, "minecraft:lever", face="wall", facing="south", powered="false")


def kitchenette(t, x: int, y: int, z: int, length: int = 5) -> None:
    for dx in range(length):
        t.set(x + dx, y, z, "minecraft:barrel", facing="up", open="false")
    t.set(x, y, z + 1, "minecraft:smoker", facing="north", lit="false")
    t.set(x + 2, y, z + 1, "minecraft:water_cauldron", level="1")
    t.set(x + length - 1, y + 1, z, "supplementaries:item_shelf")


def sitting_room(t, x: int, y: int, z: int) -> None:
    for dx in range(3):
        t.set(x + dx, y, z, "minecraft:dark_oak_stairs", facing="south", half="bottom", shape="straight", waterlogged="false")
    t.set(x + 1, y, z + 3, "minecraft:spruce_slab", type="bottom", waterlogged="false")
    t.set(x + 4, y, z + 1, "the_wasteland_reworked:radio")
    t.set(x + 4, y + 1, z + 1, "supplementaries:item_shelf")


def apartment(t, x1: int, x2: int, y: int, z1: int, z2: int, *, bed_color: str = "gray") -> None:
    """Compact but complete dwelling with living/kitchen, bath and bedroom."""
    split_z = z1 + max(5, (z2 - z1) // 2)
    A.partition_z(t, split_z, y, x1, x2, "minecraft:stripped_spruce_wood", (x2 - 2,))
    A.partition_x(t, x1 + 4, y, split_z + 1, z2, "minecraft:stripped_spruce_wood", split_z + 3)
    sitting_room(t, x1 + 1, y, z1 + 1)
    kitchenette(t, max(x1 + 1, x2 - 5), y, z1 + 1, min(5, x2 - x1 - 1))
    A.bed(t, x1 + 1, y, z2 - 2, "north", bed_color)
    bathroom(t, x1 + 5, y, z2 - 2)
    t.set(x2 - 1, y, z2 - 1, "minecraft:barrel", facing="up", open="false")


def split_level_house_clean_master():
    t = site((31, 19, 27), road=(10, 0, 20, 6))
    # Interlocking lower masonry/garage and raised timber living volumes.
    A.shell(t, (4, 1, 6), (26, 10, 23), "minecraft:mud_bricks", "minecraft:oak_planks", "minecraft:dark_prismarine")
    A.shell(t, (13, 9, 8), (27, 16, 22), "the_wasteland_reworked:decayed_planks", "minecraft:oak_planks", "minecraft:weathered_cut_copper")
    t.clear((14, 10, 9), (26, 15, 21))
    # Two-car garage, mudroom/laundry and lower den.
    for x in (6, 13):
        t.clear((x, 2, 6), (x + 5, 6, 6))
    A.partition_x(t, 18, 2, 7, 22, "minecraft:stripped_dark_oak_wood", 12)
    A.partition_z(t, 14, 2, 19, 25, "minecraft:stripped_dark_oak_wood", (22,))
    t.set(6, 2, 18, "minecraft:blast_furnace", facing="south", lit="false")
    t.set(9, 2, 18, "minecraft:water_cauldron", level="2")
    sitting_room(t, 20, 2, 16)
    # Half-flight reaches the raised public level; second flight reaches beds.
    A.stair_flight(t, 16, 2, 10, 7, "south", "minecraft:oak_stairs")
    A.partition_z(t, 15, 10, 14, 26, "minecraft:stripped_spruce_wood", (19,))
    A.partition_x(t, 20, 10, 9, 21, "minecraft:stripped_spruce_wood", 17)
    kitchenette(t, 15, 10, 10, 5)
    sitting_room(t, 21, 10, 10)
    A.bed(t, 15, 10, 19, "north", "brown")
    A.bed(t, 22, 10, 19, "north", "gray")
    bathroom(t, 18, 10, 18)
    A.double_door(t, 14, 10, 8, "north", "oak")
    for x in (6, 22):
        A.window(t, x, 4, 6)
    for x in (15, 22, 25):
        A.window(t, x, 12, 8)
    for z in (11, 18):
        A.window(t, 27, 12, z, axis="z")
    # Projecting balcony, entry canopy and chimney make the split legible.
    t.fill((12, 9, 5), (28, 9, 8), "minecraft:oak_planks")
    t.fill((12, 15, 6), (18, 15, 9), "minecraft:weathered_cut_copper_slab", type="bottom", waterlogged="false")
    for x in (12, 18):
        t.fill((x, 9, 6), (x, 14, 6), "minecraft:stripped_spruce_log", axis="y")
    t.fill((25, 15, 18), (25, 18, 18), "minecraft:bricks")
    t.fill((13, 16, 8), (27, 16, 10), "minecraft:weathered_cut_copper_slab", type="bottom", waterlogged="false")
    t.fill((16, 17, 12), (24, 18, 18), "create:framed_glass")
    t.fill((19, 9, 22), (28, 9, 25), "minecraft:oak_planks")
    for x in (19, 28):
        t.fill((x, 9, 24), (x, 13, 24), "minecraft:stripped_spruce_log", axis="y")
    t.chest(24, 10, 20, "infinite_domain:chests/wasteland_home")
    return t


def split_level_house():
    t = split_level_house_clean_master()
    t.clear((21, 13, 17), (30, 18, 26))
    t.fill((22, 1, 18), (30, 4, 26), "minecraft:gravel")
    t.set(20, 10, 19, "the_wasteland_reworked:garbage_bag")
    t.spawner(8, 2, 18, "minecraft:zombie", count=1, nearby=4)
    return t


def culdesac_house(t, x: int, z: int, facing: str, accent: str, variant: int) -> None:
    A.shell(t, (x, 1, z), (x + 14, 9, z + 15), accent, "minecraft:spruce_planks", "minecraft:weathered_cut_copper")
    # Each house receives the same required domestic program but mirrored
    # room proportions and exterior identity change by variant.
    A.partition_z(t, z + 8, 2, x + 1, x + 13, "minecraft:stripped_spruce_wood", (x + 6,))
    A.partition_x(t, x + 8 + (variant % 2), 2, z + 9, z + 14, "minecraft:stripped_spruce_wood", z + 11)
    kitchenette(t, x + 2, 2, z + 5, 5)
    sitting_room(t, x + 8, 2, z + 3)
    A.bed(t, x + 2, 2, z + 12, "north", "brown" if variant % 2 else "gray")
    bathroom(t, x + 10, 2, z + 12)
    door_z = z if facing == "north" else z + 15
    A.door(t, x + 7, 2, door_z, facing, "spruce")
    A.window(t, x + 3, 3, door_z)
    A.window(t, x + 11, 3, door_z)
    A.window(t, x, 3, z + 5, axis="z")
    A.window(t, x + 14, 3, z + 11, axis="z")
    t.fill((x + 5, 1, z - 3 if facing == "north" else z + 15), (x + 9, 1, z if facing == "north" else z + 18), "minecraft:gravel")
    if variant % 2:
        t.fill((x + 10, 9, z + 10), (x + 13, 12, z + 14), accent)
        A.window(t, x + 11, 10, z + 10)
    # Varied gables and chimneys make the loop a neighborhood, not five boxes.
    A.gable_roof_x(t, x, x + 14, z, z + 15, 9, accent, "minecraft:dark_oak_stairs", "minecraft:stripped_dark_oak_log")
    chimney_x = x + 2 if variant % 2 else x + 12
    t.fill((chimney_x, 8, z + 10), (chimney_x, 15, z + 10), "minecraft:bricks")


def abandoned_culdesac_clean_master():
    t = site((67, 18, 67))
    # Loop road with a planted island and five individually oriented homes.
    for x in range(13, 54):
        for z in range(13, 54):
            d = ((x - 33) ** 2 + (z - 33) ** 2) ** 0.5
            if 14 <= d <= 20:
                t.set(x, 0, z, "tfmg:asphalt")
    t.fill((30, 0, 0), (36, 0, 18), "tfmg:asphalt")
    t.fill((29, 0, 29), (37, 0, 37), "minecraft:coarse_dirt")
    t.fill((33, 1, 33), (33, 5, 33), "minecraft:dead_bush")
    culdesac_house(t, 5, 5, "north", "minecraft:mud_bricks", 0)
    culdesac_house(t, 47, 5, "north", "minecraft:bricks", 1)
    culdesac_house(t, 4, 45, "south", "the_wasteland_reworked:decayed_planks", 2)
    culdesac_house(t, 48, 45, "south", "minecraft:yellow_terracotta", 3)
    culdesac_house(t, 26, 48, "south", "minecraft:stone_bricks", 4)
    for x, z in ((12, 26), (51, 28), (20, 46), (43, 45)):
        t.fill((x, 1, z), (x + 2, 2, z + 2), "minecraft:oxidized_copper")
    return t


def abandoned_culdesac():
    t = abandoned_culdesac_clean_master()
    t.clear((47, 6, 44), (66, 15, 66))
    t.fill((48, 1, 47), (66, 5, 66), "minecraft:gravel")
    t.clear((4, 7, 4), (12, 15, 13))
    t.set(32, 1, 35, "wastelands:scrap_pile")
    t.spawner(33, 1, 33, "minecraft:zombie", count=3, nearby=8)
    return t


def emergency_relief_shelter_clean_master():
    t = site((49, 18, 43), road=(18, 0, 30, 6))
    # Offset lobby, broad dormitory wing and rear clinical/service wing.
    A.shell(t, (4, 1, 7), (18, 11, 38), "minecraft:light_gray_concrete", "tfmg:factory_floor", "minecraft:smooth_stone")
    A.shell(t, (17, 1, 7), (32, 13, 38), "minecraft:smooth_stone", "tfmg:factory_floor", "minecraft:smooth_stone")
    A.shell(t, (31, 1, 7), (44, 10, 38), "minecraft:light_gray_concrete", "tfmg:factory_floor", "minecraft:smooth_stone")
    A.shell(t, (17, 1, 4), (31, 8, 9), "minecraft:smooth_stone", "minecraft:polished_andesite", "minecraft:smooth_stone_slab")
    A.double_door(t, 23, 2, 4, "north", "iron")
    A.double_door(t, 23, 2, 9, "south", "iron")
    # Registration, family/single dorms and a central supervised corridor.
    A.partition_z(t, 14, 2, 5, 43, "tfmg:cinder_block", (10, 24, 38))
    A.partition_x(t, 15, 2, 15, 31, "tfmg:cinder_block", 18)
    A.partition_x(t, 34, 2, 15, 31, "tfmg:cinder_block", 18)
    A.desk(t, 19, 2, 10)
    t.set(28, 2, 10, "the_wasteland_reworked:radio")
    for x1 in (6, 17, 36):
        for z in (17, 23, 29):
            A.bed(t, x1, 2, z, "north", "white")
            A.bed(t, x1 + 4, 2, z, "north", "gray")
    # Rear band: kitchen/dining, clinic/isolation, showers, stores and office.
    A.partition_z(t, 32, 2, 5, 43, "tfmg:cinder_block", (10, 22, 31, 39))
    for x in (15, 27, 35):
        A.partition_x(t, x, 2, 33, 37, "tfmg:cinder_block", 35)
    kitchenette(t, 6, 2, 35, 7)
    t.fill((17, 2, 34), (24, 2, 36), "minecraft:spruce_slab", type="bottom", waterlogged="false")
    A.bed(t, 28, 2, 35, "north", "white")
    t.set(31, 2, 34, "minecraft:brewing_stand", has_bottle_0="false", has_bottle_1="false", has_bottle_2="false")
    for x in (36, 39):
        bathroom(t, x, 2, 35)
    t.fill((42, 2, 34), (43, 5, 36), "minecraft:scaffolding")
    for x in (8, 16, 33, 41):
        A.window(t, x, 4, 7)
    for z in (19, 27, 35):
        A.window(t, 4, 4, z, axis="z")
        A.window(t, 44, 4, z, axis="z")
    for z in (18, 29):
        A.window(t, 18, 5, z, axis="z")
        A.window(t, 31, 5, z, axis="z")
    t.fill((3, 8, 13), (19, 8, 17), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
    t.fill((30, 7, 26), (46, 7, 31), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
    # Covered ambulance drop, roof monitor and rear delivery exit.
    t.fill((13, 8, 4), (35, 8, 10), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
    for x in (13, 35):
        t.fill((x, 1, 5), (x, 7, 5), "minecraft:polished_blackstone_bricks")
    t.fill((18, 13, 18), (30, 16, 26), "create:framed_glass")
    t.fill((42, 2, 30), (42, 13, 30), "minecraft:ladder", facing="west", waterlogged="false")
    t.set(42, 14, 30, "minecraft:iron_trapdoor", facing="north", half="bottom", open="false", powered="false", waterlogged="false")
    A.double_door(t, 7, 2, 38, "south", "iron")
    t.chest(42, 2, 35, "infinite_domain:chests/wasteland_home")
    return t


def emergency_relief_shelter():
    t = emergency_relief_shelter_clean_master()
    t.clear((33, 8, 25), (48, 17, 42))
    t.fill((34, 1, 27), (48, 5, 42), "minecraft:gravel")
    t.set(31, 2, 29, "the_wasteland_reworked:garbage_bag")
    t.spawner(11, 2, 25, "minecraft:pillager", count=2, nearby=7)
    t.spawner(29, 2, 35, "minecraft:pillager", count=2, nearby=7)
    return t


def tenement_courtyard_clean_master():
    t = site((57, 31, 53), road=(20, 0, 36, 6))
    wall, floor = "minecraft:bricks", "minecraft:spruce_planks"
    # U-shaped three-storey tenement leaves a real courtyard open to the road.
    for box in (((4, 1, 7), (17, 26, 48)), ((40, 1, 7), (53, 26, 48)), ((18, 1, 35), (39, 26, 48))):
        A.shell(t, box[0], box[1], wall, floor, "minecraft:smooth_stone")
    for y in (9, 17):
        t.fill((5, y, 8), (52, y, 47), floor)
        t.clear((18, y, 8), (39, y, 34))
    # Exterior galleries face the courtyard; two enclosed stairs serve all floors.
    for y in (2, 10, 18):
        t.fill((16, y, 10), (18, y, 46), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
        t.fill((39, y, 10), (41, y, 46), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
        for z in (12, 23, 37, 45):
            A.door(t, 17, y, z, "east", "spruce")
            A.door(t, 40, y, z, "west", "spruce")
            A.window(t, 4, y + 2, z, axis="z")
            A.window(t, 53, y + 2, z, axis="z")
        for z in (13, 28, 43):
            t.fill((2, y, z), (5, y, z + 3), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
            t.fill((52, y, z), (55, y, z + 3), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
            A.window(t, 4, y + 3, z + 1, axis="z")
            A.window(t, 53, y + 3, z + 1, axis="z")
    A.stair_flight(t, 11, 2, 37, 8, "south", "minecraft:stone_brick_stairs")
    A.stair_flight(t, 11, 10, 37, 8, "south", "minecraft:stone_brick_stairs")
    A.stair_flight(t, 44, 2, 37, 8, "south", "minecraft:stone_brick_stairs")
    A.stair_flight(t, 44, 10, 37, 8, "south", "minecraft:stone_brick_stairs")
    # Twelve complete flats, four per floor, flank the galleries.
    for y in (2, 10, 18):
        for x1, x2, z1, z2 in ((5, 16, 9, 22), (5, 16, 24, 36), (41, 52, 9, 22), (41, 52, 24, 36)):
            apartment(t, x1, x2, y, z1, z2, bed_color="brown" if (x1 + z1 + y) % 2 else "gray")
    # Courtyard laundry, play area, boiler room and street arch.
    t.fill((23, 1, 18), (34, 1, 22), "minecraft:coarse_dirt")
    for x in (24, 28, 32):
        t.set(x, 2, 20, "minecraft:cauldron")
    t.fill((24, 1, 27), (33, 1, 32), "minecraft:gravel")
    t.fill((20, 2, 35), (36, 8, 35), "minecraft:air")
    A.double_door(t, 27, 2, 48, "south", "iron")
    t.fill((21, 26, 40), (27, 30, 46), "minecraft:bricks")
    t.fill((30, 26, 40), (36, 29, 46), "immersiveengineering:sheetmetal_steel")
    return t


def tenement_courtyard():
    t = tenement_courtyard_clean_master()
    t.clear((39, 16, 4), (56, 30, 25))
    t.fill((40, 1, 8), (56, 7, 26), "minecraft:gravel")
    t.set(37, 10, 22, "minecraft:bricks")
    t.spawner(27, 2, 29, "minecraft:zombie", count=3, nearby=8)
    return t


def ruined_rowhouse_block_clean_master():
    t = site((61, 27, 41), road=(0, 0, 60, 7))
    colors = ("minecraft:bricks", "minecraft:mud_bricks", "minecraft:yellow_terracotta", "minecraft:stone_bricks", "the_wasteland_reworked:decayed_planks")
    for i, x in enumerate((3, 14, 25, 36, 47)):
        wall = colors[i]
        A.shell(t, (x, 1, 7), (x + 10, 22, 36), wall, "minecraft:spruce_planks", "minecraft:smooth_stone")
        for y in (8, 15):
            t.fill((x + 1, y, 8), (x + 9, y, 35), "minecraft:spruce_planks")
        A.door(t, x + 5, 2, 7, "north", "spruce")
        A.door(t, x + 5, 2, 36, "south", "spruce")
        for y in (2, 9, 16):
            A.partition_z(t, 20, y, x + 1, x + 9, "minecraft:stripped_spruce_wood", (x + 7,))
            kitchenette(t, x + 1, y, 10, 4)
            sitting_room(t, x + 5, y, 11)
            A.bed(t, x + 1, y, 30, "north", "gray" if i % 2 else "brown")
            bathroom(t, x + 6, y, 30)
            A.window(t, x + 2, y + 2, 7)
            A.window(t, x + 8, y + 2, 7)
            A.window(t, x + 5, y + 2, 36)
        A.stair_flight(t, x + 7, 2, 22, 7, "south", "minecraft:oak_stairs")
        A.stair_flight(t, x + 7, 9, 22, 7, "south", "minecraft:oak_stairs")
        # Individual stoop/bay/parapet rhythm prevents a single long slab.
        t.fill((x + 3, 1, 4), (x + 7, 1, 7), "minecraft:stone_bricks")
        t.fill((x + 2, 8, 6), (x + 8, 14, 7), wall)
        t.fill((x + 1, 8, 5), (x + 9, 8, 8), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
        t.fill((x + 2, 15, 6), (x + 8, 21, 7), wall)
        t.fill((x + 1, 15, 5), (x + 9, 15, 8), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
        chimney_x = x + 2 + (i % 2) * 6
        t.fill((chimney_x, 20, 30), (chimney_x + 1, 26, 31), "minecraft:bricks")
        t.fill((x + 1, 23 + (i % 2), 8), (x + 9, 23 + (i % 2), 35), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
    for y in (4, 11, 18):
        A.window(t, 3, y, 15, axis="z")
        A.window(t, 57, y, 28, axis="z")
    return t


def ruined_rowhouse_block():
    t = ruined_rowhouse_block_clean_master()
    t.clear((35, 12, 5), (49, 26, 40))
    t.fill((36, 1, 8), (50, 8, 39), "minecraft:gravel")
    t.clear((2, 17, 25), (13, 26, 40))
    t.spawner(18, 2, 28, "minecraft:zombie", count=2, nearby=6)
    t.spawner(53, 9, 28, "minecraft:pillager", count=2, nearby=6)
    return t


def shattered_luxury_condo_clean_master():
    t = site((51, 37, 49), road=(17, 0, 33, 6))
    # Stepped podium-and-tower mass: two-storey amenities below six residential levels.
    A.shell(t, (5, 1, 7), (45, 13, 43), "minecraft:smooth_quartz", "minecraft:polished_andesite", "minecraft:smooth_stone")
    A.shell(t, (13, 12, 13), (39, 34, 39), "minecraft:white_concrete", "minecraft:spruce_planks", "minecraft:smooth_stone")
    for y in (8, 16, 23, 30):
        x1, x2, z1, z2 = (6, 44, 8, 42) if y == 8 else (14, 38, 14, 38)
        t.fill((x1, y, z1), (x2, y, z2), "minecraft:spruce_planks")
    # Double-height lobby, concierge, mail, fitness, pool and service rooms.
    A.shell(t, (18, 1, 4), (32, 9, 9), "minecraft:smooth_quartz", "minecraft:polished_andesite", "minecraft:smooth_stone_slab")
    A.double_door(t, 24, 2, 4, "north", "dark_oak")
    A.double_door(t, 24, 2, 9, "south", "dark_oak")
    A.desk(t, 18, 2, 12)
    t.fill((7, 2, 17), (17, 2, 28), "minecraft:light_blue_concrete")
    t.fill((8, 1, 18), (16, 1, 27), "minecraft:water")
    for x in (33, 37, 41):
        t.set(x, 2, 18, "minecraft:iron_block")
        t.set(x, 2, 22, "minecraft:polished_blackstone")
    t.fill((34, 2, 31), (43, 5, 39), "minecraft:scaffolding")
    # Four luxury apartments per tower floor with broad corner glazing.
    for y in (16, 23):
        for x1, x2, z1, z2 in ((14, 25, 14, 25), (27, 38, 14, 25), (14, 25, 27, 38), (27, 38, 27, 38)):
            apartment(t, x1, x2, y, z1, z2, bed_color="white")
    # Twin protected stairs plus roof lounge and plant.
    A.stair_flight(t, 17, 2, 32, 7, "south", "minecraft:quartz_stairs")
    A.stair_flight(t, 17, 9, 32, 7, "south", "minecraft:quartz_stairs")
    A.stair_flight(t, 17, 16, 32, 7, "south", "minecraft:quartz_stairs")
    A.stair_flight(t, 33, 2, 32, 7, "south", "minecraft:quartz_stairs")
    A.stair_flight(t, 33, 9, 32, 7, "south", "minecraft:quartz_stairs")
    A.stair_flight(t, 33, 16, 32, 7, "south", "minecraft:quartz_stairs")
    for y in (16, 23, 30):
        for x in (16, 22, 30, 36):
            A.window(t, x, y + 2, 13)
            A.window(t, x, y + 2, 39)
        # Projecting balconies wrap alternating elevations and visibly express
        # the residential floor stack.
        t.fill((16, y, 11), (24, y, 14), "minecraft:smooth_quartz_slab", type="bottom", waterlogged="false")
        t.fill((28, y, 38), (36, y, 41), "minecraft:smooth_quartz_slab", type="bottom", waterlogged="false")
        t.fill((11, y, 17), (14, y, 25), "minecraft:smooth_quartz_slab", type="bottom", waterlogged="false")
        t.fill((38, y, 27), (41, y, 35), "minecraft:smooth_quartz_slab", type="bottom", waterlogged="false")
    t.fill((17, 30, 17), (35, 34, 35), "minecraft:white_concrete")
    t.clear((18, 31, 18), (34, 33, 34))
    t.fill((19, 34, 19), (32, 36, 32), "create:framed_glass")
    t.fill((34, 34, 31), (38, 36, 36), "immersiveengineering:sheetmetal_steel")
    return t


def shattered_luxury_condo():
    t = shattered_luxury_condo_clean_master()
    t.clear((26, 20, 5), (50, 36, 31))
    t.fill((29, 1, 8), (50, 10, 33), "minecraft:gravel")
    t.fill((25, 14, 14), (38, 16, 22), "minecraft:white_concrete")
    t.spawner(19, 16, 19, "the_wasteland_reworked:ghoul", count=2, nearby=7)
    t.spawner(12, 2, 34, "minecraft:zombie", count=2, nearby=7)
    return t


def ruined_city_school_clean_master():
    t = site((65, 27, 55), road=(24, 0, 40, 6))
    # Two-storey academic bar, double-height gym and low cafeteria wing form
    # a campus courtyard instead of one monolithic school cube.
    A.shell(t, (5, 1, 7), (59, 20, 31), "minecraft:bricks", "tfmg:factory_floor", "minecraft:smooth_stone")
    A.shell(t, (42, 1, 30), (61, 18, 50), "minecraft:mud_bricks", "minecraft:smooth_stone", "minecraft:weathered_cut_copper")
    A.shell(t, (5, 1, 30), (34, 12, 50), "minecraft:yellow_terracotta", "minecraft:smooth_stone", "minecraft:smooth_stone")
    t.fill((6, 10, 8), (58, 10, 30), "tfmg:factory_floor")
    # Central corridor with four classrooms per floor, admin/library at front.
    for y in (2, 11):
        A.partition_z(t, 18, y, 6, 58, "tfmg:cinder_block", (12, 26, 39, 53))
        A.partition_z(t, 24, y, 6, 58, "tfmg:cinder_block", (12, 26, 39, 53))
        for x in (18, 32, 46):
            A.partition_x(t, x, y, 8, 30, "tfmg:cinder_block", 21)
        for x1 in (7, 20, 34, 48):
            # Teacher wall, student desks, supplies and room-specific sinks.
            A.desk(t, x1 + 1, y, 10)
            t.set(x1 + 8, y, 10, "minecraft:bookshelf")
            for x in range(x1 + 2, min(x1 + 10, 57), 3):
                for z in (14, 17):
                    t.set(x, y, z, "minecraft:spruce_stairs", facing="north", half="bottom", shape="straight", waterlogged="false")
                    t.set(x, y, z + 1, "minecraft:spruce_slab", type="bottom", waterlogged="false")
            t.set(x1 + 9, y, 16, "minecraft:water_cauldron", level="1")
        for x in (11, 24, 38, 52):
            A.window(t, x, y + 3, 7)
            A.window(t, x, y + 3, 31)
    # Main lobby/admin suite and two protected stair cores.
    A.shell(t, (24, 1, 4), (40, 9, 9), "minecraft:smooth_stone", "minecraft:polished_andesite", "minecraft:smooth_stone_slab")
    A.double_door(t, 31, 2, 4, "north", "dark_oak")
    A.double_door(t, 31, 2, 9, "south", "dark_oak")
    A.desk(t, 25, 2, 11)
    t.fill((26, 2, 14), (30, 4, 14), "minecraft:scaffolding")
    A.stair_flight(t, 8, 2, 22, 9, "south", "minecraft:stone_brick_stairs")
    A.stair_flight(t, 54, 2, 22, 9, "south", "minecraft:stone_brick_stairs")
    # Cafeteria/kitchen and stage; gym has court markings, bleachers and stores.
    for x in range(8, 27, 4):
        t.fill((x, 2, 35), (x + 2, 2, 44), "minecraft:spruce_slab", type="bottom", waterlogged="false")
    kitchenette(t, 7, 2, 47, 9)
    t.fill((19, 2, 47), (31, 4, 49), "zvhouses:stone_brick_countertop")
    t.fill((43, 1, 33), (60, 1, 48), "minecraft:orange_terracotta")
    t.fill((50, 2, 36), (52, 2, 45), "minecraft:white_concrete")
    for z in (34, 38, 42, 46):
        t.fill((43, 2, z), (46, 4, z), "minecraft:oak_stairs", facing="east", half="bottom", shape="straight", waterlogged="false")
    t.fill((56, 2, 34), (60, 5, 39), "minecraft:scaffolding")
    A.double_door(t, 47, 2, 50, "south", "iron")
    A.double_door(t, 10, 2, 50, "south", "iron")
    # Entry canopy, clock/sign blade and varied roof plant finish the campus.
    t.fill((20, 9, 3), (44, 9, 9), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
    for x in (20, 44):
        t.fill((x, 1, 4), (x, 8, 4), "minecraft:polished_blackstone_bricks")
    t.fill((29, 20, 12), (35, 26, 17), "minecraft:bricks")
    t.fill((30, 22, 11), (34, 25, 11), "minecraft:white_concrete")
    t.fill((12, 20, 24), (19, 23, 29), "immersiveengineering:sheetmetal_steel")
    # Classroom bay pilasters, gym clerestories and cafeteria loading canopy
    # make each program wing legible from outside.
    for x in (5, 18, 32, 46, 59):
        t.fill((x, 2, 6), (x, 19, 8), "minecraft:mud_bricks")
        t.fill((x, 2, 30), (x, 19, 32), "minecraft:mud_bricks")
    for z in (34, 39, 44):
        A.window(t, 42, 7, z, axis="z")
        A.window(t, 61, 7, z, axis="z")
    for x in (9, 16, 23, 30):
        A.window(t, x, 4, 50)
    t.fill((4, 8, 47), (35, 8, 53), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
    for x in (4, 35):
        t.fill((x, 1, 51), (x, 7, 51), "minecraft:polished_blackstone_bricks")
    return t


def ruined_city_school():
    t = ruined_city_school_clean_master()
    t.clear((43, 13, 28), (64, 26, 54))
    t.fill((44, 1, 31), (64, 7, 54), "minecraft:gravel")
    t.clear((4, 15, 6), (18, 26, 20))
    t.spawner(25, 2, 15, "minecraft:zombie", count=2, nearby=7)
    t.spawner(53, 2, 42, "the_wasteland_reworked:ghoul", count=2, nearby=7)
    return t


def ruined_community_center_clean_master():
    t = site((51, 21, 47), road=(18, 0, 32, 6))
    # L-shaped public wing wraps a taller multipurpose hall.
    A.shell(t, (4, 1, 7), (46, 14, 41), "minecraft:mud_bricks", "tfmg:factory_floor", "minecraft:smooth_stone")
    A.shell(t, (22, 1, 15), (46, 18, 41), "minecraft:bricks", "minecraft:smooth_stone", "minecraft:weathered_cut_copper")
    A.shell(t, (18, 1, 4), (32, 8, 9), "minecraft:smooth_stone", "minecraft:polished_andesite", "minecraft:smooth_stone_slab")
    A.double_door(t, 24, 2, 4, "north", "dark_oak")
    A.double_door(t, 24, 2, 9, "south", "dark_oak")
    # Reception, library/computer room, craft shop, childcare and meeting rooms.
    A.partition_z(t, 16, 2, 5, 21, "tfmg:cinder_block", (9, 16))
    A.partition_z(t, 28, 2, 5, 21, "tfmg:cinder_block", (9, 16))
    A.partition_x(t, 12, 2, 8, 27, "tfmg:cinder_block", 12)
    A.desk(t, 18, 2, 11)
    for x in (6, 9, 14, 17):
        t.fill((x, 2, 19), (x, 4, 24), "minecraft:bookshelf")
    for x in (6, 10, 14, 18):
        t.set(x, 2, 33, "minecraft:crafting_table")
        t.set(x, 2, 36, "minecraft:spruce_slab", type="bottom", waterlogged="false")
    t.fill((6, 2, 29), (11, 2, 31), "minecraft:green_wool")
    t.fill((14, 2, 29), (19, 2, 31), "minecraft:yellow_wool")
    # Hall: stage, seating, equipment store and independent fire exits.
    t.fill((24, 2, 34), (44, 4, 40), "minecraft:dark_oak_planks")
    for x in range(25, 44, 4):
        for z in (20, 24, 28):
            t.set(x, 2, z, "minecraft:dark_oak_stairs", facing="south", half="bottom", shape="straight", waterlogged="false")
    t.fill((39, 2, 16), (44, 5, 19), "minecraft:scaffolding")
    A.double_door(t, 30, 2, 41, "south", "iron")
    A.double_door(t, 46, 2, 25, "east", "iron")
    # Community kitchen, accessible toilets and roof lantern.
    kitchenette(t, 6, 2, 39, 8)
    bathroom(t, 16, 2, 39)
    bathroom(t, 19, 2, 39)
    for x in (7, 14, 36, 43):
        A.window(t, x, 4, 7)
    for z in (12, 22, 34):
        A.window(t, 4, 4, z, axis="z")
        A.window(t, 46, 5, z, axis="z")
    t.fill((27, 18, 21), (40, 20, 34), "create:framed_glass")
    t.fill((12, 14, 33), (18, 17, 39), "immersiveengineering:sheetmetal_steel")
    t.fill((44, 2, 38), (44, 18, 38), "minecraft:ladder", facing="west", waterlogged="false")
    t.set(44, 19, 38, "minecraft:iron_trapdoor", facing="north", half="bottom", open="false", powered="false", waterlogged="false")
    for x in (5, 12, 21, 34, 45):
        t.fill((x, 2, 6), (x, 12, 8), "minecraft:polished_blackstone_bricks")
    for z in (11, 19, 29, 37):
        A.window(t, 4, 5, z, axis="z")
        A.window(t, 46, 6, z, axis="z")
    t.fill((3, 9, 15), (23, 9, 20), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
    t.fill((20, 14, 39), (48, 14, 44), "minecraft:weathered_cut_copper_slab", type="bottom", waterlogged="false")
    return t


def ruined_community_center():
    t = ruined_community_center_clean_master()
    t.clear((3, 9, 25), (22, 20, 46))
    t.fill((4, 1, 27), (23, 6, 46), "minecraft:gravel")
    t.set(24, 2, 28, "the_wasteland_reworked:garbage_bag")
    t.spawner(35, 2, 27, "minecraft:zombie", count=2, nearby=7)
    return t


def decayed_ranch_clean_master():
    t = site((49, 19, 45), road=(0, 0, 15, 7))
    # Ranch house, offset barn, silo and paddock make a working homestead.
    A.shell(t, (4, 1, 7), (23, 11, 25), "the_wasteland_reworked:decayed_planks", "minecraft:spruce_planks", "minecraft:weathered_cut_copper")
    A.gable_roof_x(t, 4, 23, 7, 25, 11, "the_wasteland_reworked:decayed_planks", "minecraft:dark_oak_stairs", "minecraft:stripped_dark_oak_log")
    A.partition_z(t, 16, 2, 5, 22, "minecraft:stripped_spruce_wood", (10, 19))
    A.partition_x(t, 14, 2, 8, 24, "minecraft:stripped_spruce_wood", 20)
    A.door(t, 12, 2, 7, "north", "spruce")
    kitchenette(t, 6, 2, 10, 6)
    sitting_room(t, 16, 2, 10)
    A.bed(t, 6, 2, 22, "north", "brown")
    bathroom(t, 16, 2, 22)
    for x in (7, 18):
        A.window(t, x, 3, 7)
        A.window(t, x, 3, 25)
    # Barn with central threshing aisle, stalls, loft and feed room.
    A.shell(t, (28, 1, 8), (45, 14, 31), "minecraft:stripped_dark_oak_log", "minecraft:coarse_dirt", "minecraft:dark_oak_planks")
    A.gable_roof_x(t, 28, 45, 8, 31, 14, "minecraft:dark_oak_planks", "minecraft:dark_oak_stairs", "minecraft:stripped_dark_oak_log")
    t.clear((34, 2, 8), (39, 8, 8))
    t.clear((34, 2, 31), (39, 8, 31))
    for z in (12, 18, 24):
        t.fill((29, 2, z), (33, 4, z + 3), "minecraft:stripped_oak_log")
        t.fill((40, 2, z), (44, 4, z + 3), "minecraft:stripped_oak_log")
    t.fill((29, 9, 10), (44, 9, 29), "minecraft:spruce_planks")
    t.fill((29, 10, 25), (33, 12, 29), "farmersdelight:straw_bale")
    # Stable full-block paddock perimeter and water/feed stations.
    for x in range(4, 25, 4):
        t.fill((x, 1, 31), (x, 3, 31), "minecraft:stripped_oak_log")
        t.fill((x, 1, 42), (x, 3, 42), "minecraft:stripped_oak_log")
    for z in range(31, 43, 4):
        t.fill((4, 1, z), (4, 3, z), "minecraft:stripped_oak_log")
        t.fill((24, 1, z), (24, 3, z), "minecraft:stripped_oak_log")
    t.fill((6, 2, 34), (9, 2, 36), "minecraft:water_cauldron", level="3")
    t.fill((17, 2, 38), (21, 3, 40), "farmersdelight:straw_bale")
    t.fill((42, 1, 35), (47, 12, 40), "minecraft:light_gray_concrete")
    t.clear((44, 3, 37), (45, 10, 38))
    t.entity(13.5, 2.0, 36.5, "minecraft:cow", PersistenceRequired=1)
    t.entity(19.5, 2.0, 35.5, "minecraft:horse", PersistenceRequired=1)
    return t


def decayed_ranch():
    t = decayed_ranch_clean_master()
    t.clear((37, 9, 6), (48, 18, 33))
    t.fill((38, 1, 9), (48, 6, 34), "minecraft:gravel")
    t.clear((3, 9, 17), (12, 18, 28))
    t.spawner(31, 2, 26, "minecraft:zombie", count=2, nearby=6)
    return t


def roadside_church_cemetery_clean_master():
    t = site((51, 29, 49), road=(18, 0, 32, 6))
    # Cruciform nave/chancel with pitched roof, transepts and bell tower.
    A.shell(t, (16, 1, 8), (34, 15, 40), "minecraft:stone_bricks", "minecraft:dark_oak_planks", "minecraft:dark_oak_planks")
    A.gable_roof_x(t, 16, 34, 8, 40, 15, "minecraft:stone_bricks", "minecraft:dark_oak_stairs", "minecraft:stripped_dark_oak_log")
    A.shell(t, (8, 1, 22), (42, 13, 31), "minecraft:stone_bricks", "minecraft:dark_oak_planks", "minecraft:dark_oak_planks")
    A.gable_roof_x(t, 8, 42, 22, 31, 13, "minecraft:stone_bricks", "minecraft:dark_oak_stairs", "minecraft:stripped_dark_oak_log")
    A.shell(t, (20, 1, 5), (30, 22, 12), "minecraft:stone_bricks", "minecraft:dark_oak_planks", "minecraft:smooth_stone")
    A.double_door(t, 24, 2, 5, "north", "dark_oak")
    t.clear((22, 2, 12), (28, 10, 12))
    # Narthex, nave pews, side chapel, vestry and raised chancel.
    for z in range(15, 31, 4):
        for x in (18, 21, 28, 31):
            t.fill((x, 2, z), (x + 1, 2, z), "minecraft:dark_oak_stairs", facing="south", half="bottom", shape="straight", waterlogged="false")
    t.fill((19, 2, 33), (31, 4, 39), "minecraft:polished_andesite")
    t.set(25, 5, 37, "minecraft:lectern", facing="north", has_book="false", powered="false")
    t.fill((22, 5, 39), (28, 7, 39), "minecraft:gold_block")
    A.partition_x(t, 14, 2, 23, 30, "minecraft:stripped_dark_oak_wood", 27)
    A.partition_x(t, 36, 2, 23, 30, "minecraft:stripped_dark_oak_wood", 27)
    t.set(10, 2, 25, "minecraft:lectern", facing="east", has_book="false", powered="false")
    t.fill((37, 2, 25), (41, 4, 29), "minecraft:scaffolding")
    for z in (15, 22, 31, 37):
        A.window(t, 16, 5, z, axis="z")
        A.window(t, 34, 5, z, axis="z")
    t.fill((24, 22, 7), (26, 27, 9), "minecraft:polished_blackstone_bricks")
    t.set(25, 28, 8, "minecraft:lightning_rod", facing="up", waterlogged="false")
    # Cemetery has family plots, paths, crypt and maintenance shed.
    t.fill((3, 0, 12), (13, 0, 45), "minecraft:coarse_dirt")
    t.fill((38, 0, 12), (48, 0, 45), "minecraft:coarse_dirt")
    for x in (5, 9, 40, 44):
        for z in range(15, 44, 6):
            t.fill((x, 1, z), (x + 1, 3, z), "minecraft:stone_bricks")
            t.set(x, 4, z, "minecraft:chiseled_stone_bricks")
    A.shell(t, (39, 1, 35), (47, 8, 45), "minecraft:mossy_stone_bricks", "minecraft:stone", "minecraft:stone_bricks")
    A.door(t, 43, 2, 35, "north", "iron")
    t.fill((3, 1, 40), (11, 6, 47), "the_wasteland_reworked:decayed_planks")
    t.clear((6, 2, 40), (8, 4, 40))
    return t


def roadside_church_cemetery():
    t = roadside_church_cemetery_clean_master()
    t.clear((27, 12, 27), (43, 28, 48))
    t.fill((29, 1, 29), (45, 7, 48), "minecraft:gravel")
    t.clear((18, 17, 5), (27, 28, 15))
    t.spawner(10, 2, 28, "minecraft:zombie", count=2, nearby=6)
    t.spawner(41, 2, 39, "minecraft:pillager", count=1, nearby=4)
    return t


def ruined_ranger_station_clean_master():
    t = site((43, 19, 41), road=(13, 0, 27, 6))
    # L-shaped public office/residence plus equipment garage and broad porch.
    A.shell(t, (5, 1, 7), (28, 12, 31), "the_wasteland_reworked:decayed_planks", "minecraft:spruce_planks", "minecraft:weathered_cut_copper")
    A.gable_roof_x(t, 5, 28, 7, 31, 12, "the_wasteland_reworked:decayed_planks", "minecraft:dark_oak_stairs", "minecraft:stripped_dark_oak_log")
    A.shell(t, (27, 1, 17), (39, 11, 35), "minecraft:stripped_spruce_log", "minecraft:smooth_stone", "minecraft:dark_oak_planks")
    t.clear((30, 2, 35), (36, 7, 35))
    A.shell(t, (13, 1, 4), (21, 7, 9), "minecraft:stripped_spruce_log", "minecraft:spruce_planks", "minecraft:weathered_cut_copper_slab")
    A.double_door(t, 16, 2, 4, "north", "spruce")
    A.double_door(t, 16, 2, 9, "south", "spruce")
    A.partition_z(t, 16, 2, 6, 27, "minecraft:stripped_spruce_wood", (10, 20))
    A.partition_x(t, 17, 2, 17, 30, "minecraft:stripped_spruce_wood", 21)
    A.desk(t, 7, 2, 10)
    t.fill((20, 2, 10), (26, 5, 14), "minecraft:bookshelf")
    sitting_room(t, 7, 2, 20)
    kitchenette(t, 18, 2, 20, 6)
    A.bed(t, 7, 2, 28, "north", "green")
    bathroom(t, 19, 2, 28)
    t.fill((29, 2, 19), (37, 5, 23), "minecraft:scaffolding")
    t.set(32, 2, 28, "minecraft:crafting_table")
    t.set(35, 2, 28, "minecraft:blast_furnace", facing="north", lit="false")
    for x in (8, 24):
        A.window(t, x, 4, 7)
    for z in (12, 23, 29):
        A.window(t, 5, 4, z, axis="z")
    t.fill((4, 1, 5), (29, 1, 9), "minecraft:spruce_planks")
    t.fill((4, 8, 4), (29, 8, 9), "minecraft:weathered_cut_copper_slab", type="bottom", waterlogged="false")
    for x in (4, 12, 21, 29):
        t.fill((x, 1, 5), (x, 7, 5), "minecraft:stripped_spruce_log", axis="y")
    t.fill((35, 11, 20), (38, 17, 23), "minecraft:polished_blackstone_bricks")
    t.set(36, 16, 19, "the_wasteland_reworked:radio")
    t.chest(36, 2, 21, "infinite_domain:chests/wasteland_roadside")
    return t


def ruined_ranger_station():
    t = ruined_ranger_station_clean_master()
    t.clear((27, 8, 16), (42, 18, 40))
    t.fill((29, 1, 18), (42, 6, 40), "minecraft:gravel")
    t.set(25, 2, 27, "the_wasteland_reworked:garbage_bag")
    t.spawner(9, 2, 27, "minecraft:zombie", count=1, nearby=4)
    return t


def wasteland_fire_lookout_clean_master():
    t = site((35, 35, 35), road=(13, 0, 21, 8))
    # Four heavy timber legs, cross platforms and an enclosed switchback stair
    # produce usable vertical circulation without fence/girder dependencies.
    for x, z in ((9, 9), (25, 9), (9, 25), (25, 25)):
        t.fill((x, 1, z), (x + 2, 27, z + 2), "minecraft:stripped_dark_oak_log", axis="y")
        t.fill((x - 1, 1, z - 1), (x + 3, 2, z + 3), "immersiveengineering:concrete_reinforced")
    for y in (7, 14, 21, 27):
        t.fill((9, y, 9), (27, y, 27), "minecraft:spruce_planks")
        t.clear((12, y, 12), (24, y, 24))
    A.stair_flight(t, 12, 2, 12, 6, "south", "minecraft:oak_stairs")
    A.stair_flight(t, 21, 8, 19, 6, "north", "minecraft:oak_stairs")
    A.stair_flight(t, 12, 14, 12, 7, "south", "minecraft:oak_stairs")
    A.stair_flight(t, 21, 21, 19, 7, "north", "minecraft:oak_stairs")
    # Glazed observation cabin with wraparound deck and operational program.
    A.shell(t, (8, 27, 8), (28, 33, 28), "minecraft:stripped_spruce_log", "minecraft:spruce_planks", "minecraft:dark_oak_planks")
    for x in range(10, 27, 3):
        A.window(t, x, 29, 8)
        A.window(t, x, 29, 28)
    for z in range(11, 26, 3):
        A.window(t, 8, 29, z, axis="z")
        A.window(t, 28, 29, z, axis="z")
    A.door(t, 18, 28, 28, "south", "spruce")
    A.desk(t, 11, 28, 11)
    t.set(14, 28, 11, "the_wasteland_reworked:radio")
    A.bed(t, 23, 28, 23, "north", "green")
    kitchenette(t, 10, 28, 23, 5)
    bathroom(t, 20, 28, 11)
    t.fill((14, 33, 14), (22, 34, 22), "minecraft:weathered_cut_copper_slab", type="bottom", waterlogged="false")
    # Ground tool/weather hut and fuel store support the tower.
    A.shell(t, (2, 1, 12), (8, 8, 23), "minecraft:stripped_spruce_log", "minecraft:smooth_stone", "minecraft:dark_oak_planks")
    A.door(t, 5, 2, 12, "north", "spruce")
    t.fill((3, 2, 17), (7, 5, 21), "minecraft:scaffolding")
    t.set(7, 2, 14, "minecraft:blast_furnace", facing="west", lit="false")
    t.fill((28, 1, 14), (32, 4, 21), "immersiveengineering:sheetmetal_steel")
    return t


def wasteland_fire_lookout():
    t = wasteland_fire_lookout_clean_master()
    t.clear((22, 20, 20), (34, 34, 34))
    t.fill((23, 1, 22), (34, 7, 34), "minecraft:gravel")
    t.fill((21, 15, 19), (28, 17, 24), "minecraft:stripped_dark_oak_log", axis="y")
    t.spawner(5, 2, 18, "minecraft:pillager", count=1, nearby=4)
    return t
