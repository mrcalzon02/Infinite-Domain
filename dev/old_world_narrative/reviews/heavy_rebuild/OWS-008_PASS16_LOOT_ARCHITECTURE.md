# OWS-008 Heavy Rebuild — Pass 16 Loot Architecture

OWS-008 uses the existing canonical site table exactly once:

`infinite_domain:chests/old_world/ows_008_vcf_emergency_persistence_investigation_lab`

That authoritative table guarantees `kubejs:vcf_persistence_incident_file` and adds restrained industrial components. Its one container therefore serves as both the secure incident-record loot node and the one canonical proof node. Duplicating it would duplicate guaranteed proof and is prohibited.

The container belongs in the upper secure incident archive after the player has traversed or observed the treatment/verification sequence. Existing crates, coolers, tanks, depots and sample stations remain environmental equipment rather than improvised inventories. No replacement loot table or hard-coded random contents were created.
