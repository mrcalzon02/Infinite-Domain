#!/usr/bin/env node
// Two-player original KubeJS callback regression. This is an offline command/
// player model, not a NeoForge server, socket, or rendered Minecraft client.
const assert = require('node:assert/strict')
const fs = require('node:fs')
const path = require('node:path')
const vm = require('node:vm')

const HIVE = 'infinite_domain:hive_world'
const OVERWORLD = 'minecraft:overworld'
const BAR = name => 'infinite_domain:air_' + name.toLowerCase()
const PD = { exp: 'id_cinderstack_exposure', wear: 'id_cinderstack_filter_wear',
    warned: 'id_cinderstack_air_warned', bar: 'id_cinderstack_bar_ready' }

function fixture() {
    const handlers = { tick: [], login: [], death: [] }
    const commands = []
    const server = { runCommandSilent(command) { commands.push(command) } }
    const context = {
        PlayerEvents: { tick: fn => handlers.tick.push(fn),
            loggedIn: fn => handlers.login.push(fn) },
        EntityEvents: { death: (_id, fn) => handlers.death.push(fn) },
        ServerEvents: { recipes: () => {} }
    }
    const source = fs.readFileSync(path.resolve(__dirname,
        '../../kubejs/server_scripts/hive_world_atmosphere_proto.js'), 'utf8')
    vm.runInNewContext(source, context, { filename: 'hive_world_atmosphere_proto.js', timeout: 1000 })
    assert.deepEqual(handlers.tick.length, 2)
    assert.deepEqual(handlers.login.length, 1)
    assert.deepEqual(handlers.death.length, 1)
    function makePlayer(username, x) {
        const blocks = new Map()
        const slots = []
        const level = { dimension: HIVE, isClientSide: () => false,
            getBlock(bx, by, bz) {
                return { id: blocks.get([bx, by, bz].join(',')) || 'minecraft:air' }
            } }
        const player = { username, server, level, x, y: 64.5, z: 0.5,
            age: 20, persistentData: {}, messages: [],
            inventory: { size: 41, getStackInSlot: i => slots[i] ||
                { id: 'minecraft:air', isEmpty: () => true } },
            creative: false, spectator: false,
            isCreative() { return this.creative },
            isSpectator() { return this.spectator },
            tell(message) { this.messages.push(message) },
            setBlock(bx, by, bz, id) { blocks.set([bx, by, bz].join(','), id) },
            slots }
        return player
    }
    function tick(player, age) {
        player.age = age
        for (const fn of handlers.tick) fn({ player, level: player.level })
    }
    function login(player) { for (const fn of handlers.login) fn({ player }) }
    function die(player) { for (const fn of handlers.death) fn({ entity: player }) }
    const forBar = player => commands.filter(c => c.startsWith('bossbar ') && c.includes(BAR(player.username)))
    return { makePlayer, tick, login, die, commands, forBar }
}

let passed = 0
function check(name, test) {
    test()
    passed++
    console.log('PASS two-player: ' + name)
}
const owner = (p, command) => 'bossbar set ' + BAR(p.username) + ' ' + command
const warningCount = p => p.messages.filter(m => m.includes('air is not survivable')).length

check('two unique persistent assignments on shared server', () => {
    const f = fixture(), a = f.makePlayer('Ada', 0), b = f.makePlayer('Bram', 100)
    f.tick(a, 20); f.tick(b, 20)
    assert.ok(f.commands.includes(owner(a, 'players Ada')))
    assert.ok(f.commands.includes(owner(b, 'players Bram')))
    assert.equal(f.forBar(a).length, 7)
    assert.equal(f.forBar(b).length, 7)
    assert.equal(a.persistentData[PD.exp], 2.6)
    assert.equal(b.persistentData[PD.exp], 2.6)
    assert.equal(a.persistentData[PD.bar], true)
    assert.equal(b.persistentData[PD.bar], true)
})

check('interleaved HUD updates never send the other owner commands', () => {
    const f = fixture(), a = f.makePlayer('Ada', 0), b = f.makePlayer('Bram', 100)
    f.tick(a, 20); f.tick(b, 20)
    const bBefore = f.forBar(b).length, aBefore = f.forBar(a).length
    f.tick(a, 40)
    assert.equal(f.forBar(b).length, bBefore)
    assert.equal(f.forBar(a).length, aBefore + 2)
    assert.equal(b.persistentData[PD.exp], 2.6)
    f.tick(b, 40)
    assert.equal(f.forBar(a).length, aBefore + 2)
    assert.equal(f.forBar(b).length, bBefore + 2)
})

check('unchanged capped HUDs cache independently', () => {
    const f = fixture(), a = f.makePlayer('Ada', 0), b = f.makePlayer('Bram', 100)
    a.persistentData[PD.exp] = 100; b.persistentData[PD.exp] = 100
    f.tick(a, 20); f.tick(b, 20)
    const before = f.commands.filter(c => c.startsWith('bossbar ')).length
    f.tick(b, 40); f.tick(a, 40)
    assert.equal(f.commands.filter(c => c.startsWith('bossbar ')).length, before)
    assert.equal(f.commands.filter(c => c === 'damage Ada 4 minecraft:magic').length, 2)
    assert.equal(f.commands.filter(c => c === 'damage Bram 4 minecraft:magic').length, 2)
})

