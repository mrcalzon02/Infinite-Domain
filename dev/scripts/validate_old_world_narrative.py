#!/usr/bin/env python3
"""[SYSTEM REPORT] Static contract validation for the Old World narrative automation."""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import generate_wasteland_sites as structure_base
from pathlib import Path

from generate_old_world_narrative_structures import (
    CONTROLLED_WORLDGEN_TARGETS,
    DARKNET_RETURN_TARGETS,
    SPECS,
)

ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "dev/old_world_narrative"
REGISTRY = PROGRAM / "registry"
DATA = ROOT / "kubejs" / "data" / "infinite_domain"
ITEM_TEXTURES = ROOT / "kubejs" / "assets" / "kubejs" / "textures" / "item"
PREPARED_SITE_QUESTS = PROGRAM / "quests" / "prepared_site_surveys.snbt"
PREPARED_SITE_LANG = PROGRAM / "quests" / "prepared_site_surveys_lang.snbt"
SITE_QUEST_CATALOG = REGISTRY / "site_quest_catalog.json"
WORLDGEN_ROLE_REGISTRY = ROOT / "dev/docs" / "old-world" / "structure-worldgen-roles.json"
WASTELAND_CORPUS_MANIFEST = ROOT / "dev/structure_library" / "corpus-manifest.json"
PHASE_STATE = ROOT / "dev/docs" / "old-world" / "phase-state.json"
REVISION_MATRIX = PROGRAM / "source" / "04_STRUCTURE_REVISION_MATRIX.csv"
CANON = "eec4d3149e5e5823b330d5b01127b8f6e592d1938ef4e491f719617e507bf182"
DIMENSIONS = {
    "silhouette_exterior_identity",
    "interior_zoning_circulation",
    "functional_machinery_props",
    "institutional_identity",
    "historical_damage_signature",
    "narrative_evidence_loot",
}
DESTINATION_QUESTS = {
    "OWS-001": "4F57000000000011",
    "OWS-002": "4F57000000000013",
    "OWS-003": "4F57000000000015",
    "OWS-004": "4F57000000000030",
    "OWS-006": "4F57000000000032",
    "OWS-009": "4F57000000000002",
    "OWS-010": "4F57000000000004",
    "OWS-012": "4F57000000000040",
    "OWS-015": "4F57000000000021",
    "OWS-016": "4F57000000000023",
}
SITE_QUEST_BASE = int("4F58000000000000", 16)
SITE_STRUCTURE_TASK_BASE = int("4F58100000000000", 16)
SITE_PROOF_TASK_BASE = int("4F58200000000000", 16)
SITE_LEAD_QUEST_ID = "4F58F00000000000"
SITE_LEAD_TASK_ID = "4F58F10000000000"
ATLAS_TARGETS = {f"OWS-{index:03d}" for index in range(9, 15)}
VCF_TARGETS = {f"OWS-{index:03d}" for index in range(1, 9)}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def deterministic_items(table: dict) -> set[str]:
    result: set[str] = set()
    for pool in table.get("pools", []):
        entries = pool.get("entries", [])
        if pool.get("rolls") == 1 and len(entries) == 1 and entries[0].get("type") == "minecraft:item":
            result.add(entries[0].get("name"))
    return result


def ftb_id(base: int, target: str) -> str:
    return f"{base + int(target[-3:]):016X}"


