from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import generate_wasteland_sites as g

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs" / "extraction-family-validation.json"
PAIRS = {
    "abandoned_quarry": (g.abandoned_quarry_clean_master, g.abandoned_quarry),
    "collapsed_mine_entrance": (g.collapsed_mine_entrance_clean_master, g.collapsed_mine_entrance),
    "excavator_pit": (g.excavator_pit_clean_master, g.excavator_pit),
    "abandoned_oil_field": (g.abandoned_oil_field_clean_master, g.abandoned_oil_field),
}
IDENTITY = {
    "abandoned_quarry": {"minecraft:tuff", "minecraft:rail", "create:mechanical_drill"},
    "collapsed_mine_entrance": {"minecraft:rail", "minecraft:stripped_dark_oak_log", "minecraft:lantern"},
    "excavator_pit": {"minecraft:yellow_concrete", "minecraft:black_concrete", "create:framed_glass"},
    "abandoned_oil_field": {"immersiveengineering:sheetmetal_steel", "minecraft:yellow_concrete", "minecraft:black_concrete"},
}
SURFACE_LEVEL = {"abandoned_quarry": 12, "collapsed_mine_entrance": 8, "excavator_pit": 10}


def counts(t):
    return Counter(t.palette[state]["Name"] for state, _ in t.blocks.values())


def semantic(t, pos):
    placed = t.blocks.get(pos)
    if not placed:
        return None
    name = t.palette[placed[0]]["Name"]
    return None if name == "minecraft:air" else name


def below_surface_air(t, surface):
    return sum(
        1
        for (_, y, _), (state, _) in t.blocks.items()
        if y < surface and t.palette[state]["Name"] == "minecraft:air"
    )


def main() -> None:
    failures, records, signatures = [], {}, {}
    for name, (master_fn, derivative_fn) in PAIRS.items():
        master, derivative = master_fn(), derivative_fn()
        g.stabilize_door_pairs(master)
        g.stabilize_door_pairs(derivative)
        mc, dc = counts(master), counts(derivative)
        changed = sum(
            semantic(master, pos) != semantic(derivative, pos)
            for pos in set(master.blocks) | set(derivative.blocks)
        )
        lint = g.assess_fidelity(name, derivative)
        issues = []
        forbidden = sorted(set(mc | dc) & set(g.STRUCTURE_BLOCK_REPLACEMENTS))
        missing = sorted(IDENTITY[name] - set(mc))
        cut_air = below_surface_air(master, SURFACE_LEVEL[name]) if name in SURFACE_LEVEL else 0
        if master.size != derivative.size:
            issues.append("master/derivative dimensions differ")
        if changed < 40 or changed > int(sum(mc.values()) * .72):
            issues.append(f"damage-cell count {changed} outside localization range")
        if forbidden:
            issues.append(f"forbidden blocks: {forbidden}")
        if missing:
            issues.append(f"missing identity fixtures: {missing}")
        if dc["minecraft:spawner"] < 1:
            issues.append("derivative has no hostile spawner")
        if name in SURFACE_LEVEL and cut_air < 500:
            issues.append(f"terrain cut has only {cut_air} explicit below-surface air cells")
        if not lint["structural_lint_passed"]:
            issues.extend(lint["issues"])
        signature = (master.size, tuple(sorted(mc.items())))
        if signature in signatures:
            issues.append(f"duplicates {signatures[signature]}")
        signatures[signature] = name
        records[name] = {
            "size": list(master.size),
            "master_blocks": len(master.blocks),
            "changed_semantic_cells": changed,
            "below_surface_air_cells": cut_air,
            "spawners": dc["minecraft:spawner"],
            "structural_lint": lint,
            "passed": not issues,
            "issues": issues,
        }
        failures.extend(f"{name}: {issue}" for issue in issues)
    report = {
        "family": "extraction_sites",
        "asset_pairs": len(PAIRS),
        "all_passed": not failures,
        "failures": failures,
        "structures": records,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if failures:
        raise SystemExit("Extraction family validation failed:\n- " + "\n- ".join(failures))
    print("Validated 4 extraction clean-master/derivative pairs")


if __name__ == "__main__":
    main()
