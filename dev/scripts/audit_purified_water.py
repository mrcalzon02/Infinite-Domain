"""Verify the pack's bottled purified-water lifecycle."""

from __future__ import annotations

import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECIPE = ROOT / "kubejs/data/wastelands/recipe/purified_water.json"
SNOW_RECIPE = ROOT / "kubejs/data/wastelands/recipe/purified_water_from_snow.json"
JAR = ROOT / "mods/wastelands-2.4.0-neoforge.1.jar"
ITEM_CLASS = "org/takesome/necrosteam/content/PurifiedWaterItem.class"
MANIFEST = ROOT / "docs/compression-audit/generated-crafting-overrides.csv"


recipe = json.loads(RECIPE.read_text(encoding="utf-8"))
snow_recipe = json.loads(SNOW_RECIPE.read_text(encoding="utf-8"))
ingredients = recipe["ingredients"]
water = [entry for entry in ingredients if entry.get("items") == "minecraft:potion"]

assert len(water) == 1, "Purified water must consume exactly one potion bottle"
assert water[0].get("type") == "neoforge:components", "Potion input must use the installed component ingredient"
assert water[0].get("components", {}).get("minecraft:potion_contents", {}).get("potion") == "minecraft:water", "Potion input must be an ordinary water bottle"
assert not any(entry.get("item") == "minecraft:glass_bottle" for entry in ingredients), "Empty bottle must not satisfy the recipe"
assert [entry.get("item") for entry in ingredients if "item" in entry] == ["quark:charcoal_block"], "Water route must use only a water bottle and charcoal block"
assert recipe["result"] == {"id": "wastelands:purified_water", "count": 1}, "Recipe must produce one purified water"

assert snow_recipe["ingredients"] == [
    {"item": "minecraft:glass_bottle"},
    {"item": "minecraft:snow_block"},
], "Snow route must use an empty bottle and snow block"
assert snow_recipe["result"] == {"id": "wastelands:purified_water", "count": 1}, "Snow route must produce one purified water"

with zipfile.ZipFile(JAR) as jar:
    bytecode = jar.read(ITEM_CLASS)

for token in (b"GLASS_BOTTLE", b"addItem", b"drop", b"finishUsingItem"):
    assert token in bytecode, f"Installed consumption implementation is missing {token.decode()}"

assert "wastelands:purified_water," not in MANIFEST.read_text(encoding="utf-8-sig"), "Hand policy recipe must not remain scaler-owned"

print("Purified water audit passed: water-plus-charcoal and empty-bottle-plus-snow routes, with native bottle return, verified.")
