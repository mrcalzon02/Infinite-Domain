#!/usr/bin/env python3
"""Final civilian, municipal and Asterion Old World implementation waves.

Pure implementation data/builders. The authoritative Old World generator owns
all generation, registry synchronization and worldgen activation.
"""
from __future__ import annotations

import old_world_narrative_core as core

base = core.base

FINAL_EXTENSION = (
    core.Spec(
        "OWS-054",
        "ows_054_civilian_neighborhood_shelter",
        "infinite_domain:emergency_relief_shelter_clean_master",
        "emergency_relief_shelter",
        "kubejs:shelter_resident_log",
        "kubejs:shelter_resident_log",
        "Active containment",
        (
            "minecraft:white_wool",
            "minecraft:yellow_concrete",
            "minecraft:black_concrete",
            "immersiveengineering:crate",
            "create:cardboard_block",
        ),
        {
            "silhouette_exterior_identity": "the existing civic shelter remains visually modest, with improvised yellow wayfinding and crowded relief stock rather than institutional branding",
            "interior_zoning_circulation": "registration, family sleeping, single sleeping, clinic, food service, stores and resident information remain a complete civilian shelter workflow",
            "functional_machinery_props": "cots, food crates, cardboard personal stores, basic medical stock and information boards show prolonged civilian occupancy",
            "institutional_identity": "civilian identity is expressed through personal belongings, handwritten-style information areas and municipal hazard markings rather than a corporate color system",
            "historical_damage_signature": "overflow bedding and shrinking supply zones show active containment stretching an intact shelter beyond its intended capacity",
            "narrative_evidence_loot": "guaranteed shelter resident log records ordinary people adapting daily routines to a crisis they still expected institutions to survive",
        },
        "common_sites",
    ),
    core.Spec(
        "OWS-055",
        "ows_055_municipal_transit_closure_station",
        "infinite_domain:ruined_bus_terminal_clean_master",
        "ruined_bus_terminal",
        "kubejs:transit_emergency_closure_notice",
        "kubejs:transit_emergency_closure_notice",
        "Late containment",
        (
            "minecraft:red_concrete",
            "minecraft:yellow_concrete",
            "minecraft:white_concrete",
            "minecraft:oxidized_copper_grate",
            "immersiveengineering:crate",
        ),
        {
            "silhouette_exterior_identity": "municipal white transit markings survive beneath red closure bands across the terminal and boarding bays",
            "interior_zoning_circulation": "ticket hall, waiting area, closed platforms, emergency reroute desk, stranded baggage and blocked vehicle exits remain readable",
            "functional_machinery_props": "barriers, closure gates, abandoned baggage stock and emergency supply crates convert a normal terminal into a controlled shutdown site",
            "institutional_identity": "municipal transit identity remains visible underneath emergency red/yellow overlays, emphasizing service withdrawal rather than military seizure",
            "historical_damage_signature": "entire boarding bays are physically blocked while the main building remains standing, showing infrastructure being deliberately shut before destruction",
            "narrative_evidence_loot": "guaranteed transit emergency closure notice documents the moment public mobility ceased to be treated as sustainable during late containment",
        },
        "common_sites",
    ),
    core.Spec(
        "OWS-056",
        "ows_056_municipal_water_waste_failure_plant",
        "infinite_domain:city_water_treatment_plant_clean_master",
        "city_water_treatment_plant",
        "kubejs:municipal_water_integrity_log",
        "kubejs:municipal_water_integrity_log",
        "Active containment",
        (
            "create:fluid_tank",
            "create:fluid_pipe",
            "create:mechanical_pump",
            "minecraft:yellow_concrete",
            "minecraft:red_concrete",
            "immersiveengineering:crate",
        ),
        {
            "silhouette_exterior_identity": "the treatment plant retains its municipal process silhouette while yellow isolation and red failed-process markings spread across pump and filtration zones",
            "interior_zoning_circulation": "intake, clarification, filtration, disinfection, pump-out, maintenance and rejected-process routes remain physically understandable",
            "functional_machinery_props": "tanks, pumps, fluid lines, chemical stores and isolated service stock make water continuity dependent on the same failing materials seen elsewhere",
            "institutional_identity": "municipal utility markings remain utilitarian and unbranded, connecting the crisis directly to ordinary public-service infrastructure",
            "historical_damage_signature": "some process trains remain active beside red-isolated lines and staged replacement parts, showing a plant losing redundancy one subsystem at a time",
            "narrative_evidence_loot": "guaranteed municipal water integrity log records repeated seal, pump and contamination problems threatening both potable water and waste handling",
        },
        "uncommon_sites",
    ),
    core.Spec(
        "OWS-057",
        "ows_057_civilian_apartment_evacuation_block",
        "infinite_domain:tenement_courtyard_clean_master",
        "tenement_courtyard",
        "kubejs:apartment_evacuate_or_wait_note",
        "kubejs:apartment_evacuate_or_wait_note",
        "Late containment",
        (
            "minecraft:red_concrete",
            "minecraft:yellow_concrete",
            "minecraft:white_wool",
            "create:cardboard_block",
            "immersiveengineering:crate",
        ),
        {
            "silhouette_exterior_identity": "the ordinary residential block remains recognizable while evacuation arrows, red closed entrances and courtyard staging overwrite normal neighborhood circulation",
            "interior_zoning_circulation": "apartments, shared stairs, courtyard assembly, household packing, evacuation queue and abandoned units preserve the civilian decision path",
            "functional_machinery_props": "packed boxes, emergency cots, small supply caches and blocked exits make evacuation a household logistics problem rather than an abstract event",
            "institutional_identity": "civilian belongings dominate the site; government markings exist only as directional overlays and closure zones",
            "historical_damage_signature": "some homes are packed for departure while others remain occupied or abandoned in place, physically preserving the choice between evacuating and waiting",
            "narrative_evidence_loot": "guaranteed evacuate-or-wait note captures the uncertainty of civilians deciding whether official evacuation was safer than remaining home",
        },
        "common_sites",
    ),
    core.Spec(
        "OWS-058",
        "ows_058_municipal_library_refuge_center",
        "infinite_domain:ruined_community_center_clean_master",
        "ruined_community_center",
        "kubejs:refuge_information_board_log",
        "kubejs:refuge_information_board_log",
        "Late containment",
        (
            "minecraft:bookshelf",
            "minecraft:white_wool",
            "minecraft:black_concrete",
            "minecraft:yellow_concrete",
            "immersiveengineering:crate",
        ),
        {
            "silhouette_exterior_identity": "the civic building remains recognizable while municipal refuge markings and a large public-information zone replace its ordinary community program",
            "interior_zoning_circulation": "information desk, reading/reference area, sleeping hall, relief issue, family waiting and municipal notices create a combined library-refuge workflow",
            "functional_machinery_props": "bookshelves, cots, relief crates and dense information boards show a civic information institution becoming a survival coordination point",
            "institutional_identity": "municipal identity is expressed through public information and service organization rather than fortified control",
            "historical_damage_signature": "reference and meeting spaces are progressively consumed by bedding and relief stock as late containment displaces normal civic life",
            "narrative_evidence_loot": "guaranteed refuge information board log reconstructs changing closures, aid locations and contradictory public guidance during the final civilian phase",
        },
        "uncommon_sites",
    ),
    core.Spec(
        "OWS-059",
        "ows_059_municipal_school_distribution_relief_point",
        "infinite_domain:ruined_city_school_clean_master",
        "ruined_city_school",
        "kubejs:school_relief_distribution_record",
        "kubejs:school_relief_distribution_record",
        "Early containment",
        (
            "immersiveengineering:crate",
            "create:cardboard_block",
            "minecraft:white_wool",
            "minecraft:yellow_concrete",
            "minecraft:lime_concrete",
        ),
        {
            "silhouette_exterior_identity": "the school campus retains its educational identity while yellow municipal relief lanes and temporary distribution markings occupy the gym and cafeteria approaches",
            "interior_zoning_circulation": "registration, food issue, household supply issue, temporary rest, school stores and outbound family flow remain legible",
            "functional_machinery_props": "stacked relief crates, packaged goods, cots and food-distribution stock turn familiar school spaces into an emergency neighborhood hub",
            "institutional_identity": "municipal relief markings sit beside intact classroom and school architecture, reinforcing that normal institutions were repurposed rather than instantly abandoned",
            "historical_damage_signature": "the campus is largely intact and busy, establishing an early-containment baseline before later refuge sites become overcrowded and desperate",
            "narrative_evidence_loot": "guaranteed school relief distribution record shows local government still moving food and household supplies through ordinary community infrastructure",
        },
        "common_sites",
    ),
    core.Spec(
        "OWS-060",
        "ows_060_asterion_launch_support_warehouse",
        "infinite_domain:corporate_warehouse_clean_master",
        "corporate_warehouse",
        "kubejs:asterion_launch_support_manifest",
        "kubejs:asterion_launch_support_manifest",
        "Late containment",
        (
            "minecraft:blue_concrete",
            "minecraft:white_concrete",
            "minecraft:black_concrete",
            "immersiveengineering:crate",
            "create:andesite_casing",
            "minecraft:yellow_concrete",
        ),
        {
            "silhouette_exterior_identity": "Asterion blue-and-white aerospace logistics bands convert the corporate warehouse into a recognizable launch-support depot",
            "interior_zoning_circulation": "precision receiving, flight hardware storage, life-support stores, mission-kit packing and secure outbound staging remain separated",
            "functional_machinery_props": "crated components, casing stock, sealed mission packages and marked outbound hardware show a launch program consuming industrial supply at emergency tempo",
            "institutional_identity": "Asterion blue/white aerospace markings establish a distinct institution whose work continues alongside terrestrial collapse",
            "historical_damage_signature": "yellow priority lanes and partially emptied high-value stores show launch support accelerating during late containment rather than shutting down",
            "narrative_evidence_loot": "guaranteed launch support manifest proves the space program remained materially active while regional infrastructure was failing",
        },
        "uncommon_sites",
    ),
    core.Spec(
        "OWS-061",
        "ows_061_asterion_mission_control_relay_center",
        "infinite_domain:ae2_records_archive_clean_master",
        "ae2_records_archive",
        "kubejs:asterion_mission_relay_log",
        "kubejs:asterion_mission_relay_log",
        "Firebreak Wars",
        (
            "minecraft:blue_concrete",
            "minecraft:white_concrete",
            "minecraft:black_concrete",
            "ae2:drive",
            "ae2:controller",
            "immersiveengineering:capacitor_hv",
            "minecraft:red_concrete",
        ),
        {
            "silhouette_exterior_identity": "Asterion blue mission-control bands and a white-black communications crown convert the hardened archive shell into an active relay center",
            "interior_zoning_circulation": "operator gallery, mission data core, orbital relay, backup power, emergency communications and protected records remain distinct",
            "functional_machinery_props": "controller clusters, drive banks, backup capacitors and redundant communications storage make mission continuity mechanically visible",
            "institutional_identity": "Asterion aerospace blue remains dominant even as red Firebreak-era emergency overlays invade control spaces",
            "historical_damage_signature": "redundant relay routes and red emergency sectors show mission control operating through terrestrial network fragmentation",
            "narrative_evidence_loot": "guaranteed mission relay log documents continued contact with off-world assets during the Firebreak Wars",
        },
        "rare_sites",
    ),
    core.Spec(
        "OWS-062",
        "ows_062_asterion_orbital_communications_station",
        "infinite_domain:radio_mast_clean_master",
        "radio_mast",
        "kubejs:asterion_orbital_contact_record",
        "kubejs:asterion_orbital_contact_record",
        "Firebreak Wars",
        (
            "minecraft:blue_concrete",
            "minecraft:white_concrete",
            "minecraft:black_concrete",
            "ae2:drive",
            "minecraft:observer",
            "minecraft:light_blue_concrete",
        ),
        {
            "silhouette_exterior_identity": "the communications mast gains an Asterion blue/white orbital-tracking cabin and instrument crown while retaining its long-range relay silhouette",
            "interior_zoning_circulation": "ground communications support, tracking equipment, vertical service route, upper relay instrumentation and protected contact archive remain readable",
            "functional_machinery_props": "sensor arrays, data storage and hardened relay hardware physically support persistent orbital communications",
            "institutional_identity": "Asterion aerospace colors distinguish orbital traffic from Blackglass terrestrial networking despite shared data technology",
            "historical_damage_signature": "the station remains structurally useful despite terrestrial collapse, emphasizing communications persistence rather than destruction",
            "narrative_evidence_loot": "guaranteed orbital contact record proves that off-world crews or systems were still reachable while the surface crisis escalated",
        },
        "rare_sites",
    ),
    core.Spec(
        "OWS-063",
        "ows_063_asterion_spacecraft_assembly_facility",
        "infinite_domain:create_factory_clean_master",
        "abandoned_create_factory",
        "kubejs:asterion_assembly_evacuations_order",
        "kubejs:asterion_assembly_evacuations_order",
        "Late containment",
        (
            "minecraft:blue_concrete",
            "minecraft:white_concrete",
            "minecraft:black_concrete",
            "create:andesite_casing",
            "create:mechanical_press",
            "create:fluid_tank",
            "immersiveengineering:crate",
            "minecraft:red_concrete",
        ),
        {
            "silhouette_exterior_identity": "Asterion blue high-bay assembly markings and a white aerospace crown transform the Create factory lineage into a spacecraft production hall",
            "interior_zoning_circulation": "component receiving, structural assembly cells, systems integration, tank/service preparation, inspection and evacuation staging form a clear production sequence",
            "functional_machinery_props": "presses, casings, fluid tanks, integration stock and mission crates make advanced vehicle assembly legible using the pack's industrial language",
            "institutional_identity": "Asterion aerospace branding overlays recognizable Atlas/Create-style automation, showing the space program drawing on the wider industrial base",
            "historical_damage_signature": "red evacuation lanes cut through an otherwise active assembly floor, showing personnel withdrawal occurring before all spacecraft work stopped",
            "narrative_evidence_loot": "guaranteed assembly evacuations order records the conflict between preserving launch capability and removing workers from a collapsing region",
        },
        "rare_sites",
    ),
    core.Spec(
        "OWS-064",
        "ows_064_asterion_primary_meridian_launch_complex",
        "infinite_domain:collapsed_airship_terminal_clean_master",
        "collapsed_airship_terminal",
        "kubejs:asterion_primary_launch_archive",
        "kubejs:asterion_primary_launch_archive",
        "Firebreak Wars -> Post-collapse",
        (
            "minecraft:blue_concrete",
            "minecraft:white_concrete",
            "minecraft:black_concrete",
            "minecraft:red_concrete",
            "minecraft:yellow_concrete",
            "immersiveengineering:concrete_reinforced",
            "immersiveengineering:crate",
            "ae2:drive",
        ),
        {
            "silhouette_exterior_identity": "the large airship-terminal lineage is repurposed into an Asterion launch landmark with blue/white terminal identity, hardened berths and an unmistakable launch-support field",
            "interior_zoning_circulation": "arrival, mission processing, crew staging, cargo handling, launch-control archive, hardened departure route and abandoned emergency sectors remain distinct",
            "functional_machinery_props": "reinforced launch aprons, mission crates, data archives, service stock and protected control points make the complex function as a terrestrial gateway to off-world infrastructure",
            "institutional_identity": "Asterion blue/white identity dominates the landmark while red Firebreak emergency fields document the collapse occurring around an institution still trying to launch",
            "historical_damage_signature": "closed passenger areas, fortified launch access and abandoned emergency staging preserve the transition from active launch center to post-collapse archaeological landmark",
            "narrative_evidence_loot": "guaranteed primary launch archive closes the Old World physical sequence by preserving launch records, emergency decisions and the final relationship between surface collapse and off-world continuity",
        },
        "rare_sites",
    ),
)


