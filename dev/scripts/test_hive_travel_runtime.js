const assert = require('node:assert/strict')
const fs = require('node:fs')
const path = require('node:path')
const vm = require('node:vm')
const HIVE = 'infinite_domain:hive_world'
const OVERWORLD = 'minecraft:overworld'
const CORE = 'kubejs:cinderstack_portal_core'
const MARKER = 'kubejs:cinderstack_marker'
const RETURN = 'kubejs:cinderstack_return_marker'

function fixture() {
    const handlers = { login: [], tick: [], death: [], item: {} }
    const commands = [], messages = [], gifts = []
    const blocks = new Map()
    const key = (x, y, z) => [x, y, z].join(',')
    for (let x = -1; x <= 2; x++) for (let y = 0; y <= 4; y++) {
        const corner = (x === -1 || x === 2) && (y === 0 || y === 4)
        const edge = x === -1 || x === 2 || y === 0 || y === 4
        blocks.set(key(x, 63 + y, 0), corner ? 'kubejs:cinderstack_portal_actuator'
            : edge ? 'kubejs:cinderstack_portal_frame' : 'minecraft:air')
    }
    blocks.set(key(0, 63, 0), CORE)
    const level = { dimension: OVERWORLD, isClientSide: () => false,
        getBlock: (x, y, z) => ({ id: blocks.get(key(x, y, z)) || 'minecraft:air' }) }
    const player = { level, username: 'Tester', age: 20, persistentData: {},
        x: 100, y: 70, z: 200, getYRot: () => 35, getXRot: () => -10,
        tell: message => messages.push(message), give: item => gifts.push(item),
        isCreative: () => false, isSpectator: () => false,
        inventory: { size: 41, getStackInSlot: () => ({ isEmpty: () => true }) } }
    const server = { failTeleport: false, runCommandSilent(command) {
        commands.push(command)
        const tp = command.match(/^execute as Tester in (\S+) run tp Tester (\S+) (\S+) (\S+)/)
        if (tp && !this.failTeleport) {
            level.dimension = tp[1]
            player.x = Number(tp[2]); player.y = Number(tp[3]); player.z = Number(tp[4])
        }
    } }
    player.server = server
    const context = {
        BlockEvents: { rightClicked: (id, callback) => { handlers.core = callback } },
        ItemEvents: { rightClicked: (id, callback) => { handlers.item[id] = callback } },
        PlayerEvents: { loggedIn: fn => handlers.login.push(fn), tick: fn => handlers.tick.push(fn) },
        EntityEvents: { death: (id, fn) => handlers.death.push(fn) },
        ServerEvents: { recipes: () => {} }, Item: { of: id => id }
    }
    for (const script of ['hive_world_expedition.js', 'hive_world_atmosphere_proto.js']) {
        vm.runInNewContext(fs.readFileSync(path.resolve(__dirname,
            '../../kubejs/server_scripts', script), 'utf8'), context)
    }
    function click(item) {
        handlers.core({ player, level, block: { x: 0, y: 63, z: 0 }, item: { id: item },
            cancel() { throw new Error('EVENT_EXIT') } })
    }
    function use(item) { assert.throws(() => click(item), /EVENT_EXIT/) }
    return { handlers, commands, messages, gifts, level, player, server, blocks, use }
}

