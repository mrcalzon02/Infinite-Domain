from __future__ import annotations

import re
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CHAPTER = ROOT / "config/ftbquests/quests/chapters/brewery_and_winery.snbt"
LANG = ROOT / "config/ftbquests/quests/lang/en_us.snbt"
REGISTRY = ROOT / "dev/docs/registry-inventory/item-ids.txt"
BREWERY = ROOT / "mods/brewery-1.1.2.jar"
WINERY = ROOT / "mods/create_winery-2.0.2-neoforge-1.21.1.jar"

text = CHAPTER.read_text(encoding="utf-8")
language = LANG.read_text(encoding="utf-8")
registry = set(REGISTRY.read_text(encoding="utf-8").splitlines())

quest_ids = [f"6B010000000000{number:02X}" for number in range(1, 9)]
assert all(f'id: "{quest_id}"' in text for quest_id in quest_ids), "All eight quests must exist"
assert text.count("optional: true") == 8, "The complete line must remain optional"
assert 'dependencies: ["4FC0C1C678C71891"]' in text, "Line must begin after the Mechanical Foundation"
assert 'group: "3F00D00000000001"' in text, "Line must remain in the valid Industrial Food Production group"
assert all(f"quest.{quest_id}.title:" in language and f"quest.{quest_id}.quest_desc:" in language for quest_id in quest_ids), "All quests must be localized"

task_sections = re.findall(r'tasks:\s*\[([\s\S]*?)\]\s*\n\t\t\tx:', text)
task_items = re.findall(
    r'item: \{ count: 1, id: "([a-z0-9_.-]+:[a-z0-9_./-]+)" \}',
    "\n".join(task_sections),
)
assert len(task_items) == 20, "The line must retain exactly 20 concrete item objectives"
missing_items = sorted(set(task_items) - registry)
assert not missing_items, f"Unregistered quest items: {missing_items}"

required_brewery = {
    "data/brewery/recipe/mixing/beer.json",
    "data/brewery/recipe/mixing/cider.json",
    "data/brewery/recipe/mixing/wine.json",
    "data/brewery/recipe/mixing/brewers_yeast.json",
    "data/brewery/recipe/pressing/apple_mash.json",
    "data/brewery/recipe/pressing/grape_mash.json",
    "data/brewery/recipe/smoking/kilned_malt.json",
}
required_winery = {
    "data/create_winery/recipe/create/compacting_red_grapes.json",
    "data/create_winery/recipe/create/compacting_white_grapes.json",
    "data/create_winery/recipe/create/mixing_apple_must.json",
    "data/create_winery/recipe/create/wine_cellar_recipe.json",
    "data/create_winery/recipe/bordeaux_recipe.json",
    "data/create_winery/recipe/chardonnay_recipe.json",
    "data/create_winery/recipe/cider_recipe.json",
}
with zipfile.ZipFile(BREWERY) as archive:
    missing = sorted(required_brewery - set(archive.namelist()))
    assert not missing, f"Missing Brewery recipes: {missing}"
with zipfile.ZipFile(WINERY) as archive:
    missing = sorted(required_winery - set(archive.namelist()))
    assert not missing, f"Missing Create Winery recipes: {missing}"

assert text.count('id: "create_winery:bordeaux"') == 1
assert text.count('id: "create_winery:chardonnay"') == 1
assert text.count('id: "create_winery:cider"') == 1
assert "consume_items: true" not in text, "Representative products must be detected, not consumed"
assert "can_repeat: true" not in text, "No unbalanced repeatable beverage exchange"

print(f"Brewery/Winery audit passed: {len(quest_ids)} optional quests, {len(task_items)} registered item objectives, and {len(required_brewery) + len(required_winery)} required jar recipes verified.")
