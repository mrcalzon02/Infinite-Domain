from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "config/ftbquests/quests/chapters/coffee_tea_economy.snbt"
CHAPTER = "1240CAEABAC9DC56"
GROUP = "3F00D00000000001"
ENTRY_DEPENDENCY = "4FC0C1C678C71891"
OBJECTIVES = [
    ("kubejs:coffee_cherries", 8), ("kubejs:black_coffee_mug", 1),
    ("kubejs:coffee_grounds", 16), ("kubejs:green_tea_cup", 1),
    ("kubejs:espresso_mug", 1), ("kubejs:canned_coffee", 12),
    ("kubejs:coffee_case", 1), ("kubejs:tea_crate", 1),
    ("kubejs:coffee_pallet", 1),
]

lines = ["{", '\tfilename: "coffee_tea_economy"', f'\tgroup: "{GROUP}"', f'\tid: "{CHAPTER}"', '\ticon: "kubejs:coffee_cherries"', '\torder_index: 1', '\tquests: [']
previous = None
for index, (item, count) in enumerate(OBJECTIVES, 1):
    qid = f"8F11D000000000{index:X}"
    lines.append("\t\t{")
    dependency = previous or ENTRY_DEPENDENCY
    lines.append(f'\t\t\tdependencies: ["{dependency}"]')
    lines.extend([
        f'\t\t\tid: "{qid}"',
		'\t\t\toptional: true',
        f'\t\t\ttasks: [{{ count: {count}L, id: "8F12D000000000{index:X}", item: {{ count: 1, id: "{item}" }}, type: "item" }}]',
        f'\t\t\tx: {(index - 1) * 3:.1f}d', '\t\t\ty: 0.0d', '\t\t}',
    ])
    previous = qid
lines.extend(["\t]", "}", ""])
OUT.write_text("\n".join(lines), encoding="utf-8")
print(f"Generated {OUT.relative_to(ROOT)} with {len(OBJECTIVES)} optional work-beverage quests.")
