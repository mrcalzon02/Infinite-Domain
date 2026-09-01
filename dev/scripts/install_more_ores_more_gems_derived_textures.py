from __future__ import annotations

import csv
import colorsys
import hashlib
import io
import json
import math
from collections import defaultdict
from pathlib import Path
from zipfile import ZipFile

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[2]
MOD = ROOT / "mods" / "momg-1.1.9-release-neoforge-1.21.1.jar"
MINECRAFT = Path(
    r"C:\Users\Admin\curseforge\minecraft\Install\versions\1.21.1\1.21.1.jar"
)
NAMESPACE = "more_ores_more_gems"
PACK_ASSETS = (
    ROOT
    / "resourcepacks"
    / "LAST_DAYS_INFINITE_DOMAIN_1_21_1"
    / "assets"
)
TARGET = PACK_ASSETS / NAMESPACE / "textures"
SOURCES = ROOT / "ROOT_tools" / "more_ores_more_gems_authored_sources"
UPSTREAM = SOURCES / "upstream_live"
GENERATED = SOURCES / "generated_materials"
GENERATED_FAMILIES = SOURCES / "generated_gem_families"
AUTHORED_ORE_FACES = SOURCES / "generic_gem_containment" / "recolored_masters"
METAL_ORE_FACES = SOURCES / "generic_metal_ore_container" / "recolored_masters"
SCOPE = ROOT / "dev/docs" / "more-ores-more-gems-texture-scope.csv"
HOST_ANALYSIS = ROOT / "dev/docs" / "more-ores-more-gems-ore-host-analysis.csv"
LEDGER = ROOT / "dev/docs" / "more-ores-more-gems-derived-textures.csv"
MANIFEST = ROOT / "dev/docs" / "more-ores-more-gems-derived-textures.json"
REVIEW = ROOT / "ROOT_tools" / "more_ores_more_gems_review"
SIZE = 128
ORE_SIZE = 32

HOST_TEXTURES = {
    "stone": "stone.png",
    "deepslate": "deepslate.png",
    "nether": "netherrack.png",
    "end_stone": "end_stone.png",
    "clay": "clay.png",
    "magma": "magma.png",
}
VANILLA_HOSTS = {
    family: f"assets/minecraft/textures/block/{name}"
    for family, name in HOST_TEXTURES.items()
}
MANUAL_MASKS = {
    "more_ores_more_gems:aquamarine_ore": "colorful",
    "more_ores_more_gems:bromine_ore": "colorful",
    "more_ores_more_gems:deepslate_aquamarine_ore": "colorful",
    "more_ores_more_gems:dsto": "bright_neutral",
    "more_ores_more_gems:luminous_gem_ore": "colorful",
    "more_ores_more_gems:nether_osmium_ore": "low_saturation",
    "more_ores_more_gems:radium_ore": "colorful",
}

GEM_FAMILIES = {
    "corundum": {
        "leucosapphire_gemstone", "padparadscha", "rare_sapphire", "ruby_pack",
        "sapphire", "tanzanite",
    },
    "opal": {
        "black_opal", "fire_opal_gemstone", "gray_opal", "memory_opal",
        "pink_opal", "white_opal",
    },
    "fluorite": {
        "blood_fluorite", "flourite_orange_pink", "flourite_pink_color",
        "fluorescent_fluorite", "fluorite_black_color", "fluorite_green_color",
        "fluorite_orange_color", "fluorite_phantom", "fluorite_purple_color",
        "fluorite_purple_green", "fluorite_white_clear", "fluorite_yttrium",
        "luminous_gem",
    },
    "autunite": {
        "autunite_234_gemstone", "autunite_235_gemstone", "autunite_238_gemstone",
    },
    "beryl": {"aquamarine", "heliodor"},
    "quartz": {
        "amethyst", "ametrine", "citrine", "mysticrain_quartz",
        "opalized_quartz", "titanium_quartz", "small_crystal_item", "white_crystal",
    },
    "olivine": {"olivin", "peridot"},
    "carnelian": {"carnelian"},
    "ekanite": {"ekanite"},
    "ussingite": {"ussingite"},
    "jade": {"jade"},
    "sunflare": {"sunflare_gem"},
    "topaz": {"topaz"},
}

