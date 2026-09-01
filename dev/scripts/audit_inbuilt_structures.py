from __future__ import annotations

import gzip
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from generate_wasteland_sites import STRUCTURE_BLOCK_REPLACEMENTS
from build_structure_qa_world import Reader


ROOT = Path(__file__).resolve().parents[1]
SITE_MANIFEST = ROOT / "docs" / "wasteland-site-manifest.json"
LINT_REPORT = ROOT / "docs" / "wasteland-structure-structural-lint.json"
VISUAL_REPORT = ROOT / "docs" / "wasteland-structure-visual-review.json"
RENDER_MANIFEST = ROOT / "structure_library" / "audit_renders" / "render-manifest.json"
REGISTRY = ROOT / "docs" / "registry-inventory" / "block-ids.txt"
JSON_REPORT = ROOT / "docs" / "inbuilt-structure-audit.json"
MARKDOWN_REPORT = ROOT / "docs" / "INBUILT_STRUCTURE_AUDIT.md"
REBUILT = {"abandoned_bungalow", "abandoned_motel", "dilapidated_grocery", "ruined_gas_station", "freight_depot", "ruined_fire_station", "corporate_warehouse", "abandoned_create_factory", "bunker_network", "survivor_cache", "trade_outpost", "decayed_farm", "trailer_park", "mountain_military_complex", "mountain_biohazard_lab", "decayed_logging_camp", "bombed_data_center", "hydroelectric_refuge_dam", "toppled_skyscraper", "blown_apartment_complex", "ruined_mixed_use_block", "sunken_city_front", "pancaked_parking_structure", "cratered_downtown_intersection", "ruined_hospital", "ruined_police_precinct", "ruined_courthouse"}
REBUILT.update({"radio_mast", "wrecked_sedan", "delivery_van", "battle_tank", "service_garage", "scrapyard", "military_checkpoint", "ruined_roadside_diner", "abandoned_truck_stop", "wasteland_weigh_station", "destroyed_refugee_convoy", "split_level_house", "abandoned_culdesac", "emergency_relief_shelter", "tenement_courtyard", "ruined_rowhouse_block", "shattered_luxury_condo", "ruined_city_school", "ruined_community_center", "decayed_ranch", "roadside_church_cemetery", "ruined_ranger_station", "wasteland_fire_lookout"})
REBUILT.update({"ruined_shopping_mall", "ruined_department_store", "bombed_hotel", "buried_bank_vault", "ruined_office_tower"})
REBUILT.update({"collapsed_subway_station", "ruined_bus_terminal", "elevated_rail_collapse", "sunken_highway_interchange", "collapsed_airship_terminal", "crashed_cargo_airship", "warm_industrial_mountain_port", "cold_industrial_mountain_port"})
REBUILT.update({"abandoned_orchard_cannery", "ruined_grain_elevator", "shattered_greenhouse_nursery", "remote_sawmill"})
REBUILT.update({"abandoned_quarry", "collapsed_mine_entrance", "excavator_pit", "abandoned_oil_field"})
REBUILT.update({"industrial_facility", "city_electrical_substation", "city_water_treatment_plant", "district_heating_station", "municipal_incinerator", "ruined_fuel_depot", "ruined_cyberware_clinic", "ae2_records_archive", "nuclear_research_annex", "shattered_wind_farm", "broken_solar_field", "wilderness_substation", "wasteland_water_tower"})


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def unpack_structure(path: Path) -> tuple[tuple[int, int, int], dict[tuple[int, int, int], str]]:
    _, root = Reader(gzip.decompress(path.read_bytes())).root()
    data = root.value
    size = tuple(int(tag.value) for tag in data["size"].value.values)
    palette = [entry.value["Name"].value for entry in data["palette"].value.values]
    blocks: dict[tuple[int, int, int], str] = {}
    for entry_tag in data["blocks"].value.values:
        entry = entry_tag.value
        pos = tuple(int(tag.value) for tag in entry["pos"].value.values)
        name = palette[int(entry["state"].value)]
        if name not in {"minecraft:air", "minecraft:cave_air", "minecraft:void_air", "minecraft:structure_void"}:
            blocks[pos] = name
    return size, blocks


