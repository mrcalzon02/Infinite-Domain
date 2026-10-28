"""Correlate retained runtime spawner-at-air errors without guessing an owner.

Source-template validity is historical evidence, not proof of which generator
placed a block entity in the live world. This audit deliberately makes no
runtime repairs and does not touch third-party resources or saved chunks.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_AUDIT = ROOT / "dev/docs/boot-dimension-audit"
POSITION = re.compile(r"BlockPos\{x=(-?\d+),\s*y=(-?\d+),\s*z=(-?\d+)\}")


def cluster_positions(records: list[dict]) -> list[dict]:
    """Group spatially adjacent failures; grouping is NOT structure attribution."""
    remaining = set(range(len(records)))
    groups = []
    while remaining:
        seed = min(remaining)
        remaining.remove(seed)
        component = {seed}
        queue = [seed]
        while queue:
            current = queue.pop()
            a = records[current]["position"]
            neighbors = [index for index in sorted(remaining)
                         if all(abs(a[axis] - records[index]["position"][axis]) <= 16
                                for axis in ("x", "y", "z"))]
            for index in neighbors:
                remaining.remove(index)
                component.add(index)
                queue.append(index)
        members = [records[index] for index in sorted(component)]
        groups.append({
            "positions": [item["position"] for item in members],
            "log_lines": [item["log_line"] for item in members],
            "bounds": {axis: [min(item["position"][axis] for item in members),
                              max(item["position"][axis] for item in members)]
                       for axis in ("x", "y", "z")},
            "chunks": sorted({(item["position"]["x"] // 16,
                               item["position"]["z"] // 16) for item in members}),
        })
    for group in groups:
        group["chunks"] = [list(chunk) for chunk in group["chunks"]]
    return groups


def analyze(rows: list[dict], inventory: dict, runtime: dict) -> dict:
    records = []
    for row in rows:
        if row.get("category") != "chunk_block_entity" or "minecraft:mob_spawner" not in row.get("message", ""):
            continue
        # The exception may be in detail, not the short ERROR message.
        match = POSITION.search(row.get("detail", "")) or POSITION.search(row.get("message", ""))
        if match is None:
            raise ValueError(f"spawner error at log line {row.get('line', '?')} has no position")
        if "minecraft:air" not in row.get("detail", "") + row.get("message", ""):
            raise ValueError(f"spawner error at log line {row.get('line', '?')} lacks air-state evidence")
        records.append({"log_line": int(row["line"]),
                        "position": dict(zip(("x", "y", "z"), map(int, match.groups())))})
    if not records:
        raise ValueError("no positioned spawner-at-air errors: cannot make a provenance report")
    if inventory.get("failures") is None or inventory.get("spawner_payloads") is None:
        raise ValueError("source-template inventory is incomplete")
    tiles = runtime.get("tiles")
    if not isinstance(tiles, list) or not tiles:
        raise ValueError("runtime tile evidence is incomplete")
    starts = sum(int(tile.get("validStructureStarts", 0)) for tile in tiles)
    failures = inventory["failures"]
    return {
        "source": "retained boot-dimension revision-4 errors.csv and result.json; revision-2 source-template inventory",
        "runtime_spawner_at_air_errors": len(records),
        "positions": records,
        "proximity_groups_not_structure_ids": cluster_positions(records),
        "historical_first_party_template_spawner_payloads": inventory["spawner_payloads"],
        "historical_first_party_template_mismatches": len(failures),
        "sampled_valid_natural_structure_starts": starts,
        "attribution": "unresolved",
        "historical_source_inventory_has_findings": bool(failures),
        "next_evidence": [
            "capture fresh-world block state and block-entity NBT at each exact position before reload",
            "record the structure/piece or feature ID and data-pack owner during placement",
            "re-run the authored NBT scanner against current sources and test transformed/chunk-clipped placements",
        ],
        "limitations": (
            "Spatial proximity is not a structure identifier. A clean authored-template scan "
            "does not rule out upstream structures, Lost Cities palettes, later block replacement, "
            "chunk clipping, or stale saved NBT. Zero starts in the four sampled benchmark tiles "
            "does not identify the generator responsible for errors logged during world preparation. "
            "This report does not demonstrate an error-free server or repair the seven failures."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--errors", type=Path, default=DEFAULT_AUDIT / "revision-4/errors.csv")
    parser.add_argument("--inventory", type=Path, default=DEFAULT_AUDIT / "revision-2/spawner-payload-inventory.json")
    parser.add_argument("--runtime", type=Path, default=DEFAULT_AUDIT / "revision-4/result.json")
    parser.add_argument("--out", type=Path, default=DEFAULT_AUDIT / "revision-4/spawner-runtime-provenance.json")
    args = parser.parse_args()
    with args.errors.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    report = analyze(rows, json.loads(args.inventory.read_text(encoding="utf-8")),
                     json.loads(args.runtime.read_text(encoding="utf-8")))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Spawner-at-air errors: {report['runtime_spawner_at_air_errors']}; "
          f"spatial groups: {len(report['proximity_groups_not_structure_ids'])}; "
          f"source ownership: {report['attribution']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
