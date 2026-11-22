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



check('last cartridge is consumed once and the intact mask falls back to its weaker seal', () => {
    const f = fixture()
    const mask = { id: 'kubejs:cinderstack_mask', count: 1,
        damageValue: 509, maxDamage: 512, isEmpty() { return this.count <= 0 } }
    const filter = { id: 'kubejs:cinderstack_filter', count: 1,
        isEmpty() { return this.count <= 0 } }
    f.slots[0] = mask
    f.slots[1] = filter
    f.player.persistentData.id_cinderstack_filter_wear = 25.5
    f.tick(20)
    assert.equal(filter.count, 0)
    assert.equal(mask.damageValue, 510)
    assert.ok(Math.abs(f.player.persistentData.id_cinderstack_exposure - 0.416) < 0.00001)
    assert.equal(f.messages.filter(m => m.includes('last one')).length, 1)
    const wear = f.player.persistentData.id_cinderstack_filter_wear
    f.tick(40)
    assert.equal(filter.count, 0)
    assert.equal(mask.damageValue, 510) // no filter means no mask durability drain
    assert.equal(f.player.persistentData.id_cinderstack_filter_wear, wear)
    assert.ok(Math.abs(f.player.persistentData.id_cinderstack_exposure - 2.106) < 0.00001)
    assert.equal(f.messages.filter(m => m.includes('last one')).length, 1)
    assert.ok(f.commands.some(c => c.includes('Atmosphere 2%')))
})

check('last filter and damaged mask break once; reload exposes player until clean-air shelter', () => {
    const f = fixture()
    const mask = { id: 'kubejs:cinderstack_mask', count: 1,
        damageValue: 511, maxDamage: 512, isEmpty() { return this.count <= 0 } }
    const filter = { id: 'kubejs:cinderstack_filter', count: 1,
        isEmpty() { return this.count <= 0 } }
    f.slots[0] = mask
    f.slots[1] = filter
    f.player.persistentData.id_cinderstack_exposure = 64
    f.player.persistentData.id_cinderstack_filter_wear = 25.5
    f.tick(20)
    assert.equal(filter.count, 0)
    assert.equal(mask.count, 0)
    assert.ok(Math.abs(f.player.persistentData.id_cinderstack_exposure - 64.416) < 0.00001)
    assert.equal(f.commands.filter(c => c.startsWith('playsound minecraft:entity.item.break')).length, 1)
    f.tick(40) // neither spent item is eligible for further protection or consumption
    assert.equal(filter.count, 0)
    assert.equal(mask.count, 0)
    assert.ok(Math.abs(f.player.persistentData.id_cinderstack_exposure - 67.016) < 0.00001)
    assert.equal(f.messages.filter(m => m.includes('air is not survivable')).length, 1)
    const checkpoint = JSON.parse(JSON.stringify(f.player.persistentData))
    const restored = fixture()
    restored.player.persistentData = checkpoint
    restored.login()
    restored.tick(60)
    assert.ok(Math.abs(restored.player.persistentData.id_cinderstack_exposure - 69.616) < 0.00001)
    assert.equal(restored.messages.filter(m => m.includes('air is not survivable')).length, 0)
    assert.equal(restored.player.persistentData.id_cinderstack_filter_wear, checkpoint.id_cinderstack_filter_wear)
    restored.setBlock(0, 64, 0, 'minecraft:lodestone')
    for (let age = 80; age <= 240; age += 20) restored.tick(age)
    assert.equal(restored.player.persistentData.id_cinderstack_exposure, 0)
    assert.equal(restored.player.persistentData.id_cinderstack_air_warned, false)
    assert.equal(restored.player.persistentData.id_cinderstack_filter_wear, checkpoint.id_cinderstack_filter_wear)
    assert.equal(restored.messages.length, 0)
})


