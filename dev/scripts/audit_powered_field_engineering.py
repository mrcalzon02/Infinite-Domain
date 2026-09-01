#!/usr/bin/env python3
"""Validate the optional Mining Gadgets / Building Gadgets field-engineering contract."""

from __future__ import annotations

import csv
import importlib.util
import json
import re
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CHAPTER = ROOT / "config/ftbquests/quests/chapters/powered_field_engineering.snbt"
CHAPTER_DIR = CHAPTER.parent
LANG = ROOT / "config/ftbquests/quests/lang/en_us.snbt"
GENERATOR = ROOT / "dev/scripts/generators/build_powered_field_engineering.js"
SIGNPOSTING = ROOT / "dev/scripts/audit_mod_signposting.js"
ITEMS = ROOT / "dev/docs/registry-inventory/item-ids.txt"
RECIPE_INDEX = ROOT / "dev/docs/recipe-index/recipe-index.csv"
INTEGRATIONS = ROOT / "dev/scripts/apply_deep_recipe_integrations.py"
BUILDING_CONFIG = ROOT / "config/buildinggadgets2-common.toml"
MINING_CONFIG = ROOT / "config/mininggadgets-common.toml"
CHARGING_CONFIG = ROOT / "config/charginggadgets-server.toml"

ERA5 = "5510000000000001"
ERA6 = "5610000000000001"

EXPECTED = {
    "6F60000000000001": {
        "deps": {ERA5},
        "items": {
            "mininggadgets:modificationtable": 1,
            "buildinggadgets2:template_manager": 1,
            "charginggadgets:charging_station": 1,
        },
    },
    "6F60000000000002": {
        "deps": {"6F60000000000001"},
        "items": {"mininggadgets:mininggadget": 1},
    },
    "6F60000000000003": {"deps": {"6F60000000000002"}, "check": True},
    "6F60000000000004": {
        "deps": {"6F60000000000002"},
        "items": {
            "mininggadgets:upgrade_battery_1": 1,
            "mininggadgets:upgrade_battery_2": 1,
            "mininggadgets:upgrade_battery_3": 1,
        },
    },
    "6F60000000000005": {
        "deps": {"6F60000000000002"},
        "items": {
            "mininggadgets:upgrade_efficiency_3": 1,
            "mininggadgets:upgrade_magnet": 1,
            "mininggadgets:upgrade_light_placer": 1,
        },
    },
    "6F60000000000006": {
        "deps": {"6F60000000000003", "6F60000000000005"},
        "items": {
            "mininggadgets:upgrade_fortune_3": 1,
            "mininggadgets:upgrade_silk": 1,
        },
    },
    "6F60000000000007": {
        "deps": {"6F60000000000005"},
        "items": {
            "mininggadgets:upgrade_void_junk": 1,
            "mininggadgets:upgrade_freezing": 1,
        },
    },
    "6F60000000000008": {
        "deps": {"6F60000000000004", "6F60000000000006", "6F60000000000007"},
        "check": True,
    },
    "6F60000000000009": {
        "deps": {"6F60000000000008", ERA6},
        "items": {
            "mininggadgets:upgrade_range_3": 1,
            "mininggadgets:upgrade_size_2": 1,
        },
    },
    "6F6000000000000A": {"deps": {"6F60000000000009"}, "check": True},
    "6F6000000000000B": {
        "deps": {"6F60000000000001"},
        "items": {"buildinggadgets2:gadget_building": 1},
    },
    "6F6000000000000C": {
        "deps": {"6F6000000000000B"},
        "items": {
            "buildinggadgets2:gadget_exchanging": 1,
            "buildinggadgets2:gadget_destruction": 1,
        },
    },
    "6F6000000000000D": {
        "deps": {"6F6000000000000B"},
        "items": {"buildinggadgets2:gadget_copy_paste": 1},
    },
    "6F6000000000000E": {
        "deps": {"6F6000000000000D", ERA6},
        "items": {"buildinggadgets2:gadget_cut_paste": 1},
    },
    "6F6000000000000F": {
        "deps": {
            "6F6000000000000A",
            "6F6000000000000C",
            "6F6000000000000D",
            "6F6000000000000E",
        },
        "check": True,
    },
}

