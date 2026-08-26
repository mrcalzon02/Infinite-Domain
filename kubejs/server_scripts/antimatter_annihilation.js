// Gives Mekanism's SPS antimatter output (mekanism:pellet_antimatter), which has no
// vanilla use beyond AllTheCompressed's cosmetic compression chain, a real crafting
// sink: the compressed antimatter block substitutes for AE2LT's overload_singularity
// recipe (normally ae2:singularity + minecraft:nether_star), so a running SPS becomes
// an alternate path into the Matter Warping Matrix tier instead of a dead end.
ServerEvents.recipes(event => {
    event.shapeless('ae2lt:overload_singularity', [
        'allthecompressed:antimatter_block',
        'minecraft:nether_star'
    ]).id('infinite_domain:antimatter_annihilation/overload_singularity_from_antimatter')
})