check('threshold 40 is yellow-only, and 65 is red with first warning and weakness', () => {
    const f = fixture()
    f.player.persistentData.id_cinderstack_exposure = 37
    f.tick(20)
    assert.ok(Math.abs(f.player.persistentData.id_cinderstack_exposure - 39.6) < 0.00001)
    assert.ok(f.commands.includes('bossbar set ' + BAR + ' color green'))
    assert.equal(f.commands.filter(c => c.startsWith('effect give ')).length, 0)
    f.tick(40)
    assert.ok(Math.abs(f.player.persistentData.id_cinderstack_exposure - 42.2) < 0.00001)
    assert.ok(f.commands.includes('bossbar set ' + BAR + ' color yellow'))
    assert.equal(f.messages.length, 0)
    assert.equal(f.commands.filter(c => c.startsWith('effect give ')).length, 0)
    f.player.persistentData.id_cinderstack_exposure = 63
    f.tick(60)
    assert.ok(f.commands.includes('bossbar set ' + BAR + ' color red'))
    assert.ok(f.commands.includes('effect give Tester minecraft:weakness 4 0 true'))
    assert.ok(f.commands.includes('effect give Tester minecraft:nausea 4 0 true'))
    assert.equal(f.messages.filter(m => m.includes('air is not survivable')).length, 1)
    assert.equal(f.player.persistentData.id_cinderstack_air_warned, true)
    f.tick(80)
    assert.equal(f.messages.filter(m => m.includes('air is not survivable')).length, 1)
})

check('first critical exposure at 90 triggers two-damage effects and the missed 65 warning', () => {
    const f = fixture()
    // Simulate a checkpoint written in critical air before the warning flag was set.
    f.player.persistentData.id_cinderstack_exposure = 89
    f.player.persistentData.id_cinderstack_air_warned = false
    f.login()
    f.tick(20)
    assert.ok(Math.abs(f.player.persistentData.id_cinderstack_exposure - 91.6) < 0.00001)
    assert.ok(f.commands.includes('effect give Tester minecraft:darkness 4 0 true'))
    assert.ok(f.commands.includes('effect give Tester minecraft:slowness 4 1 true'))
    assert.ok(f.commands.includes('damage Tester 2 minecraft:magic'))
    assert.ok(!f.commands.some(c => c.includes('minecraft:weakness')))
    assert.equal(f.messages.filter(m => m.includes('air is not survivable')).length, 1)
    assert.equal(f.player.persistentData.id_cinderstack_air_warned, true)
    f.tick(40)
    assert.equal(f.messages.filter(m => m.includes('air is not survivable')).length, 1)
})

check('100 caps exposure and increases critical damage to four', () => {
    const f = fixture()
    f.player.persistentData.id_cinderstack_exposure = 99
    f.tick(20)
    f.tick(40)
    assert.equal(f.player.persistentData.id_cinderstack_exposure, 100)
    assert.equal(f.commands.filter(c => c === 'damage Tester 4 minecraft:magic').length, 2)
    assert.equal(f.commands.filter(c => c === 'damage Tester 2 minecraft:magic').length, 0)
})

check('warning flag persists through checkpoint/login, then resets at a true waystation', () => {
    const f = fixture()
    f.player.persistentData.id_cinderstack_exposure = 64
    f.tick(20)
    assert.equal(f.messages.filter(m => m.includes('air is not survivable')).length, 1)
    const checkpoint = JSON.parse(JSON.stringify(f.player.persistentData))
    const restored = fixture()
    restored.player.persistentData = checkpoint
    restored.login()
    restored.tick(20)
    assert.equal(restored.messages.length, 0)
    assert.equal(restored.player.persistentData.id_cinderstack_air_warned, true)
    restored.setBlock(0, 64, 0, 'minecraft:lodestone')
    restored.tick(40)
    assert.equal(restored.player.persistentData.id_cinderstack_air_warned, false)
    assert.ok(Math.abs(restored.player.persistentData.id_cinderstack_exposure - 60.2) < 0.00001)
    restored.setBlock(0, 64, 0, AIR)
    restored.tick(60)
    restored.tick(80)
    assert.equal(restored.messages.filter(m => m.includes('air is not survivable')).length, 1)
    assert.equal(restored.player.persistentData.id_cinderstack_air_warned, true)
})


