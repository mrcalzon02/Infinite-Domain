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


def storefront(t, x1: int, x2: int, y: int, z: int, facing: str, theme: int) -> None:
    """Glazed shopfront with sales fixtures, fitting/service area and stock."""
    glass_z = z if facing == "north" else z + 10
    back_z = z + 10 if facing == "north" else z
    t.fill((x1, y, glass_z), (x2, y + 5, glass_z), "create:framed_glass")
    door_x = (x1 + x2) // 2
    A.door(t, door_x, y, glass_z, facing, "dark_oak")
    for x in range(x1 + 2, x2 - 1, 3):
        t.fill((x, y, min(z, z + 10) + 2), (x, y + 2, max(z, z + 10) - 2), "minecraft:scaffolding")
    t.fill((x1 + 1, y, back_z), (x2 - 1, y + 2, back_z), "zvhouses:spruce_countertop")
    if theme % 3 == 0:
        t.set(x1 + 2, y, back_z + (1 if facing == "south" else -1), "minecraft:loom", facing="north")
    elif theme % 3 == 1:
        t.set(x1 + 2, y, back_z + (1 if facing == "south" else -1), "minecraft:bookshelf")
    else:
        t.set(x1 + 2, y, back_z + (1 if facing == "south" else -1), "minecraft:crafting_table")


