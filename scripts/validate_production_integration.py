from __future__ import annotations

import json
from pathlib import Path

import generate_wasteland_sites as g

ROOT = Path(__file__).resolve().parents[1]
APPROVALS = ROOT / "structure_library" / "production-approvals.json"
CATALOG = ROOT / "structure_library" / "catalog.json"
ARCHETYPES = ROOT / "structure_library" / "settlement-archetypes.json"
COMPILATION = ROOT / "docs" / "production-pool-compilation.json"
REPORT = ROOT / "docs" / "production-integration-validation.json"
CITYSTYLE = ROOT / "kubejs" / "data" / "infinite_domain" / "lostcities" / "citystyles" / "wasteland.json"
WORLDSTYLE = ROOT / "kubejs" / "data" / "lostcities" / "lostcities" / "worldstyles" / "standard.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    approval_document = load(APPROVALS)
    catalog = load(CATALOG)
    archetypes = load(ARCHETYPES)
    compilation = load(COMPILATION)
    catalog_by_id = {record["structure_id"]: record for record in catalog["structures"]}
    approved = {f"infinite_domain:{name}" for name in g.QUALITY_APPROVED_FOR_PRODUCTION}
    failures = []
    records = {}
    for name in g.BUILDERS:
        structure_id = f"infinite_domain:{name}"
        worldgen_path = ROOT / "kubejs" / "data" / "infinite_domain" / "worldgen" / "structure" / "wasteland" / f"{name}.json"
        worldgen = load(worldgen_path)
        catalog_record = catalog_by_id.get(structure_id)
        is_approved = structure_id in approved
        # Vanilla jigsaw worldgen placement (this file) is intentionally not
        # gated by production-approvals.json: every structure below keeps
        # spawning regardless of lint status. Only the Lost Cities
        # multibuilding/scattered selectors compiled by
        # compile_production_structure_pools.py are approval-gated (checked
        # below). Pulling unapproved structures out of vanilla worldgen too
        # is a deliberate follow-up decision, not implied by removing the
        # human-review requirement.
        disabled = worldgen.get("biomes") == "#infinite_domain:disabled_primitive_wasteland_settlements"
        issues = []
        if catalog_record is None:
            issues.append("missing catalog record")
        elif catalog_record.get("production_status") != ("approved" if is_approved else "quarantined"):
            issues.append("catalog production status disagrees with approval manifest")
        records[structure_id] = {"approved": is_approved, "worldgen_quarantined": disabled, "issues": issues}
        failures.extend(f"{structure_id}: {issue}" for issue in issues)
    approved_names = {structure_id.split(":", 1)[1] for structure_id in approved}
    expected_multi = {
        f"infinite_domain:converted/{name}"
        for name in approved_names
        if catalog_by_id[f"infinite_domain:{name}"]["conversion_target"] != "scattered"
    }
    expected_scattered = {
        f"infinite_domain:converted/{name}"
        for name in approved_names
        if catalog_by_id[f"infinite_domain:{name}"]["conversion_target"] == "scattered"
    }
    citystyle = load(CITYSTYLE)
    actual_multi = set()
    active_archetypes = set()
    for archetype, result in compilation.get("archetypes", {}).items():
        if not result.get("active"):
            continue
        active_archetypes.add(archetype)
        path = CITYSTYLE.parent / f"wasteland_{archetype}.json"
        style = load(path)
        actual_multi.update(entry["value"] for entry in style.get("selectors", {}).get("multibuildings", []))
    worldstyle = load(WORLDSTYLE)
    actual_scattered = {entry["name"] for entry in worldstyle.get("scattered", {}).get("list", [])}
    if actual_multi != expected_multi:
        failures.append("zoned Lost Cities multibuilding selectors disagree with evidence-backed approvals")
    if actual_scattered != expected_scattered:
        failures.append("Lost Cities scattered pool disagrees with evidence-backed approvals")
    if not expected_scattered and worldstyle.get("scattered", {}).get("chance") != 0.0:
        failures.append("Lost Cities scattered chance must be zero when no scattered structure is approved")
    expected_styles = {
        archetypes["archetypes"][name]["lostcities_citystyle"] for name in active_archetypes
    } or {"infinite_domain:wasteland"}
    actual_styles = {entry["citystyle"] for entry in worldstyle.get("citystyles", [])}
    if actual_styles != expected_styles:
        failures.append("Lost Cities worldstyle archetype selectors disagree with compiled active archetypes")
    report = {
        "required_checks": approval_document["required_checks"],
        "structures_checked": len(records),
        "production_approvals": len(approved),
        "all_gates_enforced": not failures,
        "failures": failures,
        "lostcities_multibuildings": len(actual_multi),
        "lostcities_scattered": len(actual_scattered),
        "active_settlement_archetypes": sorted(active_archetypes),
        "structures": records,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if failures:
        raise SystemExit("Production integration validation failed:\n- " + "\n- ".join(failures))
    print(f"Validated production quarantine for {len(records)} structures; {len(approved)} evidence-backed approvals")


if __name__ == "__main__":
    main()
