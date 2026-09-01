// Headless, fixed-seed world-generation benchmark controller.
// This script is inert in ordinary worlds. The isolated benchmark launcher
// replaces kubejs/config/worldgen_benchmark.json with an enabled run plan.
// Wrapped because KubeJS evaluates server scripts in one shared Rhino scope.
(() => {
const WorldgenBenchmark = {
    configPath: 'kubejs/config/worldgen_benchmark.json',
    prefix: '[ID-WORLDGEN-BENCH] ',
    active: false
}

function worldgenBenchmarkLog(payload) {
    console.info(WorldgenBenchmark.prefix + JSON.stringify(payload))
}

function worldgenBenchmarkStop(server, delayTicks) {
    server.scheduleInTicks(delayTicks, () => server.runCommandSilent('stop'))
}

function worldgenBenchmarkFail(server, config, code, message, detail) {
    const payload = {
        event: 'benchmark_failed',
        runId: String(config.runId),
        variant: String(config.variant),
        suite: String(config.suite),
        code: String(code),
        message: String(message)
    }
    if (detail !== undefined && detail !== null) payload.detail = String(detail)
    worldgenBenchmarkLog(payload)
    WorldgenBenchmark.active = false
    if (config.stopServerWhenComplete !== false) worldgenBenchmarkStop(server, 20)
}

function worldgenBenchmarkChunkBlock(chunkCoordinate) {
    return Number(chunkCoordinate) * 16
}

function worldgenBenchmarkTileBounds(tile) {
    const boundsMinChunkX = Number(tile.minChunkX)
    const boundsMinChunkZ = Number(tile.minChunkZ)
    const boundsWidth = Number(tile.widthChunks)
    const boundsDepth = Number(tile.depthChunks)
    return {
        minChunkX: boundsMinChunkX,
        minChunkZ: boundsMinChunkZ,
        maxChunkX: boundsMinChunkX + boundsWidth - 1,
        maxChunkZ: boundsMinChunkZ + boundsDepth - 1,
        minBlockX: worldgenBenchmarkChunkBlock(boundsMinChunkX),
        minBlockZ: worldgenBenchmarkChunkBlock(boundsMinChunkZ),
        maxBlockX: worldgenBenchmarkChunkBlock(boundsMinChunkX + boundsWidth) - 1,
        maxBlockZ: worldgenBenchmarkChunkBlock(boundsMinChunkZ + boundsDepth) - 1,
        chunks: boundsWidth * boundsDepth
    }
}

function worldgenBenchmarkForceloadCommand(action, dimension, bounds) {
    return 'execute in ' + dimension + ' run forceload ' + action + ' ' +
        bounds.minBlockX + ' ' + bounds.minBlockZ + ' ' +
        bounds.maxBlockX + ' ' + bounds.maxBlockZ
}

function worldgenBenchmarkAllChunksLoaded(server, dimension, bounds) {
    for (let loadedChunkX = bounds.minChunkX; loadedChunkX <= bounds.maxChunkX; loadedChunkX++) {
        for (let loadedChunkZ = bounds.minChunkZ; loadedChunkZ <= bounds.maxChunkZ; loadedChunkZ++) {
            const loadedBlockX = worldgenBenchmarkChunkBlock(loadedChunkX) + 8
            const loadedBlockZ = worldgenBenchmarkChunkBlock(loadedChunkZ) + 8
            const loadedCommand = 'execute in ' + dimension + ' positioned ' + loadedBlockX + ' 0 ' + loadedBlockZ +
                ' if loaded ~ ~ ~ run function infinite_domain:worldgen_benchmark/probe'
            if (server.runCommandSilent(loadedCommand) <= 0) return false
        }
    }
    return true
}

function worldgenBenchmarkModSnapshot(config) {
    const requested = ['lostcities', 'dungeons_arise', 'dungeons_arise_seven_seas']
    // Rhino re-enters the try block's lexical environment when scheduled server
    // callbacks run, and a `var` hoisted out of that block collides with the
    // binding left by the previous entry ("redeclaration of var"). Declaring at
    // function scope and assigning inside the try avoids the hoist entirely.
    let loaded = {}
    try {
        loaded = {}
        requested.forEach(modId => loaded[modId] = Boolean(Platform.isLoaded(modId)))
        worldgenBenchmarkLog({
            event: 'mod_snapshot',
            runId: String(config.runId),
            loaded: loaded
        })
    } catch (error) {
        worldgenBenchmarkLog({
            event: 'acceptance_probe_error',
            runId: String(config.runId),
            stage: 'mod_snapshot',
            detail: String(error)
        })
    }
}

function worldgenBenchmarkRegistrySnapshot(server, config) {
    const namespaces = ['dungeons_arise', 'dungeons_arise_seven_seas']
    // Declared at function scope; see worldgenBenchmarkModSnapshot for why.
    let snapshotRegistryKeys, snapshotAccess, snapshotStructureRegistry, snapshotStructureSetRegistry
    try {
        snapshotRegistryKeys = Java.loadClass('net.minecraft.core.registries.Registries')
        snapshotAccess = server.registryAccess()
        snapshotStructureRegistry = snapshotAccess.registryOrThrow(snapshotRegistryKeys.STRUCTURE)
        snapshotStructureSetRegistry = snapshotAccess.registryOrThrow(snapshotRegistryKeys.STRUCTURE_SET)

        namespaces.forEach(namespace => {
            const structures = []
            const structureSets = []
            snapshotStructureRegistry.keySet().forEach(key => {
                const snapshotStructureText = String(key)
                if (snapshotStructureText.startsWith(namespace + ':')) structures.push(snapshotStructureText)
            })
            snapshotStructureSetRegistry.keySet().forEach(key => {
                const snapshotSetText = String(key)
                if (snapshotSetText.startsWith(namespace + ':')) structureSets.push(snapshotSetText)
            })
            structures.sort()
            structureSets.sort()
            worldgenBenchmarkLog({
                event: 'registry_namespace_snapshot',
                runId: String(config.runId),
                namespace: namespace,
                structureCount: structures.length,
                structureSetCount: structureSets.length,
                structureSample: structures.slice(0, 12),
                structureSetSample: structureSets.slice(0, 12)
            })
        })
    } catch (error) {
        worldgenBenchmarkLog({
            event: 'acceptance_probe_error',
            runId: String(config.runId),
            stage: 'registry_snapshot',
            detail: String(error)
        })
    }
}

function worldgenBenchmarkStructureStarts(server, dimension, bounds) {
    const counts = {}
    let validStarts = 0
    // Declared at function scope; see worldgenBenchmarkModSnapshot for why.
    let startRegistryKeys, startResourceKey, startResourceLocation
    let startDimensionLocation, startDimensionKey, startLevel, startStructureRegistry
    try {
        startRegistryKeys = Java.loadClass('net.minecraft.core.registries.Registries')
        startResourceKey = Java.loadClass('net.minecraft.resources.ResourceKey')
        startResourceLocation = Java.loadClass('net.minecraft.resources.ResourceLocation')
        startDimensionLocation = startResourceLocation.parse(String(dimension))
        startDimensionKey = startResourceKey.create(startRegistryKeys.DIMENSION, startDimensionLocation)
        startLevel = server.getLevel(startDimensionKey)
        if (startLevel === null || startLevel === undefined) throw new Error('dimension unavailable: ' + dimension)
        startStructureRegistry = server.registryAccess().registryOrThrow(startRegistryKeys.STRUCTURE)

        for (let startChunkX = bounds.minChunkX; startChunkX <= bounds.maxChunkX; startChunkX++) {
            for (let startChunkZ = bounds.minChunkZ; startChunkZ <= bounds.maxChunkZ; startChunkZ++) {
                const starts = startLevel.getChunk(startChunkX, startChunkZ).getAllStarts()
                starts.forEach((start, structure) => {
                    if (start === null || start === undefined || !start.isValid()) return
                    const startKey = startStructureRegistry.getKey(structure)
                    if (startKey === null || startKey === undefined) return
                    const startNamespace = String(startKey.getNamespace())
                    counts[startNamespace] = (counts[startNamespace] || 0) + 1
                    validStarts++
                })
            }
        }
        return { ok: true, validStarts: validStarts, byNamespace: counts }
    } catch (error) {
        return { ok: false, validStarts: 0, byNamespace: {}, error: String(error) }
    }
}

function worldgenBenchmarkRunTile(server, config, state, tileIndex) {
    if (!WorldgenBenchmark.active) return
    if (tileIndex >= config.tiles.length) {
        // KubeJS may retain the scheduled callback's Rhino activation between
        // invocations; var is intentionally restart-safe here.
        var completionElapsedMs = Date.now() - state.startedAtMs
        worldgenBenchmarkLog({
            event: 'benchmark_completed',
            runId: String(config.runId),
            variant: String(config.variant),
            suite: String(config.suite),
            seed: String(config.seed),
            tiles: Number(config.tiles.length),
            chunks: state.completedChunks,
            generationMs: state.generationMs,
            wallClockMs: completionElapsedMs,
            chunksPerSecond: state.generationMs > 0 ? state.completedChunks * 1000.0 / state.generationMs : 0
        })
        WorldgenBenchmark.active = false
        if (config.stopServerWhenComplete !== false) worldgenBenchmarkStop(server, 40)
        return
    }

    var tile = config.tiles[tileIndex]
    var dimension = String(tile.dimension)
    var bounds = worldgenBenchmarkTileBounds(tile)
    if (bounds.chunks < 1 || bounds.chunks > 256) {
        worldgenBenchmarkFail(server, config, 'invalid_tile_size', 'Each tile must contain between 1 and 256 chunks.', String(tile.name))
        return
    }

    var startedAtMs = Date.now()
    var addResult = server.runCommandSilent(worldgenBenchmarkForceloadCommand('add', dimension, bounds))
    worldgenBenchmarkLog({
        event: 'tile_started',
        runId: String(config.runId),
        tile: String(tile.name),
        tileIndex: tileIndex,
        dimension: dimension,
        chunks: bounds.chunks,
        minChunkX: bounds.minChunkX,
        minChunkZ: bounds.minChunkZ,
        maxChunkX: bounds.maxChunkX,
        maxChunkZ: bounds.maxChunkZ,
        forceloadResult: addResult
    })

    var timeoutMs = Number(config.tileTimeoutSeconds) * 1000
    var pollIntervalTicks = Number(config.pollIntervalTicks)
    var polls = 0

    function poll() {
        if (!WorldgenBenchmark.active) return
        polls++
        var elapsedMs = Date.now() - startedAtMs
        if (elapsedMs > timeoutMs) {
            server.runCommandSilent(worldgenBenchmarkForceloadCommand('remove', dimension, bounds))
            worldgenBenchmarkFail(server, config, 'tile_timeout', 'Tile generation exceeded its timeout.', String(tile.name))
            return
        }
        if (!worldgenBenchmarkAllChunksLoaded(server, dimension, bounds)) {
            server.scheduleInTicks(pollIntervalTicks, poll)
            return
        }

        var structureStarts = worldgenBenchmarkStructureStarts(server, dimension, bounds)
        if (!structureStarts.ok) {
            worldgenBenchmarkLog({
                event: 'acceptance_probe_error',
                runId: String(config.runId),
                stage: 'structure_starts',
                tile: String(tile.name),
                detail: String(structureStarts.error)
            })
        }

        server.runCommandSilent(worldgenBenchmarkForceloadCommand('remove', dimension, bounds))
        state.completedChunks += bounds.chunks
        state.generationMs += elapsedMs
        worldgenBenchmarkLog({
            event: 'tile_completed',
            runId: String(config.runId),
            tile: String(tile.name),
            tileIndex: tileIndex,
            dimension: dimension,
            chunks: bounds.chunks,
            elapsedMs: elapsedMs,
            chunksPerSecond: elapsedMs > 0 ? bounds.chunks * 1000.0 / elapsedMs : 0,
            polls: polls,
            validStructureStarts: Number(structureStarts.validStarts),
            structureStartsByNamespace: structureStarts.byNamespace
        })
        server.scheduleInTicks(Number(config.cooldownTicks), () =>
            worldgenBenchmarkRunTile(server, config, state, tileIndex + 1))
    }

    server.scheduleInTicks(pollIntervalTicks, poll)
}

ServerEvents.loaded(event => {
    const config = JsonIO.read(WorldgenBenchmark.configPath)
    if (!config || config.enabled !== true) return

    const server = event.server
    const runId = String(config.runId)
    if (runId.length < 1 || !Array.isArray(config.tiles) || config.tiles.length < 1) {
        worldgenBenchmarkFail(server, config, 'invalid_plan', 'The enabled benchmark plan has no run ID or tiles.')
        return
    }

    let actualWorldName
    let actualSeed
    try {
        actualWorldName = String(server.getWorldData().getLevelName())
        actualSeed = String(server.overworld().getSeed())
    } catch (error) {
        worldgenBenchmarkFail(server, config, 'world_identity_unavailable', 'Could not read the benchmark world identity.', error)
        return
    }

    if (actualWorldName !== String(config.worldName)) {
        worldgenBenchmarkFail(server, config, 'wrong_world_name', 'Refusing to benchmark an unexpected world.', actualWorldName)
        return
    }
    if (actualSeed !== String(config.seed)) {
        worldgenBenchmarkFail(server, config, 'wrong_seed', 'Refusing to benchmark an unexpected seed.', actualSeed)
        return
    }

    WorldgenBenchmark.active = true
    let plannedChunks = 0
    for (let plannedTileIndex = 0; plannedTileIndex < config.tiles.length; plannedTileIndex++) {
        plannedChunks += Number(config.tiles[plannedTileIndex].widthChunks)
            * Number(config.tiles[plannedTileIndex].depthChunks)
    }
    worldgenBenchmarkLog({
        event: 'benchmark_started',
        runId: runId,
        variant: String(config.variant),
        suite: String(config.suite),
        worldName: actualWorldName,
        seed: actualSeed,
        tiles: Number(config.tiles.length),
        plannedChunks: plannedChunks
    })

    worldgenBenchmarkModSnapshot(config)
    worldgenBenchmarkRegistrySnapshot(server, config)

    const state = { startedAtMs: Date.now(), completedChunks: 0, generationMs: 0 }
    server.scheduleInTicks(Number(config.warmupTicks), () => worldgenBenchmarkRunTile(server, config, state, 0))
})
})()
