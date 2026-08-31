#!/usr/bin/env python3
"""Generate the six active Hive World band-district registries and pools.

The 30 band-specific NBT modules are authored binary inputs. This generator owns
their 18 template pools, six jigsaw structure definitions, and six random-spread
sets. Placement is biome-owned and seed-deterministic; it never consults quests,
players, teams, advancements, scoreboards, or game stages.

Use --check to verify byte-for-byte generator ownership without writing files.
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DATA = REPO / "kubejs/data/infinite_domain"
POOL_DIR = DATA / "worldgen/template_pool/hive_world"
STRUCTURE_DIR = DATA / "worldgen/structure"
SET_DIR = DATA / "worldgen/structure_set"
NBT_DIR = DATA / "structure/hive_world"


@dataclass(frozen=True)
class Band:
    slug: str
    min_y: int
    max_y: int
    size: int
    salt: int
    chamber_weight: int

    @property
    def biome(self) -> str:
        return f"infinite_domain:hive_world_{self.slug}"


BANDS = (
    Band("drown", -48, -8, 4, 927133, 3),
    Band("underworks", 12, 84, 4, 935052, 4),
    Band("furnace", 112, 192, 5, 942971, 5),
    Band("billet", 224, 336, 5, 950890, 6),
    Band("vaulting", 368, 464, 6, 958809, 7),
    Band("crown", 496, 584, 6, 966728, 8),
)
MODULE_ROLES = ("anchor", "gallery", "crossing", "chamber", "bulkhead")


def element(location: str, weight: int) -> dict:
    return {
        "weight": weight,
        "element": {
            "location": location,
            "processors": "minecraft:empty",
            "projection": "rigid",
            "element_type": "minecraft:single_pool_element",
        },
    }


def pools(band: Band) -> dict[str, dict]:
    prefix = f"infinite_domain:hive_world/{band.slug}"
    return {
        "start": {
            "fallback": "minecraft:empty",
            "elements": [element(f"{prefix}_anchor", 1)],
        },
        "branch": {
            "fallback": f"{prefix}_terminal",
            "elements": [
                element(f"{prefix}_gallery", 5),
                element(f"{prefix}_crossing", 3),
                element(f"{prefix}_chamber", band.chamber_weight),
            ],
        },
        "terminal": {
            "fallback": "minecraft:empty",
            "elements": [element(f"{prefix}_bulkhead", 1)],
        },
    }


def structure(band: Band) -> dict:
    return {
        "type": "minecraft:jigsaw",
        "biomes": [band.biome],
        "step": "underground_structures",
        "spawn_overrides": {},
        "terrain_adaptation": "none",
        "start_pool": f"infinite_domain:hive_world/{band.slug}_start",
        "size": band.size,
        "start_height": {
            "type": "minecraft:uniform",
            "min_inclusive": {"absolute": band.min_y},
            "max_inclusive": {"absolute": band.max_y},
        },
        "max_distance_from_center": 96,
        "use_expansion_hack": False,
        "liquid_settings": "ignore_waterlogging",
    }


def structure_set(band: Band) -> dict:
    return {
        "structures": [{
            "structure": f"infinite_domain:hive_world_district_{band.slug}",
            "weight": 1,
        }],
        "placement": {
            "type": "minecraft:random_spread",
            "spacing": 28,
            "separation": 12,
            "salt": band.salt,
        },
    }


def outputs() -> dict[Path, dict]:
    result: dict[Path, dict] = {}
    for band in BANDS:
        for role, payload in pools(band).items():
            result[POOL_DIR / f"{band.slug}_{role}.json"] = payload
        result[STRUCTURE_DIR / f"hive_world_district_{band.slug}.json"] = structure(band)
        result[SET_DIR / f"hive_world_district_{band.slug}.json"] = structure_set(band)
    return result


def render(payload: dict) -> str:
    return json.dumps(payload, indent=2) + "\n"


def main() -> int:
    check = "--check" in sys.argv
    missing_modules = [
        NBT_DIR / f"{band.slug}_{role}.nbt"
        for band in BANDS
        for role in MODULE_ROLES
        if not (NBT_DIR / f"{band.slug}_{role}.nbt").is_file()
    ]
    if missing_modules:
        print("FAIL - authored Hive band modules are missing:")
        for path in missing_modules:
            print(f"  {path.relative_to(REPO)}")
        return 1

    drift: list[Path] = []
    generated = outputs()
    for path, payload in generated.items():
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
        print("FAIL - Hive band-district generator drift:")
        for path in drift:
            print(f"  {path.relative_to(REPO)}")
        return 1
    if check:
        print(
            f"PASS - {len(generated)} band registry files and "
            f"{len(BANDS) * len(MODULE_ROLES)} authored modules are present and exact"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