check('outside dimension decays 25 every 40 ticks, hides owner once, clears wear and warning only at zero', () => {
    const f = fixture()
    const mask = { id: 'kubejs:cinderstack_mask', count: 1,
        damageValue: 14, maxDamage: 512, isEmpty() { return this.count <= 0 } }
    const filter = { id: 'kubejs:cinderstack_filter', count: 2,
        isEmpty() { return this.count <= 0 } }
    f.slots[0] = mask
    f.slots[1] = filter
    const d = f.player.persistentData
    d.id_cinderstack_exposure = 80
    d.id_cinderstack_filter_wear = 7
    d.id_cinderstack_air_warned = true
    f.tick(20)
    const wear = d.id_cinderstack_filter_wear
    const damage = mask.damageValue
    const count = filter.count
    const scans = f.state.reads
    f.state.dimension = 'minecraft:overworld'
    f.tick(21)
    f.tick(39)
    assert.ok(Math.abs(d.id_cinderstack_exposure - 80.416) < 0.00001)
    f.tick(40)
    assert.ok(Math.abs(d.id_cinderstack_exposure - 55.416) < 0.00001)
    assert.equal(d.id_cinderstack_filter_wear, wear)
    assert.equal(d.id_cinderstack_air_warned, true)
    assert.equal(playerRemoved(f), 1)
    f.tick(80)
    f.tick(120)
    assert.ok(Math.abs(d.id_cinderstack_exposure - 5.416) < 0.00001)
    assert.equal(d.id_cinderstack_filter_wear, wear)
    f.tick(160)
    assert.equal(d.id_cinderstack_exposure, 0)
    assert.equal(d.id_cinderstack_filter_wear, 0)
    assert.equal(d.id_cinderstack_air_warned, false)
    f.tick(200)
    assert.equal(playerRemoved(f), 1)
    assert.equal(f.state.reads, scans)
    assert.equal(mask.damageValue, damage)
    assert.equal(filter.count, count)
    assert.equal(f.messages.filter(m => m.includes('Filter cartridge spent')).length, 0)
})

check('checkpoint outside and relog preserve residual exposure without phantom warnings or PPE spend', () => {
    const f = fixture()
    const d = f.player.persistentData
    d.id_cinderstack_exposure = 70
    d.id_cinderstack_air_warned = true
    d.id_cinderstack_filter_wear = 10
    f.tick(20)
    f.state.dimension = 'minecraft:overworld'
    f.tick(40)
    assert.ok(Math.abs(d.id_cinderstack_exposure - 47.6) < 0.00001)
    const checkpoint = JSON.parse(JSON.stringify(d))
    const restored = fixture()
    restored.state.dimension = 'minecraft:overworld'
    restored.player.persistentData = checkpoint
    restored.login()
    restored.tick(60)
    assert.equal(restored.player.persistentData.id_cinderstack_exposure, checkpoint.id_cinderstack_exposure)
    assert.equal(restored.player.persistentData.id_cinderstack_filter_wear, checkpoint.id_cinderstack_filter_wear)
    assert.equal(restored.messages.length, 0)
    assert.equal(HUD(restored).length, 0)
    restored.state.dimension = HIVE
    restored.tick(80)
    assert.ok(Math.abs(restored.player.persistentData.id_cinderstack_exposure - 50.2) < 0.00001)
    assert.equal(playerAssigned(restored), 1)
    assert.equal(restored.messages.length, 0)
    assert.equal(restored.player.persistentData.id_cinderstack_air_warned, true)
    assert.equal(restored.player.persistentData.id_cinderstack_filter_wear, checkpoint.id_cinderstack_filter_wear)
})

