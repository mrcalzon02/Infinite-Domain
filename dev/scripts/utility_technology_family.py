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


def round_tank(t, cx, base, cz, radius, height, wall="immersiveengineering:sheetmetal_steel"):
    for y in range(base, base + height):
        for dx in range(-radius, radius + 1):
            for dz in range(-radius, radius + 1):
                d2 = dx * dx + dz * dz
                if d2 <= radius * radius and (y == base or d2 >= (radius - 1) * (radius - 1)):
                    t.set(cx + dx, y, cz + dz, wall)
    for rise, roof_radius in enumerate(range(radius, 0, -1)):
        y = base + height + rise
        for dx in range(-roof_radius, roof_radius + 1):
            for dz in range(-roof_radius, roof_radius + 1):
                if dx * dx + dz * dz <= roof_radius * roof_radius:
                    t.set(cx + dx, y, cz + dz, "minecraft:smooth_stone")


def chimney(t, x, z, base, top, block="minecraft:bricks"):
    t.fill((x, base, z), (x + 4, top, z + 4), block)
    t.clear((x + 1, base + 1, z + 1), (x + 3, top, z + 3))
    t.fill((x - 1, top - 2, z - 1), (x + 5, top, z + 5), "minecraft:polished_blackstone")
    t.clear((x, top - 1, z), (x + 4, top, z + 4))


def transformer_bank(t, x, y, z, count=3):
    for index in range(count):
        tx = x + index * 6
        t.fill((tx, y, z), (tx + 3, y + 1, z + 4), "minecraft:smooth_stone")
        t.fill((tx + 1, y + 2, z + 1), (tx + 2, y + 5, z + 3), "minecraft:oxidized_copper")
        t.set(tx + 1, y + 6, z + 1, "immersiveengineering:coil_hv")
        t.set(tx + 2, y + 6, z + 3, "immersiveengineering:coil_hv")


def industrial_facility_clean_master():
    t = site((69, 29, 57), road=(4, 0, 64, 7))
    # Receiving hall -> preparation -> process hall -> inspection/packing -> dispatch.
    A.shell(t, (4, 1, 12), (23, 15, 43), "minecraft:bricks", "tfmg:factory_floor", "minecraft:smooth_stone")
    A.gable_roof_x(t, 4, 23, 12, 43, 15, "minecraft:bricks", "minecraft:weathered_cut_copper_stairs", "minecraft:weathered_cut_copper")
    A.shell(t, (22, 1, 9), (50, 20, 48), "immersiveengineering:sheetmetal_steel", "tfmg:factory_floor", "minecraft:weathered_cut_copper")
    A.shell(t, (49, 1, 13), (65, 13, 35), "minecraft:bricks", "minecraft:smooth_stone", "minecraft:smooth_stone")
    t.clear((22, 2, 18), (23, 8, 36)); t.clear((49, 2, 18), (50, 8, 32))
    for x in (8, 15): A.double_door(t, x, 2, 12, "north", "iron")
    A.double_door(t, 56, 2, 13, "north", "iron")
    A.partition_z(t, 28, 2, 23, 49, "tfmg:cinder_block", (28, 37, 45))
    A.partition_z(t, 39, 2, 23, 49, "tfmg:cinder_block", (28, 37, 45))
    # Receiving pallets and progressive process cells.
    t.fill((6, 2, 18), (19, 5, 28), "jaffabricate:pallet_full")
    for x in (26, 32, 38, 44):
        t.fill((x, 2, 14), (x + 2, 7, 18), "create:fluid_tank")
        t.set(x + 1, 8, 16, "create:mechanical_mixer")
        t.set(x + 1, 2, 32, "create:mechanical_press")
        t.fill((x, 2, 41), (x + 2, 5, 45), "minecraft:scaffolding")
    A.desk(t, 52, 2, 17); t.set(62, 2, 17, "the_wasteland_reworked:radio")
    A.partition_z(t, 24, 2, 50, 64, "tfmg:cinder_block", (54, 60))
    t.fill((52, 2, 27), (63, 5, 32), "minecraft:scaffolding")
    A.stair_flight(t, 51, 2, 20, 9, "south", "minecraft:stone_brick_stairs")
    t.fill((51, 11, 15), (63, 12, 33), "minecraft:smooth_stone")
    A.desk(t, 53, 12, 18); A.desk(t, 53, 12, 27)
    for z in (15, 24, 33, 42): A.window(t, 50, 6, z, axis="z")
    for z in (16, 27, 39):
        t.fill((26, 20, z), (46, 22, z + 2), "create:framed_glass")
        t.fill((26, 23, z), (46, 23, z + 3), "minecraft:weathered_cut_copper_slab", type="bottom", waterlogged="false")
    round_tank(t, 59, 1, 44, 5, 10)
    t.fill((52, 1, 49), (66, 2, 54), "minecraft:smooth_stone")
    return t


