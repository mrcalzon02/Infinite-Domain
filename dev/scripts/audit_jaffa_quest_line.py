import csv
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "config/ftbquests/quests/chapters/era_01_mechanical_reconstruction.snbt"
LANG = ROOT / "config/ftbquests/quests/lang/en_us.snbt"
INDEX = ROOT / "docs/recipe-index/recipe-index.csv"
OUT = ROOT / "docs/quest-progression/jaffa-line-audit.csv"

QUEST_IDS = [f"610110000000{n:04X}" for n in range(1, 9)]
REQUIRED_RECIPES = [
    "jaffabricate:compacting/orange_juice",
    "jaffabricate:filling/orange_juice_bottle",
    "jaffabricate:mixing/orange_jelly",
    "jaffabricate:compacting/jaffa_base",
    "jaffabricate:deploying/bare_jaffa_cake",
    "jaffabricate:filling/jaffa_cake",
    "jaffabricate:sequenced_assembly/paperboard",
    "jaffabricate:compacting/jaffa_box_empty",
    "jaffabricate:sequenced_assembly/jaffa_box",
    "jaffabricate:sequenced_assembly/pallet_full",
    "jaffabricate:deploying/jaffa_pallet",
]

with INDEX.open(encoding="utf-8-sig", newline="") as handle:
    enabled = {row["recipe_id"]: row for row in csv.DictReader(handle) if row["enabled"].lower() == "true"}

chapter = CHAPTER.read_text(encoding="utf-8")
lang = LANG.read_text(encoding="utf-8")
rows = []
for index, quest_id in enumerate(QUEST_IDS):
    parent = "79D293B19143E993" if index == 0 else QUEST_IDS[index - 1]
    block_match = re.search(rf'\n\t\t\{{[\s\S]*?^\t\t\tid:\s*"{quest_id}"[\s\S]*?\n\t\t\}}', chapter, re.MULTILINE)
    block = block_match.group(0) if block_match else ""
    dependency_ok = f'"{parent}"' in block
    if index == 0:
        dependency_ok = dependency_ok and '"6D9810BDE000D7F6"' in block
    localized = f"quest.{quest_id}.title:" in lang and f"quest.{quest_id}.quest_desc:" in lang
    repeatable_sale_ok = True
    if index == 7:
        repeatable_sale_ok = all(token in block for token in (
            "can_repeat: true",
            "repeat_cooldown: 1",
            "consume_items: true",
            'id: "jaffabricate:jaffa_pallet"',
            'id: "numismatics:crown"',
            'auto: "enabled"',
        ))
    rows.append({
        "quest_number": index + 1,
        "quest_id": quest_id,
        "present": str(bool(block)),
        "dependency_ok": str(dependency_ok),
        "localized": str(localized),
        "repeatable_sale_ok": str(repeatable_sale_ok),
        "status": "PASS" if block and dependency_ok and localized and repeatable_sale_ok else "FAIL",
    })

missing_recipes = [recipe for recipe in REQUIRED_RECIPES if recipe not in enabled]
jar = next((ROOT / "mods").glob("jaffabricate-*.jar"))
with zipfile.ZipFile(jar) as archive:
    box = json.loads(archive.read("data/jaffabricate/recipe/sequenced_assembly/jaffa_box.json"))
    pallet = json.loads(archive.read("data/jaffabricate/recipe/sequenced_assembly/pallet_full.json"))
    orange_modifier = archive.read("data/jaffabricate/neoforge/biome_modifier/add_orange_tree.json").decode("utf-8")
    orange_loot = archive.read("data/jaffabricate/loot_table/blocks/orange_leaves.json").decode("utf-8")
box_loops = int(box["loops"])
pallet_loops = int(pallet["loops"])
cakes_per_pallet = box_loops * pallet_loops
orange_source_ok = "jaffabricate:orange_placed" in orange_modifier and "jaffabricate:orange_sapling" in orange_loot

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

failures = [row for row in rows if row["status"] != "PASS"]
if cakes_per_pallet != 240:
    failures.append({"quest_id": "recipe arithmetic"})
if missing_recipes:
    failures.extend({"quest_id": recipe} for recipe in missing_recipes)
if not orange_source_ok:
    failures.append({"quest_id": "orange worldgen/sapling source"})

print(f"Jaffa line: {len(rows) - sum(row['status'] != 'PASS' for row in rows)}/{len(rows)} quests pass; {len(REQUIRED_RECIPES) - len(missing_recipes)}/{len(REQUIRED_RECIPES)} recipes enabled.")
print(f"Verified production arithmetic: {box_loops} cakes/box x {pallet_loops} boxes/pallet = {cakes_per_pallet} cakes/pallet.")
print(f"Orange-tree world generation and renewable sapling drop: {'PASS' if orange_source_ok else 'FAIL'}.")
if failures:
    for failure in failures:
        print(f"FAIL: {failure['quest_id']}")
    raise SystemExit(1)
