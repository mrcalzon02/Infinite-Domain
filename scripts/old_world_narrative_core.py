#!/usr/bin/env python3
"""Generate the approved, locatable Old World narrative structure wave."""
from __future__ import annotations
import gzip
from dataclasses import dataclass
from pathlib import Path
import generate_wasteland_sites as base

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "kubejs" / "data" / "infinite_domain"

@dataclass(frozen=True)
class Spec:
    target: str; name: str; source_id: str; source_profile: str
    proof: str; lore: str | None; phase: str
    required_blocks: tuple[str, ...]; dimensions: dict[str, str]
    set_name: str = "common_sites"
    @property
    def structure_id(self): return f"infinite_domain:old_world/{self.name}"
    @property
    def loot_id(self): return f"infinite_domain:chests/old_world/{self.name}"

SPECS = (
    Spec("OWS-001", "ows_001_vcf_neighborhood_culture_service_depot", "infinite_domain:grocery_clean_master", "grocery", "kubejs:vcf_culture_service_manifest", "kubejs:vcf_return_crate_log", "Pre-crisis to early anomaly", ("minecraft:lime_concrete", "oritech:cooler_block", "immersiveengineering:crate"), {
        "silhouette_exterior_identity": "VCF green service blade and culture-drop canopy replace retail branding",
        "interior_zoning_circulation": "public issue counter, refrigerated culture lockers, return sorting and receiving remain legible",
        "functional_machinery_props": "cooler banks, sealed culture crates, return pallets and service workbench",
        "institutional_identity": "VCF green/white wayfinding and controlled issue-return workflow",
        "historical_damage_signature": "one quarantined cooler bay and backed-up return lane show the first supply anomaly",
        "narrative_evidence_loot": "guaranteed culture-service manifest and return-crate log establish mundane Evercrop ubiquity"}),
    Spec("OWS-002", "ows_002_vcf_emergency_community_grow_hall", "infinite_domain:ruined_community_center_clean_master", "ruined_community_center", "kubejs:emergency_grow_authorization", None, "Early containment", ("minecraft:lime_concrete", "minecraft:wheat", "create:fluid_pipe", "immersiveengineering:crate"), {
        "silhouette_exterior_identity": "municipal relief chevrons and a VCF green hall crown identify emergency food service",
        "interior_zoning_circulation": "intake, culture-kit issue, two-tier grow rows, harvest aisle and relief dispatch form a public workflow",
        "functional_machinery_props": "irrigated cultivation racks, culture crates, wash point and palletized relief stock",
        "institutional_identity": "municipal white/yellow relief markings are visibly overlaid by VCF green culture logistics",
        "historical_damage_signature": "one isolated rack and overflow dispatch lane show early containment pressure without ruin",
        "narrative_evidence_loot": "guaranteed emergency grow authorization proves governments deployed Evercrop for food security"}),
    Spec("OWS-003", "ows_003_vcf_cold_chain_culture_nursery", "infinite_domain:abandoned_orchard_cannery_clean_master", "abandoned_orchard_cannery", "kubejs:vcf_culture_batch_record", "kubejs:vcf_global_licensing_brief", "Early anomaly", ("minecraft:lime_concrete", "oritech:cooler_block", "create:framed_glass", "minecraft:yellow_concrete"), {
        "silhouette_exterior_identity": "VCF green cold-chain bands and cyan loading marks replace cannery branding",
        "interior_zoning_circulation": "receiving, cold vault, dormancy nursery, batch inspection and dispatch remain sequential",
        "functional_machinery_props": "cooler banks, sealed nursery cells, batch benches and shipping racks",
        "institutional_identity": "VCF batch colors and global-license routing turn food processing into culture logistics",
        "historical_damage_signature": "minor gasket quarantine zones and rerouted batches show the early material anomaly",
        "narrative_evidence_loot": "guaranteed batch record and LOR-005 licensing brief connect dormancy to worldwide distribution"}),
    Spec("OWS-004", "ows_004_vcf_mycological_vertical_farm_tower", "infinite_domain:ruined_office_tower_clean_master", "ruined_office_tower", "kubejs:evercrop_cultivation_handbook", "kubejs:evercrop_cultivation_handbook", "Pre-crisis to active containment", ("minecraft:lime_concrete", "minecraft:mycelium", "minecraft:brown_mushroom", "create:fluid_tank", "create:depot"), {
        "silhouette_exterior_identity": "VCF green cultivation bands and a luminous rooftop greenhouse replace corporate office branding",
        "interior_zoning_circulation": "public demonstration podium, four cultivation floors, nutrient risers, harvest transfer and packaging remain legible",
        "functional_machinery_props": "mycelial grow rows, nutrient tanks, harvest depots and packaging stock operate floor by floor",
        "institutional_identity": "clean VCF green/white public optimism contrasts with controlled yellow production zones",
        "historical_damage_signature": "the upper cultivation floor is sealed for active containment while lower floors remain productive",
        "narrative_evidence_loot": "guaranteed LOR-001 handbook is primary physical proof of industrial fungal agriculture"}, "uncommon_sites"),
    Spec("OWS-006", "ows_006_vcf_pt9_symbiosis_pilot_laboratory", "infinite_domain:ruined_cyberware_clinic_clean_master", "ruined_cyberware_clinic", "kubejs:pt9_symbiosis_report", "kubejs:pt9_symbiosis_report", "Early anomaly", ("minecraft:lime_concrete", "create:framed_glass", "minecraft:brewing_stand", "tfmg:plastic_block", "minecraft:yellow_concrete"), {
        "silhouette_exterior_identity": "VCF green pilot-lab blade and sterile white frontage replace clinic identity",
        "interior_zoning_circulation": "sample intake, three symbiosis chambers, bacterial controls, polymer observation and secure records are separated",
        "functional_machinery_props": "sealed culture chambers, reagent stations, polymer coupons and comparative control benches",
        "institutional_identity": "VCF test numbering and green/cyan bioscience zoning frame PT-9 as a useful product",
        "historical_damage_signature": "one yellow-isolated polymer observation bay records degradation before researchers understood the consequence",
        "narrative_evidence_loot": "guaranteed LOR-003 report names PT-9 and records both bacterial protection and polymer degradation"}, "rare_sites"),
    Spec("OWS-009", "ows_009_atlas_roadside_repair_depot", "infinite_domain:service_garage_clean_master", "service_garage", "kubejs:atlas_service_plate", "kubejs:atlas_transfer_maintenance_manual", "Phase A — pre-crisis / normal operation", ("minecraft:orange_concrete", "create:mechanical_press", "create:depot", "create:andesite_casing"), {
        "silhouette_exterior_identity": "orange Atlas facade band and roofline service blade",
        "interior_zoning_circulation": "three marked service stages with preserved work and customer routes",
        "functional_machinery_props": "two press/depot stations, calibration bench, parts cages and service stock",
        "institutional_identity": "Atlas color, emblem, standardized lanes, controlled records cage",
        "narrative_evidence_loot": "guaranteed Atlas service plate and LOR-006 maintenance manual"}),
    Spec("OWS-010", "ows_010_atlas_conveyor_transfer_hall", "infinite_domain:corporate_warehouse_clean_master", "corporate_warehouse", "kubejs:atlas_transfer_maintenance_card", None, "Pre-crisis to early anomaly", ("minecraft:orange_concrete", "create:depot", "create:mechanical_press", "create:andesite_casing"), {
        "silhouette_exterior_identity": "Atlas orange dock crowns and a high-bay transfer glyph read from the truck court",
        "interior_zoning_circulation": "receiving, four transfer lanes, cross-aisle and maintenance catwalk access remain distinct",
        "functional_machinery_props": "depot/press cells, drive casings, sort benches and guarded service trench",
        "institutional_identity": "numbered orange lanes and Atlas lockout stations standardize the hall",
        "historical_damage_signature": "a cannibalized fourth lane and staged spare casings record shrinking maintenance capacity",
        "narrative_evidence_loot": "guaranteed transfer-maintenance card bridges player Create knowledge to Old World industry"}),
    Spec("OWS-012", "ows_012_atlas_bulk_crushing_preparation_plant", "infinite_domain:abandoned_quarry_clean_master", "abandoned_quarry", "kubejs:atlas_bulk_process_manual", None, "Early anomaly", ("minecraft:orange_concrete", "create:crushing_wheel", "create:millstone", "create:mechanical_mixer", "create:encased_fan"), {
        "silhouette_exterior_identity": "Atlas orange crusher crowns and service-house band mark the quarry rim from a distance",
        "interior_zoning_circulation": "bench haul route, bulk feed, crushing, milling, mixing, dust extraction and service dispatch form a continuous process",
        "functional_machinery_props": "crushing wheels, millstones, mixer basin, dust fans, feed casings and maintenance stock",
        "institutional_identity": "Atlas lane numbering and orange lockout fields standardize a sophisticated bulk plant",
        "historical_damage_signature": "one isolated crusher cell and cannibalized casing bank show rapidly growing maintenance cost",
        "narrative_evidence_loot": "guaranteed bulk-process manual documents sophisticated throughput and worsening service intervals"}, "uncommon_sites"),
    Spec("OWS-015", "ows_015_polycore_utility_seal_failure_station", "infinite_domain:wasteland_water_tower_clean_master", "wasteland_water_tower", "kubejs:polycore_seal_failure_report", "kubejs:polycore_service_interval_board", "Early anomaly", ("minecraft:magenta_concrete", "create:mechanical_pump", "create:fluid_pipe", "minecraft:yellow_concrete"), {
        "silhouette_exterior_identity": "PolyCore magenta pump-house band and seal-service pylon identify the utility compound",
        "interior_zoning_circulation": "intake, paired pumps, seal bench, replacement stock and records wall form a service loop",
        "functional_machinery_props": "paired pumps, pipe manifold, tagged gasket stock and maintenance isolation zone",
        "institutional_identity": "PolyCore color coding and decreasing inspection intervals cover the ordinary utility station",
        "historical_damage_signature": "yellow isolation marks and stacked replacement crates show recurring seal failures without collapse",
        "narrative_evidence_loot": "guaranteed failure report and LOR-008 interval board make the material crisis measurable"}),
    Spec("OWS-016", "ows_016_polycore_elastomer_exposure_array", "infinite_domain:mountain_biohazard_lab_clean_master", "mountain_biohazard_lab", "kubejs:polycore_elastomer_exposure_test", "kubejs:polycore_exposure_test_04", "Early anomaly", ("minecraft:magenta_concrete", "immersiveengineering:insulating_glass", "tfmg:plastic_block", "minecraft:yellow_concrete"), {
        "silhouette_exterior_identity": "PolyCore magenta pressure-zone cap and numbered test-wing blade distinguish the laboratory",
        "interior_zoning_circulation": "sample intake, four parallel exposure chambers, clean observation route and failed-material archive are separated",
        "functional_machinery_props": "sealed glass chambers, timed control banks, polymer samples and isolation stores",
        "institutional_identity": "PolyCore test numbering and magenta/white zone control make the repeated experiment legible",
        "historical_damage_signature": "progressively larger yellow isolation fields across chambers record reproducible biological degradation",
        "narrative_evidence_loot": "guaranteed test authorization and LOR-009 document the same elastomer failure four times"}, "uncommon_sites"),
    Spec("OWS-017", "ows_017_polycore_composite_barrier_laboratory", "infinite_domain:industrial_facility_clean_master", "industrial_facility", "kubejs:polycore_composite_failure_file", None, "Active containment", ("minecraft:magenta_concrete", "immersiveengineering:insulating_glass", "tfmg:plastic_block", "minecraft:quartz_block", "minecraft:yellow_concrete"), {
        "silhouette_exterior_identity": "PolyCore magenta test-hall bands and a white composite-lab crown distinguish the facility from its industrial donor",
        "interior_zoning_circulation": "receiving, coupon preparation, four barrier cells, inspection, failed-material quarantine and records dispatch form a readable test sequence",
        "functional_machinery_props": "sealed barrier cells, layered polymer-mineral coupons, retained process equipment and inspection benches support repeated composite trials",
        "institutional_identity": "PolyCore magenta/white zone coding and numbered barrier cells present composite substitution as an organized emergency research program",
        "historical_damage_signature": "later cells carry widening yellow isolation fields, breached laminate coupons and repair stock as active containment defeats successively stronger barriers",
        "narrative_evidence_loot": "guaranteed composite failure file proves the material crisis had escalated beyond ordinary elastomers into engineered barrier systems"}, "uncommon_sites"),
    Spec("OWS-018", "ows_018_polycore_ceramic_isolation_test_center", "infinite_domain:nuclear_research_annex_clean_master", "nuclear_research_annex", "kubejs:polycore_ceramic_isolation_result", None, "Active containment", ("minecraft:magenta_concrete", "immersiveengineering:insulating_glass", "minecraft:polished_diorite", "minecraft:quartz_block", "immersiveengineering:sheetmetal_steel", "minecraft:yellow_concrete"), {
        "silhouette_exterior_identity": "PolyCore magenta retrofit bands and a white ceramic-isolation crown distinguish the annex while preserving its containment silhouette",
        "interior_zoning_circulation": "three bench-scale isolation cells progress from ceramic to ceramic-metal hybrid trials before the route reaches the full-scale containment chamber and records store",
        "functional_machinery_props": "insulating-glass observation cells, mineral barrier coupons, steel backing plates, retrofit stock and the retained containment plant support comparative isolation testing",
        "institutional_identity": "PolyCore magenta/white zone coding and numbered ceramic test bays make the emergency substitution program legible without rebuilding the donor architecture",
        "historical_damage_signature": "successive cells show larger isolation fields and localized breaches while the full-scale ring carries a patched ceramic-metal shell, demonstrating delay rather than immunity",
        "narrative_evidence_loot": "guaranteed ceramic isolation result records that non-polymer barriers extended service life but still failed after environmental contamination"}, "rare_sites"),
    Spec("OWS-019", "ows_019_polycore_emergency_material_substitution_center", "infinite_domain:corporate_warehouse_clean_master", "corporate_warehouse", "kubejs:polycore_emergency_substitution_directive", None, "Late containment", ("minecraft:magenta_concrete", "tfmg:plastic_block", "minecraft:polished_diorite", "immersiveengineering:sheetmetal_steel", "immersiveengineering:crate", "minecraft:yellow_concrete"), {
        "silhouette_exterior_identity": "PolyCore magenta emergency-dispatch bands and a white logistics crown turn the corporate warehouse into a late-containment substitution center",
        "interior_zoning_circulation": "mixed material intake lanes feed five substitution stock rows, a field-kit packing area and a marked emergency dispatch court while the office wing remains the request-and-records node",
        "functional_machinery_props": "polymer remnants, ceramic stock, steel sheets, emergency crates and cardboard field kits show a center assembling replacement packages for many industries at once",
        "institutional_identity": "PolyCore magenta/white routing lanes and repeated mixed-material bays present an organized cross-industry continuity program rather than ordinary warehousing",
        "historical_damage_signature": "the old polymer lane is increasingly isolated while ceramic and metal stocks dominate the later rows and the outbound court is choked with staged emergency kits",
        "narrative_evidence_loot": "guaranteed emergency substitution directive documents the attempt to keep utilities, hospitals and industry operating by replacing failing material classes faster than they degraded"}, "rare_sites"),
    Spec("OWS-020", "ows_020_polycore_deep_barrier_research_facility", "infinite_domain:mountain_biohazard_lab_clean_master", "mountain_biohazard_lab", "kubejs:kel_material_integrity_summary", None, "Late containment", ("minecraft:magenta_concrete", "immersiveengineering:sheetmetal_steel", "minecraft:polished_diorite", "immersiveengineering:insulating_glass", "create:fluid_tank", "minecraft:mycelium", "minecraft:yellow_concrete"), {
        "silhouette_exterior_identity": "PolyCore magenta identity is subordinated to a conspicuous deep-barrier steel/mineral retrofit, making the secure laboratory read as a last-generation containment site",
        "interior_zoning_circulation": "the donor circulation now terminates in nested metallic and mineral barriers surrounding an observation cell, with utilities isolated into a separate service zone",
        "functional_machinery_props": "steel seals, mineralized walls, insulating observation glass, segregated fluid tanks and service pumps make the facility's barrier strategy mechanically legible",
        "institutional_identity": "PolyCore zone coding and redundant barrier layers present a deliberate final containment doctrine rather than another ordinary exposure laboratory",
        "historical_damage_signature": "the outer barriers remain mostly intact while mycelium and fungal growth are already established inside the innermost observation volume, physically proving that stronger walls only delayed failure",
        "narrative_evidence_loot": "guaranteed Kel material integrity summary records the conclusion that no practical barrier material could restore a meaningful clean perimeter once environmental contamination was established"}, "rare_sites"),
    Spec("OWS-021", "ows_021_pleroma_roadside_freight_depot", "infinite_domain:freight_depot_clean_master", "freight_depot", "kubejs:pleroma_dispatch_manifest", None, "Pre-crisis", ("minecraft:cyan_concrete", "minecraft:white_concrete", "immersiveengineering:crate", "create:cardboard_block"), {
        "silhouette_exterior_identity": "cyan-and-white Pleroma dispatch bands and a simple depot blade distinguish the site without changing the donor's freight silhouette",
        "interior_zoning_circulation": "road apron, warehouse stock, dispatch board, truck court and rail approaches remain separate and readable while branded freight occupies each handoff point",
        "functional_machinery_props": "stacked crates, packaged cartons, marked loading lanes and dispatch stock make the depot read as an ordinary working logistics node",
        "institutional_identity": "repeated cyan routing marks and standardized freight groupings establish Pleroma as a mundane recurring carrier rather than an exceptional crisis institution",
        "historical_damage_signature": "the facility remains substantially normal and organized, preserving the pre-crisis baseline needed for later Pleroma sites to show degradation",
        "narrative_evidence_loot": "guaranteed Pleroma dispatch manifest proves the brand's routine participation in ordinary regional freight movement"}),
    Spec("OWS-022", "ows_022_pleroma_urban_distribution_warehouse", "infinite_domain:corporate_warehouse_clean_master", "corporate_warehouse", "kubejs:pleroma_food_distribution_manifest", None, "Pre-crisis -> Early anomaly", ("minecraft:cyan_concrete", "minecraft:white_concrete", "immersiveengineering:crate", "create:cardboard_block", "create:depot", "minecraft:lime_concrete"), {
        "silhouette_exterior_identity": "Pleroma cyan/white warehouse bands convert the corporate distribution shell into a recognizable high-volume urban logistics node",
        "interior_zoning_circulation": "five dense stock lanes feed automated sort depots and a broad outbound staging strip while the donor's office and truck circulation remain intact",
        "functional_machinery_props": "crate racks, packaged cartons, sort depots and repeated Evercrop-marked food parcels show industrial-scale throughput rather than boutique storage",
        "institutional_identity": "standardized cyan routing lanes and repeatable bay geometry make integrated Pleroma supply chains visually obvious",
        "historical_damage_signature": "the site is still mostly functioning, but outbound staging is beginning to accumulate faster than the sort lanes clear it",
        "narrative_evidence_loot": "guaranteed food distribution manifest ties Pleroma's enormous distribution capacity directly to mass Evercrop circulation"}),
    Spec("OWS-023", "ows_023_pleroma_refrigerated_cold_storage_hub", "infinite_domain:corporate_warehouse_clean_master", "corporate_warehouse", "kubejs:pleroma_coldchain_exception_log", None, "Early anomaly", ("minecraft:cyan_concrete", "immersiveengineering:insulating_glass", "oritech:cooler_block", "immersiveengineering:crate", "tfmg:plastic_block", "minecraft:yellow_concrete"), {
        "silhouette_exterior_identity": "Pleroma cyan cold-chain bands and a white warehouse crown retain the distribution identity while marking the site as refrigerated infrastructure",
        "interior_zoning_circulation": "four large cold bays progress from normal storage into seal quarantine, with outbound access retained so the logistics failure is spatially understandable",
        "functional_machinery_props": "cooler floors, insulating-glass chambers, gasket stock and quarantined replacement materials make refrigeration dependence tangible",
        "institutional_identity": "Pleroma routing remains visible underneath expanding maintenance isolation zones, linking the corporate logistics identity to the material crisis",
        "historical_damage_signature": "later cold bays have breached seals, widening yellow quarantine areas and staged polymer replacement stock while earlier bays remain serviceable",
        "narrative_evidence_loot": "guaranteed cold-chain exception log directly links polymer seal degradation to interruptions in food logistics"}),
    Spec("OWS-024", "ows_024_pleroma_intermodal_container_yard", "infinite_domain:warm_industrial_mountain_port_clean_master", "warm_industrial_mountain_port", "kubejs:pleroma_container_inspection_record", None, "Active containment", ("minecraft:cyan_concrete", "minecraft:light_gray_concrete", "minecraft:orange_concrete", "immersiveengineering:crate", "minecraft:iron_bars", "minecraft:yellow_concrete"), {
        "silhouette_exterior_identity": "stacked multicolor container masses and cyan Pleroma routing overlays dominate the port yard without erasing its harbor and mountain interfaces",
        "interior_zoning_circulation": "container stacks occupy the cargo field while a separate inspection lane and blocked outbound strip create a visible quarantine overlay on the normal port workflow",
        "functional_machinery_props": "stacked container volumes, inspection crates, fenced checkpoints and staged cargo make the intermodal handoff function immediately legible",
        "institutional_identity": "Pleroma cyan inspection markings recur across otherwise generic containers, showing how pervasive the carrier had become across modes and regions",
        "historical_damage_signature": "yellow inspection lanes, improvised barriers and backed-up outbound cargo show active containment being imposed on a system built for continuous movement",
        "narrative_evidence_loot": "guaranteed container inspection record supports BOTH SIDES OF THE WALL by showing quarantine controls layered over still-global freight movement"}, "uncommon_sites"),
    Spec("OWS-025", "ows_025_pleroma_automated_market_fulfillment_center", "infinite_domain:dilapidated_grocery", "dilapidated_grocery", "kubejs:pleroma_ration_conversion_notice", None, "Early containment", ("minecraft:cyan_concrete", "minecraft:white_concrete", "create:depot", "create:mechanical_press", "create:cardboard_block", "immersiveengineering:crate", "minecraft:yellow_concrete"), {
        "silhouette_exterior_identity": "Pleroma cyan/white fulfillment markings overwrite the damaged market frontage while leaving the donor grocery silhouette recognizable",
        "interior_zoning_circulation": "consumer shelves and receiving areas are converted into repeated sort stations feeding a broad emergency ration allocation strip and rear reserve stock",
        "functional_machinery_props": "depot/press sort stations, cartons, ration crates and marked allocation lanes turn ordinary retail fulfillment into emergency distribution",
        "institutional_identity": "Pleroma routing remains corporate and systematic even as the public-facing market is repurposed for ration issuance",
        "historical_damage_signature": "the pre-existing rear structural damage remains, but the more important story is operational: consumer flow has been replaced by controlled ration staging",
        "narrative_evidence_loot": "guaranteed ration conversion notice records the moment ordinary abundance was formally converted into civilian emergency allocation"}, "uncommon_sites"),
    Spec("OWS-026", "ows_026_pleroma_quarantine_cargo_warehouse", "infinite_domain:corporate_warehouse_clean_master", "corporate_warehouse", "kubejs:pleroma_quarantine_cargo_order", None, "Active containment", ("minecraft:cyan_concrete", "minecraft:lime_concrete", "minecraft:red_concrete", "immersiveengineering:crate", "immersiveengineering:insulating_glass", "minecraft:iron_bars", "minecraft:yellow_concrete"), {
        "silhouette_exterior_identity": "Pleroma cyan identity sits above a warehouse split into visually explicit accepted and rejected cargo zones",
        "interior_zoning_circulation": "a central customs barrier divides certified agricultural freight from rejected loads, with sealed inspection cages and separate outbound paths",
        "functional_machinery_props": "sealed cargo cages, inspection stock, quarantine fencing and separated crate fields make EP-7-style certification operational rather than textual",
        "institutional_identity": "Pleroma routing and customs segregation show trade institutions trying to manufacture clean and dirty categories inside a contaminated system",
        "historical_damage_signature": "the rejected side accumulates yellow isolation and stalled cargo while the certified side still attempts routine throughput",
        "narrative_evidence_loot": "guaranteed quarantine cargo order documents the rules used to separate accepted agricultural freight from rejected contaminated loads"}, "uncommon_sites"),
    Spec("OWS-027", "ows_027_pleroma_meridian_port_logistics_terminal", "infinite_domain:warm_industrial_mountain_port_clean_master", "warm_industrial_mountain_port", "kubejs:port_emergency_closure_record", None, "Late containment", ("minecraft:cyan_concrete", "minecraft:light_gray_concrete", "minecraft:orange_concrete", "immersiveengineering:crate", "minecraft:iron_bars", "minecraft:yellow_concrete", "minecraft:red_concrete", "minecraft:white_wool"), {
        "silhouette_exterior_identity": "Pleroma cyan port identity remains visible above dense container fields, but emergency red closure zones and fenced customs corridors now dominate the terminal",
        "interior_zoning_circulation": "normal container movement terminates at closed customs gates while backed-up cargo, civilian emergency staging and military-style barriers occupy former outbound space",
        "functional_machinery_props": "container stacks, inspection crates, continuous fencing and blocked gates show a global logistics terminal being physically converted into a closure point",
        "institutional_identity": "the same Pleroma routing seen at ordinary depots now frames an international terminal, demonstrating the carrier's global reach immediately before trade stops",
        "historical_damage_signature": "red closure fields, stalled cargo and emergency civilian shelter masses show late containment replacing commercial throughput with border control",
        "narrative_evidence_loot": "guaranteed port emergency closure record supports THE FIREBREAK WARS by documenting the final shutdown of normal international freight"}, "rare_sites"),
    Spec("OWS-028", "ows_028_aevum_neighborhood_regenerative_clinic", "infinite_domain:ruined_cyberware_clinic_clean_master", "ruined_cyberware_clinic", "kubejs:aevum_patient_recovery_brief", None, "Pre-crisis", ("minecraft:purple_concrete", "minecraft:white_concrete", "minecraft:smooth_quartz", "minecraft:light_blue_stained_glass", "create:fluid_tank", "minecraft:brewing_stand"), {
        "silhouette_exterior_identity": "Aevum purple-and-white clinical bands and a clean regenerative-care blade replace the donor clinic's cyberware identity without requiring a full facade rebuild",
        "interior_zoning_circulation": "reception leads into four ordinary recovery bays, a biologic preparation counter, follow-up monitoring and a small records point in a calm patient-facing sequence",
        "functional_machinery_props": "quartz recovery couches, glass privacy screens, biologic fluid tanks and treatment preparation stations make routine regenerative care physically legible",
        "institutional_identity": "Aevum's clean purple/white medical zoning and repeated recovery-bay layout present the treatment as normalized neighborhood healthcare rather than an elite emergency program",
        "historical_damage_signature": "the implemented treatment zone is intentionally orderly and substantially intact, establishing a desirable pre-crisis baseline before later Aevum sites show supply dependence and failure",
        "narrative_evidence_loot": "guaranteed Aevum patient recovery brief documents ordinary successful treatment and supports A CURE FOR AGE without pretending the medicine was fraudulent"}),
)

