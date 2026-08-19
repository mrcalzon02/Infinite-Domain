// Phase I authority for Create Nuclear feed preparation. The installed
// controller still consumes the original uranium_rod and graphite_rod items;
// this script makes those two accepted endpoints the result of full factories.
const nuclearCycle = JsonIO.read('kubejs/config/nuclear_fuel_cycle.json')

ServerEvents.recipes(event => {
    const u = nuclearCycle.uranium
    const g = nuclearCycle.graphite
    const organic = nuclearCycle.organicInputs

    // Remove the compact installed chain and all mined-material routes that can
    // jump directly to raw uranium, uranium dust, or a finished reactor rod.
    ;[
        'createnuclear:crushing/crushed_raw_uranium',
        'createnuclear:mixing/uranium_fluid',
        'createnuclear:compacting/uranium_fluid_to_yellowcake',
        'createnuclear:enriched/enriched_yellowcake',
        'createnuclear:mechanical_crafting/uranium_rod',
        'createnuclear:crushing/coal',
        'createnuclear:pressing/graphene',
        'createnuclear:mechanical_crafting/graphite_rod',
        'createnuclear:smelting/raw_uranium_for_uranium_ore',
        'createnuclear:blasting/raw_uranium_for_uranium_ore'
    ].forEach(id => event.remove({ id: id }))

    const minedForms = ['#c:ores/uranium', '#c:raw_materials/uranium', '#c:storage_blocks/raw_uranium', 'create:crushed_raw_uranium']
    const bypassOutputs = [
        'createnuclear:raw_uranium', 'immersiveengineering:raw_uranium', 'oritech:raw_uranium',
        'createnuclear:uranium_powder', 'immersiveengineering:dust_uranium', 'oritech:uranium_dust',
        'createnuclear:yellowcake', 'createnuclear:enriched_yellowcake', 'createnuclear:uranium_rod'
    ]
    minedForms.forEach(input => bypassOutputs.forEach(output => event.remove({ input: input, output: output })))
    event.remove({ output: u.finishedRod })
    event.remove({ output: g.finishedRod })

    // Uranium: concentration -> fictionalized organic extraction -> pellets ->
    // visible cladding assembly -> final heated seal.
    event.recipes.create.crushing(u.fines, u.trace)
        .processingTime(180).id('infinite_domain:nuclear/uranium_bearing_fines')
    event.recipes.create.splashing(u.washedConcentrate, u.fines)
        .id('infinite_domain:nuclear/washed_uranium_concentrate')
    event.recipes.create.mixing(Fluid.of(u.slurry, 1000), [
        Item.of(u.washedConcentrate, u.tracesPerBatch),
        Fluid.of(organic.extractionReagent, 250),
        Fluid.of('minecraft:water', 750)
    ]).heated().id('infinite_domain:nuclear/leached_uranium_slurry')
    event.recipes.create.compacting([
        Item.of(u.purifiedCompound, u.purifiedCompoundPerBatch),
        Item.of(u.tailings),
        Fluid.of(nuclearCycle.wasteFluid, 250)
    ], Fluid.of(u.slurry, 1000)).heated().id('infinite_domain:nuclear/purified_uranium_compound')
    event.recipes.create.crushing(Item.of(u.fuelPowder, 2), u.purifiedCompound)
        .processingTime(240).id('infinite_domain:nuclear/fuel_grade_powder')
    event.recipes.create.compacting(u.greenPellet, [
        u.fuelPowder,
        Fluid.of(organic.pelletBinder, 50)
    ]).id('infinite_domain:nuclear/green_fuel_pellet')
    event.blasting(u.firedPellet, u.greenPellet).xp(0.2)
        .id('infinite_domain:nuclear/fired_fuel_pellet')
    event.recipes.create.compacting(u.pelletStack, Item.of(u.firedPellet, u.pelletsPerRod))
        .id('infinite_domain:nuclear/fuel_pellet_stack')
    event.recipes.create.pressing(u.emptyCladding, Ingredient.of('#c:ingots/steel'))
        .id('infinite_domain:nuclear/empty_fuel_cladding')

    event.custom({
        type: 'create:sequenced_assembly',
        ingredient: { item: u.emptyCladding },
        loops: 1,
        results: [{ id: u.incompleteRod }],
        sequence: [
            {
                type: 'create:deploying',
                ingredients: [{ item: u.incompleteRod }, { item: u.pelletStack }],
                results: [{ id: u.incompleteRod }]
            },
            {
                type: 'create:deploying',
                ingredients: [{ item: u.incompleteRod }, { tag: 'c:plates/lead' }],
                results: [{ id: u.incompleteRod }]
            },
            {
                type: 'create:pressing',
                ingredients: [{ item: u.incompleteRod }],
                results: [{ id: u.incompleteRod }]
            }
        ],
        transitional_item: { id: u.incompleteRod }
    }).id('infinite_domain:nuclear/standard_fuel_rod_assembly')
    event.recipes.create.compacting(u.finishedRod, [u.incompleteRod, Fluid.of('minecraft:water', 100)])
        .heated().id('infinite_domain:nuclear/standard_fuel_rod_sealing')

    // Graphite is now an eight-operation carbon industry. In Phase I the
    // installed controller still treats its output as cooling; Phase II will
    // move the item to an explicit moderator profile.
    event.recipes.create.milling(Item.of(g.carbonFines, 2), Ingredient.of('#minecraft:coals'))
        .processingTime(160).id('infinite_domain:nuclear/carbon_fines')
    event.recipes.create.splashing(g.washedCarbon, g.carbonFines)
        .id('infinite_domain:nuclear/washed_carbon')
    event.blasting(g.refinedCarbon, g.washedCarbon).xp(0.05)
        .id('infinite_domain:nuclear/refined_reactor_carbon')
    event.recipes.create.mixing(Item.of(g.boundGraphite, 4), [
        Item.of(g.refinedCarbon, 4), Item.of(organic.graphiteBinder)
    ]).heated().id('infinite_domain:nuclear/bound_graphite_mix')
    event.recipes.create.compacting(g.greenBlank, Item.of(g.boundGraphite, 4))
        .id('infinite_domain:nuclear/green_graphite_blank')
    event.blasting(g.bakedBlank, g.greenBlank).xp(0.1)
        .id('infinite_domain:nuclear/baked_graphite_blank')
    event.recipes.create.mixing([
        g.purifiedBlank, Fluid.of(nuclearCycle.wasteFluid, 100)
    ], [g.bakedBlank, Fluid.of(organic.extractionReagent, 100)]).heated()
        .id('infinite_domain:nuclear/purified_graphite_blank')
    event.recipes.create.cutting(Item.of(g.component, 4), g.purifiedBlank)
        .processingTime(200).id('infinite_domain:nuclear/machined_graphite_component')
    event.custom({
        type: 'create:mechanical_crafting',
        accept_mirrored: true,
        category: 'misc',
        key: {
            C: { item: g.component },
            S: { tag: 'c:ingots/steel' }
        },
        pattern: ['SCS', 'SCS', 'SCS', 'SCS'],
        result: { count: 1, id: g.finishedRod }
    }).id('infinite_domain:nuclear/nuclear_grade_graphite_rod')
})
