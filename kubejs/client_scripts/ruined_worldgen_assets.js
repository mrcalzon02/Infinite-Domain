// [SYSTEM REPORT] Ruined worldgen visual assets for KubeJS 2101.
//
// The startup registry intentionally does not call removed builder methods such as
// setBlockstateJson/setModelJson. These assets are generated in the LAST client
// asset stage so they override KubeJS's default generated blockstate/model data.

const RUINED_CRACK_TEXTURE = 'minecraft:block/destroy_stage_5'

function ruinedCrackFaces() {
    return {
        down:  { texture: '#crack' },
        up:    { texture: '#crack' },
        north: { texture: '#crack' },
        south: { texture: '#crack' },
        west:  { texture: '#crack' },
        east:  { texture: '#crack' }
    }
}

function ruinedCubeModel(front, side, top, bottom) {
    return {
        parent: 'minecraft:block/block',
        ambientocclusion: true,
        textures: {
            front: front,
            side: side,
            top: top,
            bottom: bottom || top,
            crack: RUINED_CRACK_TEXTURE,
            particle: side
        },
        elements: [
            {
                from: [0, 0, 0],
                to: [16, 16, 16],
                faces: {
                    down:  { texture: '#bottom', cullface: 'down' },
                    up:    { texture: '#top',    cullface: 'up' },
                    north: { texture: '#front',  cullface: 'north' },
                    south: { texture: '#side',   cullface: 'south' },
                    west:  { texture: '#side',   cullface: 'west' },
                    east:  { texture: '#side',   cullface: 'east' }
                }
            },
            {
                from: [-0.02, -0.02, -0.02],
                to: [16.02, 16.02, 16.02],
                shade: false,
                faces: ruinedCrackFaces()
            }
        ]
    }
}

function crackOverlayModel(boxes) {
    return {
        parent: 'minecraft:block/block',
        ambientocclusion: false,
        textures: {
            crack: RUINED_CRACK_TEXTURE,
            particle: RUINED_CRACK_TEXTURE
        },
        elements: boxes.map(box => ({
            from: [box[0] - 0.02, box[1] - 0.02, box[2] - 0.02],
            to: [box[3] + 0.02, box[4] + 0.02, box[5] + 0.02],
            shade: false,
            faces: ruinedCrackFaces()
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

function layeredBlockstate(id) {
    return {
        multipart: [
            { apply: { model: `kubejs:block/${id}` } },
            { apply: { model: `kubejs:block/${id}_cracks` } }
        ]
    }
}

function horizontalLayeredBlockstate(id) {
    const rotations = { north: 0, east: 90, south: 180, west: 270 }
    const multipart = []

    Object.keys(rotations).forEach(facing => {
        const y = rotations[facing]
        const base = { model: `kubejs:block/${id}` }
        const crack = { model: `kubejs:block/${id}_cracks` }
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
        const base = { model: `kubejs:block/${id}` }
        const crack = { model: `kubejs:block/${id}_cracks` }
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

const RUINED_FURNACE_ASSETS = [
    {
        id: 'ruined_furnace',
        model: ruinedCubeModel(
            'minecraft:block/furnace_front',
            'minecraft:block/furnace_side',
            'minecraft:block/furnace_top',
            'minecraft:block/furnace_top'
        )
    },
    {
        id: 'ruined_smoker',
        model: ruinedCubeModel(
            'minecraft:block/smoker_front',
            'minecraft:block/smoker_side',
            'minecraft:block/smoker_top',
            'minecraft:block/smoker_bottom'
        )
    },
    {
        id: 'ruined_blast_furnace',
        model: ruinedCubeModel(
            'minecraft:block/blast_furnace_front',
            'minecraft:block/blast_furnace_side',
            'minecraft:block/blast_furnace_top',
            'minecraft:block/blast_furnace_top'
        )
    }
]

const RUINED_WORKSTATION_ASSETS = [
    { id: 'ruined_stonecutter', horizontal: true, boxes: [[0,0,0,16,9,16],[1,9,7.9,15,16,8.1]] },
    { id: 'ruined_smithing_table', boxes: [[0,0,0,16,16,16]] },
    { id: 'ruined_grindstone', horizontal: true, attachFace: true, boxes: [[12,0,6,14,7,10],[2,0,6,4,7,10],[12,7,5,14,13,11],[2,7,5,4,13,11],[4,4,2,12,16,14]] },
    { id: 'ruined_cartography_table', boxes: [[0,0,0,16,16,16]] },
    { id: 'ruined_fletching_table', boxes: [[0,0,0,16,16,16]] },
    { id: 'ruined_loom', horizontal: true, boxes: [[0,0,0,16,16,16]] },
    { id: 'ruined_lectern', horizontal: true, boxes: [[0,0,0,16,2,16],[4,2,4,12,15,12],[0,12,3,16,16,16]] },
    { id: 'ruined_brewing_stand', boxes: [[7,0,7,9,14,9],[1,0,1,15,2,15]] },
    { id: 'ruined_composter', boxes: [[0,0,0,16,2,16],[0,0,0,2,16,16],[14,0,0,16,16,16],[2,0,0,14,16,2],[2,0,14,14,16,16]] },
    { id: 'ruined_cauldron', boxes: [[2,0,2,14,4,14],[0,3,0,2,16,16],[14,3,0,16,16,16],[2,3,0,14,16,2],[2,3,14,14,16,16]] },
    { id: 'ruined_crafting_table', boxes: [[0,0,0,16,16,16]] },
    { id: 'ruined_anvil', horizontal: true, boxes: [[2,0,3,14,4,13],[4,4,5,12,10,11],[1,10,3,15,16,13]] },
    { id: 'ruined_campfire', horizontal: true, boxes: [[0,0,0,16,7,16]] },
    { id: 'ruined_soul_campfire', horizontal: true, boxes: [[0,0,0,16,7,16]] },
    { id: 'ruined_enchanting_table', boxes: [[0,0,0,16,12,16]] },
]

ClientEvents.generateAssets('last', event => {
    RUINED_FURNACE_ASSETS.forEach(def => {
        event.json(`kubejs:blockstates/${def.id}.json`, horizontalBlockstate(def.id))
        event.json(`kubejs:models/block/${def.id}.json`, def.model)
    })

    RUINED_WORKSTATION_ASSETS.forEach(def => {
        let blockstate
        if (def.attachFace) {
            blockstate = grindstoneLayeredBlockstate(def.id)
        } else if (def.horizontal) {
            blockstate = horizontalLayeredBlockstate(def.id)
        } else {
            blockstate = layeredBlockstate(def.id)
        }

        event.json(`kubejs:blockstates/${def.id}.json`, blockstate)
        event.json(`kubejs:models/block/${def.id}_cracks.json`, crackOverlayModel(def.boxes))
    })
})
