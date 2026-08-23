# Infinite Domain — Abyssal Ocean Depth Implementation

Authoritative parent: `docs/ABYSSAL_OCEAN_PROGRAM.md`

Status: **terrain/depth routing is active under an explicit runtime-validation waiver; all eight core abyssal structures, four optional environmental structures, the depth-graded seabed feature pass, and both deep quest branches consume the resulting depth bands. Physical seabed measurements remain unobserved.**

## Gate disposition

Fresh-world validation was unavailable on 2026-08-22. Project direction was to continue as if positive. Implementation can therefore advance, but no measured terrain, flooding, navigation or performance claim is considered proven.

## Terrain chain

The active outer-world depth chain remains:
- `custom_worldgen:east_west_ocean_corridor_mask`
- `custom_worldgen:abyssal_ocean_mask`
- `custom_worldgen:abyssal_plain_mask`
- `custom_worldgen:abyssal_fracture_mask`
- `custom_worldgen:hadal_trench_mask`
- `custom_worldgen:western_depth_depression`
- `custom_worldgen:eastern_depth_depression`
- `custom_worldgen:abyssal_outer_continents`

`custom_worldgen:continents` uses the abyssal outer branch only outside the protected central-continent mask.

Initial continentalness pressure remains:
1. slope/ocean `0.05`
2. abyssal plain `0.12`
3. fracture/hadal `0.28`

No final-density mutation has been added.

## Active routing bands

| Role | Continentalness | West | East |
| --- | --- | --- | --- |
| Continental slope | `-0.60 .. -0.455` | `western_continental_slope` | `eastern_continental_slope` |
| Abyssal plain | `-0.82 .. -0.60` | `western_abyssal_plain` | `eastern_abyssal_plain` |
| Fracture field | `-1.02 .. -0.82` | `western_fracture_field` | `eastern_fracture_field` |
| Hadal trench | `-1.20 .. -1.02` | `western_hadal_trench` | `eastern_hadal_trench` |

Every band uses the established regional humidity split:
- `-1.0 .. -0.2`: West
- `-0.2 .. 0.2`: vanilla deep-ocean seam
- `0.2 .. 1.0`: East

## Depth-graded placed features

Only verified vanilla 1.21.1 placed-feature IDs are used in the current natural population pass.

### Western continental slope
- geology: `underwater_magma`, `disk_sand`, `disk_clay`, `disk_gravel`
- vegetation: `seagrass_deep_cold`, `kelp_cold`

### Eastern continental slope
- geology: `underwater_magma`, `disk_sand`, `disk_clay`, `disk_gravel`
- vegetation: `seagrass_deep`, `kelp_cold`

### Western abyssal plain
- geology: `underwater_magma`, `disk_clay`, `disk_gravel`
- vegetation: `seagrass_deep_cold`

### Eastern abyssal plain
- geology: `underwater_magma`, `disk_clay`, `disk_gravel`
- vegetation: `seagrass_deep`

### Both fracture fields
- geology: `underwater_magma`, `disk_gravel`
- vegetation: none

### Both hadal trenches
- geology: `underwater_magma`
- vegetation: none

The intent is a readable ecological drop-off with depth: populated slope → sparse plain → barren fracture → near-sterile hadal floor. Live distribution remains unmeasured.

## Core structure consumers

Slope:
- Pelagos survey wreck
- Karsic patrol wreck

Abyssal plain:
- Pelagos abyssal relay
- Karsic abyssal pipeline station

Fracture:
- Pelagos fracture observatory
- Karsic fracture listening post

Hadal:
- Pelagos hadal probe station
- Karsic hadal blacksite

The six core deep structure definitions project to `OCEAN_FLOOR_WG`; their geometry does not alter the terrain functions. `tools/abyssal_rebuild/generate_abyssal_sites.py` is the deterministic source of their active NBTs and verifies each generated Git blob before materialization.

Every core deep installation contains an intentional underwater access breach. The five ordinary deep sites expose a 3 × 3 outer-shell opening. The Karsic hadal blacksite exposes the outer bunker and inner archive through aligned 3 × 3 breaches. These openings are static accessibility guarantees; actual water behavior and approach quality remain runtime-unmeasured.

## Optional environmental consumers

The first optional environmental family consumes the same depth routing without changing it:

- `pelagos_sensor_debris` → Western abyssal plain only; spacing/separation `112/56`, salt `78064401`.
- `karsic_pipeline_breach` → Eastern abyssal plain only; spacing/separation `112/56`, salt `78064402`.
- `abyssal_cold_seep` → both abyssal-plain families; spacing/separation `160/80`, salt `78064501`.
- `fracture_vent_field` → both fracture-field families; spacing/separation `176/88`, salt `78064601`.

All four project to `OCEAN_FLOOR_WG`, use single-piece jigsaw pools and `terrain_adaptation: bury`, and are generated deterministically by `tools/abyssal_rebuild/generate_abyssal_environmental_sites.py`.

The Pelagos debris and Karsic breach reuse the generic abyssal-plain salvage table. The cold seep and vent field have no chest. None is quest-critical and none changes evidence progression.

## Deep structure evidence

Every core deep structure physically contains its site-specific evidence chest and a secondary salvage chest:
- Pelagos relay → `pelagos_bathymetric_log`
- Pelagos observatory → `pelagos_fracture_sensor_core`
- Pelagos hadal station → `pelagos_hadal_pressure_record`
- Karsic pipeline station → `karsic_pipeline_telemetry`
- Karsic listening post → `karsic_sonar_archive`
- Karsic blacksite → `karsic_hadal_blacksite_cipher`

The six evidence items are registered and their loot tables guarantee the required record. The FTB quest chapter requires the matching structure plus the physical evidence item; compatibility-issued deep evidence rewards are removed.

## Create Aquatic Ambitions verification

Upstream 1.21.1 source was inspected before integration decisions. The addon exposes processing/automation content such as `create_aquatic_ambitions:mechanical_conduit` and prismarine-alloy materials, but it does not provide natural abyssal entities or geological placed features. It is therefore not used as a natural biome-population source. Any future use must remain controlled and progression-safe.

## Deferred validation ledger

When runtime access returns:
1. validate density-function loading;
2. verify East/West routing and transition seam;
3. inspect the central continent/mountain annulus;
4. inspect north/south oceans for abyssal contamination;
5. measure seabed Y at shelf, slope, plain, fracture and deepest hadal candidates;
6. inspect cave/aquifer/bedrock interaction;
7. verify all eight core and four optional abyssal structures resolve with `/structure_map` where applicable;
8. inspect `OCEAN_FLOOR_WG` projection, burial, open-breach flooding and chest accessibility;
9. inspect cold-seep and vent bubble behavior;
10. run both slope-return voyages and both deep expedition branches end-to-end;
11. verify the seabed features scale by depth rather than making fracture/hadal terrain visually busy;
12. verify FTB mobs remain out of starter water and scale by depth;
13. assess submarine clearance;
14. measure generation cost.

If continentalness alone later proves too shallow, only a narrowly East/West + ocean + hadal gated final-density contribution may be considered. Global Overworld deepening remains prohibited.
