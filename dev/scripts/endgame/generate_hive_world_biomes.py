#!/usr/bin/env python3
"""Authoritative generator for every loadable Hive World biome.

The eight active biomes implement the accepted C0046 routing contract: wastes and
apron own the horizontal exterior while Drown, Underworks, Furnace, Billet,
Vaulting, and Crown own exact vertical bands inside the core. The older
sump/works/vault IDs remain loadable aliases for existing worlds, but the active
dimension and structures do not route to them.

Emits (do not hand-edit):
  kubejs/data/infinite_domain/worldgen/biome/hive_world_{wastes,apron}.json
  kubejs/data/infinite_domain/worldgen/biome/hive_world_{drown,underworks,furnace,
      billet,vaulting,crown}.json
  kubejs/data/infinite_domain/worldgen/biome/hive_world_{sump,works,vault}.json

Use --check in repository gates to reject generator drift without writing files.
"""
from __future__ import annotations

import json
import pathlib
import sys
from dataclasses import dataclass

REPO = pathlib.Path(__file__).resolve().parents[3]
BIOME_DIR = REPO / "kubejs/data/infinite_domain/worldgen/biome"

STEP_COUNT = 11
STEP_UNDERGROUND_DECORATION = 7
STEP_FLUID_SPRINGS = 8
FIXTURE = "infinite_domain:hive_world_fixture_light"
SALVAGE = "infinite_domain:hive_world_salvage"
ACID = "infinite_domain:hive_world_acid_pool"


@dataclass(frozen=True)
class BiomeSpec:
    temperature: float
    downfall: float
    precipitation: bool
    sky: int
    fog: int
    water: int
    water_fog: int
    particle: str
    particle_probability: float
    ambient_sound: str
    additions_sound: str
    additions_chance: float
    music: str
    decoration: tuple[str, ...] = ()
    fluid_springs: tuple[str, ...] = ()


SPECS = {
    # Horizontal exterior roles.
    "hive_world_wastes": BiomeSpec(
        1.35, 0.92, True, 0x3B351B, 0x302D18, 0x66751E, 0x202607,
        "minecraft:white_ash", 0.005,
        "minecraft:ambient.basalt_deltas.loop",
        "minecraft:ambient.basalt_deltas.additions", 0.018,
        "minecraft:music.nether.basalt_deltas", fluid_springs=(ACID,),
    ),
    "hive_world_apron": BiomeSpec(
        1.05, 0.70, True, 0x312B1B, 0x29261A, 0x59651D, 0x1A2108,
        "minecraft:white_ash", 0.004,
        "minecraft:ambient.nether_wastes.loop",
        "minecraft:ambient.nether_wastes.additions", 0.014,
        "minecraft:music.nether.nether_wastes", decoration=(FIXTURE, SALVAGE),
    ),
    # Active vertical core roles.
    "hive_world_drown": BiomeSpec(
        0.62, 0.0, False, 0x080907, 0x171509, 0x4F6315, 0x151F04,
        "minecraft:white_ash", 0.0028,
        "minecraft:ambient.basalt_deltas.loop",
        "minecraft:ambient.basalt_deltas.additions", 0.014,
        "minecraft:music.overworld.dripstone_caves",
        decoration=(FIXTURE,), fluid_springs=(ACID,),
    ),
    "hive_world_underworks": BiomeSpec(
        0.78, 0.0, False, 0x0E100C, 0x1C1D12, 0x53621F, 0x1B2208,
        "minecraft:white_ash", 0.0024,
        "minecraft:ambient.nether_wastes.loop",
        "minecraft:ambient.nether_wastes.additions", 0.012,
        "minecraft:music.overworld.dripstone_caves", decoration=(FIXTURE, SALVAGE),
    ),
    "hive_world_furnace": BiomeSpec(
        1.25, 0.0, False, 0x1D120A, 0x2B2014, 0x41453D, 0x171712,
        "minecraft:white_ash", 0.0038,
        "minecraft:ambient.basalt_deltas.loop",
        "minecraft:ambient.basalt_deltas.additions", 0.016,
        "minecraft:music.nether.basalt_deltas", decoration=(FIXTURE, SALVAGE),
    ),
    "hive_world_billet": BiomeSpec(
        0.88, 0.0, False, 0x171612, 0x25221D, 0x3B4A4F, 0x10171B,
        "minecraft:white_ash", 0.0021,
        "minecraft:ambient.nether_wastes.loop",
        "minecraft:ambient.nether_wastes.additions", 0.010,
        "minecraft:music.nether.nether_wastes", decoration=(FIXTURE, SALVAGE),
    ),
    "hive_world_vaulting": BiomeSpec(
        0.45, 0.0, False, 0x0E141B, 0x1B2129, 0x33424E, 0x0E141B,
        "minecraft:warped_spore", 0.0012,
        "minecraft:ambient.soul_sand_valley.loop",
        "minecraft:ambient.soul_sand_valley.additions", 0.0111,
        "minecraft:music.overworld.deep_dark", decoration=(FIXTURE,),
    ),
    "hive_world_crown": BiomeSpec(
        0.20, 0.0, False, 0x15202C, 0x202B36, 0x33424E, 0x0E141B,
        "minecraft:warped_spore", 0.0006,
        "minecraft:ambient.soul_sand_valley.loop",
        "minecraft:ambient.soul_sand_valley.additions", 0.0075,
        "minecraft:music.overworld.deep_dark", decoration=(FIXTURE,),
    ),
    # Unrouted compatibility aliases retained for existing level data.
    "hive_world_sump": BiomeSpec(
        0.70, 0.0, False, 0x0B0B0A, 0x14140F, 0x53621F, 0x1B2208,
        "minecraft:white_ash", 0.0022,
        "minecraft:ambient.basalt_deltas.loop",
        "minecraft:ambient.basalt_deltas.additions", 0.0111,
        "minecraft:music.overworld.dripstone_caves",
        decoration=(FIXTURE,), fluid_springs=(ACID,),
    ),
    "hive_world_works": BiomeSpec(
        1.0, 0.0, False, 0x171410, 0x23201B, 0x3B4A4F, 0x10171B,
        "minecraft:white_ash", 0.0032,
        "minecraft:ambient.nether_wastes.loop",
        "minecraft:ambient.nether_wastes.additions", 0.0111,
        "minecraft:music.nether.nether_wastes", decoration=(FIXTURE, SALVAGE),
    ),
    "hive_world_vault": BiomeSpec(
        0.35, 0.0, False, 0x0E141B, 0x1B2129, 0x33424E, 0x0E141B,
        "minecraft:warped_spore", 0.0009,
        "minecraft:ambient.soul_sand_valley.loop",
        "minecraft:ambient.soul_sand_valley.additions", 0.0111,
        "minecraft:music.overworld.deep_dark", decoration=(FIXTURE,),
    ),
}


