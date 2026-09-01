#!/usr/bin/env python3
"""Generate the Hive World's horizontal-mask and vertical-band biome routing.

The custom stack field is converted into three discrete climate values: wastes
(-1), apron (-0.2), and core (+0.5). The dimension's multi-noise source combines
that horizontal value with the height-derived depth field to select two exterior
biomes or one of six core bands. Legacy sump/works/vault biomes remain registered
elsewhere for old saves but are intentionally absent here.

Use --check to reject routing drift without writing files.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
DATA = REPO / "kubejs/data/infinite_domain"
DF_DIR = DATA / "worldgen/density_function/hive_world"
DIMENSION = DATA / "dimension/hive_world.json"

BANDS = (
    ("drown", (0.811, 1.0)),
    ("underworks", (0.525, 0.811)),
    ("furnace", (0.191, 0.525)),
    ("billet", (-0.238, 0.191)),
    ("vaulting", (-0.620, -0.238)),
    ("crown", (-1.0, -0.620)),
)


def mask(input_id: str, minimum: float) -> dict:
    return {
        "type": "minecraft:range_choice",
        "input": input_id,
        "min_inclusive": minimum,
        "max_exclusive": 2.0,
        "when_in_range": 1.0,
        "when_out_of_range": -1.0,
    }


def climate_entry(biome: str, continentalness: tuple[float, float], depth: tuple[float, float]) -> dict:
    return {
        "biome": biome,
        "parameters": {
            "temperature": 0.0,
            "humidity": 0.0,
            "continentalness": list(continentalness),
            "erosion": 0.0,
            "weirdness": 0.0,
            "depth": list(depth),
            "offset": 0.0,
        },
    }


def outputs() -> dict[Path, dict]:
    stack_field = {
        "type": "infinite_domain_hive_world:stack_field",
        "cell_size": 3072,
        "radius": 520.0,
        "jitter": 0.15,
        "vertical_taper": 0.45,
        "salt": 927133,
    }
    core_mask = mask("infinite_domain:hive_world/stack_field", 0.0)
    apron_mask = mask("infinite_domain:hive_world/stack_field", -0.35)
    biome_region = {
        "type": "minecraft:range_choice",
        "input": "infinite_domain:hive_world/core_mask",
        "min_inclusive": 0.0,
        "max_exclusive": 2.0,
        "when_in_range": 0.5,
        "when_out_of_range": {
            "type": "minecraft:range_choice",
            "input": "infinite_domain:hive_world/apron_mask",
            "min_inclusive": 0.0,
            "max_exclusive": 2.0,
            "when_in_range": -0.2,
            "when_out_of_range": -1.0,
        },
    }
    biomes = [
        climate_entry("infinite_domain:hive_world_wastes", (-1.0, -0.6), (-1.0, 1.0)),
        climate_entry("infinite_domain:hive_world_apron", (-0.6, 0.2), (-1.0, 1.0)),
        *[
            climate_entry(f"infinite_domain:hive_world_{slug}", (0.2, 1.0), depth)
            for slug, depth in BANDS
        ],
    ]
    dimension = {
        "type": "infinite_domain:hive_world",
        "generator": {
            "type": "minecraft:noise",
            "settings": "infinite_domain:hive_world",
            "biome_source": {
                "type": "minecraft:multi_noise",
                "biomes": biomes,
            },
        },
    }
    return {
        DF_DIR / "stack_field.json": stack_field,
        DF_DIR / "core_mask.json": core_mask,
        DF_DIR / "apron_mask.json": apron_mask,
        DF_DIR / "biome_region.json": biome_region,
        DIMENSION: dimension,
    }


def render(payload: dict) -> str:
    return json.dumps(payload, indent=2) + "\n"


def main() -> int:
    check = "--check" in sys.argv
    drift: list[Path] = []
    for path, payload in outputs().items():
        expected = render(payload)
        if check:
            actual = path.read_text(encoding="utf-8") if path.is_file() else None
            if actual != expected:
                drift.append(path)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(expected, encoding="utf-8")
            print(f"wrote {path.relative_to(REPO)}")
    if drift:
        print("FAIL - Hive biome-routing generator drift:")
        for path in drift:
            print(f"  {path.relative_to(REPO)}")
        return 1
    if check:
        print("PASS - Hive horizontal-mask and eight-biome routing files are exact")
    return 0


if __name__ == "__main__":
    sys.exit(main())
