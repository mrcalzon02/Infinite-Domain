"""Validate the deliberately narrow Darknet dragon-structure admission."""

from __future__ import annotations

import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TAG_ROOT = ROOT / "kubejs/data/iceandfire/tags/worldgen/biome/structure_gen"
DRAGON_TAGS = {"fire", "ice", "lightning"}
DARKNET = "cyberspace:darknet_biome"

dimension_type = json.loads((ROOT / "kubejs/data/cyberspace/dimension_type/darknet_dimension.json").read_text(encoding="utf-8"))
dimension = json.loads((ROOT / "kubejs/data/cyberspace/dimension/darknet_dimension.json").read_text(encoding="utf-8"))
if (dimension_type["min_y"], dimension_type["height"], dimension_type["logical_height"]) != (-64, 320, 320):
    raise SystemExit("Darknet dimension no longer has its 64-layer negative-Y foundation range")
layers = dimension["generator"]["settings"]["layers"]
if layers != [
    {"height": 1, "block": "kubejs:darknet_bedrock"},
    {"height": 65, "block": "cyberspace:darknetblock_1"},
]:
    raise SystemExit("Darknet flat generator no longer preserves its Y=2 surface over the deep foundation")
if dimension["generator"]["settings"].get("features") is not True or dimension["generator"]["settings"].get("lakes") is not False:
    raise SystemExit("Darknet data features must be enabled while lakes remain disabled")

for element in sorted(DRAGON_TAGS):
    path = TAG_ROOT / f"{element}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    if data != {"replace": False, "values": [DARKNET]}:
        raise SystemExit(f"Darknet {element} structure admission is not exact: {path}")

for path in ROOT.glob("kubejs/data/**/tags/worldgen/biome/**/*.json"):
    data = json.loads(path.read_text(encoding="utf-8"))
    if DARKNET in data.get("values", []) and path.parent != TAG_ROOT:
        raise SystemExit(f"Unapproved structure-biome tag admits the Darknet: {path}")

documentation = (ROOT / "dev/docs/DARKNET_WORLDGEN.md").read_text(encoding="utf-8")
for required in [
    "Y=2", "Y=0 through Y=128", "Data Entity", "Obligator",
    "Dragon Roost", "Dragon Cave", "Y=80", "Y=31 through Y=60", "begins at Y=7",
    "Y=-64", "additional foundation layers",
]:
    if required not in documentation:
        raise SystemExit(f"Darknet worldgen documentation lost required evidence: {required}")

patch_jar = ROOT / "mods/infinite-domain-darknet-worldgen-1.8.0.jar"
required_entries = {
    "META-INF/neoforge.mods.toml",
    "infinite_domain_darknet_worldgen.mixins.json",
    "infinitedomain/darknet/DarknetWorldgenPatch.class",
    "infinitedomain/darknet/DarknetGuard.class",
    "infinitedomain/darknet/DarknetDragonTextures.class",
    "infinitedomain/darknet/mixin/Darknetblock1Mixin.class",
    "infinitedomain/darknet/mixin/DragonUtilsMixin.class",
    "infinitedomain/darknet/mixin/IafDragonDestructionManagerMixin.class",
    "infinitedomain/darknet/mixin/LegacyGeneratedStructureMixin.class",
    "infinitedomain/darknet/mixin/LegacyDragonRendererMixin.class",
    "infinitedomain/darknet/mixin/EnumDragonTexturesMixin.class",
    "infinitedomain/darknet/mixin/LegacyDragonArmorFeatureMixin.class",
    "infinitedomain/darknet/client/DarknetEntityOverlayLayer.class",
    "infinitedomain/darknet/mixin/LivingEntityRendererMixin.class",
    "infinitedomain/darknet/mixin/HumanoidArmorLayerMixin.class",
    "assets/infinite_domain/textures/entity/darknet_overlay_static.png",
    "assets/infinite_domain/textures/entity/darknet_overlay_shimmer.png",
    "assets/infinite_domain/textures/entity/darknet_overlay_shimmer.png.mcmeta",
    "infinitedomain/darknet/entity/DatavoreDragon.class",
    "infinitedomain/darknet/entity/DarknetEntities.class",
    "infinitedomain/darknet/mixin/EntityRenderDispatcherMixin.class",
    "assets/infinite_domain/textures/entity/datavore/datavore.png",
    "assets/infinite_domain/textures/entity/datavore/datavore_eyes.png",
    "assets/infinite_domain/textures/entity/datavore/datavore_skeleton.png",
}
with zipfile.ZipFile(patch_jar) as archive:
    missing_entries = sorted(required_entries - set(archive.namelist()))
    if missing_entries:
        raise SystemExit("Darknet worldgen companion mod is incomplete: " + ", ".join(missing_entries))
    mixin = json.loads(archive.read("infinite_domain_darknet_worldgen.mixins.json"))
    if mixin.get("mixins") != ["Darknetblock1Mixin", "DragonUtilsMixin", "IafDragonDestructionManagerMixin", "LegacyGeneratedStructureMixin"] or mixin.get("client") != ["EnumDragonTexturesMixin", "EntityRenderDispatcherMixin", "HumanoidArmorLayerMixin", "LegacyDragonArmorFeatureMixin", "LegacyDragonRendererMixin", "LivingEntityRendererMixin"] or not mixin.get("required"):
        raise SystemExit("Darknet worldgen mixin configuration is not exact")
    class_bytes = archive.read("infinitedomain/darknet/mixin/LegacyGeneratedStructureMixin.class")
    if int.from_bytes(class_bytes[6:8], "big") != 65:
        raise SystemExit("Darknet worldgen companion mod is not compiled for Java 21")

