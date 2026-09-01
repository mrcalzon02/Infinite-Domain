from __future__ import annotations

import json
import math
import re
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[3]
KUBEJS = ROOT / "kubejs"
NS = "kubejs"

# This file is the authoritative catalog for the pack's Stellaris expansion.
# Generated startup scripts, recipes, worldgen, quest hooks and textures must
# not be hand-edited; update these definitions and rerun this generator.

COMPONENT_FAMILIES = {
    "structure": {
        "color": (91, 132, 153),
        "items": [
            ("aerospace_aluminum_sheet", "Aerospace Aluminum Sheet", "Formed, inspected light-alloy skin"),
            ("desh_titanium_laminate", "Desh-Titanium Laminate", "Lunar laminate for pressure structures"),
            ("structural_truss", "Aerospace Structural Truss", "Load-bearing launch vehicle framing"),
            ("reinforced_frame", "Reinforced Aerospace Frame", "Machined frame for major assemblies"),
            ("pressure_bulkhead", "Pressure Bulkhead", "Sealed crew-volume divider"),
            ("incomplete_fuselage_section", "Incomplete Fuselage Section", "Partially assembled pressure-rated vehicle barrel"),
            ("fuselage_section", "Fuselage Section", "Complete pressure-rated vehicle barrel"),
            ("landing_gear_assembly", "Landing Gear Assembly", "Shock-isolated planetary landing structure"),
            ("payload_adapter", "Payload Adapter", "Standardized cargo and mission interface"),
        ],
    },
    "pressure": {
        "color": (72, 153, 194),
        "items": [
            ("pressure_vessel", "Basic Pressure Vessel", "Terrestrial gas-process vessel"),
            ("reinforced_pressure_vessel", "Reinforced Pressure Vessel", "High-cycle industrial vessel"),
            ("aerospace_pressure_vessel", "Aerospace Pressure Vessel", "Mass-efficient flight vessel"),
            ("venus_pressure_vessel", "Venus-Rated Pressure Vessel", "Extreme-temperature pressure hardware"),
            ("precision_valve", "Precision Valve", "Metered process-fluid control"),
            ("high_pressure_valve", "High-Pressure Valve", "Reinforced gas-service valve"),
            ("cryogenic_valve", "Cryogenic Valve", "Low-temperature propellant valve"),
            ("aerospace_pump", "Aerospace Pump", "Compact flight-qualified turbopump feed"),
            ("oxygen_manifold", "Oxygen Manifold", "Clean-service oxygen distribution"),
            ("propellant_manifold", "Propellant Manifold", "Redundant engine feed distribution"),
            ("empty_gas_cylinder", "Empty Gas Cylinder", "Reusable compressed-gas logistics vessel"),
            ("oxygen_cylinder", "Oxygen Cylinder", "Filled personal and habitat oxygen supply"),
            ("hydrogen_cylinder", "Hydrogen Cylinder", "Filled hydrogen process supply"),
            ("methane_cylinder", "Methane Cylinder", "Filled synthetic propellant supply"),
        ],
    },
    "electronics": {
        "color": (79, 190, 151),
        "items": [
            ("sensor_package", "Aerospace Sensor Package", "Pressure, temperature and motion instrumentation"),
            ("guidance_computer", "Guidance Computer", "Redundant launch guidance electronics"),
            ("navigation_unit", "Navigation Unit", "Interplanetary position and burn solution unit"),
            ("telemetry_array", "Telemetry Array", "Long-range vehicle health reporting"),
            ("power_distribution_unit", "Power Distribution Unit", "Fault-isolated aerospace power bus"),
            ("incomplete_avionics_controller", "Incomplete Avionics Controller", "Partially integrated flight-control electronics"),
            ("avionics_controller", "Avionics Controller", "Flight-rated control electronics"),
            ("radiation_hardened_controller", "Radiation-Hardened Controller", "Lunar rare-earth hardened control package"),
            ("flight_control_computer", "Flight Control Computer", "Triple-redundant mission controller"),
            ("avionics_bay", "Avionics Bay", "Integrated guidance, telemetry and power section"),
        ],
    },
    "thermal": {
        "color": (224, 126, 64),
        "items": [
            ("ceramic_fiber", "Ceramic Fiber", "High-temperature woven insulation"),
            ("thermal_shield_tile", "Thermal Shield Tile", "Reusable atmospheric-entry tile"),
            ("ablative_panel", "Ablative Panel", "Sacrificial high-heat protection"),
            ("radiation_laminate", "Radiation Shield Laminate", "Layered nuclear-era shielding"),
            ("structural_composite", "Structural Composite", "Fiber-reinforced vehicle material"),
            ("aerospace_composite", "Aerospace Composite", "Vacuum-rated lightweight composite"),
            ("extreme_environment_composite", "Extreme-Environment Composite", "Venusian refractory composite"),
            ("thermal_protection_package", "Thermal Protection Package", "Complete entry and engine heat system"),
        ],
    },
    "life_support": {
        "color": (92, 195, 219),
        "items": [
            ("electrolysis_membrane", "Electrolysis Membrane", "Reusable terrestrial water-splitting element"),
            ("carbon_scrubber", "Carbon Scrubber Cartridge", "Replaceable carbon-dioxide sorbent bed"),
            ("spent_scrubber", "Spent Scrubber Cartridge", "Loaded cartridge ready for regeneration"),
            ("humidity_reclaimer", "Humidity Reclaimer", "Condensate recovery and sterilization unit"),
            ("oxygen_regulator", "Oxygen Regulator", "Suit and habitat breathing-gas regulator"),
            ("life_support_controller", "Life-Support Controller", "Atmosphere monitoring and emergency isolation"),
            ("incomplete_life_support_assembly", "Incomplete Life-Support Assembly", "Partially plumbed closed-loop atmosphere plant"),
            ("closed_loop_life_support", "Closed-Loop Life-Support Assembly", "High-efficiency habitat atmosphere plant"),
            ("life_support_module", "Vehicle Life-Support Module", "Crewed-flight atmosphere and thermal package"),
        ],
    },
    "propulsion": {
        "color": (207, 84, 72),
        "items": [
            ("injector_plate", "Engine Injector Plate", "Precision propellant atomization plate"),
            ("incomplete_turbopump", "Incomplete Rocket Turbopump", "Partially assembled high-speed propellant pump"),
            ("turbopump", "Rocket Turbopump", "High-speed propellant feed assembly"),
            ("combustion_chamber", "Combustion Chamber", "Regeneratively cooled engine chamber"),
            ("engine_nozzle", "Engine Nozzle", "High-expansion refractory exhaust bell"),
            ("gimbal_actuator", "Gimbal Actuator", "Thrust-vector control actuator"),
            ("ignition_controller", "Ignition Controller", "Sequenced, redundant engine ignition"),
            ("petroleum_engine_assembly", "Petroleum Engine Assembly", "Rugged high-thrust terrestrial engine"),
            ("methalox_engine_assembly", "Methalox Engine Assembly", "Efficient Mars-supported engine"),
            ("hydrogen_engine_assembly", "Hydrogen Engine Assembly", "High-efficiency cryogenic engine"),
            ("propellant_tank_section", "Propellant Tank Section", "Insulated dual-propellant vehicle section"),
            ("service_module", "Vehicle Service Module", "Power, propulsion and life-support services"),
        ],
    },
    "planetary": {
        "color": (181, 151, 93),
        "items": [
            ("crushed_ilmenite", "Crushed Lunar Ilmenite", "Oxygen-bearing titanium feed"),
            ("lunar_oxygen_feed", "Reduced Lunar Oxygen Feed", "Prepared mineral oxygen charge"),
            ("titanium_concentrate", "Titanium Concentrate", "Refined lunar titanium feedstock"),
            ("rare_earth_concentrate", "KREEP Rare-Earth Concentrate", "Lunar electronics and catalyst feed"),
            ("helium3_adsorbate", "Helium-3 Regolith Adsorbate", "Concentrated volatile-bearing regolith"),
            ("lunar_ceramic", "Lunar Structural Ceramic", "Locally fired construction ceramic"),
            ("crushed_hematite", "Crushed Martian Hematite", "Iron-rich Martian process feed"),
            ("sulfate_salts", "Martian Sulfate Salts", "Chemical and construction feedstock"),
            ("perchlorate_salts", "Martian Perchlorate Salts", "Hazardous oxidizer-bearing salts"),
            ("nickel_cobalt_concentrate", "Martian Nickel-Cobalt Concentrate", "Catalyst and superalloy feed"),
            ("brine_salts", "Martian Brine Salts", "Hydrated local chemical feed"),
            ("martian_catalyst", "Martian Methanation Catalyst", "Nickel-cobalt catalyst for synthetic fuel"),
            ("martian_geopolymer", "Martian Structural Geopolymer", "Locally cast sulfate-silicate construction material"),
            ("sulfur_concentrate", "Venusian Sulfur Concentrate", "High-purity sulfur process feed"),
            ("vanadium_concentrate", "Vanadium Concentrate", "Extreme-alloy additive"),
            ("tungsten_concentrate", "Tungsten Concentrate", "Refractory metal feedstock"),
            ("refractory_concentrate", "Exotic Refractory Concentrate", "Venusian extreme-material feed"),
            ("venus_atmospheric_sorbent", "Venus Atmospheric Sorbent", "Loaded high-pressure atmospheric capture bed"),
            ("venus_superalloy", "Venusian Superalloy", "Cross-planet high-temperature structural alloy"),
        ],
    },
    "logistics": {
        "color": (161, 112, 67),
        "items": [
            ("structural_parts_crate", "Structural Parts Crate", "Count-preserving aerospace parts shipment"),
            ("life_support_crate", "Life-Support Supply Crate", "Filters, seals and atmosphere hardware"),
            ("avionics_crate", "Avionics Crate", "Shock-isolated electronics shipment"),
            ("propellant_equipment_crate", "Propellant Equipment Crate", "Valves, pumps and manifold shipment"),
            ("lunar_material_pallet", "Lunar Materials Pallet", "Bulk return shipment of lunar products"),
            ("martian_chemical_pallet", "Martian Chemical Pallet", "Bulk ISRU chemical shipment"),
            ("venus_material_pallet", "Venus Materials Pallet", "Extreme-material interplanetary shipment"),
        ],
    },
    "mission": {
        "color": (158, 104, 199),
        "items": [
            ("earth_launch_package", "Earth Launch Package", "High-thrust petroleum mission fit"),
            ("lunar_cargo_package", "Lunar Cargo Package", "Cargo-efficient lunar logistics fit"),
            ("mars_transfer_package", "Mars Transfer Package", "Methalox-supported interplanetary fit"),
            ("venus_return_package", "Venus Return Package", "Extreme-environment return mission fit"),
            ("emergency_return_package", "Emergency Return Package", "Rugged low-capacity contingency fit"),
        ],
    },
    "archaeology": {
        "color": (96, 214, 190),
        "items": [
            ("meridian_core", "Meridian Core", "A silent lunar relic that remains aligned to an unknown celestial meridian"),
            ("martian_signal_prism", "Martian Signal Prism", "A crystalline transmitter repeating an incomplete coordinate sequence"),
            ("venusian_pressure_seal", "Venusian Pressure Seal", "An alien seal still holding an impossible internal pressure"),
            ("burrower_carapace", "Burrower Carapace", "A heat-scored plate shed by something vast beneath the Martian crust"),
            ("jovian_arena_standard", "Jovian Arena Standard", "A banner-crest salvaged from a coliseum that drifts, empty and silent, in Jupiter's storms"),
        ],
    },
}

