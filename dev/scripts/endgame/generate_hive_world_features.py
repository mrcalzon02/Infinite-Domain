#!/usr/bin/env python3
"""Authoritative generator for the Hive World ambient / salvage features.

Endgame: spike-scale ambience and a reason-to-mine, by owner direction. The real
feature set (proper fixtures, hazard décor, salvage economy) is Phase 3/6.
Authority: docs/Endgame.md §2.3 (empty scale is authored), §2.5.

Emits (do not hand-edit):
  worldgen/configured_feature/hive_world_fixture_light.json  + placed_feature
  worldgen/configured_feature/hive_world_salvage.json        + placed_feature

- fixture_light: sparse `minecraft:sea_lantern` still-burning fixtures set into the
  mass, so the tunnel network is navigable but stays dark and oppressive.
- salvage: small veins of raw-iron / copper / coal blocks in the works bands -
  "structural salvage" - so the solid mass is worth cutting into.
"""
from __future__ import annotations

import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[3]
CF_DIR = REPO / "kubejs/data/infinite_domain/worldgen/configured_feature"
PF_DIR = REPO / "kubejs/data/infinite_domain/worldgen/placed_feature"

DEEPSLATE_TEST = {"predicate_type": "minecraft:block_match", "block": "minecraft:deepslate"}


def ore_feature(targets, size, discard_air=0.0):
    return {
        "type": "minecraft:ore",
        "config": {
            "size": size,
            "discard_chance_on_air_exposure": discard_air,
            "targets": [{"target": DEEPSLATE_TEST, "state": {"Name": s}} for s in targets],
        },
    }


def placed(feature_id, count, min_y, max_y, biome_gate=True):
    placement = [
        {"type": "minecraft:count", "count": count},
        {"type": "minecraft:in_square"},
        {"type": "minecraft:height_range", "height": {
            "type": "minecraft:uniform",
            "min_inclusive": {"absolute": min_y},
            "max_inclusive": {"absolute": max_y},
        }},
    ]
    if biome_gate:
        placement.append({"type": "minecraft:biome"})
    return {"feature": feature_id, "placement": placement}


CONFIGURED = {
    "hive_world_fixture_light": ore_feature(["minecraft:sea_lantern"], size=1, discard_air=0.0),
    "hive_world_salvage": ore_feature(
        ["minecraft:raw_iron_block", "minecraft:copper_block", "minecraft:coal_block"],
        size=4, discard_air=0.1,
    ),
}

PLACED = {
    "hive_world_fixture_light": placed("infinite_domain:hive_world_fixture_light", count=11, min_y=-60, max_y=300),
    "hive_world_salvage": placed("infinite_domain:hive_world_salvage", count=6, min_y=40, max_y=200),
}


def main() -> int:
    for d in (CF_DIR, PF_DIR):
        d.mkdir(parents=True, exist_ok=True)
    for name, data in CONFIGURED.items():
        (CF_DIR / f"{name}.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {(CF_DIR / (name + '.json')).relative_to(REPO)}")
    for name, data in PLACED.items():
        (PF_DIR / f"{name}.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {(PF_DIR / (name + '.json')).relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
