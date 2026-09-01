from __future__ import annotations

import json
from collections import Counter, deque
from pathlib import Path

from generate_wasteland_sites import (
    Template,
    abandoned_create_factory,
    bunker_network,
    bunker_network_clean_master,
    corporate_warehouse,
    corporate_warehouse_clean_master,
    create_factory_clean_master,
    fire_station_clean_master,
    freight_depot,
    freight_depot_clean_master,
    gas_station_clean_master,
    grocery_clean_master,
    grocery_store,
    motel_clean_master,
    ruined_fire_station,
    ruined_gas_station,
    survivor_cache,
    survivor_cache_clean_master,
    trade_outpost,
    trade_outpost_clean_master,
    decayed_farm,
    decayed_farm_clean_master,
    trailer_park,
    trailer_park_clean_master,
    mountain_military_complex,
    mountain_military_complex_clean_master,
    mountain_biohazard_lab,
    mountain_biohazard_lab_clean_master,
    decayed_logging_camp,
    decayed_logging_camp_clean_master,
    bombed_data_center,
    bombed_data_center_clean_master,
    hydroelectric_refuge_dam,
    hydroelectric_refuge_dam_clean_master,
    toppled_skyscraper,
    toppled_skyscraper_clean_master,
    blown_apartment_complex,
    blown_apartment_complex_clean_master,
    ruined_mixed_use_block,
    ruined_mixed_use_block_clean_master,
    sunken_city_front,
    sunken_city_front_clean_master,
    pancaked_parking_structure,
    pancaked_parking_structure_clean_master,
    cratered_downtown_intersection,
    cratered_downtown_intersection_clean_master,
    ruined_hospital,
    ruined_hospital_clean_master,
    ruined_police_precinct,
    ruined_police_precinct_clean_master,
    ruined_courthouse,
    ruined_courthouse_clean_master,
)


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs" / "structure-program-validation.json"


def block_name(template: Template, pos: tuple[int, int, int]) -> str | None:
    placed = template.blocks.get(pos)
    return template.palette[placed[0]]["Name"] if placed else None


def horizontally_reachable(
    template: Template,
    start: tuple[int, int, int],
    targets: set[tuple[int, int, int]],
) -> set[tuple[int, int, int]]:
    """Check floor circulation without treating the outside void as a route."""
    x_min, x_max, z_min, z_max = 1, template.size[0] - 2, 1, template.size[2] - 2

    def passable(pos: tuple[int, int, int]) -> bool:
        x, y, z = pos
        feet = block_name(template, pos)
        head = block_name(template, (x, y + 1, z))
        feet_open = feet == "minecraft:air" or bool(feet and feet.endswith("_door"))
        head_open = head == "minecraft:air" or bool(head and head.endswith("_door"))
        return feet_open and head_open

    visited = {start}
    queue = deque([start])
    while queue:
        x, y, z = queue.popleft()
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            candidate = (x + dx, y, z + dz)
            if candidate in visited or not (x_min <= candidate[0] <= x_max and z_min <= candidate[2] <= z_max):
                continue
            if passable(candidate):
                visited.add(candidate)
                queue.append(candidate)
    return targets & visited


def validate_motel() -> dict[str, object]:
    template = motel_clean_master()
    issues: list[str] = []
    room_centers = (6, 11, 21, 26)

    required_lower_doors = {(16, 2, 5), (17, 2, 5), (16, 2, 12), (17, 2, 12)}
    for floor_y in (2, 8):
        required_lower_doors.update({(center, floor_y, z) for center in room_centers for z in (16, 20, 24, 29)})
        required_lower_doors.update({(15, floor_y, 24), (16, floor_y, 24), (15, floor_y, 33), (16, floor_y, 33)})
    missing_doors = sorted(pos for pos in required_lower_doors if not (block_name(template, pos) or "").endswith("_door"))
    if missing_doors:
        issues.append(f"missing required lower doors at {missing_doors}")

    palette_counts = Counter(template.palette[state]["Name"] for state, _ in template.blocks.values())
    bed_blocks = sum(count for name, count in palette_counts.items() if name.endswith("_bed"))
    if bed_blocks != 32:
        issues.append(f"expected 32 bed blocks for 16 complete beds, found {bed_blocks}")

    circulation_results: dict[str, object] = {}
    for floor_y, start in ((2, (16, 2, 6)), (8, (15, 8, 13))):
        targets = {(16, floor_y, 22), (15, floor_y, 32)}
        for center in room_centers:
            targets.update({
                (center, floor_y, 15),
                (center, floor_y, 19),
                (center, floor_y, 25),
                (center, floor_y, 30),
            })
        reached = horizontally_reachable(template, start, targets)
        missing = sorted(targets - reached)
        circulation_results[f"floor_{1 if floor_y == 2 else 2}"] = {
            "targets": len(targets),
            "reached": len(reached),
            "missing": [list(pos) for pos in missing],
        }
        if missing:
            issues.append(f"floor {1 if floor_y == 2 else 2} has unreachable program points: {missing}")

    return {
        "structure_id": "infinite_domain:motel_clean_master",
        "archetype": "two-storey interior-corridor roadside motel",
        "guest_rooms": 16,
        "door_nodes_checked": len(required_lower_doors),
        "circulation": circulation_results,
        "valid": not issues,
        "issues": issues,
        "note": "Program validation checks declared doors, complete beds and same-floor reachability. It does not replace in-game player-scale inspection.",
    }


def validate_grocery() -> dict[str, object]:
    template = grocery_clean_master()
    issues: list[str] = []
    required_lower_doors = {
        (18, 2, 4), (19, 2, 4),
        (18, 2, 8), (19, 2, 8),
        (30, 2, 13),
        (8, 2, 23), (19, 2, 23), (29, 2, 23),
        (14, 2, 26), (24, 2, 26), (30, 2, 26),
        (8, 2, 29), (9, 2, 29), (32, 2, 29), (33, 2, 29),
    }
    missing_doors = sorted(pos for pos in required_lower_doors if not (block_name(template, pos) or "").endswith("_door"))
    if missing_doors:
        issues.append(f"missing required lower doors at {missing_doors}")

    targets = {
        (18, 2, 4),       # street-facing vestibule door
        (19, 2, 9),       # customer entry spine
        (12, 2, 13),      # checkout approach
        (7, 2, 15),       # produce circulation
        (8, 2, 19),       # bakery/deli approach
        (15, 2, 17), (17, 2, 17), (20, 2, 17), (22, 2, 17), (25, 2, 17), (27, 2, 17),
        (32, 2, 12),      # public restroom
        (8, 2, 24),       # receiving room threshold
        (19, 2, 24),      # stockroom threshold
        (29, 2, 24),      # staff-room threshold
        (8, 2, 29),       # loading exit
        (19, 2, 26),      # stockroom center lane
        (27, 2, 26),      # staff work area
        (32, 2, 29),      # independent staff exit
    }
    reached = horizontally_reachable(template, (18, 2, 5), targets)
    missing = sorted(targets - reached)
    if missing:
        issues.append(f"clean master has unreachable program points: {missing}")

    abandoned = grocery_store()
    survivor_targets = {(19, 2, 9), (19, 2, 24), (27, 2, 26), (32, 2, 29)}
    survivor_reached = horizontally_reachable(abandoned, (18, 2, 5), survivor_targets)
    survivor_missing = sorted(survivor_targets - survivor_reached)
    if survivor_missing:
        issues.append(f"abandoned derivative breaks required surviving routes: {survivor_missing}")

    return {
        "structure_id": "infinite_domain:grocery_clean_master",
        "archetype": "single-storey neighborhood supermarket",
        "door_nodes_checked": len(required_lower_doors),
        "clean_master_circulation": {
            "targets": len(targets),
            "reached": len(reached),
            "missing": [list(pos) for pos in missing],
        },
        "abandoned_survivor_routes": {
            "targets": len(survivor_targets),
            "reached": len(survivor_reached),
            "missing": [list(pos) for pos in survivor_missing],
        },
        "valid": not issues,
        "issues": issues,
        "note": "Program validation checks declared thresholds and same-floor reachability in both the clean master and required surviving routes in the damaged derivative. It does not replace in-game inspection.",
    }


def validate_gas_station() -> dict[str, object]:
    template = gas_station_clean_master()
    issues: list[str] = []
    required_lower_doors = {
        (11, 9, 22), (12, 9, 22),  # customer entrance
        (7, 9, 33), (14, 9, 33), (20, 9, 33),  # public-to-service thresholds
        (10, 9, 36), (17, 9, 36), (20, 9, 37),  # service-room connections
        (6, 9, 41), (7, 9, 41),  # receiving exit
    }
    missing_doors = sorted(pos for pos in required_lower_doors if not (block_name(template, pos) or "").endswith("_door"))
    if missing_doors:
        issues.append(f"missing required lower doors at {missing_doors}")

    targets = {
        (11, 9, 22),  # highway-facing customer threshold
        (12, 9, 26),  # checkout approach
        (8, 9, 27), (12, 9, 29), (16, 9, 29), (20, 9, 31),  # aisle and cooler routes
        (7, 9, 33), (7, 9, 39),  # receiving and stockroom
        (14, 9, 33), (14, 9, 39),  # office
        (20, 9, 33), (20, 9, 35),  # public restroom
        (20, 9, 37), (21, 9, 39),  # utility room
        (6, 9, 41),  # independent rear receiving exit
    }
    reached = horizontally_reachable(template, (11, 9, 23), targets)
    missing = sorted(targets - reached)
    if missing:
        issues.append(f"clean master has unreachable program points: {missing}")

    abandoned = ruined_gas_station()
    survivor_targets = {
        (12, 9, 26),  # checkout
        (7, 9, 33), (7, 9, 39),  # stockroom
        (14, 9, 33), (14, 9, 39),  # manager office
        (6, 9, 41),  # rear exit
    }
    survivor_reached = horizontally_reachable(abandoned, (11, 9, 23), survivor_targets)
    survivor_missing = sorted(survivor_targets - survivor_reached)
    if survivor_missing:
        issues.append(f"ruined derivative breaks required surviving routes: {survivor_missing}")

    return {
        "structure_id": "infinite_domain:gas_station_clean_master",
        "archetype": "highway filling station and convenience store",
        "door_nodes_checked": len(required_lower_doors),
        "clean_master_circulation": {
            "targets": len(targets),
            "reached": len(reached),
            "missing": [list(pos) for pos in missing],
        },
        "ruined_survivor_routes": {
            "targets": len(survivor_targets),
            "reached": len(survivor_reached),
            "missing": [list(pos) for pos in survivor_missing],
        },
        "valid": not issues,
        "issues": issues,
        "note": "Program validation checks declared thresholds and same-floor reachability through the shop and service rooms in both the clean master and damaged derivative. It does not replace in-game inspection.",
    }


def validate_freight_depot() -> dict[str, object]:
    template = freight_depot_clean_master()
    issues: list[str] = []
    required_lower_doors = {
        (37, 2, 4), (38, 2, 4),  # public/driver entrance
        (35, 2, 11), (38, 2, 11),  # lobby to service rooms
        (39, 2, 15),  # breakroom/restroom connection
        (33, 2, 15),  # dispatch to warehouse
        (39, 8, 12),  # upper manager/records connection
        (5, 2, 7), (6, 2, 7),  # warehouse staff exit
    }
    missing_doors = sorted(pos for pos in required_lower_doors if not (block_name(template, pos) or "").endswith("_door"))
    if missing_doors:
        issues.append(f"missing required lower doors at {missing_doors}")

    ground_targets = {
        (37, 2, 4),  # road-facing threshold
        (36, 2, 7),  # driver check-in
        (35, 2, 11), (35, 2, 15),  # dispatch and stair/service lobby
        (39, 2, 15), (42, 2, 17),  # breakroom/restroom
        (33, 2, 15),  # office-to-warehouse threshold
        (29, 2, 16),  # truck receiving
        (24, 2, 19),  # primary warehouse cross aisle
        (19, 2, 19),  # packing area
        (12, 2, 19),  # bulk-storage cross aisle
        (5, 2, 7),  # staff exit
        (18, 2, 28), (28, 2, 28),  # rail-door approaches
        (32, 2, 24),  # east truck-dock approach
    }
    ground_reached = horizontally_reachable(template, (37, 2, 5), ground_targets)
    ground_missing = sorted(ground_targets - ground_reached)
    if ground_missing:
        issues.append(f"clean master has unreachable ground program points: {ground_missing}")

    upper_targets = {
        (35, 8, 18),  # stair landing
        (37, 8, 6), (37, 8, 14),  # manager and dispatch desk approaches
        (39, 8, 12), (41, 8, 12), (41, 8, 17),  # records and observation side
    }
    upper_reached = horizontally_reachable(template, (35, 8, 18), upper_targets)
    upper_missing = sorted(upper_targets - upper_reached)
    if upper_missing:
        issues.append(f"clean master has unreachable upper-office points: {upper_missing}")

    stair_states = {
        y for (x, y, z), (state, _) in template.blocks.items()
        if template.palette[state]["Name"] == "minecraft:polished_andesite_stairs" and x == 35 and 12 <= z <= 17
    }
    if stair_states != set(range(2, 8)):
        issues.append(f"office stair does not span all six required rises: {sorted(stair_states)}")

    ruined = freight_depot()
    survivor_targets = {
        (35, 2, 15), (33, 2, 15),  # dispatch to warehouse
        (29, 2, 16), (24, 2, 19),  # receiving and central aisle
        (20, 2, 28), (28, 2, 28), (32, 2, 24),  # two rail bays and truck loading
    }
    survivor_reached = horizontally_reachable(ruined, (37, 2, 5), survivor_targets)
    survivor_missing = sorted(survivor_targets - survivor_reached)
    if survivor_missing:
        issues.append(f"ruined derivative breaks required surviving routes: {survivor_missing}")

    return {
        "structure_id": "infinite_domain:freight_depot_clean_master",
        "archetype": "rail freight depot with high-bay warehouse and dispatch offices",
        "door_nodes_checked": len(required_lower_doors),
        "clean_master_ground_circulation": {
            "targets": len(ground_targets),
            "reached": len(ground_reached),
            "missing": [list(pos) for pos in ground_missing],
        },
        "clean_master_upper_office": {
            "targets": len(upper_targets),
            "reached": len(upper_reached),
            "missing": [list(pos) for pos in upper_missing],
            "stair_rises_present": sorted(stair_states),
        },
        "ruined_survivor_routes": {
            "targets": len(survivor_targets),
            "reached": len(survivor_reached),
            "missing": [list(pos) for pos in survivor_missing],
        },
        "valid": not issues,
        "issues": issues,
        "note": "Program validation checks declared thresholds, two office levels, the full stair flight and surviving rail/truck circulation. It does not replace in-game inspection.",
    }


def validate_fire_station() -> dict[str, object]:
    template = fire_station_clean_master()
    issues: list[str] = []
    required_lower_doors = {
        (32, 2, 7), (33, 2, 7),  # public entrance
        (31, 2, 14), (37, 2, 14), (34, 2, 19),  # ground office suite
        (31, 2, 23), (37, 2, 23), (28, 2, 18),  # service corridor/apparatus
        (8, 2, 25), (16, 2, 25), (24, 2, 25),  # rear apparatus rooms
        (12, 2, 28), (20, 2, 28),  # support-room cross doors
        (37, 2, 32), (38, 2, 32),  # rear tower/staff exit
        (31, 8, 14), (37, 8, 14), (34, 8, 18),
        (31, 8, 23), (37, 8, 23),  # upper living floor
    }
    missing_doors = sorted(pos for pos in required_lower_doors if not (block_name(template, pos) or "").endswith("_door"))
    if missing_doors:
        issues.append(f"missing required lower doors at {missing_doors}")

    ground_targets = {
        (32, 2, 7), (32, 2, 10),  # entrance and lobby
        (39, 2, 9), (37, 2, 18), (39, 2, 20),  # watch, dispatch and restroom
        (28, 2, 18),  # office-to-apparatus threshold
        (8, 2, 23), (16, 2, 23), (24, 2, 20),  # three apparatus lanes
        (8, 2, 25), (8, 2, 29),  # turnout room
        (16, 2, 25), (16, 2, 29),  # workshop
        (24, 2, 25), (24, 2, 29),  # decontamination
        (37, 2, 32),  # rear tower/staff exit
    }
    ground_reached = horizontally_reachable(template, (32, 2, 8), ground_targets)
    ground_missing = sorted(ground_targets - ground_reached)
    if ground_missing:
        issues.append(f"clean master has unreachable ground program points: {ground_missing}")

    upper_targets = {
        (30, 8, 22),  # stair landing
        (31, 8, 10), (37, 8, 12),  # captain and records/dispatch
        (31, 8, 18), (32, 8, 21),  # kitchen and day room
        (36, 8, 19),  # dormitory aisle
        (31, 8, 27), (38, 8, 27),  # bathroom and linen/storage
    }
    upper_reached = horizontally_reachable(template, (30, 8, 22), upper_targets)
    upper_missing = sorted(upper_targets - upper_reached)
    if upper_missing:
        issues.append(f"clean master has unreachable upper living-floor points: {upper_missing}")

    stair_states = {
        y for (x, y, z), (state, _) in template.blocks.items()
        if template.palette[state]["Name"] == "minecraft:polished_andesite_stairs" and x == 30 and 16 <= z <= 21
    }
    if stair_states != set(range(2, 8)):
        issues.append(f"station stair does not span all six required rises: {sorted(stair_states)}")

    ruined = ruined_fire_station()
    survivor_ground_targets = {
        (39, 2, 9), (37, 2, 18), (28, 2, 18),
        (16, 2, 23), (24, 2, 20),
        (16, 2, 29), (24, 2, 29),
        (37, 2, 32),
    }
    survivor_ground_reached = horizontally_reachable(ruined, (32, 2, 8), survivor_ground_targets)
    survivor_ground_missing = sorted(survivor_ground_targets - survivor_ground_reached)
    if survivor_ground_missing:
        issues.append(f"ruined derivative breaks required ground routes: {survivor_ground_missing}")

    survivor_upper_targets = {(31, 8, 10), (31, 8, 18), (36, 8, 19), (31, 8, 27)}
    survivor_upper_reached = horizontally_reachable(ruined, (30, 8, 22), survivor_upper_targets)
    survivor_upper_missing = sorted(survivor_upper_targets - survivor_upper_reached)
    if survivor_upper_missing:
        issues.append(f"ruined derivative breaks required upper routes: {survivor_upper_missing}")

    return {
        "structure_id": "infinite_domain:fire_station_clean_master",
        "archetype": "three-bay municipal fire station with living quarters and hose tower",
        "door_nodes_checked": len(required_lower_doors),
        "clean_master_ground_circulation": {
            "targets": len(ground_targets), "reached": len(ground_reached),
            "missing": [list(pos) for pos in ground_missing],
        },
        "clean_master_upper_living_floor": {
            "targets": len(upper_targets), "reached": len(upper_reached),
            "missing": [list(pos) for pos in upper_missing],
            "stair_rises_present": sorted(stair_states),
        },
        "ruined_survivor_ground_routes": {
            "targets": len(survivor_ground_targets), "reached": len(survivor_ground_reached),
            "missing": [list(pos) for pos in survivor_ground_missing],
        },
        "ruined_survivor_upper_routes": {
            "targets": len(survivor_upper_targets), "reached": len(survivor_upper_reached),
            "missing": [list(pos) for pos in survivor_upper_missing],
        },
        "valid": not issues,
        "issues": issues,
        "note": "Program validation checks public, apparatus, support, living-floor and rear-tower routes plus the complete stair. It does not replace in-game inspection.",
    }


