#!/usr/bin/env node
// Cinderstack atmosphere regression: the actual script runs against stubbed
// KubeJS events and world blocks. Not a live Minecraft/NeoForge test.
const assert = require('node:assert/strict')
const fs = require('node:fs')
const path = require('node:path')
const vm = require('node:vm')

const source = fs.readFileSync(path.resolve(__dirname,
    '../../kubejs/server_scripts/hive_world_atmosphere_proto.js'), 'utf8')
const HIVE = 'infinite_domain:hive_world'
const BAR = 'infinite_domain:air_tester'
const AIR = 'minecraft:air'

function fixture() {
    const handlers = { ticks: [], login: [], death: [] }
    const blocks = new Map()
    const commands = []
    const messages = []
    const slots = []
    const state = { dimension: HIVE, creative: false, spectator: false, reads: 0 }
    const key = (x, y, z) => x + ',' + y + ',' + z
    const level = {
        get dimension() { return { toString: () => state.dimension } },
        getBlock(x, y, z) {
            state.reads++
            return { id: blocks.get(key(x, y, z)) || AIR }
        },
        isClientSide: () => false
    }
    const empty = { id: AIR, count: 0, isEmpty: () => true }
    const inventory = {
        size: 41,
        getStackInSlot: i => slots[i] || empty
    }
    const player = {
        username: 'Tester', x: 0.5, y: 64.5, z: 0.5,
        age: 20, level, inventory, persistentData: {},
        server: { runCommandSilent(cmd) { commands.push(cmd) } },
        isCreative: () => state.creative,
        isSpectator: () => state.spectator,
        tell(msg) { messages.push(msg) }
    }
    const context = {
        PlayerEvents: {
            tick: fn => handlers.ticks.push(fn),
            loggedIn: fn => handlers.login.push(fn)
        },
        EntityEvents: { death: (entity, fn) => handlers.death.push(fn) },
        ServerEvents: { recipes: () => {} }
    }
    vm.runInNewContext(source, context, { filename: 'hive_world_atmosphere_proto.js', timeout: 1000 })
    assert.equal(handlers.ticks.length, 2)
    assert.equal(handlers.login.length, 1)
    assert.equal(handlers.death.length, 1)
    return {
        player, level, state, slots, commands, messages,
        setBlock(x, y, z, id) { blocks.set(key(x, y, z), id) },
        tick(age) {
            player.age = age
            for (const fn of handlers.ticks) fn({ player, level })
        },
        login() { for (const fn of handlers.login) fn({ player, level }) },
        die() { for (const fn of handlers.death) fn({ entity: player, level }) }
    }
}

let passed = 0
function check(name, run) {
    run()
    passed++
    console.log('PASS ' + name)
}
const playerAssigned = f => f.commands.filter(c => c === 'bossbar set ' + BAR + ' players Tester').length
const playerRemoved = f => f.commands.filter(c => c === 'bossbar set ' + BAR + ' players').length
const HUD = f => f.commands.filter(c => c.startsWith('bossbar '))

check('first Hive tick initializes the bar and samples the full radius', () => {
    const f = fixture()
    f.tick(20)
    assert.equal(f.state.reads, 791)
    assert.equal(f.commands.length, 7)
    assert.equal(playerAssigned(f), 1)
    assert.equal(f.player.persistentData.id_cinderstack_exposure, 2.6)
})

check('center lodestone short-circuits without changing recovery', () => {
    const f = fixture()
    f.player.persistentData.id_cinderstack_exposure = 30
    f.setBlock(0, 64, 0, 'minecraft:lodestone')
    f.tick(20)
    assert.equal(f.state.reads, 4)
    assert.equal(f.player.persistentData.id_cinderstack_exposure, 21)
})

check('zero exposure hides without detaching, then reappears', () => {
    const f = fixture()
    f.tick(20)
    f.setBlock(0, 64, 0, 'minecraft:lodestone')
    f.tick(40)
    assert.equal(f.player.persistentData.id_cinderstack_exposure, 0)
    assert.ok(f.commands.includes('bossbar set ' + BAR + ' visible false'))
    assert.equal(playerRemoved(f), 0)
    f.setBlock(0, 64, 0, AIR)
    f.tick(60)
    assert.equal(playerAssigned(f), 1)
    assert.equal(playerRemoved(f), 0)
    assert.equal(f.commands.at(-1), 'bossbar set ' + BAR + ' visible true')
})

check('unchanged exposure does not resend HUD commands', () => {
    const f = fixture()
    f.player.persistentData.id_cinderstack_exposure = 100
    f.tick(20)
    const before = HUD(f).length
    f.tick(40)
    assert.equal(HUD(f).length, before)
    assert.equal(f.commands.filter(c => c.startsWith('damage Tester ')).length, 2)
})

