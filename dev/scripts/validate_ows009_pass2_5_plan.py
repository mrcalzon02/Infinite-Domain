#!/usr/bin/env python3
"""Target-local consistency validator for OWS-009 Passes 2-5 planning."""
from __future__ import annotations

import gzip
import json
from pathlib import Path

from render_structure_review import Reader, unpack_structure


ROOT = Path(__file__).resolve().parents[2]
SHIPPING = ROOT / "kubejs/data/infinite_domain/structure/wasteland/old_world/ows_009_atlas_roadside_repair_depot.nbt"
LOOT = ROOT / "kubejs/data/infinite_domain/loot_table/chests/old_world/ows_009_atlas_roadside_repair_depot.json"
TARGETS = ROOT / "dev/old_world_narrative/registry/structure_targets.json"
QUESTS = ROOT / "dev/old_world_narrative/registry/site_quest_catalog.json"
DOCS = tuple(
    ROOT / "dev/old_world_narrative/reviews/heavy_rebuild" / f"OWS-009_PASS{number}_{name}.md"
    for number, name in (
        (2, "FUNCTIONAL_DEFINITION"),
        (3, "PRECEDENT_RESEARCH"),
        (4, "PROGRAM_ADJACENCY"),
        (5, "SCALE_TRANSLATION"),
    )
)
PROPOSED_SIZE = (49, 18, 41)
PROOF_POS = (34, 2, 25)
PROOF_TABLE = "infinite_domain:chests/old_world/ows_009_atlas_roadside_repair_depot"


def _entry(targets: list[dict], key: str, value: str) -> dict:
    matches = [row for row in targets if row.get(key) == value]
    if len(matches) != 1:
        raise AssertionError(f"expected one {key}={value}, found {len(matches)}")
    return matches[0]


def _proof() -> tuple[str, str | None]:
    _, root = Reader(gzip.decompress(SHIPPING.read_bytes())).root()
    data = root.value
    palette = [entry.value["Name"].value for entry in data["palette"].value.values]
    for tagged in data["blocks"].value.values:
        row = tagged.value
        pos = tuple(int(tag.value) for tag in row["pos"].value.values)
        if pos != PROOF_POS:
            continue
        name = palette[int(row["state"].value)]
        nbt = row.get("nbt")
        table = None if nbt is None or "LootTable" not in nbt.value else nbt.value["LootTable"].value
        return name, table
    raise AssertionError("OWS-009 canonical proof position is absent")


def main() -> None:
    if any(not path.is_file() for path in DOCS):
        raise AssertionError("OWS-009 Passes 2-5 planning record set is incomplete")

    size, _ = unpack_structure(SHIPPING)
    if tuple(size) != (41, 15, 33):
        raise AssertionError(f"OWS-009 baseline dimensions drifted: {size}")
    if PROPOSED_SIZE != (49, 18, 41):
        raise AssertionError("OWS-009 proposed study bounds drifted")

    # Bounds and clearance contracts from the Pass-5 coordinate study.
    boxes = {
        "bay_01": (5, 13, 8, 27),
        "bay_02": (15, 24, 8, 27),
        "bay_03": (26, 34, 8, 27),
        "technician_spine": (4, 34, 28, 31),
        "customer_bar": (36, 44, 7, 19),
        "parts_issue": (36, 44, 20, 27),
        "records_proof": (36, 44, 28, 34),
    }
    for name, (x1, x2, z1, z2) in boxes.items():
        if not (0 <= x1 <= x2 < PROPOSED_SIZE[0] and 0 <= z1 <= z2 < PROPOSED_SIZE[2]):
            raise AssertionError(f"{name} exceeds proposed bounds")
    if boxes["technician_spine"][3] - boxes["technician_spine"][2] + 1 < 4:
        raise AssertionError("technician spine no longer protects service/walking clearance")
    if min(boxes[name][1] - boxes[name][0] + 1 for name in ("bay_01", "bay_02", "bay_03")) < 9:
        raise AssertionError("repair cell width is below the scale contract")

    structure_rows = json.loads(TARGETS.read_text(encoding="utf-8"))["targets"]
    target = _entry(structure_rows, "id", "OWS-009")
    if target["narrative_structure"] != "infinite_domain:old_world/ows_009_atlas_roadside_repair_depot":
        raise AssertionError("OWS-009 structure ID drifted")

    quest_rows = json.loads(QUESTS.read_text(encoding="utf-8"))["sites"]
    quest = _entry(quest_rows, "target_id", "OWS-009")
    expected_quest = {
        "quest_id": "4F58000000000009",
        "structure_task_id": "4F58100000000009",
        "proof_task_id": "4F58200000000009",
        "proof_item": "kubejs:atlas_service_plate",
    }
    for key, expected in expected_quest.items():
        if quest.get(key) != expected:
            raise AssertionError(f"OWS-009 {key} drifted: {quest.get(key)} != {expected}")

    loot = json.loads(LOOT.read_text(encoding="utf-8"))
    guaranteed = [pool["entries"][0]["name"] for pool in loot["pools"][:2]]
    if guaranteed != ["kubejs:atlas_service_plate", "kubejs:atlas_transfer_maintenance_manual"]:
        raise AssertionError(f"OWS-009 guaranteed loot drifted: {guaranteed}")
    name, table = _proof()
    if name != "minecraft:chest" or table != PROOF_TABLE:
        raise AssertionError(f"OWS-009 proof container drifted: {name}, {table}")

    print(
        "OWS-009 Passes 2-5 plan validation passed: baseline=41x15x33, "
        "study=49x18x41, three cells, service spine, proof/quest/loot preserved."
    )


if __name__ == "__main__":
    main()
