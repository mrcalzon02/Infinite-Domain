#!/usr/bin/env python3
"""Generate the approved, locatable Old World narrative structure wave."""
from __future__ import annotations
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
    Spec("OWS-015", "ows_015_polycore_utility_seal_failure_station", "infinite_domain:wasteland_water_tower_clean_master", "wasteland_water_tower", "kubejs:polycore_seal_failure_report", "kubejs:polycore_service_interval_board", "Early anomaly", ("minecraft:magenta_concrete", "create:mechanical_pump", "create:fluid_pipe", "minecraft:yellow_concrete"), {
        "silhouette_exterior_identity": "PolyCore magenta pump-house band and seal-service pylon identify the utility compound",
        "interior_zoning_circulation": "intake, paired pumps, seal bench, replacement stock and records wall form a service loop",
        "functional_machinery_props": "paired pumps, pipe manifold, tagged gasket stock and maintenance isolation zone",
        "institutional_identity": "PolyCore color coding and decreasing inspection intervals cover the ordinary utility station",
        "historical_damage_signature": "yellow isolation marks and stacked replacement crates show recurring seal failures without collapse",
        "narrative_evidence_loot": "guaranteed failure report and LOR-008 interval board make the material crisis measurable"}),
)

def build_001():
    t = base.grocery_clean_master()
    t.fill((14, 8, 7), (24, 11, 7), "minecraft:white_concrete"); t.fill((16, 9, 6), (22, 10, 6), "minecraft:lime_concrete"); t.fill((14, 6, 2), (24, 6, 5), "minecraft:lime_concrete")
    for x in (5, 9, 13, 17, 21, 25): t.set(x, 2, 20, "oritech:cooler_block")
    t.fill((5, 2, 24), (12, 3, 27), "immersiveengineering:crate"); t.fill((16, 2, 25), (22, 3, 27), "minecraft:lime_concrete"); t.fill((25, 2, 24), (29, 2, 27), "jaffabricate:pallet_full")
    t.fill((29, 1, 14), (35, 1, 18), "minecraft:yellow_concrete"); t.fill((33, 2, 14), (35, 4, 18), "minecraft:iron_bars"); t.chest(27, 2, 26, SPECS[0].loot_id, "west")
    return t

def build_009():
    t = base.service_garage_clean_master(); t.fill((4, 8, 7), (36, 9, 7), "minecraft:orange_concrete"); t.fill((13, 12, 6), (27, 14, 6), "minecraft:orange_concrete"); t.fill((18, 12, 5), (22, 14, 5), "minecraft:polished_blackstone")
    t.set(17, 13, 5, "minecraft:polished_blackstone"); t.set(23, 13, 5, "minecraft:polished_blackstone"); t.set(20, 11, 5, "minecraft:polished_blackstone")
    for x in (7, 16, 25): t.fill((x, 1, 10), (x + 5, 1, 11), "minecraft:yellow_concrete")
    for x in (9, 18): t.set(x, 2, 17, "create:depot"); t.set(x, 3, 16, "create:mechanical_press", facing="north")
    t.fill((26, 2, 14), (29, 3, 14), "create:andesite_casing"); t.fill((26, 2, 20), (29, 3, 20), "create:andesite_casing"); t.set(27, 2, 17, "minecraft:anvil"); t.set(28, 2, 17, "immersiveengineering:metal_barrel")
    t.fill((32, 2, 23), (35, 5, 23), "minecraft:scaffolding"); t.fill((32, 2, 27), (35, 5, 27), "minecraft:scaffolding"); t.fill((33, 2, 25), (35, 4, 25), "create:andesite_casing"); t.fill((5, 2, 27), (12, 2, 28), "minecraft:orange_concrete"); t.fill((6, 3, 27), (11, 4, 27), "minecraft:polished_blackstone"); t.chest(34, 2, 25, SPECS[1].loot_id, "west")
    return t

def build_010():
    t = base.corporate_warehouse_clean_master(); t.fill((15, 12, 8), (45, 14, 8), "minecraft:orange_concrete"); t.fill((17, 10, 35), (45, 11, 36), "minecraft:orange_concrete")
    for x in (19, 25, 31, 37):
        t.fill((x, 1, 11), (x + 3, 1, 29), "minecraft:orange_concrete"); t.set(x + 1, 2, 14, "create:depot"); t.set(x + 1, 3, 15, "create:mechanical_press", facing="north"); t.fill((x, 2, 24), (x + 2, 3, 24), "create:andesite_casing")
    t.fill((38, 2, 11), (43, 4, 18), "minecraft:scaffolding"); t.fill((38, 1, 19), (44, 1, 23), "minecraft:yellow_concrete"); t.fill((40, 2, 20), (43, 3, 22), "create:andesite_casing"); t.chest(41, 2, 13, SPECS[2].loot_id, "west")
    return t