let f = fixture()
for (const login of f.handlers.login) login({ player: f.player })
assert.equal(f.player.persistentData.id_cinderstack_bar_ready, false)
f.use(MARKER)
assert.equal(f.level.dimension, HIVE)
assert.equal(f.player.persistentData.id_cinderstack_origin_dim, OVERWORLD)
assert.equal(f.player.persistentData.id_cinderstack_origin_yaw, 35)
assert.equal(f.player.persistentData.id_cinderstack_active, true)
assert.equal(f.gifts.at(-1), RETURN)
assert.ok(f.commands.includes('execute in ' + HIVE + ' run function infinite_domain:hive_world/build_arrival'))
assert.ok(f.commands.includes('execute in ' + HIVE + ' run forceload remove 8 8'))
for (const tick of f.handlers.tick) tick({ player: f.player, level: f.level })
assert.ok(f.player.persistentData.id_cinderstack_exposure > 0)
f.use(RETURN)
assert.equal(f.level.dimension, OVERWORLD)
assert.deepEqual([f.player.x, f.player.y, f.player.z], [100, 70, 200])
assert.equal(f.player.persistentData.id_cinderstack_active, false)
assert.ok(f.commands.some(command => command.endsWith('100 70 200 35 -10')))

f = fixture()
f.blocks.clear()
f.use(MARKER)
assert.equal(f.level.dimension, OVERWORLD)
assert.equal(f.gifts.length, 0)
assert.ok(f.messages.at(-1).includes('Incomplete portal'))

f = fixture()
f.server.failTeleport = true
f.use(MARKER)
assert.equal(f.player.persistentData.id_cinderstack_pending, false)
assert.equal(f.gifts.length, 0)
assert.ok(f.messages.at(-1).includes('Transfer failed'))

f = fixture()
f.level.dimension = HIVE
f.player.persistentData.id_cinderstack_pending = true
for (const login of f.handlers.login) login({ player: f.player })
assert.equal(f.player.persistentData.id_cinderstack_active, true)
assert.equal(f.gifts.at(-1), RETURN)
for (const death of f.handlers.death) death({ entity: f.player })
assert.equal(f.player.persistentData.id_cinderstack_active, false)
assert.equal(f.player.persistentData.id_cinderstack_exposure, 0)
// Interrupted/blocked transfer regression: retain the active return contract until
// a destination change actually succeeds; retries must use the original coordinates.
f = fixture()
f.use(MARKER)
const recorded = {
    dimension: f.player.persistentData.id_cinderstack_origin_dim,
    x: f.player.persistentData.id_cinderstack_origin_x,
    y: f.player.persistentData.id_cinderstack_origin_y,
    z: f.player.persistentData.id_cinderstack_origin_z,
    yaw: f.player.persistentData.id_cinderstack_origin_yaw,
    pitch: f.player.persistentData.id_cinderstack_origin_pitch
}
assert.equal(f.gifts.length, 1)
f.use(MARKER) // repeated descent while in the destination cannot overwrite origin
assert.equal(f.gifts.length, 1)
assert.equal(f.player.persistentData.id_cinderstack_origin_x, recorded.x)
f.server.failTeleport = true // the recorded target AND safe fallback are unreachable
f.use(RETURN)
assert.equal(f.level.dimension, HIVE)
assert.equal(f.player.persistentData.id_cinderstack_active, true,
    'both failed return teleports must preserve the expedition for retry')
assert.equal(f.player.persistentData.id_cinderstack_pending, false)
assert.equal(f.player.persistentData.id_cinderstack_origin_dim, recorded.dimension)
assert.deepEqual([
    f.player.persistentData.id_cinderstack_origin_x,
    f.player.persistentData.id_cinderstack_origin_y,
    f.player.persistentData.id_cinderstack_origin_z,
    f.player.persistentData.id_cinderstack_origin_yaw,
    f.player.persistentData.id_cinderstack_origin_pitch
], [recorded.x, recorded.y, recorded.z, recorded.yaw, recorded.pitch])
assert.equal(f.commands.filter(c => c === 'clear Tester ' + RETURN).length, 0)
assert.equal(f.gifts.length, 1)
assert.ok(f.messages.at(-1).includes('retry'), 'failure must not claim a completed fallback')
for (const login of f.handlers.login) login({ player: f.player })
assert.equal(f.player.persistentData.id_cinderstack_active, true)
assert.equal(f.gifts.length, 1)
f.server.failTeleport = false
f.use(RETURN)
assert.equal(f.level.dimension, recorded.dimension)
assert.deepEqual([f.player.x, f.player.y, f.player.z], [recorded.x, recorded.y, recorded.z])
assert.equal(f.player.persistentData.id_cinderstack_active, false)
assert.equal(f.commands.filter(c => c === 'clear Tester ' + RETURN).length, 1)

