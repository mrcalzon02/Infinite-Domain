#!/usr/bin/env python3
"""[SYSTEM REPORT] Authoritative Old World structure entrypoint.

The preserved ten-site implementation lives in old_world_narrative_core.py.
This file is the only executable structure-generation entrypoint and extends
that core with later narrative waves. Imported modules are implementation
components, not independent mutation paths.

Static implementation and natural-world placement are intentionally separate.
Only targets named in CONTROLLED_WORLDGEN_TARGETS are entered into a structure
set. All other generated structure definitions, pools, NBT, loot and registry
rows remain staged until runtime validation explicitly promotes them.
"""
from __future__ import annotations

import json
from pathlib import Path

import old_world_narrative_core as core
import old_world_later_waves as later

base = core.base
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "kubejs" / "data" / "infinite_domain"
PROGRAM = ROOT / "old_world_narrative"
REGISTRY = PROGRAM / "registry"

# PT-9 is the first controlled runtime-generation target. This is not runtime
# approval: it only makes OWS-006 discoverable for deliberate fresh-world tests.
CONTROLLED_WORLDGEN_TARGETS = ("OWS-006",)
DARKNET_RETURN_TARGETS = {
    "OWS-003": "Re-open the cold-chain routing archive after Darknet access exposes hidden global batch destinations.",
    "OWS-006": "Recover encrypted PT-9 comparison telemetry from the sealed pilot-lab records bank.",
    "OWS-008": "Unlock the persistence-incident clean-room cache and compare suppressed breach chronology.",
    "OWS-013": "Interrogate manual-bypass controller history for the automation failures hidden from ordinary maintenance staff.",
    "OWS-014": "Use Darknet credentials against the controls archive to expose Atlas/Helion/Blackglass integration records.",
}
ATLAS_TARGETS = {f"OWS-{index:03d}" for index in range(9, 15)}

VCF_COMPLETION = (
    core.Spec(
        "OWS-005",
        "ows_005_vcf_harvest_packaging_annex",
        "infinite_domain:abandoned_orchard_cannery_clean_master",
        "abandoned_orchard_cannery",
        "kubejs:vcf_packaging_quality_report",
        None,
        "Early anomaly",
        (
            "minecraft:lime_concrete",
            "minecraft:light_blue_concrete",
            "oritech:cooler_block",
            "create:depot",
            "create:mechanical_press",
            "create:cardboard_block",
        ),
        {
            "silhouette_exterior_identity": "VCF green packaging bands and a cold-chain loading crown replace cannery identity while retaining the industrial food silhouette",
            "interior_zoning_circulation": "harvest receiving, PT-9 sanitation, inspection, packing, cold hold and dispatch form a continuous consumer-food workflow",
            "functional_machinery_props": "wash piping, cooler banks, inspection depots, presses, carton staging and palletized output make the annex operationally legible",
            "institutional_identity": "VCF green/white production coding and cyan sanitation lanes sell PT-9 cleanliness as part of ordinary food quality assurance",
            "historical_damage_signature": "a growing yellow quarantine around rejected packaging lots records the first quality anomaly without turning the plant into a ruin",
            "narrative_evidence_loot": "guaranteed packaging quality report proves Evercrop and PT-9 were embedded in routine consumer food production before the crisis",
        },
        "uncommon_sites",
    ),
    core.Spec(
        "OWS-007",
        "ows_007_vcf_ep7_agricultural_development_laboratory",
        "infinite_domain:nuclear_research_annex_clean_master",
        "nuclear_research_annex",
        "kubejs:ep7_distribution_and_durability_record",
        None,
        "Pre-crisis",
        (
            "minecraft:lime_concrete",
            "create:framed_glass",
            "farmersdelight:rich_soil",
            "minecraft:mycelium",
            "oritech:cooler_block",
        ),
        {
            "silhouette_exterior_identity": "VCF green research bands and glass crop-test crowns convert the annex into a polished agricultural development campus",
            "interior_zoning_circulation": "seed intake, durability chambers, spore-survival rooms, storage trials, reseeding plots and food-quality review are deliberately separated",
            "functional_machinery_props": "sealed grow cells, controlled soil beds, mycelial test strips, cooler banks and stored reseeding stock support repeatable commercial trials",
            "institutional_identity": "VCF green/white presentation and clean numbered test cells frame extreme persistence and distribution traits as product advantages",
            "historical_damage_signature": "the site is intentionally pre-crisis and largely intact; its disturbing signature is the escalating stress conditions built into successful test zones",
            "narrative_evidence_loot": "guaranteed EP-7 distribution and durability record establishes that survival, storage and reseeding persistence were engineered and celebrated",
        },
        "rare_sites",
    ),
    core.Spec(
        "OWS-008",
        "ows_008_vcf_emergency_persistence_investigation_lab",
        "infinite_domain:mountain_biohazard_lab_clean_master",
        "mountain_biohazard_lab",
        "kubejs:vcf_persistence_incident_file",
        None,
        "Active containment",
        (
            "minecraft:lime_concrete",
            "minecraft:yellow_concrete",
            "create:framed_glass",
            "create:fluid_pipe",
            "minecraft:mycelium",
            "minecraft:brown_mushroom",
        ),
        {
            "silhouette_exterior_identity": "VCF green emergency-lab markings are overpainted by yellow containment bands and repeated clean-zone numbering",
            "interior_zoning_circulation": "dirty intake, sterilization sequence, clean-room checks, service-joint inspection, persistence testing and incident archive require repeated boundary crossings",
            "functional_machinery_props": "wash piping, sealed observation rooms, sample benches and deliberately exposed service joints reproduce failed decontamination pathways",
            "institutional_identity": "VCF bioscience branding survives beneath increasingly dominant containment colors, showing a commercial lab becoming an emergency investigation site",
            "historical_damage_signature": "mycelial contamination reappears along service seams after multiple sterilization zones, turning procedural failure itself into the physical story",
            "narrative_evidence_loot": "guaranteed persistence incident file documents repeated clean-room breaches and establishes that procedure changes could not restore containment",
        },
        "rare_sites",
    ),
)