def build_054():
    t = base.emergency_relief_shelter_clean_master()
    t.fill((4, 1, 12), (44, 1, 14), "minecraft:yellow_concrete")
    t.fill((5, 2, 16), (43, 2, 31), "minecraft:white_wool")
    for x in (7, 15, 23, 31, 39):
        t.fill((x, 2, 17), (x + 2, 2, 19), "create:cardboard_block")
        t.fill((x, 2, 24), (x + 2, 2, 26), "immersiveengineering:crate")
    t.fill((17, 2, 9), (31, 5, 10), "minecraft:black_concrete")
    t.fill((32, 2, 33), (43, 4, 37), "immersiveengineering:crate")
    t.chest(41, 2, 36, "infinite_domain:chests/old_world/ows_054_civilian_neighborhood_shelter", "west")
    return t


def build_055():
    t = base.ruined_bus_terminal_clean_master()
    t.fill((5, 15, 8), (40, 17, 8), "minecraft:white_concrete")
    t.fill((7, 1, 18), (39, 1, 31), "minecraft:yellow_concrete")
    t.fill((41, 1, 9), (60, 1, 49), "minecraft:red_concrete")
    for z in (10, 17, 24, 31, 38, 45):
        t.fill((42, 2, z), (56, 5, z), "minecraft:oxidized_copper_grate")
    t.fill((18, 2, 35), (26, 5, 40), "immersiveengineering:crate")
    t.chest(37, 2, 36, "infinite_domain:chests/old_world/ows_055_municipal_transit_closure_station", "west")
    return t


