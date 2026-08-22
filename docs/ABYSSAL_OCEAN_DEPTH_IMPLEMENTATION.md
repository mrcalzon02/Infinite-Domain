# Infinite Domain — Abyssal Ocean Depth Implementation

Authoritative parent: `docs/ABYSSAL_OCEAN_PROGRAM.md`

Status: **terrain/depth routing is active under an explicit runtime-validation waiver; the structure and quest layers now consume the resulting depth bands. Physical seabed measurements remain unobserved.**

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

## Consumers now attached to the depth bands

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

The six deep structure definitions project to `OCEAN_FLOOR_WG`; their geometry does not alter the terrain functions. Richer replacement NBTs for all six have been authored and statically parsed, but the active repository paths still hold the earlier mechanical shells pending byte-exact binary promotion.

## Deep structure evidence

Site-specific evidence contracts are authored for the staged richer NBTs:
- Pelagos relay → `pelagos_bathymetric_log`
- Pelagos observatory → `pelagos_fracture_sensor_core`
- Pelagos hadal station → `pelagos_hadal_pressure_record`
- Karsic pipeline station → `karsic_pipeline_telemetry`
- Karsic listening post → `karsic_sonar_archive`
- Karsic blacksite → `karsic_hadal_blacksite_cipher`

Those six items are registered and their loot tables exist. Until the richer NBTs can replace the old shells byte-exactly, the quest layer issues each record as a compatibility reward after the matching structure is reached. After binary promotion, the quest must switch to physical chest-recovery item tasks.

## Deferred validation ledger

When runtime access returns:
1. validate density-function loading;
2. verify East/West routing and transition seam;
3. inspect the central continent/mountain annulus;
4. inspect north/south oceans for abyssal contamination;
5. measure seabed Y at shelf, slope, plain, fracture and deepest hadal candidates;
6. inspect cave/aquifer/bedrock interaction;
7. verify all eight abyssal structures resolve with `/structure_map`;
8. inspect `OCEAN_FLOOR_WG` projection, burial, flooding and chest accessibility;
9. run both slope-return voyages and both deep expedition branches end-to-end;
10. verify FTB mobs remain out of starter water and scale by depth;
11. assess submarine clearance;
12. measure generation cost.

If continentalness alone later proves too shallow, only a narrowly East/West + ocean + hadal gated final-density contribution may be considered. Global Overworld deepening remains prohibited.
