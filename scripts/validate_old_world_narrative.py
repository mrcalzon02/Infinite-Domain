#!/usr/bin/env python3
"""Static contract validation for the Old World narrative automation."""
from __future__ import annotations
import gzip
import json
from pathlib import Path
from generate_old_world_narrative_structures import SPECS

ROOT = Path(__file__).resolve().parents[1]
PROGRAM = ROOT / "old_world_narrative"
REGISTRY = PROGRAM / "registry"
DATA = ROOT / "kubejs" / "data" / "infinite_domain"
CANON = "eec4d3149e5e5823b330d5b01127b8f6e592d1938ef4e491f719617e507bf182"

def read_json(path): return json.loads(path.read_text(encoding="utf-8"))
def require(condition, message):
    if not condition: raise ValueError(message)

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

    startup = (ROOT / "kubejs" / "startup_scripts" / "old_world_narrative_items.js").read_text(encoding="utf-8")
    chapter = (ROOT / "config" / "ftbquests" / "quests" / "chapters" / "old_world_investigation.snbt").read_text(encoding="utf-8")
    structure_set = read_json(DATA / "worldgen" / "structure_set" / "old_world" / "common_sites.json")
    registered = {entry["structure"] for entry in structure_set["structures"]}
    renders = {entry["structure_id"]: entry for entry in read_json(PROGRAM / "reviews" / "render-manifest.json")["structures"]}

    for spec in SPECS:
        row = targets[int(spec.target[-3:]) - 1]
        require(row["narrative_structure"] == spec.structure_id, f"{spec.target} registry mapping is stale")
        require(row["implementation_status"] == "implemented_static_runtime_deferred", f"{spec.target} status is stale")
        require(len(row["acceptance_dimensions"]) >= 4, f"{spec.target} misses the four-dimension floor")
        for item in (spec.proof, spec.lore):
            if item:
                require(f"event.create('{item.split(':', 1)[1]}')" in startup, f"{item} is not registered")
                require(f'id: "{item}"' in chapter, f"{item} has no quest task")
        require(f'structure: "{spec.structure_id}"' in chapter, f"{spec.target} has no structure task")
        require(f"structure_map {spec.structure_id} 2" in chapter, f"{spec.target} has no locator handoff")
        require(spec.structure_id in registered, f"{spec.target} is absent from common structure set")

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

    require(len(registered) == len(SPECS), "common structure set contains stale or duplicate entries")
    print("Old World static validation passed: 64 targets, 13-quest spine, four deterministic common sites.")

if __name__ == "__main__": main()
