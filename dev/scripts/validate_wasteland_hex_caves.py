#!/usr/bin/env python3
<<<<<<< Updated upstream:dev/scripts/validate_wasteland_hex_caves.py
"""Static/reference validator for Infinite Domain's wasteland hex-cave source module."""
=======
"""Validate the canonical Wasteland hex-grid cave implementation."""
>>>>>>> Stashed changes:scripts/validate_wasteland_hex_caves.py

from __future__ import annotations

import json
import math
<<<<<<< Updated upstream:dev/scripts/validate_wasteland_hex_caves.py
import sys
from pathlib import Path

MASK = (1 << 64) - 1
SQRT_3 = 1.7320508075688772
HEX_SIZE = 28.0

WARP_X_SALT = 0x6A09E667F3BCC909
WARP_Z_SALT = 0xBB67AE8584CAA73B
MACRO_SALT = 0x3C6EF372FE94F82B
PLASMA_SALT = 0xA54FF53A5F1D36F1
WIDTH_SALT = 0x510E527FADE682D1
GOLDEN_GAMMA = 0x9E3779B97F4A7C15

REFERENCE_SEED = 123456789
REFERENCE_MIN = -256
REFERENCE_MAX = 256
REFERENCE_STEP = 2

EXPECTED_RANGES = {
    "raw_hex_percent": (28.3, 28.7),
    "visible_hex_percent": (22.3, 22.7),
    "occluded_hex_percent": (5.8, 6.2),
    "chamber_percent": (4.1, 4.5),
}


def u64(value: int) -> int:
    return value & MASK


def unsigned_shift(value: int, bits: int) -> int:
    return (value & MASK) >> bits


def random_signed(seed: int, x: int, z: int) -> float:
    mixed = u64(seed) ^ u64(x * 0x632BE59BD9B4E019) ^ u64(z * 0x9E3779B185EBCA87)
    mixed = u64(mixed ^ unsigned_shift(mixed, 30))
    mixed = u64(mixed * 0xBF58476D1CE4E5B9)
    mixed = u64(mixed ^ unsigned_shift(mixed, 27))
    mixed = u64(mixed * 0x94D049BB133111EB)
    mixed = u64(mixed ^ unsigned_shift(mixed, 31))
    mantissa = unsigned_shift(mixed, 11)
    return mantissa * (2.0 ** -53) * 2.0 - 1.0


def smooth(value: float) -> float:
    return value * value * (3.0 - 2.0 * value)


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def value_noise(seed: int, x: float, z: float) -> float:
    x0 = math.floor(x)
    z0 = math.floor(z)
    x1 = x0 + 1
    z1 = z0 + 1
    tx = smooth(x - x0)
    tz = smooth(z - z0)

    top = lerp(random_signed(seed, x0, z0), random_signed(seed, x1, z0), tx)
    bottom = lerp(random_signed(seed, x0, z1), random_signed(seed, x1, z1), tx)
    return lerp(top, bottom, tz)


def fbm(seed: int, x: float, z: float, scale: float, octaves: int) -> float:
    frequency = 1.0 / scale
    amplitude = 1.0
    total = 0.0
    normalization = 0.0

    for octave in range(octaves):
        octave_seed = u64(seed + octave * GOLDEN_GAMMA)
        total += value_noise(octave_seed, x * frequency, z * frequency) * amplitude
        normalization += amplitude
        amplitude *= 0.5
        frequency *= 2.0

    return total / normalization


def java_round(value: float) -> int:
    return math.floor(value + 0.5)


def round_axial(q: float, r: float) -> tuple[int, int]:
    x = q
    z = r
    y = -x - z

    rx = java_round(x)
    ry = java_round(y)
    rz = java_round(z)

    x_diff = abs(rx - x)
    y_diff = abs(ry - y)
    z_diff = abs(rz - z)

    if x_diff > y_diff and x_diff > z_diff:
        rx = -ry - rz
    elif y_diff > z_diff:
        ry = -rx - rz
    else:
        rz = -rx - ry

    return rx, rz


def nearest_hex_boundary(x: float, z: float) -> tuple[float, float]:
    qf = (SQRT_3 / 3.0 * x - z / 3.0) / HEX_SIZE
    rf = (2.0 / 3.0 * z) / HEX_SIZE
    rounded_q, rounded_r = round_axial(qf, rf)

    best = math.inf
    second = math.inf

    for dq in range(-2, 3):
        for dr in range(-2, 3):
            q = rounded_q + dq
            r = rounded_r + dr
            center_x = HEX_SIZE * SQRT_3 * (q + r / 2.0)
            center_z = HEX_SIZE * 1.5 * r
            distance = math.hypot(x - center_x, z - center_z)

            if distance < best:
                second, best = best, distance
            elif distance < second:
                second = distance

    return max(0.0, (second - best) * 0.5), best


