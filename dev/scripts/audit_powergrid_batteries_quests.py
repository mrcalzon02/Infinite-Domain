from __future__ import annotations

import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CHAPTER = ROOT / "config/ftbquests/quests/chapters/grid_storage_and_recovery.snbt"
LANG = ROOT / "config/ftbquests/quests/lang/en_us.snbt"
REGISTRY = ROOT / "dev/docs/registry-inventory/item-ids.txt"
RECIPE_ROOT = ROOT / "kubejs/data/powergrid_batteries/recipe"
RECIPE_OUTPUTS = ROOT / "dev/docs/recipe-index/recipe-outputs.csv"


chapter = CHAPTER.read_text(encoding="utf-8")
language = LANG.read_text(encoding="utf-8")
registry = set(REGISTRY.read_text(encoding="utf-8").splitlines())

quest_ids = [f"6C010000000000{number:02X}" for number in range(1, 6)]
assert all(f'id: "{quest_id}"' in chapter for quest_id in quest_ids), "All five grid-storage quests must exist"
assert chapter.count("optional: true") == 5, "The entire grid-storage line must remain optional"
assert 'dependencies: ["4410000000000004"]' in chapter, "The line must begin after Era 4 Battery Buffer"
assert 'group: "4E65FAAC62D57D4A"' in chapter, "The line must remain a Civilization Specialization"
assert 'icon: "powergrid_batteries:small_battery"' in chapter, "The chapter needs an explicit registered icon"
assert all(
    f"quest.{quest_id}.title:" in language and f"quest.{quest_id}.quest_desc:" in language
    for quest_id in quest_ids
), "Every grid-storage quest must be localized"

task_sections = re.findall(r"tasks:\s*\[([\s\S]*?)\]\s*\n\t\t\tx:", chapter)
task_items = re.findall(
    r'item: \{ count: 1, id: "([a-z0-9_.-]+:[a-z0-9_./-]+)" \}',
    "\n".join(task_sections),
)
missing_items = sorted(set(task_items) - registry)
assert not missing_items, f"Unregistered grid-storage task items: {missing_items}"

battery_tiers = [
    "powergrid_batteries:small_battery",
    "powergrid_batteries:medium_battery",
    "powergrid_batteries:high_voltage_battery",
    "powergrid_batteries:substation_battery",
]
assert all(chapter.count(f'id: "{item}"') >= 1 for item in battery_tiers), "Every registered battery tier needs an objective"
assert chapter.count('type: "checkmark"') == 2, "The two commissioning drills must retain witnessed-procedure checkmarks"
assert 'task.6C02000000000007.title:' in language
assert 'task.6C02000000000009.title:' in language
for quest_id in quest_ids[3:]:
    start = chapter.index(f'id: "{quest_id}"')
    end = chapter.find('\n\t\t}', start)
    assert "rewards:" not in chapter[start:end], "Witnessed procedures must not grant material rewards"
assert "can_repeat: true" not in chapter, "Grid commissioning rewards must remain one-time"
assert "consume_items: true" not in chapter, "Infrastructure detection must not destroy placed-system spares"

recipe_expectations = {
    "small_battery.json": (
        "powergrid_batteries:small_battery",
        {"powergrid:battery", "minecraft:copper_block"},
    ),
    "medium_battery.json": (
        "powergrid_batteries:medium_battery",
        {"powergrid_batteries:small_battery", "allthecompressed:iron_block_2x"},
    ),
    "high_voltage_battery.json": (
        "powergrid_batteries:high_voltage_battery",
        {"powergrid_batteries:medium_battery", "minecraft:gold_block"},
    ),
    "substation_battery.json": (
        "powergrid_batteries:substation_battery",
        {"powergrid_batteries:high_voltage_battery", "minecraft:netherite_block"},
    ),
}

for filename, (output, ingredients) in recipe_expectations.items():
    payload = json.loads((RECIPE_ROOT / filename).read_text(encoding="utf-8"))
    assert payload.get("type") == "minecraft:crafting_shaped", f"{filename} must stay a shaped recipe"
    assert payload.get("result", {}).get("id") == output, f"{filename} has the wrong registered output"
    actual = {entry.get("item") for entry in payload.get("key", {}).values()}
    assert actual == ingredients, f"{filename} recipe ladder drift: {sorted(actual)}"

with RECIPE_OUTPUTS.open(encoding="utf-8", newline="") as handle:
    enabled_outputs = {
        row["output_id"]
        for row in csv.DictReader(handle)
        if row.get("enabled") == "True"
    }
required_sources = {
    "powergrid:battery",
    "allthecompressed:iron_block_2x",
    "minecraft:copper_block",
    "minecraft:gold_block",
    "minecraft:netherite_block",
    *battery_tiers,
}
missing_sources = sorted(required_sources - enabled_outputs)
assert not missing_sources, f"Grid-storage recipe inputs or outputs are not statically reachable: {missing_sources}"

print(
    "PowerGrid Batteries audit passed: 5 optional quests, "
    f"{len(task_items)} registered item tasks, 2 witnessed drills, 4 tier recipes, "
    f"and {len(required_sources)} enabled source/output paths verified."
)
