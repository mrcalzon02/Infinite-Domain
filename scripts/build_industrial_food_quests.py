from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "config/ftbquests/quests/chapters/feeding_the_domain.snbt"

CHAPTER_ID = "2034B9BBF53C750D"
GROUP_ID = "3F00D00000000001"

# These IDs were assigned by the live FTB Quests editor before this generator
# became authoritative. Keep them stable so regeneration preserves player
# task progress and already-claimed rewards.
LIVE_OBJECT_IDS = [
    ("7B2B0CE2A9CEAD24", "2CCAE806E03DE05A", "0B5EA0DE7BFF1240"),
    ("7CF96E34F433B244", "0D7C8090ECA13BD4", "774EB5B71827C747"),
    ("60C6255859EF43EB", "7BC04F362EC404EE", "7F895B738294AB00"),
    ("62B68B083A9340FD", "58BCC462E66E9DA6", "309E4626464FEC71"),
    ("0025674D5053D8CD", "75E7E13E2DC4F3EC", "1E282BA6CA4F632C"),
    ("5B113F3538B71374", "251C8C9117A8D96F", "6D356CF098450B2D"),
    ("3CE261E9EC4CF123", "1EBDA77AB454F9F6", "07E925CE0869D9A1"),
    ("1BD60D82F5AB7FB3", "3756B175DD3A9163", "2D052408E5B25E3F"),
    ("36DCF312DDFCF7DD", "11A8FA7EE004F5CB", "3CA7B10399682E98"),
    ("6220EA917425C59A", "0ABF068D63A6B66B", "113E69A3B47E9E63"),
    ("5CAA77912D413E80", "2111F4C97BBF0E35", "3E996157A535F2BC"),
    ("066534B9EED187AC", "6FD21500FBC94956", "0980276A7C53AE9C"),
    ("271FC2FC3F6540D6", "007486054BA24453", "1987B27B85EDF227"),
    ("17E87207E385EF52", "357A00814BD746C1", "16D470EAD6DCA6E4"),
    ("52233AEAB76458BB", "2DA0E36D828CBBCD", "2999EA93AFD4C32F"),
    ("077D16DFAD15DC23", "46918445DAFD7395", "1CA94A7DEF94C330"),
    ("2C3D3B6833E06D5A", "3D4B176543DE1737", "381D5269A6F47D12"),
    ("52F44BCFA17D8586", "31B34601C506F033", "08E9CA96B5533402"),
    ("04D44ABE4F6F2CB8", "4EE77D928423CB01", "4623474DD76F6C41"),
    ("67DA49934330E1EF", "4E8FDE70AD658DD9", "752793C8E62A49B0"),
    ("4F9A7C40B90A12EA", "74FF20ED335201DB", "13F0C4002DD23AFC"),
    ("6D81BAB21AF3A8A5", "503E40BB4B7343E2", "608CBA2378D489D3"),
    ("50503724FC646207", "0FBE351C40EE9B74", "583BC1E866883221"),
    ("6058218448311BFE", "7D340AAE9D924252", "5AF89A6E22C9F81E"),
]

# Each tier is additionally gated by the corresponding era's foundation-core quest.
ERAS = [
    ("4FC0C1C678C71891", [
        ("kubejs:dried_herbs", 8),
        ("kubejs:ground_spice", 8),
        ("kubejs:prepared_seasoning", 8),
    ]),
    ("5210000000000002", [
        ("kubejs:apple_fruit_pulp", 4),
        ("kubejs:apple_juice_concentrate", 4),
        ("kubejs:bottled_apple_juice", 4),
    ]),
    ("5310000000000002", [
        ("kubejs:concentrated_soup_base", 4),
        ("kubejs:fermentation_culture", 1),
        ("kubejs:prepared_meal", 8),
    ]),
    ("5410000000000002", [
        ("kubejs:empty_beverage_can", 16),
        ("kubejs:empty_food_can", 8),
        ("kubejs:canned_stew", 8),
    ]),
    ("5510000000000002", [
        ("kubejs:apple_soda_can", 6),
        ("kubejs:berry_soda_six_pack", 2),
        ("kubejs:orange_soda_case", 1),
    ]),
    ("5610000000000002", [
        ("kubejs:electrolyte_blend", 8),
        ("kubejs:stimulant_extract", 4),
        ("kubejs:energy_drink_can", 12),
    ]),
    ("5710000000000002", [
        ("kubejs:beverage_crate", 1),
        ("kubejs:field_ration", 8),
        ("kubejs:ration_case", 2),
    ]),
    ("5810000000000002", [
        ("kubejs:ration_pallet", 1),
        ("kubejs:energy_case", 4),
        ("kubejs:beverage_pallet", 2),
    ]),
]


def quest_id(index: int) -> str:
    return LIVE_OBJECT_IDS[index - 1][0]


def task_id(index: int) -> str:
    return LIVE_OBJECT_IDS[index - 1][1]


def reward_id(index: int) -> str:
    return LIVE_OBJECT_IDS[index - 1][2]


def render() -> str:
    lines = [
        "{",
        '\tdefault_hide_dependency_lines: false',
        '\tdefault_quest_shape: "gear"',
        '\tfilename: "feeding_the_domain"',
        f'\tgroup: "{GROUP_ID}"',
        f'\tid: "{CHAPTER_ID}"',
        '\ticon: "farmersdelight:cooking_pot"',
        '\timages: [ ]',
        '\torder_index: 0',
        '\tquest_links: [ ]',
        '\tquests: [',
    ]
    previous = None
    index = 1
    for era_index, (core_quest, objectives) in enumerate(ERAS, start=1):
        for local_index, (item, count) in enumerate(objectives):
            qid = quest_id(index)
            deps = ([previous] if previous else [])
            if local_index == 0:
                deps.append(core_quest)
            lines.extend(["\t\t{"])
            if deps:
                encoded = ", ".join(f'"{dep}"' for dep in deps)
                lines.append(f"\t\t\tdependencies: [{encoded}]")
            lines.extend([
                f'\t\t\tid: "{qid}"',
				'\t\t\toptional: true',
                '\t\t\trewards: [{',
                f'\t\t\t\tid: "{reward_id(index)}"',
                f'\t\t\t\txp: {100 + era_index * 100}',
                '\t\t\t\ttype: "xp"',
                '\t\t\t}]',
                '\t\t\ttasks: [{',
                f'\t\t\t\tcount: {count}L',
                f'\t\t\t\tid: "{task_id(index)}"',
                f'\t\t\t\titem: {{ count: 1, id: "{item}" }}',
                '\t\t\t\ttype: "item"',
                '\t\t\t}]',
                f'\t\t\tx: {(-4 + local_index * 4):.1f}d',
                f'\t\t\ty: {(era_index - 1) * 5:.1f}d',
                '\t\t}',
            ])
            previous = qid
            index += 1
    lines.extend(["\t]", "}", ""])
    return "\n".join(lines)


OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(render(), encoding="utf-8")
print(f"Generated {OUT.relative_to(ROOT)} with {sum(len(e[1]) for e in ERAS)} quests.")
