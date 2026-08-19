#!/usr/bin/env python3
"""Generate locatable narrative structures separately from the generic 84-asset corpus."""

from __future__ import annotations

import json
from pathlib import Path

import generate_wasteland_sites as base


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "kubejs" / "data" / "infinite_domain"
STRUCTURE_NAME = "ows_009_atlas_roadside_repair_depot"
STRUCTURE_ID = f"infinite_domain:old_world/{STRUCTURE_NAME}"
LOOT_ID = f"infinite_domain:chests/old_world/{STRUCTURE_NAME}"


def atlas_roadside_repair_depot() -> base.Template:
    """Five-dimension narrative revision of the approved service-garage master."""
    t = base.service_garage_clean_master()

    # Silhouette and identity: a roofline Atlas service blade plus an orange
    # facade band make the depot readable before the player reaches the door.
    t.fill((4, 8, 7), (36, 9, 7), "minecraft:orange_concrete")
    t.fill((13, 12, 6), (27, 14, 6), "minecraft:orange_concrete")
    t.fill((18, 12, 5), (22, 14, 5), "minecraft:polished_blackstone")
    t.set(17, 13, 5, "minecraft:polished_blackstone")
    t.set(23, 13, 5, "minecraft:polished_blackstone")
    t.set(20, 11, 5, "minecraft:polished_blackstone")

    # A real three-stage workflow: diagnostics, component repair, then transfer
    # calibration. Yellow lanes preserve circulation around every workstation.
    for x in (7, 16, 25):
        t.fill((x, 1, 10), (x + 5, 1, 11), "minecraft:yellow_concrete")
    t.set(9, 2, 17, "create:depot")
    t.set(9, 3, 16, "create:mechanical_press", facing="north")
    t.set(18, 2, 17, "create:depot")
    t.set(18, 3, 16, "create:mechanical_press", facing="north")
    t.fill((26, 2, 14), (29, 3, 14), "create:andesite_casing")
    t.fill((26, 2, 20), (29, 3, 20), "create:andesite_casing")
    t.set(27, 2, 17, "minecraft:anvil")
    t.set(28, 2, 17, "immersiveengineering:metal_barrel")

    # Institutional control points and spare-part cages reinforce Atlas's
    # standardized maintenance language without turning the site into a lab.
    t.fill((32, 2, 23), (35, 5, 23), "minecraft:scaffolding")
    t.fill((32, 2, 27), (35, 5, 27), "minecraft:scaffolding")
    t.fill((33, 2, 25), (35, 4, 25), "create:andesite_casing")
    t.fill((5, 2, 27), (12, 2, 28), "minecraft:orange_concrete")
    t.fill((6, 3, 27), (11, 4, 27), "minecraft:polished_blackstone")

    # Mandatory proof and LOR-006 share one deterministic records chest. The
    # clean Phase-A structure intentionally has no generic collapse or spawner.
    t.chest(34, 2, 25, LOOT_ID, "west")
    return t


def guaranteed_loot_table() -> dict[str, object]:
    return {
        "type": "minecraft:chest",
        "random_sequence": LOOT_ID,
        "pools": [
            {
                "rolls": 1,
                "entries": [{"type": "minecraft:item", "name": "kubejs:atlas_service_plate"}],
            },
            {
                "rolls": 1,
                "entries": [{"type": "minecraft:item", "name": "kubejs:atlas_transfer_maintenance_manual"}],
            },
            {
                "rolls": {"type": "minecraft:uniform", "min": 3, "max": 6},
                "entries": [
                    {"type": "minecraft:item", "name": "create:andesite_alloy", "weight": 8},
                    {"type": "minecraft:item", "name": "create:shaft", "weight": 10},
                    {"type": "minecraft:item", "name": "create:cogwheel", "weight": 8},
                    {"type": "minecraft:item", "name": "minecraft:iron_ingot", "weight": 10},
                    {"type": "minecraft:item", "name": "immersiveengineering:component_iron", "weight": 5},
                ],
            },
        ],
    }


def main() -> None:
    template = atlas_roadside_repair_depot()
    base.stabilize_door_pairs(template)
    metrics = base.assess_fidelity("service_garage", template)
    if not metrics["structural_lint_passed"]:
        raise ValueError("OWS-009 failed structural lint: " + "; ".join(metrics["issues"]))
    statistics = template.save(f"old_world/{STRUCTURE_NAME}")

    base.write_json(
        DATA / "worldgen" / "template_pool" / "old_world" / f"{STRUCTURE_NAME}.json",
        {
            "fallback": "minecraft:empty",
            "elements": [
                {
                    "weight": 1,
                    "element": {
                        "location": f"infinite_domain:wasteland/old_world/{STRUCTURE_NAME}",
                        "processors": "minecraft:empty",
                        "projection": "rigid",
                        "element_type": "minecraft:single_pool_element",
                    },
                }
            ],
        },
    )
    base.write_json(
        DATA / "worldgen" / "structure" / "old_world" / f"{STRUCTURE_NAME}.json",
        {
            "type": "minecraft:jigsaw",
            "biomes": "#infinite_domain:wasteland_site_biomes",
            "step": "surface_structures",
            "spawn_overrides": {},
            "terrain_adaptation": "beard_box",
            "start_pool": f"infinite_domain:old_world/{STRUCTURE_NAME}",
            "size": 1,
            "start_height": {"absolute": 0},
            "max_distance_from_center": 80,
            "use_expansion_hack": False,
            "liquid_settings": "ignore_waterlogging",
            "project_start_to_heightmap": "WORLD_SURFACE_WG",
        },
    )
    base.write_json(
        DATA / "worldgen" / "structure_set" / "old_world" / "common_sites.json",
        {
            "structures": [{"structure": STRUCTURE_ID, "weight": 1}],
            "placement": {"type": "minecraft:random_spread", "spacing": 64, "separation": 32, "salt": 90310009},
        },
    )
    base.write_json(DATA / "loot_table" / "chests" / "old_world" / f"{STRUCTURE_NAME}.json", guaranteed_loot_table())
    base.write_json(
        ROOT / "old_world_narrative" / "structures" / "ows-009-atlas-roadside-repair-depot.json",
        {
            "format_version": 1,
            "target_id": "OWS-009",
            "structure_id": STRUCTURE_ID,
            "source_structure": "infinite_domain:service_garage_clean_master",
            "collapse_phase": "Phase A — pre-crisis / normal operation",
            "acceptance_dimensions": {
                "silhouette_exterior_identity": "orange Atlas facade band and roofline service blade",
                "interior_zoning_circulation": "three marked service stages with preserved work and customer routes",
                "functional_machinery_props": "two press/depot stations, calibration bench, parts cages and service stock",
                "institutional_identity": "Atlas color, emblem, standardized lanes, controlled records cage",
                "narrative_evidence_loot": "guaranteed Atlas service plate and LOR-006 maintenance manual",
            },
            "proof_item": "kubejs:atlas_service_plate",
            "lore_record": "kubejs:atlas_transfer_maintenance_manual",
            "loot_table": LOOT_ID,
            "locator_command": f"/structure_map {STRUCTURE_ID} 2",
            "statistics": statistics,
            "structural_lint": metrics,
            "static_render_review": "generated_and_inspected_not_runtime_approval",
            "runtime_validation": "deferred_by_user",
        },
    )
    print(f"Generated {STRUCTURE_ID} with deterministic proof loot.")


if __name__ == "__main__":
    main()
