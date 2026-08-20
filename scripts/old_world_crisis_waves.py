#!/usr/bin/env python3
"""Crisis-era Old World implementation components.

This module is data/build logic only. It is consumed through old_world_later_waves
by the sole authoritative Old World generator; it never generates or mutates
repository state on import.
"""
from __future__ import annotations

import old_world_narrative_core as core

base = core.base

CRISIS_EXTENSION = (
    core.Spec(
        "OWS-044",
        "ows_044_emergency_authority_early_quarantine_checkpoint",
        "infinite_domain:military_checkpoint_clean_master",
        "military_checkpoint",
        "kubejs:quarantine_inspection_pass",
        "kubejs:quarantine_inspection_pass",
        "Early containment",
        (
            "minecraft:white_concrete",
            "minecraft:yellow_concrete",
            "minecraft:light_blue_concrete",
            "minecraft:oxidized_copper_grate",
            "immersiveengineering:crate",
        ),
        {
            "silhouette_exterior_identity": "temporary white-and-yellow public-health markings overlay an otherwise ordinary road checkpoint, keeping the site visibly provisional",
            "interior_zoning_circulation": "approach lane, inspection stop, document check, accepted route, rejected holding strip and supply hut remain immediately readable",
            "functional_machinery_props": "inspection crates, temporary barriers, marked lanes and small screening stations show a checkpoint designed to buy time rather than seal a region",
            "institutional_identity": "Emergency Authority white/yellow control markings sit above still-visible civilian road infrastructure rather than military occupation branding",
            "historical_damage_signature": "the checkpoint is mostly intact and lightly fortified, establishing that early quarantine still functioned locally before later escalation",
            "narrative_evidence_loot": "guaranteed quarantine inspection pass demonstrates that local screening and movement controls initially remained bureaucratic and selective",
        },
        "common_sites",
    ),
    core.Spec(
        "OWS-045",
        "ows_045_emergency_authority_late_quarantine_fortress",
        "infinite_domain:military_checkpoint_clean_master",
        "military_checkpoint",
        "kubejs:continuity_perimeter_fragment",
        "kubejs:continuity_perimeter_fragment",
        "Late containment",
        (
            "immersiveengineering:concrete_reinforced",
            "minecraft:oxidized_copper_grate",
            "minecraft:red_concrete",
            "minecraft:yellow_concrete",
            "minecraft:white_concrete",
            "immersiveengineering:crate",
        ),
        {
            "silhouette_exterior_identity": "the same road-checkpoint lineage is buried under reinforced blocks, grates and red closure markings until it reads as a fortress rather than a screening post",
            "interior_zoning_circulation": "multiple stop lines, inspection pocket, sealed rejection lane, guarded passage and emergency stock turn simple traffic control into a hardened perimeter",
            "functional_machinery_props": "reinforced barriers, layered gates, stock crates and permanent exclusion lanes show quarantine consuming increasing material and manpower",
            "institutional_identity": "Emergency Authority markings remain visible beneath Continuity-adjacent perimeter fragments and increasingly militarized closure colors",
            "historical_damage_signature": "red permanently closed lanes and duplicated barriers demonstrate a late-containment doctrine built around shrinking passable corridors",
            "narrative_evidence_loot": "guaranteed Continuity perimeter fragment records the transition from selective quarantine to hardened territorial separation",
        },
        "uncommon_sites",
    ),
    core.Spec(
        "OWS-046",
        "ows_046_emergency_authority_regional_decontamination_interchange",
        "infinite_domain:abandoned_truck_stop_clean_master",
        "abandoned_truck_stop",
        "kubejs:decontamination_failure_record",
        "kubejs:decontamination_failure_record",
        "Active containment",
        (
            "minecraft:white_concrete",
            "minecraft:yellow_concrete",
            "create:fluid_tank",
            "create:fluid_pipe",
            "create:mechanical_pump",
            "minecraft:oxidized_copper_grate",
            "immersiveengineering:crate",
        ),
        {
            "silhouette_exterior_identity": "the truck-service complex is overlaid by white decontamination canopies, yellow lane coding and visible fluid-processing equipment",
            "interior_zoning_circulation": "dirty vehicle queue, wash lane, personnel transfer, clean-side inspection, rejected holding and outbound route form a complete regional decon sequence",
            "functional_machinery_props": "fluid tanks, pumps, wash manifolds, grated separators and chemical-stock crates make decontamination a real logistical process",
            "institutional_identity": "Emergency Authority lane colors and repeated dirty/clean boundaries transform commercial road infrastructure into containment infrastructure",
            "historical_damage_signature": "later wash lanes are isolated despite intact equipment, showing procedural decontamination failing even before the interchange is physically destroyed",
            "narrative_evidence_loot": "guaranteed decontamination failure record documents repeat-positive traffic after complete wash cycles and undermines faith in clean-side certification",
        },
        "uncommon_sites",
    ),
    core.Spec(
        "OWS-047",
        "ows_047_joint_research_deep_containment_laboratory",
        "infinite_domain:mountain_biohazard_lab_clean_master",
        "mountain_biohazard_lab",
        "kubejs:deep_containment_incident_record",
        "kubejs:deep_containment_incident_record",
        "Active containment",
        (
            "immersiveengineering:concrete_reinforced",
            "immersiveengineering:sheetmetal_steel",
            "create:framed_glass",
            "minecraft:mycelium",
            "minecraft:brown_mushroom",
            "minecraft:yellow_concrete",
            "minecraft:red_concrete",
        ),
        {
            "silhouette_exterior_identity": "joint-agency white markings are subordinated to reinforced deep-containment shells and red/yellow isolation bands around the secure laboratory",
            "interior_zoning_circulation": "sample intake, outer barrier, inner barrier, observation chamber, independent utilities and incident archive require deliberate nested boundary crossings",
            "functional_machinery_props": "reinforced shells, steel inner walls, sealed observation glass and isolated support stock make the laboratory's containment doctrine physically legible",
            "institutional_identity": "mixed institutional colors are intentionally minimized in favor of joint-research containment numbering, showing multiple organizations pooling resources",
            "historical_damage_signature": "fungal growth appears inside an apparently intact inner chamber while outer barriers remain standing, making containment failure spatial rather than rhetorical",
            "narrative_evidence_loot": "guaranteed deep containment incident record documents contamination discovered beyond multiple intact engineered barriers",
        },
        "rare_sites",
    ),
    core.Spec(
        "OWS-048",
        "ows_048_meridian_military_containment_base",
        "infinite_domain:mountain_military_complex_clean_master",
        "mountain_military_complex",
        "kubejs:containment_command_directive",
        "kubejs:containment_command_directive",
        "Late containment",
        (
            "immersiveengineering:concrete_reinforced",
            "minecraft:red_concrete",
            "minecraft:yellow_concrete",
            "minecraft:oxidized_copper_grate",
            "immersiveengineering:crate",
            "minecraft:orange_concrete",
        ),
        {
            "silhouette_exterior_identity": "the fortified mountain garrison gains large red containment sectors and yellow controlled-movement corridors without losing its military compound silhouette",
            "interior_zoning_circulation": "command, protected logistics, containment staging, equipment issue, restricted perimeter and troop movement remain separate enough to read operationally",
            "functional_machinery_props": "reinforced positions, barrier corridors, emergency crates and staged engineering stock show military power being redirected toward containment logistics",
            "institutional_identity": "Meridian military red/orange command markings dominate while Emergency Authority yellow survives at controlled civilian interfaces",
            "historical_damage_signature": "sealed internal sectors and duplicated perimeter lines show the base increasingly defending itself from the same environment it was ordered to contain",
            "narrative_evidence_loot": "guaranteed containment command directive records the military transition from supporting civil quarantine to commanding regional containment operations",
        },
        "rare_sites",
    ),
    core.Spec(
        "OWS-049",
        "ows_049_meridian_firebreak_observation_bunker",
        "infinite_domain:bunker_network_clean_master",
        "bunker_network",
        "kubejs:firebreak_operations_record",
        "kubejs:firebreak_operations_record",
        "Firebreak",
        (
            "immersiveengineering:concrete_reinforced",
            "minecraft:red_concrete",
            "minecraft:orange_concrete",
            "minecraft:yellow_concrete",
            "ae2:drive",
            "immersiveengineering:crate",
        ),
        {
            "silhouette_exterior_identity": "the civil-defense bunker is converted into an orange/red Firebreak observation post with protected viewing and hardened records spaces",
            "interior_zoning_circulation": "observation intake, operations room, protected communications, blast monitoring, supply reserve and sealed fallback compartments remain legible",
            "functional_machinery_props": "hardened data storage, command tables, reserve crates and reinforced observation positions support sustained monitoring of destructive containment actions",
            "institutional_identity": "Meridian Firebreak orange/red operation markings replace earlier civilian shelter identity while yellow hazard boundaries remain",
            "historical_damage_signature": "sealed fallback rooms and emergency reserve placement show observers expecting their own perimeter to fail while operations continue",
            "narrative_evidence_loot": "guaranteed Firebreak operations record documents the shift from quarantine and decontamination to deliberate destructive exclusion operations",
        },
        "rare_sites",
    ),
    core.Spec(
        "OWS-050",
        "ows_050_meridian_firebreak_crater_command_site",
        "infinite_domain:cratered_downtown_intersection_clean_master",
        "cratered_downtown_intersection",
        "kubejs:firebreak_site_six_after_action",
        "kubejs:firebreak_site_six_after_action",
        "Firebreak -> Post-collapse",
        (
            "minecraft:gravel",
            "immersiveengineering:concrete_reinforced",
            "minecraft:red_concrete",
            "minecraft:orange_concrete",
            "minecraft:black_concrete",
            "immersiveengineering:crate",
        ),
        {
            "silhouette_exterior_identity": "a cratered urban intersection is converted into a command landmark with reinforced observation points and orange/red Firebreak markings around the blast edge",
            "interior_zoning_circulation": "crater perimeter, command pocket, observation lane, protected records point and abandoned emergency stock create a readable after-action site",
            "functional_machinery_props": "reinforced command blocks, staged crates, marked blast sectors and surviving communications positions make the Firebreak event materially reconstructable",
            "institutional_identity": "Meridian command colors survive only in fragments around a landscape-scale destructive intervention, visually subordinated to the crater itself",
            "historical_damage_signature": "the central command area is literally organized around a large cleared impact zone, turning post-operation destruction into the site's defining architecture",
            "narrative_evidence_loot": "guaranteed Site Six after-action record ties the crater to a specific Firebreak operation and preserves the military assessment of its failure or limited success",
        },
        "rare_sites",
    ),
    core.Spec(
        "OWS-051",
        "ows_051_continuity_science_atmospheric_monitoring_station_19k",
        "infinite_domain:wasteland_fire_lookout_clean_master",
        "wasteland_fire_lookout",
        "kubejs:nineteen_kilometer_detection_record",
        "kubejs:nineteen_kilometer_detection_record",
        "Late containment",
        (
            "minecraft:white_concrete",
            "minecraft:light_blue_concrete",
            "minecraft:black_concrete",
            "ae2:drive",
            "minecraft:observer",
            "minecraft:yellow_concrete",
        ),
        {
            "silhouette_exterior_identity": "the remote lookout becomes a Continuity science tower through white/cyan sensor markings and a dark instrument crown while retaining its long-range observation silhouette",
            "interior_zoning_circulation": "ground support, instrument access, vertical monitoring route, upper analysis cabin and protected record point follow the existing tower circulation",
            "functional_machinery_props": "observer arrays, data storage and marked sampling positions turn a lookout into a plausible atmospheric monitoring station",
            "institutional_identity": "Continuity science uses restrained white/cyan technical markings rather than corporate branding, emphasizing cross-disciplinary field work",
            "historical_damage_signature": "yellow contamination-distance marks accumulate at a station that is otherwise intact, emphasizing the terrifying range of detection rather than structural collapse",
            "narrative_evidence_loot": "guaranteed nineteen-kilometer detection record proves viable atmospheric detection far outside the presumed local containment perimeter",
        },
        "rare_sites",
    ),
    core.Spec(
        "OWS-052",
        "ows_052_continuity_field_office",
        "infinite_domain:ruined_cyberware_clinic_clean_master",
        "ruined_cyberware_clinic",
        "kubejs:continuity_crossdisciplinary_fragment",
        "kubejs:continuity_crossdisciplinary_fragment",
        "Active containment",
        (
            "minecraft:white_concrete",
            "minecraft:light_blue_concrete",
            "minecraft:black_concrete",
            "create:framed_glass",
            "ae2:drive",
            "immersiveengineering:crate",
        ),
        {
            "silhouette_exterior_identity": "a repurposed clinic/office receives restrained Continuity white/cyan field markings while its civilian origin remains deliberately visible",
            "interior_zoning_circulation": "sample intake, biology desk, materials desk, logistics board, shared analysis room and protected records point make cross-disciplinary work spatially obvious",
            "functional_machinery_props": "small sealed work cells, data storage, sample crates and shared analysis stations show a field team synthesizing evidence rather than running one specialized laboratory",
            "institutional_identity": "Continuity identity is intentionally composite and low-key, allowing traces of VCF, PolyCore, Pleroma and Helion evidence to coexist in the same office",
            "historical_damage_signature": "the site remains functional but crowded with evidence from multiple failing systems, making information overload rather than physical destruction the central signature",
            "narrative_evidence_loot": "guaranteed cross-disciplinary fragment records the moment separate agricultural, material, logistics and atmospheric anomalies are recognized as one system",
        },
        "uncommon_sites",
    ),
    core.Spec(
        "OWS-053",
        "ows_053_continuity_archive_landmark",
        "infinite_domain:ae2_records_archive_clean_master",
        "ae2_records_archive",
        "kubejs:distributed_reservoir_summary",
        "kubejs:distributed_reservoir_summary",
        "Late containment -> Firebreak",
        (
            "minecraft:white_concrete",
            "minecraft:light_blue_concrete",
            "minecraft:black_concrete",
            "ae2:drive",
            "ae2:controller",
            "immersiveengineering:concrete_reinforced",
            "minecraft:red_concrete",
        ),
        {
            "silhouette_exterior_identity": "the hardened records campus becomes a Continuity landmark through a large white/cyan archive crown and visibly reinforced secure core",
            "interior_zoning_circulation": "evidence intake, cross-disciplinary stacks, central archive core, protected analysis, emergency duplication and sealed Firebreak-era records remain distinct",
            "functional_machinery_props": "dense data drives, controllers, reinforced archive zones and duplicated storage physically express Continuity's attempt to preserve a systemic picture of the catastrophe",
            "institutional_identity": "Continuity white/cyan markings unify records from previously separate institutions without erasing their source colors inside the archive",
            "historical_damage_signature": "red sealed archive sectors and duplicated data stores show late-containment researchers assuming facilities and networks would soon be lost",
            "narrative_evidence_loot": "guaranteed distributed reservoir summary records the conclusion that contamination existed across many environmental and infrastructural reservoirs rather than one breach point",
        },
        "rare_sites",
    ),
)


