// Authoritative organic-chemistry and recovery-budget generator.
// Material identities live in mineral_trace_ore_processing.json; family, era,
// reagent and yield policy live in organic_metallurgy.json.
// Wrapped in an IIFE so its top-level constants do not collide with other
// server scripts in KubeJS's shared scope (cf. spawn_hub_hostile_protection.js).
(() => {
    const organicMetallurgy = JsonIO.read('kubejs/config/organic_metallurgy.json')
    const organicMinerals = JsonIO.read('kubejs/config/mineral_trace_ore_processing.json')
    const organicMetalsById = {}
    organicMinerals.metals.forEach(metal => organicMetalsById[metal.id] = metal)

    ServerEvents.recipes(event => {
        const batch = organicMetallurgy.shared.batchTraces
        const reagentAmount = organicMetallurgy.shared.reagentPerBatchMb
        const spent = organicMetallurgy.shared.spentFluid

        organicMetallurgy.eras.forEach((era, index) => {
            const extractionInput = Item.of(era.feedstock, era.feedstockCount)
            const extractionOutput = Item.of(era.extract, 4)
            const singleItemOutput = CreateItem.of(era.extract, 4 / era.feedstockCount)
            const extractionId = `infinite_domain:organic_metallurgy/era_${era.era}/extract`

            if (era.extractionProcess === 'pressing') {
                event.recipes.create.pressing(singleItemOutput, era.feedstock).id(extractionId)
            } else if (era.extractionProcess === 'crushing') {
                event.recipes.create.crushing(singleItemOutput, era.feedstock).id(extractionId)
            } else if (era.extractionProcess === 'mixing') {
                event.recipes.create.mixing(extractionOutput, [extractionInput, Fluid.of('minecraft:water', 250)]).id(extractionId)
            } else if (era.feedstock === 'minecraft:wheat') {
                // create:milling/wheat already claims plain wheat for flour/seeds.
                // Merge into one recipe instead of silently shadowing it.
                event.remove({ id: 'create:milling/wheat' })
                event.recipes.create.milling([
                    'create:wheat_flour',
                    CreateItem.of(Item.of('create:wheat_flour', 2), 0.25),
                    CreateItem.of('minecraft:wheat_seeds', 0.25),
                    singleItemOutput
                ], era.feedstock).id(extractionId)
            } else {
                event.recipes.create.milling(singleItemOutput, era.feedstock).id(extractionId)
            }

            const reagentInputs = [Item.of(era.extract, 4), Fluid.of('minecraft:water', index === 0 ? 1000 : 750)]
            if (index > 0) reagentInputs.push(Fluid.of(organicMetallurgy.eras[index - 1].reagent, 250))
            const reagentRecipe = event.recipes.create.mixing(Fluid.of(era.reagent, 1000), reagentInputs)
                .id(`infinite_domain:organic_metallurgy/era_${era.era}/reagent`)
            if (era.heatedReagent) reagentRecipe.heated()

            if (era.recoveredMb > 0) {
                event.recipes.create.mixing(Fluid.of(era.reagent, era.recoveredMb), [
                    Fluid.of(spent, era.recoveredMb),
                    Item.of(era.extract)
                ]).heated().id(`infinite_domain:organic_metallurgy/era_${era.era}/regenerate_reagent`)
            }
        })

        organicMetallurgy.metalProfiles.forEach(profile => {
            const metal = organicMetalsById[profile.id]
            if (!metal) throw new Error(`Organic metallurgy profile has no mineral mapping: ${profile.id}`)

            const trace = `kubejs:${metal.id}_mineral_trace`
            const dust = `kubejs:${metal.id}_mineral_dust`
            const washed = `kubejs:washed_${metal.id}_mineral`
            const conditioned = `kubejs:conditioned_${metal.id}_mineral`
            const precipitated = `kubejs:precipitated_${metal.id}_concentrate`
            const highGrade = `kubejs:high_grade_${metal.id}_concentrate`

            event.recipes.create.milling(dust, trace)
                .id(`infinite_domain:organic_metallurgy/${metal.id}/mechanical_grinding`)

            const era1 = organicMetallurgy.eras.find(era => era.era === 1)
            event.recipes.create.mixing(Item.of(washed, batch), [
                Item.of(dust, batch), Fluid.of(era1.reagent, reagentAmount)
            ]).id(`infinite_domain:organic_metallurgy/${metal.id}/mechanical_washing`)
            event.recipes.create.compacting(Item.of(metal.nugget, 10), [Item.of(washed, batch), Fluid.of('minecraft:water', 250)])
                .id(`infinite_domain:organic_metallurgy/${metal.id}/mechanical_recovery`)

            const era2 = organicMetallurgy.eras.find(era => era.era === 2)
            event.recipes.create.mixing(Item.of(conditioned, era2.recoveryNuggets), [
                Item.of(dust, batch), Fluid.of(era2.reagent, reagentAmount)
            ]).id(`infinite_domain:organic_metallurgy/${metal.id}/tannic_conditioning`)
            event.recipes.create.compacting(Item.of(metal.nugget, era2.recoveryNuggets), Item.of(conditioned, era2.recoveryNuggets))
                .heated().id(`infinite_domain:organic_metallurgy/${metal.id}/conditioned_recovery`)

            const era3 = organicMetallurgy.eras.find(era => era.era === 3)
            event.recipes.create.mixing(Item.of(precipitated, era3.recoveryNuggets), [
                Item.of(conditioned, batch), Fluid.of(era3.reagent, reagentAmount)
            ]).heated().id(`infinite_domain:organic_metallurgy/${metal.id}/fermented_leaching`)
            event.recipes.create.compacting(Item.of(metal.nugget, era3.recoveryNuggets), Item.of(precipitated, era3.recoveryNuggets))
                .heated().id(`infinite_domain:organic_metallurgy/${metal.id}/precipitated_recovery`)

            organicMetallurgy.eras.filter(era => era.era >= 4).forEach(era => {
                if (profile.introducedEra > era.era) return
                const outputs = [Item.of(highGrade, era.recoveryNuggets)]
                if (era.recoveredMb > 0) outputs.push(Fluid.of(spent, era.recoveredMb))
                event.recipes.create.mixing(outputs, [
                    Item.of(precipitated, batch), Fluid.of(era.reagent, reagentAmount)
                ]).heated().id(`infinite_domain:organic_metallurgy/${metal.id}/era_${era.era}_selective_extraction`)
            })

            if (profile.moltenFluid) {
                event.custom({
                    type: 'createmetallurgy:melting',
                    heat_requirement: 'heated',
                    ingredients: [{ item: highGrade }],
                    processing_time: 40,
                    results: [{ id: profile.moltenFluid, amount: 10 }]
                }).id(`infinite_domain:organic_metallurgy/${metal.id}/high_grade_melting`)
            } else {
                event.smelting(metal.nugget, highGrade)
                    .xp(0.05).id(`infinite_domain:organic_metallurgy/${metal.id}/high_grade_smelting`)
                event.blasting(metal.nugget, highGrade)
                    .xp(0.05).id(`infinite_domain:organic_metallurgy/${metal.id}/high_grade_blasting`)
            }
        })
    })
})()
