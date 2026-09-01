from __future__ import annotations

import colorsys
import csv
import hashlib
import io
from pathlib import Path
from zipfile import ZipFile

from PIL import Image

import install_more_ores_more_gems_derived_textures as pipeline


ROOT = Path(__file__).resolve().parents[2]
MOD = ROOT / "mods" / "momg-1.1.9-release-neoforge-1.21.1.jar"
MINECRAFT = Path(r"C:\Users\Admin\curseforge\minecraft\Install\versions\1.21.1\1.21.1.jar")
PACK_BLOCKS = (
    ROOT / "resourcepacks" / "LAST_DAYS_INFINITE_DOMAIN_1_21_1"
    / "assets" / "minecraft" / "textures" / "block"
)
OUTPUT = ROOT / "ROOT_tools" / "more_ores_more_gems_authored_sources" / "authored_ore_variants"
MAPPING = ROOT / "dev/docs" / "more-ores-more-gems-authored-ore-variants.csv"

STYLE_BY_FAMILY = {
    "corundum": "diamond",
    "beryl": "diamond",
    "carnelian": "diamond",
    "topaz": "diamond",
    "quartz": "lapis",
    "fluorite": "lapis",
    "ussingite": "lapis",
    "opal": "emerald",
    "jade": "emerald",
    "olivine": "emerald",
    "ekanite": "emerald",
    "autunite": "redstone",
    "sunflare": "redstone",
}

TEMPLATES = {
    "stone": {
        "diamond": "diamond_ore.png",
        "lapis": "lapis_ore.png",
        "emerald": "emerald_ore.png",
        "redstone": "redstone_ore.png",
    },
    "deepslate": {
        "diamond": "deepslate_diamond_ore.png",
        "lapis": "deepslate_lapis_ore.png",
        "emerald": "deepslate_emerald_ore.png",
        "redstone": "deepslate_redstone_ore.png",
    },
    "nether": {"diamond": "deepslate_diamond_ore.png", "lapis": "lapis_ore.png"},
}


def accent(template_style: str, red: int, green: int, blue: int) -> bool:
    hue, saturation, value = colorsys.rgb_to_hsv(red / 255, green / 255, blue / 255)
    if template_style == "diamond":
        return 0.43 <= hue <= 0.58 and saturation >= 0.18 and value >= 0.24
    if template_style == "lapis":
        return 0.54 <= hue <= 0.76 and saturation >= 0.30
    if template_style == "emerald":
        return 0.21 <= hue <= 0.46 and saturation >= 0.12
    if template_style == "redstone":
        return (hue <= 0.07 or hue >= 0.94) and saturation >= 0.28
    if template_style == "nether_quartz":
        return saturation <= 0.24 and value >= 0.54
    return 0.075 <= hue <= 0.19 and saturation >= 0.30 and value >= 0.34


