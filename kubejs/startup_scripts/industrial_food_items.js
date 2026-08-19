const industrialFood = JsonIO.read('kubejs/config/industrial_food.json')
const consumableById = {}
industrialFood.consumables.forEach(product => {
    consumableById[product.id] = product
})

function effectName(id) {
    return id.split(':')[1].split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')
}

function romanLevel(amplifier) {
    return ['I', 'II', 'III', 'IV', 'V'][amplifier] || `${amplifier + 1}`
}

function registerIndustrialFoodItem(event, item) {
    let builder = event.create(item.id)
        .displayName(item.name)
        .texture(`kubejs:item/${item.id}`)
        .tooltip(`§7${item.tooltip}`)
    const product = consumableById[item.id]
    if (product) {
        builder.food(food => {
            food.nutrition(product.nutrition).saturation(product.saturation)
            if (product.nutrition === 0) food.alwaysEdible()
            product.effects.forEach(effect => food.effect(effect.id, effect.duration, effect.amplifier, effect.chance))
        })
        builder.tooltip(product.nutrition === 0 ? '§6No Hunger' : `§6Hunger: ${product.nutrition} / 20`)
        builder.tooltip(`§a${product.saturationLabel}`)
        product.effects.forEach(effect => {
            builder.tooltip(`§b${effectName(effect.id)} ${romanLevel(effect.amplifier)} — ${Math.floor(effect.duration / 20)} sec`)
        })
        builder.tooltip(`§8${product.brand} • ${product.flavor}`)
    }
}

StartupEvents.registry('item', event => {
    industrialFood.items.filter(item => item.kind !== 'pallet').forEach(item => registerIndustrialFoodItem(event, item))
    industrialFood.flavors.forEach(flavor => {
        ;[
            [`${flavor.id}_fruit_pulp`, `${flavor.name} Pulp`, 'powder', `Crushed ${flavor.name.toLowerCase()} feed for pressing`],
            [`${flavor.id}_juice_concentrate`, `${flavor.name} Juice Concentrate`, 'vial', `Reduced ${flavor.name.toLowerCase()} juice for beverages and rations`],
            [`bottled_${flavor.id}_juice`, `Bottled ${flavor.name} Juice`, 'bottle', `Prepared juice; returns its glass bottle`],
            [`${flavor.id}_soda_can`, `${flavor.name} Soda Can`, 'can', `Carbonated ${flavor.name.toLowerCase()} beverage; returns its can`],
            [`${flavor.id}_soda_six_pack`, `${flavor.name} Soda Six-Pack`, 'six_pack', `Six ${flavor.name.toLowerCase()} soda cans`],
            [`${flavor.id}_soda_case`, `${flavor.name} Soda Case`, 'case', `Twenty-four ${flavor.name.toLowerCase()} soda cans`]
        ].forEach(entry => {
            const definition = {id: entry[0], name: entry[1], kind: entry[2], tooltip: entry[3]}
            registerIndustrialFoodItem(event, definition)
        })
    })
})

StartupEvents.registry('block', event => {
    industrialFood.items.filter(item => item.kind === 'pallet').forEach(item => {
        const texture = face => `kubejs:block/${item.id}_${face}`
        event.create(item.id)
            .displayName(item.name)
            .parentModel('minecraft:block/cube')
            .texture('particle', texture('side'))
            .texture('down', texture('side'))
            .texture('up', texture('top'))
            .texture('north', texture('front'))
            .texture('south', texture('front'))
            .texture('east', texture('side'))
            .texture('west', texture('side'))
            .woodSoundType()
            .hardness(2.5)
            .resistance(3.0)
            .tagBlock('minecraft:mineable/axe')
            .item(itemBuilder => itemBuilder
                .texture(`kubejs:item/${item.id}`)
                .tooltip(`§7${item.tooltip}`)
                .tooltip('§8Placeable freight pallet'))
    })
})

StartupEvents.registry('fluid', event => {
    const fluids = []
    industrialFood.fluids.forEach(fluid => fluids.push(fluid))
    industrialFood.flavors.forEach(flavor => {
        fluids.push(
            {id: `pressed_${flavor.id}_juice`, name: `Pressed ${flavor.name} Juice`, color: flavor.color},
            {id: `prepared_${flavor.id}_beverage`, name: `Prepared ${flavor.name} Beverage`, color: flavor.accent},
            {id: `${flavor.id}_soda_base`, name: `${flavor.name} Soda Base`, color: flavor.color},
            {id: `carbonated_${flavor.id}_soda`, name: `Carbonated ${flavor.name} Soda`, color: flavor.accent}
        )
    })
    fluids.forEach(fluid => {
        event.create(fluid.id)
            .displayName(fluid.name)
            .stillTexture(`kubejs:fluid/${fluid.id}_still`)
            .flowingTexture(`kubejs:fluid/${fluid.id}_flow`)
            .translucent()
            .noBucket()
    })
})

ItemEvents.modification(event => {
    industrialFood.simpleFoodOverrides.forEach(definition => {
        event.modify(definition.id, item => {
            item.setFood(definition.nutrition, definition.saturation)
        })
    })
})
