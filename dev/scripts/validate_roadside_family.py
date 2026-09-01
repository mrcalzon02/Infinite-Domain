from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import generate_wasteland_sites as g


ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "dev/docs" / "roadside-family-validation.json"


PAIRS = {
    "radio_mast": (g.radio_mast_clean_master, g.radio_mast),
    "wrecked_sedan": (g.wrecked_sedan_clean_master, g.wrecked_sedan),
    "delivery_van": (g.delivery_van_clean_master, g.delivery_van),
    "battle_tank": (g.battle_tank_clean_master, g.battle_tank),
    "service_garage": (g.service_garage_clean_master, g.service_garage),
    "scrapyard": (g.scrapyard_clean_master, g.scrapyard),
    "military_checkpoint": (g.military_checkpoint_clean_master, g.checkpoint),
    "ruined_roadside_diner": (g.ruined_roadside_diner_clean_master, g.ruined_roadside_diner),
    "abandoned_truck_stop": (g.abandoned_truck_stop_clean_master, g.abandoned_truck_stop),
    "wasteland_weigh_station": (g.wasteland_weigh_station_clean_master, g.wasteland_weigh_station),
    "destroyed_refugee_convoy": (g.destroyed_refugee_convoy_clean_master, g.destroyed_refugee_convoy),
}


IDENTITY_TERMS = {
    "radio_mast": {"the_wasteland_reworked:radio", "create:red_nixie_tube", "minecraft:lightning_rod"},
    "wrecked_sedan": {"minecraft:blackstone", "minecraft:light_blue_stained_glass"},
    "delivery_van": {"the_wasteland_reworked:cardboard_box", "minecraft:iron_door"},
    "battle_tank": {"minecraft:blackstone", "minecraft:green_terracotta", "minecraft:blast_furnace"},
    "service_garage": {"minecraft:anvil", "immersiveengineering:metal_barrel", "minecraft:scaffolding"},
    "scrapyard": {"wastelands:scrap_pile", "create:mechanical_press", "minecraft:oxidized_copper_grate"},
    "military_checkpoint": {"the_wasteland_reworked:barricade", "the_wasteland_reworked:radio", "minecraft:iron_door"},
    "ruined_roadside_diner": {"farmersdelight:stove", "zvhouses:spruce_countertop", "minecraft:smoker"},
    "abandoned_truck_stop": {"minecraft:scaffolding", "minecraft:water_cauldron", "immersiveengineering:sheetmetal_steel"},
    "wasteland_weigh_station": {"minecraft:polished_blackstone", "minecraft:brewing_stand", "the_wasteland_reworked:radio"},
    "destroyed_refugee_convoy": {"minecraft:green_wool", "minecraft:white_bed", "the_wasteland_reworked:cardboard_box"},
}


def names(template: g.Template) -> Counter[str]:
    return Counter(template.palette[state]["Name"] for state, _ in template.blocks.values())


def semantic_cell(template: g.Template, pos: tuple[int, int, int]) -> str | None:
    placed = template.blocks.get(pos)
    if not placed:
        return None
    name = template.palette[placed[0]]["Name"]
    return None if name == "minecraft:air" else name


def main() -> None:
    records: dict[str, object] = {}
    failures: list[str] = []
    signatures: dict[tuple[tuple[int, int, int], tuple[tuple[str, int], ...]], str] = {}
    for name, (master_builder, derivative_builder) in PAIRS.items():
        master = master_builder()
        derivative = derivative_builder()
        master_names = names(master)
        derivative_names = names(derivative)
        forbidden = sorted(set(master_names | derivative_names) & set(g.STRUCTURE_BLOCK_REPLACEMENTS))
        missing_identity = sorted(IDENTITY_TERMS[name] - set(master_names))
        changed_cells = sum(
            1
            for pos in set(master.blocks) | set(derivative.blocks)
            if semantic_cell(master, pos) != semantic_cell(derivative, pos)
        )
        derivative_spawners = derivative_names["minecraft:spawner"]
        lint = g.assess_fidelity(name, derivative)
        issues: list[str] = []
        if master.size != derivative.size:
            issues.append("master and derivative dimensions differ")
        if changed_cells < 8:
            issues.append(f"damage derivative changes only {changed_cells} cells")
        if changed_cells > max(20, int(len(master.blocks) * 0.55)):
            issues.append(f"damage derivative changes {changed_cells} cells, exceeding localized-damage limit")
        if forbidden:
            issues.append(f"forbidden connection-sensitive blocks: {forbidden}")
        if missing_identity:
            issues.append(f"missing identity fixtures: {missing_identity}")
        if not lint["structural_lint_passed"]:
            issues.extend(lint["issues"])
        if name not in {"wrecked_sedan"} and derivative_spawners < 1:
            issues.append("occupied/danger derivative has no hostile spawner")

        signature = (master.size, tuple(sorted(master_names.items())))
        if signature in signatures:
            issues.append(f"master duplicates {signatures[signature]} by size and complete block inventory")
        signatures[signature] = name
        records[name] = {
            "size": list(master.size),
            "master_blocks": len(master.blocks),
            "derivative_blocks": len(derivative.blocks),
            "changed_cells": changed_cells,
            "derivative_spawners": derivative_spawners,
            "identity_fixtures_present": sorted(IDENTITY_TERMS[name]),
            "structural_lint": lint,
            "passed": not issues,
            "issues": issues,
        }
        failures.extend(f"{name}: {issue}" for issue in issues)

    report = {
        "family": "roadside_mobility_security",
        "asset_pairs": len(PAIRS),
        "all_passed": not failures,
        "failures": failures,
        "structures": records,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if failures:
        raise SystemExit("Roadside family validation failed:\n- " + "\n- ".join(failures))
    print(f"Validated {len(PAIRS)} roadside clean-master/derivative pairs")


if __name__ == "__main__":
    main()