// A rejected entry never reports arrival and never grants a marker; a later
// successful activation grants exactly one, even after the original failed try.
f = fixture()
f.server.failTeleport = true
f.use(MARKER)
assert.equal(f.level.dimension, OVERWORLD)
assert.equal(f.player.persistentData.id_cinderstack_active, undefined)
assert.equal(f.player.persistentData.id_cinderstack_pending, false)
assert.equal(f.gifts.length, 0)
f.server.failTeleport = false
f.use(MARKER)
assert.equal(f.level.dimension, HIVE)
assert.equal(f.player.persistentData.id_cinderstack_active, true)
assert.equal(f.gifts.length, 1)
f.use(MARKER)
assert.equal(f.gifts.length, 1)

// A disconnected pending transfer finalizes at most once if already arrived.
f = fixture()
f.level.dimension = HIVE
f.player.persistentData.id_cinderstack_pending = true
for (const login of f.handlers.login) login({ player: f.player })
for (const login of f.handlers.login) login({ player: f.player })
assert.equal(f.gifts.length, 1)
assert.equal(f.player.persistentData.id_cinderstack_active, true)
assert.equal(f.player.persistentData.id_cinderstack_pending, false)
for (const death of f.handlers.death) death({ entity: f.player })
assert.equal(f.player.persistentData.id_cinderstack_active, false)
assert.equal(f.player.persistentData.id_cinderstack_pending, false)

// Death during pending (before login recovery) must cancel that transaction.
f = fixture()
f.player.persistentData.id_cinderstack_pending = true
for (const death of f.handlers.death) death({ entity: f.player })
assert.equal(f.player.persistentData.id_cinderstack_pending, false)
assert.equal(f.player.persistentData.id_cinderstack_active, false)
for (const login of f.handlers.login) login({ player: f.player })
assert.equal(f.gifts.length, 0)

// A bad original dimension may use the actual safety landing, but only after
// that landing is observed: distinguish fallback from successful origin return.
f = fixture()
f.use(MARKER)
f.player.persistentData.id_cinderstack_origin_dim = 'minecraft:the_nether'
const commandRunner = f.server.runCommandSilent
f.server.runCommandSilent = function (cmd) {
    const wasBlocked = this.failTeleport
    this.failTeleport = cmd.startsWith('execute as Tester in minecraft:the_nether run tp ')
    try { return commandRunner.call(this, cmd) }
    finally { this.failTeleport = wasBlocked }
}
f.use(RETURN)
assert.equal(f.level.dimension, OVERWORLD)
assert.deepEqual([f.player.x, f.player.y, f.player.z], [100, 320, 200])
assert.equal(f.player.persistentData.id_cinderstack_active, false)
assert.equal(f.commands.filter(c => c === 'clear Tester ' + RETURN).length, 1)
assert.ok(f.messages.at(-1).includes('departure point could not be restored'))

// Relog outside during a pending entry must never manufacture arrival or gifts.
f = fixture()
f.player.persistentData.id_cinderstack_pending = true
f.player.persistentData.id_cinderstack_origin_dim = OVERWORLD
for (const login of f.handlers.login) login({ player: f.player })
assert.equal(f.player.persistentData.id_cinderstack_pending, false)
assert.equal(f.player.persistentData.id_cinderstack_active, undefined)
assert.equal(f.gifts.length, 0)
assert.ok(f.messages.some(m => m.includes('interrupted')))

console.log('Hive runtime passed: string dimension IDs, login, valid entry, atmosphere tick, exact return/rotation, incomplete frame, failed entry, reconnect, death, and feedback before EventExit.')
