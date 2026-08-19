import csv
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ERA2 = ROOT / "config/ftbquests/quests/chapters/era_02_heavy_industry.snbt"
ERA3 = ROOT / "config/ftbquests/quests/chapters/era_03_petrochemical_civilization.snbt"
LANG = ROOT / "config/ftbquests/quests/lang/en_us.snbt"
INDEX = ROOT / "docs/recipe-index/recipe-index.csv"
OUT = ROOT / "docs/quest-progression/reautomated-line-audit.csv"

QUEST_IDS = [f"630110000000{n:04X}" for n in range(1, 12)]
REQUIRED_RECIPES = [
    "createreautomatedtraces:trace_finder",
    "createreautomated:diamond_drill",
    "createreautomated:advanced_extractor",
    "createreautomated:advanced_extracting/copper_bits",
    "createreautomated:advanced_extracting/iron_bits",
    "createreautomated:advanced_extracting/zinc_bits",
    "createreautomated:advanced_extracting/gold_bits",
    "createreautomated:advanced_extracting/diamond_bits",
    "createreautomated:sequenced_assembly/unbaked_diamond_from_bits",
    "createreautomated:compacting/bake_diamond",
    "createreautomated:advanced_extracting/quartz_bits",
    "createreautomated:netherite_drill_upgrade",
    "createreautomated:stabilizer",
    "createreautomated:mechanical_crafting/infinite_iron_node",
]

with INDEX.open(encoding="utf-8-sig", newline="") as handle:
    enabled = {row["recipe_id"]: row for row in csv.DictReader(handle) if row["enabled"].lower() == "true"}

era2 = ERA2.read_text(encoding="utf-8")
era3 = ERA3.read_text(encoding="utf-8")
lang = LANG.read_text(encoding="utf-8")
rows = []
for index, quest_id in enumerate(QUEST_IDS):
    number = index + 1
    block_match = re.search(rf'\n\t\t\{{[\s\S]*?^\t\t\tid:\s*"{quest_id}"[\s\S]*?\n\t\t\}}', era3, re.MULTILINE)
    block = block_match.group(0) if block_match else ""
    previous = QUEST_IDS[index - 1] if index else "3210000000000004"
    dependency_ok = f'"{previous}"' in block
    if number == 1:
        dependency_ok = dependency_ok and '"6311000000000001"' in block
    if number == 8:
        dependency_ok = dependency_ok and '"6411000000000001"' in block
    if number == 9:
        dependency_ok = dependency_ok and '"6511000000000001"' in block
    localized = f"quest.{quest_id}.title:" in lang and f"quest.{quest_id}.quest_desc:" in lang
    rows.append({
        "quest_number": number,
        "quest_id": quest_id,
        "present": str(bool(block)),
        "dependency_ok": str(dependency_ok),
        "localized": str(localized),
        "status": "PASS" if block and dependency_ok and localized else "FAIL",
    })

missing_recipes = [recipe for recipe in REQUIRED_RECIPES if recipe not in enabled]
era2_split_ok = (
    'id: "createreautomated:iron_drill"' in era2
    and 'id: "createreautomated:iron_bit"' in era2
    and 'id: "createreautomated:diamond_drill"' not in era2
    and 'id: "createreautomated:advanced_extractor"' not in era2
)

jar = next((ROOT / "mods").glob("createreautomated-*.jar"))
with zipfile.ZipFile(jar) as archive:
    node_loot = json.loads(archive.read("data/createreautomated/loot_table/blocks/iron_node.json"))
stable_node_recovery_ok = '"stable": "true"' in json.dumps(node_loot)

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

failures = [row["quest_id"] for row in rows if row["status"] != "PASS"]
failures.extend(missing_recipes)
if not era2_split_ok:
    failures.append("Era 2/3 split")
if not stable_node_recovery_ok:
    failures.append("stable-node loot condition")

print(f"Re-Automated line: {len(rows) - sum(row['status'] != 'PASS' for row in rows)}/{len(rows)} quests pass; {len(REQUIRED_RECIPES) - len(missing_recipes)}/{len(REQUIRED_RECIPES)} recipes enabled.")
print(f"Era 2 discovery/iron split: {'PASS' if era2_split_ok else 'FAIL'}; stabilized-node recovery: {'PASS' if stable_node_recovery_ok else 'FAIL'}.")
if failures:
    for failure in failures:
        print(f"FAIL: {failure}")
    raise SystemExit(1)