BY_TARGET = {spec.target: spec for spec in SPECS}

def build_001():
    t = base.grocery_clean_master()
    t.fill((14, 8, 7), (24, 11, 7), "minecraft:white_concrete"); t.fill((16, 9, 6), (22, 10, 6), "minecraft:lime_concrete"); t.fill((14, 6, 2), (24, 6, 5), "minecraft:lime_concrete")
    for x in (5, 9, 13, 17, 21, 25): t.set(x, 2, 20, "oritech:cooler_block")
    t.fill((5, 2, 24), (12, 3, 27), "immersiveengineering:crate"); t.fill((16, 2, 25), (22, 3, 27), "minecraft:lime_concrete"); t.fill((25, 2, 24), (29, 2, 27), "jaffabricate:pallet_full")
    t.fill((29, 1, 14), (35, 1, 18), "minecraft:yellow_concrete"); t.fill((33, 2, 14), (35, 4, 18), "minecraft:iron_bars"); t.chest(27, 2, 26, BY_TARGET["OWS-001"].loot_id, "west")
    return t

def build_002():
    t = base.ruined_community_center_clean_master()
    t.fill((18, 7, 4), (32, 9, 4), "minecraft:white_concrete"); t.fill((21, 8, 3), (29, 10, 3), "minecraft:lime_concrete")
    t.fill((4, 12, 7), (46, 14, 7), "minecraft:lime_concrete"); t.fill((22, 1, 15), (46, 1, 41), "minecraft:white_concrete")
    for z in (18, 25, 32):
        t.fill((25, 2, z), (43, 2, z + 1), "farmersdelight:rich_soil")
        t.fill((25, 3, z), (43, 3, z + 1), "minecraft:wheat", age="7")
        t.fill((25, 5, z), (43, 5, z + 1), "farmersdelight:rich_soil")
        t.fill((25, 6, z), (43, 6, z + 1), "minecraft:wheat", age="7")
        for x in (24, 44): t.fill((x, 2, z), (x, 6, z + 1), "minecraft:scaffolding")
    t.fill((23, 2, 21), (45, 2, 21), "create:fluid_pipe"); t.set(34, 2, 21, "create:mechanical_pump", facing="east")
    t.fill((6, 2, 29), (18, 4, 33), "immersiveengineering:crate"); t.fill((6, 1, 36), (18, 1, 40), "minecraft:yellow_concrete")
    t.fill((7, 2, 37), (17, 3, 39), "farmersdelight:cabbage_crate"); t.chest(17, 2, 12, BY_TARGET["OWS-002"].loot_id, "west")
    return t

