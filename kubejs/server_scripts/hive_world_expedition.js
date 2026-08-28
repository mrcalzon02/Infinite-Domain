// Endgame EG-P06-S01-C0084 - constructed entry/return for infinite_domain:hive_world.
//
// Both travel markers activate at the custom core of a Nether-sized vertical frame.
// Outer dimensions may be 4x5 through 23x23. Four actuators are mandatory corners;
// the core replaces any non-corner block on the lower edge. Either cardinal axis works.
//
// Handles: origin capture, safe arrival (platform force-built every entry),
// return, death, disconnect-mid-transfer, and missing/unloaded destination.
// Player-facing strings never contain the prohibited substring "hive" (EG-P00-S02-C0003).
//
// Wrapped in an IIFE (pack pattern, see spawn_hub_hostile_protection.js) so its
// constants do not collide with other server scripts' global scope.
(() => {
    const HIVE = 'infinite_domain:hive_world'
    const ARRIVAL = { x: 8, y: 64, z: 8, yaw: 0, pitch: 0 }
    const ARRIVAL_FN = 'infinite_domain:hive_world/build_arrival'
    const RETURN_ITEM = 'kubejs:cinderstack_return_marker'
    const FALLBACK_DIM = 'minecraft:overworld'
    const CORE = 'kubejs:cinderstack_portal_core'
    const FRAME = 'kubejs:cinderstack_portal_frame'
    const ACTUATOR = 'kubejs:cinderstack_portal_actuator'
    const FIELD = 'kubejs:cinderstack_portal_field'

    const PD = {
        active: 'id_cinderstack_active',
        pending: 'id_cinderstack_pending',
        odim: 'id_cinderstack_origin_dim',
        ox: 'id_cinderstack_origin_x',
        oy: 'id_cinderstack_origin_y',
        oz: 'id_cinderstack_origin_z',
        oyaw: 'id_cinderstack_origin_yaw',
        opitch: 'id_cinderstack_origin_pitch',
    }

    function dimId(entity) {
        return entity.level.dimension.location().toString()
    }

    function charles(player, message) {
        player.tell('§8[Charles] §7' + message)
    }

    function blockAt(level, core, across, up, xPlane) {
        const x = core.x + (xPlane ? across : 0)
        const z = core.z + (xPlane ? 0 : across)
        return level.getBlock(x, core.y + up, z).id
    }

    function isPortalInterior(id) {
        return id === FIELD || id === 'minecraft:air' || id === 'minecraft:cave_air' || id === 'minecraft:void_air'
    }

    function findBottomCorner(level, core, xPlane, direction) {
        for (let distance = 1; distance <= 22; distance++) {
            const id = blockAt(level, core, direction * distance, 0, xPlane)
            if (id === ACTUATOR) return direction * distance
            if (id !== FRAME) return null
        }
        return null
    }

    function portalGeometry(level, core, xPlane) {
        const left = findBottomCorner(level, core, xPlane, -1)
        const right = findBottomCorner(level, core, xPlane, 1)
        if (left === null || right === null) return null

        const width = right - left + 1
        if (width < 4 || width > 23) return null

        let height = 0
        for (let up = 1; up <= 22; up++) {
            const leftId = blockAt(level, core, left, up, xPlane)
            const rightId = blockAt(level, core, right, up, xPlane)
            if (leftId === ACTUATOR && rightId === ACTUATOR) {
                height = up + 1
                break
            }
            if (leftId !== FRAME || rightId !== FRAME) return null
        }
        if (height < 5 || height > 23) return null

        const top = height - 1
        for (let across = left + 1; across < right; across++) {
            if (blockAt(level, core, across, 0, xPlane) !== (across === 0 ? CORE : FRAME)) return null
            if (blockAt(level, core, across, top, xPlane) !== FRAME) return null
        }
        for (let up = 1; up < top; up++) {
            for (let across = left + 1; across < right; across++) {
                if (!isPortalInterior(blockAt(level, core, across, up, xPlane))) return false
            }
        }
        return { xPlane: xPlane, left: left, right: right, height: height }
    }

    function findPortal(level, core) {
        return portalGeometry(level, core, true) || portalGeometry(level, core, false)
    }

    function energizePortal(player, core, portal) {
        const x1 = core.x + (portal.xPlane ? portal.left + 1 : 0)
        const x2 = core.x + (portal.xPlane ? portal.right - 1 : 0)
        const z1 = core.z + (portal.xPlane ? 0 : portal.left + 1)
        const z2 = core.z + (portal.xPlane ? 0 : portal.right - 1)
        player.server.runCommandSilent('execute in ' + dimId(player) + ' run fill ' +
            x1 + ' ' + (core.y + 1) + ' ' + z1 + ' ' +
            x2 + ' ' + (core.y + portal.height - 2) + ' ' + z2 + ' ' + FIELD)
    }

    function captureOrigin(player) {
        const d = player.persistentData
        d[PD.odim] = dimId(player)
        d[PD.ox] = player.x
        d[PD.oy] = player.y
        d[PD.oz] = player.z
        d[PD.oyaw] = player.yaw || 0
        d[PD.opitch] = player.pitch || 0
    }

    function clearExpedition(player) {
        const d = player.persistentData
        d[PD.active] = false
        d[PD.pending] = false
        player.server.runCommandSilent('clear ' + player.username + ' ' + RETURN_ITEM)
    }

    function giveReturnMarker(player) {
        player.give(Item.of(RETURN_ITEM))
    }

    // ---- entry --------------------------------------------------------------

    function descend(player) {
        const d = player.persistentData
        if (dimId(player) === HIVE) {
            charles(player, 'You are already inside the Cinderstack. Use the return marker to leave.')
            return
        }
        // stale record from a previous run while standing back at an origin - discard it
        if (d[PD.active]) clearExpedition(player)

        captureOrigin(player)
        d[PD.pending] = true

        const name = player.username
        const s = player.server
        s.runCommandSilent('execute in ' + HIVE + ' run forceload add 8 8')
        s.runCommandSilent('execute in ' + HIVE + ' run function ' + ARRIVAL_FN)
        s.runCommandSilent('execute as ' + name + ' in ' + HIVE + ' run tp ' + name +
            ' ' + ARRIVAL.x + ' ' + ARRIVAL.y + ' ' + ARRIVAL.z + ' ' + ARRIVAL.yaw + ' ' + ARRIVAL.pitch)

        if (dimId(player) === HIVE) {
            d[PD.active] = true
            d[PD.pending] = false
            giveReturnMarker(player)
            s.runCommandSilent('advancement grant ' + name + ' only infinite_domain:hive_world/reach_cinderstack')
            s.runCommandSilent('execute in ' + HIVE + ' run forceload remove 8 8')
            charles(player, 'Transfer complete. Your departure point is recorded. The return marker is in your inventory; the lodestone on the deck does the same job.')
        } else {
            d[PD.pending] = false
            s.runCommandSilent('execute in ' + HIVE + ' run forceload remove 8 8')
            charles(player, 'Transfer failed. You have not moved and nothing was recorded. Try again.')
        }
    }

    // ---- return -----------------------------------------------------------

    function ascend(player) {
        const d = player.persistentData
        if (!d[PD.active]) {
            charles(player, 'No active expedition is on record for you.')
            return
        }
        const name = player.username
        const s = player.server
        const dim = d[PD.odim] || FALLBACK_DIM
        const x = d[PD.ox]
        const y = d[PD.oy]
        const z = d[PD.oz]
        const yaw = d[PD.oyaw] || 0
        const pitch = d[PD.opitch] || 0

        s.runCommandSilent('execute as ' + name + ' in ' + dim + ' run tp ' + name +
            ' ' + x + ' ' + y + ' ' + z + ' ' + yaw + ' ' + pitch)

        if (dimId(player) === dim) {
            clearExpedition(player)
            charles(player, 'Returned to your recorded departure point.')
            return
        }
        // origin dimension refused (removed, renamed, unloaded) - guaranteed safe fallback
        s.runCommandSilent('execute as ' + name + ' in ' + FALLBACK_DIM + ' run tp ' + name + ' ' + Math.round(x) + ' 320 ' + Math.round(z))
        s.runCommandSilent('effect give ' + name + ' minecraft:slow_falling 15 0 true')
        s.runCommandSilent('effect give ' + name + ' minecraft:resistance 15 4 true')
        clearExpedition(player)
        charles(player, 'Your departure point could not be restored. You have been dropped over the surface at the recorded coordinates instead.')
    }

    // ---- triggers -------------------------------------------------------

    BlockEvents.rightClicked(CORE, event => {
        const player = event.player
        if (!player || event.level.isClientSide()) return
        const held = event.item ? event.item.id : ''
        if (held !== 'kubejs:cinderstack_marker' && held !== RETURN_ITEM) return
        event.cancel()
        const portal = findPortal(event.level, event.block)
        if (!portal) {
            charles(player, 'Incomplete portal: build a vertical Nether-sized frame (4 x 5 through 23 x 23), place Actuators at all four corners, and put the Portal Core on the lower edge.')
            return
        }
        energizePortal(player, event.block, portal)
        if (held === RETURN_ITEM) ascend(player)
        else descend(player)
    })

    // ---- recovery ------------------------------------------------------

    EntityEvents.death('minecraft:player', event => {
        const player = event.entity
        const d = player.persistentData
        if (!d[PD.active] && !d[PD.pending]) return
        // Dying cancels the transaction. bed_works and natural are false in the Cinderstack,
        // so vanilla respawn already returns the player to their normal spawn.
        clearExpedition(player)
        charles(player, 'Expedition record cleared on death. Recover your gear from the deck if you can get back to it.')
    })

    PlayerEvents.loggedIn(event => {
        const player = event.player
        const d = player.persistentData
        const here = dimId(player)

        if (d[PD.pending]) {
            d[PD.pending] = false
            if (here === HIVE && !d[PD.active]) {
                d[PD.active] = true
                giveReturnMarker(player)
                charles(player, 'Reconnected mid-transfer. The expedition is finalized and a return marker has been issued.')
            } else if (here !== HIVE) {
                charles(player, 'A transfer was interrupted while you were offline. You are back at your origin and nothing was recorded.')
            }
        }

        if (d[PD.active] && here !== HIVE) {
            const origin = d[PD.odim] || FALLBACK_DIM
            if (here === origin) {
                clearExpedition(player)
            } else {
                charles(player, 'You are outside the Cinderstack with an open expedition record. The return marker still points to your departure point.')
            }
        }
    })

    ServerEvents.recipes(event => {
        event.shaped('12x kubejs:cinderstack_portal_frame', ['BOB', 'ENE', 'BOB'], {
            B: 'allthecompressed:blackstone_2x',
            O: 'allthecompressed:obsidian_2x',
            E: 'allthecompressed:end_stone_2x',
            N: 'allthecompressed:netherite_block_2x',
        }).id('infinite_domain:cinderstack/portal_frame')

        event.shaped('4x kubejs:cinderstack_portal_actuator', ['OEO', 'DQD', 'OEO'], {
            O: 'allthecompressed:obsidian_2x',
            E: 'allthecompressed:ender_pearl_block_2x',
            D: 'allthecompressed:diamond_block_2x',
            Q: 'ae2:quantum_entangled_singularity',
        }).id('infinite_domain:cinderstack/portal_actuator')

        event.shaped('kubejs:cinderstack_portal_core', ['NQN', 'EIE', 'NSN'], {
            N: 'allthecompressed:netherite_block_2x',
            Q: 'ae2:quantum_entangled_singularity',
            E: 'allthecompressed:ender_pearl_block_2x',
            I: 'kubejs:infinite_domain_core',
            S: 'allthecompressed:nether_star_block_2x',
        }).id('infinite_domain:cinderstack/portal_core')

        event.shaped('kubejs:cinderstack_marker', ['CEC', 'LNL', 'CEC'], {
            C: 'minecraft:crying_obsidian',
            E: 'minecraft:echo_shard',
            L: 'minecraft:lodestone',
            N: 'minecraft:nether_star',
        }).id('infinite_domain:cinderstack/descent_marker')

        event.shaped('kubejs:cinderstack_return_marker', [' E ', 'CLC', ' R '], {
            C: 'minecraft:crying_obsidian',
            E: 'minecraft:echo_shard',
            L: 'minecraft:lodestone',
            R: 'minecraft:recovery_compass',
        }).id('infinite_domain:cinderstack/return_marker')
    })
})()