def build_044():
    t = base.military_checkpoint_clean_master()
    t.fill((2, 1, 10), (42, 1, 10), "minecraft:yellow_concrete")
    t.fill((2, 1, 20), (42, 1, 20), "minecraft:yellow_concrete")
    t.fill((15, 1, 11), (20, 1, 19), "minecraft:white_concrete")
    t.fill((16, 2, 12), (19, 4, 14), "immersiveengineering:crate")
    t.fill((25, 1, 11), (31, 1, 19), "minecraft:light_blue_concrete")
    t.fill((32, 1, 10), (32, 5, 20), "minecraft:oxidized_copper_grate")
    t.chest(18, 2, 16, "infinite_domain:chests/old_world/ows_044_emergency_authority_early_quarantine_checkpoint", "west")
    return t


def build_045():
    t = base.military_checkpoint_clean_master()
    t.fill((3, 1, 8), (41, 4, 9), "immersiveengineering:concrete_reinforced")
    t.fill((3, 1, 21), (41, 4, 22), "immersiveengineering:concrete_reinforced")
    t.fill((8, 1, 10), (13, 1, 20), "minecraft:yellow_concrete")
    t.fill((15, 1, 10), (29, 1, 20), "minecraft:red_concrete")
    t.fill((31, 1, 10), (37, 1, 20), "minecraft:white_concrete")
    t.fill((14, 2, 10), (14, 7, 20), "minecraft:oxidized_copper_grate")
    t.fill((30, 2, 10), (30, 7, 20), "minecraft:oxidized_copper_grate")
    t.fill((34, 2, 23), (41, 4, 27), "immersiveengineering:crate")
    t.chest(38, 2, 25, "infinite_domain:chests/old_world/ows_045_emergency_authority_late_quarantine_fortress", "west")
    return t


