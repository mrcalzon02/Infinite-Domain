from __future__ import annotations

import csv
import io
import json
from pathlib import Path
from zipfile import ZipFile

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "mods" / "momg-1.1.9-release-neoforge-1.21.1.jar"
PACK = ROOT / "resourcepacks" / "LAST_DAYS_INFINITE_DOMAIN_1_21_1"
SCOPE = ROOT / "docs" / "more-ores-more-gems-texture-scope.csv"
MANIFEST = ROOT / "docs" / "more-ores-more-gems-derived-textures.json"
SIZE = 128
GEM_ORE_SIZE = 32
GEM_ORE_MASTERS = (
    ROOT / "ROOT_tools" / "more_ores_more_gems_authored_sources"
    / "generic_gem_containment" / "recolored_masters"
)
METAL_ORE_MASTERS = (
    ROOT / "ROOT_tools" / "more_ores_more_gems_authored_sources"
    / "generic_metal_ore_container" / "recolored_masters"
)


def main() -> None:
    rows = list(csv.DictReader(SCOPE.open(encoding="utf-8")))
    textures: dict[str, str] = {}
    for row in rows:
        for texture in filter(None, row["Textures"].split(";")):
            textures[texture] = row["Category"]

    animated = 0
    transparent_items = 0
    errors: list[str] = []
    with ZipFile(MOD) as mod:
        names = set(mod.namelist())
        for texture_id, category in sorted(textures.items()):
            namespace, texture = texture_id.split(":", 1)
            jar_path = f"assets/{namespace}/textures/{texture}.png"
            output = PACK / "assets" / namespace / "textures" / f"{texture}.png"
            if not output.exists():
                errors.append(f"missing output: {texture_id}")
                continue
            with Image.open(io.BytesIO(mod.read(jar_path))) as source:
                frames = max(1, source.height // source.width)
            authored_gem_ore = GEM_ORE_MASTERS / f"{texture}_master.png"
            authored_metal_ore = METAL_ORE_MASTERS / f"{texture}_master.png"
            authored_ore = authored_gem_ore.exists() or authored_metal_ore.exists()
            expected_size = (
                (GEM_ORE_SIZE, GEM_ORE_SIZE)
                if authored_ore
                else (SIZE, SIZE * frames)
            )
            with Image.open(output) as derived:
                if derived.size != expected_size:
                    errors.append(
                        f"wrong size: {texture_id} {derived.size}, expected {expected_size}"
                    )
                if category == "gem_item":
                    alpha = derived.convert("RGBA").getchannel("A")
                    if alpha.getextrema()[0] != 0 or alpha.getbbox() is None:
                        errors.append(f"item alpha contract failed: {texture_id}")
                    else:
                        transparent_items += 1
            meta_path = jar_path + ".mcmeta"
            output_meta = output.with_suffix(output.suffix + ".mcmeta")
            if authored_ore:
                if output_meta.exists():
                    errors.append(f"generic containment ore must be static: {texture_id}")
            elif meta_path in names:
                animated += 1
                if not output_meta.exists() or output_meta.read_bytes() != mod.read(meta_path):
                    errors.append(f"animation metadata mismatch: {texture_id}")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if len(manifest["outputs"]) != len(textures):
        errors.append("manifest output count mismatch")
    expected_generated_sources = 3 + 13 + 63 + 71
    if len(manifest["generated_sources"]) != expected_generated_sources:
        errors.append(
            "generated source count mismatch (expected 3 materials + 13 families + 63 gem + 71 metal recolors)"
        )

    model_overrides = list((PACK / "assets" / "more_ores_more_gems" / "models").rglob("*.json"))
    blockstate_overrides = list((PACK / "assets" / "more_ores_more_gems" / "blockstates").rglob("*.json"))
    if model_overrides or blockstate_overrides:
        errors.append(
            f"unexpected model contract overrides: models={len(model_overrides)} blockstates={len(blockstate_overrides)}"
        )

    if errors:
        print("validation=FAILED")
        for error in errors:
            print(error)
        raise SystemExit(1)
    print("validation=PASS")
    print(f"live_textures={len(textures)}")
    print(f"animated_textures={animated}")
    print(f"transparent_gem_items={transparent_items}")
    print("generic_containment_gem_ores=63")
    print("generic_metal_container_ores=71")
    print(f"generated_sources={expected_generated_sources}")
    print("model_overrides=0")
    print("blockstate_overrides=0")


if __name__ == "__main__":
    main()
