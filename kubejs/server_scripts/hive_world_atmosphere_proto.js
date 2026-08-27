// Endgame EG-P01-S03-C0018 - dimension-scoped air-hazard prototype for the Cinderstack.
//
// DISPOSABLE PHASE 1 SPIKE. A data-only stand-in for the companion module's
// atmosphere service (C0002: "Phase 1 data-only; critical logic in companion module").
// Honours the C0007 exposure-model shape: a per-band rate, a PPE reduction, a
// sealed-volume gate, and recovery only in clean air. Values here are placeholders;
// tuning is EG-P05-S01-C0069.
//
// Player-facing strings never contain the prohibited substring "hive".

const HIVE = 'infinite_domain:hive_world'
const FILTER = 'kubejs:cinderstack_filter'

// arrival deck lodestone at (8,64,8) counts as the one powered safe volume in the spike
const SAFE = { x: 8, y: 64, z: 8, r2: 100 }

const EXPOSURE = 'id_cinderstack_exposure'
const FILTER_WEAR = 'id_cinderstack_filter_wear'
const WARNED = 'id_cinderstack_air_warned'

const MAX_EXPOSURE = 100
const WARN_AT = 55
const HURT_AT = 85
const FILTER_REDUCTION = 0.2      // mask + working filter -> 20% of the open-air rate
const FILTER_WEAR_PER_CARTRIDGE = 40
const RECOVERY_PER_SEC = 6

function dimId(entity) {
    return entity.level.dimension().location().toString()
}

function bandRate(y) {
    if (y < 0) return 4.0        // The Drown
    if (y < 48) return 2.5      // The Underworks
    return 1.5                  // Furnace Tiers and above
}

function findFilterSlot(player) {
    const inv = player.inventory
    const size = inv.size ? inv.size : 41
    for (let i = 0; i < size; i++) {
        const st = inv.getStackInSlot(i)
        if (st && !st.isEmpty() && st.id === FILTER) return i
    }
    return -1
}

function actionbar(player, text, color) {
    player.server.runCommandSilent(
        'title ' + player.username + ' actionbar {"text":"' + text + '","color":"' + color + '"}')
}

PlayerEvents.tick(event => {
    const player = event.player
    if (!player || player.age % 20 !== 0) return
    if (event.level.isClientSide()) return
    if (dimId(player) !== HIVE) return

    const d = player.persistentData
    if (player.isCreative() || player.isSpectator()) {
        d[EXPOSURE] = 0
        return
    }

    let exposure = d[EXPOSURE] || 0
    const dx = player.x - SAFE.x
    const dy = player.y - SAFE.y
    const dz = player.z - SAFE.z
    const inSafeVolume = (dx * dx + dy * dy + dz * dz) <= SAFE.r2

    if (inSafeVolume) {
        exposure = Math.max(0, exposure - RECOVERY_PER_SEC)
        d[EXPOSURE] = exposure
        d[WARNED] = false
        if (exposure > 0) actionbar(player, 'Filtered air - venting exposure ' + Math.round(exposure), 'aqua')
        return
    }

    const filterSlot = findFilterSlot(player)
    const protectedNow = filterSlot !== -1
    const rate = bandRate(player.y)
    const gain = rate * (protectedNow ? FILTER_REDUCTION : 1.0)

    exposure = Math.min(MAX_EXPOSURE, exposure + gain)
    d[EXPOSURE] = exposure

    if (protectedNow) {
        let wear = (d[FILTER_WEAR] || 0) + gain + rate * 0.15
        if (wear >= FILTER_WEAR_PER_CARTRIDGE) {
            wear -= FILTER_WEAR_PER_CARTRIDGE
            const st = player.inventory.getStackInSlot(filterSlot)
            st.setCount(st.getCount() - 1)
            const left = findFilterSlot(player) === -1 ? 0 : 1
            player.tell('§8[Charles] §7A filter cartridge is spent.' +
                (left ? '' : ' §cThat was your last one.'))
        }
        d[FILTER_WEAR] = wear
    }

    const name = player.username
    if (exposure >= HURT_AT) {
        player.server.runCommandSilent('effect give ' + name + ' minecraft:nausea 4 0 true')
        player.server.runCommandSilent('effect give ' + name + ' minecraft:darkness 4 0 true')
        player.server.runCommandSilent('damage ' + name + ' 2 minecraft:magic')
        actionbar(player, 'ATMOSPHERE CRITICAL ' + Math.round(exposure), 'red')
    } else if (exposure >= WARN_AT) {
        player.server.runCommandSilent('effect give ' + name + ' minecraft:nausea 4 0 true')
        actionbar(player, 'Atmosphere exposure ' + Math.round(exposure), 'gold')
        if (!d[WARNED]) {
            d[WARNED] = true
            player.tell('§8[Charles] §7The air here is not survivable unfiltered for long. Find clean air or a working cartridge.')
        }
    } else {
        actionbar(player, (protectedNow ? 'Filtered - ' : 'Unfiltered - ') + 'exposure ' + Math.round(exposure),
            protectedNow ? 'yellow' : 'gold')
    }
})

// leaving the dimension clears the meter (spike behaviour; persistence is C0080)
PlayerEvents.tick(event => {
    const player = event.player
    if (!player || player.age % 40 !== 0 || event.level.isClientSide()) return
    if (dimId(player) !== HIVE && (player.persistentData[EXPOSURE] || 0) !== 0) {
        player.persistentData[EXPOSURE] = 0
        player.persistentData[FILTER_WEAR] = 0
        player.persistentData[WARNED] = false
    }
})