ORES = [
    ("moon_ilmenite_ore", "Lunar Ilmenite", "moon", "stellaris:moon_stone", 8, 6, -48, 96, (101, 93, 111)),
    ("moon_anorthosite_ore", "Lunar Anorthosite", "moon", "stellaris:moon_stone", 11, 8, -32, 120, (205, 210, 200)),
    ("moon_kreep_ore", "Lunar KREEP Deposit", "moon", "stellaris:moon_stone", 5, 3, -48, 48, (111, 177, 165)),
    ("moon_helium_regolith", "Helium-Bearing Lunar Regolith", "moon", "stellaris:moon_stone", 7, 4, 32, 160, (178, 151, 91)),
    ("moon_silicate_ore", "Lunar Silicate Deposit", "moon", "stellaris:moon_stone", 12, 7, -32, 112, (127, 166, 190)),
    ("mars_hematite_ore", "Martian Hematite", "mars", "stellaris:mars_stone", 10, 7, -48, 96, (169, 69, 45)),
    ("mars_sulfate_ore", "Martian Sulfate Deposit", "mars", "stellaris:mars_stone", 8, 5, -32, 120, (213, 192, 143)),
    ("mars_perchlorate_ore", "Martian Perchlorate Deposit", "mars", "stellaris:mars_stone", 6, 4, -48, 72, (190, 166, 182)),
    ("mars_nickel_cobalt_ore", "Martian Nickel-Cobalt Deposit", "mars", "stellaris:mars_stone", 5, 3, -56, 40, (92, 145, 151)),
    ("mars_brine_ore", "Hydrated Martian Brine", "mars", "stellaris:mars_stone", 7, 4, -32, 80, (103, 159, 197)),
    ("mars_silicate_ore", "Martian Silicate Deposit", "mars", "stellaris:mars_stone", 11, 7, -24, 128, (193, 130, 91)),
    ("venus_sulfur_ore", "Venusian Sulfur Deposit", "venus", "stellaris:venus_stone", 9, 6, -32, 112, (224, 194, 54)),
    ("venus_vanadium_ore", "Venusian Vanadium Deposit", "venus", "stellaris:venus_stone", 5, 3, -48, 48, (93, 123, 108)),
    ("venus_tungsten_ore", "Venusian Tungsten Deposit", "venus", "stellaris:venus_stone", 4, 2, -56, 24, (138, 139, 148)),
    ("venus_refractory_ore", "Venusian Refractory Deposit", "venus", "stellaris:venus_stone", 4, 2, -56, 16, (183, 85, 54)),
]

SUITS = [
    ("emergency", "Emergency EVA", "High-visibility contingency suit; short-duration and deliberately compromised", (232, 127, 42)),
    ("surveyor", "Surveyor EVA", "Fast long-range exploration and terrain survey", (64, 164, 198)),
    ("lunar_prospector", "Lunar Prospector", "Low-gravity mining, low-light survey and moderate radiation work", (199, 184, 116)),
    ("radiation", "Radiation EVA", "Maximum exposure protection with reduced mobility", (208, 194, 44)),
    ("heavy", "Heavy EVA", "Armored expedition and dangerous-site work", (91, 104, 118)),
    ("mobility", "Mobility EVA", "Fast traversal and safer low-gravity landings", (95, 207, 145)),
    ("extended", "Extended Life-Support EVA", "Long-duration operation with expanded oxygen storage", (117, 123, 214)),
    ("martian", "Martian Field EVA", "Dust-resistant ISRU and construction operations", (184, 82, 54)),
    ("venusian", "Venusian Extreme EVA", "Refractory protection for Venus surface industry", (211, 112, 48)),
]


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def write_json(path: Path, value: object) -> None:
    write(path, json.dumps(value, indent=2) + "\n")


def merge_tag_values(path: Path, values: list[str]) -> None:
    """Add this subsystem's members without erasing members owned elsewhere."""
    existing: dict = {}
    if path.is_file():
        existing = json.loads(path.read_text(encoding="utf-8"))
    merged = list(dict.fromkeys([*existing.get("values", []), *values]))
    write_json(path, {"replace": False, "values": merged})


