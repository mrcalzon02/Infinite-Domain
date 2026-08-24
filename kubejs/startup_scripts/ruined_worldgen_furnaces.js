// Infinite Domain — Ruined Worldgen Infrastructure Progression Gate
//
// Generated progression-capable vanilla infrastructure is replaced with an
// inert ruined counterpart. Player-crafted/player-placed vanilla blocks are
// never touched because replacement only runs for newly generated chunks.
//
// Visual rule: keep the vanilla/resource-pack model underneath and add a
// permanent mid-break crack treatment so the object remains immediately
// recognizable while clearly reading as unusable Old World salvage.

const $BuiltInRegistries = Java.loadClass('net.minecraft.core.registries.BuiltInRegistries')
const $ResourceLocation = Java.loadClass('net.minecraft.resources.ResourceLocation')

const CRACK_TEXTURE = 'minecraft:block/destroy_stage_5'

function ruinedCubeModel(front, side, top, bottom) {
    const baseFaces = {
        down:  { texture: '#bottom', cullface: 'down' },
        up:    { texture: '#top',    cullface: 'up' },
        north: { texture: '#front',  cullface: 'north' },
        south: { texture: '#side',   cullface: 'south' },
        west:  { texture: '#side',   cullface: 'west' },
        east:  { texture: '#side',   cullface: 'east' }
    }
    const crackFaces = {
        down:  { texture: '#crack' },
        up:    { texture: '#crack' },
        north: { texture: '#crack' },
        south: { texture: '#crack' },
        west:  { texture: '#crack' },
        east:  { texture: '#crack' }
    }

    return {
        parent: 'minecraft:block/block',
        ambientocclusion: true,
        textures: {
            front: front,
            side: side,
            top: top,
            bottom: bottom || top,
            crack: CRACK_TEXTURE,
            particle: side
        },
        elements: [
            {
                from: [0, 0, 0],
                to: [16, 16, 16],
                faces: baseFaces
            },
            {
                // Slight expansion prevents z-fighting while preserving the
                // familiar vanilla/resource-pack texture underneath.
                from: [-0.02, -0.02, -0.02],
                to: [16.02, 16.02, 16.02],
                shade: false,
                faces: crackFaces
            }
        ]
    }
}

function crackOverlayModel(boxes) {
    function crackFaces() {
        return {
            down:  { texture: '#crack' },
            up:    { texture: '#crack' },
            north: { texture: '#crack' },
            south: { texture: '#crack' },
            west:  { texture: '#crack' },
            east:  { texture: '#crack' }
        }
    }

    return {
        parent: 'minecraft:block/block',
        ambientocclusion: false,
        textures: {
            crack: CRACK_TEXTURE,
            particle: CRACK_TEXTURE
        },
        elements: boxes.map(box => ({
            from: [box[0] - 0.02, box[1] - 0.02, box[2] - 0.02],
            to:   [box[3] + 0.02, box[4] + 0.02, box[5] + 0.02],
            shade: false,
            faces: crackFaces()
        }))
    }
}

function horizontalBlockstate(id) {
    return {
        variants: {
            'facing=north': { model: `kubejs:block/${id}` },
            'facing=east':  { model: `kubejs:block/${id}`, y: 90,  uvlock: true },
            'facing=south': { model: `kubejs:block/${id}`, y: 180, uvlock: true },
            'facing=west':  { model: `kubejs:block/${id}`, y: 270, uvlock: true }
        }
    }
}

function layeredBlockstate(id, vanillaModel) {
    return {
        multipart: [
            { apply: { model: vanillaModel } },
            { apply: { model: `kubejs:block/${id}` } }
        ]
    }
}

function horizontalLayeredBlockstate(id, vanillaModel) {
    const rotations = {
        north: 0,
        east: 90,
        south: 180,
        west: 270
    }
    const multipart = []

    Object.keys(rotations).forEach(facing => {
        const y = rotations[facing]
        const base = { model: vanillaModel }
        const crack = { model: `kubejs:block/${id}` }
        if (y !== 0) {
            base.y = y
            crack.y = y
            base.uvlock = true
            crack.uvlock = true
        }
        multipart.push({ when: { facing: facing }, apply: base })
        multipart.push({ when: { facing: facing }, apply: crack })
    })

    return { multipart: multipart }
}

