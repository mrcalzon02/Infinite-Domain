from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import generate_wasteland_sites as g

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs" / "rural-processing-family-validation.json"
PAIRS = {
    "abandoned_orchard_cannery": (g.abandoned_orchard_cannery_clean_master, g.abandoned_orchard_cannery),
    "ruined_grain_elevator": (g.ruined_grain_elevator_clean_master, g.ruined_grain_elevator),
    "shattered_greenhouse_nursery": (g.shattered_greenhouse_nursery_clean_master, g.shattered_greenhouse_nursery),
    "remote_sawmill": (g.remote_sawmill_clean_master, g.remote_sawmill),
}
IDENTITY = {
    "abandoned_orchard_cannery": {"quark:apple_crate", "minecraft:water_cauldron", "create:mechanical_press"},
    "ruined_grain_elevator": {"minecraft:rail", "minecraft:light_gray_concrete", "create:mechanical_press"},
    "shattered_greenhouse_nursery": {"create:framed_glass", "minecraft:farmland", "minecraft:composter"},
    "remote_sawmill": {"create:mechanical_saw", "minecraft:spruce_log", "minecraft:scaffolding"},
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
            "spawners": dc["minecraft:spawner"],
            "structural_lint": lint,
            "passed": not issues,
            "issues": issues,
        }
        failures.extend(f"{name}: {issue}" for issue in issues)
    report = {
        "family": "rural_processing",
        "asset_pairs": len(PAIRS),
        "all_passed": not failures,
        "failures": failures,
        "structures": records,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if failures:
        raise SystemExit("Rural processing validation failed:\n- " + "\n- ".join(failures))
    print("Validated 4 rural-processing clean-master/derivative pairs")


if __name__ == "__main__":
    main()
