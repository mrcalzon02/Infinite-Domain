"""Validate the optional submarine, airship, and orbital cargo qualification line."""

from __future__ import annotations

import csv
import importlib.util
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "config/ftbquests/quests/chapters/air_sea_global_logistics.snbt"
LANG = ROOT / "config/ftbquests/quests/lang/en_us.snbt"
GENERATOR = ROOT / "scripts/generators/build_quest_expansion.js"
SIGNPOSTING = ROOT / "scripts/audit_mod_signposting.js"
ITEMS = ROOT / "docs/registry-inventory/item-ids.txt"
RECIPE_INDEX = ROOT / "docs/recipe-index/recipe-index.csv"
STARTUP = ROOT / "kubejs/startup_scripts/space_industry_catalog.js"
SPACE_RECIPES = ROOT / "kubejs/server_scripts/space_industry_recipes.js"
INTEGRATIONS = ROOT / "scripts/apply_deep_recipe_integrations.py"

ERA4 = "5510000000000001"
ERA5 = "5610000000000001"
ERA6 = "5710000000000001"
ERA7 = "5810000000000001"

EXPECTED = {
    "5E00000000000030": {
        "deps": {"5E00000000000006", ERA4},
        "items": {
            "create_submarine:electrolyzer": 1,
            "create_submarine:oxygene_diffuser": 2,
            "create_submarine:water_thruster": 2,
        },
    },
    "5E00000000000031": {"deps": {"5E00000000000030"}, "check": True},
    "5E00000000000032": {
        "deps": {"5E00000000000009", ERA4},
        "items": {
            "aeronautics_utility_objects:universal_joint_rod2": 2,
            "aeronautics_utility_objects:hydraulic_regulator": 2,
        },
    },
    "5E00000000000033": {
        "deps": {"5E0000000000000B", "5E00000000000032"},
        "check": True,
    },
    "5E00000000000034": {
        "deps": {"5E0000000000000C", "5E00000000000033", ERA5},
        "items": {
            "create_radar:radar_dish_block": 1,
            "create_aero_radar:radar_link": 2,
            "create_radar:radar_safe_zone_designator": 1,
        },
    },
    "5E00000000000035": {
        "deps": {"5E00000000000034", ERA6},
        "items": {
            "kubejs:avionics_controller": 1,
            "kubejs:navigation_unit": 1,
            "kubejs:power_distribution_unit": 1,
        },
    },
    "5E00000000000036": {
        "deps": {"5E00000000000035"},
        "items": {
            "createpropulsion:vector_thruster": 4,
            "createthrusters:thruster": 4,
        },
    },
    "5E00000000000037": {
        "deps": {"5E00000000000036", ERA7},
        "check": True,
    },
    "5E00000000000038": {
        "deps": {"5E0000000000000E", "5E00000000000037"},
        "items": {"kubejs:lunar_material_pallet": 1},
    },
    "5E00000000000039": {"deps": {"5E00000000000038"}, "check": True},
}

CHECK_IDS = {qid for qid, spec in EXPECTED.items() if spec.get("check")}
COG_IDS = {"5E00000000000032", "5E00000000000035", "5E00000000000038"}
GATEWAYS = {
    "create_radar:radar_dish_block": 3,
    "createpropulsion:vector_thruster": 3,
    "createthrusters:thruster": 3,
}
SCRIPTED_ITEMS = {
    "kubejs:avionics_controller": "seq('avionics_controller'",
    "kubejs:navigation_unit": "compact(I('navigation_unit')",
    "kubejs:power_distribution_unit": "compact(I('power_distribution_unit')",
    "kubejs:lunar_material_pallet": "['lunar_material_pallet', I('desh_titanium_laminate'), 16]",
}
MILESTONE_SYMBOLS = {
    ERA4: "milestones.era4",
    ERA5: "milestones.era5",
    ERA6: "milestones.era6",
    ERA7: "milestones.era7",
}


def quest_blocks(text: str) -> dict[str, str]:
    blocks: dict[str, str] = {}
    pattern = re.compile(r"(?ms)^\t\t\{\n(.*?)(?=^\t\t\{\n|^\t\]\n\})")
    for match in pattern.finditer(text):
        block = match.group(0)
        qid = re.search(r'^\t\t\tid:\s*"([0-9A-F]{16})"', block, re.M)
        if qid:
            blocks[qid.group(1)] = block
    return blocks


def dependencies(block: str) -> set[str]:
    match = re.search(r"dependencies:\s*\[([\s\S]*?)\]\s*\n\t\t\t", block)
    return set(re.findall(r'"([0-9A-F]{16})"', match.group(1))) if match else set()


def task_items(block: str) -> dict[str, int]:
    found: dict[str, int] = {}
    for count, item in re.findall(
        r'\{\s*(?:count:\s*(\d+)L,\s*)?item:\s*\{ count: 1, id: "([^"]+)" \},\s*id:\s*"6E[0-9A-F]+",\s*type:\s*"item"\s*\}',
        block,
    ):
        found[item] = int(count or 1)
    return found


def reward_items(block: str) -> list[str]:
    match = re.search(r"rewards:\s*\[([\s\S]*?)\]\s*\n\t\t\ttasks", block)
    return re.findall(r'item:\s*\{(?:\s*count:\s*\d+,\s*)?id:\s*"([^"]+)"', match.group(1)) if match else []


