#!/usr/bin/env python3
"""Authoritative generator for the Hive World biomes.

Endgame checkpoint EG-P01-S02-C0015 (spike biomes), extended by owner direction
to three band-group biomes so the strata read distinctly (fog / light / sound).
Authority: docs/Endgame.md §3, docs/endgame/contracts/spatial-metrics.md.

Emits (do not hand-edit):
  kubejs/data/infinite_domain/worldgen/biome/hive_world_sump.json    (The Drown + The Underworks)
  kubejs/data/infinite_domain/worldgen/biome/hive_world_works.json   (The Furnace Tiers + The Billet Decks)
  kubejs/data/infinite_domain/worldgen/biome/hive_world_vault.json   (The Vaulting + The Crown)

Routing (C0016) is by the noise-router depth gradient; the multi_noise split is in
dimension/hive_world.json. No mob spawners yet - the enemy roster is EG-P06-S04-C0089.
"""
from __future__ import annotations

import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
BIOME_DIR = REPO / "kubejs/data/infinite_domain/worldgen/biome"

STEP_COUNT = 11               # GenerationStep.Decoration indices in 1.21.1
STEP_UNDERGROUND_DECORATION = 7
STEP_FLUID_SPRINGS = 8


def empty_features():
    return [[] for _ in range(STEP_COUNT)]


def biome(temperature, fog, sky, water, water_fog, particle=None, ambient_sound=None,
          additions_sound=None, music=None, features=None):
    effects = {
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
    }
    if particle is not None:
        effects["particle"] = particle
    if ambient_sound is not None:
        effects["ambient_sound"] = ambient_sound
    if additions_sound is not None:
        effects["additions_sound"] = additions_sound
    if music is not None:
        effects["music"] = {
            "sound": music, "min_delay": 12000, "max_delay": 24000,
            "replace_current_music": True,
        }
    return {
        "temperature": temperature,
        "downfall": 0.0,
        "has_precipitation": False,
        "carvers": {"air": []},
        "spawners": {k: [] for k in (
            "monster", "creature", "ambient", "axolotls",
            "underground_water_creature", "water_creature", "water_ambient", "misc",
        )},
        "spawn_costs": {},
        "features": features if features is not None else empty_features(),
        "effects": effects,
    }


def build():
    # --- The Drown + The Underworks: flooded, acidic, low light -------------
    sump_feat = empty_features()
    sump_feat[STEP_FLUID_SPRINGS] = ["infinite_domain:hive_world_acid_pool"]
    sump_feat[STEP_UNDERGROUND_DECORATION] = ["infinite_domain:hive_world_fixture_light"]
    sump = biome(
        temperature=0.7, fog=0x14140F, sky=0x0B0B0A, water=0x53621F, water_fog=0x1B2208,
        particle={"probability": 0.0022, "options": {"type": "minecraft:white_ash"}},
        ambient_sound="minecraft:ambient.basalt_deltas.loop",
        additions_sound={"sound": "minecraft:ambient.basalt_deltas.additions", "tick_chance": 0.0111},
        music="minecraft:music.overworld.dripstone_caves",
        features=sump_feat,
    )

    # --- The Furnace Tiers + The Billet Decks: hot industrial haze ---------
    works_feat = empty_features()
    works_feat[STEP_UNDERGROUND_DECORATION] = [
        "infinite_domain:hive_world_fixture_light",
        "infinite_domain:hive_world_salvage",
    ]
    works = biome(
        temperature=1.0, fog=0x23201B, sky=0x171410, water=0x3B4A4F, water_fog=0x10171B,
        particle={"probability": 0.0032, "options": {"type": "minecraft:white_ash"}},
        ambient_sound="minecraft:ambient.nether_wastes.loop",
        additions_sound={"sound": "minecraft:ambient.nether_wastes.additions", "tick_chance": 0.0111},
        music="minecraft:music.nether.nether_wastes",
        features=works_feat,
    )

    # --- The Vaulting + The Crown: cold, thin, echoing monumental space ---
    vault_feat = empty_features()
    vault_feat[STEP_UNDERGROUND_DECORATION] = ["infinite_domain:hive_world_fixture_light"]
    vault = biome(
        temperature=0.35, fog=0x1B2129, sky=0x0E141B, water=0x33424E, water_fog=0x0E141B,
        particle={"probability": 0.0009, "options": {"type": "minecraft:warped_spore"}},
        ambient_sound="minecraft:ambient.soul_sand_valley.loop",
        additions_sound={"sound": "minecraft:ambient.soul_sand_valley.additions", "tick_chance": 0.0111},
        music="minecraft:music.overworld.deep_dark",
        features=vault_feat,
    )

    return {"hive_world_sump": sump, "hive_world_works": works, "hive_world_vault": vault}


def main() -> int:
    BIOME_DIR.mkdir(parents=True, exist_ok=True)
    for name, data in build().items():
        out = BIOME_DIR / f"{name}.json"
        out.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {out.relative_to(REPO)}")
    # remove the superseded two-biome spike files if present
    for old in ("hive_world_dead_waste", "hive_world_stack_test"):
        p = BIOME_DIR / f"{old}.json"
        if p.is_file():
            p.unlink()
            print(f"removed superseded {p.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