def validate_corporate_warehouse() -> dict[str, object]:
    template = corporate_warehouse_clean_master()
    issues: list[str] = []
    required_lower_doors = {
        (8, 2, 4), (9, 2, 4),  # corporate entrance
        (6, 2, 11), (14, 2, 11), (10, 2, 15), (14, 2, 15),
        (12, 2, 18), (16, 2, 18), (18, 2, 17),  # office/service connections
        (18, 2, 21), (21, 2, 19),  # quality-control room
        (41, 2, 16), (39, 2, 12),  # maintenance room
        (45, 2, 20),  # east staff exit
        (6, 8, 11), (14, 8, 11), (10, 8, 16), (14, 8, 18),  # upper offices
    }
    missing_doors = sorted(pos for pos in required_lower_doors if not (block_name(template, pos) or "").endswith("_door"))
    if missing_doors:
        issues.append(f"missing required lower doors at {missing_doors}")

    ground_targets = {
        (8, 2, 4), (8, 2, 7), (16, 2, 7),
        (6, 2, 15), (12, 2, 15), (16, 2, 15),
        (18, 2, 17), (19, 2, 18),
        (24, 2, 19), (31, 2, 19), (36, 2, 19), (42, 2, 19),
        (42, 2, 14), (21, 2, 34),
        (20, 2, 35), (27, 2, 35), (34, 2, 35), (41, 2, 35),
        (45, 2, 20),
    }
    ground_reached = horizontally_reachable(template, (8, 2, 5), ground_targets)
    ground_missing = sorted(ground_targets - ground_reached)
    if ground_missing:
        issues.append(f"clean master has unreachable ground program points: {ground_missing}")

    upper_targets = {
        (5, 8, 19), (7, 8, 7), (13, 8, 7),
        (11, 8, 15), (16, 8, 18), (12, 8, 20),
    }
    upper_reached = horizontally_reachable(template, (5, 8, 19), upper_targets)
    upper_missing = sorted(upper_targets - upper_reached)
    if upper_missing:
        issues.append(f"clean master has unreachable upper office points: {upper_missing}")

    stair_states = {
        y for (x, y, z), (state, _) in template.blocks.items()
        if template.palette[state]["Name"] == "minecraft:polished_andesite_stairs" and x == 5 and 13 <= z <= 18
    }
    if stair_states != set(range(2, 8)):
        issues.append(f"corporate stair does not span all six required rises: {sorted(stair_states)}")

    ruined = corporate_warehouse()
    survivor_ground_targets = {
        (12, 2, 15), (18, 2, 17), (19, 2, 18),
        (24, 2, 19), (31, 2, 19), (36, 2, 19),
        (20, 2, 35), (27, 2, 35), (34, 2, 35), (45, 2, 20),
    }
    survivor_ground_reached = horizontally_reachable(ruined, (8, 2, 5), survivor_ground_targets)
    survivor_ground_missing = sorted(survivor_ground_targets - survivor_ground_reached)
    if survivor_ground_missing:
        issues.append(f"ruined derivative breaks required ground routes: {survivor_ground_missing}")

    survivor_upper_targets = {(7, 8, 7), (13, 8, 7), (11, 8, 15), (12, 8, 20)}
    survivor_upper_reached = horizontally_reachable(ruined, (5, 8, 19), survivor_upper_targets)
    survivor_upper_missing = sorted(survivor_upper_targets - survivor_upper_reached)
    if survivor_upper_missing:
        issues.append(f"ruined derivative breaks required upper routes: {survivor_upper_missing}")

    return {
        "structure_id": "infinite_domain:corporate_warehouse_clean_master",
        "archetype": "road distribution center with corporate offices and truck docks",
        "door_nodes_checked": len(required_lower_doors),
        "clean_master_ground_circulation": {
            "targets": len(ground_targets), "reached": len(ground_reached),
            "missing": [list(pos) for pos in ground_missing],
        },
        "clean_master_upper_office": {
            "targets": len(upper_targets), "reached": len(upper_reached),
            "missing": [list(pos) for pos in upper_missing],
            "stair_rises_present": sorted(stair_states),
        },
        "ruined_survivor_ground_routes": {
            "targets": len(survivor_ground_targets), "reached": len(survivor_ground_reached),
            "missing": [list(pos) for pos in survivor_ground_missing],
        },
        "ruined_survivor_upper_routes": {
            "targets": len(survivor_upper_targets), "reached": len(survivor_upper_reached),
            "missing": [list(pos) for pos in survivor_upper_missing],
        },
        "valid": not issues,
        "issues": issues,
        "note": "Program validation checks both corporate floors, quality/maintenance rooms, rack aisles, staging, dock approaches and the east staff exit. It does not replace in-game inspection.",
    }


def validate_create_factory() -> dict[str, object]:
    template = create_factory_clean_master()
    issues: list[str] = []
    required_lower_doors = {
        (38, 2, 4), (39, 2, 4),  # staff entrance
        (39, 2, 11), (42, 2, 11), (40, 2, 16), (35, 2, 17),  # ground offices/hall
        (37, 8, 11), (42, 8, 11), (40, 8, 16),  # upper engineering/records
        (29, 2, 21), (34, 2, 29),  # maintenance and quality rooms
        (35, 2, 27),  # production hall to powerhouse
    }
    missing_doors = sorted(pos for pos in required_lower_doors if not (block_name(template, pos) or "").endswith("_door"))
    if missing_doors:
        issues.append(f"missing required lower doors at {missing_doors}")

    ground_targets = {
        (38, 2, 4), (38, 2, 7), (41, 2, 7),
        (38, 2, 13), (42, 2, 13), (42, 2, 18),
        (35, 2, 17), (11, 2, 18),
        (16, 2, 17), (25, 2, 17), (14, 2, 22), (24, 2, 22),
        (29, 2, 21), (34, 2, 29), (34, 2, 31),
        (35, 2, 27), (39, 2, 26),
        (10, 2, 32), (20, 2, 32), (30, 2, 32),
    }
    ground_reached = horizontally_reachable(template, (38, 2, 5), ground_targets)
    ground_missing = sorted(ground_targets - ground_reached)
    if ground_missing:
        issues.append(f"clean master has unreachable ground program points: {ground_missing}")

    upper_targets = {
        (37, 8, 18), (37, 8, 7), (40, 8, 7),
        (38, 8, 14), (41, 8, 14), (41, 8, 18),
    }
    upper_reached = horizontally_reachable(template, (37, 8, 18), upper_targets)
    upper_missing = sorted(upper_targets - upper_reached)
    if upper_missing:
        issues.append(f"clean master has unreachable upper-office points: {upper_missing}")

    catwalk_targets = {(32, 10, 19), (14, 10, 19), (24, 10, 19), (33, 10, 28)}
    catwalk_reached = horizontally_reachable(template, (32, 10, 19), catwalk_targets)
    catwalk_missing = sorted(catwalk_targets - catwalk_reached)
    if catwalk_missing:
        issues.append(f"clean master has unreachable production-catwalk points: {catwalk_missing}")

    office_stair_states = {
        y for (x, y, z), (state, _) in template.blocks.items()
        if template.palette[state]["Name"] == "minecraft:polished_andesite_stairs" and x == 37 and 12 <= z <= 17
    }
    if office_stair_states != set(range(2, 8)):
        issues.append(f"office stair does not span all six required rises: {sorted(office_stair_states)}")
    catwalk_stair_states = {
        y for (x, y, z), (state, _) in template.blocks.items()
        if template.palette[state]["Name"] == "minecraft:polished_andesite_stairs" and x == 32 and 12 <= z <= 18
    }
    if catwalk_stair_states != set(range(2, 9)):
        issues.append(f"catwalk stair does not span all seven required rises: {sorted(catwalk_stair_states)}")

    ruined = abandoned_create_factory()
    survivor_ground_targets = {
        (38, 2, 7), (42, 2, 13), (35, 2, 17),
        (25, 2, 17), (24, 2, 22), (29, 2, 21), (34, 2, 29),
        (35, 2, 27), (39, 2, 26),
        (10, 2, 32), (20, 2, 32), (30, 2, 32),
    }
    survivor_ground_reached = horizontally_reachable(ruined, (38, 2, 5), survivor_ground_targets)
    survivor_ground_missing = sorted(survivor_ground_targets - survivor_ground_reached)
    if survivor_ground_missing:
        issues.append(f"ruined derivative breaks required ground routes: {survivor_ground_missing}")

    survivor_upper_targets = {(37, 8, 7), (40, 8, 7), (38, 8, 14), (41, 8, 18)}
    survivor_upper_reached = horizontally_reachable(ruined, (37, 8, 18), survivor_upper_targets)
    survivor_upper_missing = sorted(survivor_upper_targets - survivor_upper_reached)
    if survivor_upper_missing:
        issues.append(f"ruined derivative breaks required upper-office routes: {survivor_upper_missing}")

    survivor_catwalk_targets = {(14, 10, 19), (24, 10, 19), (33, 10, 28)}
    survivor_catwalk_reached = horizontally_reachable(ruined, (32, 10, 19), survivor_catwalk_targets)
    survivor_catwalk_missing = sorted(survivor_catwalk_targets - survivor_catwalk_reached)
    if survivor_catwalk_missing:
        issues.append(f"ruined derivative breaks required catwalk routes: {survivor_catwalk_missing}")

    return {
        "structure_id": "infinite_domain:create_factory_clean_master",
        "archetype": "Create-era sequential fabrication plant with offices, powerhouse and docks",
        "door_nodes_checked": len(required_lower_doors),
        "clean_master_ground_circulation": {
            "targets": len(ground_targets), "reached": len(ground_reached),
            "missing": [list(pos) for pos in ground_missing],
        },
        "clean_master_upper_office": {
            "targets": len(upper_targets), "reached": len(upper_reached),
            "missing": [list(pos) for pos in upper_missing],
            "stair_rises_present": sorted(office_stair_states),
        },
        "clean_master_production_catwalk": {
            "targets": len(catwalk_targets), "reached": len(catwalk_reached),
            "missing": [list(pos) for pos in catwalk_missing],
            "stair_rises_present": sorted(catwalk_stair_states),
        },
        "ruined_survivor_ground_routes": {
            "targets": len(survivor_ground_targets), "reached": len(survivor_ground_reached),
            "missing": [list(pos) for pos in survivor_ground_missing],
        },
        "ruined_survivor_upper_routes": {
            "targets": len(survivor_upper_targets), "reached": len(survivor_upper_reached),
            "missing": [list(pos) for pos in survivor_upper_missing],
        },
        "ruined_survivor_catwalk_routes": {
            "targets": len(survivor_catwalk_targets), "reached": len(survivor_catwalk_reached),
            "missing": [list(pos) for pos in survivor_catwalk_missing],
        },
        "valid": not issues,
        "issues": issues,
        "note": "Program validation checks sequential production approaches, both office floors, maintenance/quality rooms, powerhouse, three docks, two complete stairs and the surviving ruin routes. It does not replace in-game inspection.",
    }


def validate_bunker_network() -> dict[str, object]:
    template = bunker_network_clean_master()
    issues: list[str] = []
    required_lower_doors = {
        (22, 18, 1), (23, 18, 1), (22, 18, 7), (23, 18, 7), (25, 18, 11),
        (22, 10, 8), (23, 10, 8),
        (22, 10, 13), (23, 10, 13), (22, 10, 16), (23, 10, 16),
        (13, 10, 22), (13, 10, 23), (16, 10, 22), (16, 10, 23),
        (31, 10, 22), (31, 10, 23), (33, 10, 22), (33, 10, 23),
        (8, 10, 24), (38, 10, 24),
        (22, 10, 31), (23, 10, 31), (22, 10, 35), (23, 10, 35),
        (22, 10, 40), (23, 10, 40),
        (13, 2, 22), (13, 2, 23), (16, 2, 22), (16, 2, 23),
        (31, 2, 22), (31, 2, 23), (33, 2, 22), (33, 2, 23),
        (22, 2, 31), (23, 2, 31), (27, 2, 25), (11, 2, 24),
        (5, 2, 20), (8, 2, 20), (11, 2, 20), (38, 2, 24),
        (22, 2, 40), (23, 2, 40),
    }
    missing_doors = sorted(pos for pos in required_lower_doors if not (block_name(template, pos) or "").endswith("_door"))
    if missing_doors:
        issues.append(f"missing required lower doors at {missing_doors}")

    surface_targets = {
        (22, 18, 1), (22, 18, 4), (19, 18, 4), (27, 18, 4),
        (22, 18, 7), (19, 18, 10), (28, 18, 9), (26, 18, 12),
    }
    surface_reached = horizontally_reachable(template, (22, 18, 2), surface_targets)
    surface_missing = sorted(surface_targets - surface_reached)
    if surface_missing:
        issues.append(f"clean master has unreachable surface-entrance points: {surface_missing}")

    main_targets = {
        (22, 10, 5), (22, 10, 10), (22, 10, 13), (22, 10, 16),
        (23, 10, 20), (17, 10, 26),
        (8, 10, 22), (8, 10, 28),
        (38, 10, 20), (42, 10, 28), (42, 10, 29),
        (22, 10, 35), (22, 10, 38), (22, 10, 42),
    }
    main_reached = horizontally_reachable(template, (22, 10, 5), main_targets)
    main_missing = sorted(main_targets - main_reached)
    if main_missing:
        issues.append(f"clean master has unreachable operational-level points: {main_missing}")

    lower_targets = {
        (17, 2, 17), (20, 2, 22), (27, 2, 25),
        (8, 2, 22), (8, 2, 28),
        (38, 2, 22), (38, 2, 28),
        (22, 2, 35), (23, 2, 38), (22, 2, 42),
    }
    lower_reached = horizontally_reachable(template, (17, 2, 17), lower_targets)
    lower_missing = sorted(lower_targets - lower_reached)
    if lower_missing:
        issues.append(f"clean master has unreachable protected-level points: {lower_missing}")

    stair_states = {
        y for (x, y, z), (state, _) in template.blocks.items()
        if template.palette[state]["Name"] == "minecraft:polished_andesite_stairs" and x == 17 and 18 <= z <= 25
    }
    if stair_states != set(range(2, 10)):
        issues.append(f"inter-level stair does not span all eight required rises: {sorted(stair_states)}")
    north_ladder = {
        y for (x, y, z), (state, _) in template.blocks.items()
        if template.palette[state]["Name"] == "minecraft:ladder" and x == 18 and z == 10
    }
    east_ladder = {
        y for (x, y, z), (state, _) in template.blocks.items()
        if template.palette[state]["Name"] == "minecraft:ladder" and x == 43 and z == 29
    }
    if north_ladder != set(range(10, 17)):
        issues.append(f"north access ladder is incomplete: {sorted(north_ladder)}")
    if east_ladder != set(range(10, 17)):
        issues.append(f"east emergency ladder is incomplete: {sorted(east_ladder)}")

    occupied = bunker_network()
    survivor_surface_reached = horizontally_reachable(occupied, (22, 18, 2), surface_targets)
    survivor_surface_missing = sorted(surface_targets - survivor_surface_reached)
    if survivor_surface_missing:
        issues.append(f"occupied derivative breaks required surface-entrance routes: {survivor_surface_missing}")
    survivor_main_targets = {
        (22, 10, 10), (22, 10, 16), (23, 10, 20), (17, 10, 26),
        (8, 10, 28), (38, 10, 20), (42, 10, 28), (42, 10, 29),
        (22, 10, 38), (22, 10, 42),
    }
    survivor_main_reached = horizontally_reachable(occupied, (22, 10, 5), survivor_main_targets)
    survivor_main_missing = sorted(survivor_main_targets - survivor_main_reached)
    if survivor_main_missing:
        issues.append(f"occupied derivative breaks required operational-level routes: {survivor_main_missing}")

    survivor_lower_targets = {
        (20, 2, 22), (27, 2, 25), (8, 2, 22), (8, 2, 28),
        (38, 2, 22), (38, 2, 28), (22, 2, 35), (23, 2, 38),
    }
    survivor_lower_reached = horizontally_reachable(occupied, (17, 2, 17), survivor_lower_targets)
    survivor_lower_missing = sorted(survivor_lower_targets - survivor_lower_reached)
    if survivor_lower_missing:
        issues.append(f"occupied derivative breaks required protected-level routes: {survivor_lower_missing}")

    spawner_count = sum(
        1 for state, _ in occupied.blocks.values()
        if occupied.palette[state]["Name"] == "minecraft:spawner"
    )
    if spawner_count != 6:
        issues.append(f"expected six distributed pillager spawners, found {spawner_count}")

    return {
        "structure_id": "infinite_domain:bunker_network_clean_master",
        "archetype": "two-level modular civil-defense bunker network",
        "door_nodes_checked": len(required_lower_doors),
        "clean_master_surface_entrance": {
            "targets": len(surface_targets), "reached": len(surface_reached),
            "missing": [list(pos) for pos in surface_missing],
        },
        "clean_master_operational_level": {
            "targets": len(main_targets), "reached": len(main_reached),
            "missing": [list(pos) for pos in main_missing],
        },
        "clean_master_protected_level": {
            "targets": len(lower_targets), "reached": len(lower_reached),
            "missing": [list(pos) for pos in lower_missing],
        },
        "vertical_access": {
            "stair_rises_present": sorted(stair_states),
            "north_ladder_levels": sorted(north_ladder),
            "east_ladder_levels": sorted(east_ladder),
        },
        "occupied_survivor_operational_routes": {
            "targets": len(survivor_main_targets), "reached": len(survivor_main_reached),
            "missing": [list(pos) for pos in survivor_main_missing],
        },
        "occupied_survivor_surface_routes": {
            "targets": len(surface_targets), "reached": len(survivor_surface_reached),
            "missing": [list(pos) for pos in survivor_surface_missing],
        },
        "occupied_survivor_protected_routes": {
            "targets": len(survivor_lower_targets), "reached": len(survivor_lower_reached),
            "missing": [list(pos) for pos in survivor_lower_missing],
        },
        "pillager_spawners": spawner_count,
        "valid": not issues,
        "issues": issues,
        "note": "Program validation checks the surface entrance facility, both bunker levels, forty-five declared door thresholds, the complete inter-level stair, two exit ladders, distributed occupation and required routes through the damaged derivative. It does not replace in-game inspection.",
    }
def validate_survivor_cache() -> dict[str, object]:
    template = survivor_cache_clean_master()
    issues: list[str] = []
    required_lower_doors = {
        (12, 10, 1), (13, 10, 1), (13, 10, 6),
        (7, 2, 13), (17, 2, 13), (12, 2, 17), (7, 2, 19), (17, 2, 19),
    }
    missing_doors = sorted(pos for pos in required_lower_doors if not (block_name(template, pos) or "").endswith("_door"))
    if missing_doors:
        issues.append(f"missing required lower doors at {missing_doors}")

    surface_targets = {
        (12, 10, 1), (12, 10, 3), (13, 10, 6),
        (10, 10, 8), (17, 10, 8), (12, 10, 7),
    }
    surface_reached = horizontally_reachable(template, (12, 10, 2), surface_targets)
    surface_missing = sorted(surface_targets - surface_reached)
    if surface_missing:
        issues.append(f"clean master has unreachable surface-shed points: {surface_missing}")

    underground_targets = {
        (11, 2, 14), (7, 2, 13), (17, 2, 13),
        (7, 2, 19), (17, 2, 19),
        (5, 2, 16), (6, 2, 22),
        (17, 2, 17), (15, 2, 22), (22, 2, 23),
    }
    underground_reached = horizontally_reachable(template, (11, 2, 14), underground_targets)
    underground_missing = sorted(underground_targets - underground_reached)
    if underground_missing:
        issues.append(f"clean master has unreachable shelter points: {underground_missing}")

    stair_states = {
        y for (x, y, z), (state, _) in template.blocks.items()
        if template.palette[state]["Name"] == "minecraft:polished_andesite_stairs" and x == 12 and 7 <= z <= 14
    }
    if stair_states != set(range(2, 10)):
        issues.append(f"shelter stair does not span all eight required rises: {sorted(stair_states)}")
    emergency_ladder = {
        y for (x, y, z), (state, _) in template.blocks.items()
        if template.palette[state]["Name"] == "minecraft:ladder" and x == 23 and z == 23
    }
    if emergency_ladder != set(range(2, 9)):
        issues.append(f"emergency ladder is incomplete: {sorted(emergency_ladder)}")

    occupied = survivor_cache()
    survivor_surface_reached = horizontally_reachable(occupied, (12, 10, 2), surface_targets)
    survivor_surface_missing = sorted(surface_targets - survivor_surface_reached)
    if survivor_surface_missing:
        issues.append(f"occupied derivative breaks required surface routes: {survivor_surface_missing}")
    survivor_underground_reached = horizontally_reachable(occupied, (11, 2, 14), underground_targets)
    survivor_underground_missing = sorted(underground_targets - survivor_underground_reached)
    if survivor_underground_missing:
        issues.append(f"occupied derivative breaks required shelter routes: {survivor_underground_missing}")

    spawner_count = sum(
        1 for state, _ in occupied.blocks.values()
        if occupied.palette[state]["Name"] == "minecraft:spawner"
    )
    if spawner_count != 4:
        issues.append(f"expected four distributed pillager spawners, found {spawner_count}")

    return {
        "structure_id": "infinite_domain:survivor_cache_clean_master",
        "archetype": "surface-concealed survivor shelter with independent emergency hatch",
        "door_nodes_checked": len(required_lower_doors),
        "clean_master_surface_shed": {
            "targets": len(surface_targets), "reached": len(surface_reached),
            "missing": [list(pos) for pos in surface_missing],
        },
        "clean_master_underground_shelter": {
            "targets": len(underground_targets), "reached": len(underground_reached),
            "missing": [list(pos) for pos in underground_missing],
        },
        "vertical_access": {
            "stair_rises_present": sorted(stair_states),
            "emergency_ladder_levels": sorted(emergency_ladder),
        },
        "occupied_survivor_surface_routes": {
            "targets": len(surface_targets), "reached": len(survivor_surface_reached),
            "missing": [list(pos) for pos in survivor_surface_missing],
        },
        "occupied_survivor_shelter_routes": {
            "targets": len(underground_targets), "reached": len(survivor_underground_reached),
            "missing": [list(pos) for pos in survivor_underground_missing],
        },
        "pillager_spawners": spawner_count,
        "valid": not issues,
        "issues": issues,
        "note": "Program validation checks the surface shed, roomed underground shelter, complete stair, independent emergency hatch, pillager occupation and all required damaged-variant routes. It does not replace in-game inspection.",
    }


