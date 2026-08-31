// Headless, fixed-seed world-generation benchmark controller.
// This script is inert in ordinary worlds. The isolated benchmark launcher
// replaces kubejs/config/worldgen_benchmark.json with an enabled run plan.

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
    const minChunkX = Number(tile.minChunkX)
    const minChunkZ = Number(tile.minChunkZ)
    const width = Number(tile.widthChunks)
    const depth = Number(tile.depthChunks)
    return {
        minChunkX: minChunkX,
        minChunkZ: minChunkZ,
        maxChunkX: minChunkX + width - 1,
        maxChunkZ: minChunkZ + depth - 1,
        minBlockX: worldgenBenchmarkChunkBlock(minChunkX),
        minBlockZ: worldgenBenchmarkChunkBlock(minChunkZ),
        maxBlockX: worldgenBenchmarkChunkBlock(minChunkX + width) - 1,
        maxBlockZ: worldgenBenchmarkChunkBlock(minChunkZ + depth) - 1,
        chunks: width * depth
    }
}

function worldgenBenchmarkForceloadCommand(action, dimension, bounds) {
    return 'execute in ' + dimension + ' run forceload ' + action + ' ' +
        bounds.minBlockX + ' ' + bounds.minBlockZ + ' ' +
        bounds.maxBlockX + ' ' + bounds.maxBlockZ
}

function worldgenBenchmarkAllChunksLoaded(server, dimension, bounds) {
    for (let chunkX = bounds.minChunkX; chunkX <= bounds.maxChunkX; chunkX++) {
        for (let chunkZ = bounds.minChunkZ; chunkZ <= bounds.maxChunkZ; chunkZ++) {
            const blockX = worldgenBenchmarkChunkBlock(chunkX) + 8
            const blockZ = worldgenBenchmarkChunkBlock(chunkZ) + 8
            const command = 'execute in ' + dimension + ' positioned ' + blockX + ' 0 ' + blockZ +
                ' if loaded ~ ~ ~ run function infinite_domain:worldgen_benchmark/probe'
            if (server.runCommandSilent(command) <= 0) return false
        }
    }
    return true
}

function worldgenBenchmarkRunTile(server, config, state, tileIndex) {
    if (!WorldgenBenchmark.active) return
    if (tileIndex >= config.tiles.length) {
        const elapsedMs = Date.now() - state.startedAtMs
        worldgenBenchmarkLog({
            event: 'benchmark_completed',
            runId: String(config.runId),
            variant: String(config.variant),
            suite: String(config.suite),
            seed: String(config.seed),
            tiles: Number(config.tiles.length),
            chunks: state.completedChunks,
            generationMs: state.generationMs,
            wallClockMs: elapsedMs,
            chunksPerSecond: state.generationMs > 0 ? state.completedChunks * 1000.0 / state.generationMs : 0
        })
        WorldgenBenchmark.active = false
        if (config.stopServerWhenComplete !== false) worldgenBenchmarkStop(server, 40)
        return
    }

    const tile = config.tiles[tileIndex]
    const dimension = String(tile.dimension)
    const bounds = worldgenBenchmarkTileBounds(tile)
    if (bounds.chunks < 1 || bounds.chunks > 256) {
        worldgenBenchmarkFail(server, config, 'invalid_tile_size', 'Each tile must contain between 1 and 256 chunks.', String(tile.name))
        return
    }

    const startedAtMs = Date.now()
    const addResult = server.runCommandSilent(worldgenBenchmarkForceloadCommand('add', dimension, bounds))
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

    const timeoutMs = Number(config.tileTimeoutSeconds) * 1000
    const pollIntervalTicks = Number(config.pollIntervalTicks)
    let polls = 0

    function poll() {
        if (!WorldgenBenchmark.active) return
        polls++
        const elapsedMs = Date.now() - startedAtMs
        if (elapsedMs > timeoutMs) {
            server.runCommandSilent(worldgenBenchmarkForceloadCommand('remove', dimension, bounds))
            worldgenBenchmarkFail(server, config, 'tile_timeout', 'Tile generation exceeded its timeout.', String(tile.name))
            return
        }
        if (!worldgenBenchmarkAllChunksLoaded(server, dimension, bounds)) {
            server.scheduleInTicks(pollIntervalTicks, poll)
            return
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
            polls: polls
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
    const runtime = Java.loadClass('java.lang.Runtime').getRuntime()
    worldgenBenchmarkLog({
        event: 'benchmark_started',
        runId: runId,
        variant: String(config.variant),
        suite: String(config.suite),
        worldName: actualWorldName,
        seed: actualSeed,
        tiles: Number(config.tiles.length),
        plannedChunks: config.tiles.reduce((sum, tile) => sum + Number(tile.widthChunks) * Number(tile.depthChunks), 0),
        maxHeapBytes: Number(runtime.maxMemory())
    })

    const state = { startedAtMs: Date.now(), completedChunks: 0, generationMs: 0 }
    server.scheduleInTicks(Number(config.warmupTicks), () => worldgenBenchmarkRunTile(server, config, state, 0))
})