def prepared_map_reward_id(target: str) -> str:
    return "71E" + hashlib.sha256(f"old-world-site-map:{target}".encode()).hexdigest()[:13].upper()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scope-worldgen-only",
        action="store_true",
        help="Validate the 84-source/64-descendant boundary and placement ownership without the legacy serialized-block audit.",
    )
    args = parser.parse_args()

    expected_targets = [f"OWS-{i:03d}" for i in range(1, 65)]
    spec_targets = [spec.target for spec in SPECS]
    require(len(SPECS) == 64, f"authoritative generator must expose 64 specs, found {len(SPECS)}")
    require(spec_targets == expected_targets, "authoritative generator must expose the stable OWS-001 through OWS-064 sequence")
    require(len(set(spec_targets)) == 64, "authoritative generator contains duplicate OWS targets")

    manifest = read_json(PROGRAM / "source" / "source-manifest.json")
    require(manifest["canon_docx_sha256"] == CANON, "canonical narrative checksum is not pinned")

    registry = read_json(REGISTRY / "structure_targets.json")
    targets = registry["targets"]
    require(registry.get("target_count") == 64, "Old World registry target_count must remain 64")
    require(len(targets) == 64, "structure registry must contain 64 targets")
    require([row["id"] for row in targets] == expected_targets, "unstable OWS ID sequence")
    with REVISION_MATRIX.open(encoding="utf-8", newline="") as handle:
        matrix_targets = [row["id"] for row in csv.DictReader(handle)]
    require(matrix_targets == expected_targets, "canonical revision matrix must contain OWS-001 through OWS-064 exactly once")

    phase_state = read_json(PHASE_STATE)
    corpus_manifest = read_json(WASTELAND_CORPUS_MANIFEST)
    require(
        phase_state["prerequisite_handoff"].get("accepted_source_structures") == 84,
        "Old World prerequisite handoff must retain the 84-template Wasteland source corpus",
    )
    require(
        corpus_manifest["counts"].get("inbuilt_variants_and_sources") == 84,
        "authoritative Wasteland source corpus must retain 84 templates",
    )

    worldgen_roles = read_json(WORLDGEN_ROLE_REGISTRY).get("roles", {})
    require(list(worldgen_roles) == expected_targets, "worldgen-role registry must cover OWS-001 through OWS-064 in order")
    require(
        {row.get("role") for row in worldgen_roles.values()}
        <= {
            "CITY_INTEGRATED",
            "RURAL_INTEGRATED",
            "HIGHWAY_INTEGRATED",
            "INDEPENDENT_MOUNTAIN",
            "COASTAL_TERMINAL",
            "INDEPENDENT_LANDMARK",
        },
        "worldgen-role registry contains an unknown placement role",
    )
    require(read_json(REGISTRY / "lore_seed.json")["seed_count"] == 36, "lore seed count changed")
    spine = read_json(REGISTRY / "quest_spine.json")
    require(spine["major_quest_count"] == 13 and spine["quests"][0]["title"] == "THEY WERE HERE FIRST", "canonical quest spine changed")

    proof_registry = read_json(ROOT / "kubejs" / "config" / "old_world_evidence.json")
    proof_rows = proof_registry["items"]
    proof_ids = {f"kubejs:{entry['id']}" for entry in proof_rows}
    evidence_by_site = {entry["site"]: entry for entry in proof_rows}
    require(len(proof_ids) == 64, "canonical proof registry must contain 64 unique IDs")
    require(set(evidence_by_site) == set(expected_targets), "canonical evidence registry must cover every OWS site exactly once")
    proof_startup = (ROOT / "kubejs" / "startup_scripts" / "old_world_evidence_items.js").read_text(encoding="utf-8")
    require("oldWorldEvidence.items.forEach" in proof_startup, "canonical proof startup no longer consumes the JSON registry")
    supplemental_startup = (ROOT / "kubejs" / "startup_scripts" / "old_world_narrative_items.js").read_text(encoding="utf-8")

    chapter = (ROOT / "config" / "ftbquests" / "quests" / "chapters" / "old_world_investigation.snbt").read_text(encoding="utf-8")
    require(SITE_LEAD_QUEST_ID not in chapter, "activation-gated survey root leaked into the live FTB chapter")

    require(SITE_QUEST_CATALOG.is_file(), "64-site prepared quest catalog was not generated")
    require(PREPARED_SITE_QUESTS.is_file(), "prepared site survey SNBT was not generated")
    require(PREPARED_SITE_LANG.is_file(), "prepared site survey language SNBT was not generated")
    quest_catalog = read_json(SITE_QUEST_CATALOG)
    prepared_quests = PREPARED_SITE_QUESTS.read_text(encoding="utf-8")
    prepared_lang = PREPARED_SITE_LANG.read_text(encoding="utf-8")
    require(quest_catalog["status"] == "fully_authored_activation_gated", "prepared quest catalog status is stale")
    require(quest_catalog["site_count"] == 64, "prepared quest catalog must contain 64 site entries")
    require(quest_catalog["lead_quest_id"] == SITE_LEAD_QUEST_ID, "prepared quest lead ID is unstable")
    require(f'id: "{SITE_LEAD_QUEST_ID}"' in prepared_quests, "prepared survey root quest is missing")
    require(f'id: "{SITE_LEAD_TASK_ID}"' in prepared_quests, "prepared survey root task is missing")

    institution_order: list[str] = []
    institution_sites: dict[str, list[str]] = {}
    for target in expected_targets:
        institution = evidence_by_site[target]["institution"]
        if institution not in institution_sites:
            institution_order.append(institution)
            institution_sites[institution] = []
        institution_sites[institution].append(target)
    require(quest_catalog["institution_count"] == len(institution_order), "prepared quest institution count is stale")
    require(quest_catalog["institutions"] == institution_order, "prepared quest institution order is unstable")

    major_hooks: dict[str, list[str]] = {target: [] for target in expected_targets}
    for quest in spine["quests"]:
        for target in quest["target_structures"]:
            if target in major_hooks:
                major_hooks[target].append(f"{quest['id']}:{quest['title']}")

    catalog_sites = quest_catalog["sites"]
    expected_catalog_order = [
        target
        for institution in institution_order
        for target in institution_sites[institution]
    ]
    require(
        [entry["target_id"] for entry in catalog_sites] == expected_catalog_order,
        "prepared quest catalog institution-grouped order is unstable",
    )
    require(set(expected_catalog_order) == set(expected_targets) and len(expected_catalog_order) == 64, "prepared quest catalog order does not cover all OWS targets exactly once")
    catalog_by_target = {entry["target_id"]: entry for entry in catalog_sites}
    require(len(catalog_by_target) == 64, "prepared quest catalog contains duplicate target entries")

    first_sites = {sites[0] for sites in institution_sites.values()}
    for target in sorted(first_sites):
        spec = SPECS[int(target[-3:]) - 1]
        require(
            f"structure_map {spec.structure_id} 2" in prepared_quests,
            f"{target} institution lead locator is missing from the prepared survey root",
        )
        require(
            f'id: "{prepared_map_reward_id(target)}"' in prepared_quests,
            f"{target} institution lead locator reward ID is unstable",
        )

    structure_set_dir = DATA / "worldgen" / "structure_set" / "old_world"
    structure_set_paths = sorted(structure_set_dir.glob("*.json"))
    expected_set_files = {
        "controlled_pt9_probe.json",
        "old_world_city_sites.json",
        "old_world_landmark_sites.json",
        "old_world_mountain_sites.json",
        "old_world_port_sites.json",
        "old_world_rural_sites.json",
    }
    require(
        {path.name for path in structure_set_paths} == expected_set_files,
        "Old World grouped natural-worldgen set inventory is stale",
    )
    structure_sets = {path.stem: read_json(path) for path in structure_set_paths}
    controlled_set = structure_sets["controlled_pt9_probe"]
    require(
        controlled_set.get("placement", {}).get("type") == "minecraft:random_spread",
        "Old World controlled placement must use ordinary datapack random-spread ownership",
    )
    for set_name, structure_set in structure_sets.items():
        require(
            structure_set.get("placement", {}).get("type") == "minecraft:random_spread",
            f"Old World set {set_name} must use ordinary datapack random-spread ownership",
        )
        serialized = json.dumps(structure_set, sort_keys=True).lower()
        require(
            not any(token in serialized for token in ("quest", "player", "team", "advancement", "scoreboard", "game_stage", "gamestage")),
            f"Old World set {set_name} must not depend on quest or player progression state",
        )

    registered_list = [
        entry["structure"]
        for value in structure_sets.values()
        for entry in value["structures"]
    ]
    registered = set(registered_list)
    require(len(registered_list) == len(registered), "Old World structure sets contain a duplicate target")
    independent_roles = {"INDEPENDENT_MOUNTAIN", "INDEPENDENT_LANDMARK", "COASTAL_TERMINAL"}
    expected_worldgen_targets = {
        target
        for target, role in worldgen_roles.items()
        if role["role"] in independent_roles or target in DESTINATION_QUESTS
    }
    expected_active = {
        next(spec.structure_id for spec in SPECS if spec.target == target)
        for target in expected_worldgen_targets
    }
    require(len(expected_worldgen_targets) == 20, "Old World grouped worldgen must cover exactly 20 locatable/independent targets")
    require(registered == expected_active, "Old World grouped worldgen contains a staged or missing target")
    require(
        {entry["structure"] for entry in controlled_set["structures"]}
        == {next(spec.structure_id for spec in SPECS if spec.target == "OWS-006")},
        "PT-9 controlled set must remain limited to OWS-006",
    )

    if args.scope_worldgen_only:
        for spec in SPECS:
            pool = read_json(DATA / "worldgen" / "template_pool" / "old_world" / f"{spec.name}.json")
            worldgen = read_json(DATA / "worldgen" / "structure" / "old_world" / f"{spec.name}.json")
            worldgen_role = worldgen_roles[spec.target]
            require(worldgen_role["file"] == f"{spec.name}.json", f"{spec.target} worldgen-role filename is stale")
            require(worldgen["start_pool"] == f"infinite_domain:old_world/{spec.name}", f"{spec.target} start pool is stale")
            require(worldgen["biomes"] == worldgen_role["biomes_tag"], f"{spec.target} worldgen biome role is stale")
            require(
                pool["elements"][0]["element"]["location"] == f"infinite_domain:wasteland/old_world/{spec.name}",
                f"{spec.target} template is stale",
            )
        print("Old World source/descendant scope: 84 / 64")
        print("Old World grouped natural worldgen: 20 targets across 6 random-spread sets")
        print("Old World placement ownership: datapack-only; no quest/player/team gate")
        return

    renders = {
        entry["structure_id"]: entry
        for entry in read_json(PROGRAM / "reviews" / "render-manifest.json")["structures"]
    }

    def registered_item(item: str) -> bool:
        if item in proof_ids:
            return True
        local = item.split(":", 1)[1]
        return f"event.create('{local}')" in supplemental_startup or f'event.create("{local}")' in supplemental_startup

    integrated_count = 0
    for spec in SPECS:
        row = targets[int(spec.target[-3:]) - 1]
        evidence = evidence_by_site[spec.target]
        quest_entry = catalog_by_target[spec.target]
        institution_sites_for_spec = institution_sites[evidence["institution"]]
        institution_index = institution_sites_for_spec.index(spec.target)
        predecessor = institution_sites_for_spec[institution_index - 1] if institution_index else None
        next_target = institution_sites_for_spec[institution_index + 1] if institution_index + 1 < len(institution_sites_for_spec) else None
        expected_quest_id = ftb_id(SITE_QUEST_BASE, spec.target)
        expected_structure_task = ftb_id(SITE_STRUCTURE_TASK_BASE, spec.target)
        expected_proof_task = ftb_id(SITE_PROOF_TASK_BASE, spec.target)
        expected_dependency = ftb_id(SITE_QUEST_BASE, predecessor) if predecessor else SITE_LEAD_QUEST_ID
        is_probe = spec.target in CONTROLLED_WORLDGEN_TARGETS

        require(row["narrative_structure"] == spec.structure_id, f"{spec.target} registry mapping is stale")
        require(row["implementation_status"] == "implemented_static_runtime_deferred", f"{spec.target} status is stale")
        require(row.get("functional_status") == "static_source_implemented", f"{spec.target} functional status must remain source-level until runtime validation")
        require(row.get("quality_status") == "schematic_revision_pending", f"{spec.target} schematic revision debt is not recorded")
        require(set(row["acceptance_dimensions"]) == DIMENSIONS, f"{spec.target} must implement all six revision dimensions")
        require(set(spec.dimensions) == DIMENSIONS, f"{spec.target} spec does not carry all six revision dimensions")
        require(registered_item(spec.proof), f"{spec.proof} is not registered")
        if spec.lore:
            require(registered_item(spec.lore), f"{spec.lore} is not registered")

        require(quest_entry["institution"] == evidence["institution"], f"{spec.target} prepared quest institution is stale")
        require(quest_entry["quest_id"] == expected_quest_id, f"{spec.target} prepared quest ID is unstable")
        require(quest_entry["structure_task_id"] == expected_structure_task, f"{spec.target} structure task ID is unstable")
        require(quest_entry["proof_task_id"] == expected_proof_task, f"{spec.target} proof task ID is unstable")
        require(quest_entry["dependency_quest_id"] == expected_dependency, f"{spec.target} dependency quest ID is stale")
        require(quest_entry["predecessor_target"] == predecessor, f"{spec.target} institution predecessor is stale")
        require(quest_entry["next_target"] == next_target, f"{spec.target} institution successor is stale")
        require(quest_entry["structure_id"] == spec.structure_id, f"{spec.target} prepared structure task target is stale")
        require(quest_entry["proof_item"] == spec.proof, f"{spec.target} prepared proof task target is stale")
        require(quest_entry["locator_command"] == f"/structure_map {spec.structure_id} 2", f"{spec.target} prepared locator command is stale")
        require(quest_entry["locator_reward_id"] == prepared_map_reward_id(spec.target), f"{spec.target} prepared locator reward ID is unstable")
        require(quest_entry["locator_reward_source"] == (SITE_LEAD_QUEST_ID if predecessor is None else expected_dependency), f"{spec.target} prepared locator reward source is stale")
        require(quest_entry["major_quest_hooks"] == major_hooks[spec.target], f"{spec.target} major quest hooks are stale")
        require(quest_entry["requires_worldgen_activation"] is (not is_probe), f"{spec.target} prepared quest activation guard is stale")
        require(quest_entry["darknet_return_reserved"] is (spec.target in DARKNET_RETURN_TARGETS), f"{spec.target} prepared Darknet reservation is stale")
        require(quest_entry["activation_state"] == ("controlled_probe_ready" if is_probe else "authored_staged_not_live"), f"{spec.target} prepared activation state is stale")

        require(f'id: "{expected_quest_id}"' in prepared_quests, f"{spec.target} prepared quest block is missing")
        require(f'id: "{expected_structure_task}" structure: "{spec.structure_id}"' in prepared_quests, f"{spec.target} prepared structure task is missing")
        require(f'id: "{expected_proof_task}" item: {{ count: 1, id: "{spec.proof}" }}' in prepared_quests, f"{spec.target} prepared proof task is missing")
        require(f'quest.{expected_quest_id}.title:' in prepared_lang, f"{spec.target} prepared quest language is missing")
        require(f'task.{expected_structure_task}.title:' in prepared_lang, f"{spec.target} prepared structure-task language is missing")
        require(f'task.{expected_proof_task}.title:' in prepared_lang, f"{spec.target} prepared proof-task language is missing")
        if next_target:
            next_spec = SPECS[int(next_target[-3:]) - 1]
            require(f"structure_map {next_spec.structure_id} 2" in prepared_quests, f"{spec.target} does not hand off the next institutional locator")
            require(f'id: "{prepared_map_reward_id(next_target)}"' in prepared_quests, f"{spec.target} next locator reward ID is unstable")

        require(
            row["worldgen_activation"] == ("controlled_pt9_probe" if is_probe else "staged_not_in_structure_set"),
            f"{spec.target} worldgen activation state is stale",
        )
        require(
            row["runtime_validation"] == ("pending_controlled_test" if is_probe else "deferred"),
            f"{spec.target} runtime validation state is stale",
        )
        require(row["locator"]["command"] == f"/structure_map {spec.structure_id} 2", f"{spec.target} locator command is stale")
        require(
            row["locator"]["status"] == ("controlled_probe_ready" if is_probe else "prepared_requires_worldgen_activation"),
            f"{spec.target} locator readiness is stale",
        )
        require(row["exploration_hook"]["mode"] == "additive_old_world_investigation", f"{spec.target} exploration hook is not additive")
        require(row["exploration_hook"]["requires_worldgen_activation"] is (not is_probe), f"{spec.target} exploration activation guard is stale")

        if spec.target in DARKNET_RETURN_TARGETS:
            hook = row.get("darknet_return_hook", {})
            require(hook.get("status") == "reserved_for_later_darknet_phase", f"{spec.target} Darknet return hook is missing")
            require(hook.get("purpose") == DARKNET_RETURN_TARGETS[spec.target], f"{spec.target} Darknet return purpose is stale")
        else:
            require("darknet_return_hook" not in row, f"{spec.target} has an unplanned Darknet return hook")

        # Existing live quests remain a separate contract from the prepared
        # catalog. Do not force staged destinations into live player progression.
        if spec.target in DESTINATION_QUESTS:
            integrated_count += 1
            for item in (spec.proof, spec.lore):
                if item:
                    require(f'id: "{item}"' in chapter, f"{item} has no live quest task")
            require(f'structure: "{spec.structure_id}"' in chapter, f"{spec.target} has no live structure task")
            require(f"structure_map {spec.structure_id} 2" in chapter, f"{spec.target} has no live locator handoff")
            expected_reward = "70E" + hashlib.sha256(DESTINATION_QUESTS[spec.target].encode()).hexdigest()[:13].upper()
            require(f'id: "{expected_reward}"' in chapter, f"{spec.target} live locator reward ID is not stable")

        require(
            (spec.structure_id in registered) is (spec.target in expected_worldgen_targets),
            f"{spec.target} grouped structure-set ownership is wrong",
        )

        pool = read_json(DATA / "worldgen" / "template_pool" / "old_world" / f"{spec.name}.json")
        worldgen = read_json(DATA / "worldgen" / "structure" / "old_world" / f"{spec.name}.json")
        worldgen_role = worldgen_roles[spec.target]
        require(worldgen_role["file"] == f"{spec.name}.json", f"{spec.target} worldgen-role filename is stale")
        require(worldgen["start_pool"] == f"infinite_domain:old_world/{spec.name}", f"{spec.target} start pool is stale")
        require(worldgen["biomes"] == worldgen_role["biomes_tag"], f"{spec.target} staged worldgen biome role is stale")
        require(pool["elements"][0]["element"]["location"] == f"infinite_domain:wasteland/old_world/{spec.name}", f"{spec.target} template is stale")

        mandatory = {spec.proof} | ({spec.lore} if spec.lore else set())
        loot = read_json(DATA / "loot_table" / "chests" / "old_world" / f"{spec.name}.json")
        require(mandatory.issubset(deterministic_items(loot)), f"{spec.target} proof loot is not deterministic")

        if not args.scope_worldgen_only:
            raw = gzip.decompress((DATA / "structure" / "wasteland" / "old_world" / f"{spec.name}.nbt").read_bytes())
            require(spec.loot_id.encode() in raw, f"{spec.target} NBT lacks its proof chest")
            for block in spec.required_blocks:
                serialized_block = structure_base.STRUCTURE_BLOCK_REPLACEMENTS.get(block, block)
                require(
                    serialized_block.encode() in raw,
                    f"{spec.target} lacks required serialized block {serialized_block} (declared {block})",
                )

        require(spec.structure_id in renders, f"{spec.target} has no static review renders")
        require(len(renders[spec.structure_id]["renders"]) == 4, f"{spec.target} needs four review views")
        require(renders[spec.structure_id]["visual_approval"] is False, f"{spec.target} must not claim runtime approval")

        proof_texture = ITEM_TEXTURES / f"{spec.proof.split(':', 1)[1]}.png"
        if spec.target in VCF_TARGETS:
            require(proof_texture.is_file(), f"{spec.target} accepted VCF proof texture is missing")
        if spec.target in ATLAS_TARGETS:
            require(not proof_texture.exists(), f"{spec.target} rejected Atlas proof art is still present")

    state = read_json(REGISTRY / "implementation_state.json")
    live_targets = sorted(spec.target for spec in SPECS if f'structure: "{spec.structure_id}"' in chapter)
    require(state.get("quest_authored") == expected_targets, "implementation state must record all 64 authored site quests")
    require(state.get("quest_live") == live_targets, "implementation state live-quest list is stale")
    require(state.get("quest_activation_pending") == sorted(set(expected_targets) - set(live_targets)), "implementation state activation-pending list is stale")
    require(state.get("quest_layer_status") == "full_64_site_catalog_authored_activation_gated", "implementation state quest-layer status is stale")

    require(len(DARKNET_RETURN_TARGETS) >= 5, "at least five earlier sites must reserve meaningful Darknet return visits")
    require(set(DARKNET_RETURN_TARGETS).issubset(set(expected_targets)), "Darknet return hook references an unimplemented site")

    heavy_state = read_json(REGISTRY / "heavy_rebuild_state.json")
    require(heavy_state.get("scope") == "OWS-001 through OWS-064", "heavy-rebuild scope drifted from the 64-target narrative program")
    require(not heavy_state.get("runtime_quality_approved"), "runtime-quality approvals require retained in-world evidence")
    if heavy_state.get("active_target") == "OWS-008":
        gate_a = heavy_state.get("visual_review_gates", {}).get("gate_a_massing", {})
        require(
            gate_a.get("status") in {"r2_rendered_pending_manual_review", "passed_r2"},
            "OWS-008 Gate-A state must track the r2 candidate rather than the revision-required r1 artifact",
        )
        r1_review = (PROGRAM / "reviews" / "heavy_rebuild" / "OWS-008_GATE_A_R1_REVIEW.md").read_text(encoding="utf-8")
        require("OWS-008 GATE A r1: REVISION REQUIRED" in r1_review, "OWS-008 Gate-A r1 rejection record is missing")
        if gate_a.get("status") != "passed_r2":
            r2_candidate = (PROGRAM / "reviews" / "heavy_rebuild" / "OWS-008_GATE_A_R2_CANDIDATE.md").read_text(encoding="utf-8")
            require("GATE A R2: REVIEW NEEDED" in r2_candidate, "OWS-008 Gate-A r2 pending-review boundary is missing")

    print(
        f"Old World static validation passed: 84 source templates, 64 narrative structures, "
        f"64 activation-gated site quests, "
        f"13 canonical major quests, {len(registered)} controlled worldgen target, "
        f"{integrated_count} live early-site integrations, {len(DARKNET_RETURN_TARGETS)} Darknet return hooks; "
        f"mode={'scope_worldgen' if args.scope_worldgen_only else 'full'}."
    )


if __name__ == "__main__":
    main()
