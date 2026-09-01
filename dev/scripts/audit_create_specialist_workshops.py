#!/usr/bin/env python3
"""Validate the optional Create specialist-workshop quest chapter and gateways."""

from __future__ import annotations

import csv
import importlib.util
import json
import re
import tomllib
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CHAPTER = ROOT / "config/ftbquests/quests/chapters/create_specialist_workshops.snbt"
CHAPTER_DIR = CHAPTER.parent
LANG = ROOT / "config/ftbquests/quests/lang/en_us.snbt"
GENERATOR = ROOT / "dev/scripts/generators/build_quest_expansion.js"
SIGNPOSTING = ROOT / "dev/scripts/audit_mod_signposting.js"
ITEMS = ROOT / "dev/docs/registry-inventory/item-ids.txt"
RECIPE_INDEX = ROOT / "dev/docs/recipe-index/recipe-index.csv"
INTEGRATIONS = ROOT / "dev/scripts/apply_deep_recipe_integrations.py"
SERVER_CONFIG = ROOT / "config/createdeliveryrequired-server.toml"
CONTRACT_PRICES = ROOT / "config/createdeliveryrequired-contract-item-prices.toml"
MARKET_PRICES = ROOT / "config/createdeliveryrequired-market-item-prices.toml"

ERA1 = "4FC0C1C678C71891"
ERA2_START = "5210000000000001"
ERA2 = "5310000000000001"
ERA4 = "5510000000000001"

EXPECTED = {
    "6F00000000000001": {"deps": {ERA1}, "items": {"create:wrench": 1}},
    "6F00000000000002": {
        "deps": {"6F00000000000001"},
        "items": {"create_chimneys:chimney_iron": 8, "create_chimneys:chimney_bricks": 8},
    },
    "6F00000000000003": {"deps": {"6F00000000000002"}, "check": True},
    "6F00000000000004": {
        "deps": {"6F00000000000001", ERA2_START},
        "items": {"sable_kardanwelle:cardan_connector": 4},
    },
    "6F00000000000005": {
        "deps": {"6F00000000000004"},
        "items": {"linearbearing:linear_bearing": 2, "linearbearing:linear_casing": 8},
    },
    "6F00000000000006": {
        "deps": {"6F00000000000005"},
        "items": {"linearbearing:magnetic_port": 2, "linearbearing:torsional_anchor": 2},
    },
    "6F00000000000007": {"deps": {"6F00000000000006"}, "check": True},
    "6F00000000000008": {
        "deps": {"6F00000000000001", ERA2_START},
        "items": {"escalated:wooden_walkway_steps": 2, "escalated:metal_walkway_steps": 2},
    },
    "6F00000000000009": {
        "deps": {"6F00000000000008"}, "advancement": "escalated:walkway"
    },
    "6F0000000000000A": {
        "deps": {"6F00000000000009"}, "advancement": "escalated:escalator_100"
    },
    "6F0000000000000B": {
        "deps": {"6F00000000000001", ERA2},
        "items": {
            "bellsandwhistles:station_platform": 16,
            "bellsandwhistles:headlight": 4,
            "bellsandwhistles:brass_grab_rails": 8,
        },
    },
    "6F0000000000000C": {
        "deps": {"6F0000000000000B"},
        "items": {
            "create_mtg:announcement_box": 2,
            "create_mtg:empty_train_signal": 3,
        },
    },
    "6F0000000000000D": {"deps": {"6F0000000000000C"}, "check": True},
    "6F0000000000000E": {
        "deps": {"6F00000000000001", ERA2},
        "items": {"compactgearbox:compact_gearbox": 1},
    },
    "6F0000000000000F": {
        "deps": {"6F0000000000000E"},
        "items": {"compactgearbox:gearbox_controller": 1, "compactgearbox:sequential_gearbox": 1},
    },
    "6F00000000000010": {"deps": {"6F0000000000000F"}, "check": True},
    "6F00000000000011": {
        "deps": {"6F00000000000001", "5E00000000000002", ERA2},
        "items": {
            "createdeliveryrequired:contractor": 1,
            "createdeliveryrequired:delivery_marker": 2,
            "create:clipboard": 2,
        },
    },
    "6F00000000000012": {"deps": {"6F00000000000011"}, "check": True},
    "6F00000000000013": {
        "deps": {"6F00000000000012"},
        "items": {"createdeliveryrequired:market": 1, "createdeliveryrequired:numismatics_monocle": 1},
    },
    "6F00000000000014": {
        "deps": {"6F00000000000013", ERA4},
        "items": {"createdeliveryrequired:p2p_terminal": 1, "createdeliveryrequired:p2p_link": 2},
    },
    "6F00000000000015": {"deps": {"6F00000000000014"}, "check": True},
    "6F00000000000016": {
        "deps": {"6F00000000000001", ERA4},
        "items": {
            "create_hypertube:hypertube": 32,
            "create_hypertube:hypertube_entrance": 2,
            "create_hypertube:hypertube_accelerator": 2,
        },
    },
    "6F00000000000017": {
        "deps": {"6F00000000000016"},
        "items": {
            "create_hypertube:hypertube_junction": 2,
            "create_hypertube:tube_scanner_attachment": 2,
            "create_hypertube:redstone_detector_tube_attachment": 2,
        },
    },
    "6F00000000000018": {"deps": {"6F00000000000017"}, "check": True},
}

