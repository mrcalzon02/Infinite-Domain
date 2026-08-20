#!/usr/bin/env python3
"""[SYSTEM REPORT] Authoritative Old World structure entrypoint.

The preserved ten-site implementation lives in old_world_narrative_core.py.
This file is the only executable structure-generation entrypoint and extends
that core with later narrative waves. Imported modules are implementation
components, not independent mutation paths.
"""
from __future__ import annotations

import json
from pathlib import Path

import old_world_narrative_core as core

base = core.base
ROOT = Path(__file__).resolve().parents[1]
PROGRAM = ROOT / "old_world_narrative"
REGISTRY = PROGRAM / "registry"

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


def build_005():
    t = base.abandoned_orchard_cannery_clean_master()
    t.fill((6, 9, 8), (55, 11, 8), "minecraft:white_concrete")
    t.fill((12, 10, 7), (49, 13, 7), "minecraft:lime_concrete")
    # PT-9 sanitation lane: cyan wash path feeding packaging inspection.
    t.fill((7, 1, 13), (23, 1, 20), "minecraft:light_blue_concrete")
    t.fill((8, 2, 15), (22, 2, 15), "create:fluid_pipe")
    t.fill((8, 2, 17), (11, 6, 19), "create:fluid_tank")
    # Inspection and packaging line.
    for x in (27, 34, 41, 48):
        t.set(x, 2, 16, "create:depot")
        t.set(x, 3, 17, "create:mechanical_press", facing="north")
        t.fill((x - 1, 2, 21), (x + 2, 4, 23), "create:cardboard_block")
    # Cold hold and outgoing consumer-food stock.
    for x in (29, 35, 41, 47):
        t.fill((x, 2, 28), (x + 2, 5, 31), "oritech:cooler_block")
    t.fill((8, 2, 28), (20, 4, 34), "jaffabricate:pallet_full")
    # Rejected packaging lots accumulate behind a quarantine stripe as the anomaly begins.
    t.fill((45, 1, 33), (56, 1, 39), "minecraft:yellow_concrete")
    t.fill((47, 2, 34), (55, 4, 38), "create:cardboard_block")
    t.chest(52, 2, 36, "infinite_domain:chests/old_world/ows_005_vcf_harvest_packaging_annex", "west")
    return t


def build_007():
    t = base.nuclear_research_annex_clean_master()
    t.fill((5, 10, 10), (38, 12, 10), "minecraft:white_concrete")
    t.fill((12, 11, 9), (31, 14, 9), "minecraft:lime_concrete")
    # Parallel durability and environmental-stress chambers.
    for index, x in enumerate((8, 16, 24, 32), 1):
        t.fill((x, 2, 16), (x + 5, 8, 24), "create:framed_glass")
        t.clear((x + 1, 3, 17), (x + 4, 7, 23))
        t.fill((x + 1, 2, 18), (x + 4, 2, 22), "farmersdelight:rich_soil")
        if index % 2:
            t.fill((x + 2, 3, 19), (x + 3, 3, 21), "minecraft:wheat", age="7")
        else:
            t.fill((x + 2, 2, 19), (x + 3, 2, 21), "minecraft:mycelium")
            t.set(x + 2, 3, 20, "minecraft:brown_mushroom")
    # Storage and reseeding deliberately test long-duration viability.
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
    # Repeated sterilization cells and clean-zone checkpoints.
    for index, x in enumerate((7, 18, 29, 40), 1):
        t.fill((x, 2, 14), (x + 7, 8, 23), "create:framed_glass")
        t.clear((x + 1, 3, 15), (x + 6, 7, 22))
        t.fill((x + 1, 2, 25), (x + 6, 2, 27), "minecraft:yellow_concrete")
        t.fill((x + 2, 3, 26), (x + 5, 3, 26), "create:fluid_pipe")
        # Contamination returns farther into each successive supposedly clean room.
        seam = x + min(index + 1, 6)
        t.fill((seam, 2, 20), (seam, 2, 22), "minecraft:mycelium")
        t.set(seam, 3, 21, "minecraft:brown_mushroom")
    # Service-joint investigation corridor and incident archive.
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


EXTENSIONS = VCF_COMPLETION + ATLAS_EXTENSION
core.SPECS = tuple(sorted(core.SPECS + EXTENSIONS, key=lambda spec: int(spec.target[-3:])))
core.BY_TARGET.update({spec.target: spec for spec in EXTENSIONS})
core.BUILDERS.update({
    "OWS-005": build_005,
    "OWS-007": build_007,
    "OWS-008": build_008,
    "OWS-011": build_011,
    "OWS-013": build_013,
    "OWS-014": build_014,
})

Spec = core.Spec
SPECS = core.SPECS
BY_TARGET = core.BY_TARGET
BUILDERS = core.BUILDERS


def _sync_registry() -> None:
    targets_path = REGISTRY / "structure_targets.json"
    if not targets_path.is_file():
        return
    document = json.loads(targets_path.read_text(encoding="utf-8"))
    targets = document["targets"]
    for spec in SPECS:
        row = targets[int(spec.target[-3:]) - 1]
        row.update({
            "implementation_status": "implemented_static_runtime_deferred",
            "mapped_source_structure": spec.source_id,
            "narrative_structure": spec.structure_id,
            "narrative_source_template": f"kubejs/data/infinite_domain/structure/wasteland/old_world/{spec.name}.nbt",
            "acceptance_dimensions": list(spec.dimensions),
            "runtime_validation": "deferred",
        })
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
        state["current_wave"] = "vcf_family_closure_and_atlas_controls_wave"
        implemented_set = set(implemented)
        state["next_targets"] = [
            row["id"] for row in targets
            if row["id"] not in implemented_set and row.get("implementation_status") == "approved_for_mapping"
        ][:5]
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    core.main()
    _sync_registry()
    print("Extended authoritative Old World generator through the complete VCF and Atlas families.")


if __name__ == "__main__":
    main()
