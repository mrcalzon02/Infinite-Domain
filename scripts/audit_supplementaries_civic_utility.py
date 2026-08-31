#!/usr/bin/env python3
"""Validate the optional Supplementaries civic-utility progression contract."""

from __future__ import annotations

import csv
import importlib.util
import json
import re
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHAPTER = ROOT / "config/ftbquests/quests/chapters/supplementaries_civic_utility.snbt"
CHAPTER_DIR = CHAPTER.parent
LANG = ROOT / "config/ftbquests/quests/lang/en_us.snbt"
GENERATOR = ROOT / "scripts/generators/build_supplementaries_civic_utility.js"
SIGNPOSTING = ROOT / "scripts/audit_mod_signposting.js"
ITEMS = ROOT / "docs/registry-inventory/item-ids.txt"
RECIPE_INDEX = ROOT / "docs/recipe-index/recipe-index.csv"
INTEGRATIONS = ROOT / "scripts/apply_deep_recipe_integrations.py"
CONFIG = ROOT / "config/supplementaries-common.toml"

ERA1 = "4FC0C1C678C71891"
ERA2 = "5210000000000001"
ERA4 = "5410000000000001"
ERA5 = "5510000000000001"
SHULKER_FREIGHT = "5E0000000000001D"

EXPECTED = {
    "6F40000000000001": {
        "deps": {ERA1},
        "items": {"supplementaries:sack": 4, "supplementaries:rope": 32},
    },
    "6F40000000000002": {
        "deps": {"6F40000000000001"},
        "items": {"supplementaries:pulley_block": 2},
    },
    "6F40000000000003": {"deps": {"6F40000000000002"}, "check": True},
    "6F40000000000004": {
        "deps": {"6F40000000000001"},
        "items": {
            "supplementaries:jar": 4,
            "supplementaries:item_shelf": 8,
            "supplementaries:lunch_basket": 2,
        },
    },
    "6F40000000000005": {
        "deps": {"6F40000000000004"},
        "items": {"supplementaries:faucet": 2},
    },
    "6F40000000000006": {
        "deps": {"6F40000000000004"},
        "items": {
            "supplementaries:way_sign_oak": 8,
            "supplementaries:notice_board": 2,
            "supplementaries:blackboard": 2,
        },
    },
    "6F40000000000007": {
        "deps": {
            "6F40000000000003",
            "6F40000000000005",
            "6F40000000000006",
        },
        "check": True,
    },
    "6F40000000000008": {
        "deps": {"6F40000000000007", ERA2},
        "items": {
            "supplementaries:bellows": 2,
            "supplementaries:turn_table": 2,
            "supplementaries:dispenser_minecart": 2,
        },
    },
    "6F40000000000009": {
        "deps": {"6F40000000000008"},
        "items": {
            "supplementaries:wind_vane": 2,
            "supplementaries:altimeter": 2,
            "supplementaries:hourglass": 2,
        },
    },
    "6F4000000000000A": {
        "deps": {"6F40000000000009"},
        "items": {"supplementaries:redstone_illuminator": 8},
    },
    "6F4000000000000B": {
        "deps": {"6F4000000000000A", ERA4},
        "items": {"supplementaries:relayer": 4},
    },
    "6F4000000000000C": {
        "deps": {"6F4000000000000B", ERA5},
        "items": {
            "supplementaries:speaker_block": 2,
            "supplementaries:notice_board": 1,
        },
    },
    "6F4000000000000D": {
        "deps": {"6F40000000000007", SHULKER_FREIGHT},
        "items": {"supplementaries:safe": 1, "supplementaries:key": 2},
    },
    "6F4000000000000E": {
        "deps": {
            "6F4000000000000B",
            "6F4000000000000C",
            "6F4000000000000D",
        },
        "check": True,
    },
}

