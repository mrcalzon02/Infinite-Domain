"""Install one approved generated icon as a compact Minecraft item texture."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]


def install(source: Path, item_id: str, size: int = 128) -> Path:
    """Crop transparent padding, fit safely, and install one approved source."""
    with Image.open(source) as loaded:
        image = loaded.convert("RGBA")
    alpha = image.getchannel("A")
    bounds = alpha.getbbox()
    if not bounds:
        raise ValueError(f"Generated source contains no visible pixels: {source}")
    image = image.crop(bounds)
    margin = max(4, size // 16)
    available = size - margin * 2
    scale = min(available / image.width, available / image.height)
    resized = image.resize((max(1, round(image.width * scale)), max(1, round(image.height * scale))), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    canvas.alpha_composite(resized, ((size - resized.width) // 2, (size - resized.height) // 2))
    output = ROOT / f"kubejs/assets/kubejs/textures/item/{item_id}.png"
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output, optimize=True)
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("item_id")
    parser.add_argument("--size", type=int, default=128)
    args = parser.parse_args()

    output = install(args.source, args.item_id, args.size)
    print(f"Installed {args.item_id} at {args.size}x{args.size}: {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
