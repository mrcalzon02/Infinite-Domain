#!/usr/bin/env python3
"""Static contract validation for Old World narrative automation."""

from __future__ import annotations

import gzip
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROGRAM = ROOT / "old_world_narrative"
REGISTRY = PROGRAM / "registry"
DATA = ROOT / "kubejs" / "data" / "infinite_domain"
NAME = "ows_009_atlas_roadside_repair_depot"
STRUCTURE_ID = f"infinite_domain:old_world/{NAME}"
PROOF = "kubejs:atlas_service_plate"
MANUAL = "kubejs:atlas_transfer_maintenance_manual"


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def deterministic_items(table: dict[str, object]) -> set[str]:
    result: set[str] = set()
    for pool in table.get("pools", []):
        if pool.get("rolls") != 1:
            continue
        entries = pool.get("entries", [])
        if len(entries) == 1 and entries[0].get("type") == "minecraft:item":
            result.add(entries[0].get("name"))
    return result


def main() -> None:
    source_manifest = read_json(PROGRAM / "source" / "source-manifest.json")
    require(
        source_manifest["canon_docx_sha256"] == "eec4d3149e5e5823b330d5b01127b8f6e592d1938ef4e491f719617e507bf182",
        "canonical narrative checksum is not pinned",
    )

    structures = read_json(REGISTRY / "structure_targets.json")
    targets = structures["targets"]
    require(len(targets) == 64, "structure registry must contain exactly 64 targets")
    require([row["id"] for row in targets] == [f"OWS-{index:03d}" for index in range(1, 65)], "unstable OWS ID sequence")
    ows009 = targets[8]
    require(ows009["narrative_structure"] == STRUCTURE_ID, "OWS-009 registry mapping is stale")
    require(len(ows009["acceptance_dimensions"]) >= 4, "OWS-009 does not meet the four-dimension acceptance floor")

    lore = read_json(REGISTRY / "lore_seed.json")
    require(lore["seed_count"] == 36 and lore["minimum_completion_count"] == 96, "lore corpus requirements are stale")
    quest_spine = read_json(REGISTRY / "quest_spine.json")
    require(quest_spine["major_quest_count"] == 13, "major Exploration quest spine must contain 13 quests")
    require(quest_spine["quests"][0]["title"] == "THEY WERE HERE FIRST", "opening quest is not canonical")

    startup = (ROOT / "kubejs" / "startup_scripts" / "old_world_narrative_items.js").read_text(encoding="utf-8")
    require("event.create('atlas_service_plate')" in startup, "proof item is not registered")
    require("event.create('atlas_transfer_maintenance_manual')" in startup, "LOR-006 record is not registered")

    chapter = (ROOT / "config" / "ftbquests" / "quests" / "chapters" / "old_world_investigation.snbt").read_text(encoding="utf-8")
    require(f'structure: "{STRUCTURE_ID}"' in chapter, "quest does not target the registered structure")
    require(f"structure_map {STRUCTURE_ID} 2" in chapter, "quest locator reward is missing or stale")
    require('id: "kubejs:atlas_service_plate"' in chapter and "consume_items: true" in chapter, "proof submission task is missing")
    require('id: "kubejs:atlas_transfer_maintenance_manual"' in chapter, "maintenance record task is missing")

    pool = read_json(DATA / "worldgen" / "template_pool" / "old_world" / f"{NAME}.json")
    structure = read_json(DATA / "worldgen" / "structure" / "old_world" / f"{NAME}.json")
    structure_set = read_json(DATA / "worldgen" / "structure_set" / "old_world" / "common_sites.json")
    require(structure["start_pool"] == f"infinite_domain:old_world/{NAME}", "worldgen start pool is stale")
    require(structure["biomes"] != "#infinite_domain:disabled_primitive_wasteland_settlements", "OWS-009 remains quarantined")
    require(pool["elements"][0]["element"]["location"] == f"infinite_domain:wasteland/old_world/{NAME}", "template location is stale")
    require(structure_set["structures"] == [{"structure": STRUCTURE_ID, "weight": 1}], "structure set does not contain exactly OWS-009")

    loot = read_json(DATA / "loot_table" / "chests" / "old_world" / f"{NAME}.json")
    guaranteed = deterministic_items(loot)
    require({PROOF, MANUAL}.issubset(guaranteed), "mandatory proof or lore record is not deterministic")

    nbt_path = DATA / "structure" / "wasteland" / "old_world" / f"{NAME}.nbt"
    raw = gzip.decompress(nbt_path.read_bytes())
    require(b"infinite_domain:chests/old_world/ows_009_atlas_roadside_repair_depot" in raw, "structure NBT lacks the proof chest")
    for block in (b"minecraft:orange_concrete", b"create:mechanical_press", b"create:depot", b"create:andesite_casing"):
        require(block in raw, f"structure NBT lacks required identity/machinery block {block.decode()}")

    render_manifest = read_json(PROGRAM / "reviews" / "render-manifest.json")
    rendered = {entry["structure_id"]: entry for entry in render_manifest["structures"]}
    require(STRUCTURE_ID in rendered, "OWS-009 has no static review render")
    require(len(rendered[STRUCTURE_ID]["renders"]) == 4, "OWS-009 static review set must contain four views")
    require(rendered[STRUCTURE_ID]["visual_approval"] is False, "static rendering must not claim runtime visual approval")

    print("Old World static validation passed: 64 targets, 13 quests, deterministic OWS-009 proof slice.")


if __name__ == "__main__":
    main()
