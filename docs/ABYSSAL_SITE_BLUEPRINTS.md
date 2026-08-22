# Infinite Domain — Abyssal Site Blueprint Authority

Status: **mechanically implemented / Heavy Rebuild polish pending / runtime placement unmeasured**

This document is the blueprint authority for the eight first-class Infinite Domain abyssal structures. It complements `docs/ABYSSAL_OCEAN_PROGRAM.md` and records purpose, layout, evidence, and visual-language requirements without creating a competing terrain authority.

Runtime validation was explicitly waived on 2026-08-22. Structure existence and static integration may advance; placement quality, seabed clearance, aquifer interaction, and generation performance remain deferred observations.

## Design rules

Every abyssal site must have a readable former purpose, a regional identity, an accessible evidence path, and a progression-safe salvage path. The site-specific evidence container must be physically present in the structure. Generic salvage may supplement it but may not substitute for it.

Pelagos structures use maritime-scientific language: copper, prismarine, observation glazing, exposed sensors, survey masts, broad approaches, and readable instrumentation.

Karsic structures use industrial-military language: deepslate armor, pipelines, iron barriers, red warning systems, sonar/listening hardware, restricted vaults, and heavier defensive mass.

All current structures are single-template jigsaw sites projected to `OCEAN_FLOOR_WG`. Their IDs, structure sets, template pools, and biome tags remain stable while the NBT geometry improves.

## Slope recovery sites

### `infinite_domain:abyssal/pelagos_survey_wreck`
Role: first Western submarine recovery destination.
Evidence: `kubejs:abyssal_navigation_core`.
Required chest table: `infinite_domain:chests/abyssal/pelagos_survey_recovery`.
Status: custom pack-owned NBT with guaranteed evidence chest. Heavy Rebuild art remains open.

### `infinite_domain:abyssal/karsic_patrol_wreck`
Role: first Eastern submarine recovery destination.
Evidence: `kubejs:karsic_subsea_data_recorder`.
Required chest table: `infinite_domain:chests/abyssal/karsic_patrol_recovery`.
Status: custom pack-owned NBT with guaranteed evidence chest. Heavy Rebuild art remains open.

## Abyssal-plain installations

### `infinite_domain:abyssal/pelagos_abyssal_relay`
Current rebuilt footprint: **21 × 12 × 17**.
Purpose: Pelagos bathymetric survey and communications relay.
Visual language: prismarine foundation, copper pressure pod, tinted observation faces, sea-lantern work lighting, external copper instrument pylons, sensor crown and cross-mast.
Interior logic: dry central survey pod with console spine and two separated salvage positions.
Evidence container: `infinite_domain:chests/abyssal/pelagos_abyssal_relay`.
Evidence item: `kubejs:pelagos_bathymetric_log`.
Secondary salvage: `infinite_domain:chests/abyssal/abyssal_plain_salvage`.
Heavy Rebuild objective: add believable cabling, damaged pressure seals, scientific labeling, partial exterior collapse, and an alternate damaged-state template without changing the structure ID.

### `infinite_domain:abyssal/karsic_abyssal_pipeline_station`
Current rebuilt footprint: **29 × 10 × 15**.
Purpose: Karsic subsea freight/energy pipeline maintenance station.
Visual language: deepslate maintenance bunker, oxidized copper trunk pipeline, valve housings, iron inspection barriers, red warning lamps.
Interior logic: armored service room centered on the through-pipeline with separated evidence and salvage positions.
Evidence container: `infinite_domain:chests/abyssal/karsic_pipeline_station`.
Evidence item: `kubejs:karsic_pipeline_telemetry`.
Secondary salvage: `infinite_domain:chests/abyssal/abyssal_plain_salvage`.
Heavy Rebuild objective: add burst-pipe variants, maintenance gantries, freight-line junction pieces, damaged valves, and external cable/pipeline continuation stubs.

## Fracture-field installations

