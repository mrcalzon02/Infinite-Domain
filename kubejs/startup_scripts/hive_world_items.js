// Endgame EG-P01-S04-C0019 - Phase 1 spike expedition items for infinite_domain:hive_world.
// DISPOSABLE: promoted or removed at EG-P01-S06-C0023. The real constructible access
// mechanism is Phase 6 EG-P06-S01-C0084.
//
// Registry IDs use the internal token "cinderstack"; display strings never contain the
// prohibited substring "hive" (EG-P00-S02-C0003).

StartupEvents.registry('item', event => {
    event.create('cinderstack_marker')
        .displayName('Cinderstack Descent Marker')
        .texture('minecraft:item/heart_of_the_sea')
        .maxStackSize(1)
        .glow(true)
        .tooltip('§8Operator expedition tool - Phase 1 spike.')
        .tooltip('§7Use it anywhere outside the Cinderstack to descend.')
        .tooltip('§7Your exact departure point is recorded for the return.')

    event.create('cinderstack_return_marker')
        .displayName('Cinderstack Return Marker')
        .texture('minecraft:item/echo_shard')
        .maxStackSize(1)
        .glow(true)
        .tooltip('§8Issued on arrival.')
        .tooltip('§7Use it inside the Cinderstack to return to your recorded departure point.')
})
