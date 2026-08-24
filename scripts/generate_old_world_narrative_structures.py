#!/usr/bin/env python3
"""Generate the approved, locatable Old World narrative structure wave."""
from __future__ import annotations
import gzip
from dataclasses import dataclass
from pathlib import Path
import generate_wasteland_sites as base
import old_world_v2_compliance as v2
import structure_geometry_lint as geometry_lint

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

BUILDERS = {"OWS-001": build_001, "OWS-002": build_002, "OWS-003": build_003, "OWS-004": build_004, "OWS-006": build_006, "OWS-009": build_009, "OWS-010": build_010, "OWS-012": build_012, "OWS-015": build_015, "OWS-016": build_016}


# ---------------------------------------------------------------------------
# Structure Rebuild System v2 compliance
# ---------------------------------------------------------------------------
#
# `structure_library/STRUCTURE_REBUILD_SYSTEM_V2.md` retires `assess_fidelity`
# as the production gate. These sites are therefore gated on
# `structure_geometry_lint` checks 1-3 instead, and repaired by
# `old_world_v2_compliance` rather than regenerated from scratch — see that
# module's header for why repair rather than rebuild is the correct
# disposition for this particular wave.
#
# Two kinds of fix run, and the split is deliberate:
#
#   * the finding-driven retrofit (`v2.converge`) handles defect classes where
#     there is exactly one correct answer — a stair run needs a shaft, a ladder
#     needs backing, a door needs jambs. It repairs only the coordinates the
#     gate reported, so a site with no findings is left untouched.
#
#   * `_authored_*` functions below handle the cases where the fix is a design
#     decision. Those are written out longhand, per site, so they can be read
#     and disagreed with rather than buried in a generic operator.

# Per-site repair palette, chosen to match each building's existing material
# vocabulary so a retrofit does not read as a patch.
COMPLIANCE_PALETTE: dict[str, dict[str, str]] = {
    "OWS-001": {"wall_block": "minecraft:white_concrete"},
    "OWS-002": {"wall_block": "minecraft:white_concrete", "backing_block": "minecraft:stripped_spruce_log"},
    "OWS-003": {"wall_block": "minecraft:white_concrete"},
    "OWS-004": {"wall_block": "minecraft:smooth_stone", "frame_block": "minecraft:white_concrete"},
    "OWS-006": {"wall_block": "minecraft:white_concrete"},
    "OWS-009": {"wall_block": "minecraft:polished_blackstone"},
    "OWS-010": {"wall_block": "minecraft:polished_andesite"},
    "OWS-012": {"wall_block": "minecraft:polished_blackstone"},
    "OWS-015": {"wall_block": "minecraft:white_concrete"},
    "OWS-016": {"wall_block": "minecraft:white_concrete"},
}

# Templates that model an excavation must declare the grade their at-grade
# structures stand on; see structure_geometry_lint.lint_structure's `ground_y`.
COMPLIANCE_GROUND_Y: dict[str, tuple[int, ...]] = {
    "OWS-012": (12, 13),
}


def _authored_002(t):
    """Roof-hatch curb.

    The escape ladder's iron trapdoor sits one course above the copper roof
    deck with nothing beside it — a hatch with no curb, floating over its own
    shaft. A four-block curb ring is what a real roof hatch has, and it ties
    the trapdoor back into the deck.
    """
    for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        v2.place_if_empty(t, (44 + dx, 19, 38 + dz), "minecraft:weathered_cut_copper")


def _authored_006(t):
    """Airlocks into the three PT-9 symbiosis chambers.

    Each chamber was a sealed glass box containing soil, cultures and a
    reagent station — legible from outside, impossible to enter. The site's
    own acceptance dimension calls for "sample intake, three symbiosis
    chambers, bacterial controls ... separated", which means separated by a
    controlled door, not walled off entirely. Each chamber gets a framed iron
    airlock on its corridor face and a threshold step up from the hall floor
    to the raised chamber deck.
    """
    for x in (8, 16, 24):
        v2.cut_access_doorway(
            t, (x + 2, 3, 14), "north",
            door_block="minecraft:iron_door",
            frame_block="minecraft:white_concrete",
        )


