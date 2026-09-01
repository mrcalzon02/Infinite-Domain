from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "dev/structure_library" / "catalog.json"
ARCHETYPES = ROOT / "dev/structure_library" / "settlement-archetypes.json"
REPORT = ROOT / "dev/docs" / "settlement-archetype-validation.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def record_culture(record) -> str:
    source = record.get("source_template", "").replace("\\", "/")
    marker = "/structure/"
    if marker not in source:
        return "unknown"
    return source.split(marker, 1)[1].split("/", 1)[0]


def eligible(record, definition) -> bool:
    if record_culture(record) != definition.get("culture", "wasteland"):
        return False
    return record["structure_id"] in definition.get("explicit_include", []) or (
        bool(set(record.get("settlement_types", [])) & set(definition["settlement_types"]))
        and record.get("category") in definition["categories"]
        and record.get("road_connection") in definition["road_connections"]
    )


def main() -> None:
    document = load(ARCHETYPES)
    records = []
    for record in load(CATALOG)["structures"]:
        if record.get("source_role") != "damage_variant" or record.get("conversion_target") == "scattered":
            continue
        culture = record_culture(record)
        if culture == "wasteland" or record.get("placement_owner") == f"{culture}_citystyle":
            records.append(record)
    failures = []
    results = {}
    memberships = {record["structure_id"]: [] for record in records}
    required_central = {
        "highway_service_cluster", "small_town", "industrial_district", "port_town",
        "rail_town", "suburb", "city_district",
    }
    actual_central = {
        name for name, definition in document["archetypes"].items()
        if definition.get("culture", "wasteland") == "wasteland"
    }
    if actual_central != required_central:
        failures.append("central archetype set must contain exactly the seven required settlement grammars")
    if "karsic_mikrorayon" not in document["archetypes"]:
        failures.append("the approved Karsic panel slab requires a mikrorayon archetype")
    known_ids = set(memberships)
    for name, definition in document["archetypes"].items():
        unknown = sorted(set(definition.get("explicit_include", [])) - known_ids)
        if unknown:
            failures.append(f"{name}: explicit members are unknown: {', '.join(unknown)}")
        selection_factors = definition.get("selection_factors", {})
        unknown_factors = sorted(set(selection_factors) - known_ids)
        invalid_factors = sorted(
            structure_id for structure_id, factor in selection_factors.items()
            if not isinstance(factor, (int, float)) or factor <= 0
        )
        if unknown_factors:
            failures.append(f"{name}: selection factors name unknown members: {', '.join(unknown_factors)}")
        if invalid_factors:
            failures.append(f"{name}: selection factors must be positive numbers: {', '.join(invalid_factors)}")
        members = sorted(record["structure_id"] for record in records if eligible(record, definition))
        for structure_id in members:
            memberships[structure_id].append(name)
        culture = definition.get("culture", "wasteland")
        minimum_candidates = 2 if culture == "wasteland" else 1
        if len(members) < minimum_candidates:
            failures.append(f"{name}: fewer than {minimum_candidates} candidate structures")
        road_classes = sorted({record["road_connection"] for record in records if record["structure_id"] in members})
        results[name] = {
            "candidate_count": len(members),
            "candidate_members": members,
            "road_connector_classes": road_classes,
            "lostcities_citystyle": definition["lostcities_citystyle"],
            "culture": culture,
            "selection_factors": selection_factors,
            "production_activation": "approval_compiler",
        }
    unassigned = sorted(structure_id for structure_id, groups in memberships.items() if not groups)
    if unassigned:
        failures.append("candidate structures without any archetype: " + ", ".join(unassigned))
    report = {
        "scope": "Culture-aware settlement grammars with catalog-driven zoning and approval-gated Lost Cities compilation.",
        "archetypes_checked": len(results),
        "candidate_structures_checked": len(records),
        "all_candidates_zoned": not unassigned,
        "static_wiring_passed": not failures,
        "production_admission": "evidence_backed_approvals_only",
        "runtime_generation_status": "pending_after_first_approved_representative_set",
        "failures": failures,
        "archetypes": results,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if failures:
        raise SystemExit("Settlement archetype validation failed:\n- " + "\n- ".join(failures))
    print(f"Validated {len(results)} settlement archetypes and zoned all {len(records)} candidate structures")


if __name__ == "__main__":
    main()