def build_003():
    t = base.abandoned_orchard_cannery_clean_master()
    t.fill((26, 9, 8), (55, 11, 8), "minecraft:white_concrete"); t.fill((30, 10, 7), (51, 12, 7), "minecraft:lime_concrete")
    t.fill((26, 15, 22), (55, 17, 22), "minecraft:lime_concrete"); t.fill((27, 1, 24), (45, 1, 31), "minecraft:light_blue_concrete")
    t.fill((27, 2, 24), (45, 7, 31), "create:framed_glass"); t.clear((28, 3, 25), (44, 6, 30))
    for x in (29, 33, 37, 41):
        t.fill((x, 2, 25), (x + 1, 2, 29), "oritech:cooler_block")
        t.fill((x, 3, 27), (x + 1, 4, 28), "immersiveengineering:crate")
    t.fill((47, 2, 25), (53, 5, 31), "minecraft:scaffolding"); t.fill((46, 1, 32), (55, 1, 39), "minecraft:yellow_concrete")
    t.fill((48, 2, 34), (53, 3, 38), "immersiveengineering:crate"); t.chest(50, 2, 15, BY_TARGET["OWS-003"].loot_id, "west")
    return t

def build_004():
    t = base.ruined_office_tower_clean_master()
    t.fill((10, 13, 11), (40, 15, 11), "minecraft:lime_concrete"); t.fill((10, 13, 37), (40, 15, 37), "minecraft:lime_concrete")
    t.fill((17, 7, 4), (33, 9, 4), "minecraft:white_concrete"); t.fill((20, 8, 3), (30, 11, 3), "minecraft:lime_concrete")
    for floor_index, y in enumerate((14, 21, 28, 35)):
        for x1, x2 in ((12, 20), (30, 38)):
            for z in (15, 19, 28, 32):
                t.fill((x1, y, z), (x2, y, z + 1), "minecraft:mycelium")
                for x in range(x1 + 1, x2, 2): t.set(x, y + 1, z, "minecraft:brown_mushroom")
        t.fill((12, y + 1, 24), (14, y + 3, 25), "create:fluid_tank")
        for x in (30, 33, 36): t.set(x, y + 1, 24, "create:depot")
        t.fill((39, y, 24), (39, y + 4, 31), "minecraft:lime_concrete")
        if floor_index == 3: t.fill((28, y, 12), (39, y, 36), "minecraft:yellow_concrete")
    t.fill((32, 2, 33), (44, 4, 39), "immersiveengineering:crate"); t.fill((7, 2, 33), (20, 2, 39), "create:cardboard_block")
    t.clear((15, 43, 15), (26, 45, 25)); t.fill((16, 43, 16), (25, 43, 24), "minecraft:mycelium")
    t.chest(20, 2, 12, BY_TARGET["OWS-004"].loot_id, "west")
    return t

