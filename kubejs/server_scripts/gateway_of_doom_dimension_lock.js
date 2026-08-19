// Gateway encounters belong in ordinary Cyberspace only. Passive scheduling is
// separately restricted in config/gateway_of_doom.json; this guard also blocks
// players from manually activating any Devil Eye in every other dimension.
const GatewayDevilEyes = [
    'gateway_of_doom:devil_eye',
    'gateway_of_doom:devil_eye_blue',
    'gateway_of_doom:devil_eye_red',
    'gateway_of_doom:devil_eye_violet'
]

function gatewayDimensionName(dimension) {
    const knownDimensions = {
        'minecraft:overworld': 'the Overworld',
        'minecraft:the_nether': 'the Nether',
        'minecraft:the_end': 'the End',
        'cyberspace:darknet_dimension': 'the Darknet',
        'cyberspace:cyberspace_dimension': 'Cyberspace'
    }
    if (knownDimensions[dimension]) return knownDimensions[dimension]
    return dimension.split(':').pop().replaceAll('_', ' ')
}

const GatewayDeniedMessages = [
    place => '\u00a7cThis is only usable in Cyberspace. \u00a77You are currently in ' + place + '. Do try to operate the reality-breaching artifact in the reality it was designed to breach.',
    place => '\u00a7cThis is only usable in Cyberspace. \u00a77You are currently in ' + place + '. No carrier, no gateway. Even you should be able to appreciate the elegance of that arrangement.',
    place => '\u00a7cThis is only usable in Cyberspace. \u00a77You are currently in ' + place + '. The Eye has found no network, only your increasingly questionable judgment.',
    place => '\u00a7cThis is only usable in Cyberspace. \u00a77You are currently in ' + place + '. Enter the network first; then you may antagonize whatever is waiting there.',
    place => '\u00a7cThis is only usable in Cyberspace. \u00a77You are currently in ' + place + ', which remains stubbornly incompatible despite your clicking.',
    place => '\u00a7cThis is only usable in Cyberspace. \u00a77You are currently in ' + place + '. Similar levels of danger do not make two dimensions interchangeable.',
    place => '\u00a7cThis is only usable in Cyberspace. \u00a77You have brought a network key into ' + place + '. A bold new category of mistake.',
    place => '\u00a7cThis is only usable in Cyberspace. \u00a77You are currently in ' + place + '. Please find a valid carrier before waving the Eye about like an occult paperweight.'
]

function showGatewayRejection(event, place) {
    const playerName = event.player.getGameProfile().getName()
    event.server.runCommandSilent('title ' + playerName + ' times 10 1500 20')
    event.server.runCommandSilent('title ' + playerName + ' title {"text":"Only usable in Cyberspace","color":"red","bold":true}')
    event.server.runCommandSilent('title ' + playerName + ' subtitle {"text":"You are currently in ' + place + '. - Charles","color":"gray"}')
}

GatewayDevilEyes.forEach(eyeId => {
    ItemEvents.rightClicked(eyeId, event => {
        const dimension = event.level.dimension().location().toString()
        if (dimension === 'cyberspace:cyberspace_dimension') return

        event.cancel()
        const response = GatewayDeniedMessages[Math.floor(Math.random() * GatewayDeniedMessages.length)]
        const place = gatewayDimensionName(dimension)
        event.player.tell(response(place))
        showGatewayRejection(event, place)
    })
})
