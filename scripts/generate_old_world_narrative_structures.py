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


def build_011():
    t = base.fire_station_clean_master()
    # Municipal shell remains recognizable; Atlas takes over the apparatus/service program.
    t.fill((4, 8, 7), (38, 10, 7), "minecraft:orange_concrete")
    t.fill((9, 11, 6), (33, 13, 6), "minecraft:white_concrete")
    t.fill((14, 12, 5), (28, 14, 5), "minecraft:orange_concrete")
    for bay, x in enumerate((5, 16, 27), 1):
        t.fill((x, 1, 11), (x + 8, 1, 18), "minecraft:yellow_concrete")
        t.fill((x + 1, 2, 20), (x + 4, 3, 21), "create:andesite_casing")
        t.set(x + 2, 2, 23, "minecraft:anvil")
        t.fill((x + 5, 2, 20), (x + 7, 3, 22), "immersiveengineering:crate")
        t.fill((x + 1, 2, 25), (x + 6, 2, 26), "minecraft:orange_concrete")
    # The last bay is no longer a complete repair line: it is being stripped to keep the others alive.
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
    # Cell four is explicitly in emergency manual mode and has been cannibalized for replacement drive parts.
    t.fill((34, 1, 12), (43, 1, 28), "minecraft:yellow_concrete")
    t.fill((36, 2, 20), (43, 5, 23), "minecraft:scaffolding")
    t.fill((37, 2, 25), (42, 4, 27), "create:andesite_casing")
    t.fill((6, 2, 32), (18, 4, 34), "immersiveengineering:crate")
    t.chest(15, 2, 33, "infinite_domain:chests/old_world/ows_013_atlas_automated_assembly_hall", "west")
    return t


def build_014():
    t = base.ae2_records_archive_clean_master()
    # The archive becomes a live industrial-control integration campus.
    t.fill((6, 9, 10), (57, 11, 10), "minecraft:orange_concrete")
    t.fill((18, 22, 25), (58, 24, 25), "minecraft:light_blue_concrete")
    t.fill((34, 25, 33), (46, 27, 33), "minecraft:black_concrete")
    # Prototype Atlas control cells occupy the intake wing without erasing the secure archive route.
    for x in (8, 15, 22):
        t.fill((x, 2, 14), (x + 3, 3, 16), "create:andesite_casing")
        t.set(x + 1, 2, 18, "create:depot")
        t.fill((x, 1, 20), (x + 3, 1, 22), "minecraft:orange_concrete")
        t.fill((x + 1, 2, 23), (x + 2, 3, 23), "minecraft:polished_blackstone")
        t.set(x + 1, 3, 22, "minecraft:lever", face="wall", facing="north", powered="false")
    # Cross-vendor retrofit language: cyan power path, black secured data path, Atlas orange integration spine.
    t.fill((39, 13, 27), (57, 13, 28), "minecraft:orange_concrete")
    t.fill((41, 14, 30), (56, 14, 31), "minecraft:light_blue_concrete")
    t.fill((41, 14, 46), (56, 14, 47), "minecraft:black_concrete")
    t.fill((45, 14, 34), (55, 17, 36), "ae2:drive")
    t.fill((47, 14, 39), (53, 17, 42), "ae2:controller")
    t.fill((46, 14, 18), (55, 17, 20), "immersiveengineering:capacitor_hv")
    # Late-containment isolation and redundant manual switching show the system being kept alive by retrofit.
    t.fill((34, 13, 43), (58, 13, 49), "minecraft:yellow_concrete")
    for x in (37, 43, 49, 55):
        t.fill((x, 14, 44), (x + 2, 15, 44), "minecraft:polished_blackstone")
        t.set(x + 1, 15, 43, "minecraft:lever", face="wall", facing="north", powered="false")
    t.chest(54, 14, 33, "infinite_domain:chests/old_world/ows_014_atlas_industrial_controls_integration_center", "west")
    return t


core.SPECS = core.SPECS + ATLAS_EXTENSION
core.BY_TARGET.update({spec.target: spec for spec in ATLAS_EXTENSION})
core.BUILDERS.update({
    "OWS-011": build_011,
    "OWS-013": build_013,
    "OWS-014": build_014,
})

# Public compatibility exports for validators and tooling.
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
        state["current_wave"] = "atlas_service_assembly_controls_wave"
        implemented_set = set(implemented)
        state["next_targets"] = [
            row["id"] for row in targets
            if row["id"] not in implemented_set and row.get("implementation_status") == "approved_for_mapping"
        ][:5]
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    core.main()
    _sync_registry()
    print("Extended authoritative Old World generator through Atlas OWS-014.")


if __name__ == "__main__":
    main()
