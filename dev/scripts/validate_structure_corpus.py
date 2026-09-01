from __future__ import annotations

import gzip
import json
import re
from pathlib import Path
from typing import Any

from build_structure_qa_world import NbtList, Reader


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "structure_library" / "catalog.json"
APPROVALS = ROOT / "structure_library" / "production-approvals.json"
REPORT = ROOT / "docs" / "structure-corpus-validation.json"
RESOURCE_ID = re.compile(r"^[a-z0-9_.-]+:[a-z0-9_./-]+$")
CATEGORIES = {"residential", "commercial", "civic", "industrial", "agricultural", "highway", "railway", "utility_infrastructure", "military", "miscellaneous"}
ORIENTATIONS = {"north", "south", "east", "west"}
ROAD_CONNECTIONS = {"none", "pedestrian", "driveway", "local_road", "main_road", "highway", "rail_siding"}
SETTLEMENT_TYPES = {"highway_frontage", "town_center", "residential", "industrial", "railway", "rural", "military"}
INTENSITIES = {"repair", "light", "standard", "heavy", "rebuild"}
TARGETS = {"part", "building", "multibuilding", "scattered"}


def nbt_size(path: Path) -> tuple[int, int, int]:
    _, root = Reader(gzip.decompress(path.read_bytes())).root()
    size = root.value.get("size")
    if size is None or not isinstance(size.value, NbtList) or len(size.value.values) != 3:
        raise ValueError("missing three-value NBT size")
    return tuple(int(value.value) for value in size.value.values)  # type: ignore[return-value]


def require(entry: dict[str, Any], name: str, expected: type, issues: list[str]) -> Any:
    value = entry.get(name)
    if not isinstance(value, expected):
        issues.append(f"{name}: expected {expected.__name__}")
    return value


def validate_entry(entry: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    structure_id = require(entry, "structure_id", str, issues)
    if isinstance(structure_id, str) and not RESOURCE_ID.fullmatch(structure_id):
        issues.append("structure_id: invalid resource location")
    if entry.get("category") not in CATEGORIES:
        issues.append("category: invalid value")
    if entry.get("main_entrance") not in ORIENTATIONS:
        issues.append("main_entrance: invalid orientation")
    secondary = require(entry, "secondary_entrances", list, issues)
    if isinstance(secondary, list) and any(side not in ORIENTATIONS for side in secondary):
        issues.append("secondary_entrances: invalid orientation")
    if entry.get("road_connection") not in ROAD_CONNECTIONS:
        issues.append("road_connection: invalid value")
    if entry.get("refinement_intensity") not in INTENSITIES:
        issues.append("refinement_intensity: invalid value")
    if entry.get("conversion_target") not in TARGETS:
        issues.append("conversion_target: invalid value")
    settlement_types = require(entry, "settlement_types", list, issues)
    if isinstance(settlement_types, list) and (not settlement_types or any(value not in SETTLEMENT_TYPES for value in settlement_types)):
        issues.append("settlement_types: empty or invalid")
    for flag in ("supports_intact", "supports_damage_variants", "supports_occupation_variants"):
        require(entry, flag, bool, issues)
    for box_name in ("footprint", "minimum_lot"):
        box = require(entry, box_name, dict, issues)
        if isinstance(box, dict) and (not isinstance(box.get("width"), int) or not isinstance(box.get("depth"), int) or box.get("width", 0) < 1 or box.get("depth", 0) < 1):
            issues.append(f"{box_name}: width/depth must be positive integers")
    height = require(entry, "height", int, issues)
    source = require(entry, "source_template", str, issues)
    license_data = require(entry, "source_license", dict, issues)
    if isinstance(license_data, dict) and not all(key in license_data for key in ("origin", "license", "redistributable")):
        issues.append("source_license: missing provenance field")
    if isinstance(source, str):
        path = (ROOT / source).resolve()
        try:
            path.relative_to(ROOT.resolve())
        except ValueError:
            issues.append("source_template: escapes project root")
        else:
            if not path.is_file():
                issues.append("source_template: file not found")
            else:
                try:
                    width, actual_height, depth = nbt_size(path)
                    footprint = entry.get("footprint", {})
                    if (footprint.get("width"), footprint.get("depth"), height) != (width, depth, actual_height):
                        issues.append(f"declared dimensions do not match NBT {width}x{actual_height}x{depth}")
                except (OSError, EOFError, KeyError, ValueError) as error:
                    issues.append(f"source_template: unreadable NBT ({error})")
    return issues


def main() -> None:
    document = json.loads(CATALOG.read_text(encoding="utf-8"))
    structures = document.get("structures", [])
    approvals = json.loads(APPROVALS.read_text(encoding="utf-8")).get("approvals", [])
    approved_ids = {entry.get("structure_id") for entry in approvals}
    results: dict[str, Any] = {}
    seen: set[str] = set()
    for index, entry in enumerate(structures):
        structure_id = entry.get("structure_id", f"entry_{index}") if isinstance(entry, dict) else f"entry_{index}"
        issues = validate_entry(entry) if isinstance(entry, dict) else ["entry is not an object"]
        if structure_id in seen:
            issues.append("duplicate structure_id")
        seen.add(structure_id)
        results[structure_id] = {"metadata_valid": not issues, "issues": issues}
    catalog_by_id = {entry.get("structure_id"): entry for entry in structures}
    for structure_id in sorted(approved_ids):
        entry = catalog_by_id.get(structure_id)
        if entry is None:
            results[structure_id] = {
                "metadata_valid": False,
                "issues": ["production approval has no catalog record"],
            }
        elif entry.get("source_role") != "damage_variant" or entry.get("production_status") != "approved":
            results[structure_id]["metadata_valid"] = False
            results[structure_id]["issues"].append(
                "production approval requires an approved damage-variant catalog record"
            )
    report = {
        "purpose": "Corpus metadata and source-NBT dimension validation. This is not visual approval.",
        "structures_checked": len(structures),
        "valid": all(result["metadata_valid"] for result in results.values()),
        "production_approved": len(approved_ids),
        "structures": results,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
    if not report["valid"]:
        failures = [f"{name}: {', '.join(result['issues'])}" for name, result in results.items() if result["issues"]]
        raise SystemExit("\n".join(failures))
    print(
        f"Validated {len(structures)} corpus records against source NBT dimensions; "
        f"{len(approved_ids)} production approvals resolve to approved damage variants"
    )


if __name__ == "__main__":
    main()
