const nuclearFuelCycle = JsonIO.read('kubejs/config/nuclear_fuel_cycle.json')

StartupEvents.registry('item', event => {
    const items = [
        ['uranium_bearing_fines', 'Uranium-Bearing Fines', 'immersiveengineering:item/metal_dust_uranium', 'Mechanically concentrated radioactive mineral fraction'],
        ['washed_uranium_concentrate', 'Washed Uranium Concentrate', 'createnuclear:item/yellowcake', 'Washed feed awaiting fictionalized chemical extraction'],
        ['purified_uranium_compound', 'Purified Uranium Compound', 'createnuclear:item/enriched_yellowcake', 'Separated nuclear feed compound; not yet reactor fuel'],
        ['stabilized_uranium_tailings', 'Stabilized Uranium Tailings', 'create:item/crushed_raw_uranium', 'Contained process residue requiring controlled storage'],
        ['fuel_grade_uranium_powder', 'Fuel-Grade Uranium Powder', 'oritech:item/uranium_dust', 'Qualified powder for pellet pressing'],
        ['green_fuel_pellet', 'Green Fuel Pellet', 'oritech:item/uranium_pellet', 'Pressed pellet requiring high-temperature firing'],
        ['fired_fuel_pellet', 'Fired Fuel Pellet', 'oritech:item/uranium_pellet', 'Stable pellet ready for stacking and cladding'],
        ['fuel_pellet_stack', 'Fuel Pellet Stack', 'createnuclear:item/enriched_yellowcake', 'Eight fired pellets prepared as one rod charge'],
        ['empty_fuel_cladding', 'Empty Fuel Cladding', 'immersiveengineering:item/metal_plate_steel', 'Pressed steel tube for a standard reactor rod'],
        ['incomplete_standard_fuel_rod', 'Incomplete Standard Fuel Rod', 'createnuclear:item/uranium_rod', 'Loaded and capped assembly awaiting final sealing'],
        ['carbon_fines', 'Carbon Fines', 'createnuclear:item/coal_dust', 'Sized carbon feed for nuclear graphite'],
        ['washed_carbon', 'Washed Carbon', 'createnuclear:item/coal_dust', 'Low-ash carbon fraction'],
        ['refined_reactor_carbon', 'Refined Reactor Carbon', 'minecraft:item/charcoal', 'Thermally refined carbon for graphite manufacture'],
        ['bound_graphite_mix', 'Bound Graphite Mix', 'createnuclear:item/graphene', 'Refined carbon combined with a renewable binder'],
        ['green_graphite_blank', 'Green Graphite Blank', 'createnuclear:item/graphene', 'Pressed graphite blank awaiting baking'],
        ['baked_graphite_blank', 'Baked Graphite Blank', 'createnuclear:item/graphene', 'Baked graphite requiring final purification'],
        ['purified_graphite_blank', 'Purified Graphite Blank', 'createnuclear:item/graphene', 'High-purity blank ready for machining'],
        ['nuclear_graphite_component', 'Nuclear-Grade Graphite Component', 'createnuclear:item/graphite_rod', 'Finished graphite segment for the installed reactor rod']
    ]

    items.forEach(entry => {
        event.create(entry[0]).displayName(entry[1]).texture(entry[2]).tooltip(`§7${entry[3]}`)
    })
})

StartupEvents.registry('fluid', event => {
    event.create(nuclearFuelCycle.uranium.slurry.split(':')[1])
        .displayName('Leached Uranium Slurry')
        .tint(0x9CAA36)
        .translucent()
    event.create(nuclearFuelCycle.wasteFluid.split(':')[1])
        .displayName('Spent Nuclear Process Solution')
        .tint(0x5E6544)
        .translucent()
})