def industrial_facility():
    t = industrial_facility_clean_master(); t.clear((3, 11, 30), (27, 28, 56)); t.fill((7, 1, 34), (16, 3, 44), "minecraft:gravel"); t.fill((12, 1, 39), (23, 5, 49), "minecraft:gravel"); t.fill((17, 1, 46), (27, 2, 55), "minecraft:gravel"); t.spawner(34, 2, 36, "minecraft:pillager", count=3, nearby=8); return t


def city_electrical_substation_clean_master():
    t = site((61, 22, 51), road=(7, 0, 53, 7))
    # Incoming gantry -> HV transformers -> switchyard -> control house -> city feeders.
    t.fill((5, 1, 10), (55, 1, 45), "minecraft:gravel")
    for x in (9, 29, 49):
        t.fill((x, 2, 11), (x + 2, 18, 13), "minecraft:polished_blackstone")
        t.fill((x, 17, 10), (x + 14, 19, 14), "minecraft:smooth_stone")
    transformer_bank(t, 9, 2, 19, 3)
    transformer_bank(t, 31, 2, 19, 3)
    for x in range(8, 54, 5):
        t.fill((x, 2, 31), (x + 1, 8, 32), "minecraft:smooth_stone")
        t.set(x, 9, 31, "immersiveengineering:capacitor_hv")
        t.fill((x, 6, 32), (x, 6, 40), "minecraft:oxidized_copper")
    A.shell(t, (7, 2, 36), (24, 13, 47), "minecraft:bricks", "tfmg:factory_floor", "minecraft:smooth_stone")
    A.door(t, 12, 3, 36, "north", "iron"); A.door(t, 20, 3, 47, "south", "iron")
    A.window(t, 7, 6, 40, axis="z"); A.desk(t, 9, 3, 39)
    t.fill((16, 3, 39), (21, 7, 44), "immersiveengineering:capacitor_mv")
    t.set(21, 3, 38, "the_wasteland_reworked:radio")
    for x in (32, 42, 52):
        t.fill((x, 2, 43), (x + 2, 14, 45), "minecraft:polished_blackstone")
        t.fill((x - 3, 13, 44), (x + 5, 15, 44), "minecraft:smooth_stone")
    return t


def city_electrical_substation():
    t = city_electrical_substation_clean_master(); t.clear((36, 9, 26), (60, 21, 50)); t.fill((38, 1, 29), (58, 4, 48), "minecraft:gravel"); t.spawner(15, 3, 42, "minecraft:pillager", count=2, nearby=7); return t


def city_water_treatment_plant_clean_master():
    t = site((75, 24, 65), road=(5, 0, 69, 7))
    # Intake screens and grit channels feed clarifiers, filters, disinfection and pump-out.
    t.fill((5, 1, 12), (20, 4, 24), "immersiveengineering:concrete_reinforced")
    for x in (7, 12, 17): t.fill((x, 2, 14), (x + 1, 3, 22), "minecraft:water")
    for cx, cz in ((31, 20), (48, 20), (65, 20)):
        t.fill((cx - 7, 1, cz - 7), (cx + 7, 2, cz + 7), "immersiveengineering:concrete_reinforced")
        for dx in range(-6, 7):
            for dz in range(-6, 7):
                if dx * dx + dz * dz <= 36: t.set(cx + dx, 3, cz + dz, "minecraft:water")
        t.fill((cx, 4, cz), (cx, 8, cz), "minecraft:oxidized_copper")
        t.fill((cx - 5, 7, cz), (cx + 5, 8, cz), "minecraft:oxidized_copper")
    for x in (7, 20, 33, 46):
        t.fill((x, 1, 34), (x + 10, 1, 46), "immersiveengineering:concrete_reinforced")
        t.fill((x, 2, 34), (x + 10, 4, 34), "immersiveengineering:concrete_reinforced")
        t.fill((x, 2, 46), (x + 10, 4, 46), "immersiveengineering:concrete_reinforced")
        t.fill((x, 2, 34), (x, 4, 46), "immersiveengineering:concrete_reinforced")
        t.fill((x + 10, 2, 34), (x + 10, 4, 46), "immersiveengineering:concrete_reinforced")
        t.fill((x + 1, 2, 35), (x + 9, 3, 45), "minecraft:water")
    A.shell(t, (55, 1, 33), (71, 15, 57), "minecraft:bricks", "tfmg:factory_floor", "minecraft:smooth_stone")
    A.double_door(t, 61, 2, 33, "north", "iron"); A.door(t, 68, 2, 57, "south", "iron")
    A.partition_z(t, 43, 2, 56, 70, "tfmg:cinder_block", (60, 67))
    for x in (58, 63, 68):
        t.fill((x, 2, 37), (x + 1, 8, 40), "create:fluid_tank")
        t.set(x, 2, 49, "create:mechanical_pump", facing="south")
    A.desk(t, 57, 2, 52); t.set(68, 2, 52, "the_wasteland_reworked:radio")
    for z in (38, 47, 54): A.window(t, 71, 5, z, axis="z")
    return t


