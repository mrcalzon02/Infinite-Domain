// Infinite Domain — Ruined Worldgen Furnace Progression Gate
//
// Generated furnaces must read visually as their vanilla counterparts but be
// mechanically dead. Player-crafted/player-placed vanilla furnaces are never
// touched because replacement only runs once for newly generated chunks.

const $BuiltInRegistries = Java.loadClass('net.minecraft.core.registries.BuiltInRegistries')
const $ResourceLocation = Java.loadClass('net.minecraft.resources.ResourceLocation')

function ruinedCubeModel(front, side, top, bottom) {
    const crack = 'minecraft:block/destroy_stage_5'
    const baseFaces = {
        down:  { texture: '#bottom', cullface: 'down' },
        up:    { texture: '#top',    cullface: 'up' },
        north: { texture: '#front',  cullface: 'north' },
        south: { texture: '#side',   cullface: 'south' },
        west:  { texture: '#side',   cullface: 'west' },
        east:  { texture: '#side',   cullface: 'east' }
    }
    const crackFaces = {
        down:  { texture: '#crack', cullface: 'down' },
        up:    { texture: '#crack', cullface: 'up' },
        north: { texture: '#crack', cullface: 'north' },
        south: { texture: '#crack', cullface: 'south' },
        west:  { texture: '#crack', cullface: 'west' },
        east:  { texture: '#crack', cullface: 'east' }
    }

    return {
        parent: 'minecraft:block/block',
        ambientocclusion: true,
        textures: {
            front: front,
            side: side,
            top: top,
            bottom: bottom || top,
            crack: crack,
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

StartupEvents.registry('block', event => {
    const ruined = [
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

    ruined.forEach(def => {
        event.create(def.id)
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
            .item(item => {
                item.parentModel(`kubejs:block/${def.id}`)
                    .tooltip('§8Ruined Old World infrastructure')
                    .tooltip('§7Inoperable. Salvage only.')
            })
    })
})

function ruinedSourceKey(state) {
    if (state.is(Blocks.FURNACE)) return 'furnace'
    if (state.is(Blocks.SMOKER)) return 'smoker'
    if (state.is(Blocks.BLAST_FURNACE)) return 'blast_furnace'
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
    // Delay world mutation by one server tick, then scan only this new chunk.
    server.scheduleInTicks(1, () => {
        if (!level.hasChunk(chunkX, chunkZ)) return

        const chunk = level.getChunk(chunkX, chunkZ)
        const replacements = []

        chunk.findBlocks(
            state => ruinedSourceKey(state) !== null,
            (pos, state) => {
                replacements.push({
                    pos: pos.immutable(),
                    source: ruinedSourceKey(state),
                    facing: state.getValue(BlockProperties.HORIZONTAL_FACING)
                })
            }
        )

        replacements.forEach(entry => {
            const target = registeredBlock(`kubejs:ruined_${entry.source}`)
            let targetState = target.defaultBlockState()
                .setValue(BlockProperties.HORIZONTAL_FACING, entry.facing)

            level.setBlock(entry.pos, targetState, 3)
        })
    })
})