def build_046():
    t = base.abandoned_truck_stop_clean_master()
    for x in (5, 15, 25, 35):
        t.fill((x, 1, 10), (x + 7, 1, 31), "minecraft:yellow_concrete")
        t.fill((x + 1, 2, 14), (x + 3, 6, 18), "create:fluid_tank")
        t.fill((x + 1, 2, 21), (x + 5, 2, 21), "create:fluid_pipe")
        t.set(x + 3, 2, 23, "create:mechanical_pump", facing="south")
        t.fill((x, 2, 28), (x + 7, 5, 28), "minecraft:oxidized_copper_grate")
    t.fill((6, 2, 34), (22, 4, 39), "immersiveengineering:crate")
    t.fill((29, 1, 34), (45, 1, 40), "minecraft:white_concrete")
    t.chest(42, 2, 37, "infinite_domain:chests/old_world/ows_046_emergency_authority_regional_decontamination_interchange", "west")
    return t


def build_047():
    t = base.mountain_biohazard_lab_clean_master()
    t.fill((19, 9, 3), (35, 11, 3), "minecraft:white_concrete")
    t.fill((28, 13, 13), (51, 15, 13), "immersiveengineering:concrete_reinforced")
    t.fill((28, 1, 17), (51, 1, 20), "minecraft:yellow_concrete")
    t.clear((29, 2, 17), (50, 8, 34))
    t.fill((29, 2, 18), (50, 8, 18), "immersiveengineering:concrete_reinforced")
    t.fill((29, 2, 34), (50, 8, 34), "immersiveengineering:concrete_reinforced")
    t.fill((29, 2, 18), (29, 8, 34), "immersiveengineering:concrete_reinforced")
    t.fill((50, 2, 18), (50, 8, 34), "immersiveengineering:concrete_reinforced")
    t.fill((33, 2, 22), (46, 7, 22), "immersiveengineering:sheetmetal_steel")
    t.fill((33, 2, 30), (46, 7, 30), "immersiveengineering:sheetmetal_steel")
    t.fill((33, 2, 22), (33, 7, 30), "immersiveengineering:sheetmetal_steel")
    t.fill((46, 2, 22), (46, 7, 30), "immersiveengineering:sheetmetal_steel")
    t.fill((35, 2, 24), (44, 6, 29), "create:framed_glass")
    t.clear((36, 3, 25), (43, 5, 28))
    t.fill((36, 2, 25), (43, 2, 28), "minecraft:mycelium")
    for x, z in ((37, 26), (39, 27), (41, 26), (42, 28)):
        t.set(x, 3, z, "minecraft:brown_mushroom")
    t.fill((28, 1, 35), (51, 1, 39), "minecraft:red_concrete")
    t.chest(47, 2, 38, "infinite_domain:chests/old_world/ows_047_joint_research_deep_containment_laboratory", "west")
    return t


