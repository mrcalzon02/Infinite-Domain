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
    / "generic_metal_ore_container" / "master.png"
)
MASTERS = GENERIC.parent / "recolored_masters"
GEM_MASTERS = (
    ROOT / "ROOT_tools" / "more_ores_more_gems_authored_sources"
    / "generic_gem_containment" / "recolored_masters"
)
RUNTIME = (
    ROOT / "resourcepacks" / "LAST_DAYS_INFINITE_DOMAIN_1_21_1"
    / "assets" / "more_ores_more_gems" / "textures"
)
MAPPING = ROOT / "docs" / "more-ores-more-gems-generic-metal-container-recolors.csv"
REVIEW = ROOT / "ROOT_tools" / "more_ores_more_gems_generic_metal_container_review"
SIZE = 32


def sample_mask(red: int, green: int, blue: int, x: int, y: int, width: int, height: int) -> bool:
    if not (0.39 <= x / width <= 0.58 and 0.39 <= y / height <= 0.66):
        return False
    _, saturation, value = colorsys.rgb_to_hsv(red / 255, green / 255, blue / 255)
    return saturation <= 0.30 and value >= 0.28


def stripe_mask(red: int, green: int, blue: int, x: int, y: int, width: int, height: int) -> bool:
    normalized_x, normalized_y = x / width, y / height
    in_plate = (
        0.24 <= normalized_x <= 0.58 and 0.18 <= normalized_y <= 0.40
    ) or (
        0.46 <= normalized_x <= 0.77 and 0.66 <= normalized_y <= 0.85
    )
    hue, saturation, value = colorsys.rgb_to_hsv(red / 255, green / 255, blue / 255)
    return in_plate and 0.07 <= hue <= 0.18 and saturation >= 0.32 and value >= 0.24


def recolor(
    master: Image.Image,
    palette: list[tuple[int, int, int]],
    identity: str,
) -> tuple[Image.Image, str, str]:
    image = master.convert("RGBA").copy()
    pixels = image.load()
    swatches = [colorsys.rgb_to_hsv(*(channel / 255 for channel in color)) for color in palette]
    sample_hsv = max(swatches, key=lambda hsv: hsv[2] * (0.45 + hsv[1]))
    saturated = [hsv for hsv in swatches if hsv[1] >= 0.18]
    if saturated:
        stripe_hsv = max(saturated, key=lambda hsv: hsv[1] * hsv[2])
    else:
        warning_hues = (0.035, 0.11, 0.34, 0.56, 0.78)
        stripe_hsv = (
            warning_hues[hashlib.sha256(identity.encode()).digest()[0] % len(warning_hues)],
            0.72,
            0.72,
        )
    for y in range(image.height):
        for x in range(image.width):
            red, green, blue, alpha = pixels[x, y]
            if sample_mask(red, green, blue, x, y, image.width, image.height):
                _, _, source_value = colorsys.rgb_to_hsv(red / 255, green / 255, blue / 255)
                hue, saturation, target_value = sample_hsv
                value = max(0.06, min(1.0, source_value * (0.70 + target_value * 0.45)))
                out_red, out_green, out_blue = colorsys.hsv_to_rgb(
                    hue, min(0.82, saturation * 0.86 + 0.025), value
                )
            elif stripe_mask(red, green, blue, x, y, image.width, image.height):
                _, _, source_value = colorsys.rgb_to_hsv(red / 255, green / 255, blue / 255)
                hue, saturation, target_value = stripe_hsv
                value = max(0.16, min(0.88, source_value * (0.72 + target_value * 0.42)))
                out_red, out_green, out_blue = colorsys.hsv_to_rgb(
                    hue, max(0.48, min(0.92, saturation)), value
                )
            else:
                continue
            pixels[x, y] = (
                round(out_red * 255), round(out_green * 255), round(out_blue * 255), alpha
            )
    sample_rgb = tuple(round(channel * 255) for channel in colorsys.hsv_to_rgb(*sample_hsv))
    sample_hex = "#%02x%02x%02x" % sample_rgb
    stripe_rgb = tuple(round(channel * 255) for channel in colorsys.hsv_to_rgb(*stripe_hsv))
    stripe_hex = "#%02x%02x%02x" % stripe_rgb
    return image, sample_hex, stripe_hex


def make_reviews(entries: list[tuple[str, Image.Image]]) -> None:
    REVIEW.mkdir(parents=True, exist_ok=True)
    font = ImageFont.load_default(size=13)
    for sheet_number, start in enumerate(range(0, len(entries), 25), 1):
        batch = entries[start : start + 25]
        sheet = Image.new("RGB", (5 * 180, 5 * 205), (17, 19, 18))
        draw = ImageDraw.Draw(sheet)
        for index, (name, image) in enumerate(batch):
            x, y = (index % 5) * 180 + 10, (index // 5) * 205 + 8
            sheet.paste(image.convert("RGB").resize((160, 160), Image.Resampling.NEAREST), (x, y))
            draw.text((x, y + 166), name[:25], fill=(226, 224, 210), font=font)
        sheet.save(REVIEW / f"generic_metal_ore_{sheet_number:02d}.png", optimize=True)


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
            if row["Category"] != "ore_block":
                continue
            identity = row["RegistryId"]
            texture_id = row["Textures"].split(";", 1)[0]
            _, texture = texture_id.split(":", 1)
            if (GEM_MASTERS / f"{texture}_master.png").exists():
                continue
            source_bytes = mod.read(f"assets/more_ores_more_gems/textures/{texture}.png")
            source = pipeline.frames(Image.open(io.BytesIO(source_bytes)).convert("RGBA"))[0]
            host = hosts[identity]
            mask = pipeline.ore_mask(identity, source, vanilla_hosts[host][0])
            palette = pipeline.semantic_palette(source, mask)
            authored, sample_color, stripe_color = recolor(master, palette, identity)
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
                    "SampleColor": sample_color,
                    "HazardStripeColor": stripe_color,
                    "Method": "approved generic metallic container; sample insert and hazard-paint recolor only",
                }
            )
            reviews.append((identity.split(":", 1)[1], runtime))
    with MAPPING.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    make_reviews(reviews)
    print(f"recolored_metal_ores={len(rows)}")
    print(f"runtime_resolution={SIZE}")
    print(f"mapping={MAPPING}")
    print(f"review_sheets={(len(reviews) + 24) // 25}")


if __name__ == "__main__":
    main()
