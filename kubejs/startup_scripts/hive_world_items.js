// Endgame - Cinderstack expedition + PPE items for infinite_domain:hive_world.
// Registry IDs use the internal token "cinderstack"; display strings never contain the
// prohibited substring "hive" (EG-P00-S02-C0003).
//
// EG-P06-S01-C0084 (constructed entry/return) + EG-P05 (mask/filter).

StartupEvents.registry('item', event => {
    event.create('cinderstack_marker')
        .displayName('Cinderstack Descent Marker')
        .texture('minecraft:item/heart_of_the_sea')
        .maxStackSize(1)
        .glow(true)
        .tooltip('§7Portal: Nether dimensions (4x5 to 23x23), four corner Actuators.')
        .tooltip('§7Use on the Portal Core in its lower edge to descend.')

    event.create('cinderstack_return_marker')
        .displayName('Cinderstack Return Marker')
        .texture('minecraft:item/echo_shard')
        .maxStackSize(1)
        .glow(true)
        .tooltip('§8Issued on arrival.')
        .tooltip('§7Portal: Nether dimensions (4x5 to 23x23), four corner Actuators.')
        .tooltip('§7Use on the Portal Core in its lower edge to return.')

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

StartupEvents.registry('block', event => {
    event.create('cinderstack_portal_frame')
        .displayName('Cinderstack Portal Frame')
        .parentModel('minecraft:block/cube')
        .texture('particle', 'minecraft:block/reinforced_deepslate_side')
        .texture('down', 'minecraft:block/reinforced_deepslate_bottom')
        .texture('up', 'minecraft:block/reinforced_deepslate_top')
        .texture('north', 'minecraft:block/reinforced_deepslate_side')
        .texture('south', 'minecraft:block/reinforced_deepslate_side')
        .texture('east', 'minecraft:block/reinforced_deepslate_side')
        .texture('west', 'minecraft:block/reinforced_deepslate_side')
        .stoneSoundType()
        .hardness(50.0)
        .resistance(1200.0)
        .requiresTool()
        .tagBlock('minecraft:mineable/pickaxe')
        .noValidSpawns(true)
        .item(item => item.tooltip('§7Structural member for a Nether-sized Cinderstack portal.'))

    event.create('cinderstack_portal_actuator')
        .displayName('Cinderstack Portal Actuator')
        .texture('create:block/refined_radiance_casing')
        .stoneSoundType()
        .hardness(75.0)
        .resistance(1200.0)
        .requiresTool()
        .tagBlock('minecraft:mineable/pickaxe')
        .lightLevel(0.65)
        .noValidSpawns(true)
        .item(item => item
            .rarity('rare')
            .glow(true)
            .tooltip('§7Install one at each of the portal frame\'s four corners.'))

    event.create('cinderstack_portal_core')
        .displayName('Cinderstack Portal Core')
        .parentModel('minecraft:block/cube')
        .texture('particle', 'create:block/creative_casing')
        .texture('down', 'minecraft:block/reinforced_deepslate_bottom')
        .texture('up', 'minecraft:block/end_portal_frame_top')
        .texture('north', 'create:block/creative_casing')
        .texture('south', 'create:block/creative_casing')
        .texture('east', 'create:block/creative_casing')
        .texture('west', 'create:block/creative_casing')
        .stoneSoundType()
        .hardness(100.0)
        .resistance(1200.0)
        .requiresTool()
        .tagBlock('minecraft:mineable/pickaxe')
        .lightLevel(0.85)
        .noValidSpawns(true)
        .item(item => item
            .rarity('epic')
            .glow(true)
            .tooltip('§5Control block installed anywhere along the portal\'s lower edge.'))

    // This is a generated field block, not a survival crafting component. Using
    // the vanilla End Portal sprite gives it the requested End Portal appearance
    // without inheriting the vanilla End-dimension teleport behavior.
    event.create('cinderstack_portal_field')
        .displayName('Cinderstack Portal Field')
        .texture('minecraft:entity/end_portal')
        .stoneSoundType()
        .unbreakable()
        .resistance(3600000.0)
        .noDrops()
        .noCollision()
        .notSolid()
        .opaque(false)
        .fullBlock(false)
        .defaultCutout()
        .lightLevel(1.0)
        .noValidSpawns(true)
        .item(item => item
            .rarity('epic')
            .glow(true)
            .tooltip('§8Generated when a completed portal is actuated.'))
})
