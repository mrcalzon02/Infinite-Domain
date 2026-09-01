from __future__ import annotations

import colorsys
import csv
import hashlib
import io
from pathlib import Path
from zipfile import ZipFile

from PIL import Image, ImageDraw, ImageFont

import install_more_ores_more_gems_derived_textures as pipeline


ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "mods" / "momg-1.1.9-release-neoforge-1.21.1.jar"
MINECRAFT = Path(r"C:\Users\Admin\curseforge\minecraft\Install\versions\1.21.1\1.21.1.jar")
GENERIC = (
    ROOT / "ROOT_tools" / "more_ores_more_gems_authored_sources"
    / "generic_gem_containment" / "deepslate_master.png"
)
MASTERS = GENERIC.parent / "recolored_masters"
RUNTIME = (
    ROOT / "resourcepacks" / "LAST_DAYS_INFINITE_DOMAIN_1_21_1"
    / "assets" / "more_ores_more_gems" / "textures"
)
MAPPING = ROOT / "docs" / "more-ores-more-gems-generic-containment-recolors.csv"
REVIEW = ROOT / "ROOT_tools" / "more_ores_more_gems_generic_containment_review"
SIZE = 32


def gem_mask(red: int, green: int, blue: int, x: int, y: int, width: int, height: int) -> bool:
    if not (0.49 <= x / width <= 0.73 and 0.25 <= y / height <= 0.75):
        return False
    hue, saturation, value = colorsys.rgb_to_hsv(red / 255, green / 255, blue / 255)
    return 0.68 <= hue <= 0.91 and saturation >= 0.16 and value >= 0.09


def recolor(master: Image.Image, palette: list[tuple[int, int, int]]) -> Image.Image:
    image = master.convert("RGBA").copy()
    pixels = image.load()
    swatches = [colorsys.rgb_to_hsv(*(channel / 255 for channel in color)) for color in palette]
    for y in range(image.height):
        for x in range(image.width):
            red, green, blue, alpha = pixels[x, y]
            if not gem_mask(red, green, blue, x, y, image.width, image.height):
                continue
            _, _, source_value = colorsys.rgb_to_hsv(red / 255, green / 255, blue / 255)
            zone = min(len(swatches) - 1, int((x / image.width - 0.49) / 0.24 * len(swatches)))
            hue, saturation, swatch_value = swatches[zone]
            value = max(0.035, min(1.0, source_value * (0.68 + swatch_value * 0.46)))
            out_red, out_green, out_blue = colorsys.hsv_to_rgb(
                hue, min(0.95, saturation * 0.92 + 0.04), value
            )
            pixels[x, y] = (
                round(out_red * 255), round(out_green * 255), round(out_blue * 255), alpha
            )
    return image


def make_reviews(entries: list[tuple[str, Image.Image]]) -> None:
    REVIEW.mkdir(parents=True, exist_ok=True)
    font = ImageFont.load_default(size=13)
    for sheet_number, start in enumerate(range(0, len(entries), 25), 1):
        batch = entries[start : start + 25]
        sheet = Image.new("RGB", (5 * 180, 5 * 205), (17, 19, 18))
        draw = ImageDraw.Draw(sheet)
        for index, (name, image) in enumerate(batch):
            x, y = (index % 5) * 180 + 10, (index // 5) * 205 + 8
            preview = image.convert("RGB").resize((160, 160), Image.Resampling.NEAREST)
            sheet.paste(preview, (x, y))
            draw.text((x, y + 166), name[:25], fill=(226, 224, 210), font=font)
        sheet.save(REVIEW / f"generic_gem_ore_{sheet_number:02d}.png", optimize=True)


def main() -> None:
    master = Image.open(GENERIC).convert("RGBA")
    scope = list(csv.DictReader(pipeline.SCOPE.open(encoding="utf-8")))
    hosts = {
        row["RegistryId"]: row["SelectedHost"]
        for row in csv.DictReader(pipeline.HOST_ANALYSIS.open(encoding="utf-8"))
    }
    rows = []
    reviews = []
    with ZipFile(MOD) as mod, ZipFile(MINECRAFT) as minecraft:
        vanilla_hosts = {
            family: pipeline.frames(Image.open(io.BytesIO(minecraft.read(path))))
            for family, path in pipeline.VANILLA_HOSTS.items()
        }
        for row in scope:
            identity = row["RegistryId"]
            host = hosts.get(identity)
            if (
                row["Category"] != "ore_block"
                or not pipeline.family_for(identity)
                or host not in {"stone", "deepslate", "nether"}
            ):
                continue
            texture_id = row["Textures"].split(";", 1)[0]
            _, texture = texture_id.split(":", 1)
            source_bytes = mod.read(f"assets/more_ores_more_gems/textures/{texture}.png")
            source = pipeline.frames(Image.open(io.BytesIO(source_bytes)).convert("RGBA"))[0]
            mask = pipeline.ore_mask(identity, source, vanilla_hosts[host][0])
            palette = pipeline.semantic_palette(source, mask)
            authored = recolor(master, palette)
            master_path = MASTERS / f"{texture}_master.png"
            master_path.parent.mkdir(parents=True, exist_ok=True)
            authored.save(master_path, optimize=True)
            runtime = authored.resize((SIZE, SIZE), Image.Resampling.LANCZOS)
            runtime_path = RUNTIME / f"{texture}.png"
            runtime_path.parent.mkdir(parents=True, exist_ok=True)
            runtime.save(runtime_path, optimize=True)
            runtime_meta = runtime_path.with_suffix(runtime_path.suffix + ".mcmeta")
            if runtime_meta.exists():
                runtime_meta.unlink()
            rows.append(
                {
                    "RegistryId": identity,
                    "Texture": texture_id,
                    "GenericMaster": GENERIC.relative_to(ROOT).as_posix(),
                    "RecoloredMaster": master_path.relative_to(ROOT).as_posix(),
                    "Runtime": runtime_path.relative_to(ROOT).as_posix(),
                    "Palette": ";".join("#%02x%02x%02x" % color for color in palette),
                    "MasterSha256": hashlib.sha256(master_path.read_bytes()).hexdigest(),
                    "Method": "approved generic containment unit; contained gem recolor only",
                }
            )
            reviews.append((identity.split(":", 1)[1], runtime))
    with MAPPING.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    make_reviews(reviews)
    print(f"recolored_gem_ores={len(rows)}")
    print(f"runtime_resolution={SIZE}")
    print(f"mapping={MAPPING}")
    print(f"review_sheets={(len(reviews) + 24) // 25}")


if __name__ == "__main__":
    main()