### `infinite_domain:abyssal/pelagos_fracture_observatory`
Current rebuilt footprint: **23 × 14 × 19**.
Purpose: Pelagos geological fracture monitoring and abyssal observation laboratory.
Visual language: weathered copper laboratory pod, broad forward observation blister, amethyst/geophone sensor arms, calibrated sensors, high mast.
Interior logic: paired laboratory benches, dry observation space, dedicated evidence and salvage positions.
Evidence container: `infinite_domain:chests/abyssal/pelagos_fracture_observatory`.
Evidence item: `kubejs:pelagos_fracture_sensor_core`.
Secondary salvage: `infinite_domain:chests/abyssal/abyssal_plain_salvage`.
Heavy Rebuild objective: tilt/settlement variants for unstable terrain, cracked glazing, collapsed sensor arm, exposed cable runs, and one partially flooded state.

### `infinite_domain:abyssal/karsic_fracture_listening_post`
Current rebuilt footprint: **23 × 14 × 23**.
Purpose: Karsic passive-acoustic surveillance and submarine contact station.
Visual language: polished deepslate bunker, armored slit architecture, dark-prismarine/iron sonar array, amethyst acoustic elements, red warning lamps.
Interior logic: rear archive cage, dry command bunker, mast and forward acoustic face.
Evidence container: `infinite_domain:chests/abyssal/karsic_listening_post`.
Evidence item: `kubejs:karsic_sonar_archive`.
Secondary salvage: `infinite_domain:chests/abyssal/abyssal_plain_salvage`.
Heavy Rebuild objective: add operator room, cable vault, flooded breach, exterior hydrophone field and damaged-array variant.

## Hadal installations

### `infinite_domain:abyssal/pelagos_hadal_probe_station`
Current rebuilt footprint: **17 × 19 × 17**.
Purpose: Pelagos pressure, probe and extreme-depth monitoring station.
Visual language: reinforced-deepslate anchors, compact dark-prismarine pressure pod, oxidized copper roof, tall copper probe tower and multiple horizontal sensor stages.
Interior logic: small protected evidence chamber with separate hadal salvage.
Evidence container: `infinite_domain:chests/abyssal/pelagos_hadal_probe`.
Evidence item: `kubejs:pelagos_hadal_pressure_record`.
Secondary salvage: `infinite_domain:chests/abyssal/hadal_salvage`.
Heavy Rebuild objective: add pressure-buckling damage states, tether equipment, dropped probe hardware and terrain-gripping anchor detail.

### `infinite_domain:abyssal/karsic_hadal_blacksite`
Current rebuilt footprint: **21 × 16 × 21**.
Purpose: restricted Karsic hadal archive / strategic research installation.
Visual language: reinforced-deepslate foundation and corner pylons, deepslate-tile bunker, polished-blackstone inner vault, obsidian archive floor, iron-bar blast vestibule, cold soul-lighting.
Interior logic: nested outer bunker and inner archive vault with physically separated evidence and generic hadal salvage.
Evidence container: `infinite_domain:chests/abyssal/karsic_hadal_blacksite`.
Evidence item: `kubejs:karsic_hadal_blacksite_cipher`.
Secondary salvage: `infinite_domain:chests/abyssal/hadal_salvage`.
Heavy Rebuild objective: add sealed research chambers, restricted signage, destroyed data hardware, pressure-door damage, partial cave-in and exterior surveillance hardware.

## Expedition progression contract

After `Ballast and Propulsion`, the player first completes both slope recovery voyages and returns the Pelagos navigation core and Karsic recorder to civilization. The deep expedition then splits:

**Pelagos:** Western abyssal plain → Pelagos relay + bathymetric log → Western fracture field + fracture observatory + sensor core → Western hadal trench + hadal probe station + pressure record.

**Karsic:** Eastern abyssal plain → Karsic pipeline station + telemetry → Eastern fracture field + listening post + sonar archive → Eastern hadal trench + blacksite + cipher.

The final convergence requires both hadal evidence items and produces `kubejs:abyssal_comparative_dossier`.

Maps may point to the next site, but evidence is no longer issued merely for arriving. The evidence must exist in the site-specific loot container and the quest must detect the physical item.

## Promotion boundary

These rebuilt NBTs are the authoritative mechanical structures. Heavy Rebuild work may replace geometry in-place under the same IDs. Do not create parallel duplicate structure IDs solely for visual revisions.

Deferred runtime checks remain:
- floor projection and burial quality;
- submarine approach/clearance;
- dry-space behavior and flooding;
- chest accessibility;
- structure-map resolution;
- encounter density around each depth band;
- generation cost.
