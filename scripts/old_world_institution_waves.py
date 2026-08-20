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

BLACKGLASS_EXTENSION = (
    core.Spec(
        "OWS-039",
        "ows_039_blackglass_street_communications_exchange",
        "infinite_domain:radio_mast_clean_master",
        "radio_mast",
        "kubejs:blackglass_exchange_access_token",
        "kubejs:blackglass_exchange_access_token",
        "Early anomaly",
        (
            "minecraft:black_concrete",
            "minecraft:white_concrete",
            "minecraft:tinted_glass",
            "ae2:drive",
            "ae2:controller",
            "minecraft:light_blue_concrete",
        ),
        {
            "silhouette_exterior_identity": "a compact black-and-white Blackglass exchange hut anchors the existing communications mast, making secure telecom infrastructure recognizable at street scale",
            "interior_zoning_circulation": "street service entry, routing cabinets, secure controller core and mast handoff form a tiny but legible communications workflow",
            "functional_machinery_props": "data drives, controller hardware and protected cabinet rows establish a sophisticated digital exchange without requiring later Darknet functionality",
            "institutional_identity": "Blackglass black fields, white service edges and sparse cyan routing marks create a consistent secure-network identity",
            "historical_damage_signature": "the exchange remains operationally intact with only early service isolation, establishing an information-infrastructure baseline before later archive failures",
            "narrative_evidence_loot": "guaranteed exchange access token is usable as physical archaeological evidence now while preserving its deeper network meaning for the later Darknet phase",
        },
        "common_sites",
    ),
    core.Spec(
        "OWS-040",
        "ows_040_blackglass_civic_data_relay",
        "infinite_domain:ae2_records_archive_clean_master",
        "ae2_records_archive",
        "kubejs:encrypted_civic_data_cartridge",
        "kubejs:encrypted_civic_data_cartridge",
        "Active containment",
        (
            "minecraft:black_concrete",
            "minecraft:white_concrete",
            "minecraft:light_blue_concrete",
            "ae2:drive",
            "ae2:controller",
            "immersiveengineering:capacitor_hv",
            "minecraft:yellow_concrete",
        ),
        {
            "silhouette_exterior_identity": "Blackglass black relay bands and a white civic-network crown turn the hardened archive shell into a municipal data node",
            "interior_zoning_circulation": "public-network intake, encrypted civic routing, secure data core, backup power and physical archive handoff are separated",
            "functional_machinery_props": "controller and drive banks, backup capacitors and isolated terminal zones make civic networking and resilience physically legible",
            "institutional_identity": "Blackglass security colors are interrupted by civic white and cyan route coding, showing a private technical layer embedded in government services",
            "historical_damage_signature": "yellow backup-power and isolation fields show active containment forcing the relay to operate increasingly as a hardened island",
            "narrative_evidence_loot": "guaranteed encrypted civic data cartridge provides physical evidence immediately while its protected contents remain reserved for later re-exploration",
        },
        "uncommon_sites",
    ),
    core.Spec(
        "OWS-041",
        "ows_041_blackglass_industrial_control_archive",
        "infinite_domain:industrial_facility_clean_master",
        "industrial_facility",
        "kubejs:encrypted_industrial_archive",
        "kubejs:encrypted_industrial_archive",
        "Late containment",
        (
            "minecraft:black_concrete",
            "minecraft:orange_concrete",
            "minecraft:light_blue_concrete",
            "ae2:drive",
            "ae2:controller",
            "immersiveengineering:capacitor_hv",
            "minecraft:yellow_concrete",
        ),
        {
            "silhouette_exterior_identity": "a black Blackglass control/archive wing is visibly attached to the industrial plant while Atlas-orange and Helion-cyan interface markings remain distinct",
            "interior_zoning_circulation": "industrial telemetry intake, vendor correlation cells, secure archive core, backup power and records dispatch create a cross-industry evidence chain",
            "functional_machinery_props": "data drives, controllers, power backup and color-coded Atlas/Helion interfaces physically connect failures previously seen at separate sites",
            "institutional_identity": "Blackglass security fields contain rather than erase the orange automation and cyan power identities of the systems being monitored",
            "historical_damage_signature": "late-containment yellow isolation surrounds an archive still ingesting emergency data, showing institutions correlating systemic failure even while losing control",
            "narrative_evidence_loot": "guaranteed encrypted industrial archive preserves the cross-industry correlation object for later interpretation without implementing Darknet decryption early",
        },
        "uncommon_sites",
    ),
    core.Spec(
        "OWS-042",
        "ows_042_blackglass_regional_data_center",
        "infinite_domain:bombed_data_center_clean_master",
        "bombed_data_center",
        "kubejs:blackglass_regional_archive_module",
        "kubejs:blackglass_regional_archive_module",
        "Late containment",
        (
            "minecraft:black_concrete",
            "minecraft:white_concrete",
            "minecraft:tinted_glass",
            "ae2:drive",
            "ae2:controller",
            "immersiveengineering:capacitor_hv",
            "minecraft:yellow_concrete",
        ),
        {
            "silhouette_exterior_identity": "Blackglass black security bands and white hardened-utility markings reinforce the purpose-built data campus rather than changing its fundamental silhouette",
            "interior_zoning_circulation": "security intake, server halls, controller core, hardened utilities, backup power and inaccessible archive vaults remain separately readable",
            "functional_machinery_props": "dense drive banks, controller clusters, backup capacitors and secure glazing make regional data infrastructure materially convincing",
            "institutional_identity": "Blackglass branding dominates because this is a primary company facility rather than a relay embedded in another institution",
            "historical_damage_signature": "yellow utility-isolation paths and segmented server halls show late containment preserving fragments of service by sacrificing full-campus connectivity",
            "narrative_evidence_loot": "guaranteed regional archive module establishes a major technological-archaeology return site while leaving encrypted contents inaccessible until the intended later phase",
        },
        "rare_sites",
    ),
    core.Spec(
        "OWS-043",
        "ows_043_blackglass_government_continuity_archive_node",
        "infinite_domain:bunker_network_clean_master",
        "bunker_network",
        "kubejs:government_encrypted_archive",
        "kubejs:government_encrypted_archive",
        "Firebreak Wars",
        (
            "minecraft:black_concrete",
            "minecraft:white_concrete",
            "immersiveengineering:concrete_reinforced",
            "ae2:drive",
            "ae2:controller",
            "immersiveengineering:capacitor_hv",
            "minecraft:red_concrete",
            "minecraft:yellow_concrete",
        ),
        {
            "silhouette_exterior_identity": "the civil-defense bunker remains externally austere while Blackglass security markings identify an internal government continuity archive rather than a generic shelter",
            "interior_zoning_circulation": "hardened intake, political records, military communications, secure data core, damaged archive sectors and continuity command handoff are compartmentalized",
            "functional_machinery_props": "reinforced rooms, redundant drive banks, controllers and backup power show why selected records survived deeper into the Firebreak period",
            "institutional_identity": "Blackglass technical security is visibly subordinate to government continuity markings, demonstrating contractor infrastructure embedded in state emergency operations",
            "historical_damage_signature": "red sealed sectors and yellow partially corrupted archive lanes show a hardened node surviving physically while losing pieces of its informational record",
            "narrative_evidence_loot": "guaranteed government encrypted archive preserves political and military crisis evidence for later interpretation without prematurely exposing its protected contents",
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


def build_039():
    t = base.radio_mast_clean_master()
    t.fill((1, 1, 1), (4, 6, 5), "minecraft:black_concrete")
    t.clear((2, 2, 2), (3, 5, 4))
    t.fill((1, 2, 2), (1, 4, 4), "minecraft:tinted_glass")
    t.fill((2, 2, 3), (3, 4, 3), "ae2:drive")
    t.set(3, 2, 4, "ae2:controller")
    t.fill((1, 6, 1), (4, 7, 5), "minecraft:white_concrete")
    t.fill((5, 1, 4), (9, 1, 5), "minecraft:light_blue_concrete")
    t.chest(3, 2, 2, "infinite_domain:chests/old_world/ows_039_blackglass_street_communications_exchange", "south")
    return t


def build_040():
    t = base.ae2_records_archive_clean_master()
    t.fill((6, 9, 10), (57, 11, 10), "minecraft:black_concrete")
    t.fill((18, 22, 25), (58, 24, 25), "minecraft:white_concrete")
    t.fill((39, 13, 27), (57, 13, 28), "minecraft:light_blue_concrete")
    t.fill((45, 14, 34), (55, 17, 36), "ae2:drive")
    t.fill((47, 14, 39), (53, 17, 42), "ae2:controller")
    t.fill((46, 14, 18), (55, 17, 20), "immersiveengineering:capacitor_hv")
    t.fill((34, 13, 43), (58, 13, 49), "minecraft:yellow_concrete")
    t.chest(54, 14, 33, "infinite_domain:chests/old_world/ows_040_blackglass_civic_data_relay", "west")
    return t


def build_041():
    t = base.industrial_facility_clean_master()
    t.fill((51, 10, 13), (64, 12, 13), "minecraft:black_concrete")
    t.fill((52, 1, 24), (64, 1, 26), "minecraft:white_concrete")
    t.fill((54, 2, 18), (62, 5, 20), "ae2:drive")
    t.fill((56, 2, 22), (60, 5, 23), "ae2:controller")
    t.fill((54, 2, 28), (62, 4, 30), "immersiveengineering:capacitor_hv")
    t.fill((52, 1, 32), (64, 1, 34), "minecraft:yellow_concrete")
    t.fill((53, 2, 35), (58, 3, 37), "minecraft:orange_concrete")
    t.fill((59, 2, 35), (64, 3, 37), "minecraft:light_blue_concrete")
    t.chest(62, 2, 33, "infinite_domain:chests/old_world/ows_041_blackglass_industrial_control_archive", "west")
    return t


def build_042():
    t = base.bombed_data_center_clean_master()
    t.fill((5, 9, 7), (55, 11, 7), "minecraft:black_concrete")
    t.fill((12, 12, 6), (48, 14, 6), "minecraft:white_concrete")
    for x in (9, 17, 25, 33, 41, 49):
        t.fill((x, 2, 16), (x + 3, 6, 20), "ae2:drive")
        t.fill((x, 2, 24), (x + 3, 5, 27), "ae2:controller")
    t.fill((42, 2, 33), (56, 5, 36), "immersiveengineering:capacitor_hv")
    t.fill((40, 1, 38), (57, 1, 47), "minecraft:yellow_concrete")
    t.fill((45, 2, 40), (56, 7, 47), "minecraft:tinted_glass")
    t.chest(52, 2, 45, "infinite_domain:chests/old_world/ows_042_blackglass_regional_data_center", "west")
    return t


def build_043():
    t = base.bunker_network_clean_master()
    t.fill((4, 2, 4), (42, 4, 4), "minecraft:black_concrete")
    t.fill((8, 2, 10), (38, 2, 12), "minecraft:white_concrete")
    for x in (9, 16, 23, 30, 37):
        t.fill((x, 3, 15), (x + 3, 6, 19), "ae2:drive")
        t.set(x + 1, 3, 21, "ae2:controller")
    t.fill((7, 2, 25), (39, 2, 29), "minecraft:yellow_concrete")
    t.fill((27, 2, 30), (41, 2, 38), "minecraft:red_concrete")
    t.fill((30, 3, 32), (39, 6, 36), "immersiveengineering:capacitor_hv")
    t.chest(22, 2, 22, "infinite_domain:chests/old_world/ows_043_blackglass_government_continuity_archive_node", "east")
    return t

SPECS = HELION_EXTENSION + BLACKGLASS_EXTENSION
BUILDERS = {
    "OWS-034": build_034,
    "OWS-035": build_035,
    "OWS-036": build_036,
    "OWS-037": build_037,
    "OWS-038": build_038,
    "OWS-039": build_039,
    "OWS-040": build_040,
    "OWS-041": build_041,
    "OWS-042": build_042,
    "OWS-043": build_043,
}
CURRENT_WAVE = "blackglass_functional_coverage_and_pt9_controlled_runtime_probe"
