#!/usr/bin/env node
// Tests the actual KubeJS script with stubbed Minecraft classes and events.
// These handler checks do not certify NeoForge event delivery or a live world.
const assert = require('node:assert/strict')
const fs = require('node:fs')
const path = require('node:path')
const vm = require('node:vm')

class Mob {
    constructor(type, x = 0, z = 0) { Object.assign(this, { type, x, z }) }
}
class Monster extends Mob {}
class PeacefulMob extends Mob {}
class Projectile {
    constructor(type, x = 0, z = 0) { Object.assign(this, { type, x, z }) }
}
const handlers = {}
const script = fs.readFileSync(path.resolve(__dirname,
    '../../kubejs/server_scripts/spawn_hub_hostile_protection.js'), 'utf8')
vm.runInNewContext(script, {
    Java: { loadClass(name) {
        if (name === 'net.minecraft.world.entity.Mob') return Mob
        if (name === 'net.minecraft.world.entity.monster.Monster') return Monster
        throw new Error('Unexpected Java class: ' + name)
    } },
    EntityEvents: {
        checkSpawn(handler) { assert.equal(handlers.checkSpawn, undefined); handlers.checkSpawn = handler },
        spawned(handler) { assert.equal(handlers.spawned, undefined); handlers.spawned = handler }
    }
}, { filename: 'spawn_hub_hostile_protection.js', timeout: 1000 })
assert.deepEqual(Object.keys(handlers).sort(), ['checkSpawn', 'spawned'])

let cases = 0
function check(description, entity, dimension, expectedCancel, x = entity.x, z = entity.z) {
    for (const eventName of ['checkSpawn', 'spawned']) {
        let cancelled = 0
        const event = {
            level: { dimension: { toString: () => dimension } },
            entity, x, z,
            cancel() { cancelled++ }
        }
        handlers[eventName](event)
        assert.equal(cancelled, expectedCancel ? 1 : 0, description + ' (' + eventName + ')')
        cases++
    }
}

check('vanilla monster at hub center', new Monster('minecraft:zombie'), 'minecraft:overworld', true)
check('Spore custom hostile at hub center', new PeacefulMob('spore:slasher'), 'minecraft:overworld', true)
check('villager at hub center', new PeacefulMob('minecraft:villager'), 'minecraft:overworld', false)
check('cow at hub center', new PeacefulMob('minecraft:cow'), 'minecraft:overworld', false)
check('pet at hub center', new PeacefulMob('minecraft:wolf'), 'minecraft:overworld', false)
check('custom passive mob at hub center', new PeacefulMob('other:critter'), 'minecraft:overworld', false)
check('Spore projectile at hub center', new Projectile('spore:acid'), 'minecraft:overworld', false)
check('nonliving item at hub center', new Projectile('minecraft:item'), 'minecraft:overworld', false)
check('monster in the Nether', new Monster('minecraft:zombie'), 'minecraft:the_nether', false)
check('monster in another dimension', new Monster('minecraft:zombie'), 'infinite_domain:hive_world', false)
check('dimension substring is not Overworld', new Monster('minecraft:zombie'), 'custom:minecraft:overworld_clone', false)
check('minimum X/Z corner included', new Monster('minecraft:zombie', -48, -48), 'minecraft:overworld', true)
check('maximum X/Z corner included', new Monster('minecraft:zombie', 63, 63), 'minecraft:overworld', true)
check('X immediately below range', new Monster('minecraft:zombie', -49, 0), 'minecraft:overworld', false)
check('X immediately above range', new Monster('minecraft:zombie', 64, 0), 'minecraft:overworld', false)
check('Z immediately below range', new Monster('minecraft:zombie', 0, -49), 'minecraft:overworld', false)
check('Z immediately above range', new Monster('minecraft:zombie', 0, 64), 'minecraft:overworld', false)
check('Spore mob outside claim', new PeacefulMob('spore:slasher', 120, 0), 'minecraft:overworld', false)
check('unrelated namespace with spore in path', new PeacefulMob('other:spore:slasher'), 'minecraft:overworld', false)

console.log('Spawn hub protection: ' + cases + ' handler cases passed (19 scenarios × 2 events).')