def _authored_012(t):
    """The quarry's missing ground, and a continuous process deck.

    This template modelled only what was excavated. The haul road, service
    house, crushing plant and timber headframe all stood at natural grade with
    nothing beneath them, which is why this site alone accounted for 2,731 of
    the wave's connectivity findings — not because the buildings were badly
    built, but because the site had no ground.

    Three fixes, in the order the site reads:

    1. An industrial-hardstanding working yard at grade (y=12) under the haul
       road bed and the three building pads, laid in coherent patches rather
       than the universal asphalt speckle v2 doctrine 3.5 bans. The pit itself
       is untouched; the pads stop at the rim and the existing benches already
       carry the haul route down to the pit floor.
    2. The process deck carried south from z=19 to z=23, so bulk feed,
       crushing, milling, mixing and dust extraction stand on one continuous
       structure. The acceptance dimension already claims this process line is
       continuous; now it is.
    3. An overhead gantry for the mechanical mixer. The mixer must hang two
       courses above its basin with the span between them clear, so it is
       carried from a beam above rather than propped from below — a support
       column under it would have satisfied the geometry gate and broken the
       machine.
    """
    for corner_a, corner_b, seed in (
        ((2, 0), (66, 17), 1201),    # haul road bed and north working yard
        ((2, 14), (17, 36), 1202),   # west service-house pad
        ((44, 19), (66, 31), 1203),  # east crushing-plant pad
        ((54, 40), (66, 52), 1204),  # southeast headframe pad
    ):
        v2.grade_pad(t, corner_a, corner_b, "industrial_hardstanding", y=12, seed=seed)

    for x in range(46, 63):
        for z in range(19, 24):
            v2.place_if_empty(t, (x, 14, z), "create:andesite_casing")
            v2.place_if_empty(t, (x, 13, z), "create:andesite_casing")

    for y in range(15, 19):
        v2.place_if_empty(t, (50, y, 20), "create:andesite_casing")
        v2.place_if_empty(t, (54, y, 20), "create:andesite_casing")
    for x in range(50, 55):
        v2.place_if_empty(t, (x, 18, 20), "create:andesite_casing")


def _authored_003(t):
    """Access into the cold vault.

    The glazed cold vault holds the cooler banks and the sealed culture
    crates the whole site exists to move, and had no way in — the crates
    could be seen and never reached. The vault's own workflow runs receiving
    to dispatch west to east, so the door goes on the east face where the
    scaffolding racks and the dispatch apron already are.
    """
    v2.cut_access_doorway(
        t, (45, 3, 28), "east",
        door_block="minecraft:iron_door",
        frame_block="minecraft:white_concrete",
    )


def _authored_004(t):
    """Access into the rooftop cultivation greenhouse.

    The greenhouse is the tower's crown and the most public thing on the
    site — "a luminous rooftop greenhouse" in its own silhouette dimension —
    and it was a sealed glass box on top of the roof deck. A door on its
    south face opens it onto the deck at the head of the tower's circulation.
    """
    v2.cut_access_doorway(
        t, (20, 44, 26), "south",
        door_block="minecraft:dark_oak_door",
        frame_block="minecraft:white_concrete",
    )