mixin_source = (ROOT / "dev/packdev/darknet-worldgen-patch/src/main/java/infinitedomain/darknet/mixin/LegacyGeneratedStructureMixin.java").read_text(encoding="utf-8")
for required in ["OCEAN_FLOOR_WG", "darknet_biome", "DARKNET_CAVE_VIRTUAL_SURFACE_Y = 80"]:
    if required not in mixin_source:
        raise SystemExit(f"Darknet cave-height source lost its scope guard: {required}")

guard_source = (ROOT / "dev/packdev/darknet-worldgen-patch/src/main/java/infinitedomain/darknet/mixin/DragonUtilsMixin.java").read_text(encoding="utf-8")
explosion_source = (ROOT / "dev/packdev/darknet-worldgen-patch/src/main/java/infinitedomain/darknet/mixin/IafDragonDestructionManagerMixin.java").read_text(encoding="utf-8")
if "canGrief" not in guard_source or "callback.setReturnValue(false)" not in guard_source:
    raise SystemExit("Darknet dragon griefing guard is incomplete")
if "destroyAreaCharge" not in explosion_source or "ExplosionInteraction.NONE" not in explosion_source:
    raise SystemExit("Darknet charged-breath explosion guard is incomplete")

foundation_source = (ROOT / "dev/packdev/darknet-worldgen-patch/src/main/java/infinitedomain/darknet/mixin/Darknetblock1Mixin.java").read_text(encoding="utf-8")
for required in ["DARKNET_FOUNDATION_HARDNESS = 12.0F", "DARKNET_FOUNDATION_BLAST_RESISTANCE = 1200.0F"]:
    if required not in foundation_source:
        raise SystemExit(f"Darknet foundation mining properties changed unexpectedly: {required}")
for tag_path in [
    ROOT / "kubejs/data/minecraft/tags/block/mineable/pickaxe.json",
    ROOT / "kubejs/data/minecraft/tags/block/needs_diamond_tool.json",
]:
    tag = json.loads(tag_path.read_text(encoding="utf-8"))
    required_darknet_mining_values = {
        "cyberspace:darknetblock_1",
        "kubejs:fragmented_data_node",
        "kubejs:corrupted_data_node",
        "kubejs:encrypted_data_node",
        "kubejs:root_access_node",
    }
    if tag.get("replace") is not False or not required_darknet_mining_values.issubset(set(tag.get("values", []))):
        raise SystemExit(f"Darknet foundation mining tag is incomplete: {tag_path}")
