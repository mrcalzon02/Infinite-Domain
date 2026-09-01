from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import generate_wasteland_sites as g


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs" / "urban-commercial-family-validation.json"
PAIRS = {
    "ruined_shopping_mall": (g.ruined_shopping_mall_clean_master, g.ruined_shopping_mall),
    "ruined_department_store": (g.ruined_department_store_clean_master, g.ruined_department_store),
    "bombed_hotel": (g.bombed_hotel_clean_master, g.bombed_hotel),
    "buried_bank_vault": (g.buried_bank_vault_clean_master, g.buried_bank_vault),
    "ruined_office_tower": (g.ruined_office_tower_clean_master, g.ruined_office_tower),
}
IDENTITY = {
    "ruined_shopping_mall": {"create:framed_glass", "minecraft:scaffolding", "minecraft:smoker"},
    "ruined_department_store": {"minecraft:loom", "minecraft:scaffolding", "zvhouses:spruce_countertop"},
    "bombed_hotel": {"minecraft:white_bed", "farmersdelight:stove", "minecraft:white_wool"},
    "buried_bank_vault": {"immersiveengineering:concrete_reinforced", "immersiveengineering:sheetmetal_steel", "minecraft:iron_door"},
    "ruined_office_tower": {"minecraft:lectern", "the_wasteland_reworked:radio", "minecraft:scaffolding"},
}


def block_counts(t: g.Template) -> Counter[str]:
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
    signatures: set[tuple[tuple[int, int, int], tuple[tuple[str, int], ...]]] = set()
    for name, (master_fn, derivative_fn) in PAIRS.items():
        master, derivative = master_fn(), derivative_fn()
        g.stabilize_door_pairs(master)
        g.stabilize_door_pairs(derivative)
        master_counts, derivative_counts = block_counts(master), block_counts(derivative)
        changed = sum(semantic(master, pos) != semantic(derivative, pos) for pos in set(master.blocks) | set(derivative.blocks))
        forbidden = sorted(set(master_counts | derivative_counts) & set(g.STRUCTURE_BLOCK_REPLACEMENTS))
        missing = sorted(IDENTITY[name] - set(master_counts))
        lint = g.assess_fidelity(name, derivative)
        issues: list[str] = []
        if master.size != derivative.size:
            issues.append("master/derivative dimensions differ")
        if changed < 50 or changed > int(sum(master_counts.values()) * 0.62):
            issues.append(f"damage semantic-cell count {changed} is outside the family localization range")
        if forbidden:
            issues.append(f"forbidden blocks: {forbidden}")
        if missing:
            issues.append(f"missing identity fixtures: {missing}")
        if derivative_counts["minecraft:spawner"] < 1:
            issues.append("derivative has no hostile spawner")
        if not lint["structural_lint_passed"]:
            issues.extend(lint["issues"])
        signature = (master.size, tuple(sorted(master_counts.items())))
        if signature in signatures:
            issues.append("duplicates another family master")
        signatures.add(signature)
        records[name] = {"size": list(master.size), "master_blocks": len(master.blocks), "changed_semantic_cells": changed, "spawners": derivative_counts["minecraft:spawner"], "structural_lint": lint, "passed": not issues, "issues": issues}
        failures.extend(f"{name}: {issue}" for issue in issues)
    report = {"family": "urban_commercial", "asset_pairs": len(PAIRS), "all_passed": not failures, "failures": failures, "structures": records}
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if failures:
        raise SystemExit("Urban-commercial family validation failed:\n- " + "\n- ".join(failures))
    print(f"Validated {len(PAIRS)} urban-commercial clean-master/derivative pairs")


if __name__ == "__main__":
    main()