def sample_reference(seed: int, block_x: int, block_z: int) -> tuple[bool, bool, bool, bool]:
    x = block_x + 0.5
    z = block_z + 0.5

    warp_x = fbm(u64(seed ^ WARP_X_SALT), x, z, 112.0, 4) * 7.0
    warp_z = fbm(u64(seed ^ WARP_Z_SALT), x + 317.0, z - 191.0, 112.0, 4) * 7.0
    boundary_distance, center_distance = nearest_hex_boundary(x + warp_x, z + warp_z)

    macro = fbm(u64(seed ^ MACRO_SALT), x, z, 180.0, 5)
    plasma = fbm(u64(seed ^ PLASMA_SALT), x - 911.0, z + 613.0, 54.0, 4)
    width_noise = fbm(u64(seed ^ WIDTH_SALT), x + 83.0, z + 47.0, 72.0, 3)
    local_width = 2.48 + (width_noise + 1.0) * 1.3

    raw_hex = boundary_distance <= local_width
    occluded = macro > 0.43 or (plasma > 0.41 and macro > -0.15)
    visible_hex = raw_hex and not occluded
    occluded_hex = raw_hex and occluded
    chamber = macro < -0.20 and plasma < 0.30 and center_distance < HEX_SIZE * 0.72
    return raw_hex, visible_hex, occluded_hex, chamber


def reference_metrics() -> dict[str, float]:
    counts = [0, 0, 0, 0]
    samples = 0

    for x in range(REFERENCE_MIN, REFERENCE_MAX, REFERENCE_STEP):
        for z in range(REFERENCE_MIN, REFERENCE_MAX, REFERENCE_STEP):
            values = sample_reference(REFERENCE_SEED, x, z)
            counts = [count + int(value) for count, value in zip(counts, values)]
            samples += 1

    names = ("raw_hex_percent", "visible_hex_percent", "occluded_hex_percent", "chamber_percent")
    return {name: count / samples * 100.0 for name, count in zip(names, counts)}


def require_text(text: str, needle: str, failures: list[str], label: str) -> None:
    if needle not in text:
        failures.append(f"{label}: missing required source contract {needle!r}")


