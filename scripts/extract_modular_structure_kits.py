from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import generate_wasteland_sites as g
from generate_wasteland_sites import DATA, Template

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "structure_library" / "modules" / "structure-kits.json"
REPORT = ROOT / "docs" / "structure-kit-extraction.json"


@dataclass(frozen=True)
class Spec:
    module_id: str
    kit: str
    role: str
    source_id: str
    builder: Callable[[], Template]
    bounds: tuple[int, int, int, int, int, int]
    connectors: tuple[str, ...]


SPECS = (
    # Port/dock kit: climate-specific piers/tunnels plus shared service modules.
    Spec("harbor_loading_pier_warm", "port_dock", "wharf_pier_crane_cargo_staging", "warm_industrial_mountain_port_clean_master", g.warm_industrial_mountain_port_clean_master, (4, 2, 0, 24, 23, 19), ("water_north", "service_south", "cargo_east")),
    Spec("harbor_loading_pier_cold", "port_dock", "wharf_pier_crane_cargo_staging", "cold_industrial_mountain_port_clean_master", g.cold_industrial_mountain_port_clean_master, (4, 2, 0, 24, 23, 19), ("water_north", "service_south", "cargo_east")),
    Spec("port_customs_warehouse", "port_dock", "warehouse_customs_dock_office", "warm_industrial_mountain_port_clean_master", g.warm_industrial_mountain_port_clean_master, (1, 4, 19, 15, 17, 35), ("service_north", "yard_east")),
    Spec("port_tunnel_control", "port_dock", "dockmaster_tunnel_control", "warm_industrial_mountain_port_clean_master", g.warm_industrial_mountain_port_clean_master, (32, 4, 20, 45, 16, 35), ("yard_north", "tunnel_west")),
    Spec("mountain_transport_tunnel_warm", "port_dock", "road_rail_mountain_connector", "warm_industrial_mountain_port_clean_master", g.warm_industrial_mountain_port_clean_master, (16, 2, 18, 30, 15, 46), ("harbor_north", "wasteland_south")),
    Spec("mountain_transport_tunnel_cold", "port_dock", "road_rail_mountain_connector", "cold_industrial_mountain_port_clean_master", g.cold_industrial_mountain_port_clean_master, (16, 2, 18, 30, 15, 46), ("harbor_north", "wasteland_south")),
    Spec("fuel_tank_containment_cell", "port_dock", "fuel_tank", "ruined_fuel_depot_clean_master", g.ruined_fuel_depot_clean_master, (8, 1, 12, 24, 13, 28), ("pipe_any", "service_any")),
    Spec("fuel_loading_rack", "port_dock", "fuel_loading_service", "ruined_fuel_depot_clean_master", g.ruined_fuel_depot_clean_master, (61, 1, 38, 78, 12, 58), ("service_north", "tank_west")),

    # Marketplace kit: four specialist stalls, lodge/services and public well.
    Spec("market_stall_provisions", "marketplace", "specialist_stall_provisions", "trade_outpost_clean_master", g.trade_outpost_clean_master, (4, 0, 10, 13, 8, 18), ("aisle_east",)),
    Spec("market_stall_medicine", "marketplace", "specialist_stall_medicine", "trade_outpost_clean_master", g.trade_outpost_clean_master, (35, 0, 10, 44, 8, 18), ("aisle_west",)),
    Spec("market_stall_repair", "marketplace", "specialist_stall_repair", "trade_outpost_clean_master", g.trade_outpost_clean_master, (4, 0, 23, 13, 8, 31), ("aisle_east",)),
    Spec("market_stall_livestock", "marketplace", "specialist_stall_livestock_feed", "trade_outpost_clean_master", g.trade_outpost_clean_master, (35, 0, 23, 44, 8, 31), ("aisle_west",)),
    Spec("market_trade_lodge", "marketplace", "covered_market_storage_office", "trade_outpost_clean_master", g.trade_outpost_clean_master, (14, 0, 15, 34, 17, 30), ("public_north", "service_south")),
    Spec("market_square_well", "marketplace", "public_square_service", "trade_outpost_clean_master", g.trade_outpost_clean_master, (20, 0, 29, 28, 4, 34), ("aisle_north", "aisle_south", "aisle_east", "aisle_west")),

    # Industrial kit: office, storage, truck/rail loading, process and power.
    Spec("industrial_office_annex", "industrial", "administration_staff_services", "corporate_warehouse_clean_master", g.corporate_warehouse_clean_master, (2, 0, 2, 19, 15, 23), ("public_north", "plant_east")),
    Spec("industrial_truck_dock_bank", "industrial", "truck_loading_staging", "corporate_warehouse_clean_master", g.corporate_warehouse_clean_master, (14, 0, 30, 48, 15, 42), ("warehouse_north", "truck_south")),
    Spec("industrial_storage_rack_bay", "industrial", "warehouse_storage_quality_maintenance", "corporate_warehouse_clean_master", g.corporate_warehouse_clean_master, (20, 0, 8, 45, 14, 30), ("receiving_north", "dispatch_south", "office_west")),
    Spec("industrial_rail_loading_platform", "industrial", "rail_loading_siding", "freight_depot_clean_master", g.freight_depot_clean_master, (2, 0, 28, 34, 12, 36), ("warehouse_north", "rail_east", "rail_west")),
    Spec("industrial_dispatch_annex", "industrial", "freight_dispatch_driver_services", "freight_depot_clean_master", g.freight_depot_clean_master, (32, 0, 2, 45, 13, 21), ("public_north", "warehouse_west", "truck_south")),
    Spec("industrial_process_line", "industrial", "sequential_factory_process", "create_factory_clean_master", g.create_factory_clean_master, (11, 0, 8, 30, 10, 29), ("raw_west", "output_south", "service_east")),
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


def main() -> None:
    source_cache: dict[str, Template] = {}
    records = []
    extraction = []
    for spec in SPECS:
        if spec.source_id not in source_cache:
            source_cache[spec.source_id] = spec.builder()
        source = source_cache[spec.source_id]
        module = crop(source, spec.bounds)
        statistics = module.save(f"modules/{spec.module_id}")
        path = DATA / "structure" / "wasteland" / "modules" / f"{spec.module_id}.nbt"
        record = {
            "module_id": f"infinite_domain:{spec.module_id}",
            "kit": spec.kit,
            "role": spec.role,
            "source_clean_master": f"infinite_domain:{spec.source_id}",
            "source_bounds_inclusive": list(spec.bounds),
            "size": list(module.size),
            "connectors": list(spec.connectors),
            "placement_context": "terrain_embedded" if spec.role == "road_rail_mountain_connector" else "surface_module",
            "terrain_adaptation_requirement": "bury_or_mountain_mask" if spec.role == "road_rail_mountain_connector" else "contextual_lot_feathering",
            "source_template": f"kubejs/data/infinite_domain/structure/wasteland/modules/{spec.module_id}.nbt",
            "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "source_license": "Infinite Domain original work; distributable with the modpack",
            "extraction_tool": "scripts/extract_modular_structure_kits.py",
            "production_status": "quarantined_pending_module_review",
        }
        records.append(record)
        extraction.append({"module_id": record["module_id"], **statistics})
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
