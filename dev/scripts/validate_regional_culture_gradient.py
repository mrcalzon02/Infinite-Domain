#!/usr/bin/env python3
"""Prove the regional culture gradient's no-op range from the actual datapack files.

`custom_worldgen:regional_culture_gradient` is the single worldgen change that
gives the Karsic (East) and Pelagos (West) surface regions somewhere to be. It
multiplies the existing `regional_east_west_gradient` by `1 - central_continent_mask`
so that:

  * inside the central continent the culture signal is neutralised, and the
    existing ungated land biome rules keep the centre exactly as it is;
  * outside radius 4800 the multiplier is exactly 1, so the function is
    bit-identical to the pre-change behaviour and the entire implemented
    abyssal ocean program is untouched;
  * between 4000 and 4800 the mask feathers, producing the graded cultural
    approach the narrative canon calls a "transition zone".

This script does not take that on trust. It parses the density-function JSON
graph, evaluates it, reconstructs the pre-change `city_humidity`, and reports
exactly where old and new differ.

Authority: docs/KARSIC_DIRECTORATE_STRUCTURE_PROGRAM.md section 12.2
           docs/PELAGOS_COMPACT_STRUCTURE_PROGRAM.md section 12.2

Usage:
    python scripts/validate_regional_culture_gradient.py
    python scripts/validate_regional_culture_gradient.py --json
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
DF_DIR = ROOT / "datapacks" / "gradient_ocean_pack" / "data" / "custom_worldgen" / "worldgen" / "density_function"
WORLD_PRESET = ROOT / "kubejs" / "data" / "minecraft" / "worldgen" / "world_preset" / "normal.json"
REPORT = ROOT / "docs" / "regional-culture-gradient-validation.json"

NAMESPACE = "custom_worldgen"

# The land lobes reach full strength once |x| - |z| >= 250 (east_west_continent_mask
# saturates) and the culture gradient saturates once |x| >= 500. Regional biome
# rules key on the humidity bands below, taken from the canonical normal preset.
WEST_BAND = (-1.0, -0.2)
EAST_BAND = (0.2, 1.0)

CENTRAL_CORE_R = 4000.0    # central_continent_mask == 1 at or inside this radius
CENTRAL_EDGE_R = 4800.0    # central_continent_mask == 0 at or outside this radius


# ---------------------------------------------------------------------------
# Density function evaluation
# ---------------------------------------------------------------------------

class Graph:
    """The custom_worldgen density-function graph, resolved by name."""

    def __init__(self, directory: Path):
        self.nodes: dict[str, Any] = {}
        for path in sorted(directory.glob("*.json")):
            self.nodes[f"{NAMESPACE}:{path.stem}"] = json.loads(path.read_text(encoding="utf-8"))
        self.external: set[str] = set()

    def references(self, name: str) -> set[str]:
        """Every custom_worldgen function referenced by `name`, one level deep."""
        found: set[str] = set()

        def walk(node: Any) -> None:
            if isinstance(node, str):
                if node.startswith(NAMESPACE + ":"):
                    found.add(node)
            elif isinstance(node, dict):
                for value in node.values():
                    walk(value)
            elif isinstance(node, list):
                for value in node:
                    walk(value)

        walk(self.nodes[name])
        return found

    def referrers(self, target: str) -> set[str]:
        """Every function that references `target`."""
        return {name for name in self.nodes if target in self.references(name)}

    def evaluate(self, node: Any, x: float, y: float, z: float, noise: Callable[[str, float, float, float], float]) -> float:
        if isinstance(node, (int, float)):
            return float(node)

        if isinstance(node, str):
            if node in self.nodes:
                return self.evaluate(self.nodes[node], x, y, z, noise)
            # A vanilla or mod-provided function we do not model; treated as the
            # noise provider's responsibility and recorded so it cannot hide.
            self.external.add(node)
            return noise(node, x, y, z)

        kind = node.get("type")
        ev = lambda k: self.evaluate(node[k], x, y, z, noise)  # noqa: E731

        if kind == "isekai_api:constant":
            return float(node["value"])
        if kind == "isekai_api:coordinate":
            return {"x": x, "y": y, "z": z}[node["axis"]]
        if kind == "isekai_api:add":
            return ev("a") + ev("b")
        if kind == "isekai_api:multiply":
            return ev("a") * ev("b")
        if kind == "isekai_api:negate":
            return -ev("f")
        if kind == "isekai_api:abs":
            return abs(ev("f"))
        if kind == "minecraft:abs":
            return abs(ev("argument"))
        if kind == "isekai_api:clamp":
            return min(max(ev("f"), float(node["min"])), float(node["max"]))
        if kind == "isekai_api:min":
            return min(ev("a"), ev("b"))
        if kind == "isekai_api:max":
            return max(ev("a"), ev("b"))
        if kind == "isekai_api:lerp":
            t, a, b = ev("t"), ev("a"), ev("b")
            return a + t * (b - a)
        if kind == "isekai_api:distance":
            rx, ry, rz = float(node.get("ref_x", 0.0)), float(node.get("ref_y", 0.0)), float(node.get("ref_z", 0.0))
            if node.get("mode") == "xz":
                return math.hypot(x - rx, z - rz)
            return math.sqrt((x - rx) ** 2 + (y - ry) ** 2 + (z - rz) ** 2)
        if kind == "isekai_api:step":
            value = ev("value")
            return ev("high") if value >= float(node["threshold"]) else ev("low")
        if kind in ("minecraft:cache_2d", "minecraft:flat_cache", "minecraft:cache_once"):
            # Cache markers are semantically transparent to this point evaluator.
            # Runtime Minecraft replaces them with chunk-local memoizing wrappers.
            return ev("argument")
        if kind in ("minecraft:shifted_noise", "minecraft:noise"):
            return noise(node["noise"], x, y, z)

        raise NotImplementedError(f"unhandled density function type: {kind}")


def make_noise(fixed: float) -> Callable[[str, float, float, float], float]:
    """A noise provider pinned to one value.

    Every noise term in this chain enters linearly (`x*0.002 + noise*0.35`)
    before a clamp, and the clamp is monotone, so evaluating at -1 and +1
    brackets the true value for any real noise sample in that range.
    """
    return lambda name, x, y, z: fixed


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def sample_points() -> list[tuple[float, float]]:
    """A grid covering the centre, the feather, both land lobes and both corridors."""
    points: list[tuple[float, float]] = []
    for r in (0, 500, 1500, 2500, 3500, 3999, 4000, 4200, 4400, 4600, 4799,
              4800, 5200, 6000, 8000, 12000, 20000):
        for deg in range(0, 360, 15):
            rad = math.radians(deg)
            points.append((r * math.cos(rad), r * math.sin(rad)))
    # Explicit axis and diagonal probes, including the value called out in the
    # planning documents as the reason the naive humidity gate fails.
    points += [(2000.0, 0.0), (-2000.0, 0.0), (0.0, 2000.0), (0.0, -2000.0),
               (6000.0, 0.0), (-6000.0, 0.0), (0.0, 6000.0), (0.0, -6000.0),
               (5000.0, 4000.0), (-5000.0, 4000.0), (4000.0, 5000.0), (4000.0, -5000.0)]
    return points


def run_checks(graph: Graph) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    checks: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []

    def record(check_id: str, name: str, ok: bool, detail: str, evidence: Any = None) -> None:
        entry = {"id": check_id, "check": name, "passed": ok, "detail": detail}
        if evidence is not None:
            entry["evidence"] = evidence
        checks.append(entry)
        if not ok:
            failures.append(entry)

    culture = f"{NAMESPACE}:regional_culture_gradient"
    base = f"{NAMESPACE}:regional_east_west_gradient"
    humidity = f"{NAMESPACE}:city_humidity"
    central = f"{NAMESPACE}:central_continent_mask"

    # --- RC-1: the function exists -----------------------------------------
    record("RC-1", "regional_culture_gradient is defined",
           culture in graph.nodes,
           f"{culture} present in {DF_DIR.relative_to(ROOT).as_posix()}")

    # --- RC-2: reference graph ---------------------------------------------
    referrers = graph.referrers(culture)
    record("RC-2a", "city_humidity references the culture gradient",
           humidity in referrers,
           f"referrers of {culture}: {sorted(referrers) or 'none'}",
           sorted(referrers))
    record("RC-2b", "the culture gradient is referenced by nothing else",
           referrers == {humidity},
           "must be exactly {city_humidity} so the change cannot leak into another chain",
           sorted(referrers))

    base_referrers = graph.referrers(base)
    record("RC-2c", "the old gradient now feeds only the culture gradient",
           base_referrers == {culture},
           f"referrers of {base}: {sorted(base_referrers) or 'none'}",
           sorted(base_referrers))

    # --- RC-3/4/5: pointwise behaviour, evaluated from the files ------------
    noop_violations: list[dict[str, Any]] = []
    centre_violations: list[dict[str, Any]] = []
    feather_violations: list[dict[str, Any]] = []
    corridor_violations: list[dict[str, Any]] = []
    east_violations: list[dict[str, Any]] = []
    west_violations: list[dict[str, Any]] = []

    for noise_value in (-1.0, -0.5, 0.0, 0.5, 1.0):
        noise = make_noise(noise_value)
        for x, z in sample_points():
            r = math.hypot(x, z)
            c = graph.evaluate(culture, x, 0.0, z, noise)
            b = graph.evaluate(base, x, 0.0, z, noise)
            mask = graph.evaluate(central, x, 0.0, z, noise)
            probe = {"x": round(x, 1), "z": round(z, 1), "r": round(r, 1),
                     "noise": noise_value, "culture": c, "base": b, "central_mask": mask}

            if r >= CENTRAL_EDGE_R:
                if c != b:
                    noop_violations.append(probe)
            if r <= CENTRAL_CORE_R:
                if c != 0.0:
                    centre_violations.append(probe)
            if CENTRAL_CORE_R < r < CENTRAL_EDGE_R:
                if abs(c) > abs(b) + 1e-12:
                    feather_violations.append(probe)

            # North/south ocean corridors: culture signal must stay at the seam.
            if abs(z) - abs(x) >= 250 and r >= CENTRAL_EDGE_R:
                if c != 0.0:
                    corridor_violations.append(probe)

            # Land lobes at full strength must land inside the regional bands
            # for every noise sample, not just the average one.
            if r >= CENTRAL_EDGE_R and abs(x) - abs(z) >= 250:
                if x > 0 and not (EAST_BAND[0] <= c <= EAST_BAND[1]):
                    east_violations.append(probe)
                if x < 0 and not (WEST_BAND[0] <= c <= WEST_BAND[1]):
                    west_violations.append(probe)

    record("RC-3", "no-op outside the central continent (r >= 4800)",
           not noop_violations,
           "culture gradient is bit-identical to the pre-change gradient, so the "
           "implemented abyssal ocean program is unaffected",
           noop_violations[:5])
    record("RC-4", "central continent neutralised (r <= 4000)",
           not centre_violations,
           "culture gradient is exactly 0, so the centre keeps the existing ungated land rules",
           centre_violations[:5])
    record("RC-5", "monotone feather between r = 4000 and r = 4800",
           not feather_violations,
           "|culture| never exceeds |base| inside the transition annulus",
           feather_violations[:5])
    record("RC-6", "north/south ocean corridors stay at the seam",
           not corridor_violations,
           "culture gradient is 0 where |z| - |x| >= 250, so the abyssal corridors keep vanilla routing",
           corridor_violations[:5])
    record("RC-7", "eastern lobe lands in the Karsic humidity band for all noise",
           not east_violations,
           f"culture gradient within {EAST_BAND} wherever x > 0 and |x| - |z| >= 250 beyond r = 4800",
           east_violations[:5])
    record("RC-8", "western lobe lands in the Pelagos humidity band for all noise",
           not west_violations,
           f"culture gradient within {WEST_BAND} wherever x < 0 and |x| - |z| >= 250 beyond r = 4800",
           west_violations[:5])

    # --- RC-9: what actually changed ---------------------------------------
    # Reconstruct the pre-change city_humidity by pointing it back at the old
    # gradient, then diff old against new across the whole sample grid.
    old_humidity = json.loads(json.dumps(graph.nodes[humidity]).replace(culture, base))
    changed: list[dict[str, Any]] = []
    unchanged_beyond_edge = True
    for noise_value in (-1.0, 0.0, 1.0):
        noise = make_noise(noise_value)
        for x, z in sample_points():
            r = math.hypot(x, z)
            new_v = graph.evaluate(graph.nodes[humidity], x, 0.0, z, noise)
            old_v = graph.evaluate(old_humidity, x, 0.0, z, noise)
            if new_v != old_v:
                changed.append({"x": round(x, 1), "z": round(z, 1), "r": round(r, 1),
                                "noise": noise_value, "old": old_v, "new": new_v})
                if r >= CENTRAL_EDGE_R:
                    unchanged_beyond_edge = False

    max_changed_r = max((c["r"] for c in changed), default=0.0)
    record("RC-9", "the change is confined to the central continent and its feather",
           unchanged_beyond_edge,
           f"city_humidity differs from its pre-change value at {len(changed)} sampled "
           f"probes, none beyond r = {CENTRAL_EDGE_R:.0f} (max changed r = {max_changed_r:.1f})",
           {"changed_probe_count": len(changed), "max_changed_radius": max_changed_r})

    # --- RC-10: the masks that must not move -------------------------------
    noise = make_noise(0.0)
    spawn = graph.evaluate(graph.nodes[humidity], 0.0, 0.0, 0.0, noise)
    ring = graph.evaluate(graph.nodes[humidity], 3500.0, 0.0, 0.0, noise)
    record("RC-10a", "start city still forces humidity 2.0",
           abs(spawn - 2.0) < 1e-9, f"city_humidity at origin = {spawn}", spawn)
    record("RC-10b", "mountain ring still forces humidity 1.25",
           abs(ring - 1.25) < 1e-9, f"city_humidity at r = 3500 = {ring}", ring)

    # --- RC-11: unmodelled references --------------------------------------
    record("RC-11", "every referenced function is modelled or is a known noise source",
           all(name.startswith("minecraft:") for name in graph.external),
           f"external references treated as noise: {sorted(graph.external) or 'none'}",
           sorted(graph.external))

    return checks, failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--json", action="store_true", help="print the report to stdout instead of a summary")
    args = parser.parse_args()

    graph = Graph(DF_DIR)
    checks, failures = run_checks(graph)

    report = {
        "purpose": "Static proof that custom_worldgen:regional_culture_gradient neutralises the "
                   "cultural East/West signal inside the central continent while remaining a "
                   "no-op outside radius 4800.",
        "authority": [
            "docs/KARSIC_DIRECTORATE_STRUCTURE_PROGRAM.md#12-placement-and-worldgen",
            "docs/PELAGOS_COMPACT_STRUCTURE_PROGRAM.md#12-placement-and-worldgen",
        ],
        "source": DF_DIR.relative_to(ROOT).as_posix(),
        "central_core_radius": CENTRAL_CORE_R,
        "central_edge_radius": CENTRAL_EDGE_R,
        "noise_samples": [-1.0, -0.5, 0.0, 0.5, 1.0],
        "probe_count": len(sample_points()),
        "checks": checks,
        "passed": not failures,
        "runtime_validation": "This is a static proof over the density-function graph. "
                              "Actual in-world biome placement, terrain height and chunk "
                              "generation cost remain unmeasured.",
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
