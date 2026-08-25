// [SYSTEM REPORT] Infinite Domain — Ruined Worldgen Infrastructure Progression Gate
//
// Generated progression-capable vanilla infrastructure is replaced with an
// inert ruined counterpart only when a new chunk is generated.
//
// KubeJS 2101 removed the legacy BasicKubeBlock.Builder methods
// setBlockstateJson/setModelJson. Visual blockstate/model composition therefore
// lives in the supported ClientEvents.generateAssets('last', ...) pipeline; this
// startup script owns only registry behavior and worldgen replacement.

const $BuiltInRegistries = Java.loadClass('net.minecraft.core.registries.BuiltInRegistries')
const $ResourceLocation = Java.loadClass('net.minecraft.resources.ResourceLocation')

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

const RUINED_REPLACEMENTS = [
    { source: Blocks.FURNACE,           id: 'ruined_furnace',           horizontal: true },
    { source: Blocks.SMOKER,            id: 'ruined_smoker',            horizontal: true },
    { source: Blocks.BLAST_FURNACE,     id: 'ruined_blast_furnace',     horizontal: true },
    { source: Blocks.STONECUTTER,       id: 'ruined_stonecutter',       horizontal: true },
    { source: Blocks.SMITHING_TABLE,    id: 'ruined_smithing_table' },
    { source: Blocks.GRINDSTONE,        id: 'ruined_grindstone',        horizontal: true, attachFace: true },
    { source: Blocks.CARTOGRAPHY_TABLE, id: 'ruined_cartography_table' },
    { source: Blocks.FLETCHING_TABLE,   id: 'ruined_fletching_table' },
    { source: Blocks.LOOM,              id: 'ruined_loom',              horizontal: true },
    { source: Blocks.LECTERN,           id: 'ruined_lectern',           horizontal: true },
    { source: Blocks.BREWING_STAND,     id: 'ruined_brewing_stand' },
    { source: Blocks.COMPOSTER,         id: 'ruined_composter' },
    { source: Blocks.CAULDRON,          id: 'ruined_cauldron' },
    { source: Blocks.WATER_CAULDRON,    id: 'ruined_cauldron' },
    { source: Blocks.LAVA_CAULDRON,     id: 'ruined_cauldron' },
    { source: Blocks.POWDER_SNOW_CAULDRON, id: 'ruined_cauldron' },
    { source: Blocks.CRAFTING_TABLE,    id: 'ruined_crafting_table' },
    { source: Blocks.ANVIL,             id: 'ruined_anvil',             horizontal: true },
    { source: Blocks.CHIPPED_ANVIL,     id: 'ruined_anvil',             horizontal: true },
    { source: Blocks.DAMAGED_ANVIL,     id: 'ruined_anvil',             horizontal: true },
    { source: Blocks.CAMPFIRE,          id: 'ruined_campfire',          horizontal: true },
    { source: Blocks.SOUL_CAMPFIRE,     id: 'ruined_soul_campfire',     horizontal: true },
    { source: Blocks.ENCHANTING_TABLE,  id: 'ruined_enchanting_table' }
]

function ruinedReplacement(state) {
    for (let i = 0; i < RUINED_REPLACEMENTS.length; i++) {
        const def = RUINED_REPLACEMENTS[i]
        if (state.is(def.source)) return def
    }
    return null
}

function registeredBlock(id) {
    return $BuiltInRegistries.BLOCK.get($ResourceLocation.tryParse(id))
}

NativeEvents.onEvent(Java.loadClass('net.neoforged.neoforge.event.level.ChunkEvent$Load'), event => {
    if (!event.isNewChunk()) return

    const level = event.getLevel()
    if (level.isClientSide()) return

    const chunkPos = event.getChunk().getPos()
    const chunkX = chunkPos.x
    const chunkZ = chunkPos.z
    const server = level.getServer()

    // ChunkEvent.Load can fire before the LevelChunk is promoted to FULL.
    // Delay world mutation by one server tick, then inspect only this new chunk.
    server.scheduleInTicks(1, () => {
        if (!level.hasChunk(chunkX, chunkZ)) return

        const chunk = level.getChunk(chunkX, chunkZ)
        const replacements = []

        chunk.findBlocks(
            state => ruinedReplacement(state) !== null,
            (pos, state) => {
                const def = ruinedReplacement(state)
                replacements.push({
                    pos: pos.immutable(),
                    id: def.id,
                    horizontal: def.horizontal === true,
                    attachFace: def.attachFace === true,
                    facing: def.horizontal ? state.getValue(BlockProperties.HORIZONTAL_FACING) : null,
                    face: def.attachFace ? state.getValue(BlockProperties.ATTACH_FACE) : null
                })
            }
        )

        replacements.forEach(entry => {
            const target = registeredBlock(`kubejs:${entry.id}`)
            let targetState = target.defaultBlockState()

            if (entry.horizontal) {
                targetState = targetState.setValue(BlockProperties.HORIZONTAL_FACING, entry.facing)
            }
            if (entry.attachFace) {
                targetState = targetState.setValue(BlockProperties.ATTACH_FACE, entry.face)
            }

            level.setBlock(entry.pos, targetState, 3)
        })
    })
})