def generate_startup() -> None:
    rows = []
    for family, data in COMPONENT_FAMILIES.items():
        for item_id, name, tip in data["items"]:
            rows.append(f"        ['{item_id}', {json.dumps(name)}, {json.dumps(tip)}, '{family}']")
    ore_rows = [f"        ['{ore[0]}', {json.dumps(ore[1])}]" for ore in ORES]
    script = f"""// GENERATED by scripts/generate_stellaris_space_industry.py. Do not hand-edit.
const SPACE_INDUSTRY_ITEMS = [
{',\n'.join(rows)}
]

StartupEvents.registry('item', event => {{
    SPACE_INDUSTRY_ITEMS.forEach(([id, name, tooltip, family]) => {{
        event.create(id)
            .displayName(name)
            .texture(`kubejs:item/space_industry/${{id}}`)
            .tooltip(`§7${{tooltip}}`)
            .tooltip(`§8Infinite Domain aerospace component · ${{family.replace('_', ' ')}}`)
    }})
}})

StartupEvents.registry('block', event => {{
    const ores = [
{',\n'.join(ore_rows)}
    ]
    ores.forEach(([id, name]) => {{
        event.create(id)
            .displayName(name)
            .texture(`kubejs:block/space_industry/${{id}}`)
            .stoneSoundType()
            .hardness(5.5)
            .resistance(8.0)
            .requiresTool()
    }})
}})
"""
    write(KUBEJS / "startup_scripts" / "space_industry_catalog.js", script)


