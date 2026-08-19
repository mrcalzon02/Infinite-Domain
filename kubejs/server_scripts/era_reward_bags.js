// Side-lesson reward bags. Entries are useful inputs and subassemblies from the
// named era, never complete gateway machines or capstone items.
const eraRewardBagTables = {
    'kubejs:era0_priority_cache': { rolls: 4, entries: [
        ['the_wasteland_reworked:bandage', 18, 1, 3], ['wastelands:purified_water', 18, 1, 3],
        ['wastelands:canned_food', 18, 1, 3], ['wastelands:filter_canister', 10, 1, 2],
        ['minecraft:coal', 10, 4, 12], ['minecraft:iron_ingot', 6, 1, 3],
        ['spore:gas_mask', 2, 1, 1], ['the_wasteland_reworked:scrap_metal', 12, 2, 6]
    ]},
    'kubejs:era1_supply_bag': { rolls: 2, entries: [
        ['create:andesite_alloy', 18, 2, 6], ['create:shaft', 14, 4, 12],
        ['create:cogwheel', 14, 2, 6], ['create:large_cogwheel', 10, 1, 3],
        ['create:belt_connector', 12, 1, 3], ['minecraft:copper_ingot', 12, 2, 6],
        ['farmersdelight:rope', 8, 2, 6], ['sophisticatedstorage:upgrade_base', 5, 1, 1]
    ]},
    'kubejs:era1_priority_cache': { rolls: 4, entries: [
        ['create:precision_mechanism', 14, 1, 1], ['create:brass_ingot', 14, 1, 3],
        ['create:brass_casing', 7, 1, 1], ['create:mechanical_bearing', 7, 1, 1],
        ['create:electron_tube', 12, 1, 3], ['create:sturdy_sheet', 8, 1, 2],
        ['sophisticatedstorage:upgrade_base', 12, 1, 2], ['create:belt_connector', 14, 2, 5]
    ]},
    'kubejs:era2_supply_bag': { rolls: 2, entries: [
        ['tfmg:steel_ingot', 18, 1, 3], ['tfmg:coal_coke', 16, 2, 6],
        ['tfmg:heavy_plate', 12, 1, 3], ['tfmg:fireproof_bricks', 14, 2, 6],
        ['tfmg:cast_iron_pipe', 10, 2, 6], ['createmetallurgy:graphite_ingot_mold', 7, 1, 1],
        ['createreautomated:node_fragment', 8, 1, 2], ['tfmg:steel_cogwheel', 10, 1, 3]
    ]},
    'kubejs:era2_priority_cache': { rolls: 4, entries: [
        ['tfmg:steel_mechanism', 15, 1, 2], ['tfmg:heavy_plate', 15, 2, 5],
        ['tfmg:steel_casing', 10, 1, 2], ['tfmg:steel_fluid_tank', 8, 1, 2],
        ['tfmg:steel_mechanical_pump', 8, 1, 1], ['create:sturdy_sheet', 12, 1, 3],
        ['createreautomated:node_fragment', 10, 2, 4], ['tfmg:fireproof_brick_reinforcement', 12, 2, 5]
    ]},
    'kubejs:era3_supply_bag': { rolls: 2, entries: [
        ['tfmg:plastic_sheet', 16, 2, 6], ['tfmg:rubber_sheet', 16, 2, 6],
        ['petrochem:sulfur_dust', 16, 2, 6], ['petrochem:petroleum_coke', 14, 2, 6],
        ['petrochem:steel_fluid_pipe', 12, 2, 6], ['tfmg:steel_pipe', 10, 2, 6],
        ['createdieselgenerators:engine_piston', 7, 1, 2], ['petrochem:bronze_sheet', 9, 1, 3]
    ]},
    'kubejs:era3_priority_cache': { rolls: 4, entries: [
        ['tfmg:circuit_board', 13, 1, 2], ['petrochem:steel_fluid_tank', 12, 1, 2],
        ['createdieselgenerators:pumpjack_head', 8, 1, 1], ['createdieselgenerators:engine_piston', 12, 1, 3],
        ['petrochem:sulfuric_acid_bucket', 6, 1, 1], ['tfmg:plastic_block', 10, 1, 2],
        ['tfmg:rubber_sheet', 14, 4, 8], ['petrochem:steel_sheet', 14, 2, 5]
    ]},
    'kubejs:era4_supply_bag': { rolls: 2, entries: [
        ['create_new_age:copper_wire', 16, 4, 12], ['powergrid:insulated_copper_wire', 16, 4, 12],
        ['powergrid:copper_coil', 12, 1, 3], ['powergrid:circuit_board', 12, 1, 3],
        ['create_new_age:layered_magnet', 10, 1, 3], ['powergrid:wire_connector', 12, 2, 6],
        ['powergrid:resistive_coil', 10, 1, 3], ['create_new_age:overcharged_iron_wire', 8, 1, 3]
    ]},
    'kubejs:era4_priority_cache': { rolls: 4, entries: [
        ['powergrid:integrated_circuit', 14, 1, 2], ['powergrid:portable_battery', 8, 1, 1],
        ['powergrid:transformer_core', 12, 1, 2], ['create_new_age:generator_coil', 12, 1, 2],
        ['create_new_age:copper_circuit', 14, 1, 3], ['powergrid:heavy_wire_connector', 10, 1, 3],
        ['create_new_age:basic_motor', 6, 1, 1], ['powergrid:battery', 12, 1, 2]
    ]},
    'kubejs:era5_supply_bag': { rolls: 2, entries: [
        ['ae2:certus_quartz_crystal', 16, 4, 12], ['ae2:fluix_crystal', 14, 2, 6],
        ['ae2:fluix_glass_cable', 14, 4, 12], ['ae2:logic_processor', 10, 1, 2],
        ['oritech:biosteel_ingot', 12, 1, 3], ['oritech:motor', 10, 1, 2],
        ['createcybernetics:component_wiring', 10, 1, 3], ['createcybernetics:component_storage', 8, 1, 2]
    ]},
    'kubejs:era5_priority_cache': { rolls: 4, entries: [
        ['ae2:engineering_processor', 14, 1, 2], ['ae2:calculation_processor', 14, 1, 2],
        ['ae2:cell_component_4k', 10, 1, 1], ['oritech:machine_core_1', 10, 1, 2],
        ['oritech:adamant_ingot', 10, 1, 3], ['createcybernetics:component_fiberoptics', 10, 1, 3],
        ['createcybernetics:component_synthnerves', 8, 1, 2], ['ae2:energy_cell', 6, 1, 1]
    ]},
    'kubejs:era6_supply_bag': { rolls: 2, entries: [
        ['createnuclear:uranium_powder', 16, 2, 6], ['createnuclear:yellowcake', 14, 1, 4],
        ['createnuclear:lead_ingot', 14, 2, 6], ['createnuclear:reactor_casing', 10, 1, 3],
        ['wastelands:rad_away', 12, 1, 3], ['wastelands:purified_water', 10, 2, 6],
        ['oritech:plutonium_dust', 8, 1, 2], ['create_new_age:nuclear_fuel', 6, 1, 2]
    ]},
    'kubejs:era6_priority_cache': { rolls: 4, entries: [
        ['createnuclear:enriched_yellowcake', 14, 1, 3], ['createnuclear:uranium_rod', 12, 1, 3],
        ['oritech:advanced_battery', 10, 1, 1], ['oritech:plutonium_pellet', 10, 1, 2],
        ['createnuclear:reactor_casing', 14, 2, 5], ['create_new_age:nuclear_fuel', 10, 2, 4],
        ['ae2:engineering_processor', 12, 1, 3], ['wastelands:rad_away', 12, 2, 5]
    ]},
    'kubejs:era7_supply_bag': { rolls: 2, entries: [
        ['stellaris:desh_ingot', 16, 1, 3], ['stellaris:steel_ingot', 14, 2, 6],
        ['stellaris:heavy_metal_ingot', 12, 1, 3], ['stellaris:corronium_ingot', 10, 1, 3],
        ['stellaris:oxygen_tank', 10, 1, 2], ['stellaris:ice_shard', 14, 2, 6],
        ['oritech:machine_core_5', 5, 1, 1], ['ae2:cell_component_16k', 7, 1, 1]
    ]},
    'kubejs:era7_priority_cache': { rolls: 4, entries: [
        ['stellaris:desh_block', 12, 1, 2], ['stellaris:desh_plating_block', 12, 1, 3],
        ['stellaris:big_oxygen_tank', 8, 1, 1], ['oritech:machine_core_5', 10, 1, 2],
        ['ae2:cell_component_64k', 8, 1, 1], ['oritech:advanced_battery', 12, 1, 2],
        ['stellaris:heavy_metal_ingot', 14, 2, 5], ['stellaris:corronium_ingot', 14, 2, 5]
    ]},
    'kubejs:era8_supply_bag': { rolls: 2, entries: [
        ['oritech:prometheum_ingot', 12, 1, 3], ['oritech:superconductor', 12, 1, 3],
        ['oritech:machine_core_7', 5, 1, 1], ['ae2:cell_component_64k', 12, 1, 2],
        ['ae2:engineering_processor', 14, 2, 5], ['ae2:calculation_processor', 14, 2, 5],
        ['stellaris:desh_block', 10, 1, 2], ['createnuclear:uranium_rod', 10, 2, 5]
    ]},
    'kubejs:era8_priority_cache': { rolls: 4, entries: [
        ['oritech:machine_core_7', 12, 1, 2], ['ae2:cell_component_256k', 10, 1, 1],
        ['ae2:dense_energy_cell', 7, 1, 1], ['oritech:prometheum_ingot', 14, 2, 5],
        ['oritech:superconductor', 14, 2, 5], ['stellaris:desh_block', 12, 2, 4],
        ['createnuclear:reactor_casing', 12, 2, 5], ['ae2:engineering_processor', 14, 3, 6]
    ]}
}

function chooseEraReward(entries) {
    let total = entries.reduce((sum, entry) => sum + entry[1], 0)
    let choice = Math.random() * total
    for (const entry of entries) {
        choice -= entry[1]
        if (choice < 0) return entry
    }
    return entries[entries.length - 1]
}

Object.entries(eraRewardBagTables).forEach(([bagId, table]) => {
    ItemEvents.rightClicked(bagId, event => {
        for (let roll = 0; roll < table.rolls; roll++) {
            const selected = chooseEraReward(table.entries)
            const count = selected[2] + Math.floor(Math.random() * (selected[3] - selected[2] + 1))
            event.player.give(Item.of(selected[0], count))
        }
        event.item.count--
    })
})
