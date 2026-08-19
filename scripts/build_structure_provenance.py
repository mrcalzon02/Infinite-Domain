from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
LIBRARY = ROOT / "structure_library"
SITE_MANIFEST = ROOT / "docs" / "wasteland-site-manifest.json"
CATALOG = LIBRARY / "catalog.json"
OUTPUT = LIBRARY / "licensing" / "provenance.json"
CORPUS = LIBRARY / "corpus-manifest.json"
EXTERNAL_PROVENANCE = [
    LIBRARY / "licensing" / "creativelands-extracted-provenance.json",
]


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def file_record(structure_id: str, relative: str, integration_status: str, modifications: list[str], lineage: list[str]) -> dict[str, Any]:
    path = ROOT / relative
    raw = path.read_bytes()
    return {
        "structure_id": structure_id,
        "source_kind": "project_generated",
        "source_project": "Infinite Domain",
        "source_author": "Infinite Domain project",
        "source_url": None,
        "source_license": "project-owned",
        "license_classification": "approved_for_redistribution",
        "required_attribution": "none",
        "commercial_use_allowed": True,
        "modification_allowed": True,
        "redistribution_allowed": True,
        "original_minecraft_version": "1.21.1",
        "original_format": "Minecraft compressed structure NBT",
        "original_filename": relative.replace("\\", "/"),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "file_size_bytes": len(raw),
        "conversion_history": lineage,
        "our_modifications": modifications,
        "integration_status": integration_status,
    }