CHECK_IDS = {qid for qid, spec in EXPECTED.items() if spec.get("check")}
ADVANCEMENTS = {
    qid: spec["advancement"] for qid, spec in EXPECTED.items() if "advancement" in spec
}
COG_IDS = {
    "6F00000000000006",
    "6F0000000000000C",
    "6F0000000000000F",
    "6F00000000000014",
    "6F00000000000017",
}
GATEWAYS = {
    "compactgearbox:compact_gearbox": 2,
    "createdeliveryrequired:p2p_terminal": 3,
    "create_hypertube:hypertube_junction": 4,
}
MILESTONE_SYMBOLS = {
    ERA1: "milestones.era1",
    ERA2_START: "milestones.era2Start",
    ERA2: "milestones.era2",
    ERA4: "milestones.era4",
}
NAMED_SYSTEMS = [
    "Create: Bells & Whistles",
    "Create: Compact Gearbox",
    "Create Cardan Shafts",
    "Create: Linear Bearing",
    "Create: Chimneys",
    "Create: Hypertubes",
    "Create Aeronautics: Delivery Required",
    "Create: Escalated",
    "Create: Mind the Gap",
]


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
        r'\{\s*(?:count:\s*(\d+)L,\s*)?item:\s*\{ count: 1, id: "([^"]+)" \},\s*id:\s*"7F[0-9A-F]+",\s*type:\s*"item"\s*\}',
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


def advancement_is_installed(advancement: str) -> bool:
    namespace, path = advancement.split(":", 1)
    candidates = {
        f"data/{namespace}/advancement/{path}.json",
        f"data/{namespace}/advancements/{path}.json",
    }
    for jar in (ROOT / "mods").glob("*.jar"):
        try:
            with zipfile.ZipFile(jar) as archive:
                if candidates & set(archive.namelist()):
                    return True
        except zipfile.BadZipFile:
            continue
    return False


def assert_absent_stale_orbital_namespaces() -> None:
    stale = ("rocketnautics", "cosmonautics")
    hits: list[str] = []
    for jar in (ROOT / "mods").glob("*.jar"):
        try:
            with zipfile.ZipFile(jar) as archive:
                for entry in archive.namelist():
                    lowered = entry.lower()
                    if any(f"/{namespace}/" in lowered or lowered.startswith(f"{namespace}/") for namespace in stale):
                        hits.append(f"{jar.name}:{entry}")
                        break
        except zipfile.BadZipFile:
            continue
    assert not hits, f"Stale orbital namespace assumption is no longer absent: {hits}"


