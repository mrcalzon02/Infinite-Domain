"""Static release audit for the Datavore Dragon boss."""
from __future__ import annotations

import json
import struct
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
JAR = ROOT / "mods/infinite-domain-darknet-worldgen-1.8.0.jar"
SOURCE = ROOT / "dev/packdev/darknet-worldgen-patch/src/main/java/infinitedomain/darknet/entity/DatavoreDragon.java"

with zipfile.ZipFile(JAR) as archive:
    entries = set(archive.namelist())
    required = {
        "infinitedomain/darknet/entity/DatavoreDragon.class",
        "infinitedomain/darknet/entity/DarknetEntities.class",
        "infinitedomain/darknet/mixin/EntityRenderDispatcherMixin.class",
        "assets/infinite_domain/textures/entity/datavore/datavore.png",
        "assets/infinite_domain/textures/entity/datavore/datavore_eyes.png",
        "assets/infinite_domain/textures/entity/datavore/datavore_skeleton.png",
        "assets/infinite_domain_darknet_worldgen/lang/en_us.json",
    }
    missing = sorted(required - entries)
    if missing:
        raise SystemExit("Datavore jar is incomplete: " + ", ".join(missing))

source = SOURCE.read_text(encoding="utf-8")
for required in [
    "extends EntityLightningDragon", "MAX_HEALTH = 1000.0", "MIN_RADIUS = 2800", "MAX_RADIUS = 3600",
    "ServerBossEvent", "BossBarOverlay.NOTCHED_20", "getDeadLootTable", "setPersistenceRequired",
    "inflate(512.0)", "DatavoreDragon::canSpawn",
]:
    if required not in source and required not in (ROOT / "dev/packdev/darknet-worldgen-patch/src/main/java/infinitedomain/darknet/entity/DarknetEntities.java").read_text(encoding="utf-8"):
        raise SystemExit(f"Datavore source lost required behavior: {required}")

modifier = json.loads((ROOT / "kubejs/data/infinite_domain/neoforge/biome_modifier/darknet_datavore_dragon.json").read_text(encoding="utf-8"))
if modifier != {
    "type": "neoforge:add_spawns", "biomes": "cyberspace:darknet_biome",
    "spawners": {"type": "infinite_domain_darknet_worldgen:datavore_dragon", "weight": 1, "minCount": 1, "maxCount": 1},
}:
    raise SystemExit("Datavore biome spawn modifier changed unexpectedly")

loot_path = ROOT / "kubejs/data/infinite_domain/loot_table/entities/datavore_dragon.json"
loot = json.loads(loot_path.read_text(encoding="utf-8"))
loot_text = json.dumps(loot)
reward_ids = [
    "kubejs:darknet_data_cache", "kubejs:scraped_access_token", "kubejs:encrypted_credential_bundle",
    "kubejs:black_ice_kernel", "kubejs:zero_day_archive", "kubejs:root_authority_key",
    "minecraft:netherite_ingot", "minecraft:nether_star",
]
for reward in reward_ids:
    if reward not in loot_text:
        raise SystemExit(f"Datavore apocalyptic loot lost reward: {reward}")

startup = (ROOT / "kubejs/startup_scripts/main.js").read_text(encoding="utf-8")
for reward in reward_ids[:6]:
    if reward.removeprefix("kubejs:") not in startup:
        raise SystemExit(f"Datavore reward item is not registered: {reward}")

texture_root = ROOT / "dev/packdev/darknet-worldgen-patch/src/main/resources/assets/infinite_domain/textures/entity/datavore"
dimensions = []
for name in ["datavore.png", "datavore_eyes.png", "datavore_skeleton.png"]:
    data = (texture_root / name).read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit(f"Datavore texture is not PNG: {name}")
    dimensions.append(struct.unpack(">II", data[16:24]))
if len(set(dimensions)) != 1:
    raise SystemExit(f"Datavore UV sheets do not share exact dimensions: {dimensions}")

duplicates = [p.name for p in (ROOT / "mods").glob("infinite-domain-darknet-worldgen-*.jar") if p != JAR]
if duplicates:
    raise SystemExit("Duplicate companion mod jars: " + ", ".join(sorted(duplicates)))

print("Audit passed: Datavore Dragon is registered, naturally radius-gated to the Darknet, 1,000 HP, boss-barred, exact-UV skinned, persistent, and carries complete apocalyptic loot.")