def city_water_treatment_plant():
    t = city_water_treatment_plant_clean_master(); t.clear((42, 7, 10), (74, 23, 31)); t.fill((45, 1, 12), (57, 3, 21), "minecraft:gravel"); t.fill((53, 1, 17), (67, 5, 27), "minecraft:gravel"); t.fill((64, 1, 23), (74, 2, 31), "minecraft:gravel"); t.spawner(62, 2, 50, "minecraft:pillager", count=2, nearby=7); return t


def district_heating_station_clean_master():
    t = site((65, 31, 55), road=(5, 0, 59, 7))
    A.shell(t, (5, 1, 12), (38, 20, 47), "minecraft:bricks", "tfmg:factory_floor", "minecraft:weathered_cut_copper")
    A.gable_roof_x(t, 5, 38, 12, 47, 20, "minecraft:bricks", "minecraft:weathered_cut_copper_stairs", "minecraft:weathered_cut_copper")
    A.shell(t, (39, 1, 12), (60, 14, 32), "minecraft:bricks", "minecraft:smooth_stone", "minecraft:smooth_stone")
    t.clear((37, 2, 18), (40, 8, 28))
    A.double_door(t, 12, 2, 12, "north", "iron"); A.door(t, 47, 2, 12, "north", "iron")
    for x in (9, 18, 27):
        t.fill((x, 2, 18), (x + 5, 3, 27), "tfmg:steel_block")
        t.fill((x, 4, 18), (x + 5, 13, 18), "immersiveengineering:sheetmetal_steel")
        t.fill((x, 4, 27), (x + 5, 13, 27), "immersiveengineering:sheetmetal_steel")
        t.fill((x, 4, 18), (x, 13, 27), "immersiveengineering:sheetmetal_steel")
        t.fill((x + 5, 4, 18), (x + 5, 13, 27), "immersiveengineering:sheetmetal_steel")
        for bx in range(x + 1, x + 5): t.set(bx, 4, 18, "minecraft:blast_furnace", facing="north", lit="false")
        t.fill((x + 1, 14, 20), (x + 4, 18, 25), "create:fluid_tank")
        t.set(x + 2, 2, 34, "create:mechanical_pump", facing="south")
    t.fill((8, 2, 38), (34, 5, 44), "minecraft:polished_blackstone")
    A.partition_z(t, 22, 2, 40, 59, "tfmg:cinder_block", (44, 53))
    A.desk(t, 42, 2, 16); t.set(56, 2, 16, "the_wasteland_reworked:radio")
    t.fill((42, 2, 25), (57, 7, 29), "immersiveengineering:capacitor_mv")
    chimney(t, 51, 38, 1, 29)
    for z in (17, 28, 39): A.window(t, 5, 7, z, axis="z")
    return t


def district_heating_station():
    t = district_heating_station_clean_master(); t.clear((1, 13, 29), (35, 30, 54)); t.fill((6, 1, 33), (17, 3, 43), "minecraft:gravel"); t.fill((14, 1, 38), (27, 5, 49), "minecraft:gravel"); t.fill((24, 1, 45), (35, 2, 53), "minecraft:gravel"); t.spawner(47, 2, 25, "minecraft:pillager", count=3, nearby=8); return t


