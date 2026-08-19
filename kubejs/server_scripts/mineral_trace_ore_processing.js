// Infinite Domain's authoritative ore -> trace -> dust -> nugget economy.
// All metal mappings and balance values live in the adjacent JSON config.
const mineralTraceConfig = JsonIO.read('kubejs/config/mineral_trace_ore_processing.json')
const mineralTraceBalance = mineralTraceConfig.balance

mineralTraceConfig.metals.forEach(metal => {
    const trace = `kubejs:${metal.id}_mineral_trace`

    metal.ores.forEach(ore => {
        BlockEvents.drops(ore, event => {
            event.items.clear()

            const spread = mineralTraceBalance.maximumTracesPerOre - mineralTraceBalance.minimumTracesPerOre + 1
            let traceCount = mineralTraceBalance.minimumTracesPerOre + Math.floor(Math.random() * spread)
            if (ore.includes('deepslate')) {
                const bonusSpread = mineralTraceBalance.maximumDeepslateBonus - mineralTraceBalance.minimumDeepslateBonus + 1
                traceCount += mineralTraceBalance.minimumDeepslateBonus + Math.floor(Math.random() * bonusSpread)
            }
            event.addItem(Item.of(trace, traceCount))

            if (Math.random() < mineralTraceBalance.rawChunkChance) {
                event.addItem(Item.of(metal.rawChunk))
            }
        })
    })
})

ServerEvents.recipes(event => {
    mineralTraceConfig.metals.forEach(metal => {
        const trace = `kubejs:${metal.id}_mineral_trace`
        const dust = `kubejs:${metal.id}_mineral_dust`
        const rawTag = `#c:raw_materials/${metal.id}`
        const oreTag = `#c:ores/${metal.id}`
        const dustTag = `#c:dusts/${metal.id}`
        const rawBlockTag = `#c:storage_blocks/raw_${metal.id}`
        const ingotTag = `#c:ingots/${metal.id}`

        // Remove every direct full-ingot route from mined or primitive ore forms.
        ;[rawTag, oreTag, dustTag, rawBlockTag].concat(metal.crushed).forEach(input => {
            event.remove({ input: input, output: ingotTag })
            event.remove({ input: input, output: metal.nugget })
        })

        // Create: Metallurgy's raw/raw-block melt paths would bypass the trace economy.
        ;['raw_material', 'raw_crushed'].forEach(form => {
            event.remove({ id: `createmetallurgy:melting/${metal.id}/${form}` })
        })
        ;['raw_block', 'ore', 'deepslate_ore'].forEach(form => {
            event.remove({ id: `createmetallurgy:bulk_melting/${metal.id}/${form}` })
        })

        // A jackpot raw chunk is valuable, but still only seven trace-equivalents.
        event.smelting(Item.of(trace, mineralTraceBalance.tracesPerRawChunk), metal.rawChunk)
            .xp(0.1)
            .id(`infinite_domain:mineral_traces/${metal.id}/raw_chunk_smelting`)
        event.blasting(Item.of(trace, mineralTraceBalance.tracesPerRawChunk), metal.rawChunk)
            .xp(0.1)
            .id(`infinite_domain:mineral_traces/${metal.id}/raw_chunk_blasting`)

        // Nuclear-bearing traces are deliberately handed to their dedicated
        // fuel-cycle refinery instead of becoming primitive metal nuggets.
        if (metal.primitiveRecovery === false) return

        // Primitive concentration preserves one trace as one eventual nugget.
        event.shapeless(dust, trace)
            .id(`infinite_domain:mineral_traces/${metal.id}/trace_to_dust`)
        event.smelting(metal.nugget, dust)
            .xp(0.01)
            .id(`infinite_domain:mineral_traces/${metal.id}/dust_to_nugget_smelting`)
        event.blasting(metal.nugget, dust)
            .xp(0.01)
            .id(`infinite_domain:mineral_traces/${metal.id}/dust_to_nugget_blasting`)
        event.shapeless(metal.ingot, Array(9).fill(metal.nugget))
            .id(`infinite_domain:mineral_traces/${metal.id}/nuggets_to_ingot`)
    })
})