CHECK_IDS = {qid for qid, spec in EXPECTED.items() if spec.get("check")}
COG_IDS = {
    "6F40000000000002",
    "6F40000000000004",
    "6F40000000000008",
    "6F4000000000000B",
    "6F4000000000000D",
}
GATEWAYS = {
    "supplementaries:relayer": 3,
    "supplementaries:speaker_block": 3,
}
SPECIAL_ACQUISITION = {"supplementaries:safe"}
JAR_EVIDENCE = {
    "data/supplementaries/recipe/safe.json",
    "net/mehvahdjukaar/supplementaries/common/block/blocks/PulleyBlock.class",
    "net/mehvahdjukaar/supplementaries/common/block/blocks/RelayerBlock.class",
    "net/mehvahdjukaar/supplementaries/common/block/blocks/SpeakerBlock.class",
    "net/mehvahdjukaar/supplementaries/common/block/blocks/SafeBlock.class",
    "net/mehvahdjukaar/supplementaries/common/entities/dispenser_minecart/DispenserMinecartEntity.class",
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
    config = CONFIG.read_text(encoding="utf-8-sig")
    registered = set(ITEMS.read_text(encoding="utf-8-sig").splitlines())
    blocks = quest_blocks(chapter_text)

    assert 'id: "6F50000000000004"' in chapter_text, "Chapter ID drift"
    assert 'group: "4E65FAAC62D57D4A"' in chapter_text, "Chapter group drift"
    assert 'icon: "supplementaries:relayer"' in chapter_text, "Chapter icon drift"
    assert 'chapter.6F50000000000004.title: "Supplementaries Civic Utility"' in lang
    assert (
        'chapter.6F50000000000004.subtitle: "Rigging, public stores and accountable settlement services"'
        in lang
    )
    assert set(blocks) == set(EXPECTED), f"Civic quest inventory drift: {sorted(set(blocks) ^ set(EXPECTED))}"
    assert 'type: "structure"' not in chapter_text
    assert 'type: "biome"' not in chapter_text
    assert 'type: "dimension"' not in chapter_text
    assert 'type: "advancement"' not in chapter_text
    assert "commandForStructure" not in generator and "structure_map" not in generator

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
        task_id = "7F4" + qid[3:]
        assert re.search(rf'^\ttask\.{task_id}\.title:', lang, re.M), f"{task_id} title missing"
        assert not reward_items(blocks[qid]), f"{qid} rewards self-certification"

    all_blocks: dict[str, str] = {}
    for chapter in CHAPTER_DIR.glob("*.snbt"):
        all_blocks.update(quest_blocks(chapter.read_text(encoding="utf-8-sig")))
    for qid, block in all_blocks.items():
        if qid not in EXPECTED:
            leaked = dependencies(block) & set(EXPECTED)
            assert not leaked, f"Core quest {qid} depends on optional civic work: {sorted(leaked)}"

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
    ordinary_items = objective_items - SPECIAL_ACQUISITION
    assert ordinary_items <= indexed_outputs, f"No enabled recipe for: {sorted(ordinary_items - indexed_outputs)}"

    jars = list((ROOT / "mods").glob("supplementaries-*.jar"))
    assert len(jars) == 1, f"Expected one installed Supplementaries JAR, found {jars}"
    with zipfile.ZipFile(jars[0]) as archive:
        names = set(archive.namelist())
        assert JAR_EVIDENCE <= names, f"Installed civic feature evidence missing: {sorted(JAR_EVIDENCE - names)}"
        safe_recipe = json.loads(archive.read("data/supplementaries/recipe/safe.json"))
        assert safe_recipe.get("type") == "supplementaries:safe"
        assert safe_recipe.get("shulker", {}).get("tag") == "c:shulker_boxes"
        assert safe_recipe.get("ingot", {}).get("item") == "minecraft:netherite_ingot"

    for token in (
        "continuous_retraction = true",
        "cooperative_pulleys = true",
        "pull_limit = 8",
        "narrator_enabled = true",
        "max_text = 32",
        "range = 64",
        "adjust_projectile_angle = true",
        "drink_from_jar = false",
        "drink_from_jar_item = false",
    ):
        assert token in config, f"Supplementaries operating/config contract drift: {token}"

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
            row
            for row in rows
            if row.get("enabled", "").lower() == "true"
            and output in {part.strip() for part in row.get("output_ids", "").split(";")}
        ]
        assert output_rows, f"No effective recipe IDs found for {output}"
        for row in output_rows:
            path = ROOT / row["recommended_override_path"]
            assert path.exists(), f"Missing non-bypassable override: {path.relative_to(ROOT)}"
            assert json.loads(path.read_text(encoding="utf-8-sig")) == authored, f"Gateway override drift: {path}"

    assert "Supplementaries" in generator, "Generator omits player-facing mod name"
    assert "Supplementaries" in signposting, "Signposting audit omits Supplementaries"
    assert "does not spawn, locate, unlock, or claim" in generator
    assert "quest-triggered placement" in generator
    for item_id in objective_items:
        assert item_id in generator, f"Generator lost objective {item_id}"

    print(
        "Supplementaries civic utility audit passed: "
        f"{len(EXPECTED)} optional quests, {item_tasks} item tasks, "
        f"{len(CHECK_IDS)} witnessed procedures, {len(COG_IDS)} restrained Cog rewards, "
        f"{len(GATEWAYS)} multi-industry gateways, and no progression-owned worldgen."
    )


if __name__ == "__main__":
    main()
