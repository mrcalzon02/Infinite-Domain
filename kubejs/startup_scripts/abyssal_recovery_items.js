// [SYSTEM REPORT] Abyssal recovery evidence registry.
// Mechanical-first implementation: bespoke art may replace vanilla placeholder textures later.
//
// Deep-expedition research items are registered authoritatively in
// abyssal_deep_research_items.js. This file owns only the two initial recovery
// items so every kubejs item ID has exactly one registry owner.

StartupEvents.registry('item', event => {
    event.create('abyssal_navigation_core')
        .displayName('Recovered Abyssal Navigation Core')
        .texture('minecraft:item/echo_shard')
        .tooltip('§7Recovered from a drowned Old World navigation package.')
        .tooltip('§8Pelagos deepwater survey hardware — preserve for analysis.')

    event.create('karsic_subsea_data_recorder')
        .displayName('Recovered Karsic Subsea Data Recorder')
        .texture('minecraft:item/prismarine_crystals')
        .tooltip('§7Recovered from a drowned military-industrial patrol package.')
        .tooltip('§8Karsic bathymetric and patrol telemetry — preserve for analysis.')
})
