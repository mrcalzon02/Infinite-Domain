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
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "kubejs/data/infinite_domain"
DIMENSION = DATA / "dimension/hive_world.json"
NOISE_SETTINGS = DATA / "worldgen/noise_settings/hive_world.json"
BIOME_DIR = DATA / "worldgen/biome"
STRUCTURE_DIR = DATA / "worldgen/structure"
REPORT = ROOT / "docs/endgame/hive-world-biome-routing.json"

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

    depth_node = noise_settings.get("noise_router", {}).get("depth", {})
    depth_ok = depth_node == {
        "type": "minecraft:y_clamped_gradient",
        "from_y": MIN_Y,
        "to_y": MAX_Y,
        "from_value": 1.0,
        "to_value": -1.0,
    }
    record(
        "HBR-2",
        "biome depth consumes the accepted full-height gradient",
        depth_ok,
        "depth maps Y-64..607 monotonically from +1 to -1",
        depth_node,
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
    for band in BANDS:
        path = STRUCTURE_DIR / f"hive_world_district_{band.slug}.json"
        try:
            payload = load(path)
            actual = payload.get("biomes")
        except (OSError, json.JSONDecodeError) as exc:
            actual = {"error": str(exc)}
        expected = [band.biome]
        passed = actual == expected
        structures_ok = structures_ok and passed
        structure_evidence[band.slug] = {"expected": expected, "actual": actual, "passed": passed}
    record(
        "HBR-6",
        "band districts and band biomes share exact placement ownership",
        structures_ok,
        "each Y-bounded district is eligible only in its matching core biome",
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

    report = {
        "contract": "EG-P03-S05-C0046-static-candidate-v1",
        "passed": not failures,
        "check_count": len(checks),
        "failure_count": len(failures),
        "runtime_acceptance": "pending in-client codec load, /locate biome sampling, chunk seams, and P03-GATE",
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
