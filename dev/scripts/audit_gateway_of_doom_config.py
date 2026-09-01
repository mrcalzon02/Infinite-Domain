"""Validate that passive Gateway events are confined to Cyberspace."""

import json
from pathlib import Path


root = Path(__file__).resolve().parents[1]
path = root / "config/gateway_of_doom.json"
data = json.loads(path.read_text(encoding="utf-8"))
automatic = data["automaticGateways"]

if not automatic["enabled"]:
    raise SystemExit("Gateway of Doom automatic scheduler is disabled")

enabled_rules = [rule["id"] for rule in automatic["rules"] if rule["enabled"]]
if enabled_rules != ["cyberspace_timer"]:
    raise SystemExit("Unexpected enabled automatic rules: " + ", ".join(enabled_rules))

expected = {"overworld_exploration", "nether_timer", "end_timer", "cyberspace_timer"}
actual = {rule["id"] for rule in automatic["rules"]}
if actual != expected:
    raise SystemExit(f"Automatic rule roster changed: expected {sorted(expected)}, found {sorted(actual)}")

if not data["profiles"]:
    raise SystemExit("Manual Gateway of Doom profiles were unexpectedly removed")

rule = next(rule for rule in automatic["rules"] if rule["id"] == "cyberspace_timer")
if rule["dimensions"] != ["cyberspace:cyberspace_dimension"]:
    raise SystemExit("Cyberspace automatic rule leaks into other dimensions")
if rule["triggerMode"] != "timer" or rule["profileId"] != "hard":
    raise SystemExit("Cyberspace automatic rule lost its timed hard-profile settings")

recipe_dir = root / "kubejs/data/gateway_of_doom/recipe"
registered_items = set((root / "docs/registry-inventory/item-ids.txt").read_text(encoding="utf-8").splitlines())
for tier in range(1, 6):
    recipe = json.loads((recipe_dir / f"portal_ward_{tier}.json").read_text(encoding="utf-8"))
    if recipe["result"]["id"] != f"gateway_of_doom:portal_ward_{tier}":
        raise SystemExit(f"Portal Ward {tier} has the wrong output")
    ingredients = [entry["item"] for entry in recipe["key"].values()]
    cyberware = [item for item in ingredients if item.startswith("cyber_ware_port:")]
    if not cyberware:
        raise SystemExit(f"Portal Ward {tier} lacks Cyberware Port integration")
    missing = sorted(set(ingredients) - registered_items)
    if missing:
        raise SystemExit(f"Portal Ward {tier} has missing ingredients: {', '.join(missing)}")
    if tier > 1 and f"gateway_of_doom:portal_ward_{tier - 1}" not in ingredients:
        raise SystemExit(f"Portal Ward {tier} does not consume the previous tier")

eye_recipes = {
    "blue": ("Easy", "cyberspace:data_hardware", "gateway_of_doom:portal_ward_1"),
    "red": ("Medium", "cyberspace:virtual_machine_core", "gateway_of_doom:portal_ward_2"),
    "violet": ("Hard", "cyberspace:quantum_core", "gateway_of_doom:portal_ward_3"),
}
for color, (difficulty, cyberspace_part, ward) in eye_recipes.items():
    eye_id = f"gateway_of_doom:devil_eye_{color}"
    eye_recipe = json.loads((recipe_dir / f"devil_eye_{color}.json").read_text(encoding="utf-8"))
    if eye_recipe["result"]["id"] != eye_id:
        raise SystemExit(f"The {difficulty} Devil Eye recipe has the wrong output")
    eye_ingredients = [entry["item"] for entry in eye_recipe["key"].values()]
    if cyberspace_part not in eye_ingredients:
        raise SystemExit(f"Devil Eye ({difficulty}) lost its required {cyberspace_part}")
    if ward not in eye_ingredients:
        raise SystemExit(f"Devil Eye ({difficulty}) lost its matching Portal Ward")
    if not any(item.startswith("cyber_ware_port:") for item in eye_ingredients):
        raise SystemExit(f"Devil Eye ({difficulty}) lacks Cyberware Port integration")
    missing_eye_ingredients = sorted(set(eye_ingredients) - registered_items)
    if missing_eye_ingredients:
        raise SystemExit(f"Devil Eye ({difficulty}) has missing ingredients: " + ", ".join(missing_eye_ingredients))

guard_path = root / "kubejs/server_scripts/gateway_of_doom_dimension_lock.js"
guard = guard_path.read_text(encoding="utf-8")
expected_eyes = {
    "gateway_of_doom:devil_eye",
    "gateway_of_doom:devil_eye_blue",
    "gateway_of_doom:devil_eye_red",
    "gateway_of_doom:devil_eye_violet",
}
missing_guards = sorted(eye for eye in expected_eyes if eye not in guard)
if missing_guards:
    raise SystemExit("Dimension guard omits Devil Eyes: " + ", ".join(missing_guards))
if "dimension === 'cyberspace:cyberspace_dimension'" not in guard or "event.cancel()" not in guard:
    raise SystemExit("Devil Eye dimension guard no longer enforces the Cyberspace-only rule")
if guard.count("This is only usable in Cyberspace.") < 6:
    raise SystemExit("Charles's Devil Eye rejection dialogue lost its message variety")
if "times 10 1500 20" not in guard:
    raise SystemExit("Devil Eye rejection banner no longer remains visible for 75 seconds")

print("Audit passed: passive and player-triggered gateways are Cyberspace-only; Charles has varied rejection dialogue; all three Devil Eyes have tiered recipes; the Hard Eye requires a Quantum Core; all five Portal Wards require Cyberware Port parts.")