def build_006():
    t = base.ruined_cyberware_clinic_clean_master()
    t.fill((5, 10, 10), (53, 12, 10), "minecraft:white_concrete"); t.fill((11, 11, 9), (47, 14, 9), "minecraft:lime_concrete")
    t.clear((7, 2, 13), (32, 8, 23))
    for index, x in enumerate((8, 16, 24), 1):
        t.fill((x, 2, 14), (x + 5, 7, 21), "create:framed_glass"); t.clear((x + 1, 3, 15), (x + 4, 6, 20))
        t.fill((x + 1, 2, 16), (x + 4, 2, 19), "farmersdelight:rich_soil")
        t.set(x + 2, 3, 17, "minecraft:brown_mushroom"); t.set(x + 3, 3, 18, "minecraft:red_mushroom")
        t.set(x + 1, 3, 20, "minecraft:brewing_stand", has_bottle_0="false", has_bottle_1="false", has_bottle_2="false")
        t.fill((x, 1, 24), (x + index + 1, 1, 28), "minecraft:yellow_concrete")
    t.fill((39, 2, 12), (50, 4, 17), "tfmg:plastic_block"); t.fill((39, 2, 20), (50, 5, 22), "minecraft:scaffolding")
    t.fill((22, 12, 25), (50, 14, 25), "minecraft:lime_concrete"); t.chest(28, 2, 14, BY_TARGET["OWS-006"].loot_id, "west")
    return t

