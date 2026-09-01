from __future__ import annotations

import csv
import io
import json
import re
from collections import Counter
from pathlib import Path
from zipfile import ZipFile

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
JAR = ROOT / "mods" / "momg-1.1.9-release-neoforge-1.21.1.jar"
NAMESPACE = "more_ores_more_gems"
PACK = (
    ROOT
    / "resourcepacks"
    / "LAST_DAYS_INFINITE_DOMAIN_1_21_1"
    / "assets"
    / NAMESPACE
)
CATALOG = ROOT / "dev/docs" / "more-ores-more-gems-texture-scope.csv"
SUMMARY = ROOT / "dev/docs" / "more-ores-more-gems-texture-scope-summary.json"

GEM_ITEMS = {
    "amethyst",
    "ametrine",
    "aquamarine",
    "autunite_234_gemstone",
    "autunite_235_gemstone",
    "autunite_238_gemstone",
    "black_opal",
    "blood_fluorite",
    "carnelian",
    "citrine",
    "ekanite",
    "fire_opal_gemstone",
    "flourite_orange_pink",
    "flourite_pink_color",
    "fluorescent_fluorite",
    "fluorite_black_color",
    "fluorite_green_color",
    "fluorite_orange_color",
    "fluorite_phantom",
    "fluorite_purple_color",
    "fluorite_purple_green",
    "fluorite_white_clear",
    "fluorite_yttrium",
    "gray_opal",
    "heliodor",
    "jade",
    "leucosapphire_gemstone",
    "luminous_gem",
    "memory_opal",
    "mysticrain_quartz",
    "olivin",
    "opalized_quartz",
    "padparadscha",
    "peridot",
    "pink_opal",
    "rare_sapphire",
    "ruby_pack",
    "sapphire",
    "small_crystal_item",
    "sunflare_gem",
    "tanzanite",
    "titanium_quartz",
    "topaz",
    "ussingite",
    "white_crystal",
    "white_opal",
}


def clean_name(value: str) -> str:
    return re.sub(r"\u00a7.", "", value).replace("�", "").strip()


def dimensions(data: bytes) -> str:
    with Image.open(io.BytesIO(data)) as image:
        return f"{image.width}x{image.height}"


def host_family(identifier: str) -> str:
    if "deepslate" in identifier or identifier == "dsto":
        return "deepslate"
    if identifier.startswith("nether_"):
        return "nether"
    if identifier.startswith("end_stone_"):
        return "end_stone"
    if identifier.startswith("clay_"):
        return "clay"
    if identifier.startswith("magma_"):
        return "magma"
    return "stone"


