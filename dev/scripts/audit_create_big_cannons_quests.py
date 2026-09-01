#!/usr/bin/env python3
"""Validate the optional Create Big Cannons doctrine, recipes, and safety contract."""

from __future__ import annotations

import csv
import importlib.util
import json
import re
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CHAPTER = ROOT / "config/ftbquests/quests/chapters/create_big_cannons_doctrine.snbt"
CHAPTER_DIR = CHAPTER.parent
LANG = ROOT / "config/ftbquests/quests/lang/en_us.snbt"
GENERATOR = ROOT / "dev/scripts/generators/build_create_big_cannons_quests.js"
SIGNPOSTING = ROOT / "dev/scripts/audit_mod_signposting.js"
ITEMS = ROOT / "dev/docs/registry-inventory/item-ids.txt"
RECIPE_INDEX = ROOT / "dev/docs/recipe-index/recipe-index.csv"
INTEGRATIONS = ROOT / "dev/scripts/apply_deep_recipe_integrations.py"

ERA3 = "5410000000000001"
ERA4 = "5510000000000001"

EXPECTED = {
    "6F10000000000001": {
        "deps": {ERA3},
        "items": {
            "createbigcannons:basin_foundry_lid": 1,
            "createbigcannons:casting_sand": 64,
            "createbigcannons:small_cast_mould": 2,
            "createbigcannons:sliding_breech_cast_mould": 1,
        },
    },
    "6F10000000000002": {
        "deps": {"6F10000000000001"},
        "items": {"createbigcannons:cannon_drill": 1, "createbigcannons:cannon_builder": 1},
    },
    "6F10000000000003": {
        "deps": {"6F10000000000002"},
        "items": {
            "createbigcannons:cast_iron_cannon_barrel": 2,
            "createbigcannons:cast_iron_cannon_chamber": 1,
            "createbigcannons:cast_iron_sliding_breech": 1,
            "createbigcannons:block_armor_inspection_tool": 1,
        },
    },
    "6F10000000000004": {"deps": {"6F10000000000003"}, "check": True},
    "6F10000000000005": {
        "deps": {"6F10000000000004"},
        "items": {"createbigcannons:cast_iron_sliding_breechblock": 1},
    },
    "6F10000000000006": {
        "deps": {"6F10000000000005"},
        "items": {
            "createbigcannons:cannon_loader": 1,
            "createbigcannons:ram_rod": 1,
            "createbigcannons:worm": 1,
        },
    },
    "6F10000000000007": {
        "deps": {"6F10000000000005"},
        "items": {"createbigcannons:fixed_cannon_mount": 1, "createbigcannons:cannon_carriage": 1},
    },
    "6F10000000000008": {
        "deps": {"6F10000000000006", "6F10000000000007"},
        "items": {"createbigcannons:solid_shot": 8},
    },
    "6F10000000000009": {
        "deps": {"6F10000000000008"},
        "items": {"createbigcannons:powder_charge": 8},
    },
    "6F1000000000000A": {"deps": {"6F10000000000009"}, "check": True},
    "6F1000000000000B": {"deps": {"6F1000000000000A"}, "check": True},
    "6F1000000000000C": {
        "deps": {"6F1000000000000B", ERA4},
        "items": {"createbigcannons:cannon_mount": 1, "createbigcannons:cannon_mount_extension": 2},
    },
    "6F1000000000000D": {
        "deps": {"6F1000000000000B"},
        "items": {"createbigcannons:smoke_shell": 4, "createbigcannons:timed_fuze": 4},
    },
    "6F1000000000000E": {
        "deps": {"6F1000000000000B", ERA4},
        "items": {
            "createbigcannons:cast_iron_autocannon_barrel": 1,
            "createbigcannons:cast_iron_autocannon_breech": 1,
            "createbigcannons:cast_iron_autocannon_recoil_spring": 1,
            "createbigcannons:autocannon_ammo_container": 1,
            "createbigcannons:ap_autocannon_round": 32,
        },
    },
    "6F1000000000000F": {
        "deps": {"6F1000000000000C", "6F1000000000000D", "6F1000000000000E"},
        "check": True,
    },
}