def main() -> None:
    manifest = load(SITE_MANIFEST)
    catalog = load(CATALOG)["structures"]
    catalog_by_id = {entry["structure_id"]: entry for entry in catalog}
    rebuilt = {
        "abandoned_bungalow": "infinite_domain:bungalow_clean_master",
        "abandoned_motel": "infinite_domain:motel_clean_master",
        "dilapidated_grocery": "infinite_domain:grocery_clean_master",
        "ruined_gas_station": "infinite_domain:gas_station_clean_master",
        "freight_depot": "infinite_domain:freight_depot_clean_master",
        "ruined_fire_station": "infinite_domain:fire_station_clean_master",
        "corporate_warehouse": "infinite_domain:corporate_warehouse_clean_master",
        "abandoned_create_factory": "infinite_domain:create_factory_clean_master",
        "bunker_network": "infinite_domain:bunker_network_clean_master",
        "survivor_cache": "infinite_domain:survivor_cache_clean_master",
        "trade_outpost": "infinite_domain:trade_outpost_clean_master",
        "decayed_farm": "infinite_domain:decayed_farm_clean_master",
        "trailer_park": "infinite_domain:trailer_park_clean_master",
        "mountain_military_complex": "infinite_domain:mountain_military_complex_clean_master",
        "mountain_biohazard_lab": "infinite_domain:mountain_biohazard_lab_clean_master",
        "decayed_logging_camp": "infinite_domain:decayed_logging_camp_clean_master",
        "bombed_data_center": "infinite_domain:bombed_data_center_clean_master",
        "hydroelectric_refuge_dam": "infinite_domain:hydroelectric_refuge_dam_clean_master",
        "toppled_skyscraper": "infinite_domain:toppled_skyscraper_clean_master",
        "blown_apartment_complex": "infinite_domain:blown_apartment_complex_clean_master",
        "ruined_mixed_use_block": "infinite_domain:ruined_mixed_use_block_clean_master",
        "sunken_city_front": "infinite_domain:sunken_city_front_clean_master",
        "pancaked_parking_structure": "infinite_domain:pancaked_parking_structure_clean_master",
        "cratered_downtown_intersection": "infinite_domain:cratered_downtown_intersection_clean_master",
        "ruined_hospital": "infinite_domain:ruined_hospital_clean_master",
        "ruined_police_precinct": "infinite_domain:ruined_police_precinct_clean_master",
        "ruined_courthouse": "infinite_domain:ruined_courthouse_clean_master",
        "radio_mast": "infinite_domain:radio_mast_clean_master",
        "wrecked_sedan": "infinite_domain:wrecked_sedan_clean_master",
        "delivery_van": "infinite_domain:delivery_van_clean_master",
        "battle_tank": "infinite_domain:battle_tank_clean_master",
        "service_garage": "infinite_domain:service_garage_clean_master",
        "scrapyard": "infinite_domain:scrapyard_clean_master",
        "military_checkpoint": "infinite_domain:military_checkpoint_clean_master",
        "ruined_roadside_diner": "infinite_domain:ruined_roadside_diner_clean_master",
        "abandoned_truck_stop": "infinite_domain:abandoned_truck_stop_clean_master",
        "wasteland_weigh_station": "infinite_domain:wasteland_weigh_station_clean_master",
        "destroyed_refugee_convoy": "infinite_domain:destroyed_refugee_convoy_clean_master",
        "split_level_house": "infinite_domain:split_level_house_clean_master",
        "abandoned_culdesac": "infinite_domain:abandoned_culdesac_clean_master",
        "emergency_relief_shelter": "infinite_domain:emergency_relief_shelter_clean_master",
        "tenement_courtyard": "infinite_domain:tenement_courtyard_clean_master",
        "ruined_rowhouse_block": "infinite_domain:ruined_rowhouse_block_clean_master",
        "shattered_luxury_condo": "infinite_domain:shattered_luxury_condo_clean_master",
        "ruined_city_school": "infinite_domain:ruined_city_school_clean_master",
        "ruined_community_center": "infinite_domain:ruined_community_center_clean_master",
        "decayed_ranch": "infinite_domain:decayed_ranch_clean_master",
        "roadside_church_cemetery": "infinite_domain:roadside_church_cemetery_clean_master",
        "ruined_ranger_station": "infinite_domain:ruined_ranger_station_clean_master",
        "wasteland_fire_lookout": "infinite_domain:wasteland_fire_lookout_clean_master",
        "ruined_shopping_mall": "infinite_domain:ruined_shopping_mall_clean_master",
        "ruined_department_store": "infinite_domain:ruined_department_store_clean_master",
        "bombed_hotel": "infinite_domain:bombed_hotel_clean_master",
        "buried_bank_vault": "infinite_domain:buried_bank_vault_clean_master",
        "ruined_office_tower": "infinite_domain:ruined_office_tower_clean_master",
        "collapsed_subway_station": "infinite_domain:collapsed_subway_station_clean_master",
        "ruined_bus_terminal": "infinite_domain:ruined_bus_terminal_clean_master",
        "elevated_rail_collapse": "infinite_domain:elevated_rail_collapse_clean_master",
        "sunken_highway_interchange": "infinite_domain:sunken_highway_interchange_clean_master",
        "collapsed_airship_terminal": "infinite_domain:collapsed_airship_terminal_clean_master",
        "crashed_cargo_airship": "infinite_domain:crashed_cargo_airship_clean_master",
        "warm_industrial_mountain_port": "infinite_domain:warm_industrial_mountain_port_clean_master",
        "cold_industrial_mountain_port": "infinite_domain:cold_industrial_mountain_port_clean_master",
        "abandoned_orchard_cannery": "infinite_domain:abandoned_orchard_cannery_clean_master",
        "ruined_grain_elevator": "infinite_domain:ruined_grain_elevator_clean_master",
        "shattered_greenhouse_nursery": "infinite_domain:shattered_greenhouse_nursery_clean_master",
        "remote_sawmill": "infinite_domain:remote_sawmill_clean_master",
        "abandoned_quarry": "infinite_domain:abandoned_quarry_clean_master",
        "collapsed_mine_entrance": "infinite_domain:collapsed_mine_entrance_clean_master",
        "excavator_pit": "infinite_domain:excavator_pit_clean_master",
        "abandoned_oil_field": "infinite_domain:abandoned_oil_field_clean_master",
        "industrial_facility": "infinite_domain:industrial_facility_clean_master",
        "city_electrical_substation": "infinite_domain:city_electrical_substation_clean_master",
        "city_water_treatment_plant": "infinite_domain:city_water_treatment_plant_clean_master",
        "district_heating_station": "infinite_domain:district_heating_station_clean_master",
        "municipal_incinerator": "infinite_domain:municipal_incinerator_clean_master",
        "ruined_fuel_depot": "infinite_domain:ruined_fuel_depot_clean_master",
        "ruined_cyberware_clinic": "infinite_domain:ruined_cyberware_clinic_clean_master",
        "ae2_records_archive": "infinite_domain:ae2_records_archive_clean_master",
        "nuclear_research_annex": "infinite_domain:nuclear_research_annex_clean_master",
        "shattered_wind_farm": "infinite_domain:shattered_wind_farm_clean_master",
        "broken_solar_field": "infinite_domain:broken_solar_field_clean_master",
        "wilderness_substation": "infinite_domain:wilderness_substation_clean_master",
        "wasteland_water_tower": "infinite_domain:wasteland_water_tower_clean_master",
    }

    records: list[dict[str, Any]] = []
    for name in manifest["structures"]:
        structure_id = f"infinite_domain:{name}"
        clean_master = rebuilt.get(name)
        if clean_master:
            lineage = [
                "generated by scripts/generate_wasteland_sites.py",
                f"derived from immutable clean master {clean_master}",
                "localized damage/environment/occupation pass",
            ]
            modifications = [
                "heavy architectural rebuild completed on clean master",
                "purpose-specific program and circulation validation",
                "coherent wasteland derivative regenerated from clean master",
            ]
            status = "quarantined_rebuilt_pending_in_world_review"
        else:
            lineage = ["generated by scripts/generate_wasteland_sites.py"]
            modifications = ["mechanically validated and rendered for Stage A audit"]
            status = "quarantined_requires_purpose_built_rebuild"
        records.append(file_record(
            structure_id,
            f"kubejs/data/infinite_domain/structure/wasteland/{name}.nbt",
            status,
            modifications,
            lineage,
        ))

    for entry in catalog:
        if entry["source_role"] != "clean_master":
            continue
        structure_id = entry["structure_id"]
        records.append(file_record(
            structure_id,
            entry["source_template"],
            "quarantined_clean_master_pending_in_world_review",
            [
                "heavy architectural articulation",
                "purpose-specific room program",
                "rendered review and automatic validation",
            ],
            ["generated by scripts/generate_wasteland_sites.py as immutable clean master"],
        ))

    for external_provenance in EXTERNAL_PROVENANCE:
        if external_provenance.is_file():
            records.extend(load(external_provenance)["records"])

    ids = [record["structure_id"] for record in records]
    if len(ids) < 87 or len(set(ids)) != len(ids):
        raise SystemExit(f"Expected at least 87 unique provenance records, found {len(ids)} total / {len(set(ids))} unique")
    missing_catalog = sorted(entry["structure_id"] for entry in catalog if entry["structure_id"] not in set(ids))
    if missing_catalog:
        raise SystemExit(f"Catalog entries lack provenance: {missing_catalog}")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    document = {
        "format_version": 1,
        "policy": {
            "unknown_or_uncertain_license": "exclude_from_distributable_builds",
            "provenance_removal": "forbidden",
            "approved_classifications": ["approved_for_redistribution", "approved_with_attribution"],
        },
        "records": records,
    }
    OUTPUT.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8", newline="\n")

    corpus = {
        "format_version": 1,
        "canonical_root": "structure_library",
        "authoritative_inbuilt_inventory": "docs/wasteland-site-manifest.json",
        "metadata_catalog": "structure_library/catalog.json",
        "provenance_manifest": "structure_library/licensing/provenance.json",
        "clean_master_storage": "kubejs/data/infinite_domain/structure/wasteland/masters",
        "generated_variant_storage": "kubejs/data/infinite_domain/structure/wasteland",
        "programs": "structure_library/programs",
        "variant_descriptions": "structure_library/variants",
        "modules": "structure_library/modules/catalog.json",
        "infrastructure": "structure_library/infrastructure/catalog.json",
        "rendered_reviews": "structure_library/reviews",
        "full_audit_renders": "structure_library/audit_renders",
        "extracted_review_storage": "structure_library/extracted",
        "counts": {
            "inbuilt_variants_and_sources": 84,
            "clean_masters": sum(1 for entry in catalog if entry["source_role"] == "clean_master"),
            "provenance_records": len(records),
            "production_approved": 0,
        },
        "integration_rule": "Only explicitly approved records may be referenced by production Lost Cities or custom worldgen selectors.",
    }
    CORPUS.write_text(json.dumps(corpus, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Built canonical corpus/provenance manifests for {len(records)} retained structures; 0 production approvals")


if __name__ == "__main__":
    main()
