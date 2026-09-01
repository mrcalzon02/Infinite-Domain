"""Validate the Darknet-only fauna, UV skins, foliage, worldgen, and built jar."""

from __future__ import annotations

import json
import struct
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
JAR = ROOT / "mods/infinite-domain-darknet-worldgen-1.8.0.jar"
SOURCE = ROOT / "packdev/darknet-worldgen-patch/src/main"
JAVA = SOURCE / "java/infinitedomain/darknet"
RESOURCES = SOURCE / "resources"
VANILLA = Path(r"C:\Users\Admin\curseforge\minecraft\Install\versions\1.21.1\1.21.1.jar")


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def png_size_bytes(data: bytes) -> tuple[int, int]:
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise SystemExit("Invalid PNG data")
    return struct.unpack(">II", data[16:24])


def png_size(path: Path) -> tuple[int, int]:
    return png_size_bytes(path.read_bytes())


entity_source = (JAVA / "entity/DarknetEntities.java").read_text(encoding="utf-8")
client_source = (JAVA / "client/DarknetClient.java").read_text(encoding="utf-8")
rules_source = (JAVA / "entity/DarknetFaunaRules.java").read_text(encoding="utf-8")

entities = {
    "darknet_rabbit": ("DarknetRabbit", "Rabbit", "CREATURE", 12, 2, 4),
    "darknet_cow": ("DarknetCow", "Cow", "CREATURE", 8, 2, 3),
    "darknet_hound": ("DarknetWolf", "Wolf", "CREATURE", 4, 1, 3),
    "darknet_fox": ("DarknetFox", "Fox", "CREATURE", 6, 1, 2),
    "darknet_slime": ("DarknetSlime", "Slime", "MONSTER", 10, 1, 2),
}

for entity_id, (class_name, parent, category, weight, minimum, maximum) in entities.items():
    source_path = JAVA / f"entity/{class_name}.java"
    source = source_path.read_text(encoding="utf-8")
    if f"extends {parent}" not in source:
        raise SystemExit(f"{entity_id} no longer inherits vanilla {parent} behavior")
    for token in [f'"{entity_id}"', f"MobCategory.{category}", f"EntityType<{class_name}>"]:
        if token not in entity_source:
            raise SystemExit(f"Missing {entity_id} registration token: {token}")
    modifier = load(ROOT / f"kubejs/data/infinite_domain/neoforge/biome_modifier/{entity_id}.json")
    expected = {
        "type": "neoforge:add_spawns",
        "biomes": "cyberspace:darknet_biome",
        "spawners": {
            "type": f"infinite_domain_darknet_worldgen:{entity_id}",
            "weight": weight,
            "minCount": minimum,
            "maxCount": maximum,
        },
    }
    if modifier != expected:
        raise SystemExit(f"Natural spawn scope or population changed for {entity_id}: {modifier}")
    loot = load(RESOURCES / f"data/infinite_domain_darknet_worldgen/loot_table/entities/{entity_id}.json")
    vanilla_id = {"darknet_hound": "wolf"}.get(entity_id, entity_id.removeprefix("darknet_"))
    value = loot["pools"][0]["entries"][0].get("value")
    if value != f"minecraft:entities/{vanilla_id}":
        raise SystemExit(f"{entity_id} is not delegating to its vanilla-compatible loot: {value}")

for token in [
    "DarknetGuard.isDarknet", "pos.getY() < 2", "pos.below()", "getFluidState(pos).isEmpty()",
]:
    if token not in rules_source:
        raise SystemExit(f"Fauna spawn guard lost required behavior: {token}")
for token in [
    "DarknetRabbitRenderer::new", "DarknetCowRenderer::new", "DarknetWolfRenderer::new",
    "DarknetFoxRenderer::new", "DarknetSlimeRenderer::new",
]:
    if token not in client_source:
        raise SystemExit(f"Missing custom fauna renderer: {token}")

for class_name, tokens in {
    "DarknetRabbit.java": ["getBreedOffspring", "DARKNET_RABBIT", "setVariant"],
    "DarknetCow.java": ["getBreedOffspring", "DARKNET_COW"],
    "DarknetWolf.java": ["getBreedOffspring", "DARKNET_HOUND", "setOwnerUUID", "setTame(true, true)"],
    "DarknetFox.java": ["getBreedOffspring", "DARKNET_FOX", "setVariant"],
    "DarknetSlime.java": ["extends Slime"],
}.items():
    source = (JAVA / "entity" / class_name).read_text(encoding="utf-8")
    for token in tokens:
        if token not in source:
            raise SystemExit(f"{class_name} lost behavior: {token}")