def generate_recipes() -> None:
    # Recipe declarations deliberately reuse established pack materials. Each
    # family is processed through multiple Create operations before assembly.
    script = r"""// GENERATED by scripts/generate_stellaris_space_industry.py. Do not hand-edit.
ServerEvents.recipes(event => {
    const I = id => `kubejs:${id}`
    const press = (out, input) => event.recipes.create.pressing(I(out), input.startsWith('#') ? Ingredient.of(input) : input).id(`infinite_domain:space/pressing/${out}`)
    const cut = (out, count, input) => event.recipes.create.cutting(Item.of(I(out), count), input).id(`infinite_domain:space/cutting/${out}`)
    const mix = (out, inputs, heat) => {
        const recipe = event.recipes.create.mixing(out, inputs).id(`infinite_domain:space/mixing/${String(out).replace(/[^a-z0-9_]+/gi, '_')}`)
        if (heat === 'heated') recipe.heated()
        if (heat === 'superheated') recipe.superheated()
        return recipe
    }
    const compact = (out, inputs) => event.recipes.create.compacting(out, inputs).id(`infinite_domain:space/compacting/${String(out).replace(/[^a-z0-9_]+/gi, '_')}`)
    const deploy = (out, base, applied) => event.recipes.create.deploying(I(out), [base, applied]).id(`infinite_domain:space/deploying/${out}`)
    const seq = (out, input, transitional, loops, applied) => event.custom({
        type: 'create:sequenced_assembly', ingredient: {item: input}, loops: loops,
        results: [{id: I(out), count: 1}], transitional_item: {id: I(transitional)},
        sequence: applied.map(id => ({
                type: 'create:deploying',
                ingredients: [{item: I(transitional)}, id.startsWith('#') ? {tag: id.slice(1)} : {item: id}],
                results: [{id: I(transitional), count: 1}]
            })).concat([{
                type: 'create:pressing',
                ingredients: [{item: I(transitional)}],
                results: [{id: I(transitional), count: 1}]
            }])
    }).id(`infinite_domain:space/sequenced/${out}`)

    // Planetary ore beneficiation: crushing -> separation -> chemical or thermal reduction.
    // create:splashing is water-only fan washing (no fluid ingredient exists), so it is
    // kept only for genuinely aqueous steps; airless lunar separation uses milling instead.
    event.recipes.create.crushing([Item.of(I('crushed_ilmenite'), 2), CreateItem.of('stellaris:moon_stone_dust', 0.35)], I('moon_ilmenite_ore')).id('infinite_domain:space/moon/crush_ilmenite')
    event.recipes.create.milling([Item.of(I('titanium_concentrate')), CreateItem.of(I('lunar_oxygen_feed'), 0.75)], I('crushed_ilmenite')).id('infinite_domain:space/moon/mill_ilmenite')
    event.recipes.create.crushing([Item.of(I('rare_earth_concentrate'), 2), CreateItem.of('stellaris:moon_stone_dust', 0.5)], I('moon_kreep_ore')).id('infinite_domain:space/moon/crush_kreep')
    event.recipes.create.crushing([Item.of(I('helium3_adsorbate')), Item.of('stellaris:moon_stone_dust', 2)], I('moon_helium_regolith')).id('infinite_domain:space/moon/heat_regolith')
    event.recipes.create.crushing([Item.of(I('lunar_ceramic'), 2), Item.of('tfmg:aluminum_nugget', 3)], I('moon_anorthosite_ore')).id('infinite_domain:space/moon/crush_anorthosite')
    event.recipes.create.crushing(Item.of(I('crushed_hematite'), 2), I('mars_hematite_ore')).id('infinite_domain:space/mars/crush_hematite')
    event.recipes.create.crushing(Item.of(I('sulfate_salts'), 2), I('mars_sulfate_ore')).id('infinite_domain:space/mars/crush_sulfate')
    event.recipes.create.crushing(Item.of(I('perchlorate_salts'), 2), I('mars_perchlorate_ore')).id('infinite_domain:space/mars/crush_perchlorate')
    event.recipes.create.crushing(Item.of(I('nickel_cobalt_concentrate'), 2), I('mars_nickel_cobalt_ore')).id('infinite_domain:space/mars/crush_nickel_cobalt')
    event.recipes.create.crushing(Item.of(I('brine_salts'), 2), I('mars_brine_ore')).id('infinite_domain:space/mars/crush_brine')
    event.recipes.create.splashing([Item.of('minecraft:iron_nugget', 8), CreateItem.of(I('sulfate_salts'), 0.25)], I('crushed_hematite')).id('infinite_domain:space/mars/wash_hematite')
    event.recipes.create.crushing(Item.of(I('sulfur_concentrate'), 2), I('venus_sulfur_ore')).id('infinite_domain:space/venus/crush_sulfur')
    event.recipes.create.crushing(Item.of(I('vanadium_concentrate'), 2), I('venus_vanadium_ore')).id('infinite_domain:space/venus/crush_vanadium')
    event.recipes.create.crushing(Item.of(I('tungsten_concentrate'), 2), I('venus_tungsten_ore')).id('infinite_domain:space/venus/crush_tungsten')
    event.recipes.create.crushing(Item.of(I('refractory_concentrate'), 2), I('venus_refractory_ore')).id('infinite_domain:space/venus/crush_refractory')
    compact(Item.of(I('lunar_ceramic'), 2), [I('moon_silicate_ore'), 'minecraft:clay_ball']).heated()
    mix(Item.of(I('martian_catalyst'), 2), [I('nickel_cobalt_concentrate'), I('sulfate_salts'), 'create:powdered_obsidian'], 'heated')
    compact(Item.of(I('martian_geopolymer'), 2), [I('mars_silicate_ore'), I('sulfate_salts'), Fluid.of('minecraft:water', 250)]).heated()
    mix([Fluid.of('minecraft:water', 250), Item.of(I('sulfate_salts'))], [Item.of(I('brine_salts'), 2)], 'heated').id('infinite_domain:space/mars/brine_water_recovery')
    mix(I('venus_atmospheric_sorbent'), [I('sulfur_concentrate'), I('refractory_concentrate'), Fluid.of('tfmg:carbon_dioxide', 1000)], 'superheated').id('infinite_domain:space/venus/atmospheric_capture')
    mix(I('venus_superalloy'), [I('vanadium_concentrate'), I('tungsten_concentrate'), 'stellaris:heavy_metal_ingot', 'stellaris:desh_ingot', I('rare_earth_concentrate')], 'superheated')

    // Structural and thermal families.
    press('aerospace_aluminum_sheet', '#c:ingots/aluminum')
    compact(I('desh_titanium_laminate'), [I('titanium_concentrate'), 'stellaris:desh_ingot', 'immersiveengineering:plate_nickel']).heated()
    cut('structural_truss', 2, I('aerospace_aluminum_sheet'))
    deploy('reinforced_frame', I('structural_truss'), 'immersiveengineering:component_steel')
    compact(I('pressure_bulkhead'), [I('reinforced_frame'), I('aerospace_aluminum_sheet'), 'tfmg:rubber_sheet'])
    compact(I('structural_composite'), ['oritech:carbon_fibre_strands', 'tfmg:plastic_sheet', 'create:sturdy_sheet']).heated()
    compact(I('aerospace_composite'), [I('structural_composite'), I('desh_titanium_laminate'), 'oritech:reinforced_carbon_sheet']).heated()
    mix(Item.of(I('ceramic_fiber'), 2), [I('lunar_ceramic'), 'createnuclear:graphite_rod', 'minecraft:string'], 'heated')
    compact(Item.of(I('thermal_shield_tile'), 2), [I('ceramic_fiber'), 'create:powdered_obsidian']).heated()
    compact(I('ablative_panel'), [I('thermal_shield_tile'), 'tfmg:plastic_sheet', 'createnuclear:graphite_rod']).heated()
    compact(I('radiation_laminate'), ['immersiveengineering:plate_lead', 'createnuclear:graphite_rod', I('rare_earth_concentrate')]).heated()
    compact(I('extreme_environment_composite'), [I('aerospace_composite'), I('venus_superalloy'), I('refractory_concentrate'), I('venus_atmospheric_sorbent')]).heated()
    seq('fuselage_section', I('reinforced_frame'), 'incomplete_fuselage_section', 2, [I('aerospace_aluminum_sheet'), I('structural_truss'), I('pressure_bulkhead'), I('aerospace_composite')])
    compact(I('thermal_protection_package'), [Item.of(I('thermal_shield_tile'), 4), Item.of(I('ablative_panel'), 2), I('radiation_laminate')])

    // Pressure hardware hierarchy.
    compact('kubejs:pressure_vessel', ['tfmg:steel_fluid_tank', '#c:plates/steel', 'tfmg:rubber_sheet'])
    deploy('reinforced_pressure_vessel', I('pressure_vessel'), 'tfmg:heavy_plate')
    deploy('aerospace_pressure_vessel', I('reinforced_pressure_vessel'), I('desh_titanium_laminate'))
    deploy('venus_pressure_vessel', I('aerospace_pressure_vessel'), I('extreme_environment_composite'))
    deploy('precision_valve', 'tfmg:steel_fluid_valve', 'powergrid:integrated_circuit')
    deploy('high_pressure_valve', I('precision_valve'), 'tfmg:heavy_plate')
    deploy('cryogenic_valve', I('high_pressure_valve'), I('ceramic_fiber'))
    compact(I('aerospace_pump'), ['tfmg:electric_pump', I('high_pressure_valve'), 'create_new_age:advanced_motor'])
    compact(I('oxygen_manifold'), [Item.of(I('precision_valve'), 2), I('aerospace_pressure_vessel'), 'create:fluid_pipe'])
    compact(I('propellant_manifold'), [Item.of(I('cryogenic_valve'), 2), I('aerospace_pressure_vessel'), 'tfmg:steel_pipe'])
    compact(Item.of(I('empty_gas_cylinder'), 2), [I('aerospace_aluminum_sheet'), I('precision_valve')])
    event.recipes.create.filling(I('oxygen_cylinder'), [I('empty_gas_cylinder'), Fluid.of('stellaris:oxygen', 1000)]).id('infinite_domain:space/filling/oxygen_cylinder')
    event.recipes.create.filling(I('hydrogen_cylinder'), [I('empty_gas_cylinder'), Fluid.of('stellaris:hydrogen', 1000)]).id('infinite_domain:space/filling/hydrogen_cylinder')
    event.recipes.create.filling(I('methane_cylinder'), [I('empty_gas_cylinder'), Fluid.of('stellaris:fuel', 1000)]).id('infinite_domain:space/filling/methane_cylinder')

    // Avionics reuse the established electrical and AE2 industries.
    compact(I('sensor_package'), ['immersiveengineering:component_electronic', 'create:electron_tube', 'powergrid:integrated_circuit'])
    compact(I('guidance_computer'), ['ae2:calculation_processor', I('sensor_package'), 'powergrid:circuit_board'])
    compact(I('navigation_unit'), ['ae2:engineering_processor', I('guidance_computer'), 'minecraft:compass'])
    compact(I('telemetry_array'), ['stellaris:antenna', I('sensor_package'), 'ae2:wireless_receiver'])
    compact(I('power_distribution_unit'), ['create_new_age:generator_coil', 'powergrid:integrated_circuit', 'immersiveengineering:coil_hv'])
    seq('avionics_controller', I('power_distribution_unit'), 'incomplete_avionics_controller', 2, [I('guidance_computer'), I('telemetry_array'), I('sensor_package')])
    deploy('radiation_hardened_controller', I('avionics_controller'), I('radiation_laminate'))
    compact(I('flight_control_computer'), [Item.of(I('radiation_hardened_controller'), 2), I('navigation_unit'), 'ae2:engineering_processor'])
    compact(I('avionics_bay'), [I('flight_control_computer'), I('telemetry_array'), I('power_distribution_unit'), I('reinforced_frame')])

    // Life support and four oxygen economies.
    compact(I('electrolysis_membrane'), ['immersiveengineering:plate_nickel', 'tfmg:plastic_sheet', 'ae2:quartz_glass'])
    compact(I('carbon_scrubber'), ['minecraft:charcoal', 'tfmg:plastic_sheet', I('precision_valve')])
    compact(I('humidity_reclaimer'), [I('aerospace_pump'), I('sensor_package'), 'create:copper_sheet'])
    compact(I('oxygen_regulator'), [I('precision_valve'), I('sensor_package'), 'tfmg:rubber_sheet'])
    compact(I('life_support_controller'), ['powergrid:integrated_circuit', I('sensor_package'), I('oxygen_regulator')])
    seq('closed_loop_life_support', I('life_support_controller'), 'incomplete_life_support_assembly', 2, [I('carbon_scrubber'), I('humidity_reclaimer'), I('oxygen_manifold')])
    compact(I('life_support_module'), [I('closed_loop_life_support'), Item.of(I('oxygen_cylinder'), 2), I('pressure_bulkhead'), I('thermal_protection_package')])
    mix(Fluid.of('stellaris:oxygen', 750), [Fluid.of('minecraft:water', 1000), I('electrolysis_membrane'), 'create_new_age:generator_coil'], 'heated').id('infinite_domain:space/oxygen/terrestrial_electrolysis')
    mix([Fluid.of('stellaris:oxygen', 1000), Item.of(I('titanium_concentrate'))], [Item.of(I('lunar_oxygen_feed'), 2), 'createnuclear:graphite_rod'], 'superheated').id('infinite_domain:space/oxygen/lunar_mineral_reduction')
    mix(Fluid.of('stellaris:oxygen', 1250), [Item.of(I('perchlorate_salts'), 2), I('martian_catalyst'), Fluid.of('tfmg:carbon_dioxide', 1000)], 'heated').id('infinite_domain:space/oxygen/martian_atmospheric_separation')
    mix([Fluid.of('stellaris:oxygen', 900), I('spent_scrubber')], [I('carbon_scrubber'), Fluid.of('minecraft:water', 250), 'minecraft:charcoal'], 'heated').id('infinite_domain:space/oxygen/closed_loop_recovery')
    mix(I('carbon_scrubber'), [I('spent_scrubber'), 'minecraft:charcoal'], 'heated').id('infinite_domain:space/oxygen/scrubber_regeneration')

    // Three propellant paths: petroleum, Mars methalox and advanced hydrogen.
    mix(Fluid.of('stellaris:fuel', 1000), [Fluid.of('petrochem:kerosene', 750), Fluid.of('petrochem:hydrogen', 250), I('sulfur_concentrate')], 'heated').id('infinite_domain:space/fuel/petroleum_route')
    mix(Fluid.of('stellaris:fuel', 1250), [Fluid.of('tfmg:carbon_dioxide', 1000), Fluid.of('stellaris:hydrogen', 1000), I('martian_catalyst')], 'superheated').id('infinite_domain:space/fuel/mars_methalox_route')
    mix(Fluid.of('stellaris:hydrogen', 1000), [Fluid.of('minecraft:water', 1000), I('electrolysis_membrane'), I('rare_earth_concentrate'), I('helium3_adsorbate')], 'superheated').id('infinite_domain:space/fuel/advanced_hydrogen_route')

    // Propulsion is a component tree, not a single expensive grid.
    press('injector_plate', I('desh_titanium_laminate'))
    seq('turbopump', I('aerospace_pump'), 'incomplete_turbopump', 2, ['create_new_age:advanced_motor', I('cryogenic_valve'), I('precision_valve')])
    compact(I('combustion_chamber'), [Item.of(I('desh_titanium_laminate'), 2), I('injector_plate'), 'create_new_age:heat_pipe'])
    compact(I('engine_nozzle'), [I('venus_superalloy'), I('ceramic_fiber'), 'stellaris:heavy_metal_plate'])
    compact(I('gimbal_actuator'), ['create:mechanical_piston', 'create_new_age:reinforced_motor', I('sensor_package')])
    compact(I('ignition_controller'), ['powergrid:integrated_circuit', 'create_new_age:overcharged_golden_sheet', I('sensor_package')])
    compact(I('petroleum_engine_assembly'), [I('turbopump'), I('combustion_chamber'), I('engine_nozzle'), I('gimbal_actuator'), I('ignition_controller'), I('propellant_manifold')])
    compact(I('methalox_engine_assembly'), [I('petroleum_engine_assembly'), I('martian_catalyst'), I('cryogenic_valve'), I('radiation_hardened_controller')])
    compact(I('hydrogen_engine_assembly'), [I('methalox_engine_assembly'), I('rare_earth_concentrate'), I('venus_superalloy'), I('flight_control_computer')])
    compact(I('propellant_tank_section'), [Item.of(I('aerospace_pressure_vessel'), 4), Item.of(I('cryogenic_valve'), 2), I('propellant_manifold'), I('structural_truss')])
    compact(I('service_module'), [I('propellant_tank_section'), I('power_distribution_unit'), I('life_support_controller'), I('aerospace_pump')])
    compact(I('landing_gear_assembly'), [Item.of(I('structural_truss'), 3), Item.of(I('gimbal_actuator'), 2), 'create:sturdy_sheet'])
    compact(I('payload_adapter'), [I('reinforced_frame'), I('sensor_package'), 'create:mechanical_bearing'])

    // Mission sidegrades retain different economic niches.
    compact(I('earth_launch_package'), [I('petroleum_engine_assembly'), I('propellant_tank_section'), I('avionics_bay')])
    compact(I('lunar_cargo_package'), [I('payload_adapter'), Item.of(I('landing_gear_assembly'), 2), I('desh_titanium_laminate'), I('radiation_hardened_controller')])
    compact(I('mars_transfer_package'), [I('methalox_engine_assembly'), I('closed_loop_life_support'), I('martian_catalyst'), I('martian_geopolymer'), I('thermal_protection_package')])
    compact(I('venus_return_package'), [I('hydrogen_engine_assembly'), I('venus_pressure_vessel'), I('extreme_environment_composite'), I('flight_control_computer')])
    compact(I('emergency_return_package'), [I('petroleum_engine_assembly'), I('navigation_unit'), I('oxygen_cylinder'), I('landing_gear_assembly')])
    event.shaped('stellaris:tiny_rocket_upgrade', [' P ', 'MBM', ' P '], {P: I('emergency_return_package'), M: 'stellaris:base_module_tier_1', B: I('payload_adapter')}).id('infinite_domain:space/mission/emergency_return_upgrade')
    event.shaped('stellaris:small_rocket_upgrade', [' P ', 'MBM', ' P '], {P: I('earth_launch_package'), M: 'stellaris:base_module_tier_1', B: I('payload_adapter')}).id('infinite_domain:space/mission/earth_launch_upgrade')
    event.shaped('stellaris:normal_rocket_upgrade', [' P ', 'MBM', ' P '], {P: I('lunar_cargo_package'), M: 'stellaris:base_module_tier_2', B: I('payload_adapter')}).id('infinite_domain:space/mission/lunar_cargo_upgrade')
    event.shaped('stellaris:big_rocket_upgrade', [' P ', 'MBM', ' P '], {P: I('mars_transfer_package'), M: 'stellaris:base_module_tier_2', B: I('service_module')}).id('infinite_domain:space/mission/mars_transfer_upgrade')
    event.shaped('stellaris:big_fuel_tank_upgrade', [' P ', 'MBM', ' P '], {P: I('venus_return_package'), M: 'stellaris:base_module_tier_2', B: I('propellant_tank_section')}).id('infinite_domain:space/mission/venus_return_upgrade')

    // Count-preserving logistics units. Unpacking recovers the exact contents.
    const packages = [
        ['structural_parts_crate', I('fuselage_section'), 4], ['life_support_crate', I('life_support_module'), 4],
        ['avionics_crate', I('avionics_bay'), 4], ['propellant_equipment_crate', I('propellant_manifold'), 8],
        ['lunar_material_pallet', I('desh_titanium_laminate'), 16], ['martian_chemical_pallet', I('martian_catalyst'), 16],
        ['venus_material_pallet', I('venus_superalloy'), 16]
    ]
    packages.forEach(([packed, content, count]) => {
        compact(I(packed), [Item.of(content, count), 'create:cardboard_block'])
        event.shapeless(Item.of(content, count), [I(packed)]).id(`infinite_domain:space/unpacking/${packed}`)
    })

    // Partial recovery only; launch hardware never recycles at 100% yield.
    event.recipes.create.crushing([Item.of('tfmg:steel_nugget', 5), CreateItem.of('create:iron_sheet', 0.5)], I('pressure_vessel')).id('infinite_domain:space/recycling/pressure_vessel')
    event.recipes.create.crushing([Item.of('ae2:silicon', 2), CreateItem.of('immersiveengineering:component_electronic', 0.35)], I('avionics_controller')).id('infinite_domain:space/recycling/avionics_controller')
})
"""
    write(KUBEJS / "server_scripts" / "space_industry_recipes.js", script)