def validate_repository(root: Path) -> list[str]:
    failures: list[str] = []
    module = root / "dev" / "packdev" / "wasteland-hex-caves"
    source = module / "src" / "main" / "java" / "infinitedomain" / "wastelandhexcaves"
    resources = module / "src" / "main" / "resources"

    feature_path = source / "HexCaveFeature.java"
    modifier_path = source / "WastelandNamespaceBiomeModifier.java"
    main_path = source / "WastelandHexCaves.java"

    for path in (feature_path, modifier_path, main_path):
        if not path.is_file():
            failures.append(f"missing source file: {path.relative_to(root)}")

    if failures:
        return failures

    feature = feature_path.read_text(encoding="utf-8")
    modifier = modifier_path.read_text(encoding="utf-8")
    main = main_path.read_text(encoding="utf-8")

    for needle in (
        "level.getSeed()",
        "nearestHexBoundary",
        "double localWidth = 2.48",
        "macro > 0.43",
        "plasma > 0.41 && macro > -0.15",
        "macro < -0.20",
        "plasma < 0.30",
        "HEX_SIZE * 0.72",
        "surfaceY - 10",
        "BlockTags.BASE_STONE_OVERWORLD",
        "BlockTags.DIRT",
        "Blocks.GRAVEL",
        "state.hasBlockEntity()",
        "state.getFluidState().isEmpty()",
    ):
        require_text(feature, needle, failures, "HexCaveFeature.java")

    for needle in (
        '"the_wasteland_reworked"',
        '"wastelands"',
        "GenerationStep.Decoration.UNDERGROUND_DECORATION",
        'PlacedFeature.CODEC.fieldOf("feature")',
    ):
        require_text(modifier, needle, failures, "WastelandNamespaceBiomeModifier.java")

    for needle in (
        'FEATURES.register("hex_caves"',
        '"wasteland_namespace"',
        "BIOME_MODIFIER_SERIALIZERS",
    ):
        require_text(main, needle, failures, "WastelandHexCaves.java")

    json_contracts = {
        resources / "data" / "infinite_domain_wasteland_hex_caves" / "worldgen" / "configured_feature" / "hex_caves.json": {
            "type": "infinite_domain_wasteland_hex_caves:hex_caves",
            "config": {},
        },
        resources / "data" / "infinite_domain_wasteland_hex_caves" / "worldgen" / "placed_feature" / "hex_caves.json": {
            "feature": "infinite_domain_wasteland_hex_caves:hex_caves",
            "placement": [],
        },
        resources / "data" / "infinite_domain_wasteland_hex_caves" / "neoforge" / "biome_modifier" / "add_hex_caves.json": {
            "type": "infinite_domain_wasteland_hex_caves:wasteland_namespace",
            "feature": "infinite_domain_wasteland_hex_caves:hex_caves",
        },
    }

    for path, expected in json_contracts.items():
        if not path.is_file():
            failures.append(f"missing JSON resource: {path.relative_to(root)}")
            continue
        try:
            observed = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            failures.append(f"{path.relative_to(root)}: invalid JSON: {exc}")
            continue
        if observed != expected:
            failures.append(
                f"{path.relative_to(root)}: resource contract mismatch; expected {expected!r}, got {observed!r}"
            )

    metrics = reference_metrics()
    for name, (minimum, maximum) in EXPECTED_RANGES.items():
        value = metrics[name]
        if not minimum <= value <= maximum:
            failures.append(
                f"{name}: {value:.3f}% outside expected range {minimum:.1f}-{maximum:.1f}%"
            )

    return failures


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    failures = validate_repository(root)
    metrics = reference_metrics()

    print("Wasteland hex-cave static/reference validation")
    print(f"seed={REFERENCE_SEED} domain=512x512 step={REFERENCE_STEP}")
    print(f"raw literal hex grid: {metrics['raw_hex_percent']:.1f}%")
    print(f"surviving visible grid: {metrics['visible_hex_percent']:.1f}%")
    print(f"occluded/interrupted grid: {metrics['occluded_hex_percent']:.1f}%")
    print(f"larger fractal chambers: {metrics['chamber_percent']:.1f}%")

    if failures:
        print("FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS")
    return 0
=======
import re
import sys
import zipfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "datapacks/gradient_ocean_pack/data/custom_worldgen/worldgen"
DENSITY = PACK / "density_function"
NOISE = PACK / "noise"
SETTINGS = ROOT / "kubejs/data/wastelands/worldgen/noise_settings/wasteland.json"
JAR = ROOT / "mods/infinite-domain-overworld-terrain-1.0.0.jar"
REPORT = ROOT / "docs/wasteland-hex-cave-validation.json"
FORBIDDEN_GATE = re.compile(
    r"quest|ftbquests|player|team|advancement|scoreboard|game_?stage|gamestage",
    re.IGNORECASE,
)


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def nearest_cell(x: float, z: float, radius: float) -> tuple[int, int]:
    q = (2.0 / 3.0 * x) / radius
    r = (-x / 3.0 + math.sqrt(3.0) / 3.0 * z) / radius
    cube_x, cube_z = q, r
    cube_y = -cube_x - cube_z
    rx, ry, rz = round(cube_x), round(cube_y), round(cube_z)
    dx, dy, dz = abs(rx - cube_x), abs(ry - cube_y), abs(rz - cube_z)
    if dx > dy and dx > dz:
        rx = -ry - rz
    elif dy > dz:
        ry = -rx - rz
    else:
        rz = -rx - ry
    return rx, rz


def signed_hex(x: float, z: float, radius: float) -> float:
    normal_x = math.sqrt(3.0) * 0.5
    return max(abs(x) * normal_x + abs(z) * 0.5, abs(z)) - radius * normal_x


def sample(params: dict[str, Any], x: int, y: int, z: int) -> float:
    if (
        y < params["min_y"]
        or y > params["max_y"]
        or math.hypot(x, z) < params["origin_exclusion_radius"]
    ):
        return 1.0
    radius = params["cell_radius"]
    q, r = nearest_cell(x, z, radius)
    cx = radius * 1.5 * q
    cz = radius * math.sqrt(3.0) * (r + q * 0.5)
    local_x, local_z = x - cx, z - cz
    edge = -signed_hex(local_x, local_z, radius) - params["corridor_half_width"]
    chamber = signed_hex(local_x, local_z, params["chamber_radius"])
    horizontal = min(edge, chamber)
    layer = round((y - params["layer_offset"]) / params["layer_spacing"])
    center_y = params["layer_offset"] + layer * params["layer_spacing"]
    vertical = abs(y - center_y) - params["layer_half_height"]
    return max(-1.0, min(1.0, max(horizontal, vertical) / params["feather"]))


