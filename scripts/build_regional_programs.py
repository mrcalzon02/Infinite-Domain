#!/usr/bin/env python3
"""Author the per-structure program files the regional generators require.

STRUCTURE_REBUILD_SYSTEM_V2.md section 3.1 makes the program file a *required
generation input*, not documentation written afterwards: geometry generation
reads its room lists and a validator diffs the produced room ledger against
them. No geometry pass may run for a structure whose program is absent.

Programs here are not filled with generic text. Each master is mapped to a
building type, and each type carries an authored room program, circulation,
damage constraints and review checks. Per-structure specialisation comes from
the roster (identity, strata, damage archetype, conversion class) and from the
base master's catalog metadata (category, settlement types, road connection,
footprint).

Authority: docs/KARSIC_DIRECTORATE_STRUCTURE_PROGRAM.md sections 7, 8.2, 10
           structure_library/STRUCTURE_REBUILD_SYSTEM_V2.md section 3.1

Usage:
    python scripts/build_regional_programs.py --culture karsic
    python scripts/build_regional_programs.py --culture karsic --family KF1 KF2
    python scripts/build_regional_programs.py --culture karsic --check
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGIONAL = ROOT / "structure_library" / "regional"
PROGRAMS = ROOT / "structure_library" / "programs"
CATALOG = ROOT / "structure_library" / "catalog.json"

# --------------------------------------------------------------------------
# Karsic building types
# --------------------------------------------------------------------------

KARSIC_TYPES: dict[str, str] = {
    # agricultural
    "kar_001_fruit_processing_combine": "process_plant",
    "kar_002_state_farm_unit": "farmstead",
    "kar_003_livestock_station": "farmstead",
    "kar_004_grain_reception_point": "silo_bank",
    "kar_005_heated_greenhouse_block": "greenhouse_range",
    # civic
    "kar_006_state_archive_repository": "institutional_hall",
    "kar_007_civil_defence_shelter": "bunker",
    "kar_008_fire_rescue_detachment": "appliance_hall",
    "kar_009_memorial_and_chapel": "memorial",
    "kar_010_school_series_block": "school_block",
    "kar_011_house_of_culture": "institutional_hall",
    "kar_012_district_administration": "institutional_hall",
    "kar_013_prosthetics_institute": "hospital_korpus",
    "kar_014_district_hospital": "hospital_korpus",
    "kar_015_militia_district_station": "appliance_hall",
    "kar_016_forestry_cordon": "detached_small",
    # commercial
    "kar_017_highway_service_point": "roadside_service",
    "kar_018_state_hotel": "panel_slab",
    "kar_019_state_bank_branch": "institutional_hall",
    "kar_020_administrative_square": "civic_square",
    "kar_021_gastronom": "retail_plinth",
    "kar_022_roadside_rest_house": "roadside_service",
    "kar_023_univermag": "department_store",
    "kar_024_panel_block_service_premises": "retail_plinth",
    "kar_025_design_institute_tower": "panel_slab",
    "kar_026_roadside_canteen": "roadside_service",
    "kar_027_trade_centre": "department_store",
    "kar_028_embankment_front": "civic_square",
    "kar_029_toppled_institute_tower": "panel_slab",
    "kar_030_supply_point": "warehouse_depot",
    # highway
    "kar_031_service_van": "prop_vehicle",
    "kar_032_evacuation_convoy": "wreck_scene",
    "kar_033_fuel_station": "roadside_service",
    "kar_034_avalanche_gallery": "linear_infrastructure",
    "kar_035_bus_station": "transit_hall",
    "kar_036_grade_separated_interchange": "linear_infrastructure",
    "kar_037_traffic_inspection_post": "checkpoint",
    "kar_038_state_sedan": "prop_vehicle",
    # industrial
    "kar_039_oil_field": "extraction_site",
    "kar_040_stone_quarry": "extraction_site",
    "kar_041_computing_centre": "hardened_technical",
    "kar_042_northern_industrial_port": "port_apron",
    "kar_043_mine_headframe": "extraction_site",
    "kar_044_bonded_warehouse": "warehouse_depot",
    "kar_045_downed_cargo_airship": "wreck_scene",
    "kar_046_machine_hall": "machine_hall",
    "kar_047_timber_combine": "machine_hall",
    "kar_048_dragline_pit": "extraction_site",
    "kar_049_industrial_combine": "machine_hall",
    "kar_050_waste_incineration_plant": "process_plant",
    "kar_051_reactor_service_annex": "hardened_technical",
    "kar_052_forest_sawmill": "machine_hall",
    "kar_053_fuel_depot": "tank_farm",
    "kar_054_scrap_reclamation_yard": "open_yard",
    "kar_055_motor_pool": "open_yard",
    "kar_056_southern_industrial_port": "port_apron",
    # military
    "kar_057_directorate_tank": "prop_vehicle",
    "kar_058_hardened_command_bunker": "bunker",
    "kar_059_control_post": "checkpoint",
    "kar_060_isolated_biological_institute": "hardened_technical",
    "kar_061_mountain_garrison": "barrack_row",
    # miscellaneous
    "kar_062_airship_mooring_terminal": "transit_hall",
    "kar_063_civil_defence_stores_cache": "bunker",
    # railway
    "kar_064_deep_metro_station": "transit_hall",
    "kar_065_rail_overpass_collapse": "linear_infrastructure",
    "kar_066_classification_yard": "open_yard",
    # residential
    "kar_067_series_panel_block": "panel_slab",
    "kar_068_dacha": "detached_small",
    "kar_069_workers_barrack_row": "barrack_row",
    "kar_070_nomenklatura_block": "panel_slab",
    "kar_071_courtyard_block": "courtyard_block",
    # utility
    "kar_072_imported_solar_array": "field_array",
    "kar_073_district_substation": "switchyard",
    "kar_074_water_treatment_works": "process_plant",
    "kar_075_district_heating_station": "process_plant",
    "kar_076_hydroelectric_works": "process_plant",
    "kar_077_institute_garage_deck": "open_yard",
    "kar_078_relay_mast": "mast_tower",
    "kar_079_imported_wind_array": "field_array",
    "kar_080_forestry_watchtower": "mast_tower",
    "kar_081_steel_water_tower": "mast_tower",
    "kar_082_remote_substation": "switchyard",
    # natives
    "kar_083_district_heating_main": "linear_infrastructure",
    "kar_084_transformer_kiosk": "kiosk",
    "kar_085_bus_shelter_and_stop": "kiosk",
    "kar_086_courtyard_housing_group": "courtyard_group",
    "kar_087_village_cottage": "detached_small",
    "kar_088_construction_camp": "camp_row",
    "kar_089_garage_cooperative": "open_yard",
    "kar_090_kindergarten_block": "school_block",
    "kar_091_technical_institute": "institutional_hall",
    "kar_092_memorial_complex": "memorial",
    "kar_093_seed_storage_bunker": "bunker",
    "kar_094_tracking_station": "hardened_technical",
}

# --------------------------------------------------------------------------
# Authored type templates
# --------------------------------------------------------------------------
# Each template supplies: the program domain key, the room list, circulation,
# damage constraints, required manual review checks, and the site/foundation
# defaults for that building type. Nothing here is filler; every room named is
# a room the geometry pass must produce and the room-ledger validator must find.

T = dict[str, Any]

KARSIC_TEMPLATES: dict[str, T] = {
    "panel_slab": {
        "domain": "residential_program",
        "repeatable_storey": True,
        "site_context": "karsic_district_yard",
        "foundation_profile": "full_basement",
        "district_role": "courtyard_slab",
        "heating_main_connection": "north_basement",
        "rooms": [
            "identical apartment or office floors repeated the full height of the slab",
            "two stair cores expressed as projecting towers with a continuous glazing slot",
            "a landing serving two to four doors at every core on every floor",
            "ground-floor entrance vestibules with an unheated lobby between two door leaves",
            "ground-floor mail, pram and refuse stores off the entrance lobby",
            "a basement pipe gallery running the long axis to the exterior heating main stub",
            "a basement electrical room and a lockable tenant store bay",
            "a roof bulkhead over each stair core with the roof plant clustered against it",
        ],
        "circulation": [
            "vertical circulation is two encased stair cores, landing-connected at both ends",
            "no floor may be reachable only through another dwelling",
            "the basement gallery connects both cores",
        ],
        "damage": [
            "the heating main is severed at one visible saddle on the lot",
            "frost damage, burst risers and boarded openings appear only on the bays downstream of the break",
            "both stair cores and the basement route survive",
            "at least one entrance vestibule remains intact and passable",
        ],
        "review": [
            "the panel joint grid is continuous and unbroken across every elevation",
            "storey bands above the plinth are silhouette-identical",
            "the plinth reads as one block proud on all four elevations",
            "the break in the heating main is findable without entering the building",
        ],
    },
    "courtyard_block": {
        "domain": "residential_program",
        "repeatable_storey": True,
        "site_context": "karsic_district_yard",
        "foundation_profile": "full_basement",
        "district_role": "perimeter_block",
        "heating_main_connection": "courtyard_basement",
        "rooms": [
            "a continuous perimeter range enclosing a single courtyard",
            "one arched gateway through the range, the only vehicle way in",
            "stair cores opening onto the courtyard, not the street",
            "apartments arranged two per landing on every upper floor",
            "ground-floor communal laundry, drying room and refuse store",
            "a courtyard with drying frames, benches and a standpipe",
            "a basement pipe gallery ringing the courtyard",
        ],
        "circulation": [
            "the gateway is the single vehicle entry and must remain passable",
            "every core is reached from the courtyard",
        ],
        "damage": [
            "one range of the perimeter is breached, opening the courtyard to the street",
            "the gateway survives",
            "rubble falls into the courtyard and the street, never sealing the gateway",
        ],
        "review": [
            "the courtyard reads as an enclosed outdoor room, not a gap between buildings",
            "the gateway is the obvious way in",
        ],
    },
    "courtyard_group": {
        "domain": "settlement_program",
        "repeatable_storey": True,
        "site_context": "karsic_district_yard",
        "foundation_profile": "partial_basement",
        "district_role": "mikrorayon",
        "heating_main_connection": "group_spine",
        "rooms": [
            "three panel slabs placed to enclose a shared courtyard on three sides",
            "a communal playground with frames and a sand pit",
            "drying frames and carpet-beating rails",
            "a small boiler stub serving the group, with its main running to every slab",
            "a refuse platform and a transformer kiosk at the service road edge",
            "footpaths entering the courtyard from the road ring",
        ],
        "circulation": [
            "roads pass around the group; footpaths pass through it",
            "no road enters the courtyard",
        ],
        "damage": [
            "the group boiler has failed and the slabs show frost damage in step, worst furthest from it",
            "the playground and footpaths remain legible",
        ],
        "review": [
            "the group reads as one designed district, not three separate buildings",
            "the heating main visibly links all three slabs to one source",
        ],
    },
    "barrack_row": {
        "domain": "residential_program",
        "repeatable_storey": False,
        "site_context": "karsic_district_yard",
        "foundation_profile": "surface",
        "district_role": "workers_row",
        "heating_main_connection": "row_end",
        "rooms": [
            "a two-storey brick row of repeated single-room dwellings",
            "external stair flights serving the upper doors directly",
            "a shared yard behind with outbuildings, a standpipe and a latrine block",
            "a stove flue per dwelling rising through the roof",
            "a coal or fuel store at each end of the row",
        ],
        "circulation": [
            "every dwelling is entered from outside; there is no internal corridor",
            "external stairs land on a real walkway, not in open air",
        ],
        "damage": [
            "one bay of the row has collapsed, exposing the party walls either side",
            "the external stairs and the yard route survive",
        ],
        "review": [
            "the row reads as many small dwellings, not one long building",
            "the stove flue rhythm is regular and matches the dwelling count",
        ],
    },
    "detached_small": {
        "domain": "residential_program",
        "repeatable_storey": False,
        "site_context": "rural_worked",
        "foundation_profile": "surface",
        "district_role": "rural_plot",
        "heating_main_connection": None,
        "rooms": [
            "a single-storey dwelling of two or three rooms around a masonry stove",
            "an enclosed veranda or storm porch at the entrance",
            "a garden plot with beds, a water butt and a compost corner",
            "a timber outbuilding for tools and fuel",
            "a fence of mismatched boards enclosing the plot",
        ],
        "circulation": ["one entrance through the storm porch", "the plot is entered from a track, not a road"],
        "damage": [
            "the roof has partly fallen at the ridge; the stove and its flue still stand",
            "the garden has gone to seed but its bed lines are still readable",
        ],
        "review": [
            "the building reads as informal and individually built, unlike everything else in the region",
            "the stove is the obvious centre of the plan",
        ],
    },
    "school_block": {
        "domain": "civic_program",
        "repeatable_storey": True,
        "site_context": "karsic_district_yard",
        "foundation_profile": "partial_basement",
        "district_role": "district_service",
        "heating_main_connection": "rear_basement",
        "rooms": [
            "a symmetric teaching block with cellular classrooms both sides of a wide corridor",
            "a central entrance vestibule on the axis of symmetry",
            "a double-height assembly hall wing",
            "a gymnasium wing with changing rooms",
            "a canteen with a serving line and communal tables",
            "a staff room, a records room and a nurse's room off the ground corridor",
            "cloakroom bays along the ground corridor",
            "an asphalt yard with painted markings and a boundary fence",
            "a basement pipe gallery and boiler substation",
        ],
        "circulation": [
            "a 3-wide double-loaded corridor on every teaching floor",
            "stair cores at both ends of the corridor, neither a dead end",
        ],
        "damage": [
            "the hall or gymnasium roof has failed; the teaching block stands",
            "both stair cores survive",
            "the yard markings remain readable",
        ],
        "review": [
            "classrooms read as classrooms rather than repeated empty rooms",
            "the assembly hall is legibly double-height from inside and out",
        ],
    },
    "institutional_hall": {
        "domain": "civic_program",
        "repeatable_storey": False,
        "site_context": "urban_paved",
        "foundation_profile": "full_basement",
        "district_role": "axial_terminus",
        "heating_main_connection": "below_forecourt",
        "rooms": [
            "a ceremonial entrance on the central axis reached by a broad flight of steps",
            "a full-width entrance hall with a cloakroom and an attendant's desk",
            "a principal double-height hall, chamber or reading room on the axis",
            "flanking cellular offices or club rooms on both upper floors",
            "a records or stack room below grade",
            "a service entrance and plant access from a rear or basement yard",
            "an oversized paved forecourt at least as deep as the building is tall",
        ],
        "circulation": [
            "the public route is axial and symmetric from forecourt to principal hall",
            "back-of-house is reached from below, keeping the ceremonial elevation clean",
        ],
        "damage": [
            "the principal hall roof has partly failed; the entrance sequence survives",
            "the below-grade records level stays dry and intact",
        ],
        "review": [
            "the approach reads as ceremonial without any added ornament",
            "the building has no crown; the top is a flat entablature band",
        ],
    },
    "hospital_korpus": {
        "domain": "medical_program",
        "repeatable_storey": True,
        "site_context": "karsic_district_yard",
        "foundation_profile": "full_basement",
        "district_role": "district_service",
        "heating_main_connection": "gallery_basement",
        "rooms": [
            "two or more ward blocks standing apart from each other",
            "enclosed heated galleries physically linking the blocks at ground level",
            "repeated ward rooms off a wide double-loaded corridor",
            "a treatment and examination suite on the ground floor",
            "an admissions hall with a waiting bay and a records counter",
            "a laboratory or dispensary wing",
            "a mortuary and a plant room below grade",
            "an ambulance apron with a canopy at the admissions entrance",
        ],
        "circulation": [
            "the heated galleries are the primary inter-block route and must be walkable end to end",
            "every ward floor has two stair cores",
        ],
        "damage": [
            "one ward block is dark and sealed with improvised partitions; another remains in use",
            "the heated galleries survive as the route between them",
            "the basement plant room stays intact",
        ],
        "review": [
            "the enclosed heated link between blocks is the first thing that reads",
            "wards read as wards, not as repeated empty rooms",
        ],
    },
    "retail_plinth": {
        "domain": "commercial_program",
        "repeatable_storey": True,
        "site_context": "urban_paved",
        "foundation_profile": "partial_basement",
        "district_role": "street_frontage",
        "heating_main_connection": "rear_basement",
        "rooms": [
            "a glazed ground-floor retail hall running the full street frontage",
            "a serving counter run and shelving bays inside the hall",
            "a back-of-house store, cold room and staff room behind the hall",
            "a goods entrance from the rear service yard",
            "identical residential or office floors above the retail plinth",
            "a separate residential entrance vestibule away from the shop door",
            "a basement store and pipe gallery",
        ],
        "circulation": [
            "shop and dwellings have entirely separate entrances",
            "goods reach the store without crossing the retail hall",
        ],
        "damage": [
            "the retail glazing is gone and the hall is open to the street",
            "the upper floors and the residential entrance survive",
            "the back store is partly intact",
        ],
        "review": [
            "the ground floor reads as retail and the floors above read as dwellings",
            "the plinth offset is unbroken behind the shopfront",
        ],
    },
    "department_store": {
        "domain": "commercial_program",
        "repeatable_storey": True,
        "site_context": "urban_paved",
        "foundation_profile": "full_basement",
        "district_role": "street_frontage",
        "heating_main_connection": "rear_basement",
        "rooms": [
            "a concrete-framed trading floor on every level, free of partitions",
            "a central escalator or stair hall rising the full height",
            "continuous ribbon glazing to the street on the upper floors",
            "a goods lift and back-of-house spine along the rear elevation",
            "stock rooms and a loading dock at the rear",
            "a basement trading floor and plant room",
            "a rooftop plant enclosure",
        ],
        "circulation": [
            "the vertical hall is the primary public route and is visible from the entrance",
            "goods circulation never crosses the trading floor",
        ],
        "damage": [
            "one corner of the frame has failed, exposing several trading floors at once",
            "the vertical hall survives",
        ],
        "review": [
            "trading floors read as open retail, not as offices",
            "the frame is legible where the corner has gone",
        ],
    },
    "machine_hall": {
        "domain": "industrial_program",
        "repeatable_storey": False,
        "site_context": "industrial_hardstanding",
        "foundation_profile": "surface",
        "district_role": "works",
        "heating_main_connection": "ancillary_basement",
        "rail_served": True,
        "rooms": [
            "a clear-span machine hall three storeys tall with a crane rail at eaves level",
            "a clerestory glazing band in the top two blocks of the hall wall",
            "a machine access lane running the full length of the hall to a door at each end",
            "a control room at mezzanine level glazed onto the hall",
            "a changing and wash block at the workers' entrance",
            "a repair bay with spare-parts racking",
            "an attached low ancillary block with offices and a canteen",
            "a rail siding with a loading gantry over it",
            "a stack standing clear of the roof mass",
        ],
        "circulation": [
            "the access lane is 4 wide and reaches a door at both ends",
            "the control room is reached without crossing the hall floor",
        ],
        "damage": [
            "the hall stands but has been stripped: cut cable ends, empty mountings, drag marks to the doors",
            "the crane rail survives; the crane does not",
            "the changing block and control room remain legible",
        ],
        "review": [
            "the hall reads as one large working volume, not as subdivided rooms",
            "what was removed is inferable from what is left behind",
        ],
    },
    "process_plant": {
        "domain": "industrial_program",
        "repeatable_storey": False,
        "site_context": "industrial_hardstanding",
        "foundation_profile": "partial_basement",
        "district_role": "utility_anchor",
        "heating_main_connection": "plant_origin",
        "rail_served": True,
        "rooms": [
            "a tall plant hall containing the principal process vessels",
            "a fuel or feedstock yard with a delivery route into the hall",
            "a control room at mezzanine level glazed onto the plant hall",
            "a pump and pipe gallery below the hall floor",
            "a changing and wash block at the workers' entrance",
            "a workshop with extensive spare-parts storage",
            "a tall stack standing clear of the roof",
            "the origin manifold of the district heating main, leaving the site above ground on saddles",
        ],
        "circulation": [
            "the pipe gallery connects the plant hall to the exterior main",
            "the control room overlooks the vessels it controls",
        ],
        "damage": [
            "the same pump or seal has been repaired many times: a stack of replacement parts beside the failed unit and a wall of tally marks",
            "the plant hall is intact enough to read as recently worked",
            "the heating main leaves the site and is severed beyond the fence",
        ],
        "review": [
            "the input, process and output route through the site is followable on foot",
            "the heating main visibly originates here",
        ],
    },
    "hardened_technical": {
        "domain": "technical_program",
        "repeatable_storey": False,
        "site_context": "industrial_hardstanding",
        "foundation_profile": "full_basement",
        "district_role": "restricted",
        "heating_main_connection": "below_slab",
        "rooms": [
            "a hardened envelope with few openings and a single controlled entrance",
            "an airlock or double-door screening lobby inside the entrance",
            "a principal technical hall on a raised floor",
            "a plant room with air handling and suppression equipment",
            "a secure store or archive vault below grade",
            "a control and monitoring room glazed onto the technical hall",
            "a decontamination or changing suite adjacent to the lobby",
            "a fenced perimeter with a gate house and floodlights",
        ],
        "circulation": [
            "everyone entering passes the screening lobby; there is no second public way in",
            "the below-grade vault is reached from inside the envelope only",
        ],
        "damage": [
            "the public levels are open to the sky; the below-grade vault is dry, sealed and still holding its contents",
            "the screening lobby remains identifiable",
        ],
        "review": [
            "the building reads as restricted before any sign is read",
            "the contrast between the ruined upper levels and the intact vault is unmistakable",
        ],
    },
    "switchyard": {
        "domain": "utility_program",
        "repeatable_storey": False,
        "site_context": "industrial_hardstanding",
        "foundation_profile": "surface",
        "district_role": "utility_node",
        "heating_main_connection": None,
        "rooms": [
            "an open switchyard of gantries, bus bars and insulator stacks",
            "a brick or concrete control building at the yard edge",
            "a relay and battery room inside the control building",
            "transformer bays on bunded plinths",
            "a cable trench route from the transformers into the control building",
            "a secure perimeter fence with a single gate and floodlights",
        ],
        "circulation": ["the yard is entered through one gate", "the cable trench route is traceable"],
        "damage": [
            "the yard has been stripped of switchgear: cut cable ends, empty plinths and drag marks toward the gate",
            "the control building stands and its relay room is intact",
        ],
        "review": ["the absence of the removed equipment is the story", "the drag route out of the gate is followable"],
    },
    "warehouse_depot": {
        "domain": "logistics_program",
        "repeatable_storey": False,
        "site_context": "karsic_rail_ballast",
        "foundation_profile": "surface",
        "district_role": "freight",
        "heating_main_connection": None,
        "rail_served": True,
        "rooms": [
            "a long storage hall with numbered bays marked on the floor",
            "a rail-side loading platform at wagon-floor height under a gantry",
            "a road-side loading dock with levellers",
            "a dispatcher's office with a window onto both loading faces",
            "a sealed goods store with a heavier door",
            "a staff room and wash block at the workers' entrance",
            "a rail siding stub reaching the template edge",
        ],
        "circulation": ["goods move rail-side to hall to road-side without doubling back"],
        "damage": [
            "part of the roof has failed over the road-side bays; the rail-side platform is intact",
            "the numbered bay markings survive",
        ],
        "review": ["the bay numbering system is consistent and legible", "the rail siding reaches the template edge"],
    },
    "extraction_site": {
        "domain": "industrial_program",
        "repeatable_storey": False,
        "site_context": "industrial_hardstanding",
        "foundation_profile": "surface",
        "district_role": "extraction",
        "heating_main_connection": None,
        "rail_served": True,
        "rooms": [
            "an excavation with worked faces, benches and haul route",
            "a winding, crushing or pumping structure at the excavation edge",
            "a processing shed with a conveyor to a loading point",
            "a rail or road loading point with a weigh house",
            "a changing and wash block for the workforce",
            "a spoil ridge or tip placed downwind of the workings",
            "a workshop with spare-parts storage",
        ],
        "circulation": ["the haul route from face to processing to loading is continuous and followable"],
        "damage": [
            "the machinery has been cannibalised for parts; the excavation and haul route remain",
            "the changing block survives",
        ],
        "review": ["the extraction geometry is specific to this material, not a generic hole"],
    },
    "tank_farm": {
        "domain": "industrial_program",
        "repeatable_storey": False,
        "site_context": "industrial_hardstanding",
        "foundation_profile": "surface",
        "district_role": "utility_anchor",
        "heating_main_connection": None,
        "rail_served": True,
        "rooms": [
            "cylindrical storage tanks inside bunded enclosures",
            "a rail loading rack with a walkway over the wagons",
            "a pump house with a manifold and valve set",
            "a fire water main and monitor positions around the bund",
            "a control and gauging hut with sight of the loading rack",
            "a secure perimeter with one gate",
        ],
        "circulation": ["the pipe route from tank to pump house to loading rack is traceable above ground"],
        "damage": [
            "one tank has burnt out and its bund is scorched; adjacent tanks are heat-blistered but standing",
            "the fire main and monitors are in place and were used",
        ],
        "review": ["the fire actually reads as having been fought, not merely as damage"],
    },
    "open_yard": {
        "domain": "logistics_program",
        "repeatable_storey": False,
        "site_context": "karsic_rail_ballast",
        "foundation_profile": "surface",
        "district_role": "yard",
        "heating_main_connection": None,
        "rooms": [
            "a large open working surface with a defined vehicle route",
            "a low workshop or office building at the yard edge",
            "inspection pits or racking appropriate to what the yard handles",
            "sorted stacks or rows of the yard's material",
            "a gate house controlling the single entrance",
            "a fenced perimeter",
        ],
        "circulation": ["one gate, one vehicle loop, no dead ends for a long vehicle"],
        "damage": ["the yard is still sorted; the sorting has simply stopped mid-task"],
        "review": ["the sorting logic is inferable from the arrangement of what is stacked"],
    },
    "port_apron": {
        "domain": "logistics_program",
        "repeatable_storey": False,
        "site_context": "waterfront",
        "foundation_profile": "surface",
        "district_role": "freight",
        "heating_main_connection": "quay_basement",
        "rail_served": True,
        "rooms": [
            "a quay wall with bollards and fenders",
            "a rail apron running the length of the quay under a gantry crane",
            "a heated transit warehouse behind the apron",
            "a port office with sight of the quay",
            "a fuel and water point for vessels",
            "a workshop and wash block",
        ],
        "circulation": ["quay to apron to warehouse to rail is a continuous handling route"],
        "damage": ["the gantry is derailed at one end of its travel; the quay and warehouse stand"],
        "review": ["the handling sequence is followable from the water inland"],
    },
    "transit_hall": {
        "domain": "transit_program",
        "repeatable_storey": False,
        "site_context": "urban_paved",
        "foundation_profile": "full_basement",
        "district_role": "assembly_point",
        "heating_main_connection": "below_concourse",
        "rooms": [
            "a public concourse with a ticket hall and a departure board",
            "a covered platform or stand area with a cantilevered canopy",
            "a waiting room with benches and a stove or radiator bank",
            "a left-luggage counter and a small buffet",
            "staff and dispatcher rooms with sight of the platforms",
            "a below-grade service level with plant and stores",
            "queue barriers and a numbered boarding order marked on the ground",
        ],
        "circulation": [
            "the route from street to concourse to platform is direct and step-free at least once",
            "the dispatcher can see the platforms",
        ],
        "damage": [
            "the concourse shows an evacuation that failed: barriers in place, abandoned baggage, a departure board frozen mid-update",
            "no vehicle remains at the platforms",
            "the below-grade service level is intact",
        ],
        "review": [
            "the boarding order painted on the ground is readable and implies a plan that existed",
            "the canopy reads as cantilevered rather than propped",
        ],
    },
    "bunker": {
        "domain": "technical_program",
        "repeatable_storey": False,
        "site_context": "wilderness_undisturbed",
        "foundation_profile": "full_basement",
        "district_role": "restricted",
        "heating_main_connection": None,
        "rooms": [
            "a low surface entrance structure that gives away little",
            "a stair or ramp descending to a blast door",
            "an airlock lobby with a filter plant room beside it",
            "a principal below-grade room appropriate to the bunker's purpose",
            "bunk or store bays off the principal room",
            "a water tank, latrine and ventilation shaft",
            "an emergency exit shaft reaching the surface separately from the entrance",
        ],
        "circulation": [
            "two independent ways to the surface",
            "the blast door is on the route and is passable",
        ],
        "damage": [
            "the surface structure is damaged; everything below the blast door is dry and intact",
            "the emergency shaft remains usable",
        ],
        "review": ["the below-grade level reads as still habitable", "the two exits are genuinely independent"],
    },
    "checkpoint": {
        "domain": "military_program",
        "repeatable_storey": False,
        "site_context": "urban_paved",
        "foundation_profile": "surface",
        "district_role": "control",
        "heating_main_connection": None,
        "rooms": [
            "a barrier across the carriageway with a lifting arm",
            "a glazed observation post with sight of both approaches",
            "a vehicle inspection bay off the running lane",
            "a guard block with a stove, bunks and a weapons store",
            "a documents window facing the queueing side",
            "concrete blocks and barriers forming a slalom approach",
        ],
        "circulation": ["the slalom forces a slow approach past the observation post"],
        "damage": ["the barrier is down and the slalom is still in place; the guard block is abandoned in a hurry"],
        "review": ["the approach geometry makes the checkpoint's intent obvious from a distance"],
    },
    "appliance_hall": {
        "domain": "civic_program",
        "repeatable_storey": False,
        "site_context": "urban_paved",
        "foundation_profile": "partial_basement",
        "district_role": "district_service",
        "heating_main_connection": "rear_basement",
        "rooms": [
            "a run of tall vehicle bays opening directly to the street",
            "a watch room with sight of the bays and the approach",
            "a drill or hose tower attached to the rear",
            "dormitory and mess rooms on the upper floor",
            "a locker and drying room beside the bays",
            "a rear yard with a hardstanding and a fuel point",
        ],
        "circulation": [
            "crew reach the bays from the upper floor without crossing the watch room",
            "vehicles leave forward onto the street without reversing",
        ],
        "damage": ["the bays are empty and their doors are open; the tower stands"],
        "review": ["the bays read as vehicle bays, not as a warehouse"],
    },
    "farmstead": {
        "domain": "agricultural_program",
        "repeatable_storey": False,
        "site_context": "rural_worked",
        "foundation_profile": "surface",
        "district_role": "rural_unit",
        "heating_main_connection": "barn_end",
        "rail_served": False,
        "rooms": [
            "long parallel barn ranges of identical design on one axis",
            "a machine yard with a repair shed and a fuel point",
            "a silo or feed store bank",
            "a workers' block with a canteen and wash room",
            "a small boiler house serving the heated barn",
            "field access tracks leaving the yard",
        ],
        "circulation": ["one yard serves every range; tracks leave it to the fields"],
        "damage": ["one range has lost its roof; the boiler house and the machine yard survive"],
        "review": ["the site reads as designed as a system, not accumulated over time"],
    },
    "silo_bank": {
        "domain": "agricultural_program",
        "repeatable_storey": False,
        "site_context": "karsic_rail_ballast",
        "foundation_profile": "surface",
        "district_role": "freight",
        "rail_served": True,
        "heating_main_connection": None,
        "rooms": [
            "a bank of identical cylindrical silos rising well above everything around",
            "a headhouse above the silos carrying the conveyor gallery",
            "a conveyor gallery bridging from the headhouse to the rail loading point",
            "a rail scale house and loading spout over the siding",
            "an intake pit with a truck tipping ramp",
            "a control room with sight of the intake and the loading point",
        ],
        "circulation": ["grain path from intake to silo to gallery to wagon is continuous and visible"],
        "damage": ["one silo has split down its side and spilled; the gallery and headhouse stand"],
        "review": ["the silhouette reads on the horizon from well outside the site"],
    },
    "greenhouse_range": {
        "domain": "agricultural_program",
        "repeatable_storey": False,
        "site_context": "rural_worked",
        "foundation_profile": "surface",
        "district_role": "rural_unit",
        "heating_main_connection": "boiler_on_lot",
        "rooms": [
            "parallel glazed growing ranges on a shared service spine",
            "a boiler house on the lot with its main running to every range",
            "growing beds and irrigation runs inside each range",
            "a potting and packing shed at the spine head",
            "a cold store beside the packing shed",
            "a small office and wash room",
        ],
        "circulation": ["the service spine reaches every range without entering the growing beds"],
        "damage": [
            "the boiler has failed and the ranges furthest from it are frost-killed while the nearest still hold growth",
            "the glazing is largely gone; the frames stand",
        ],
        "review": ["the gradient of survival away from the boiler is visible at a glance"],
    },
    "memorial": {
        "domain": "civic_program",
        "repeatable_storey": False,
        "site_context": "urban_paved",
        "foundation_profile": "surface",
        "district_role": "axial_terminus",
        "heating_main_connection": None,
        "rooms": [
            "a paved terrace approached on a single axis",
            "a tall plain obelisk or monolith on the axis",
            "a wall of names flanking the approach",
            "an eternal-flame plinth at the foot of the monument",
            "low planting and benches at the terrace edge",
            "a boundary of standard fencing and lamp standards",
        ],
        "circulation": ["the approach is axial and unobstructed"],
        "damage": ["the flame is out and the plinth is cracked; the monument and the wall of names stand"],
        "review": ["the site carries civic weight without any national emblem"],
    },
    "civic_square": {
        "domain": "civic_program",
        "repeatable_storey": False,
        "site_context": "urban_paved",
        "foundation_profile": "partial_basement",
        "district_role": "axial_terminus",
        "heating_main_connection": "below_square",
        "rooms": [
            "a broad paved square terminating an axial boulevard",
            "institutional frontages on at least two sides",
            "a monument or fountain on the axis",
            "trolleybus or tram catenary poles along the boulevard",
            "an underpass or service stair below the square",
            "standard lamp standards, bollards and notice boards",
        ],
        "circulation": ["the boulevard axis is unobstructed to the terminating frontage"],
        "damage": ["a crater interrupts the square; the axis and the terminating frontage remain readable"],
        "review": ["the square reads as designed around the axis, not as a gap between buildings"],
    },
    "roadside_service": {
        "domain": "commercial_program",
        "repeatable_storey": False,
        "site_context": "urban_paved",
        "foundation_profile": "surface",
        "district_role": "roadside",
        "heating_main_connection": None,
        "rooms": [
            "a forecourt or apron addressing the road directly",
            "a single-storey service building with a serving counter",
            "communal tables rather than booths",
            "a driver rest or dormitory bay",
            "a wash room and a small kitchen store",
            "a canopy over the working area of the forecourt",
        ],
        "circulation": ["vehicles enter and leave the forecourt without reversing"],
        "damage": ["the canopy has partly collapsed; the service building stands"],
        "review": ["the seating reads as communal, never as booths"],
    },
    "mast_tower": {
        "domain": "utility_program",
        "repeatable_storey": False,
        "site_context": "wilderness_undisturbed",
        "foundation_profile": "surface",
        "district_role": "utility_node",
        "heating_main_connection": None,
        "rooms": [
            "a slender vertical structure on a substantial concrete footing",
            "a service ladder with a backing structure the full height",
            "a head assembly appropriate to the tower's function",
            "a small equipment hut at the base",
            "a cable or pipe route from the hut to the head",
            "a fenced compound three blocks clear of the structure",
        ],
        "circulation": ["the ladder reaches a real platform, never open air"],
        "damage": ["the head assembly is damaged; the structure and ladder remain climbable"],
        "review": ["the silhouette is legible from a long distance", "the footing is proportionate to the height"],
    },
    "kiosk": {
        "domain": "utility_program",
        "repeatable_storey": False,
        "site_context": "urban_paved",
        "foundation_profile": "surface",
        "district_role": "street_furniture",
        "heating_main_connection": None,
        "rooms": [
            "a single small windowless or slot-windowed volume",
            "a ventilation louvre on at least one face",
            "one service door with a hasp",
            "the equipment or shelter function the kiosk exists for",
            "a hazard plate and a numbered identification plate",
        ],
        "circulation": ["one door, opening outward onto a hard surface"],
        "damage": ["the door is forced and the interior stripped; the shell is intact"],
        "review": ["it recurs identically wherever it appears; that recurrence is the point"],
    },
    "linear_infrastructure": {
        "domain": "infrastructure_program",
        "repeatable_storey": False,
        "site_context": "karsic_district_yard",
        "foundation_profile": "surface",
        "district_role": "network",
        "heating_main_connection": "through_run",
        "tiling": True,
        "rooms": [
            "a continuous run whose ends meet the template edge at matching heights and offsets",
            "regular supports or saddles at a fixed spacing",
            "one crossing structure where the run steps over a road or track",
            "an access or inspection point along the run",
            "hazard marking where the run is at head height",
        ],
        "circulation": ["the run is continuous; consecutive placements read as one system"],
        "damage": ["the run is severed at one support, with the break visible and the ends displaced"],
        "review": [
            "two copies placed end to end read as a single continuous run",
            "the break is findable and obviously the cause of what failed downstream",
        ],
    },
    "field_array": {
        "domain": "utility_program",
        "repeatable_storey": False,
        "site_context": "rural_worked",
        "foundation_profile": "surface",
        "district_role": "utility_node",
        "heating_main_connection": None,
        "rooms": [
            "a regular array of identical units on a field",
            "a small inverter or control cabin at the array edge",
            "a cable route from the array to the cabin",
            "a perimeter fence with one gate and an import plate",
            "an access track from the road to the gate",
        ],
        "circulation": ["one gate, one track, service lanes between array rows"],
        "damage": ["units are down in a wind-driven pattern rather than at random; the cabin stands"],
        "review": [
            "the equipment reads as foreign to the region and the import plate explains why it is here",
            "no housing, no heating main, no settlement around it",
        ],
    },
    "camp_row": {
        "domain": "residential_program",
        "repeatable_storey": False,
        "site_context": "karsic_district_yard",
        "foundation_profile": "surface",
        "district_role": "temporary_settlement",
        "heating_main_connection": None,
        "rooms": [
            "rows of identical cabins raised on blocks above the ground",
            "a canteen cabin larger than the rest",
            "a generator and fuel store serving the camp",
            "a drying and boot room cabin",
            "a wash block and latrine at the row end",
            "duckboard walkways between the rows",
        ],
        "circulation": ["duckboards connect every cabin to the canteen and the wash block"],
        "damage": ["some cabins have been stripped for material to repair others; the canteen survives"],
        "review": ["the camp reads as temporary accommodation that stayed too long"],
    },
    "wreck_scene": {
        "domain": "infrastructure_program",
        "repeatable_storey": False,
        "site_context": "urban_paved",
        "foundation_profile": "surface",
        "district_role": "roadside",
        "heating_main_connection": None,
        "rooms": [
            "the wrecked vehicles or vessel arranged as a single readable event",
            "a debris field consistent with the direction of travel",
            "evidence of the people who were with it",
            "any barrier, marking or instruction that was in force at the time",
        ],
        "circulation": ["the scene can be walked through and read in one direction"],
        "damage": ["the event is the asset; damage is authored as the event itself"],
        "review": ["a player can tell what happened and which way it was going without any text"],
    },
    "prop_vehicle": {
        "domain": "infrastructure_program",
        "repeatable_storey": False,
        "site_context": "urban_paved",
        "foundation_profile": "surface",
        "district_role": "roadside",
        "heating_main_connection": None,
        "rooms": [
            "a boxy body with a clear cab, load and running-gear division",
            "wheels or tracks seated on the ground surface",
            "one opened or missing panel showing the interior",
            "a numbered plate consistent with the regional signage grammar",
        ],
        "circulation": ["not applicable"],
        "damage": ["the vehicle stopped where it failed and was then stripped of anything useful"],
        "review": ["the silhouette is regionally distinct at prop scale"],
    },
}

CULTURES = {
    "karsic": {
        "prefix": "kar",
        "types": KARSIC_TYPES,
        "templates": KARSIC_TEMPLATES,
        "doc": "docs/KARSIC_DIRECTORATE_STRUCTURE_PROGRAM.md",
    },
}

# Family membership, from section 14.1 of each program document.
KARSIC_FAMILIES: dict[str, list[str]] = {
    "KF1": ["kar_010", "kar_021", "kar_024", "kar_067", "kar_069", "kar_071", "kar_086", "kar_090"],
    "KF2": ["kar_031", "kar_038", "kar_045", "kar_057", "kar_078", "kar_081", "kar_083", "kar_084", "kar_085", "kar_089"],
    "KF3": ["kar_006", "kar_011", "kar_012", "kar_018", "kar_064", "kar_070", "kar_091", "kar_092"],
    "KF4": ["kar_039", "kar_040", "kar_042", "kar_043", "kar_044", "kar_046", "kar_047", "kar_048",
            "kar_049", "kar_050", "kar_052", "kar_053", "kar_054", "kar_055", "kar_056"],
    "KF5": ["kar_051", "kar_072", "kar_073", "kar_074", "kar_075", "kar_076", "kar_077", "kar_079", "kar_082"],
    "KF6": ["kar_004", "kar_034", "kar_035", "kar_036", "kar_062", "kar_065", "kar_066"],
    "KF7": ["kar_001", "kar_002", "kar_003", "kar_005", "kar_009", "kar_016", "kar_068", "kar_080",
            "kar_087", "kar_088", "kar_093"],
    "KF8": ["kar_007", "kar_032", "kar_058", "kar_059", "kar_060", "kar_061", "kar_063", "kar_094"],
    "KF9": ["kar_008", "kar_013", "kar_014", "kar_015", "kar_017", "kar_019", "kar_022", "kar_023",
            "kar_025", "kar_026", "kar_027", "kar_030", "kar_033", "kar_037", "kar_041"],
    "KF10": ["kar_020", "kar_028", "kar_029"],
}
FAMILIES = {"karsic": KARSIC_FAMILIES}


def ordinal_for(regional_id: str, low: int, high: int) -> int:
    """Deterministic institutional ordinal, per the naming grammar."""
    import zlib
    span = high - low + 1
    return low + (zlib.crc32(regional_id.encode("utf-8")) % span)


def signage_series(regional_id: str, identity: str, building_type: str) -> str:
    """The Directorate numbers things; the grammar carries the culture."""
    upper = identity.upper()
    if building_type in ("prop_vehicle", "wreck_scene"):
        return f"{upper} / PLATE {ordinal_for(regional_id, 100, 999)}"
    if building_type in ("machine_hall", "process_plant", "extraction_site", "tank_farm"):
        return f"{upper} {ordinal_for(regional_id, 1, 9)} / SHOP {ordinal_for(regional_id + 'shop', 1, 24)}"
    if building_type in ("panel_slab", "courtyard_block", "courtyard_group", "barrack_row", "camp_row"):
        return f"SERIES {ordinal_for(regional_id, 1, 9)} / BLOCK {ordinal_for(regional_id + 'block', 1, 48)}"
    if building_type in ("hospital_korpus", "school_block"):
        return f"{upper} {ordinal_for(regional_id, 1, 9)} / SECTION {chr(65 + ordinal_for(regional_id + 'sec', 0, 5))}"
    return f"{upper} {ordinal_for(regional_id, 1, 9)}"


def build_program(entry: dict[str, Any], catalog: dict[str, Any], spec: dict[str, Any]) -> dict[str, Any]:
    rid = entry["regional_id"]
    building_type = spec["types"][rid]
    template = spec["templates"][building_type]
    strata = entry.get("strata") or []
    primary = strata[0] if strata else "prop"
    secondary = strata[1] if len(strata) > 1 else None

    base = entry.get("base_master")
    meta = catalog.get(base, {}) if base else {}

    program: dict[str, Any] = {
        "structure_id": f"infinite_domain:{rid}",
        "culture": spec_name(spec),
        "building_type": building_type,
        "conversion_class": entry.get("conversion_class", "N"),
        "base_master": base,
        "primary_stratum": primary,
        "secondary_stratum": secondary,
        "repeatable_storey": bool(template.get("repeatable_storey", False)),
        "site_context": template["site_context"],
        "foundation_profile": template["foundation_profile"],
        "back_of_house": "below" if primary == "K-IV" else "behind",
        "district_role": template["district_role"],
        "rail_served": bool(template.get("rail_served", False)),
        "heating_main_connection": template.get("heating_main_connection"),
        "tiling_asset": bool(template.get("tiling", False)),
        "signage_series": signage_series(rid, entry.get("identity") or rid, building_type),
        "archetype": entry.get("identity") or rid,
        "roster_note": entry.get("note", ""),
        "damage_archetype": entry.get("damage_archetype"),
        template["domain"]: list(template["rooms"]),
        "circulation": list(template["circulation"]),
        "damage_constraints": list(template["damage"]) + [
            "derive all damage and occupation only from the immutable clean master",
            "use an authored fracture with a gravity-consistent rubble apron, never a cleared box "
            "and never per-block random deletion",
        ],
        "review_gate": {
            "automatic_checks_are_approval": False,
            "required_previews": ["exterior_a", "exterior_b", "roof_off_cutaway", "floor_slices"],
            "required_manual_checks": list(template["review"]),
        },
    }
    if meta:
        program["source_metadata"] = {
            "category": meta.get("category"),
            "settlement_types": meta.get("settlement_types"),
            "road_connection": meta.get("road_connection"),
            "base_footprint": meta.get("footprint"),
            "base_height": meta.get("height"),
            "conversion_target": meta.get("conversion_target"),
        }
    return program


def spec_name(spec: dict[str, Any]) -> str:
    for name, value in CULTURES.items():
        if value is spec:
            return name
    return "unknown"


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--culture", required=True, choices=sorted(CULTURES))
    parser.add_argument("--family", nargs="*", help="limit to these families, e.g. KF1 KF2")
    parser.add_argument("--check", action="store_true", help="verify files exist and match, do not write")
    args = parser.parse_args()

    spec = CULTURES[args.culture]
    assignment = json.loads((REGIONAL / f"{args.culture}-assignment.json").read_text(encoding="utf-8"))
    catalog = {
        e["structure_id"].split(":", 1)[1].removesuffix("_clean_master"): e
        for e in json.loads(CATALOG.read_text(encoding="utf-8"))["structures"]
        if e["source_role"] == "clean_master"
    }

    entries = [e for e in assignment["conversions"] if e["conversion_class"] != "X"] + assignment["natives"]

    if args.family:
        wanted: set[str] = set()
        for family in args.family:
            members = FAMILIES[args.culture].get(family)
            if members is None:
                parser.error(f"unknown family {family}")
            wanted.update(members)
        entries = [e for e in entries if e["regional_id"].rsplit("_", maxsplit=99)[0][:7] in wanted
                   or "_".join(e["regional_id"].split("_")[:2]) in wanted]

    missing_types = [e["regional_id"] for e in entries if e["regional_id"] not in spec["types"]]
    if missing_types:
        print(f"FAIL  {len(missing_types)} master(s) have no building type mapping:")
        for rid in missing_types:
            print(f"  - {rid}")
        return 1

    missing_templates = sorted({spec["types"][e["regional_id"]] for e in entries} - set(spec["templates"]))
    if missing_templates:
        print(f"FAIL  {len(missing_templates)} building type(s) have no template:")
        for name in missing_templates:
            print(f"  - {name}")
        return 1

    PROGRAMS.mkdir(parents=True, exist_ok=True)
    written = 0
    drift: list[str] = []
    type_counts: dict[str, int] = {}

    for entry in entries:
        program = build_program(entry, catalog, spec)
        path = PROGRAMS / f"{entry['regional_id']}.json"
        type_counts[program["building_type"]] = type_counts.get(program["building_type"], 0) + 1
        if args.check:
            if not path.exists():
                drift.append(f"missing: {path.name}")
            elif json.loads(path.read_text(encoding="utf-8")) != program:
                drift.append(f"drifted: {path.name}")
        else:
            path.write_text(json.dumps(program, indent=2) + "\n", encoding="utf-8", newline="\n")
            written += 1

    if args.check:
        if drift:
            print(f"FAIL  {len(drift)} program(s) differ:")
            for d in drift[:20]:
                print(f"  - {d}")
            return 1
        print(f"PASS  {len(entries)} programs match the authored templates")
        return 0

    print(f"culture         {args.culture}")
    print(f"programs written {written} -> {PROGRAMS.relative_to(ROOT).as_posix()}")
    print(f"building types   {len(type_counts)}")
    for name, count in sorted(type_counts.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"  {name:<24} {count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
