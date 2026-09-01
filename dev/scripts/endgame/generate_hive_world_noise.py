#!/usr/bin/env python3
"""Authoritative generator for the Hive World noise settings.

Endgame checkpoint EG-P01-S01-C0014 (baseline generator), extended by owner
direction with the real density graph (generate_hive_world_density.py) and
band-differentiated surface rules.
Authority: docs/Endgame.md, docs/endgame/contracts/height-contract.md,
docs/endgame/contracts/spatial-metrics.md.

Emits (do not hand-edit):
  kubejs/data/infinite_domain/worldgen/noise_settings/hive_world.json

The terrain mass, tunnel network, shafts, and monumental hall come from
infinite_domain:hive_world/final (see generate_hive_world_density.py). This file
wires that graph into the owner-directed -64..607 candidate height contract and paints
each of the six C0004 bands with its own floor palette.
"""
from __future__ import annotations

import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
OUT = REPO / "kubejs/data/infinite_domain/worldgen/noise_settings/hive_world.json"

MIN_Y = -64
HEIGHT = 672          # top block Y = 607; 608 blocks of build space above Y0
SEA_LEVEL = 0         # planetary waste/acid-sea datum

FINAL_DENSITY = "infinite_domain:hive_world/final"
BIOME_REGION = "infinite_domain:hive_world/biome_region"

# C0004 band ceilings (exclusive upper Y) -> floor-skin block
BAND_SKINS = [
    (0, "minecraft:tuff"),                         # The Drown        (-64..-1)
    (96, "minecraft:cobbled_deepslate"),           # The Underworks   (0..95)
    (208, "minecraft:blackstone"),                 # The Furnace Tiers(96..207)
    (352, "minecraft:polished_blackstone_bricks"), # The Billet Decks (208..351)
    (480, "minecraft:polished_blackstone"),        # The Vaulting     (352..479)
    (None, "minecraft:deepslate_bricks"),          # The Crown        (480..607)
]


def y_gradient(from_y, from_value, to_y, to_value):
    return {
        "type": "minecraft:y_clamped_gradient",
        "from_y": from_y, "to_y": to_y,
        "from_value": from_value, "to_value": to_value,
    }


def block(name):
    return {"type": "minecraft:block", "result_state": {"Name": name}}


def band_skin(name):
    # a few blocks of the band palette on every upward-facing solid surface
    return {
        "type": "minecraft:condition",
        "if_true": {
            "type": "minecraft:stone_depth",
            "offset": 0, "surface_type": "floor",
            "add_surface_depth": True, "secondary_depth_range": 4,
        },
        "then_run": block(name),
    }


def y_below(ceiling):
    # true when Y < ceiling
    return {
        "type": "minecraft:not",
        "invert": {
            "type": "minecraft:y_above",
            "anchor": {"absolute": ceiling},
            "surface_depth_multiplier": 0,
            "add_stone_depth": False,
        },
    }


def surface_rule():
    band_sequence = []
    for ceiling, skin in BAND_SKINS:
        if ceiling is None:
            band_sequence.append(band_skin(skin))
        else:
            band_sequence.append({
                "type": "minecraft:condition",
                "if_true": y_below(ceiling),
                "then_run": band_skin(skin),
            })

    return {
        "type": "minecraft:sequence",
        "sequence": [
            # bedrock floor
            {
                "type": "minecraft:condition",
                "if_true": {
                    "type": "minecraft:vertical_gradient",
                    "random_name": "infinite_domain:hive_world_bedrock_floor",
                    "true_at_and_below": {"above_bottom": 0},
                    "false_at_and_above": {"above_bottom": 5},
                },
                "then_run": block("minecraft:bedrock"),
            },
            # bedrock roof (the sealed cap)
            {
                "type": "minecraft:condition",
                "if_true": {
                    "type": "minecraft:not",
                    "invert": {
                        "type": "minecraft:vertical_gradient",
                        "random_name": "infinite_domain:hive_world_bedrock_roof",
                        "true_at_and_below": {"below_top": 5},
                        "false_at_and_above": {"below_top": 0},
                    },
                },
                "then_run": block("minecraft:bedrock"),
            },
            # band palettes
            {"type": "minecraft:sequence", "sequence": band_sequence},
            # everything else is the default block
            block("minecraft:deepslate"),
        ],
    }


def build() -> dict:
    router = {
        "barrier": 0,
        # Discrete wastes/apron/core climate value for the C0046 biome source.
        "continents": BIOME_REGION,
        # depth increases downward; feeds the multi_noise biome source (C0016 routing)
        "depth": y_gradient(MIN_Y, 1.0, 607, -1.0),
        "erosion": 0,
        "ridges": 0,
        "lava": 0,
        "temperature": 0,
        "vegetation": 0,
        "fluid_level_floodedness": 0,
        "fluid_level_spread": 0,
        "vein_gap": 0,
        "vein_ridged": 0,
        "vein_toggle": 0,
        "initial_density_without_jaggedness": FINAL_DENSITY,
        "final_density": FINAL_DENSITY,
    }

    return {
        "aquifers_enabled": False,
        "ore_veins_enabled": False,
        "legacy_random_source": False,
        "disable_mob_generation": False,
        "default_block": {"Name": "minecraft:deepslate"},
        "default_fluid": {"Name": "the_wasteland_reworked:acid"},
        "sea_level": SEA_LEVEL,
        "noise": {"min_y": MIN_Y, "height": HEIGHT, "size_horizontal": 1, "size_vertical": 2},
        "noise_router": router,
        "spawn_target": [],
        "surface_rule": surface_rule(),
    }


def main() -> int:
    data = build()
    assert data["noise"]["min_y"] == -64 and data["noise"]["height"] == 672, "height contract violation"
    expected = json.dumps(data, indent=2) + "\n"
    if "--check" in sys.argv:
        actual = OUT.read_text(encoding="utf-8") if OUT.is_file() else None
        if actual != expected:
            print(f"FAIL - Hive noise-settings generator drift: {OUT.relative_to(REPO)}")
            return 1
        print("PASS - Hive noise settings match the authoritative generator")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(expected, encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
