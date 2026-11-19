#!/usr/bin/env node
// Exercise the live KubeJS 2101 injector handlers without launching Minecraft.
// Rejection cancellation uses a thrown sentinel to model KubeJS EventExit.
const assert = require('node:assert/strict')
const fs = require('node:fs')
const path = require('node:path')
const vm = require('node:vm')

const script = fs.readFileSync(path.resolve(__dirname,
    '../../kubejs/server_scripts/darknet_session_injector.js'), 'utf8')
const handlers = new Map()
const seconds = [30, 60, 120, 240, 480, 960, 1920, 3840]
const ids = seconds.map((_, index) => 'kubejs:darknet_session_injector_tier_' + (index + 1))
vm.runInNewContext(script, {
    Java: { loadClass: () => ({ PLAYER_VARIABLES: 'variables' }) },
    ItemEvents: { rightClicked(id, callback) {
        assert.equal(handlers.has(id), false, 'duplicate injector registration')
        handlers.set(id, callback)
    } },
    Math
}, { filename: 'darknet_session_injector.js', timeout: 1000 })
assert.deepEqual([...handlers.keys()], ids, 'all eight injector tiers must register')

let scenarios = 0
function useInjector(id, dimension, internal, remaining) {
    const messages = []
    const commands = []
    const variables = { DarknetInternalTimer: internal, DarknetTimer: remaining,
        syncs: 0, markSyncDirty() { this.syncs++ } }
    const player = {
        getData: () => variables,
        getGameProfile: () => ({ getName: () => 'Tester_42' }),
        tell: text => messages.push(text)
    }
    const item = { count: 2 }
    const eventExit = Symbol('KubeJS EventExit')
    let cancellations = 0
    const event = {
        // This must be a property; a fake dimension() method hides the real bug.
        level: { dimension: { toString: () => dimension } },
        player, item,
        server: { runCommandSilent: cmd => commands.push(cmd) },
        cancel() { cancellations++; throw eventExit }
    }
    try { handlers.get(id)(event) }
    catch (err) { if (err !== eventExit) throw err }
    scenarios++
    return { messages, commands, variables, item, cancellations }
}

for (let index = 0; index < ids.length; index++) {
    const id = ids[index]
    for (const [dimension, name] of [
        ['minecraft:overworld', 'the Overworld'],
        ['minecraft:the_nether', 'the Nether'],
        ['cyberspace:cyberspace_dimension', 'Cyberspace']
    ]) {
        const f = useInjector(id, dimension, 1, 60)
        assert.equal(f.cancellations, 1, id + ' must reject ' + dimension)
        assert.equal(f.item.count, 2, 'rejected injector must not be consumed')
        assert.equal(f.variables.DarknetTimer, 60)
        assert.equal(f.variables.syncs, 0)
        assert.equal(f.messages.length, 1)
        assert.ok(f.messages[0].includes(name))
        assert.equal(f.commands[0], 'title Tester_42 times 5 45 10')
        assert.equal(f.commands.length, 3)
        assert.ok(f.commands[1].includes('Darknet injectors only'))
    }
    for (const [internal, remaining] of [[0, 60], [1, 0]]) {
        const f = useInjector(id, 'cyberspace:darknet_dimension', internal, remaining)
        assert.equal(f.cancellations, 1, 'inactive session must be rejected')
        assert.equal(f.item.count, 2)
        assert.equal(f.variables.DarknetTimer, remaining)
        assert.equal(f.variables.syncs, 0)
        assert.equal(f.messages.length, 1)
        assert.ok(f.messages[0].includes('No active Darknet session'))
        assert.equal(f.commands[0], 'title Tester_42 times 5 45 10')
    }
    const f = useInjector(id, 'cyberspace:darknet_dimension', 1, 60)
    assert.equal(f.cancellations, 0)
    assert.equal(f.item.count, 1)
    assert.equal(f.variables.DarknetTimer, 60 + seconds[index])
    assert.equal(f.variables.syncs, 1)
    assert.equal(f.commands.length, 1)
    assert.equal(f.commands[0], 'advancement grant Tester_42 only infinite_domain:darknet_time_extended')
    assert.equal(f.messages.length, 1)
    assert.ok(f.messages[0].includes('Darknet carrier extended'))
}

console.log('Darknet Injector runtime: ' + handlers.size + ' tiers, ' + scenarios + ' handler scenarios passed.')