def municipal_incinerator_clean_master():
    t = site((71, 33, 59), road=(5, 0, 65, 7))
    # Tipping hall -> refuse bunker -> furnace line -> scrubbers -> ash dispatch.
    A.shell(t, (4, 1, 12), (27, 18, 49), "minecraft:bricks", "tfmg:factory_floor", "minecraft:smooth_stone")
    A.gable_roof_x(t, 4, 27, 12, 49, 18, "minecraft:bricks", "minecraft:weathered_cut_copper_stairs", "minecraft:weathered_cut_copper")
    A.shell(t, (26, 1, 10), (52, 23, 51), "immersiveengineering:sheetmetal_steel", "tfmg:factory_floor", "minecraft:weathered_cut_copper")
    A.shell(t, (51, 1, 12), (67, 13, 34), "minecraft:bricks", "minecraft:smooth_stone", "minecraft:smooth_stone")
    t.clear((25, 2, 18), (28, 9, 42)); t.clear((50, 2, 17), (53, 8, 29))
    for x in (8, 16): A.double_door(t, x, 2, 12, "north", "iron")
    t.fill((6, 2, 20), (23, 8, 44), "minecraft:coarse_dirt")
    for x in (30, 38, 46):
        t.fill((x, 2, 16), (x + 4, 3, 24), "tfmg:steel_block")
        t.fill((x, 4, 16), (x + 4, 12, 16), "immersiveengineering:sheetmetal_steel")
        t.fill((x, 4, 24), (x + 4, 12, 24), "immersiveengineering:sheetmetal_steel")
        t.fill((x, 4, 16), (x, 12, 24), "immersiveengineering:sheetmetal_steel")
        t.fill((x + 4, 4, 16), (x + 4, 12, 24), "immersiveengineering:sheetmetal_steel")
        for bx in range(x + 1, x + 4): t.set(bx, 4, 16, "minecraft:blast_furnace", facing="north", lit="false")
        t.fill((x, 2, 31), (x + 4, 16, 38), "create:fluid_tank")
        t.set(x + 2, 2, 44, "create:mechanical_press")
    A.partition_z(t, 22, 2, 52, 66, "tfmg:cinder_block", (56, 63))
    A.desk(t, 54, 2, 16); t.set(64, 2, 16, "the_wasteland_reworked:radio")
    t.fill((54, 2, 26), (64, 6, 31), "minecraft:scaffolding")
    chimney(t, 58, 40, 1, 31)
    t.fill((28, 7, 47), (53, 8, 56), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
    return t


def municipal_incinerator():
    t = municipal_incinerator_clean_master(); t.clear((37, 15, 6), (70, 32, 35)); t.fill((40, 1, 12), (51, 3, 22), "minecraft:gravel"); t.fill((48, 1, 17), (61, 5, 29), "minecraft:gravel"); t.fill((58, 1, 25), (69, 2, 35), "minecraft:gravel"); t.spawner(17, 2, 37, "minecraft:pillager", count=3, nearby=8); return t


def ruined_fuel_depot_clean_master():
    t = site((79, 25, 65), road=(6, 0, 72, 7))
    # Tank farm with individual containment cells, pump house and loading rack.
    for cx, cz in ((16, 20), (35, 20), (54, 20), (16, 43), (35, 43), (54, 43)):
        t.fill((cx - 8, 1, cz - 8), (cx + 8, 2, cz - 8), "minecraft:bricks")
        t.fill((cx - 8, 1, cz + 8), (cx + 8, 2, cz + 8), "minecraft:bricks")
        t.fill((cx - 8, 1, cz - 8), (cx - 8, 2, cz + 8), "minecraft:bricks")
        t.fill((cx + 8, 1, cz - 8), (cx + 8, 2, cz + 8), "minecraft:bricks")
        round_tank(t, cx, 1, cz, 6, 10)
    A.shell(t, (63, 1, 12), (75, 12, 31), "minecraft:bricks", "tfmg:factory_floor", "minecraft:smooth_stone")
    A.door(t, 67, 2, 12, "north", "iron"); A.door(t, 72, 2, 31, "south", "iron")
    A.window(t, 75, 5, 18, axis="z"); A.desk(t, 65, 2, 16)
    t.set(72, 2, 16, "the_wasteland_reworked:radio")
    for x in (64, 69, 74): t.set(x, 2, 25, "create:mechanical_pump", facing="south")
    t.fill((61, 1, 38), (76, 2, 57), "minecraft:smooth_stone")
    for x in (64, 70, 76):
        t.fill((x, 2, 41), (x + 1, 9, 42), "minecraft:polished_blackstone")
    t.fill((63, 9, 40), (77, 11, 44), "minecraft:smooth_stone")
    t.fill((64, 2, 49), (75, 5, 55), "minecraft:scaffolding")
    return t


def ruined_fuel_depot():
    t = ruined_fuel_depot_clean_master(); t.clear((30, 8, 31), (61, 24, 64)); t.fill((32, 1, 35), (59, 2, 61), "minecraft:black_concrete"); t.fill((39, 3, 41), (48, 5, 50), "minecraft:gravel"); t.fill((46, 3, 47), (57, 7, 57), "minecraft:gravel"); t.spawner(69, 2, 26, "minecraft:pillager", count=3, nearby=8); return t


def ruined_cyberware_clinic_clean_master():
    t = site((59, 26, 51), road=(6, 0, 52, 7))
    # Public diagnostic wing steps into secure surgery, recovery, lab and implant storage.
    A.shell(t, (5, 1, 10), (34, 13, 35), "minecraft:smooth_quartz", "minecraft:smooth_stone", "minecraft:smooth_stone")
    A.shell(t, (20, 1, 22), (53, 20, 47), "minecraft:light_gray_concrete", "tfmg:factory_floor", "minecraft:smooth_stone")
    A.shell(t, (36, 1, 9), (53, 12, 24), "minecraft:smooth_quartz", "minecraft:smooth_stone", "minecraft:smooth_stone")
    t.fill((12, 7, 7), (22, 8, 10), "minecraft:smooth_quartz_slab", type="bottom", waterlogged="false")
    for x in (12, 22): t.fill((x, 1, 8), (x, 6, 8), "minecraft:smooth_quartz")
    for x in (9, 16, 25, 31, 41, 48): A.window(t, x, 6, 10)
    A.shell(t, (29, 20, 29), (43, 24, 42), "create:framed_glass", "minecraft:smooth_stone", "minecraft:smooth_stone")
    t.clear((20, 2, 25), (22, 8, 32)); t.clear((36, 2, 17), (38, 8, 22))
    A.double_door(t, 16, 2, 10, "north", "iron")
    A.door(t, 44, 2, 9, "north", "iron"); A.door(t, 49, 2, 47, "south", "iron")
    # Reception/waiting and four examination rooms around a controlled hall.
    A.desk(t, 9, 2, 14); t.set(29, 2, 14, "the_wasteland_reworked:radio")
    for x in (9, 14, 25, 30): t.set(x, 2, 21, "minecraft:quartz_stairs", facing="south", half="bottom", shape="straight", waterlogged="false")
    A.partition_z(t, 24, 2, 6, 33, "minecraft:smooth_quartz", (10, 18, 28))
    A.partition_x(t, 14, 2, 25, 34, "minecraft:smooth_quartz", 29)
    A.partition_x(t, 26, 2, 25, 34, "minecraft:smooth_quartz", 29)
    for x in (8, 18, 29):
        A.bed(t, x, 2, 29, "south", "white")
        t.set(x + 3, 2, 29, "minecraft:brewing_stand", has_bottle_0="false", has_bottle_1="false", has_bottle_2="false")
    # Surgical suites, sterile prep, recovery and rear implant lab/store.
    A.partition_z(t, 34, 2, 21, 52, "minecraft:smooth_quartz", (25, 35, 45))
    A.partition_x(t, 36, 2, 35, 46, "minecraft:smooth_quartz", 40)
    for x in (25, 38):
        A.bed(t, x, 2, 29, "east", "cyan")
        t.fill((x, 5, 27), (x + 5, 5, 33), "minecraft:sea_lantern")
    for x in (24, 30, 40, 46): A.bed(t, x, 2, 40, "south", "gray")
    t.fill((39, 2, 12), (50, 6, 17), "ae2:drive")
    t.fill((39, 2, 20), (50, 5, 22), "minecraft:scaffolding")
    A.stair_flight(t, 23, 2, 25, 9, "south", "minecraft:quartz_stairs")
    t.fill((23, 12, 25), (50, 13, 44), "minecraft:smooth_stone")
    A.partition_x(t, 36, 13, 24, 45, "minecraft:smooth_quartz", 34)
    A.desk(t, 26, 13, 28); A.desk(t, 40, 13, 28)
    t.fill((39, 13, 36), (49, 17, 42), "ae2:controller")
    for x in (9, 17, 27, 40, 48): A.window(t, x, 6, 10)
    for z in (27, 38, 44): A.window(t, 53, 7, z, axis="z")
    return t


def ruined_cyberware_clinic():
    t = ruined_cyberware_clinic_clean_master(); t.clear((35, 13, 31), (58, 25, 50)); t.fill((38, 1, 34), (47, 3, 42), "minecraft:gravel"); t.fill((44, 1, 39), (55, 5, 48), "minecraft:gravel"); t.fill((52, 1, 45), (58, 2, 50), "minecraft:gravel"); t.spawner(28, 2, 39, "minecraft:pillager", count=3, nearby=8); return t


def ae2_records_archive_clean_master():
    t = site((63, 30, 55), road=(6, 0, 56, 7))
    # Intake/scanning front, two archive halls, secure digital core and backup plant.
    A.shell(t, (5, 1, 10), (29, 13, 31), "minecraft:bricks", "minecraft:smooth_stone", "minecraft:smooth_stone")
    A.shell(t, (16, 1, 25), (58, 22, 50), "minecraft:polished_deepslate", "tfmg:factory_floor", "minecraft:smooth_stone")
    A.shell(t, (39, 1, 9), (58, 15, 27), "minecraft:bricks", "minecraft:smooth_stone", "minecraft:smooth_stone")
    t.fill((10, 7, 7), (21, 8, 11), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
    for x in (10, 21): t.fill((x, 1, 8), (x, 6, 8), "minecraft:polished_deepslate")
    for x in (9, 15, 23, 44, 52): A.window(t, x, 6, 10)
    t.clear((17, 2, 25), (27, 8, 27)); t.clear((40, 2, 20), (42, 8, 27))
    A.double_door(t, 14, 2, 10, "north", "iron"); A.door(t, 47, 2, 9, "north", "iron")
    A.desk(t, 8, 2, 14); t.set(25, 2, 14, "the_wasteland_reworked:radio")
    A.partition_z(t, 21, 2, 6, 28, "tfmg:cinder_block", (10, 18, 25))
    for x in (8, 14, 21): t.fill((x, 2, 24), (x + 3, 5, 29), "ae2:quartz_glass")
    t.fill((8, 2, 18), (25, 3, 19), "minecraft:barrel", facing="up", open="false")
    # Physical archive stacks retain cross aisles; digital core is separately controlled.
    for x in (20, 27, 34, 48, 55):
        t.fill((x, 2, 31), (x + 2, 9, 46), "minecraft:scaffolding")
    t.fill((38, 2, 29), (44, 12, 47), "ae2:controller")
    t.clear((39, 3, 31), (43, 10, 45))
    for y in (3, 7, 11):
        t.fill((39, y, 31), (43, y, 45), "ae2:drive")
    A.stair_flight(t, 18, 2, 28, 10, "south", "minecraft:stone_brick_stairs")
    t.fill((18, 13, 28), (57, 14, 48), "minecraft:smooth_stone")
    for x in (21, 30, 49): A.desk(t, x, 14, 32)
    t.fill((42, 2, 12), (55, 8, 18), "ae2:dense_energy_cell")
    t.fill((43, 9, 13), (54, 13, 17), "immersiveengineering:capacitor_hv")
    for x in (9, 17, 25, 44, 52): A.window(t, x, 6, 10)
    A.shell(t, (34, 22, 33), (46, 28, 45), "ae2:quartz_glass", "minecraft:smooth_stone", "minecraft:smooth_stone")
    for z in (30, 40):
        t.fill((20, 22, z), (31, 24, z + 2), "create:framed_glass")
        t.fill((20, 25, z), (31, 25, z + 3), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
    return t


def ae2_records_archive():
    t = ae2_records_archive_clean_master(); t.clear((2, 14, 33), (31, 29, 54)); t.fill((7, 1, 37), (16, 3, 45), "minecraft:gravel"); t.fill((13, 1, 42), (24, 6, 51), "minecraft:gravel"); t.fill((21, 1, 48), (31, 2, 54), "minecraft:gravel"); t.spawner(47, 2, 40, "minecraft:pillager", count=3, nearby=8); return t


def nuclear_research_annex_clean_master():
    t = site((73, 33, 63), road=(6, 0, 66, 7))
    # Public/security and laboratories wrap a distinct cylindrical containment cell.
    A.shell(t, (5, 1, 10), (38, 16, 37), "minecraft:smooth_quartz", "minecraft:smooth_stone", "minecraft:smooth_stone")
    A.shell(t, (5, 1, 36), (43, 13, 57), "minecraft:light_gray_concrete", "tfmg:factory_floor", "minecraft:smooth_stone")
    A.double_door(t, 18, 2, 10, "north", "iron"); A.door(t, 12, 2, 57, "south", "iron")
    t.fill((13, 7, 7), (24, 8, 11), "minecraft:smooth_quartz_slab", type="bottom", waterlogged="false")
    for x in (13, 24): t.fill((x, 1, 8), (x, 6, 8), "minecraft:smooth_quartz")
    for x in (9, 17, 26, 34): A.window(t, x, 6, 10)
    for z in (16, 26, 46):
        t.fill((9, 16, z), (34, 18, z + 2), "create:framed_glass")
        t.fill((9, 19, z), (34, 19, z + 3), "minecraft:smooth_stone_slab", type="bottom", waterlogged="false")
    A.partition_z(t, 20, 2, 6, 37, "minecraft:smooth_quartz", (11, 18, 28, 35))
    A.partition_x(t, 18, 2, 21, 36, "minecraft:smooth_quartz", 29)
    A.partition_x(t, 29, 2, 21, 36, "minecraft:smooth_quartz", 29)
    A.desk(t, 8, 2, 14); t.set(34, 2, 14, "the_wasteland_reworked:radio")
    for x in (8, 21, 32):
        t.fill((x, 2, 25), (x + 6, 2, 31), "minecraft:smooth_quartz")
        for dx, dz in ((1, 1), (3, 3), (5, 5)):
            t.set(x + dx, 3, 25 + dz, "minecraft:brewing_stand", has_bottle_0="false", has_bottle_1="false", has_bottle_2="false")
    t.fill((8, 2, 41), (18, 6, 53), "minecraft:scaffolding")
    t.fill((22, 2, 41), (39, 5, 47), "create:fluid_tank")
    t.fill((22, 2, 51), (39, 6, 54), "immersiveengineering:capacitor_hv")
    # Reactor containment ring and observation bridge.
    cx, cz, radius = 56, 38, 13
    for y in range(1, 23):
        for dx in range(-radius, radius + 1):
            for dz in range(-radius, radius + 1):
                d2 = dx * dx + dz * dz
                if 130 <= d2 <= 169: t.set(cx + dx, y, cz + dz, "createnuclear:reactor_casing")
    t.fill((51, 1, 33), (61, 3, 43), "createnuclear:reactor_frame")
    t.fill((53, 4, 35), (59, 16, 41), "createnuclear:reactor_core")
    t.set(56, 17, 38, "createnuclear:reactor_controller")
    for rise, roof_radius in enumerate(range(13, 0, -1)):
        y = 23 + rise // 2
        for dx in range(-roof_radius, roof_radius + 1):
            for dz in range(-roof_radius, roof_radius + 1):
                if dx * dx + dz * dz <= roof_radius * roof_radius: t.set(cx + dx, y, cz + dz, "createnuclear:reinforced_glass")
    t.fill((35, 9, 34), (49, 11, 42), "minecraft:smooth_stone")
    A.stair_flight(t, 32, 2, 33, 8, "south", "minecraft:quartz_stairs")
    for x in (9, 17, 26, 34): A.window(t, x, 6, 10)
    return t


def nuclear_research_annex():
    t = nuclear_research_annex_clean_master(); t.clear((47, 17, 26), (72, 32, 62)); t.fill((49, 1, 30), (59, 3, 41), "minecraft:gravel"); t.fill((56, 1, 37), (68, 6, 51), "minecraft:gravel"); t.fill((65, 1, 47), (72, 2, 60), "minecraft:gravel"); t.spawner(26, 2, 28, "minecraft:pillager", count=4, nearby=9); return t


def shattered_wind_farm_clean_master():
    t = site((83, 39, 71), road=(7, 0, 75, 7))
    # Five serviceable turbines with individual pads and a central maintenance hut.
    for cx, cz in ((15, 20), (41, 18), (68, 21), (25, 51), (59, 51)):
        t.fill((cx - 5, 1, cz - 5), (cx + 5, 2, cz + 5), "minecraft:smooth_stone")
        for y in range(3, 30):
            width = 2 if y < 14 else 1
            t.fill((cx - width, y, cz - width), (cx + width, y, cz + width), "minecraft:white_concrete")
        t.fill((cx - 2, 30, cz - 2), (cx + 3, 33, cz + 2), "minecraft:light_gray_concrete")
        t.fill((cx, 31, cz - 14), (cx, 31, cz + 14), "minecraft:white_concrete")
        t.fill((cx, 17, cz), (cx, 37, cz), "minecraft:white_concrete")
        t.fill((cx, 31, cz), (cx + 12, 31, cz), "minecraft:white_concrete")
    A.shell(t, (34, 1, 38), (49, 12, 59), "minecraft:bricks", "tfmg:factory_floor", "minecraft:smooth_stone")
    A.door(t, 40, 2, 38, "north", "iron"); A.window(t, 34, 5, 45, axis="z")
    A.desk(t, 36, 2, 42); t.set(46, 2, 42, "the_wasteland_reworked:radio")
    t.fill((36, 2, 50), (47, 7, 56), "immersiveengineering:capacitor_mv")
    return t


def shattered_wind_farm():
    t = shattered_wind_farm_clean_master(); t.clear((51, 18, 34), (82, 38, 70)); t.fill((53, 1, 39), (63, 3, 49), "minecraft:gravel"); t.fill((60, 1, 46), (72, 5, 58), "minecraft:gravel"); t.fill((69, 1, 55), (81, 2, 69), "minecraft:gravel"); t.fill((55, 5, 44), (78, 6, 46), "minecraft:white_concrete"); t.spawner(42, 2, 53, "minecraft:pillager", count=2, nearby=8); return t


def broken_solar_field_clean_master():
    t = site((83, 17, 69), road=(7, 0, 75, 7))
    # Four independently wired panel fields converge on inverter/control cabins.
    for z in (14, 25, 38, 49):
        for x in range(7, 69, 5):
            t.fill((x, 2, z), (x + 3, 2, z + 1), "oritech:big_solar_panel_block")
            t.fill((x, 1, z + 2), (x + 3, 1, z + 3), "minecraft:polished_blackstone")
            t.fill((x, 3, z - 1), (x + 3, 3, z), "minecraft:black_stained_glass")
    A.shell(t, (6, 1, 56), (22, 11, 65), "minecraft:bricks", "tfmg:factory_floor", "minecraft:smooth_stone")
    A.shell(t, (58, 1, 55), (75, 12, 65), "minecraft:bricks", "tfmg:factory_floor", "minecraft:smooth_stone")
    A.door(t, 11, 2, 56, "north", "iron"); A.door(t, 64, 2, 55, "north", "iron")
    A.window(t, 6, 5, 59, axis="z"); A.window(t, 75, 5, 59, axis="z")
    for x in (9, 14, 61, 67, 72): t.fill((x, 2, 59), (x + 2, 7, 63), "immersiveengineering:capacitor_hv")
    A.desk(t, 24, 2, 58); t.set(54, 2, 58, "the_wasteland_reworked:radio")
    return t


def broken_solar_field():
    t = broken_solar_field_clean_master(); t.clear((38, 2, 31), (82, 16, 68)); t.fill((41, 1, 35), (52, 2, 45), "minecraft:gravel"); t.fill((49, 1, 42), (63, 4, 54), "minecraft:gravel"); t.fill((59, 1, 50), (72, 3, 61), "minecraft:gravel"); t.fill((69, 1, 58), (81, 2, 67), "minecraft:gravel"); t.spawner(14, 2, 61, "minecraft:pillager", count=2, nearby=8); return t


def wilderness_substation_clean_master():
    t = site((47, 19, 43), road=(5, 0, 41, 7))
    t.fill((5, 1, 11), (41, 1, 38), "minecraft:gravel")
    transformer_bank(t, 8, 2, 14, 3)
    for x in (8, 19, 30, 39):
        t.fill((x, 2, 26), (x + 1, 12, 27), "minecraft:polished_blackstone")
        t.fill((x - 2, 11, 25), (x + 4, 13, 28), "minecraft:smooth_stone")
    A.shell(t, (27, 2, 30), (41, 12, 39), "minecraft:bricks", "tfmg:factory_floor", "minecraft:smooth_stone")
    A.door(t, 32, 3, 30, "north", "iron"); A.window(t, 41, 6, 34, axis="z")
    A.desk(t, 29, 3, 33); t.set(38, 3, 33, "the_wasteland_reworked:radio")
    return t


def wilderness_substation():
    t = wilderness_substation_clean_master(); t.clear((1, 9, 20), (25, 18, 42)); t.fill((5, 1, 23), (13, 2, 31), "minecraft:gravel"); t.fill((11, 1, 28), (21, 4, 37), "minecraft:gravel"); t.fill((19, 1, 35), (25, 2, 42), "minecraft:gravel"); t.spawner(35, 3, 35, "minecraft:pillager", count=2, nearby=7); return t


def wasteland_water_tower_clean_master():
    t = site((45, 36, 45), road=(6, 0, 38, 7))
    # Pump/chlorination house below an elevated rounded municipal reservoir.
    A.shell(t, (5, 1, 12), (18, 11, 31), "minecraft:bricks", "tfmg:factory_floor", "minecraft:smooth_stone")
    A.gable_roof_x(t, 5, 18, 12, 31, 11, "minecraft:bricks", "minecraft:weathered_cut_copper_stairs", "minecraft:weathered_cut_copper")
    A.door(t, 10, 2, 12, "north", "iron"); A.window(t, 5, 5, 19, axis="z")
    A.desk(t, 7, 2, 16); t.set(15, 2, 16, "the_wasteland_reworked:radio")
    for x in (8, 13): t.set(x, 2, 25, "create:mechanical_pump", facing="south")
    for x, z in ((25, 15), (37, 15), (25, 33), (37, 33)):
        t.fill((x, 1, z), (x + 2, 22, z + 2), "minecraft:polished_blackstone")
    t.fill((24, 20, 14), (39, 23, 36), "minecraft:smooth_stone")
    round_tank(t, 31, 22, 25, 10, 8, "minecraft:light_blue_concrete")
    t.fill((30, 1, 24), (32, 21, 26), "minecraft:oxidized_copper")
    t.fill((21, 8, 12), (23, 30, 14), "minecraft:stone_bricks")
    t.fill((21, 28, 14), (28, 30, 14), "minecraft:stone_bricks")
    return t


def wasteland_water_tower():
    t = wasteland_water_tower_clean_master(); t.clear((32, 18, 27), (44, 35, 44)); t.fill((33, 1, 29), (40, 3, 36), "minecraft:gravel"); t.fill((37, 1, 34), (44, 6, 43), "minecraft:gravel"); t.fill((31, 7, 31), (42, 8, 33), "minecraft:light_blue_concrete"); t.spawner(12, 2, 25, "minecraft:pillager", count=2, nearby=7); return t
