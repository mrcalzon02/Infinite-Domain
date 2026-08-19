// Turn AE2's real powered Spatial Anchor into a player-bound Darknet tether.
// AE2 owns the chunk ticket; this script only holds and releases the timer.
const DarknetAnchorVariables = Java.loadClass('cyberspace.network.CyberspaceModVariables')
const SpatialAnchorBlockEntity = Java.loadClass('appeng.blockentity.spatial.SpatialAnchorBlockEntity')
const DarknetAnchorBlockPos = Java.loadClass('net.minecraft.core.BlockPos')

const DarknetAnchorDimension = 'cyberspace:darknet_dimension'
const DarknetAnchorData = {
    bound: 'infinite_domain_darknet_anchor_bound',
    x: 'infinite_domain_darknet_anchor_x',
    y: 'infinite_domain_darknet_anchor_y',
    z: 'infinite_domain_darknet_anchor_z',
    grace: 'infinite_domain_darknet_anchor_grace_until'
}

function playerDarknetAnchorMatches(player, block) {
    const data = player.persistentData
    return data[DarknetAnchorData.bound]
        && data[DarknetAnchorData.x] === block.x
        && data[DarknetAnchorData.y] === block.y
        && data[DarknetAnchorData.z] === block.z
}

function clearPlayerDarknetAnchor(player, recall) {
    const data = player.persistentData
    data[DarknetAnchorData.bound] = false
    data[DarknetAnchorData.grace] = 0
    if (recall && player.level.dimension().location().toString() === DarknetAnchorDimension) {
        const variables = player.getData(DarknetAnchorVariables.PLAYER_VARIABLES)
        variables.DarknetTimer = 0
        variables.markSyncDirty()
        player.tell('\u00a7cDarknet Anchor link terminated. \u00a77Returning you to the recorded Overworld position. Try not to look surprised; you unplugged it. - Charles')
    }
}

BlockEvents.placed('ae2:spatial_anchor', event => {
    const player = event.player
    if (!player) return

    const dimension = event.level.dimension().location().toString()
    if (dimension !== DarknetAnchorDimension) {
        event.cancel()
        player.tell('\u00a7cThe Darknet Anchor is only placeable in the Darknet. \u00a77Chunk-loading the Overworld was not the assignment. - Charles')
        return
    }

    const data = player.persistentData
    if (data[DarknetAnchorData.bound]) {
        event.cancel()
        player.tell('\u00a7cYou may bind only one Darknet Anchor. \u00a77Maintaining one impossible connection is quite enough for you. - Charles')
        return
    }

    data[DarknetAnchorData.bound] = true
    data[DarknetAnchorData.x] = event.block.x
    data[DarknetAnchorData.y] = event.block.y
    data[DarknetAnchorData.z] = event.block.z
    data[DarknetAnchorData.grace] = player.age + 200
    player.tell('\u00a74Darknet Anchor bound. \u00a77Connect it to a powered ME network before your current session expires. - Charles')
})

BlockEvents.blockEntityTick('ae2:spatial_anchor', event => {
    if (event.tick % 20 !== 0) return
    if (event.level.dimension().location().toString() !== DarknetAnchorDimension) return

    const blockEntity = event.block.entity
    const online = blockEntity instanceof SpatialAnchorBlockEntity && blockEntity.isActive()
    event.server.players.forEach(player => {
        if (!playerDarknetAnchorMatches(player, event.block)) return
        if (!online) {
            if (player.age < player.persistentData[DarknetAnchorData.grace]) return
            clearPlayerDarknetAnchor(player, true)
            return
        }
        player.persistentData[DarknetAnchorData.grace] = 0
        if (player.level.dimension().location().toString() !== DarknetAnchorDimension) return

        const variables = player.getData(DarknetAnchorVariables.PLAYER_VARIABLES)
        if (variables.DarknetInternalTimer > 0 && variables.DarknetTimer > 0 && variables.DarknetTimer < 20) {
            variables.DarknetTimer = 20
            variables.markSyncDirty()
        }
    })
})

BlockEvents.broken('ae2:spatial_anchor', event => {
    event.server.players.forEach(player => {
        if (playerDarknetAnchorMatches(player, event.block)) clearPlayerDarknetAnchor(player, true)
    })
})

// Catch anchors removed while their owner was offline and any lost AE2 chunk
// ticket. An active Spatial Anchor keeps its own position loaded, so an
// unloaded registered position is itself evidence that the tether has failed.
PlayerEvents.loggedIn(event => {
    if (event.player.persistentData[DarknetAnchorData.bound]) {
        event.player.persistentData[DarknetAnchorData.grace] = event.player.age + 200
    }
})

PlayerEvents.tick(event => {
    const player = event.player
    if (player.age % 20 !== 0) return
    const data = player.persistentData
    if (!data[DarknetAnchorData.bound]) return
    if (player.level.dimension().location().toString() !== DarknetAnchorDimension) return
    if (player.age < data[DarknetAnchorData.grace]) return

    const pos = new DarknetAnchorBlockPos(data[DarknetAnchorData.x], data[DarknetAnchorData.y], data[DarknetAnchorData.z])
    if (!player.level.hasChunkAt(pos)
        || player.level.getBlock(data[DarknetAnchorData.x], data[DarknetAnchorData.y], data[DarknetAnchorData.z]).id !== 'ae2:spatial_anchor') {
        clearPlayerDarknetAnchor(player, true)
    }
})

EntityEvents.death('minecraft:player', event => {
    const player = event.entity
    const data = player.persistentData
    if (!data[DarknetAnchorData.bound]) return

    if (player.level.dimension().location().toString() === DarknetAnchorDimension) {
        const block = player.level.getBlock(data[DarknetAnchorData.x], data[DarknetAnchorData.y], data[DarknetAnchorData.z])
        if (block.id === 'ae2:spatial_anchor') block.set('minecraft:air')
    }
    clearPlayerDarknetAnchor(player, false)
})
