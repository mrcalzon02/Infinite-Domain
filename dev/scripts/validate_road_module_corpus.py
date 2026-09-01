from __future__ import annotations

import json
import hashlib
from collections import defaultdict, deque
from pathlib import Path

from convert_nbt_to_lostcities import load_structure
from generate_wasteland_sites import STRUCTURE_BLOCK_REPLACEMENTS

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "structure_library" / "roads" / "road-modules.json"
REPORT = ROOT / "docs" / "road-module-validation.json"

REQUIRED_TOPOLOGIES = {
    "straight", "bend", "t", "four_way", "roundabout", "dead_end",
    "driveway", "alley", "highway", "ramp", "bridge_approach",
}
REQUIRED_CONDITIONS = {"clean", "cracked", "buried", "cratered", "overgrown", "flooded", "burned"}
DIRECTIONS = ("north", "east", "south", "west")
ROAD_SURFACES = {
    "minecraft:black_concrete", "minecraft:yellow_concrete", "minecraft:cracked_deepslate_tiles",
    "minecraft:polished_deepslate", "minecraft:moss_block", "minecraft:blackstone",
    "minecraft:cobbled_deepslate",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def base_name(state: str) -> str:
    return state.split("[", 1)[0]


def rotate(direction: str, turns: int) -> str:
    return DIRECTIONS[(DIRECTIONS.index(direction) + turns) % 4]


def drivable(blocks):
    cells = {}
    for (x, y, z), (state, _tag) in blocks.items():
        if base_name(state) in ROAD_SURFACES and (x, z) not in cells or (
            base_name(state) in ROAD_SURFACES and y > cells[(x, z)]
        ):
            cells[(x, z)] = y
    return cells


def connector_cells(record, direction: str):
    size_x, _size_y, size_z = record["size"]
    center_x, center_z = size_x // 2, size_z // 2
    width = next(item["width"] for item in record["connectors"] if item["direction"] == direction)
    half = width // 2
    if direction == "north":
        return [(x, 0) for x in range(center_x - half, center_x + half + 1)]
    if direction == "south":
        return [(x, size_z - 1) for x in range(center_x - half, center_x + half + 1)]
    if direction == "west":
        return [(0, z) for z in range(center_z - half, center_z + half + 1)]
    return [(size_x - 1, z) for z in range(center_z - half, center_z + half + 1)]


def reachable(cells, start, targets) -> bool:
    queue = deque([start])
    seen = {start}
    while queue:
        x, z = queue.popleft()
        if (x, z) in targets:
            return True
        y = cells[(x, z)]
        for neighbor in ((x - 1, z), (x + 1, z), (x, z - 1), (x, z + 1)):
            if neighbor in cells and neighbor not in seen and abs(cells[neighbor] - y) <= 1:
                seen.add(neighbor)
                queue.append(neighbor)
    return False


def boundary_signature(blocks, size):
    sx, _sy, sz = size
    return sorted(
        (pos, state, tag) for pos, (state, tag) in blocks.items()
        if pos[0] < 4 or pos[2] < 4 or pos[0] >= sx - 4 or pos[2] >= sz - 4
    )


def main() -> None:
    document = load(CATALOG)
    failures = []
    records = document["modules"]
    families = defaultdict(list)
    if document.get("production_approvals"):
        failures.append("road corpus must remain quarantined until runtime review")
    if len(document.get("required_approval_checks", [])) != 5:
        failures.append("road production approval contract is incomplete")
    if {record["topology"] for record in records} != REQUIRED_TOPOLOGIES:
        failures.append("road corpus does not cover the required topology set")
    for record in records:
        families[record["architecture_family"]].append(record)
    family_results = {}
    for family, members in sorted(families.items()):
        issues = []
        conditions = {record["condition"] for record in members}
        if conditions != REQUIRED_CONDITIONS or len(members) != len(REQUIRED_CONDITIONS):
            issues.append("condition set is incomplete or duplicated")
        clean = next((record for record in members if record["condition"] == "clean"), None)
        if not clean:
            issues.append("clean topology master is missing")
            continue
        clean_size, clean_blocks = load_structure(ROOT / clean["source_template"])
        clean_signature = boundary_signature(clean_blocks, clean_size)
        clean_contract = {
            key: clean[key] for key in (
                "road_class", "topology", "size", "width", "length", "lane_count",
                "median", "sidewalk", "connectors", "rotation_support",
            )
        }
        variants = {}
        for record in members:
            size, blocks = load_structure(ROOT / record["source_template"])
            variant_issues = []
            source_path = ROOT / record["source_template"]
            if hashlib.sha256(source_path.read_bytes()).hexdigest() != record.get("source_sha256"):
                variant_issues.append("source NBT hash disagrees with catalog provenance")
            if not record.get("source_license") or record.get("source_provenance") != "scripts/generate_road_module_corpus.py":
                variant_issues.append("source license/provenance is incomplete")
            contract = {key: record[key] for key in clean_contract}
            if contract != clean_contract:
                variant_issues.append("condition variant changed topology metadata")
            if size != tuple(record["size"]):
                variant_issues.append("NBT dimensions disagree with catalog")
            if boundary_signature(blocks, size) != clean_signature:
                variant_issues.append("condition variant changed the four-block connector boundary band")
            palette = {base_name(state) for state, _tag in blocks.values()}
            prohibited = sorted(palette & set(STRUCTURE_BLOCK_REPLACEMENTS))
            if prohibited:
                variant_issues.append("prohibited structure blocks: " + ", ".join(prohibited))
            cells = drivable(blocks)
            connectors = [entry["direction"] for entry in record["connectors"]]
            endpoints = {}
            for entry in record["connectors"]:
                edge = connector_cells(record, entry["direction"])
                expected_y = 1 + entry["elevation"]
                present = [cell for cell in edge if cells.get(cell) == expected_y]
                if len(present) != entry["width"]:
                    variant_issues.append(f"{entry['direction']} connector geometry/elevation mismatch")
                elif present:
                    endpoints[entry["direction"]] = present[len(present) // 2]
            if len(endpoints) == len(connectors) and len(connectors) > 1:
                origin = endpoints[connectors[0]]
                for direction in connectors[1:]:
                    if not reachable(cells, origin, set(connector_cells(record, direction))):
                        variant_issues.append(f"no traversable road path from {connectors[0]} to {direction}")
            if record["condition"] != "clean" and blocks == clean_blocks:
                variant_issues.append("condition variant is geometrically identical to clean")
            rotations = []
            for turns in range(4):
                rotations.append({
                    "degrees": turns * 90,
                    "connectors": [
                        {
                            "direction": rotate(entry["direction"], turns),
                            "width": entry["width"],
                            "elevation": entry["elevation"],
                        }
                        for entry in record["connectors"]
                    ],
                })
            variants[record["condition"]] = {
                "placed_blocks": len(blocks),
                "drivable_cells": len(cells),
                "rotations": rotations,
                "issues": variant_issues,
            }
            issues.extend(f"{record['condition']}: {issue}" for issue in variant_issues)
        failures.extend(f"{family}: {issue}" for issue in issues)
        family_results[family] = {
            "topology": clean["topology"],
            "road_class": clean["road_class"],
            "connectors": clean["connectors"],
            "issues": issues,
            "variants": variants,
        }
    report = {
        "scope": "NBT-backed road topology, connector boundary, four-way rotation, elevation and condition-invariance validation.",
        "families_checked": len(families),
        "modules_checked": len(records),
        "topologies": sorted({record["topology"] for record in records}),
        "conditions": sorted({record["condition"] for record in records}),
        "static_road_contracts_passed": not failures,
        "production_approvals": len(document.get("production_approvals", [])),
        "runtime_status": "pending_in_game_adjacency_rotation_elevation_and_vehicle_walkthrough",
        "failures": failures,
        "families": family_results,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if failures:
        raise SystemExit("Road-module validation failed:\n- " + "\n- ".join(failures))
    print(f"Validated {len(records)} NBT road modules across {len(families)} topology families; all connector graphs and condition boundaries pass")


if __name__ == "__main__":
    main()