foundation_loot = json.loads((ROOT / "kubejs/data/cyberspace/loot_table/blocks/darknetblock_1.json").read_text(encoding="utf-8"))
if "cyberspace:darknetblock_1" not in json.dumps(foundation_loot):
    raise SystemExit("Mineable Darknet foundation does not drop itself")

dragon_texture_root = ROOT / "dev/packdev/darknet-worldgen-patch/src/main/resources/assets/infinite_domain/textures/entity/darknet/models"
dragon_textures = list(dragon_texture_root.glob("*dragon/*.png"))
if len(dragon_textures) != 326:
    raise SystemExit(f"Digitized dragon texture family is incomplete: expected 326, found {len(dragon_textures)}")
for representative in [
    dragon_texture_root / "firedragon/red_5.png",
    dragon_texture_root / "icedragon/blue_5.png",
    dragon_texture_root / "lightningdragon/electric_5.png",
]:
    if not representative.is_file():
        raise SystemExit(f"Missing representative digitized dragon skin: {representative}")
texture_mixin_source = (ROOT / "dev/packdev/darknet-worldgen-patch/src/main/java/infinitedomain/darknet/mixin/EnumDragonTexturesMixin.java").read_text(encoding="utf-8")
renderer_source = (ROOT / "dev/packdev/darknet-worldgen-patch/src/main/java/infinitedomain/darknet/mixin/LegacyDragonRendererMixin.java").read_text(encoding="utf-8")
armor_source = (ROOT / "dev/packdev/darknet-worldgen-patch/src/main/java/infinitedomain/darknet/mixin/LegacyDragonArmorFeatureMixin.java").read_text(encoding="utf-8")
for required in ["getTextureFromDragon", "getEyeTextureFromDragon", "getFireDragonSkullTextures", "getIceDragonSkullTextures", "getLightningDragonSkullTextures"]:
    if required not in texture_mixin_source:
        raise SystemExit(f"Darknet dragon full-entity texture redirect lost required hook: {required}")
if "maleOverlay" not in renderer_source:
    raise SystemExit("Darknet dragon male overlay is no longer digitized")
for required in ["LegacyDragonArmorFeature", "ResourceLocation;toString", "digitize(nativeTexture)"]:
    if required not in armor_source:
        raise SystemExit(f"Darknet dragon armor redirect lost required behavior: {required}")

entity_overlay_source = (ROOT / "dev/packdev/darknet-worldgen-patch/src/main/java/infinitedomain/darknet/client/DarknetEntityOverlayLayer.java").read_text(encoding="utf-8")
living_renderer_source = (ROOT / "dev/packdev/darknet-worldgen-patch/src/main/java/infinitedomain/darknet/mixin/LivingEntityRendererMixin.java").read_text(encoding="utf-8")
humanoid_armor_source = (ROOT / "dev/packdev/darknet-worldgen-patch/src/main/java/infinitedomain/darknet/mixin/HumanoidArmorLayerMixin.java").read_text(encoding="utf-8")
for required in ["entity.isInvisible()", "DarknetGuard.isDarknet", "CIRCUITRY", "SHIMMER", "entityTranslucentEmissive"]:
    if required not in entity_overlay_source:
        raise SystemExit(f"Living-entity Darknet overlay lost required behavior: {required}")
if "LivingEntityRenderer" not in living_renderer_source or "addLayer(new DarknetEntityOverlayLayer" not in living_renderer_source:
    raise SystemExit("Universal living-entity overlay is not attached at the common renderer")
if "renderArmorPiece" not in humanoid_armor_source or humanoid_armor_source.count("renderToBuffer") != 2:
    raise SystemExit("Humanoid armor no longer receives both Darknet overlay passes")

old_patches = sorted(path.name for path in (ROOT / "mods").glob("infinite-domain-darknet-worldgen-*.jar") if path != patch_jar)
if old_patches:
    raise SystemExit("Duplicate Darknet worldgen companion mods: " + ", ".join(old_patches))

print("Audit passed: Darknet worldgen and dragon protections are intact; 326 dragon textures plus universal living-entity/player circuitry, shimmer, and armor overlays are packaged.")
