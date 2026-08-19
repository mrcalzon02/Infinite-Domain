"""Validate Darknet data strata, their drops, textures, and bottom boundary."""

from __future__ import annotations

import hashlib
import json
import struct
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "kubejs/data/infinite_domain"
KUBE_DATA = ROOT / "kubejs/data/kubejs"
ASSETS = ROOT / "kubejs/assets/kubejs/textures"

NODES = {
    "fragmented_data_node": {"size": 8, "min": -24, "max": 1, "count": 11},
    "corrupted_data_node": {"size": 5, "min": -40, "max": -8, "count": 6},
    "encrypted_data_node": {"size": 3, "min": -55, "max": -24, "count": 3},
    "root_access_node": {"size": 2, "min": -63, "max": -48, "rarity": 24},
}
REWARDS = {
    "fragmented_data_node": {"kubejs:scraped_access_token", "kubejs:darknet_data_cache"},
    "corrupted_data_node": {
        "kubejs:scraped_access_token", "kubejs:darknet_data_cache",
        "kubejs:encrypted_credential_bundle", "kubejs:ghost_market_cipher",
    },
    "encrypted_data_node": {
        "kubejs:darknet_data_cache", "kubejs:encrypted_credential_bundle",
        "kubejs:black_ice_kernel", "kubejs:zero_day_archive",
        "kubejs:ghost_market_cipher", "kubejs:black_ledger_writ",
    },
    "root_access_node": {
        "kubejs:darknet_data_cache", "kubejs:black_ice_kernel",
        "kubejs:zero_day_archive", "kubejs:root_authority_key",
        "kubejs:ghost_market_cipher", "kubejs:black_ledger_writ",
    },
}
ITEM_TEXTURES = {
    "darknet_data_cache", "scraped_access_token", "encrypted_credential_bundle",
    "black_ice_kernel", "zero_day_archive", "root_authority_key", "darknet_scrip",
    "ghost_market_cipher", "black_ledger_writ",
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise SystemExit(f"Not a PNG texture: {path}")
    return struct.unpack(">II", data[16:24])


dimension = load(ROOT / "kubejs/data/cyberspace/dimension/darknet_dimension.json")
settings = dimension["generator"]["settings"]
if settings.get("features") is not True or settings.get("lakes") is not False:
    raise SystemExit("Darknet decoration/lake policy is not exact")
if settings["layers"] != [
    {"height": 1, "block": "kubejs:darknet_bedrock"},
    {"height": 65, "block": "cyberspace:darknetblock_1"},
]:
    raise SystemExit("Darknet Bedrock is not the exact Y=-64 boundary layer")

startup = (ROOT / "kubejs/startup_scripts/main.js").read_text(encoding="utf-8")
for node in NODES:
    if f"['{node}'" not in startup or f"kubejs:block/${{id}}" not in startup:
        raise SystemExit(f"Missing localized startup registration for {node}")
for required in [
    "event.create('darknet_bedrock')", ".unbreakable()", ".noDrops()",
    ".requiresTool()", ".noValidSpawns(true)",
]:
    if required not in startup:
        raise SystemExit(f"Darknet block registration lost required behavior: {required}")
for item in ITEM_TEXTURES:
    if f"kubejs:item/{item}" not in startup:
        raise SystemExit(f"Darknet reward does not use its custom texture: {item}")

block_hashes = set()
for name in [*NODES, "darknet_bedrock"]:
    path = ASSETS / "block" / f"{name}.png"
    if png_size(path) != (32, 32):
        raise SystemExit(f"Darknet block texture is not 32x32: {path}")
    block_hashes.add(hashlib.sha256(path.read_bytes()).hexdigest())
if len(block_hashes) != 5:
    raise SystemExit("Darknet block rarity textures are not visually distinct files")
for name in ITEM_TEXTURES:
    path = ASSETS / "item" / f"{name}.png"
    if png_size(path) != (32, 32):
        raise SystemExit(f"Darknet reward texture is not 32x32: {path}")

enchantment = load(DATA / "enchantment/darknet_extraction.json")
if enchantment != {
    "anvil_cost": 8,
    "description": {"translate": "enchantment.infinite_domain.darknet_extraction"},
    "exclusive_set": "#minecraft:exclusive_set/mining",
    "max_cost": {"base": 58, "per_level_above_first": 8},
    "max_level": 5,
    "min_cost": {"base": 10, "per_level_above_first": 8},
    "slots": ["mainhand"],
    "supported_items": "#minecraft:pickaxes",
    "weight": 1,
}:
    raise SystemExit("Darknet Extraction definition is not the exact five-level pickaxe enchantment")
for tag_path in [
    ROOT / "kubejs/data/minecraft/tags/enchantment/non_treasure.json",
    ROOT / "kubejs/data/minecraft/tags/enchantment/exclusive_set/mining.json",
]:
    tag = load(tag_path)
    if tag != {"replace": False, "values": ["infinite_domain:darknet_extraction"]}:
        raise SystemExit(f"Darknet Extraction acquisition or exclusivity tag changed: {tag_path}")
language = load(ROOT / "kubejs/assets/infinite_domain/lang/en_us.json")
if language.get("enchantment.infinite_domain.darknet_extraction") != "Darknet Extraction":
    raise SystemExit("Darknet Extraction lost its localized name")

for name, expected in NODES.items():
    configured = load(DATA / "worldgen/configured_feature" / f"{name}.json")
    config = configured.get("config", {})
    if configured.get("type") != "minecraft:ore" or config.get("size") != expected["size"]:
        raise SystemExit(f"Configured feature changed for {name}")
    targets = config.get("targets", [])
    if len(targets) != 1:
        raise SystemExit(f"Darknet node has an unexpected target count: {name}")
    target = targets[0]
    if target.get("state") != {"Name": f"kubejs:{name}"} or target.get("target") != {
        "predicate_type": "minecraft:block_match", "block": "cyberspace:darknetblock_1"
    }:
        raise SystemExit(f"Darknet node can replace the wrong material: {name}")

    placed = load(DATA / "worldgen/placed_feature" / f"{name}.json")
    if placed.get("feature") != f"infinite_domain:{name}":
        raise SystemExit(f"Placed feature points to the wrong configured feature: {name}")
    placements = placed.get("placement", [])
    height = next((p["height"] for p in placements if p.get("type") == "minecraft:height_range"), None)
    if height != {
        "type": "minecraft:uniform",
        "min_inclusive": {"absolute": expected["min"]},
        "max_inclusive": {"absolute": expected["max"]},
    }:
        raise SystemExit(f"Darknet node height band changed: {name}")
    expected_density = (
        {"type": "minecraft:count", "count": expected["count"]}
        if "count" in expected
        else {"type": "minecraft:rarity_filter", "chance": expected["rarity"]}
    )
    if expected_density not in placements or {"type": "minecraft:biome"} not in placements:
        raise SystemExit(f"Darknet node density or biome placement changed: {name}")

    modifier = load(DATA / "neoforge/biome_modifier" / f"darknet_{name}.json")
    if modifier != {
        "type": "neoforge:add_features",
        "biomes": "cyberspace:darknet_biome",
        "features": f"infinite_domain:{name}",
        "step": "underground_ores",
    }:
        raise SystemExit(f"Darknet-only biome scope changed: {name}")

    loot = load(KUBE_DATA / "loot_table/blocks" / f"{name}.json")
    serialized = json.dumps(loot)
    missing_rewards = sorted(REWARDS[name] - {reward for reward in REWARDS[name] if reward in serialized})
    if missing_rewards:
        raise SystemExit(f"Darknet node lost rewards {missing_rewards}: {name}")
    if f"kubejs:{name}" in serialized:
        raise SystemExit(f"Darknet node incorrectly drops itself instead of recovered data: {name}")
    if serialized.count("infinite_domain:darknet_extraction") != 1:
        raise SystemExit(f"Darknet Extraction must affect exactly the primary recovery for {name}")
    if "minecraft:ore_drops" not in serialized or "minecraft:fortune" in serialized:
        raise SystemExit(f"Darknet node is not using only the custom Fortune formula: {name}")

required_tag_values = {"cyberspace:darknetblock_1", *(f"kubejs:{name}" for name in NODES)}
for tag_path in [
    ROOT / "kubejs/data/minecraft/tags/block/mineable/pickaxe.json",
    ROOT / "kubejs/data/minecraft/tags/block/needs_diamond_tool.json",
]:
    tag = load(tag_path)
    if tag.get("replace") is not False or not required_tag_values.issubset(set(tag.get("values", []))):
        raise SystemExit(f"Darknet data mining tag is incomplete: {tag_path}")

for required in [
    ROOT / "docs/art-direction/darknet-content-reference.png",
    ROOT / "docs/art-direction/darknet-data-node-production-atlas.png",
    ROOT / "docs/art-direction/darknet-data-node-production-atlas.prompt.txt",
    ROOT / "scripts/generate_darknet_data_node_textures.ps1",
]:
    if not required.is_file():
        raise SystemExit(f"Missing reproducible Darknet art source: {required}")

documentation = " ".join((ROOT / "docs/DARKNET_DATA_NODES.md").read_text(encoding="utf-8").split())
for required in [
    "Fragmented Data Node", "Corrupted Data Node", "Encrypted Data Node",
    "Root Access Node", "Darknet Bedrock", "Y=-64", "one attempt per 24 chunks",
    "newly generated Darknet chunks only", "five-level pickaxe enchantment",
    "Fortune ore-drop formula", "mutually exclusive with ordinary Fortune",
    "Ghost-Market Cipher", "Black-Ledger Writ",
]:
    if required not in documentation:
        raise SystemExit(f"Darknet data-node documentation lost required detail: {required}")

print("Audit passed: four Darknet-only data strata, two premium Broker recoveries, Darknet Extraction I-V, nine economy icons, and the unbreakable Y=-64 Darknet Bedrock are complete.")
