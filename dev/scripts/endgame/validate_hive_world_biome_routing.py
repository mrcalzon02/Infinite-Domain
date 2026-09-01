#!/usr/bin/env python3
"""Validate the static C0046 six-band Hive World biome-routing candidate.

The report samples each horizontal mask class at every vertical-band midpoint,
checks half-block boundary thresholds against the active height gradient, verifies
band-specific feature/effect identities, and proves each district is owned by its
matching core biome. This is offline evidence only; in-client volume sampling and
codec acceptance remain required by P03-GATE.
"""
from __future__ import annotations

import json
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "kubejs/data/infinite_domain"
DIMENSION = DATA / "dimension/hive_world.json"
NOISE_SETTINGS = DATA / "worldgen/noise_settings/hive_world.json"
BIOME_DIR = DATA / "worldgen/biome"
STRUCTURE_DIR = DATA / "worldgen/structure"
STRUCTURE_SET_DIR = DATA / "worldgen/structure_set"
POOL_DIR = DATA / "worldgen/template_pool/hive_world"
NBT_DIR = DATA / "structure/hive_world"
REPORT = ROOT / "docs/endgame/hive-world-biome-routing.json"
OWNERSHIP = ROOT / "docs/endgame/generated-output-manifest.json"
COMPANION_MAIN = ROOT / (
    "packdev/hive-world-companion/src/main/java/infinitedomain/hiveworld/"
    "HiveWorldCompanion.java"
)
COMPANION_REGISTRY = ROOT / (
    "packdev/hive-world-companion/src/main/java/infinitedomain/hiveworld/"
    "worldgen/HiveDensityFunctions.java"
)
COMPANION_JAR = ROOT / "mods/infinite-domain-hive-world-companion-0.1.0.jar"

MIN_Y = -64
MAX_Y = 607
FIXTURE = "infinite_domain:hive_world_fixture_light"
SALVAGE = "infinite_domain:hive_world_salvage"
ACID = "infinite_domain:hive_world_acid_pool"


@dataclass(frozen=True)
class Band:
    slug: str
    min_y: int
    max_y: int
    depth: tuple[float, float]
    decoration: tuple[str, ...]
    fluid_springs: tuple[str, ...] = ()

    @property
    def biome(self) -> str:
        return f"infinite_domain:hive_world_{self.slug}"

    @property
    def midpoint(self) -> int:
        return (self.min_y + self.max_y) // 2


BANDS = (
    Band("drown", -64, -1, (0.811, 1.0), (FIXTURE,), (ACID,)),
    Band("underworks", 0, 95, (0.525, 0.811), (FIXTURE, SALVAGE)),
    Band("furnace", 96, 207, (0.191, 0.525), (FIXTURE, SALVAGE)),
    Band("billet", 208, 351, (-0.238, 0.191), (FIXTURE, SALVAGE)),
    Band("vaulting", 352, 479, (-0.620, -0.238), (FIXTURE,)),
    Band("crown", 480, 607, (-1.0, -0.620), (FIXTURE,)),
)
LEGACY_ALIASES = (
    "infinite_domain:hive_world_sump",
    "infinite_domain:hive_world_works",
    "infinite_domain:hive_world_vault",
)
DISTRICT_CONFIG = {
    "drown": (-48, -8, 4, 927133, 3),
    "underworks": (12, 84, 4, 935052, 4),
    "furnace": (112, 192, 5, 942971, 5),
    "billet": (224, 336, 5, 950890, 6),
    "vaulting": (368, 464, 6, 958809, 7),
    "crown": (496, 584, 6, 966728, 8),
}
MODULE_ROLES = ("anchor", "gallery", "crossing", "chamber", "bulkhead")


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def depth_at(y: float) -> float:
    return 1.0 - 2.0 * ((y - MIN_Y) / (MAX_Y - MIN_Y))


def interval_contains(value: float, interval: Any) -> bool:
    if isinstance(interval, list) and len(interval) == 2:
        return interval[0] <= value <= interval[1]
    return interval == value


def route(entries: list[dict[str, Any]], continentalness: float, depth: float) -> list[str]:
    return [
        entry.get("biome", "")
        for entry in entries
        if interval_contains(continentalness, entry.get("parameters", {}).get("continentalness"))
        and interval_contains(depth, entry.get("parameters", {}).get("depth"))
    ]


