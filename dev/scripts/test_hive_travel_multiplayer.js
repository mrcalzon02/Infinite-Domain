// Original-source KubeJS callback regression: two players share a server, but
// never a return target, pending flag, item grant, exposure state, or marker clear.
const assert = require('node:assert/strict')
const fs = require('node:fs')
const path = require('node:path')
const vm = require('node:vm')

const HIVE = 'infinite_domain:hive_world'
const OVERWORLD = 'minecraft:overworld'
const DESCENT = 'kubejs:cinderstack_marker'
const RETURN = 'kubejs:cinderstack_return_marker'

function multiplayerFixture() {
    const handlers = { login: [], tick: [], death: [], item: {} }
    const commands = [], cleared = [], players = new Map()
    const blocks = new Map()
    const key = (x, y, z) => [x, y, z].join(',')
    for (let x = -1; x <= 2; x++) for (let y = 0; y <= 4; y++) {
        const corner = (x === -1 || x === 2) && (y === 0 || y === 4)
        const edge = x === -1 || x === 2 || y === 0 || y === 4
        blocks.set(key(x, 63 + y, 0), corner ? 'kubejs:cinderstack_portal_actuator'
            : edge ? 'kubejs:cinderstack_portal_frame' : 'minecraft:air')
    }
    blocks.set(key(0, 63, 0), 'kubejs:cinderstack_portal_core')

    const server = { blocked: new Set(), runCommandSilent(command) {
        commands.push(command)
        const tp = command.match(/^execute as (\w+) in (\S+) run tp (\w+) (\S+) (\S+) (\S+)/)
        if (tp) {
            assert.equal(tp[1], tp[3], 'command executor and target must be the same player')
            const p = players.get(tp[3])
            assert.ok(p, 'teleport target must be an existing player')
            if (!this.blocked.has(tp[3])) {
                p.level.dimension = tp[2]
                p.x = Number(tp[4]); p.y = Number(tp[5]); p.z = Number(tp[6])
            }
        }
        const clear = command.match(/^clear (\w+) kubejs:cinderstack_return_marker$/)
        if (clear) {
            assert.ok(players.has(clear[1]), 'marker clear must name an existing player')
            cleared.push(clear[1])
        }
    } }
    function makePlayer(username, x, y, z, yaw, pitch) {
        const level = { dimension: OVERWORLD, isClientSide: () => false,
            getBlock: (bx, by, bz) => ({ id: blocks.get(key(bx, by, bz)) || 'minecraft:air' }) }
        const p = { username, level, x, y, z, age: 20, server,
            persistentData: {}, messages: [], gifts: [],
            getYRot: () => yaw, getXRot: () => pitch,
            tell(message) { this.messages.push(message) },
            give(item) { this.gifts.push(item) },
            isCreative: () => false, isSpectator: () => false,
            inventory: { size: 41, getStackInSlot: () => ({ isEmpty: () => true }) } }
        players.set(username, p)
        return p
    }
    const callbacks = {
        BlockEvents: { rightClicked: (id, fn) => { handlers.core = fn } },
        ItemEvents: { rightClicked: (id, fn) => { handlers.item[id] = fn } },
        PlayerEvents: { loggedIn: fn => handlers.login.push(fn), tick: fn => handlers.tick.push(fn) },
        EntityEvents: { death: (id, fn) => handlers.death.push(fn) },
        ServerEvents: { recipes: () => {} }, Item: { of: id => id }
    }
    for (const script of ['hive_world_expedition.js', 'hive_world_atmosphere_proto.js']) {
        vm.runInNewContext(fs.readFileSync(path.resolve(__dirname,
            '../../kubejs/server_scripts', script), 'utf8'), callbacks, { filename: script })
    }
    function use(p, item) {
        assert.throws(() => handlers.core({ player: p, level: p.level,
            block: { x: 0, y: 63, z: 0 }, item: { id: item },
            cancel() { throw new Error('EVENT_EXIT') } }), /EVENT_EXIT/)
    }
    function login(p) { for (const fn of handlers.login) fn({ player: p }) }
    function tick(p) { for (const fn of handlers.tick) fn({ player: p, level: p.level }) }
    function death(p) { for (const fn of handlers.death) fn({ entity: p }) }
    return { makePlayer, use, login, tick, death, server, commands, cleared }
}

const f = multiplayerFixture()
const ada = f.makePlayer('Ada', 111, 74, 211, 25, 9)
const bram = f.makePlayer('Bram', -88, 92, -30, -40, -7)
f.login(ada); f.login(bram)
f.use(ada, DESCENT); f.use(bram, DESCENT)
assert.equal(ada.level.dimension, HIVE)
assert.equal(bram.level.dimension, HIVE)
assert.deepEqual([ada.persistentData.id_cinderstack_origin_x,
    ada.persistentData.id_cinderstack_origin_y,
    ada.persistentData.id_cinderstack_origin_z], [111, 74, 211])
assert.deepEqual([bram.persistentData.id_cinderstack_origin_x,
    bram.persistentData.id_cinderstack_origin_y,
    bram.persistentData.id_cinderstack_origin_z], [-88, 92, -30])