def build_048():
    t = base.mountain_military_complex_clean_master()
    t.fill((4, 1, 4), (56, 1, 9), "minecraft:orange_concrete")
    t.fill((4, 1, 11), (56, 1, 17), "minecraft:yellow_concrete")
    t.fill((6, 2, 20), (54, 2, 22), "minecraft:red_concrete")
    t.fill((6, 3, 23), (54, 6, 24), "minecraft:oxidized_copper_grate")
    t.fill((8, 2, 28), (20, 5, 34), "immersiveengineering:crate")
    t.fill((24, 2, 28), (38, 5, 34), "immersiveengineering:concrete_reinforced")
    t.fill((42, 2, 28), (54, 5, 34), "immersiveengineering:crate")
    t.fill((10, 1, 38), (52, 1, 44), "minecraft:red_concrete")
    t.chest(48, 2, 32, "infinite_domain:chests/old_world/ows_048_meridian_military_containment_base", "west")
    return t


def build_049():
    t = base.bunker_network_clean_master()
    t.fill((4, 2, 4), (42, 3, 4), "minecraft:orange_concrete")
    t.fill((7, 2, 9), (39, 2, 12), "minecraft:red_concrete")
    t.fill((8, 3, 14), (20, 6, 18), "ae2:drive")
    t.fill((24, 3, 14), (39, 5, 18), "immersiveengineering:crate")
    t.fill((7, 2, 22), (39, 2, 25), "minecraft:yellow_concrete")
    t.fill((8, 3, 27), (38, 5, 31), "immersiveengineering:concrete_reinforced")
    t.fill((27, 2, 34), (40, 2, 40), "minecraft:red_concrete")
    t.chest(22, 2, 22, "infinite_domain:chests/old_world/ows_049_meridian_firebreak_observation_bunker", "east")
    return t


