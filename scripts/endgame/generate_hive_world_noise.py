#!/usr/bin/env python3
"""Authoritative generator for the Hive World spike noise settings.

Endgame checkpoint EG-P01-S01-C0014 (baseline generator).
Authority: docs/Endgame.md, docs/endgame/contracts/height-contract.md,
docs/endgame/contracts/namespace-layout.md.

Emits (do not hand-edit the output):
  kubejs/data/infinite_domain/worldgen/noise_settings/hive_world.json

This is a DISPOSABLE PHASE 1 SPIKE generator. It produces the simplest terrain
that satisfies the Phase 1 evidence bar:
  * respects the -64..319 height contract exactly (min_y -64, height 384);
  * a solid deepslate crust from bedrock up to ~Y0 (the Drown is mined into it);
  * a hollow middle (Y1..305) that later structure work fills;
  * a sealed bedrock-capped roof at Y306..319;
  * no aquifers, no ore veins, no fluid, deterministic, no jaggedness.

The real multi-field density graph (crust / core mask / apron / strata / voids)
is Phase 3 work starting at EG-P03-S01-C0037 and will replace this file.
"""
from __future__ import annotations

import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
OUT = REPO / "kubejs/data/infinite_domain/worldgen/noise_settings/hive_world.json"

# --- height contract (EG-P00-S03-C0006) -------------------------------------
MIN_Y = -64
HEIGHT = 384          # top block Y = MIN_Y + HEIGHT - 1 = 319
SEA_LEVEL = -63       # no sea in the spike; acid is added as a feature at C0017


def y_gradient(from_y: int, from_value: float, to_y: int, to_value: float) -> dict:
    return {
        "type": "minecraft:y_clamped_gradient",
        "from_y": from_y,
        "to_y": to_y,
        "from_value": from_value,
        "to_value": to_value,
    }


def build() -> dict:
    # Solid where density > 0. Crust: positive below ~Y0. Roof: positive above ~Y306.
    crust = y_gradient(MIN_Y, 2.0, 64, -2.0)          # zero-crossing at Y0
    roof = y_gradient(296, -2.0, 316, 2.0)            # zero-crossing at ~Y306
    final_density = {"type": "minecraft:max", "argument1": crust, "argument2": roof}

    router = {
        "barrier": 0,
        "continents": 0,
        "depth": 0,
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
        "initial_density_without_jaggedness": final_density,
        "final_density": final_density,
    }

    surface_rule = {
        "type": "minecraft:sequence",
        "sequence": [
            # bedrock floor, 0..4 above the world bottom
            {
                "type": "minecraft:condition",
                "if_true": {
                    "type": "minecraft:vertical_gradient",
                    "random_name": "infinite_domain:hive_world_bedrock_floor",
                    "true_at_and_below": {"above_bottom": 0},
                    "false_at_and_above": {"above_bottom": 5},
                },
                "then_run": {"type": "minecraft:block", "result_state": {"Name": "minecraft:bedrock"}},
            },
            # bedrock roof, 0..4 below the world top (the sealed cap)
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
                "then_run": {"type": "minecraft:block", "result_state": {"Name": "minecraft:bedrock"}},
            },
            # a thin dark "slag skin" on the exposed top of the crust
            {
                "type": "minecraft:condition",
                "if_true": {"type": "minecraft:stone_depth", "offset": 0, "surface_type": "floor",
                            "add_surface_depth": False, "secondary_depth_range": 0},
                "then_run": {"type": "minecraft:block", "result_state": {"Name": "minecraft:blackstone"}},
            },
            # everything else is the default block
            {"type": "minecraft:block", "result_state": {"Name": "minecraft:deepslate"}},
        ],
    }

    return {
        "aquifers_enabled": False,
        "ore_veins_enabled": False,
        "legacy_random_source": False,
        "disable_mob_generation": False,
        "default_block": {"Name": "minecraft:deepslate"},
        # codec-safe fluid; sea level sits at the world floor so no fluid body
        # actually appears in the spike (the crust is solid there).
        "default_fluid": {"Name": "minecraft:water", "Properties": {"level": "0"}},
        "sea_level": SEA_LEVEL,
        "noise": {"min_y": MIN_Y, "height": HEIGHT, "size_horizontal": 1, "size_vertical": 2},
        "noise_router": router,
        "spawn_target": [],
        "surface_rule": surface_rule,
    }


def main() -> int:
    data = build()
    # contract asserts
    assert data["noise"]["min_y"] == -64 and data["noise"]["height"] == 384, "height contract violation"
    assert (data["noise"]["min_y"] + data["noise"]["height"]) % 16 == 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
