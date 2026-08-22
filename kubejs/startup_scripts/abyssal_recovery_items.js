// [SYSTEM REPORT] Abyssal recovery proof-item registry.
// Mechanical-first implementation: bespoke art may replace the vanilla echo-shard texture later.

StartupEvents.registry('item', event => {
    event.create('abyssal_navigation_core')
        .displayName('Recovered Abyssal Navigation Core')
        .texture('minecraft:item/echo_shard')
        .tooltip('§7Recovered from a drowned Old World navigation package.')
        .tooltip('§8Pelagos deepwater survey hardware — preserve for analysis.')
})