check('critical warnings and damage target each owner separately', () => {
    const f = fixture(), a = f.makePlayer('Ada', 0), b = f.makePlayer('Bram', 100)
    a.persistentData[PD.exp] = 89
    f.tick(a, 20); f.tick(b, 20)
    assert.equal(warningCount(a), 1)
    assert.equal(warningCount(b), 0)
    assert.ok(f.commands.some(c => c.startsWith('damage Ada ')))
    assert.equal(f.commands.some(c => c.startsWith('damage Bram ')), false)
    b.persistentData[PD.exp] = 64
    f.tick(b, 40); f.tick(a, 40)
    assert.equal(warningCount(b), 1)
    assert.equal(warningCount(a), 1)
    assert.equal(a.persistentData[PD.warned], true)
    assert.equal(b.persistentData[PD.warned], true)
})

check('one recovery-to-zero hides without detaching either owner', () => {
    const f = fixture(), a = f.makePlayer('Ada', 0), b = f.makePlayer('Bram', 100)
    f.tick(a, 20); f.tick(b, 20)
    a.setBlock(0, 64, 0, 'minecraft:lodestone')
    f.tick(a, 40)
    assert.equal(a.persistentData[PD.exp], 0)
    assert.ok(f.commands.includes(owner(a, 'visible false')))
    assert.equal(f.commands.includes(owner(a, 'players')), false)
    assert.equal(f.commands.includes(owner(b, 'visible false')), false)
    assert.equal(b.persistentData[PD.exp], 2.6)
    f.tick(b, 40)
    assert.ok(b.persistentData[PD.exp] > 2.6)
})

check('one player leaves while another stays: only departed HUD detached', () => {
    const f = fixture(), a = f.makePlayer('Ada', 0), b = f.makePlayer('Bram', 100)
    f.tick(a, 20); f.tick(b, 20)
    a.level.dimension = OVERWORLD
    f.tick(a, 40)
    assert.ok(f.commands.includes(owner(a, 'players')))
    assert.equal(f.commands.includes(owner(b, 'players')), false)
    assert.equal(a.persistentData[PD.bar], false)
    assert.equal(b.persistentData[PD.bar], true)
    assert.equal(a.persistentData[PD.exp], 0)
})

check('relogin clears only returning user and reattaches own HUD', () => {
    const f = fixture(), a = f.makePlayer('Ada', 0), b = f.makePlayer('Bram', 100)
    f.tick(a, 20); f.tick(b, 20)
    const aBefore = f.forBar(a).length
    f.login(b)
    assert.equal(f.forBar(a).length, aBefore)
    assert.ok(f.commands.includes(owner(b, 'players')))
    assert.equal(b.persistentData[PD.bar], false)
    f.tick(b, 40)
    assert.equal(b.persistentData[PD.bar], true)
    assert.equal(f.commands.filter(c => c === owner(b, 'players Bram')).length, 2)
    assert.equal(f.forBar(a).length, aBefore)
})

check('death of one player clears only that owner and warnings', () => {
    const f = fixture(), a = f.makePlayer('Ada', 0), b = f.makePlayer('Bram', 100)
    f.tick(a, 20); f.tick(b, 20)
    b.persistentData[PD.warned] = true
    const bBefore = f.forBar(b).length
    f.die(a)
    assert.equal(a.persistentData[PD.exp], 0)
    assert.equal(a.persistentData[PD.warned], false)
    assert.equal(a.persistentData[PD.bar], false)
    assert.equal(b.persistentData[PD.bar], true)
    assert.equal(b.persistentData[PD.warned], true)
    assert.equal(f.forBar(b).length, bBefore)
})

check('creative / spectator exemption never detaches other player', () => {
    const f = fixture(), a = f.makePlayer('Ada', 0), b = f.makePlayer('Bram', 100)
    f.tick(a, 20); f.tick(b, 20)
    a.creative = true
    f.tick(a, 40)
    assert.ok(f.commands.includes(owner(a, 'players')))
    assert.equal(f.commands.includes(owner(b, 'players')), false)
    a.creative = false; a.spectator = true
    f.tick(a, 60)
    assert.equal(a.persistentData[PD.bar], false)
    a.spectator = false
    f.tick(a, 80)
    assert.equal(a.persistentData[PD.bar], true)
    assert.equal(b.persistentData[PD.bar], true)
})

check('filtered-air title and equipment wear never leak to other HUD', () => {
    const f = fixture(), a = f.makePlayer('Ada', 0), b = f.makePlayer('Bram', 100)
    a.slots[0] = { id: 'kubejs:cinderstack_mask', count: 1, damageValue: 0,
        maxDamage: 512, isEmpty() { return this.count <= 0 } }
    a.slots[1] = { id: 'kubejs:cinderstack_filter', count: 2,
        isEmpty() { return this.count <= 0 } }
    f.tick(a, 20); f.tick(b, 20)
    assert.ok(f.commands.some(c => c === owner(a, 'name {"text":"Filtered air 0%"}')))
    assert.ok(f.commands.some(c => c === owner(b, 'name {"text":"Atmosphere 3%"}')))
    assert.equal(a.slots[0].damageValue, 1)
    assert.ok(a.persistentData[PD.wear] > 0)
    assert.equal(b.persistentData[PD.wear], undefined)
    assert.equal(f.commands.some(c => c.includes('bossbar remove ')), false)
})

console.log('Cinderstack two-player atmosphere: ' + passed + ' original-callback scenarios passed.')
