// Endgame - Cinderstack expedition + PPE items for infinite_domain:hive_world.
// Registry IDs use the internal token "cinderstack"; display strings never contain the
// prohibited substring "hive" (EG-P00-S02-C0003).
//
// EG-P01-S04-C0019 (marker/return) + EG-P05 (mask/filter). DISPOSABLE spike items:
// the constructible entry is Phase 6 C0084; the companion module owns the real PPE
// adapters at Phase 5 C0070.

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

    // EG-P05 C0070 - the reusable respirator. Held or carried, not required to be worn.
    // Has durability so it is not permanent immunity (mission 2.5).
    event.create('cinderstack_mask')
        .displayName('Cinderstack Respirator')
        .texture('minecraft:item/turtle_helmet')
        .maxStackSize(1)
        .maxDamage(512)
        .glow(true)
        .tooltip('§7Carry it in the Cinderstack. With a filter cartridge it cuts')
        .tooltip('§7atmosphere exposure sharply; without one it helps only a little.')
        .tooltip('§8Wears down with use. No filter, no seal.')

    // EG-P05 C0072 - the consumable. Spent by sustained filtered exposure.
    event.create('cinderstack_filter')
        .displayName('Cinderstack Filter Cartridge')
        .texture('minecraft:item/dried_kelp')
        .maxStackSize(16)
        .tooltip('§7Fits the respirator. Each cartridge is consumed by')
        .tooltip('§7sustained exposure; carry spares.')
})
