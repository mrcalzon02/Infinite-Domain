from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import generate_wasteland_sites as g
import structure_geometry_primitives_v2 as v2p
from generate_wasteland_sites import DATA, Template
from structure_geometry_lint import lint_structure, positions_from_template

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "dev/structure_library" / "modules" / "structure-kits.json"
REPORT = ROOT / "dev/docs" / "structure-kit-extraction.json"


@dataclass(frozen=True)
class Spec:
    module_id: str
    kit: str
    role: str
    source_id: str
    builder: Callable[[], Template]
    bounds: tuple[int, int, int, int, int, int]
    connectors: tuple[str, ...]
    refinement: str = "none"


def refine_market_stall(module: Template) -> None:
    """Tie the canvas ridge into the four corner posts with real gable beams.

    The source tent's top four-wide wool ridge only met the lower slopes
    diagonally.  That is visually plausible at a glance but is disconnected
    Minecraft geometry once the stall is separated from its parent site.
    """
    for z in (1, module.size[2] - 2):
        module.fill((1, 5, z), (module.size[0] - 2, 5, z), "minecraft:stripped_oak_log", axis="x")


def refine_industrial_office_stair(module: Template) -> None:
    v2p.encased_stairwell(
        module, 3, 2, 11, 6, "south",
        block="minecraft:polished_andesite_stairs",
        wall="tfmg:cinder_block",
        width=1,
    )


def refine_industrial_dispatch_stair(module: Template) -> None:
    v2p.encased_stairwell(
        module, 3, 2, 10, 6, "south",
        block="minecraft:polished_andesite_stairs",
        wall="tfmg:cinder_block",
        width=1,
    )


def refine_industrial_process_line(module: Template) -> None:
    """Give the suspended mixer its own floor-supported drive gantry."""
    for x in (10, 14):
        module.fill((x, 2, 4), (x, 7, 4), "tfmg:steel_block")
    module.fill((10, 7, 4), (14, 7, 4), "tfmg:steel_block")
    module.set(12, 6, 4, "create:shaft", axis="y")


def refine_port_customs_warehouse(module: Template) -> None:
    """Complete the cropped facade and make the customs stair purposeful."""
    # The source's five-wide wall cut left a two-wide door hanging in open
    # air.  Restore masonry jambs and a lintel at the reusable-module edge.
    module.fill((5, 2, 1), (5, 4, 1), "tfmg:cinder_block")
    module.fill((8, 2, 1), (8, 4, 1), "tfmg:cinder_block")
    module.fill((5, 4, 1), (8, 4, 1), "tfmg:cinder_block")

    # A records mezzanine turns the formerly bare diagonal stair into a real
    # circulation route.  Build the floor before the v2 stair so the upper
    # tread and landing remain explicit and walkable.
    module.fill((2, 6, 11), (12, 6, 14), "minecraft:polished_andesite")
    module.fill((2, 7, 14), (4, 8, 14), "minecraft:bookshelf")
    module.fill((6, 7, 14), (8, 7, 14), "zvhouses:stone_brick_countertop")
    module.set(8, 8, 14, "supplementaries:item_shelf")
    v2p.encased_stairwell(
        module, 10, 2, 6, 5, "south",
        block="minecraft:stone_brick_stairs",
        wall="tfmg:cinder_block",
        width=1,
    )


REFINEMENTS: dict[str, Callable[[Template], None]] = {
    "market_stall_gable_frame": refine_market_stall,
    "industrial_office_stair": refine_industrial_office_stair,
    "industrial_dispatch_stair": refine_industrial_dispatch_stair,
    "industrial_process_gantry": refine_industrial_process_line,
    "port_customs_mezzanine": refine_port_customs_warehouse,
}