ATLAS_EXTENSION = (
    core.Spec(
        "OWS-011",
        "ows_011_atlas_municipal_machine_service_shop",
        "infinite_domain:fire_station_clean_master",
        "ruined_fire_station",
        "kubejs:atlas_emergency_service_log",
        None,
        "Early containment",
        (
            "minecraft:orange_concrete",
            "minecraft:yellow_concrete",
            "create:andesite_casing",
            "minecraft:anvil",
            "immersiveengineering:crate",
        ),
        {
            "silhouette_exterior_identity": "Atlas orange service bands and municipal emergency chevrons convert the civic apparatus frontage into a machine-response depot",
            "interior_zoning_circulation": "three service bays, triage lane, teardown bench, parts issue, emergency work-order wall and staff route remain distinct",
            "functional_machinery_props": "casing stacks, anvils, stripped mechanisms, service crates and cannibalized repair stock fill the apparatus program",
            "institutional_identity": "Atlas orange equipment coding overlays municipal yellow/white emergency markings rather than replacing the civic identity",
            "historical_damage_signature": "the third bay has been cannibalized for parts and isolated as service intervals collapse across municipal equipment",
            "narrative_evidence_loot": "guaranteed emergency service log records the maintenance backlog accelerating from inconvenience into civic-system failure",
        },
        "common_sites",
    ),
    core.Spec(
        "OWS-013",
        "ows_013_atlas_automated_assembly_hall",
        "infinite_domain:create_factory_clean_master",
        "abandoned_create_factory",
        "kubejs:atlas_manual_bypass_notice",
        None,
        "Active containment",
        (
            "minecraft:orange_concrete",
            "minecraft:yellow_concrete",
            "create:mechanical_press",
            "create:depot",
            "create:andesite_casing",
            "minecraft:lever",
        ),
        {
            "silhouette_exterior_identity": "Atlas orange production bands, numbered cell crowns and a marked manual-control spine turn the fabrication plant into a standardized assembly hall",
            "interior_zoning_circulation": "feed staging, four assembly cells, inspection/rework, manual-bypass corridor and outbound handling form a readable production sequence",
            "functional_machinery_props": "press/depot stations, drive casings, calibration stock and dedicated bypass pedestals make automated handling physically legible",
            "institutional_identity": "Atlas numbered orange cells and black/yellow lockout stations standardize both normal automation and emergency intervention",
            "historical_damage_signature": "the final cell runs under a conspicuous manual bypass with stripped automation and staged replacement casings during active containment",
            "narrative_evidence_loot": "guaranteed manual-bypass notice shows Old World automation remaining productive only through increasingly desperate human intervention",
        },
        "uncommon_sites",
    ),
    core.Spec(
        "OWS-014",
        "ows_014_atlas_industrial_controls_integration_center",
        "infinite_domain:ae2_records_archive_clean_master",
        "ae2_records_archive",
        "kubejs:atlas_controls_archive_module",
        None,
        "Late containment",
        (
            "minecraft:orange_concrete",
            "minecraft:light_blue_concrete",
            "minecraft:black_concrete",
            "ae2:controller",
            "ae2:drive",
            "immersiveengineering:capacitor_hv",
        ),
        {
            "silhouette_exterior_identity": "Atlas orange control bands and a cyan/black integration crown identify a cross-vendor industrial controls campus rather than a passive records archive",
            "interior_zoning_circulation": "intake, prototype control cells, operator gallery, secure controller core, vendor-retrofit bay and archive route are separately readable",
            "functional_machinery_props": "AE2 controller/drive banks, Atlas prototype casings, high-voltage retrofit equipment and manual isolation stations form a real integration lab",
            "institutional_identity": "Atlas orange is deliberately interrupted by Helion-like cyan power coding and Blackglass-like black data-security fields",
            "historical_damage_signature": "late-containment yellow isolation fields, redundant manual switches and overlapping vendor retrofits show a control system being kept alive beyond its design envelope",
            "narrative_evidence_loot": "guaranteed controls archive module connects Atlas automation to power, data and later Darknet archaeological return visits",
        },
        "rare_sites",
    ),
)