FAMILY_KEYWORDS = {
    "corundum": ("sapphire", "ruby", "padparadscha", "tanzanite"),
    "opal": ("opal",),
    "fluorite": ("fluorite", "flourite", "luminous"),
    "autunite": ("autunite",),
    "beryl": ("aquamarine", "heliodor"),
    "quartz": ("quartz", "amethyst", "ametrine", "citrine", "white_crystal"),
    "olivine": ("olivin", "peridot"),
    "carnelian": ("carnelian",),
    "ekanite": ("ekanite",),
    "ussingite": ("ussingite",),
    "jade": ("jade",),
    "sunflare": ("sunflare",),
    "topaz": ("topaz",),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frames(image: Image.Image) -> list[Image.Image]:
    image = image.convert("RGBA")
    count = max(1, image.height // image.width)
    return [
        image.crop((0, index * image.width, image.width, (index + 1) * image.width))
        for index in range(count)
    ]


def stack(images: list[Image.Image]) -> Image.Image:
    mode = "RGBA" if any(image.mode == "RGBA" for image in images) else "RGB"
    sheet = Image.new(mode, (images[0].width, images[0].height * len(images)))
    for index, image in enumerate(images):
        sheet.paste(image.convert(mode), (0, index * images[0].height))
    return sheet


def stable_variant(image: Image.Image, identity: str) -> Image.Image:
    digest = hashlib.sha256(identity.encode("utf-8")).digest()
    turns = digest[0] % 4
    result = image.rotate(-90 * turns, expand=False)
    if digest[1] & 1:
        result = result.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    if digest[1] & 2:
        result = result.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    return result


def material(name: str, identity: str, mode: str = "RGB") -> Image.Image:
    image = Image.open(GENERATED / name).convert(mode)
    edge = min(image.size)
    image = image.crop(
        (
            (image.width - edge) // 2,
            (image.height - edge) // 2,
            (image.width + edge) // 2,
            (image.height + edge) // 2,
        )
    )
    image = stable_variant(image, identity)
    return image.resize((SIZE, SIZE), Image.Resampling.LANCZOS)


def family_for(identity: str) -> str | None:
    name = identity.split(":", 1)[-1]
    for family, members in GEM_FAMILIES.items():
        if name in members:
            return family
    for family, keywords in FAMILY_KEYWORDS.items():
        if any(keyword in name for keyword in keywords):
            return family
    return None


def family_master(family: str, identity: str, extent: int = SIZE) -> Image.Image:
    image = Image.open(GENERATED_FAMILIES / f"{family}_master.png").convert("RGBA")
    bbox = image.getchannel("A").getbbox()
    if bbox:
        image = image.crop(bbox)
    image.thumbnail((extent, extent), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (SIZE, SIZE))
    x = (SIZE - image.width) // 2
    y = (SIZE - image.height) // 2
    canvas.alpha_composite(image, (x, y))
    return stable_variant(canvas, identity)


def family_relief(family: str, identity: str) -> Image.Image:
    master = family_master(family, identity).convert("RGBA")
    gray = master.convert("L")
    alpha = master.getchannel("A")
    visible = [value for value, opacity in zip(gray.getdata(), alpha.getdata()) if opacity > 32]
    neutral = sorted(visible)[len(visible) // 2] if visible else 128
    return Image.composite(gray, Image.new("L", gray.size, neutral), alpha)


def semantic_palette(
    image: Image.Image, mask: Image.Image | None = None
) -> list[tuple[int, int, int]]:
    """Extract non-spatial color swatches; pixel positions are deliberately discarded."""
    rgba = image.convert("RGBA")
    alpha = rgba.getchannel("A")
    if mask is not None:
        alpha = ImageChops.multiply(alpha, mask.convert("L").resize(rgba.size))
    pixels = [
        pixel[:3]
        for pixel, opacity in zip(rgba.getdata(), alpha.getdata())
        if opacity > 48
    ]
    if not pixels:
        return [(128, 128, 128)]
    sample = Image.new("RGB", (len(pixels), 1))
    sample.putdata(pixels)
    quantized = sample.quantize(colors=8, method=Image.Quantize.MEDIANCUT).convert("RGB")
    candidates = [color for _, color in sorted(quantized.getcolors(8) or [], reverse=True)]
    selected: list[tuple[int, int, int]] = []
    selected_hsv: list[tuple[float, float, float]] = []
    for color in candidates:
        hsv = colorsys.rgb_to_hsv(*(channel / 255 for channel in color))
        if hsv[2] < 0.07:
            continue
        if not selected_hsv or all(
            min(abs(hsv[0] - other[0]), 1 - abs(hsv[0] - other[0])) > 0.075
            or abs(hsv[1] - other[1]) > 0.28
            for other in selected_hsv
        ):
            selected.append(color)
            selected_hsv.append(hsv)
        if len(selected) == 4:
            break
    return selected or [candidates[0]]


def colorize_authored_relief(
    relief: Image.Image, palette: list[tuple[int, int, int]], identity: str
) -> Image.Image:
    """Apply unordered swatches across authored lighting, never an upstream color map."""
    rgba = relief.convert("RGBA")
    luma = rgba.convert("L")
    alpha = rgba.getchannel("A")
    swatches = [
        colorsys.rgb_to_hsv(*(channel / 255 for channel in color)) for color in palette
    ]
    digest = hashlib.sha256(identity.encode("utf-8")).digest()
    angle = digest[3] / 255 * math.pi
    axis_x, axis_y = math.cos(angle), math.sin(angle)
    corners = [
        x * axis_x + y * axis_y
        for x, y in ((0, 0), (SIZE - 1, 0), (0, SIZE - 1), (SIZE - 1, SIZE - 1))
    ]
    low, span = min(corners), max(1.0, max(corners) - min(corners))
    output = Image.new("RGBA", rgba.size)
    out_pixels, light_pixels, alpha_pixels = output.load(), luma.load(), alpha.load()
    for y in range(SIZE):
        for x in range(SIZE):
            opacity = alpha_pixels[x, y]
            if not opacity:
                continue
            if len(swatches) == 1:
                hue, saturation, source_value = swatches[0]
            else:
                position = ((x * axis_x + y * axis_y - low) / span) * (len(swatches) - 1)
                first, second = min(len(swatches) - 1, int(position)), min(len(swatches) - 1, int(position) + 1)
                blend = position - first
                h1, s1, v1 = swatches[first]
                h2, s2, v2 = swatches[second]
                delta = h2 - h1
                if abs(delta) > 0.5:
                    delta -= math.copysign(1.0, delta)
                hue = (h1 + delta * blend) % 1.0
                saturation = s1 + (s2 - s1) * blend
                source_value = v1 + (v2 - v1) * blend
            authored_light = light_pixels[x, y] / 255
            value = max(0.035, min(0.94, authored_light * 0.82 + source_value * 0.18))
            saturation = min(0.86, saturation * 0.88 + 0.035)
            red, green, blue = colorsys.hsv_to_rgb(hue, saturation, value)
            out_pixels[x, y] = (
                round(red * 255), round(green * 255), round(blue * 255), opacity
            )
    return output


def max_channel_difference(first: Image.Image, second: Image.Image) -> Image.Image:
    difference = ImageChops.difference(first.convert("RGB"), second.convert("RGB"))
    red, green, blue = difference.split()
    return ImageChops.lighter(ImageChops.lighter(red, green), blue)


def manual_mask(frame: Image.Image, kind: str) -> Image.Image:
    rgb = frame.convert("RGB")
    mask = Image.new("L", rgb.size)
    output = []
    for red, green, blue in rgb.getdata():
        high = max(red, green, blue)
        low = min(red, green, blue)
        saturation = 0 if high == 0 else (high - low) / high
        luminance = 0.299 * red + 0.587 * green + 0.114 * blue
        if kind == "colorful":
            value = max(0, min(255, round((saturation - 0.12) * 800)))
        elif kind == "bright_neutral":
            value = 255 if saturation < 0.30 and luminance > 92 else 0
        else:
            value = 255 if saturation < 0.24 and luminance > 48 else 0
        output.append(value)
    mask.putdata(output)
    return mask


def ore_mask(
    registry_id: str, source: Image.Image, vanilla_host: Image.Image
) -> Image.Image:
    if registry_id in MANUAL_MASKS:
        return manual_mask(source, MANUAL_MASKS[registry_id])
    difference = max_channel_difference(source, vanilla_host.resize(source.size))
    return difference.point(lambda value: max(0, min(255, (value - 4) * 9)))


def host_frame(hosts: dict[str, list[Image.Image]], family: str, index: int) -> Image.Image:
    choices = hosts[family]
    return choices[index % len(choices)].convert("RGB").resize(
        (SIZE, SIZE), Image.Resampling.NEAREST
    ).filter(ImageFilter.UnsharpMask(radius=0.7, percent=70, threshold=2))


def grade(
    image: Image.Image, saturation: float, brightness: float, contrast: float
) -> Image.Image:
    image = ImageEnhance.Color(image).enhance(saturation)
    image = ImageEnhance.Brightness(image).enhance(brightness)
    return ImageEnhance.Contrast(image).enhance(contrast)


def derive_ore(
    registry_id: str,
    source_frames: list[Image.Image],
    family: str,
    vanilla_hosts: dict[str, list[Image.Image]],
    last_days_hosts: dict[str, list[Image.Image]],
) -> Image.Image:
    mineral_family = family_for(registry_id)
    relief = (
        family_relief(mineral_family, registry_id)
        if mineral_family
        else material("neutral_ore_relief_master.png", registry_id).convert("L")
    )
    outputs = []
    for index, source in enumerate(source_frames):
        vanilla = vanilla_hosts[family][index % len(vanilla_hosts[family])]
        small_mask = ore_mask(registry_id, source, vanilla)
        anchor = small_mask.resize((SIZE, SIZE), Image.Resampling.BILINEAR)
        mask = Image.new("L", (SIZE, SIZE))
        mask.putdata(
            [
                max(0, min(255, round((base - 82) * 1.62 + (surface - 128) * 0.52)))
                for base, surface in zip(anchor.getdata(), relief.getdata())
            ]
        )
        mask = mask.filter(ImageFilter.GaussianBlur(0.45))
        host = host_frame(last_days_hosts, family, index)

        blurred = mask.filter(ImageFilter.GaussianBlur(2.2))
        outside_shadow = ImageChops.subtract(blurred, mask)
        shadow = Image.new("RGB", host.size, (8, 10, 9))
        host = Image.composite(shadow, host, outside_shadow.point(lambda v: v * 2 // 3))

        authored_relief = Image.merge(
            "RGBA", (relief, relief, relief, Image.new("L", (SIZE, SIZE), 255))
        )
        lit = colorize_authored_relief(
            authored_relief, semantic_palette(source, small_mask), registry_id
        ).convert("RGB")
        lit = grade(lit, saturation=0.82, brightness=0.80, contrast=1.14)
        lit = lit.filter(ImageFilter.UnsharpMask(radius=0.75, percent=95, threshold=2))
        outputs.append(Image.composite(lit, host, mask).convert("RGBA"))
    return stack(outputs)


def derive_gem(identity: str, source_frames: list[Image.Image]) -> Image.Image:
    family = family_for(identity)
    if not family:
        raise ValueError(f"No authored gem family assigned for {identity}")
    master = family_master(family, identity, extent=112)
    outputs = []
    for source in source_frames:
        lit = colorize_authored_relief(master, semantic_palette(source), identity)
        lit = grade(lit.convert("RGB"), saturation=0.84, brightness=0.78, contrast=1.14)
        alpha = master.getchannel("A")
        lit.putalpha(alpha)
        outputs.append(lit)
    return stack(outputs)


def derive_storage(identity: str, source_frames: list[Image.Image]) -> Image.Image:
    mineral_family = family_for(identity)
    neutral_relief = material("neutral_storage_crystal_master.png", identity).convert("L")
    relief = Image.blend(neutral_relief, family_relief(mineral_family, identity), 0.28) if mineral_family else neutral_relief
    outputs = []
    for source in source_frames:
        authored_relief = Image.merge(
            "RGBA", (relief, relief, relief, Image.new("L", (SIZE, SIZE), 255))
        )
        lit = colorize_authored_relief(
            authored_relief, semantic_palette(source), identity
        ).convert("RGB")
        lit = grade(lit, saturation=0.66, brightness=0.74, contrast=1.18)
        outputs.append(
            lit.filter(ImageFilter.UnsharpMask(radius=0.8, percent=90, threshold=2)).convert(
                "RGBA"
            )
        )
    return stack(outputs)


def make_review(category: str, entries: list[tuple[str, Image.Image]]) -> None:
    REVIEW.mkdir(parents=True, exist_ok=True)
    columns = 5
    cell = 180
    rows_per_sheet = 5
    batch_size = columns * rows_per_sheet
    font = ImageFont.load_default(size=13)
    for sheet_index, start in enumerate(range(0, len(entries), batch_size), 1):
        batch = entries[start : start + batch_size]
        sheet = Image.new("RGB", (columns * cell, rows_per_sheet * 205), (17, 19, 18))
        draw = ImageDraw.Draw(sheet)
        for index, (name, icon) in enumerate(batch):
            x = (index % columns) * cell + 10
            y = (index // columns) * 205 + 8
            frame = icon.crop((0, 0, icon.width, icon.width)).convert("RGBA")
            preview = frame.resize((160, 160), Image.Resampling.NEAREST)
            backdrop = Image.new("RGB", (160, 160), (35, 38, 36))
            backdrop.paste(preview, (0, 0), preview)
            sheet.paste(backdrop, (x, y))
            draw.text((x, y + 166), name[:25], fill=(226, 224, 210), font=font)
        sheet.save(REVIEW / f"{category}_{sheet_index:02d}.png", optimize=True)


def main() -> None:
    scope = list(csv.DictReader(SCOPE.open(encoding="utf-8")))
    host_analysis = {
        row["RegistryId"]: row
        for row in csv.DictReader(HOST_ANALYSIS.open(encoding="utf-8"))
    }
    by_texture = {}
    for row in scope:
        for texture in filter(None, row["Textures"].split(";")):
            by_texture[texture] = row

    with ZipFile(MOD) as mod, ZipFile(MINECRAFT) as minecraft:
        vanilla_hosts = {
            family: frames(Image.open(io.BytesIO(minecraft.read(path))))
            for family, path in VANILLA_HOSTS.items()
        }
        last_days_hosts = {
            family: frames(Image.open(PACK_ASSETS / "minecraft" / "textures" / "block" / name))
            for family, name in HOST_TEXTURES.items()
        }

        ledger_rows = []
        reviews: dict[str, list[tuple[str, Image.Image]]] = defaultdict(list)
        manifest_outputs = []

        for texture_id, row in sorted(by_texture.items()):
            namespace, texture = texture_id.split(":", 1)
            jar_path = f"assets/{namespace}/textures/{texture}.png"
            source_bytes = mod.read(jar_path)
            source_path = UPSTREAM / "textures" / f"{texture}.png"
            source_path.parent.mkdir(parents=True, exist_ok=True)
            source_path.write_bytes(source_bytes)

            metadata_path = jar_path + ".mcmeta"
            if metadata_path in mod.namelist():
                source_meta = source_path.with_suffix(source_path.suffix + ".mcmeta")
                source_meta.write_bytes(mod.read(metadata_path))

            source_image = Image.open(io.BytesIO(source_bytes))
            source_frames = frames(source_image)
            identity = row["RegistryId"]
            gem_variant = AUTHORED_ORE_FACES / f"{texture}_master.png"
            metal_variant = METAL_ORE_FACES / f"{texture}_master.png"
            authored_variant = gem_variant if gem_variant.exists() else metal_variant
            art_source_path = source_path
            art_source_image = source_image
            runtime_metadata: bytes | None = None
            if row["Category"] == "ore_block" and authored_variant.exists():
                art_source_image = Image.open(authored_variant)
                authored_frames = frames(art_source_image)
                runtime_metadata = b""
                derived = stack(
                    [
                        frame.resize((ORE_SIZE, ORE_SIZE), Image.Resampling.LANCZOS)
                        for frame in authored_frames
                    ]
                )
                art_source_path = authored_variant
                authored_meta = authored_variant.with_suffix(authored_variant.suffix + ".mcmeta")
                if authored_meta.exists():
                    runtime_metadata = authored_meta.read_bytes()
                method = (
                    "approved generic gem containment machinery; contained gem recolor only; 32px runtime"
                    if gem_variant.exists()
                    else "approved generic metallic ore container; sample insert and hazard-paint recolor only; 32px runtime"
                )
            elif (
                row["Category"] == "ore_block"
            ):
                raise RuntimeError(
                    f"Missing approved generic machinery face for {identity}"
                )
            elif row["Category"] == "ore_block":
                family = host_analysis[identity]["SelectedHost"]
                derived = derive_ore(
                    identity, source_frames, family, vanilla_hosts, last_days_hosts
                )
                method = f"authored mineral relief and palette-only recolor; coarse deposit silhouette; Last Days {family} host; no upstream RGB overlay"
            elif row["Category"] == "gem_item":
                derived = derive_gem(identity, source_frames)
                method = f"authored {family_for(identity)} family silhouette/lighting; non-spatial palette swatches and animation only; no upstream RGB overlay"
            else:
                derived = derive_storage(identity, source_frames)
                method = f"authored compressed-crystal and {family_for(identity) or 'neutral crystal'} relief; non-spatial palette swatches only; no upstream RGB overlay"

            output_path = TARGET / f"{texture}.png"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            derived.save(output_path, optimize=True)
            output_meta = output_path.with_suffix(output_path.suffix + ".mcmeta")
            if runtime_metadata:
                output_meta.write_bytes(runtime_metadata)
            elif runtime_metadata == b"":
                if output_meta.exists():
                    output_meta.unlink()
            elif metadata_path in mod.namelist():
                output_meta.write_bytes(mod.read(metadata_path))
            elif output_meta.exists():
                output_meta.unlink()

            ledger_rows.append(
                {
                    "Category": row["Category"],
                    "RegistryId": identity,
                    "Texture": texture_id,
                    "SourceArt": art_source_path.relative_to(ROOT).as_posix(),
                    "DerivedOutput": output_path.relative_to(ROOT).as_posix(),
                    "SourceSize": f"{art_source_image.width}x{art_source_image.height}",
                    "OutputSize": f"{derived.width}x{derived.height}",
                    "Frames": str(derived.height // derived.width),
                    "Method": method,
                }
            )
            reviews[row["Category"]].append((identity.split(":", 1)[1], derived))
            manifest_outputs.append(
                {
                    "texture": texture_id,
                    "source_sha256": sha256(art_source_path),
                    "output_sha256": sha256(output_path),
                    "frames": derived.height // derived.width,
                    "method": method,
                }
            )

    with LEDGER.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=ledger_rows[0].keys())
        writer.writeheader()
        writer.writerows(ledger_rows)

    for category, entries in reviews.items():
        make_review(category, entries)

    generated_sources = []
    for path in sorted(GENERATED.glob("*.png")):
        with Image.open(path) as image:
            size = list(image.size)
        generated_sources.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "sha256": sha256(path),
                "size": size,
                "role": "authoritative generated material source",
            }
        )
    for path in sorted(GENERATED_FAMILIES.glob("*.png")):
        with Image.open(path) as image:
            size = list(image.size)
        generated_sources.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "sha256": sha256(path),
                "size": size,
                "role": "authoritative generated mineral-family source",
            }
        )
    for path in sorted(AUTHORED_ORE_FACES.rglob("*_master.png")):
        with Image.open(path) as image:
            size = list(image.size)
        generated_sources.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "sha256": sha256(path),
                "size": size,
                "role": "authoritative generic-containment recolored gem source",
            }
        )
    for path in sorted(METAL_ORE_FACES.rglob("*_master.png")):
        with Image.open(path) as image:
            size = list(image.size)
        generated_sources.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "sha256": sha256(path),
                "size": size,
                "role": "authoritative generic-metal-container recolored ore source",
            }
        )

    manifest = {
        "mod": MOD.relative_to(ROOT).as_posix(),
        "scope": {
            "ore_blocks": sum(row["Category"] == "ore_block" for row in scope),
            "gem_items": sum(row["Category"] == "gem_item" for row in scope),
            "gem_storage_blocks": sum(
                row["Category"] == "gem_storage_block" for row in scope
            ),
            "live_textures": len(manifest_outputs),
        },
        "authority": "approved generic gem-containment and metallic-container machinery masters; upstream mod art supplies non-spatial identity palettes only; resource-pack PNGs are derived outputs",
        "runtime_resolution": {
            "all_ore_blocks": ORE_SIZE,
            "other_textures": SIZE,
        },
        "model_contract": "all live models retain their upstream cube/cube_all/item-generated texture paths; no model or blockstate overrides",
        "animation_contract": "all generic ore machinery is static; animated item/storage textures retain upstream frame order and mcmeta",
        "generated_sources": generated_sources,
        "outputs": manifest_outputs,
        "installer": "scripts/install_more_ores_more_gems_derived_textures.py",
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"installed={len(manifest_outputs)}")
    print(f"ledger={LEDGER}")
    print(f"manifest={MANIFEST}")
    print(f"review_sheets={sum((len(entries) + 24) // 25 for entries in reviews.values())}")


if __name__ == "__main__":
    main()
