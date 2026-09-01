from __future__ import annotations

import json
from pathlib import Path

import generate_wasteland_sites as g
from compile_production_structure_pools import partition_approvals

ROOT = Path(__file__).resolve().parents[2]
APPROVALS = ROOT / "dev/structure_library" / "production-approvals.json"
CATALOG = ROOT / "dev/structure_library" / "catalog.json"
ARCHETYPES = ROOT / "dev/structure_library" / "settlement-archetypes.json"
COMPILATION = ROOT / "dev/docs" / "production-pool-compilation.json"
REPORT = ROOT / "dev/docs" / "production-integration-validation.json"
CITYSTYLE = ROOT / "kubejs" / "data" / "infinite_domain" / "lostcities" / "citystyles" / "wasteland.json"
WORLDSTYLE = ROOT / "kubejs" / "data" / "lostcities" / "lostcities" / "worldstyles" / "standard.json"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def record_culture(record) -> str:
    source = record.get("source_template", "").replace("\\", "/")
    marker = "/structure/"
    if marker not in source:
        return "unknown"
    return source.split(marker, 1)[1].split("/", 1)[0]


def main() -> None:
    approval_document = load(APPROVALS)
    catalog = load(CATALOG)
    archetypes = load(ARCHETYPES)
    compilation = load(COMPILATION)
    catalog_by_id = {record["structure_id"]: record for record in catalog["structures"]}
    failures = []
    approval_ids = {
        entry["structure_id"] for entry in approval_document.get("approvals", [])
        if isinstance(entry, dict) and isinstance(entry.get("structure_id"), str)
    }
    approved_all = sorted(structure_id.split(":", 1)[1] for structure_id in approval_ids)
    damage_records = {
        record["structure_id"]: record for record in catalog["structures"]
        if record.get("source_role") == "damage_variant"
    }
    try:
        central_names, regional_names = partition_approvals(approved_all, damage_records)
    except ValueError as error:
        failures.append(str(error))
        central_names, regional_names = [], []
    approved = {f"infinite_domain:{name}" for name in central_names}
    regional_approved = {f"infinite_domain:{name}" for name in regional_names}
    generator_approved = {f"infinite_domain:{name}" for name in g.QUALITY_APPROVED_FOR_PRODUCTION}
    if generator_approved != approval_ids:
        failures.append("loaded generator approvals disagree with production-approvals.json")
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
    approved_names = set(central_names)
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
    actual_multi = set()
    actual_regional_multi = set()
    active_archetypes = set()
    active_regional_cultures = set()
    for archetype, result in compilation.get("archetypes", {}).items():
        if not result.get("active"):
            continue
        active_archetypes.add(archetype)
        culture = result.get("culture", "wasteland")
        path = ROOT / result.get(
            "citystyle_file",
            f"kubejs/data/infinite_domain/lostcities/citystyles/wasteland_{archetype}.json",
        )
        style = load(path)
        members = {
            entry["value"] for entry in style.get("selectors", {}).get("multibuildings", [])
        }
        if culture == "wasteland":
            actual_multi.update(members)
        else:
            active_regional_cultures.add(culture)
            actual_regional_multi.update(members)
    worldstyle = load(WORLDSTYLE)
    actual_scattered = {entry["name"] for entry in worldstyle.get("scattered", {}).get("list", [])}
    regional_resources = {f"infinite_domain:converted/{name}" for name in regional_names}
    regional_leaks = sorted(regional_resources & (actual_multi | actual_scattered))
    expected_regional_multi = {
        f"infinite_domain:converted/{name}"
        for name in regional_names
        if (
            catalog_by_id[f"infinite_domain:{name}"].get("conversion_target") != "scattered"
            and catalog_by_id[f"infinite_domain:{name}"].get("placement_owner")
            == f"{record_culture(catalog_by_id[f'infinite_domain:{name}'])}_citystyle"
        )
    }
    if actual_multi != expected_multi:
        failures.append("zoned Lost Cities multibuilding selectors disagree with evidence-backed approvals")
    if actual_regional_multi != expected_regional_multi:
        failures.append("regional Lost Cities selectors disagree with citystyle-owned approvals")
    if actual_scattered != expected_scattered:
        failures.append("Lost Cities scattered pool disagrees with evidence-backed approvals")
    if regional_leaks:
        failures.append("biome-owned regional approvals leaked into the global Wastelands selectors")
    if not expected_scattered and worldstyle.get("scattered", {}).get("chance") != 0.0:
        failures.append("Lost Cities scattered chance must be zero when no scattered structure is approved")
    expected_styles = {
        result["citystyle"]
        for result in compilation.get("archetypes", {}).values()
        if result.get("active")
    } or {"infinite_domain:wasteland"}
    worldstyle_selectors = {
        entry["citystyle"]: entry for entry in worldstyle.get("citystyles", [])
    }
    actual_styles = set(worldstyle_selectors)
    if actual_styles != expected_styles:
        failures.append("Lost Cities worldstyle archetype selectors disagree with compiled active archetypes")
    expected_exclusions = {
        f"#infinite_domain:{culture}_region_biomes" for culture in active_regional_cultures
    }
    for archetype in active_archetypes:
        result = compilation["archetypes"][archetype]
        selector = worldstyle_selectors.get(result["citystyle"], {})
        culture = result.get("culture", "wasteland")
        matcher = selector.get("biomes", {})
        if culture == "wasteland" and set(matcher.get("excluding", [])) != expected_exclusions:
            failures.append(f"{result['citystyle']}: central selector regional exclusions are stale")
        if culture != "wasteland" and matcher.get("if_any") != [f"#infinite_domain:{culture}_region_biomes"]:
            failures.append(f"{result['citystyle']}: regional selector lacks its culture biome matcher")

    expected_central_ids = {f"infinite_domain:{name}" for name in central_names}
    expected_regional_ids = {f"infinite_domain:{name}" for name in regional_names}
    if compilation.get("production_approvals") != len(approval_ids):
        failures.append("production compilation total approval count is stale")
    if compilation.get("central_wasteland_approvals") != len(expected_central_ids):
        failures.append("production compilation central approval count is stale")
    if set(compilation.get("approved_structure_ids", [])) != expected_central_ids:
        failures.append("production compilation central approval roster is stale")
    if set(compilation.get("regional_approvals", [])) != expected_regional_ids:
        failures.append("production compilation regional approval roster is stale")

    regional_records = {}
    for structure_id in sorted(regional_approved):
        name = structure_id.split(":", 1)[1]
        record = catalog_by_id.get(structure_id, {})
        culture = record_culture(record)
        worldgen_path = (
            ROOT / "kubejs" / "data" / "infinite_domain" / "worldgen" / "structure"
            / culture / f"{name}.json"
        )
        issues = []
        citystyle_owned = record.get("placement_owner") == f"{culture}_citystyle"
        citystyle_staged = citystyle_owned and record.get("worldgen_status") == "citystyle_staged"
        citystyle_active = citystyle_owned and record.get("worldgen_status") == "citystyle_active"
        if record.get("production_status") != "approved":
            issues.append("catalog production status is not approved")
        if not culture or culture == "wasteland":
            issues.append("regional source template has no non-central culture owner")
        resource = f"infinite_domain:converted/{name}"
        if citystyle_active:
            if worldgen_path.is_file():
                issues.append("citystyle-active asset unexpectedly has open-country worldgen registration")
            if resource not in actual_regional_multi:
                issues.append("citystyle-active asset is missing from its regional selector")
            biomes = f"#infinite_domain:{culture}_region_biomes"
        elif citystyle_staged:
            if worldgen_path.is_file():
                issues.append("citystyle-staged asset unexpectedly has open-country worldgen registration")
            biomes = None
        elif not worldgen_path.is_file():
            issues.append("biome-owned worldgen structure registration is missing")
            biomes = None
        else:
            biomes = load(worldgen_path).get("biomes")
            if biomes != f"#infinite_domain:{culture}_region_biomes":
                issues.append("worldgen registration does not use its culture-region biome tag")
        regional_records[structure_id] = {
            "culture": culture,
            "placement_owner": record.get("placement_owner", "datapack_worldgen"),
            "worldgen_status": record.get("worldgen_status", "active"),
            "worldgen_biomes": biomes,
            "global_selector_excluded": resource not in (actual_multi | actual_scattered),
            "regional_citystyle_selected": resource in actual_regional_multi,
            "issues": issues,
        }
        failures.extend(f"{structure_id}: {issue}" for issue in issues)

    report = {
        "required_checks": approval_document["required_checks"],
        "structures_checked": len(records),
        "production_approvals": len(approval_ids),
        "central_wasteland_approvals": len(approved),
        "regional_approvals": sorted(regional_approved),
        "all_gates_enforced": not failures,
        "failures": failures,
        "lostcities_multibuildings": len(actual_multi),
        "regional_lostcities_multibuildings": len(actual_regional_multi),
        "lostcities_scattered": len(actual_scattered),
        "global_selector_regional_leaks": regional_leaks,
        "active_settlement_archetypes": sorted(active_archetypes),
        "regional_structures": regional_records,
        "structures": records,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if failures:
        raise SystemExit("Production integration validation failed:\n- " + "\n- ".join(failures))
    print(
        f"Validated production quarantine for {len(records)} central structures; "
        f"{len(approved)} central, {len(actual_regional_multi)} regional citystyle and "
        f"{len(regional_approved) - len(actual_regional_multi)} biome-owned approvals"
    )


if __name__ == "__main__":
    main()
