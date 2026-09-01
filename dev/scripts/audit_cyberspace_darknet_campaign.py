"""Validate Cyberspace/Darknet spawns and the Darknet draconic quest campaign."""

from __future__ import annotations

import json
import re
from pathlib import Path

from build_cyberspace_darknet_campaign import (
    CHAPTER, DRAGONS, INJECTOR_SECONDS, INJECTOR_UPGRADES, MEKANITES, MODIFIERS, QUESTS, RECIPES,
)


for short, (entity, weight, minimum, maximum) in MEKANITES.items():
    path = MODIFIERS / f"cyber_dimensions_mekanite_{short}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    if data["biomes"] != ["cyberspace:cyberspace_biome", "cyberspace:darknet_biome"]:
        raise SystemExit(f"Wrong Mekanite biome targets: {path}")
    expected = {"type": entity, "weight": weight, "minCount": minimum, "maxCount": maximum}
    if data["spawners"] != expected:
        raise SystemExit(f"Wrong native spawn settings: {path}")

for short, entity in DRAGONS.items():
    path = MODIFIERS / f"darknet_{short}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    if data["biomes"] != "cyberspace:darknet_biome" or data["spawners"] != {
        "type": entity, "weight": 1, "minCount": 1, "maxCount": 1
    }:
        raise SystemExit(f"Wrong Darknet dragon spawn: {path}")

text = CHAPTER.read_text(encoding="utf-8")
if len(re.findall(r'^\s*id: "5B10', text, re.MULTILINE)) != len(QUESTS):
    raise SystemExit("Quest count mismatch")
for required in ["cyberspace:darknet_dimension", "cyberspace:netcracker", *DRAGONS.values(),
                 "iceandfire:dragonsteel_fire_ingot", "iceandfire:dragonsteel_ice_ingot",
                 "iceandfire:dragonsteel_lightning_ingot", "iceandfire:iceandfire/dragon_egg",
                 "kubejs:darknet_temporal_core", "infinite_domain:darknet_time_extended",
                 *[f"kubejs:darknet_session_injector_tier_{tier}" for tier in range(1, 9)]]:
    if required not in text:
        raise SystemExit(f"Missing campaign coverage: {required}")

if INJECTOR_SECONDS != [30, 60, 120, 240, 480, 960, 1920, 3840]:
    raise SystemExit("Injector times are not the required eight doubling tiers")
if len(INJECTOR_UPGRADES) != 7:
    raise SystemExit("Injector upgrade ingredient count mismatch")
for tier in range(1, 9):
    path = RECIPES / f"darknet_session_injector_tier_{tier}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    if data["result"]["id"] != f"kubejs:darknet_session_injector_tier_{tier}":
        raise SystemExit(f"Wrong injector output: {path}")
    expected_count = 4 if tier == 1 else 1
    if data["result"].get("count", 1) != expected_count:
        raise SystemExit(f"Wrong injector output count: {path}")
    if tier > 1:
        if sum(row.count("P") for row in data["pattern"]) != 1:
            raise SystemExit(f"Injector tier does not consume exactly one prior injector: {path}")
        if data["key"]["P"]["item"] != f"kubejs:darknet_session_injector_tier_{tier - 1}":
            raise SystemExit(f"Wrong prior injector in progression recipe: {path}")

root = Path(__file__).resolve().parents[1]
core_recipe = json.loads((root / "kubejs/data/infinite_domain/recipe/darknet_temporal_core.json").read_text(encoding="utf-8"))
json.loads((root / "kubejs/data/infinite_domain/advancement/darknet_time_extended.json").read_text(encoding="utf-8"))
registered_items = set((root / "docs/registry-inventory/item-ids.txt").read_text(encoding="utf-8").splitlines())
external_ingredients = {entry["item"] for entry in core_recipe["key"].values()} | set(INJECTOR_UPGRADES) | {
    "cyberspace:graphene_coated_iron_ingot", "ae2:fluix_crystal", "ae2:logic_processor",
    "ae2:energy_cell",
}
missing_ingredients = sorted(external_ingredients - registered_items)
if missing_ingredients:
    raise SystemExit("Unregistered injector ingredients: " + ", ".join(missing_ingredients))
forbidden_ingredients = {
    "cyberspace:data_hardware", "minecraft:nether_star", "ae2:singularity",
    "ae2:cell_component_256k", "oritech:machine_core_7", "oritech:superconductor",
    "createnuclear:reactor_casing", "stellaris:desh_block", "oritech:prometheum_ingot",
    "iceandfire:dragonsteel_lightning_block", "mekanite_mobs:reinforced_end_pearl",
}
recipe_inputs = {entry["item"] for entry in core_recipe["key"].values()}
for tier in range(1, 9):
    data = json.loads((RECIPES / f"darknet_session_injector_tier_{tier}.json").read_text(encoding="utf-8"))
    recipe_inputs.update(entry["item"] for entry in data["key"].values())
forbidden_found = sorted(recipe_inputs & forbidden_ingredients)
if forbidden_found:
    raise SystemExit("Injector ladder still contains non-Overworld or late-game ingredients: " + ", ".join(forbidden_found))
runtime = (root / "kubejs/server_scripts/darknet_session_injector.js").read_text(encoding="utf-8")
for seconds in INJECTOR_SECONDS:
    if str(seconds) not in runtime:
        raise SystemExit(f"Runtime is missing injector duration {seconds}")
for required in ["DarknetTimer", "DarknetInternalTimer", "variables.markSyncDirty()", "event.item.count--"]:
    if required not in runtime:
        raise SystemExit(f"Runtime is missing behavior: {required}")
if runtime.count("Darknet Session Injectors are only usable in the Darknet.") < 8:
    raise SystemExit("Charles's wrong-dimension injector dialogue lost its message variety")
if runtime.count("No active Darknet session detected.") < 8:
    raise SystemExit("Charles's inactive-session injector dialogue lost its message variety")
for dimension in ["minecraft:overworld", "minecraft:the_nether", "minecraft:the_end", "cyberspace:cyberspace_dimension"]:
    if dimension not in runtime:
        raise SystemExit(f"Injector dialogue cannot name dimension: {dimension}")
if "times 10 1500 20" not in runtime:
    raise SystemExit("Injector rejection banner no longer remains visible for 75 seconds")

print(f"Audit passed: {len(MEKANITES)} Mekanites in both cyber dimensions, {len(DRAGONS)} Darknet dragons, {len(QUESTS)} quests, an Overworld-achievable one-to-one eight-tier injector ladder, and dimension-aware Charles rejection dialogue.")