function grindstoneLayeredBlockstate(id) {
    const states = [
        ['floor',   'north',   0,   0],
        ['floor',   'east',    0,  90],
        ['floor',   'south',   0, 180],
        ['floor',   'west',    0, 270],
        ['wall',    'north',  90,   0],
        ['wall',    'east',   90,  90],
        ['wall',    'south',  90, 180],
        ['wall',    'west',   90, 270],
        ['ceiling', 'north', 180, 180],
        ['ceiling', 'east',  180, 270],
        ['ceiling', 'south', 180,   0],
        ['ceiling', 'west',  180,  90]
    ]
    const multipart = []

    states.forEach(([face, facing, x, y]) => {
        const base = { model: 'minecraft:block/grindstone' }
        const crack = { model: `kubejs:block/${id}` }
        if (x !== 0) {
            base.x = x
            crack.x = x
        }
        if (y !== 0) {
            base.y = y
            crack.y = y
        }
        multipart.push({ when: { face: face, facing: facing }, apply: base })
        multipart.push({ when: { face: face, facing: facing }, apply: crack })
    })

    return { multipart: multipart }
}

function configureRuinedItem(builder, parentModel) {
    builder.item(item => {
        item.parentModel(parentModel)
            .tooltip('§8Ruined Old World infrastructure')
            .tooltip('§7Inoperable. Salvage only.')
    })
}