check('HUD state caches display attributes separately', () => {
    const f = fixture()
    f.tick(20)
    const before = HUD(f).length
    f.tick(40)
    const change = HUD(f).slice(before)
    assert.equal(change.length, 2)
    assert.ok(change[0].startsWith('bossbar set ' + BAR + ' value '))
    assert.ok(change[1].startsWith('bossbar set ' + BAR + ' name '))
})

check('creative mode removes the old owner, survival reattaches', () => {
    const f = fixture()
    f.tick(20)
    f.state.creative = true
    f.tick(40)
    assert.equal(f.player.persistentData.id_cinderstack_exposure, 0)
    assert.equal(f.player.persistentData.id_cinderstack_bar_ready, false)
    assert.equal(playerRemoved(f), 1)
    f.state.creative = false
    f.tick(60)
    assert.equal(playerAssigned(f), 2)
})

check('spectator mode removes owner even at zero exposure', () => {
    const f = fixture()
    f.tick(20)
    f.setBlock(0, 64, 0, 'minecraft:lodestone')
    f.tick(40)
    f.state.spectator = true
    f.tick(60)
    assert.equal(playerRemoved(f), 1)
})

check('leaving Hive removes owner and re-entry rebuilds', () => {
    const f = fixture()
    f.tick(20)
    f.state.dimension = 'minecraft:overworld'
    f.tick(40)
    assert.equal(playerRemoved(f), 1)
    assert.equal(f.player.persistentData.id_cinderstack_bar_ready, false)
    f.state.dimension = HIVE
    f.tick(60)
    assert.equal(playerAssigned(f), 2)
})

check('relog cleans a stale assignment before rebuilding', () => {
    const f = fixture()
    f.tick(20)
    f.login()
    assert.equal(playerRemoved(f), 1)
    f.tick(40)
    assert.equal(playerAssigned(f), 2)
})

check('fresh Overworld login with no bar sends no bossbar commands', () => {
    const f = fixture()
    f.state.dimension = 'minecraft:overworld'
    f.login()
    f.tick(20)
    assert.equal(HUD(f).length, 0)
    assert.equal(f.state.reads, 0)
})

check('death clears exposure, wear, warning and assignment', () => {
    const f = fixture()
    f.tick(20)
    f.player.persistentData.id_cinderstack_filter_wear = 9
    f.player.persistentData.id_cinderstack_air_warned = true
    f.die()
    assert.equal(f.player.persistentData.id_cinderstack_exposure, 0)
    assert.equal(f.player.persistentData.id_cinderstack_filter_wear, 0)
    assert.equal(f.player.persistentData.id_cinderstack_air_warned, false)
    assert.equal(playerRemoved(f), 1)
})

check('acid fumes still multiply exposure by 1.5', () => {
    const f = fixture()
    f.setBlock(0, 64, 0, 'the_wasteland_reworked:acid')
    f.tick(20)
    assert.ok(Math.abs(f.player.persistentData.id_cinderstack_exposure - 3.9) < 0.00001)
    assert.equal(f.state.reads, 791)
})

check('lodestone takes priority over acid at any scan position', () => {
    const f = fixture()
    f.player.persistentData.id_cinderstack_exposure = 20
    f.setBlock(0, 64, 0, 'the_wasteland_reworked:acid')
    f.setBlock(6, 67, 0, 'minecraft:lodestone')
    f.tick(20)
    assert.equal(f.player.persistentData.id_cinderstack_exposure, 11)
    assert.ok(f.state.reads <= 791)
})

check('horizontal and vertical scan bounds are unchanged', () => {
    const f = fixture()
    f.setBlock(7, 64, 0, 'the_wasteland_reworked:acid')
    f.setBlock(0, 68, 0, 'the_wasteland_reworked:acid')
    f.tick(20)
    assert.equal(f.player.persistentData.id_cinderstack_exposure, 2.6)
    assert.equal(f.state.reads, 791)
})

check('filter and mask costs continue once each atmosphere second', () => {
    const f = fixture()
    const mask = { id: 'kubejs:cinderstack_mask', count: 1,
        damageValue: 0, maxDamage: 512, isEmpty() { return this.count <= 0 } }
    const filter = { id: 'kubejs:cinderstack_filter', count: 2,
        isEmpty() { return this.count <= 0 } }
    f.slots[0] = mask
    f.slots[1] = filter
    f.tick(20)
    assert.ok(Math.abs(f.player.persistentData.id_cinderstack_exposure - 0.416) < 0.00001)
    assert.equal(mask.damageValue, 1)
    assert.ok(f.player.persistentData.id_cinderstack_filter_wear > 0)
    f.setBlock(0, 64, 0, 'minecraft:lodestone')
    f.tick(40)
    assert.equal(mask.damageValue, 1)
    assert.equal(filter.count, 2)
})

console.log('Cinderstack atmosphere: ' + passed + ' handler scenarios passed.')
