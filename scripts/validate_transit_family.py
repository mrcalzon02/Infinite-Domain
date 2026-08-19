from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import generate_wasteland_sites as g

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs" / "transit-family-validation.json"
PAIRS = {
    "collapsed_subway_station": (g.collapsed_subway_station_clean_master, g.collapsed_subway_station),
    "ruined_bus_terminal": (g.ruined_bus_terminal_clean_master, g.ruined_bus_terminal),
    "elevated_rail_collapse": (g.elevated_rail_collapse_clean_master, g.elevated_rail_collapse),
    "sunken_highway_interchange": (g.sunken_highway_interchange_clean_master, g.sunken_highway_interchange),
    "collapsed_airship_terminal": (g.collapsed_airship_terminal_clean_master, g.collapsed_airship_terminal),
    "crashed_cargo_airship": (g.crashed_cargo_airship_clean_master, g.crashed_cargo_airship),
    "warm_industrial_mountain_port": (g.warm_industrial_mountain_port_clean_master, lambda: g.industrial_mountain_port(False)),
    "cold_industrial_mountain_port": (g.cold_industrial_mountain_port_clean_master, lambda: g.industrial_mountain_port(True)),
}
IDENTITY = {
    "collapsed_subway_station": {"minecraft:rail", "create:red_nixie_tube", "immersiveengineering:concrete_reinforced"},
    "ruined_bus_terminal": {"zvhouses:spruce_countertop", "minecraft:dark_oak_stairs", "minecraft:smoker"},
    "elevated_rail_collapse": {"minecraft:rail", "immersiveengineering:concrete_reinforced", "zvhouses:stone_brick_countertop"},
    "sunken_highway_interchange": {"tfmg:asphalt", "minecraft:stone_bricks", "minecraft:yellow_concrete"},
    "collapsed_airship_terminal": {"immersiveengineering:sheetmetal_steel", "zvhouses:stone_brick_countertop", "create:framed_glass"},
    "crashed_cargo_airship": {"minecraft:oxidized_copper", "jaffabricate:pallet_full", "create:mechanical_press"},
    "warm_industrial_mountain_port": {"minecraft:stone", "minecraft:orange_concrete", "minecraft:rail"},
    "cold_industrial_mountain_port": {"minecraft:deepslate", "minecraft:light_blue_concrete", "minecraft:rail"},
}


def counts(t):
    return Counter(t.palette[state]["Name"] for state, _ in t.blocks.values())


def semantic(t, pos):
    placed = t.blocks.get(pos)
    if not placed:
        return None
    name = t.palette[placed[0]]["Name"]
    return None if name == "minecraft:air" else name


def main() -> None:
    failures, records = [], {}
    signatures = {}
    for name, (master_fn, derivative_fn) in PAIRS.items():
        master, derivative = master_fn(), derivative_fn()
        g.stabilize_door_pairs(master); g.stabilize_door_pairs(derivative)
        mc, dc = counts(master), counts(derivative)
        changed = sum(semantic(master, p) != semantic(derivative, p) for p in set(master.blocks) | set(derivative.blocks))
        lint = g.assess_fidelity(name, derivative)
        issues = []
        forbidden = sorted(set(mc | dc) & set(g.STRUCTURE_BLOCK_REPLACEMENTS))
        missing = sorted(IDENTITY[name] - set(mc))
        if master.size != derivative.size: issues.append("master/derivative dimensions differ")
        if changed < 40 or changed > int(sum(mc.values()) * .72): issues.append(f"damage-cell count {changed} outside localization range")
        if forbidden: issues.append(f"forbidden blocks: {forbidden}")
        if missing: issues.append(f"missing identity fixtures: {missing}")
        if dc["minecraft:spawner"] < 1: issues.append("derivative has no hostile spawner")
        if not lint["structural_lint_passed"]: issues.extend(lint["issues"])
        signature = (master.size, tuple(sorted(mc.items())))
        if signature in signatures and {name, signatures[signature]} != {"warm_industrial_mountain_port", "cold_industrial_mountain_port"}:
            issues.append(f"duplicates {signatures[signature]}")
        signatures[signature] = name
        records[name] = {"size": list(master.size), "master_blocks": len(master.blocks), "changed_semantic_cells": changed, "spawners": dc["minecraft:spawner"], "structural_lint": lint, "passed": not issues, "issues": issues}
        failures.extend(f"{name}: {issue}" for issue in issues)
    report = {"family": "transit_and_ports", "asset_pairs": 8, "all_passed": not failures, "failures": failures, "structures": records}
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if failures: raise SystemExit("Transit family validation failed:\n- " + "\n- ".join(failures))
    print("Validated 8 transit/ports clean-master/derivative pairs")


if __name__ == "__main__":
    main()
