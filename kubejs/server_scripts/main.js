// Give every player Charles's guide exactly once. Persistent player data keeps
// this safe across reconnects and deaths while also covering existing worlds.
PlayerEvents.loggedIn(event => {
    const key = 'infinite_domain_received_quest_book'
    const obsoleteBookKey = 'infinite_domain_removed_obsolete_momg_book'
    const data = event.player.persistentData
    const username = event.player.username

    // Correct one stale personal spawn after a missing lobby is bootstrapped.
    // Completion is delayed one tick so it wins over starter-world login code.
    event.server.runCommandSilent(`execute if data storage infinite_domain:spawn_hub teleport_next_arrival run tag ${username} add infinite_domain_spawn_arrival`)
    event.server.runCommandSilent('execute if data storage infinite_domain:spawn_hub teleport_next_arrival run schedule function infinite_domain:admin/complete_pending_spawn_arrival 1t replace')

    // MOMG 1.1.9 has no functional book toggle: its login procedure hardcodes
    // the book grant behind an advancement. Remove that obsolete recipe guide
    // once, one tick after the mod has processed the login event.
    if (!data[obsoleteBookKey]) {
        event.server.runCommandSilent(`tag ${username} add infinite_domain_obsolete_book_cleanup`)
        event.server.runCommandSilent('schedule function infinite_domain:admin/remove_obsolete_starting_book 1t replace')
        data[obsoleteBookKey] = true
    }

    // FTB Library's stock stage provider stores stages as player tags. Echoes
    // reads the same provider, so this unlock is shared without a custom bridge.
    event.player.stages.add('infinite_domain:era_0')

    if (!data[key]) {
        event.player.give('ftbquests:book')
        data[key] = true
    }
})