def ore_feature(ore: tuple) -> None:
    item_id, _, planet, host, size, count, min_y, max_y, _ = ore
    root = KUBEJS / "data" / "infinite_domain"
    write_json(root / "worldgen" / "configured_feature" / f"{item_id}.json", {
        "type": "minecraft:ore",
        "config": {"discard_chance_on_air_exposure": 0.0, "size": size, "targets": [{
            "state": {"Name": f"kubejs:{item_id}"},
            "target": {"block": host, "predicate_type": "minecraft:block_match"},
        }]},
    })
    write_json(root / "worldgen" / "placed_feature" / f"{item_id}.json", {
        "feature": f"infinite_domain:{item_id}",
        "placement": [
            {"type": "minecraft:count", "count": count},
            {"type": "minecraft:in_square"},
            {"type": "minecraft:height_range", "height": {"type": "minecraft:trapezoid", "min_inclusive": {"absolute": min_y}, "max_inclusive": {"absolute": max_y}}},
            {"type": "minecraft:biome"},
        ],
    })


def generate_worldgen() -> None:
    for ore in ORES:
        ore_feature(ore)
    for planet in ("moon", "mars", "venus"):
        features = [f"infinite_domain:{ore[0]}" for ore in ORES if ore[2] == planet]
        write_json(KUBEJS / "data" / "infinite_domain" / "neoforge" / "biome_modifier" / f"add_{planet}_space_industry_ores.json", {
            "type": "neoforge:add_features",
            "biomes": f"#stellaris:{planet}_biomes",
            "features": features,
            "step": "underground_ores",
        })
    for tag_path in (
        KUBEJS / "data" / "minecraft" / "tags" / "block" / "mineable" / "pickaxe.json",
        KUBEJS / "data" / "minecraft" / "tags" / "block" / "needs_diamond_tool.json",
    ):
        merge_tag_values(tag_path, [f"kubejs:{ore[0]}" for ore in ORES])


def shaped(output: str, pattern: list[str], keys: dict[str, str], count: int = 1) -> dict:
    return {"type": "minecraft:crafting_shaped", "category": "misc", "pattern": pattern,
            "key": {key: {"item": value} for key, value in keys.items()}, "result": {"id": output, "count": count}}