assert.equal(ada.persistentData.id_cinderstack_origin_yaw, 25)
assert.equal(bram.persistentData.id_cinderstack_origin_pitch, -7)
assert.deepEqual(ada.gifts, [RETURN])
assert.deepEqual(bram.gifts, [RETURN])
f.tick(ada); f.tick(bram)
const adaExposure = ada.persistentData.id_cinderstack_exposure
assert.ok(adaExposure > 0)
assert.ok(bram.persistentData.id_cinderstack_exposure > 0)
assert.equal(ada.persistentData.id_cinderstack_bar_ready, true)
assert.equal(bram.persistentData.id_cinderstack_bar_ready, true)
assert.ok(f.commands.some(c => c.includes('bossbar set infinite_domain:air_ada players Ada')))
assert.ok(f.commands.some(c => c.includes('bossbar set infinite_domain:air_bram players Bram')))

// Ada cannot reach either exit. Bram can return while Ada remains stranded.
f.server.blocked.add('Ada')
f.use(ada, RETURN)
assert.equal(ada.level.dimension, HIVE)
assert.equal(ada.persistentData.id_cinderstack_active, true)
assert.equal(ada.persistentData.id_cinderstack_pending, false)
assert.deepEqual(f.cleared, [])
f.use(bram, RETURN)
assert.equal(bram.level.dimension, OVERWORLD)
assert.deepEqual([bram.x, bram.y, bram.z], [-88, 92, -30])
assert.equal(bram.persistentData.id_cinderstack_active, false)
assert.deepEqual(f.cleared, ['Bram'], 'success must clear only Bram\'s marker')
assert.equal(ada.persistentData.id_cinderstack_active, true)
assert.equal(ada.level.dimension, HIVE)
assert.equal(ada.persistentData.id_cinderstack_origin_x, 111)
assert.equal(ada.persistentData.id_cinderstack_exposure, adaExposure)
assert.deepEqual(ada.gifts, [RETURN])
assert.deepEqual(bram.gifts, [RETURN])

// Reconnect and atmosphere cleanup must not affect the other user's record.
f.login(ada); f.login(bram)
assert.deepEqual(ada.gifts, [RETURN]); assert.deepEqual(bram.gifts, [RETURN])
assert.equal(ada.persistentData.id_cinderstack_bar_ready, false)
assert.equal(bram.persistentData.id_cinderstack_bar_ready, false)
f.tick(ada) // a relog reattaches only Ada's on-dimension HUD
const adaAfterRelogExposure = ada.persistentData.id_cinderstack_exposure
assert.ok(adaAfterRelogExposure > adaExposure)
bram.age = 40
f.tick(bram)
assert.equal(bram.persistentData.id_cinderstack_exposure, 0)
assert.equal(bram.persistentData.id_cinderstack_bar_ready, false)
assert.equal(ada.persistentData.id_cinderstack_bar_ready, true)
assert.equal(ada.persistentData.id_cinderstack_exposure, adaAfterRelogExposure)
f.use(ada, RETURN) // second blocked exit is safe and idempotent
assert.deepEqual(f.cleared, ['Bram'])
f.server.blocked.delete('Ada')
f.use(ada, RETURN)
assert.equal(ada.level.dimension, OVERWORLD)
assert.deepEqual([ada.x, ada.y, ada.z], [111, 74, 211])
assert.equal(ada.persistentData.id_cinderstack_active, false)
assert.deepEqual(f.cleared, ['Bram', 'Ada'])
f.use(ada, RETURN) // no active expedition -> no second clear
assert.deepEqual(f.cleared, ['Bram', 'Ada'])
assert.deepEqual(bram.gifts, [RETURN])

// Interleaved death: one active expedition ends, the other persists to exit.
const d = multiplayerFixture()
const dAda = d.makePlayer('Ada', 1, 69, 2, 0, 0)
const dBram = d.makePlayer('Bram', 3, 77, 4, 0, 0)
d.use(dAda, DESCENT); d.use(dBram, DESCENT)
d.tick(dAda); d.tick(dBram)
d.death(dAda)
assert.equal(dAda.persistentData.id_cinderstack_active, false)
assert.equal(dAda.persistentData.id_cinderstack_exposure, 0)
assert.equal(dBram.persistentData.id_cinderstack_active, true)
assert.ok(dBram.persistentData.id_cinderstack_exposure > 0)
assert.deepEqual(d.cleared, ['Ada'])
d.use(dBram, RETURN)
assert.deepEqual(d.cleared, ['Ada', 'Bram'])
assert.deepEqual([dBram.x, dBram.y, dBram.z], [3, 77, 4])

// Simultaneous login recovery must finalize only the player who really arrived.
const r = multiplayerFixture()
const rAda = r.makePlayer('Ada', 15, 80, 18, 0, 0)
const rBram = r.makePlayer('Bram', 24, 81, 30, 0, 0)
rAda.level.dimension = HIVE
rAda.persistentData.id_cinderstack_pending = true
rBram.persistentData.id_cinderstack_pending = true
r.login(rBram); r.login(rAda); r.login(rAda)
assert.equal(rBram.persistentData.id_cinderstack_pending, false)
assert.equal(rBram.persistentData.id_cinderstack_active, undefined)
assert.deepEqual(rBram.gifts, [])
assert.equal(rAda.persistentData.id_cinderstack_active, true)
assert.equal(rAda.persistentData.id_cinderstack_pending, false)
assert.deepEqual(rAda.gifts, [RETURN])
r.death(rAda)
assert.equal(rAda.persistentData.id_cinderstack_active, false)
assert.deepEqual(r.cleared, ['Ada'])
assert.deepEqual(rBram.gifts, [])
assert.equal(rBram.persistentData.id_cinderstack_active, undefined)
console.log('Cinderstack two-player original-callback isolation passed: mixed return, retry, relog, atmosphere, death and interrupted arrivals.')