AEVUM_EXTENSION = (
    core.Spec(
        "OWS-029",
        "ows_029_aevum_longevity_treatment_center",
        "infinite_domain:bombed_hotel_clean_master",
        "bombed_hotel",
        "kubejs:aevum_longevity_brief",
        "kubejs:aevum_longevity_brief",
        "Pre-crisis",
        (
            "minecraft:purple_concrete",
            "minecraft:white_concrete",
            "minecraft:smooth_quartz",
            "create:framed_glass",
            "create:fluid_tank",
            "minecraft:brewing_stand",
        ),
        {
            "silhouette_exterior_identity": "Aevum purple and white treatment-center bands convert the hotel-derived tower into an upscale longevity clinic without erasing its comfortable pre-crisis hospitality scale",
            "interior_zoning_circulation": "reception, consultation suites, repeated treatment rooms, long-term monitoring stations and recovery lounges create a deliberate elective-care sequence",
            "functional_machinery_props": "quartz treatment couches, privacy glass, biologic tanks, preparation stations and monitoring counters make recurring longevity therapy physically legible",
            "institutional_identity": "Aevum branding is polished and aspirational, presenting extended healthy lifespan as an ordinary premium service rather than a secret experiment",
            "historical_damage_signature": "the center remains intact and orderly; the historical signature is normalized long-duration treatment infrastructure rather than crisis damage",
            "narrative_evidence_loot": "guaranteed Aevum longevity brief establishes that healthy lifespan extension was real, socially desirable and already integrated into normal life",
        },
        "uncommon_sites",
    ),
    core.Spec(
        "OWS-030",
        "ows_030_aevum_apl_hospital_recovery_ward",
        "infinite_domain:ruined_hospital_clean_master",
        "ruined_hospital",
        "kubejs:apl_clinical_record",
        "kubejs:apl_clinical_record",
        "Early containment",
        (
            "minecraft:purple_concrete",
            "minecraft:white_concrete",
            "create:fluid_tank",
            "oritech:cooler_block",
            "minecraft:brewing_stand",
            "immersiveengineering:crate",
            "minecraft:yellow_concrete",
        ),
        {
            "silhouette_exterior_identity": "Aevum purple recovery-wing markings overlay the intact hospital facade while municipal clinical identity remains visible",
            "interior_zoning_circulation": "advanced recovery bays, biologic preparation, monitored step-down beds, supply control and conventional hospital circulation remain readable together",
            "functional_machinery_props": "fluid tanks, treatment preparation stations, refrigerated biologics and bedside stock demonstrate medicine that genuinely works but depends on material supply",
            "institutional_identity": "Aevum treatment coding is integrated into ordinary hospital operations rather than isolated as a private laboratory service",
            "historical_damage_signature": "yellow shortage lanes and replacement-stock staging appear beside still-functional advanced care, showing containment pressure before clinical collapse",
            "narrative_evidence_loot": "guaranteed APL clinical record proves the regenerative treatment produced real recoveries while documenting the first supply interruptions",
        },
        "uncommon_sites",
    ),
    core.Spec(
        "OWS-031",
        "ows_031_aevum_biologic_pharmacy_cold_store",
        "infinite_domain:grocery_clean_master",
        "grocery",
        "kubejs:aevum_supply_dependence_log",
        "kubejs:aevum_supply_dependence_log",
        "Active containment",
        (
            "minecraft:purple_concrete",
            "minecraft:white_concrete",
            "oritech:cooler_block",
            "immersiveengineering:crate",
            "create:cardboard_block",
            "minecraft:yellow_concrete",
        ),
        {
            "silhouette_exterior_identity": "Aevum purple pharmacy bands and white medical wayfinding replace ordinary retail identity while retaining a neighborhood distribution footprint",
            "interior_zoning_circulation": "prescription intake, refrigerated biologic vaults, controlled issue counters, rationed reserve stock and patient pickup form a compact medical supply chain",
            "functional_machinery_props": "dense cooler banks, sealed crates, packaged biologics and controlled dispensing stock make cold-chain dependence unavoidable",
            "institutional_identity": "Aevum clinical branding is overlaid by emergency allocation markings as treatment supply moves from ordinary prescription service to rationing",
            "historical_damage_signature": "expanding yellow reserve zones and shrinking accessible cold stock show active containment forcing treatment prioritization rather than immediate abandonment",
            "narrative_evidence_loot": "guaranteed supply dependence log records that thousands of patients could not safely stop APL therapy simply because infrastructure was failing",
        },
        "common_sites",
    ),
    core.Spec(
        "OWS-032",
        "ows_032_aevum_apl3_research_campus",
        "infinite_domain:mountain_biohazard_lab_clean_master",
        "mountain_biohazard_lab",
        "kubejs:apl3_research_summary",
        "kubejs:apl3_research_summary",
        "Early anomaly -> Active containment",
        (
            "minecraft:purple_concrete",
            "minecraft:white_concrete",
            "create:framed_glass",
            "create:fluid_tank",
            "minecraft:brewing_stand",
            "oritech:cooler_block",
            "minecraft:lime_concrete",
            "minecraft:yellow_concrete",
        ),
        {
            "silhouette_exterior_identity": "Aevum purple clinical-research bands and white laboratory crowns distinguish the secure campus while a limited green dependency stripe marks agricultural feedstock handling",
            "interior_zoning_circulation": "clinical sample intake, peptide preparation, four APL research cells, cold biologic archive, Evercrop-derived input handling and incident review are separated",
            "functional_machinery_props": "sealed glass cells, reagent stations, biologic tanks, coolers and marked agricultural-input stores demonstrate a real translational research workflow",
            "institutional_identity": "Aevum clinical branding remains dominant while VCF-green dependency markings make the APL/Evercrop relationship visible without implying the therapy was fraudulent",
            "historical_damage_signature": "later cells acquire yellow isolation and supply-diversion zones as a successful medical program becomes entangled with the growing biological containment crisis",
            "narrative_evidence_loot": "guaranteed APL-3 research summary reveals the treatment's origin, genuine effectiveness and dependence on the same agricultural biotechnology network now destabilizing civilization",
        },
        "rare_sites",
    ),
    core.Spec(
        "OWS-033",
        "ows_033_aevum_evacuation_dependency_ward",
        "infinite_domain:ruined_hospital_clean_master",
        "ruined_hospital",
        "kubejs:orlov_dependency_memorandum",
        "kubejs:orlov_dependency_memorandum",
        "Late containment",
        (
            "minecraft:purple_concrete",
            "minecraft:white_concrete",
            "oritech:cooler_block",
            "immersiveengineering:crate",
            "minecraft:yellow_concrete",
            "minecraft:red_concrete",
            "minecraft:white_wool",
        ),
        {
            "silhouette_exterior_identity": "Aevum recovery markings remain visible on an intact hospital wing now overwritten by emergency evacuation and triage colors",
            "interior_zoning_circulation": "dependent patients, triage beds, dwindling biologic issue points, evacuation holding areas and a blocked departure route turn normal recovery circulation into a humanitarian dilemma",
            "functional_machinery_props": "remaining cooler banks, ration crates, treatment cots and emergency staging show why patients could not simply be moved or taken off therapy",
            "institutional_identity": "Aevum medical identity survives underneath civilian emergency overlays, keeping the site focused on patient dependence rather than corporate villainy",
            "historical_damage_signature": "red triage zones, nearly empty cold storage and crowded white-cot holding areas show late-containment evacuation failing for medical rather than purely military reasons",
            "narrative_evidence_loot": "guaranteed Orlov dependency memorandum explains why continued APL production and delayed evacuation carried real human consequences",
        },
        "rare_sites",
    ),
)


