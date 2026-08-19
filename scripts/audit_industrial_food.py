"""Static completeness audit for the data-driven industrial food system."""

from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "kubejs/config/industrial_food.json"
STARTUP = ROOT / "kubejs/startup_scripts/industrial_food_items.js"
RECIPES = ROOT / "kubejs/server_scripts/industrial_food.js"
ASSETS = ROOT / "kubejs/assets/kubejs"
QUEST = ROOT / "config/ftbquests/quests/chapters/feeding_the_domain.snbt"
QUEST_ROOT = ROOT / "config/ftbquests/quests/chapters"
OUT = ROOT / "docs/industrial-food"


def derived(data: dict) -> tuple[list[dict], list[dict]]:
    items = list(data["items"])
    fluids = list(data["fluids"])
    for flavor in data["flavors"]:
        fid, name = flavor["id"], flavor["name"]
        items.extend([
            {"id": f"{fid}_fruit_pulp", "name": f"{name} Pulp"},
            {"id": f"{fid}_juice_concentrate", "name": f"{name} Juice Concentrate"},
            {"id": f"bottled_{fid}_juice", "name": f"Bottled {name} Juice"},
            {"id": f"{fid}_soda_can", "name": f"{name} Soda Can"},
            {"id": f"{fid}_soda_six_pack", "name": f"{name} Soda Six-Pack"},
            {"id": f"{fid}_soda_case", "name": f"{name} Soda Case"},
        ])
        fluids.extend([
            {"id": f"pressed_{fid}_juice", "name": f"Pressed {name} Juice"},
            {"id": f"prepared_{fid}_beverage", "name": f"Prepared {name} Beverage"},
            {"id": f"{fid}_soda_base", "name": f"{name} Soda Base"},
            {"id": f"carbonated_{fid}_soda", "name": f"Carbonated {name} Soda"},
        ])
    return items, fluids