def load_integrations():
    spec = importlib.util.spec_from_file_location("deep_integrations", INTEGRATIONS)
    if spec is None or spec.loader is None:
        raise AssertionError("Could not import the curated integration authority")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    chapter_text = CHAPTER.read_text(encoding="utf-8")
    lang = LANG.read_text(encoding="utf-8-sig")
    generator = GENERATOR.read_text(encoding="utf-8")
    signposting = SIGNPOSTING.read_text(encoding="utf-8")
    startup = STARTUP.read_text(encoding="utf-8")
    scripted_recipes = SPACE_RECIPES.read_text(encoding="utf-8")
    registered = set(ITEMS.read_text(encoding="utf-8-sig").splitlines())
    blocks = quest_blocks(chapter_text)

    missing = set(EXPECTED) - set(blocks)
    assert not missing, f"Missing qualification quests: {sorted(missing)}"

    item_tasks = 0
    for qid, expected in EXPECTED.items():
        block = blocks[qid]
        assert "\n\t\t\toptional: true\n" in block, f"{qid} is not optional"
        assert dependencies(block) == expected["deps"], f"{qid} dependency drift"
        assert task_items(block) == expected.get("items", {}), f"{qid} item objective drift"
        item_tasks += len(expected.get("items", {}))
        if expected.get("check"):
            assert 'type: "checkmark"' in block, f"{qid} lost its witnessed procedure"
            assert not reward_items(block), f"{qid} rewards self-certification"
        elif qid in COG_IDS:
            assert reward_items(block) == ["numismatics:cog"], f"{qid} modest reward drift"
        else:
            assert not reward_items(block), f"{qid} gained an unplanned reward"

        assert re.search(rf'^\tquest\.{qid}\.title:', lang, re.M), f"{qid} title missing"
        assert re.search(rf'^\tquest\.{qid}\.quest_desc:', lang, re.M), f"{qid} description missing"
        generator_lines = [line for line in generator.splitlines() if f"id: '{qid}'" in line]
        assert len(generator_lines) == 1, f"{qid} is not uniquely owned by the generator"
        source_line = generator_lines[0]
        assert "chain: false" in source_line and "optional: true" in source_line, (
            f"{qid} generator optionality drift"
        )
        for item in expected.get("items", {}):
            assert f"'{item}'" in source_line, f"{qid} generator lost objective {item}"
        for dependency in expected["deps"]:
            token = MILESTONE_SYMBOLS.get(dependency, f"'{dependency}'")
            assert token in source_line, f"{qid} generator lost dependency {dependency}"
        if expected.get("check"):
            assert "check(" in source_line, f"{qid} generator lost its witnessed procedure"

    for qid in CHECK_IDS:
        tid = "6E" + qid[2:]
        assert re.search(rf'^\ttask\.{tid}\.title:', lang, re.M), f"{tid} task title missing"

    new_ids = set(EXPECTED)
    for qid, block in blocks.items():
        if qid not in new_ids:
            leaked = dependencies(block) & new_ids
            assert not leaked, f"Core quest {qid} depends on optional qualification work: {sorted(leaked)}"

    objective_items = {item for spec in EXPECTED.values() for item in spec.get("items", {})}
    for item in objective_items - set(SCRIPTED_ITEMS):
        assert item in registered, f"Objective item is absent from installed registry: {item}"
    for item, recipe_token in SCRIPTED_ITEMS.items():
        short = item.split(":", 1)[1]
        assert f"['{short}'" in startup, f"Project item is not registered: {item}"
        assert recipe_token in scripted_recipes, f"Project item has no scripted source: {item}"

    with RECIPE_INDEX.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    static_items = objective_items - set(SCRIPTED_ITEMS)
    for item in static_items:
        sources = [
            row for row in rows
            if row.get("enabled", "").lower() == "true"
            and item in {part.strip() for part in row.get("output_ids", "").split(";")}
        ]
        assert sources, f"No enabled installed recipe for objective item: {item}"

    integrations = load_integrations()
    for output, minimum_foreign_namespaces in GATEWAYS.items():
        authored = integrations.RECIPES[output]
        output_namespace = output.split(":", 1)[0]
        ingredient_namespaces = {
            value["item"].split(":", 1)[0]
            for value in authored["key"].values()
            if value["item"].split(":", 1)[0] not in {"minecraft", output_namespace}
        }
        assert len(ingredient_namespaces) >= minimum_foreign_namespaces, (
            f"{output} has only {sorted(ingredient_namespaces)} foreign industries"
        )
        output_rows = [
            row for row in rows
            if row.get("enabled", "").lower() == "true"
            and output in {part.strip() for part in row.get("output_ids", "").split(";")}
        ]
        assert output_rows, f"No effective recipe IDs found for {output}"
        for row in output_rows:
            path = ROOT / row["recommended_override_path"]
            assert path.exists(), f"Missing non-bypassable override: {path.relative_to(ROOT)}"
            assert json.loads(path.read_text(encoding="utf-8-sig")) == authored, (
                f"Gateway override drift: {path.relative_to(ROOT)}"
            )

    named_systems = [
        "Create: Deep Seas",
        "Create Aeronautics",
        "Create Aeronautics: Automated Logistics",
        "Create Aeronautics: Transmission & Linkage",
        "Create: Radars",
        "Create Aero Radars",
        "Create Propulsion: Simulated",
        "Create Aeronautics: Gadgets & Gizmos",
    ]
    for name in named_systems:
        assert name in lang, f"Player-facing signposting missing: {name}"
        assert name in generator, f"Owning generator omits player-facing name: {name}"
        assert name in signposting, f"Signposting audit omits: {name}"
    assert "q.task.type !== 'checkmark'" in generator, "Generator can reward checkmarks"

    print(
        "Vehicle qualification audit passed: "
        f"{len(EXPECTED)} optional quests, {item_tasks} item tasks, {len(CHECK_IDS)} witnessed procedures, "
        f"{len(GATEWAYS)} non-bypassable multi-industry gateways, and {len(named_systems)} named systems."
    )


if __name__ == "__main__":
    main()
