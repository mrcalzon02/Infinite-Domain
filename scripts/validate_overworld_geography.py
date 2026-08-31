#!/usr/bin/env python3
"""Validate Infinite Domain's authoritative overworld geography contract.

This is the pack-wide static gate for the central main continent, the cold and
hot north/south ocean zones, the recurring east/west continental regime, and
the Pelagos/Karsic abyssal corridors. It also proves that datapack structure
placement is worldgen-owned rather than quest-, player-, or team-gated.

Usage:
    python scripts/validate_overworld_geography.py
    python scripts/validate_overworld_geography.py --json
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path
from typing import Any

from validate_regional_culture_gradient import Graph, make_noise


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "datapacks" / "gradient_ocean_pack"
DATA = PACK / "data"
DF_DIR = DATA / "custom_worldgen" / "worldgen" / "density_function"
PRESET = ROOT / "kubejs" / "data" / "minecraft" / "worldgen" / "world_preset" / "normal.json"
STRUCTURES = ROOT / "kubejs" / "data" / "infinite_domain" / "worldgen" / "structure"
STRUCTURE_SETS = ROOT / "kubejs" / "data" / "infinite_domain" / "worldgen" / "structure_set"
SERVER_SCRIPTS = ROOT / "kubejs" / "server_scripts"
REPORT = ROOT / "docs" / "overworld-geography-validation.json"

CACHE_TYPES = {"minecraft:cache_2d", "minecraft:flat_cache", "minecraft:cache_once"}
STANDARD_PLACEMENTS = {"minecraft:random_spread", "minecraft:concentric_rings"}
FORBIDDEN_WORLDGEN_GATE = re.compile(
    r'"(?:quest|ftbquests|game_?stage|gamestage|advancement|scoreboard|team|player)"',
    re.IGNORECASE,
)
SCRIPTED_QUEST_PLACEMENT = re.compile(
    r"(?:quest|ftbquests|game.?stage|advancement).{0,160}(?:/place|place\s+structure|structure)"
    r"|(?:/place|place\s+structure|structure).{0,160}(?:quest|ftbquests|game.?stage|advancement)",
    re.IGNORECASE | re.DOTALL,
)


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def unwrap_cache(node: Any) -> Any:
    while isinstance(node, dict) and node.get("type") in CACHE_TYPES:
        node = node["argument"]
    return node


def custom_refs(node: Any) -> set[str]:
    found: set[str] = set()

    def walk(value: Any) -> None:
        if isinstance(value, str) and value.startswith("custom_worldgen:"):
            found.add(value)
        elif isinstance(value, dict):
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(node)
    return found


def close(a: float, b: float, tolerance: float = 1.0e-9) -> bool:
    return math.isclose(a, b, rel_tol=0.0, abs_tol=tolerance)


def run_checks(graph: Graph) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    checks: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []

    def record(check_id: str, name: str, passed: bool, detail: str, evidence: Any = None) -> None:
        entry: dict[str, Any] = {
            "id": check_id,
            "check": name,
            "passed": passed,
            "detail": detail,
        }
        if evidence is not None:
            entry["evidence"] = evidence
        checks.append(entry)
        if not passed:
            failures.append(entry)

    # OG-1: the only advertised overworld preset is the maintained normal preset,
    # and Moonlight actually loads the instance datapacks directory globally.
    moonlight = (ROOT / "config" / "moonlight-common.toml").read_text(encoding="utf-8")
    normal_tag = load(ROOT / "kubejs/data/minecraft/tags/worldgen/world_preset/normal.json")
    extended_tag = load(ROOT / "kubejs/data/minecraft/tags/worldgen/world_preset/extended.json")
    pack_meta = load(PACK / "pack.mcmeta")
    activation_ok = (
        re.search(r'^\s*global_datapacks_folder\s*=\s*"datapacks"\s*$', moonlight, re.MULTILINE)
        is not None
        and normal_tag == {"replace": True, "values": ["minecraft:normal"]}
        and extended_tag == {"replace": True, "values": ["minecraft:normal"]}
        and pack_meta.get("pack", {}).get("pack_format") == 48
    )
    record(
        "OG-1",
        "the maintained normal preset and gradient datapack are globally active",
        activation_ok,
        "Moonlight points at datapacks; normal and extended tags expose only minecraft:normal; pack format is 48",
    )

    preset = load(PRESET)
    overworld = preset.get("dimensions", {}).get("minecraft:overworld", {})
    generator = overworld.get("generator", {})
    source = generator.get("biome_source", {})
    canonical_ok = (
        overworld.get("type") == "minecraft:overworld"
        and generator.get("type") == "minecraft:noise"
        and generator.get("settings") == "wastelands:wasteland"
        and source.get("type") == "isekai_api:climate_zones"
        and source.get("fallback") == "wastelands:apocalypse"
    )
    record(
        "OG-2",
        "minecraft:normal owns the Wastelands overworld routing",
        canonical_ok,
        "noise settings wastelands:wasteland with the Isekai climate-zone source and Wastelands fallback",
    )

    # OG-3: terrain consumers reach the custom topology and direct abyssal-depth
    # channel through vanilla density-function overrides.
    mc_continents = load(DATA / "minecraft/worldgen/density_function/overworld/continents.json")
    mc_depth = load(DATA / "minecraft/worldgen/density_function/overworld/depth.json")
    bridge_ok = (
        mc_continents == {"type": "minecraft:cache_2d", "argument": "custom_worldgen:continents"}
        and "custom_worldgen:abyssal_floor_depression" in custom_refs(mc_depth)
    )
    record(
        "OG-3",
        "vanilla Overworld terrain consumes the custom continent and abyssal-depth chains",
        bridge_ok,
        "overworld/continents delegates to custom_worldgen:continents and overworld/depth subtracts abyssal_floor_depression",
        {
            "continent_override": mc_continents,
            "depth_custom_refs": sorted(custom_refs(mc_depth)),
        },
    )

    # OG-4: prove the radial central continent's core and shoreline feather from
    # the density graph, then bracket its land-biased branch across noise extrema.
    central_samples = {
        str(radius): graph.evaluate("custom_worldgen:central_continent_mask", radius, 0.0, 0.0, make_noise(0.0))
        for radius in (0, 4000, 4400, 4800, 8000)
    }
    continents_node = unwrap_cache(graph.nodes["custom_worldgen:continents"])
    central_branch = continents_node.get("b") if isinstance(continents_node, dict) else None
    central_land_samples = {
        str(noise_value): graph.evaluate(central_branch, 0.0, 0.0, 0.0, make_noise(noise_value))
        for noise_value in (-1.0, -0.5, 0.0, 0.5, 1.0)
    }
    central_ok = (
        close(central_samples["0"], 1.0)
        and close(central_samples["4000"], 1.0)
        and close(central_samples["4400"], 0.5)
        and close(central_samples["4800"], 0.0)
        and close(central_samples["8000"], 0.0)
        and min(central_land_samples.values()) >= 0.05
        and custom_refs(continents_node) >= {
            "custom_worldgen:central_continent_mask",
            "custom_worldgen:abyssal_outer_continents",
            "custom_worldgen:large_continents",
        }
    )
    record(
        "OG-4",
        "the central main continent is guaranteed through radius 4000 and feathers to ocean by 4800",
        central_ok,
        "radial mask is 1/1/0.5/0 at r=0/4000/4400/4800 and the central branch never falls below continentalness 0.05",
        {"mask": central_samples, "central_land_bracket": central_land_samples},
    )

    # OG-5: compare directional branches under the same artificial noise. East
    # and west must carry the recurring large-continent bias; north and south
    # must carry the smaller, ocean-separated bias.
    axes = {
        "east": (8000.0, 0.0),
        "west": (-8000.0, 0.0),
        "south": (0.0, 8000.0),
        "north": (0.0, -8000.0),
        "diagonal": (8000.0, 8000.0),
    }
    direction_mask = {
        name: graph.evaluate("custom_worldgen:east_west_continent_mask", x, 0.0, z, make_noise(0.0))
        for name, (x, z) in axes.items()
    }
    directional_samples: dict[str, dict[str, float]] = {}
    directional_ok = True
    for noise_value in (-1.0, -0.5, 0.0, 0.5, 1.0):
        values = {
            name: graph.evaluate("custom_worldgen:outer_directional_continents", x, 0.0, z, make_noise(noise_value))
            for name, (x, z) in axes.items()
            if name != "diagonal"
        }
        directional_samples[str(noise_value)] = values
        directional_ok = directional_ok and close(values["east"] - values["north"], 0.5)
        directional_ok = directional_ok and close(values["west"] - values["south"], 0.5)
    directional_ok = directional_ok and all(
        close(direction_mask[name], expected)
        for name, expected in {"east": 1.0, "west": 1.0, "north": 0.0, "south": 0.0, "diagonal": 0.5}.items()
    )
    record(
        "OG-5",
        "east/west prefer recurring large continents while north/south remain ocean-separated",
        directional_ok,
        "the directional mask selects opposite branches on cardinal axes; the east/west branch is exactly 0.50 more land-biased under identical noise",
        {"direction_mask": direction_mask, "continentalness_brackets": directional_samples},
    )

    # OG-6: the north/south axes retain their cold/hot identities while the
    # central and east/west Wastelands regimes remain climate-neutral.
    temperature_samples = {
        name: graph.evaluate("custom_worldgen:regional_temperature", x, 0.0, z, make_noise(0.0))
        for name, (x, z) in {"center": (0.0, 0.0), **{k: v for k, v in axes.items() if k != "diagonal"}}.items()
    }
    temperature_ok = (
        close(temperature_samples["north"], -1.0)
        and close(temperature_samples["south"], 1.0)
        and close(temperature_samples["east"], 0.0)
        and close(temperature_samples["west"], 0.0)
        and close(temperature_samples["center"], 0.0)
    )
    record(
        "OG-6",
        "north is cold, south is hot, and the central/east/west land regimes stay temperate",
        temperature_ok,
        "regional_temperature resolves to -1/+1 on the north/south axes and 0 on center/east/west",
        temperature_samples,
    )

    # OG-7: abyssal shaping belongs only to the east/west ocean corridor, with
    # separate selectors for the Pelagos (west) and Karsic (east) sides.
    corridor_samples = {
        name: graph.evaluate("custom_worldgen:east_west_ocean_corridor_mask", x, 0.0, z, make_noise(0.0))
        for name, (x, z) in axes.items()
        if name != "diagonal"
    }
    selector_samples = {
        "west_at_west": graph.evaluate("custom_worldgen:western_abyss_selector", -8000.0, 0.0, 0.0, make_noise(0.0)),
        "east_at_west": graph.evaluate("custom_worldgen:eastern_abyss_selector", -8000.0, 0.0, 0.0, make_noise(0.0)),
        "west_at_east": graph.evaluate("custom_worldgen:western_abyss_selector", 8000.0, 0.0, 0.0, make_noise(0.0)),
        "east_at_east": graph.evaluate("custom_worldgen:eastern_abyss_selector", 8000.0, 0.0, 0.0, make_noise(0.0)),
    }
    west_refs = custom_refs(graph.nodes["custom_worldgen:western_depth_depression"])
    east_refs = custom_refs(graph.nodes["custom_worldgen:eastern_depth_depression"])
    abyss_refs = custom_refs(graph.nodes["custom_worldgen:abyssal_outer_continents"])
    floor_refs = custom_refs(graph.nodes["custom_worldgen:abyssal_floor_depression"])
    abyss_ok = (
        corridor_samples["east"] >= 0.98
        and corridor_samples["west"] >= 0.98
        and close(corridor_samples["north"], 0.0)
        and close(corridor_samples["south"], 0.0)
        and selector_samples == {
            "west_at_west": 1.0,
            "east_at_west": 0.0,
            "west_at_east": 0.0,
            "east_at_east": 1.0,
        }
        and {"custom_worldgen:western_abyss_selector", "custom_worldgen:east_west_ocean_corridor_mask"} <= west_refs
        and {"custom_worldgen:eastern_abyss_selector", "custom_worldgen:east_west_ocean_corridor_mask"} <= east_refs
        and {"custom_worldgen:outer_directional_continents", "custom_worldgen:western_depth_depression", "custom_worldgen:eastern_depth_depression"} <= abyss_refs
        and {"custom_worldgen:western_depth_depression", "custom_worldgen:eastern_depth_depression"} <= floor_refs
    )
    record(
        "OG-7",
        "Pelagos and Karsic abyssal deformation is confined to the west/east ocean corridors",
        abyss_ok,
        "the corridor mask is active only on the X axis; side selectors are mutually exclusive; both continent pressure and direct floor depth consume the paired depressions",
        {"corridor": corridor_samples, "selectors": selector_samples},
    )

    rules: list[dict[str, Any]] = source.get("rules", [])

    # OG-8: all eight named abyssal depth biomes retain their exact humidity and
    # continentalness contracts, including the neutral multiplayer seam.
    abyssal_contract = {
        "western_hadal_trench": ([-1.0, -0.2], [-1.2, -1.02]),
        "eastern_hadal_trench": ([0.2, 1.0], [-1.2, -1.02]),
        "western_fracture_field": ([-1.0, -0.2], [-1.02, -0.82]),
        "eastern_fracture_field": ([0.2, 1.0], [-1.02, -0.82]),
        "western_abyssal_plain": ([-1.0, -0.2], [-0.82, -0.6]),
        "eastern_abyssal_plain": ([0.2, 1.0], [-0.82, -0.6]),
        "western_continental_slope": ([-1.0, -0.2], [-0.6, -0.455]),
        "eastern_continental_slope": ([0.2, 1.0], [-0.6, -0.455]),
    }
    abyssal_rule_failures: list[str] = []
    for path, (humidity, continentalness) in abyssal_contract.items():
        matches = [rule for rule in rules if rule.get("biome") == f"infinite_domain:{path}"]
        if len(matches) != 1 or matches[0].get("temperature") != [-0.99, 0.99] or matches[0].get("humidity") != humidity or matches[0].get("continentalness") != continentalness:
            abyssal_rule_failures.append(path)
    seam_bands = {
        tuple(rule.get("continentalness", []))
        for rule in rules
        if rule.get("biome") == "minecraft:deep_ocean" and rule.get("humidity") == [-0.2, 0.2]
    }
    expected_seams = {(-1.2, -1.02), (-1.02, -0.82), (-0.82, -0.6), (-0.6, -0.455)}
    record(
        "OG-8",
        "all eight depth-graded abyssal biomes and the neutral seam are routable",
        not abyssal_rule_failures and seam_bands == expected_seams,
        "four Pelagos/Karsic band pairs keep exact humidity and continentalness ranges; -0.2..0.2 stays vanilla deep ocean",
        {"invalid_biomes": abyssal_rule_failures, "neutral_seam_bands": sorted(seam_bands)},
    )

    # OG-9: the five implemented Karsic land biomes must precede the ungated
    # temperate fallback. Pelagos remains deliberately deferred by its plan.
    karsic_expected = {
        "infinite_domain:karsic_uplands": [-1.0, -0.55],
        "infinite_domain:karsic_district": [-0.55, -0.15],
        "infinite_domain:karsic_taiga_margin": [-0.15, 0.2],
        "infinite_domain:karsic_industrial_belt": [0.2, 0.5],
        "infinite_domain:karsic_steppe_waste": [0.5, 1.0],
    }
    first_fallback = next(
        (index for index, rule in enumerate(rules) if rule.get("temperature") == [-0.99, 0.99] and "erosion" in rule and "humidity" not in rule),
        -1,
    )
    karsic_failures: list[str] = []
    for biome, erosion in karsic_expected.items():
        matches = [(index, rule) for index, rule in enumerate(rules) if rule.get("biome") == biome]
        biome_file = ROOT / "kubejs/data/infinite_domain/worldgen/biome" / f"{biome.split(':', 1)[1]}.json"
        if (
            len(matches) != 1
            or matches[0][0] >= first_fallback
            or matches[0][1].get("temperature") != [-0.99, 0.99]
            or matches[0][1].get("humidity") != [0.2, 1.0]
            or matches[0][1].get("continentalness") != [-0.19, 1.2]
            or matches[0][1].get("erosion") != erosion
            or not biome_file.is_file()
        ):
            karsic_failures.append(biome)
    record(
        "OG-9",
        "the implemented eastern Karsic land zone is reachable without changing the central continent",
        not karsic_failures and first_fallback >= 0,
        "five humidity-gated Karsic rules and biome files precede the ungated temperate Wastelands fallback; Pelagos land remains plan-deferred",
        {"invalid_biomes": karsic_failures, "fallback_index": first_fallback},
    )

    # OG-10: preserve the documented north/south biome vocabulary.
    north_required = {
        "minecraft:snowy_taiga", "minecraft:grove", "minecraft:taiga",
        "minecraft:old_growth_spruce_taiga", "minecraft:old_growth_pine_taiga",
        "minecraft:ice_spikes", "minecraft:snowy_slopes", "minecraft:jagged_peaks",
        "minecraft:frozen_peaks", "minecraft:frozen_river", "minecraft:snowy_beach",
    }
    south_required = {
        "minecraft:mangrove_swamp", "minecraft:jungle", "minecraft:bamboo_jungle",
        "minecraft:sparse_jungle", "minecraft:savanna", "minecraft:savanna_plateau",
        "minecraft:windswept_savanna", "minecraft:desert", "minecraft:badlands",
        "minecraft:wooded_badlands", "minecraft:eroded_badlands",
    }
    north_present = {rule.get("biome") for rule in rules if rule.get("temperature") == [-1.0, -0.99]}
    south_present = {rule.get("biome") for rule in rules if rule.get("temperature") == [0.99, 1.0]}
    north_oceans = {"minecraft:deep_frozen_ocean", "minecraft:deep_cold_ocean", "minecraft:frozen_ocean", "minecraft:cold_ocean"}
    south_oceans = {"minecraft:deep_lukewarm_ocean", "minecraft:warm_ocean"}
    record(
        "OG-10",
        "cold northern and hot southern land/ocean biome families remain complete",
        north_required | north_oceans <= north_present and south_required | south_oceans <= south_present,
        "required polar and warm biome families remain represented in their saturated temperature bands",
        {
            "missing_north": sorted((north_required | north_oceans) - north_present),
            "missing_south": sorted((south_required | south_oceans) - south_present),
        },
    )

    # OG-11: the hottest 2D graph nodes stay cached. This is a static ownership
    # check; only runtime profiling can measure the actual generation cost.
    cached_nodes = [
        "continents", "outer_directional_continents", "east_west_continent_mask",
        "small_continents", "large_continents", "city_humidity", "regional_temperature",
        "abyssal_ocean_mask", "abyssal_plain_mask", "abyssal_fracture_mask",
        "hadal_trench_mask", "abyssal_slope_band_mask",
    ]
    uncached = [name for name in cached_nodes if graph.nodes[f"custom_worldgen:{name}"].get("type") not in CACHE_TYPES]
    record(
        "OG-11",
        "high-fanout horizontal geography fields retain chunk-local caches",
        not uncached,
        "central/directional continents, climate routing, and abyssal band masks are cache_2d or flat_cache wrapped",
        {"uncached": uncached, "checked": cached_nodes},
    )

    # OG-12: structure starts are ordinary datapack worldgen. No player, team,
    # quest, advancement, or game-stage token may enter a structure definition,
    # structure set, or scripted placement bridge.
    structure_files = sorted(STRUCTURES.rglob("*.json"))
    set_files = sorted(STRUCTURE_SETS.rglob("*.json"))
    gated_json: list[str] = []
    invalid_placements: list[str] = []
    missing_structure_refs: list[str] = []
    for path in structure_files + set_files:
        text = path.read_text(encoding="utf-8")
        if FORBIDDEN_WORLDGEN_GATE.search(text):
            gated_json.append(path.relative_to(ROOT).as_posix())
    for path in set_files:
        payload = load(path)
        placement_type = payload.get("placement", {}).get("type")
        if placement_type not in STANDARD_PLACEMENTS:
            invalid_placements.append(f"{path.relative_to(ROOT).as_posix()}: {placement_type}")
        for entry in payload.get("structures", []):
            structure_id = entry.get("structure", "")
            if structure_id.startswith("infinite_domain:"):
                rel = structure_id.split(":", 1)[1]
                if not (STRUCTURES / f"{rel}.json").is_file():
                    missing_structure_refs.append(f"{path.relative_to(ROOT).as_posix()} -> {structure_id}")
    scripted_gates = [
        path.relative_to(ROOT).as_posix()
        for path in sorted(SERVER_SCRIPTS.rglob("*.js"))
        if SCRIPTED_QUEST_PLACEMENT.search(path.read_text(encoding="utf-8"))
    ]
    quest_independent = not gated_json and not invalid_placements and not missing_structure_refs and not scripted_gates
    record(
        "OG-12",
        "structure spawning is datapack-owned and independent of quests, players, and teams",
        quest_independent,
        f"{len(structure_files)} structures and {len(set_files)} structure sets use standard worldgen placement with registered references; no scripted quest-placement bridge exists",
        {
            "gated_json": gated_json,
            "invalid_placements": invalid_placements,
            "missing_structure_references": missing_structure_refs,
            "scripted_quest_placement": scripted_gates,
        },
    )

    return checks, failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--json", action="store_true", help="print the report to stdout instead of a summary")
    args = parser.parse_args()

    graph = Graph(DF_DIR)
    checks, failures = run_checks(graph)
    report = {
        "purpose": "Static contract for Infinite Domain's central continent, north/south zones, east/west continents and Abyssal oceans, plus multiplayer-safe quest-independent structure spawning.",
        "authority": [
            "datapacks/gradient_ocean_pack/README.md",
            "docs/GRADIENT_OCEAN_PACK_VALIDATION.md",
            "docs/ABYSSAL_OCEAN_PROGRAM.md",
            "docs/KARSIC_DIRECTORATE_STRUCTURE_PROGRAM.md",
            "docs/WORLDGEN_STRUCTURE_SAFETY.md",
        ],
        "checks": checks,
        "passed": not failures,
        "runtime_validation": "This gate proves file-backed topology, routing, registration, and multiplayer ownership. Fresh-world terrain appearance, structure placement quality, and generation performance remain runtime checks.",
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        for check in checks:
            print(f"{'PASS' if check['passed'] else 'FAIL'}  {check['id']:<6} {check['check']}")
            print(f"               {check['detail']}")
        print()
        print(f"{len(checks) - len(failures)}/{len(checks)} checks passed")
        print(f"report: {REPORT.relative_to(ROOT).as_posix()}")

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
