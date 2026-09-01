#!/usr/bin/env python3
"""Insert the regional land-biome rules into the canonical Overworld preset.

The preset routes ocean bands by humidity (West -1.0..-0.2, seam -0.2..0.2,
East 0.2..1.0) but its temperate *land* rules carry no humidity gate at all, so
East and West land are identical. This adds the regional rules immediately
before that ungated temperate block, where first-match-wins ordering means:

  * ocean and the polar/desert temperature extremes are already claimed by
    earlier rules and are untouched;
  * the central continent is untouched, because
    `custom_worldgen:regional_culture_gradient` holds humidity at the neutral
    seam inside radius 4000 (see scripts/validate_regional_culture_gradient.py);
  * only land in the East or West lobes, beyond the central continent, matches.

The operation is idempotent: existing regional rules are removed and rewritten,
so re-running after a roster or band change is safe.

Authority: docs/KARSIC_DIRECTORATE_STRUCTURE_PROGRAM.md section 12.3
           docs/PELAGOS_COMPACT_STRUCTURE_PROGRAM.md section 12.3

Usage:
    python scripts/patch_regional_biome_routing.py --culture karsic
    python scripts/patch_regional_biome_routing.py --culture karsic --check
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PRESET = ROOT / "kubejs" / "data" / "minecraft" / "worldgen" / "world_preset" / "normal.json"

TEMPERATE = [-0.99, 0.99]
LAND_CONTINENTALNESS = [-0.19, 1.2]

HUMIDITY_BAND = {
    "karsic": [0.2, 1.0],     # East, positive side of east_west_gradient
    "pelagos": [-1.0, -0.2],  # West, negative side
}

# Mirrors the erosion bands of the ungated temperate land rules this block
# precedes, so a regional biome inherits the terrain role of what it replaces.
EROSION_BANDS = {
    "karsic": [
        ("infinite_domain:karsic_uplands", [-1.0, -0.55]),
        ("infinite_domain:karsic_district", [-0.55, -0.15]),
        ("infinite_domain:karsic_taiga_margin", [-0.15, 0.2]),
        ("infinite_domain:karsic_industrial_belt", [0.2, 0.5]),
        ("infinite_domain:karsic_steppe_waste", [0.5, 1.0]),
    ],
    "pelagos": [
        ("infinite_domain:pelagos_moorland", [-1.0, -0.55]),
        ("infinite_domain:pelagos_town", [-0.55, -0.15]),
        ("infinite_domain:pelagos_wooded_vale", [-0.15, 0.2]),
        ("infinite_domain:pelagos_estuary_belt", [0.2, 0.5]),
        ("infinite_domain:pelagos_coastal_waste", [0.5, 1.0]),
    ],
}

ALL_REGIONAL_PREFIXES = ("infinite_domain:karsic_", "infinite_domain:pelagos_")


def regional_rules(culture: str) -> list[dict[str, Any]]:
    return [
        {
            "biome": biome,
            "temperature": list(TEMPERATE),
            "humidity": list(HUMIDITY_BAND[culture]),
            "continentalness": list(LAND_CONTINENTALNESS),
            "erosion": list(erosion),
        }
        for biome, erosion in EROSION_BANDS[culture]
    ]


def is_regional(rule: dict[str, Any]) -> bool:
    return rule.get("biome", "").startswith(ALL_REGIONAL_PREFIXES)


def temperate_land_index(rules: list[dict[str, Any]]) -> int:
    """Index of the first ungated temperate land rule."""
    for index, rule in enumerate(rules):
        if rule.get("temperature") == TEMPERATE and "erosion" in rule and "humidity" not in rule:
            return index
    raise SystemExit("could not locate the ungated temperate land rules in the world preset")


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--culture", required=True, choices=sorted(HUMIDITY_BAND))
    parser.add_argument("--check", action="store_true", help="report the routing, do not write")
    args = parser.parse_args()

    preset = json.loads(PRESET.read_text(encoding="utf-8"))
    source = preset["dimensions"]["minecraft:overworld"]["generator"]["biome_source"]
    rules: list[dict[str, Any]] = source["rules"]

    existing = [r for r in rules if is_regional(r)]
    others = [r for r in rules if not is_regional(r)]
    keep = [r for r in existing if not r["biome"].startswith(f"infinite_domain:{args.culture}_")]

    insert_at = temperate_land_index(others)
    new_rules = others[:insert_at] + keep + regional_rules(args.culture) + others[insert_at:]

    if args.check:
        print(f"rules total       {len(rules)}")
        print(f"regional present  {len(existing)}")
        print(f"temperate land at index {insert_at} (of the non-regional rules)")
        print()
        print("current tail:")
        for rule in rules[-12:]:
            gates = {k: v for k, v in rule.items() if k != "biome"}
            print(f"  {rule['biome']:<44} {gates}")
        return 0

    source["rules"] = new_rules
    PRESET.write_text(json.dumps(preset, separators=(", ", ": ")) + "\n", encoding="utf-8", newline="\n")

    added = len(regional_rules(args.culture))
    print(f"culture           {args.culture}")
    print(f"humidity band     {HUMIDITY_BAND[args.culture]}")
    print(f"rules before      {len(rules)}")
    print(f"rules after       {len(new_rules)}  (+{len(new_rules) - len(rules)})")
    print(f"inserted          {added} regional rules before the ungated temperate land block")
    print()
    print("new tail:")
    for rule in new_rules[-(added + 5):]:
        gates = {k: v for k, v in rule.items() if k != "biome"}
        print(f"  {rule['biome']:<44} {gates}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
