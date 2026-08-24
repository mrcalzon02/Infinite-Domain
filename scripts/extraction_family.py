from __future__ import annotations

from typing import Any

A: Any = None


def configure(api: Any) -> None:
    global A
    A = api


def rim_road(t, y, x1, x2, z1=1, z2=7):
    t.fill((x1, y, z1), (x2, y, z2), "tfmg:asphalt")
    for x in range(x1 + 2, x2, 7):
        t.set(x, y + 1, (z1 + z2) // 2, "minecraft:yellow_concrete")


def abandoned_quarry_clean_master():
    t = A.Template((69, 30, 61))
    surface = 12
    rim_road(t, surface, 4, 64)
    # A three-bench stone excavation. Explicit air below template surface cuts
    # into the projected terrain instead of placing a decorative bowl on top.
    t.clear((18, 10, 18), (62, 22, 55))
    t.fill((18, 9, 18), (62, 9, 55), "minecraft:stone")
    t.clear((24, 7, 23), (57, 22, 51))
    t.fill((24, 6, 23), (57, 6, 51), "minecraft:andesite")
    t.clear((32, 3, 29), (51, 22, 45))
    t.fill((32, 2, 29), (51, 2, 45), "minecraft:tuff")
    # Broken-rhythm ledges and a switchback haul ramp connect every bench.
    t.fill((18, 10, 18), (23, 12, 55), "minecraft:stone")
    t.fill((24, 7, 46), (57, 9, 51), "minecraft:andesite")
    t.fill((32, 3, 29), (37, 6, 45), "minecraft:tuff")
    for step in range(8):
        t.fill((18 + step * 3, 11 - step // 3, 18 + step * 4), (25 + step * 3, 12 - step // 3, 23 + step * 4), "minecraft:gravel")
    # Rim crusher/sort line and covered maintenance/dispatch building.
    t.fill((48, 13, 8), (61, 14, 17), "minecraft:smooth_stone")
    for x in (50, 55, 60):
        t.set(x, 15, 12, "create:mechanical_drill", facing="down")
        t.fill((x, 13, 15), (x, 15, 24), "minecraft:polished_blackstone")
    A.shell(t, (4, 13, 15), (17, 23, 31), "minecraft:bricks", "tfmg:factory_floor", "minecraft:weathered_cut_copper")
    A.gable_roof_x(t, 4, 17, 15, 31, 23, "minecraft:bricks", "minecraft:weathered_cut_copper_stairs", "minecraft:weathered_cut_copper")
    A.door(t, 9, 14, 15, "north", "iron")
    A.door(t, 14, 14, 31, "south", "iron")
    A.window(t, 4, 17, 21, axis="z")
    A.window(t, 17, 17, 21, axis="z")
    A.desk(t, 6, 14, 19)
    t.set(14, 14, 19, "the_wasteland_reworked:radio")
    t.fill((6, 14, 25), (14, 17, 28), "minecraft:scaffolding")
    # Survey mast and bench loading rails.
    t.fill((63, 13, 46), (65, 27, 48), "minecraft:stripped_dark_oak_log", axis="y")
    t.fill((58, 26, 47), (65, 28, 47), "minecraft:dark_oak_planks")
    for x in range(17, 55):
        t.set(x, 7, 48, "minecraft:rail", shape="east_west", waterlogged="false")
    return t


def abandoned_quarry():
    t = abandoned_quarry_clean_master()
    t.clear((47, 14, 7), (67, 29, 26))
    t.fill((47, 10, 11), (62, 12, 24), "minecraft:gravel")
    t.fill((52, 7, 18), (62, 9, 30), "minecraft:gravel")
    t.spawner(12, 14, 24, "minecraft:pillager", count=2, nearby=7)
    return t


def collapsed_mine_entrance_clean_master():
    t = A.Template((55, 27, 49))
    surface = 8
    rim_road(t, surface, 8, 46)
    # Two-level timbered drift descending south from a surface portal.
    t.clear((21, 2, 10), (33, 15, 46))
    for z in range(12, 45, 5):
        floor_y = max(2, 7 - (z - 12) // 10)
        t.fill((22, floor_y, z), (22, floor_y + 6, z), "minecraft:stripped_dark_oak_log", axis="y")
        t.fill((32, floor_y, z), (32, floor_y + 6, z), "minecraft:stripped_dark_oak_log", axis="y")
        t.fill((22, floor_y + 6, z), (32, floor_y + 6, z), "minecraft:stripped_dark_oak_log", axis="x")
        t.fill((23, floor_y - 1, z - 2), (31, floor_y - 1, z + 2), "minecraft:deepslate")
        for x in range(24, 31):
            t.set(x, floor_y, z, "minecraft:rail", shape="north_south", waterlogged="false")
        t.set(27, floor_y + 5, z, "minecraft:lantern", hanging="true", waterlogged="false")
    # Portal headframe, hoist house, ore bins and worker change room.
    for x in (20, 34):
        t.fill((x, 9, 9), (x, 23, 9), "minecraft:stripped_dark_oak_log", axis="y")
    t.fill((20, 22, 9), (34, 24, 9), "minecraft:dark_oak_planks")
    t.fill((25, 10, 9), (29, 22, 9), "minecraft:chain")
    A.shell(t, (4, 9, 14), (18, 19, 31), "minecraft:bricks", "tfmg:factory_floor", "minecraft:weathered_cut_copper")
    A.door(t, 9, 10, 14, "north", "iron")
    A.door(t, 15, 10, 31, "south", "iron")
    A.window(t, 4, 13, 20, axis="z")
    A.desk(t, 6, 10, 18)
    t.set(14, 10, 18, "the_wasteland_reworked:radio")
    t.fill((6, 10, 24), (15, 13, 28), "minecraft:scaffolding")
    for x in (38, 44, 50):
        t.fill((x, 9, 16), (x + 3, 16, 23), "minecraft:dark_oak_planks")
        t.clear((x + 1, 11, 17), (x + 2, 15, 22))
    return t


def collapsed_mine_entrance():
    t = collapsed_mine_entrance_clean_master()
    t.clear((17, 14, 7), (38, 26, 21))
    t.fill((19, 7, 9), (36, 11, 19), "minecraft:gravel")
    t.fill((23, 4, 16), (33, 8, 25), "minecraft:cobbled_deepslate")
    t.spawner(11, 10, 25, "minecraft:pillager", count=2, nearby=7)
    return t


def excavator_pit_clean_master():
    t = A.Template((73, 31, 63))
    surface = 10
    rim_road(t, surface, 5, 68)
    # Long strip-mine benches differ from the quarry's compact stone bowl.
    t.clear((19, 8, 12), (67, 22, 57))
    t.fill((19, 7, 12), (67, 7, 57), "minecraft:dirt")
    t.clear((25, 5, 18), (67, 22, 52))
    t.fill((25, 4, 18), (67, 4, 52), "minecraft:coarse_dirt")
    t.clear((31, 2, 25), (67, 22, 46))
    t.fill((31, 1, 25), (67, 1, 46), "minecraft:deepslate")
    t.fill((19, 8, 12), (24, 10, 57), "minecraft:dirt")
    t.fill((25, 5, 18), (30, 7, 52), "minecraft:coarse_dirt")
    # Bucket-wheel excavator: tracked base, machinery deck, wheel and boom.
    t.fill((18, 8, 19), (39, 10, 29), "minecraft:black_concrete")
    t.fill((21, 11, 21), (31, 17, 27), "minecraft:yellow_concrete")
    t.clear((23, 13, 21), (29, 16, 22))
    t.fill((30, 13, 21), (37, 20, 27), "create:framed_glass")
    t.fill((31, 13, 22), (36, 17, 26), "minecraft:air")
    # Open trussed boom climbs toward a bucket wheel instead of using a solid beam.
    for x in range(36, 59):
        y = 16 + (x - 36) // 8
        t.set(x, y, 23, "minecraft:yellow_concrete")
        t.set(x, y + 3, 25, "minecraft:yellow_concrete")
        if (x - 36) % 4 == 0:
            t.fill((x, y, 23), (x, y + 3, 25), "minecraft:yellow_concrete")
    wheel_y, wheel_z = 17, 24
    for dy in range(-6, 7):
        for dz in range(-6, 7):
            d2 = dy * dy + dz * dz
            if 24 <= d2 <= 40:
                t.set(59, wheel_y + dy, wheel_z + dz, "minecraft:yellow_concrete")
    for dy, dz in ((-7, 0), (7, 0), (0, -7), (0, 7), (-5, -5), (5, 5), (-5, 5), (5, -5)):
        t.fill((58, wheel_y + dy, wheel_z + dz), (60, wheel_y + dy, wheel_z + dz), "minecraft:black_concrete")
    # Conveyor climbs to a distinct rim loading tower and truck pad.
    for x in range(31, 66):
        y = 12 + (x - 31) // 8
        t.fill((x, y, 31), (x, y + 1, 34), "minecraft:polished_blackstone")
    t.fill((61, 11, 29), (68, 23, 38), "minecraft:yellow_concrete")
    t.clear((63, 13, 31), (66, 21, 36))
    A.shell(t, (4, 11, 40), (17, 21, 56), "minecraft:bricks", "tfmg:factory_floor", "minecraft:smooth_stone")
    A.door(t, 9, 12, 40, "north", "iron")
    A.window(t, 4, 15, 46, axis="z")
    A.desk(t, 6, 12, 44)
    t.set(14, 12, 44, "the_wasteland_reworked:radio")
    # Authored rock footings. The bucket-wheel machine, the loading tower and
    # the rim office all sat on benches or floors that were never actually
    # tied down to the pit's own lowest solid layer (y=1) — each was its own
    # large floating island, not a single 5-block gap. Rather than a floating
    # bench with nothing under it, each gets a real support pillar standing
    # in the excavated pit, the way a working quarry leaves rock pillars to
    # carry a bench or platform above open ground.
    t.fill((19, 1, 20), (20, 6, 23), "minecraft:stone")
    t.fill((63, 1, 32), (64, 10, 33), "minecraft:stone")
    t.fill((9, 1, 48), (10, 10, 49), "minecraft:stone")
    # The rim road itself (rim_road()'s asphalt surface) is a flat plane at
    # the surface height with nothing under it in the template either;
    # give it a few footings too rather than leaving it floating end to end.
    for px in (10, 30, 50, 65):
        t.fill((px, 1, 3), (px + 1, 9, 4), "minecraft:stone")
    return t


def excavator_pit():
    t = excavator_pit_clean_master()
    t.clear((47, 15, 16), (72, 30, 42))
    t.fill((48, 8, 20), (58, 10, 32), "minecraft:gravel")
    t.fill((55, 5, 26), (66, 8, 40), "minecraft:coarse_dirt")
    t.fill((63, 2, 34), (72, 5, 45), "minecraft:gravel")
    t.spawner(10, 12, 49, "minecraft:pillager", count=2, nearby=7)
    return t


def abandoned_oil_field_clean_master():
    t = A.Template((75, 25, 61))
    A.roadside_apron(t, road=(5, 0, 69, 7))

    def pumpjack(cx, cz):
        t.fill((cx - 4, 1, cz - 3), (cx + 4, 2, cz + 3), "minecraft:smooth_stone")
        t.fill((cx - 2, 3, cz - 1), (cx + 2, 7, cz + 1), "minecraft:yellow_concrete")
        t.fill((cx, 8, cz), (cx, 16, cz), "minecraft:polished_blackstone")
        t.fill((cx - 7, 14, cz), (cx + 6, 16, cz), "minecraft:yellow_concrete")
        t.fill((cx + 5, 10, cz), (cx + 7, 14, cz), "minecraft:polished_blackstone")
        t.fill((cx - 7, 11, cz), (cx - 5, 14, cz), "minecraft:black_concrete")

    for center in ((14, 18), (37, 17), (59, 20), (23, 43), (50, 44)):
        pumpjack(*center)
    # Separator plant and circular-ish three-tank battery.
    t.fill((58, 1, 35), (70, 2, 55), "minecraft:smooth_stone")
    for cx, cz in ((61, 41), (67, 41), (64, 50)):
        for y in range(3, 12):
            for dx, dz in ((-2, -1), (-2, 0), (-2, 1), (2, -1), (2, 0), (2, 1), (-1, -2), (0, -2), (1, -2), (-1, 2), (0, 2), (1, 2)):
                t.set(cx + dx, y, cz + dz, "immersiveengineering:sheetmetal_steel")
        t.fill((cx - 1, 3, cz - 1), (cx + 1, 3, cz + 1), "immersiveengineering:sheetmetal_steel")
        t.fill((cx - 2, 12, cz - 2), (cx + 2, 12, cz + 2), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
    t.fill((54, 2, 33), (57, 9, 37), "tfmg:steel_block")
    t.fill((54, 10, 34), (70, 11, 36), "minecraft:polished_blackstone")
    # Maintenance/control cabin and spill berm.
    A.shell(t, (4, 1, 34), (17, 11, 54), "minecraft:bricks", "tfmg:factory_floor", "minecraft:weathered_cut_copper")
    A.door(t, 9, 2, 34, "north", "iron")
    A.door(t, 14, 2, 54, "south", "iron")
    A.window(t, 4, 5, 42, axis="z")
    A.desk(t, 6, 2, 38)
    t.set(14, 2, 38, "the_wasteland_reworked:radio")
    t.fill((6, 2, 46), (15, 5, 51), "minecraft:scaffolding")
    t.fill((55, 1, 32), (72, 2, 32), "minecraft:bricks")
    t.fill((72, 1, 32), (72, 2, 57), "minecraft:bricks")
    t.fill((55, 1, 57), (72, 2, 57), "minecraft:bricks")
    return t


def abandoned_oil_field():
    t = abandoned_oil_field_clean_master()
    t.clear((43, 12, 35), (74, 24, 60))
    t.fill((47, 1, 38), (69, 2, 56), "minecraft:black_concrete")
    t.fill((55, 3, 43), (70, 5, 55), "minecraft:gravel")
    t.spawner(11, 2, 48, "minecraft:pillager", count=2, nearby=7)
    return t
