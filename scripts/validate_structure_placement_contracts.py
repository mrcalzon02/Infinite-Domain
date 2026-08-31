from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "structure_library" / "catalog.json"
MANIFEST = ROOT / "docs" / "wasteland-site-manifest.json"
REPORT = ROOT / "docs" / "structure-placement-contract-validation.json"
SETS = ROOT / "kubejs" / "data" / "infinite_domain" / "worldgen" / "structure_set" / "wasteland"
STRUCTURES = ROOT / "kubejs" / "data" / "infinite_domain" / "worldgen" / "structure" / "wasteland"
POOLS = ROOT / "kubejs" / "data" / "infinite_domain" / "worldgen" / "template_pool" / "wasteland"

DIRECTIONS = ("north", "east", "south", "west")
VALID_ROADS = {"none", "pedestrian", "driveway", "local_road", "main_road", "highway", "rail_siding"}
EXPECTED_OFFSETS = {
    "ruined_gas_station": -7,
    "buried_bank_vault": -7,
    "bunker_network": -17,
    "survivor_cache": -9,
    "abandoned_quarry": -12,
    "collapsed_mine_entrance": -8,
    "excavator_pit": -10,
}
# Surface buildings with a hollow sub-grade room: they seat negative but must NOT
# beard, or beard_box carves the whole bounding box into an open scoop instead of
# leaving the room buried (docs/TERRAIN_AFFORDANCE_AND_SPAWN_SEPARATION.md A6/OD-2).
NO_BEARD_BURIED_ROOM = {"ruined_gas_station", "buried_bank_vault"}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def rotate(direction: str, quarter_turns: int) -> str:
    return DIRECTIONS[(DIRECTIONS.index(direction) + quarter_turns) % 4]


def main() -> None:
    manifest = load(MANIFEST)
    catalog = {
        record["structure_id"].split(":", 1)[1]: record
        for record in load(CATALOG)["structures"]
        if record.get("source_role") == "damage_variant"
        and "/structure/wasteland/" in record.get("source_template", "").replace("\\", "/")
    }
    failures = []
    membership = defaultdict(list)
    family_records = {}
    for family, metadata in manifest["families"].items():
        structure_set = load(SETS / f"{family}.json")
        expected = set(metadata["members"])
        actual = {entry["structure"].rsplit("/", 1)[1] for entry in structure_set["structures"]}
        issues = []
        if expected != actual:
            issues.append("structure-set members disagree with manifest family")
        placement = structure_set["placement"]
        if placement.get("type") != "minecraft:random_spread":
            issues.append("unsupported structure-set placement type")
        if placement.get("spacing") != metadata["spacing_chunks"] or placement.get("separation") != metadata["separation_chunks"]:
            issues.append("structure-set spacing disagrees with manifest")
        if placement.get("spacing", 0) <= placement.get("separation", 0):
            issues.append("spacing must exceed separation")
        for name in expected:
            membership[name].append(family)
        failures.extend(f"{family}: {issue}" for issue in issues)
        family_records[family] = {"members": sorted(actual), "issues": issues}

    structure_records = {}
    for name, record in catalog.items():
        issues = []
        if len(membership[name]) != 1:
            issues.append(f"belongs to {len(membership[name])} structure-set families")
        if record.get("road_connection") not in VALID_ROADS:
            issues.append("unknown road connector class")
        entrance = record.get("main_entrance")
        secondary = record.get("secondary_entrances", [])
        if entrance not in DIRECTIONS or any(direction not in DIRECTIONS for direction in secondary):
            issues.append("non-cardinal entrance metadata")
        width, depth = record["footprint"]["width"], record["footprint"]["depth"]
        lot_width, lot_depth = record["minimum_lot"]["width"], record["minimum_lot"]["depth"]
        if lot_width < width or lot_depth < depth:
            issues.append("minimum lot is smaller than canonical footprint")
        rotations = []
        if entrance in DIRECTIONS:
            for turns in range(4):
                rotated_width, rotated_depth = (width, depth) if turns % 2 == 0 else (depth, width)
                rotated_lot_width, rotated_lot_depth = (lot_width, lot_depth) if turns % 2 == 0 else (lot_depth, lot_width)
                if rotated_lot_width < rotated_width or rotated_lot_depth < rotated_depth:
                    issues.append(f"rotation {turns * 90} exceeds rotated lot")
                rotations.append({
                    "degrees": turns * 90,
                    "footprint": [rotated_width, rotated_depth],
                    "lot": [rotated_lot_width, rotated_lot_depth],
                    "main_entrance": rotate(entrance, turns),
                    "secondary_entrances": [rotate(direction, turns) for direction in secondary],
                })

        worldgen = load(STRUCTURES / f"{name}.json")
        pool = load(POOLS / f"{name}.json")
        element = pool.get("elements", [{}])[0].get("element", {})
        if element.get("location") != f"infinite_domain:wasteland/{name}":
            issues.append("template pool location mismatch")
        adaptation = worldgen.get("terrain_adaptation")
        if name in NO_BEARD_BURIED_ROOM:
            if adaptation != "none":
                issues.append("buried-room site must use terrain_adaptation 'none' (beard_box scoops it out of the ground)")
        elif adaptation not in {"beard_box", "bury"}:
            issues.append("structure lacks supported terrain feathering mode")
        start_height = worldgen.get("start_height", {})
        if name in EXPECTED_OFFSETS and start_height.get("absolute") != EXPECTED_OFFSETS[name]:
            issues.append(f"expected projected terrain offset {EXPECTED_OFFSETS[name]}")
        if name in EXPECTED_OFFSETS and worldgen.get("project_start_to_heightmap") != "WORLD_SURFACE_WG":
            issues.append("surface-cut/buried entrance is not projected to world surface")
        failures.extend(f"{name}: {issue}" for issue in issues)
        structure_records[name] = {
            "family": membership[name][0] if len(membership[name]) == 1 else None,
            "road_connection": record.get("road_connection"),
            "rotations": rotations,
            "terrain_adaptation": worldgen.get("terrain_adaptation"),
            "start_height": start_height,
            "issues": issues,
        }

    report = {
        "scope": "Static four-way footprint/entrance, family selector and terrain-placement contracts.",
        "structures_checked": len(structure_records),
        "families_checked": len(family_records),
        "static_contracts_passed": not failures,
        "failures": failures,
        "runtime_rotation_status": "pending_in_game_blockstate_and_connector_walkthrough",
        "runtime_terrain_status": "pending_in_game_representative_biome_placement",
        "families": family_records,
        "structures": structure_records,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if failures:
        raise SystemExit("Structure placement contract validation failed:\n- " + "\n- ".join(failures))
    print(f"Validated four-way placement contracts for {len(structure_records)} structures across {len(family_records)} families")


if __name__ == "__main__":
    main()