def build_005():
    t = base.abandoned_orchard_cannery_clean_master()
    t.fill((6, 9, 8), (55, 11, 8), "minecraft:white_concrete")
    t.fill((12, 10, 7), (49, 13, 7), "minecraft:lime_concrete")
    t.fill((7, 1, 13), (23, 1, 20), "minecraft:light_blue_concrete")
    t.fill((8, 2, 15), (22, 2, 15), "create:fluid_pipe")
    t.fill((8, 2, 17), (11, 6, 19), "create:fluid_tank")
    for x in (27, 34, 41, 48):
        t.set(x, 2, 16, "create:depot")
        t.set(x, 3, 17, "create:mechanical_press", facing="north")
        t.fill((x - 1, 2, 21), (x + 2, 4, 23), "create:cardboard_block")
    for x in (29, 35, 41, 47):
        t.fill((x, 2, 28), (x + 2, 5, 31), "oritech:cooler_block")
    t.fill((8, 2, 28), (20, 4, 34), "jaffabricate:pallet_full")
    t.fill((45, 1, 33), (56, 1, 39), "minecraft:yellow_concrete")
    t.fill((47, 2, 34), (55, 4, 38), "create:cardboard_block")
    t.chest(52, 2, 36, "infinite_domain:chests/old_world/ows_005_vcf_harvest_packaging_annex", "west")
    return t