SPECS = (
    # Port/dock kit: climate-specific piers/tunnels plus shared service modules.
    Spec("harbor_loading_pier_warm", "port_dock", "wharf_pier_crane_cargo_staging", "warm_industrial_mountain_port_clean_master", g.warm_industrial_mountain_port_clean_master, (4, 2, 0, 24, 23, 19), ("water_north", "service_south", "cargo_east")),
    Spec("harbor_loading_pier_cold", "port_dock", "wharf_pier_crane_cargo_staging", "cold_industrial_mountain_port_clean_master", g.cold_industrial_mountain_port_clean_master, (4, 2, 0, 24, 23, 19), ("water_north", "service_south", "cargo_east")),
    Spec("port_customs_warehouse", "port_dock", "warehouse_customs_dock_office", "warm_industrial_mountain_port_clean_master", g.warm_industrial_mountain_port_clean_master, (1, 4, 19, 15, 17, 35), ("service_north", "yard_east"), "port_customs_mezzanine"),
    Spec("port_tunnel_control", "port_dock", "dockmaster_tunnel_control", "warm_industrial_mountain_port_clean_master", g.warm_industrial_mountain_port_clean_master, (32, 4, 20, 45, 16, 35), ("yard_north", "tunnel_west")),
    Spec("mountain_transport_tunnel_warm", "port_dock", "road_rail_mountain_connector", "warm_industrial_mountain_port_clean_master", g.warm_industrial_mountain_port_clean_master, (16, 2, 18, 30, 15, 46), ("harbor_north", "wasteland_south")),
    Spec("mountain_transport_tunnel_cold", "port_dock", "road_rail_mountain_connector", "cold_industrial_mountain_port_clean_master", g.cold_industrial_mountain_port_clean_master, (16, 2, 18, 30, 15, 46), ("harbor_north", "wasteland_south")),
    Spec("fuel_tank_containment_cell", "port_dock", "fuel_tank", "ruined_fuel_depot_clean_master", g.ruined_fuel_depot_clean_master, (8, 1, 12, 24, 13, 28), ("pipe_any", "service_any")),
    Spec("fuel_loading_rack", "port_dock", "fuel_loading_service", "ruined_fuel_depot_clean_master", g.ruined_fuel_depot_clean_master, (61, 1, 38, 78, 12, 58), ("service_north", "tank_west")),

    # Marketplace kit: four specialist stalls, lodge/services and public well.
    Spec("market_stall_provisions", "marketplace", "specialist_stall_provisions", "trade_outpost_clean_master", g.trade_outpost_clean_master, (4, 0, 10, 13, 8, 18), ("aisle_east",), "market_stall_gable_frame"),
    Spec("market_stall_medicine", "marketplace", "specialist_stall_medicine", "trade_outpost_clean_master", g.trade_outpost_clean_master, (35, 0, 10, 44, 8, 18), ("aisle_west",), "market_stall_gable_frame"),
    Spec("market_stall_repair", "marketplace", "specialist_stall_repair", "trade_outpost_clean_master", g.trade_outpost_clean_master, (4, 0, 23, 13, 8, 31), ("aisle_east",), "market_stall_gable_frame"),
    Spec("market_stall_livestock", "marketplace", "specialist_stall_livestock_feed", "trade_outpost_clean_master", g.trade_outpost_clean_master, (35, 0, 23, 44, 8, 31), ("aisle_west",), "market_stall_gable_frame"),
    Spec("market_trade_lodge", "marketplace", "covered_market_storage_office", "trade_outpost_clean_master", g.trade_outpost_clean_master, (14, 0, 15, 34, 17, 30), ("public_north", "service_south")),
    Spec("market_square_well", "marketplace", "public_square_service", "trade_outpost_clean_master", g.trade_outpost_clean_master, (20, 0, 29, 28, 4, 34), ("aisle_north", "aisle_south", "aisle_east", "aisle_west")),

    # Industrial kit: office, storage, truck/rail loading, process and power.
    Spec("industrial_office_annex", "industrial", "administration_staff_services", "corporate_warehouse_clean_master", g.corporate_warehouse_clean_master, (2, 0, 2, 19, 15, 23), ("public_north", "plant_east"), "industrial_office_stair"),
    Spec("industrial_truck_dock_bank", "industrial", "truck_loading_staging", "corporate_warehouse_clean_master", g.corporate_warehouse_clean_master, (14, 0, 30, 48, 15, 42), ("warehouse_north", "truck_south")),
    Spec("industrial_storage_rack_bay", "industrial", "warehouse_storage_quality_maintenance", "corporate_warehouse_clean_master", g.corporate_warehouse_clean_master, (20, 0, 8, 45, 14, 30), ("receiving_north", "dispatch_south", "office_west")),
    Spec("industrial_rail_loading_platform", "industrial", "rail_loading_siding", "freight_depot_clean_master", g.freight_depot_clean_master, (2, 0, 28, 34, 12, 36), ("warehouse_north", "rail_east", "rail_west")),
    Spec("industrial_dispatch_annex", "industrial", "freight_dispatch_driver_services", "freight_depot_clean_master", g.freight_depot_clean_master, (32, 0, 2, 45, 13, 21), ("public_north", "warehouse_west", "truck_south"), "industrial_dispatch_stair"),
    Spec("industrial_process_line", "industrial", "sequential_factory_process", "create_factory_clean_master", g.create_factory_clean_master, (11, 0, 8, 30, 10, 29), ("raw_west", "output_south", "service_east"), "industrial_process_gantry"),
    Spec("industrial_powerhouse", "industrial", "utility_power_steam_controls", "create_factory_clean_master", g.create_factory_clean_master, (34, 0, 19, 45, 26, 34), ("plant_west", "service_north")),
)


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")


