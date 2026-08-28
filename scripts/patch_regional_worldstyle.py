#!/usr/bin/env python3
"""Wire a region into the Lost Cities worldstyle.

Two independent operations, deliberately separable because they have different
prerequisites:

  --multipliers   Add citybiomemultipliers for the region's biomes. Safe to run
                  as soon as the biomes exist. Without it, newly-created
                  regional biomes would fall back to a 1.0 multiplier while
                  wastelands:city keeps 1.35, silently reducing city density in
                  the region compared to before the biomes were introduced.

  --citystyles    Add the region's biome-matched citystyle selectors AND add the
                  `excluding` matcher to the central-continent wasteland
                  selectors. These MUST land together: excluding the wasteland
                  styles from a region that has no styles of its own would leave
                  that region with nothing to build. Requires the citystyles to
                  exist first.

Lost Cities' CityStyleSelector carries an optional `biomes` field of type
BiomeMatcher (if_all / if_any / excluding), verified against
mods/lostcities-1.21-8.4.1.jar. No mod change is required.

Both operations are idempotent.

Authority: docs/KARSIC_DIRECTORATE_STRUCTURE_PROGRAM.md sections 11.4, 11.5, 12.3
           docs/PELAGOS_COMPACT_STRUCTURE_PROGRAM.md sections 11.4, 11.5, 12.3

Usage:
    python scripts/patch_regional_worldstyle.py --culture karsic --multipliers
    python scripts/patch_regional_worldstyle.py --culture karsic --citystyles
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
WORLDSTYLE = ROOT / "kubejs" / "data" / "lostcities" / "lostcities" / "worldstyles" / "standard.json"

REGION_TAG = {
    "karsic": "#infinite_domain:karsic_region_biomes",
    "pelagos": "#infinite_domain:pelagos_region_biomes",
}
ALL_REGION_TAGS = ["#infinite_domain:karsic_region_biomes", "#infinite_domain:pelagos_region_biomes"]

# Mirrors the existing wastelands:city (1.35) and forest/apocalypse (0.75)
# weighting so a region keeps the density role of the biomes it replaces.
MULTIPLIERS = {
    "karsic": [
        (1.35, ["infinite_domain:karsic_district"]),
        (1.2, ["infinite_domain:karsic_industrial_belt"]),
        (0.75, ["infinite_domain:karsic_taiga_margin", "infinite_domain:karsic_steppe_waste"]),
    ],
    "pelagos": [
        (1.35, ["infinite_domain:pelagos_town"]),
        (1.2, ["infinite_domain:pelagos_estuary_belt"]),
        (0.75, ["infinite_domain:pelagos_wooded_vale", "infinite_domain:pelagos_coastal_waste"]),
    ],
}

CITYSTYLES = {
    "karsic": [
        ("infinite_domain:karsic_mikrorayon", 1.0),
        ("infinite_domain:karsic_administrative_core", 1.0),
        ("infinite_domain:karsic_industrial_combine", 1.0),
        ("infinite_domain:karsic_rail_settlement", 1.0),
        ("infinite_domain:karsic_utility_compound", 1.0),
        ("infinite_domain:karsic_highway_service", 1.0),
        ("infinite_domain:karsic_rural_settlement", 1.0),
        ("infinite_domain:karsic_garrison", 1.0),
    ],
    "pelagos": [
        ("infinite_domain:pelagos_terraced_district", 2.0),
        ("infinite_domain:pelagos_high_street", 1.0),
        ("infinite_domain:pelagos_industrial_estate", 1.0),
        ("infinite_domain:pelagos_rail_quarter", 1.0),
        ("infinite_domain:pelagos_dockside", 1.0),
        ("infinite_domain:pelagos_civic_campus", 1.0),
        ("infinite_domain:pelagos_suburban_estate", 1.0),
        ("infinite_domain:pelagos_village_and_coast", 1.0),
    ],
}


def load() -> dict[str, Any]:
    return json.loads(WORLDSTYLE.read_text(encoding="utf-8"))


def save(style: dict[str, Any]) -> None:
    WORLDSTYLE.write_text(json.dumps(style, indent=2) + "\n", encoding="utf-8", newline="\n")


def patch_multipliers(style: dict[str, Any], culture: str) -> tuple[int, int]:
    entries: list[dict[str, Any]] = style.setdefault("citybiomemultipliers", [])
    prefix = f"infinite_domain:{culture}_"
    before = len(entries)
    kept = [
        e for e in entries
        if not any(b.startswith(prefix) for b in e.get("biomes", {}).get("if_any", []))
    ]
    added = [
        {"multiplier": multiplier, "biomes": {"if_any": biomes}}
        for multiplier, biomes in MULTIPLIERS[culture]
    ]
    style["citybiomemultipliers"] = kept + added
    return before, len(style["citybiomemultipliers"])


def patch_citystyles(style: dict[str, Any], culture: str) -> tuple[int, int, int]:
    selectors: list[dict[str, Any]] = style["citystyles"]
    prefix = f"infinite_domain:{culture}_"
    kept = [s for s in selectors if not s["citystyle"].startswith(prefix)]

    # Central-continent styles must exclude every regional territory, or a
    # region would grow central architecture alongside its own.
    excluded = 0
    for selector in kept:
        if selector["citystyle"].startswith("infinite_domain:wasteland_"):
            matcher = selector.setdefault("biomes", {})
            if matcher.get("excluding") != ALL_REGION_TAGS:
                matcher["excluding"] = list(ALL_REGION_TAGS)
                excluded += 1

    added = [
        {"factor": factor, "citystyle": name, "biomes": {"if_any": [REGION_TAG[culture]]}}
        for name, factor in CITYSTYLES[culture]
    ]
    style["citystyles"] = kept + added
    return len(selectors), len(style["citystyles"]), excluded


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--culture", required=True, choices=sorted(REGION_TAG))
    parser.add_argument("--multipliers", action="store_true")
    parser.add_argument("--citystyles", action="store_true")
    args = parser.parse_args()

    if not (args.multipliers or args.citystyles):
        parser.error("pass --multipliers and/or --citystyles")

    style = load()

    if args.multipliers:
        before, after = patch_multipliers(style, args.culture)
        print(f"citybiomemultipliers  {before} -> {after}")
        for multiplier, biomes in MULTIPLIERS[args.culture]:
            print(f"  {multiplier:>5}  {', '.join(biomes)}")

    if args.citystyles:
        missing = [
            name for name, _ in CITYSTYLES[args.culture]
            if not (ROOT / "kubejs" / "data" / "infinite_domain" / "lostcities" / "citystyles"
                    / f"{name.split(':', 1)[1]}.json").exists()
        ]
        if missing:
            print("REFUSED  --citystyles would exclude the wasteland styles from a region "
                  "that has no styles of its own.")
            print("         Missing citystyle files:")
            for name in missing:
                print(f"           {name}")
            return 1
        before, after, excluded = patch_citystyles(style, args.culture)
        print(f"citystyles            {before} -> {after}")
        print(f"wasteland selectors given an `excluding` matcher: {excluded}")

    save(style)
    print(f"wrote {WORLDSTYLE.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