StartupEvents.registry('block', event => {
    const furnaceFamily = [
        {
            id: 'ruined_furnace',
            name: 'Ruined Furnace',
            model: ruinedCubeModel(
                'minecraft:block/furnace_front',
                'minecraft:block/furnace_side',
                'minecraft:block/furnace_top',
                'minecraft:block/furnace_top'
            )
        },
        {
            id: 'ruined_smoker',
            name: 'Ruined Smoker',
            model: ruinedCubeModel(
                'minecraft:block/smoker_front',
                'minecraft:block/smoker_side',
                'minecraft:block/smoker_top',
                'minecraft:block/smoker_bottom'
            )
        },
        {
            id: 'ruined_blast_furnace',
            name: 'Ruined Blast Furnace',
            model: ruinedCubeModel(
                'minecraft:block/blast_furnace_front',
                'minecraft:block/blast_furnace_side',
                'minecraft:block/blast_furnace_top',
                'minecraft:block/blast_furnace_top'
            )
        }
    ]

    furnaceFamily.forEach(def => {
        const builder = event.create(def.id)
            .displayName(def.name)
            .stoneSoundType()
            .hardness(3.5)
            .resistance(3.5)
            .requiresTool(true)
            .tagBlock('minecraft:mineable/pickaxe')
            .property(BlockProperties.HORIZONTAL_FACING)
            .defaultState(state => {
                state.setValue(BlockProperties.HORIZONTAL_FACING, Direction.NORTH)
            })
            .placementState(state => {
                state.setValue(BlockProperties.HORIZONTAL_FACING, state.horizontalDirection.opposite)
            })
            .defaultCutout()
            .setBlockstateJson(horizontalBlockstate(def.id))
            .setModelJson(def.model)

        configureRuinedItem(builder, `kubejs:block/${def.id}`)
    })

    const workstationFamily = [
        {
            id: 'ruined_stonecutter',
            name: 'Ruined Stonecutter',
            sourceModel: 'minecraft:block/stonecutter',
            horizontal: true,
            stone: true,
            fullBlock: false,
            boxes: [[0, 0, 0, 16, 9, 16], [1, 9, 7.9, 15, 16, 8.1]]
        },
        {
            id: 'ruined_smithing_table',
            name: 'Ruined Smithing Table',
            sourceModel: 'minecraft:block/smithing_table',
            stone: false,
            boxes: [[0, 0, 0, 16, 16, 16]]
        },
        {
            id: 'ruined_grindstone',
            name: 'Ruined Grindstone',
            sourceModel: 'minecraft:block/grindstone',
            horizontal: true,
            attachFace: true,
            stone: true,
            fullBlock: false,
            boxes: [
                [12, 0, 6, 14, 7, 10],
                [2, 0, 6, 4, 7, 10],
                [12, 7, 5, 14, 13, 11],
                [2, 7, 5, 4, 13, 11],
                [4, 4, 2, 12, 16, 14]
            ]
        },
        {
            id: 'ruined_cartography_table',
            name: 'Ruined Cartography Table',
            sourceModel: 'minecraft:block/cartography_table',
            stone: false,
            boxes: [[0, 0, 0, 16, 16, 16]]
        },
        {
            id: 'ruined_fletching_table',
            name: 'Ruined Fletching Table',
            sourceModel: 'minecraft:block/fletching_table',
            stone: false,
            boxes: [[0, 0, 0, 16, 16, 16]]
        },
        {
            id: 'ruined_loom',
            name: 'Ruined Loom',
            sourceModel: 'minecraft:block/loom',
            horizontal: true,
            stone: false,
            boxes: [[0, 0, 0, 16, 16, 16]]
        },
        {
            id: 'ruined_lectern',
            name: 'Ruined Lectern',
            sourceModel: 'minecraft:block/lectern',
            horizontal: true,
            stone: false,
            fullBlock: false,
            boxes: [
                [0, 0, 0, 16, 2, 16],
                [4, 2, 4, 12, 15, 12],
                [0, 12, 3, 16, 16, 16]
            ]
        },
        {
            id: 'ruined_brewing_stand',
            name: 'Ruined Brewing Stand',
            sourceModel: 'minecraft:block/brewing_stand',
            stone: true,
            fullBlock: false,
            boxes: [
                [7, 0, 7, 9, 14, 9],
                [1, 0, 1, 15, 2, 15]
            ]
        },
        {
            id: 'ruined_composter',
            name: 'Ruined Composter',
            sourceModel: 'minecraft:block/composter',
            stone: false,
            fullBlock: false,
            boxes: [
                [0, 0, 0, 16, 2, 16],
                [0, 0, 0, 2, 16, 16],
                [14, 0, 0, 16, 16, 16],
                [2, 0, 0, 14, 16, 2],
                [2, 0, 14, 14, 16, 16]
            ]
        },
        {
            id: 'ruined_cauldron',
            name: 'Ruined Cauldron',
            sourceModel: 'minecraft:block/cauldron',
            stone: true,
            fullBlock: false,
            boxes: [
                [2, 0, 2, 14, 4, 14],
                [0, 3, 0, 2, 16, 16],
                [14, 3, 0, 16, 16, 16],
                [2, 3, 0, 14, 16, 2],
                [2, 3, 14, 14, 16, 16]
            ]
        },
        {
            id: 'ruined_crafting_table',
            name: 'Ruined Crafting Table',
            sourceModel: 'minecraft:block/crafting_table',
            stone: false,
            boxes: [[0, 0, 0, 16, 16, 16]]
        },
        {
            id: 'ruined_anvil',
            name: 'Ruined Anvil',
            sourceModel: 'minecraft:block/damaged_anvil',
            horizontal: true,
            stone: true,
            fullBlock: false,
            boxes: [
                [2, 0, 3, 14, 4, 13],
                [4, 4, 5, 12, 10, 11],
                [1, 10, 3, 15, 16, 13]
            ]
        },
        {
            id: 'ruined_campfire',
            name: 'Ruined Campfire',
            sourceModel: 'minecraft:block/campfire_off',
            horizontal: true,
            stone: false,
            fullBlock: false,
            boxes: [[0, 0, 0, 16, 7, 16]]
        },
        {
            id: 'ruined_soul_campfire',
            name: 'Ruined Soul Campfire',
            sourceModel: 'minecraft:block/soul_campfire_off',
            horizontal: true,
            stone: false,
            fullBlock: false,
            boxes: [[0, 0, 0, 16, 7, 16]]
        },
        {
            id: 'ruined_enchanting_table',
            name: 'Ruined Enchanting Table',
            sourceModel: 'minecraft:block/enchanting_table',
            stone: true,
            fullBlock: false,
            boxes: [[0, 0, 0, 16, 12, 16]]
        }
    ]

    workstationFamily.forEach(def => {
        let builder = event.create(def.id)
            .displayName(def.name)
            .hardness(2.5)
            .resistance(3.0)
            .requiresTool(true)
            .defaultCutout()

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

        if (def.attachFace) {
            builder.setBlockstateJson(grindstoneLayeredBlockstate(def.id))
        } else if (def.horizontal) {
            builder.setBlockstateJson(horizontalLayeredBlockstate(def.id, def.sourceModel))
        } else {
            builder.setBlockstateJson(layeredBlockstate(def.id, def.sourceModel))
        }

        builder.setModelJson(crackOverlayModel(def.boxes))
        configureRuinedItem(builder, def.sourceModel)
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

ForgeEvents.onEvent('net.minecraftforge.event.level.ChunkEvent$Load', event => {
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
