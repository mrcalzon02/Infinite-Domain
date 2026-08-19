from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import generate_wasteland_sites as g

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs" / "utility-technology-family-validation.json"
REGISTRY = set((ROOT / "docs" / "registry-inventory" / "block-ids.txt").read_text(encoding="utf-8").splitlines())
NAMES = (
    "industrial_facility", "city_electrical_substation", "city_water_treatment_plant",
    "district_heating_station", "municipal_incinerator", "ruined_fuel_depot",
    "ruined_cyberware_clinic", "ae2_records_archive", "nuclear_research_annex",
    "shattered_wind_farm", "broken_solar_field", "wilderness_substation",
    "wasteland_water_tower",
)
PAIRS = {name: (getattr(g, f"{name}_clean_master"), getattr(g, name)) for name in NAMES}
IDENTITY = {
    "industrial_facility": {"create:mechanical_mixer", "create:mechanical_press", "create:fluid_tank"},
    "city_electrical_substation": {"minecraft:oxidized_copper", "immersiveengineering:capacitor_hv", "immersiveengineering:coil_hv"},
    "city_water_treatment_plant": {"immersiveengineering:concrete_reinforced", "minecraft:water", "create:mechanical_pump"},
    "district_heating_station": {"minecraft:blast_furnace", "create:fluid_tank", "create:mechanical_pump"},
    "municipal_incinerator": {"minecraft:blast_furnace", "create:fluid_tank", "create:mechanical_press"},
    "ruined_fuel_depot": {"immersiveengineering:sheetmetal_steel", "create:mechanical_pump", "minecraft:bricks"},
    "ruined_cyberware_clinic": {"minecraft:white_bed", "minecraft:brewing_stand", "ae2:drive"},
    "ae2_records_archive": {"ae2:controller", "ae2:drive", "minecraft:barrel"},
    "nuclear_research_annex": {"createnuclear:reactor_core", "createnuclear:reactor_controller", "createnuclear:reinforced_glass"},
    "shattered_wind_farm": {"minecraft:white_concrete", "minecraft:light_gray_concrete", "immersiveengineering:capacitor_mv"},
    "broken_solar_field": {"oritech:big_solar_panel_block", "minecraft:black_stained_glass", "immersiveengineering:capacitor_hv"},
    "wilderness_substation": {"minecraft:oxidized_copper", "immersiveengineering:coil_hv", "minecraft:polished_blackstone"},
    "wasteland_water_tower": {"minecraft:light_blue_concrete", "minecraft:oxidized_copper", "create:mechanical_pump"},
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
        g.stabilize_door_pairs(master); g.stabilize_door_pairs(derivative)
        mc, dc = counts(master), counts(derivative)
        changed = sum(semantic(master, p) != semantic(derivative, p) for p in set(master.blocks) | set(derivative.blocks))
        lint = g.assess_fidelity(name, derivative)
        issues = []
        forbidden = sorted(set(mc | dc) & set(g.STRUCTURE_BLOCK_REPLACEMENTS))
        unknown = sorted((set(mc) | set(dc)) - REGISTRY - {"minecraft:air"})
        missing = sorted(IDENTITY[name] - set(mc))
        if master.size != derivative.size: issues.append("master/derivative dimensions differ")
        if changed < 40 or changed > int(sum(mc.values()) * .72): issues.append(f"damage-cell count {changed} outside localization range")
        if forbidden: issues.append(f"forbidden blocks: {forbidden}")
        if unknown: issues.append(f"unregistered blocks: {unknown}")
        if missing: issues.append(f"missing identity fixtures: {missing}")
        if dc["minecraft:spawner"] < 1: issues.append("derivative has no hostile spawner")
        if not lint["structural_lint_passed"]: issues.extend(lint["issues"])
        signature = (master.size, tuple(sorted(mc.items())))
        if signature in signatures: issues.append(f"duplicates {signatures[signature]}")
        signatures[signature] = name
        records[name] = {"size": list(master.size), "master_blocks": len(master.blocks), "changed_semantic_cells": changed, "spawners": dc["minecraft:spawner"], "structural_lint": lint, "passed": not issues, "issues": issues}
        failures.extend(f"{name}: {issue}" for issue in issues)
    REPORT.write_text(json.dumps({"family": "industrial_utility_technology", "asset_pairs": len(PAIRS), "all_passed": not failures, "failures": failures, "structures": records}, indent=2) + "\n", encoding="utf-8")
    if failures: raise SystemExit("Utility/technology validation failed:\n- " + "\n- ".join(failures))
    print("Validated 13 industrial/utility/technology clean-master/derivative pairs")


if __name__ == "__main__":
    main()