def validate_trade_outpost() -> dict[str, object]:
    template = trade_outpost_clean_master()
    issues: list[str] = []
    required_lower_doors = {
        (18, 2, 9), (30, 2, 9),
        (23, 2, 16), (24, 2, 16), (19, 2, 23), (29, 2, 23),
        (24, 2, 26), (23, 2, 29), (24, 2, 29),
        (23, 2, 34), (24, 2, 34),
        (11, 1, 33), (12, 1, 33), (37, 1, 33), (38, 1, 33),
    }
    missing_doors = sorted(pos for pos in required_lower_doors if not (block_name(template, pos) or "").endswith("_door"))
    if missing_doors:
        issues.append(f"missing required lower doors at {missing_doors}")

    program_targets = {
        (24, 2, 9), (18, 2, 8), (30, 2, 8),
        (12, 2, 14), (36, 2, 14), (12, 2, 27), (36, 2, 27),
        (23, 2, 16), (20, 2, 20), (28, 2, 20),
        (19, 2, 26), (29, 2, 26), (24, 2, 29),
        (24, 2, 32), (24, 2, 35), (21, 2, 39), (28, 2, 39),
        (11, 2, 33), (10, 2, 37), (37, 2, 33), (38, 2, 37),
    }
    reached = horizontally_reachable(template, (24, 2, 10), program_targets)
    missing = sorted(program_targets - reached)
    if missing:
        issues.append(f"clean master has unreachable settlement program points: {missing}")

    # Each paddock boundary must remain continuous at both rail levels. Doors
    # count as stable full threshold blocks; absent cells would release stock.
    paddock_missing: list[tuple[int, int, int]] = []
    for x1, x2 in ((5, 17), (31, 43)):
        boundary = {(x, z) for x in range(x1, x2 + 1) for z in (33, 43)}
        boundary.update({(x, z) for x in (x1, x2) for z in range(34, 43)})
        for x, z in boundary:
            for y in (1, 2):
                if block_name(template, (x, y, z)) in {None, "minecraft:air"}:
                    paddock_missing.append((x, y, z))
    if paddock_missing:
        issues.append(f"paddock boundaries contain gaps: {paddock_missing}")

    animal_types = Counter(
        str(entity["nbt"]["id"]) for entity in template.entities
        if str(entity["nbt"]["id"]) in {"minecraft:cow", "minecraft:sheep", "minecraft:pig", "minecraft:chicken"}
    )
    expected_animals = Counter({"minecraft:cow": 2, "minecraft:sheep": 2, "minecraft:pig": 1, "minecraft:chicken": 1})
    if animal_types != expected_animals:
        issues.append(f"expected stocked mixed paddocks {dict(expected_animals)}, found {dict(animal_types)}")

    inhabited = trade_outpost()
    survivor_reached = horizontally_reachable(inhabited, (24, 2, 10), program_targets)
    survivor_missing = sorted(program_targets - survivor_reached)
    if survivor_missing:
        issues.append(f"damaged derivative breaks required settlement routes: {survivor_missing}")
    derivative_animals = Counter(
        str(entity["nbt"]["id"]) for entity in inhabited.entities
        if str(entity["nbt"]["id"]) in expected_animals
    )
    if derivative_animals != expected_animals:
        issues.append("damaged derivative does not preserve the mixed livestock program")

    return {
        "structure_id": "infinite_domain:trade_outpost_clean_master",
        "archetype": "palisaded caravan trade outpost with market, lodging and stocked paddocks",
        "door_nodes_checked": len(required_lower_doors),
        "clean_master_settlement_program": {
            "targets": len(program_targets), "reached": len(reached),
            "missing": [list(pos) for pos in missing],
        },
        "paddock_boundary_cells_checked": 2 * (2 * 13 + 2 * 9) * 2,
        "paddock_boundary_gaps": [list(pos) for pos in paddock_missing],
        "livestock": dict(animal_types),
        "damaged_survivor_routes": {
            "targets": len(program_targets), "reached": len(survivor_reached),
            "missing": [list(pos) for pos in survivor_missing],
        },
        "valid": not issues,
        "issues": issues,
        "note": "Program validation checks gatehouse, four distinct market stalls, lodge rooms, well, bunkhouse, both fully enclosed paddocks, mixed livestock and all required routes through the damaged inhabited derivative. It does not replace in-game inspection.",
    }


def validate_decayed_farm() -> dict[str, object]:
    template = decayed_farm_clean_master()
    issues: list[str] = []
    required_lower_doors = {
        # Farmhouse exterior and room thresholds.
        (10, 2, 3), (11, 2, 3), (16, 2, 19),
        (6, 2, 9), (12, 2, 9), (17, 2, 9),
        (10, 2, 6), (9, 2, 12), (14, 2, 12),
        # Barn wagon, tack/feed, aisle and stall thresholds.
        (36, 2, 3), (37, 2, 3), (36, 2, 25), (37, 2, 25),
        (33, 2, 9), (37, 2, 9), (41, 2, 9), (35, 2, 7), (39, 2, 7),
        (34, 2, 14), (40, 2, 14), (34, 2, 20), (40, 2, 20),
        # Silo and machinery shed.
        (24, 2, 6), (37, 2, 30), (38, 2, 30), (46, 2, 37), (42, 2, 36),
    }
    missing_doors = sorted(pos for pos in required_lower_doors if not (block_name(template, pos) or "").endswith("_door"))
    if missing_doors:
        issues.append(f"missing required lower doors at {missing_doors}")

    ground_targets = {
        # Farmhouse public and private rooms plus rear exit.
        (10, 2, 3), (6, 2, 6), (15, 2, 6), (6, 2, 13),
        (11, 2, 14), (16, 2, 13), (16, 2, 19),
        # Silo and complete barn workflow.
        (24, 2, 7), (24, 2, 8), (37, 2, 4), (32, 2, 6),
        (42, 2, 8), (37, 2, 12), (32, 2, 12), (42, 2, 12),
        (32, 2, 17), (42, 2, 17), (37, 2, 22), (37, 2, 25),
        # Fields, machinery lane and both shed rooms/exits.
        (20, 2, 28), (28, 2, 35), (38, 2, 31), (34, 2, 34),
        (44, 2, 38), (42, 2, 36), (46, 2, 37),
    }
    ground_reached = horizontally_reachable(template, (11, 2, 2), ground_targets)
    ground_missing = sorted(ground_targets - ground_reached)
    if ground_missing:
        issues.append(f"clean master has unreachable farm program points: {ground_missing}")

    loft_targets = {(30, 9, 17), (33, 9, 15), (33, 9, 22), (38, 9, 23), (41, 9, 12), (43, 9, 15)}
    loft_reached = horizontally_reachable(template, (30, 9, 17), loft_targets)
    loft_missing = sorted(loft_targets - loft_reached)
    if loft_missing:
        issues.append(f"clean master has unreachable hayloft points: {loft_missing}")

    stair_states = {
        y for (x, y, z), (state, _) in template.blocks.items()
        if template.palette[state]["Name"] == "minecraft:spruce_stairs" and x == 30 and 11 <= z <= 16
    }
    if stair_states != set(range(2, 8)):
        issues.append(f"hayloft stair does not span all six required rises: {sorted(stair_states)}")

    animal_types = Counter(
        str(entity["nbt"]["id"]) for entity in template.entities
        if str(entity["nbt"]["id"]) in {"minecraft:cow", "minecraft:sheep", "minecraft:pig"}
    )
    expected_animals = Counter({"minecraft:cow": 2, "minecraft:sheep": 1, "minecraft:pig": 1})
    if animal_types != expected_animals:
        issues.append(f"expected barn livestock {dict(expected_animals)}, found {dict(animal_types)}")

    ruined = decayed_farm()
    survivor_ground_targets = {
        (10, 2, 3), (15, 2, 6), (6, 2, 13), (11, 2, 14),
        (16, 2, 13), (16, 2, 19), (24, 2, 7), (37, 2, 4),
        (42, 2, 8), (37, 2, 12), (32, 2, 12), (32, 2, 17),
        (37, 2, 22), (37, 2, 25), (28, 2, 35), (38, 2, 31),
        (34, 2, 34), (44, 2, 38), (46, 2, 37),
    }
    survivor_ground_reached = horizontally_reachable(ruined, (11, 2, 2), survivor_ground_targets)
    survivor_ground_missing = sorted(survivor_ground_targets - survivor_ground_reached)
    if survivor_ground_missing:
        issues.append(f"decayed derivative breaks required ground routes: {survivor_ground_missing}")
    survivor_loft_targets = {(30, 9, 17), (33, 9, 15), (33, 9, 22)}
    survivor_loft_reached = horizontally_reachable(ruined, (30, 9, 17), survivor_loft_targets)
    survivor_loft_missing = sorted(survivor_loft_targets - survivor_loft_reached)
    if survivor_loft_missing:
        issues.append(f"decayed derivative breaks surviving southwest loft routes: {survivor_loft_missing}")

    spawner_count = sum(
        1 for state, _ in ruined.blocks.values()
        if ruined.palette[state]["Name"] == "minecraft:spawner"
    )
    if spawner_count != 2:
        issues.append(f"expected two distributed hostile spawners, found {spawner_count}")

    return {
        "structure_id": "infinite_domain:decayed_farm_clean_master",
        "archetype": "family farm with roomed farmhouse, aisle barn, silo, machinery shed and irrigated fields",
        "door_nodes_checked": len(required_lower_doors),
        "clean_master_ground_program": {
            "targets": len(ground_targets), "reached": len(ground_reached),
            "missing": [list(pos) for pos in ground_missing],
        },
        "clean_master_hayloft": {
            "targets": len(loft_targets), "reached": len(loft_reached),
            "missing": [list(pos) for pos in loft_missing],
        },
        "vertical_access": {"hayloft_stair_rises_present": sorted(stair_states)},
        "livestock": dict(animal_types),
        "decayed_survivor_ground_routes": {
            "targets": len(survivor_ground_targets), "reached": len(survivor_ground_reached),
            "missing": [list(pos) for pos in survivor_ground_missing],
        },
        "decayed_survivor_loft_routes": {
            "targets": len(survivor_loft_targets), "reached": len(survivor_loft_reached),
            "missing": [list(pos) for pos in survivor_loft_missing],
        },
        "hostile_spawners": spawner_count,
        "valid": not issues,
        "issues": issues,
        "note": "Program validation checks the farmhouse room plan, silo, complete barn ground program, traversable hayloft, field-to-machinery workflow, livestock, distributed danger and declared routes through the decayed derivative. It does not replace in-game inspection.",
    }


def validate_trailer_park() -> dict[str, object]:
    template = trailer_park_clean_master()
    issues: list[str] = []
    trailer_specs = ((4, 16, "east"), (4, 38, "east"), (4, 60, "east"), (56, 16, "west"), (56, 38, "west"), (56, 60, "west"))

    required_lower_doors = {
        # Management and communal laundry/maintenance.
        (40, 2, 7), (40, 2, 8), (56, 2, 13),
        (49, 2, 7), (56, 2, 7), (60, 2, 8),
        (26, 2, 7), (26, 2, 8), (12, 2, 13), (15, 2, 7),
    }
    for x, z, side in trailer_specs:
        required_lower_doors.update({
            (x + 8 if side == "east" else x, 2, z + 8),
            (x + 6, 2, z + 6),
            (x + 4, 2, z + 9),
            (x + 6, 2, z + 11),
        })
    missing_doors = sorted(pos for pos in required_lower_doors if not (block_name(template, pos) or "").endswith("_door"))
    if missing_doors:
        issues.append(f"missing required lower doors at {missing_doors}")

    shared_targets = {
        (40, 2, 7), (45, 2, 7), (52, 2, 7), (59, 2, 6),
        (60, 2, 11), (56, 2, 13),
        (26, 2, 7), (9, 2, 7), (20, 2, 9), (12, 2, 13),
        (29, 2, 73), (40, 2, 71),
    }
    trailer_targets: set[tuple[int, int, int]] = set()
    for x, z, side in trailer_specs:
        trailer_targets.update({
            (x + 8 if side == "east" else x, 2, z + 8),
            (x + 5, 2, z + 3),
            (x + 6, 2, z + 8),
            (x + 6, 2, z + 12),
        })
    all_targets = shared_targets | trailer_targets
    reached = horizontally_reachable(template, (34, 2, 1), all_targets)
    missing = sorted(all_targets - reached)
    if missing:
        issues.append(f"clean master has unreachable park program points: {missing}")

    # Every trailer must independently expose all four residential zones from
    # its own exterior doorway, preventing the site-wide flood fill from hiding
    # a sealed or accidentally interconnected mobile home.
    trailer_results: dict[str, dict[str, object]] = {}
    for index, (x, z, side) in enumerate(trailer_specs, start=1):
        entrance = (x + 8 if side == "east" else x, 2, z + 8)
        targets = {
            entrance, (x + 5, 2, z + 3),
            (x + 6, 2, z + 8), (x + 6, 2, z + 12),
        }
        local_reached = horizontally_reachable(template, entrance, targets)
        local_missing = sorted(targets - local_reached)
        if local_missing:
            issues.append(f"trailer {index} has unreachable residential zones: {local_missing}")
        trailer_results[str(index)] = {
            "targets": len(targets), "reached": len(local_reached),
            "missing": [list(pos) for pos in local_missing],
        }

    ruined = trailer_park()
    survivor_targets = set(shared_targets)
    for index, (x, z, side) in enumerate(trailer_specs, start=1):
        entrance = (x + 8 if side == "east" else x, 2, z + 8)
        living = (x + 5, 2, z + 3)
        hall = (x + 6, 2, z + 8)
        bedroom = (x + 6, 2, z + 12)
        survivor_targets.update({entrance, hall})
        if index != 1:
            survivor_targets.add(living)
        if index != 6:
            survivor_targets.add(bedroom)
    survivor_reached = horizontally_reachable(ruined, (34, 2, 1), survivor_targets)
    survivor_missing = sorted(survivor_targets - survivor_reached)
    if survivor_missing:
        issues.append(f"abandoned derivative breaks required park routes: {survivor_missing}")

    spawner_count = sum(
        1 for state, _ in ruined.blocks.values()
        if ruined.palette[state]["Name"] == "minecraft:spawner"
    )
    if spawner_count != 3:
        issues.append(f"expected three distributed hostile spawners, found {spawner_count}")

    return {
        "structure_id": "infinite_domain:trailer_park_clean_master",
        "archetype": "six-lot mobile-home park with branched road, management and shared services",
        "door_nodes_checked": len(required_lower_doors),
        "clean_master_park_program": {
            "targets": len(all_targets), "reached": len(reached),
            "missing": [list(pos) for pos in missing],
        },
        "individual_trailer_programs": trailer_results,
        "abandoned_survivor_routes": {
            "targets": len(survivor_targets), "reached": len(survivor_reached),
            "missing": [list(pos) for pos in survivor_missing],
        },
        "hostile_spawners": spawner_count,
        "valid": not issues,
        "issues": issues,
        "note": "Program validation checks management, shared laundry/maintenance, road-end utilities, all six independent living/kitchen-bath-bedroom programs and declared routes through the abandoned derivative. It does not replace in-game inspection.",
    }


def validate_mountain_military_complex() -> dict[str, object]:
    template = mountain_military_complex_clean_master()
    issues: list[str] = []
    required_lower_doors = {
        # Gatehouses and four watchtower bases.
        (22, 2, 10), (38, 2, 10),
        (8, 2, 6), (53, 2, 6), (8, 2, 55), (53, 2, 55),
        # Command ground and upper controlled thresholds.
        (14, 2, 13), (15, 2, 13), (10, 2, 20), (21, 2, 20), (16, 2, 25),
        (11, 9, 22), (21, 9, 22), (16, 9, 27),
        # Barracks, motor pool and armory/logistics.
        (44, 2, 13), (45, 2, 13), (40, 2, 19), (50, 2, 19),
        (45, 2, 16), (47, 2, 25),
        (36, 2, 46), (12, 2, 46), (22, 2, 46), (32, 2, 46),
        (17, 2, 49), (27, 2, 49),
        (40, 2, 44), (46, 2, 44), (47, 2, 44), (51, 2, 44),
    }
    missing_doors = sorted(pos for pos in required_lower_doors if not (block_name(template, pos) or "").endswith("_door"))
    if missing_doors:
        issues.append(f"missing required lower doors at {missing_doors}")

    ground_targets = {
        # Vehicle gate, gatehouses and tower bases.
        (30, 2, 8), (22, 2, 8), (38, 2, 8),
        (7, 2, 6), (54, 2, 6), (7, 2, 55), (54, 2, 55),
        # Command security, operations, communications and archive.
        (14, 2, 13), (10, 2, 16), (9, 2, 26), (20, 2, 24), (20, 2, 29),
        # Barracks duty/mess, infirmary, bunks and wash/locker wing.
        (44, 2, 14), (39, 2, 17), (50, 2, 16),
        (40, 2, 23), (40, 2, 29), (50, 2, 23), (50, 2, 29),
        # Motor bays and three rear service functions.
        (12, 2, 44), (21, 2, 44), (30, 2, 44),
        (12, 2, 49), (25, 2, 49), (32, 2, 49), (36, 2, 46),
        # Armory vestibule, quartermaster room, vault and central helipad.
        (40, 2, 44), (43, 2, 42), (50, 2, 40), (51, 2, 48),
        (30, 2, 25),
    }
    ground_reached = horizontally_reachable(template, (30, 2, 11), ground_targets)
    ground_missing = sorted(ground_targets - ground_reached)
    if ground_missing:
        issues.append(f"clean master has unreachable ground program points: {ground_missing}")

    upper_targets = {(22, 9, 28), (11, 9, 18), (10, 9, 26), (20, 9, 26)}
    upper_reached = horizontally_reachable(template, (22, 9, 28), upper_targets)
    upper_missing = sorted(upper_targets - upper_reached)
    if upper_missing:
        issues.append(f"clean master has unreachable command-level points: {upper_missing}")

    stair_states = {
        y for (x, y, z), (state, _) in template.blocks.items()
        if template.palette[state]["Name"] == "minecraft:polished_andesite_stairs" and x == 22 and 22 <= z <= 27
    }
    if stair_states != set(range(2, 8)):
        issues.append(f"command stair does not span all six required rises: {sorted(stair_states)}")
    comm_ladder = {
        y for (x, y, z), (state, _) in template.blocks.items()
        if template.palette[state]["Name"] == "minecraft:ladder" and x == 14 and z == 24
    }
    if comm_ladder != set(range(10, 20)):
        issues.append(f"communications-bridge ladder is incomplete: {sorted(comm_ladder)}")
    tower_ladders: dict[str, list[int]] = {}
    for label, x, z in (("nw", 4, 7), ("ne", 54, 7), ("sw", 4, 57), ("se", 54, 57)):
        levels = sorted(
            y for (px, y, pz), (state, _) in template.blocks.items()
            if template.palette[state]["Name"] == "minecraft:ladder" and px == x and pz == z
        )
        tower_ladders[label] = levels
        if set(levels) != set(range(2, 14)):
            issues.append(f"{label} watchtower ladder is incomplete: {levels}")

    occupied = mountain_military_complex()
    survivor_ground_targets = set(ground_targets) - {(12, 2, 44), (50, 2, 23), (50, 2, 29)}
    survivor_ground_reached = horizontally_reachable(occupied, (30, 2, 11), survivor_ground_targets)
    survivor_ground_missing = sorted(survivor_ground_targets - survivor_ground_reached)
    if survivor_ground_missing:
        issues.append(f"occupied derivative breaks required ground routes: {survivor_ground_missing}")
    survivor_upper_targets = {(22, 9, 28), (11, 9, 18), (10, 9, 26), (20, 9, 26)}
    survivor_upper_reached = horizontally_reachable(occupied, (22, 9, 28), survivor_upper_targets)
    survivor_upper_missing = sorted(survivor_upper_targets - survivor_upper_reached)
    if survivor_upper_missing:
        issues.append(f"occupied derivative breaks command-level routes: {survivor_upper_missing}")

    spawner_count = sum(
        1 for state, _ in occupied.blocks.values()
        if occupied.palette[state]["Name"] == "minecraft:spawner"
    )
    if spawner_count != 6:
        issues.append(f"expected six distributed pillager spawners, found {spawner_count}")

    return {
        "structure_id": "infinite_domain:mountain_military_complex_clean_master",
        "archetype": "fortified mountain garrison with command, barracks, motor pool and armory",
        "door_nodes_checked": len(required_lower_doors),
        "clean_master_ground_program": {
            "targets": len(ground_targets), "reached": len(ground_reached),
            "missing": [list(pos) for pos in ground_missing],
        },
        "clean_master_command_level": {
            "targets": len(upper_targets), "reached": len(upper_reached),
            "missing": [list(pos) for pos in upper_missing],
        },
        "vertical_access": {
            "command_stair_rises_present": sorted(stair_states),
            "communications_ladder_levels": sorted(comm_ladder),
            "watchtower_ladder_levels": tower_ladders,
        },
        "occupied_survivor_ground_routes": {
            "targets": len(survivor_ground_targets), "reached": len(survivor_ground_reached),
            "missing": [list(pos) for pos in survivor_ground_missing],
        },
        "occupied_survivor_command_routes": {
            "targets": len(survivor_upper_targets), "reached": len(survivor_upper_reached),
            "missing": [list(pos) for pos in survivor_upper_missing],
        },
        "pillager_spawners": spawner_count,
        "valid": not issues,
        "issues": issues,
        "note": "Program validation checks the guarded gate, tower bases/ladders, two command levels, barracks functions, three motor bays, rear service rooms, secure armory, all vertical access and declared routes through the damaged occupied derivative. It does not replace in-game inspection.",
    }


