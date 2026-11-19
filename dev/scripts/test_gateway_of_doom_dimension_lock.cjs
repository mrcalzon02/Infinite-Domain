#!/usr/bin/env node
// Pure Node regression test for the KubeJS 2101 gateway restriction handler.
// Does not claim a Minecraft/NeoForge client or server acceptance run.
const assert = require('node:assert/strict')
const fs = require('node:fs')
const path = require('node:path')
const vm = require('node:vm')

const scriptPath = path.resolve(__dirname, '../../kubejs/server_scripts/gateway_of_doom_dimension_lock.js')
const source = fs.readFileSync(scriptPath, 'utf8')
const handlers = new Map()
const expectedEyes = [
    'gateway_of_doom:devil_eye',
    'gateway_of_doom:devil_eye_blue',
    'gateway_of_doom:devil_eye_red',
    'gateway_of_doom:devil_eye_violet'
]

vm.runInNewContext(source, {
    ItemEvents: {
        rightClicked(itemId, handler) {
            assert.equal(typeof handler, 'function')
            assert.equal(handlers.has(itemId), false, 'duplicate handler for ' + itemId)
            handlers.set(itemId, handler)
        }
    },
    Math,
    String
}, { filename: scriptPath, timeout: 1000 })

assert.deepEqual([...handlers.keys()], expectedEyes, 'all four Devil Eyes must be guarded')

let verified = 0
function useEye(eye, dimension) {
    const messages = []
    const commands = []
    let cancelled = 0
    const event = {
        // Deliberately a property, never a callable dimension() method.
        level: { dimension: { toString: () => dimension } },
        player: {
            getGameProfile: () => ({ getName: () => 'Tester_42' }),
            tell: message => messages.push(message)
        },
        server: { runCommandSilent: command => commands.push(command) },
        cancel: () => { cancelled++ }
    }
    handlers.get(eye)(event)
    verified++
    return { messages, commands, cancelled }
}

for (const eye of expectedEyes) {
    const accepted = useEye(eye, 'cyberspace:cyberspace_dimension')
    assert.equal(accepted.cancelled, 0, eye + ' should work in Cyberspace')
    assert.equal(accepted.messages.length, 0)
    assert.equal(accepted.commands.length, 0)

    for (const [dimension, label] of [
        ['minecraft:overworld', 'the Overworld'],
        ['minecraft:the_nether', 'the Nether'],
        ['minecraft:the_end', 'the End'],
        ['cyberspace:darknet_dimension', 'the Darknet'],
        ['custom:forgotten_realm', 'forgotten realm']
    ]) {
        const rejected = useEye(eye, dimension)
        assert.equal(rejected.cancelled, 1, eye + ' must be rejected in ' + dimension)
        assert.equal(rejected.messages.length, 1)
        assert.match(rejected.messages[0], /only usable in Cyberspace/)
        assert.ok(rejected.messages[0].includes(label), 'chat should name ' + label)
        assert.equal(rejected.commands.length, 3)
        assert.equal(rejected.commands[0], 'title Tester_42 times 5 45 10')
        assert.ok(rejected.commands[1].includes('Only usable in Cyberspace'))
        assert.ok(rejected.commands[2].includes('You are currently in ' + label + '. - Charles'))
    }
}

console.log('Gateway restriction regression passed: ' + handlers.size + ' eyes, ' + verified + ' dimension/interaction cases')