def main() -> int:
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

    geometry = load(DENSITY / "wasteland_hex_geometry.json")
    caves = load(DENSITY / "wasteland_hex_caves.json")
    barrier = load(DENSITY / "wasteland_hex_plasma_barrier.json")
    noise = load(NOISE / "wasteland_hex_plasma.json")
    settings = load(SETTINGS)

    expected_geometry = {
        "type": "infinite_domain_worldgen:hex_grid_cave",
        "cell_radius": 48.0,
        "corridor_half_width": 4.0,
        "chamber_radius": 12.0,
        "layer_spacing": 44,
        "layer_offset": -40,
        "layer_half_height": 5.0,
        "min_y": -48,
        "max_y": 58,
        "origin_exclusion_radius": 288.0,
        "feather": 4.0,
    }
    record(
        "WHC-1",
        "the custom codec has one exact bounded geometry contract",
        geometry == expected_geometry,
        "48-block cells carry 8-block corridors, 24-block chambers, three 11-block-high strata, and a 288-block protected origin",
        geometry,
    )

    final_density = settings.get("noise_router", {}).get("final_density", {})
    base_density = final_density.get("argument1", {}) if isinstance(final_density, dict) else {}
    integration_ok = (
        final_density.get("type") == "minecraft:min"
        and final_density.get("argument2") == "custom_worldgen:wasteland_hex_caves"
        and base_density.get("type") == "minecraft:min"
        and base_density.get("argument2") == "minecraft:overworld/caves/noodle"
    )
    record(
        "WHC-2",
        "the canonical Wastelands final-density router consumes the cave field",
        integration_ok,
        "the new field wraps, rather than replaces, the prior terrain and vanilla cave/noodle density graph",
    )

    land_gate_ok = (
        caves.get("type") == "minecraft:range_choice"
        and caves.get("input") == "custom_worldgen:continents"
        and caves.get("min_inclusive") == -0.19
        and caves.get("max_exclusive") == 1.21
        and caves.get("when_out_of_range") == 1.0
        and caves.get("when_in_range") == {
            "type": "minecraft:max",
            "argument1": "custom_worldgen:wasteland_hex_geometry",
            "argument2": "custom_worldgen:wasteland_hex_plasma_barrier",
        }
    )
    record(
        "WHC-3",
        "hex caves carve land without cutting the Abyssal oceans",
        land_gate_ok,
        "continentalness -0.19..1.21 owns the carve; ocean values resolve to positive solid-preserving density",
        caves,
    )

    noise_node = barrier.get("argument", {}).get("input", {}).get("argument2", {})
    plasma_ok = (
        noise.get("firstOctave") == -7
        and noise.get("amplitudes") == [1.0, 0.55, 0.3, 0.15]
        and barrier.get("type") == "minecraft:cache_once"
        and barrier.get("argument", {}).get("type") == "minecraft:clamp"
        and barrier.get("argument", {}).get("input", {}).get("argument1") == -0.58
        and noise_node == {
            "type": "minecraft:noise",
            "noise": "custom_worldgen:wasteland_hex_plasma",
            "xz_scale": 0.018,
            "y_scale": 0.055,
        }
    )
    record(
        "WHC-4",
        "world-seeded multi-octave plasma selectively occludes the literal grid",
        plasma_ok,
        "four NormalNoise octaves close only high positive lobes while lower values preserve or narrow the authored corridors",
        {"noise": noise, "barrier": barrier},
    )

    # Probe one exact remote axial cell (q=14,r=-7) and all six neighbours.
    radius = geometry["cell_radius"]
    origin_q, origin_r = 14, -7

    def center(q: int, r: int) -> tuple[float, float]:
        return radius * 1.5 * q, radius * math.sqrt(3.0) * (r + q * 0.5)

    origin_x, origin_z = center(origin_q, origin_r)
    directions = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]
    center_samples: list[float] = []
    edge_samples: list[float] = []
    wall_samples: list[float] = []
    for dq, dr in [(0, 0), *directions]:
        x, z = center(origin_q + dq, origin_r + dr)
        center_samples.append(sample(geometry, round(x), 4, round(z)))
    for dq, dr in directions:
        x, z = center(origin_q + dq, origin_r + dr)
        edge_samples.append(sample(geometry, round((origin_x + x) * 0.5), 4, round((origin_z + z) * 0.5)))
        wall_samples.append(sample(geometry, round(origin_x + (x - origin_x) * 0.28), 4, round(origin_z + (z - origin_z) * 0.28)))
    topology_ok = (
        all(value < 0.0 for value in center_samples)
        and all(value < 0.0 for value in edge_samples)
        and all(value > 0.0 for value in wall_samples)
    )
    record(
        "WHC-5",
        "sampled geometry contains literal chambers, six-sided corridors, and intervening walls",
        topology_ok,
        "seven adjacent chamber centers and all six shared edges carve while six chamber-to-edge wall samples remain solid",
        {"centers": center_samples, "shared_edges": edge_samples, "walls": wall_samples},
    )

    layer_samples = {
        str(y): sample(geometry, round(origin_x), y, round(origin_z))
        for y in (-48, -45, -40, -35, -18, -1, 4, 9, 26, 43, 48, 53, 58, 59)
    }
    layers_ok = (
        all(layer_samples[str(y)] <= 0.0 for y in (-45, -40, -35, -1, 4, 9, 43, 48, 53))
        and all(layer_samples[str(y)] > 0.0 for y in (-48, -18, 26, 58, 59))
        and sample(geometry, 0, 4, 0) == 1.0
    )
    record(
        "WHC-6",
        "three cave strata and the spawn-hospital exclusion remain bounded",
        layers_ok,
        "carve bands center at Y -40, 4, and 48; rock separates them; the field is inert above Y58 and within radius 288",
        layer_samples,
    )

    required_entries = {
        "META-INF/neoforge.mods.toml",
        "infinitedomain/worldgen/InfiniteDomainWorldgen.class",
        "infinitedomain/worldgen/density/OverworldDensityFunctions.class",
        "infinitedomain/worldgen/density/HexGridCaveGeometry.class",
        "infinitedomain/worldgen/density/WastelandHexGridCave.class",
    }
    jar_evidence: dict[str, Any]
    jar_ok = False
    try:
        with zipfile.ZipFile(JAR) as archive:
            entries = set(archive.namelist())
            manifest = archive.read("META-INF/neoforge.mods.toml").decode("utf-8")
        missing = sorted(required_entries - entries)
        jar_ok = not missing and 'modId = "infinite_domain_worldgen"' in manifest and 'version = "1.0.0"' in manifest
        jar_evidence = {"path": JAR.relative_to(ROOT).as_posix(), "missing_entries": missing}
    except (OSError, KeyError, zipfile.BadZipFile) as exc:
        jar_evidence = {"error": str(exc)}
    record(
        "WHC-7",
        "the installed project-owned companion supplies the registered codec",
        jar_ok,
        "the installed JAR has the NeoForge mod entry point, registry class, geometry, and density-function implementation",
        jar_evidence,
    )

    owned_paths = [
        DENSITY / "wasteland_hex_geometry.json",
        DENSITY / "wasteland_hex_plasma_barrier.json",
        DENSITY / "wasteland_hex_caves.json",
        NOISE / "wasteland_hex_plasma.json",
        SETTINGS,
    ]
    gated = [path.relative_to(ROOT).as_posix() for path in owned_paths if FORBIDDEN_GATE.search(path.read_text(encoding="utf-8"))]
    record(
        "WHC-8",
        "cave generation is worldgen-owned and multiplayer-safe",
        not gated,
        "no quest, player, team, advancement, scoreboard, or game-stage token participates in the terrain graph",
        {"gated_paths": gated},
    )

    report = {
        "purpose": "Static and geometric proof for Infinite Domain's visible, fractally occluded Wasteland hex-grid cave system.",
        "checks": checks,
        "passed": not failures,
        "runtime_validation": "This gate proves codec packaging, graph reachability, exact geometry, land/spawn bounds, and multiplayer ownership. A fresh-world visual and performance pass remains required.",
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
    for check in checks:
        print(f"{'PASS' if check['passed'] else 'FAIL'}  {check['id']:<6} {check['check']}")
        print(f"               {check['detail']}")
    print()
    print(f"{len(checks) - len(failures)}/{len(checks)} checks passed")
    print(f"report: {REPORT.relative_to(ROOT).as_posix()}")
    return 1 if failures else 0
>>>>>>> Stashed changes:scripts/validate_wasteland_hex_caves.py


if __name__ == "__main__":
    sys.exit(main())
