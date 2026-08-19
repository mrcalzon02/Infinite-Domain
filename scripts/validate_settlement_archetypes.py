from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "structure_library" / "catalog.json"
ARCHETYPES = ROOT / "structure_library" / "settlement-archetypes.json"
REPORT = ROOT / "docs" / "settlement-archetype-validation.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def eligible(record, definition) -> bool:
    return record["structure_id"] in definition.get("explicit_include", []) or (
        bool(set(record.get("settlement_types", [])) & set(definition["settlement_types"]))
        and record.get("category") in definition["categories"]
        and record.get("road_connection") in definition["road_connections"]
    )


def main() -> None:
    document = load(ARCHETYPES)
    records = [
        record for record in load(CATALOG)["structures"]
        if record.get("source_role") == "damage_variant" and record.get("conversion_target") != "scattered"
    ]
    failures = []
    results = {}
    memberships = {record["structure_id"]: [] for record in records}
    required = {
        "highway_service_cluster", "small_town", "industrial_district", "port_town",
        "rail_town", "suburb", "city_district",
    }
    if set(document["archetypes"]) != required:
        failures.append("archetype set must contain exactly the seven required settlement grammars")
    known_ids = set(memberships)
    for name, definition in document["archetypes"].items():
        unknown = sorted(set(definition.get("explicit_include", [])) - known_ids)
        if unknown:
            failures.append(f"{name}: explicit members are unknown: {', '.join(unknown)}")
        members = sorted(record["structure_id"] for record in records if eligible(record, definition))
        for structure_id in members:
            memberships[structure_id].append(name)
        if len(members) < 2:
            failures.append(f"{name}: fewer than two candidate structures")
        road_classes = sorted({record["road_connection"] for record in records if record["structure_id"] in members})
        results[name] = {
            "candidate_count": len(members),
            "candidate_members": members,
            "road_connector_classes": road_classes,
            "lostcities_citystyle": definition["lostcities_citystyle"],
            "production_activation": "approval_compiler",
        }
    unassigned = sorted(structure_id for structure_id, groups in memberships.items() if not groups)
    if unassigned:
        failures.append("candidate structures without any archetype: " + ", ".join(unassigned))
    report = {
        "scope": "Seven settlement grammars with catalog-driven candidate zoning and approval-gated Lost Cities compilation.",
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
