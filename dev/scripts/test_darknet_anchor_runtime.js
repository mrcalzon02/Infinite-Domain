// Exercise the live KubeJS tether handlers without starting Minecraft.
const assert = require('node:assert/strict')
const fs = require('node:fs')
const path = require('node:path')
const vm = require('node:vm')

const DARKNET = 'cyberspace:darknet_dimension'
const OVERWORLD = 'minecraft:overworld'
const keys = {
    bound: 'infinite_domain_darknet_anchor_bound',
    grace: 'infinite_domain_darknet_anchor_grace_until'
}
class Anchor {
    constructor(active) { this.active = active }
    isActive() { return this.active }
}
class BlockPos {
    constructor(x, y, z) { Object.assign(this, { x, y, z }) }
}
function fixture() {
    const handlers = {}
    const register = name => (...args) => { handlers[name] = args.at(-1) }
    const context = {
        Java: { loadClass: name => name.includes('SpatialAnchorBlockEntity') ? Anchor
            : name.endsWith('BlockPos') ? BlockPos : { PLAYER_VARIABLES: 'variables' } },
        BlockEvents: {
            placed: register('placed'), broken: register('broken'),
            blockEntityTick: register('anchorTick')
        },
        PlayerEvents: { loggedIn: register('login'), tick: register('playerTick') },
        EntityEvents: { death: register('death') }
    }
    vm.runInNewContext(fs.readFileSync(path.resolve(__dirname,
        '../../kubejs/server_scripts/darknet_anchor.js'), 'utf8'), context)
    const block = { x: 12, y: 64, z: 24, id: 'ae2:spatial_anchor', entity: new Anchor(true),
        set(id) { this.id = id } }
    const level = dimension => ({
        dimension: () => ({ location: () => ({ toString: () => dimension }) }),
        hasChunkAt: () => true, getBlock: () => block
    })
    const variables = { DarknetTimer: 5, DarknetInternalTimer: 1, syncs: 0,
        markSyncDirty() { this.syncs++ } }
    const player = { age: 100, persistentData: {}, level: level(DARKNET), messages: [],
        getData: () => variables, tell(message) { this.messages.push(message) } }
    const server = { players: [player] }
    const event = { player, entity: player, block, level: player.level, server, tick: 20,
        cancelled: false, cancel() { this.cancelled = true } }
    return { handlers, block, level, variables, player, event }
}

const tests = {
    'placement binds coordinates and allows ten seconds to initialize'() {
        const f = fixture()
        f.handlers.placed(f.event)
        assert.equal(f.player.persistentData[keys.bound], true)
        assert.equal(f.player.persistentData[keys.grace], 300)
        assert.equal(f.event.cancelled, false)
    },
    'placement outside Darknet gives feedback before cancellation'() {
        const f = fixture()
        f.event.level = f.level(OVERWORLD)
        f.event.cancel = () => {
            assert.equal(f.player.messages.length, 1)
            f.event.cancelled = true
        }
        f.handlers.placed(f.event)
        assert.equal(f.event.cancelled, true)
        assert.equal(f.player.persistentData[keys.bound], undefined)
    },
    'second placement cannot replace a bound anchor'() {
        const f = fixture()
        f.handlers.placed(f.event)
        f.event.block = { ...f.block, x: 50 }
        f.handlers.placed(f.event)
        assert.equal(f.event.cancelled, true)
        assert.equal(f.player.persistentData.infinite_domain_darknet_anchor_x, 12)
    },
    'matching coordinates in another dimension cannot sever the tether'() {
        const f = fixture()
        f.handlers.placed(f.event)
        f.event.level = f.level(OVERWORLD)
        f.handlers.broken(f.event)
        assert.equal(f.player.persistentData[keys.bound], true)
        assert.equal(f.variables.DarknetTimer, 5)
    },
    'breaking a different Darknet anchor cannot sever the tether'() {
        const f = fixture()
        f.handlers.placed(f.event)
        f.event.block = { ...f.block, x: 50 }
        f.handlers.broken(f.event)
        assert.equal(f.player.persistentData[keys.bound], true)
    },
    'breaking the bound Darknet anchor recalls its owner'() {
        const f = fixture()
        f.handlers.placed(f.event)
        f.handlers.broken(f.event)
        assert.equal(f.player.persistentData[keys.bound], false)
        assert.equal(f.variables.DarknetTimer, 0)
        assert.equal(f.variables.syncs, 1)
    },
    'powered anchor maintains a live session but cannot revive an expired one'() {
        const f = fixture()
        f.handlers.placed(f.event)
        f.handlers.anchorTick(f.event)
        assert.equal(f.variables.DarknetTimer, 20)
        f.variables.DarknetTimer = 0
        f.handlers.anchorTick(f.event)
        assert.equal(f.variables.DarknetTimer, 0)
    },
    'power loss respects startup grace then recalls'() {
        const f = fixture()
        f.handlers.placed(f.event)
        f.block.entity.active = false
        f.handlers.anchorTick(f.event)
        assert.equal(f.player.persistentData[keys.bound], true)
        f.player.age = 300
        f.handlers.anchorTick(f.event)
        assert.equal(f.player.persistentData[keys.bound], false)
        assert.equal(f.variables.DarknetTimer, 0)
    },
    'missing or unloaded anchor recalls after grace'() {
        for (const unloaded of [true, false]) {
            const f = fixture()
            f.handlers.placed(f.event)
            f.player.age = 300
            if (unloaded) f.player.level.hasChunkAt = () => false
            else f.block.id = 'minecraft:air'
            f.handlers.playerTick(f.event)
            assert.equal(f.player.persistentData[keys.bound], false)
            assert.equal(f.variables.DarknetTimer, 0)
        }
    },
    'login resets initialization grace'() {
        const f = fixture()
        f.handlers.placed(f.event)
        f.player.age = 0
        f.handlers.login(f.event)
        assert.equal(f.player.persistentData[keys.grace], 200)
    },
    'death in Darknet destroys the bound anchor'() {
        const f = fixture()
        f.handlers.placed(f.event)
        f.handlers.death(f.event)
        assert.equal(f.block.id, 'minecraft:air')
        assert.equal(f.player.persistentData[keys.bound], false)
    }
}
for (const [name, test] of Object.entries(tests)) {
    test()
    console.log('PASS ' + name)
}
console.log(`Darknet Anchor runtime: ${Object.keys(tests).length} scenarios passed.`)
