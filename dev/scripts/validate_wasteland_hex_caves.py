#!/usr/bin/env python3
"""Static/reference validator for Infinite Domain's wasteland hex-cave source module."""

from __future__ import annotations

import json
import math
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


if __name__ == "__main__":
    sys.exit(main())
