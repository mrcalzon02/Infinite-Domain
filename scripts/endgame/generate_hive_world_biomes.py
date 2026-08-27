#!/usr/bin/env python3
"""Authoritative generator for the Hive World spike biomes.

Endgame checkpoint EG-P01-S02-C0015 (spike biomes). Also owns the acid feature
reference wiring for EG-P01-S03-C0017.
Authority: docs/Endgame.md, docs/endgame/contracts/namespace-layout.md.

Emits (do not hand-edit):
  kubejs/data/infinite_domain/worldgen/biome/hive_world_dead_waste.json
  kubejs/data/infinite_domain/worldgen/biome/hive_world_stack_test.json

DISPOSABLE PHASE 1 SPIKE. Two biomes only: one exterior wasteland, one interior
stack test volume. No mob spawners (enemy roster is EG-P06-S04-C0089), no
decoration features except the bounded acid pool (C0017) in the wasteland.
The real 3D biome family is EG-P03-S05-C0046.
"""
from __future__ import annotations

import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
BIOME_DIR = REPO / "kubejs/data/infinite_domain/worldgen/biome"

# GenerationStep.Decoration has 11 indices in 1.21.1
STEP_COUNT = 11
STEP_FLUID_SPRINGS = 8  # index of FLUID_SPRINGS - where lake-like features sit


def empty_features() -> list[list[str]]:
    return [[] for _ in range(STEP_COUNT)]


def base(temperature: float, fog: int, sky: int, water: int, water_fog: int) -> dict:
    return {
        "temperature": temperature,
        "downfall": 0.0,
        "has_precipitation": False,
        "carvers": {"air": []},
        "spawners": {
            "monster": [], "creature": [], "ambient": [], "axolotls": [],
            "underground_water_creature": [], "water_creature": [],
            "water_ambient": [], "misc": [],
        },
        "spawn_costs": {},
        "features": empty_features(),
        "effects": {
            "sky_color": sky,
            "fog_color": fog,
            "water_color": water,
            "water_fog_color": water_fog,
            "mood_sound": {
                "sound": "minecraft:ambient.cave",
                "tick_delay": 6000,
                "block_search_extent": 8,
                "offset": 2.0,
            },
        },
    }


def build() -> dict[str, dict]:
    # The spike routes these by depth (C0016): stack_test occupies the buried low
    # bands (roughly Y < 48), dead_waste the open shaft and upper void (Y >= 48).

    # low buried interior - carries the bounded acid pool (C0017, "The Drown")
    stack_test = base(temperature=0.7, fog=0x201F26, sky=0x101019, water=0x4A5A2A, water_fog=0x1D2413)
    stack_test["features"][STEP_FLUID_SPRINGS] = ["infinite_domain:hive_world_acid_pool"]

    # open vertical void and upper region - hotter, sulfurous fog, no features in the spike
    dead_waste = base(temperature=0.9, fog=0x3A3228, sky=0x2B2A26, water=0x3D5460, water_fog=0x101B23)

    return {
        "hive_world_dead_waste": dead_waste,
        "hive_world_stack_test": stack_test,
    }


def main() -> int:
    BIOME_DIR.mkdir(parents=True, exist_ok=True)
    for name, data in build().items():
        out = BIOME_DIR / f"{name}.json"
        out.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {out.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
