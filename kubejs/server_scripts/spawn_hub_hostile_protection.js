// Infinite Domain spawn-hub hostile exclusion zone.
//
// Match the Admin Spawn claim exactly: chunk coordinates -3..3 on both axes,
// or block coordinates -48..63. This contains the radius-48 blended terrain
// platform at -40..39. The check covers every Y level, including the roof and
// caves beneath the hub, without changing spawning elsewhere in the world.
(() => {
    const $Mob = Java.loadClass('net.minecraft.world.entity.Mob')
    const $Monster = Java.loadClass('net.minecraft.world.entity.monster.Monster')
    const MIN_X = -48
    const MAX_X_EXCLUSIVE = 64
    const MIN_Z = -48
    const MAX_Z_EXCLUSIVE = 64

    function isProtectedHostile(event, entity, x, z) {
        // KubeJS 2101 exposes Level.dimension as a property, not a function.
        if (String(event.level.dimension) !== 'minecraft:overworld') return false
        if (x < MIN_X || x >= MAX_X_EXCLUSIVE || z < MIN_Z || z >= MAX_Z_EXCLUSIVE) return false

        // The old Mob-only check also blocked cows, villagers, pets and other
        // peaceful creatures. Keep vanilla Monster subclasses out of the hub.
        if (!(entity instanceof $Mob)) return false
        if (entity instanceof $Monster) return true

        // Some Spore entities are generated through custom Mob subclasses rather
        // than vanilla Monster. Exclude their living mobs without suppressing
        // Spore projectiles, dropped items, or other non-Mob entities.
        return String(entity.type).startsWith('spore:')
    }

    // Deny ordinary, patrol, structure, and spawner-driven hostile finalization.
    EntityEvents.checkSpawn(event => {
        if (isProtectedHostile(event, event.entity, event.x, event.z)) event.cancel()
    })

    // Safety net for modded paths that add an entity without FinalizeSpawnEvent.
    EntityEvents.spawned(event => {
        const entity = event.entity
        if (isProtectedHostile(event, entity, entity.x, entity.z)) event.cancel()
    })
})()