def build(spec: BiomeSpec) -> dict:
    features = [[] for _ in range(STEP_COUNT)]
    features[STEP_UNDERGROUND_DECORATION] = list(spec.decoration)
    features[STEP_FLUID_SPRINGS] = list(spec.fluid_springs)
    return {
        "temperature": spec.temperature,
        "downfall": spec.downfall,
        "has_precipitation": spec.precipitation,
        "carvers": {"air": []},
        "spawners": {key: [] for key in (
            "monster", "creature", "ambient", "axolotls",
            "underground_water_creature", "water_creature", "water_ambient", "misc",
        )},
        "spawn_costs": {},
        "features": features,
        "effects": {
            "sky_color": spec.sky,
            "fog_color": spec.fog,
            "water_color": spec.water,
            "water_fog_color": spec.water_fog,
            "mood_sound": {
                "sound": "minecraft:ambient.cave",
                "tick_delay": 6000,
                "block_search_extent": 8,
                "offset": 2.0,
            },
            "particle": {
                "probability": spec.particle_probability,
                "options": {"type": spec.particle},
            },
            "ambient_sound": spec.ambient_sound,
            "additions_sound": {
                "sound": spec.additions_sound,
                "tick_chance": spec.additions_chance,
            },
            "music": {
                "sound": spec.music,
                "min_delay": 12000,
                "max_delay": 24000,
                "replace_current_music": True,
            },
        },
    }


def render(payload: dict) -> str:
    return json.dumps(payload, indent=2) + "\n"


def main() -> int:
    check = "--check" in sys.argv
    drift: list[str] = []
    BIOME_DIR.mkdir(parents=True, exist_ok=True)
    for name, spec in SPECS.items():
        out = BIOME_DIR / f"{name}.json"
        expected = render(build(spec))
        if check:
            actual = out.read_text(encoding="utf-8") if out.is_file() else None
            if actual != expected:
                drift.append(str(out.relative_to(REPO)).replace("\\", "/"))
        else:
            out.write_text(expected, encoding="utf-8")
            print(f"wrote {out.relative_to(REPO)}")
    if drift:
        print("FAIL - Hive biome generator drift:")
        for path in drift:
            print(f"  {path}")
        return 1
    if check:
        print(f"PASS - {len(SPECS)} Hive biome files match the authoritative generator")
    return 0


if __name__ == "__main__":
    sys.exit(main())