check('death resets exposure wear warning and HUD without offworld residue or phantom filter use', () => {
    const f = fixture()
    const mask = { id: 'kubejs:cinderstack_mask', count: 1,
        damageValue: 5, maxDamage: 512, isEmpty() { return this.count <= 0 } }
    const filter = { id: 'kubejs:cinderstack_filter', count: 1,
        isEmpty() { return this.count <= 0 } }
    f.slots[0] = mask
    f.slots[1] = filter
    const d = f.player.persistentData
    d.id_cinderstack_exposure = 90
    d.id_cinderstack_filter_wear = 12
    d.id_cinderstack_air_warned = true
    f.tick(20)
    assert.equal(d.id_cinderstack_bar_ready, true)
    const maskDamage = mask.damageValue
    const filterCount = filter.count
    f.die()
    assert.equal(d.id_cinderstack_exposure, 0)
    assert.equal(d.id_cinderstack_filter_wear, 0)
    assert.equal(d.id_cinderstack_air_warned, false)
    assert.equal(d.id_cinderstack_bar_ready, false)
    assert.equal(playerRemoved(f), 1)
    f.state.dimension = 'minecraft:overworld'
    f.tick(40)
    f.login()
    assert.equal(playerRemoved(f), 1)
    assert.equal(d.id_cinderstack_exposure, 0)
    assert.equal(mask.damageValue, maskDamage)
    assert.equal(filter.count, filterCount)
    assert.equal(f.messages.length, 0)
    assert.equal(d.id_cinderstack_bar_ready, false)
})


check('creative exemption clears spent-wear carryover before resumed PPE use', () => {
    const f = fixture()
    const d = f.player.persistentData
    d.id_cinderstack_exposure = 80
    d.id_cinderstack_filter_wear = 25.8
    d.id_cinderstack_air_warned = true
    f.tick(20) // original hazardous survival tick establishes attached HUD
    const mask = { id: 'kubejs:cinderstack_mask', count: 1,
        damageValue: 7, maxDamage: 512, isEmpty() { return this.count <= 0 } }
    const filter = { id: 'kubejs:cinderstack_filter', count: 2,
        isEmpty() { return this.count <= 0 } }
    f.slots[0] = mask
    f.slots[1] = filter
    const reads = f.state.reads
    f.state.creative = true
    f.tick(40)
    assert.equal(d.id_cinderstack_exposure, 0)
    assert.equal(d.id_cinderstack_filter_wear, 0)
    assert.equal(d.id_cinderstack_air_warned, false)
    assert.equal(d.id_cinderstack_bar_ready, false)
    assert.equal(playerRemoved(f), 1)
    assert.equal(f.state.reads, reads)
    assert.equal(mask.damageValue, 7)
    assert.equal(filter.count, 2)
    f.state.creative = false
    f.tick(60)
    assert.equal(playerAssigned(f), 2)
    assert.equal(filter.count, 2)
    assert.equal(mask.damageValue, 8)
    assert.ok(d.id_cinderstack_filter_wear > 0 && d.id_cinderstack_filter_wear < 1)
    assert.equal(d.id_cinderstack_air_warned, false)
    assert.equal(f.messages.filter(m => m.includes('Filter cartridge spent')).length, 0)
})

