# Infinite Domain — Abyssal Ocean Depth Implementation

Authoritative parent: `docs/ABYSSAL_OCEAN_PROGRAM.md`

Status: **terrain/depth routing is active under an explicit runtime-validation waiver; six-pattern systemic seabed deformation, custom slope/fracture cave carvers, all eight core abyssal structures, five optional environmental structures, the depth-graded seabed feature pass, and both deep quest branches consume the resulting depth bands. Physical seabed measurements remain unobserved.**

## Gate disposition

Fresh-world validation was unavailable on 2026-08-22. Project direction was to continue as if positive. Implementation can therefore advance, but no measured terrain, flooding, navigation or performance claim is considered proven.

## Terrain chain

The active outer-world depth chain now includes both the original depth masks and the reference-pattern deformation layer:
- `custom_worldgen:east_west_ocean_corridor_mask`
- `custom_worldgen:abyssal_ocean_mask`
- `custom_worldgen:abyssal_plain_mask`
- `custom_worldgen:abyssal_fracture_mask`
- `custom_worldgen:hadal_trench_mask`
- `custom_worldgen:abyssal_slope_band_mask`
- `custom_worldgen:abyssal_cellular_basin_pattern`
- `custom_worldgen:abyssal_coarse_fracture_pattern`
- `custom_worldgen:abyssal_diffuse_roughness_pattern`
- `custom_worldgen:abyssal_mottled_collapse_pattern`
- `custom_worldgen:abyssal_vent_caldera_pattern`
- `custom_worldgen:abyssal_fine_fracture_pattern`
- `custom_worldgen:abyssal_pattern_depression`
- `custom_worldgen:western_depth_depression`
- `custom_worldgen:eastern_depth_depression`
- `custom_worldgen:abyssal_outer_continents`

`custom_worldgen:continents` uses the abyssal outer branch only outside the protected central-continent mask. No global `final_density` mutation has been added.

Base continentalness pressure remains:
1. slope/ocean `0.05`
2. abyssal plain `0.12`
3. fracture/hadal `0.28`

The pattern layer is additional and remains inside the same East/West selector + ocean-corridor gate.

## Noise vocabulary derived from the supplied reference patterns

Pack-owned noise parameter sets:
- `custom_worldgen:abyssal_cells` — octave profile `-6`, amplitudes `[1.0, 0.5, 0.25]`;
- `custom_worldgen:abyssal_faults` — octave profile `-7`, amplitudes `[1.0, 1.0]`;
- `custom_worldgen:abyssal_roughness` — octave profile `-5`, amplitudes `[1.0, 0.7, 0.35]`;
- `custom_worldgen:abyssal_vents` — octave profile `-8`, amplitudes `[1.0, 0.5]`.

Reference motif → density function:
- rounded cellular field → `abyssal_cellular_basin_pattern`;
- coarse connected cracks → `abyssal_coarse_fracture_pattern`;
- diffuse granular roughness → `abyssal_diffuse_roughness_pattern`;
- mottled collapse/pockmark field → `abyssal_mottled_collapse_pattern`;
- central/radial vent disturbance → `abyssal_vent_caldera_pattern`;
- fine crack mesh → `abyssal_fine_fracture_pattern`.

The coarse and fine fracture functions select narrow contours around zero crossings of shifted fault noise, producing corridor-like depressions rather than simply lowering every noisy pixel. The vent selector uses rare positive peaks of a much lower-frequency field, while cellular/collapse/roughness patterns operate at different spatial frequencies to prevent the entire abyss from sharing one texture.

### Pattern amplitudes

`custom_worldgen:abyssal_pattern_depression` applies:
- slope band: diffuse roughness `0.008` + coarse gully/fault `0.012`;
- abyssal plain mask: cellular basins `0.025` + diffuse roughness `0.008` + mottled collapse `0.012` + coarse faults `0.035` + fine faults `0.012`;
- hadal mask: rare vent/caldera depression `0.065`.