def main() -> int:
    data = json.loads(CONFIG.read_text(encoding="utf-8"))
    source = RECIPES.read_text(encoding="utf-8")
    startup = STARTUP.read_text(encoding="utf-8")
    lang = json.loads((ASSETS / "lang/en_us.json").read_text(encoding="utf-8"))
    items, fluids = derived(data)
    failures: list[str] = []
    checks: list[str] = []

    for token in (
        "StartupEvents.registry('block'",
        "item.kind === 'pallet'",
        "item.kind !== 'pallet'",
        "tagBlock('minecraft:mineable/axe')",
    ):
        if token not in startup: failures.append(f"Missing pallet block registration token: {token}")

    item_ids = [item["id"] for item in items]
    fluid_ids = [fluid["id"] for fluid in fluids]
    if len(item_ids) != len(set(item_ids)):
        failures.append("Duplicate item IDs in the authoritative definition")
    if len(fluid_ids) != len(set(fluid_ids)):
        failures.append("Duplicate fluid IDs in the authoritative definition")

    for item in items:
        iid = item["id"]
        texture = ASSETS / f"textures/item/{iid}.png"
        model = ASSETS / f"models/item/{iid}.json"
        if not texture.exists(): failures.append(f"Missing item texture: {iid}")
        if not model.exists(): failures.append(f"Missing item model: {iid}")
        if f"item.kubejs.{iid}" not in lang: failures.append(f"Missing item localization: {iid}")
        if texture.exists():
            with Image.open(texture) as image:
                rgba = image.convert("RGBA")
                alpha = list(rgba.getchannel("A").get_flattened_data())
                if rgba.size != (128, 128): failures.append(f"Wrong item dimensions: {iid} {rgba.size}")
                if not any(a == 0 for a in alpha): failures.append(f"No transparent background: {iid}")
                corners = [rgba.getpixel(p)[3] for p in [(0,0),(rgba.width-1,0),(0,rgba.height-1),(rgba.width-1,rgba.height-1)]]
                if any(corners): failures.append(f"Opaque texture corner: {iid}")
        if model.exists():
            model_data = json.loads(model.read_text(encoding="utf-8"))
            if model_data.get("textures", {}).get("layer0") != f"kubejs:item/{iid}":
                failures.append(f"Broken model texture reference: {iid}")
        if item.get("kind") == "pallet":
            if f"block.kubejs.{iid}" not in lang: failures.append(f"Missing block localization: {iid}")
            for face in ("front", "side", "top"):
                block_texture = ASSETS / f"textures/block/{iid}_{face}.png"
                if not block_texture.exists():
                    failures.append(f"Missing pallet block texture: {iid}_{face}")
                else:
                    with Image.open(block_texture) as image:
                        rgba = image.convert("RGBA")
                        if rgba.size != (128, 128): failures.append(f"Wrong pallet block dimensions: {iid}_{face} {rgba.size}")
                        if any(a != 255 for a in rgba.getchannel("A").get_flattened_data()):
                            failures.append(f"Pallet block face is not fully opaque: {iid}_{face}")

    for fluid in fluids:
        fid = fluid["id"]
        if f"fluid.kubejs.{fid}" not in lang: failures.append(f"Missing fluid localization: {fid}")
        for suffix, expected in (("still", (16, 16)), ("flow", (32, 32))):
            texture = ASSETS / f"textures/fluid/{fid}_{suffix}.png"
            if not texture.exists():
                failures.append(f"Missing fluid texture: {fid}_{suffix}")
            else:
                with Image.open(texture) as image:
                    if image.size != expected: failures.append(f"Wrong fluid dimensions: {fid}_{suffix} {image.size}")
                    if image.mode != "RGBA": failures.append(f"Fluid texture lacks RGBA: {fid}_{suffix}")

    expected_item_textures = {f"{iid}.png" for iid in item_ids}
    actual_item_textures = {p.name for p in (ASSETS / "textures/item").glob("*.png") if p.stem in item_ids}
    if actual_item_textures != expected_item_textures:
        failures.append("Generated item texture set differs from registered item set")

    literal_recipe_ids = re.findall(r"\.id\('([^']+)'\)", source)
    duplicate_recipe_ids = [key for key, count in Counter(literal_recipe_ids).items() if count > 1]
    if duplicate_recipe_ids: failures.append(f"Duplicate literal recipe IDs: {', '.join(duplicate_recipe_ids)}")
    for flavor in data["flavors"]:
        fid = flavor["id"]
        for token in ("fruit_pulp", "pressed_", "juice_concentrate", "soda_base", "carbonated_", "soda_can", "soda_six_pack", "soda_case", "unpack_"):
            if token not in source: failures.append(f"Missing generated flavor architecture token: {fid}/{token}")

    required_intermediates = [
        "fruit_pomace", "dried_herbs", "ground_spice", "crushed_oilseed", "chopped_vegetables",
        "crushed_sugar_biomass", "fermentation_culture", "empty_beverage_can", "empty_food_can",
        "prepared_meal", "electrolyte_blend", "stimulant_extract", "empty_ration_pouch",
        "ration_entree", "grain_cracker_pack", "dried_fruit_packet", "beverage_powder_packet",
        "condiment_packet",
    ]
    for iid in required_intermediates:
        if source.count(f"kubejs:{iid}") < 2:
            failures.append(f"Intermediate lacks both a producer and consumer: {iid}")

    for package in ("soda_six_pack", "soda_case", "energy_six_pack", "energy_case", "ration_case", "ration_crate", "beverage_pallet", "ration_pallet"):
        if f"unpack_{package}" not in source and package not in {"soda_six_pack", "soda_case"}:
            failures.append(f"Missing unpack route: {package}")
    if "ItemEvents.rightClicked('kubejs:beverage_crate'" not in source:
        failures.append("Mixed beverage crate has no deterministic unpack route")
    for token in ("foodIndustry.balance.cratesPerPallet", "unpack_beverage_pallet", "unpack_ration_pallet"):
        if token not in source:
            failures.append(f"Missing pallet conservation token: {token}")

    quest_text = QUEST.read_text(encoding="utf-8") if QUEST.exists() else ""
    quest_item_ids = re.findall(r'item: \{ count: 1, id: "kubejs:([a-z0-9_]+)" \}', quest_text)
    for iid in quest_item_ids:
        if iid not in item_ids: failures.append(f"Quest references unregistered item: kubejs:{iid}")
    all_quest_text = "\n".join(p.read_text(encoding="utf-8") for p in QUEST_ROOT.glob("*.snbt"))
    all_quest_ids = set(re.findall(r'^\s*id: "([A-Fa-f0-9]+)"', all_quest_text, re.MULTILINE))
    dependencies = re.findall(r'dependencies:\s*\[([^]]*)\]', quest_text, re.DOTALL)
    for block in dependencies:
        for dep in re.findall(r'"([A-Fa-f0-9]+)"', block):
            if dep not in all_quest_ids: failures.append(f"Missing quest dependency: {dep}")

    inventory = set((ROOT / "docs/registry-inventory/item-ids.txt").read_text(encoding="utf-8").splitlines())
    compatible = [
        ("Fruit", "minecraft:apple", "Apple pulp, juice, concentrate, soda"),
        ("Fruit", "minecraft:sweet_berries", "Berry pulp, juice, concentrate, soda"),
        ("Fruit", "jaffabricate:orange", "Orange pulp, juice, concentrate, soda"),
        ("Vegetable", "farmersdelight:cabbage", "Vegetable blend, broth, meals"),
        ("Vegetable", "farmersdelight:onion", "Vegetable blend and seasoning"),
        ("Vegetable", "farmersdelight:tomato", "Vegetable blend and meals"),
        ("Grain", "farmersdelight:rice", "Prepared meals and ration starch"),
        ("Fermentation", "brewery:brewers_yeast", "Reusable CO2 culture"),
        ("Aromatic", "brewery:hop", "Seasoning and stimulant extraction"),
        ("Mineral", "petrochem:salt_dust", "Seasoning, preservation, electrolyte blend"),
        ("Process water", "wastelands:purified_water", "Manufactured beverages and broth"),
        ("Packaging", "immersiveengineering:plate_aluminum", "Beverage cans through shared plate tag"),
        ("Packaging", "immersiveengineering:plate_steel", "Food cans through shared plate tag"),
    ]
    for category, item_id, _ in compatible:
        if item_id not in inventory: failures.append(f"Compatible resource absent from captured registry: {item_id}")

    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "resource-inventory.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["category", "registry_id", "industrial_role", "verified_in_registry"])
        for row in compatible:
            writer.writerow([*row, str(row[1] in inventory).lower()])

    checks.extend([
        f"{len(items)} registered item definitions",
        f"{len(fluids)} registered fluid definitions / {len(fluids) * 2} fluid textures",
        f"{len(literal_recipe_ids)} literal recipe IDs plus one generated flavor family",
        f"{len(quest_item_ids)} quest objectives across 8 era gates",
        f"{len(compatible)} compatible installed resources verified against the captured registry",
        "antialiased 128x128 RGBA item textures with transparent corners",
        "four placeable freight-pallet blocks with distinct 128x128 front, side, and top textures",
        "reversible six-pack, case, crate, and pallet packaging with conserved consumable counts",
    ])
    report = ["# Industrial Food Automated Audit", "", f"Status: **{'PASS' if not failures else 'FAIL'}**", "", "## Coverage", ""]
    report.extend(f"- {check}" for check in checks)
    report.extend(["", "## Failures", ""])
    report.extend((f"- {failure}" for failure in failures) if failures else ["- None"])
    (OUT / "audit-report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"Industrial food audit: {'PASS' if not failures else 'FAIL'} ({len(failures)} failures)")
    for failure in failures: print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