def _authored_006_plenum(t):
    """Turn the lab's roof void into a legible mechanical plenum.

    468 blocks of sealed, undressed air sat above the laboratory — exactly
    the "undifferentiated mass" v2 doctrine 3.7 rejects. Filling it with
    furniture would be dishonest; it is a plenum. So it is dressed as one and
    given service access, which for a building whose whole purpose is sealed
    containment chambers is the most load-bearing room in it: this is where
    the air handling that keeps those chambers sealed would live.

    It reads as what it is: a rooftop plant room standing on the roof deck,
    entered by a door off the roof, with a service ladder dropping through
    its floor into the laboratory below. Duct runs are carried directly
    beneath the ceiling slab so they hang from it rather than floating.
    """
    # Door off the roof deck into the plant room.
    v2.cut_access_doorway(
        t, (29, 21, 35), "west",
        door_block="minecraft:iron_door",
        frame_block="minecraft:smooth_stone",
    )

    # Service hatch and ladder down into the floor below.
    for y in range(20, 21):
        t.set(30, y, 31, "minecraft:air")
    for y in range(17, 22):
        v2.place_if_empty(t, (29, y, 31), "minecraft:smooth_stone")
        t.set(30, y, 31, "minecraft:ladder", facing="east", waterlogged="false")

    # Duct runs beneath the ceiling slab, with an air handler on each line.
    for x in (33, 36, 39):
        for z in range(31, 41):
            v2.place_if_empty(t, (x, 23, z), "create:fluid_pipe")
        v2.place_if_empty(t, (x, 23, 30), "create:encased_fan", facing="south")
    for z in (33, 37):
        for x in range(31, 42):
            v2.place_if_empty(t, (x, 23, z), "create:fluid_pipe")


def _authored_016(t):
    """Access into the four elastomer exposure chambers.

    Same defect and same answer as the PT-9 laboratory: four sealed glass
    cells holding the polymer coupons whose repeated failure is the site's
    entire evidence, with no way for the technicians who loaded them — or the
    player — to reach them. Each gets a framed airlock on its clean-corridor
    face, which is also what makes the "clean observation route" the site
    claims actually a route.
    """
    for x in (30, 35, 40, 45):
        v2.cut_access_doorway(
            t, (x + 1, 3, 19), "north",
            door_block="minecraft:iron_door",
            frame_block="minecraft:white_concrete",
        )


def _authored_006_all(t):
    _authored_006(t)
    _authored_006_plenum(t)


# OWS-015's tank is deliberately absent from this table. Its flagged void is
# the water tower's own vessel: a sealed tank is what a water tower is, and
# the lint names that case explicitly ("may be ... an intentionally sealed
# vessel, verify"). It was verified and left alone. Cutting a door into a
# pressure vessel to satisfy a heuristic would be the wrong reading of the
# gate, and the finding stays reported so the next reader re-checks it rather
# than inheriting a silent exemption.
AUTHORED_COMPLIANCE = {
    "OWS-002": _authored_002,
    "OWS-003": _authored_003,
    "OWS-004": _authored_004,
    "OWS-006": _authored_006_all,
    "OWS-012": _authored_012,
    "OWS-016": _authored_016,
}


def apply_v2_compliance(target, template):
    """Bring one site to Structure Rebuild System v2 compliance.

    Returns the final `LintResult` and a record of what the retrofit wrote, so
    the site's registry entry can state what was actually done rather than
    asserting the structure is fine.
    """
    authored = AUTHORED_COMPLIANCE.get(target)
    if authored:
        authored(template)
        base.stabilize_door_pairs(template)

    palette = dict(COMPLIANCE_PALETTE[target])
    ground_y = COMPLIANCE_GROUND_Y.get(target)
    if ground_y:
        palette["ground_y"] = ground_y
    result, rounds = v2.converge(template, geometry_lint, target, **palette)
    base.stabilize_door_pairs(template)

    size, positions = geometry_lint.positions_from_template(template)
    result = geometry_lint.lint_structure(target, size, positions, ground_y=ground_y)
    retrofit = {key: sum(r.get(key, 0) for r in rounds) for key in (rounds[0] if rounds else {})}
    return result, {
        "authored_repair": bool(authored),
        "retrofit_rounds": len(rounds),
        "retrofit_blocks_written": {key: value for key, value in retrofit.items() if value},
    }