def build_056():
    t = base.city_water_treatment_plant_clean_master()
    for x in (7, 20, 33, 46):
        t.fill((x, 1, 48), (x + 10, 1, 52), "minecraft:yellow_concrete")
        t.fill((x + 1, 2, 49), (x + 3, 6, 51), "create:fluid_tank")
        t.fill((x + 4, 2, 50), (x + 8, 2, 50), "create:fluid_pipe")
        t.set(x + 7, 2, 52, "create:mechanical_pump", facing="south")
    t.fill((55, 1, 33), (71, 1, 40), "minecraft:red_concrete")
    t.fill((57, 2, 42), (69, 4, 46), "immersiveengineering:crate")
    t.chest(68, 2, 52, "infinite_domain:chests/old_world/ows_056_municipal_water_waste_failure_plant", "west")
    return t


def build_057():
    t = base.tenement_courtyard_clean_master()
    t.fill((18, 1, 8), (39, 1, 34), "minecraft:yellow_concrete")
    for x in (20, 27, 34):
        t.fill((x, 2, 12), (x + 4, 3, 16), "create:cardboard_block")
        t.fill((x, 2, 20), (x + 4, 2, 23), "minecraft:white_wool")
    t.fill((18, 1, 35), (39, 1, 42), "minecraft:red_concrete")
    t.fill((20, 2, 37), (37, 4, 41), "immersiveengineering:crate")
    t.chest(35, 2, 39, "infinite_domain:chests/old_world/ows_057_civilian_apartment_evacuation_block", "west")
    return t


