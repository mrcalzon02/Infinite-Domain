// Single recipe authority for Infinite Domain's industrial food economy.
const foodIndustry = JsonIO.read('kubejs/config/industrial_food.json')

ServerEvents.tags('item', event => {
    event.add('infinite_domain:juice_fruits', foodIndustry.flavors.map(f => f.crop))
    event.add('infinite_domain:seasoning_crops', ['farmersdelight:onion', 'brewery:hop', 'minecraft:dried_kelp'])
    event.add('infinite_domain:oilseeds', ['minecraft:pumpkin_seeds', 'minecraft:melon_seeds'])
    event.add('infinite_domain:industrial_vegetables', ['minecraft:carrot', 'minecraft:potato', 'minecraft:beetroot', 'farmersdelight:cabbage', 'farmersdelight:onion', 'farmersdelight:tomato'])
    event.add('infinite_domain:meal_proteins', ['minecraft:cooked_beef', 'minecraft:cooked_chicken', 'minecraft:cooked_porkchop', 'minecraft:cooked_mutton', 'farmersdelight:cooked_bacon'])
})

ServerEvents.recipes(event => {
    const r = foodIndustry.resources
    const itemIngredient = value => typeof value === 'string' && value.startsWith('#')
        ? Ingredient.of(value)
        : value

    // Seasoning: agricultural aromatics become one readable industrial input.
    event.smoking('kubejs:dried_herbs', '#infinite_domain:seasoning_crops').xp(0.05)
        .id('infinite_domain:food/dried_herbs')
    event.recipes.create.milling(Item.of('kubejs:ground_spice', 2), 'kubejs:dried_herbs')
        .processingTime(100).id('infinite_domain:food/ground_spice')
    event.recipes.create.mixing(Item.of('kubejs:prepared_seasoning', 2), [
        Item.of('kubejs:ground_spice', 2), r.salt
    ]).id('infinite_domain:food/prepared_seasoning')

    // Oil: crushing and pressing improve useful yield and return seed meal.
    event.recipes.create.milling(Item.of('kubejs:crushed_oilseed', 2), Ingredient.of('#infinite_domain:oilseeds'))
        .processingTime(120).id('infinite_domain:food/crushed_oilseed')
    event.recipes.create.compacting([
        Fluid.of('kubejs:crude_vegetable_oil', 250), Item.of('kubejs:seed_meal')
    ], Item.of('kubejs:crushed_oilseed', 4)).id('infinite_domain:food/crude_vegetable_oil')
    event.recipes.create.mixing(Fluid.of('kubejs:cooking_oil', 250), [
        Fluid.of('kubejs:crude_vegetable_oil', 250), 'minecraft:charcoal'
    ]).heated().id('infinite_domain:food/cooking_oil')

    // Vegetable broth and concentrated soup feed prepared meals and cans.
    event.recipes.create.cutting(Item.of('kubejs:chopped_vegetables', 2), Ingredient.of('#infinite_domain:industrial_vegetables'))
        .processingTime(80).id('infinite_domain:food/chopped_vegetables')
    event.recipes.create.mixing([Fluid.of('kubejs:vegetable_broth', 1000), 'minecraft:glass_bottle'], [
        Item.of('kubejs:chopped_vegetables', 4), r.purifiedWater
    ]).heated().id('infinite_domain:food/vegetable_broth')
    event.recipes.create.compacting('kubejs:concentrated_soup_base', [
        Fluid.of('kubejs:vegetable_broth', 1000), r.salt
    ]).heated().id('infinite_domain:food/concentrated_soup_base')

    // Sugar and syrup establish a fluid sweetener line for manufactured drinks.
    event.recipes.create.crushing(Item.of('kubejs:crushed_sugar_biomass', 3), 'minecraft:sugar_cane')
        .processingTime(100).id('infinite_domain:food/crushed_sugar_biomass')
    event.recipes.create.mixing(Fluid.of('kubejs:raw_sugar_solution', 1000), [
        Item.of('kubejs:crushed_sugar_biomass', 4), Fluid.of('minecraft:water', 750)
    ]).heated().id('infinite_domain:food/raw_sugar_solution')
    event.recipes.create.compacting(Fluid.of('kubejs:refined_beverage_syrup', 500), [
        Fluid.of('kubejs:raw_sugar_solution', 1000), 'minecraft:charcoal'
    ]).heated().id('infinite_domain:food/refined_beverage_syrup')

    // Fermentation turns processing waste into captured, reusable process CO2.
    event.shapeless('kubejs:fermentation_culture', ['brewery:brewers_yeast', 'minecraft:honey_bottle'])
        .id('infinite_domain:food/fermentation_culture')
    event.recipes.create.mixing([
        Fluid.of('kubejs:process_co2', 500), 'kubejs:fermentation_culture'
    ], ['kubejs:fruit_pomace', 'minecraft:sugar', 'kubejs:fermentation_culture', Fluid.of('minecraft:water', 250)])
        .heated().id('infinite_domain:food/captured_process_co2')

    // Shared container economy: aluminum drink cans and heavier steel food cans.
    event.recipes.create.pressing(Item.of('kubejs:empty_beverage_can', foodIndustry.balance.cansPerAluminumPlate), itemIngredient(r.aluminumPlate))
        .id('infinite_domain:food/empty_beverage_can')
    event.recipes.create.pressing(Item.of('kubejs:empty_food_can', foodIndustry.balance.foodCansPerSteelPlate), itemIngredient(r.steelPlate))
        .id('infinite_domain:food/empty_food_can')

    // Diversified meals outperform single-food survival without becoming magic.
    event.recipes.create.mixing('kubejs:prepared_meal', [
        Ingredient.of('#infinite_domain:meal_proteins'), Item.of('kubejs:chopped_vegetables', 2),
        'farmersdelight:cooked_rice', 'kubejs:prepared_seasoning', Fluid.of('kubejs:cooking_oil', 100)
    ]).heated().id('infinite_domain:food/prepared_meal')
    event.recipes.create.sequenced_assembly(
        ['kubejs:canned_stew'],
        'kubejs:empty_food_can',
        [
            event.recipes.create.deploying('kubejs:filled_food_can', ['kubejs:filled_food_can', 'kubejs:prepared_meal']),
            event.recipes.create.filling('kubejs:filled_food_can', ['kubejs:filled_food_can', Fluid.of('kubejs:vegetable_broth', 100)]),
            event.recipes.create.pressing('kubejs:filled_food_can', 'kubejs:filled_food_can')
        ]
    ).transitionalItem('kubejs:filled_food_can').loops(1)
        .id('infinite_domain:food/canned_settlement_stew')

    // Three crop-supported juice and soda families share one factory grammar.
    foodIndustry.flavors.forEach(flavor => {
        const id = flavor.id
        event.recipes.create.crushing([
            Item.of(`kubejs:${id}_fruit_pulp`, 2), CreateItem.of('kubejs:fruit_pomace', 0.5)
        ], flavor.crop).processingTime(120).id(`infinite_domain:food/${id}_fruit_pulp`)
        event.recipes.create.compacting(Fluid.of(`kubejs:pressed_${id}_juice`, 500), Item.of(`kubejs:${id}_fruit_pulp`, 3))
            .id(`infinite_domain:food/pressed_${id}_juice`)
        event.recipes.create.compacting(`kubejs:${id}_juice_concentrate`, Fluid.of(`kubejs:pressed_${id}_juice`, 1000))
            .heated().id(`infinite_domain:food/${id}_juice_concentrate`)
        event.recipes.create.mixing([
            Fluid.of(`kubejs:prepared_${id}_beverage`, 1000), 'minecraft:glass_bottle'
        ], [`kubejs:${id}_juice_concentrate`, r.purifiedWater, Fluid.of('minecraft:water', 500)])
            .id(`infinite_domain:food/prepared_${id}_beverage`)
        event.recipes.create.filling(`kubejs:bottled_${id}_juice`, [
            'minecraft:glass_bottle', Fluid.of(`kubejs:prepared_${id}_beverage`, 250)
        ]).id(`infinite_domain:food/bottled_${id}_juice`)
        event.recipes.create.mixing(Fluid.of(`kubejs:${id}_soda_base`, 1000), [
            `kubejs:${id}_juice_concentrate`, Fluid.of('kubejs:refined_beverage_syrup', 250),
            Fluid.of(`kubejs:prepared_${id}_beverage`, 750)
        ]).id(`infinite_domain:food/${id}_soda_base`)
        event.recipes.create.mixing(Fluid.of(`kubejs:carbonated_${id}_soda`, 1000), [
            Fluid.of(`kubejs:${id}_soda_base`, 1000), Fluid.of('kubejs:process_co2', 250)
        ]).id(`infinite_domain:food/carbonated_${id}_soda`)
        event.recipes.create.filling(`kubejs:${id}_soda_can`, [
            'kubejs:empty_beverage_can', Fluid.of(`kubejs:carbonated_${id}_soda`, 250)
        ]).id(`infinite_domain:food/${id}_soda_can`)
        event.recipes.create.compacting(`kubejs:${id}_soda_six_pack`, [
            Item.of(`kubejs:${id}_soda_can`, 6), r.paperBundle
        ]).id(`infinite_domain:food/${id}_soda_six_pack`)
        event.recipes.create.compacting(`kubejs:${id}_soda_case`, [
            Item.of(`kubejs:${id}_soda_six_pack`, 4), r.paperBundle
        ]).id(`infinite_domain:food/${id}_soda_case`)
        event.shapeless(Item.of(`kubejs:${id}_soda_can`, 6), [`kubejs:${id}_soda_six_pack`])
            .id(`infinite_domain:food/unpack_${id}_soda_six_pack`)
        event.shapeless(Item.of(`kubejs:${id}_soda_six_pack`, 4), [`kubejs:${id}_soda_case`])
            .id(`infinite_domain:food/unpack_${id}_soda_case`)
    })

    // Energy beverages connect food production to salt/mineral chemistry.
    event.recipes.create.mixing('kubejs:electrolyte_blend', [r.salt, 'minecraft:bone_meal'])
        .id('infinite_domain:food/electrolyte_blend')
    event.recipes.create.mixing('kubejs:stimulant_extract', [
        'minecraft:cocoa_beans', 'brewery:hop', Fluid.of('kubejs:refined_beverage_syrup', 100)
    ]).heated().id('infinite_domain:food/stimulant_extract')
    event.recipes.create.mixing([
        Fluid.of('kubejs:energy_beverage_base', 1000), 'minecraft:glass_bottle'
    ], [r.purifiedWater, 'kubejs:berry_juice_concentrate', 'kubejs:electrolyte_blend',
        'kubejs:stimulant_extract', Fluid.of('kubejs:refined_beverage_syrup', 250)])
        .id('infinite_domain:food/energy_beverage_base')
    event.recipes.create.mixing(Fluid.of('kubejs:carbonated_energy_beverage', 1000), [
        Fluid.of('kubejs:energy_beverage_base', 1000), Fluid.of('kubejs:process_co2', 250)
    ]).id('infinite_domain:food/carbonated_energy_beverage')
    event.recipes.create.filling('kubejs:energy_drink_can', [
        'kubejs:empty_beverage_can', Fluid.of('kubejs:carbonated_energy_beverage', 250)
    ]).id('infinite_domain:food/energy_drink_can')
    event.recipes.create.compacting('kubejs:energy_six_pack', [Item.of('kubejs:energy_drink_can', 6), r.paperBundle])
        .id('infinite_domain:food/energy_six_pack')
    event.recipes.create.compacting('kubejs:energy_case', [Item.of('kubejs:energy_six_pack', 4), r.paperBundle])
        .id('infinite_domain:food/energy_case')
    event.shapeless(Item.of('kubejs:energy_drink_can', 6), ['kubejs:energy_six_pack']).id('infinite_domain:food/unpack_energy_six_pack')
    event.shapeless(Item.of('kubejs:energy_six_pack', 4), ['kubejs:energy_case']).id('infinite_domain:food/unpack_energy_case')

    // Coffee and tea are zero-food work beverages. The installed pack has no
    // compatible Create Cafe/Brewing build, so this native chain reuses the
    // shared crop, fluid, cup, bottle, can, crate, and pallet infrastructure.
    event.shapeless(Item.of('kubejs:coffee_cherries', 2), ['minecraft:cocoa_beans', 'minecraft:sweet_berries'])
        .id('infinite_domain:food/coffee_cherry_cultivar')
    event.recipes.create.cutting([CreateItem.of('kubejs:pulped_coffee_cherries', 2 / 3), CreateItem.of('kubejs:fruit_pomace', 0.5)], 'kubejs:coffee_cherries')
        .processingTime(100).id('infinite_domain:food/pulp_coffee_cherries')
    event.recipes.create.splashing('kubejs:green_coffee_beans', 'kubejs:pulped_coffee_cherries')
        .id('infinite_domain:food/wash_green_coffee_beans')
    event.smelting('kubejs:light_roast_coffee_beans', 'kubejs:green_coffee_beans').xp(0.05)
        .id('infinite_domain:food/light_roast_coffee')
    event.smelting('kubejs:medium_roast_coffee_beans', 'kubejs:light_roast_coffee_beans').xp(0.05)
        .id('infinite_domain:food/medium_roast_coffee')
    event.smelting('kubejs:dark_roast_coffee_beans', 'kubejs:medium_roast_coffee_beans').xp(0.05)
        .id('infinite_domain:food/dark_roast_coffee')
    ;['light', 'medium', 'dark'].forEach(roast => {
        event.recipes.create.milling(Item.of('kubejs:coffee_grounds', 2), `kubejs:${roast}_roast_coffee_beans`)
            .processingTime(100).id(`infinite_domain:food/${roast}_roast_grounds`)
    })
    event.recipes.create.mixing(Fluid.of('kubejs:brewed_coffee', 1000), [Item.of('kubejs:coffee_grounds', 4), r.purifiedWater, Fluid.of('minecraft:water', 500)])
        .heated().id('infinite_domain:food/brewed_coffee')
    event.recipes.create.compacting(Fluid.of('kubejs:coffee_concentrate', 500), Fluid.of('kubejs:brewed_coffee', 1000))
        .heated().id('infinite_domain:food/coffee_concentrate')
    event.recipes.create.mixing([Fluid.of('kubejs:milk_coffee', 1000), 'minecraft:bucket'], [Fluid.of('kubejs:brewed_coffee', 1000), 'minecraft:milk_bucket'])
        .id('infinite_domain:food/milk_coffee')
    event.recipes.create.mixing(Fluid.of('kubejs:cold_brew', 1000), [Item.of('kubejs:coffee_grounds', 5), r.purifiedWater, Fluid.of('minecraft:water', 500)])
        .id('infinite_domain:food/cold_brew')
    event.recipes.create.filling('kubejs:black_coffee_mug', ['stellaris:coffee_cup', Fluid.of('kubejs:brewed_coffee', 250)]).id('infinite_domain:food/black_coffee_mug')
    event.recipes.create.filling('kubejs:espresso_mug', ['stellaris:coffee_cup', Fluid.of('kubejs:coffee_concentrate', 125)]).id('infinite_domain:food/espresso_mug')
    event.recipes.create.filling('kubejs:latte_mug', ['stellaris:coffee_cup', Fluid.of('kubejs:milk_coffee', 250)]).id('infinite_domain:food/latte_mug')
    event.recipes.create.filling('kubejs:cold_brew_bottle', ['minecraft:glass_bottle', Fluid.of('kubejs:cold_brew', 250)]).id('infinite_domain:food/cold_brew_bottle')
    event.recipes.create.filling('kubejs:canned_coffee', ['kubejs:empty_beverage_can', Fluid.of('kubejs:brewed_coffee', 250)]).id('infinite_domain:food/canned_coffee')

    event.recipes.create.cutting(Item.of('kubejs:fresh_tea_leaves', 2), 'brewery:hop').processingTime(80)
        .id('infinite_domain:food/fresh_tea_leaves')
    event.smoking('kubejs:green_tea_leaves', 'kubejs:fresh_tea_leaves').xp(0.05).id('infinite_domain:food/green_tea_leaves')
    event.recipes.create.milling('kubejs:black_tea_leaves', 'kubejs:fresh_tea_leaves').processingTime(120).id('infinite_domain:food/black_tea_leaves')
    event.recipes.create.mixing('kubejs:oolong_tea_leaves', ['kubejs:fresh_tea_leaves', 'kubejs:green_tea_leaves']).heated().id('infinite_domain:food/oolong_tea_leaves')
    ;['green', 'black', 'oolong'].forEach(tea => {
        event.recipes.create.mixing(Fluid.of(`kubejs:${tea}_tea`, 1000), [Item.of(`kubejs:${tea}_tea_leaves`, 4), r.purifiedWater, Fluid.of('minecraft:water', 500)])
            .heated().id(`infinite_domain:food/brewed_${tea}_tea`)
        event.recipes.create.filling(`kubejs:${tea}_tea_cup`, ['stellaris:coffee_cup', Fluid.of(`kubejs:${tea}_tea`, 250)])
            .id(`infinite_domain:food/${tea}_tea_cup`)
    })
    event.recipes.create.mixing(Fluid.of('kubejs:iced_tea', 1000), [Fluid.of('kubejs:black_tea', 750), Fluid.of('kubejs:refined_beverage_syrup', 100), r.purifiedWater])
        .id('infinite_domain:food/iced_tea')
    event.recipes.create.filling('kubejs:bottled_iced_tea', ['minecraft:glass_bottle', Fluid.of('kubejs:iced_tea', 250)]).id('infinite_domain:food/bottled_iced_tea')
    event.recipes.create.filling('kubejs:canned_iced_tea', ['kubejs:empty_beverage_can', Fluid.of('kubejs:iced_tea', 250)]).id('infinite_domain:food/canned_iced_tea')

    ;[['coffee', 'canned_coffee'], ['tea', 'canned_iced_tea']].forEach(line => {
        const family = line[0], drink = line[1]
        event.recipes.create.compacting(`kubejs:${family}_six_pack`, [Item.of(`kubejs:${drink}`, 6), r.paperBundle]).id(`infinite_domain:food/${family}_six_pack`)
        event.recipes.create.compacting(`kubejs:${family}_case`, [Item.of(`kubejs:${family}_six_pack`, 4), r.paperBundle]).id(`infinite_domain:food/${family}_case`)
        event.recipes.create.compacting(`kubejs:${family}_crate`, [Item.of(`kubejs:${family}_case`, 4), r.woodenCrate]).id(`infinite_domain:food/${family}_crate`)
        event.recipes.create.compacting(`kubejs:${family}_pallet`, [Item.of(`kubejs:${family}_crate`, foodIndustry.balance.cratesPerPallet), r.emptyPallet]).id(`infinite_domain:food/${family}_pallet`)
        event.shapeless(Item.of(`kubejs:${drink}`, 6), [`kubejs:${family}_six_pack`]).id(`infinite_domain:food/unpack_${family}_six_pack`)
        event.shapeless(Item.of(`kubejs:${family}_six_pack`, 4), [`kubejs:${family}_case`]).id(`infinite_domain:food/unpack_${family}_case`)
        event.shapeless(Item.of(`kubejs:${family}_case`, 4), [`kubejs:${family}_crate`]).id(`infinite_domain:food/unpack_${family}_crate`)
        event.shapeless(Item.of(`kubejs:${family}_crate`, foodIndustry.balance.cratesPerPallet), [`kubejs:${family}_pallet`]).id(`infinite_domain:food/unpack_${family}_pallet`)
    })

    // Field rations are components and packaging, never steak wrapped in paper.
    event.recipes.create.compacting('kubejs:ration_entree', ['kubejs:canned_stew', 'kubejs:prepared_seasoning'])
        .heated().id('infinite_domain:food/ration_entree')
    event.smelting('kubejs:grain_cracker_pack', 'farmersdelight:wheat_dough').xp(0.05)
        .id('infinite_domain:food/grain_cracker_pack')
    event.smoking('kubejs:dried_fruit_packet', 'kubejs:apple_fruit_pulp').xp(0.05)
        .id('infinite_domain:food/dried_fruit_packet')
    event.recipes.create.compacting('kubejs:beverage_powder_packet', ['kubejs:orange_juice_concentrate', 'minecraft:sugar'])
        .id('infinite_domain:food/beverage_powder_packet')
    event.recipes.create.compacting('kubejs:condiment_packet', ['kubejs:prepared_seasoning', 'minecraft:paper'])
        .id('infinite_domain:food/condiment_packet')
    event.recipes.create.compacting('kubejs:empty_ration_pouch', [r.canvas, r.paperBundle])
        .id('infinite_domain:food/empty_ration_pouch')
    event.custom({
        type: 'create:sequenced_assembly', ingredient: {item: 'kubejs:empty_ration_pouch'}, loops: 1,
        transitional_item: {id: 'kubejs:empty_ration_pouch'}, results: [{id: 'kubejs:field_ration'}],
        sequence: [
            {type: 'create:deploying', ingredients: [{item: 'kubejs:empty_ration_pouch'}, {item: 'kubejs:ration_entree'}], results: [{id: 'kubejs:empty_ration_pouch'}]},
            {type: 'create:deploying', ingredients: [{item: 'kubejs:empty_ration_pouch'}, {item: 'kubejs:grain_cracker_pack'}], results: [{id: 'kubejs:empty_ration_pouch'}]},
            {type: 'create:deploying', ingredients: [{item: 'kubejs:empty_ration_pouch'}, {item: 'kubejs:dried_fruit_packet'}], results: [{id: 'kubejs:empty_ration_pouch'}]},
            {type: 'create:deploying', ingredients: [{item: 'kubejs:empty_ration_pouch'}, {item: 'kubejs:beverage_powder_packet'}], results: [{id: 'kubejs:empty_ration_pouch'}]},
            {type: 'create:deploying', ingredients: [{item: 'kubejs:empty_ration_pouch'}, {item: 'kubejs:condiment_packet'}], results: [{id: 'kubejs:empty_ration_pouch'}]},
            {type: 'create:pressing', ingredients: [{item: 'kubejs:empty_ration_pouch'}], results: [{id: 'kubejs:empty_ration_pouch'}]}
        ]
    }).id('infinite_domain:food/field_ration_assembly')
    event.recipes.create.compacting('kubejs:ration_case', [Item.of('kubejs:field_ration', 8), r.paperBundle])
        .id('infinite_domain:food/ration_case')
    event.recipes.create.compacting('kubejs:ration_crate', [Item.of('kubejs:ration_case', 4), r.woodenCrate])
        .id('infinite_domain:food/ration_crate')
    event.shapeless(Item.of('kubejs:field_ration', 8), ['kubejs:ration_case']).id('infinite_domain:food/unpack_ration_case')
    event.shapeless(Item.of('kubejs:ration_case', 4), ['kubejs:ration_crate']).id('infinite_domain:food/unpack_ration_crate')

    event.recipes.create.compacting('kubejs:beverage_crate', [
        'kubejs:apple_soda_case', 'kubejs:berry_soda_case', 'kubejs:orange_soda_case', r.woodenCrate
    ]).id('infinite_domain:food/mixed_beverage_crate')

    // Freight pallets preserve crate counts exactly; they are logistics forms,
    // never compressed sources of additional nutrition.
    event.recipes.create.compacting('kubejs:beverage_pallet', [
        Item.of('kubejs:beverage_crate', foodIndustry.balance.cratesPerPallet), r.emptyPallet
    ]).id('infinite_domain:food/beverage_pallet')
    event.shapeless(Item.of('kubejs:beverage_crate', foodIndustry.balance.cratesPerPallet), ['kubejs:beverage_pallet'])
        .id('infinite_domain:food/unpack_beverage_pallet')
    event.recipes.create.compacting('kubejs:ration_pallet', [
        Item.of('kubejs:ration_crate', foodIndustry.balance.cratesPerPallet), r.emptyPallet
    ]).id('infinite_domain:food/ration_pallet')
    event.shapeless(Item.of('kubejs:ration_crate', foodIndustry.balance.cratesPerPallet), ['kubejs:ration_pallet'])
        .id('infinite_domain:food/unpack_ration_pallet')
})

// A mixed crate contains unlike products, which vanilla crafting cannot return
// as three distinct outputs. Right-click unpacking is deterministic and does
// no scanning or ticking.
ItemEvents.rightClicked('kubejs:beverage_crate', event => {
    event.player.give('kubejs:apple_soda_case')
    event.player.give('kubejs:berry_soda_case')
    event.player.give('kubejs:orange_soda_case')
    event.item.count--
})