def main() -> None:
    with ZipFile(JAR) as archive:
        names = set(archive.namelist())
        lang = json.loads(archive.read(f"assets/{NAMESPACE}/lang/en_us.json"))

        def read_json(path: str) -> dict:
            return json.loads(archive.read(path))

        def model_textures(model_id: str, seen: set[str] | None = None) -> set[str]:
            seen = set() if seen is None else seen
            if model_id in seen:
                return set()
            seen.add(model_id)
            namespace, path = (
                model_id.split(":", 1) if ":" in model_id else ("minecraft", model_id)
            )
            model_path = f"assets/{namespace}/models/{path}.json"
            if model_path not in names:
                return set()
            model = read_json(model_path)
            found = {
                texture
                for texture in model.get("textures", {}).values()
                if isinstance(texture, str) and not texture.startswith("#")
            }
            parent = model.get("parent")
            if isinstance(parent, str):
                found.update(model_textures(parent, seen))
            return found

        def block_models(identifier: str) -> set[str]:
            path = f"assets/{NAMESPACE}/blockstates/{identifier}.json"
            if path not in names:
                return set()
            state = read_json(path)
            models: set[str] = set()
            for value in state.get("variants", {}).values():
                variants = value if isinstance(value, list) else [value]
                for variant in variants:
                    if isinstance(variant, dict) and "model" in variant:
                        models.add(variant["model"])
            for part in state.get("multipart", []):
                apply = part.get("apply", {})
                variants = apply if isinstance(apply, list) else [apply]
                for variant in variants:
                    if isinstance(variant, dict) and "model" in variant:
                        models.add(variant["model"])
            return models

        ore_ids = []
        for key, display in lang.items():
            prefix = f"block.{NAMESPACE}."
            if not key.startswith(prefix):
                continue
            identifier = key[len(prefix) :]
            cleaned = clean_name(display)
            if re.search(r"\bore\b", cleaned, re.IGNORECASE) or identifier.endswith("_ore"):
                ore_ids.append(identifier)

        rows: list[dict[str, str]] = []
        texture_paths: set[str] = set()

        def append(identifier: str, asset_type: str, category: str, models: set[str]) -> None:
            textures: set[str] = set()
            for model in models:
                textures.update(model_textures(model))
            textures = {
                texture for texture in textures if texture.startswith(f"{NAMESPACE}:")
            }
            texture_paths.update(textures)
            lang_key = f"{asset_type}.{NAMESPACE}.{identifier}"
            rows.append(
                {
                    "Category": category,
                    "RegistryId": f"{NAMESPACE}:{identifier}",
                    "DisplayName": clean_name(lang.get(lang_key, identifier)),
                    "HostFamily": host_family(identifier) if category == "ore_block" else "",
                    "Models": ";".join(sorted(models)),
                    "Textures": ";".join(sorted(textures)),
                }
            )

        for identifier in sorted(set(ore_ids)):
            append(identifier, "block", "ore_block", block_models(identifier))

        for identifier in sorted(GEM_ITEMS):
            model = f"{NAMESPACE}:item/{identifier}"
            append(identifier, "item", "gem_item", {model})

        gem_words = {
            clean_name(lang.get(f"item.{NAMESPACE}.{identifier}", identifier)).lower()
            for identifier in GEM_ITEMS
        }
        block_prefix = f"block.{NAMESPACE}."
        for key, display in sorted(lang.items()):
            if not key.startswith(block_prefix):
                continue
            identifier = key[len(block_prefix) :]
            cleaned = clean_name(display).lower()
            if not cleaned.startswith("block of "):
                continue
            material = cleaned.removeprefix("block of ").strip()
            if any(material == gem or material in gem or gem in material for gem in gem_words):
                append(identifier, "block", "gem_storage_block", block_models(identifier))

        texture_rows = []
        for texture in sorted(texture_paths):
            namespace, texture_id = texture.split(":", 1)
            jar_path = f"assets/{namespace}/textures/{texture_id}.png"
            pack_path = PACK / "textures" / f"{texture_id}.png"
            upstream = archive.read(jar_path) if jar_path in names else b""
            local = pack_path.read_bytes() if pack_path.is_file() else b""
            texture_rows.append(
                {
                    "Texture": texture,
                    "JarPath": jar_path,
                    "PackPath": pack_path.relative_to(ROOT).as_posix(),
                    "UpstreamSize": dimensions(upstream) if upstream else "missing",
                    "PackSize": dimensions(local) if local else "missing",
                    "PackOverride": "yes" if local else "no",
                    "DiffersFromUpstream": (
                        "yes" if local and upstream and local != upstream else "no"
                    ),
                }
            )

    CATALOG.parent.mkdir(parents=True, exist_ok=True)
    with CATALOG.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = [
            "Category",
            "RegistryId",
            "DisplayName",
            "HostFamily",
            "Models",
            "Textures",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sorted(rows, key=lambda row: (row["Category"], row["RegistryId"])))

    texture_catalog = CATALOG.with_name("more-ores-more-gems-live-textures.csv")
    with texture_catalog.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=texture_rows[0].keys())
        writer.writeheader()
        writer.writerows(texture_rows)

    summary = {
        "mod": JAR.relative_to(ROOT).as_posix(),
        "scope": Counter(row["Category"] for row in rows),
        "ore_host_families": Counter(
            row["HostFamily"] for row in rows if row["Category"] == "ore_block"
        ),
        "live_texture_count": len(texture_rows),
        "pack_overrides": sum(row["PackOverride"] == "yes" for row in texture_rows),
        "pack_overrides_different_from_upstream": sum(
            row["DiffersFromUpstream"] == "yes" for row in texture_rows
        ),
        "catalog": CATALOG.relative_to(ROOT).as_posix(),
        "texture_catalog": texture_catalog.relative_to(ROOT).as_posix(),
    }
    SUMMARY.write_text(json.dumps(summary, indent=2, default=dict) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, default=dict))


if __name__ == "__main__":
    main()