def build_058():
    t = base.ruined_community_center_clean_master()
    t.fill((18, 7, 4), (32, 9, 4), "minecraft:white_concrete")
    for x in (6, 12, 18):
        t.fill((x, 2, 12), (x + 2, 6, 20), "minecraft:bookshelf")
    t.fill((22, 1, 15), (46, 1, 31), "minecraft:white_wool")
    for x in (24, 31, 38):
        t.fill((x, 2, 18), (x + 4, 2, 21), "minecraft:white_wool")
        t.fill((x, 2, 24), (x + 4, 4, 27), "immersiveengineering:crate")
    t.fill((5, 2, 32), (20, 6, 34), "minecraft:black_concrete")
    t.fill((22, 1, 33), (46, 1, 39), "minecraft:yellow_concrete")
    t.chest(42, 2, 36, "infinite_domain:chests/old_world/ows_058_municipal_library_refuge_center", "west")
    return t


def build_059():
    t = base.ruined_city_school_clean_master()
    t.fill((5, 18, 7), (59, 20, 7), "minecraft:white_concrete")
    t.fill((6, 1, 32), (40, 1, 49), "minecraft:yellow_concrete")
    for x in (8, 16, 24, 32):
        t.fill((x, 2, 35), (x + 5, 4, 39), "immersiveengineering:crate")
        t.fill((x, 2, 42), (x + 5, 3, 45), "create:cardboard_block")
    t.fill((43, 1, 31), (60, 1, 49), "minecraft:lime_concrete")
    for x in (45, 52):
        t.fill((x, 2, 34), (x + 5, 2, 39), "minecraft:white_wool")
    t.chest(56, 2, 45, "infinite_domain:chests/old_world/ows_059_municipal_school_distribution_relief_point", "west")
    return t