CHECK_IDS = {qid for qid, spec in EXPECTED.items() if spec.get("check")}
COG_IDS = {
    "6F60000000000002",
    "6F60000000000004",
    "6F60000000000009",
    "6F6000000000000B",
    "6F6000000000000D",
}
GATEWAYS = {
    "mininggadgets:mininggadget": 5,
    "buildinggadgets2:gadget_building": 5,
    "buildinggadgets2:gadget_exchanging": 4,
    "buildinggadgets2:gadget_destruction": 5,
    "buildinggadgets2:gadget_copy_paste": 5,
    "buildinggadgets2:gadget_cut_paste": 5,
    "charginggadgets:charging_station": 4,
}
BUILDING_JAR_EVIDENCE = {
    "com/direwolf20/buildinggadgets2/common/blocks/TemplateManager.class",
    "com/direwolf20/buildinggadgets2/common/items/GadgetBuilding.class",
    "com/direwolf20/buildinggadgets2/common/items/GadgetExchanger.class",
    "com/direwolf20/buildinggadgets2/common/items/GadgetDestruction.class",
    "com/direwolf20/buildinggadgets2/common/items/GadgetCopyPaste.class",
    "com/direwolf20/buildinggadgets2/common/items/GadgetCutPaste.class",
    "com/direwolf20/buildinggadgets2/common/network/handler/PacketUndo.class",
}
MINING_JAR_EVIDENCE = {
    "com/direwolf20/mininggadgets/common/items/MiningGadget.class",
    "com/direwolf20/mininggadgets/common/items/UpgradeCard.class",
    "com/direwolf20/mininggadgets/common/blocks/ModificationTable.class",
    "com/direwolf20/mininggadgets/common/network/handler/PacketToggleFilters.class",
    "com/direwolf20/mininggadgets/common/network/handler/PacketChangeMiningSize.class",
    "com/direwolf20/mininggadgets/common/network/handler/PacketChangeRange.class",
}
CHARGING_JAR_EVIDENCE = {
    "com/direwolf20/charginggadgets/blocks/chargingstation/ChargingStationBlock.class",
    "com/direwolf20/charginggadgets/blocks/chargingstation/ChargingStationContainer.class",
    "com/direwolf20/charginggadgets/blocks/chargingstation/ChargingStationTile.class",
    "com/direwolf20/charginggadgets/capabilities/ChargerEnergyStorage.class",
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
    building_config = BUILDING_CONFIG.read_text(encoding="utf-8-sig")
    mining_config = MINING_CONFIG.read_text(encoding="utf-8-sig")
    charging_config = CHARGING_CONFIG.read_text(encoding="utf-8-sig")
    registered = set(ITEMS.read_text(encoding="utf-8-sig").splitlines())
    blocks = quest_blocks(chapter_text)

    assert 'id: "6F50000000000005"' in chapter_text, "Chapter ID drift"
    assert 'group: "4E65FAAC62D57D4A"' in chapter_text, "Chapter group drift"
    assert 'icon: "mininggadgets:mininggadget"' in chapter_text, "Chapter icon drift"
    assert 'chapter.6F50000000000005.title: "Powered Field Engineering"' in lang
    assert (
        'chapter.6F50000000000005.subtitle: "Rechargeable excavation, templated construction and controlled civil works"'
        in lang
    )
    assert set(blocks) == set(EXPECTED), f"Field-engineering quest inventory drift: {sorted(set(blocks) ^ set(EXPECTED))}"
    for forbidden in ('type: "structure"', 'type: "biome"', 'type: "dimension"', 'type: "advancement"'):
        assert forbidden not in chapter_text, f"Unexpected world/progression task: {forbidden}"
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
        task_id = "7F6" + qid[3:]
        assert re.search(rf'^\ttask\.{task_id}\.title:', lang, re.M), f"{task_id} title missing"
        assert not reward_items(blocks[qid]), f"{qid} rewards self-certification"

    all_blocks: dict[str, str] = {}
    for chapter in CHAPTER_DIR.glob("*.snbt"):
        all_blocks.update(quest_blocks(chapter.read_text(encoding="utf-8-sig")))
    for qid, block in all_blocks.items():
        if qid not in EXPECTED:
            leaked = dependencies(block) & set(EXPECTED)
            assert not leaked, f"Core quest {qid} depends on optional field work: {sorted(leaked)}"

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
    assert objective_items <= indexed_outputs, f"No enabled recipe for: {sorted(objective_items - indexed_outputs)}"

    building_jars = list((ROOT / "mods").glob("buildinggadgets2-*.jar"))
    mining_jars = list((ROOT / "mods").glob("mininggadgets-*.jar"))
    charging_jars = list((ROOT / "mods").glob("charginggadgets-*.jar"))
    assert len(building_jars) == 1, f"Expected one Building Gadgets 2 JAR, found {building_jars}"
    assert len(mining_jars) == 1, f"Expected one Mining Gadgets JAR, found {mining_jars}"
    assert len(charging_jars) == 1, f"Expected one Charging Gadgets JAR, found {charging_jars}"
    with zipfile.ZipFile(building_jars[0]) as archive:
        names = set(archive.namelist())
        assert BUILDING_JAR_EVIDENCE <= names, f"Building feature evidence missing: {sorted(BUILDING_JAR_EVIDENCE - names)}"
    with zipfile.ZipFile(mining_jars[0]) as archive:
        names = set(archive.namelist())
        assert MINING_JAR_EVIDENCE <= names, f"Mining feature evidence missing: {sorted(MINING_JAR_EVIDENCE - names)}"
    with zipfile.ZipFile(charging_jars[0]) as archive:
        names = set(archive.namelist())
        assert CHARGING_JAR_EVIDENCE <= names, f"Charging feature evidence missing: {sorted(CHARGING_JAR_EVIDENCE - names)}"

    for token in (
        "rayTraceRange = 32",
        "maxPower = 500000",
        "baseCost = 50",
        "maxPower = 5000000",
        "maxPower = 1000000",
        "maxPower = 2000000",
        "baseCost = 100",
    ):
        assert token in building_config, f"Building Gadgets config drift: {token}"
    for token in (
        "maxPower = 1000000",
        "baseCost = 200",
        "battery1 = 2000000",
        "battery2 = 5000000",
        "battery3 = 10000000",
        "upgradeFortune3 = 100",
        "upgradeVoid = 10",
        "upgradeLight = 100",
        "upgradeFreeze = 100",
    ):
        assert token in mining_config, f"Mining Gadgets config drift: {token}"
    assert "chargerMaxEnergy = 1000000" in charging_config, "Charging Gadgets capacity drift"

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
            loaded = json.loads(path.read_text(encoding="utf-8-sig"))
            assert loaded == authored, f"Gateway override drift: {path}"
            assert "ae2:dense_energy_cell" not in path.read_text(encoding="utf-8-sig"), (
                f"{output} regained the accidental Era 8 battery dependency"
            )

    assert "Mining Gadgets, Building Gadgets 2, and Charging Gadgets" in generator, "Generator omits player-facing mod names"
    assert "Mining Gadgets" in signposting, "Signposting audit omits Mining Gadgets"
    assert "Building Gadgets 2" in signposting, "Signposting audit omits Building Gadgets 2"
    assert "Charging Gadgets" in signposting, "Signposting audit omits Charging Gadgets"
    assert "No quest or player state owns any world-generated structure" in generator
    for item_id in objective_items:
        assert item_id in generator, f"Generator lost objective {item_id}"

    print(
        "Powered field engineering audit passed: "
        f"{len(EXPECTED)} optional quests, {item_tasks} item tasks, "
        f"{len(CHECK_IDS)} witnessed procedures, {len(COG_IDS)} restrained Cog rewards, "
        f"{len(GATEWAYS)} cross-industry gateways, and zero Era 8 battery or progression-owned worldgen dependencies."
    )


if __name__ == "__main__":
    main()