def build_050():
    t = base.cratered_downtown_intersection_clean_master()
    t.clear((22, 6, 22), (42, 22, 42))
    t.fill((22, 5, 22), (42, 5, 42), "minecraft:gravel")
    t.clear((27, 5, 27), (37, 5, 37))
    t.fill((8, 6, 24), (19, 10, 39), "immersiveengineering:concrete_reinforced")
    t.clear((9, 7, 25), (18, 9, 38))
    t.fill((8, 6, 23), (19, 6, 23), "minecraft:orange_concrete")
    t.fill((8, 6, 40), (19, 6, 40), "minecraft:red_concrete")
    t.fill((10, 7, 28), (17, 9, 31), "immersiveengineering:crate")
    t.fill((43, 5, 23), (57, 5, 42), "minecraft:black_concrete")
    t.chest(15, 7, 35, "infinite_domain:chests/old_world/ows_050_meridian_firebreak_crater_command_site", "west")
    return t


def build_051():
    t = base.wasteland_fire_lookout_clean_master()
    t.fill((8, 27, 8), (28, 29, 8), "minecraft:white_concrete")
    t.fill((8, 27, 26), (28, 29, 26), "minecraft:light_blue_concrete")
    for x, z in ((12, 12), (17, 12), (22, 12), (12, 22), (17, 22), (22, 22)):
        t.set(x, 29, z, "minecraft:observer", facing="up", powered="false")
    t.fill((13, 29, 16), (21, 31, 18), "ae2:drive")
    t.fill((11, 28, 20), (23, 28, 23), "minecraft:black_concrete")
    t.fill((10, 1, 27), (25, 1, 31), "minecraft:yellow_concrete")
    t.chest(17, 29, 20, "infinite_domain:chests/old_world/ows_051_continuity_science_atmospheric_monitoring_station_19k", "north")
    return t


