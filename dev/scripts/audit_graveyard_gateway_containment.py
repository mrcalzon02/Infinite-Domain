#!/usr/bin/env python3
"""Validate the Graveyard/Gateway quest branch and multiplayer-safe ownership."""

from __future__ import annotations

import csv
import json
import re
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CHAPTER = ROOT / "config/ftbquests/quests/chapters/graveyard_gateway_containment.snbt"
CHAPTER_DIR = CHAPTER.parent
LANG = ROOT / "config/ftbquests/quests/lang/en_us.snbt"
GENERATOR = ROOT / "dev/scripts/generators/build_graveyard_gateway_containment.js"
SIGNPOSTING = ROOT / "dev/scripts/audit_mod_signposting.js"
ITEMS = ROOT / "dev/docs/registry-inventory/item-ids.txt"
ENTITIES = ROOT / "dev/docs/registry-inventory/entity-ids.txt"
RECIPE_INDEX = ROOT / "dev/docs/recipe-index/recipe-index.csv"
GRAVEYARD_CONFIG = ROOT / "config/graveyard-common.toml"
GATEWAY_CONFIG = ROOT / "config/gateway_of_doom.json"
GATEWAY_LOCK = ROOT / "kubejs/server_scripts/gateway_of_doom_dimension_lock.js"
SITE = ROOT / "kubejs/data/infinite_domain/worldgen/structure/wasteland/roadside_church_cemetery.json"
SITE_SET = ROOT / "kubejs/data/infinite_domain/worldgen/structure_set/wasteland/wasteland_common.json"
APPROVALS = ROOT / "dev/structure_library/production-approvals.json"

ERA1 = "5CED58896AEFF1B9"
ERA2 = "5210000000000001"
ERA3 = "5310000000000001"
ERA5 = "5510000000000001"
ERA6 = "5610000000000001"
ERA7 = "5710000000000001"
CYBERSPACE_ENTRY = "5B00000000000011"

EXPECTED = {
    "6F30000000000001": {"deps": {ERA1}, "items": {"graveyard:candle_holder": 4, "graveyard:gravestone": 1}},
    "6F30000000000002": {"deps": {"6F30000000000001"}, "structure": "infinite_domain:wasteland/roadside_church_cemetery"},
    "6F30000000000003": {
        "deps": {"6F30000000000001"},
        "kills": {"graveyard:ghoul": 1, "graveyard:revenant": 1, "graveyard:reaper": 1, "graveyard:skeleton_creeper": 1},
    },
    "6F30000000000004": {"deps": {"6F30000000000003"}, "items": {"graveyard:corruption": 8}},
    "6F30000000000005": {
        "deps": {"6F30000000000004", ERA2},
        "items": {
            "graveyard:dark_iron_ingot": 16,
            "graveyard:dark_iron_bars": 16,
            "graveyard:dark_iron_door": 2,
            "graveyard:dark_iron_trapdoor": 2,
        },
    },
    "6F30000000000006": {"deps": {"6F30000000000005"}, "advancement": "graveyard:graveyard/kill_horde"},
    "6F30000000000007": {"deps": {"6F30000000000002", "6F30000000000006"}, "check": True},
    "6F30000000000008": {
        "deps": {ERA3, CYBERSPACE_ENTRY},
        "items": {"gateway_of_doom:portal_ward_1": 1, "gateway_of_doom:devil_eye_blue": 1},
    },
    "6F30000000000009": {"deps": {"6F30000000000008"}, "check": True},
    "6F3000000000000A": {
        "deps": {"6F30000000000009", ERA5},
        "items": {"gateway_of_doom:portal_ward_2": 1, "gateway_of_doom:devil_eye_red": 1},
    },
    "6F3000000000000B": {"deps": {"6F3000000000000A"}, "check": True},
    "6F3000000000000C": {
        "deps": {"6F3000000000000B", ERA6},
        "items": {"gateway_of_doom:portal_ward_3": 1, "gateway_of_doom:devil_eye_violet": 1},
    },
    "6F3000000000000D": {"deps": {"6F3000000000000C"}, "check": True},
    "6F3000000000000E": {
        "deps": {"6F3000000000000D", ERA7},
        "items": {"gateway_of_doom:portal_ward_4": 1, "gateway_of_doom:portal_ward_5": 1},
    },
    "6F3000000000000F": {"deps": {"6F30000000000007", "6F3000000000000E"}, "check": True},
}

