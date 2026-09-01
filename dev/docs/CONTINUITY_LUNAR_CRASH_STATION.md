# Continuity Lunar Crash Station

**Structure ID:** `infinite_domain:offworld/continuity_lunar_crash_station`  
**Minecraft:** NeoForge 1.21.1  
**Authority:** Stellaris lunar biomes and machinery  
**StructureSmith DataVersion:** 3955  
**Template size:** 47 × 26 × 47  
**Block count:** 4365  
**Placement:** seeded `minecraft:random_spread`, moon-biome gated, projected to `WORLD_SURFACE_WG`

## Design intent

A late-era Continuity orbital station failed during the final collapse and struck the lunar surface. The surviving crew did not simply die in the wreck: they spent enough time alive to turn the crash into a crude redoubt. The result is two architectures occupying the same site — a damaged high-technology pressure station and a later layer of improvised survival construction.

The surviving station spine contains a crushed command nose, pressure bulkheads, habitation storage, a life-support salvage core and a ruptured engineering compartment. Outside, the crew built **Patch Alpha**, a low field shelter buried under lunar regolith for radiation and impact shielding. It is connected back to the hull by a tiny jury-rigged crawl-tube. A broken solar field, exposed cables, scavenged tanks, improvised antenna work and mismatched hull plating make the emergency effort readable from the exterior.

## Exploration read

The intended player path begins at the impact rim, enters either the torn station or the exterior shelter, follows improvised power/life-support infrastructure, and eventually reaches the command-side evidence cache. A guaranteed Stellaris tablet is used as the evidence object; the second chest is general lunar salvage.

## Worldgen

The structure is restricted to `#stellaris:moon_biomes`. The supplied structure set uses spacing **96 chunks**, separation **56 chunks**, and salt **1686787742**. This is intentionally rarer than the existing Continuity far-side redoubt while still allowing deterministic discovery from a world seed.

## Required runtime gate

Before promotion, test on a fresh lunar world and verify: jigsaw placement, surface projection, crater/terrain blending, no invalid Stellaris blockstates, traversable compartments, chest loot resolution, and acceptable encounter/exploration distance.