These numbers are density-function/continentalness contributions, not literal block-depth offsets. Because masks can overlap, runtime inspection is required before any further amplitude increase.

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

## Custom deep cave carvers

Two pack-owned configured carvers add real cave geometry without touching non-abyssal biomes.

### `custom_worldgen:abyssal_slope_cave`
Attached to both continental-slope biomes in addition to the existing vanilla cave/canyon set.
- probability: `0.045`
- configured vertical range: `Y -48 .. 40`
- horizontal radius multiplier: `1.2 .. 2.2`
- vertical radius multiplier: `0.55 .. 1.15`
- y-scale: `0.25 .. 0.75`
- lava floor threshold: 4 blocks above world bottom

Purpose: submerged cliff caves, shelf galleries and openings along the continental break.

### `custom_worldgen:abyssal_fracture_cave`
Attached to both fracture-field and both hadal biomes in addition to the existing vanilla cave/canyon set.
- probability: `0.065`
- configured vertical range: `Y -56 .. 16`
- horizontal radius multiplier: `1.1 .. 2.4`
- vertical radius multiplier: `0.65 .. 1.35`
- y-scale: `0.20 .. 0.90`
- lava floor threshold: 4 blocks above world bottom

Purpose: deeper fissure caves and chamber systems associated with fracture/hadal terrain.

The Wastelands router still owns aquifers. The intended result is flooded deep caves where aquifer logic permits, but actual flooding, dry pockets, entrances and submarine clearance are not claimed until runtime inspection.

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

The environmental family consumes the same depth routing without changing evidence progression:

- `pelagos_sensor_debris` → Western abyssal plain only; spacing/separation `112/56`, salt `78064401`.
- `karsic_pipeline_breach` → Eastern abyssal plain only; spacing/separation `112/56`, salt `78064402`.
- `abyssal_cold_seep` → both abyssal-plain families; spacing/separation `160/80`, salt `78064501`.
- `fracture_vent_field` → both fracture-field families; spacing/separation `176/88`, salt `78064601`.
- `hadal_vent_complex` → both hadal families; spacing/separation `224/112`, salt `78064602`.

All five project to `OCEAN_FLOOR_WG`, use single-piece jigsaw pools and `terrain_adaptation: bury`, and are generated deterministically by `tools/abyssal_rebuild/generate_abyssal_environmental_sites.py`.

The Pelagos debris and Karsic breach reuse the generic abyssal-plain salvage table. The cold seep, fracture vent field and hadal vent complex have no chest. None is quest-critical and none changes evidence progression.

`#infinite_domain:abyssal_hydrothermal_sites` groups the two vent scales; `#infinite_domain:hadal_environmental_sites` currently contains the major hadal complex.

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
1. validate all four custom noise parameter registrations and all new density-function references;
2. verify the six reference-pattern motifs appear at useful biome-scale frequencies rather than visual static;
3. verify East/West routing and transition seam;
4. inspect the central continent/mountain annulus and confirm no deformation leaks into the protected branch;
5. inspect north/south oceans for abyssal contamination;
6. measure seabed Y at shelf, slope, plain, fracture and deepest hadal candidates;
7. inspect both custom cave carvers for frequency, cave-mouth exposure, aquifer flooding and bedrock interaction;
8. verify all eight core and five optional abyssal structures resolve with `/structure_map` where applicable;
9. inspect `OCEAN_FLOOR_WG` projection, burial, open-breach flooding and chest accessibility;
10. inspect cold-seep, fracture-vent and hadal-vent bubble behavior;
11. run both slope-return voyages and both deep expedition branches end-to-end;
12. verify the seabed features scale by depth rather than making fracture/hadal terrain visually busy;
13. verify FTB mobs remain out of starter water and scale by depth;
14. assess submarine clearance through deformed slope/fracture terrain and cave entrances;
15. measure generation cost.

If continentalness-based deformation later proves too shallow, only a narrowly East/West + ocean + hadal gated final-density contribution may be considered. Global Overworld deepening remains prohibited.
