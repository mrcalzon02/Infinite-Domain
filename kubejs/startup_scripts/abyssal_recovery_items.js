// [SYSTEM REPORT] Abyssal recovery and deep-expedition evidence registry.
// Mechanical-first implementation: bespoke art may replace vanilla placeholder textures later.

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

    event.create('pelagos_bathymetric_log')
        .displayName('Pelagos Bathymetric Survey Log')
        .texture('minecraft:item/map')
        .tooltip('§7A sealed deep-ocean survey record recovered from a Pelagos relay.')
        .tooltip('§8Contains abyssal-plain depth and route data.')

    event.create('pelagos_fracture_sensor_core')
        .displayName('Pelagos Fracture Sensor Core')
        .texture('minecraft:item/amethyst_shard')
        .tooltip('§7A hardened sensor package recovered from a fracture observatory.')
        .tooltip('§8Its readings describe unstable abyssal terrain.')

    event.create('pelagos_hadal_pressure_record')
        .displayName('Pelagos Hadal Pressure Record')
        .texture('minecraft:item/nautilus_shell')
        .tooltip('§7A pressure and probe record recovered from a hadal station.')
        .tooltip('§8Evidence from the deepest Pelagos operating envelope.')

    event.create('karsic_pipeline_telemetry')
        .displayName('Karsic Pipeline Telemetry Package')
        .texture('minecraft:item/redstone')
        .tooltip('§7Industrial subsea-flow and maintenance telemetry.')
        .tooltip('§8Recovered from a Karsic abyssal pipeline station.')

    event.create('karsic_sonar_archive')
        .displayName('Karsic Sonar Archive')
        .texture('minecraft:item/echo_shard')
        .tooltip('§7A hardened passive-acoustic archive from a fracture listening post.')
        .tooltip('§8Contains patrol and contact data from the final operating period.')

    event.create('karsic_hadal_blacksite_cipher')
        .displayName('Karsic Hadal Blacksite Cipher')
        .texture('minecraft:item/recovery_compass')
        .tooltip('§7Encrypted blacksite records recovered from hadal depth.')
        .tooltip('§8Preserve intact for comparative analysis.')

    event.create('abyssal_comparative_dossier')
        .displayName('Comparative Abyssal Dossier')
        .texture('minecraft:item/book')
        .tooltip('§7A compiled Pelagos/Karsic deep-ocean evidence package.')
        .tooltip('§8Proof that both abyssal systems were active during the final era.')
})