def build_007():
    t = base.nuclear_research_annex_clean_master()
    t.fill((5, 10, 10), (38, 12, 10), "minecraft:white_concrete")
    t.fill((12, 11, 9), (31, 14, 9), "minecraft:lime_concrete")
    for index, x in enumerate((8, 16, 24, 32), 1):
        t.fill((x, 2, 16), (x + 5, 8, 24), "create:framed_glass")
        t.clear((x + 1, 3, 17), (x + 4, 7, 23))
        t.fill((x + 1, 2, 18), (x + 4, 2, 22), "farmersdelight:rich_soil")
        if index % 2:
            t.fill((x + 2, 3, 19), (x + 3, 3, 21), "minecraft:wheat", age="7")
        else:
            t.fill((x + 2, 2, 19), (x + 3, 2, 21), "minecraft:mycelium")
            t.set(x + 2, 3, 20, "minecraft:brown_mushroom")
    for x in (45, 50, 55):
        t.fill((x, 2, 28), (x + 2, 6, 32), "oritech:cooler_block")
        t.fill((x, 2, 35), (x + 2, 4, 38), "immersiveengineering:crate")
    t.fill((10, 1, 42), (31, 1, 53), "minecraft:lime_concrete")
    for x in range(12, 30, 4):
        t.fill((x, 2, 44), (x + 2, 2, 51), "farmersdelight:rich_soil")
        t.fill((x + 1, 3, 46), (x + 1, 3, 49), "minecraft:wheat", age="7")
    t.chest(58, 2, 36, "infinite_domain:chests/old_world/ows_007_vcf_ep7_agricultural_development_laboratory", "west")
    return t


def build_008():
    t = base.mountain_biohazard_lab_clean_master()
    t.fill((19, 9, 3), (35, 11, 3), "minecraft:white_concrete")
    t.fill((22, 10, 2), (32, 13, 2), "minecraft:lime_concrete")
    for index, x in enumerate((7, 18, 29, 40), 1):
        t.fill((x, 2, 14), (x + 7, 8, 23), "create:framed_glass")
        t.clear((x + 1, 3, 15), (x + 6, 7, 22))
        t.fill((x + 1, 2, 25), (x + 6, 2, 27), "minecraft:yellow_concrete")
        t.fill((x + 2, 3, 26), (x + 5, 3, 26), "create:fluid_pipe")
        seam = x + min(index + 1, 6)
        t.fill((seam, 2, 20), (seam, 2, 22), "minecraft:mycelium")
        t.set(seam, 3, 21, "minecraft:brown_mushroom")
    t.fill((7, 1, 30), (49, 1, 34), "minecraft:yellow_concrete")
    t.fill((8, 2, 31), (48, 2, 31), "create:fluid_pipe")
    for x in (10, 22, 34, 46):
        t.fill((x, 2, 35), (x + 2, 4, 38), "minecraft:lime_concrete")
        t.fill((x, 2, 40), (x + 2, 4, 43), "immersiveengineering:crate")
    t.chest(47, 2, 41, "infinite_domain:chests/old_world/ows_008_vcf_emergency_persistence_investigation_lab", "west")
    return t


def build_011():
    t = base.fire_station_clean_master()
    t.fill((4, 8, 7), (38, 10, 7), "minecraft:orange_concrete")
    t.fill((9, 11, 6), (33, 13, 6), "minecraft:white_concrete")
    t.fill((14, 12, 5), (28, 14, 5), "minecraft:orange_concrete")
    for bay, x in enumerate((5, 16, 27), 1):
        t.fill((x, 1, 11), (x + 8, 1, 18), "minecraft:yellow_concrete")
        t.fill((x + 1, 2, 20), (x + 4, 3, 21), "create:andesite_casing")
        t.set(x + 2, 2, 23, "minecraft:anvil")
        t.fill((x + 5, 2, 20), (x + 7, 3, 22), "immersiveengineering:crate")
        t.fill((x + 1, 2, 25), (x + 6, 2, 26), "minecraft:orange_concrete")
    t.fill((28, 1, 24), (38, 1, 31), "minecraft:yellow_concrete")
    t.fill((29, 2, 25), (37, 5, 25), "minecraft:scaffolding")
    t.fill((31, 2, 27), (37, 4, 30), "create:andesite_casing")
    t.fill((5, 2, 32), (14, 5, 32), "minecraft:black_concrete")
    t.fill((6, 3, 31), (13, 4, 31), "minecraft:orange_concrete")
    t.chest(12, 2, 33, "infinite_domain:chests/old_world/ows_011_atlas_municipal_machine_service_shop", "west")
    return t


def build_013():
    t = base.create_factory_clean_master()
    t.fill((5, 10, 7), (41, 12, 7), "minecraft:orange_concrete")
    t.fill((12, 13, 6), (34, 15, 6), "minecraft:black_concrete")
    for index, x in enumerate((7, 16, 25, 34), 1):
        t.fill((x, 1, 11), (x + 6, 1, 28), "minecraft:orange_concrete")
        t.set(x + 2, 2, 15, "create:depot")
        t.set(x + 2, 3, 16, "create:mechanical_press", facing="north")
        t.fill((x + 1, 2, 21), (x + 4, 3, 22), "create:andesite_casing")
        t.fill((x + 1, 1, 29), (x + 5, 1, 31), "minecraft:yellow_concrete")
        t.fill((x + 2, 2, 30), (x + 4, 3, 30), "minecraft:polished_blackstone")
        t.set(x + 3, 3, 29, "minecraft:lever", face="wall", facing="north", powered="false")
    t.fill((34, 1, 12), (43, 1, 28), "minecraft:yellow_concrete")
    t.fill((36, 2, 20), (43, 5, 23), "minecraft:scaffolding")
    t.fill((37, 2, 25), (42, 4, 27), "create:andesite_casing")
    t.fill((6, 2, 32), (18, 4, 34), "immersiveengineering:crate")
    t.chest(15, 2, 33, "infinite_domain:chests/old_world/ows_013_atlas_automated_assembly_hall", "west")
    return t


