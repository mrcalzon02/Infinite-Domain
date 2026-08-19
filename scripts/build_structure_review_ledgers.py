from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "structure_library" / "review"
CATALOG = ROOT / "structure_library" / "catalog.json"
ROAD_CATALOG = ROOT / "structure_library" / "roads" / "road-modules.json"
MODULE_CATALOG = ROOT / "structure_library" / "modules" / "structure-kits.json"

LEDGERS = {
    "building-production-review.csv": {
        "id_field": "asset_id",
        "checks": [
            "player_scale_walkthrough",
            "rotation_and_connectors",
            "terrain_placement_and_feathering",
            "runtime_lostcities_codec",
        ],
    },
    "road-production-review.csv": {
        "id_field": "asset_id",
        "checks": [
            "player_and_vehicle_scale_walkthrough",
            "adjacent_connector_alignment",
            "four_way_rotation",
            "ramp_and_bridge_elevation",
            "representative_terrain_placement",
        ],
    },
    "module-production-review.csv": {
        "id_field": "asset_id",
        "checks": [
            "visual_module_boundary_review",
            "connector_and_rotation_test",
            "assembly_with_adjacent_modules",
            "terrain_and_coastline_placement",
        ],
    },
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def existing_rows(path: Path, id_field: str):
    if not path.exists():
        return {}
    with path.open(encoding="utf-8", newline="") as handle:
        return {row[id_field]: row for row in csv.DictReader(handle)}


def write_ledger(filename: str, asset_ids: list[str]) -> None:
    definition = LEDGERS[filename]
    id_field = definition["id_field"]
    checks = definition["checks"]
    path = REVIEW / filename
    old = existing_rows(path, id_field)
    fields = [id_field, *checks, "reviewer", "reviewed_at", "notes"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for asset_id in asset_ids:
            prior = old.get(asset_id, {})
            writer.writerow({
                id_field: asset_id,
                **{check: prior.get(check, "pending") for check in checks},
                "reviewer": prior.get("reviewer", ""),
                "reviewed_at": prior.get("reviewed_at", ""),
                "notes": prior.get("notes", ""),
            })


def main() -> None:
    REVIEW.mkdir(parents=True, exist_ok=True)
    buildings = [
        record["structure_id"] for record in load(CATALOG)["structures"]
        if record.get("source_role") == "damage_variant"
    ]
    roads = [record["module_id"] for record in load(ROAD_CATALOG)["modules"]]
    modules = [record["module_id"] for record in load(MODULE_CATALOG)["modules"]]
    write_ledger("building-production-review.csv", buildings)
    write_ledger("road-production-review.csv", roads)
    write_ledger("module-production-review.csv", modules)
    print(f"Prepared resumable review ledgers for {len(buildings)} buildings, {len(roads)} roads and {len(modules)} structure modules")


if __name__ == "__main__":
    main()