skin_sources = {
    "rabbit.png": "assets/minecraft/textures/entity/rabbit/brown.png",
    "cow.png": "assets/minecraft/textures/entity/cow/cow.png",
    "wolf.png": "assets/minecraft/textures/entity/wolf/wolf.png",
    "wolf_tame.png": "assets/minecraft/textures/entity/wolf/wolf_tame.png",
    "wolf_angry.png": "assets/minecraft/textures/entity/wolf/wolf_angry.png",
    "fox.png": "assets/minecraft/textures/entity/fox/fox.png",
    "fox_sleep.png": "assets/minecraft/textures/entity/fox/fox_sleep.png",
    "slime.png": "assets/minecraft/textures/entity/slime/slime.png",
}
skin_root = RESOURCES / "assets/infinite_domain/textures/entity/darknet"
with zipfile.ZipFile(VANILLA) as vanilla:
    for skin, vanilla_entry in skin_sources.items():
        actual = png_size(skin_root / skin)
        expected = png_size_bytes(vanilla.read(vanilla_entry))
        if actual != expected:
            raise SystemExit(f"{skin} does not preserve its exact vanilla UV dimensions: {actual} != {expected}")

startup = (ROOT / "kubejs/startup_scripts/main.js").read_text(encoding="utf-8")
foliage = ["darknet_signal_grass", "darknet_packet_fern", "darknet_cipher_bloom", "darknet_blackroot_shrub"]
foliage_loop = startup.split("darknetFoliage.forEach", 1)[1]
for token in [".parentModel('minecraft:block/cross')", ".texture('cross', `kubejs:block/${id}`)", ".defaultCutout()"]:
    if token not in foliage_loop:
        raise SystemExit(f"KubeJS foliage generator lost its transparent cross-model instruction: {token}")
data_node_loop = startup.split("dataNodes.forEach", 1)[1].split("event.create('darknet_bedrock')", 1)[0]
if ".parentModel('minecraft:block/cross')" in data_node_loop or ".texture('cross'" in data_node_loop:
    raise SystemExit("Darknet data nodes were accidentally converted into foliage models")
for block in foliage:
    if f"['{block}'" not in startup:
        raise SystemExit(f"Missing foliage block registration: {block}")
    if png_size(ROOT / f"kubejs/assets/kubejs/textures/block/{block}.png") != (16, 16):
        raise SystemExit(f"Foliage texture is not 16x16: {block}")
    model = load(ROOT / f"kubejs/assets/kubejs/models/block/{block}.json")
    if model.get("parent") != "minecraft:block/cross" or model.get("render_type") != "minecraft:cutout":
        raise SystemExit(f"Foliage block is not a transparent cross model: {block}")

configured = load(ROOT / "kubejs/data/infinite_domain/worldgen/configured_feature/darknet_foliage.json")
if configured.get("type") != "minecraft:random_patch" or configured["config"].get("tries") != 20:
    raise SystemExit("Darknet foliage is not using its sparse 20-try patch")
entries = configured["config"]["feature"]["feature"]["config"]["to_place"]["entries"]
weights = {entry["data"]["Name"]: entry["weight"] for entry in entries}
if weights != {
    "kubejs:darknet_signal_grass": 9,
    "kubejs:darknet_packet_fern": 4,
    "kubejs:darknet_cipher_bloom": 1,
    "kubejs:darknet_blackroot_shrub": 3,
}:
    raise SystemExit(f"Darknet foliage weights changed: {weights}")
modifier = load(ROOT / "kubejs/data/infinite_domain/neoforge/biome_modifier/darknet_foliage.json")
if modifier != {
    "type": "neoforge:add_features",
    "biomes": "cyberspace:darknet_biome",
    "features": "infinite_domain:darknet_foliage",
    "step": "vegetal_decoration",
}:
    raise SystemExit("Darknet foliage feature escaped its biome scope")

