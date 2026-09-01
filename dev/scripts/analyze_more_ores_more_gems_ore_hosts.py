from __future__ import annotations

import csv
import io
import json
from collections import Counter
from pathlib import Path
from zipfile import ZipFile

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "mods" / "momg-1.1.9-release-neoforge-1.21.1.jar"
MINECRAFT = Path(
    r"C:\Users\Admin\curseforge\minecraft\Install\versions\1.21.1\1.21.1.jar"
)
SCOPE = ROOT / "docs" / "more-ores-more-gems-texture-scope.csv"
OUTPUT = ROOT / "docs" / "more-ores-more-gems-ore-host-analysis.csv"
HOSTS = {
    "stone": "assets/minecraft/textures/block/stone.png",
    "deepslate": "assets/minecraft/textures/block/deepslate.png",
    "nether": "assets/minecraft/textures/block/netherrack.png",
    "end_stone": "assets/minecraft/textures/block/end_stone.png",
    "clay": "assets/minecraft/textures/block/clay.png",
    "magma": "assets/minecraft/textures/block/magma.png",
}


def first_frame(data: bytes) -> Image.Image:
    image = Image.open(io.BytesIO(data)).convert("RGB")
    return image.crop((0, 0, image.width, image.width))


def main() -> None:
    scope = [
        row
        for row in csv.DictReader(SCOPE.open(encoding="utf-8"))
        if row["Category"] == "ore_block"
    ]
    with ZipFile(MOD) as mod, ZipFile(MINECRAFT) as minecraft:
        hosts = {
            family: first_frame(minecraft.read(path)) for family, path in HOSTS.items()
        }
        rows = []
        for entry in scope:
            texture_id = entry["Textures"].split(";", 1)[0]
            namespace, texture = texture_id.split(":", 1)
            path = f"assets/{namespace}/textures/{texture}.png"
            ore = first_frame(mod.read(path))
            scores = {}
            for family, host in hosts.items():
                candidate = host.resize(ore.size, Image.Resampling.NEAREST)
                exact = sum(a == b for a, b in zip(ore.getdata(), candidate.getdata()))
                scores[family] = exact / (ore.width * ore.height)
            best = max(scores, key=scores.get)
            expected = entry["HostFamily"]
            selected = expected if scores[expected] >= 0.20 else best
            rows.append(
                {
                    "RegistryId": entry["RegistryId"],
                    "Texture": texture_id,
                    "ExpectedHost": expected,
                    "BestPixelMatchHost": best,
                    "SelectedHost": selected,
                    "ExactHostCoverage": f"{scores[selected]:.4f}",
                    "MineralMaskCoverage": f"{1.0 - scores[selected]:.4f}",
                    "NeedsManualMaskReview": "yes" if scores[selected] < 0.20 else "no",
                }
            )

    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print("ores", len(rows))
    print("selected_hosts", dict(Counter(row["SelectedHost"] for row in rows)))
    print("manual_review", sum(row["NeedsManualMaskReview"] == "yes" for row in rows))
    print("output", OUTPUT)


if __name__ == "__main__":
    main()
