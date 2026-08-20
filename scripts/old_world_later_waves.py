#!/usr/bin/env python3
"""Later Old World implementation waves consumed by the authoritative generator.

This module is an implementation component only. It exports immutable specs and
builders; generate_old_world_narrative_structures.py remains the sole executable
entrypoint and owns registry/worldgen synchronization.
"""
from __future__ import annotations

import old_world_narrative_core as core

base = core.base

HELION_EXTENSION = (
    core.Spec(
        "OWS-034",
        "ows_034_helion_neighborhood_electrical_substation",
        "infinite_domain:city_electrical_substation_clean_master",
        "city_electrical_substation",
        "kubejs:helion_insulation_service_log",
        "kubejs:helion_insulation_service_log",
        "Early anomaly",
        (
            "minecraft:light_blue_concrete",
            "minecraft:white_concrete",
            "immersiveengineering:capacitor_hv",
            "immersiveengineering:capacitor_mv",
            "immersiveengineering:coil_hv",
            "immersiveengineering:crate",
            "minecraft:yellow_concrete",
        ),
        {
            "silhouette_exterior_identity": "Helion light-blue and white service markings overlay the neighborhood substation without obscuring its transformer and feeder silhouette",
            "interior_zoning_circulation": "incoming power, transformer banks, switchyard, service staging, control house and city feeders remain legible as a maintenance sequence",
            "functional_machinery_props": "high-voltage coils, capacitor banks, temporary replacement components and service crates show ordinary electrical infrastructure under repair",
            "institutional_identity": "Helion cyan-white electrical coding repeats across transformer and control zones, presenting the grid operator as a mundane civic utility",
            "historical_damage_signature": "localized yellow isolation around failed insulation and temporary capacitor replacements shows the first material-driven maintenance escalation without grid collapse",
            "narrative_evidence_loot": "guaranteed insulation service log connects small polymer insulation failures to increasingly frequent neighborhood grid work",
        },
        "common_sites",
    ),
    core.Spec(
        "OWS-035",
        "ows_035_helion_grid_storage_compound",
        "infinite_domain:industrial_facility_clean_master",
        "industrial_facility",
        "kubejs:helion_grid_continuity_order",
        "kubejs:helion_grid_continuity_order",
        "Active containment",
        (
            "minecraft:light_blue_concrete",
            "minecraft:white_concrete",
            "immersiveengineering:capacitor_hv",
            "immersiveengineering:capacitor_mv",
            "minecraft:lever",
            "immersiveengineering:crate",
            "minecraft:yellow_concrete",
        ),
        {
            "silhouette_exterior_identity": "Helion cyan storage-bay bands and white utility crowns convert the industrial compound into a recognizable regional grid-storage yard",
            "interior_zoning_circulation": "storage-bank rows, isolation lanes, emergency switching, replacement stock and control dispatch form a readable power-continuity workflow",
            "functional_machinery_props": "dense capacitor banks, manual switch pedestals, service crates and isolated replacement rows make stored-grid capacity mechanically visible",
            "institutional_identity": "Helion zone numbering and cyan-white switching lanes standardize the emergency storage compound even as field modifications accumulate",
            "historical_damage_signature": "expanding yellow exclusion around later storage banks and permanent manual switching show active containment converting exceptional repairs into normal operation",
            "narrative_evidence_loot": "guaranteed grid continuity order documents the increasingly expensive effort to keep essential loads energized despite material failures",
        },
        "common_sites",
    ),
    core.Spec(
        "OWS-036",
        "ows_036_helion_coolant_pump_service_station",
        "infinite_domain:district_heating_station_clean_master",
        "district_heating_station",
        "kubejs:helion_coolant_integrity_report",
        "kubejs:helion_coolant_integrity_report",
        "Active containment",
        (
            "minecraft:light_blue_concrete",
            "minecraft:white_concrete",
            "create:fluid_tank",
            "create:fluid_pipe",
            "create:mechanical_pump",
            "immersiveengineering:crate",
            "minecraft:yellow_concrete",
        ),
        {
            "silhouette_exterior_identity": "Helion cyan pump-service bands and white coolant markings overlay the heating-station plant while preserving its heavy fluid-system silhouette",
            "interior_zoning_circulation": "coolant intake, pump rows, seal-service benches, replacement stock, leak isolation and outbound utility connections remain sequential",
            "functional_machinery_props": "large fluid tanks, repeated pumps, pipe manifolds and seal-replacement crates make coolant integrity dependence physically explicit",
            "institutional_identity": "Helion electrical-utility colors are carried into fluid service, linking power reliability to the same maintenance organization",
            "historical_damage_signature": "multiple yellow leak zones and replacement-seal stores show active containment driving pump and coolant service intervals downward",
            "narrative_evidence_loot": "guaranteed coolant integrity report links polymer degradation directly to escalating thermal-management and power-system risk",
        },
        "uncommon_sites",
    ),
    core.Spec(
        "OWS-037",
        "ows_037_helion_regional_power_operations_center",
        "infinite_domain:ae2_records_archive_clean_master",
        "ae2_records_archive",
        "kubejs:helion_regional_outage_directive",
        "kubejs:helion_regional_outage_directive",
        "Late containment",
        (
            "minecraft:light_blue_concrete",
            "minecraft:white_concrete",
            "minecraft:black_concrete",
            "ae2:controller",
            "ae2:drive",
            "immersiveengineering:capacitor_hv",
            "minecraft:lever",
            "minecraft:red_concrete",
            "minecraft:yellow_concrete",
        ),
        {
            "silhouette_exterior_identity": "Helion cyan operations bands and a white-black control crown turn the hardened data building into a regional power command center",
            "interior_zoning_circulation": "operator gallery, grid-control core, outage-priority lanes, backup power, manual switching and records archive are separated",
            "functional_machinery_props": "controller banks, data drives, high-voltage backup equipment and manual priority switches make rolling grid management tangible",
            "institutional_identity": "Helion cyan control coding is overlaid by red essential-load and yellow outage-priority markings as reliability deteriorates",
            "historical_damage_signature": "late-containment manual switching, priority fields and redundant backup systems show a regional grid no longer capable of universal service",
            "narrative_evidence_loot": "guaranteed regional outage directive records rolling power cuts and explicit prioritization of hospitals, water, communications and containment sites",
        },
        "uncommon_sites",
    ),
    core.Spec(
        "OWS-038",
        "ows_038_helion_nuclear_auxiliary_emergency_complex",
        "infinite_domain:nuclear_research_annex_clean_master",
        "nuclear_research_annex",
        "kubejs:helion_reactor_emergency_log",
        "kubejs:helion_reactor_emergency_log",
        "Late containment -> Firebreak",
        (
            "minecraft:light_blue_concrete",
            "minecraft:white_concrete",
            "create:fluid_tank",
            "create:fluid_pipe",
            "create:mechanical_pump",
            "immersiveengineering:capacitor_hv",
            "immersiveengineering:crate",
            "minecraft:yellow_concrete",
            "minecraft:red_concrete",
            "minecraft:oxidized_copper_grate",
        ),
        {
            "silhouette_exterior_identity": "Helion cyan auxiliary-system bands are increasingly dominated by red emergency shutdown fields and hardened perimeter work around the nuclear annex",
            "interior_zoning_circulation": "auxiliary cooling, emergency pumps, backup power, shutdown control, repair stock and protected access form a last-resort plant-support sequence",
            "functional_machinery_props": "redundant coolant tanks, pumps, high-voltage backup banks, repair crates and hardened barriers show the systems required to shut a reactor down safely",
            "institutional_identity": "Helion utility coding remains readable underneath military-style emergency restrictions, keeping the site tied to infrastructure rather than weapons research",
            "historical_damage_signature": "red shutdown zones, isolated coolant circuits and protected repair corridors show late containment crossing into Firebreak-era emergency plant stabilization",
            "narrative_evidence_loot": "guaranteed reactor emergency log bridges ordinary material degradation to the nuclear and grid emergencies encountered later in the collapse narrative",
        },
        "rare_sites",
    ),
)


