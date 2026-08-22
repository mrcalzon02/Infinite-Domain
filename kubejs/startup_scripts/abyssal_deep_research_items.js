// [SYSTEM REPORT] Deep abyssal expedition evidence registry.
// Mechanical-first assets: vanilla textures are intentional placeholders until the abyssal visual pass.

StartupEvents.registry('item', event => {
    event.create('pelagos_bathymetric_log')
        .displayName('Pelagos Bathymetric Survey Log')
        .texture('minecraft:item/map')
        .tooltip('§7Pressure-stained depth and current records from a Pelagos survey relay.')
        .tooltip('§8A route deeper into the Western Abyss can be reconstructed from this data.')

    event.create('karsic_pipeline_telemetry')
        .displayName('Karsic Pipeline Telemetry Spool')
        .texture('minecraft:item/paper')
        .tooltip('§7Recovered flow, pressure, and maintenance telemetry from an eastern subsea trunk line.')
        .tooltip('§8The timestamps imply traffic continued long after the surface network failed.')

    event.create('pelagos_fracture_sensor_core')
        .displayName('Pelagos Fracture Sensor Core')
        .texture('minecraft:item/amethyst_shard')
        .tooltip('§7A hardened geophone and chemical-sensor core from the Western fracture observatory.')
        .tooltip('§8Its surviving readings point toward extreme-depth probe operations.')

    event.create('karsic_sonar_archive')
        .displayName('Karsic Sonar Archive')
        .texture('minecraft:item/echo_shard')
        .tooltip('§7A military acoustic archive recovered from a Karsic listening post.')
        .tooltip('§8Several classified tracks terminate inside the hadal zone.')

    event.create('pelagos_hadal_pressure_record')
        .displayName('Pelagos Hadal Pressure Record')
        .texture('minecraft:item/prismarine_crystals')
        .tooltip('§7The final pressure and probe telemetry recovered from a Pelagos hadal station.')
        .tooltip('§8Scientific evidence gathered where ordinary subsea engineering stopped being sufficient.')

    event.create('karsic_hadal_blacksite_cipher')
        .displayName('Karsic Hadal Blacksite Cipher')
        .texture('minecraft:item/disc_fragment_5')
        .tooltip('§7A sealed cipher package recovered from a Karsic extreme-depth blacksite.')
        .tooltip('§8Its contents were important enough to bury beneath kilometers of water.')

    event.create('abyssal_comparative_dossier')
        .displayName('Comparative Abyssal Dossier')
        .texture('minecraft:item/writable_book')
        .tooltip('§7A reconstructed comparison of Pelagos scientific records and Karsic military archives.')
        .tooltip('§8Knowledge token: preserves the completed abyssal investigation for later progression.')
})