def build_009():
    t = base.service_garage_clean_master(); t.fill((4, 8, 7), (36, 9, 7), "minecraft:orange_concrete"); t.fill((13, 12, 6), (27, 14, 6), "minecraft:orange_concrete"); t.fill((18, 12, 5), (22, 14, 5), "minecraft:polished_blackstone")
    t.set(17, 13, 5, "minecraft:polished_blackstone"); t.set(23, 13, 5, "minecraft:polished_blackstone"); t.set(20, 11, 5, "minecraft:polished_blackstone")
    for x in (7, 16, 25): t.fill((x, 1, 10), (x + 5, 1, 11), "minecraft:yellow_concrete")
    for x in (9, 18): t.set(x, 2, 17, "create:depot"); t.set(x, 3, 16, "create:mechanical_press", facing="north")
    t.fill((26, 2, 14), (29, 3, 14), "create:andesite_casing"); t.fill((26, 2, 20), (29, 3, 20), "create:andesite_casing"); t.set(27, 2, 17, "minecraft:anvil"); t.set(28, 2, 17, "immersiveengineering:metal_barrel")
    t.fill((32, 2, 23), (35, 5, 23), "minecraft:scaffolding"); t.fill((32, 2, 27), (35, 5, 27), "minecraft:scaffolding"); t.fill((33, 2, 25), (35, 4, 25), "create:andesite_casing"); t.fill((5, 2, 27), (12, 2, 28), "minecraft:orange_concrete"); t.fill((6, 3, 27), (11, 4, 27), "minecraft:polished_blackstone"); t.chest(34, 2, 25, BY_TARGET["OWS-009"].loot_id, "west")
    return t

def build_010():
    t = base.corporate_warehouse_clean_master(); t.fill((15, 12, 8), (45, 14, 8), "minecraft:orange_concrete"); t.fill((17, 10, 35), (45, 11, 36), "minecraft:orange_concrete")
    for x in (19, 25, 31, 37):
        t.fill((x, 1, 11), (x + 3, 1, 29), "minecraft:orange_concrete"); t.set(x + 1, 2, 14, "create:depot"); t.set(x + 1, 3, 15, "create:mechanical_press", facing="north"); t.fill((x, 2, 24), (x + 2, 3, 24), "create:andesite_casing")
    t.fill((38, 2, 11), (43, 4, 18), "minecraft:scaffolding"); t.fill((38, 1, 19), (44, 1, 23), "minecraft:yellow_concrete"); t.fill((40, 2, 20), (43, 3, 22), "create:andesite_casing"); t.chest(41, 2, 13, BY_TARGET["OWS-010"].loot_id, "west")
    return t

def build_012():
    t = base.abandoned_quarry_clean_master()
    t.fill((4, 21, 15), (17, 23, 15), "minecraft:orange_concrete"); t.fill((5, 20, 14), (16, 22, 14), "minecraft:polished_blackstone")
    t.fill((47, 13, 8), (62, 14, 18), "create:andesite_casing")
    for x in (49, 54, 59):
        t.set(x, 15, 11, "create:crushing_wheel"); t.set(x + 1, 15, 13, "create:crushing_wheel")
        t.set(x, 15, 16, "create:millstone")
    t.set(52, 15, 20, "create:basin"); t.set(52, 17, 20, "create:mechanical_mixer")
    for x in (48, 56, 61): t.set(x, 15, 22, "create:encased_fan")
    t.fill((45, 12, 24), (63, 12, 28), "minecraft:orange_concrete"); t.fill((56, 13, 24), (63, 16, 28), "minecraft:yellow_concrete")
    t.fill((38, 7, 45), (54, 9, 50), "jaffabricate:pallet_full"); t.fill((6, 14, 25), (14, 17, 28), "create:andesite_casing")
    t.chest(12, 14, 26, BY_TARGET["OWS-012"].loot_id, "west")
    return t

def build_015():
    t = base.wasteland_water_tower_clean_master(); t.fill((5, 8, 12), (18, 10, 12), "minecraft:magenta_concrete"); t.fill((7, 11, 11), (16, 13, 11), "minecraft:magenta_concrete"); t.fill((6, 1, 22), (17, 1, 28), "minecraft:yellow_concrete"); t.fill((7, 2, 23), (16, 2, 23), "create:fluid_pipe")
    for x in (8, 13): t.set(x, 2, 25, "create:mechanical_pump", facing="south")
    t.fill((6, 2, 17), (9, 3, 19), "immersiveengineering:crate"); t.fill((14, 2, 17), (17, 3, 19), "minecraft:magenta_concrete"); t.fill((14, 4, 17), (17, 5, 17), "minecraft:black_concrete"); t.chest(15, 2, 18, BY_TARGET["OWS-015"].loot_id, "west")
    return t

def build_016():
    t = base.mountain_biohazard_lab_clean_master()
    t.fill((19, 9, 3), (35, 11, 3), "minecraft:white_concrete"); t.fill((22, 10, 2), (32, 13, 2), "minecraft:magenta_concrete")
    t.fill((28, 13, 13), (51, 15, 13), "minecraft:magenta_concrete"); t.clear((29, 2, 17), (50, 8, 34))
    for index, x in enumerate((30, 35, 40, 45), 1):
        t.fill((x, 2, 19), (x + 3, 7, 27), "immersiveengineering:insulating_glass")
        t.clear((x + 1, 3, 20), (x + 2, 6, 26))
        t.fill((x + 1, 2, 21), (x + 2, 2, 25), "tfmg:plastic_block")
        t.fill((x, 1, 29), (x + index - 1, 1, 33), "minecraft:yellow_concrete")
        t.fill((x, 2, 30), (x + 2, 3, 32), "minecraft:magenta_concrete")
    t.fill((29, 2, 16), (50, 2, 16), "minecraft:white_concrete"); t.fill((29, 2, 35), (50, 2, 35), "minecraft:white_concrete")
    t.fill((6, 2, 16), (12, 4, 19), "immersiveengineering:crate"); t.chest(11, 2, 17, BY_TARGET["OWS-016"].loot_id, "west")
    return t

