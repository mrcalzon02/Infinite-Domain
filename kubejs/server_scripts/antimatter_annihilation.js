// allthecompressed:antimatter_block is now producible via the Oritech Particle
// Accelerator (see data/oritech/recipe/particle/antimatter.json). This gives it a
// crafting sink: it substitutes for AE2LT's overload_singularity recipe (normally
// ae2:singularity + minecraft:nether_star), so pushing the accelerator past nether
// stars becomes an alternate path into the Matter Warping Matrix tier.
ServerEvents.recipes(event => {
    event.shapeless('ae2lt:overload_singularity', [
        'allthecompressed:antimatter_block',
        'minecraft:nether_star'
    ]).id('infinite_domain:antimatter_annihilation/overload_singularity_from_antimatter')
})