def build_060():
    t = base.corporate_warehouse_clean_master()
    t.fill((15, 12, 8), (45, 14, 8), "minecraft:white_concrete")
    t.fill((20, 13, 7), (40, 15, 7), "minecraft:blue_concrete")
    for x in (17, 23, 29, 35, 41):
        t.fill((x, 1, 12), (x + 3, 1, 30), "minecraft:blue_concrete")
        t.fill((x, 2, 14), (x + 3, 5, 19), "immersiveengineering:crate")
        t.fill((x, 2, 22), (x + 3, 4, 27), "create:andesite_casing")
    t.fill((16, 1, 33), (45, 1, 38), "minecraft:yellow_concrete")
    t.fill((18, 2, 34), (43, 4, 37), "minecraft:black_concrete")
    t.chest(43, 2, 15, "infinite_domain:chests/old_world/ows_060_asterion_launch_support_warehouse", "west")
    return t


def build_061():
    t = base.ae2_records_archive_clean_master()
    t.fill((6, 9, 10), (57, 11, 10), "minecraft:blue_concrete")
    t.fill((18, 22, 25), (58, 24, 25), "minecraft:white_concrete")
    t.fill((34, 25, 33), (46, 27, 33), "minecraft:black_concrete")
    t.fill((45, 14, 34), (55, 17, 36), "ae2:drive")
    t.fill((47, 14, 39), (53, 17, 42), "ae2:controller")
    t.fill((46, 14, 18), (55, 17, 20), "immersiveengineering:capacitor_hv")
    t.fill((34, 13, 43), (58, 13, 49), "minecraft:red_concrete")
    t.chest(54, 14, 33, "infinite_domain:chests/old_world/ows_061_asterion_mission_control_relay_center", "west")
    return t


