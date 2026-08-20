#!/usr/bin/env python3
"""[SYSTEM REPORT] Static contract validation for the Old World narrative automation."""
from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path

from generate_old_world_narrative_structures import SPECS

ROOT = Path(__file__).resolve().parents[1]
PROGRAM = ROOT / "old_world_narrative"
REGISTRY = PROGRAM / "registry"
DATA = ROOT / "kubejs" / "data" / "infinite_domain"
CANON = "eec4d3149e5e5823b330d5b01127b8f6e592d1938ef4e491f719617e507bf182"
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
    structure_sets = {
        name: read_json(DATA / "worldgen" / "structure_set" / "old_world" / f"{name}.json")
        for name in ("common_sites", "uncommon_sites", "rare_sites")
    }
    registered_by_set = {
        name: {entry["structure"] for entry in value["structures"]}
        for name, value in structure_sets.items()
    }
    registered = set().union(*registered_by_set.values())
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
        require(len(row["acceptance_dimensions"]) >= 4, f"{spec.target} misses the four-dimension floor")
        require(registered_item(spec.proof), f"{spec.proof} is not registered")
        if spec.lore:
            require(registered_item(spec.lore), f"{spec.lore} is not registered")

        # Quest wiring deliberately trails physical-site authoring. Only sites already
        # listed here may claim the locator/task contract; newly built sites remain
        # static content until the Exploration spine reaches them.
        if spec.target in DESTINATION_QUESTS:
            integrated_count += 1
            for item in (spec.proof, spec.lore):
                if item:
                    require(f'id: "{item}"' in chapter, f"{item} has no quest task")
            require(f'structure: "{spec.structure_id}"' in chapter, f"{spec.target} has no structure task")
            require(f"structure_map {spec.structure_id} 2" in chapter, f"{spec.target} has no locator handoff")
            expected_reward = "70E" + hashlib.sha256(DESTINATION_QUESTS[spec.target].encode()).hexdigest()[:13].upper()
            require(f'id: "{expected_reward}"' in chapter, f"{spec.target} locator reward ID is not stable")

        require(spec.structure_id in registered, f"{spec.target} is absent from the structure sets")
        require(spec.structure_id in registered_by_set[spec.set_name], f"{spec.target} is in the wrong rarity set")

        pool = read_json(DATA / "worldgen" / "template_pool" / "old_world" / f"{spec.name}.json")
        worldgen = read_json(DATA / "worldgen" / "structure" / "old_world" / f"{spec.name}.json")
        require(worldgen["start_pool"] == f"infinite_domain:old_world/{spec.name}", f"{spec.target} start pool is stale")
        require(worldgen["biomes"] == "#infinite_domain:wasteland_site_biomes", f"{spec.target} is not active")
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

    require(len(registered) == len(SPECS), "structure sets contain stale or duplicate entries")
    set_names = tuple(registered_by_set)
    for index, left in enumerate(set_names):
        for right in set_names[index + 1:]:
            require(not (registered_by_set[left] & registered_by_set[right]), f"structure rarity sets overlap: {left} and {right}")

    print(
        f"Old World static validation passed: 64 targets, 13-quest canonical spine, "
        f"{len(SPECS)} deterministic sites, {integrated_count} currently quest-integrated."
    )


if __name__ == "__main__":
    main()