CHECK_IDS = {qid for qid, spec in EXPECTED.items() if spec.get("check")}
COG_IDS = {"6F10000000000003", "6F10000000000007", "6F1000000000000C", "6F1000000000000E"}
SPECIAL_ACQUISITION = {
    "createbigcannons:cast_iron_cannon_barrel": (
        "data/createbigcannons/createbigcannons/block_recipes/cast_iron_cannon_barrel.json",
        "createbigcannons:cast_iron_cannon_barrel",
    ),
    "createbigcannons:cast_iron_cannon_chamber": (
        "data/createbigcannons/createbigcannons/block_recipes/cast_iron_cannon_chamber.json",
        "createbigcannons:cast_iron_cannon_chamber",
    ),
    "createbigcannons:cast_iron_sliding_breech": (
        "data/createbigcannons/createbigcannons/block_recipes/incomplete_cast_iron_sliding_breech.json",
        "createbigcannons:incomplete_cast_iron_sliding_breech",
    ),
    "createbigcannons:cast_iron_autocannon_barrel": (
        "data/createbigcannons/createbigcannons/block_recipes/cast_iron_autocannon_barrel.json",
        "createbigcannons:cast_iron_autocannon_barrel",
    ),
    "createbigcannons:cast_iron_autocannon_breech": (
        "data/createbigcannons/createbigcannons/block_recipes/incomplete_cast_iron_autocannon_breech.json",
        "createbigcannons:incomplete_cast_iron_autocannon_breech",
    ),
    "createbigcannons:cast_iron_autocannon_recoil_spring": (
        "data/createbigcannons/createbigcannons/block_recipes/incomplete_cast_iron_autocannon_recoil_spring.json",
        "createbigcannons:incomplete_cast_iron_autocannon_recoil_spring",
    ),
}
ASSEMBLY_COMPONENTS = {
    "createbigcannons:cast_iron_sliding_breechblock",
    "createbigcannons:cast_iron_autocannon_breech_extractor",
    "createbigcannons:recoil_spring",
}
GATEWAYS = {
    "createbigcannons:basin_foundry_lid": 3,
    "createbigcannons:cannon_mount": 3,
}
PONDERS = {
    "assets/createbigcannons/ponder/cannon_crafting/basin_foundry.nbt",
    "assets/createbigcannons/ponder/cannon_crafting/cannon_casting.nbt",
    "assets/createbigcannons/ponder/cannon_crafting/cannon_boring.nbt",
    "assets/createbigcannons/ponder/cannon_crafting/cannon_building.nbt",
    "assets/createbigcannons/ponder/cannon_loader/loading_big_cannons.nbt",
    "assets/createbigcannons/ponder/cannon_loader/handloading_tools.nbt",
    "assets/createbigcannons/ponder/cannon_mount/firing_big_cannons.nbt",
    "assets/createbigcannons/ponder/munitions/cannon_loads.nbt",
    "assets/createbigcannons/ponder/munitions/wet_ammo_storage.nbt",
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
    for count, item_id in re.findall(
        r'\{\s*(?:count:\s*(\d+)L,\s*)?item:\s*\{ count: 1, id: "([^"]+)" \},\s*id:\s*"7F[0-9A-F]+",\s*type:\s*"item"\s*\}',
        block,
    ):
        found[item_id] = int(count or 1)
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
    chapter_text = CHAPTER.read_text(encoding="utf-8-sig")
    lang = LANG.read_text(encoding="utf-8-sig")
    generator = GENERATOR.read_text(encoding="utf-8-sig")
    signposting = SIGNPOSTING.read_text(encoding="utf-8-sig")
    registered = set(ITEMS.read_text(encoding="utf-8-sig").splitlines())
    blocks = quest_blocks(chapter_text)

    assert 'id: "6F50000000000002"' in chapter_text, "Chapter ID drift"
    assert 'group: "4E65FAAC62D57D4A"' in chapter_text, "Chapter group drift"
    assert 'icon: "createbigcannons:cannon_mount"' in chapter_text, "Chapter icon drift"
    assert 'chapter.6F50000000000002.title: "Create Big Cannons Doctrine"' in lang
    assert 'chapter.6F50000000000002.subtitle: "Foundry discipline, proof loading and settlement defense"' in lang
    assert set(blocks) == set(EXPECTED), f"Doctrine quest inventory drift: {sorted(set(blocks) ^ set(EXPECTED))}"
    assert 'type: "structure"' not in chapter_text, "Defense doctrine must not own structure discovery or spawning"

    item_tasks = 0
    for qid, expected in EXPECTED.items():
        block = blocks[qid]
        assert "\n\t\t\toptional: true\n" in block, f"{qid} is not optional"
        assert dependencies(block) == expected["deps"], f"{qid} dependency drift"
        assert task_items(block) == expected.get("items", {}), f"{qid} item objective drift"
        item_tasks += len(expected.get("items", {}))
        if expected.get("check"):
            assert 'type: "checkmark"' in block, f"{qid} lost its witnessed procedure"
        rewards = reward_items(block)
        if qid in COG_IDS:
            assert rewards == ["numismatics:cog"], f"{qid} modest reward drift"
        else:
            assert not rewards, f"{qid} gained an unplanned reward"
        assert re.search(rf'^\tquest\.{qid}\.title:', lang, re.M), f"{qid} title missing"
        assert re.search(rf'^\tquest\.{qid}\.quest_desc:', lang, re.M), f"{qid} description missing"

    for qid in CHECK_IDS:
        task_id = "7F1" + qid[3:]
        assert re.search(rf'^\ttask\.{task_id}\.title:', lang, re.M), f"{task_id} title missing"
        assert not reward_items(blocks[qid]), f"{qid} rewards self-certification"

    all_blocks: dict[str, str] = {}
    for chapter in CHAPTER_DIR.glob("*.snbt"):
        all_blocks.update(quest_blocks(chapter.read_text(encoding="utf-8-sig")))
    for qid, block in all_blocks.items():
        if qid not in EXPECTED:
            leaked = dependencies(block) & set(EXPECTED)
            assert not leaked, f"Core quest {qid} depends on optional artillery work: {sorted(leaked)}"

    objective_items = {item_id for spec in EXPECTED.values() for item_id in spec.get("items", {})}
    missing_items = objective_items - registered
    assert not missing_items, f"Objective items are absent from installed registry: {sorted(missing_items)}"

    with RECIPE_INDEX.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    indexed_outputs = {
        part.strip()
        for row in rows
        if row.get("enabled", "").lower() == "true"
        for part in row.get("output_ids", "").split(";")
    }
    ordinary_items = objective_items - set(SPECIAL_ACQUISITION)
    assert ordinary_items <= indexed_outputs, f"No enabled recipe for: {sorted(ordinary_items - indexed_outputs)}"
    assert ASSEMBLY_COMPONENTS <= indexed_outputs, f"Missing special assembly components: {sorted(ASSEMBLY_COMPONENTS - indexed_outputs)}"

    jars = list((ROOT / "mods").glob("createbigcannons-*.jar"))
    assert len(jars) == 1, f"Expected one installed Create Big Cannons JAR, found {jars}"
    with zipfile.ZipFile(jars[0]) as archive:
        names = set(archive.namelist())
        assert PONDERS <= names, f"Missing operating Ponders: {sorted(PONDERS - names)}"
        for item_id, (entry, expected_result) in SPECIAL_ACQUISITION.items():
            assert entry in names, f"Missing special acquisition path for {item_id}: {entry}"
            payload = json.loads(archive.read(entry))
            assert payload.get("type") == "createbigcannons:drill_boring", f"Unexpected block recipe type: {entry}"
            assert payload.get("result") == expected_result, f"Unexpected block recipe result: {entry}"

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
            assert json.loads(path.read_text(encoding="utf-8-sig")) == authored, f"Gateway override drift: {path}"

    assert "Create Big Cannons" in generator, "Generator omits player-facing mod name"
    assert "Create Big Cannons" in signposting, "Signposting audit omits Create Big Cannons"
    for item_id in objective_items:
        assert item_id in generator, f"Generator lost objective {item_id}"

    print(
        "Create Big Cannons doctrine audit passed: "
        f"{len(EXPECTED)} optional quests, {item_tasks} item tasks, {len(CHECK_IDS)} witnessed procedures, "
        f"{len(PONDERS)} installed Ponders, {len(SPECIAL_ACQUISITION)} special-process outputs, "
        f"and {len(GATEWAYS)} multi-industry gateways."
    )


if __name__ == "__main__":
    main()