def main() -> int:
    checks: list[dict[str, Any]] = []
    failures: list[str] = []

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
            failures.append(f"{check_id}: {detail}")

    try:
        dimension = load(DIMENSION)
        noise_settings = load(NOISE_SETTINGS)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL - cannot load routing inputs: {exc}")
        return 1

    source = dimension.get("generator", {}).get("biome_source", {})
    entries = source.get("biomes", []) if source.get("type") == "minecraft:multi_noise" else []
    routed = [entry.get("biome") for entry in entries]
    expected_routed = [
        "infinite_domain:hive_world_wastes",
        "infinite_domain:hive_world_apron",
        *(band.biome for band in BANDS),
    ]
    record(
        "HBR-1",
        "fresh generation exposes two horizontal and six vertical biome roles",
        routed == expected_routed,
        "multi_noise routing order and cardinality match the C0046 contract",
        {"actual": routed, "expected": expected_routed},
    )

    router = noise_settings.get("noise_router", {})
    depth_node = router.get("depth", {})
    depth_ok = depth_node == {
        "type": "minecraft:y_clamped_gradient",
        "from_y": MIN_Y,
        "to_y": MAX_Y,
        "from_value": 1.0,
        "to_value": -1.0,
    }
    continents_node = router.get("continents")
    region_path = DATA / "worldgen/density_function/hive_world/biome_region.json"
    try:
        region_node = load(region_path)
    except (OSError, json.JSONDecodeError) as exc:
        region_node = {"error": str(exc)}
    region_ok = region_node == {
        "type": "minecraft:range_choice",
        "input": "infinite_domain:hive_world/core_mask",
        "min_inclusive": 0.0,
        "max_exclusive": 2.0,
        "when_in_range": 0.5,
        "when_out_of_range": {
            "type": "minecraft:range_choice",
            "input": "infinite_domain:hive_world/apron_mask",
            "min_inclusive": 0.0,
            "max_exclusive": 2.0,
            "when_in_range": -0.2,
            "when_out_of_range": -1.0,
        },
    }
    record(
        "HBR-2",
        "biome routing consumes the horizontal mask and full-height depth gradient",
        depth_ok and continents_node == "infinite_domain:hive_world/biome_region" and region_ok,
        "continents emits discrete wastes/apron/core values; depth maps Y-64..607 monotonically from +1 to -1",
        {"continents": continents_node, "biome_region": region_node, "depth": depth_node},
    )

    actual_depths = {
        entry.get("biome"): entry.get("parameters", {}).get("depth")
        for entry in entries
        if entry.get("biome") in {band.biome for band in BANDS}
    }
    expected_depths = {band.biome: list(band.depth) for band in BANDS}
    boundary_samples = {
        f"{band.max_y + 0.5:g}": round(depth_at(band.max_y + 0.5), 3)
        for band in BANDS[:-1]
    }
    expected_boundaries = [band.depth[0] for band in BANDS[:-1]]
    boundary_ok = list(boundary_samples.values()) == expected_boundaries
    record(
        "HBR-3",
        "six depth windows tile the bands at half-block boundaries",
        actual_depths == expected_depths and boundary_ok,
        "rounded half-block thresholds are shared exactly, with no gap between core bands",
        {
            "depth_windows": actual_depths,
            "half_block_boundary_samples": boundary_samples,
        },
    )

    samples: list[dict[str, Any]] = []
    samples_ok = True
    horizontal = (
        ("wastes", -1.0, "infinite_domain:hive_world_wastes"),
        ("apron", -0.2, "infinite_domain:hive_world_apron"),
        ("core", 0.5, None),
    )
    for band in BANDS:
        sample_depth = depth_at(band.midpoint)
        for region, continentalness, horizontal_expected in horizontal:
            expected = horizontal_expected or band.biome
            actual = route(entries, continentalness, sample_depth)
            passed = actual == [expected]
            samples_ok = samples_ok and passed
            samples.append({
                "region": region,
                "band": band.slug,
                "y": band.midpoint,
                "continentalness": continentalness,
                "depth": round(sample_depth, 6),
                "expected": expected,
                "actual": actual,
                "passed": passed,
            })
    record(
        "HBR-4",
        "sampled biome volumes separate masks and every vertical midpoint",
        samples_ok,
        "18 horizontal/vertical samples each resolve to exactly one intended biome",
        samples,
    )

    biome_evidence: dict[str, Any] = {}
    biomes_ok = True
    fog_colours: set[int] = set()
    for band in BANDS:
        path = BIOME_DIR / f"hive_world_{band.slug}.json"
        try:
            payload = load(path)
        except (OSError, json.JSONDecodeError) as exc:
            biomes_ok = False
            biome_evidence[band.slug] = {"error": str(exc)}
            continue
        features = payload.get("features", [])
        decoration = features[7] if len(features) == 11 else None
        fluid_springs = features[8] if len(features) == 11 else None
        spawners_empty = all(not values for values in payload.get("spawners", {}).values())
        effects = payload.get("effects", {})
        fog = effects.get("fog_color")
        particle_probability = effects.get("particle", {}).get("probability")
        valid = (
            len(features) == 11
            and decoration == list(band.decoration)
            and fluid_springs == list(band.fluid_springs)
            and spawners_empty
            and payload.get("has_precipitation") is False
            and isinstance(fog, int)
            and isinstance(particle_probability, (int, float))
        )
        biomes_ok = biomes_ok and valid
        if isinstance(fog, int):
            fog_colours.add(fog)
        biome_evidence[band.slug] = {
            "valid": valid,
            "temperature": payload.get("temperature"),
            "fog_color": fog,
            "particle_probability": particle_probability,
            "decoration": decoration,
            "fluid_springs": fluid_springs,
            "spawners_empty": spawners_empty,
        }
    biomes_ok = biomes_ok and len(fog_colours) == len(BANDS)
    record(
        "HBR-5",
        "each band has a distinct fallback identity and bounded feature vocabulary",
        biomes_ok,
        "six unique fog colours; no native spawns; acid only in The Drown; salvage only in middle inhabited/industrial bands",
        biome_evidence,
    )

    structure_evidence: dict[str, Any] = {}
    structures_ok = True
    live_salts: list[int] = []
    for band in BANDS:
        min_y, max_y, size, salt, chamber_weight = DISTRICT_CONFIG[band.slug]
        structure_path = STRUCTURE_DIR / f"hive_world_district_{band.slug}.json"
        set_path = STRUCTURE_SET_DIR / f"hive_world_district_{band.slug}.json"
        expected_structure = {
            "type": "minecraft:jigsaw",
            "biomes": [band.biome],
            "step": "underground_structures",
            "spawn_overrides": {},
            "terrain_adaptation": "none",
            "start_pool": f"infinite_domain:hive_world/{band.slug}_start",
            "size": size,
            "start_height": {
                "type": "minecraft:uniform",
                "min_inclusive": {"absolute": min_y},
                "max_inclusive": {"absolute": max_y},
            },
            "max_distance_from_center": 96,
            "use_expansion_hack": False,
            "liquid_settings": "ignore_waterlogging",
        }
        expected_set = {
            "structures": [{
                "structure": f"infinite_domain:hive_world_district_{band.slug}",
                "weight": 1,
            }],
            "placement": {
                "type": "minecraft:random_spread",
                "spacing": 28,
                "separation": 12,
                "salt": salt,
            },
        }
        prefix = f"infinite_domain:hive_world/{band.slug}"

        def pool_element(role: str, weight: int) -> dict[str, Any]:
            return {
                "weight": weight,
                "element": {
                    "location": f"{prefix}_{role}",
                    "processors": "minecraft:empty",
                    "projection": "rigid",
                    "element_type": "minecraft:single_pool_element",
                },
            }

        expected_pools = {
            "start": {
                "fallback": "minecraft:empty",
                "elements": [pool_element("anchor", 1)],
            },
            "branch": {
                "fallback": f"{prefix}_terminal",
                "elements": [
                    pool_element("gallery", 5),
                    pool_element("crossing", 3),
                    pool_element("chamber", chamber_weight),
                ],
            },
            "terminal": {
                "fallback": "minecraft:empty",
                "elements": [pool_element("bulkhead", 1)],
            },
        }
        try:
            actual_structure = load(structure_path)
            actual_set = load(set_path)
            actual_pools = {
                role: load(POOL_DIR / f"{band.slug}_{role}.json")
                for role in ("start", "branch", "terminal")
            }
        except (OSError, json.JSONDecodeError) as exc:
            actual_structure = {"error": str(exc)}
            actual_set = {"error": str(exc)}
            actual_pools = {"error": str(exc)}
        missing_modules = [
            f"{band.slug}_{role}.nbt"
            for role in MODULE_ROLES
            if not (NBT_DIR / f"{band.slug}_{role}.nbt").is_file()
        ]
        passed = (
            actual_structure == expected_structure
            and actual_set == expected_set
            and actual_pools == expected_pools
            and not missing_modules
        )
        structures_ok = structures_ok and passed
        if actual_set == expected_set:
            live_salts.append(salt)
        structure_evidence[band.slug] = {
            "passed": passed,
            "biome": actual_structure.get("biomes"),
            "start_height": actual_structure.get("start_height"),
            "size": actual_structure.get("size"),
            "placement": actual_set.get("placement"),
            "pool_roles_exact": actual_pools == expected_pools,
            "missing_modules": missing_modules,
        }
    structures_ok = structures_ok and len(live_salts) == len(set(live_salts)) == len(BANDS)
    record(
        "HBR-6",
        "band districts, pools, modules, and biomes share exact placement ownership",
        structures_ok,
        "each Y-bounded district uses its matching biome, exact authored modules, and a unique deterministic salt",
        structure_evidence,
    )

    aliases_present = all(
        (BIOME_DIR / f"{alias.split(':', 1)[1]}.json").is_file()
        for alias in LEGACY_ALIASES
    )
    aliases_unrouted = not (set(routed) & set(LEGACY_ALIASES))
    placed_biomes = {
        biome_id
        for path in sorted(STRUCTURE_DIR.glob("hive_world_district_*.json"))
        for biome_id in load(path).get("biomes", [])
    }
    aliases_unplaced = not (placed_biomes & set(LEGACY_ALIASES))
    record(
        "HBR-7",
        "legacy three-way biome IDs remain loadable but cannot own fresh generation",
        aliases_present and aliases_unrouted and aliases_unplaced,
        "sump/works/vault compatibility files exist outside the routing and structure selectors",
        {
            "aliases": list(LEGACY_ALIASES),
            "present": aliases_present,
            "unrouted": aliases_unrouted,
            "unplaced": aliases_unplaced,
        },
    )

    legacy_structure_path = STRUCTURE_DIR / "hive_world_district.json"
    legacy_set_path = STRUCTURE_SET_DIR / "hive_world_district.json"
    try:
        legacy_structure = load(legacy_structure_path)
        legacy_set = load(legacy_set_path)
        ownership = load(OWNERSHIP)
    except (OSError, json.JSONDecodeError) as exc:
        legacy_structure = {"error": str(exc)}
        legacy_set = {"error": str(exc)}
        ownership = {}
    generators = ownership.get("generators", {})
    band_owner = set(generators.get(
        "scripts/endgame/generate_hive_world_band_districts.py", []
    ))
    biome_owner = set(generators.get("scripts/endgame/generate_hive_world_biomes.py", []))
    routing_owner = set(generators.get(
        "scripts/endgame/generate_hive_world_biome_routing.py", []
    ))
    hand_authored = set(ownership.get("hand_authored", []))
    expected_band_outputs = {
        f"kubejs/data/infinite_domain/worldgen/template_pool/hive_world/{band.slug}_{role}.json"
        for band in BANDS
        for role in ("start", "branch", "terminal")
    } | {
        f"kubejs/data/infinite_domain/worldgen/structure/hive_world_district_{band.slug}.json"
        for band in BANDS
    } | {
        f"kubejs/data/infinite_domain/worldgen/structure_set/hive_world_district_{band.slug}.json"
        for band in BANDS
    }
    expected_biome_outputs = {
        f"kubejs/data/infinite_domain/worldgen/biome/hive_world_{slug}.json"
        for slug in (
            "wastes", "apron", "drown", "underworks", "furnace", "billet",
            "vaulting", "crown", "sump", "works", "vault",
        )
    }
    expected_band_modules = {
        f"kubejs/data/infinite_domain/structure/hive_world/{band.slug}_{role}.nbt"
        for band in BANDS
        for role in MODULE_ROLES
    }
    expected_routing_outputs = {
        "kubejs/data/infinite_domain/worldgen/density_function/hive_world/stack_field.json",
        "kubejs/data/infinite_domain/worldgen/density_function/hive_world/core_mask.json",
        "kubejs/data/infinite_domain/worldgen/density_function/hive_world/apron_mask.json",
        "kubejs/data/infinite_domain/worldgen/density_function/hive_world/biome_region.json",
        "kubejs/data/infinite_domain/dimension/hive_world.json",
    }
    ownership_ok = (
        band_owner == expected_band_outputs
        and biome_owner == expected_biome_outputs
        and routing_owner == expected_routing_outputs
        and expected_band_modules <= hand_authored
    )
    legacy_ok = (
        legacy_structure.get("biomes") == list(LEGACY_ALIASES)
        and legacy_set.get("structures") == []
        and legacy_set.get("placement", {}).get("salt") == 927132
    )
    record(
        "HBR-8",
        "generator ownership is complete and the legacy placement set is inert",
        ownership_ok and legacy_ok,
        "all active biome/district JSON has one generator; band NBT is declared authored input; the unrouted compatibility district cannot schedule starts",
        {
            "ownership_exact": ownership_ok,
            "legacy_structure_biomes": legacy_structure.get("biomes"),
            "legacy_set": legacy_set,
        },
    )

    required_companion_entries = {
        "META-INF/neoforge.mods.toml",
        "infinitedomain/hiveworld/HiveWorldCompanion.class",
        "infinitedomain/hiveworld/client/HiveAtmosphereClient.class",
        "infinitedomain/hiveworld/client/HiveAtmosphereClient$HiveDimensionEffects.class",
        "infinitedomain/hiveworld/client/HiveCloudRenderer.class",
        "infinitedomain/hiveworld/client/HiveSulfurRain.class",
        "infinitedomain/hiveworld/client/LayeredFogProfile.class",
        "infinitedomain/hiveworld/worldgen/HiveDensityFunctions.class",
        "infinitedomain/hiveworld/worldgen/HiveMacroLayout.class",
        "infinitedomain/hiveworld/worldgen/HiveStackField.class",
        "infinitedomain/hiveworld/worldgen/HiveTrunkAxis.class",
    }
    companion_evidence: dict[str, Any] = {}
    companion_ok = False
    try:
        main_source = COMPANION_MAIN.read_text(encoding="utf-8")
        registry_source = COMPANION_REGISTRY.read_text(encoding="utf-8")
        with zipfile.ZipFile(COMPANION_JAR) as archive:
            entries = set(archive.namelist())
            main_class = archive.read(
                "infinitedomain/hiveworld/HiveWorldCompanion.class"
            )
            atmosphere_class = archive.read(
                "infinitedomain/hiveworld/client/"
                "HiveAtmosphereClient$HiveDimensionEffects.class"
            )
            bad_member = archive.testzip()
        missing_entries = sorted(required_companion_entries - entries)
        source_wired = "HiveDensityFunctions.register(modBus);" in main_source
        registry_wired = (
            'TYPES.register("stack_field"' in registry_source
            and 'TYPES.register("trunk_axis"' in registry_source
        )
        bytecode_wired = (
            b"infinitedomain/hiveworld/worldgen/HiveDensityFunctions" in main_class
            and b"register" in main_class
        )
        client_bytecode_wired = (
            b"infinitedomain/hiveworld/client/HiveCloudRenderer" in atmosphere_class
            and b"infinitedomain/hiveworld/client/HiveSulfurRain" in atmosphere_class
        )
        companion_ok = (
            not missing_entries
            and bad_member is None
            and source_wired
            and registry_wired
            and bytecode_wired
            and client_bytecode_wired
        )
        companion_evidence = {
            "jar": str(COMPANION_JAR.relative_to(ROOT)),
            "missing_entries": missing_entries,
            "zip_integrity": bad_member is None,
            "source_registration_call": source_wired,
            "source_codec_registrations": registry_wired,
            "installed_bytecode_registration_reference": bytecode_wired,
            "installed_client_atmosphere_references": client_bytecode_wired,
        }
    except (OSError, KeyError, zipfile.BadZipFile) as exc:
        companion_evidence = {"error": str(exc)}
    record(
        "HBR-9",
        "installed companion owns the custom density-function codecs",
        companion_ok,
        "source registration, packaged codec classes, bytecode wiring, and jar integrity are all required before JSON may reference the custom types",
        companion_evidence,
    )

    report = {
        "contract": "EG-P03-S05-C0046-static-candidate-v2",
        "passed": not failures,
        "check_count": len(checks),
        "failure_count": len(failures),
        "runtime_acceptance": "pending dedicated-server codec load, /locate biome sampling, chunk seams, and P03-GATE",
        "checks": checks,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print("Hive World six-band biome routing validator")
    for check in checks:
        print(f"  {'PASS' if check['passed'] else 'FAIL'} {check['id']} - {check['check']}")
    print(f"  report -> {REPORT.relative_to(ROOT)}")
    if failures:
        for failure in failures:
            print(f"  {failure}")
        return 1
    print(f"PASS - {len(checks)}/{len(checks)} checks; 18 sampled biome volumes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
