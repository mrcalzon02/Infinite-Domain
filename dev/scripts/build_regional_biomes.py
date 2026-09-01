#!/usr/bin/env python3
"""Author the regional land biomes for the Karsic and Pelagos surface regions.

These biomes exist for one reason: Lost Cities' CityStyleSelector matches on
biomes, so a region needs distinct biome ids before it can have distinct city
styles. Their terrain behaviour deliberately mirrors the surrounding wasteland -
same carver set, same vanilla ore suite, same wasteland surface features - so
the regions read as *architecturally* different, not ecologically different.

Per the regional structure programs: "Do not invent new terrain behaviour here.
The point of the region is architecture, not a new biome ecology."

These files are project-authored. Third-party feature and carver identifiers are
referenced (which is ordinary datapack interop) but no upstream biome definition
is copied, per REPOSITORY_SCOPE.md.

Authority: docs/KARSIC_DIRECTORATE_STRUCTURE_PROGRAM.md section 12.3
           docs/PELAGOS_COMPACT_STRUCTURE_PROGRAM.md section 12.3

Usage:
    python scripts/build_regional_biomes.py --culture karsic
    python scripts/build_regional_biomes.py --culture karsic --check
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BIOME_DIR = ROOT / "kubejs" / "data" / "infinite_domain" / "worldgen" / "biome"
TAG_DIR = ROOT / "kubejs" / "data" / "infinite_domain" / "tags" / "worldgen" / "biome"

CARVERS = ["minecraft:cave", "minecraft:cave_extra_underground", "minecraft:canyon"]

# The standard overworld ore suite, so a regional biome does not accidentally
# create its own mining economy.
ORES = [
    "minecraft:ore_dirt", "minecraft:ore_gravel",
    "minecraft:ore_granite_upper", "minecraft:ore_granite_lower",
    "minecraft:ore_diorite_upper", "minecraft:ore_diorite_lower",
    "minecraft:ore_andesite_upper", "minecraft:ore_andesite_lower",
    "minecraft:ore_tuff",
    "minecraft:ore_coal_upper", "minecraft:ore_coal_lower",
    "minecraft:ore_iron_upper", "minecraft:ore_iron_middle", "minecraft:ore_iron_small",
    "minecraft:ore_gold", "minecraft:ore_gold_lower",
    "minecraft:ore_redstone", "minecraft:ore_redstone_lower",
    "minecraft:ore_diamond", "minecraft:ore_diamond_medium",
    "minecraft:ore_diamond_large", "minecraft:ore_diamond_buried",
    "minecraft:ore_lapis", "minecraft:ore_lapis_buried",
    "minecraft:ore_copper",
    "minecraft:underwater_magma",
    "minecraft:disk_sand", "minecraft:disk_clay", "minecraft:disk_gravel",
]

EMPTY_SPAWNERS = {
    "ambient": [], "axolotls": [], "creature": [], "misc": [], "monster": [],
    "underground_water_creature": [], "water_ambient": [], "water_creature": [],
}

MOOD_SOUND = {
    "block_search_extent": 8, "offset": 2.0,
    "sound": "minecraft:ambient.cave", "tick_delay": 6000,
}


def features(surface: list[str], vegetal: list[str] | None = None) -> list[list[str]]:
    """The eleven generation steps, with our choices in the surface and vegetal slots."""
    steps: list[list[str]] = [[] for _ in range(11)]
    steps[1] = ["minecraft:lake_lava_underground"]
    steps[2] = ["minecraft:amethyst_geode"]
    steps[3] = ["minecraft:monster_room", "minecraft:monster_room_deep"]
    steps[4] = list(surface)
    steps[6] = list(ORES)
    steps[7] = ["minecraft:glow_lichen"]
    steps[8] = ["minecraft:spring_water", "minecraft:spring_lava"]
    steps[9] = list(vegetal or [])
    steps[10] = ["minecraft:freeze_top_layer"]
    return steps


def biome(*, temperature: float, downfall: float, precipitation: bool,
          sky: int, fog: int, grass: int, foliage: int, water: int, water_fog: int,
          surface: list[str], vegetal: list[str] | None = None,
          spawn_probability: float = 0.03, music: str = "minecraft:music.overworld.badlands") -> dict[str, Any]:
    return {
        "carvers": {"air": CARVERS},
        "creature_spawn_probability": spawn_probability,
        "downfall": downfall,
        "effects": {
            "fog_color": fog,
            "foliage_color": foliage,
            "grass_color": grass,
            "mood_sound": MOOD_SOUND,
            "music": {"max_delay": 24000, "min_delay": 12000,
                      "replace_current_music": False, "sound": music},
            "sky_color": sky,
            "water_color": water,
            "water_fog_color": water_fog,
        },
        "features": features(surface, vegetal),
        "has_precipitation": precipitation,
        "spawn_costs": {},
        "spawners": EMPTY_SPAWNERS,
        "temperature": temperature,
    }


# --- Karsic (East) --------------------------------------------------------
# Cold continental. Cooler, greyer, slightly blue-shifted against the central
# wasteland so the region reads as further north and further inland.
KARSIC_SKY, KARSIC_FOG = 0x6E7A85, 0x5C6670
KARSIC_WATER, KARSIC_WATER_FOG = 0x2E4A52, 0x1A2E33

KARSIC = {
    "karsic_uplands": biome(
        temperature=0.15, downfall=0.2, precipitation=True,
        sky=KARSIC_SKY, fog=KARSIC_FOG, grass=0x6B7A5C, foliage=0x5E6B4F,
        water=KARSIC_WATER, water_fog=KARSIC_WATER_FOG,
        surface=["wastelands:infrastructure"],
    ),
    "karsic_district": biome(
        temperature=0.3, downfall=0.0, precipitation=False,
        sky=KARSIC_SKY, fog=KARSIC_FOG, grass=0x63705A, foliage=0x58654C,
        water=KARSIC_WATER, water_fog=KARSIC_WATER_FOG,
        surface=["wastelands:infrastructure", "wastelands:contaminated_site"],
    ),
    "karsic_taiga_margin": biome(
        temperature=0.2, downfall=0.35, precipitation=True,
        sky=0x74808A, fog=0x626C76, grass=0x5D7050, foliage=0x4F6245,
        water=KARSIC_WATER, water_fog=KARSIC_WATER_FOG,
        surface=["wastelands:infrastructure"],
    ),
    "karsic_industrial_belt": biome(
        temperature=0.35, downfall=0.0, precipitation=False,
        sky=0x6A7078, fog=0x585E66, grass=0x67705C, foliage=0x5A6350,
        water=0x33474C, water_fog=0x1E2E33,
        surface=["wastelands:infrastructure", "wastelands:contaminated_site"],
    ),
    "karsic_steppe_waste": biome(
        temperature=0.45, downfall=0.0, precipitation=False,
        sky=0x7B818A, fog=0x676D75, grass=0x74765E, foliage=0x686A54,
        water=KARSIC_WATER, water_fog=KARSIC_WATER_FOG,
        surface=["wastelands:infrastructure"],
    ),
}

KARSIC_TAGS = {
    "karsic_region_biomes": [f"infinite_domain:{name}" for name in KARSIC],
    "karsic_settlement_biomes": ["infinite_domain:karsic_district", "infinite_domain:karsic_industrial_belt"],
    "karsic_rural_biomes": ["infinite_domain:karsic_taiga_margin", "infinite_domain:karsic_steppe_waste"],
    "karsic_upland_biomes": ["infinite_domain:karsic_uplands"],
}

CULTURES = {
    "karsic": (KARSIC, KARSIC_TAGS),
}


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--culture", required=True, choices=sorted(CULTURES))
    parser.add_argument("--check", action="store_true", help="verify on-disk files match, do not write")
    args = parser.parse_args()

    biomes, tags = CULTURES[args.culture]
    drift: list[str] = []

    for name, definition in biomes.items():
        path = BIOME_DIR / f"{name}.json"
        if args.check:
            if not path.exists():
                drift.append(f"missing: {path.relative_to(ROOT).as_posix()}")
            elif json.loads(path.read_text(encoding="utf-8")) != definition:
                drift.append(f"drifted: {path.relative_to(ROOT).as_posix()}")
        else:
            write_json(path, definition)

    for name, values in tags.items():
        path = TAG_DIR / f"{name}.json"
        payload = {"replace": False, "values": values}
        if args.check:
            if not path.exists():
                drift.append(f"missing: {path.relative_to(ROOT).as_posix()}")
            elif json.loads(path.read_text(encoding="utf-8")) != payload:
                drift.append(f"drifted: {path.relative_to(ROOT).as_posix()}")
        else:
            write_json(path, payload)

    if args.check:
        if drift:
            print(f"FAIL  {len(drift)} file(s) differ from the authored definitions:")
            for d in drift:
                print(f"  - {d}")
            return 1
        print(f"PASS  {len(biomes)} biomes and {len(tags)} tags match the authored definitions")
        return 0

    print(f"wrote {len(biomes)} biomes to {BIOME_DIR.relative_to(ROOT).as_posix()}")
    for name in biomes:
        print(f"  infinite_domain:{name}")
    print(f"wrote {len(tags)} tags to {TAG_DIR.relative_to(ROOT).as_posix()}")
    for name, values in tags.items():
        print(f"  #infinite_domain:{name}  ({len(values)} entries)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
