// These "creative_*" blocks (AE2's infinite energy/storage cells, Oritech's infinite
// storage/tank blocks) ship with zero recipes in their source mods -- they exist only
// for creative-mode/admin use. Fully-compressed antimatter (allthecompressed:antimatter_block_9x,
// itself 9^9 accelerator-forged antimatter blocks folded into one item) is the pack's
// highest resource-sink material, so it gates the survival-craftable versions: each
// recipe upgrades the mod's own best finite equivalent into its infinite counterpart.
ServerEvents.recipes(event => {
    event.shapeless('ae2:creative_energy_cell', [
        'ae2:dense_energy_cell',
        'allthecompressed:antimatter_block_9x'
    ]).id('infinite_domain:godtier/creative_energy_cell')

    event.shapeless('ae2:creative_storage_cell', [
        'ae2:item_storage_cell_256k',
        'allthecompressed:antimatter_block_9x'
    ]).id('infinite_domain:godtier/creative_storage_cell')

    event.shapeless('oritech:creative_storage_block', [
        'oritech:large_storage_block',
        'allthecompressed:antimatter_block_9x'
    ]).id('infinite_domain:godtier/creative_storage_block')

    event.shapeless('oritech:creative_tank_block', [
        'oritech:small_tank_block',
        'allthecompressed:antimatter_block_9x'
    ]).id('infinite_domain:godtier/creative_tank_block')
})
