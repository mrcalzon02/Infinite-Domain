from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import generate_wasteland_sites as g


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs" / "habitation-family-validation.json"
PAIRS = {
    "split_level_house": (g.split_level_house_clean_master, g.split_level_house),
    "abandoned_culdesac": (g.abandoned_culdesac_clean_master, g.culdesac),
    "emergency_relief_shelter": (g.emergency_relief_shelter_clean_master, g.emergency_relief_shelter),
    "tenement_courtyard": (g.tenement_courtyard_clean_master, g.tenement_courtyard),
    "ruined_rowhouse_block": (g.ruined_rowhouse_block_clean_master, g.ruined_rowhouse_block),
    "shattered_luxury_condo": (g.shattered_luxury_condo_clean_master, g.shattered_luxury_condo),
    "ruined_city_school": (g.ruined_city_school_clean_master, g.ruined_city_school),
    "ruined_community_center": (g.ruined_community_center_clean_master, g.ruined_community_center),
    "decayed_ranch": (g.decayed_ranch_clean_master, g.decayed_ranch),
    "roadside_church_cemetery": (g.roadside_church_cemetery_clean_master, g.roadside_church_cemetery),
    "ruined_ranger_station": (g.ruined_ranger_station_clean_master, g.ruined_ranger_station),
    "wasteland_fire_lookout": (g.wasteland_fire_lookout_clean_master, g.wasteland_fire_lookout),
}
IDENTITY = {
    "split_level_house": {"minecraft:blast_furnace", "minecraft:smoker", "minecraft:brown_bed"},
    "abandoned_culdesac": {"minecraft:smoker", "the_wasteland_reworked:radio", "minecraft:gray_bed"},
    "emergency_relief_shelter": {"minecraft:white_bed", "minecraft:brewing_stand", "minecraft:scaffolding"},
    "tenement_courtyard": {"minecraft:cauldron", "minecraft:gray_bed", "minecraft:smoker"},
    "ruined_rowhouse_block": {"minecraft:oak_stairs", "minecraft:brown_bed", "minecraft:water_cauldron"},
    "shattered_luxury_condo": {"minecraft:water", "minecraft:white_bed", "minecraft:smooth_quartz"},
    "ruined_city_school": {"minecraft:bookshelf", "minecraft:orange_terracotta", "zvhouses:stone_brick_countertop"},
    "ruined_community_center": {"minecraft:bookshelf", "minecraft:crafting_table", "minecraft:green_wool"},
    "decayed_ranch": {"farmersdelight:straw_bale", "minecraft:coarse_dirt", "minecraft:stripped_dark_oak_log"},
    "roadside_church_cemetery": {"minecraft:lectern", "minecraft:gold_block", "minecraft:chiseled_stone_bricks"},
    "ruined_ranger_station": {"the_wasteland_reworked:radio", "minecraft:bookshelf", "minecraft:blast_furnace"},
    "wasteland_fire_lookout": {"the_wasteland_reworked:radio", "minecraft:green_bed", "minecraft:stripped_dark_oak_log"},
}


def counts(t: g.Template) -> Counter[str]:
    return Counter(t.palette[state]["Name"] for state, _ in t.blocks.values())


def semantic(t: g.Template, pos: tuple[int, int, int]) -> str | None:
    placed = t.blocks.get(pos)
    if not placed:
        return None
    name = t.palette[placed[0]]["Name"]
    return None if name == "minecraft:air" else name


def main() -> None:
    failures: list[str] = []
    records: dict[str, object] = {}
    signatures: dict[tuple[tuple[int, int, int], tuple[tuple[str, int], ...]], str] = {}
    for name, (master_fn, derivative_fn) in PAIRS.items():
        master, derivative = master_fn(), derivative_fn()
        g.stabilize_door_pairs(master)
        g.stabilize_door_pairs(derivative)
        master_counts, derivative_counts = counts(master), counts(derivative)
        changed = sum(semantic(master, pos) != semantic(derivative, pos) for pos in set(master.blocks) | set(derivative.blocks))
        forbidden = sorted(set(master_counts | derivative_counts) & set(g.STRUCTURE_BLOCK_REPLACEMENTS))
        missing = sorted(IDENTITY[name] - set(master_counts))
        lint = g.assess_fidelity(name, derivative)
        issues: list[str] = []
        if master.size != derivative.size:
            issues.append("master and derivative dimensions differ")
        if changed < 24:
            issues.append(f"derivative changes only {changed} semantic cells")
        if changed > max(50, int(sum(master_counts.values()) * 0.62)):
            issues.append(f"damage changes {changed} semantic cells, exceeding family localization limit")
        if forbidden:
            issues.append(f"forbidden connection-sensitive blocks: {forbidden}")
        if missing:
            issues.append(f"missing purpose fixtures: {missing}")
        if derivative_counts["minecraft:spawner"] < 1:
            issues.append("occupied derivative has no hostile spawner")
        if not lint["structural_lint_passed"]:
            issues.extend(lint["issues"])
        signature = (master.size, tuple(sorted(master_counts.items())))
        if signature in signatures:
            issues.append(f"duplicates {signatures[signature]} by dimensions and complete block inventory")
        signatures[signature] = name
        records[name] = {
            "size": list(master.size),
            "master_blocks": len(master.blocks),
            "changed_semantic_cells": changed,
            "spawners": derivative_counts["minecraft:spawner"],
            "entities_in_clean_master": len(master.entities),
            "structural_lint": lint,
            "passed": not issues,
            "issues": issues,
        }
        failures.extend(f"{name}: {issue}" for issue in issues)
    report = {"family": "habitation_and_community", "asset_pairs": len(PAIRS), "all_passed": not failures, "failures": failures, "structures": records}
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if failures:
        raise SystemExit("Habitation family validation failed:\n- " + "\n- ".join(failures))
    print(f"Validated {len(PAIRS)} habitation/community clean-master/derivative pairs")


if __name__ == "__main__":
    main()