def generate_stellaris_overrides() -> None:
    base = KUBEJS / "data" / "stellaris" / "recipe"
    overrides = {
        "misc/rocket_engine.json": shaped("stellaris:rocket_engine", [" T ", "CEC", "GNG"], {
            "T": "kubejs:turbopump", "C": "kubejs:combustion_chamber", "E": "kubejs:petroleum_engine_assembly", "G": "kubejs:gimbal_actuator", "N": "kubejs:engine_nozzle"}),
        "misc/rocket_fin.json": shaped("stellaris:rocket_fin", [" S ", "SCS", " S "], {"S": "kubejs:aerospace_aluminum_sheet", "C": "kubejs:structural_composite"}, 2),
        "misc/rocket_nose_cone.json": shaped("stellaris:rocket_nose_cone", [" T ", "TBT", "SAS"], {"T": "kubejs:thermal_shield_tile", "B": "kubejs:pressure_bulkhead", "S": "kubejs:sensor_package", "A": "kubejs:aerospace_composite"}),
        "misc/rocket_launch_pad.json": shaped("stellaris:rocket_launch_pad", ["HTH", "FCF", "HTH"], {"H": "tfmg:heavy_plate", "T": "kubejs:structural_truss", "F": "kubejs:reinforced_frame", "C": "createnuclear:reactor_casing"}, 4),
        "misc/rocket_station_block.json": shaped("stellaris:rocket_station", ["TAT", "CFC", "PDP"], {"T": "kubejs:telemetry_array", "A": "stellaris:antenna", "C": "kubejs:avionics_controller", "F": "kubejs:flight_control_computer", "P": "kubejs:power_distribution_unit", "D": "ae2:dense_energy_cell"}),
        "misc/oxygen_distributor.json": shaped("stellaris:oxygen_distributor", ["OMO", "RCR", "PVP"], {"O": "kubejs:oxygen_cylinder", "M": "kubejs:oxygen_manifold", "R": "kubejs:oxygen_regulator", "C": "kubejs:life_support_controller", "P": "kubejs:aerospace_pump", "V": "kubejs:reinforced_pressure_vessel"}),
        "misc/oxygen_tank.json": shaped("stellaris:oxygen_tank", [" V ", "SRS", " V "], {"V": "kubejs:precision_valve", "S": "kubejs:aerospace_aluminum_sheet", "R": "tfmg:rubber_sheet"}),
        "misc/big_oxygen_tank.json": shaped("stellaris:big_oxygen_tank", ["OVO", "TMT", "OVO"], {"O": "kubejs:oxygen_cylinder", "V": "kubejs:high_pressure_valve", "T": "kubejs:aerospace_pressure_vessel", "M": "kubejs:oxygen_manifold"}),
        "misc/spacesuit_helmet.json": shaped("stellaris:space_suit_helmet", ["ATA", "RSR", " O "], {"A": "kubejs:aerospace_aluminum_sheet", "T": "kubejs:thermal_shield_tile", "R": "tfmg:rubber_sheet", "S": "kubejs:sensor_package", "O": "kubejs:oxygen_regulator"}),
        "misc/spacesuit_chestplate.json": shaped("stellaris:space_suit_chestplate", ["BMB", "LCL", "ATA"], {"B": "kubejs:pressure_bulkhead", "M": "kubejs:oxygen_manifold", "L": "kubejs:radiation_laminate", "C": "kubejs:life_support_controller", "A": "kubejs:aerospace_aluminum_sheet", "T": "stellaris:oxygen_tank"}),
        "misc/spacesuit_leggings.json": shaped("stellaris:space_suit_leggings", ["ALA", "R R", "A A"], {"A": "kubejs:aerospace_aluminum_sheet", "L": "kubejs:radiation_laminate", "R": "tfmg:rubber_sheet"}),
        "misc/spacesuit_boots.json": shaped("stellaris:space_suit_boots", ["R R", "A A", "T T"], {"R": "tfmg:rubber_sheet", "A": "kubejs:aerospace_aluminum_sheet", "T": "create:sturdy_sheet"}),
        "misc/hydrogen_motor.json": shaped("stellaris:hydrogen_motor", ["CHC", "TIT", "VGV"], {"C": "kubejs:cryogenic_valve", "H": "kubejs:hydrogen_engine_assembly", "T": "kubejs:turbopump", "I": "kubejs:ignition_controller", "V": "kubejs:venus_superalloy", "G": "kubejs:gimbal_actuator"}),
        "misc/fuel_refinery.json": shaped("stellaris:fuel_refinery", ["PVP", "CHC", "ESE"], {"P": "kubejs:aerospace_pump", "V": "kubejs:high_pressure_valve", "C": "petrochem:distillation_controller", "H": "tfmg:steel_chemical_vat", "E": "powergrid:integrated_circuit", "S": "kubejs:sensor_package"}),
        "misc/water_separator.json": shaped("stellaris:water_separator", ["MEM", "PCP", "VTV"], {"M": "kubejs:electrolysis_membrane", "E": "create_new_age:generator_coil", "P": "kubejs:aerospace_pump", "C": "kubejs:life_support_controller", "V": "kubejs:precision_valve", "T": "kubejs:reinforced_pressure_vessel"}),
        "misc/pumpjack.json": shaped("stellaris:pumpjack", ["TRT", "PMP", "FSF"], {"T": "tfmg:steel_truss", "R": "kubejs:reinforced_frame", "P": "petrochem:pumpjack_well", "M": "kubejs:aerospace_pump", "F": "tfmg:steel_frame", "S": "kubejs:sensor_package"}),
        "misc/solar_panel.json": shaped("stellaris:solar_panel", ["GGG", "CEC", "AFA"], {"G": "ae2:quartz_glass", "C": "create_new_age:copper_circuit", "E": "powergrid:integrated_circuit", "A": "kubejs:aerospace_aluminum_sheet", "F": "kubejs:reinforced_frame"}),
    }
    for rel, data in overrides.items():
        write_json(base / rel, data)
    # 7x7 mechanical build: 25+ distinct systems/subassemblies feed one native Stellaris rocket.
    rocket = {
        "type": "create:mechanical_crafting",
        "accept_mirrored": False,
        "pattern": ["  NNN  ", " FTTTF ", "SACCLSS", "SPMMLPS", "SEEEELS", " GGGGG ", "   G   "],
        "key": {
            "N": {"item": "stellaris:rocket_nose_cone"}, "F": {"item": "stellaris:rocket_fin"},
            "T": {"item": "kubejs:thermal_protection_package"}, "S": {"item": "kubejs:fuselage_section"},
            "A": {"item": "kubejs:avionics_bay"}, "C": {"item": "kubejs:flight_control_computer"},
            "P": {"item": "kubejs:propellant_tank_section"}, "M": {"item": "kubejs:service_module"},
            "L": {"item": "kubejs:life_support_module"}, "E": {"item": "stellaris:rocket_engine"},
            "G": {"item": "kubejs:landing_gear_assembly"},
        },
        "result": {"id": "stellaris:rocket", "count": 1},
    }
    write_json(base / "rocket.json", rocket)


def draw_icon(path: Path, color: tuple[int, int, int], family: str, index: int) -> None:
    image = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    edge = tuple(max(0, c - 55) for c in color) + (255,)
    light = tuple(min(255, c + 55) for c in color) + (255,)
    fill = color + (255,)
    shape = index % 5
    if family in {"pressure", "life_support"}:
        draw.rounded_rectangle((4, 1, 11, 14), radius=2, fill=edge)
        draw.rectangle((5, 3, 10, 12), fill=fill)
        draw.line((6, 4, 9, 4), fill=light)
        draw.rectangle((7, 0, 8, 2), fill=light)
    elif family in {"electronics", "mission"}:
        draw.rectangle((2, 3, 13, 12), fill=edge)
        draw.rectangle((4, 5, 11, 10), fill=fill)
        for p in range(3, 14, 3):
            draw.point((p, 2), fill=light); draw.point((p, 13), fill=light)
        draw.line((5, 7, 10, 7), fill=light)
    elif family == "propulsion":
        draw.polygon([(5, 1), (10, 1), (12, 10), (10, 13), (5, 13), (3, 10)], fill=edge)
        draw.rectangle((6, 2, 9, 10), fill=fill)
        draw.polygon([(5, 12), (10, 12), (12, 15), (3, 15)], fill=light)
    else:
        draw.polygon([(2, 5), (5, 2), (13, 2), (14, 10), (10, 14), (2, 11)], fill=edge)
        draw.polygon([(4, 6), (6, 4), (11, 4), (12, 9), (9, 12), (4, 10)], fill=fill)
        draw.line((5, 6, 11, 9), fill=light)
    if shape == 0:
        draw.point((3, 3), fill=(255, 255, 255, 220))
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)


