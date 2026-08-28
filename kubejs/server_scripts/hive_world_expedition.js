// Endgame EG-P01-S04-C0019 - reversible entry/return for infinite_domain:hive_world.
//
// DISPOSABLE PHASE 1 SPIKE. Operator/creative-gated. No recipe, no automation.
// The real constructible access mechanism is Phase 6 EG-P06-S01-C0084; the transactional
// travel service moves to the packdev/hive-world-companion module at Phase 5.
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
        return entity.level.dimension().location().toString()
    }

    function charles(player, message) {
        player.tell('§8[Charles] §7' + message)
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
        if (!player.hasPermissions(2) && !player.isCreative()) {
            charles(player, 'The descent marker is an operator instrument in this build. Access opens for everyone at the constructed gate later.')
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

    ItemEvents.rightClicked('kubejs:cinderstack_marker', event => {
        const player = event.player
        if (!player || event.level.isClientSide()) return
        descend(player)
    })

    ItemEvents.rightClicked(RETURN_ITEM, event => {
        const player = event.player
        if (!player || event.level.isClientSide()) return
        ascend(player)
    })

    BlockEvents.rightClicked('minecraft:lodestone', event => {
        const player = event.player
        if (!player || event.level.isClientSide()) return
        if (event.level.dimension().location().toString() !== HIVE) return
        // let the item handler own the interaction when the return marker is in hand
        if (event.item && event.item.id === RETURN_ITEM) return
        ascend(player)
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
})()
