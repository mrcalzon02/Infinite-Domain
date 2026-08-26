// Establish the protected public arrival hub through FTB Teams + FTB Chunks.
// FTB Chunks' command radius is measured in blocks. A 48-block radius around
// block 0,0 resolves to chunk coordinates -3..3 on both axes: 49 chunks. This
// fully protects the radius-48 blended hospital terrain footprint.
ServerEvents.loaded(event => {
    const server = event.server

    // The dedicated flat QA save owns its spawn area and command-block gallery.
    // Do not place or claim the campaign arrival hospital in that one exact world.
    if (server.getWorldData().getLevelName() === 'Infinite Domain - Structure QA Flatworld') {
        console.info('[Infinite Domain] Structure QA Flatworld detected; campaign spawn hospital and Admin Spawn claims skipped')
        return
    }

    const $FTBTeamsAPI = Java.loadClass('dev.ftb.mods.ftbteams.api.FTBTeamsAPI')
    const $ClaimedChunkManager = Java.loadClass('dev.ftb.mods.ftbchunks.data.ClaimedChunkManagerImpl')
    const $ChunkDimPos = Java.loadClass('dev.ftb.mods.ftblibrary.math.ChunkDimPos')
    const $TeamProperties = Java.loadClass('dev.ftb.mods.ftbteams.api.property.TeamProperties')
    const $FTBChunksProperties = Java.loadClass('dev.ftb.mods.ftbchunks.api.FTBChunksProperties')
    const $PrivacyMode = Java.loadClass('dev.ftb.mods.ftbteams.api.property.PrivacyMode')
    const $Color4I = Java.loadClass('dev.ftb.mods.ftblibrary.icon.Color4I')
    const $Level = Java.loadClass('net.minecraft.world.level.Level')

    // Verify the arrival structure before any player can connect. The function
    // is guarded by a high, structure-specific signature block, so completed
    // lobbies are left untouched.
    server.runCommandSilent('function infinite_domain:admin/bootstrap_spawn_hospital')

    // Reassert the global arrival point on every server load. Do not issue a
    // blanket /spawnpoint command here: existing beds and personal respawn
    // anchors must remain valid after the initial world setup.
    server.runCommandSilent('execute in minecraft:overworld run setworldspawn 0 64 0 0')
    server.runCommandSilent('gamerule spawnRadius 0')

    // FTB's managers finish loading alongside the world. Delay team configuration
    // by one second, then use the installed API for both creation and repair. The
    // 2101 command grammar no longer accepts the former server-team command path.
    // Retry a few times because a brand-new save can finish loading FTB Teams a
    // tick or two before FTB Chunks has made its ownership index writable.
    // getTeamByName keys off FTB Teams' internal normalized short-name, not the
    // literal display string, so it never matches 'Admin Spawn' as created below.
    // That silently failed on every retry and recreated a fresh duplicate server
    // team each time (confirmed: 6 'Created new server team' log lines on one
    // load). Look the team up by the DISPLAY_NAME property we set ourselves
    // instead, since that value is exact and under our control.
    function findAdminSpawnTeam(manager) {
        const teams = manager.getTeams().toArray()
        for (let i = 0; i < teams.length; i++) {
            const candidate = teams[i]
            if (!candidate.isServerTeam()) continue
            const displayName = candidate.getProperty($TeamProperties.DISPLAY_NAME)
            if (displayName !== null && String(displayName) === 'Admin Spawn') {
                return candidate
            }
        }
        return null
    }

    function configureSpawnClaims(attempt) {
        const manager = $FTBTeamsAPI.api().getManager()
        const source = server.createCommandSourceStack()
        let team = manager.getTeamByName('Admin Spawn').orElse(null)
        if (team === null) team = manager.getTeamByName('spawn').orElse(null)
        if (team === null) team = findAdminSpawnTeam(manager)
        if (team === null) {
            try {
                team = manager.createServerTeam(
                    source,
                    'Admin Spawn',
                    'Protected public arrival, rules, quests, and shops',
                    $Color4I.fromString('#D6A84B'),
                    null
                )
            } catch (error) {
                console.error(`[Infinite Domain] Admin Spawn team creation failed: ${error}`)
            }
        }
        if (team === null) {
            console.error('[Infinite Domain] Could not create or find the Admin Spawn server team')
            if (attempt < 5) server.scheduleInTicks(40, () => configureSpawnClaims(attempt + 1))
            return
        }

        // Apply policy through the API as well as commands. This makes the
        // result independent of command parsing and repairs older saves whose
        // team was created with FTB's defaults.
        team.setProperty($TeamProperties.DISPLAY_NAME, 'Admin Spawn')
        team.setProperty($TeamProperties.DESCRIPTION, 'Protected public arrival, rules, quests, and shops')
        team.setProperty($TeamProperties.COLOR, $Color4I.fromString('#D6A84B'))
        team.setProperty($FTBChunksProperties.BLOCK_EDIT_MODE, $PrivacyMode.PRIVATE)
        team.setProperty($FTBChunksProperties.BLOCK_INTERACT_MODE, $PrivacyMode.PRIVATE)
        team.setProperty($FTBChunksProperties.ENTITY_INTERACT_MODE, $PrivacyMode.PRIVATE)
        team.setProperty($FTBChunksProperties.NONLIVING_ENTITY_ATTACK_MODE, $PrivacyMode.PRIVATE)
        team.setProperty($FTBChunksProperties.ALLOW_EXPLOSIONS, false)
        team.setProperty($FTBChunksProperties.ALLOW_MOB_GRIEFING, false)
        team.setProperty($FTBChunksProperties.ALLOW_PVP, false)
        team.setProperty($FTBChunksProperties.CLAIM_VISIBILITY, $PrivacyMode.PUBLIC)
        team.markDirty()

        const claimedChunkManager = $ClaimedChunkManager.getInstance()
        const chunkData = claimedChunkManager.getOrCreateData(team)
        const teamId = team.getId()
        let claimPosition = null
        let existingClaim = null
        let existingTeamId = null
        let verifiedClaims = 0

        // Idempotent fallback and repair path for existing worlds. Rhino treats
        // a loop-local const as a repeated var declaration, so the position is
        // deliberately allocated through one outer binding and reassigned.
        for (let chunkX = -3; chunkX <= 3; chunkX++) {
            for (let chunkZ = -3; chunkZ <= 3; chunkZ++) {
                claimPosition = new $ChunkDimPos($Level.OVERWORLD, chunkX, chunkZ)
                existingClaim = claimedChunkManager.getChunk(claimPosition)

                // The spawn reservation is authoritative. Repair stale personal
                // or abandoned claims left in the protected arrival footprint.
                if (existingClaim !== null) {
                    existingTeamId = existingClaim.getTeamData().getTeam().getId()
                    if (!existingTeamId.equals(teamId)) existingClaim.unclaim(source, true)
                }

                chunkData.claim(source, claimPosition, true)
                existingClaim = claimedChunkManager.getChunk(claimPosition)
                if (existingClaim !== null && existingClaim.getTeamData().getTeam().getId().equals(teamId)) {
                    verifiedClaims++
                }
            }
        }

        chunkData.saveNow()
        chunkData.syncChunksToAll(server)
        if (verifiedClaims === 49) {
            console.info('[Infinite Domain] Spawn hospital verified; Admin Spawn owns all 49 required spawn chunks')
        } else if (attempt < 5) {
            console.warn(`[Infinite Domain] Admin Spawn owns ${verifiedClaims}/49 required spawn chunks; retry ${attempt + 1}/5 scheduled`)
            server.scheduleInTicks(40, () => configureSpawnClaims(attempt + 1))
        } else {
            console.error(`[Infinite Domain] Admin Spawn claim repair stopped after 5 attempts with ${verifiedClaims}/49 chunks verified`)
        }
    }

    server.scheduleInTicks(20, () => configureSpawnClaims(1))
})