def build_015():
    t = base.wasteland_water_tower_clean_master(); t.fill((5, 8, 12), (18, 10, 12), "minecraft:magenta_concrete"); t.fill((7, 11, 11), (16, 13, 11), "minecraft:magenta_concrete"); t.fill((6, 1, 22), (17, 1, 28), "minecraft:yellow_concrete"); t.fill((7, 2, 23), (16, 2, 23), "create:fluid_pipe")
    for x in (8, 13): t.set(x, 2, 25, "create:mechanical_pump", facing="south")
    t.fill((6, 2, 17), (9, 3, 19), "immersiveengineering:crate"); t.fill((14, 2, 17), (17, 3, 19), "minecraft:magenta_concrete"); t.fill((14, 4, 17), (17, 5, 17), "minecraft:black_concrete"); t.chest(15, 2, 18, SPECS[3].loot_id, "west")
    return t

BUILDERS = {"OWS-001": build_001, "OWS-009": build_009, "OWS-010": build_010, "OWS-015": build_015}

def loot_table(spec):
    items = [spec.proof] + ([spec.lore] if spec.lore else [])
    pools = [{"rolls": 1, "entries": [{"type": "minecraft:item", "name": item}]} for item in items]
    extra = [{"type": "minecraft:item", "name": "create:andesite_alloy", "weight": 8}]
    if spec.target == "OWS-009": extra += [{"type": "minecraft:item", "name": "create:shaft", "weight": 10}, {"type": "minecraft:item", "name": "create:cogwheel", "weight": 8}]
    extra += [{"type": "minecraft:item", "name": "minecraft:iron_ingot", "weight": 10}, {"type": "minecraft:item", "name": "immersiveengineering:component_iron", "weight": 5}]
    pools.append({"rolls": {"type": "minecraft:uniform", "min": 3 if spec.target == "OWS-009" else 2, "max": 6 if spec.target == "OWS-009" else 4}, "entries": extra})
    return {"type": "minecraft:chest", "random_sequence": spec.loot_id, "pools": pools}

def generate(spec):
    template = BUILDERS[spec.target](); base.stabilize_door_pairs(template); metrics = base.assess_fidelity(spec.source_profile, template)
    if not metrics["structural_lint_passed"]: raise ValueError(f"{spec.target} failed structural lint: " + "; ".join(metrics["issues"]))
    statistics = template.save(f"old_world/{spec.name}")
    base.write_json(DATA / "worldgen" / "template_pool" / "old_world" / f"{spec.name}.json", {"fallback": "minecraft:empty", "elements": [{"weight": 1, "element": {"location": f"infinite_domain:wasteland/old_world/{spec.name}", "processors": "minecraft:empty", "projection": "rigid", "element_type": "minecraft:single_pool_element"}}]})
    base.write_json(DATA / "worldgen" / "structure" / "old_world" / f"{spec.name}.json", {"type": "minecraft:jigsaw", "biomes": "#infinite_domain:wasteland_site_biomes", "step": "surface_structures", "spawn_overrides": {}, "terrain_adaptation": "beard_box", "start_pool": f"infinite_domain:old_world/{spec.name}", "size": 1, "start_height": {"absolute": 0}, "max_distance_from_center": 80, "use_expansion_hack": False, "liquid_settings": "ignore_waterlogging", "project_start_to_heightmap": "WORLD_SURFACE_WG"})
    base.write_json(DATA / "loot_table" / "chests" / "old_world" / f"{spec.name}.json", loot_table(spec))
    base.write_json(ROOT / "old_world_narrative" / "structures" / f"{spec.target.lower()}-{spec.name[8:].replace('_', '-')}.json", {"format_version": 1, "target_id": spec.target, "structure_id": spec.structure_id, "source_structure": spec.source_id, "collapse_phase": spec.phase, "acceptance_dimensions": spec.dimensions, "proof_item": spec.proof, "lore_record": spec.lore, "loot_table": spec.loot_id, "locator_command": f"/structure_map {spec.structure_id} 2", "statistics": statistics, "structural_lint": metrics, "static_render_review": "generated_and_inspected_not_runtime_approval", "runtime_validation": "deferred_by_user"})

def main():
    for spec in SPECS: generate(spec)
    base.write_json(DATA / "worldgen" / "structure_set" / "old_world" / "common_sites.json", {"structures": [{"structure": spec.structure_id, "weight": 1} for spec in SPECS], "placement": {"type": "minecraft:random_spread", "spacing": 48, "separation": 24, "salt": 90310009}})
    print("Generated four approved common Old World sites with deterministic proof loot.")

if __name__ == "__main__": main()
