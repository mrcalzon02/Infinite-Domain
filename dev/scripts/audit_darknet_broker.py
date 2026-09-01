"""Validate the Darknet Broker entity, art, spawn scope, currency, and offers."""

from __future__ import annotations

import json
import struct
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
JAR = ROOT / "mods/infinite-domain-darknet-worldgen-1.8.0.jar"
SOURCE_ROOT = ROOT / "packdev/darknet-worldgen-patch/src/main"
TRADER_SOURCE = SOURCE_ROOT / "java/infinitedomain/darknet/entity/DarknetTrader.java"
ENTITY_SOURCE = SOURCE_ROOT / "java/infinitedomain/darknet/entity/DarknetEntities.java"
RENDERER_SOURCE = SOURCE_ROOT / "java/infinitedomain/darknet/client/DarknetTraderRenderer.java"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise SystemExit(f"Not a PNG: {path}")
    return struct.unpack(">II", data[16:24])


startup = (ROOT / "kubejs/startup_scripts/main.js").read_text(encoding="utf-8")
for token in [
    "event.create('darknet_scrip')", ".displayName('Darknet Scrip')",
    "event.create('ghost_market_cipher')", ".displayName('Ghost-Market Cipher')",
    "event.create('black_ledger_writ')", ".displayName('Black-Ledger Writ')",
]:
    if token not in startup:
        raise SystemExit(f"Missing Broker economy item registration: {token}")

for name in ["darknet_scrip", "ghost_market_cipher", "black_ledger_writ"]:
    texture = ROOT / "kubejs/assets/kubejs/textures/item" / f"{name}.png"
    if png_size(texture) != (32, 32):
        raise SystemExit(f"Broker economy icon is not 32x32: {texture}")

skin = SOURCE_ROOT / "resources/assets/infinite_domain/textures/entity/darknet_broker.png"
if png_size(skin) != (64, 64):
    raise SystemExit("Darknet Broker skin is not an exact 64x64 wandering-trader UV sheet")

modifier = load(ROOT / "kubejs/data/infinite_domain/neoforge/biome_modifier/darknet_trader.json")
if modifier != {
    "type": "neoforge:add_spawns",
    "biomes": "cyberspace:darknet_biome",
    "spawners": {
        "type": "infinite_domain_darknet_worldgen:darknet_trader",
        "weight": 1,
        "minCount": 1,
        "maxCount": 1,
    },
}:
    raise SystemExit("Darknet Broker natural spawn is not narrowly scoped")

trader = TRADER_SOURCE.read_text(encoding="utf-8")
entities = ENTITY_SOURCE.read_text(encoding="utf-8")
renderer = RENDERER_SOURCE.read_text(encoding="utf-8")
for token in [
    "extends WanderingTrader", "DESPAWN_TICKS = 72_000", "EXCLUSION_RADIUS = 384.0",
    "DarknetGuard.isDarknet", "pos.getY() < 2", "Mob.checkMobSpawnRules",
    "protected void updateTrades()", "kubejs:darknet_scrip", "ae2:spatial_anchor",
    "new ItemCost(resolve(SCRIP), 64)", "new ItemCost(resolve(\"kubejs:root_authority_key\"), 8)",
]:
    if token not in trader:
        raise SystemExit(f"Darknet Broker source lost required behavior: {token}")
if "super.updateTrades" in trader:
    raise SystemExit("Darknet Broker is leaking vanilla wandering-trader offers")
for token in [
    "EntityType<DarknetTrader>", "MobCategory.CREATURE", "DarknetTrader::canSpawn",
    "Attributes.MAX_HEALTH, 60.0", "Attributes.ARMOR, 12.0",
    "Attributes.KNOCKBACK_RESISTANCE, 0.5",
]:
    if token not in entities:
        raise SystemExit(f"Darknet Broker registration lost required behavior: {token}")
for token in ["extends WanderingTraderRenderer", "textures/entity/darknet_broker.png"]:
    if token not in renderer:
        raise SystemExit(f"Darknet Broker renderer lost its custom skin: {token}")