def validate_mountain_biohazard_lab() -> dict[str, object]:
    template = mountain_biohazard_lab_clean_master()
    issues: list[str] = []
    required_lower_doors = {
        # Wing connectors and intake pressure thresholds.
        (23, 2, 14), (24, 2, 14), (30, 2, 14), (31, 2, 14),
        (27, 2, 23), (16, 2, 39), (17, 2, 39),
        (26, 2, 3), (27, 2, 3), (22, 2, 9), (27, 2, 9), (32, 2, 9),
        (25, 2, 6), (30, 2, 6), (27, 2, 12),
        # West ground and upper research-room thresholds.
        (15, 2, 21), (15, 2, 34), (8, 2, 24), (20, 2, 24),
        (8, 2, 31), (20, 2, 31),
        (15, 9, 21), (15, 9, 34), (8, 9, 24), (20, 9, 24),
        (8, 9, 31), (20, 9, 31),
        # East controlled spine, cross-zones, cells and containment.
        (36, 2, 18), (36, 2, 26), (36, 2, 34), (36, 2, 40),
        (32, 2, 21), (42, 2, 21), (48, 2, 21),
        (32, 2, 29), (42, 2, 29), (48, 2, 29),
        (32, 2, 37), (42, 2, 37), (48, 2, 37),
        (42, 2, 16), (42, 2, 24), (43, 2, 31), (51, 2, 39),
        # Rear utility annex and independent emergency exit.
        (16, 2, 46), (17, 2, 46), (18, 2, 42),
    }
    missing_doors = sorted(pos for pos in required_lower_doors if not (block_name(template, pos) or "").endswith("_door"))
    if missing_doors:
        issues.append(f"missing required lower doors at {missing_doors}")

    ground_targets = {
        # Intake/security workflow.
        (26, 2, 3), (23, 2, 5), (28, 2, 7), (33, 2, 7),
        (22, 2, 12), (31, 2, 12),
        # West receiving, research, clinical and rear support.
        (10, 2, 18), (22, 2, 20), (8, 2, 27), (21, 2, 29),
        (8, 2, 35), (22, 2, 35), (17, 2, 39), (16, 2, 46),
        # East decon, quarantine, containment, waste and loading.
        (32, 2, 18), (32, 2, 26), (44, 2, 18), (44, 2, 26),
        (34, 2, 34), (45, 2, 33), (42, 2, 41), (51, 2, 39),
        (49, 2, 41),
        # Rear utilities and loading apron.
        (14, 2, 42), (20, 2, 45), (53, 2, 42),
    }
    ground_reached = horizontally_reachable(template, (27, 2, 2), ground_targets)
    ground_missing = sorted(ground_targets - ground_reached)
    if ground_missing:
        issues.append(f"clean master has unreachable ground program points: {ground_missing}")

    upper_targets = {
        (6, 9, 36), (23, 9, 36),
        (10, 9, 18), (24, 9, 20),
        (10, 9, 27), (24, 9, 29),
        (10, 9, 35), (20, 9, 35),
    }
    upper_reached = horizontally_reachable(template, (6, 9, 36), upper_targets)
    upper_missing = sorted(upper_targets - upper_reached)
    if upper_missing:
        issues.append(f"clean master has unreachable research-level points: {upper_missing}")

    stair_results: dict[str, list[int]] = {}
    for label, x in (("west_emergency", 6), ("east_primary", 23)):
        levels = sorted(
            y for (px, y, z), (state, _) in template.blocks.items()
            if template.palette[state]["Name"] == "minecraft:polished_andesite_stairs" and px == x and 30 <= z <= 35
        )
        stair_results[label] = levels
        if set(levels) != set(range(2, 8)):
            issues.append(f"{label} research stair is incomplete: {levels}")

    breached = mountain_biohazard_lab()
    survivor_ground_targets = set(ground_targets) - {(22, 2, 20), (45, 2, 33)}
    survivor_ground_reached = horizontally_reachable(breached, (27, 2, 2), survivor_ground_targets)
    survivor_ground_missing = sorted(survivor_ground_targets - survivor_ground_reached)
    if survivor_ground_missing:
        issues.append(f"breached derivative breaks required ground routes: {survivor_ground_missing}")
    survivor_upper_targets = set(upper_targets) - {(24, 9, 20)}
    survivor_upper_reached = horizontally_reachable(breached, (6, 9, 36), survivor_upper_targets)
    survivor_upper_missing = sorted(survivor_upper_targets - survivor_upper_reached)
    if survivor_upper_missing:
        issues.append(f"breached derivative breaks required research-level routes: {survivor_upper_missing}")

    spawner_count = sum(
        1 for state, _ in breached.blocks.values()
        if breached.palette[state]["Name"] == "minecraft:spawner"
    )
    if spawner_count != 5:
        issues.append(f"expected five distributed hostile spawners, found {spawner_count}")

    return {
        "structure_id": "infinite_domain:mountain_biohazard_lab_clean_master",
        "archetype": "pressure-zoned mountain research, quarantine and specimen-containment laboratory",
        "door_nodes_checked": len(required_lower_doors),
        "clean_master_ground_program": {
            "targets": len(ground_targets), "reached": len(ground_reached),
            "missing": [list(pos) for pos in ground_missing],
        },
        "clean_master_research_level": {
            "targets": len(upper_targets), "reached": len(upper_reached),
            "missing": [list(pos) for pos in upper_missing],
        },
        "vertical_access": {"research_stair_rises_present": stair_results},
        "breached_survivor_ground_routes": {
            "targets": len(survivor_ground_targets), "reached": len(survivor_ground_reached),
            "missing": [list(pos) for pos in survivor_ground_missing],
        },
        "breached_survivor_research_routes": {
            "targets": len(survivor_upper_targets), "reached": len(survivor_upper_reached),
            "missing": [list(pos) for pos in survivor_upper_missing],
        },
        "hostile_spawners": spawner_count,
        "valid": not issues,
        "issues": issues,
        "note": "Program validation checks sequential intake/decon, west clinical/research rooms, dual research-floor stairs, quarantine cells, specimen containment, waste/filtration, rear utilities and declared routes through the breached derivative. It does not replace in-game inspection.",
    }


def validate_decayed_logging_camp() -> dict[str, object]:
    template = decayed_logging_camp_clean_master()
    issues: list[str] = []
    required_lower_doors = {
        # Dispatch and administration.
        (20, 2, 10), (13, 2, 18), (12, 2, 10), (8, 2, 11), (16, 2, 11),
        # Mess, wash/locker and two bunk rooms.
        (23, 2, 29), (11, 2, 43), (12, 2, 43), (8, 2, 32), (19, 2, 32),
        (15, 2, 28), (13, 2, 37),
        # Three production cells, rear support rooms and service exit.
        (37, 2, 16), (47, 2, 16), (32, 2, 21), (42, 2, 21), (52, 2, 21),
        (57, 2, 24),
        # Garage repair floor, parts/fuel rooms and service exit.
        (57, 2, 45), (40, 2, 44), (50, 2, 44), (47, 2, 48),
    }
    missing_doors = sorted(pos for pos in required_lower_doors if not (block_name(template, pos) or "").endswith("_door"))
    if missing_doors:
        issues.append(f"missing required lower doors at {missing_doors}")

    ground_targets = {
        # Dispatch and crew support.
        (20, 2, 10), (8, 2, 8), (16, 2, 8), (8, 2, 14), (15, 2, 16), (13, 2, 18),
        (23, 2, 29), (8, 2, 27), (18, 2, 27), (8, 2, 35), (18, 2, 35),
        (8, 2, 40), (18, 2, 40), (11, 2, 43),
        # Infeed/debarking, primary saw, edging/sorting and rear support.
        (32, 2, 7), (34, 2, 15), (42, 2, 10), (45, 2, 16), (52, 2, 14),
        (32, 2, 24), (46, 2, 24), (52, 2, 24), (57, 2, 24),
        # Vehicle repair, parts/fuel and outside timber-handling yards.
        (45, 2, 38), (53, 2, 38), (50, 2, 40), (45, 2, 48), (52, 2, 47), (57, 2, 45),
        (24, 2, 30), (28, 2, 39), (32, 2, 46),
    }
    ground_reached = horizontally_reachable(template, (30, 2, 2), ground_targets)
    ground_missing = sorted(ground_targets - ground_reached)
    if ground_missing:
        issues.append(f"clean master has unreachable ground program points: {ground_missing}")

    catwalk_targets = {(30, 9, 24), (42, 9, 24), (54, 9, 24)}
    catwalk_reached = horizontally_reachable(template, (54, 9, 23), catwalk_targets)
    catwalk_missing = sorted(catwalk_targets - catwalk_reached)
    if catwalk_missing:
        issues.append(f"clean master has unreachable service-catwalk points: {catwalk_missing}")
    stair_states = {
        y for (x, y, z), (state, _) in template.blocks.items()
        if template.palette[state]["Name"] == "minecraft:polished_andesite_stairs" and x == 54 and 17 <= z <= 22
    }
    if stair_states != set(range(2, 8)):
        issues.append(f"service stair does not span all six required rises: {sorted(stair_states)}")

    abandoned = decayed_logging_camp()
    survivor_ground_targets = set(ground_targets) - {(8, 2, 35), (8, 2, 40), (52, 2, 14)}
    survivor_ground_reached = horizontally_reachable(abandoned, (30, 2, 2), survivor_ground_targets)
    survivor_ground_missing = sorted(survivor_ground_targets - survivor_ground_reached)
    if survivor_ground_missing:
        issues.append(f"abandoned derivative breaks required ground routes: {survivor_ground_missing}")
    survivor_catwalk_reached = horizontally_reachable(abandoned, (54, 9, 23), catwalk_targets)
    survivor_catwalk_missing = sorted(catwalk_targets - survivor_catwalk_reached)
    if survivor_catwalk_missing:
        issues.append(f"abandoned derivative breaks service-catwalk routes: {survivor_catwalk_missing}")

    spawner_count = sum(
        1 for state, _ in abandoned.blocks.values()
        if abandoned.palette[state]["Name"] == "minecraft:spawner"
    )
    if spawner_count != 4:
        issues.append(f"expected four distributed hostile spawners, found {spawner_count}")

    return {
        "structure_id": "infinite_domain:decayed_logging_camp_clean_master",
        "archetype": "forest timber camp with crew support, sawmill workflow, drying yard and vehicle maintenance",
        "door_nodes_checked": len(required_lower_doors),
        "clean_master_ground_program": {
            "targets": len(ground_targets), "reached": len(ground_reached),
            "missing": [list(pos) for pos in ground_missing],
        },
        "clean_master_service_catwalk": {
            "targets": len(catwalk_targets), "reached": len(catwalk_reached),
            "missing": [list(pos) for pos in catwalk_missing],
        },
        "vertical_access": {"service_stair_rises_present": sorted(stair_states)},
        "abandoned_survivor_ground_routes": {
            "targets": len(survivor_ground_targets), "reached": len(survivor_ground_reached),
            "missing": [list(pos) for pos in survivor_ground_missing],
        },
        "abandoned_survivor_catwalk_routes": {
            "targets": len(catwalk_targets), "reached": len(survivor_catwalk_reached),
            "missing": [list(pos) for pos in survivor_catwalk_missing],
        },
        "hostile_spawners": spawner_count,
        "valid": not issues,
        "issues": issues,
        "note": "Program validation checks dispatch, crew accommodation, the complete timber-production sequence, garage support, outside handling yards, catwalk access and declared routes through the abandoned derivative. It does not replace in-game inspection.",
    }


def validate_bombed_data_center() -> dict[str, object]:
    template = bombed_data_center_clean_master()
    issues: list[str] = []
    required_lower_doors = {
        # Public arrival, ground administration and paired hardened connectors.
        (12, 2, 6), (13, 2, 6), (12, 2, 11), (13, 2, 11),
        (14, 2, 18), (9, 2, 21), (18, 2, 21),
        (23, 2, 14), (24, 2, 14), (23, 2, 27), (24, 2, 27),
        # Upper administration and incident-command thresholds.
        (9, 9, 17), (18, 9, 17), (14, 9, 22),
        # Data-hall fire zones, central spine and paired rear thresholds.
        (33, 2, 14), (37, 2, 32), (29, 2, 23), (35, 2, 23), (42, 2, 23),
        (39, 2, 28),
        (29, 2, 40), (35, 2, 40), (42, 2, 40),
        (29, 2, 41), (35, 2, 41), (42, 2, 41),
        # Paired data-to-power thresholds, internal utility rooms and east exit.
        (46, 2, 14), (47, 2, 14), (46, 2, 27), (47, 2, 27),
        (46, 2, 35), (47, 2, 35), (52, 2, 18), (52, 2, 29), (58, 2, 35),
        # Rear receiving, maintenance, suppression/cooling and service exits.
        (36, 2, 46), (47, 2, 46), (28, 2, 50), (29, 2, 50),
        (40, 2, 50), (41, 2, 50), (58, 2, 46),
    }
    missing_doors = sorted(pos for pos in required_lower_doors if not (block_name(template, pos) or "").endswith("_door"))
    if missing_doors:
        issues.append(f"missing required lower doors at {missing_doors}")

    ground_targets = {
        # Security, staff support, network operations and records.
        (12, 2, 6), (8, 2, 8), (21, 2, 8), (12, 2, 14), (17, 2, 16),
        (10, 2, 24), (18, 2, 24), (23, 2, 14), (23, 2, 27),
        # Both server halls, central spine, meet-me room and media vault.
        (29, 2, 11), (29, 2, 30), (35, 2, 14), (35, 2, 30),
        (42, 2, 11), (42, 2, 32), (29, 2, 27), (40, 2, 28),
        # Switchgear, UPS, generators and east utility egress.
        (48, 2, 14), (50, 2, 20), (48, 2, 35), (58, 2, 35),
        # Receiving, maintenance, suppression, cooling and two service exits.
        (34, 2, 46), (37, 2, 46), (45, 2, 46), (49, 2, 46),
        (28, 2, 50), (40, 2, 50), (58, 2, 46),
    }
    ground_reached = horizontally_reachable(template, (12, 2, 5), ground_targets)
    ground_missing = sorted(ground_targets - ground_reached)
    if ground_missing:
        issues.append(f"clean master has unreachable ground program points: {ground_missing}")

    upper_targets = {(6, 9, 27), (8, 9, 12), (18, 9, 12), (12, 9, 20), (18, 9, 20), (18, 9, 24)}
    upper_reached = horizontally_reachable(template, (6, 9, 27), upper_targets)
    upper_missing = sorted(upper_targets - upper_reached)
    if upper_missing:
        issues.append(f"clean master has unreachable upper-administration points: {upper_missing}")
    stair_states = {
        y for (x, y, z), (state, _) in template.blocks.items()
        if template.palette[state]["Name"] == "minecraft:polished_andesite_stairs" and x == 6 and 21 <= z <= 26
    }
    if stair_states != set(range(2, 8)):
        issues.append(f"administration stair does not span all six required rises: {sorted(stair_states)}")

    bombed = bombed_data_center()
    survivor_ground_targets = {
        (12, 2, 6), (8, 2, 8), (21, 2, 8), (12, 2, 14), (17, 2, 16),
        (10, 2, 24), (18, 2, 24), (23, 2, 14), (23, 2, 27),
        (29, 2, 11), (29, 2, 30), (35, 2, 14), (35, 2, 30),
        (29, 2, 27), (34, 2, 46), (37, 2, 46), (28, 2, 50),
    }
    survivor_ground_reached = horizontally_reachable(bombed, (12, 2, 5), survivor_ground_targets)
    survivor_ground_missing = sorted(survivor_ground_targets - survivor_ground_reached)
    if survivor_ground_missing:
        issues.append(f"bombed derivative breaks required ground survivor routes: {survivor_ground_missing}")
    survivor_upper_reached = horizontally_reachable(bombed, (6, 9, 27), upper_targets)
    survivor_upper_missing = sorted(upper_targets - survivor_upper_reached)
    if survivor_upper_missing:
        issues.append(f"bombed derivative breaks upper-administration routes: {survivor_upper_missing}")

    spawner_count = sum(
        1 for state, _ in bombed.blocks.values()
        if bombed.palette[state]["Name"] == "minecraft:spawner"
    )
    if spawner_count != 5:
        issues.append(f"expected five distributed hostile spawners, found {spawner_count}")

    return {
        "structure_id": "infinite_domain:bombed_data_center_clean_master",
        "archetype": "hardened two-hall data campus with security, network operations, power, cooling and loading",
        "door_nodes_checked": len(required_lower_doors),
        "clean_master_ground_program": {"targets": len(ground_targets), "reached": len(ground_reached), "missing": [list(pos) for pos in ground_missing]},
        "clean_master_upper_administration": {"targets": len(upper_targets), "reached": len(upper_reached), "missing": [list(pos) for pos in upper_missing]},
        "vertical_access": {"administration_stair_rises_present": sorted(stair_states)},
        "bombed_survivor_ground_routes": {"targets": len(survivor_ground_targets), "reached": len(survivor_ground_reached), "missing": [list(pos) for pos in survivor_ground_missing]},
        "bombed_survivor_upper_routes": {"targets": len(upper_targets), "reached": len(survivor_upper_reached), "missing": [list(pos) for pos in survivor_upper_missing]},
        "hostile_spawners": spawner_count,
        "valid": not issues,
        "issues": issues,
        "note": "Program validation checks secure arrival, administration, network operations, twin data halls, power/UPS/generators, receiving, suppression, cooling, vertical access and declared survivor routes through the bombed derivative. It does not replace in-game inspection.",
    }


def validate_hydroelectric_refuge_dam() -> dict[str, object]:
    template = hydroelectric_refuge_dam_clean_master()
    issues: list[str] = []
    required_lower_doors = {
        # Powerhouse public/service thresholds and turbine/rear zoning.
        (31, 2, 4), (32, 2, 4), (16, 2, 20), (48, 2, 20),
        (22, 2, 10), (32, 2, 10), (42, 2, 10),
        (20, 2, 21), (28, 2, 21), (36, 2, 21), (44, 2, 21),
        # Crest control house.
        (31, 29, 29), (32, 29, 29), (41, 29, 35),
        (28, 29, 34), (37, 29, 34), (33, 29, 37),
        # West refuge intake, pressure threshold and emergency tunnel.
        (8, 3, 19), (9, 3, 19), (8, 3, 23), (9, 3, 23), (1, 3, 44),
        # East refuge intake, pressure threshold and emergency tunnel.
        (54, 3, 19), (55, 3, 19), (54, 3, 23), (55, 3, 23), (63, 3, 44),
    }
    missing_doors = sorted(pos for pos in required_lower_doors if not (block_name(template, pos) or "").endswith("_door"))
    if missing_doors:
        issues.append(f"missing required lower doors at {missing_doors}")

    powerhouse_targets = {
        (31, 2, 4), (18, 2, 7), (25, 2, 7), (37, 2, 7), (46, 2, 7),
        (22, 2, 10), (23, 2, 15), (31, 2, 15), (39, 2, 15), (47, 2, 15),
        (20, 2, 23), (28, 2, 23), (36, 2, 23), (44, 2, 23),
        (16, 2, 20), (48, 2, 20),
    }
    powerhouse_reached = horizontally_reachable(template, (31, 2, 3), powerhouse_targets)
    powerhouse_missing = sorted(powerhouse_targets - powerhouse_reached)
    if powerhouse_missing:
        issues.append(f"clean master has unreachable powerhouse points: {powerhouse_missing}")

    gallery_targets = {(18, 9, 19), (27, 9, 12), (40, 9, 12), (27, 9, 17), (46, 9, 17)}
    gallery_reached = horizontally_reachable(template, (18, 9, 19), gallery_targets)
    gallery_missing = sorted(gallery_targets - gallery_reached)
    if gallery_missing:
        issues.append(f"clean master has unreachable powerhouse-gallery points: {gallery_missing}")
    stair_states = {
        y for (x, y, z), (state, _) in template.blocks.items()
        if template.palette[state]["Name"] == "minecraft:polished_andesite_stairs" and x == 18 and 14 <= z <= 19
    }
    if stair_states != set(range(2, 8)):
        issues.append(f"powerhouse stair does not span all six required rises: {sorted(stair_states)}")

    control_targets = {(31, 29, 29), (30, 29, 31), (40, 29, 31), (28, 29, 37), (39, 29, 37), (41, 29, 35)}
    control_reached = horizontally_reachable(template, (31, 29, 28), control_targets)
    control_missing = sorted(control_targets - control_reached)
    if control_missing:
        issues.append(f"clean master has unreachable crest-control points: {control_missing}")

    refuge_specs = {
        "west": ((8, 3, 17), {(8, 3, 19), (8, 3, 23), (5, 3, 29), (5, 3, 40), (15, 3, 29), (12, 3, 45), (8, 3, 51), (1, 3, 44)}),
        "east": ((54, 3, 17), {(54, 3, 19), (54, 3, 23), (51, 3, 29), (51, 3, 40), (61, 3, 29), (58, 3, 45), (54, 3, 51), (63, 3, 44)}),
    }
    refuge_results: dict[str, dict[str, object]] = {}
    for label, (start, targets) in refuge_specs.items():
        reached = horizontally_reachable(template, start, targets)
        missing = sorted(targets - reached)
        if missing:
            issues.append(f"clean master {label} refuge has unreachable program points: {missing}")
        refuge_results[label] = {"targets": len(targets), "reached": len(reached), "missing": [list(pos) for pos in missing]}

    ladder_results: dict[str, list[int]] = {}
    for label, x in (("west", 15), ("east", 49)):
        levels = sorted(
            y for (px, y, z), (state, _) in template.blocks.items()
            if template.palette[state]["Name"] == "minecraft:ladder" and px == x and z == 34
        )
        ladder_results[label] = levels
        if set(levels) != set(range(3, 28)):
            issues.append(f"{label} refuge crest ladder is incomplete: {levels}")

    abandoned = hydroelectric_refuge_dam()
    survivor_powerhouse_targets = set(powerhouse_targets) - {(47, 2, 15), (44, 2, 23)}
    survivor_powerhouse_reached = horizontally_reachable(abandoned, (31, 2, 3), survivor_powerhouse_targets)
    survivor_powerhouse_missing = sorted(survivor_powerhouse_targets - survivor_powerhouse_reached)
    if survivor_powerhouse_missing:
        issues.append(f"abandoned derivative breaks powerhouse routes: {survivor_powerhouse_missing}")
    survivor_control_targets = {(31, 29, 29), (30, 29, 31), (28, 29, 37)}
    survivor_control_reached = horizontally_reachable(abandoned, (31, 29, 28), survivor_control_targets)
    survivor_control_missing = sorted(survivor_control_targets - survivor_control_reached)
    if survivor_control_missing:
        issues.append(f"abandoned derivative breaks crest-control routes: {survivor_control_missing}")
    survivor_refuges: dict[str, dict[str, object]] = {}
    for label, (start, targets) in refuge_specs.items():
        reached = horizontally_reachable(abandoned, start, targets)
        missing = sorted(targets - reached)
        if missing:
            issues.append(f"abandoned derivative breaks {label} refuge routes: {missing}")
        survivor_refuges[label] = {"targets": len(targets), "reached": len(reached), "missing": [list(pos) for pos in missing]}

    palette_counts = Counter(abandoned.palette[state]["Name"] for state, _ in abandoned.blocks.values())
    spawner_count = palette_counts["minecraft:spawner"]
    if spawner_count != 4:
        issues.append(f"expected four distributed hostile spawners, found {spawner_count}")
    if palette_counts["minecraft:water"] < 15000:
        issues.append(f"reservoir water volume is unexpectedly small: {palette_counts['minecraft:water']}")

    return {
        "structure_id": "infinite_domain:hydroelectric_refuge_dam_clean_master",
        "archetype": "water-retaining gravity dam with powerhouse, crest controls and twin planned refuge caverns",
        "door_nodes_checked": len(required_lower_doors),
        "clean_master_powerhouse": {"targets": len(powerhouse_targets), "reached": len(powerhouse_reached), "missing": [list(pos) for pos in powerhouse_missing]},
        "clean_master_gallery": {"targets": len(gallery_targets), "reached": len(gallery_reached), "missing": [list(pos) for pos in gallery_missing]},
        "clean_master_crest_control": {"targets": len(control_targets), "reached": len(control_reached), "missing": [list(pos) for pos in control_missing]},
        "clean_master_refuges": refuge_results,
        "vertical_access": {"powerhouse_stair_rises_present": sorted(stair_states), "refuge_crest_ladders": ladder_results},
        "abandoned_survivor_powerhouse": {"targets": len(survivor_powerhouse_targets), "reached": len(survivor_powerhouse_reached), "missing": [list(pos) for pos in survivor_powerhouse_missing]},
        "abandoned_survivor_control": {"targets": len(survivor_control_targets), "reached": len(survivor_control_reached), "missing": [list(pos) for pos in survivor_control_missing]},
        "abandoned_survivor_refuges": survivor_refuges,
        "reservoir_water_blocks": palette_counts["minecraft:water"],
        "hostile_spawners": spawner_count,
        "valid": not issues,
        "issues": issues,
        "note": "Program validation checks hydraulic mass, powerhouse operations, elevated gallery, crest controls, both multi-room refuges, emergency exits, crest ladders and declared routes through the abandoned derivative. It does not replace shoreline and terrain inspection in game.",
    }