def main() -> None:
    manifest = load_json(SITE_MANIFEST)
    lint = load_json(LINT_REPORT)["structures"]
    visual = load_json(VISUAL_REPORT)["structures"]
    render_document = load_json(RENDER_MANIFEST)
    registry = {line.strip() for line in REGISTRY.read_text(encoding="utf-8").splitlines() if line.strip()}
    structures = manifest["structures"]
    names = list(structures)

    global_issues: list[str] = []
    if len(names) != 84 or len(set(names)) != 84:
        global_issues.append(f"authoritative inventory expected 84 unique names, found {len(names)}")
    if set(names) != set(lint):
        global_issues.append("structural-lint inventory disagrees with authoritative manifest")
    if set(names) != set(visual):
        global_issues.append("visual-disposition inventory disagrees with authoritative manifest")

    render_entries = {entry["structure_id"].split(":", 1)[1]: entry for entry in render_document["structures"]}
    if set(names) != set(render_entries):
        global_issues.append("render inventory disagrees with authoritative manifest")

    family_membership: dict[str, list[str]] = defaultdict(list)
    for family, data in manifest["families"].items():
        for name in data["members"]:
            family_membership[name].append(family)

    results: dict[str, Any] = {}
    all_unknown_blocks: set[str] = set()
    for name in names:
        issues: list[str] = []
        metadata = structures[name]
        nbt_path = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{name}.nbt"
        structure_json = ROOT / "kubejs" / "data" / "infinite_domain" / "worldgen" / "structure" / "wasteland" / f"{name}.json"
        pool_json = ROOT / "kubejs" / "data" / "infinite_domain" / "worldgen" / "template_pool" / "wasteland" / f"{name}.json"

        if not nbt_path.is_file():
            issues.append("missing source NBT")
            size, blocks = (0, 0, 0), {}
        else:
            try:
                size, blocks = unpack_structure(nbt_path)
            except (OSError, EOFError, KeyError, ValueError) as error:
                issues.append(f"unreadable source NBT: {error}")
                size, blocks = (0, 0, 0), {}
        if list(size) != metadata["size"]:
            issues.append(f"manifest size {metadata['size']} disagrees with NBT {list(size)}")

        palette = set(blocks.values())
        unknown_blocks = sorted(palette - registry)
        all_unknown_blocks.update(unknown_blocks)
        if unknown_blocks:
            issues.append(f"{len(unknown_blocks)} palette blocks absent from registry inventory")
        forbidden_blocks = sorted(palette & set(STRUCTURE_BLOCK_REPLACEMENTS))
        if forbidden_blocks:
            issues.append(f"forbidden unstable template blocks present: {forbidden_blocks}")

        if not structure_json.is_file():
            issues.append("missing worldgen structure definition")
            worldgen = {}
        else:
            worldgen = load_json(structure_json)
            if worldgen.get("biomes") != "#infinite_domain:disabled_primitive_wasteland_settlements":
                issues.append("structure is not quarantined by the disabled biome tag")
        if not pool_json.is_file():
            issues.append("missing template pool")

        lint_entry = lint.get(name, {})
        if not lint_entry.get("structural_lint_passed"):
            issues.append("mechanical structural lint failed")
        expected_visual = "rebuilt_pending_in_world_review" if name in REBUILT else "requires_purpose_built_rebuild"
        if visual.get(name, {}).get("status") != expected_visual:
            issues.append(f"visual disposition should be {expected_visual}")

        render_entry = render_entries.get(name, {})
        render_files = render_entry.get("renders", {})
        for view in ("exterior_a", "exterior_b", "roof_off_cutaway", "floor_slices"):
            relative = render_files.get(view)
            if not relative or not (ROOT / relative).is_file():
                issues.append(f"missing {view} audit render")

        families = family_membership.get(name, [])
        if not families:
            issues.append("not assigned to a structure family")

        disposition = "rebuilt_pending_in_world_review" if name in REBUILT else "quarantined_requires_purpose_built_rebuild"
        deferred = [
            "canonical in-world player-scale walkthrough",
            "four-way rotation and connector test",
            "terrain-placement and feathering test",
        ]
        if name not in REBUILT:
            deferred.extend([
                "architectural program and circulation review",
                "facade, roof and silhouette refinement",
                "coherent damage/occupation derivation from a clean master",
            ])

        results[name] = {
            "audit_disposition": disposition,
            "audit_complete": not issues,
            "production_approved": False,
            "families": families,
            "profile": lint_entry.get("profile"),
            "size": list(size),
            "non_air_blocks": len(blocks),
            "palette_blocks": len(palette),
            "block_entities": metadata.get("spawners", 0),
            "entities": metadata.get("entities", 0),
            "mechanical_lint": lint_entry,
            "worldgen_quarantined": worldgen.get("biomes") == "#infinite_domain:disabled_primitive_wasteland_settlements",
            "render_evidence": render_files,
            "blocking_audit_issues": issues,
            "explicitly_deferred_checks": deferred,
        }

    incomplete = [name for name, entry in results.items() if not entry["audit_complete"]]
    report = {
        "purpose": "Authoritative Stage A inventory reconciliation and audit disposition. Quarantine/rebuild disposition is audit completion, not architectural or production approval.",
        "minecraft_version": manifest["minecraft_version"],
        "authoritative_inventory": "docs/wasteland-site-manifest.json structures",
        "structures_expected": 84,
        "structures_audited": len(results),
        "completed_audit_dispositions": sum(1 for entry in results.values() if entry["audit_complete"]),
        "rebuilt_pending_in_world_review": sum(1 for entry in results.values() if entry["audit_disposition"] == "rebuilt_pending_in_world_review"),
        "quarantined_requires_purpose_built_rebuild": sum(1 for entry in results.values() if entry["audit_disposition"] == "quarantined_requires_purpose_built_rebuild"),
        "production_approved": 0,
        "unknown_palette_blocks": sorted(all_unknown_blocks),
        "global_issues": global_issues,
        "stage_a_inventory_gate_passed": not global_issues and not incomplete and len(results) == 84,
        "structures": results,
    }
    JSON_REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")

    lines = [
        "# Inbuilt Structure Audit",
        "",
        "This is the authoritative Stage A disposition ledger for the 84 Infinite Domain Wasteland templates. A quarantined rebuild requirement is a completed audit disposition, not a quality approval.",
        "",
        f"- Inventory: {len(results)}/84",
        f"- Completed dispositions: {report['completed_audit_dispositions']}/84",
        f"- Rebuilt, awaiting in-world review: {report['rebuilt_pending_in_world_review']}",
        f"- Quarantined for purpose-built rebuild: {report['quarantined_requires_purpose_built_rebuild']}",
        "- Production approvals: 0",
        f"- Stage A inventory gate: {'PASS' if report['stage_a_inventory_gate_passed'] else 'FAIL'}",
        "",
        "| Structure | Family | Profile | Size | Disposition | Audit evidence |",
        "|---|---|---|---:|---|---|",
    ]
    for name, entry in results.items():
        evidence = "4 renders + lint + NBT + worldgen" if entry["audit_complete"] else "; ".join(entry["blocking_audit_issues"])
        lines.append(f"| `{name}` | {', '.join(entry['families'])} | {entry['profile']} | {'x'.join(map(str, entry['size']))} | {entry['audit_disposition']} | {evidence} |")
    MARKDOWN_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

    failures = [*global_issues, *(f"{name}: {', '.join(results[name]['blocking_audit_issues'])}" for name in incomplete)]
    if failures:
        raise SystemExit("\n".join(failures))
    print(
        f"Audited 84/84 inbuilt structures: {report['rebuilt_pending_in_world_review']} rebuilt candidates, "
        f"{report['quarantined_requires_purpose_built_rebuild']} quarantined rebuild dispositions, 0 production approvals"
    )


if __name__ == "__main__":
    main()