def build_017():
    t = base.industrial_facility_clean_master()
    # Preserve the donor workflow while making the composite emergency program unmistakable.
    t.fill((24, 13, 9), (48, 15, 9), "minecraft:white_concrete")
    t.fill((28, 14, 8), (44, 17, 8), "minecraft:magenta_concrete")
    t.fill((5, 12, 12), (22, 14, 12), "minecraft:magenta_concrete")
    t.fill((51, 10, 13), (64, 12, 13), "minecraft:magenta_concrete")
    # Four barrier cells replace the generic pressing stations. Each contains a layered
    # polymer/mineral coupon and an observation shell; later cells show escalating failure.
    for index, x in enumerate((25, 31, 37, 43), 1):
        t.fill((x, 2, 24), (x + 4, 7, 31), "immersiveengineering:insulating_glass")
        t.clear((x + 1, 3, 25), (x + 3, 6, 30))
        t.fill((x + 1, 2, 25), (x + 3, 2, 30), "tfmg:plastic_block")
        t.fill((x + 2, 3, 27), (x + 2, 5, 28), "minecraft:quartz_block")
        t.fill((x + 1, 3, 29), (x + 3, 4, 29), "immersiveengineering:sheetmetal_steel")
        t.fill((x, 1, 33), (x + index, 1, 37), "minecraft:yellow_concrete")
        t.fill((x + 1, 2, 34), (x + 3, 3, 36), "minecraft:magenta_concrete")
        if index >= 3:
            t.clear((x + 2, 3, 29), (x + 2, 4 + (index - 3), 29))
            t.fill((x + 1, 2, 38), (x + 3, 3, 39), "immersiveengineering:crate")
    # Inspection and failed-material quarantine retain the original dispatch wing.
    t.fill((52, 1, 24), (64, 1, 26), "minecraft:white_concrete")
    t.fill((55, 2, 24), (63, 4, 25), "tfmg:plastic_block")
    t.fill((56, 1, 33), (64, 1, 35), "minecraft:yellow_concrete")
    t.fill((57, 2, 34), (63, 4, 35), "immersiveengineering:crate")
    t.chest(62, 2, 33, BY_TARGET["OWS-017"].loot_id, "west")
    return t

def build_018():
    t = base.nuclear_research_annex_clean_master()
    # Keep the annex massing and circulation; overlay only the emergency PolyCore identity.
    t.fill((5, 13, 10), (38, 15, 10), "minecraft:white_concrete")
    t.fill((12, 14, 9), (31, 17, 9), "minecraft:magenta_concrete")
    t.fill((5, 11, 36), (43, 13, 36), "minecraft:magenta_concrete")
    # Rework the three existing laboratory benches into increasingly expensive isolation trials.
    for index, x in enumerate((8, 21, 32), 1):
        t.fill((x, 2, 24), (x + 6, 8, 32), "immersiveengineering:insulating_glass")
        t.clear((x + 1, 3, 25), (x + 5, 7, 31))
        t.fill((x + 1, 2, 25), (x + 5, 2, 31), "minecraft:polished_diorite")
        t.fill((x + 2, 3, 27), (x + 4, 5, 29), "minecraft:quartz_block")
        if index >= 2:
            t.fill((x + 1, 3, 30), (x + 5, 4, 30), "immersiveengineering:sheetmetal_steel")
        t.fill((x, 1, 33), (x + index + 2, 1, 36), "minecraft:yellow_concrete")
        t.fill((x + 1, 2, 34), (x + 4, 3, 35), "minecraft:magenta_concrete")
        if index == 2:
            t.clear((x + 4, 4, 30), (x + 5, 6, 31))
        elif index == 3:
            t.clear((x + 3, 3, 29), (x + 5, 7, 32))
            t.fill((x + 1, 2, 37), (x + 5, 3, 39), "immersiveengineering:crate")
    # The donor reactor ring becomes the full-scale ceramic/metal isolation trial.
    cx, cz, radius = 56, 38, 13
    for y in range(2, 11):
        for dx in range(-radius, radius + 1):
            for dz in range(-radius, radius + 1):
                d2 = dx * dx + dz * dz
                if 130 <= d2 <= 169:
                    block = "minecraft:polished_diorite" if (dx + dz + y) % 4 else "immersiveengineering:sheetmetal_steel"
                    t.set(cx + dx, y, cz + dz, block)
    for x, z in ((56, 25), (56, 51), (43, 38), (69, 38)):
        t.fill((x, 4, z), (x, 10, z), "minecraft:magenta_concrete")
    # A localized late breach makes the result unambiguous: ceramic buys time, not immunity.
    t.clear((64, 4, 43), (69, 9, 48))
    t.fill((62, 1, 42), (69, 1, 49), "minecraft:yellow_concrete")
    t.fill((64, 2, 45), (68, 3, 49), "immersiveengineering:crate")
    # Retain the rear support wing as retrofit stock and records storage.
    t.fill((8, 2, 41), (18, 4, 53), "minecraft:polished_diorite")
    t.fill((10, 5, 43), (16, 6, 51), "immersiveengineering:sheetmetal_steel")
    t.fill((36, 1, 50), (42, 1, 56), "minecraft:yellow_concrete")
    t.chest(40, 2, 55, BY_TARGET["OWS-018"].loot_id, "west")
    return t

def build_019():
    t = base.corporate_warehouse_clean_master()
    # Preserve the warehouse traffic plan; convert its stock program to emergency substitutions.
    t.fill((15, 12, 8), (45, 14, 8), "minecraft:white_concrete")
    t.fill((19, 13, 7), (41, 15, 7), "minecraft:magenta_concrete")
    t.fill((16, 10, 35), (46, 11, 36), "minecraft:magenta_concrete")
    materials = (
        "tfmg:plastic_block",
        "minecraft:polished_diorite",
        "immersiveengineering:sheetmetal_steel",
        "minecraft:polished_diorite",
        "immersiveengineering:sheetmetal_steel",
    )
    for index, (x, material) in enumerate(zip((17, 23, 29, 35, 41), materials), 1):
        t.fill((x, 1, 12), (x + 3, 1, 29), "minecraft:white_concrete")
        t.fill((x, 2, 14), (x + 3, 4, 20), material)
        t.fill((x, 2, 23), (x + 3, 4, 28), "immersiveengineering:crate")
        t.fill((x, 1, 30), (x + index, 1, 33), "minecraft:yellow_concrete")
    # Packing and dispatch retain the donor's circulation but show continuity work at emergency tempo.
    t.fill((5, 2, 23), (13, 4, 30), "immersiveengineering:crate")
    t.fill((6, 2, 32), (14, 3, 36), "create:cardboard_block")
    t.fill((16, 1, 36), (45, 1, 40), "minecraft:yellow_concrete")
    for x in (18, 26, 34, 42):
        t.fill((x, 2, 37), (x + 3, 3, 39), "immersiveengineering:crate")
    # The original polymer lane is separately quarantined as substitutions move mineral and metallic.
    t.fill((17, 1, 19), (21, 1, 25), "minecraft:yellow_concrete")
    t.fill((18, 2, 20), (20, 4, 24), "tfmg:plastic_block")
    t.chest(43, 2, 15, BY_TARGET["OWS-019"].loot_id, "west")
    return t

def build_020():
    t = base.mountain_biohazard_lab_clean_master()
    # Preserve the donor shell and circulation while making the late-containment retrofit legible.
    t.fill((19, 9, 3), (35, 11, 3), "minecraft:white_concrete")
    t.fill((22, 10, 2), (32, 13, 2), "minecraft:magenta_concrete")
    t.fill((27, 13, 13), (52, 15, 13), "immersiveengineering:sheetmetal_steel")
    t.clear((28, 2, 17), (51, 9, 35))
    # Outer metallic barrier and mineralized floor.
    t.fill((29, 2, 18), (50, 8, 18), "immersiveengineering:sheetmetal_steel")
    t.fill((29, 2, 34), (50, 8, 34), "immersiveengineering:sheetmetal_steel")
    t.fill((29, 2, 18), (29, 8, 34), "immersiveengineering:sheetmetal_steel")
    t.fill((50, 2, 18), (50, 8, 34), "immersiveengineering:sheetmetal_steel")
    t.fill((29, 1, 18), (50, 1, 34), "minecraft:polished_diorite")
    t.clear((38, 2, 18), (40, 5, 18))
    # Inner mineral barrier creates a second apparently intact perimeter.
    t.fill((33, 2, 22), (46, 7, 22), "minecraft:polished_diorite")
    t.fill((33, 2, 30), (46, 7, 30), "minecraft:polished_diorite")
    t.fill((33, 2, 22), (33, 7, 30), "minecraft:polished_diorite")
    t.fill((46, 2, 22), (46, 7, 30), "minecraft:polished_diorite")
    t.clear((38, 2, 22), (40, 5, 22))
    # The contamination is already inside both barriers, which is the actual evidence.
    t.fill((35, 2, 24), (44, 6, 29), "immersiveengineering:insulating_glass")
    t.clear((36, 3, 25), (43, 5, 28))
    t.fill((36, 2, 25), (43, 2, 28), "minecraft:mycelium")
    for x, z in ((37, 26), (39, 27), (41, 26), (42, 28)):
        t.set(x, 3, z, "minecraft:brown_mushroom")
    # Utilities are physically segregated so a failed pipe cannot be mistaken for the ingress route.
    t.fill((6, 2, 22), (16, 4, 26), "create:fluid_tank")
    t.fill((6, 2, 29), (18, 2, 29), "create:fluid_pipe")
    for x in (8, 14):
        t.set(x, 2, 31, "create:mechanical_pump", facing="south")
    t.fill((5, 1, 27), (19, 1, 34), "minecraft:yellow_concrete")
    t.fill((8, 2, 33), (17, 4, 34), "immersiveengineering:crate")
    t.chest(11, 2, 17, BY_TARGET["OWS-020"].loot_id, "west")
    return t