def hotel_room(t, x1: int, x2: int, y: int, z1: int, z2: int, facing: str, color: str) -> None:
    door_z = z2 if facing == "south" else z1
    A.door(t, (x1 + x2) // 2, y, door_z, facing, "spruce")
    A.bed(t, x1 + 1, y, z1 + 2, "north", color)
    t.set(x2 - 1, y, z1 + 2, "minecraft:barrel", facing="up", open="false")
    t.set(x2 - 2, y + 1, z1 + 2, "supplementaries:item_shelf")
    t.set(x1 + 2, y, z2 - 2, "minecraft:spruce_stairs", facing="north", half="bottom", shape="straight", waterlogged="false")
    t.set(x1 + 4, y, z2 - 2, "minecraft:spruce_slab", type="bottom", waterlogged="false")
    t.set(x2 - 2, y, z2 - 2, "minecraft:water_cauldron", level="1")
    t.set(x2 - 1, y, z2 - 2, "minecraft:quartz_stairs", facing="west", half="bottom", shape="straight", waterlogged="false")


def office_suite(t, x1: int, x2: int, y: int, z1: int, z2: int, facing: str) -> None:
    door_z = z2 if facing == "south" else z1
    A.door(t, (x1 + x2) // 2, y, door_z, facing, "dark_oak")
    for x in range(x1 + 1, x2, 4):
        A.desk(t, x, y, z1 + 2)
    t.fill((x1 + 1, y, z2 - 2), (min(x1 + 4, x2 - 1), y + 2, z2 - 2), "minecraft:bookshelf")
    t.set(x2 - 1, y, z1 + 2, "the_wasteland_reworked:radio")


def ruined_shopping_mall_clean_master():
    t = site((73, 28, 63), road=(26, 0, 46, 7))
    # Two unequal anchor stores frame a two-level concourse and central atrium.
    A.shell(t, (3, 1, 9), (22, 22, 56), "minecraft:bricks", "tfmg:factory_floor", "minecraft:smooth_stone")
    A.shell(t, (51, 1, 7), (69, 19, 55), "minecraft:mud_bricks", "tfmg:factory_floor", "minecraft:weathered_cut_copper")
    A.shell(t, (21, 1, 12), (52, 18, 52), "minecraft:smooth_stone", "minecraft:polished_andesite", "minecraft:smooth_stone")
    t.fill((4, 10, 10), (68, 10, 55), "tfmg:factory_floor")
    t.clear((23, 10, 13), (50, 10, 51))
    t.clear((30, 2, 21), (43, 17, 42))
    # Main entry and skylit atrium with paired stairs/escalator analogues.
    A.shell(t, (27, 1, 4), (46, 9, 14), "minecraft:smooth_stone", "minecraft:polished_andesite", "minecraft:smooth_stone_slab")
    A.double_door(t, 35, 2, 4, "north", "dark_oak")
    A.double_door(t, 35, 2, 14, "south", "dark_oak")
    t.fill((28, 18, 18), (45, 22, 45), "create:framed_glass")
    A.stair_flight(t, 25, 2, 22, 8, "south", "minecraft:quartz_stairs")
    A.stair_flight(t, 46, 2, 33, 8, "north", "minecraft:quartz_stairs")
    # Six distinct inline stores per level face the concourse.
    for level, y in enumerate((2, 11)):
        for i, x in enumerate((23, 33, 43)):
            storefront(t, x, x + 8, y, 13, "north", i + level)
            storefront(t, x, x + 8, y, 41, "south", i + level + 3)
    # Anchor departments, food court, management/security and loading spine.
    for y in (2, 11):
        for x in (6, 11, 16, 54, 59, 64):
            t.fill((x, y, 16), (x, y + 3, 47), "minecraft:scaffolding")
    for x, z in ((25, 47), (31, 47), (39, 47), (45, 47)):
        t.set(x, 2, z, "minecraft:smoker", facing="north", lit="false")
        t.fill((x - 1, 2, z + 2), (x + 2, 2, z + 3), "minecraft:spruce_slab", type="bottom", waterlogged="false")
    A.partition_z(t, 50, 2, 4, 68, "tfmg:cinder_block", (10, 20, 36, 57, 65))
    A.partition_x(t, 14, 2, 51, 55, "tfmg:cinder_block", 53)
    A.partition_x(t, 60, 2, 51, 54, "tfmg:cinder_block", 53)
    A.desk(t, 6, 2, 52)
    t.set(11, 2, 52, "the_wasteland_reworked:radio")
    t.fill((55, 2, 52), (66, 5, 54), "minecraft:scaffolding")
    A.double_door(t, 7, 2, 56, "south", "iron")
    A.double_door(t, 61, 2, 55, "south", "iron")
    # Exterior storefront rhythm, anchor signs, service canopies and roof plant.
    for x in (6, 12, 18, 55, 61, 67):
        A.window(t, x, 4, 9 if x < 23 else 7)
    t.fill((20, 8, 5), (53, 8, 12), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
    for x in (20, 53):
        t.fill((x, 1, 6), (x, 7, 6), "minecraft:polished_blackstone_bricks")
    t.fill((5, 22, 20), (18, 27, 36), "minecraft:bricks")
    t.fill((55, 19, 21), (66, 24, 35), "minecraft:mud_bricks")
    t.fill((30, 18, 48), (42, 21, 55), "immersiveengineering:sheetmetal_steel")
    return t


def ruined_shopping_mall():
    t = ruined_shopping_mall_clean_master()
    t.clear((46, 12, 3), (72, 27, 37))
    t.fill((49, 1, 7), (72, 10, 39), "minecraft:gravel")
    t.clear((28, 15, 34), (45, 27, 58))
    t.spawner(35, 2, 31, "minecraft:zombie", count=3, nearby=9)
    t.spawner(12, 11, 32, "minecraft:pillager", count=2, nearby=7)
    return t


def ruined_department_store_clean_master():
    t = site((59, 31, 51), road=(19, 0, 39, 6))
    A.shell(t, (4, 1, 7), (54, 25, 46), "minecraft:bricks", "tfmg:factory_floor", "minecraft:smooth_stone")
    for y in (9, 17):
        t.fill((5, y, 8), (53, y, 45), "tfmg:factory_floor")
    # Grand central entrance/void and two stairs divide floor departments.
    A.shell(t, (19, 1, 4), (39, 10, 9), "minecraft:smooth_stone", "minecraft:polished_andesite", "minecraft:smooth_stone_slab")
    A.double_door(t, 28, 2, 4, "north", "dark_oak")
    A.double_door(t, 28, 2, 9, "south", "dark_oak")
    t.clear((23, 2, 13), (35, 23, 25))
    A.stair_flight(t, 8, 2, 32, 7, "south", "minecraft:quartz_stairs")
    A.stair_flight(t, 8, 10, 32, 7, "south", "minecraft:quartz_stairs")
    A.stair_flight(t, 45, 2, 32, 7, "south", "minecraft:quartz_stairs")
    A.stair_flight(t, 45, 10, 32, 7, "south", "minecraft:quartz_stairs")
    # Clothing, housewares, furniture, electronics, cosmetics and offices.
    for y in (2, 10, 18):
        for x in (7, 13, 39, 47):
            t.fill((x, y, 13), (x + 2, y + 3, 31), "minecraft:scaffolding")
        for x in (9, 17, 39, 47):
            t.fill((x, y, 35), (x + 4, y, 40), "minecraft:spruce_planks")
            t.set(x + 1, y + 1, 37, "minecraft:loom", facing="north")
    t.fill((7, 2, 10), (19, 2, 10), "zvhouses:spruce_countertop")
    t.fill((39, 2, 10), (51, 2, 10), "zvhouses:spruce_countertop")
    # Rear stockrooms, freight receiving and staff offices on every level.
    for y in (2, 10, 18):
        A.partition_z(t, 41, y, 5, 53, "tfmg:cinder_block", (11, 28, 46))
        t.fill((7, y, 43), (20, y + 3, 45), "minecraft:scaffolding")
        A.desk(t, 38, y, 43)
    A.double_door(t, 10, 2, 46, "south", "iron")
    t.fill((5, 8, 44), (24, 8, 50), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
    for x in (5, 24):
        t.fill((x, 1, 49), (x, 7, 49), "minecraft:polished_blackstone_bricks")
    # Facade bays, cornices, sign tower and rooftop service penthouse.
    for y in (4, 12, 20):
        for x in (7, 14, 22, 36, 44, 51):
            A.window(t, x, y, 7)
    for x in (4, 15, 29, 43, 54):
        t.fill((x, 2, 6), (x, 24, 8), "minecraft:mud_bricks")
    for y in (9, 17, 25):
        t.fill((3, y, 6), (55, y, 8), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
    t.fill((24, 25, 18), (34, 30, 29), "immersiveengineering:sheetmetal_steel")
    t.fill((19, 18, 5), (39, 24, 7), "minecraft:red_terracotta")
    t.set(41, 2, 43, "the_wasteland_reworked:radio")
    t.set(48, 2, 43, "minecraft:barrel", facing="up", open="false")
    t.chest(18, 2, 44, "infinite_domain:chests/wasteland_market", "south")
    return t


def ruined_department_store():
    t = ruined_department_store_clean_master()
    t.clear((2, 15, 28), (25, 30, 50))
    t.fill((4, 1, 30), (26, 9, 50), "minecraft:gravel")
    t.clear((37, 22, 4), (58, 30, 23))
    t.spawner(29, 10, 34, "the_wasteland_reworked:ghoul", count=2, nearby=7)
    t.spawner(45, 2, 43, "minecraft:zombie", count=2, nearby=7)
    return t


def bombed_hotel_clean_master():
    t = site((53, 39, 47), road=(17, 0, 35, 6))
    # Two-storey public/service podium and five-storey guest tower.
    A.shell(t, (4, 1, 7), (48, 14, 41), "minecraft:bricks", "minecraft:polished_andesite", "minecraft:smooth_stone")
    A.shell(t, (11, 13, 12), (42, 36, 38), "minecraft:light_gray_concrete", "minecraft:spruce_planks", "minecraft:smooth_stone")
    for y in (20, 27):
        t.fill((12, y, 13), (41, y, 37), "minecraft:spruce_planks")
    # Lobby, reception, lounge/restaurant, kitchen, offices and laundry.
    A.shell(t, (17, 1, 4), (35, 9, 9), "minecraft:smooth_stone", "minecraft:polished_andesite", "minecraft:smooth_stone_slab")
    A.double_door(t, 25, 2, 4, "north", "dark_oak")
    A.double_door(t, 25, 2, 9, "south", "dark_oak")
    A.desk(t, 13, 2, 11)
    t.fill((8, 2, 18), (20, 2, 26), "minecraft:dark_oak_planks")
    for x in (9, 13, 17):
        for z in (19, 23):
            t.set(x, 2, z, "minecraft:dark_oak_stairs", facing="south", half="bottom", shape="straight", waterlogged="false")
    t.fill((25, 2, 17), (44, 2, 17), "zvhouses:stone_brick_countertop")
    t.set(27, 2, 19, "farmersdelight:stove", facing="north", lit="false")
    t.set(31, 2, 19, "minecraft:smoker", facing="north", lit="false")
    t.set(35, 2, 19, "minecraft:water_cauldron", level="2")
    A.partition_z(t, 29, 2, 5, 47, "tfmg:cinder_block", (10, 20, 32, 43))
    t.fill((6, 2, 33), (18, 5, 39), "minecraft:scaffolding")
    t.fill((31, 2, 33), (45, 4, 39), "minecraft:white_wool")
    A.desk(t, 21, 2, 33)
    A.double_door(t, 8, 2, 41, "south", "iron")
    # Central guest corridor; sixteen complete rooms over three rendered floors.
    for y in (14, 21, 28):
        t.clear((25, y, 13), (28, y + 4, 37))
        for i, x in enumerate((12, 20, 29, 37)):
            hotel_room(t, x, x + 5, y, 13, 24, "south", "white" if i % 2 else "gray")
            hotel_room(t, x, x + 5, y, 27, 38, "north", "brown" if i % 2 else "gray")
    # Two protected stairs, service lift core, balconies and rooftop plant.
    for start_y in (2, 9, 16, 23):
        A.stair_flight(t, 7, start_y, 31, 7, "south", "minecraft:stone_brick_stairs")
        A.stair_flight(t, 39, start_y, 31, 7, "south", "minecraft:stone_brick_stairs")
    t.fill((24, 2, 31), (29, 34, 36), "minecraft:polished_blackstone_bricks")
    for y in (14, 21, 28):
        t.fill((14, y, 10), (22, y, 13), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
        t.fill((31, y, 37), (39, y, 40), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
        for x in (14, 21, 32, 39):
            A.window(t, x, y + 2, 12)
            A.window(t, x, y + 2, 38)
    t.fill((16, 36, 17), (25, 38, 26), "create:framed_glass")
    t.fill((30, 36, 27), (40, 38, 36), "immersiveengineering:sheetmetal_steel")
    return t


def bombed_hotel():
    t = bombed_hotel_clean_master()
    t.clear((29, 20, 3), (52, 38, 31))
    t.fill((31, 1, 8), (52, 11, 33), "minecraft:gravel")
    t.clear((3, 9, 27), (18, 23, 46))
    t.spawner(18, 14, 19, "minecraft:zombie", count=2, nearby=7)
    t.spawner(12, 2, 35, "minecraft:pillager", count=2, nearby=7)
    return t


def buried_bank_vault_clean_master():
    t = site((49, 31, 45), road=(15, 0, 33, 6))
    # Surface bank is lifted eight levels; the armored vault and service tunnel
    # occupy an excavated underground cell beneath the public banking hall.
    A.shell(t, (5, 8, 7), (43, 22, 39), "minecraft:stone_bricks", "minecraft:polished_andesite", "minecraft:smooth_stone")
    A.shell(t, (15, 8, 4), (33, 16, 9), "minecraft:smooth_quartz", "minecraft:polished_andesite", "minecraft:smooth_stone_slab")
    A.double_door(t, 23, 9, 4, "north", "iron")
    A.double_door(t, 23, 9, 9, "south", "iron")
    # Teller hall, offices, records, security and staff service corridor.
    t.fill((10, 9, 16), (38, 9, 16), "zvhouses:stone_brick_countertop")
    for x in range(12, 38, 5):
        t.set(x, 10, 16, "minecraft:iron_trapdoor", facing="north", half="top", open="false", powered="false", waterlogged="false")
    A.partition_z(t, 27, 9, 6, 42, "tfmg:cinder_block", (11, 19, 29, 37))
    for x in (15, 25, 35):
        A.partition_x(t, x, 9, 28, 38, "tfmg:cinder_block", 31)
    A.desk(t, 8, 9, 30)
    A.desk(t, 18, 9, 30)
    t.fill((27, 9, 30), (33, 12, 36), "minecraft:bookshelf")
    t.fill((37, 9, 30), (41, 12, 36), "minecraft:scaffolding")
    A.double_door(t, 8, 9, 39, "south", "iron")
    for x in (8, 15, 34, 41):
        A.window(t, x, 11, 7)
    # Secure stair descends to sally corridor, vault, deposit cages and tunnel.
    A.stair_flight(t, 37, 2, 24, 7, "south", "minecraft:stone_brick_stairs")
    t.clear((7, 1, 10), (41, 7, 38))
    t.fill((7, 1, 10), (41, 1, 38), "immersiveengineering:concrete_reinforced")
    for x in range(7, 42):
        t.fill((x, 2, 10), (x, 7, 10), "immersiveengineering:concrete_reinforced")
        t.fill((x, 2, 38), (x, 7, 38), "immersiveengineering:concrete_reinforced")
    for z in range(11, 38):
        t.fill((7, 2, z), (7, 7, z), "immersiveengineering:concrete_reinforced")
        t.fill((41, 2, z), (41, 7, z), "immersiveengineering:concrete_reinforced")
    t.fill((7, 7, 10), (41, 7, 38), "immersiveengineering:concrete_reinforced")
    # Central armored vault with two-door vestibule and three content zones.
    A.shell(t, (14, 1, 15), (34, 7, 33), "immersiveengineering:sheetmetal_steel", "minecraft:polished_blackstone", "immersiveengineering:sheetmetal_steel")
    A.double_door(t, 23, 2, 15, "north", "iron")
    A.partition_z(t, 21, 2, 15, 33, "immersiveengineering:sheetmetal_steel", (23,))
    for x in (16, 20, 27, 31):
        t.fill((x, 2, 24), (x + 1, 5, 31), "minecraft:scaffolding")
    t.chest(29, 2, 29, "infinite_domain:chests/wasteland_market")
    t.fill((8, 2, 18), (12, 5, 34), "minecraft:oxidized_copper_grate")
    t.fill((36, 2, 18), (40, 5, 34), "minecraft:oxidized_copper_grate")
    t.clear((0, 2, 22), (13, 6, 27))
    t.fill((0, 1, 21), (14, 1, 28), "immersiveengineering:concrete_reinforced")
    t.fill((0, 7, 21), (14, 7, 28), "immersiveengineering:concrete_reinforced")
    # Monumental facade, columns, cornice and roof lantern.
    for x in (8, 14, 34, 40):
        t.fill((x, 8, 5), (x + 1, 20, 7), "minecraft:smooth_quartz")
    t.fill((4, 21, 5), (44, 23, 9), "minecraft:smooth_quartz")
    t.fill((17, 22, 17), (31, 30, 29), "create:framed_glass")
    # Reapply the protected stair after excavating and lining the underground
    # cell so the public/service floors retain a traversable vault connection.
    A.stair_flight(t, 37, 2, 24, 7, "south", "minecraft:stone_brick_stairs")
    return t


def buried_bank_vault():
    t = buried_bank_vault_clean_master()
    t.clear((31, 17, 4), (48, 30, 29))
    t.fill((33, 8, 7), (48, 14, 31), "minecraft:gravel")
    t.clear((7, 5, 26), (16, 12, 44))
    t.spawner(24, 2, 25, "minecraft:pillager", count=3, nearby=8)
    return t


def ruined_office_tower_clean_master():
    t = site((51, 47, 47), road=(17, 0, 33, 6))
    # Two-storey podium and six-level setback office slab.
    A.shell(t, (4, 1, 7), (46, 14, 41), "minecraft:polished_blackstone_bricks", "tfmg:factory_floor", "minecraft:smooth_stone")
    A.shell(t, (10, 13, 11), (40, 42, 37), "minecraft:light_gray_concrete", "tfmg:factory_floor", "minecraft:smooth_stone")
    for y in (20, 27, 34):
        t.fill((11, y, 12), (39, y, 36), "tfmg:factory_floor")
    # Lobby/security, public conference center, cafeteria and service dock.
    A.shell(t, (17, 1, 4), (33, 9, 9), "minecraft:smooth_stone", "minecraft:polished_andesite", "minecraft:smooth_stone_slab")
    A.double_door(t, 24, 2, 4, "north", "dark_oak")
    A.double_door(t, 24, 2, 9, "south", "dark_oak")
    A.desk(t, 14, 2, 11)
    t.set(19, 2, 11, "the_wasteland_reworked:radio")
    for x in (7, 15, 31, 39):
        t.fill((x, 2, 20), (x + 5, 2, 27), "minecraft:dark_oak_planks")
        t.set(x + 2, 2, 23, "minecraft:lectern", facing="north", has_book="false", powered="false")
    t.fill((7, 2, 33), (20, 2, 39), "zvhouses:stone_brick_countertop")
    t.set(9, 2, 35, "minecraft:smoker", facing="north", lit="false")
    t.fill((32, 2, 33), (44, 5, 39), "minecraft:scaffolding")
    A.double_door(t, 37, 2, 41, "south", "iron")
    # Four suites and central core on each office level.
    for y in (14, 21, 28, 35):
        t.clear((23, y, 12), (27, y + 5, 36))
        office_suite(t, 11, 22, y, 12, 23, "south")
        office_suite(t, 28, 39, y, 12, 23, "south")
        office_suite(t, 11, 22, y, 25, 36, "north")
        office_suite(t, 28, 39, y, 25, 36, "north")
    # Twin stairs and a solid service/elevator core.
    for start_y in (2, 9, 16, 23, 30):
        A.stair_flight(t, 7, start_y, 29, 7, "south", "minecraft:stone_brick_stairs")
        A.stair_flight(t, 37, start_y, 29, 7, "south", "minecraft:stone_brick_stairs")
    t.fill((23, 2, 25), (27, 41, 31), "minecraft:polished_blackstone_bricks")
    # Curtain-wall bays, sunshades, rooftop boardroom and mechanical plant.
    for y in (16, 23, 30, 37):
        for x in (13, 19, 31, 37):
            A.window(t, x, y, 11)
            A.window(t, x, y, 37)
        t.fill((12, y - 1, 9), (22, y - 1, 12), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
        t.fill((28, y - 1, 36), (38, y - 1, 39), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
    t.fill((14, 42, 14), (27, 46, 26), "create:framed_glass")
    t.fill((30, 42, 27), (39, 46, 36), "immersiveengineering:sheetmetal_steel")
    return t


def ruined_office_tower():
    t = ruined_office_tower_clean_master()
    t.clear((27, 25, 5), (50, 46, 32))
    t.fill((29, 1, 8), (50, 14, 34), "minecraft:gravel")
    t.clear((3, 10, 28), (17, 26, 46))
    t.spawner(17, 21, 19, "minecraft:zombie", count=2, nearby=7)
    t.spawner(15, 2, 34, "minecraft:pillager", count=2, nearby=7)
    return t
