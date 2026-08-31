from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
from pathlib import Path
from typing import Any

PREFIX = "[ID-WORLDGEN-BENCH] "
ACCEPTANCE_MODS = ("lostcities", "dungeons_arise", "dungeons_arise_seven_seas")
ARISE_NAMESPACES = ("dungeons_arise", "dungeons_arise_seven_seas")


def percentile(values: list[float], quantile: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    rank = (len(ordered) - 1) * quantile
    lower = math.floor(rank)
    upper = math.ceil(rank)
    if lower == upper:
        return ordered[lower]
    return ordered[lower] * (upper - rank) + ordered[upper] * (rank - lower)


def read_markers(log_path: Path) -> list[dict[str, Any]]:
    markers: list[dict[str, Any]] = []
    for line_number, line in enumerate(log_path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        marker_at = line.find(PREFIX)
        if marker_at < 0:
            continue
        payload = line[marker_at + len(PREFIX) :].strip()
        try:
            event = json.loads(payload)
        except json.JSONDecodeError as error:
            raise ValueError(f"Malformed benchmark marker at {log_path}:{line_number}: {error}") from error
        event["_line"] = line_number
        markers.append(event)
    return markers


def summarize_acceptance(markers: list[dict[str, Any]], tiles: list[dict[str, Any]]) -> dict[str, Any]:
    mod_events = [event for event in markers if event.get("event") == "mod_snapshot"]
    registry_events = [event for event in markers if event.get("event") == "registry_namespace_snapshot"]
    probe_errors = [event for event in markers if event.get("event") == "acceptance_probe_error"]

    loaded_mods: dict[str, bool | None] = {mod_id: None for mod_id in ACCEPTANCE_MODS}
    if mod_events:
        loaded = mod_events[-1].get("loaded", {})
        for mod_id in ACCEPTANCE_MODS:
            if mod_id in loaded:
                loaded_mods[mod_id] = bool(loaded[mod_id])

    registries: dict[str, dict[str, Any]] = {}
    for namespace in ARISE_NAMESPACES:
        matching = [event for event in registry_events if event.get("namespace") == namespace]
        if not matching:
            registries[namespace] = {
                "structureCount": None,
                "structureSetCount": None,
                "structureSample": [],
                "structureSetSample": [],
            }
            continue
        event = matching[-1]
        registries[namespace] = {
            "structureCount": int(event.get("structureCount", 0)),
            "structureSetCount": int(event.get("structureSetCount", 0)),
            "structureSample": list(event.get("structureSample", [])),
            "structureSetSample": list(event.get("structureSetSample", [])),
        }

    starts_by_namespace: dict[str, int] = {}
    total_valid_starts = 0
    for tile in tiles:
        total_valid_starts += int(tile.get("validStructureStarts", 0))
        for namespace, count in dict(tile.get("structureStartsByNamespace", {})).items():
            starts_by_namespace[str(namespace)] = starts_by_namespace.get(str(namespace), 0) + int(count)

    arise: dict[str, dict[str, Any]] = {}
    for namespace in ARISE_NAMESPACES:
        registry = registries[namespace]
        structure_count = registry["structureCount"]
        structure_set_count = registry["structureSetCount"]
        observed_starts = starts_by_namespace.get(namespace, 0)
        arise[namespace] = {
            "modLoaded": loaded_mods.get(namespace),
            "structureCount": structure_count,
            "structureSetCount": structure_set_count,
            "observedNaturalStarts": observed_starts,
            "runtimeRegistryReady": (
                loaded_mods.get(namespace) is True
                and structure_count is not None
                and structure_count > 0
                and structure_set_count is not None
                and structure_set_count > 0
            ),
            "naturalGenerationObserved": observed_starts > 0,
            "structureSample": registry["structureSample"],
            "structureSetSample": registry["structureSetSample"],
        }

    lostcities_loaded = loaded_mods.get("lostcities")
    return {
        "probeErrors": probe_errors,
        "loadedMods": loaded_mods,
        "totalValidStructureStarts": total_valid_starts,
        "structureStartsByNamespace": dict(sorted(starts_by_namespace.items())),
        "arise": arise,
        "lostCities": {
            "modLoaded": lostcities_loaded,
            "freshWorldGenerated": bool(tiles),
            "runtimeLoadAccepted": lostcities_loaded is True and bool(tiles) and not probe_errors,
            "visualDistributionAccepted": False,
            "note": (
                "Headless evidence proves the mod loaded during fresh fixed-seed generation. "
                "It does not by itself approve Lost Cities skyline, rotation, terrain seating, or visual distribution."
            ),
        },
    }


def analyze(log_path: Path, manifest_path: Path) -> dict[str, Any]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    markers = read_markers(log_path)
    starts = [event for event in markers if event.get("event") == "benchmark_started"]
    failures = [event for event in markers if event.get("event") == "benchmark_failed"]
    completions = [event for event in markers if event.get("event") == "benchmark_completed"]
    tiles = [event for event in markers if event.get("event") == "tile_completed"]

    if len(starts) != 1:
        raise ValueError(f"Expected one benchmark_started marker, found {len(starts)}")
    start = starts[0]
    run_id = str(start["runId"])
    if run_id != str(manifest["runId"]):
        raise ValueError(f"Run ID mismatch: log={run_id}, manifest={manifest['runId']}")
    reported_seed = str(start["seed"])
    manifest_seed = str(manifest["seed"])
    seed_validation = "exact"
    if reported_seed != manifest_seed:
        try:
            precision_equivalent = float(reported_seed) == float(manifest_seed)
        except ValueError:
            precision_equivalent = False
        if not precision_equivalent:
            raise ValueError(f"Seed mismatch: log={reported_seed}, manifest={manifest_seed}")
        seed_validation = "rhino_double_equivalent"

    status = "failed" if failures else "complete" if len(completions) == 1 else "incomplete"
    elapsed_values = [float(tile["elapsedMs"]) for tile in tiles]
    result: dict[str, Any] = {
        "schemaVersion": 2,
        "status": status,
        "runId": run_id,
        "batchId": manifest["batchId"],
        "repetition": manifest["repetition"],
        "variant": str(start["variant"]),
        "suite": str(start["suite"]),
        "seed": manifest_seed,
        "reportedSeed": reported_seed,
        "seedValidation": seed_validation,
        "worldName": str(start["worldName"]),
        "configurationFingerprint": manifest["configurationFingerprint"],
        "plannedChunks": int(start["plannedChunks"]),
        "completedChunks": sum(int(tile["chunks"]) for tile in tiles),
        "tileCount": len(tiles),
        "tileP50Ms": round(percentile(elapsed_values, 0.50), 3),
        "tileP95Ms": round(percentile(elapsed_values, 0.95), 3),
        "tileMaxMs": max(elapsed_values, default=0),
        "tiles": tiles,
        "failure": failures[-1] if failures else None,
        "acceptance": summarize_acceptance(markers, tiles),
    }
    if completions:
        completion = completions[0]
        result.update(
            generationMs=int(completion["generationMs"]),
            wallClockMs=int(completion["wallClockMs"]),
            chunksPerSecond=round(float(completion["chunksPerSecond"]), 6),
        )
    else:
        generation_ms = int(sum(elapsed_values))
        result.update(
            generationMs=generation_ms,
            wallClockMs=None,
            chunksPerSecond=round(result["completedChunks"] * 1000 / generation_ms, 6) if generation_ms else 0,
        )
    return result


def validate_matrix(matrix_path: Path) -> None:
    matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    int(str(matrix["seed"]))
    if not matrix.get("worldName"):
        raise ValueError("worldName is required")
    if "baseline" not in matrix.get("variants", {}):
        raise ValueError("The benchmark matrix must define a baseline variant")
    for suite_name, tiles in matrix.get("suites", {}).items():
        if not tiles:
            raise ValueError(f"Suite {suite_name} has no tiles")
        occupied: set[tuple[str, int, int]] = set()
        for tile in tiles:
            width = int(tile["widthChunks"])
            depth = int(tile["depthChunks"])
            if width < 1 or depth < 1 or width * depth > 256:
                raise ValueError(f"Suite {suite_name}, tile {tile['name']} violates the 1..256 chunk limit")
            for x in range(int(tile["minChunkX"]), int(tile["minChunkX"]) + width):
                for z in range(int(tile["minChunkZ"]), int(tile["minChunkZ"]) + depth):
                    key = (str(tile["dimension"]), x, z)
                    if key in occupied:
                        raise ValueError(f"Suite {suite_name} contains overlapping tiles at {key}")
                    occupied.add(key)


def aggregate(root: Path, csv_path: Path, json_path: Path) -> dict[str, Any]:
    results = [json.loads(path.read_text(encoding="utf-8")) for path in root.rglob("result.json")]
    complete = [result for result in results if result.get("status") == "complete"]
    grouped: dict[tuple[str, str, str], list[dict[str, Any]]] = {}
    for result in complete:
        key = (str(result["suite"]), str(result["seed"]), str(result["variant"]))
        grouped.setdefault(key, []).append(result)

    rows: list[dict[str, Any]] = []
    baseline_rates: dict[tuple[str, str], float] = {}
    for (suite, seed, variant), group in sorted(grouped.items()):
        rates = [float(result["chunksPerSecond"]) for result in group]
        median_rate = statistics.median(rates)
        row = {
            "suite": suite,
            "seed": seed,
            "variant": variant,
            "runs": len(group),
            "medianChunksPerSecond": round(median_rate, 6),
            "minChunksPerSecond": round(min(rates), 6),
            "maxChunksPerSecond": round(max(rates), 6),
            "speedupVsBaseline": None,
        }
        rows.append(row)
        if variant == "baseline":
            baseline_rates[(suite, seed)] = median_rate

    for row in rows:
        baseline = baseline_rates.get((row["suite"], row["seed"]))
        if baseline and baseline > 0:
            row["speedupVsBaseline"] = round(row["medianChunksPerSecond"] / baseline, 4)

    csv_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "suite", "seed", "variant", "runs", "medianChunksPerSecond",
        "minChunksPerSecond", "maxChunksPerSecond", "speedupVsBaseline",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    summary = {
        "schemaVersion": 1,
        "root": str(root.resolve()),
        "resultsFound": len(results),
        "completeResults": len(complete),
        "groups": rows,
    }
    json_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze Infinite Domain fixed-seed worldgen benchmarks")
    subparsers = parser.add_subparsers(dest="command", required=True)
    analyze_parser = subparsers.add_parser("analyze")
    analyze_parser.add_argument("--log", type=Path, required=True)
    analyze_parser.add_argument("--manifest", type=Path, required=True)
    analyze_parser.add_argument("--output", type=Path, required=True)
    aggregate_parser = subparsers.add_parser("aggregate")
    aggregate_parser.add_argument("--root", type=Path, required=True)
    aggregate_parser.add_argument("--csv", type=Path, required=True)
    aggregate_parser.add_argument("--json", type=Path, required=True)
    validate_parser = subparsers.add_parser("validate-matrix")
    validate_parser.add_argument("--matrix", type=Path, required=True)

    args = parser.parse_args()
    if args.command == "analyze":
        result = analyze(args.log, args.manifest)
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(f"{result['runId']}: {result['status']}, {result['chunksPerSecond']:.3f} chunks/s")
        if result["status"] != "complete":
            raise SystemExit(1)
    elif args.command == "aggregate":
        summary = aggregate(args.root, args.csv, args.json)
        print(f"Aggregated {summary['completeResults']}/{summary['resultsFound']} complete benchmark result(s)")
    else:
        validate_matrix(args.matrix)
        print("Worldgen benchmark matrix is valid")


if __name__ == "__main__":
    main()
