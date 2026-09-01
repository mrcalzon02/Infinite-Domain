#!/usr/bin/env python3
"""Authoritative generator for the Hive World spike acid feature.

Endgame checkpoint EG-P01-S03-C0017 (acid feature).
Authority: docs/Endgame.md, docs/endgame/contracts/hazard-contract.md.

Emits (do not hand-edit):
  kubejs/data/infinite_domain/worldgen/configured_feature/hive_world_acid_pool.json
  kubejs/data/infinite_domain/worldgen/placed_feature/hive_world_acid_pool.json

DISPOSABLE PHASE 1 SPIKE. One bounded acid pool using the verified block
`the_wasteland_reworked:acid` (a static, non-flowing AcidBlock - blockstate has no
properties, so there are zero ongoing fluid updates once placed). Wired into
hive_world_stack_test by generate_hive_world_biomes.py. The full acid hydrology is
Phase 3 (EG-P03-S04-C0044) and Phase 5 (EG-P05-S03-C0074).
"""
from __future__ import annotations

import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[3]
CF = REPO / "kubejs/data/infinite_domain/worldgen/configured_feature/hive_world_acid_pool.json"
PF = REPO / "kubejs/data/infinite_domain/worldgen/placed_feature/hive_world_acid_pool.json"

CONFIGURED = {
    "type": "minecraft:lake",
    "config": {
        "fluid": {
            "type": "minecraft:simple_state_provider",
            "state": {"Name": "the_wasteland_reworked:acid"},
        },
        "barrier": {
            "type": "minecraft:simple_state_provider",
            "state": {"Name": "minecraft:deepslate"},
        },
    },
}

PLACED = {
    "feature": "infinite_domain:hive_world_acid_pool",
    "placement": [
        {"type": "minecraft:rarity_filter", "chance": 3},
        {"type": "minecraft:in_square"},
        # Target the thin planetary waste/crust layer around the Y0 acid-sea datum.
        {"type": "minecraft:height_range", "height": {
            "type": "minecraft:uniform",
            "min_inclusive": {"absolute": -56},
            "max_inclusive": {"absolute": 4},
        }},
        {"type": "minecraft:biome"},
    ],
}


def main() -> int:
    for path, data in ((CF, CONFIGURED), (PF, PLACED)):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {path.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