def crop(source: Template, bounds: tuple[int, int, int, int, int, int]) -> Template:
    x1, y1, z1, x2, y2, z2 = bounds
    target = Template((x2 - x1 + 1, y2 - y1 + 1, z2 - z1 + 1))
    for (x, y, z), (state_index, nbt) in source.blocks.items():
        if not (x1 <= x <= x2 and y1 <= y <= y2 and z1 <= z <= z2):
            continue
        state = source.palette[state_index]
        target.set(x - x1, y - y1, z - z1, state["Name"], nbt, **state.get("Properties", {}))
    return target


def extract_module(spec: Spec, source: Template) -> Template:
    """Crop a reusable kit component and finish its severed module boundary."""
    module = crop(source, spec.bounds)
    if spec.refinement != "none":
        REFINEMENTS[spec.refinement](module)
    return module


def main() -> None:
    source_cache: dict[str, Template] = {}
    built_modules: list[tuple[Spec, Template, object]] = []
    geometry_failures: list[str] = []
    for spec in SPECS:
        if spec.source_id not in source_cache:
            source_cache[spec.source_id] = spec.builder()
        module = extract_module(spec, source_cache[spec.source_id])
        size, positions = positions_from_template(module)
        lint = lint_structure(spec.module_id, size, positions)
        if not lint.passed:
            geometry_failures.append(f"{spec.module_id}: {lint.hard_fail_count} hard-fail finding(s)")
        built_modules.append((spec, module, lint))
    if geometry_failures:
        raise SystemExit("Module extraction geometry gate failed:\n- " + "\n- ".join(geometry_failures))

    records = []
    extraction = []
    for spec, module, lint in built_modules:
        statistics = module.save(f"modules/{spec.module_id}")
        path = DATA / "structure" / "wasteland" / "modules" / f"{spec.module_id}.nbt"
        record = {
            "module_id": f"infinite_domain:{spec.module_id}",
            "kit": spec.kit,
            "role": spec.role,
            "source_clean_master": f"infinite_domain:{spec.source_id}",
            "source_bounds_inclusive": list(spec.bounds),
            "boundary_refinement": spec.refinement,
            "size": list(module.size),
            "connectors": list(spec.connectors),
            "placement_context": "terrain_embedded" if spec.role == "road_rail_mountain_connector" else "surface_module",
            "terrain_adaptation_requirement": "bury_or_mountain_mask" if spec.role == "road_rail_mountain_connector" else "contextual_lot_feathering",
            "source_template": f"kubejs/data/infinite_domain/structure/wasteland/modules/{spec.module_id}.nbt",
            "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "source_license": "Infinite Domain original work; distributable with the modpack",
            "extraction_tool": "scripts/extract_modular_structure_kits.py",
            "production_status": "quarantined_pending_module_review",
            "geometry_gate": {
                "passed": lint.passed,
                "hard_fail_count": lint.hard_fail_count,
            },
        }
        records.append(record)
        extraction.append({
            "module_id": record["module_id"],
            "boundary_refinement": spec.refinement,
            "geometry_hard_fail_count": lint.hard_fail_count,
            **statistics,
        })
    write_json(CATALOG, {
        "format_version": 1,
        "purpose": "Reusable components extracted from validated Infinite Domain clean masters; complete landmarks remain available but settlement assembly can select modules by lot and context.",
        "required_approval_checks": [
            "visual_module_boundary_review",
            "connector_and_rotation_test",
            "assembly_with_adjacent_modules",
            "terrain_and_coastline_placement"
        ],
        "known_source_limitations": [
            "No separate fish-market clean master exists; marketplace stalls are shared with port-town commercial assembly.",
            "Fuel tank and loading modules derive from the validated fuel-depot clean master rather than the monolithic port landmark."
        ],
        "production_approvals": [],
        "modules": records,
    })
    write_json(REPORT, {
        "kits": sorted({spec.kit for spec in SPECS}),
        "source_clean_masters": sorted(source_cache),
        "modules_extracted": len(records),
        "production_approvals": 0,
        "modules": extraction,
    })
    print(f"Extracted {len(records)} reusable modules from {len(source_cache)} clean masters across 3 kits")


if __name__ == "__main__":
    main()