def build_014():
    t = base.ae2_records_archive_clean_master()
    t.fill((6, 9, 10), (57, 11, 10), "minecraft:orange_concrete")
    t.fill((18, 22, 25), (58, 24, 25), "minecraft:light_blue_concrete")
    t.fill((34, 25, 33), (46, 27, 33), "minecraft:black_concrete")
    for x in (8, 15, 22):
        t.fill((x, 2, 14), (x + 3, 3, 16), "create:andesite_casing")
        t.set(x + 1, 2, 18, "create:depot")
        t.fill((x, 1, 20), (x + 3, 1, 22), "minecraft:orange_concrete")
        t.fill((x + 1, 2, 23), (x + 2, 3, 23), "minecraft:polished_blackstone")
        t.set(x + 1, 3, 22, "minecraft:lever", face="wall", facing="north", powered="false")
    t.fill((39, 13, 27), (57, 13, 28), "minecraft:orange_concrete")
    t.fill((41, 14, 30), (56, 14, 31), "minecraft:light_blue_concrete")
    t.fill((41, 14, 46), (56, 14, 47), "minecraft:black_concrete")
    t.fill((45, 14, 34), (55, 17, 36), "ae2:drive")
    t.fill((47, 14, 39), (53, 17, 42), "ae2:controller")
    t.fill((46, 14, 18), (55, 17, 20), "immersiveengineering:capacitor_hv")
    t.fill((34, 13, 43), (58, 13, 49), "minecraft:yellow_concrete")
    for x in (37, 43, 49, 55):
        t.fill((x, 14, 44), (x + 2, 15, 44), "minecraft:polished_blackstone")
        t.set(x + 1, 15, 43, "minecraft:lever", face="wall", facing="north", powered="false")
    t.chest(54, 14, 33, "infinite_domain:chests/old_world/ows_014_atlas_industrial_controls_integration_center", "west")
    return t


def build_029():
    t = base.bombed_hotel_clean_master()
    t.fill((17, 8, 4), (35, 9, 4), "minecraft:white_concrete")
    t.fill((21, 9, 3), (31, 12, 3), "minecraft:purple_concrete")
    for y in (14, 21, 28):
        for x in (14, 22, 30, 38):
            t.fill((x, y, 16), (x + 4, y, 19), "minecraft:smooth_quartz")
            t.fill((x, y + 1, 20), (x + 4, y + 3, 20), "create:framed_glass")
            t.set(x + 1, y + 1, 17, "minecraft:brewing_stand", has_bottle_0="false", has_bottle_1="false", has_bottle_2="false")
    t.fill((6, 2, 28), (10, 5, 31), "create:fluid_tank")
    t.fill((12, 1, 28), (39, 1, 31), "minecraft:purple_concrete")
    t.fill((13, 2, 29), (38, 3, 30), "minecraft:white_concrete")
    t.chest(44, 2, 35, "infinite_domain:chests/old_world/ows_029_aevum_longevity_treatment_center", "west")
    return t


def build_030():
    t = base.ruined_hospital_clean_master()
    t.fill((15, 9, 7), (51, 11, 7), "minecraft:white_concrete")
    t.fill((23, 10, 6), (43, 13, 6), "minecraft:purple_concrete")
    for x in (8, 16, 24, 32):
        t.fill((x, 2, 14), (x + 5, 2, 20), "minecraft:smooth_quartz")
        t.set(x + 1, 3, 16, "minecraft:brewing_stand", has_bottle_0="false", has_bottle_1="false", has_bottle_2="false")
        t.fill((x + 4, 3, 17), (x + 5, 5, 19), "create:fluid_tank")
    for x in (44, 49, 54):
        t.fill((x, 2, 15), (x + 2, 5, 20), "oritech:cooler_block")
    t.fill((42, 1, 22), (61, 1, 27), "minecraft:yellow_concrete")
    t.fill((44, 2, 23), (59, 4, 26), "immersiveengineering:crate")
    t.chest(58, 2, 18, "infinite_domain:chests/old_world/ows_030_aevum_apl_hospital_recovery_ward", "west")
    return t


