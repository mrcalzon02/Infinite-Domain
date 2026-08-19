// Infinite Domain spawn-hub hostile exclusion zone.
//
// Match the Admin Spawn claim exactly: chunk coordinates -3..3 on both axes,
// or block coordinates -48..63. This fully contains the radius-48 blended terrain
// platform at -40..39. The check covers every Y level, including the roof and
// caves beneath the hub, without changing spawning elsewhere in the world.
(() => {
    const $Mob = Java.loadClass('net.minecraft.world.entity.Mob')
    const MIN_X = -48
    const MAX_X_EXCLUSIVE = 64
    const MIN_Z = -48
    const MAX_Z_EXCLUSIVE = 64

    function isProtectedMob(event, entity, x, z) {
        // In KubeJS 2101 Level.dimension is a property, not a function.
        if (!event.level.dimension.toString().includes('minecraft:overworld')) {
            return false
        }

        // EntityType#getCategory is not exposed by KubeJS 2101's Rhino wrapper.
        // Checking the Java base class catches vanilla and modded living mobs
        // (including Spore's programmatically-added creatures) without touching
        // players, dropped items, projectiles, paintings, or armor stands.
        if (!(entity instanceof $Mob)) {
            return false
        }

        return x >= MIN_X && x < MAX_X_EXCLUSIVE &&
            z >= MIN_Z && z < MAX_Z_EXCLUSIVE
    }

    // Deny ordinary, patrol, structure, and spawner-driven mob finalization.
    EntityEvents.checkSpawn(event => {
        if (isProtectedMob(event, event.entity, event.x, event.z)) {
            event.cancel()
        }
    })

    // Safety net for modded paths that add an entity without FinalizeSpawnEvent.
    EntityEvents.spawned(event => {
        const entity = event.entity
        if (isProtectedMob(event, entity, entity.x, entity.z)) {
            event.cancel()
        }
    })
})()