def build_021():
    t = base.freight_depot_clean_master()
    # Keep road, rail and truck approaches intact; add only the Pleroma handoff identity and stock.
    t.fill((5, 11, 5), (30, 13, 5), "minecraft:white_concrete")
    t.fill((10, 12, 4), (25, 15, 4), "minecraft:cyan_concrete")
    for x in (6, 14, 22):
        t.fill((x, 2, 10), (x + 4, 4, 15), "immersiveengineering:crate")
        t.fill((x, 1, 16), (x + 4, 1, 18), "minecraft:cyan_concrete")
    t.fill((34, 1, 6), (44, 1, 28), "minecraft:white_concrete")
    for z in (8, 15, 22):
        t.fill((36, 2, z), (43, 3, z + 3), "create:cardboard_block")
    # Dispatch board and evidence are intentionally simple; visual refinement is deferred.
    t.fill((7, 2, 6), (15, 4, 7), "minecraft:black_concrete")
    t.fill((8, 3, 5), (14, 4, 5), "minecraft:cyan_concrete")
    t.chest(28, 2, 12, BY_TARGET["OWS-021"].loot_id, "west")
    return t

def build_022():
    t = base.corporate_warehouse_clean_master()
    t.fill((15, 12, 8), (45, 14, 8), "minecraft:white_concrete")
    t.fill((20, 13, 7), (40, 15, 7), "minecraft:cyan_concrete")
    # Dense lanes and repeated Evercrop parcels emphasize scale, not architectural detail.
    for x in (17, 23, 29, 35, 41):
        t.fill((x, 1, 12), (x + 3, 1, 30), "minecraft:cyan_concrete")
        t.fill((x, 2, 13), (x + 3, 5, 18), "immersiveengineering:crate")
        t.fill((x, 2, 21), (x + 3, 4, 26), "create:cardboard_block")
        t.fill((x + 1, 2, 28), (x + 2, 3, 29), "minecraft:lime_concrete")
    for x in (18, 26, 34, 42):
        t.set(x, 2, 32, "create:depot")
    t.fill((16, 1, 34), (45, 1, 36), "minecraft:white_concrete")
    t.chest(43, 2, 15, BY_TARGET["OWS-022"].loot_id, "west")
    return t

def build_023():
    t = base.corporate_warehouse_clean_master()
    t.fill((15, 12, 8), (45, 14, 8), "minecraft:white_concrete")
    t.fill((20, 13, 7), (40, 15, 7), "minecraft:cyan_concrete")
    # Four cold bays show the same seal problem becoming operationally expensive.
    for index, x in enumerate((17, 25, 33, 41), 1):
        t.fill((x, 2, 12), (x + 5, 7, 25), "immersiveengineering:insulating_glass")
        t.clear((x + 1, 3, 13), (x + 4, 6, 24))
        t.fill((x + 1, 2, 14), (x + 4, 2, 22), "oritech:cooler_block")
        t.fill((x + 1, 3, 20), (x + 4, 4, 23), "immersiveengineering:crate")
        t.fill((x, 1, 27), (x + index + 1, 1, 31), "minecraft:yellow_concrete")
        if index >= 3:
            t.clear((x + 4, 4, 24), (x + 5, 6, 25))
            t.fill((x + 1, 2, 29), (x + 4, 3, 31), "tfmg:plastic_block")
    t.fill((16, 1, 33), (45, 1, 36), "minecraft:yellow_concrete")
    t.chest(43, 2, 15, BY_TARGET["OWS-023"].loot_id, "west")
    return t

def build_024():
    t = base.warm_industrial_mountain_port_clean_master()
    # Container masses are deliberately block-simple; the later schematic pass owns their detail.
    t.fill((4, 17, 8), (30, 19, 8), "minecraft:white_concrete")
    t.fill((10, 18, 7), (24, 21, 7), "minecraft:cyan_concrete")
    container_blocks = ("minecraft:cyan_concrete", "minecraft:light_gray_concrete", "minecraft:orange_concrete")
    for row, z in enumerate((9, 18, 27)):
        for col, x in enumerate((5, 13, 21)):
            block = container_blocks[(row + col) % len(container_blocks)]
            t.fill((x, 2, z), (x + 5, 4, z + 6), block)
            if (row + col) % 2 == 0:
                t.fill((x, 5, z), (x + 5, 7, z + 6), block)
    # Inspection lane and improvised quarantine barriers overlay the normal port workflow.
    t.fill((31, 1, 8), (43, 1, 31), "minecraft:yellow_concrete")
    for z in (10, 17, 24):
        t.fill((33, 2, z), (40, 4, z + 3), "immersiveengineering:crate")
        t.fill((41, 2, z), (42, 5, z + 3), "minecraft:iron_bars")
    t.fill((30, 2, 33), (44, 4, 35), "minecraft:orange_concrete")
    t.fill((30, 1, 36), (44, 1, 41), "minecraft:yellow_concrete")
    t.chest(39, 2, 29, BY_TARGET["OWS-024"].loot_id, "west")
    return t

def build_025():
    t = base.grocery_store()
    t.fill((14, 8, 7), (24, 11, 7), "minecraft:white_concrete")
    t.fill((16, 9, 6), (22, 10, 6), "minecraft:cyan_concrete")
    # Former consumer fulfillment lanes are mechanically repurposed for ration allocation.
    for x in (8, 14, 20, 26):
        t.set(x, 2, 15, "create:depot")
        t.set(x, 3, 16, "create:mechanical_press", facing="north")
        t.fill((x - 1, 2, 18), (x + 2, 4, 21), "create:cardboard_block")
    t.fill((6, 1, 22), (30, 1, 25), "minecraft:yellow_concrete")
    for x in (8, 15, 22, 29):
        t.fill((x, 2, 23), (x + 3, 4, 25), "immersiveengineering:crate")
    t.fill((24, 2, 27), (34, 4, 30), "immersiveengineering:crate")
    t.chest(32, 2, 28, BY_TARGET["OWS-025"].loot_id, "west")
    return t

def build_026():
    t = base.corporate_warehouse_clean_master()
    t.fill((15, 12, 8), (45, 14, 8), "minecraft:white_concrete")
    t.fill((20, 13, 7), (40, 15, 7), "minecraft:cyan_concrete")
    # The floor itself encodes the attempted clean/dirty customs distinction.
    t.fill((16, 1, 11), (29, 1, 31), "minecraft:lime_concrete")
    t.fill((32, 1, 11), (45, 1, 31), "minecraft:red_concrete")
    for x in (18, 24, 34, 40):
        t.fill((x, 2, 13), (x + 4, 5, 21), "immersiveengineering:crate")
        t.fill((x, 2, 23), (x + 4, 6, 28), "immersiveengineering:insulating_glass")
        t.clear((x + 1, 3, 24), (x + 3, 5, 27))
    t.fill((30, 2, 10), (31, 7, 32), "minecraft:iron_bars")
    t.fill((31, 1, 10), (32, 1, 32), "minecraft:yellow_concrete")
    t.fill((35, 2, 25), (43, 4, 29), "minecraft:yellow_concrete")
    t.chest(43, 2, 15, BY_TARGET["OWS-026"].loot_id, "west")
    return t