def build_031():
    t = base.grocery_clean_master()
    t.fill((14, 8, 7), (24, 11, 7), "minecraft:white_concrete")
    t.fill((16, 9, 6), (22, 10, 6), "minecraft:purple_concrete")
    for x in (5, 9, 13, 17, 21, 25):
        t.fill((x, 2, 20), (x + 1, 5, 22), "oritech:cooler_block")
    t.fill((5, 1, 24), (29, 1, 27), "minecraft:yellow_concrete")
    t.fill((6, 2, 25), (14, 4, 27), "immersiveengineering:crate")
    t.fill((16, 2, 25), (22, 3, 27), "create:cardboard_block")
    t.fill((24, 2, 24), (29, 4, 27), "minecraft:purple_concrete")
    t.chest(27, 2, 26, "infinite_domain:chests/old_world/ows_031_aevum_biologic_pharmacy_cold_store", "west")
    return t


def build_032():
    t = base.mountain_biohazard_lab_clean_master()
    t.fill((19, 9, 3), (35, 11, 3), "minecraft:white_concrete")
    t.fill((22, 10, 2), (32, 13, 2), "minecraft:purple_concrete")
    t.clear((7, 2, 14), (49, 8, 27))
    for index, x in enumerate((8, 18, 28, 38), 1):
        t.fill((x, 2, 15), (x + 7, 7, 23), "create:framed_glass")
        t.clear((x + 1, 3, 16), (x + 6, 6, 22))
        t.fill((x + 1, 2, 17), (x + 6, 2, 21), "minecraft:smooth_quartz")
        t.set(x + 2, 3, 18, "minecraft:brewing_stand", has_bottle_0="false", has_bottle_1="false", has_bottle_2="false")
        t.fill((x + 4, 3, 19), (x + 5, 5, 21), "create:fluid_tank")
        t.fill((x, 1, 25), (x + index + 2, 1, 27), "minecraft:yellow_concrete")
    t.fill((7, 1, 30), (24, 1, 34), "minecraft:lime_concrete")
    t.fill((8, 2, 31), (14, 4, 33), "immersiveengineering:crate")
    for x in (30, 35, 40, 45):
        t.fill((x, 2, 31), (x + 2, 5, 34), "oritech:cooler_block")
    t.chest(47, 2, 32, "infinite_domain:chests/old_world/ows_032_aevum_apl3_research_campus", "west")
    return t


def build_033():
    t = base.ruined_hospital_clean_master()
    t.fill((15, 9, 7), (51, 11, 7), "minecraft:white_concrete")
    t.fill((23, 10, 6), (43, 13, 6), "minecraft:purple_concrete")
    t.fill((5, 1, 28), (61, 1, 37), "minecraft:yellow_concrete")
    for row, z in enumerate((29, 33)):
        for col, x in enumerate((7, 15, 23, 31, 39, 47)):
            t.fill((x, 2, z), (x + 4, 2, z + 2), "minecraft:white_wool")
            if (row + col) % 3 == 0:
                t.fill((x, 1, z), (x + 4, 1, z + 2), "minecraft:red_concrete")
    for x in (50, 54, 58):
        t.fill((x, 2, 40), (x + 2, 5, 44), "oritech:cooler_block")
    t.fill((45, 1, 46), (63, 1, 53), "minecraft:red_concrete")
    t.fill((47, 2, 47), (61, 4, 50), "immersiveengineering:crate")
    t.fill((5, 1, 47), (36, 1, 53), "minecraft:yellow_concrete")
    t.fill((7, 2, 48), (34, 4, 52), "minecraft:white_wool")
    t.chest(58, 2, 51, "infinite_domain:chests/old_world/ows_033_aevum_evacuation_dependency_ward", "west")
    return t


# OWS-009 was already a materially distinct Atlas service depot, but its spec
# omitted the sixth dimension. Preserve its pre-crisis character by making the
# ordinary repaired-bay baseline explicit and physically enforceable.
_core_build_009 = core.BUILDERS["OWS-009"]
_core_spec_009 = next(spec for spec in core.SPECS if spec.target == "OWS-009")


def build_009():
    t = _core_build_009()
    # Ordinary pre-crisis wear: repaired guard rail plus swapped casing stock.
    t.fill((5, 2, 12), (5, 4, 13), "minecraft:oxidized_copper_grate")
    t.fill((6, 1, 12), (8, 1, 13), "minecraft:black_concrete")
    t.fill((7, 2, 12), (8, 3, 13), "create:andesite_casing")
    return t


spec_009 = core.Spec(
    _core_spec_009.target,
    _core_spec_009.name,
    _core_spec_009.source_id,
    _core_spec_009.source_profile,
    _core_spec_009.proof,
    _core_spec_009.lore,
    _core_spec_009.phase,
    tuple(dict.fromkeys(_core_spec_009.required_blocks + ("minecraft:oxidized_copper_grate",))),
    {
        **_core_spec_009.dimensions,
        "historical_damage_signature": "ordinary pre-crisis service wear is preserved as a repaired bay guard, replacement casing stock and intact calibration baseline rather than crisis ruin",
    },
    _core_spec_009.set_name,
)

