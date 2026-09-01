from __future__ import annotations

import json
import re
import zipfile
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFINITIONS = ROOT / "kubejs/data/infinite_domain/echo_definitions"
REGISTRY = ROOT / "docs/registry-inventory/item-ids.txt"
BRIDGE = ROOT / "mods/infinite-domain-echo-economy-1.0.0.jar"
CYBERWARE_EXPANSION = ROOT / "mods/infinite-domain-cyberware-mastery-1.0.0.jar"
EXPECTED_VENDORS = {
    "quartermaster",
    "mechanist",
    "foundry_broker",
    "chemical_cooperative",
    "grid_supply",
    "systems_exchange",
    "containment_office",
    "expedition_exchange",
    "cybernetics_exchange",
}
DENOMINATIONS = (4096, 512, 64, 16, 8, 1)
DENOMINATION_NAMES = {
    4096: "Sun",
    512: "Crown",
    64: "Cog",
    16: "Sprocket",
    8: "Bevel",
    1: "Spur",
}
QUEST_IDS = {
    "quartermaster": "6E01000000000001",
    "mechanist": "6E01000000000002",
    "foundry_broker": "6E01000000000003",
    "chemical_cooperative": "6E01000000000004",
    "grid_supply": "6E01000000000005",
    "systems_exchange": "6E01000000000006",
    "containment_office": "6E01000000000007",
    "expedition_exchange": "6E01000000000008",
    "cybernetics_exchange": "6E01000000000009",
}


def item_ids(entry: dict) -> list[str]:
    value = entry["item"]
    stacks = value if isinstance(value, list) else [value]
    return [stack["id"] for stack in stacks]


def format_price(value: int) -> str:
    parts = []
    remaining = value
    for denomination in DENOMINATIONS:
        count, remaining = divmod(remaining, denomination)
        if count:
            name = DENOMINATION_NAMES[denomination]
            parts.append(f"{count} {name}{'' if count == 1 else 's'}")
    return " + ".join(parts)


registry = set(REGISTRY.read_text(encoding="utf-8").splitlines())
assert CYBERWARE_EXPANSION.is_file(), "Cyberware mastery expansion JAR is missing"
with zipfile.ZipFile(CYBERWARE_EXPANSION) as cyberware_jar:
    prefix = "assets/infinite_domain_cyberware/models/item/"
    for name in cyberware_jar.namelist():
        if name.startswith(prefix) and name.endswith(".json"):
            registry.add(f"infinite_domain_cyberware:{Path(name).stem}")
files = {path.stem: path for path in DEFINITIONS.glob("*.json")}
assert files.keys() == EXPECTED_VENDORS, sorted(files)
language = (ROOT / "config/ftbquests/quests/lang/en_us.snbt").read_text(encoding="utf-8")

offer_count = 0
for vendor, path in sorted(files.items()):
    definition = json.loads(path.read_text(encoding="utf-8"))
    assert definition["id"] == f"infinite_domain:{vendor}"
    stages = definition["stages"]
    assert len(stages) == 1
    offers = stages[0]["shop_unlock"]
    assert len(offers) == 12, f"{vendor}: expected 12 offers, found {len(offers)}"
    assert stages[0]["completion_reward"]["currency"] > 0
    for offer in offers:
        assert isinstance(offer["cost"], int) and offer["cost"] > 0
        assert any(offer["cost"] >= value for value in reversed(DENOMINATIONS))
        for item_id in item_ids(offer):
            assert item_id in registry, f"{vendor}: unknown item {item_id}"

    quest_id = QUEST_IDS[vendor]
    match = re.search(
        rf"quest\.{quest_id}\.quest_desc: \[(.*?)\n\t\]",
        language,
        flags=re.DOTALL,
    )
    assert match, f"{vendor}: missing Spawn Exchange quest description"
    mirror = match.group(1)
    assert "physical Numismatics coins" in mirror
    mirrored_prices = re.findall(r" - ([^;.\"]+)(?=[;.])", mirror)
    expected_prices = [format_price(offer["cost"]) for offer in offers]
    assert Counter(mirrored_prices) == Counter(expected_prices), (
        f"{vendor}: quest mirror prices differ from Echo definition\n"
        f"expected={expected_prices}\nfound={mirrored_prices}"
    )
    offer_count += len(offers)

assert BRIDGE.is_file(), "Numismatics bridge JAR is missing"
with zipfile.ZipFile(BRIDGE) as jar:
    names = set(jar.namelist())
    for required in (
        "infinitedomain/echoeconomy/InfiniteDomainEchoEconomy.class",
        "infinitedomain/echoeconomy/NumismaticsCurrencyProvider.class",
        "infinitedomain/echoeconomy/mixin/MiscUtilMixin.class",
        "infinite_domain_echo_economy.mixins.json",
        "META-INF/neoforge.mods.toml",
    ):
        assert required in names, f"bridge JAR missing {required}"

print(
    f"Audit passed: {len(files)} Echo vendors, {offer_count} valid offers, "
    "matching quest-book price mirrors, and the Numismatics currency bridge are packaged."
)