def validate_toppled_skyscraper() -> dict[str, object]:
    template = toppled_skyscraper_clean_master()
    issues: list[str] = []
    office_levels = (10, 17, 24, 31)
    required_lower_doors = {
        # Podium exterior and internal service thresholds.
        (16, 2, 6), (17, 2, 6), (26, 2, 46), (27, 2, 46), (31, 2, 39),
        (12, 2, 13), (20, 2, 13), (27, 2, 13),
        (10, 2, 27), (18, 2, 27), (26, 2, 27), (15, 2, 20), (22, 2, 36),
        # Crown communications/mechanical thresholds.
        (17, 39, 30), (18, 39, 22),
    }
    for feet_y in office_levels:
        required_lower_doors.update({
            (14, feet_y, 15), (20, feet_y, 29),
            (11, feet_y, 34), (17, feet_y, 34), (24, feet_y, 34),
            (10, feet_y, 39), (25, feet_y, 39),
        })
    missing_doors = sorted(pos for pos in required_lower_doors if not (block_name(template, pos) or "").endswith("_door"))
    if missing_doors:
        issues.append(f"missing required lower doors at {missing_doors}")

    podium_targets = {
        (16, 2, 6), (10, 2, 9), (24, 2, 9),
        (13, 2, 20), (18, 2, 20), (26, 2, 20),
        (10, 2, 31), (18, 2, 33), (23, 2, 31),
        (10, 2, 40), (25, 2, 40), (26, 2, 46), (31, 2, 39),
    }
    podium_reached = horizontally_reachable(template, (16, 2, 5), podium_targets)
    podium_missing = sorted(podium_targets - podium_reached)
    if podium_missing:
        issues.append(f"clean master has unreachable podium points: {podium_missing}")

    floor_results: dict[str, dict[str, object]] = {}
    for index, feet_y in enumerate(office_levels, start=1):
        targets = {
            (17, feet_y, 11), (12, feet_y, 15), (22, feet_y, 15),
            (12, feet_y, 27), (22, feet_y, 27), (17, feet_y, 34),
            (10, feet_y, 39), (25, feet_y, 39),
        }
        reached = horizontally_reachable(template, (17, feet_y, 11), targets)
        missing = sorted(targets - reached)
        if missing:
            issues.append(f"clean master office level {index} has unreachable points: {missing}")
        floor_results[str(index)] = {"targets": len(targets), "reached": len(reached), "missing": [list(pos) for pos in missing]}

    crown_targets = {(17, 39, 30), (16, 39, 17), (21, 39, 22), (18, 39, 22)}
    crown_reached = horizontally_reachable(template, (17, 39, 30), crown_targets)
    crown_missing = sorted(crown_targets - crown_reached)
    if crown_missing:
        issues.append(f"clean master has unreachable crown points: {crown_missing}")

    ladder_results: dict[str, list[int]] = {}
    for label, x in (("west", 9), ("east", 26)):
        levels = sorted(
            y for (px, y, z), (state, _) in template.blocks.items()
            if template.palette[state]["Name"] == "minecraft:ladder" and px == x and z == 39
        )
        ladder_results[label] = levels
        if set(levels) != set(range(10, 43)):
            issues.append(f"{label} emergency ladder is incomplete: {levels}")

    toppled = toppled_skyscraper()
    survivor_podium_targets = set(podium_targets) - {(25, 2, 40), (26, 2, 46), (31, 2, 39)}
    survivor_podium_reached = horizontally_reachable(toppled, (16, 2, 5), survivor_podium_targets)
    survivor_podium_missing = sorted(survivor_podium_targets - survivor_podium_reached)
    if survivor_podium_missing:
        issues.append(f"toppled derivative breaks podium survivor routes: {survivor_podium_missing}")
    survivor_floor_results: dict[str, dict[str, object]] = {}
    for index, feet_y in enumerate((10, 17), start=1):
        targets = {(17, feet_y, 11), (12, feet_y, 15), (12, feet_y, 27), (17, feet_y, 34), (10, feet_y, 39)}
        reached = horizontally_reachable(toppled, (17, feet_y, 11), targets)
        missing = sorted(targets - reached)
        if missing:
            issues.append(f"toppled derivative breaks stump level {index} routes: {missing}")
        survivor_floor_results[str(index)] = {"targets": len(targets), "reached": len(reached), "missing": [list(pos) for pos in missing]}
    surviving_west_ladder = sorted(
        y for (x, y, z), (state, _) in toppled.blocks.items()
        if toppled.palette[state]["Name"] == "minecraft:ladder" and x == 9 and z == 39 and 10 <= y <= 22
    )
    if set(surviving_west_ladder) != set(range(10, 23)):
        issues.append(f"stump west ladder is incomplete: {surviving_west_ladder}")

    spawner_count = sum(1 for state, _ in toppled.blocks.values() if toppled.palette[state]["Name"] == "minecraft:spawner")
    if spawner_count != 3:
        issues.append(f"expected three distributed hostile spawners, found {spawner_count}")

    return {
        "structure_id": "infinite_domain:toppled_skyscraper_clean_master",
        "archetype": "six-level corporate office tower with public/service podium, twin emergency cores and roof crown",
        "door_nodes_checked": len(required_lower_doors),
        "clean_master_podium": {"targets": len(podium_targets), "reached": len(podium_reached), "missing": [list(pos) for pos in podium_missing]},
        "clean_master_office_levels": floor_results,
        "clean_master_crown": {"targets": len(crown_targets), "reached": len(crown_reached), "missing": [list(pos) for pos in crown_missing]},
        "vertical_access": {"emergency_ladders": ladder_results},
        "toppled_survivor_podium": {"targets": len(survivor_podium_targets), "reached": len(survivor_podium_reached), "missing": [list(pos) for pos in survivor_podium_missing]},
        "toppled_survivor_stump_levels": survivor_floor_results,
        "toppled_survivor_west_ladder": surviving_west_ladder,
        "hostile_spawners": spawner_count,
        "valid": not issues,
        "issues": issues,
        "note": "Program validation checks the podium, four complete office levels, crown, both full-height emergency cores and declared accessible stump routes after toppling. The fractured horizontal tower is additionally gated by rendered and in-game review.",
    }


def validate_blown_apartment_complex() -> dict[str, object]:
    template = blown_apartment_complex_clean_master()
    issues: list[str] = []
    floor_levels = (2, 9, 16, 23)
    required_lower_doors = {
        (29, 2, 5), (30, 2, 5), (29, 2, 47), (30, 2, 47),
        (30, 24, 13),
    }
    for feet_y in floor_levels:
        required_lower_doors.update({
            # Four apartment entries and gallery/core thresholds.
            (19, feet_y, 12), (19, feet_y, 40), (41, feet_y, 12), (41, feet_y, 40),
            (21, feet_y, 12), (39, feet_y, 12), (21, feet_y, 40), (39, feet_y, 40),
            # Living-to-private and bedroom-to-bath thresholds in every unit.
            (10, feet_y, 16), (13, feet_y, 21), (10, feet_y, 37), (13, feet_y, 32),
            (50, feet_y, 16), (49, feet_y, 21), (50, feet_y, 37), (49, feet_y, 32),
        })
    missing_doors = sorted(pos for pos in required_lower_doors if not (block_name(template, pos) or "").endswith("_door"))
    if missing_doors:
        issues.append(f"missing required lower doors at {missing_doors}")

    apartment_targets = {
        "west_north": {(19, 0, 12), (12, 0, 12), (7, 0, 10), (9, 0, 20), (16, 0, 21)},
        "west_south": {(19, 0, 40), (10, 0, 43), (9, 0, 43), (9, 0, 30), (16, 0, 34)},
        "east_north": {(41, 0, 12), (48, 0, 12), (53, 0, 10), (50, 0, 20), (44, 0, 21)},
        "east_south": {(41, 0, 40), (50, 0, 43), (53, 0, 43), (50, 0, 30), (44, 0, 34)},
    }
    clean_floor_results: dict[str, dict[str, object]] = {}
    for floor_index, feet_y in enumerate(floor_levels, start=1):
        targets = {(x, feet_y, z) for unit in apartment_targets.values() for x, _, z in unit}
        # Both public/core bands and the complete courtyard gallery ring.
        targets.update({(20, feet_y, 25), (40, feet_y, 25), (30, feet_y, 40)})
        targets.add((20, feet_y, 12) if feet_y == 23 else (30, feet_y, 12))
        reached = horizontally_reachable(template, (20, feet_y, 25), targets)
        missing = sorted(targets - reached)
        if missing:
            issues.append(f"clean master floor {floor_index} has unreachable residential points: {missing}")
        clean_floor_results[str(floor_index)] = {"targets": len(targets), "reached": len(reached), "missing": [list(pos) for pos in missing]}

    ground_shared_targets = {(29, 2, 5), (28, 2, 9), (33, 2, 9), (28, 2, 43), (32, 2, 43), (29, 2, 47)}
    ground_shared_reached = horizontally_reachable(template, (29, 2, 4), ground_shared_targets)
    ground_shared_missing = sorted(ground_shared_targets - ground_shared_reached)
    if ground_shared_missing:
        issues.append(f"clean master has unreachable shared-service points: {ground_shared_missing}")

    stair_results: dict[str, list[int]] = {}
    for label, x, z_min, z_max in (("north", 25, 6, 11), ("south", 35, 41, 46)):
        levels = sorted(
            y for (px, y, z), (state, _) in template.blocks.items()
            if template.palette[state]["Name"] == "minecraft:oak_stairs" and px == x and z_min <= z <= z_max
        )
        stair_results[label] = levels
        expected = set(range(2, 8)) | set(range(9, 15)) | set(range(16, 22))
        if set(levels) != expected:
            issues.append(f"{label} apartment stair stack is incomplete: {levels}")

    blown = blown_apartment_complex()
    survivor_floor_results: dict[str, dict[str, object]] = {}
    survivor_units = ("west_north", "west_south", "east_south")
    for floor_index, feet_y in enumerate(floor_levels, start=1):
        targets = {(x, feet_y, z) for name in survivor_units for x, _, z in apartment_targets[name]}
        targets.update({(20, feet_y, 25), (30, feet_y, 40)})
        reached = horizontally_reachable(blown, (20, feet_y, 25), targets)
        missing = sorted(targets - reached)
        if missing:
            issues.append(f"blown derivative floor {floor_index} breaks surviving apartments: {missing}")
        survivor_floor_results[str(floor_index)] = {"targets": len(targets), "reached": len(reached), "missing": [list(pos) for pos in missing]}

    blown_stairs: dict[str, list[int]] = {}
    for label, x, z_min, z_max in (("north", 25, 6, 11), ("south", 35, 41, 46)):
        levels = sorted(
            y for (px, y, z), (state, _) in blown.blocks.items()
            if blown.palette[state]["Name"] == "minecraft:oak_stairs" and px == x and z_min <= z <= z_max
        )
        blown_stairs[label] = levels
        expected = set(range(2, 8)) | set(range(9, 15)) | set(range(16, 22))
        if set(levels) != expected:
            issues.append(f"blown derivative damages the {label} stair stack: {levels}")

    palette_counts = Counter(blown.palette[state]["Name"] for state, _ in blown.blocks.values())
    spawner_count = palette_counts["minecraft:spawner"]
    if spawner_count != 4:
        issues.append(f"expected four distributed hostile spawners, found {spawner_count}")

    return {
        "structure_id": "infinite_domain:blown_apartment_complex_clean_master",
        "archetype": "four-storey courtyard apartment building with sixteen complete dwellings and dual stairs",
        "door_nodes_checked": len(required_lower_doors),
        "clean_master_floors": clean_floor_results,
        "clean_master_shared_services": {"targets": len(ground_shared_targets), "reached": len(ground_shared_reached), "missing": [list(pos) for pos in ground_shared_missing]},
        "vertical_access": {"clean_master_stair_stacks": stair_results, "blown_survivor_stair_stacks": blown_stairs},
        "blown_survivor_floors": survivor_floor_results,
        "hostile_spawners": spawner_count,
        "valid": not issues,
        "issues": issues,
        "note": "Program validation checks five functional zones in each of sixteen apartments, the courtyard gallery, shared services, dual stacked stairs and three surviving apartments on every blown-open floor. It does not replace in-game courtyard and collapse inspection.",
    }


def validate_ruined_mixed_use_block() -> dict[str, object]:
    template = ruined_mixed_use_block_clean_master()
    issues: list[str] = []
    residential_levels = (9, 16, 23)

    required_lower_doors = {
        # Four independent storefronts, residential lobby and rear deliveries.
        (10, 2, 5), (23, 2, 5), (28, 2, 5), (29, 2, 5),
        (36, 2, 5), (47, 2, 5),
        (10, 2, 39), (23, 2, 39), (29, 2, 39), (36, 2, 39), (47, 2, 39),
    }
    for service_z in (24, 32):
        required_lower_doors.update((x, 2, service_z) for x in (10, 23, 29, 36, 47))
    for feet_y in residential_levels:
        required_lower_doors.update({
            # Apartment entries off the cross-corridor.
            (27, feet_y, 14), (31, feet_y, 14),
            (27, feet_y, 30), (31, feet_y, 30),
            # Living/private-room thresholds in all four dwellings.
            (19, feet_y, 12), (10, feet_y, 14),
            (39, feet_y, 12), (48, feet_y, 14),
            (19, feet_y, 28), (10, feet_y, 30),
            (39, feet_y, 28), (48, feet_y, 30),
        })
    required_lower_doors.add((29, 30, 27))
    missing_doors = sorted(
        pos for pos in required_lower_doors
        if not (block_name(template, pos) or "").endswith("_door")
    )
    if missing_doors:
        issues.append(f"missing required mixed-use thresholds at {missing_doors}")

    ground_programs = {
        "diner": {
            (10, 2, 5), (10, 2, 6), (14, 2, 12), (14, 2, 20),
            (10, 2, 27), (14, 2, 35), (10, 2, 39),
        },
        "pharmacy": {
            (23, 2, 5), (23, 2, 9), (23, 2, 16), (23, 2, 23),
            (26, 2, 27), (26, 2, 35), (23, 2, 39),
        },
        "residential_lobby": {
            (28, 2, 5), (29, 2, 6), (29, 2, 13), (29, 2, 20),
            (29, 2, 30), (29, 2, 39),
        },
        "hardware_repair": {
            (36, 2, 5), (36, 2, 9), (36, 2, 14), (38, 2, 23),
            (38, 2, 27), (40, 2, 35), (36, 2, 39),
        },
        "laundromat": {
            (47, 2, 5), (47, 2, 8), (50, 2, 14), (50, 2, 20),
            (50, 2, 23), (51, 2, 27), (51, 2, 35), (47, 2, 39),
        },
    }
    ground_results: dict[str, dict[str, object]] = {}
    ground_starts = {
        "diner": (10, 2, 4),
        "pharmacy": (23, 2, 4),
        "residential_lobby": (28, 2, 4),
        "hardware_repair": (36, 2, 4),
        "laundromat": (47, 2, 4),
    }
    for label, targets in ground_programs.items():
        reached = horizontally_reachable(template, ground_starts[label], targets)
        missing = sorted(targets - reached)
        if missing:
            issues.append(f"clean master has unreachable {label} points: {missing}")
        ground_results[label] = {
            "targets": len(targets), "reached": len(reached),
            "missing": [list(pos) for pos in missing],
        }

    apartment_targets = {
        "northwest": {(27, 0, 14), (23, 0, 10), (23, 0, 16), (19, 0, 12), (15, 0, 10), (10, 0, 14), (8, 0, 8)},
        "northeast": {(31, 0, 14), (35, 0, 10), (35, 0, 16), (39, 0, 12), (43, 0, 10), (48, 0, 14), (51, 0, 8)},
        "southwest": {(27, 0, 30), (23, 0, 34), (23, 0, 27), (19, 0, 28), (15, 0, 34), (10, 0, 30), (8, 0, 36)},
        "southeast": {(31, 0, 30), (35, 0, 34), (35, 0, 27), (39, 0, 28), (43, 0, 34), (48, 0, 30), (51, 0, 36)},
    }
    clean_floor_results: dict[str, dict[str, object]] = {}
    for floor_index, feet_y in enumerate(residential_levels, start=1):
        targets = {
            (x, feet_y, z)
            for unit in apartment_targets.values()
            for x, _, z in unit
        }
        targets.update({(29, feet_y, 13), (29, feet_y, 22), (29, feet_y, 34)})
        start = (29, feet_y, 22)
        reached = horizontally_reachable(template, start, targets)
        missing = sorted(targets - reached)
        if missing:
            issues.append(f"clean master residential floor {floor_index} has unreachable points: {missing}")
        clean_floor_results[str(floor_index)] = {
            "targets": len(targets), "reached": len(reached),
            "missing": [list(pos) for pos in missing],
        }

    stair_results: dict[str, list[int]] = {}
    stair_specs = {
        "front": (7, 12, set(range(2, 8)) | set(range(9, 15)) | set(range(16, 22))),
        "rear": (32, 37, set(range(2, 8)) | set(range(9, 15)) | set(range(16, 22)) | set(range(23, 29))),
    }
    for label, (z_min, z_max, expected) in stair_specs.items():
        levels = sorted(
            y for (x, y, z), (state, _) in template.blocks.items()
            if template.palette[state]["Name"] == "minecraft:oak_stairs"
            and x == 29 and z_min <= z <= z_max
        )
        stair_results[label] = levels
        if set(levels) != expected:
            issues.append(f"{label} mixed-use stair stack is incomplete: {levels}")

    roof_targets = {(29, 30, 27), (24, 30, 29), (24, 30, 35), (29, 30, 35), (34, 30, 35)}
    roof_reached = horizontally_reachable(template, (29, 30, 26), roof_targets)
    roof_missing = sorted(roof_targets - roof_reached)
    if roof_missing:
        issues.append(f"clean master has unreachable roof-plant points: {roof_missing}")

    ruined = ruined_mixed_use_block()
    survivor_ground_programs = {
        "diner": ground_programs["diner"],
        "pharmacy": ground_programs["pharmacy"],
        "residential_lobby": ground_programs["residential_lobby"],
        "hardware_repair": {(36, 2, 5), (36, 2, 9), (36, 2, 14), (38, 2, 23), (38, 2, 27)},
    }
    survivor_ground_results: dict[str, dict[str, object]] = {}
    survivor_ground_missing_all: list[tuple[int, int, int]] = []
    for label, targets in survivor_ground_programs.items():
        reached = horizontally_reachable(ruined, ground_starts[label], targets)
        missing = sorted(targets - reached)
        survivor_ground_missing_all.extend(missing)
        if missing:
            issues.append(f"ruined derivative breaks surviving {label} program: {missing}")
        survivor_ground_results[label] = {
            "targets": len(targets), "reached": len(reached),
            "missing": [list(pos) for pos in missing],
        }

    survivor_floor_results: dict[str, dict[str, object]] = {}
    surviving_units = ("northwest", "northeast", "southwest")
    for floor_index, feet_y in enumerate(residential_levels, start=1):
        targets = {
            (x, feet_y, z)
            for name in surviving_units
            for x, _, z in apartment_targets[name]
        }
        targets.update({(29, feet_y, 13), (29, feet_y, 22), (29, feet_y, 34)})
        reached = horizontally_reachable(ruined, (29, feet_y, 22), targets)
        missing = sorted(targets - reached)
        if missing:
            issues.append(f"ruined derivative floor {floor_index} breaks surviving units: {missing}")
        survivor_floor_results[str(floor_index)] = {
            "targets": len(targets), "reached": len(reached),
            "missing": [list(pos) for pos in missing],
        }

    ruined_stairs: dict[str, list[int]] = {}
    for label, (z_min, z_max, expected) in stair_specs.items():
        levels = sorted(
            y for (x, y, z), (state, _) in ruined.blocks.items()
            if ruined.palette[state]["Name"] == "minecraft:oak_stairs"
            and x == 29 and z_min <= z <= z_max
        )
        ruined_stairs[label] = levels
        if set(levels) != expected:
            issues.append(f"ruined derivative damages the {label} stair stack: {levels}")

    spawner_count = sum(
        1 for state, _ in ruined.blocks.values()
        if ruined.palette[state]["Name"] == "minecraft:spawner"
    )
    if spawner_count != 4:
        issues.append(f"expected four distributed hostile spawners, found {spawner_count}")

    return {
        "structure_id": "infinite_domain:ruined_mixed_use_block_clean_master",
        "archetype": "four-storey mixed-use city block with four businesses, separate residential access and twelve apartments",
        "door_nodes_checked": len(required_lower_doors),
        "clean_master_ground_programs": ground_results,
        "clean_master_residential_floors": clean_floor_results,
        "clean_master_roof_plant": {
            "targets": len(roof_targets), "reached": len(roof_reached),
            "missing": [list(pos) for pos in roof_missing],
        },
        "vertical_access": {
            "clean_master_stair_stacks": stair_results,
            "ruined_survivor_stair_stacks": ruined_stairs,
        },
        "ruined_survivor_ground_programs": survivor_ground_results,
        "ruined_survivor_residential_floors": survivor_floor_results,
        "hostile_spawners": spawner_count,
        "valid": not issues,
        "issues": issues,
        "note": "Program validation checks four distinct businesses, the residential lobby, twelve apartments, two stair stacks, roof plant and declared survivor routes after the southeast corner collapse. It does not replace rendered and in-game inspection.",
    }