def recolor_frame(
    frame: Image.Image,
    template_style: str,
    palette: list[tuple[int, int, int]],
    identity: str,
    frame_index: int,
) -> Image.Image:
    image = frame.convert("RGBA")
    pixels = image.load()
    digest = hashlib.sha256(identity.encode("utf-8")).digest()
    swatches = [colorsys.rgb_to_hsv(*(channel / 255 for channel in color)) for color in palette]
    for y in range(image.height):
        for x in range(image.width):
            red, green, blue, alpha = pixels[x, y]
            if not accent(template_style, red, green, blue):
                continue
            _, _, template_value = colorsys.rgb_to_hsv(red / 255, green / 255, blue / 255)
            swatch = swatches[(x // 6 + y // 7 + frame_index + digest[1]) % len(swatches)]
            hue, saturation, swatch_value = swatch
            value = max(0.04, min(1.0, template_value * (0.62 + swatch_value * 0.56)))
            out_red, out_green, out_blue = colorsys.hsv_to_rgb(
                hue, min(0.94, saturation * 0.92 + 0.04), value
            )
            pixels[x, y] = (
                round(out_red * 255), round(out_green * 255), round(out_blue * 255), alpha
            )
    return image


def nether_chassis(frame: Image.Image, template_style: str) -> Image.Image:
    """Heat-treat an existing mechanical ore face without introducing rock imagery."""
    image = frame.convert("RGBA")
    pixels = image.load()
    for y in range(image.height):
        for x in range(image.width):
            red, green, blue, alpha = pixels[x, y]
            if accent(template_style, red, green, blue):
                continue
            hue, saturation, value = colorsys.rgb_to_hsv(red / 255, green / 255, blue / 255)
            if 0.10 <= hue <= 0.20 and saturation > 0.30:
                hue, saturation, value = 0.055, saturation * 0.82, value * 0.82
            elif saturation < 0.24:
                hue, saturation, value = 0.035, 0.10 + saturation * 0.55, value * 0.72
            else:
                value *= 0.82
            out_red, out_green, out_blue = colorsys.hsv_to_rgb(hue, saturation, value)
            pixels[x, y] = (
                round(out_red * 255), round(out_green * 255), round(out_blue * 255), alpha
            )
    return image


def main() -> None:
    scope = list(csv.DictReader(pipeline.SCOPE.open(encoding="utf-8")))
    hosts = {
        row["RegistryId"]: row["SelectedHost"]
        for row in csv.DictReader(pipeline.HOST_ANALYSIS.open(encoding="utf-8"))
    }
    rows = []
    with ZipFile(MOD) as mod, ZipFile(MINECRAFT) as minecraft:
        vanilla_hosts = {
            family: pipeline.frames(Image.open(io.BytesIO(minecraft.read(path))))
            for family, path in pipeline.VANILLA_HOSTS.items()
        }
        for row in scope:
            identity = row["RegistryId"]
            family = pipeline.family_for(identity)
            host = hosts.get(identity)
            if row["Category"] != "ore_block" or not family or host not in TEMPLATES:
                continue
            texture_id = row["Textures"].split(";", 1)[0]
            _, texture = texture_id.split(":", 1)
            jar_path = f"assets/more_ores_more_gems/textures/{texture}.png"
            upstream = Image.open(io.BytesIO(mod.read(jar_path))).convert("RGBA")
            upstream_frame = pipeline.frames(upstream)[0]
            vanilla = vanilla_hosts[host][0]
            mineral_mask = pipeline.ore_mask(identity, upstream_frame, vanilla)
            palette = pipeline.semantic_palette(upstream_frame, mineral_mask)

            style = STYLE_BY_FAMILY[family]
            if host == "nether":
                style = "diamond" if int(hashlib.sha256(identity.encode()).hexdigest(), 16) % 2 == 0 else "lapis"
            template_name = TEMPLATES[host][style]
            accent_style = style
            template_path = PACK_BLOCKS / template_name
            template = Image.open(template_path).convert("RGBA")
            authored_frames = [
                recolor_frame(
                    nether_chassis(frame, accent_style) if host == "nether" else frame,
                    accent_style,
                    palette,
                    identity,
                    index,
                )
                for index, frame in enumerate(pipeline.frames(template))
            ]
            authored = pipeline.stack(authored_frames)
            output = OUTPUT / f"{texture}.png"
            output.parent.mkdir(parents=True, exist_ok=True)
            authored.save(output, optimize=True)
            template_meta = template_path.with_suffix(template_path.suffix + ".mcmeta")
            if template_meta.exists():
                output.with_suffix(output.suffix + ".mcmeta").write_bytes(template_meta.read_bytes())
            rows.append(
                {
                    "RegistryId": identity,
                    "Texture": texture_id,
                    "HostFamily": host,
                    "MineralFamily": family,
                    "LastDaysTemplate": template_path.relative_to(ROOT).as_posix(),
                    "AuthoredVariant": output.relative_to(ROOT).as_posix(),
                    "Frames": len(authored_frames),
                    "Method": "existing Last Days machinery artwork; material-indicator variant only; Nether chassis heat-treated",
                }
            )
    MAPPING.parent.mkdir(parents=True, exist_ok=True)
    with MAPPING.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"authored_variants={len(rows)}")
    print(f"mapping={MAPPING}")


if __name__ == "__main__":
    main()