def build_027():
    t = base.warm_industrial_mountain_port_clean_master()
    t.fill((4, 17, 8), (30, 19, 8), "minecraft:white_concrete")
    t.fill((10, 18, 7), (24, 21, 7), "minecraft:cyan_concrete")
    # The familiar container field is now trapped behind a hardened closure corridor.
    for row, z in enumerate((8, 17, 26)):
        for col, x in enumerate((4, 12, 20)):
            block = ("minecraft:cyan_concrete", "minecraft:light_gray_concrete", "minecraft:orange_concrete")[(row + col) % 3]
            t.fill((x, 2, z), (x + 5, 4, z + 6), block)
    t.fill((30, 1, 7), (44, 1, 32), "minecraft:yellow_concrete")
    t.fill((31, 2, 7), (31, 6, 32), "minecraft:iron_bars")
    t.fill((43, 2, 7), (43, 6, 32), "minecraft:iron_bars")
    for z in (10, 18, 26):
        t.fill((34, 2, z), (40, 4, z + 3), "immersiveengineering:crate")
    # Civilian emergency staging and the final closed outbound gate replace normal trade flow.
    t.fill((5, 1, 36), (24, 1, 42), "minecraft:red_concrete")
    t.fill((7, 2, 37), (22, 4, 41), "minecraft:white_wool")
    t.fill((27, 1, 34), (45, 1, 42), "minecraft:red_concrete")
    t.fill((27, 2, 34), (45, 5, 35), "minecraft:iron_bars")
    t.chest(39, 2, 29, BY_TARGET["OWS-027"].loot_id, "west")
    return t

def build_028():
    t = base.ruined_cyberware_clinic_clean_master()
    # Re-establish a calm, ordinary clinic program inside the reusable donor shell.
    t.fill((5, 10, 10), (53, 12, 10), "minecraft:white_concrete")
    t.fill((12, 11, 9), (46, 14, 9), "minecraft:purple_concrete")
    t.clear((7, 2, 13), (50, 8, 24))
    t.fill((7, 1, 13), (50, 1, 24), "minecraft:smooth_quartz")
    # Reception and patient routing.
    t.fill((8, 2, 14), (17, 3, 16), "minecraft:smooth_quartz")
    t.fill((9, 4, 14), (16, 5, 14), "minecraft:purple_concrete")
    # Four recovery bays: privacy screens, treatment couches and biologic preparation points.
    for x in (20, 28, 36, 44):
        t.fill((x, 2, 14), (x + 5, 6, 21), "minecraft:light_blue_stained_glass")
        t.clear((x + 1, 3, 15), (x + 4, 5, 20))
        t.fill((x + 1, 2, 16), (x + 4, 2, 18), "minecraft:smooth_quartz")
        t.fill((x + 1, 3, 19), (x + 2, 4, 20), "create:fluid_tank")
        t.set(x + 4, 3, 20, "minecraft:brewing_stand", has_bottle_0="false", has_bottle_1="false", has_bottle_2="false")
    # Follow-up monitoring and records stay directly accessible from the recovery route.
    t.fill((8, 2, 20), (16, 4, 23), "minecraft:white_concrete")
    t.fill((9, 3, 22), (15, 4, 23), "minecraft:purple_concrete")
    t.chest(14, 2, 22, BY_TARGET["OWS-028"].loot_id, "west")
    return t

BUILDERS = {"OWS-001": build_001, "OWS-002": build_002, "OWS-003": build_003, "OWS-004": build_004, "OWS-006": build_006, "OWS-009": build_009, "OWS-010": build_010, "OWS-012": build_012, "OWS-015": build_015, "OWS-016": build_016, "OWS-017": build_017, "OWS-018": build_018, "OWS-019": build_019, "OWS-020": build_020, "OWS-021": build_021, "OWS-022": build_022, "OWS-023": build_023, "OWS-024": build_024, "OWS-025": build_025, "OWS-026": build_026, "OWS-027": build_027, "OWS-028": build_028}

def loot_table(spec):
    items = list(dict.fromkeys([spec.proof] + ([spec.lore] if spec.lore else [])))
    pools = [{"rolls": 1, "entries": [{"type": "minecraft:item", "name": item}]} for item in items]
    extra = [{"type": "minecraft:item", "name": "create:andesite_alloy", "weight": 8}]
    if spec.target == "OWS-009": extra += [{"type": "minecraft:item", "name": "create:shaft", "weight": 10}, {"type": "minecraft:item", "name": "create:cogwheel", "weight": 8}]
    extra += [{"type": "minecraft:item", "name": "minecraft:iron_ingot", "weight": 10}, {"type": "minecraft:item", "name": "immersiveengineering:component_iron", "weight": 5}]
    pools.append({"rolls": {"type": "minecraft:uniform", "min": 3 if spec.target == "OWS-009" else 2, "max": 6 if spec.target == "OWS-009" else 4}, "entries": extra})
    return {"type": "minecraft:chest", "random_sequence": spec.loot_id, "pools": pools}

def generate(spec):
    template = BUILDERS[spec.target](); base.stabilize_door_pairs(template); metrics = base.assess_fidelity(spec.source_profile, template)
    if not metrics["structural_lint_passed"]: raise ValueError(f"{spec.target} failed structural lint: " + "; ".join(metrics["issues"]))
    nbt_path = DATA / "structure" / "wasteland" / "old_world" / f"{spec.name}.nbt"
    previous_nbt = nbt_path.read_bytes() if nbt_path.is_file() else None
    statistics = template.save(f"old_world/{spec.name}")
    if previous_nbt is not None:
        generated_nbt = nbt_path.read_bytes()
        if gzip.decompress(previous_nbt) == gzip.decompress(generated_nbt):
            nbt_path.write_bytes(previous_nbt)
    base.write_json(DATA / "worldgen" / "template_pool" / "old_world" / f"{spec.name}.json", {"fallback": "minecraft:empty", "elements": [{"weight": 1, "element": {"location": f"infinite_domain:wasteland/old_world/{spec.name}", "processors": "minecraft:empty", "projection": "rigid", "element_type": "minecraft:single_pool_element"}}]})
    base.write_json(DATA / "worldgen" / "structure" / "old_world" / f"{spec.name}.json", {"type": "minecraft:jigsaw", "biomes": "#infinite_domain:wasteland_site_biomes", "step": "surface_structures", "spawn_overrides": {}, "terrain_adaptation": "beard_box", "start_pool": f"infinite_domain:old_world/{spec.name}", "size": 1, "start_height": {"absolute": 0}, "max_distance_from_center": 80, "use_expansion_hack": False, "liquid_settings": "ignore_waterlogging", "project_start_to_heightmap": "WORLD_SURFACE_WG"})
    base.write_json(DATA / "loot_table" / "chests" / "old_world" / f"{spec.name}.json", loot_table(spec))
    base.write_json(ROOT / "old_world_narrative" / "structures" / f"{spec.target.lower()}-{spec.name[8:].replace('_', '-')}.json", {"format_version": 1, "target_id": spec.target, "structure_id": spec.structure_id, "source_structure": spec.source_id, "collapse_phase": spec.phase, "acceptance_dimensions": spec.dimensions, "proof_item": spec.proof, "lore_record": spec.lore, "loot_table": spec.loot_id, "locator_command": f"/structure_map {spec.structure_id} 2", "statistics": statistics, "structural_lint": metrics, "static_render_review": "generated_and_inspected_not_runtime_approval", "runtime_validation": "deferred_by_user"})

def main():
    for spec in SPECS: generate(spec)
    for set_name, spacing, separation, salt in (("common_sites", 48, 24, 90310009), ("uncommon_sites", 96, 48, 90310016), ("rare_sites", 160, 80, 90310006)):
        members = [spec for spec in SPECS if spec.set_name == set_name]
        base.write_json(DATA / "worldgen" / "structure_set" / "old_world" / f"{set_name}.json", {"structures": [{"structure": spec.structure_id, "weight": 1} for spec in members], "placement": {"type": "minecraft:random_spread", "spacing": spacing, "separation": separation, "salt": salt}})
    print(f"Generated {len(SPECS)} approved Old World sites with deterministic proof loot.")

if __name__ == "__main__": main()