check('spectator exemption clears old warning and rewarns on genuinely new danger', () => {
    const f = fixture()
    const d = f.player.persistentData
    d.id_cinderstack_exposure = 94
    d.id_cinderstack_filter_wear = 12
    d.id_cinderstack_air_warned = true
    f.tick(20)
    const effects = f.commands.filter(c => c.startsWith('effect give ') || c.startsWith('damage ')).length
    const reads = f.state.reads
    f.state.spectator = true
    f.tick(40)
    f.tick(60)
    assert.equal(d.id_cinderstack_exposure, 0)
    assert.equal(d.id_cinderstack_filter_wear, 0)
    assert.equal(d.id_cinderstack_air_warned, false)
    assert.equal(playerRemoved(f), 1)
    assert.equal(f.state.reads, reads)
    assert.equal(f.commands.filter(c => c.startsWith('effect give ') || c.startsWith('damage ')).length, effects)
    f.state.spectator = false
    f.tick(80)
    assert.equal(playerAssigned(f), 2)
    assert.equal(f.messages.length, 0)
    d.id_cinderstack_exposure = 63
    f.tick(100)
    assert.equal(d.id_cinderstack_air_warned, true)
    assert.equal(f.messages.filter(m => m.includes('air is not survivable')).length, 1)
    f.tick(120)
    assert.equal(f.messages.filter(m => m.includes('air is not survivable')).length, 1)
})

check('creative spectator relog sequence has no stale HUD, warning or PPE cost', () => {
    const f = fixture()
    f.tick(20)
    const d = f.player.persistentData
    d.id_cinderstack_filter_wear = 20
    d.id_cinderstack_air_warned = true
    f.state.creative = true
    f.tick(40)
    f.state.creative = false
    f.state.spectator = true
    f.tick(60)
    f.login()
    f.tick(80)
    assert.equal(playerRemoved(f), 1)
    assert.equal(d.id_cinderstack_bar_ready, false)
    assert.equal(d.id_cinderstack_filter_wear, 0)
    assert.equal(d.id_cinderstack_air_warned, false)
    assert.equal(d.id_cinderstack_exposure, 0)
    assert.equal(f.messages.length, 0)
    f.state.spectator = false
    f.tick(100)
    assert.equal(playerAssigned(f), 2)
    assert.equal(d.id_cinderstack_filter_wear, 0)
    assert.equal(d.id_cinderstack_air_warned, false)
    assert.equal(f.commands.filter(c => c.startsWith('damage ')).length, 0)
})


check('acid and edge lodestone shelter recover without PPE cost, then outside fume resumes cartridge and warning', () => {
    const f = fixture()
    const d = f.player.persistentData
    const mask = { id: 'kubejs:cinderstack_mask', count: 1,
        damageValue: 8, maxDamage: 512, isEmpty() { return this.count <= 0 } }
    const filter = { id: 'kubejs:cinderstack_filter', count: 2,
        isEmpty() { return this.count <= 0 } }
    f.slots[0] = mask
    f.slots[1] = filter
    d.id_cinderstack_exposure = 80
    d.id_cinderstack_filter_wear = 25.8
    d.id_cinderstack_air_warned = true
    f.setBlock(0, 64, 0, 'the_wasteland_reworked:acid')
    f.setBlock(6, 67, 0, 'minecraft:lodestone') // exactly horizontal 6 / vertical +3

    f.tick(20)
    assert.equal(d.id_cinderstack_exposure, 71) // shelter overrides even center acid
    assert.equal(d.id_cinderstack_filter_wear, 25.8)
    assert.equal(d.id_cinderstack_air_warned, false)
    assert.equal(mask.damageValue, 8)
    assert.equal(filter.count, 2)
    assert.equal(f.messages.length, 0)
    assert.ok(f.state.reads <= 791)

    // The lodestone is now seven blocks away: only fumes remain in the new scan.
    f.player.x = 13.5
    f.setBlock(13, 64, 0, 'the_wasteland_reworked:acid')
    const before = f.state.reads
    f.tick(40)
    assert.equal(f.state.reads - before, 791)
    assert.ok(Math.abs(d.id_cinderstack_exposure - 71.624) < 0.000001)
    assert.ok(Math.abs(d.id_cinderstack_filter_wear - 0.814) < 0.000001)
    assert.equal(filter.count, 1) // first resumed tick spends exactly one cartridge
    assert.equal(mask.damageValue, 9)
    assert.equal(d.id_cinderstack_air_warned, true)
    assert.equal(f.messages.filter(m => m.includes('air is not survivable')).length, 1)
    assert.equal(f.messages.filter(m => m.includes('Filter cartridge spent')).length, 1)
    f.tick(60)
    assert.equal(filter.count, 1)
    assert.equal(mask.damageValue, 10)
    assert.equal(f.messages.filter(m => m.includes('air is not survivable')).length, 1)
})

