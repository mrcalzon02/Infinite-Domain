#!/usr/bin/env python3
"""Prove the central-continent interior loses its mountain band, and only there.

`custom_worldgen:central_interior_mask` is a radial plateau -- 1 out to radius
4650, feathering to 0 by radius 4750 -- multiplied by `1 - mountain_ring_mask`.
The gradient pack's `minecraft:overworld/erosion` override lerps between the
vanilla erosion noise and `max(erosion, -0.5)` using that mask, so that:

  * inside the central continent, outside the guaranteed mountain ring, the
    erosion parameter can never fall into the `wastelands:mountains` band
    (`erosion [-1.0, -0.55]` in the Wastelands world preset), so the interior
    fills with the other temperate wasteland biomes instead of mountains;
  * the mountain ring annulus (radius 3200-3900) keeps the untouched erosion
    noise, so its guaranteed `wastelands:mountains` routing is preserved;
  * a thin residual mountain band may survive in the 100-block mask feather
    (radius ~4650-4750), where the central continent has already blended almost
    entirely to open ocean -- far outside the ring and the playable interior;
  * outside radius 4750 the mask is exactly 0, so erosion is bit-identical to
    vanilla and the outer directional continents keep their mountains.

Why this matters beyond biome flavour: Lost Cities' pack worldstyle
(`kubejs/data/lostcities/lostcities/worldstyles/standard.json`) gives every
biome in `#infinite_domain:lostcities_city_excluded` -- which contains
`wastelands:mountains` -- a city-chance multiplier of 0.0. A mountain-dominated
central continent therefore suppresses city generation near spawn entirely.
Removing interior mountains restores it.

This script does not take that on trust. It parses the density-function JSON
graph, evaluates the erosion override, and reports exactly where the effective
erosion differs from vanilla.

Authority: docs/GRADIENT_OCEAN_PACK_VALIDATION.md

Usage:
    python scripts/validate_central_interior_mask.py
    python scripts/validate_central_interior_mask.py --json
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

from validate_regional_culture_gradient import Graph, make_noise

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "datapacks" / "gradient_ocean_pack" / "data"
DF_DIR = PACK / "custom_worldgen" / "worldgen" / "density_function"
EROSION_OVERRIDE = PACK / "minecraft" / "worldgen" / "density_function" / "overworld" / "erosion.json"
REPORT = ROOT / "docs" / "central-interior-mask-validation.json"

NAMESPACE = "custom_worldgen"

# Mountain routing band from the Wastelands world preset temperate land rules:
#   {"biome": "wastelands:mountains", "temperature": [-0.99, 0.99], "erosion": [-1.0, -0.55]}
MOUNTAIN_EROSION_MAX = -0.55

RING_INNER_R = 3200.0
RING_OUTER_R = 3900.0
MASK_PLATEAU_R = 4650.0   # central_interior_mask == 1 at or inside this radius
MASK_EDGE_R = 4750.0      # central_interior_mask == 0 at or outside this radius

# Noise samples that bracket any real erosion sample. The override is a lerp of
# monotone terms, so testing the extremes and the mountain-band edge is enough.
NOISE_SAMPLES = (-1.0, -0.9, -0.7, -0.55, -0.3, 0.0, 0.5, 1.0)


def _unwrap(node: Any) -> Any:
    """Strip the vanilla per-column cache wrappers the override shares with vanilla."""
    while isinstance(node, dict) and node.get("type") in ("minecraft:flat_cache", "minecraft:cache_2d", "minecraft:cache_once"):
        node = node["argument"]
    return node


def sample_points() -> list[tuple[float, float]]:
    points: list[tuple[float, float]] = []
    radii = (0, 500, 1500, 2500, 3000, 3199, 3200, 3550, 3899, 3900, 3950,
             4000, 4200, 4400, 4600, 4649, 4650, 4700, 4749, 4750, 4800, 5200, 6000, 9000, 16000)
    for r in radii:
        for deg in range(0, 360, 15):
            rad = math.radians(deg)
            points.append((r * math.cos(rad), r * math.sin(rad)))
    return points


def run_checks(graph: Graph, override: Any) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    checks: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []

    def record(check_id: str, name: str, ok: bool, detail: str, evidence: Any = None) -> None:
        entry = {"id": check_id, "check": name, "passed": ok, "detail": detail}
        if evidence is not None:
            entry["evidence"] = evidence
        checks.append(entry)
        if not ok:
            failures.append(entry)

    mask = f"{NAMESPACE}:central_interior_mask"
    base = f"{NAMESPACE}:base_erosion"
    ring = f"{NAMESPACE}:mountain_ring_mask"
    body = _unwrap(override)

    # --- CIM-1: files exist ----------------------------------------------------
    record("CIM-1a", "central_interior_mask is defined",
           mask in graph.nodes, f"{mask} present in {DF_DIR.relative_to(ROOT).as_posix()}")
    record("CIM-1b", "base_erosion is defined",
           base in graph.nodes, f"{base} present in {DF_DIR.relative_to(ROOT).as_posix()}")
    record("CIM-1c", "the vanilla overworld/erosion override exists",
           EROSION_OVERRIDE.exists(), EROSION_OVERRIDE.relative_to(ROOT).as_posix())

    # --- CIM-2: reference graph ---------------------------------------------
    refs: set[str] = set()

    def walk(node: Any) -> None:
        if isinstance(node, str) and node.startswith(NAMESPACE + ":"):
            refs.add(node)
        elif isinstance(node, dict):
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    walk(override)
    record("CIM-2a", "the erosion override consumes only central_interior_mask and base_erosion",
           refs == {mask, base}, f"custom_worldgen references in the override: {sorted(refs)}", sorted(refs))
    record("CIM-2b", "central_interior_mask is a radial plateau gated by the mountain ring",
           graph.references(mask) == {ring},
           f"references of {mask}: {sorted(graph.references(mask))} (plus an inline radial distance feather)",
           sorted(graph.references(mask)))

    # --- CIM-3/4/5: pointwise erosion behaviour ---------------------------------
    interior_band_hits: list[dict[str, Any]] = []
    feather_mountain_radii: list[float] = []
    ring_drift: list[dict[str, Any]] = []
    outer_drift: list[dict[str, Any]] = []
    changed: list[dict[str, Any]] = []
    max_changed_r = 0.0

    # From the lerp `base + m*(max(base,-0.5) - base)`, the worst case base = -1
    # leaves the mountain band (`erosion <= -0.55`) impossible once m > 0.9.
    FULL_SUPPRESSION_MASK = 0.9

    for nv in NOISE_SAMPLES:
        noise = make_noise(nv)
        for x, z in sample_points():
            r = math.hypot(x, z)
            eff = graph.evaluate(body, x, 0.0, z, noise)
            m = graph.evaluate(mask, x, 0.0, z, noise)
            probe = {"x": round(x, 1), "z": round(z, 1), "r": round(r, 1),
                     "noise": nv, "erosion": round(eff, 4), "base": nv, "mask": round(m, 4)}

            if eff != nv:
                changed.append(probe)
                max_changed_r = max(max_changed_r, r)

            # Wherever the interior mask is essentially saturated the mountain
            # erosion band must be unreachable for any bracketing noise sample.
            if m > FULL_SUPPRESSION_MASK and eff <= MOUNTAIN_EROSION_MAX:
                interior_band_hits.append(probe)

            # Where a residual mountain routing survives it must be only in the
            # outer feather, never in the playable interior or near the ring.
            if 0.0 < m <= FULL_SUPPRESSION_MASK and eff <= MOUNTAIN_EROSION_MAX:
                feather_mountain_radii.append(r)

            # Ring annulus: erosion is the untouched noise.
            if RING_INNER_R + 50 <= r <= RING_OUTER_R - 50 and abs(eff - nv) > 1e-12:
                ring_drift.append(probe)

            # Outer regime: bit-identical to vanilla.
            if r >= MASK_EDGE_R and abs(eff - nv) > 1e-12:
                outer_drift.append(probe)

    record("CIM-3", "wherever the interior mask is saturated the wastelands:mountains erosion band is unreachable",
           not interior_band_hits,
           f"effective erosion stays above {MOUNTAIN_EROSION_MAX} for every bracketing noise sample "
           f"wherever central_interior_mask > {FULL_SUPPRESSION_MASK}",
           interior_band_hits[:5])
    min_feather_r = min(feather_mountain_radii) if feather_mountain_radii else None
    record("CIM-3b", "any residual mountain routing is confined to the outer shoreline feather",
           min_feather_r is None or min_feather_r >= MASK_PLATEAU_R,
           "in the 100-block mask feather the lerp can still admit occasional mountains right at the "
           "central shoreline, where the continent has already blended almost entirely to ocean; this "
           "check proves none survive inside the ring, the guaranteed-land radius, or the playable interior. "
           f"nearest residual mountain radius: {round(min_feather_r, 1) if min_feather_r else 'none'} "
           f"(plateau ends at {MASK_PLATEAU_R:.0f})",
           {"nearest_residual_mountain_radius": round(min_feather_r, 1) if min_feather_r else None})
    record("CIM-4", "mountain ring annulus (3250-3850) keeps the untouched erosion noise",
           not ring_drift,
           "central_interior_mask is 0 across the ring, so its guaranteed wastelands:mountains routing is preserved",
           ring_drift[:5])
    record("CIM-5", "no-op outside the central continent (r >= 4750)",
           not outer_drift,
           "erosion is bit-identical to vanilla, so the outer directional continents keep their mountains "
           "and the abyssal ocean program is unaffected",
           outer_drift[:5])
    record("CIM-6", "the change is confined to the central continent and its feather",
           max_changed_r < MASK_EDGE_R,
           f"effective erosion differs from vanilla at {len(changed)} sampled probes, "
           f"none at or beyond r = {MASK_EDGE_R:.0f} (max changed r = {max_changed_r:.1f})",
           {"changed_probe_count": len(changed), "max_changed_radius": round(max_changed_r, 1)})

    # --- CIM-7: the ring mask itself is unchanged -----------------------------
    noise = make_noise(0.0)
    r_in = graph.evaluate(graph.nodes[ring], 3500.0, 0.0, 0.0, noise)
    r_out = graph.evaluate(graph.nodes[ring], 5000.0, 0.0, 0.0, noise)
    r_core = graph.evaluate(graph.nodes[ring], 1000.0, 0.0, 0.0, noise)
    record("CIM-7", "mountain_ring_mask still steps 0 -> 1 -> 0 across the annulus",
           abs(r_core) < 1e-9 and abs(r_in - 1.0) < 1e-9 and abs(r_out) < 1e-9,
           f"mountain_ring_mask at r=1000/3500/5000 = {r_core}/{r_in}/{r_out}")

    # --- CIM-8: unmodelled references ----------------------------------------
    record("CIM-8", "every referenced function is modelled or is a known noise source",
           all(name.startswith("minecraft:") for name in graph.external),
           f"external references treated as noise: {sorted(graph.external) or 'none'}",
           sorted(graph.external))

    return checks, failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--json", action="store_true", help="print the full report to stdout")
    args = parser.parse_args()

    graph = Graph(DF_DIR)
    override = json.loads(EROSION_OVERRIDE.read_text(encoding="utf-8"))
    checks, failures = run_checks(graph, override)

    report = {
        "purpose": "Static proof that the central-continent interior loses the wastelands:mountains "
                   "erosion band while the mountain ring and everything beyond radius 4750 are untouched.",
        "authority": ["docs/GRADIENT_OCEAN_PACK_VALIDATION.md"],
        "source": {
            "masks": DF_DIR.relative_to(ROOT).as_posix(),
            "override": EROSION_OVERRIDE.relative_to(ROOT).as_posix(),
        },
        "mountain_erosion_band_max": MOUNTAIN_EROSION_MAX,
        "ring_radii": [RING_INNER_R, RING_OUTER_R],
        "mask_plateau_radius": MASK_PLATEAU_R,
        "mask_edge_radius": MASK_EDGE_R,
        "noise_samples": list(NOISE_SAMPLES),
        "probe_count": len(sample_points()),
        "checks": checks,
        "passed": not failures,
        "runtime_validation": "Static proof over the density-function graph. Actual in-world biome "
                              "placement, terrain height and Lost Cities city density remain unmeasured; "
                              "generate a fresh test world to confirm.",
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        for check in checks:
            print(f"{'PASS' if check['passed'] else 'FAIL'}  {check['id']:<7} {check['check']}")
            print(f"                {check['detail']}")
        print()
        print(f"{len(checks) - len(failures)}/{len(checks)} checks passed")
        print(f"report: {REPORT.relative_to(ROOT).as_posix()}")

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