def validate_sunken_city_front() -> dict[str, object]:
    template = sunken_city_front_clean_master()
    issues: list[str] = []
    buildings = {
        "cafe_apartments": {"side": "west", "z1": 3, "z2": 25, "top": 25},
        "hardware_offices": {"side": "west", "z1": 28, "z2": 52, "top": 32},
        "pharmacy_clinic": {"side": "east", "z1": 3, "z2": 27, "top": 32},
        "post_bank_offices": {"side": "east", "z1": 30, "z2": 52, "top": 25},
    }

    required_lower_doors: set[tuple[int, int, int]] = set()
    building_layout: dict[str, dict[str, object]] = {}
    for label, spec in buildings.items():
        west = spec["side"] == "west"
        z1, z2, top = int(spec["z1"]), int(spec["z2"]), int(spec["top"])
        entry_z = (z1 + z2) // 2
        street_x, rear_x = (20, 2) if west else (40, 58)
        split_x = 12 if west else 48
        rear_door_x = 7 if west else 53
        stair_x = 5 if west else 55
        corridor_wall_x = 7 if west else 53
        private_x = 14 if west else 46
        upper_levels = [feet_y for feet_y in (12, 19, 26) if feet_y + 4 < top]
        required_lower_doors.update({
            (street_x, 5, entry_z), (rear_x, 5, entry_z + 3),
            (split_x, 5, entry_z - 3), (rear_door_x, 5, entry_z),
            (stair_x, 1, entry_z),
        })
        for feet_y in upper_levels:
            required_lower_doors.update({
                (corridor_wall_x, feet_y, z1 + 5),
                (corridor_wall_x, feet_y, z2 - 5),
                (private_x, feet_y, z1 + 7),
                (private_x, feet_y, z2 - 7),
            })
        building_layout[label] = {
            **spec,
            "entry_z": entry_z,
            "street_x": street_x,
            "rear_x": rear_x,
            "split_x": split_x,
            "rear_door_x": rear_door_x,
            "stair_x": stair_x,
            "corridor_wall_x": corridor_wall_x,
            "private_x": private_x,
            "upper_levels": upper_levels,
        }

    missing_doors = sorted(
        pos for pos in required_lower_doors
        if not (block_name(template, pos) or "").endswith("_door")
    )
    if missing_doors:
        issues.append(f"missing required intact-frontage thresholds at {missing_doors}")

    ground_results: dict[str, dict[str, object]] = {}
    ground_routes: dict[str, tuple[tuple[int, int, int], set[tuple[int, int, int]]]] = {}
    for label, layout in building_layout.items():
        west = layout["side"] == "west"
        z1, z2, entry_z = int(layout["z1"]), int(layout["z2"]), int(layout["entry_z"])
        street_x, rear_x = int(layout["street_x"]), int(layout["rear_x"])
        split_x, rear_door_x = int(layout["split_x"]), int(layout["rear_door_x"])
        if west:
            targets = {
                (street_x, 5, entry_z), (17, 5, entry_z - 3),
                (split_x, 5, entry_z - 3), (10, 5, entry_z - 3),
                (rear_door_x, 5, entry_z), (6, 5, entry_z + 2),
                (rear_x, 5, entry_z + 3),
            }
            start = (21, 5, entry_z)
        else:
            targets = {
                (street_x, 5, entry_z), (43, 5, entry_z - 3),
                (split_x, 5, entry_z - 3), (50, 5, entry_z - 3),
                (rear_door_x, 5, entry_z), (55, 5, entry_z + 2),
                (rear_x, 5, entry_z + 3),
            }
            start = (39, 5, entry_z)
        if label == "cafe_apartments":
            targets.discard((17, 5, entry_z - 3))
            targets.add((18, 5, entry_z - 2))
        elif label == "post_bank_offices":
            targets.discard((43, 5, entry_z - 3))
            targets.discard((50, 5, entry_z - 3))
            targets.update({(45, 5, entry_z - 4), (52, 5, entry_z + 1)})
        reached = horizontally_reachable(template, start, targets)
        missing = sorted(targets - reached)
        if missing:
            issues.append(f"clean master has unreachable {label} ground program: {missing}")
        ground_results[label] = {
            "targets": len(targets), "reached": len(reached),
            "missing": [list(pos) for pos in missing],
        }
        ground_routes[label] = (start, targets)

    basement_results: dict[str, dict[str, object]] = {}
    for label, layout in building_layout.items():
        west = layout["side"] == "west"
        z1, z2, entry_z = int(layout["z1"]), int(layout["z2"]), int(layout["entry_z"])
        stair_x = int(layout["stair_x"])
        targets = {
            (stair_x, 1, entry_z),
            ((8 if west else 52), 1, z1 + 3),
            ((8 if west else 52), 1, z2 - 3),
        }
        start = ((8 if west else 52), 1, z1 + 2)
        reached = horizontally_reachable(template, start, targets)
        missing = sorted(targets - reached)
        if missing:
            issues.append(f"clean master has unreachable {label} cellar points: {missing}")
        basement_results[label] = {
            "targets": len(targets), "reached": len(reached),
            "missing": [list(pos) for pos in missing],
        }

    upper_results: dict[str, dict[str, object]] = {}
    for label, layout in building_layout.items():
        west = layout["side"] == "west"
        z1, z2 = int(layout["z1"]), int(layout["z2"])
        corridor_wall_x = int(layout["corridor_wall_x"])
        private_x = int(layout["private_x"])
        stair_x = int(layout["stair_x"])
        for floor_index, feet_y in enumerate(layout["upper_levels"], start=1):
            targets = {
                (corridor_wall_x, feet_y, z1 + 5),
                (corridor_wall_x, feet_y, z2 - 5),
                (private_x, feet_y, z1 + 7),
                (private_x, feet_y, z2 - 7),
                ((10 if west else 50), feet_y, z1 + 3),
                ((18 if west else 42), feet_y, z1 + 9),
                ((10 if west else 50), feet_y, z2 - 8),
                ((18 if west else 42), feet_y, z2 - 3),
            }
            start = (stair_x, feet_y, z1 + 2)
            reached = horizontally_reachable(template, start, targets)
            missing = sorted(targets - reached)
            if missing:
                issues.append(f"clean master {label} upper floor {floor_index} has unreachable points: {missing}")
            upper_results[f"{label}:{floor_index}"] = {
                "targets": len(targets), "reached": len(reached),
                "missing": [list(pos) for pos in missing],
            }

    stair_results: dict[str, dict[str, list[int]]] = {}
    for label, layout in building_layout.items():
        z1, top = int(layout["z1"]), int(layout["top"])
        stair_x = int(layout["stair_x"])
        basement_levels = sorted(
            y for (x, y, z), (state, _) in template.blocks.items()
            if template.palette[state]["Name"] == "minecraft:polished_andesite_stairs"
            and x == stair_x and z1 + 3 <= z <= z1 + 6
        )
        upper_levels = sorted(
            y for (x, y, z), (state, _) in template.blocks.items()
            if template.palette[state]["Name"] == "minecraft:oak_stairs"
            and x == stair_x and z1 + 3 <= z <= z1 + 8
        )
        expected_upper = set(range(5, 11)) | set(range(12, 18))
        if top == 32:
            expected_upper |= set(range(19, 25))
        if set(basement_levels) != set(range(1, 5)):
            issues.append(f"{label} cellar stair is incomplete: {basement_levels}")
        if set(upper_levels) != expected_upper:
            issues.append(f"{label} upper stair stack is incomplete: {upper_levels}")
        stair_results[label] = {"cellar": basement_levels, "upper": upper_levels}

    ruined = sunken_city_front()
    survivor_ground_results: dict[str, dict[str, object]] = {}
    for label, (start, targets) in ground_routes.items():
        reached = horizontally_reachable(ruined, start, targets)
        missing = sorted(targets - reached)
        if missing:
            issues.append(f"sunken derivative breaks surviving {label} ground program: {missing}")
        survivor_ground_results[label] = {
            "targets": len(targets), "reached": len(reached),
            "missing": [list(pos) for pos in missing],
        }

    survivor_upper_results: dict[str, dict[str, object]] = {}
    for label, layout in building_layout.items():
        west = layout["side"] == "west"
        z1, z2 = int(layout["z1"]), int(layout["z2"])
        corridor_wall_x = int(layout["corridor_wall_x"])
        private_x = int(layout["private_x"])
        stair_x = int(layout["stair_x"])
        preserve_south = label == "pharmacy_clinic"
        for floor_index, feet_y in enumerate(layout["upper_levels"], start=1):
            if preserve_south:
                targets = {
                    (corridor_wall_x, feet_y, z2 - 5),
                    (private_x, feet_y, z2 - 7),
                    ((10 if west else 50), feet_y, z2 - 8),
                    ((18 if west else 42), feet_y, z2 - 3),
                }
            else:
                targets = {
                    (corridor_wall_x, feet_y, z1 + 5),
                    (private_x, feet_y, z1 + 7),
                    ((10 if west else 50), feet_y, z1 + 3),
                    ((18 if west else 42), feet_y, z1 + 9),
                }
            start = (stair_x, feet_y, z1 + 2)
            reached = horizontally_reachable(ruined, start, targets)
            missing = sorted(targets - reached)
            if missing:
                issues.append(f"sunken derivative breaks {label} survivor floor {floor_index}: {missing}")
            survivor_upper_results[f"{label}:{floor_index}"] = {
                "targets": len(targets), "reached": len(reached),
                "missing": [list(pos) for pos in missing],
            }

    ruined_stairs: dict[str, dict[str, list[int]]] = {}
    for label, layout in building_layout.items():
        z1, top = int(layout["z1"]), int(layout["top"])
        stair_x = int(layout["stair_x"])
        basement_levels = sorted(
            y for (x, y, z), (state, _) in ruined.blocks.items()
            if ruined.palette[state]["Name"] == "minecraft:polished_andesite_stairs"
            and x == stair_x and z1 + 3 <= z <= z1 + 6
        )
        upper_levels = sorted(
            y for (x, y, z), (state, _) in ruined.blocks.items()
            if ruined.palette[state]["Name"] == "minecraft:oak_stairs"
            and x == stair_x and z1 + 3 <= z <= z1 + 8
        )
        expected_upper = set(range(5, 11)) | set(range(12, 18))
        if top == 32:
            expected_upper |= set(range(19, 25))
        if set(basement_levels) != set(range(1, 5)) or set(upper_levels) != expected_upper:
            issues.append(f"sunken derivative damages {label} vertical access")
        ruined_stairs[label] = {"cellar": basement_levels, "upper": upper_levels}

    # Each subsided road edge must descend from city grade to the Y=1 roadbed.
    road_edge_heights = {
        x: max(y for (px, y, z), (state, _) in ruined.blocks.items() if px == x and z == 0 and ruined.palette[state]["Name"] in {"minecraft:coarse_dirt", "minecraft:gravel"})
        for x in (21, 22, 23, 24, 25, 35, 36, 37, 38, 39)
    }
    if min(road_edge_heights.values()) != 1 or max(road_edge_heights.values()) != 4:
        issues.append(f"subsidence feathering does not span roadbed Y=1 to city grade Y=4: {road_edge_heights}")

    spawner_count = sum(
        1 for state, _ in ruined.blocks.values()
        if ruined.palette[state]["Name"] == "minecraft:spawner"
    )
    if spawner_count != 4:
        issues.append(f"expected four distributed hostile spawners, found {spawner_count}")

    return {
        "structure_id": "infinite_domain:sunken_city_front_clean_master",
        "archetype": "four-building avenue frontage with furnished cellars, mixed ground uses and apartment/office floors",
        "door_nodes_checked": len(required_lower_doors),
        "clean_master_ground_programs": ground_results,
        "clean_master_cellars": basement_results,
        "clean_master_upper_floors": upper_results,
        "sunken_survivor_ground_programs": survivor_ground_results,
        "sunken_survivor_upper_floors": survivor_upper_results,
        "vertical_access": {"clean_master": stair_results, "sunken_derivative": ruined_stairs},
        "subsidence_edge_heights": road_edge_heights,
        "hostile_spawners": spawner_count,
        "valid": not issues,
        "issues": issues,
        "note": "Program validation checks four different street premises, their furnished cellars, all upper suites, every stair stack, three-block road subsidence and distributed occupation. Rendered and in-game review remain required for collapse readability and terrain feathering.",
    }