def build_034():
    t = base.city_electrical_substation_clean_master()
    t.fill((7, 12, 36), (24, 14, 36), "minecraft:white_concrete")
    t.fill((10, 13, 35), (21, 16, 35), "minecraft:light_blue_concrete")
    t.fill((7, 1, 17), (27, 1, 28), "minecraft:yellow_concrete")
    for x in (10, 16, 22):
        t.fill((x, 2, 20), (x + 2, 4, 23), "immersiveengineering:capacitor_mv")
        t.fill((x, 2, 25), (x + 2, 3, 27), "immersiveengineering:crate")
    t.fill((31, 1, 28), (55, 1, 34), "minecraft:yellow_concrete")
    for x in (34, 42, 50):
        t.set(x, 2, 30, "immersiveengineering:capacitor_hv")
    t.chest(20, 3, 43, "infinite_domain:chests/old_world/ows_034_helion_neighborhood_electrical_substation", "west")
    return t


def build_035():
    t = base.industrial_facility_clean_master()
    t.fill((24, 13, 9), (48, 15, 9), "minecraft:white_concrete")
    t.fill((28, 14, 8), (44, 17, 8), "minecraft:light_blue_concrete")
    for index, x in enumerate((7, 17, 27, 37, 47), 1):
        t.fill((x, 1, 16), (x + 6, 1, 28), "minecraft:light_blue_concrete")
        t.fill((x + 1, 2, 18), (x + 5, 5, 22), "immersiveengineering:capacitor_hv")
        t.fill((x + 1, 2, 25), (x + 5, 4, 27), "immersiveengineering:capacitor_mv")
        t.fill((x, 1, 30), (x + index + 2, 1, 33), "minecraft:yellow_concrete")
        t.set(x + 3, 2, 31, "minecraft:lever", face="floor", facing="north", powered="false")
    t.fill((52, 2, 27), (63, 4, 32), "immersiveengineering:crate")
    t.chest(62, 2, 30, "infinite_domain:chests/old_world/ows_035_helion_grid_storage_compound", "west")
    return t


