"""Create full-resolution era/tier variants from approved family masters."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

from install_generated_item_texture import install


ROOT = Path(__file__).resolve().parents[1]
MASTERS = ROOT / "docs/texture-audit/family-masters"
SOURCES = ROOT / "docs/texture-audit/generated-sources"

# PIL HSV hue values. Materials stay fixed; only magenta identification fields move.
ERA_HUES = {0: 24, 1: 18, 2: 5, 3: 39, 4: 33, 5: 134, 6: 76, 7: 156, 8: 196}
INJECTOR_HUES = {1: 18, 2: 5, 3: 39, 4: 76, 5: 134, 6: 156, 7: 184, 8: 218}


def recolor(source: Path, target_hue: int) -> Image.Image:
    with Image.open(source) as loaded:
        rgba = loaded.convert("RGBA")
    alpha = np.array(rgba.getchannel("A"), dtype=np.uint8)
    hsv = np.array(rgba.convert("RGB").convert("HSV"), dtype=np.uint8)
    hue = hsv[:, :, 0].astype(np.int16)
    saturation = hsv[:, :, 1]
    value = hsv[:, :, 2]
    # The masters deliberately reserve the violet/magenta band for tier identity.
    mask = (alpha > 0) & (saturation > 78) & (hue >= 184) & (hue <= 244) & (value > 28)
    variation = ((hue - 214) * 0.22).astype(np.int16)
    hue[mask] = np.clip(target_hue + variation[mask], 0, 255)
    hsv[:, :, 0] = hue.astype(np.uint8)
    rgb = Image.fromarray(hsv, "HSV").convert("RGB")
    rgb.putalpha(Image.fromarray(alpha, "L"))
    return rgb


def save_family(master_name: str, variants: dict[str, int]) -> int:
    master = MASTERS / master_name
    if not master.exists():
        raise FileNotFoundError(master)
    count = 0
    for item_id, hue in variants.items():
        full_source = SOURCES / f"{item_id}.png"
        recolor(master, hue).save(full_source, optimize=True)
        install(full_source, item_id)
        count += 1
    return count


def main() -> None:
    SOURCES.mkdir(parents=True, exist_ok=True)
    total = 0
    total += save_family("priority_cache_master.png", {f"era{era}_priority_cache": hue for era, hue in ERA_HUES.items()})
    total += save_family("supply_bag_master.png", {f"era{era}_supply_bag": ERA_HUES[era] for era in range(1, 9)})
    total += save_family("darknet_injector_master.png", {f"darknet_session_injector_tier_{tier}": hue for tier, hue in INJECTOR_HUES.items()})
    total += save_family("mastery_emblem_master.png", {f"era{era}_mastery_emblem": hue for era, hue in ERA_HUES.items()})
    print(f"Archived and installed {total} full-resolution family variants.")


if __name__ == "__main__":
    main()