def ore_texture(path: Path, host_path: str, vein: tuple[int, int, int]) -> None:
    jar = ROOT / "mods" / "stellaris-1.21-neoforge-1.4.25.jar"
    host_name = host_path.split(":", 1)[1]
    try:
        with zipfile.ZipFile(jar) as zf:
            raw = zf.read(f"assets/stellaris/textures/block/{host_name}.png")
        import io
        image = Image.open(io.BytesIO(raw)).convert("RGBA").resize((16, 16), Image.Resampling.NEAREST)
    except Exception:
        image = Image.new("RGBA", (16, 16), (82, 78, 74, 255))
    draw = ImageDraw.Draw(image)
    dark = tuple(max(0, c - 50) for c in vein) + (255,)
    light = tuple(min(255, c + 45) for c in vein) + (255,)
    points = [(2, 3), (5, 2), (9, 4), (13, 2), (3, 8), (7, 7), (11, 9), (14, 7), (5, 13), (10, 12), (13, 14)]
    for i, (x, y) in enumerate(points):
        draw.rectangle((x, y, min(15, x + (i % 2)), min(15, y + 1)), fill=dark if i % 3 == 0 else vein + (255,))
        if i % 4 == 0:
            draw.point((min(15, x + 1), y), fill=light)
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path)


def generate_textures() -> None:
    item_root = KUBEJS / "assets" / "kubejs" / "textures" / "item" / "space_industry"
    for family, data in COMPONENT_FAMILIES.items():
        for index, (item_id, _, _) in enumerate(data["items"]):
            # Authored item icons are generated as full-size masters and reduced
            # to 128px. The old 16px Pillow icon is retained only as a missing-file
            # fallback so regeneration can never overwrite finished artwork.
            path = item_root / f"{item_id}.png"
            if not path.exists():
                draw_icon(path, data["color"], family, index)
    block_root = KUBEJS / "assets" / "kubejs" / "textures" / "block" / "space_industry"
    for ore in ORES:
        ore_texture(block_root / f"{ore[0]}.png", ore[3], ore[8])


def generate_tags() -> None:
    all_items = [f"kubejs:{item[0]}" for data in COMPONENT_FAMILIES.values() for item in data["items"]]
    write_json(KUBEJS / "data" / "infinite_domain" / "tags" / "item" / "aerospace_components.json", {"replace": False, "values": all_items})
    for family, data in COMPONENT_FAMILIES.items():
        write_json(KUBEJS / "data" / "infinite_domain" / "tags" / "item" / f"space_{family}.json", {"replace": False, "values": [f"kubejs:{item[0]}" for item in data["items"]]})
    suit_items = [f"infinite_domain_space:{role}_{piece}" for role, _, _, _ in SUITS for piece in ("helmet", "chestplate", "leggings", "boots")]
    write_json(KUBEJS / "data" / "stellaris" / "tags" / "item" / "space_suit.json", {"replace": False, "values": suit_items})
    radiation_roles = {"radiation": "ppe_late", "venusian": "ppe_late", "heavy": "ppe_advanced", "martian": "ppe_advanced", "lunar_prospector": "ppe_industrial"}
    for role, tier in radiation_roles.items():
        path = KUBEJS / "data" / "infinite_domain_radiation" / "tags" / "item" / f"{tier}.json"
        existing = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"replace": False, "values": []}
        existing["values"] = sorted(set(existing.get("values", [])) | {f"infinite_domain_space:{role}_{piece}" for piece in ("helmet", "chestplate", "leggings", "boots")})
        write_json(path, existing)


def generate_suits() -> None:
    resources = ROOT / "dev/packdev" / "stellaris-space-industry" / "src" / "main" / "resources"
    model_root = resources / "assets" / "infinite_domain_space" / "models" / "item"
    texture_root = resources / "assets" / "infinite_domain_space" / "textures" / "item"
    lang = {}
    role_recipes = {
        "emergency": ["tfmg:rubber_sheet", "kubejs:oxygen_regulator"],
        "surveyor": ["kubejs:sensor_package", "kubejs:navigation_unit"],
        "lunar_prospector": ["kubejs:radiation_laminate", "kubejs:desh_titanium_laminate"],
        "radiation": ["kubejs:radiation_laminate", "createnuclear:graphite_rod"],
        "heavy": ["tfmg:heavy_plate", "kubejs:reinforced_frame"],
        "mobility": ["kubejs:gimbal_actuator", "create_new_age:advanced_motor"],
        "extended": ["kubejs:closed_loop_life_support", "kubejs:oxygen_cylinder"],
        "martian": ["kubejs:martian_catalyst", "kubejs:aerospace_composite"],
        "venusian": ["kubejs:extreme_environment_composite", "kubejs:venus_superalloy"],
    }
    piece_base = {"helmet": "stellaris:space_suit_helmet", "chestplate": "stellaris:space_suit_chestplate", "leggings": "stellaris:space_suit_leggings", "boots": "stellaris:space_suit_boots"}
    emergency_base = {"helmet": "enviromine:gas_mask_advanced_helmet", "chestplate": "minecraft:leather_chestplate", "leggings": "minecraft:leather_leggings", "boots": "minecraft:leather_boots"}
    for role, display, tooltip, color in SUITS:
        for index, piece in enumerate(("helmet", "chestplate", "leggings", "boots")):
            item_id = f"{role}_{piece}"
            lang[f"item.infinite_domain_space.{item_id}"] = f"{display} {piece.title()}"
            write_json(model_root / f"{item_id}.json", {"parent": "minecraft:item/generated", "textures": {"layer0": f"infinite_domain_space:item/{item_id}"}})
            draw_icon(texture_root / f"{item_id}.png", color, "life_support", index)
            first, second = role_recipes[role]
            write_json(KUBEJS / "data" / "infinite_domain_space" / "recipe" / "suits" / f"{item_id}.json", shaped(
                f"infinite_domain_space:{item_id}", ["ABA", "CDC", "AEA"], {
                    "A": "kubejs:aerospace_aluminum_sheet", "B": first, "C": second,
                    "D": emergency_base[piece] if role == "emergency" else piece_base[piece], "E": "tfmg:rubber_sheet"}))
    write_json(resources / "assets" / "infinite_domain_space" / "lang" / "en_us.json", {
        **lang,
        "tooltip.infinite_domain_space.emergency": "Minimal endurance and reduced mobility; cheap enough for first-launch contingencies",
        "tooltip.infinite_domain_space.surveyor": "Improves movement speed and survey reach",
        "tooltip.infinite_domain_space.lunar_prospector": "Improves mining and work reach; industrial radiation protection",
        "tooltip.infinite_domain_space.radiation": "Late-tier radiation protection with a mobility penalty",
        "tooltip.infinite_domain_space.heavy": "High toughness and knockback resistance at reduced speed",
        "tooltip.infinite_domain_space.mobility": "Fast traversal, step assistance and safer falls",
        "tooltip.infinite_domain_space.extended": "Eight-bucket oxygen capacity for long-duration EVA",
        "tooltip.infinite_domain_space.martian": "Dust-field mining and terrain efficiency; advanced radiation protection",
        "tooltip.infinite_domain_space.venusian": "Extreme heat tolerance, toughness and late-tier radiation protection",
    })