def build_036():
    t = base.district_heating_station_clean_master()
    t.fill((5, 18, 12), (38, 20, 12), "minecraft:white_concrete")
    t.fill((12, 19, 11), (31, 22, 11), "minecraft:light_blue_concrete")
    for x in (8, 18, 28, 42, 50):
        t.fill((x, 2, 34), (x + 2, 6, 38), "create:fluid_tank")
        t.fill((x, 2, 40), (x + 4, 2, 40), "create:fluid_pipe")
        t.set(x + 2, 2, 42, "create:mechanical_pump", facing="south")
    t.fill((7, 1, 39), (57, 1, 45), "minecraft:yellow_concrete")
    t.fill((42, 2, 45), (59, 4, 49), "immersiveengineering:crate")
    t.chest(55, 2, 47, "infinite_domain:chests/old_world/ows_036_helion_coolant_pump_service_station", "west")
    return t


def build_037():
    t = base.ae2_records_archive_clean_master()
    t.fill((6, 9, 10), (57, 11, 10), "minecraft:light_blue_concrete")
    t.fill((18, 22, 25), (58, 24, 25), "minecraft:white_concrete")
    t.fill((34, 25, 33), (46, 27, 33), "minecraft:black_concrete")
    t.fill((39, 13, 27), (57, 13, 28), "minecraft:light_blue_concrete")
    t.fill((45, 14, 34), (55, 17, 36), "ae2:drive")
    t.fill((47, 14, 39), (53, 17, 42), "ae2:controller")
    t.fill((46, 14, 18), (55, 17, 20), "immersiveengineering:capacitor_hv")
    t.fill((34, 13, 43), (58, 13, 46), "minecraft:yellow_concrete")
    t.fill((34, 13, 47), (58, 13, 49), "minecraft:red_concrete")
    for x in (37, 43, 49, 55):
        t.set(x, 14, 44, "minecraft:lever", face="floor", facing="north", powered="false")
    t.chest(54, 14, 33, "infinite_domain:chests/old_world/ows_037_helion_regional_power_operations_center", "west")
    return t


def build_038():
    t = base.nuclear_research_annex_clean_master()
    t.fill((5, 13, 10), (38, 15, 10), "minecraft:white_concrete")
    t.fill((12, 14, 9), (31, 17, 9), "minecraft:light_blue_concrete")
    for x in (8, 17, 26, 35):
        t.fill((x, 2, 18), (x + 3, 7, 23), "create:fluid_tank")
        t.fill((x, 2, 25), (x + 5, 2, 25), "create:fluid_pipe")
        t.set(x + 2, 2, 27, "create:mechanical_pump", facing="south")
    t.fill((7, 1, 29), (43, 1, 34), "minecraft:yellow_concrete")
    t.fill((45, 1, 25), (69, 1, 50), "minecraft:red_concrete")
    t.fill((48, 2, 28), (66, 4, 31), "immersiveengineering:capacitor_hv")
    t.fill((48, 2, 34), (66, 4, 38), "immersiveengineering:crate")
    t.fill((44, 2, 24), (44, 7, 51), "minecraft:oxidized_copper_grate")
    t.chest(40, 2, 55, "infinite_domain:chests/old_world/ows_038_helion_nuclear_auxiliary_emergency_complex", "west")
    return t

SPECS = HELION_EXTENSION
BUILDERS = {
    "OWS-034": build_034,
    "OWS-035": build_035,
    "OWS-036": build_036,
    "OWS-037": build_037,
    "OWS-038": build_038,
}
CURRENT_WAVE = "helion_functional_coverage_and_pt9_controlled_runtime_probe"