def validate_pancaked_parking_structure() -> dict[str, object]:
    template = pancaked_parking_structure_clean_master()
    issues: list[str] = []
    feet_levels = (2, 9, 16, 23, 30)
    required_lower_doors = {
        (35, 2, 10), (40, 2, 12),
        (35, 2, 39), (35, 2, 40),
        (7, 2, 45), (8, 2, 45),
        (47, 2, 16), (48, 2, 16),
        (34, 30, 40),
    }
    for feet_y in feet_levels:
        required_lower_doors.update({(11, feet_y, 40), (45, feet_y, 22)})
    missing_doors = sorted(
        pos for pos in required_lower_doors
        if not (block_name(template, pos) or "").endswith("_door")
    )
    if missing_doors:
        issues.append(f"missing required parking-garage thresholds at {missing_doors}")

    ground_targets = {
        (8, 2, 4), (17, 2, 4),
        (35, 2, 10), (38, 2, 10), (40, 2, 12), (42, 2, 12),
        (35, 2, 39), (35, 2, 40), (39, 2, 40),
        (11, 2, 40), (45, 2, 22),
    }
    ground_reached = horizontally_reachable(template, (8, 2, 3), ground_targets)
    ground_missing = sorted(ground_targets - ground_reached)
    if ground_missing:
        issues.append(f"clean master has unreachable ground/service points: {ground_missing}")

    deck_results: dict[str, dict[str, object]] = {}
    for index, feet_y in enumerate(feet_levels, start=1):
        targets = {
            (11, feet_y, 40),
            (17, feet_y, 10), (17, feet_y, 25), (17, feet_y, 40),
            (22, feet_y, 7), (22, feet_y, 20),
            (31, feet_y, 10), (31, feet_y, 20), (31, feet_y, 40),
            (45, feet_y, 22),
        }
        if feet_y == 30:
            targets.add((34, 30, 40))
        reached = horizontally_reachable(template, (11, feet_y, 40), targets)
        missing = sorted(targets - reached)
        if missing:
            issues.append(f"clean master parking deck {index} has unreachable points: {missing}")
        deck_results[str(index)] = {
            "targets": len(targets), "reached": len(reached),
            "missing": [list(pos) for pos in missing],
        }

    stair_results: dict[str, list[int]] = {}
    expected_stairs = set(range(2, 8)) | set(range(9, 15)) | set(range(16, 22)) | set(range(23, 29))
    for label, x, z1, z2 in (("northwest", 8, 36, 41), ("southeast", 48, 18, 23)):
        levels = sorted(
            y for (px, y, z), (state, _) in template.blocks.items()
            if template.palette[state]["Name"] == "minecraft:polished_andesite_stairs"
            and px == x and z1 <= z <= z2
        )
        stair_results[label] = levels
        if set(levels) != expected_stairs:
            issues.append(f"{label} parking stair stack is incomplete: {levels}")

    ramp_points = {
        (25, base_y + run // 2, 7 + run)
        for base_y in (1, 8, 15, 22)
        for run in range(14)
    }
    missing_ramp = sorted(
        pos for pos in ramp_points
        if block_name(template, pos) != "minecraft:smooth_stone"
    )
    if missing_ramp:
        issues.append(f"vehicle-ramp stack is incomplete at {missing_ramp}")

    clean_counts = Counter(template.palette[state]["Name"] for state, _ in template.blocks.values())
    parked_vehicle_blocks = sum(clean_counts[name] for name in (
        "minecraft:red_terracotta", "minecraft:blue_terracotta", "minecraft:yellow_terracotta",
        "minecraft:oxidized_copper", "minecraft:white_terracotta", "minecraft:green_terracotta",
        "minecraft:orange_terracotta", "minecraft:cyan_terracotta",
    ))
    if parked_vehicle_blocks < 250:
        issues.append(f"garage has insufficient visible parked-vehicle mass: {parked_vehicle_blocks} blocks")

    pancaked = pancaked_parking_structure()
    survivor_deck_results: dict[str, dict[str, object]] = {}
    for index, feet_y in enumerate(feet_levels, start=1):
        targets = {
            (11, feet_y, 40),
            (17, feet_y, 10), (17, feet_y, 25), (17, feet_y, 40),
            (22, feet_y, 7), (22, feet_y, 20),
        }
        reached = horizontally_reachable(pancaked, (11, feet_y, 40), targets)
        missing = sorted(targets - reached)
        if missing:
            issues.append(f"pancaked derivative breaks survivor deck {index}: {missing}")
        survivor_deck_results[str(index)] = {
            "targets": len(targets), "reached": len(reached),
            "missing": [list(pos) for pos in missing],
        }
    surviving_northwest_stairs = sorted(
        y for (x, y, z), (state, _) in pancaked.blocks.items()
        if pancaked.palette[state]["Name"] == "minecraft:polished_andesite_stairs"
        and x == 8 and 36 <= z <= 41
    )
    if set(surviving_northwest_stairs) != expected_stairs:
        issues.append(f"pancaked derivative damages northwest escape stair: {surviving_northwest_stairs}")

    fallen_deck_levels = {
        y for (x, y, z), (state, _) in pancaked.blocks.items()
        if x >= 30 and z >= 22 and pancaked.palette[state]["Name"] == "minecraft:smooth_stone"
        and y in {9, 12, 15, 18}
    }
    if fallen_deck_levels != {9, 12, 15, 18}:
        issues.append(f"progressive-collapse deck stack is incomplete: {sorted(fallen_deck_levels)}")

    spawner_count = sum(
        1 for state, _ in pancaked.blocks.values()
        if pancaked.palette[state]["Name"] == "minecraft:spawner"
    )
    if spawner_count != 4:
        issues.append(f"expected four distributed hostile spawners, found {spawner_count}")

    return {
        "structure_id": "infinite_domain:pancaked_parking_structure_clean_master",
        "archetype": "five-deck municipal parking garage with vehicle ramp, dual stairs, security and maintenance",
        "door_nodes_checked": len(required_lower_doors),
        "clean_master_ground_services": {
            "targets": len(ground_targets), "reached": len(ground_reached),
            "missing": [list(pos) for pos in ground_missing],
        },
        "clean_master_parking_decks": deck_results,
        "vertical_access": {
            "clean_master_stairs": stair_results,
            "surviving_northwest_stairs": surviving_northwest_stairs,
            "vehicle_ramp_points": len(ramp_points),
            "missing_vehicle_ramp_points": [list(pos) for pos in missing_ramp],
        },
        "parked_vehicle_blocks": parked_vehicle_blocks,
        "pancaked_survivor_decks": survivor_deck_results,
        "fallen_deck_levels": sorted(fallen_deck_levels),
        "hostile_spawners": spawner_count,
        "valid": not issues,
        "issues": issues,
        "note": "Program validation checks entry control, security, maintenance, five complete decks, dual pedestrian cores, a four-flight vehicle ramp, parked vehicles and the surviving western circulation after eastern deck pancaking. Rendered and in-game collapse inspection remain required.",
    }


def validate_cratered_downtown_intersection() -> dict[str, object]:
    template = cratered_downtown_intersection_clean_master()
    issues: list[str] = []
    buildings = {
        "bank_offices": {"x1": 2, "z1": 2, "x2": 23, "z2": 23, "top": 26, "street_x": 23, "street_z": 23, "start": (24, 6, 12)},
        "pharmacy_housing": {"x1": 41, "z1": 2, "x2": 62, "z2": 23, "top": 33, "street_x": 41, "street_z": 23, "start": (40, 6, 12)},
        "diner_apartments": {"x1": 2, "z1": 41, "x2": 23, "z2": 62, "top": 26, "street_x": 23, "street_z": 41, "start": (24, 6, 51)},
        "electronics_offices": {"x1": 41, "z1": 41, "x2": 62, "z2": 62, "top": 33, "street_x": 41, "street_z": 41, "start": (40, 6, 51)},
    }
    required_lower_doors: set[tuple[int, int, int]] = {(16, 7, 18)}
    layout: dict[str, dict[str, object]] = {}
    for label, spec in buildings.items():
        x1, z1, x2, z2, top = (int(spec[key]) for key in ("x1", "z1", "x2", "z2", "top"))
        xmid, zmid = (x1 + x2) // 2, (z1 + z2) // 2
        upper_levels = [feet_y for feet_y in (13, 20, 27) if feet_y + 4 < top]
        required_lower_doors.update({
            (int(spec["street_x"]), 6, zmid),
            (xmid, 6, int(spec["street_z"])),
        })
        for feet_y in (6, *upper_levels):
            required_lower_doors.update({
                (xmid - 2, feet_y, zmid - 6), (xmid - 2, feet_y, zmid + 6),
                (xmid + 2, feet_y, zmid - 6), (xmid + 2, feet_y, zmid + 6),
                (xmid - 6, feet_y, zmid - 2), (xmid + 6, feet_y, zmid - 2),
                (xmid - 6, feet_y, zmid + 2), (xmid + 6, feet_y, zmid + 2),
            })
        layout[label] = {**spec, "xmid": xmid, "zmid": zmid, "upper_levels": upper_levels}

    missing_doors = sorted(
        pos for pos in required_lower_doors
        if not (block_name(template, pos) or "").endswith("_door")
    )
    if missing_doors:
        issues.append(f"missing required intersection-building thresholds at {missing_doors}")

    ground_room_points = {
        "bank_offices": {(8, 6, 8), (18, 6, 8), (8, 6, 20), (18, 6, 15)},
        "pharmacy_housing": {(45, 6, 9), (57, 6, 9), (45, 6, 21), (57, 6, 21)},
        "diner_apartments": {(8, 6, 45), (18, 6, 45), (8, 6, 54), (18, 6, 58)},
        "electronics_offices": {(45, 6, 53), (57, 6, 45), (45, 6, 59), (57, 6, 53)},
    }
    ground_results: dict[str, dict[str, object]] = {}
    for label, spec in layout.items():
        xmid, zmid = int(spec["xmid"]), int(spec["zmid"])
        targets = set(ground_room_points[label])
        targets.update({(int(spec["street_x"]), 6, zmid), (xmid, 6, int(spec["street_z"])), (xmid, 6, zmid)})
        reached = horizontally_reachable(template, spec["start"], targets)
        missing = sorted(targets - reached)
        if missing:
            issues.append(f"clean master has unreachable {label} ground program: {missing}")
        ground_results[label] = {
            "targets": len(targets), "reached": len(reached),
            "missing": [list(pos) for pos in missing],
        }

    upper_results: dict[str, dict[str, object]] = {}
    for label, spec in layout.items():
        x1, z1, x2, z2 = (int(spec[key]) for key in ("x1", "z1", "x2", "z2"))
        xmid, zmid = int(spec["xmid"]), int(spec["zmid"])
        for floor_index, feet_y in enumerate(spec["upper_levels"], start=1):
            targets = {
                (xmid, feet_y, zmid),
                (x1 + 7, feet_y, z1 + 7), (x2 - 7, feet_y, z1 + 7),
                (x1 + 7, feet_y, z2 - 7), (x2 - 7, feet_y, z2 - 7),
                (xmid - 2, feet_y, zmid - 6), (xmid + 2, feet_y, zmid + 6),
                (xmid - 6, feet_y, zmid - 2), (xmid + 6, feet_y, zmid + 2),
            }
            occupied_replacements = {
                "bank_offices": ((x2 - 7, z2 - 7), (18, 16)),
                "pharmacy_housing": ((x1 + 7, z1 + 7), (46, 9)),
                "diner_apartments": ((x1 + 7, z1 + 7), (8, 47)),
                "electronics_offices": ((x2 - 7, z2 - 7), (57, 55)),
            }
            old_point, new_point = occupied_replacements[label]
            targets.discard((old_point[0], feet_y, old_point[1]))
            targets.add((new_point[0], feet_y, new_point[1]))
            reached = horizontally_reachable(template, (xmid, feet_y, zmid), targets)
            missing = sorted(targets - reached)
            if missing:
                issues.append(f"clean master {label} upper floor {floor_index} has unreachable points: {missing}")
            upper_results[f"{label}:{floor_index}"] = {
                "targets": len(targets), "reached": len(reached),
                "missing": [list(pos) for pos in missing],
            }

    stair_results: dict[str, dict[str, list[int]]] = {}
    for label, spec in layout.items():
        xmid, z1, top = int(spec["xmid"]), int(spec["z1"]), int(spec["top"])
        cellar = sorted(
            y for (x, y, z), (state, _) in template.blocks.items()
            if template.palette[state]["Name"] == "minecraft:polished_andesite_stairs"
            and x == xmid and z1 + 3 <= z <= z1 + 7
        )
        upper = sorted(
            y for (x, y, z), (state, _) in template.blocks.items()
            if template.palette[state]["Name"] == "minecraft:oak_stairs"
            and x == xmid and z1 + 3 <= z <= z1 + 8
        )
        expected_upper = set(range(6, 12)) | set(range(13, 19))
        if top == 33:
            expected_upper |= set(range(20, 26))
        if set(cellar) != set(range(1, 6)):
            issues.append(f"{label} cellar stair is incomplete: {cellar}")
        if set(upper) != expected_upper:
            issues.append(f"{label} upper stair stack is incomplete: {upper}")
        stair_results[label] = {"cellar": cellar, "upper": upper}

    utility_targets = {(32, 1, 20), (32, 1, 31), (20, 1, 32), (44, 1, 32), (32, 1, 44)}
    utility_reached = horizontally_reachable(template, (31, 1, 14), utility_targets)
    utility_missing = sorted(utility_targets - utility_reached)
    if utility_missing:
        issues.append(f"clean master has unreachable underground utility points: {utility_missing}")
    ladder_results: dict[str, list[int]] = {}
    for label, x, z in (("north", 30, 14), ("south", 34, 50), ("west", 14, 30), ("east", 50, 34)):
        levels = sorted(
            y for (px, y, pz), (state, _) in template.blocks.items()
            if template.palette[state]["Name"] == "minecraft:ladder" and px == x and pz == z
        )
        ladder_results[label] = levels
        if set(levels) != set(range(1, 6)):
            issues.append(f"{label} utility ladder is incomplete: {levels}")

    cratered = cratered_downtown_intersection()
    survivor_results: dict[str, dict[str, object]] = {}
    outer_targets = {
        "bank_offices": (9, 9),
        "pharmacy_housing": (56, 8),
        "diner_apartments": (8, 56),
        "electronics_offices": (54, 54),
    }
    for label, spec in layout.items():
        xmid, zmid = int(spec["xmid"]), int(spec["zmid"])
        target_x, target_z = outer_targets[label]
        for floor_index, feet_y in enumerate((6, *spec["upper_levels"]), start=0):
            targets = {(xmid, feet_y, zmid), (target_x, feet_y, target_z)}
            reached = horizontally_reachable(cratered, (xmid, feet_y, zmid), targets)
            missing = sorted(targets - reached)
            if missing:
                issues.append(f"cratered derivative breaks {label} survivor level {floor_index}: {missing}")
            survivor_results[f"{label}:{floor_index}"] = {
                "targets": len(targets), "reached": len(reached),
                "missing": [list(pos) for pos in missing],
            }

    survivor_stairs: dict[str, dict[str, list[int]]] = {}
    for label, spec in layout.items():
        xmid, z1, top = int(spec["xmid"]), int(spec["z1"]), int(spec["top"])
        cellar = sorted(
            y for (x, y, z), (state, _) in cratered.blocks.items()
            if cratered.palette[state]["Name"] == "minecraft:polished_andesite_stairs"
            and x == xmid and z1 + 3 <= z <= z1 + 7
        )
        upper = sorted(
            y for (x, y, z), (state, _) in cratered.blocks.items()
            if cratered.palette[state]["Name"] == "minecraft:oak_stairs"
            and x == xmid and z1 + 3 <= z <= z1 + 8
        )
        expected_upper = set(range(6, 12)) | set(range(13, 19))
        if top == 33:
            expected_upper |= set(range(20, 26))
        if set(cellar) != set(range(1, 6)) or set(upper) != expected_upper:
            issues.append(f"cratered derivative damages {label} stair spine")
        survivor_stairs[label] = {"cellar": cellar, "upper": upper}

    center_empty = all(block_name(cratered, (32, y, 32)) in {None, "minecraft:air"} for y in range(0, 16))
    if not center_empty:
        issues.append("central crater does not fully penetrate the road and utility chamber")
    spawner_count = sum(
        1 for state, _ in cratered.blocks.values()
        if cratered.palette[state]["Name"] == "minecraft:spawner"
    )
    if spawner_count != 4:
        issues.append(f"expected four distributed hostile spawners, found {spawner_count}")

    return {
        "structure_id": "infinite_domain:cratered_downtown_intersection_clean_master",
        "archetype": "signalized mixed-use downtown crossing with four corner buildings and underground utilities",
        "door_nodes_checked": len(required_lower_doors),
        "clean_master_ground_programs": ground_results,
        "clean_master_upper_floors": upper_results,
        "clean_master_vertical_access": {"stairs": stair_results, "utility_ladders": ladder_results},
        "clean_master_utility_network": {
            "targets": len(utility_targets), "reached": len(utility_reached),
            "missing": [list(pos) for pos in utility_missing],
        },
        "cratered_survivor_levels": survivor_results,
        "cratered_survivor_stairs": survivor_stairs,
        "central_crater_penetrates_utilities": center_empty,
        "hostile_spawners": spawner_count,
        "valid": not issues,
        "issues": issues,
        "note": "Program validation checks four distinct corner buildings, all room thresholds, ten upper floors, four cellar/upper stair spines, the underground utility cross, four surface hatches and surviving outer suites after crater formation. Rendered and in-game blast geometry review remain required.",
    }


def validate_ruined_hospital() -> dict[str, object]:
    template = ruined_hospital_clean_master()
    issues: list[str] = []
    floor_levels = (2, 9, 16, 23)
    required_lower_doors: set[tuple[int, int, int]] = {
        (14, 2, 8), (15, 2, 8), (37, 2, 8), (38, 2, 8),
        (27, 2, 13), (43, 2, 13),
        (20, 2, 22), (34, 2, 23), (48, 2, 22),
        (32, 2, 27), (33, 2, 27), (32, 2, 44), (33, 2, 44),
        (32, 2, 50), (33, 2, 50), (33, 2, 47),
        (33, 30, 22),
    }
    for feet_y in floor_levels:
        required_lower_doors.update((x, feet_y, 17) for x in (12, 24, 33, 39, 52))
        if feet_y > 2:
            for split_x in (20, 34, 48):
                required_lower_doors.update({(split_x, feet_y, 13), (split_x, feet_y, 22)})
        for wall_x in (13, 17, 49, 53):
            required_lower_doors.update((wall_x, feet_y, z) for z in (33, 40, 46))
        for z in (36, 43):
            required_lower_doors.update((x, feet_y, z) for x in (9, 21, 44, 57))
    missing_doors = sorted(
        pos for pos in required_lower_doors
        if not (block_name(template, pos) or "").endswith("_door")
    )
    if missing_doors:
        issues.append(f"missing required hospital thresholds at {missing_doors}")

    ground_targets = {
        # Ambulance/public intake and front clinical departments.
        (14, 2, 8), (37, 2, 8), (10, 2, 13), (18, 2, 22),
        (24, 2, 17), (33, 2, 17), (39, 2, 17),
        (33, 2, 22), (40, 2, 22), (45, 2, 21), (54, 2, 22),
        # Ward corridors, rooms, courtyard and rear services.
        (15, 2, 33), (15, 2, 40), (15, 2, 46),
        (51, 2, 33), (51, 2, 40), (51, 2, 46),
        (29, 2, 30), (33, 2, 47), (32, 2, 50),
    }
    ground_reached = horizontally_reachable(template, (37, 2, 7), ground_targets)
    ground_missing = sorted(ground_targets - ground_reached)
    if ground_missing:
        issues.append(f"clean master has unreachable hospital ground points: {ground_missing}")

    upper_results: dict[str, dict[str, object]] = {}
    for floor_index, feet_y in enumerate((9, 16, 23), start=1):
        targets = {
            (12, feet_y, 17), (24, feet_y, 17), (33, feet_y, 17),
            (39, feet_y, 17), (52, feet_y, 17),
            (10, feet_y, 22), (25, feet_y, 22), (40, feet_y, 22), (55, feet_y, 22),
            (15, feet_y, 33), (15, feet_y, 40), (15, feet_y, 46),
            (51, feet_y, 33), (51, feet_y, 40), (51, feet_y, 46),
        }
        front_approaches = {
            1: ((15, 12), (31, 12), (46, 12), (60, 12)),
            2: ((10, 12), (30, 12), (45, 12), (60, 12)),
            3: ((14, 12), (30, 12), (45, 12), (60, 12)),
        }[floor_index]
        targets.update((x, feet_y, z) for x, z in front_approaches)
        reached = horizontally_reachable(template, (33, feet_y, 17), targets)
        missing = sorted(targets - reached)
        if missing:
            issues.append(f"clean master hospital floor {floor_index} has unreachable points: {missing}")
        upper_results[str(floor_index)] = {
            "targets": len(targets), "reached": len(reached),
            "missing": [list(pos) for pos in missing],
        }

    expected_stairs = set(range(2, 8)) | set(range(9, 15)) | set(range(16, 22))
    stair_results: dict[str, list[int]] = {}
    for label, x in (("west", 16), ("east", 50)):
        levels = sorted(
            y for (px, y, z), (state, _) in template.blocks.items()
            if template.palette[state]["Name"] == "minecraft:polished_andesite_stairs"
            and px == x and 30 <= z <= 35
        )
        stair_results[label] = levels
        if set(levels) != expected_stairs:
            issues.append(f"{label} hospital stair stack is incomplete: {levels}")

    palette_counts = Counter(template.palette[state]["Name"] for state, _ in template.blocks.values())
    bed_blocks = sum(count for name, count in palette_counts.items() if name.endswith("_bed"))
    if bed_blocks < 100:
        issues.append(f"hospital has insufficient patient-bed representation: {bed_blocks} bed blocks")
    if palette_counts["minecraft:brewing_stand"] < 10:
        issues.append(f"hospital has insufficient clinical/pharmacy fixtures: {palette_counts['minecraft:brewing_stand']} brewing stands")
    if palette_counts["minecraft:water"] < 40 or palette_counts["minecraft:moss_block"] < 100:
        issues.append("hospital courtyard water/landscape program is incomplete")

    ruined = ruined_hospital()
    survivor_ground_targets = {
        (14, 2, 8), (37, 2, 8), (10, 2, 13), (18, 2, 22),
        (24, 2, 17), (33, 2, 17), (33, 2, 22),
        (15, 2, 33), (15, 2, 40), (15, 2, 46),
        (51, 2, 33), (51, 2, 46), (33, 2, 47), (32, 2, 50),
    }
    survivor_ground_reached = horizontally_reachable(ruined, (37, 2, 7), survivor_ground_targets)
    survivor_ground_missing = sorted(survivor_ground_targets - survivor_ground_reached)
    if survivor_ground_missing:
        issues.append(f"ruined hospital breaks surviving ground routes: {survivor_ground_missing}")

    survivor_floor_results: dict[str, dict[str, object]] = {}
    for floor_index, feet_y in enumerate((9, 16, 23), start=1):
        targets = {
            (12, feet_y, 17), (24, feet_y, 17), (33, feet_y, 17),
            (10, feet_y, 22), (25, feet_y, 22),
            (15, feet_y, 33), (15, feet_y, 40), (15, feet_y, 46),
            (51, feet_y, 33), (51, feet_y, 46),
        }
        survivor_front = {
            1: ((15, 12), (31, 12)),
            2: ((10, 12), (30, 12)),
            3: ((14, 12), (30, 12)),
        }[floor_index]
        targets.update((x, feet_y, z) for x, z in survivor_front)
        reached = horizontally_reachable(ruined, (33, feet_y, 17), targets)
        missing = sorted(targets - reached)
        if missing:
            issues.append(f"ruined hospital floor {floor_index} breaks survivor routes: {missing}")
        survivor_floor_results[str(floor_index)] = {
            "targets": len(targets), "reached": len(reached),
            "missing": [list(pos) for pos in missing],
        }

    ruined_stairs: dict[str, list[int]] = {}
    for label, x in (("west", 16), ("east", 50)):
        levels = sorted(
            y for (px, y, z), (state, _) in ruined.blocks.items()
            if ruined.palette[state]["Name"] == "minecraft:polished_andesite_stairs"
            and px == x and 30 <= z <= 35
        )
        ruined_stairs[label] = levels
        if set(levels) != expected_stairs:
            issues.append(f"ruined hospital damages {label} stair stack: {levels}")

    spawner_count = sum(
        1 for state, _ in ruined.blocks.values()
        if ruined.palette[state]["Name"] == "minecraft:spawner"
    )
    if spawner_count != 5:
        issues.append(f"expected five distributed hospital spawners, found {spawner_count}")

    return {
        "structure_id": "infinite_domain:ruined_hospital_clean_master",
        "archetype": "four-storey U-plan hospital with emergency, diagnostics, surgery, wards, support and roof plant",
        "door_nodes_checked": len(required_lower_doors),
        "clean_master_ground_program": {
            "targets": len(ground_targets), "reached": len(ground_reached),
            "missing": [list(pos) for pos in ground_missing],
        },
        "clean_master_upper_floors": upper_results,
        "vertical_access": {"clean_master_stairs": stair_results, "ruined_survivor_stairs": ruined_stairs},
        "clinical_fixture_counts": {
            "bed_blocks": bed_blocks,
            "brewing_stands": palette_counts["minecraft:brewing_stand"],
            "courtyard_water_blocks": palette_counts["minecraft:water"],
            "courtyard_landscape_blocks": palette_counts["minecraft:moss_block"],
        },
        "ruined_survivor_ground": {
            "targets": len(survivor_ground_targets), "reached": len(survivor_ground_reached),
            "missing": [list(pos) for pos in survivor_ground_missing],
        },
        "ruined_survivor_floors": survivor_floor_results,
        "hostile_spawners": spawner_count,
        "valid": not issues,
        "issues": issues,
        "note": "Program validation checks ambulance/public intake, ground clinical departments, three upper clinical floors, ward corridors, both stairs, courtyard/service connections, clinical fixture density and routes surviving the northeast collapse. Rendered and in-game hospital workflow review remain required.",
    }


def validate_ruined_police_precinct() -> dict[str, object]:
    template = ruined_police_precinct_clean_master()
    issues: list[str] = []
    required_lower_doors: set[tuple[int, int, int]] = {
        (21, 2, 6), (22, 2, 6),
        (12, 2, 14), (21, 2, 14), (22, 2, 14), (32, 2, 14),
        (10, 2, 19), (22, 2, 19), (34, 2, 19),
        (17, 2, 23), (30, 2, 23),
        (14, 2, 28), (15, 2, 28),
        (18, 2, 30), (18, 2, 33), (18, 2, 36), (18, 2, 40),
        (13, 2, 30), (13, 2, 33), (13, 2, 36), (13, 2, 39),
        (11, 2, 32), (25, 2, 32), (11, 2, 35), (25, 2, 35),
        (11, 2, 38), (25, 2, 38),
        (20, 2, 43), (21, 2, 43),
        (28, 2, 34), (28, 2, 35), (40, 2, 22), (40, 2, 23),
        (10, 9, 19), (22, 9, 19), (34, 9, 19),
        (14, 9, 13), (14, 9, 23), (27, 9, 13), (27, 9, 23),
        (14, 9, 28), (15, 9, 28),
        (10, 9, 35), (17, 9, 35), (24, 9, 35),
        (10, 9, 39), (17, 9, 39), (24, 9, 39),
        (13, 16, 16), (19, 16, 16), (15, 16, 19),
    }
    missing_doors = sorted(
        pos for pos in required_lower_doors
        if not (block_name(template, pos) or "").endswith("_door")
    )
    if missing_doors:
        issues.append(f"missing required precinct thresholds at {missing_doors}")

    ground_targets = {
        # Public arrival, controlled spine and operations.
        (21, 2, 6), (21, 2, 10), (12, 2, 10), (32, 2, 10),
        (21, 2, 14), (22, 2, 17), (10, 2, 19), (22, 2, 19), (34, 2, 19),
        (10, 2, 26), (22, 2, 23), (34, 2, 23), (35, 2, 24),
        # Booking, four cells, evidence/interview and rear staff exit.
        (14, 2, 28), (15, 2, 30), (15, 2, 39),
        (11, 2, 30), (11, 2, 33), (11, 2, 36), (11, 2, 39),
        (25, 2, 30), (23, 2, 34), (23, 2, 37), (23, 2, 40), (20, 2, 43),
        # Sally port and motor pool.
        (28, 2, 34), (35, 2, 40), (40, 2, 34),
        (44, 2, 18), (47, 2, 27), (48, 2, 32), (47, 2, 40),
    }
    ground_reached = horizontally_reachable(template, (21, 2, 5), ground_targets)
    ground_missing = sorted(ground_targets - ground_reached)
    if ground_missing:
        issues.append(f"clean master has unreachable precinct ground points: {ground_missing}")

    upper_targets = {
        (10, 9, 19), (22, 9, 19), (34, 9, 19),
        (10, 9, 13), (20, 9, 13), (32, 9, 13),
        (10, 9, 23), (23, 9, 23), (34, 9, 23),
        (14, 9, 28), (14, 9, 33), (16, 9, 33),
        (14, 9, 37), (17, 9, 37), (24, 9, 37),
        (10, 9, 41), (17, 9, 41), (24, 9, 41),
    }
    upper_reached = horizontally_reachable(template, (10, 9, 26), upper_targets)
    upper_missing = sorted(upper_targets - upper_reached)
    if upper_missing:
        issues.append(f"clean master has unreachable precinct first-floor points: {upper_missing}")

    command_targets = {
        (10, 16, 26), (10, 16, 19), (13, 16, 16),
        (10, 16, 12), (19, 16, 12), (19, 16, 19), (21, 16, 22),
    }
    command_reached = horizontally_reachable(template, (10, 16, 26), command_targets)
    command_missing = sorted(command_targets - command_reached)
    if command_missing:
        issues.append(f"clean master has unreachable precinct command-floor points: {command_missing}")

    expected_main_stairs = set(range(2, 8)) | set(range(9, 15))
    expected_secure_stairs = set(range(2, 8))
    main_stairs = sorted(
        y for (x, y, z), (state, _) in template.blocks.items()
        if template.palette[state]["Name"] == "minecraft:polished_andesite_stairs"
        and x == 10 and 20 <= z <= 25
    )
    secure_stairs = sorted(
        y for (x, y, z), (state, _) in template.blocks.items()
        if template.palette[state]["Name"] == "minecraft:polished_andesite_stairs"
        and x == 34 and 20 <= z <= 25
    )
    if set(main_stairs) != expected_main_stairs:
        issues.append(f"main precinct stair stack is incomplete: {main_stairs}")
    if set(secure_stairs) != expected_secure_stairs:
        issues.append(f"secure precinct stair is incomplete: {secure_stairs}")

    palette_counts = Counter(template.palette[state]["Name"] for state, _ in template.blocks.values())
    bed_blocks = sum(count for name, count in palette_counts.items() if name.endswith("_bed"))
    if bed_blocks != 8:
        issues.append(f"expected four complete detention beds, found {bed_blocks} bed blocks")
    if palette_counts["immersiveengineering:crate"] < 70:
        issues.append("precinct evidence, armory and garage storage is under-furnished")

    ruined = ruined_police_precinct()
    survivor_ground_targets = {
        (21, 2, 6), (21, 2, 10), (21, 2, 14), (22, 2, 17),
        (22, 2, 23), (34, 2, 23), (14, 2, 28),
        (15, 2, 30), (15, 2, 39), (23, 2, 34), (23, 2, 40),
        (28, 2, 34), (35, 2, 40), (40, 2, 34), (48, 2, 32), (47, 2, 40),
    }
    survivor_ground_reached = horizontally_reachable(ruined, (21, 2, 5), survivor_ground_targets)
    survivor_ground_missing = sorted(survivor_ground_targets - survivor_ground_reached)
    if survivor_ground_missing:
        issues.append(f"ruined precinct breaks surviving ground routes: {survivor_ground_missing}")

    survivor_upper_targets = {
        (10, 9, 26), (22, 9, 19), (34, 9, 19),
        (20, 9, 13), (32, 9, 13), (23, 9, 23), (34, 9, 23),
        (14, 9, 28), (16, 9, 33), (17, 9, 37), (24, 9, 41),
    }
    survivor_upper_reached = horizontally_reachable(ruined, (10, 9, 26), survivor_upper_targets)
    survivor_upper_missing = sorted(survivor_upper_targets - survivor_upper_reached)
    if survivor_upper_missing:
        issues.append(f"ruined precinct breaks surviving first-floor routes: {survivor_upper_missing}")

    survivor_command_targets = {(10, 16, 26), (10, 16, 19), (19, 16, 12), (20, 16, 19), (21, 16, 22)}
    survivor_command_reached = horizontally_reachable(ruined, (10, 16, 26), survivor_command_targets)
    survivor_command_missing = sorted(survivor_command_targets - survivor_command_reached)
    if survivor_command_missing:
        issues.append(f"ruined precinct breaks surviving command-floor routes: {survivor_command_missing}")

    ruined_main_stairs = sorted(
        y for (x, y, z), (state, _) in ruined.blocks.items()
        if ruined.palette[state]["Name"] == "minecraft:polished_andesite_stairs"
        and x == 10 and 20 <= z <= 25
    )
    ruined_secure_stairs = sorted(
        y for (x, y, z), (state, _) in ruined.blocks.items()
        if ruined.palette[state]["Name"] == "minecraft:polished_andesite_stairs"
        and x == 34 and 20 <= z <= 25
    )
    if set(ruined_main_stairs) != expected_main_stairs or set(ruined_secure_stairs) != expected_secure_stairs:
        issues.append("ruined precinct damages a required stair stack")

    spawner_count = sum(
        1 for state, _ in ruined.blocks.values()
        if ruined.palette[state]["Name"] == "minecraft:spawner"
    )
    if spawner_count != 5:
        issues.append(f"expected five distributed precinct spawners, found {spawner_count}")

    return {
        "structure_id": "infinite_domain:ruined_police_precinct_clean_master",
        "archetype": "L-plan police precinct with public, patrol, detention, evidence, command and motor-pool programs",
        "door_nodes_checked": len(required_lower_doors),
        "clean_master_ground_program": {"targets": len(ground_targets), "reached": len(ground_reached), "missing": [list(pos) for pos in ground_missing]},
        "clean_master_first_floor": {"targets": len(upper_targets), "reached": len(upper_reached), "missing": [list(pos) for pos in upper_missing]},
        "clean_master_command_floor": {"targets": len(command_targets), "reached": len(command_reached), "missing": [list(pos) for pos in command_missing]},
        "vertical_access": {
            "clean_main_stairs": main_stairs, "clean_secure_stairs": secure_stairs,
            "ruined_main_stairs": ruined_main_stairs, "ruined_secure_stairs": ruined_secure_stairs,
        },
        "program_counts": {"detention_bed_blocks": bed_blocks, "crate_blocks": palette_counts["immersiveengineering:crate"]},
        "ruined_survivor_ground": {"targets": len(survivor_ground_targets), "reached": len(survivor_ground_reached), "missing": [list(pos) for pos in survivor_ground_missing]},
        "ruined_survivor_first_floor": {"targets": len(survivor_upper_targets), "reached": len(survivor_upper_reached), "missing": [list(pos) for pos in survivor_upper_missing]},
        "ruined_survivor_command_floor": {"targets": len(survivor_command_targets), "reached": len(survivor_command_reached), "missing": [list(pos) for pos in survivor_command_missing]},
        "hostile_spawners": spawner_count,
        "valid": not issues,
        "issues": issues,
        "note": "Program validation checks public/secure arrival, operations, booking, four cells, evidence, sally port, three garage lanes, two upper programs, both stairs and routes surviving the front-west blast. Rendered and in-game police workflow review remain required.",
    }


def validate_ruined_courthouse() -> dict[str, object]:
    template = ruined_courthouse_clean_master()
    issues: list[str] = []
    required_lower_doors: set[tuple[int, int, int]] = {
        (28, 2, 8), (29, 2, 8),
        (14, 2, 18), (28, 2, 18), (29, 2, 18), (44, 2, 18),
        (18, 2, 14), (40, 2, 14),
        (23, 2, 22), (23, 2, 29), (35, 2, 22), (35, 2, 29),
        (12, 2, 36), (28, 2, 36), (29, 2, 36), (46, 2, 36),
        (9, 2, 39), (13, 2, 39), (24, 2, 39), (34, 2, 39), (44, 2, 39), (49, 2, 39),
        (11, 2, 42), (15, 2, 42), (29, 2, 42), (41, 2, 42), (47, 2, 42),
        (28, 2, 45), (29, 2, 45),
        (12, 11, 21), (27, 11, 21), (31, 11, 21), (46, 11, 21),
        (14, 11, 16), (28, 11, 16), (42, 11, 16),
        (26, 11, 26), (26, 11, 32), (32, 11, 26), (32, 11, 32),
        (12, 11, 36), (27, 11, 36), (31, 11, 36), (46, 11, 36),
        (18, 11, 41), (30, 11, 41), (42, 11, 41),
    }
    missing_doors = sorted(
        pos for pos in required_lower_doors
        if not (block_name(template, pos) or "").endswith("_door")
    )
    if missing_doors:
        issues.append(f"missing required courthouse thresholds at {missing_doors}")

    ground_targets = {
        # Public arrival and service rooms.
        (28, 2, 8), (28, 2, 12), (14, 2, 14), (44, 2, 14),
        (14, 2, 18), (28, 2, 18), (44, 2, 18),
        # Central atrium and both ground courtrooms.
        (29, 2, 22), (29, 2, 30),
        (23, 2, 22), (15, 2, 20), (15, 2, 32),
        (35, 2, 22), (44, 2, 20), (44, 2, 31),
        # Rear secure corridor, holding, chambers, evidence/archive and exit.
        (12, 2, 36), (29, 2, 36), (46, 2, 36),
        (9, 2, 41), (13, 2, 41), (24, 2, 41), (34, 2, 41),
        (44, 2, 41), (49, 2, 41), (28, 2, 45),
        # Stair approaches.
        (29, 2, 32), (46, 2, 43),
    }
    ground_reached = horizontally_reachable(template, (28, 2, 7), ground_targets)
    ground_missing = sorted(ground_targets - ground_reached)
    if ground_missing:
        issues.append(f"clean master has unreachable courthouse ground points: {ground_missing}")

    upper_targets = {
        (27, 11, 24), (12, 11, 21), (27, 11, 21), (31, 11, 21), (46, 11, 21),
        (10, 11, 14), (20, 11, 14), (34, 11, 14), (48, 11, 14),
        (26, 11, 26), (15, 11, 23), (15, 11, 32),
        (32, 11, 26), (44, 11, 23), (44, 11, 32),
        (12, 11, 36), (27, 11, 36), (31, 11, 36), (46, 11, 36),
        (10, 11, 40), (24, 11, 40), (35, 11, 40), (47, 11, 40),
        (47, 11, 35),
    }
    upper_reached = horizontally_reachable(template, (27, 11, 24), upper_targets)
    upper_missing = sorted(upper_targets - upper_reached)
    if upper_missing:
        issues.append(f"clean master has unreachable courthouse upper points: {upper_missing}")

    expected_stairs = set(range(2, 10))
    public_stairs = sorted(
        y for (x, y, z), (state, _) in template.blocks.items()
        if template.palette[state]["Name"] == "minecraft:polished_andesite_stairs"
        and x == 27 and 25 <= z <= 32
    )
    secure_stairs = sorted(
        y for (x, y, z), (state, _) in template.blocks.items()
        if template.palette[state]["Name"] == "minecraft:polished_andesite_stairs"
        and x == 47 and 36 <= z <= 43
    )
    if set(public_stairs) != expected_stairs:
        issues.append(f"public courthouse stair is incomplete: {public_stairs}")
    if set(secure_stairs) != expected_stairs:
        issues.append(f"secure courthouse stair is incomplete: {secure_stairs}")

    palette_counts = Counter(template.palette[state]["Name"] for state, _ in template.blocks.values())
    bed_blocks = sum(count for name, count in palette_counts.items() if name.endswith("_bed"))
    courtroom_seats = palette_counts["minecraft:dark_oak_stairs"]
    if bed_blocks != 4:
        issues.append(f"expected two complete holding-cell beds, found {bed_blocks} bed blocks")
    if courtroom_seats < 160:
        issues.append(f"courthouse has insufficient gallery/hearing seating: {courtroom_seats}")

    ruined = ruined_courthouse()
    survivor_ground_targets = {
        (28, 2, 8), (28, 2, 12), (14, 2, 14), (28, 2, 18),
        (29, 2, 22), (29, 2, 30), (23, 2, 22), (15, 2, 20), (15, 2, 32),
        (12, 2, 36), (29, 2, 36), (46, 2, 36),
        (9, 2, 41), (13, 2, 41), (24, 2, 41), (34, 2, 41),
        (45, 2, 41), (49, 2, 41), (28, 2, 45), (29, 2, 32), (46, 2, 43),
    }
    survivor_ground_reached = horizontally_reachable(ruined, (28, 2, 7), survivor_ground_targets)
    survivor_ground_missing = sorted(survivor_ground_targets - survivor_ground_reached)
    if survivor_ground_missing:
        issues.append(f"ruined courthouse breaks surviving ground routes: {survivor_ground_missing}")

    survivor_upper_targets = {
        (27, 11, 24), (12, 11, 21), (27, 11, 21), (31, 11, 21),
        (10, 11, 14), (20, 11, 14), (34, 11, 14),
        (26, 11, 26), (15, 11, 23), (15, 11, 32),
        (12, 11, 36), (27, 11, 36), (31, 11, 36), (46, 11, 36),
        (10, 11, 40), (24, 11, 40), (35, 11, 40), (47, 11, 40), (47, 11, 35),
    }
    survivor_upper_reached = horizontally_reachable(ruined, (27, 11, 24), survivor_upper_targets)
    survivor_upper_missing = sorted(survivor_upper_targets - survivor_upper_reached)
    if survivor_upper_missing:
        issues.append(f"ruined courthouse breaks surviving upper routes: {survivor_upper_missing}")

    ruined_public_stairs = sorted(
        y for (x, y, z), (state, _) in ruined.blocks.items()
        if ruined.palette[state]["Name"] == "minecraft:polished_andesite_stairs"
        and x == 27 and 25 <= z <= 32
    )
    ruined_secure_stairs = sorted(
        y for (x, y, z), (state, _) in ruined.blocks.items()
        if ruined.palette[state]["Name"] == "minecraft:polished_andesite_stairs"
        and x == 47 and 36 <= z <= 43
    )
    if set(ruined_public_stairs) != expected_stairs or set(ruined_secure_stairs) != expected_stairs:
        issues.append("ruined courthouse damages a required stair")

    spawner_count = sum(
        1 for state, _ in ruined.blocks.values()
        if ruined.palette[state]["Name"] == "minecraft:spawner"
    )
    if spawner_count != 5:
        issues.append(f"expected five distributed courthouse spawners, found {spawner_count}")

    return {
        "structure_id": "infinite_domain:ruined_courthouse_clean_master",
        "archetype": "two-storey courthouse with paired courtrooms, hearing rooms and separate public/secure circulation",
        "door_nodes_checked": len(required_lower_doors),
        "clean_master_ground_program": {"targets": len(ground_targets), "reached": len(ground_reached), "missing": [list(pos) for pos in ground_missing]},
        "clean_master_upper_program": {"targets": len(upper_targets), "reached": len(upper_reached), "missing": [list(pos) for pos in upper_missing]},
        "vertical_access": {"clean_public_stairs": public_stairs, "clean_secure_stairs": secure_stairs, "ruined_public_stairs": ruined_public_stairs, "ruined_secure_stairs": ruined_secure_stairs},
        "program_counts": {"holding_bed_blocks": bed_blocks, "courtroom_seat_blocks": courtroom_seats},
        "ruined_survivor_ground": {"targets": len(survivor_ground_targets), "reached": len(survivor_ground_reached), "missing": [list(pos) for pos in survivor_ground_missing]},
        "ruined_survivor_upper": {"targets": len(survivor_upper_targets), "reached": len(survivor_upper_reached), "missing": [list(pos) for pos in survivor_upper_missing]},
        "hostile_spawners": spawner_count,
        "valid": not issues,
        "issues": issues,
        "note": "Program validation checks portico/public services, both courtrooms, holding/chambers/evidence, two upper hearing rooms, rear support, both stairs and routes surviving the east-courtroom blast. Rendered and in-game courthouse workflow review remain required.",
    }


def main() -> None:
    motel = validate_motel()
    grocery = validate_grocery()
    gas_station = validate_gas_station()
    freight = validate_freight_depot()
    fire_station = validate_fire_station()
    corporate = validate_corporate_warehouse()
    factory = validate_create_factory()
    bunker = validate_bunker_network()
    cache = validate_survivor_cache()
    outpost = validate_trade_outpost()
    farm = validate_decayed_farm()
    park = validate_trailer_park()
    military = validate_mountain_military_complex()
    biohazard = validate_mountain_biohazard_lab()
    logging = validate_decayed_logging_camp()
    data_center = validate_bombed_data_center()
    dam = validate_hydroelectric_refuge_dam()
    skyscraper = validate_toppled_skyscraper()
    apartments = validate_blown_apartment_complex()
    mixed_use = validate_ruined_mixed_use_block()
    sunken_front = validate_sunken_city_front()
    parking = validate_pancaked_parking_structure()
    intersection = validate_cratered_downtown_intersection()
    hospital = validate_ruined_hospital()
    precinct = validate_ruined_police_precinct()
    courthouse = validate_ruined_courthouse()
    report = {
        "purpose": "Building-program and circulation validation for heavily rebuilt clean masters.",
        "valid": motel["valid"] and grocery["valid"] and gas_station["valid"] and freight["valid"] and fire_station["valid"] and corporate["valid"] and factory["valid"] and bunker["valid"] and cache["valid"] and outpost["valid"] and farm["valid"] and park["valid"] and military["valid"] and biohazard["valid"] and logging["valid"] and data_center["valid"] and dam["valid"] and skyscraper["valid"] and apartments["valid"] and mixed_use["valid"] and sunken_front["valid"] and parking["valid"] and intersection["valid"] and hospital["valid"] and precinct["valid"] and courthouse["valid"],
        "structures": {
            "infinite_domain:motel_clean_master": motel,
            "infinite_domain:grocery_clean_master": grocery,
            "infinite_domain:gas_station_clean_master": gas_station,
            "infinite_domain:freight_depot_clean_master": freight,
            "infinite_domain:fire_station_clean_master": fire_station,
            "infinite_domain:corporate_warehouse_clean_master": corporate,
            "infinite_domain:create_factory_clean_master": factory,
            "infinite_domain:bunker_network_clean_master": bunker,
            "infinite_domain:survivor_cache_clean_master": cache,
            "infinite_domain:trade_outpost_clean_master": outpost,
            "infinite_domain:decayed_farm_clean_master": farm,
            "infinite_domain:trailer_park_clean_master": park,
            "infinite_domain:mountain_military_complex_clean_master": military,
            "infinite_domain:mountain_biohazard_lab_clean_master": biohazard,
            "infinite_domain:decayed_logging_camp_clean_master": logging,
            "infinite_domain:bombed_data_center_clean_master": data_center,
            "infinite_domain:hydroelectric_refuge_dam_clean_master": dam,
            "infinite_domain:toppled_skyscraper_clean_master": skyscraper,
            "infinite_domain:blown_apartment_complex_clean_master": apartments,
            "infinite_domain:ruined_mixed_use_block_clean_master": mixed_use,
            "infinite_domain:sunken_city_front_clean_master": sunken_front,
            "infinite_domain:pancaked_parking_structure_clean_master": parking,
            "infinite_domain:cratered_downtown_intersection_clean_master": intersection,
            "infinite_domain:ruined_hospital_clean_master": hospital,
            "infinite_domain:ruined_police_precinct_clean_master": precinct,
            "infinite_domain:ruined_courthouse_clean_master": courthouse,
        },
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
    if not report["valid"]:
        all_issues = [*motel["issues"], *grocery["issues"], *gas_station["issues"], *freight["issues"], *fire_station["issues"], *corporate["issues"], *factory["issues"], *bunker["issues"], *cache["issues"], *outpost["issues"], *farm["issues"], *park["issues"], *military["issues"], *biohazard["issues"], *logging["issues"], *data_center["issues"], *dam["issues"], *skyscraper["issues"], *apartments["issues"], *mixed_use["issues"], *sunken_front["issues"], *parking["issues"], *intersection["issues"], *hospital["issues"], *precinct["issues"], *courthouse["issues"]]
        raise SystemExit("\n".join(all_issues))
    print("Validated structure programs including logging camp ground workflow, service catwalk, vertical access and damaged-variant survivor routes")


if __name__ == "__main__":
    main()