def build_062():
    t = base.radio_mast_clean_master()
    t.fill((1, 1, 1), (4, 6, 5), "minecraft:blue_concrete")
    t.clear((2, 2, 2), (3, 5, 4))
    t.fill((1, 6, 1), (4, 7, 5), "minecraft:white_concrete")
    t.fill((1, 1, 6), (4, 2, 7), "minecraft:black_concrete")
    t.fill((2, 2, 3), (3, 4, 3), "ae2:drive")
    for x, z in ((5, 5), (9, 5), (5, 9), (9, 9)):
        t.set(x, 3, z, "minecraft:observer", facing="up", powered="false")
    t.fill((5, 1, 10), (10, 1, 12), "minecraft:light_blue_concrete")
    t.chest(3, 2, 2, "infinite_domain:chests/old_world/ows_062_asterion_orbital_communications_station", "south")
    return t


def build_063():
    t = base.create_factory_clean_master()
    t.fill((5, 10, 7), (41, 12, 7), "minecraft:blue_concrete")
    t.fill((12, 13, 6), (34, 15, 6), "minecraft:white_concrete")
    for x in (7, 16, 25, 34):
        t.fill((x, 1, 11), (x + 6, 1, 28), "minecraft:blue_concrete")
        t.set(x + 2, 2, 15, "create:depot")
        t.set(x + 2, 3, 16, "create:mechanical_press", facing="north")
        t.fill((x + 1, 2, 21), (x + 4, 4, 23), "create:andesite_casing")
        t.fill((x + 1, 2, 25), (x + 4, 5, 27), "create:fluid_tank")
    t.fill((6, 1, 29), (42, 1, 30), "minecraft:black_concrete")
    t.fill((6, 1, 31), (42, 1, 34), "minecraft:red_concrete")
    t.fill((8, 2, 32), (40, 4, 34), "immersiveengineering:crate")
    t.chest(38, 2, 33, "infinite_domain:chests/old_world/ows_063_asterion_spacecraft_assembly_facility", "west")
    return t


def build_064():
    t = base.collapsed_airship_terminal_clean_master()
    t.fill((5, 20, 7), (45, 22, 7), "minecraft:blue_concrete")
    t.fill((15, 9, 4), (35, 11, 4), "minecraft:white_concrete")
    t.fill((47, 1, 8), (64, 1, 48), "immersiveengineering:concrete_reinforced")
    t.fill((49, 2, 10), (62, 2, 20), "minecraft:blue_concrete")
    t.fill((49, 2, 25), (62, 2, 35), "minecraft:white_concrete")
    t.fill((49, 2, 40), (62, 2, 47), "minecraft:red_concrete")
    t.fill((7, 1, 35), (43, 1, 47), "minecraft:yellow_concrete")
    for x in (9, 17, 25, 33):
        t.fill((x, 2, 38), (x + 5, 5, 43), "immersiveengineering:crate")
    t.fill((37, 2, 12), (44, 6, 18), "ae2:drive")
    t.fill((37, 2, 21), (44, 5, 25), "minecraft:black_concrete")
    t.chest(42, 2, 16, "infinite_domain:chests/old_world/ows_064_asterion_primary_meridian_launch_complex", "west")
    return t

SPECS = FINAL_EXTENSION
BUILDERS = {
    "OWS-054": build_054,
    "OWS-055": build_055,
    "OWS-056": build_056,
    "OWS-057": build_057,
    "OWS-058": build_058,
    "OWS-059": build_059,
    "OWS-060": build_060,
    "OWS-061": build_061,
    "OWS-062": build_062,
    "OWS-063": build_063,
    "OWS-064": build_064,
}
CURRENT_WAVE = "old_world_full_source_coverage_ows_001_through_064"