expected_trade_lines = [
    'buy(offers, "kubejs:scraped_access_token", 16, 1, 12);',
    'buy(offers, "kubejs:darknet_data_cache", 8, 2, 12);',
    'buy(offers, "kubejs:encrypted_credential_bundle", 4, 3, 10);',
    'buy(offers, "kubejs:black_ice_kernel", 2, 5, 8);',
    'buy(offers, "kubejs:zero_day_archive", 1, 10, 6);',
    'buy(offers, "kubejs:root_authority_key", 1, 24, 4);',
    'buy(offers, "kubejs:ghost_market_cipher", 1, 16, 6);',
    'buy(offers, "kubejs:black_ledger_writ", 1, 48, 3);',
    'sell(offers, 6, "kubejs:fragmented_data_node", 1, 12);',
    'sell(offers, 14, "kubejs:corrupted_data_node", 1, 8);',
    'sell(offers, 32, "kubejs:encrypted_data_node", 1, 4);',
    'sell(offers, 64, "kubejs:root_access_node", 1, 2);',
]
for line in expected_trade_lines:
    if line not in trader:
        raise SystemExit(f"Darknet Broker trade table changed unexpectedly: {line}")

expected_bonus_chances = {
    "corrupted_data_node": {"kubejs:ghost_market_cipher": 0.02},
    "encrypted_data_node": {
        "kubejs:ghost_market_cipher": 0.075,
        "kubejs:black_ledger_writ": 0.01,
    },
    "root_access_node": {
        "kubejs:ghost_market_cipher": 0.25,
        "kubejs:black_ledger_writ": 0.075,
    },
}
for node, expectations in expected_bonus_chances.items():
    loot = load(ROOT / "kubejs/data/kubejs/loot_table/blocks" / f"{node}.json")
    found: dict[str, float] = {}
    for pool in loot.get("pools", []):
        names = {entry.get("name") for entry in pool.get("entries", [])}
        for item in expectations:
            if item in names:
                condition = next((c for c in pool.get("conditions", []) if c.get("condition") == "minecraft:random_chance"), None)
                if condition is not None:
                    found[item] = condition.get("chance")
    if found != expectations:
        raise SystemExit(f"Premium Broker recovery odds changed for {node}: {found}")

language = load(SOURCE_ROOT / "resources/assets/infinite_domain_darknet_worldgen/lang/en_us.json")
if language.get("entity.infinite_domain_darknet_worldgen.darknet_trader") != "Darknet Broker":
    raise SystemExit("Darknet Broker lost its localized entity name")

art_files = [
    ROOT / "docs/art-direction/darknet-broker-reference.png",
    ROOT / "docs/art-direction/darknet-broker-reference.prompt.txt",
    ROOT / "docs/art-direction/darknet-broker-items-reference.png",
    ROOT / "docs/art-direction/darknet-broker-items-reference.prompt.txt",
    ROOT / "scripts/generate_darknet_broker_art.ps1",
]
for path in art_files:
    if not path.is_file():
        raise SystemExit(f"Missing reproducible Darknet Broker art source: {path}")

with zipfile.ZipFile(JAR) as archive:
    names = set(archive.namelist())
    required_entries = {
        "infinitedomain/darknet/entity/DarknetTrader.class",
        "infinitedomain/darknet/client/DarknetClient.class",
        "infinitedomain/darknet/client/DarknetTraderRenderer.class",
        "assets/infinite_domain/textures/entity/darknet_broker.png",
        "assets/infinite_domain_darknet_worldgen/lang/en_us.json",
    }
    missing = sorted(required_entries - names)
    if missing:
        raise SystemExit("Broker companion jar is incomplete: " + ", ".join(missing))
    class_bytes = archive.read("infinitedomain/darknet/entity/DarknetTrader.class")
    if int.from_bytes(class_bytes[6:8], "big") != 65:
        raise SystemExit("Darknet Broker is not compiled for Java 21")
    toml = archive.read("META-INF/neoforge.mods.toml").decode("utf-8")
    if 'version = "1.8.0"' not in toml:
        raise SystemExit("Darknet Broker companion jar version is stale")

duplicates = sorted(path.name for path in (ROOT / "mods").glob("infinite-domain-darknet-worldgen-*.jar") if path != JAR)
if duplicates:
    raise SystemExit("Duplicate Darknet companion mods: " + ", ".join(duplicates))

documentation = " ".join((ROOT / "docs/DARKNET_BROKER.md").read_text(encoding="utf-8").split())
for token in [
    "Darknet Broker", "72,000 ticks", "384 blocks", "Darknet Scrip",
    "Ghost-Market Cipher", "Black-Ledger Writ", "64 Darknet Scrip plus eight Root Authority Keys",
    "352 Scrip", "full game restart",
]:
    if token not in documentation:
        raise SystemExit(f"Darknet Broker documentation lost required detail: {token}")

print("Audit passed: the Darknet-only Broker has its custom UV skin, eight buyback offers, ten retail offers, two premium ore recoveries, and 352-Scrip-equivalent emergency Anchor route.")