def generate_quests() -> None:
    chapter_id = "7C50000000000001"
    lines = ["{", "\tdefault_hide_dependency_lines: false", "\tdefault_quest_shape: \"gear\"", "\tfilename: \"stellaris_space_industrialization\"", "\tgroup: \"4E65FAAC62D57D4A\"", f"\tid: \"{chapter_id}\"", "\ticon: \"infinite_domain_space:emergency_helmet\"", "\torder_index: 5", "\tquests: ["]
    branches = [
        ("Orbital Engineering", ["emergency_helmet", "kubejs:reinforced_frame", "stellaris:rocket_launch_pad", "stellaris:rocket"]),
        ("Aerospace Manufacturing", ["kubejs:structural_truss", "kubejs:avionics_bay", "kubejs:petroleum_engine_assembly", "kubejs:fuselage_section"]),
        ("Life Support", ["kubejs:electrolysis_membrane", "kubejs:oxygen_cylinder", "kubejs:closed_loop_life_support", "stellaris:oxygen_distributor"]),
        ("Propellant Engineering", ["kubejs:propellant_manifold", "kubejs:petroleum_engine_assembly", "kubejs:methalox_engine_assembly", "kubejs:hydrogen_engine_assembly"]),
        ("Lunar Industry", ["kubejs:moon_ilmenite_ore", "kubejs:titanium_concentrate", "kubejs:rare_earth_concentrate", "kubejs:lunar_material_pallet"]),
        ("Martian Industry", ["kubejs:mars_perchlorate_ore", "kubejs:martian_catalyst", "kubejs:mars_transfer_package", "kubejs:martian_chemical_pallet"]),
        ("EVA Engineering", ["surveyor_helmet", "lunar_prospector_helmet", "radiation_helmet", "extended_helmet"]),
        ("Venus Engineering", ["kubejs:venus_tungsten_ore", "kubejs:venus_superalloy", "venusian_helmet", "kubejs:venus_return_package"]),
        ("Alien Archaeology", ["kubejs:meridian_core", "kubejs:martian_signal_prism", "kubejs:venusian_pressure_seal", "kubejs:burrower_carapace", "kubejs:jovian_arena_standard"]),
    ]
    lang = [(f"chapter.{chapter_id}.title", "Stellaris Space Industrialization"), (f"chapter.{chapter_id}.subtitle", "Era 7 annex: one space program, many specialized factories")]
    previous = "5710000000000001"
    qnum = 1
    x_positions = [-16, -12, -8, -4, 0, 4, 8, 12, 16]
    for bidx, (branch, items) in enumerate(branches):
        branch_prev = previous
        for step, raw_item in enumerate(items):
            item = raw_item if ":" in raw_item else f"infinite_domain_space:{raw_item}"
            qid = f"7C51{qnum:012X}"
            tid = f"7C52{qnum:012X}"
            lines.extend(["\t\t{", f"\t\t\tdependencies: [\"{branch_prev}\"]", f"\t\t\tid: \"{qid}\"", f"\t\t\ticon: {{ id: \"{item}\" }}", "\t\t\tshape: \"gear\"", f"\t\t\ttasks: [{{ id: \"{tid}\", item: {{ count: 1, id: \"{item}\" }}, type: \"item\" }}]", f"\t\t\tx: {x_positions[bidx]}.0d", f"\t\t\ty: {2 + step * 2}.0d", "\t\t}"])
            name = item.split(":", 1)[1].replace("_", " ").title()
            lang.append((f"quest.{qid}.title", name))
            lang.append((f"quest.{qid}.quest_desc", f"Advance the {branch} production line. Use JEI to trace the complete factory chain; this endpoint is intentionally built from reusable aerospace systems."))
            branch_prev = qid
            qnum += 1
    lines.extend(["\t]", "}"])
    write(ROOT / "config" / "ftbquests" / "quests" / "chapters" / "stellaris_space_industrialization.snbt", "\n".join(lines) + "\n")

    lang_path = ROOT / "config" / "ftbquests" / "quests" / "lang" / "en_us.snbt"
    text = lang_path.read_text(encoding="utf-8")
    text = "\n".join(line for line in text.splitlines() if not re.match(r"\s*(chapter|quest)\.7C5", line))
    insert = []
    for key, value in lang:
        if key.endswith("quest_desc"):
            insert.append(f"\t{key}: [{json.dumps(value)}]")
        else:
            insert.append(f"\t{key}: {json.dumps(value)}")
    close = text.rfind("}")
    text = text[:close].rstrip() + "\n" + "\n".join(insert) + "\n}\n"
    write(lang_path, text)


def generate_docs() -> None:
    component_count = sum(len(data["items"]) for data in COMPONENT_FAMILIES.values())
    text = f"""# Stellaris Space-Industry Audit and Implementation

Generated by `scripts/generate_stellaris_space_industry.py`.

## Audited baseline

- Minecraft 1.21.1 / NeoForge 21.1.248
- Stellaris 1.4.25 is the sole travel, planet, rocket, oxygen-room and personal oxygen authority.
- Create 6.0.10 provides mechanical processing and final rocket assembly.
- TFMG 1.2.0, Petrochem 1.3.2, Create Metallurgy 1.0.3, Create Nuclear 1.3.2-beta.3, Oritech 1.2.10, Immersive Engineering 12.4.2-194, PowerGrid 0.5.5.1 and AE2 provide established materials and machinery.
- Stellaris oxygen compatibility is tag-aware, but native tank draining identifies native suit sets. The installed `infinite-domain-stellaris-industry` bridge registers custom chest tanks through Stellaris/Potentials and extends that exact suit check without replacing Stellaris oxygen logic.
- Planet biome tags audited: `#stellaris:moon_biomes`, `#stellaris:mars_biomes`, and `#stellaris:venus_biomes`.

## Generated scope

- {component_count} reusable aerospace, pressure, electronics, thermal, life-support, propulsion, logistics and planetary process items.
- {len(ORES)} planetary ore blocks across Moon, Mars and Venus, added through normal configured/placed features and NeoForge biome modifiers.
- {len(SUITS)} four-piece EVA families with Stellaris oxygen storage and event-driven specialization attributes.
- Four dedicated Create sequenced-assembly lines for fuselage, avionics, closed-loop life support and turbopump production.
- Four oxygen economies: terrestrial electrolysis, lunar mineral reduction, Martian atmospheric processing, and closed-loop recovery.
- Three propellant economies: petroleum, Martian methalox, and advanced hydrogen.
- A 7×7 mechanical rocket build using 35 placed subassemblies and all required vehicle systems.
- Nine quest branches dependent on the existing Era progression but displayed in the adjacent top-level `Space Industrialization` quest group.

## Item texture reauthoring

- The original 97 catalog icons were generated directly at 16x16 with Pillow primitives and are rejected as final artwork.
- Replacement uses a reuse-first policy: semantically suitable artwork already shipped in the pack is alpha-fitted to 128px; built-in image generation is reserved for parts with no honest existing equivalent.
- Bespoke icons use one full-resolution generated master per item, genuine alpha transparency, retained workspace masters, and inspected Lanczos reduction to 128x128.
- The catalog generator now creates the old 16px icons only when a texture is missing; rerunning it cannot overwrite authored replacements.
- Progress is recorded in `docs/space-industry-authored-item-textures.csv` and `docs/space-industry-reused-item-textures.csv`.

## Authority and compatibility decisions

- No Stellaris jar classes or resources are modified.
- No duplicate titanium, steel, aluminum, nickel, sulfur, hydrogen or oxygen base material was registered. Planetary feeds refine into existing pack materials or reusable aerospace composites.
- Native `stellaris:rocket`, oxygen distributor, tanks, suits, engine, fins, nose cone, launch pad and station remain the functional endpoints; only their data recipes are authoritatively replaced.
- The expansion uses recipes and equipment-change events; it adds no continuous world scans or custom ticking machines.
- All generated content is owned by this catalog. Modify the catalog and rerun the generator instead of layering corrective scripts.
"""
    write(ROOT / "dev/docs" / "stellaris-space-industry.md", text)


def main() -> None:
    generate_startup()
    generate_recipes()
    generate_worldgen()
    generate_tags()
    generate_suits()
    generate_stellaris_overrides()
    generate_textures()
    generate_quests()
    generate_docs()
    print(f"Generated {sum(len(v['items']) for v in COMPONENT_FAMILIES.values())} components, {len(ORES)} ores, {len(SUITS)} suit definitions")


if __name__ == "__main__":
    main()
