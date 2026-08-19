// Extend Cyberspace 4.1.1's synchronized Darknet timer directly.
const CyberspaceVariables = Java.loadClass('cyberspace.network.CyberspaceModVariables')

const DarknetInjectorSeconds = [30, 60, 120, 240, 480, 960, 1920, 3840]

function injectorDimensionName(dimension) {
    const knownDimensions = {
        'minecraft:overworld': 'the Overworld',
        'minecraft:the_nether': 'the Nether',
        'minecraft:the_end': 'the End',
        'cyberspace:cyberspace_dimension': 'Cyberspace',
        'cyberspace:darknet_dimension': 'the Darknet'
    }
    if (knownDimensions[dimension]) return knownDimensions[dimension]
    return dimension.split(':').pop().replaceAll('_', ' ')
}

const DarknetInjectorWrongDimensionMessages = [
    place => '\u00a7cDarknet Session Injectors are only usable in the Darknet. \u00a77You are currently in ' + place + ', where there is no session to extend.',
    place => '\u00a7cDarknet Session Injectors are only usable in the Darknet. \u00a77You are currently in ' + place + '. You cannot add time to a connection you have not entered.',
    place => '\u00a7cDarknet Session Injectors are only usable in the Darknet. \u00a77You are currently in ' + place + '. The required carrier signal is, rather conspicuously, absent.',
    place => '\u00a7cDarknet Session Injectors are only usable in the Darknet. \u00a77You are currently in ' + place + '. Please establish which reality you occupy before medicating the network.',
    place => '\u00a7cDarknet Session Injectors are only usable in the Darknet. \u00a77You are currently in ' + place + '. That location has no Darknet timer, however impatiently you click.',
    place => '\u00a7cDarknet Session Injectors are only usable in the Darknet. \u00a77You are currently in ' + place + '. Similar hostility does not constitute protocol compatibility.',
    place => '\u00a7cDarknet Session Injectors are only usable in the Darknet. \u00a77You are currently in ' + place + '. Enter through the Terminal first; sequence is not decorative.',
    place => '\u00a7cDarknet Session Injectors are only usable in the Darknet. \u00a77You are currently in ' + place + '. At present you are injecting bandwidth into local scenery.'
]

const DarknetInjectorInactiveSessionMessages = [
    '\u00a7cNo active Darknet session detected. \u00a77Reconnect through the Terminal before using an injector. It extends time; it does not invent it.',
    '\u00a7cNo active Darknet session detected. \u00a77You reached the correct dimension and still neglected the connection. Almost impressive.',
    '\u00a7cNo active Darknet session detected. \u00a77The timer is already dead. Kindly stop trying to resuscitate a number.',
    '\u00a7cNo active Darknet session detected. \u00a77Reconnect through the Terminal, then inject while the carrier is actually running.',
    '\u00a7cNo active Darknet session detected. \u00a77The device extends a live lease. Your present lease is exceptionally, definitively expired.',
    '\u00a7cNo active Darknet session detected. \u00a77There is nothing to reinforce until the Terminal establishes a fresh carrier.',
    '\u00a7cNo active Darknet session detected. \u00a77Correct location, incorrect timing. Progress of a sort, I suppose.',
    '\u00a7cNo active Darknet session detected. \u00a77Save the injector, reconnect, and try again while causality is still accepting applications.'
]

function randomInjectorEntry(messages) {
    return messages[Math.floor(Math.random() * messages.length)]
}

function showInjectorRejection(event, title, subtitle) {
    const playerName = event.player.getGameProfile().getName()
    event.server.runCommandSilent('title ' + playerName + ' times 10 1500 20')
    event.server.runCommandSilent('title ' + playerName + ' title {"text":"' + title + '","color":"red","bold":true}')
    event.server.runCommandSilent('title ' + playerName + ' subtitle {"text":"' + subtitle + ' - Charles","color":"gray"}')
}

DarknetInjectorSeconds.forEach((seconds, index) => {
ItemEvents.rightClicked('kubejs:darknet_session_injector_tier_' + (index + 1), event => {
    const player = event.player
    const dimension = event.level.dimension().location().toString()

    if (dimension !== 'cyberspace:darknet_dimension') {
        const response = randomInjectorEntry(DarknetInjectorWrongDimensionMessages)
        const place = injectorDimensionName(dimension)
        player.tell(response(place))
        showInjectorRejection(event, 'Darknet injectors only', 'You are currently in ' + place + '. Enter the Darknet first.')
        return
    }

    const variables = player.getData(CyberspaceVariables.PLAYER_VARIABLES)
    if (variables.DarknetInternalTimer <= 0 || variables.DarknetTimer <= 0) {
        player.tell(randomInjectorEntry(DarknetInjectorInactiveSessionMessages))
        showInjectorRejection(event, 'No active Darknet session', 'Reconnect through the Terminal before injecting.')
        return
    }

    variables.DarknetTimer = variables.DarknetTimer + seconds
    variables.markSyncDirty()
    event.item.count--
    event.server.runCommandSilent('advancement grant ' + player.getGameProfile().getName() + ' only infinite_domain:darknet_time_extended')
    player.tell('\u00a7dDarknet carrier extended by ' + seconds.toLocaleString() + ' seconds. ' + Math.round(variables.DarknetTimer).toLocaleString() + ' seconds remain.')
})
})
