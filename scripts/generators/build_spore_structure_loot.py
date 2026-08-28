"""Replace Spore structure chests with restrained Era 1–3 survival loot."""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "kubejs/data/spore/loot_table/chests"
REPORT = ROOT / "docs/spore-structure-loot"
REGISTRY = ROOT / "docs/registry-inventory/item-ids.txt"


def entry(name: str, weight: int, minimum: int = 1, maximum: int = 1) -> dict:
    value = {"type": "minecraft:item", "name": name, "weight": weight}
    if minimum != 1 or maximum != 1:
        value["functions"] = [{
            "function": "minecraft:set_count",
            "count": {"type": "minecraft:uniform", "min": minimum, "max": maximum},
        }]
    return value


def empty(weight: int) -> dict:
    return {"type": "minecraft:empty", "weight": weight}


def pool(minimum: int, maximum: int, entries: list[dict]) -> dict:
    rolls: int | dict = minimum if minimum == maximum else {
        "type": "minecraft:uniform", "min": minimum, "max": maximum,
    }
    return {"rolls": rolls, "entries": entries}


TABLES = {
    "document_chest": [
        pool(2, 4, [
            entry("minecraft:paper", 24, 2, 8), entry("minecraft:book", 12),
            entry("minecraft:writable_book", 5), entry("spore:documents", 12, 1, 2),
            entry("spore:circuit_board", 3), entry("enviromine:pda", 1), empty(18),
        ]),
    ],
    "equipment_chest": [
        pool(2, 3, [
            entry("the_wasteland_reworked:bandage", 20, 1, 3),
            entry("minecraft:arrow", 14, 4, 12), entry("minecraft:shield", 4),
            entry("minecraft:iron_helmet", 3), entry("minecraft:iron_chestplate", 2),
            entry("minecraft:iron_leggings", 2), entry("minecraft:iron_boots", 3),
            entry("enviromine:gas_mask_basic_helmet", 6), entry("enviromine:hard_hat_helmet", 5),
            entry("enviromine:air_filter", 12, 1, 2), entry("spore:gas_mask", 5), empty(24),
        ]),
        pool(1, 2, [
            entry("enviromine:vent_pipe", 10, 2, 6), entry("enviromine:vent_pipe_h", 10, 2, 6),
            entry("enviromine:vent_pipe_o", 7, 1, 4), entry("enviromine:vent_intake", 5),
            entry("enviromine:vent", 3), entry("spore:compound_plate", 7, 1, 3),
            entry("spore:circuit_board", 5), entry("spore:syringe", 8, 1, 2),
            entry("spore:scanner", 1), empty(28),
        ]),
    ],
    "food_chest": [
        pool(3, 5, [
            entry("wastelands:canned_food", 16, 1, 3),
            entry("the_wasteland_reworked:canned_food", 14, 1, 3),
            entry("wastelands:purified_water", 24, 1, 3),
            entry("minecraft:bread", 12, 1, 3),
            entry("minecraft:cooked_beef", 7, 1, 3), entry("minecraft:cooked_chicken", 7, 1, 3),
            entry("minecraft:milk_bucket", 3), entry("the_wasteland_reworked:bandage", 8, 1, 2),
            empty(16),
        ]),
    ],
    "ice_chest": [
        pool(2, 4, [
            entry("minecraft:ice", 24, 2, 8), entry("minecraft:packed_ice", 15, 1, 5),
            entry("minecraft:blue_ice", 4, 1, 2), entry("minecraft:snow_block", 14, 2, 8),
            entry("spore:ice_canister", 5, 1, 2), entry("enviromine:air_filter", 5), empty(18),
        ]),
    ],
    "organ_chest": [
        pool(3, 5, [
            entry("spore:mutated_heart", 12, 1, 2), entry("spore:innards", 14, 1, 3),
            entry("spore:alveolic_sack", 9, 1, 2), entry("spore:armor_fragment", 14, 1, 4),
            entry("spore:mutated_fiber", 16, 1, 4), entry("spore:cerebrum", 4),
            entry("spore:tendons", 12, 1, 3), entry("spore:altered_spleen", 3),
            entry("spore:tumor", 16, 1, 3), empty(20),
        ]),
    ],
}


def main() -> None:
    registered = set(REGISTRY.read_text(encoding="utf-8-sig").splitlines())
    bad: list[str] = []
    rows: list[tuple[str, str, int, int, int]] = []
    for table, pools in TABLES.items():
        for pindex, loot_pool in enumerate(pools, 1):
            for item in loot_pool["entries"]:
                if item["type"] == "minecraft:empty":
                    continue
                name = item["name"]
                if name not in registered:
                    bad.append(f"{table}: {name}")
                count = item.get("functions", [{}])[0].get("count", {})
                rows.append((table, name, item["weight"], count.get("min", 1), count.get("max", 1)))
    if bad:
        raise SystemExit("Unknown loot item IDs:\n" + "\n".join(bad))

    OUT.mkdir(parents=True, exist_ok=True)
    for name, pools in TABLES.items():
        data = {"type": "minecraft:chest", "pools": pools, "random_sequence": f"spore:chests/{name}"}
        (OUT / f"{name}.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    REPORT.mkdir(parents=True, exist_ok=True)
    with (REPORT / "effective-spore-chest-loot.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["loot_table", "item", "weight", "min_count", "max_count"])
        writer.writerows(rows)
    print(f"Wrote {len(TABLES)} Spore chest overrides containing {len(rows)} weighted item entries.")


if __name__ == "__main__":
    main()
