// Item registration is driven by the same mapping used by drops and recipes.
const mineralTraceConfig = JsonIO.read('kubejs/config/mineral_trace_ore_processing.json')
const organicMetallurgyConfig = JsonIO.read('kubejs/config/organic_metallurgy.json')
const organicMetalIds = {}
organicMetallurgyConfig.metalProfiles.forEach(profile => organicMetalIds[profile.id] = true)

StartupEvents.registry('item', event => {
    mineralTraceConfig.metals.forEach(metal => {
        event.create(`${metal.id}_mineral_trace`)
            .displayName(`${metal.name} Mineral Traces`)
            .texture(metal.traceTexture)
            .tooltip('§7Low-grade mineral-bearing material')

        event.create(`${metal.id}_mineral_dust`)
            .displayName(`${metal.name} Mineral Dust`)
            .texture(metal.dustTexture)
            .tooltip(metal.processingClass === 'nuclear'
                ? '§7Controlled feed for the nuclear refining chain'
                : '§7Concentrated enough to recover one metal nugget')

        if (!organicMetalIds[metal.id]) return
        event.create(`washed_${metal.id}_mineral`)
            .displayName(`Washed ${metal.name} Mineral`)
            .texture(metal.dustTexture)
            .tooltip('§7Mechanically separated mineral fraction')

        event.create(`conditioned_${metal.id}_mineral`)
            .displayName(`Conditioned ${metal.name} Mineral`)
            .texture(metal.dustTexture)
            .tooltip('§7Mineral conditioned by a renewable organic reagent')

        event.create(`precipitated_${metal.id}_concentrate`)
            .displayName(`Precipitated ${metal.name} Concentrate`)
            .texture(metal.dustTexture)
            .tooltip('§7Metal-bearing concentrate separated from a treated slurry')

        event.create(`high_grade_${metal.id}_concentrate`)
            .displayName(`High-Grade ${metal.name} Concentrate`)
            .texture(metal.dustTexture)
            .tooltip('§7Purified feedstock for foundry or advanced refining')
    })

    organicMetallurgyConfig.eras.forEach(era => {
        const extractId = era.extract.split(':')[1]
        event.create(extractId)
            .displayName(era.extractName)
            .texture(era.extractTexture)
            .tooltip(`§7Renewable precursor for ${era.reagentName}`)
    })
})

StartupEvents.registry('fluid', event => {
    organicMetallurgyConfig.eras.forEach(era => {
        event.create(era.reagent.split(':')[1])
            .displayName(era.reagentName)
            .stillTexture('minecraft:block/water_still')
            .flowingTexture('minecraft:block/water_flow')
            .tint(era.fluidColor)
            .translucent()
    })

    event.create(organicMetallurgyConfig.shared.spentFluid.split(':')[1])
        .displayName('Spent Process Solution')
        .stillTexture('minecraft:block/water_still')
        .flowingTexture('minecraft:block/water_flow')
        .tint(0x6B6657)
        .translucent()
})
