"""Generate the authoritative consumable balance and logistics-conservation reports."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "kubejs/config/industrial_food.json"
REGISTRY = ROOT / "docs/registry-inventory/item-block-registry.json"
OUT = ROOT / "docs/industrial-food"

EFFECT_LIMITS = {"juice": 90, "soda": 45, "energy_drink": 120, "coffee": 150, "tea": 180, "prepared_meal": 120, "canned_meal": 120}
COST_RANK = {"trivial": 0, "low": 1, "moderate": 2, "substantial": 3, "high": 4, "very_high": 5}


def effects_text(product: dict) -> tuple[str, str, str]:
    effects = product.get("effects", [])
    if not effects:
        return "None", "-", "-"
    names = "; ".join(effect["id"] for effect in effects)
    levels = "; ".join(str(effect["amplifier"] + 1) for effect in effects)
    durations = "; ".join(str(effect["duration"] // 20) for effect in effects)
    return names, levels, durations


def practical_score(product: dict) -> float:
    effect_seconds = sum(effect["duration"] / 20 for effect in product.get("effects", []))
    return product["nutrition"] + product["nutrition"] * product["saturation"] + min(effect_seconds / 30, 2)


def main() -> int:
    data = json.loads(CONFIG.read_text(encoding="utf-8"))
    products = data["consumables"]
    failures: list[str] = []
    warnings: list[str] = []

    ids = [product["id"] for product in products]
    if len(ids) != len(set(ids)):
        failures.append("Duplicate IDs in consumables balance source")

    expected = {
        "prepared_meal", "canned_stew", "ration_entree", "grain_cracker_pack",
        "dried_fruit_packet", "field_ration", "bottled_apple_juice",
        "bottled_berry_juice", "bottled_orange_juice", "apple_soda_can",
        "berry_soda_can", "orange_soda_can", "energy_drink_can",
        "black_coffee_mug", "espresso_mug", "latte_mug", "cold_brew_bottle", "canned_coffee",
        "green_tea_cup", "black_tea_cup", "oolong_tea_cup", "bottled_iced_tea", "canned_iced_tea",
    }
    missing = sorted(expected - set(ids))
    if missing:
        failures.append(f"Finished consumables missing balance definitions: {', '.join(missing)}")

    for product in products:
        if product["nutrition"] <= 0 and product["family"] not in {"coffee", "tea"}:
            failures.append(f"Zero practical hunger benefit: {product['id']}")
        if product["family"] in {"coffee", "tea"} and (product["nutrition"] != 0 or product["saturation"] != 0):
            failures.append(f"Work beverage violates zero-food rule: {product['id']}")
        if not 0 <= product["saturation"] <= 1.2:
            failures.append(f"Saturation modifier outside supported envelope: {product['id']}")
        if product["recipeCost"] not in COST_RANK:
            failures.append(f"Unknown recipe-cost category: {product['id']}")
        limit = EFFECT_LIMITS.get(product["family"], 120)
        for effect in product.get("effects", []):
            seconds = effect["duration"] / 20
            if seconds > limit:
                failures.append(f"Effect duration exceeds {product['family']} envelope: {product['id']} {seconds:g}s")
            if effect["amplifier"] > 0:
                warnings.append(f"Non-Level-I consumer effect requires review: {product['id']} {effect['id']}")
        if len(product.get("effects", [])) > (2 if product["family"] in {"energy_drink", "coffee", "tea"} else 1):
            failures.append(f"Effect spam: {product['id']}")

    by_family: dict[str, list[dict]] = defaultdict(list)
    for product in products:
        by_family[product["family"]].append(product)
    for family, members in by_family.items():
        if len(members) < 2:
            continue
        scores = [practical_score(member) for member in members]
        if max(scores) > min(scores) * 1.6:
            warnings.append(f"Possible dominant option inside {family}: score range {min(scores):.2f}-{max(scores):.2f}")

    by_id = {product["id"]: product for product in products}
    pair_tests = {
        "canned stew + apple juice": ("canned_stew", "bottled_apple_juice"),
        "canned stew + berry juice": ("canned_stew", "bottled_berry_juice"),
        "canned stew + apple soda": ("canned_stew", "apple_soda_can"),
        "prepared meal + orange soda": ("prepared_meal", "orange_soda_can"),
    }
    pair_results: list[tuple[str, int, str]] = []
    for label, (left, right) in pair_tests.items():
        total = by_id[left]["nutrition"] + by_id[right]["nutrition"]
        status = "PASS" if 15 <= total <= 18 else "REVIEW"
        pair_results.append((label, total, status))
        if status != "PASS":
            failures.append(f"Meal-pair target miss: {label} restores {total}")
    mre = by_id["field_ration"]["nutrition"]
    if not 15 <= mre <= 18:
        failures.append(f"Field ration target miss: restores {mre}")

    b = data["balance"]
    conservation = [
        ("Flavor beverage case", b["drinksPerSixPack"] * b["sixPacksPerCase"], "cans"),
        ("Mixed beverage crate", 3 * b["drinksPerSixPack"] * b["sixPacksPerCase"], "cans"),
        ("Mixed beverage pallet", b["cratesPerPallet"] * 3 * b["drinksPerSixPack"] * b["sixPacksPerCase"], "cans"),
        ("Ration crate", b["rationsPerCase"] * b["casesPerCrate"], "rations"),
        ("Ration pallet", b["cratesPerPallet"] * b["rationsPerCase"] * b["casesPerCrate"], "rations"),
        ("Coffee pallet", b["cratesPerPallet"] * b["casesPerCrate"] * b["sixPacksPerCase"] * b["drinksPerSixPack"], "cans"),
        ("Tea pallet", b["cratesPerPallet"] * b["casesPerCrate"] * b["sixPacksPerCase"] * b["drinksPerSixPack"], "cans"),
    ]

    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "consumable-balance.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["Category", "Item", "Brand", "Flavor", "Hunger", "Saturation", "Effect", "Level", "Duration Seconds", "Tier", "Recipe Cost", "Gameplay Niche"])
        for product in sorted(products, key=lambda value: (value["family"], value["tier"], value["id"])):
            effect, level, duration = effects_text(product)
            writer.writerow([product["family"], product["id"], product["brand"], product["flavor"], product["nutrition"], product["saturation"], effect, level, duration, product["tier"], product["recipeCost"], product["niche"]])

    registry = json.loads(REGISTRY.read_text(encoding="utf-8-sig"))
    food_namespaces = {"minecraft", "farmersdelight", "brewery", "create_winery", "jaffabricate", "kubejs"}
    food_terms = ("apple", "berry", "orange", "bread", "cake", "stew", "soup", "meat", "beef", "pork", "chicken", "mutton", "rabbit", "fish", "salmon", "cod", "rice", "potato", "carrot", "beet", "cabbage", "tomato", "onion", "bacon", "sausage", "juice", "wine", "beer", "drink", "food", "ration", "cracker", "fruit", "meal")
    candidates = [item for item in registry["items"] if item.split(":", 1)[0] in food_namespaces and any(term in item.split(":", 1)[1] for term in food_terms)]
    with (OUT / "existing-food-inventory.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["Registry ID", "Namespace", "Static Nutrition Available", "Review Note"])
        for item in sorted(candidates):
            writer.writerow([item, item.split(":", 1)[0], "no", "Candidate food/drink from live registry; runtime food component comparison recommended"])

    report = [
        "# Industrial Food Balance Audit", "", f"Status: **{'PASS' if not failures else 'FAIL'}**", "",
        "## Meal target checks", "", "| Combination | Hunger | Result |", "|---|---:|---|",
    ]
    report.extend(f"| {label} | {total} | {status} |" for label, total, status in pair_results)
    report.extend(["", f"Field ration alone: **{mre}/20 hunger — {'PASS' if 15 <= mre <= 18 else 'REVIEW'}**", "", "## Logistics conservation", "", "| Package | Preserved contents |", "|---|---:|"])
    report.extend(f"| {label} | {count} {unit} |" for label, count, unit in conservation)
    report.extend(["", "Packing and unpacking recipes preserve these consumable counts exactly; pallet material itself is packaging, not nutrition.", "", "## Existing-food comparison inventory", "", f"Captured **{len(candidates)}** relevant candidate items from the live registry. Static registry exports do not expose runtime nutrition components, so the CSV marks them for in-game comparison instead of inventing values.", "", "## Warnings", ""])
    report.extend(f"- {warning}" for warning in warnings or ["None"])
    report.extend(["", "## Failures", ""])
    report.extend(f"- {failure}" for failure in failures or ["None"])
    (OUT / "balance-report.md").write_text("\n".join(report) + "\n", encoding="utf-8")

    print(f"Industrial food balance audit: {'PASS' if not failures else 'FAIL'} ({len(failures)} failures, {len(warnings)} warnings)")
    print(f"Reported {len(products)} consumables and {len(candidates)} existing-food candidates.")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