def loot_table(spec):
    items = list(dict.fromkeys([spec.proof] + ([spec.lore] if spec.lore else [])))
    pools = [{"rolls": 1, "entries": [{"type": "minecraft:item", "name": item}]} for item in items]
    extra = [{"type": "minecraft:item", "name": "create:andesite_alloy", "weight": 8}]
    if spec.target == "OWS-009": extra += [{"type": "minecraft:item", "name": "create:shaft", "weight": 10}, {"type": "minecraft:item", "name": "create:cogwheel", "weight": 8}]
    extra += [{"type": "minecraft:item", "name": "minecraft:iron_ingot", "weight": 10}, {"type": "minecraft:item", "name": "immersiveengineering:component_iron", "weight": 5}]
    pools.append({"rolls": {"type": "minecraft:uniform", "min": 3 if spec.target == "OWS-009" else 2, "max": 6 if spec.target == "OWS-009" else 4}, "entries": extra})
    return {"type": "minecraft:chest", "random_sequence": spec.loot_id, "pools": pools}

def generate(spec):
    template = BUILDERS[spec.target]()
    base.stabilize_door_pairs(template)

    # Structure Rebuild System v2 gate. `assess_fidelity` counted door halves,
    # glass blocks and fixture keywords; it could not see a floating window, an
    # unsupported stair, or a building standing on nothing, and every site in
    # this wave passed it while carrying exactly those defects. It is kept
    # below as a supplementary record only — the gate is the geometry lint.
    lint_result, retrofit = apply_v2_compliance(spec.target, template)
    if not lint_result.passed:
        detail = "; ".join(f"{f.check}@{f.position}: {f.detail}" for f in lint_result.findings if f.severity == "hard_fail")
        raise ValueError(f"{spec.target} failed structure_geometry_lint checks 1-3: {detail}")

    legacy_metrics = base.assess_fidelity(spec.source_profile, template)
    metrics = {
        "gate": "structure_geometry_lint",
        "gate_version": "structure_rebuild_system_v2",
        "hard_fail_count": lint_result.hard_fail_count,
        "structural_lint_passed": lint_result.passed,
        "review_findings": [
            {"check": f.check, "position": list(f.position) if f.position else None, "detail": f.detail}
            for f in lint_result.findings if f.severity == "review_flag"
        ],
        "v2_compliance": retrofit,
        "legacy_assess_fidelity": legacy_metrics,
    }
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
    base.write_json(ROOT / "old_world_narrative" / "structures" / f"{spec.target.lower()}-{spec.name[8:].replace('_', '-')}.json", {"format_version": 1, "target_id": spec.target, "structure_id": spec.structure_id, "source_structure": spec.source_id, "collapse_phase": spec.phase, "acceptance_dimensions": spec.dimensions, "proof_item": spec.proof, "lore_record": spec.lore, "loot_table": spec.loot_id, "locator_command": f"/structure_map {spec.structure_id} 2", "statistics": statistics, "structural_lint": metrics, "static_render_review": "regenerated_under_structure_rebuild_system_v2_not_runtime_approval", "runtime_validation": "deferred_by_user"})

def main():
    for spec in SPECS: generate(spec)
    for set_name, spacing, separation, salt in (("common_sites", 48, 24, 90310009), ("uncommon_sites", 96, 48, 90310016), ("rare_sites", 160, 80, 90310006)):
        members = [spec for spec in SPECS if spec.set_name == set_name]
        base.write_json(DATA / "worldgen" / "structure_set" / "old_world" / f"{set_name}.json", {"structures": [{"structure": spec.structure_id, "weight": 1} for spec in members], "placement": {"type": "minecraft:random_spread", "spacing": spacing, "separation": separation, "salt": salt}})
    print(f"Generated {len(SPECS)} approved Old World sites with deterministic proof loot.")

if __name__ == "__main__": main()