EXTENSIONS = VCF_COMPLETION + ATLAS_EXTENSION + AEVUM_EXTENSION + tuple(later.SPECS)
core.SPECS = tuple(
    sorted(
        tuple(spec_009 if spec.target == "OWS-009" else spec for spec in core.SPECS) + EXTENSIONS,
        key=lambda spec: int(spec.target[-3:]),
    )
)
core.BY_TARGET.update({spec.target: spec for spec in core.SPECS})
core.BUILDERS.update({
    "OWS-005": build_005,
    "OWS-007": build_007,
    "OWS-008": build_008,
    "OWS-009": build_009,
    "OWS-011": build_011,
    "OWS-013": build_013,
    "OWS-014": build_014,
    "OWS-029": build_029,
    "OWS-030": build_030,
    "OWS-031": build_031,
    "OWS-032": build_032,
    "OWS-033": build_033,
    **later.BUILDERS,
})

Spec = core.Spec
SPECS = core.SPECS
BY_TARGET = core.BY_TARGET
BUILDERS = core.BUILDERS


def _write_controlled_worldgen_activation() -> None:
    structure_set_dir = DATA / "worldgen" / "structure_set" / "old_world"
    structure_set_dir.mkdir(parents=True, exist_ok=True)
    for stale in structure_set_dir.glob("*.json"):
        stale.unlink()

    members = [BY_TARGET[target] for target in CONTROLLED_WORLDGEN_TARGETS]
    base.write_json(
        structure_set_dir / "controlled_pt9_probe.json",
        {
            "structures": [
                {"structure": spec.structure_id, "weight": 1}
                for spec in members
            ],
            "placement": {
                "type": "minecraft:random_spread",
                "spacing": 160,
                "separation": 80,
                "salt": 90310609,
            },
        },
    )


def sync_registry() -> None:
    targets_path = REGISTRY / "structure_targets.json"
    if not targets_path.is_file():
        return
    document = json.loads(targets_path.read_text(encoding="utf-8"))
    targets = document["targets"]
    for spec in SPECS:
        is_probe = spec.target in CONTROLLED_WORLDGEN_TARGETS
        row = targets[int(spec.target[-3:]) - 1]
        row.update({
            "implementation_status": "implemented_static_runtime_deferred",
            "mapped_source_structure": spec.source_id,
            "narrative_structure": spec.structure_id,
            "narrative_source_template": f"kubejs/data/infinite_domain/structure/wasteland/old_world/{spec.name}.nbt",
            "acceptance_dimensions": list(spec.dimensions),
            "runtime_validation": "pending_controlled_test" if is_probe else "deferred",
            "worldgen_activation": "controlled_pt9_probe" if is_probe else "staged_not_in_structure_set",
            "locator": {
                "command": f"/structure_map {spec.structure_id} 2",
                "status": "controlled_probe_ready" if is_probe else "prepared_requires_worldgen_activation",
            },
            "exploration_hook": {
                "mode": "additive_old_world_investigation",
                "status": "prepared_static",
                "requires_worldgen_activation": not is_probe,
            },
        })
        if spec.target in DARKNET_RETURN_TARGETS:
            row["darknet_return_hook"] = {
                "status": "reserved_for_later_darknet_phase",
                "purpose": DARKNET_RETURN_TARGETS[spec.target],
            }
        else:
            row.pop("darknet_return_hook", None)

    targets_path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8", newline="\n")

    state_path = REGISTRY / "implementation_state.json"
    if state_path.is_file():
        state = json.loads(state_path.read_text(encoding="utf-8"))
        implemented = sorted(spec.target for spec in SPECS)
        state["static_implemented"] = implemented
        render_path = PROGRAM / "reviews" / "render-manifest.json"
        rendered = set()
        if render_path.is_file():
            rendered = {
                entry["structure_id"]
                for entry in json.loads(render_path.read_text(encoding="utf-8")).get("structures", [])
            }
        state["static_render_reviewed"] = sorted(
            spec.target for spec in SPECS if spec.structure_id in rendered
        )
        state["controlled_worldgen_targets"] = list(CONTROLLED_WORLDGEN_TARGETS)
        state["production_worldgen_status"] = "staged_pending_runtime_validation"
        state["darknet_return_targets_reserved"] = sorted(DARKNET_RETURN_TARGETS)
        state["current_wave"] = later.CURRENT_WAVE
        implemented_set = set(implemented)
        state["next_targets"] = [
            row["id"] for row in targets
            if row["id"] not in implemented_set and row.get("implementation_status") == "approved_for_mapping"
        ][:5]
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    for spec in SPECS:
        core.generate(spec)
    _write_controlled_worldgen_activation()
    sync_registry()
    print(
        f"Generated {len(SPECS)} static Old World sites; "
        f"controlled worldgen target(s): {', '.join(CONTROLLED_WORLDGEN_TARGETS)}."
    )


if __name__ == "__main__":
    main()
