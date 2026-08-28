// Second-job generator for the organic chemistry program.
// Every chemical produced by organic_metallurgy.js carries exactly one secondary
// use outside metal recovery. Shapes, targets and quantified effects live in
// organic_secondary_uses.json; era chemistry still lives in organic_metallurgy.json.
// Wrapped in an IIFE so its top-level constants do not collide with other
// server scripts in KubeJS's shared scope (cf. spawn_hub_hostile_protection.js).
(() => {
    const secondaryUses = JsonIO.read('kubejs/config/organic_secondary_uses.json')
    const organicMetallurgy = JsonIO.read('kubejs/config/organic_metallurgy.json')

    ServerEvents.recipes(event => {
        const shared = secondaryUses.shared
        const prefix = shared.recipePrefix
        const spent = shared.spentFluid

        const stack = entry => {
            if (entry.tag) return Ingredient.of(entry.tag)
            if (entry.fluid) return Fluid.of(entry.fluid, entry.amount)
            if (entry.item) return Item.of(entry.item, entry.count === undefined ? 1 : entry.count)
            throw new Error(`Secondary-use entry is neither item, tag nor fluid: ${JSON.stringify(entry)}`)
        }

        const build = (recipe, chemical) => {
            const outputs = recipe.outputs.map(stack)
            const inputs = recipe.inputs.map(stack)

            let built
            if (recipe.machine === 'mixing') {
                built = event.recipes.create.mixing(outputs, inputs)
            } else if (recipe.machine === 'compacting') {
                built = event.recipes.create.compacting(outputs, inputs)
            } else {
                throw new Error(`Unsupported secondary-use machine '${recipe.machine}' for ${chemical}`)
            }

            if (recipe.heat === 'heated') built.heated()
            else if (recipe.heat === 'superheated') built.superheated()
            return built.id(`${prefix}/${recipe.id}`)
        }

        // The Era 8 pair points back at the chemistry ladder itself. Both skip the era
        // whose own chemical is the catalyst, so neither can return more of that
        // chemical than it consumes, and both drop an ingredient their baseline
        // requires so a basin can never resolve the weaker recipe instead.
        const expandReagentRegeneration = use => {
            organicMetallurgy.eras.forEach(era => {
                if (era.recoveredMb <= 0) return
                if (era.reagent === use.chemical) return
                // The catalyst replaces the sacrificial extract the plain regeneration burns.
                event.recipes.create.mixing(
                    Fluid.of(era.reagent, era.recoveredMb * shared.regenerationMultiplier),
                    [
                        Fluid.of(spent, era.recoveredMb),
                        Fluid.of(use.chemical, shared.regenerationCatalystMb)
                    ]
                ).heated().id(`${prefix}/era_8/catalysed_regeneration_era_${era.era}`)
            })
        }

        const expandReagentBrewing = use => {
            organicMetallurgy.eras.forEach((era, index) => {
                if (era.extract === use.chemical) return
                const inputs = [
                    Item.of(era.extract, shared.brewingExtractReduced),
                    Item.of(use.chemical),
                    Fluid.of('minecraft:water', index === 0 ? 1000 : 750)
                ]
                if (index > 0) inputs.push(Fluid.of(organicMetallurgy.eras[index - 1].reagent, 250))
                // Deliberately never heated: the catalyst removes the burner the
                // full-charge brew needs, which is also what keeps the two apart.
                event.recipes.create.mixing(Fluid.of(era.reagent, 1000), inputs)
                    .id(`${prefix}/era_8/catalysed_brewing_era_${era.era}`)
            })
        }

        const expansions = {
            reagentRegeneration: expandReagentRegeneration,
            reagentBrewing: expandReagentBrewing
        }

        secondaryUses.uses.forEach(use => {
            use.recipes.forEach(recipe => build(recipe, use.chemical))

            if (!use.expand) return
            const expansion = expansions[use.expand]
            if (!expansion) throw new Error(`Unknown secondary-use expansion '${use.expand}' for ${use.chemical}`)
            expansion(use)
        })
    })
})()
