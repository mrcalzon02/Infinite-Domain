#!/usr/bin/env python3
"""[SYSTEM REPORT] Static contract validation for the Old World narrative automation."""
from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path

from generate_old_world_narrative_structures import (
    CONTROLLED_WORLDGEN_TARGETS,
    DARKNET_RETURN_TARGETS,
    SPECS,
)

ROOT = Path(__file__).resolve().parents[1]
PROGRAM = ROOT / "old_world_narrative"
REGISTRY = PROGRAM / "registry"
DATA = ROOT / "kubejs" / "data" / "infinite_domain"
ITEM_TEXTURES = ROOT / "kubejs" / "assets" / "kubejs" / "textures" / "item"
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
ATLAS_TARGETS = {f"OWS-{index:03d}" for index in range(9, 15)}
VCF_TARGETS = {f"OWS-{index:03d}" for index in range(1, 9)}


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def deterministic_items(table):
    result = set()
    for pool in table.get("pools", []):
        entries = pool.get("entries", [])
        if pool.get("rolls") == 1 and len(entries) == 1 and entries[0].get("type") == "minecraft:item":
            result.add(entries[0].get("name"))
    return result


def main():
    manifest = read_json(PROGRAM / "source" / "source-manifest.json")
    require(manifest["canon_docx_sha256"] == CANON, "canonical narrative checksum is not pinned")

    registry = read_json(REGISTRY / "structure_targets.json")
    targets = registry["targets"]
    require(len(targets) == 64, "structure registry must contain 64 targets")
    require([row["id"] for row in targets] == [f"OWS-{i:03d}" for i in range(1, 65)], "unstable OWS ID sequence")
    require(read_json(REGISTRY / "lore_seed.json")["seed_count"] == 36, "lore seed count changed")
    spine = read_json(REGISTRY / "quest_spine.json")
    require(spine["major_quest_count"] == 13 and spine["quests"][0]["title"] == "THEY WERE HERE FIRST", "canonical quest spine changed")

    proof_registry = read_json(ROOT / "kubejs" / "config" / "old_world_evidence.json")
    proof_ids = {f"kubejs:{entry['id']}" for entry in proof_registry["items"]}
    require(len(proof_ids) == 64, "canonical proof registry must contain 64 unique IDs")
    proof_startup = (ROOT / "kubejs" / "startup_scripts" / "old_world_evidence_items.js").read_text(encoding="utf-8")
    require("oldWorldEvidence.items.forEach" in proof_startup, "canonical proof startup no longer consumes the JSON registry")
    supplemental_startup = (ROOT / "kubejs" / "startup_scripts" / "old_world_narrative_items.js").read_text(encoding="utf-8")

    chapter = (ROOT / "config" / "ftbquests" / "quests" / "chapters" / "old_world_investigation.snbt").read_text(encoding="utf-8")

    structure_set_dir = DATA / "worldgen" / "structure_set" / "old_world"
    structure_set_paths = sorted(structure_set_dir.glob("*.json"))
    require(
        [path.name for path in structure_set_paths] == ["controlled_pt9_probe.json"],
        "Old World natural worldgen must remain gated to the PT-9 controlled probe",
    )
    structure_sets = {path.stem: read_json(path) for path in structure_set_paths}
    registered = {
        entry["structure"]
        for value in structure_sets.values()
        for entry in value["structures"]
    }
    expected_active = {
        next(spec.structure_id for spec in SPECS if spec.target == target)
        for target in CONTROLLED_WORLDGEN_TARGETS
    }
    require(registered == expected_active, "controlled worldgen set contains a staged or missing target")

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
        require(row["narrative_structure"] == spec.structure_id, f"{spec.target} registry mapping is stale")
        require(row["implementation_status"] == "implemented_static_runtime_deferred", f"{spec.target} status is stale")
        require(set(row["acceptance_dimensions"]) == DIMENSIONS, f"{spec.target} must implement all six revision dimensions")
        require(set(spec.dimensions) == DIMENSIONS, f"{spec.target} spec does not carry all six revision dimensions")
        require(registered_item(spec.proof), f"{spec.proof} is not registered")
        if spec.lore:
            require(registered_item(spec.lore), f"{spec.lore} is not registered")

        is_probe = spec.target in CONTROLLED_WORLDGEN_TARGETS
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

        # Quest wiring is additive and can be prepared before worldgen promotion.
        # Locator rewards for staged sites are explicitly marked as requiring
        # worldgen activation in the registry and must not be treated as runtime proof.
        if spec.target in DESTINATION_QUESTS:
            integrated_count += 1
            for item in (spec.proof, spec.lore):
                if item:
                    require(f'id: "{item}"' in chapter, f"{item} has no quest task")
            require(f'structure: "{spec.structure_id}"' in chapter, f"{spec.target} has no structure task")
            require(f"structure_map {spec.structure_id} 2" in chapter, f"{spec.target} has no locator handoff")
            expected_reward = "70E" + hashlib.sha256(DESTINATION_QUESTS[spec.target].encode()).hexdigest()[:13].upper()
            require(f'id: "{expected_reward}"' in chapter, f"{spec.target} locator reward ID is not stable")

        require((spec.structure_id in registered) is is_probe, f"{spec.target} structure-set gating is wrong")

        pool = read_json(DATA / "worldgen" / "template_pool" / "old_world" / f"{spec.name}.json")
        worldgen = read_json(DATA / "worldgen" / "structure" / "old_world" / f"{spec.name}.json")
        require(worldgen["start_pool"] == f"infinite_domain:old_world/{spec.name}", f"{spec.target} start pool is stale")
        require(worldgen["biomes"] == "#infinite_domain:wasteland_site_biomes", f"{spec.target} staged worldgen definition is stale")
        require(pool["elements"][0]["element"]["location"] == f"infinite_domain:wasteland/old_world/{spec.name}", f"{spec.target} template is stale")

        mandatory = {spec.proof} | ({spec.lore} if spec.lore else set())
        loot = read_json(DATA / "loot_table" / "chests" / "old_world" / f"{spec.name}.json")
        require(mandatory.issubset(deterministic_items(loot)), f"{spec.target} proof loot is not deterministic")

        raw = gzip.decompress((DATA / "structure" / "wasteland" / "old_world" / f"{spec.name}.nbt").read_bytes())
        require(spec.loot_id.encode() in raw, f"{spec.target} NBT lacks its proof chest")
        for block in spec.required_blocks:
            require(block.encode() in raw, f"{spec.target} lacks required block {block}")

        require(spec.structure_id in renders, f"{spec.target} has no static review renders")
        require(len(renders[spec.structure_id]["renders"]) == 4, f"{spec.target} needs four review views")
        require(renders[spec.structure_id]["visual_approval"] is False, f"{spec.target} must not claim runtime approval")

        proof_texture = ITEM_TEXTURES / f"{spec.proof.split(':', 1)[1]}.png"
        if spec.target in VCF_TARGETS:
            require(proof_texture.is_file(), f"{spec.target} accepted VCF proof texture is missing")
        if spec.target in ATLAS_TARGETS:
            require(not proof_texture.exists(), f"{spec.target} rejected Atlas proof art is still present")

    require(len(DARKNET_RETURN_TARGETS) >= 5, "at least five earlier sites must reserve meaningful Darknet return visits")
    require(set(DARKNET_RETURN_TARGETS).issubset({spec.target for spec in SPECS}), "Darknet return hook references an unimplemented site")

    print(
        f"Old World static validation passed: 64 targets, 13-quest canonical spine, "
        f"{len(SPECS)} deterministic sites, {len(registered)} controlled worldgen target, "
        f"{integrated_count} prepared quest integrations, {len(DARKNET_RETURN_TARGETS)} Darknet return hooks."
    )


if __name__ == "__main__":
    main()
