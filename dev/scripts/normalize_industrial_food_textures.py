"""Normalize registered industrial-food item textures to the pack's 128 px standard."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "kubejs/config/industrial_food.json"
TEXTURES = ROOT / "kubejs/assets/kubejs/textures/item"


def registered_item_ids(data: dict) -> list[str]:
    ids = [item["id"] for item in data["items"]]
    for flavor in data["flavors"]:
        flavor_id = flavor["id"]
        ids.extend(
            [
                f"{flavor_id}_fruit_pulp",
                f"{flavor_id}_juice_concentrate",
                f"bottled_{flavor_id}_juice",
                f"{flavor_id}_soda_can",
                f"{flavor_id}_soda_six_pack",
                f"{flavor_id}_soda_case",
            ]
        )
    return ids


def main() -> None:
    data = json.loads(CONFIG.read_text(encoding="utf-8"))
    resized: list[str] = []
    for item_id in registered_item_ids(data):
        path = TEXTURES / f"{item_id}.png"
        if not path.exists():
            continue
        with Image.open(path) as source:
            if source.size != (32, 32):
                continue
            normalized = source.convert("RGBA").resize((128, 128), Image.Resampling.NEAREST)
            normalized.save(path)
            resized.append(item_id)
    print(f"Resized {len(resized)} industrial-food textures to 128 x 128.")


if __name__ == "__main__":
    main()