def main() -> None:
    chapter_text = CHAPTER.read_text(encoding="utf-8")
    lang = LANG.read_text(encoding="utf-8-sig")
    generator = GENERATOR.read_text(encoding="utf-8")
    signposting = SIGNPOSTING.read_text(encoding="utf-8")
    registered = set(ITEMS.read_text(encoding="utf-8-sig").splitlines())
    blocks = quest_blocks(chapter_text)

    assert 'id: "6F50000000000001"' in chapter_text, "Chapter ID drift"
    assert 'group: "4E65FAAC62D57D4A"' in chapter_text, "Chapter group drift"
    assert 'icon: "compactgearbox:sequential_gearbox"' in chapter_text, "Chapter icon drift"
    assert 'chapter.6F50000000000001.title: "Create Specialist Workshops"' in lang
    assert 'chapter.6F50000000000001.subtitle: "Compact motion, public transit and accountable delivery systems"' in lang
    assert set(blocks) == set(EXPECTED), f"Workshop quest inventory drift: {sorted(set(blocks) ^ set(EXPECTED))}"

    item_tasks = 0
    for qid, expected in EXPECTED.items():
        block = blocks[qid]
        assert "\n\t\t\toptional: true\n" in block, f"{qid} is not optional"
        assert dependencies(block) == expected["deps"], f"{qid} dependency drift"
        assert task_items(block) == expected.get("items", {}), f"{qid} item objective drift"
        item_tasks += len(expected.get("items", {}))

        if expected.get("check"):
            assert 'type: "checkmark"' in block, f"{qid} lost its witnessed procedure"
        elif "advancement" in expected:
            assert f'advancement: "{expected["advancement"]}"' in block, f"{qid} advancement drift"
            assert 'type: "advancement"' in block, f"{qid} lost advancement task type"
            assert advancement_is_installed(expected["advancement"]), (
                f"Advancement is not packaged by the installed mods: {expected['advancement']}"
            )

        rewards = reward_items(block)
        if qid in COG_IDS:
            assert rewards == ["numismatics:cog"], f"{qid} modest reward drift"
        else:
            assert not rewards, f"{qid} gained an unplanned reward"

        assert re.search(rf'^\tquest\.{qid}\.title:', lang, re.M), f"{qid} title missing"
        assert re.search(rf'^\tquest\.{qid}\.quest_desc:', lang, re.M), f"{qid} description missing"
        generator_lines = [line for line in generator.splitlines() if f"id: '{qid}'" in line]
        assert len(generator_lines) == 1, f"{qid} is not uniquely owned by the generator"
        source_line = generator_lines[0]
        assert "chain: false" in source_line and "optional: true" in source_line
        for item in expected.get("items", {}):
            assert f"'{item}'" in source_line, f"{qid} generator lost objective {item}"
        for dependency in expected["deps"]:
            token = MILESTONE_SYMBOLS.get(dependency, f"'{dependency}'")
            assert token in source_line, f"{qid} generator lost dependency {dependency}"

    for qid in CHECK_IDS:
        tid = "7F" + qid[2:]
        assert re.search(rf'^\ttask\.{tid}\.title:', lang, re.M), f"{tid} task title missing"

    all_blocks: dict[str, str] = {}
    for chapter in CHAPTER_DIR.glob("*.snbt"):
        all_blocks.update(quest_blocks(chapter.read_text(encoding="utf-8-sig")))
    for qid, block in all_blocks.items():
        if qid not in EXPECTED:
            leaked = dependencies(block) & set(EXPECTED)
            assert not leaked, f"Core quest {qid} depends on optional workshop work: {sorted(leaked)}"

    objective_items = {item for spec in EXPECTED.values() for item in spec.get("items", {})}
    missing_items = objective_items - registered
    assert not missing_items, f"Objective items are absent from installed registry: {sorted(missing_items)}"
    with RECIPE_INDEX.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    for item in objective_items:
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

    server = tomllib.loads(SERVER_CONFIG.read_text(encoding="utf-8-sig"))
    assert server["contractorOffers"]["demandBudgetSpurs"] == 64
    assert server["marketOffers"]["maximumPurchasableAmount"] == 256
    assert server["marketOffers"]["priceMultiplier"] == 3.0
    assert server["contractorRanks"]["completionXpPerDeliveredItem"] == 0.25
    contract_prices = tomllib.loads(CONTRACT_PRICES.read_text(encoding="utf-8-sig"))["item_prices"]
    market_prices = tomllib.loads(MARKET_PRICES.read_text(encoding="utf-8-sig"))["item_prices"]
    assert len(contract_prices) == 32, f"Contract export allowlist drift: {len(contract_prices)}"
    assert len(market_prices) == 29, f"Market allowlist drift: {len(market_prices)}"
    assert sum(1 for item in market_prices if item.startswith("minecraft:")) == 17

    ponders = {
        "contractor": ROOT / "kubejs/client_scripts/cdr_contractor_ponder.js",
        "market": ROOT / "kubejs/client_scripts/cdr_market_ponder.js",
        "p2p_terminal": ROOT / "kubejs/client_scripts/cdr_p2p_ponder.js",
    }
    for item, path in ponders.items():
        text = path.read_text(encoding="utf-8-sig")
        assert f"createdeliveryrequired:{item}" in text, f"Missing {item} Ponder registration"

    for name in NAMED_SYSTEMS:
        assert name in lang, f"Player-facing signposting missing: {name}"
        assert name in generator, f"Owning generator omits player-facing name: {name}"
        assert name in signposting, f"Signposting audit omits: {name}"

    assert_absent_stale_orbital_namespaces()
    print(
        "Create specialist-workshop audit passed: "
        f"{len(EXPECTED)} optional quests, {item_tasks} item tasks, {len(CHECK_IDS)} witnessed procedures, "
        f"{len(ADVANCEMENTS)} installed advancements, {len(GATEWAYS)} multi-industry gateways, "
        f"and {len(NAMED_SYSTEMS)} named systems."
    )


if __name__ == "__main__":
    main()
