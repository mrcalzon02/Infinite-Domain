from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
MODEL = (
    ROOT
    / "ROOT_tools"
    / "createnuclear_model_audit"
    / "assets"
    / "createnuclear"
    / "models"
    / "block"
    / "reactor"
    / "core"
    / "block.json"
)
CURRENT = (
    ROOT
    / "resourcepacks"
    / "LAST_DAYS_INFINITE_DOMAIN_1_21_1"
    / "assets"
    / "createnuclear"
    / "textures"
    / "block"
    / "reactor"
    / "core"
)
PREVIOUS = ROOT / "ROOT_tools" / "createnuclear_model_audit" / "previous_pack"
OUTPUT = ROOT / "ROOT_tools" / "createnuclear_reactor_core_model_comparison.png"
SCALE = 32
FACE_SIZE = 16 * SCALE


def load_texture(path: Path) -> Image.Image:
    image = Image.open(path).convert("RGB")
    if image.height > image.width:
        image = image.crop((0, 0, image.width, image.width))
    return image


def uv_patch(texture: Image.Image, uv: list[float], rotation: int) -> Image.Image:
    factor = texture.width / 16
    u1, v1, u2, v2 = uv
    box = (
        round(min(u1, u2) * factor),
        round(min(v1, v2) * factor),
        round(max(u1, u2) * factor),
        round(max(v1, v2) * factor),
    )
    patch = texture.crop(box)
    if u1 > u2:
        patch = patch.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    if v1 > v2:
        patch = patch.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    if rotation:
        patch = patch.rotate(-rotation, expand=True)
    return patch


def render(texture_dir: Path) -> Image.Image:
    model = json.loads(MODEL.read_text(encoding="utf-8"))
    texture_names = {
        "#1": "reactor_core_casing.png",
        "#2": "reactor_core_center.png",
        "#3": "reactor_core_bars.png",
    }
    textures = {
        key: load_texture(texture_dir / name) for key, name in texture_names.items()
    }
    canvas = Image.new("RGB", (FACE_SIZE, FACE_SIZE), (17, 19, 18))

    visible = [
        element
        for element in model["elements"]
        if "north" in element.get("faces", {})
    ]
    # North is negative Z: large Z is behind, small Z is in front.
    visible.sort(key=lambda element: element["from"][2], reverse=True)

    for element in visible:
        face = element["faces"]["north"]
        x1, y1, _ = element["from"]
        x2, y2, _ = element["to"]
        width = max(1, round((x2 - x1) * SCALE))
        height = max(1, round((y2 - y1) * SCALE))
        patch = uv_patch(
            textures[face["texture"]], face["uv"], face.get("rotation", 0)
        ).resize((width, height), Image.Resampling.NEAREST)
        destination = (round(x1 * SCALE), round((16 - y2) * SCALE))
        canvas.paste(patch, destination)
    return canvas


def main() -> None:
    old = render(PREVIOUS)
    new = render(CURRENT)
    comparison = Image.new("RGB", (FACE_SIZE * 2 + 48, FACE_SIZE + 64), (11, 13, 12))
    draw = ImageDraw.Draw(comparison)
    font = ImageFont.load_default(size=20)
    draw.text((16, 14), "BEFORE: texture duplicates the cage", fill=(220, 218, 204), font=font)
    draw.text(
        (FACE_SIZE + 32, 14),
        "AFTER: texture supports the model",
        fill=(220, 218, 204),
        font=font,
    )
    comparison.paste(old, (16, 48))
    comparison.paste(new, (FACE_SIZE + 32, 48))
    old.save(OUTPUT.with_name("createnuclear_reactor_core_model_before.png"), optimize=True)
    new.save(OUTPUT.with_name("createnuclear_reactor_core_model_after.png"), optimize=True)
    comparison.save(OUTPUT, optimize=True)
    print(OUTPUT)


if __name__ == "__main__":
    main()