COG_IDS = {
    "6F30000000000003",
    "6F30000000000005",
    "6F30000000000006",
    "6F3000000000000A",
    "6F3000000000000E",
}
CHECK_IDS = {qid for qid, spec in EXPECTED.items() if spec.get("check")}


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
        r'\{\s*(?:count:\s*(\d+)L,\s*)?item:\s*\{ count: 1, id: "([^"]+)" \}[^}]*type:\s*"item"\s*\}',
        block,
    ):
        found[item_id] = int(count or 1)
    return found


def task_kills(block: str) -> dict[str, int]:
    return {
        entity: int(count)
        for entity, count in re.findall(r'entity:\s*"([^"]+)"[^}]*value:\s*(\d+)L[^}]*type:\s*"kill"', block)
    }


def reward_items(block: str) -> list[str]:
    match = re.search(r"rewards:\s*\[([\s\S]*?)\]\s*\n\t\t\t(?:tags|tasks)", block)
    return re.findall(r'item:\s*\{(?:\s*count:\s*\d+,\s*)?id:\s*"([^"]+)"', match.group(1)) if match else []


def main() -> None:
    chapter_text = CHAPTER.read_text(encoding="utf-8-sig")
    lang = LANG.read_text(encoding="utf-8-sig")
    generator = GENERATOR.read_text(encoding="utf-8-sig")
    signposting = SIGNPOSTING.read_text(encoding="utf-8-sig")
    blocks = quest_blocks(chapter_text)
    registered_items = set(ITEMS.read_text(encoding="utf-8-sig").splitlines())
    registered_entities = set(ENTITIES.read_text(encoding="utf-8-sig").splitlines())

    assert 'id: "6F50000000000003"' in chapter_text, "Chapter ID drift"
    assert 'group: "4E65FAAC62D57D4A"' in chapter_text, "Chapter group drift"
    assert 'icon: "gateway_of_doom:portal_ward_3"' in chapter_text, "Chapter icon drift"
    assert set(blocks) == set(EXPECTED), f"Quest inventory drift: {sorted(set(blocks) ^ set(EXPECTED))}"
    assert 'chapter.6F50000000000003.title: "Graveyard and Gateway Containment"' in lang
    assert "independent worldgen" in lang

    item_tasks = 0
    kill_tasks = 0
    for qid, expected in EXPECTED.items():
        block = blocks[qid]
        assert "\n\t\t\toptional: true\n" in block, f"{qid} is not optional"
        assert dependencies(block) == expected["deps"], f"{qid} dependency drift"
        assert task_items(block) == expected.get("items", {}), f"{qid} item objective drift"
        assert task_kills(block) == expected.get("kills", {}), f"{qid} kill objective drift"
        item_tasks += len(expected.get("items", {}))
        kill_tasks += len(expected.get("kills", {}))
        if expected.get("structure"):
            assert f'structure: "{expected["structure"]}"' in block, f"{qid} structure drift"
        if expected.get("advancement"):
            assert f'advancement: "{expected["advancement"]}"' in block, f"{qid} advancement drift"
        if expected.get("check"):
            assert 'type: "checkmark"' in block, f"{qid} lost its witnessed procedure"
        rewards = reward_items(block)
        if qid in COG_IDS:
            assert rewards == ["numismatics:cog"], f"{qid} modest reward drift: {rewards}"
        else:
            assert not rewards, f"{qid} gained an unplanned reward"
        assert re.search(rf'^\tquest\.{qid}\.title:', lang, re.M), f"{qid} title missing"
        assert re.search(rf'^\tquest\.{qid}\.quest_desc:', lang, re.M), f"{qid} description missing"

    assert chapter_text.count('type: "structure"') == 1, "Only the pack-owned cemetery may be a structure objective"
    assert 'structure: "graveyard:' not in chapter_text, "Disabled upstream Graveyard worldgen leaked into quests"
    expected_map_command = (
        'command: "execute in minecraft:overworld run structure_map '
        'infinite_domain:wasteland/roadside_church_cemetery 2"'
    )
    assert chapter_text.count('type: "command"') == 1, "Only the cemetery explorer-map handoff may run a command"
    assert expected_map_command in blocks["6F30000000000001"], "Cemetery map handoff drift"
    assert 'id: "70E31D31A3D08DCA"' in blocks["6F30000000000001"], "Standard cemetery map reward ID drift"
    assert not re.search(r'command:\s*"[^"]*(?:place|setblock|fill|summon|gateway)', chapter_text, re.I), (
        "Containment quests must not place structures or open gateways"
    )
    for qid in CHECK_IDS:
        task_id = "7F3" + qid[3:]
        assert re.search(rf'^\ttask\.{task_id}\.title:', lang, re.M), f"{task_id} title missing"
        assert not reward_items(blocks[qid]), f"{qid} rewards self-certification"

    all_blocks: dict[str, str] = {}
    for chapter in CHAPTER_DIR.glob("*.snbt"):
        all_blocks.update(quest_blocks(chapter.read_text(encoding="utf-8-sig")))
    for qid, block in all_blocks.items():
        if qid not in EXPECTED:
            leaked = dependencies(block) & set(EXPECTED)
            assert not leaked, f"Core quest {qid} depends on optional containment work: {sorted(leaked)}"

    objective_items = {item_id for spec in EXPECTED.values() for item_id in spec.get("items", {})}
    objective_entities = {entity for spec in EXPECTED.values() for entity in spec.get("kills", {})}
    assert objective_items <= registered_items, f"Missing objective items: {sorted(objective_items - registered_items)}"
    assert objective_entities <= registered_entities, f"Missing objective entities: {sorted(objective_entities - registered_entities)}"

    with RECIPE_INDEX.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    indexed_outputs = {
        output.strip()
        for row in rows
        if row.get("enabled", "").lower() == "true"
        for output in row.get("output_ids", "").split(";")
    }
    crafted_items = objective_items - {"graveyard:corruption"}
    assert crafted_items <= indexed_outputs, f"No enabled recipe for: {sorted(crafted_items - indexed_outputs)}"

    graveyard_jars = list((ROOT / "mods").glob("graveyard-*.jar"))
    assert len(graveyard_jars) == 1, f"Expected one Graveyard JAR, found {graveyard_jars}"
    with zipfile.ZipFile(graveyard_jars[0]) as archive:
        names = set(archive.namelist())
        advancement_name = "data/graveyard/advancement/graveyard/kill_horde.json"
        assert advancement_name in names, "Installed Graveyard horde advancement missing"
        advancement_data = json.loads(archive.read(advancement_name))
        assert advancement_data["criteria"]["kill_horde"]["trigger"] == "graveyard:kill_horde"
        for mob in ("ghoul", "revenant", "reaper", "skeleton_creeper"):
            loot_name = f"data/graveyard/loot_table/entities/{mob}.json"
            assert loot_name in names, f"Missing installed loot table {loot_name}"
            assert "graveyard:corruption" in archive.read(loot_name).decode("utf-8"), f"{mob} lacks Corruption evidence"

    graveyard_config = GRAVEYARD_CONFIG.read_text(encoding="utf-8-sig")
    structure_switches = re.findall(r'\["The Graveyard - Structures Config"\.[^\]]+\]\s+generate\s*=\s*(true|false)', graveyard_config)
    assert len(structure_switches) == 17, f"Expected 17 Graveyard structure switches, found {len(structure_switches)}"
    assert set(structure_switches) == {"false"}, "Upstream Graveyard structure generation was re-enabled"
    assert re.search(r'\["The Graveyard - Horde Config"\.horde\]\s+generate\s*=\s*true', graveyard_config)
    for mob in ("ghoul", "revenant", "reaper", "nightmare", "skeleton_creeper"):
        assert re.search(rf'\["The Graveyard - Mob Spawning Config"\.{mob}\]\s+enabled\s*=\s*true', graveyard_config), f"{mob} ecology disabled"

    site = json.loads(SITE.read_text(encoding="utf-8-sig"))
    site_set = json.loads(SITE_SET.read_text(encoding="utf-8-sig"))
    approvals = json.loads(APPROVALS.read_text(encoding="utf-8-sig"))
    assert site["type"] == "minecraft:jigsaw"
    assert site["biomes"] == "#infinite_domain:wasteland_rural_biomes"
    assert site["start_pool"] == "infinite_domain:wasteland/roadside_church_cemetery"
    assert any(entry["structure"] == "infinite_domain:wasteland/roadside_church_cemetery" for entry in site_set["structures"])
    assert any(entry["structure_id"] == "infinite_domain:roadside_church_cemetery" for entry in approvals["approvals"])

    gateway = json.loads(GATEWAY_CONFIG.read_text(encoding="utf-8-sig"))
    assert gateway["mobDropsEnabled"] is False, "Gateway combat became a loot faucet"
    rules = {rule["id"]: rule for rule in gateway["automaticGateways"]["rules"]}
    assert rules["cyberspace_timer"]["enabled"] is True
    assert rules["cyberspace_timer"]["profileId"] == "hard"
    assert rules["cyberspace_timer"]["dimensions"] == ["cyberspace:cyberspace_dimension"]
    assert rules["cyberspace_timer"]["minIntervalSeconds"] == 1800
    assert rules["cyberspace_timer"]["maxIntervalSeconds"] == 3600
    for rule_id in ("overworld_exploration", "nether_timer", "end_timer"):
        assert rules[rule_id]["enabled"] is False, f"{rule_id} was re-enabled"

    lock = GATEWAY_LOCK.read_text(encoding="utf-8-sig")
    for eye in ("devil_eye", "devil_eye_blue", "devil_eye_red", "devil_eye_violet"):
        assert f"gateway_of_doom:{eye}" in lock, f"Dimension guard lost {eye}"
    assert "cyberspace:cyberspace_dimension" in lock

    gateway_recipes = ROOT / "kubejs/data/gateway_of_doom/recipe"
    expected_recipe_names = {f"portal_ward_{tier}.json" for tier in range(1, 6)} | {
        "devil_eye_blue.json", "devil_eye_red.json", "devil_eye_violet.json"
    }
    assert {path.name for path in gateway_recipes.glob("*.json")} == expected_recipe_names
    for tier in range(2, 6):
        payload = json.loads((gateway_recipes / f"portal_ward_{tier}.json").read_text(encoding="utf-8-sig"))
        assert payload["key"]["W"]["item"] == f"gateway_of_doom:portal_ward_{tier - 1}", f"Ward {tier} bypasses its predecessor"
    for color, tier in (("blue", 1), ("red", 2), ("violet", 3)):
        payload = json.loads((gateway_recipes / f"devil_eye_{color}.json").read_text(encoding="utf-8-sig"))
        assert payload["key"]["W"]["item"] == f"gateway_of_doom:portal_ward_{tier}"
        ingredient_namespaces = {value["item"].split(":", 1)[0] for value in payload["key"].values()}
        assert "cyber_ware_port" in ingredient_namespaces and "cyberspace" in ingredient_namespaces

    assert "The Graveyard" in generator and "Gateway of Doom" in generator
    assert "The Graveyard" in signposting and "Gateway of Doom" in signposting
    for item_id in objective_items:
        assert item_id in generator, f"Generator lost objective {item_id}"

    print(
        "Graveyard/Gateway containment audit passed: "
        f"{len(EXPECTED)} optional quests, {item_tasks} item tasks, {kill_tasks} kill tasks, "
        f"{len(CHECK_IDS)} witnessed procedures, 1 biome-owned structure observation, "
        "17 disabled upstream structures, and 8 staged Gateway recipes."
    )


if __name__ == "__main__":
    main()
