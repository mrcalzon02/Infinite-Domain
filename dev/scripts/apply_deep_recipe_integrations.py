"""Install curated, non-bypassable cross-mod recipes for progression gateways.

Run this after build_compressed_crafting_overrides.ps1. Every effective recipe
ID producing a selected output is overridden, so alternate recipes cannot evade
the intended dependency. The explicit table below is the design source of truth.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
INDEX = ROOT / "dev/docs" / "recipe-index" / "recipe-index.csv"
MANIFEST = ROOT / "dev/docs" / "compression-audit" / "generated-crafting-overrides.csv"
ITEM_REGISTRY = ROOT / "dev/docs" / "registry-inventory" / "item-ids.txt"


def shaped(output: str, pattern: list[str], key: dict[str, str], count: int = 1) -> dict:
    return {
        "type": "minecraft:crafting_shaped",
        "category": "misc",
        "pattern": pattern,
        "key": {symbol: {"item": item} for symbol, item in key.items()},
        "result": {"id": output, "count": count},
    }


# The recipes deliberately use functional parts: pumps in refining, coils and
# transformers in power conversion, processors in automation, batteries in
# reactor control, and high-tier computation/power components in spacecraft.
RECIPES = {
    # Era 2 — first deliberate bridge: Create infrastructure bootstraps TFMG steel.
    "createmetallurgy:industrial_crucible": shaped("createmetallurgy:industrial_crucible", ["FRF", "CBC", "FRF"], {
        "F": "tfmg:fireproof_bricks", "R": "create:mechanical_press",
        "C": "create:copper_casing", "B": "create:basin",
    }),
    "tfmg:blast_stove": shaped("tfmg:blast_stove", ["FPF", "PBP", "FSF"], {
        "F": "tfmg:fireproof_bricks", "P": "create:mechanical_pump",
        "B": "create:blaze_burner", "S": "createmetallurgy:industrial_crucible",
    }),
    "create:mechanical_saw": shaped("create:mechanical_saw", ["MMM", "STS", "ACA"], {
        "M": "createmetallurgy:graphite_ingot_mold", "S": "tfmg:steel_ingot",
        "T": "create:shaft", "A": "create:andesite_casing", "C": "create:cogwheel",
    }),
    # Era 3 — refining joins TFMG pressure hardware to Create fluid handling.
    "petrochem:distillation_controller": shaped("petrochem:distillation_controller", ["SVS", "PCP", "SVS"], {
        "S": "petrochem:steel_block", "V": "tfmg:steel_chemical_vat",
        "P": "create:mechanical_pump", "C": "create:precision_mechanism",
    }),
    "petrochem:pumpjack_well": shaped("petrochem:pumpjack_well", ["HPH", "TCT", "SPS"], {
        "H": "createdieselgenerators:pumpjack_head", "P": "create:mechanical_pump",
        "T": "tfmg:steel_pipe", "C": "petrochem:steel_block", "S": "tfmg:heavy_plate",
    }),
    "tfmg:steel_chemical_vat": shaped("tfmg:steel_chemical_vat", ["PVP", "STS", "PVP"], {
        "P": "petrochem:steel_fluid_pipe", "V": "create:mechanical_pump",
        "S": "tfmg:steel_block", "T": "tfmg:steel_fluid_tank",
    }),
    # Era 4 — grid machines require mechanical, heavy-industrial, and electrical parts.
    "create_new_age:basic_motor": shaped("create_new_age:basic_motor", ["TST", "MCM", "TST"], {
        "T": "tfmg:plastic_sheet", "S": "create:shaft",
        "M": "create_new_age:magnetite_block", "C": "create:andesite_casing",
    }),
    "ae2:energy_acceptor": shaped("ae2:energy_acceptor", ["QGQ", "TCT", "QGQ"], {
        "Q": "ae2:quartz_glass", "G": "create_new_age:generator_coil",
        "T": "powergrid:transformer_core", "C": "tfmg:steel_block",
    }),
    "powergrid:circuit_design_table": shaped("powergrid:circuit_design_table", ["PWP", "CMC", "PWP"], {
        "P": "petrochem:steel_block", "W": "create_new_age:copper_wire_block",
        "C": "create:precision_mechanism", "M": "powergrid:circuit_board",
    }),
    "create_new_age:advanced_energiser": shaped("create_new_age:advanced_energiser", ["EPE", "MGM", "EPE"], {
        "E": "ae2:energy_acceptor", "P": "powergrid:portable_battery",
        "M": "create_new_age:basic_motor", "G": "create:precision_mechanism",
    }),
    # Era 5 — computation and factory automation bootstrap one another in stages.
    "ae2:inscriber": shaped("ae2:inscriber", ["WGW", "PFP", "WGW"], {
        "W": "create_new_age:copper_wire_block", "G": "powergrid:copper_coil",
        "P": "create:mechanical_press", "F": "ae2:fluix_block",
    }),
    "oritech:assembler_block": shaped("oritech:assembler_block", ["EAE", "MCM", "EAE"], {
        "E": "ae2:engineering_processor", "A": "create_new_age:advanced_motor",
        "M": "oritech:motor", "C": "powergrid:circuit_board",
    }),
    "ae2:molecular_assembler": shaped("ae2:molecular_assembler", ["OMO", "CFC", "OMO"], {
        "O": "oritech:machine_core_1", "M": "create_new_age:basic_motor",
        "C": "powergrid:circuit_board", "F": "ae2:formation_core",
    }),
    "ae2:pattern_provider": shaped("ae2:pattern_provider", ["OCO", "MIM", "OCO"], {
        "O": "oritech:machine_core_1", "C": "powergrid:integrated_circuit",
        "M": "create_new_age:basic_motor", "I": "ae2:interface",
    }),
    "ae2:crafting_terminal": shaped("ae2:crafting_terminal", ["ODO", "CTC", "OEO"], {
        "O": "oritech:machine_core_1", "D": "create:display_link",
        "C": "powergrid:integrated_circuit", "T": "ae2:terminal", "E": "ae2:engineering_processor",
    }),
    "oritech:centrifuge_block": shaped("oritech:centrifuge_block", ["LML", "ECE", "LBL"], {
        "L": "ae2:logic_processor", "M": "create_new_age:advanced_motor",
        "E": "powergrid:integrated_circuit", "C": "oritech:machine_core_3", "B": "oritech:motor",
    }),
    "createcybernetics:surgery_table": shaped("createcybernetics:surgery_table", ["IAI", "BCB", "IAI"], {
        "I": "ae2:interface", "A": "oritech:assembler_block",
        "B": "powergrid:battery", "C": "createcybernetics:surgery_chamber",
    }),
    # Era 6 — nuclear controls require computation, stored power, and field coils.
    "createnuclear:reactor_controller": shaped("createnuclear:reactor_controller", ["EAE", "CNC", "EAE"], {
        "E": "ae2:engineering_processor", "A": "oritech:advanced_battery",
        "C": "createnuclear:reactor_casing", "N": "create_new_age:nuclear_fuel",
    }),
    "oritech:reactor_controller": shaped("oritech:reactor_controller", ["DGD", "RPR", "DGD"], {
        "D": "ae2:dense_energy_cell", "G": "create_new_age:generator_coil",
        "R": "createnuclear:reactor_controller", "P": "oritech:processing_unit",
    }),
    "ae2lt:module_radiation_protection": shaped("ae2lt:module_radiation_protection", ["RAR", "LML", "RAR"], {
        "R": "createnuclear:reactor_casing", "A": "oritech:advanced_battery",
        "L": "create_new_age:layered_magnet", "M": "ae2lt:overload_module_base",
    }),
    # Era 7 — spaceflight consumes mature nuclear, digital, electrical, and heavy industry.
    "stellaris:rocket_engine": shaped("stellaris:rocket_engine", ["DED", "CRC", "SMS"], {
        "D": "ae2:dense_energy_cell", "E": "oritech:machine_core_5",
        "C": "createnuclear:reactor_casing", "R": "stellaris:engine_fan",
        "S": "createbigcannons:steel_block", "M": "tfmg:steel_block",
    }),
    "stellaris:rocket_launch_pad": shaped("stellaris:rocket_launch_pad", ["HCH", "SMS", "HCH"], {
        "H": "powergrid:heavy_wire_connector", "C": "oritech:machine_core_5",
        "S": "createbigcannons:steel_block", "M": "tfmg:steel_block",
    }, 3),
    "stellaris:oxygen_distributor": shaped("stellaris:oxygen_distributor", ["ATA", "EPE", "ATA"], {
        "A": "ae2:energy_acceptor", "T": "powergrid:transformer_core",
        "E": "oritech:machine_core_5", "P": "stellaris:oxygen_tank",
    }),
    "stellaris:rocket_nose_cone": shaped("stellaris:rocket_nose_cone", [" C ", "OTO", "TAT"], {
        "C": "ae2:calculation_processor", "O": "oritech:machine_core_5",
        "T": "tfmg:steel_block", "A": "stellaris:steel_plating_block",
    }),
    "stellaris:rocket_fin": shaped("stellaris:rocket_fin", ["OTO", "SCS", "OTO"], {
        "O": "oritech:machine_core_3", "T": "tfmg:steel_block",
        "S": "createbigcannons:steel_block", "C": "stellaris:steel_plating_block",
    }),
    # Era 8 — endgame links orbital materials, atomic control, and Oritech cores into AE2.
    # One corner of each recipe's most-repeated part is spent on a fully-compressed
    # antimatter block instead: these are the pack's final gateway outputs, so each
    # now also gates on having run the antimatter economy (Oritech particle collision
    # -> AllTheCompressed x9 compression) all the way to its top tier.
    "ae2:quantum_ring": shaped("ae2:quantum_ring", ["ADO", "RER", "ODO"], {
        "A": "allthecompressed:antimatter_block_9x", "O": "oritech:machine_core_7", "D": "stellaris:desh_block",
        "R": "createnuclear:reactor_controller", "E": "ae2:engineering_processor",
    }),
    "oritech:accelerator_controller": shaped("oritech:accelerator_controller", ["ADQ", "RPR", "QDQ"], {
        "A": "allthecompressed:antimatter_block_9x", "Q": "ae2:quantum_ring", "D": "stellaris:desh_block",
        "R": "createnuclear:reactor_controller", "P": "oritech:processing_unit",
    }),
    "ae2:drive": shaped("ae2:drive", ["ADO", "RER", "ODO"], {
        "A": "allthecompressed:antimatter_block_9x", "O": "oritech:machine_core_7", "D": "stellaris:desh_plating_block",
        "R": "createnuclear:reactor_controller", "E": "ae2:engineering_processor",
    }),
    "ae2:dense_energy_cell": shaped("ae2:dense_energy_cell", ["ADO", "RER", "ODO"], {
        "A": "allthecompressed:antimatter_block_9x", "O": "oritech:advanced_battery", "D": "stellaris:desh_block",
        "R": "createnuclear:reactor_casing", "E": "ae2:energy_cell",
    }),
    "ae2:item_storage_cell_256k": shaped("ae2:item_storage_cell_256k", ["ADO", "RCR", "ODO"], {
        "A": "allthecompressed:antimatter_block_9x", "O": "oritech:machine_core_7", "D": "stellaris:desh_block",
        "R": "createnuclear:reactor_controller", "C": "ae2:cell_component_256k",
    }),
}


def main() -> None:
    registered = set(ITEM_REGISTRY.read_text(encoding="utf-8-sig").splitlines())
    invalid: list[str] = []
    for output, recipe in RECIPES.items():
        for ingredient in (entry["item"] for entry in recipe["key"].values()):
            if ingredient == output:
                invalid.append(f"{output}: direct self-recursion through {ingredient}")
            elif ingredient not in registered:
                invalid.append(f"{output}: unknown ingredient {ingredient}")
    if invalid:
        raise SystemExit("Invalid integration table:\n" + "\n".join(invalid))

    with INDEX.open(encoding="utf-8-sig", newline="") as handle:
        index_rows = list(csv.DictReader(handle))

    targets: list[tuple[str, str, Path]] = []
    for row in index_rows:
        if row.get("enabled", "").lower() != "true":
            continue
        outputs = {part.strip() for part in row.get("output_ids", "").split(";")}
        for output in RECIPES.keys() & outputs:
            path = ROOT / row["recommended_override_path"]
            targets.append((row["recipe_id"], output, path))

    seen = set()
    written = []
    for recipe_id, output, path in targets:
        if recipe_id in seen:
            continue
        seen.add(recipe_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(RECIPES[output], indent=2) + "\n", encoding="utf-8")
        written.append((recipe_id, output, path.relative_to(ROOT).as_posix()))

    # These are hand-designed policy overrides, not scaler-owned files. Removing
    # their IDs from the scaler manifest prevents later regeneration replacing them.
    if MANIFEST.exists():
        with MANIFEST.open(encoding="utf-8-sig", newline="") as handle:
            manifest_rows = list(csv.DictReader(handle))
            fields = list(manifest_rows[0]) if manifest_rows else []
        kept = [row for row in manifest_rows if row.get("recipe_id") not in seen]
        with MANIFEST.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(kept)

    report_dir = ROOT / "dev/docs" / "recipe-integration-audit"
    report_dir.mkdir(parents=True, exist_ok=True)
    with (report_dir / "curated-gateway-overrides.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["recipe_id", "output", "override_path"])
        writer.writerows(written)

    missing = sorted(set(RECIPES) - {output for _, output, _ in written})
    print(f"Wrote {len(written)} overrides for {len(RECIPES)} gateway outputs.")
    if missing:
        raise SystemExit(f"No effective recipe IDs found for: {', '.join(missing)}")


if __name__ == "__main__":
    main()