check('six-block lodestone boundary is inclusive but seventh block cannot suppress nearby fumes', () => {
    const f = fixture()
    const d = f.player.persistentData
    d.id_cinderstack_exposure = 20
    f.setBlock(6, 67, 0, 'minecraft:lodestone')
    f.setBlock(0, 64, 0, 'the_wasteland_reworked:acid')
    f.tick(20)
    assert.equal(d.id_cinderstack_exposure, 11)
    f.player.x = -0.5 // floor -1: lodestone horizontal distance = 7
    const before = f.state.reads
    f.tick(40)
    assert.equal(f.state.reads - before, 791)
    assert.ok(Math.abs(d.id_cinderstack_exposure - 14.9) < 0.000001)
    f.player.x = 0.5
    f.tick(60)
    assert.ok(Math.abs(d.id_cinderstack_exposure - 5.9) < 0.000001)
})

check('diagonal circle and vertical three-block boundaries exclude over-radius shelters', () => {
    const f = fixture()
    const d = f.player.persistentData
    d.id_cinderstack_exposure = 30
    f.setBlock(0, 64, 0, 'the_wasteland_reworked:acid')
    f.setBlock(4, 67, 4, 'minecraft:lodestone') // 4²+4²=32; dy=+3
    f.tick(20)
    assert.equal(d.id_cinderstack_exposure, 21)
    f.setBlock(4, 67, 4, AIR)
    f.setBlock(5, 67, 4, 'minecraft:lodestone') // 5²+4²=41, outside circle
    const before = f.state.reads
    f.tick(40)
    assert.equal(f.state.reads - before, 791)
    assert.ok(Math.abs(d.id_cinderstack_exposure - 24.9) < 0.000001)
    f.setBlock(5, 67, 4, AIR)
    f.setBlock(0, 68, 0, 'minecraft:lodestone') // dy +4 outside vertical range
    f.tick(60)
    assert.ok(Math.abs(d.id_cinderstack_exposure - 28.8) < 0.000001)
    f.setBlock(0, 68, 0, AIR)
    f.setBlock(0, 61, 0, 'minecraft:lodestone') // dy -3 inside range
    f.tick(80)
    assert.ok(Math.abs(d.id_cinderstack_exposure - 19.8) < 0.000001)
})


check('continuous exposure climbs 39 40 65 90 100 with exact HUD severity and one warning', () => {
    const f = fixture()
    const d = f.player.persistentData
    const stages = [
        { start: 36.4, value: 39, color: 'green', warnings: 0 },
        { start: 37.4, value: 40, color: 'yellow', warnings: 0 },
        { start: 62.4, value: 65, color: 'red', warnings: 1 },
        { start: 87.4, value: 90, color: 'red', warnings: 1 },
        { start: 99, value: 100, color: 'red', warnings: 1 },
    ]
    let priorColor = null
    for (let i = 0; i < stages.length; i++) {
        const s = stages[i]
        d.id_cinderstack_exposure = s.start
        const previous = HUD(f).length
        f.tick(20 * (i + 1))
        assert.equal(d.id_cinderstack_exposure, s.value)
        const changes = HUD(f).slice(previous)
        assert.ok(changes.includes('bossbar set ' + BAR + ' value ' + s.value))
        assert.ok(changes.includes('bossbar set ' + BAR + ' name ' +
            JSON.stringify({ text: 'Atmosphere ' + s.value + '%' })))
        assert.equal(changes.filter(c => c.includes(' color ')).length,
            priorColor === s.color ? 0 : 1)
        if (priorColor !== s.color) {
            assert.ok(changes.includes('bossbar set ' + BAR + ' color ' + s.color))
        }
        assert.equal(f.messages.filter(m => m.includes('air is not survivable')).length,
            s.warnings)
        priorColor = s.color
    }
    assert.equal(f.commands.filter(c => c === 'damage Tester 2 minecraft:magic').length, 1)
    assert.equal(f.commands.filter(c => c === 'damage Tester 4 minecraft:magic').length, 1)
    const atCap = HUD(f).length
    f.tick(101) // skipped: only 20-tick atmosphere cadence
    f.tick(120) // still capped: gameplay effects recur but HUD is unchanged
    assert.equal(HUD(f).length, atCap)
    assert.equal(f.messages.filter(m => m.includes('air is not survivable')).length, 1)
})

