// Endgame EG-P05 - Cinderstack atmosphere: exposure, PPE, filters, shelter, HUD.
//
// Promoted from the EG-P01-S03-C0018 prototype. Still a data-only spike stand-in for
// the companion module's atmosphere service (C0002: "Phase 1 data-only; critical logic
// in companion module"). Honours the C0007 exposure-model shape: per-band rate, PPE
// reduction, sealed-volume gate, clean-air recovery, non-trivialisation.
// Tuned values: docs/endgame/contracts/environment-implementation.md.
//
// Player-facing strings never contain the prohibited substring "hive".
// Wrapped in an IIFE (KubeJS server scripts share one global scope).
(() => {
    const DIM = 'infinite_domain:hive_world'
    const MASK = 'kubejs:cinderstack_mask'
    const FILTER = 'kubejs:cinderstack_filter'
    const ACID = 'the_wasteland_reworked:acid'

    const PD = {
        exp: 'id_cinderstack_exposure',
        wear: 'id_cinderstack_filter_wear',
        warned: 'id_cinderstack_air_warned',
        bar: 'id_cinderstack_bar_ready',
    }
    const MAX = 100
    const WARN_AT = 40
    const HURT_AT = 65
    const CRIT_AT = 90
    const RECOVER_PER_SEC = 9
    const WEAR_PER_CARTRIDGE = 26
    const SCAN_R = 6

    function inHive(entity) {
        return entity.level.dimension.location().toString() === DIM
    }

    function barId(player) {
        return 'infinite_domain:air_' + player.username.toLowerCase()
    }

    // C0069 base_band_rate by Y band (spatial-metrics.md bands)
    function bandRate(y) {
        if (y < 0) return 4.0     // The Drown / planetary crust
        if (y < 96) return 2.6    // The Underworks
        if (y < 208) return 1.9   // The Furnace Tiers
        if (y < 352) return 1.5   // The Billet Decks
        if (y < 480) return 1.2   // The Vaulting
        return 1.0                // The Crown
    }

    function findItem(player, id) {
        const inv = player.inventory
        const n = inv.size ? inv.size : 41
        for (let i = 0; i < n; i++) {
            const s = inv.getStackInSlot(i)
            if (s && !s.isEmpty() && s.id === id) return i
        }
        return -1
    }

    // One scan pass: a lodestone in range is a clean-air waystation (spike C0073);
    // acid in range is a fume zone (C0074 -> exposure event multiplier).
    function scanEnvironment(player) {
        const bx = Math.floor(player.x)
        const by = Math.floor(player.y)
        const bz = Math.floor(player.z)
        const lvl = player.level
        let waystation = false
        let fume = false
        for (let dx = -SCAN_R; dx <= SCAN_R; dx++) {
            for (let dz = -SCAN_R; dz <= SCAN_R; dz++) {
                if (dx * dx + dz * dz > SCAN_R * SCAN_R) continue
                for (let dy = -3; dy <= 3; dy++) {
                    const id = lvl.getBlock(bx + dx, by + dy, bz + dz).id
                    if (id === 'minecraft:lodestone') waystation = true
                    else if (id === ACID) fume = true
                }
            }
        }
        return { waystation: waystation, fume: fume }
    }

    function ensureBar(player) {
        const id = barId(player)
        const name = player.username
        const s = player.server
        s.runCommandSilent('bossbar add ' + id + ' {"text":"Atmosphere exposure"}')
        s.runCommandSilent('bossbar set ' + id + ' max 100')
        s.runCommandSilent('bossbar set ' + id + ' players ' + name)
        player.persistentData[PD.bar] = true
    }

    function hideBar(player) {
        player.server.runCommandSilent('bossbar set ' + barId(player) + ' players')
    }

    function updateBar(player, exposure, protectedNow) {
        const id = barId(player)
        const s = player.server
        const colour = exposure >= HURT_AT ? 'red' : exposure >= WARN_AT ? 'yellow' : 'green'
        s.runCommandSilent('bossbar set ' + id + ' value ' + Math.round(exposure))
        s.runCommandSilent('bossbar set ' + id + ' color ' + colour)
        s.runCommandSilent('bossbar set ' + id + ' name {"text":"' +
            (protectedNow ? 'Filtered air ' : 'Atmosphere ') + Math.round(exposure) + '%"}')
        s.runCommandSilent('bossbar set ' + id + ' visible ' + (exposure > 0 ? 'true' : 'false'))
    }

    PlayerEvents.tick(event => {
        const player = event.player
        if (!player || player.age % 20 !== 0 || event.level.isClientSide()) return
        if (!inHive(player)) return

        const d = player.persistentData
        if (player.isCreative() || player.isSpectator()) {
            if (d[PD.exp]) { d[PD.exp] = 0; hideBar(player) }
            return
        }
        if (!d[PD.bar]) ensureBar(player)

        let exposure = d[PD.exp] || 0
        const env = scanEnvironment(player)

        if (env.waystation) {
            exposure = Math.max(0, exposure - RECOVER_PER_SEC)
            d[PD.exp] = exposure
            d[PD.warned] = false
            updateBar(player, exposure, true)
            if (exposure === 0) hideBar(player)
            return
        }

        const maskSlot = findItem(player, MASK)
        const hasMask = maskSlot !== -1
        const hasFilter = hasMask && findItem(player, FILTER) !== -1
        const reduction = hasFilter ? 0.84 : hasMask ? 0.35 : 0.0
        const rate = bandRate(player.y) * (env.fume ? 1.5 : 1.0)
        const gain = rate * (1 - reduction)

        exposure = Math.min(MAX, exposure + gain)
        d[PD.exp] = exposure

        // filter + mask wear (only while actually filtering)
        if (hasFilter) {
            let wear = (d[PD.wear] || 0) + gain + rate * 0.1
            if (wear >= WEAR_PER_CARTRIDGE) {
                wear -= WEAR_PER_CARTRIDGE
                player.inventory.getStackInSlot(findItem(player, FILTER)).count--
                const last = findItem(player, FILTER) === -1
                player.tell('§8[Charles] §7Filter cartridge spent.' + (last ? ' §cThat was the last one.' : ''))
            }
            d[PD.wear] = wear
            const ms = player.inventory.getStackInSlot(maskSlot)
            if (ms && ms.id === MASK) {
                if (ms.damageValue + 1 >= ms.maxDamage) {
                    ms.count--
                    player.server.runCommandSilent('playsound minecraft:entity.item.break player ' + player.username)
                    player.tell('§8[Charles] §7The respirator seal has failed. Replace it.')
                } else {
                    ms.damageValue = ms.damageValue + 1
                }
            }
        }

        const name = player.username
        if (exposure >= CRIT_AT) {
            player.server.runCommandSilent('effect give ' + name + ' minecraft:nausea 4 0 true')
            player.server.runCommandSilent('effect give ' + name + ' minecraft:darkness 4 0 true')
            player.server.runCommandSilent('effect give ' + name + ' minecraft:slowness 4 1 true')
            player.server.runCommandSilent('damage ' + name + ' ' + (exposure >= MAX ? 4 : 2) + ' minecraft:magic')
        } else if (exposure >= HURT_AT) {
            player.server.runCommandSilent('effect give ' + name + ' minecraft:nausea 4 0 true')
            player.server.runCommandSilent('effect give ' + name + ' minecraft:weakness 4 0 true')
            if (!d[PD.warned]) {
                d[PD.warned] = true
                player.tell('§8[Charles] §7The air is not survivable unfiltered for long. Reach a waystation - a lodestone marks clean air - or seal a fresh cartridge.')
            }
        }
        updateBar(player, exposure, hasFilter)
    })

    // dimension leave: fast decay + hide the bar
    PlayerEvents.tick(event => {
        const player = event.player
        if (!player || player.age % 40 !== 0 || event.level.isClientSide()) return
        if (inHive(player)) return
        const d = player.persistentData
        if ((d[PD.exp] || 0) > 0) {
            d[PD.exp] = Math.max(0, d[PD.exp] - 25)
            if (d[PD.exp] === 0) { d[PD.wear] = 0; d[PD.warned] = false }
        }
        if (d[PD.bar]) { hideBar(player); d[PD.bar] = false }
    })

    EntityEvents.death('minecraft:player', event => {
        const player = event.entity
        const d = player.persistentData
        d[PD.exp] = 0
        d[PD.wear] = 0
        d[PD.warned] = false
        if (d[PD.bar]) { hideBar(player); d[PD.bar] = false }
    })

    PlayerEvents.loggedIn(event => {
        const player = event.player
        player.persistentData[PD.bar] = false
        if (!inHive(player)) hideBar(player)
    })

    ServerEvents.recipes(event => {
        event.shaped('kubejs:cinderstack_mask', ['GLG', 'IPI', ' L '], {
            G: 'minecraft:glass_pane', L: 'minecraft:leather',
            I: 'minecraft:iron_ingot', P: 'minecraft:paper',
        }).id('infinite_domain:cinderstack/mask')
        event.shapeless('2x kubejs:cinderstack_filter', [
            'minecraft:paper', 'minecraft:paper',
            'minecraft:charcoal', 'minecraft:charcoal', 'minecraft:iron_nugget',
        ]).id('infinite_domain:cinderstack/filter')
    })
})()