conversion_root = ROOT / "kubejs/data/infinite_domain/recipe/darknet_ecology_conversion"
conversion_map = {
    "kubejs:scraped_access_token": {
        "kubejs:darknet_signal_grass", "minecraft:rabbit", "minecraft:cooked_rabbit",
        "minecraft:beef", "minecraft:cooked_beef",
    },
    "kubejs:darknet_data_cache": {
        "kubejs:darknet_packet_fern", "minecraft:rabbit_hide", "minecraft:leather",
        "minecraft:slime_ball",
    },
    "kubejs:encrypted_credential_bundle": {
        "kubejs:darknet_cipher_bloom", "kubejs:darknet_blackroot_shrub", "minecraft:rabbit_foot",
    },
}
found_conversions: dict[str, set[str]] = {output: set() for output in conversion_map}
recipe_paths = sorted(conversion_root.rglob("*.json"))
if len(recipe_paths) != 12:
    raise SystemExit(f"Expected 12 ecology conversion recipes, found {len(recipe_paths)}")
for recipe_path in recipe_paths:
    recipe = load(recipe_path)
    if recipe.get("type") != "minecraft:crafting_shaped" or recipe.get("pattern") != ["EEE", "EEE", "EEE"]:
        raise SystemExit(f"Ecology conversion is not an exact 3x3 shaped recipe: {recipe_path}")
    if set(recipe.get("key", {})) != {"E"}:
        raise SystemExit(f"Ecology conversion has unexpected ingredients: {recipe_path}")
    ingredient = recipe["key"]["E"].get("item")
    result = recipe.get("result", {})
    output = result.get("id")
    if result.get("count") != 1 or output not in conversion_map:
        raise SystemExit(f"Ecology conversion escaped tiers 1-3: {recipe_path} -> {result}")
    found_conversions[output].add(ingredient)
if found_conversions != conversion_map:
    raise SystemExit(f"Ecology conversion inputs changed: {found_conversions}")
for forbidden in [
    "kubejs:black_ice_kernel", "kubejs:zero_day_archive", "kubejs:root_authority_key",
    "kubejs:ghost_market_cipher", "kubejs:black_ledger_writ",
]:
    if forbidden in {output for output in found_conversions}:
        raise SystemExit(f"High-value Darknet resource became ecology-craftable: {forbidden}")

language = load(RESOURCES / "assets/infinite_domain_darknet_worldgen/lang/en_us.json")
for entity_id in entities:
    key = f"entity.infinite_domain_darknet_worldgen.{entity_id}"
    if key not in language:
        raise SystemExit(f"Missing localized fauna name: {key}")

for path in [
    ROOT / "DARKNET-ASSETS-LICENSE.md",
    ROOT / "docs/DARKNET_ECOLOGY.md",
    ROOT / "docs/art-direction/darknet-ecology-reference.png",
    ROOT / "docs/art-direction/darknet-ecology-reference.prompt.txt",
    ROOT / "scripts/generate_darknet_ecology_art.ps1",
]:
    if not path.is_file():
        raise SystemExit(f"Missing reproducible ecology asset: {path}")

with zipfile.ZipFile(JAR) as archive:
    names = set(archive.namelist())
    required = {
        "infinitedomain/darknet/entity/DarknetFaunaRules.class",
        *{f"infinitedomain/darknet/entity/{class_name}.class" for class_name, *_ in entities.values()},
        "infinitedomain/darknet/client/DarknetRabbitRenderer.class",
        "infinitedomain/darknet/client/DarknetCowRenderer.class",
        "infinitedomain/darknet/client/DarknetWolfRenderer.class",
        "infinitedomain/darknet/client/DarknetFoxRenderer.class",
        "infinitedomain/darknet/client/DarknetSlimeRenderer.class",
        *{f"assets/infinite_domain/textures/entity/darknet/{skin}" for skin in skin_sources},
        *{f"data/infinite_domain_darknet_worldgen/loot_table/entities/{entity}.json" for entity in entities},
        "DARKNET-ASSETS-LICENSE.md",
    }
    missing = sorted(required - names)
    if missing:
        raise SystemExit("Ecology companion jar is incomplete: " + ", ".join(missing))
    toml = archive.read("META-INF/neoforge.mods.toml").decode("utf-8")
    if 'version = "1.8.0"' not in toml:
        raise SystemExit("Ecology companion jar version is stale")

duplicates = [path.name for path in (ROOT / "mods").glob("infinite-domain-darknet-worldgen-*.jar") if path != JAR]
if duplicates:
    raise SystemExit("Duplicate Darknet companion mods: " + ", ".join(sorted(duplicates)))

print("Audit passed: five model-correct Darknet creatures retain vanilla behavior and loot, spawn only in the Darknet, and share a sparse four-plant native ecology.")