def build_052():
    t = base.ruined_cyberware_clinic_clean_master()
    t.fill((5, 10, 10), (53, 12, 10), "minecraft:white_concrete")
    t.fill((11, 11, 9), (47, 14, 9), "minecraft:light_blue_concrete")
    t.clear((7, 2, 13), (32, 8, 23))
    for index, x in enumerate((8, 16, 24), 1):
        t.fill((x, 2, 14), (x + 5, 7, 21), "create:framed_glass")
        t.clear((x + 1, 3, 15), (x + 4, 6, 20))
        t.fill((x + 1, 2, 16), (x + 4, 2, 19), ("minecraft:lime_concrete", "minecraft:magenta_concrete", "minecraft:orange_concrete")[index - 1])
    t.fill((38, 2, 14), (50, 5, 17), "ae2:drive")
    t.fill((38, 2, 20), (50, 4, 23), "immersiveengineering:crate")
    t.fill((36, 1, 25), (52, 1, 29), "minecraft:black_concrete")
    t.chest(47, 2, 21, "infinite_domain:chests/old_world/ows_052_continuity_field_office", "west")
    return t


def build_053():
    t = base.ae2_records_archive_clean_master()
    t.fill((6, 9, 10), (57, 11, 10), "minecraft:white_concrete")
    t.fill((18, 22, 25), (58, 24, 25), "minecraft:light_blue_concrete")
    t.fill((34, 25, 33), (46, 27, 33), "minecraft:black_concrete")
    for x in (9, 17, 25, 33, 41, 49):
        t.fill((x, 14, 30), (x + 3, 17, 33), "ae2:drive")
    t.fill((44, 14, 36), (55, 17, 40), "ae2:controller")
    t.fill((41, 13, 42), (58, 13, 49), "minecraft:red_concrete")
    t.fill((42, 14, 43), (57, 18, 48), "immersiveengineering:concrete_reinforced")
    t.clear((44, 15, 44), (55, 17, 47))
    t.fill((10, 13, 42), (32, 13, 49), "minecraft:light_blue_concrete")
    t.chest(54, 14, 33, "infinite_domain:chests/old_world/ows_053_continuity_archive_landmark", "west")
    return t

SPECS = CRISIS_EXTENSION
BUILDERS = {
    "OWS-044": build_044,
    "OWS-045": build_045,
    "OWS-046": build_046,
    "OWS-047": build_047,
    "OWS-048": build_048,
    "OWS-049": build_049,
    "OWS-050": build_050,
    "OWS-051": build_051,
    "OWS-052": build_052,
    "OWS-053": build_053,
}
CURRENT_WAVE = "continuity_archive_functional_coverage_and_pt9_controlled_runtime_probe"
