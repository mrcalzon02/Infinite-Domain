// [SYSTEM REPORT] Infinite Domain — Ruined Infrastructure Block Registry
//
// Registers inert ruined infrastructure blocks for authored structures and
// schematics. These blocks are placed deliberately by Infinite Domain content;
// normal world generation is not scanned or rewritten.
//
// KubeJS 2101 removed the legacy BasicKubeBlock.Builder methods
// setBlockstateJson/setModelJson. Visual blockstate/model composition therefore
// lives in the supported ClientEvents.generateAssets('last', ...) pipeline; this
// startup script owns registry behavior only.

const RUINED_BLOCK_DEFS = [
    { id: 'ruined_furnace', name: 'Ruined Furnace', sourceModel: 'minecraft:block/furnace', stone: true, horizontal: true, furnaceFamily: true },
    { id: 'ruined_smoker', name: 'Ruined Smoker', sourceModel: 'minecraft:block/smoker', stone: true, horizontal: true, furnaceFamily: true },
    { id: 'ruined_blast_furnace', name: 'Ruined Blast Furnace', sourceModel: 'minecraft:block/blast_furnace', stone: true, horizontal: true, furnaceFamily: true },
    { id: 'ruined_stonecutter', name: 'Ruined Stonecutter', sourceModel: 'minecraft:block/stonecutter', stone: true, horizontal: true, fullBlock: false },
    { id: 'ruined_smithing_table', name: 'Ruined Smithing Table', sourceModel: 'minecraft:block/smithing_table', stone: false },
    { id: 'ruined_grindstone', name: 'Ruined Grindstone', sourceModel: 'minecraft:block/grindstone', stone: true, horizontal: true, attachFace: true, fullBlock: false },
    { id: 'ruined_cartography_table', name: 'Ruined Cartography Table', sourceModel: 'minecraft:block/cartography_table', stone: false },
    { id: 'ruined_fletching_table', name: 'Ruined Fletching Table', sourceModel: 'minecraft:block/fletching_table', stone: false },
    { id: 'ruined_loom', name: 'Ruined Loom', sourceModel: 'minecraft:block/loom', stone: false, horizontal: true },
    { id: 'ruined_lectern', name: 'Ruined Lectern', sourceModel: 'minecraft:block/lectern', stone: false, horizontal: true, fullBlock: false },
    { id: 'ruined_brewing_stand', name: 'Ruined Brewing Stand', sourceModel: 'minecraft:block/brewing_stand', stone: true, fullBlock: false },
    { id: 'ruined_composter', name: 'Ruined Composter', sourceModel: 'minecraft:block/composter', stone: false, fullBlock: false },
    { id: 'ruined_cauldron', name: 'Ruined Cauldron', sourceModel: 'minecraft:block/cauldron', stone: true, fullBlock: false },
    { id: 'ruined_crafting_table', name: 'Ruined Crafting Table', sourceModel: 'minecraft:block/crafting_table', stone: false },
    { id: 'ruined_anvil', name: 'Ruined Anvil', sourceModel: 'minecraft:block/damaged_anvil', stone: true, horizontal: true, fullBlock: false },
    { id: 'ruined_campfire', name: 'Ruined Campfire', sourceModel: 'minecraft:block/campfire_off', stone: false, horizontal: true, fullBlock: false },
    { id: 'ruined_soul_campfire', name: 'Ruined Soul Campfire', sourceModel: 'minecraft:block/soul_campfire_off', stone: false, horizontal: true, fullBlock: false },
    { id: 'ruined_enchanting_table', name: 'Ruined Enchanting Table', sourceModel: 'minecraft:block/enchanting_table', stone: true, fullBlock: false },
]

function configureRuinedItem(builder, parentModel) {
    builder.item(item => {
        item.parentModel(parentModel)
            .tooltip('§8Ruined Old World infrastructure')
            .tooltip('§7Inoperable. Salvage only.')
    })
}

StartupEvents.registry('block', event => {
    RUINED_BLOCK_DEFS.forEach(def => {
        const builder = event.create(def.id)
            .displayName(def.name)
            .hardness(def.furnaceFamily ? 3.5 : 2.5)
            .resistance(def.furnaceFamily ? 3.5 : 3.0)
            .requiresTool(true)
            .defaultCutout()
            .parentModel(def.sourceModel)

        if (def.stone) {
            builder.stoneSoundType().tagBlock('minecraft:mineable/pickaxe')
        } else {
            builder.woodSoundType().tagBlock('minecraft:mineable/axe')
        }

        if (def.fullBlock === false) builder.fullBlock(false)

        if (def.horizontal) {
            builder.property(BlockProperties.HORIZONTAL_FACING)
                .defaultState(state => {
                    state.setValue(BlockProperties.HORIZONTAL_FACING, Direction.NORTH)
                })
                .placementState(state => {
                    state.setValue(BlockProperties.HORIZONTAL_FACING, state.horizontalDirection.opposite)
                })
        }

        if (def.attachFace) builder.property(BlockProperties.ATTACH_FACE)

        configureRuinedItem(
            builder,
            def.furnaceFamily ? `kubejs:block/${def.id}` : def.sourceModel
        )
    })
})