check('same rounded exposure changes only the HUD title when PPE becomes active or inactive', () => {
    const f = fixture()
    const d = f.player.persistentData
    d.id_cinderstack_exposure = 62.4
    f.tick(20)
    assert.equal(d.id_cinderstack_exposure, 65)
    f.slots[0] = { id: 'kubejs:cinderstack_mask', count: 1,
        damageValue: 0, maxDamage: 512, isEmpty() { return this.count <= 0 } }
    f.slots[1] = { id: 'kubejs:cinderstack_filter', count: 2,
        isEmpty() { return this.count <= 0 } }
    d.id_cinderstack_exposure = 64.584
    const beforeFiltering = HUD(f).length
    f.tick(40)
    assert.equal(Math.round(d.id_cinderstack_exposure), 65)
    assert.equal(HUD(f).length - beforeFiltering, 1)
    assert.equal(HUD(f).at(-1), 'bossbar set ' + BAR + ' name ' +
        JSON.stringify({ text: 'Filtered air 65%' }))
    f.slots.length = 0
    d.id_cinderstack_exposure = 62.4
    const beforeUnfiltered = HUD(f).length
    f.tick(60)
    assert.equal(Math.round(d.id_cinderstack_exposure), 65)
    assert.equal(HUD(f).length - beforeUnfiltered, 1)
    assert.equal(HUD(f).at(-1), 'bossbar set ' + BAR + ' name ' +
        JSON.stringify({ text: 'Atmosphere 65%' }))
    assert.equal(f.messages.filter(m => m.includes('air is not survivable')).length, 1)
})

check('recovery to zero hides once, offworld exit detaches and relog safely reattaches', () => {
    const f = fixture()
    const d = f.player.persistentData
    d.id_cinderstack_exposure = 100
    d.id_cinderstack_air_warned = true
    f.tick(20)
    f.setBlock(0, 64, 0, 'minecraft:lodestone')
    for (let age = 40; age <= 280; age += 20) f.tick(age)
    assert.equal(d.id_cinderstack_exposure, 0)
    assert.equal(d.id_cinderstack_air_warned, false)
    assert.equal(f.commands.filter(c => c === 'bossbar set ' + BAR + ' visible false').length, 1)
    assert.equal(playerAssigned(f), 1)
    assert.equal(playerRemoved(f), 0)
    const atZero = HUD(f).length
    f.tick(300)
    assert.equal(HUD(f).length, atZero)
    f.state.dimension = 'minecraft:overworld'
    f.tick(320)
    assert.equal(playerRemoved(f), 1)
    f.login()
    f.tick(360)
    assert.equal(playerRemoved(f), 1)
    f.state.dimension = HIVE
    f.setBlock(0, 64, 0, AIR)
    f.tick(380)
    assert.equal(playerAssigned(f), 2)
    assert.equal(f.commands.filter(c => c === 'bossbar set ' + BAR + ' visible true').length, 2)
    assert.equal(d.id_cinderstack_exposure, 2.6)
})

console.log('Cinderstack atmosphere: ' + passed + ' handler scenarios passed.')
