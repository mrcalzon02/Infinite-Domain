# Infinite Domain — Abyssal Ocean Depth Implementation

Authoritative parent: `docs/ABYSSAL_OCEAN_PROGRAM.md`

Status: **terrain/depth routing is active under an explicit runtime-validation waiver; six reference-pattern seabed motifs plus four derived vertical-relief processes, a direct seabed-depth channel (2026-08-27), custom slope/fracture cave carvers, all eight core abyssal structures, five optional environmental structures, the depth-graded seabed feature pass, and both deep quest branches consume the resulting depth bands. Physical seabed measurements remain unobserved.**

## Gate disposition

Fresh-world validation was unavailable on 2026-08-22. Project direction was to continue as if positive. Implementation can therefore advance, but no measured terrain, flooding, navigation or performance claim is considered proven.

## Terrain chain

The active outer-world depth chain now includes the original depth masks, the six reference-pattern deformation functions, and the derived vertical-relief layer:
- `custom_worldgen:east_west_ocean_corridor_mask`
- `custom_worldgen:abyssal_ocean_mask`
- `custom_worldgen:abyssal_plain_mask`
- `custom_worldgen:abyssal_fracture_mask`
- `custom_worldgen:hadal_trench_mask`
- `custom_worldgen:abyssal_slope_band_mask`
- `custom_worldgen:abyssal_slope_edge_mask`
- `custom_worldgen:hadal_edge_mask`
- `custom_worldgen:abyssal_cellular_basin_pattern`
- `custom_worldgen:abyssal_coarse_fracture_pattern`
- `custom_worldgen:abyssal_diffuse_roughness_pattern`
- `custom_worldgen:abyssal_mottled_collapse_pattern`
- `custom_worldgen:abyssal_vent_caldera_pattern`
- `custom_worldgen:abyssal_fine_fracture_pattern`
- `custom_worldgen:abyssal_shelf_slump_pattern`
- `custom_worldgen:abyssal_exposed_cliff_pattern`
- `custom_worldgen:abyssal_trench_scarp_pattern`
- `custom_worldgen:abyssal_vent_rim_pattern`
- `custom_worldgen:abyssal_pattern_depression`
- `custom_worldgen:western_depth_depression`
- `custom_worldgen:eastern_depth_depression`
- `custom_worldgen:abyssal_outer_continents`
- `custom_worldgen:abyssal_floor_depression` (direct seabed-depth channel; see below)

The direct depth channel additionally overrides `minecraft:overworld/depth`
(alongside the existing `minecraft:overworld/continents` and
`minecraft:overworld/erosion` overrides).

`custom_worldgen:continents` uses the abyssal outer branch only outside the protected central-continent mask. The datapack-owned `minecraft:overworld/continents` override delegates to `custom_worldgen:continents`, so vanilla Overworld terrain functions such as `minecraft:overworld/sloped_cheese` consume the custom continentalness signal instead of the system merely changing biome labels. No global `final_density` mutation has been added.

Base continentalness pressure remains:
1. slope/ocean `0.05`
2. abyssal plain `0.12`
3. fracture/hadal `0.28`

The pattern layer is additional and remains inside the same East/West selector + ocean-corridor gate.

## Direct seabed-depth channel (2026-08-27)

Continentalness pressure alone cannot deepen the abyss. The vanilla
`minecraft:overworld/offset` spline over the continents coordinate is a **flat
plateau at `-0.2222`** for continentalness `-0.51 .. -1.02`, and it *rises*
toward `+0.044` past `-1.02`. Every abyssal band (plain `-0.82..-0.60`, fracture
`-1.02..-0.82`, hadal `-1.20..-1.02`) therefore lands on — or past — that
plateau, so all of the depression work above only relabels biomes and produces
essentially **no floor drop** relative to a vanilla deep ocean (seabed ~Y 35).
Pushing continentalness below `-1.02` for the hadal band was additionally
counterproductive: the spline there trends upward, so hadal could generate
*shallower* than the plain.

The fix is a direct, still-gated contribution to terrain height that bypasses the
saturated spline:

- `custom_worldgen:abyssal_floor_depression` = `flat_cache(cache_2d(clamp(0.0,
  0.55, 1.0 * max(western_depth_depression, eastern_depth_depression))))`. It
  reuses the *existing* regional depression signal unchanged, so it carries the
  same East/West selector, ocean-corridor gate, slope/plain/hadal band grading,
  and pattern texture. It is `0` everywhere outside the abyss.
- `data/minecraft/worldgen/density_function/overworld/depth.json` overrides the
  vanilla `depth` function to `y_clamped_gradient + (overworld/offset - abyssal_floor_depression)`.
  Because `depth` maps to terrain height at roughly **`-128` blocks per unit**,
  the clamp ceiling `0.55` bounds the extra drop at about **70 blocks** below the
  vanilla deep-ocean floor.
- Both `initial_density_without_jaggedness` and `sloped_cheese` consume
  `minecraft:overworld/depth`, so the preliminary-surface/aquifer view and the
  final terrain stay consistent.

Approximate resulting floor, from the vanilla deep-ocean datum (seabed ~Y 35,
sea level 63); absolute numbers are **unmeasured estimates**, the `-128 b/unit`
slope and the relative ordering are the reliable parts:

| Band | `abyssal_floor_depression` (typical) | Extra drop | Est. floor |
| --- | --- | --- | --- |
| Shelf/slope | ~0.03 ramping | ~4-8 blocks | ~Y 45 -> 30 |
| Abyssal plain | ~0.17 - 0.22 | ~22-28 blocks | ~Y 8-15 |
| Fracture field | ~0.35 - 0.50 | ~45-64 blocks | ~Y -10 to -25 |
| Hadal trench | clamped at 0.55 | ~70 blocks | ~Y -35 (>= ~25 above bedrock) |

### Tuning knobs

- The `1.0` constant multiplier inside `abyssal_floor_depression` is the global
  depth-gain knob. Raise it to deepen every band proportionally.
- The `0.55` clamp ceiling is the bedrock guard for the hadal floor. Do not
  raise it without confirming the hadal seabed stays clear of `-64` in world.
- Per-band shaping still lives in `western_depth_depression` /
  `eastern_depth_depression` (the `0.05 / 0.12 / 0.28` mask coefficients) and in
  `abyssal_pattern_depression`; both now translate to real relief instead of
  being absorbed by the spline plateau, so their existing amplitudes are worth
  re-checking against the first in-world observation.

## Seafloor structure seating fix (2026-08-27)

All 64 `kubejs/data/infinite_domain/worldgen/structure/abyssal/*.json` used
`start_height: {absolute: 32}` together with `project_start_to_heightmap:
OCEAN_FLOOR_WG`. `start_height` is a **signed offset added to the projected
seabed height**, not an absolute Y when a heightmap projection is present, so
every abyssal structure's start piece generated **32 blocks above the seabed**.
With `terrain_adaptation: bury` the beardifier then filled that piece's bounding
box (plus a 6-block taper) with solid terrain, which the ocean-floor surface
rule finished as dirt/gravel: a **floating, chunk-aligned square dirt block
hanging above the abyssal plain**, repeated at every structure site.

All 64 files are now `start_height: {absolute: 0}` (template `y=0` seats on the
seabed), matching the `deep_sea/*` seabed convention and every heightmap-projected
structure elsewhere in the pack. `terrain_adaptation: bury` is unchanged and is
still recorded in the abyssal feature catalogs; whether `bury` or `none` reads
better for the taller vent/chimney features is a deferred in-world call.
`tools/abyssal_worldgen/validate_abyssal_deformation.py` now fails if any
heightmap-projected abyssal structure regains a non-zero `start_height`.

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

## Derived vertical-relief processes

The six reference motifs are now recombined into four boundary-sensitive geological processes intended to create readable height transitions rather than only mottled horizontal depth variation.

### Shelf-edge slump selector
`custom_worldgen:abyssal_slope_edge_mask` is derived as approximately `4 × slope × (1 - slope)`. It peaks along the transition edges of the continental-slope mask rather than across the full slope interior.

`custom_worldgen:abyssal_shelf_slump_pattern` multiplies that boundary selector by the mottled-collapse pattern. Its purpose is localized slump bowls, failed sediment shelves and scalloped continental-break deformation.

### Exposed continental-break faces
`custom_worldgen:abyssal_exposed_cliff_pattern` multiplies the full slope band by the stronger of the coarse and fine fracture selectors. This creates line-like gullies and fault cuts through the slope, increasing the chance that the continental break reads as scarred cliff terrain rather than a smooth descending plane.

### Hadal trench-wall scarps
`custom_worldgen:hadal_edge_mask` is derived as approximately `4 × hadal × (1 - hadal)` and therefore concentrates on the boundary of the hadal selector.

`custom_worldgen:abyssal_trench_scarp_pattern` multiplies that edge band by the stronger coarse/fine fracture contour. It deepens narrow faulted portions of the trench boundary, producing sharper wall relief without globally lowering the entire hadal floor.

### Hydrothermal caldera rims
`custom_worldgen:abyssal_vent_rim_pattern` is derived as approximately `4 × vent × (1 - vent)` from the existing normalized vent-caldera selector. This creates a contour band around the strongest vent peaks.

The rim enters `abyssal_pattern_depression` with a **negative** coefficient. Because the regional depth depression is later subtracted from continentalness, this negative term locally reduces the depression and therefore acts as an uplift. The existing positive vent-caldera term still depresses the core. Together they form a depressed vent/caldera center with a raised surrounding rim rather than a featureless bowl.

### Pattern amplitudes

`custom_worldgen:abyssal_pattern_depression` now applies:
- slope base: diffuse roughness `+0.008` + coarse gully/fault `+0.012`;
- shelf-edge slump: `+0.018`;
- exposed continental-break cliff/fault cuts: `+0.014`;
- abyssal plain mask: cellular basins `+0.025` + diffuse roughness `+0.008` + mottled collapse `+0.012` + coarse faults `+0.035` + fine faults `+0.012`;
- hadal vent/caldera core: `+0.065`;
- hydrothermal vent rim: `-0.018`;
- hadal trench-wall scarp cuts: `+0.040`.

Positive values increase the regional depth-depression term and therefore deepen the terrain contribution. The negative vent-rim value reduces that depression locally and creates relative uplift. These numbers are density-function/continentalness contributions, not literal block-depth offsets. Because masks can overlap, runtime inspection is required before any further amplitude increase.

## Static deformation integrity gate

`tools/abyssal_worldgen/validate_abyssal_deformation.py` statically verifies that:
- all four pack-owned noise registrations exist;
- all six supplied reference motifs exist;
- both boundary helper masks remain attached to the correct slope/hadal selectors;
- all four derived vertical-relief processes reference their intended base masks/patterns;
- all ten deformation processes feed `abyssal_pattern_depression`;
- both regional depression functions retain the East/West selector and ocean-corridor gate;
- `abyssal_outer_continents` and the protected `custom_worldgen:continents` branch remain connected;
- `minecraft:overworld/continents` continues delegating to `custom_worldgen:continents`;
- the Wastelands router still consumes that continentalness signal and still uses the vanilla Overworld terrain-density chain;
- custom slope/fracture cave carvers remain attached only to their intended biome bands.

`.github/workflows/abyssal-deformation-integrity.yml` runs this validator whenever the relevant density functions, noises, Wastelands noise settings, biome definitions, validator, or workflow change.

This gate proves static connectivity, not runtime appearance.

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
1. run `python tools/abyssal_worldgen/validate_abyssal_deformation.py` and confirm the static graph passes before opening a world;
2. validate all four custom noise parameter registrations and all density-function references at datapack load;
3. verify the six reference-pattern motifs appear at useful biome-scale frequencies rather than visual static;
4. inspect shelf-edge slump bowls and exposed continental-break fault cuts for readable vertical relief rather than noisy corrugation;
5. inspect hadal trench-wall scarp bands for real wall relief without fragmenting the entire trench boundary;
6. inspect vent provinces for a depressed caldera core plus raised rim rather than inverted or flat relief;
7. verify East/West routing and transition seam;
8. inspect the central continent/mountain annulus and confirm no deformation leaks into the protected branch;
9. inspect north/south oceans for abyssal contamination;
10. measure seabed Y at shelf, slope, plain, fracture and deepest hadal candidates, and confirm the direct depth channel produces a readable slope -> plain -> fracture -> hadal descent (plain clearly below vanilla deep ocean, hadal well clear of bedrock);
10a. re-tune the `abyssal_floor_depression` gain (`1.0`) and clamp (`0.55`), and the `western/eastern_depth_depression` band coefficients, against that first measurement;
10b. confirm no floating square dirt blocks remain above any abyssal structure (the `start_height` 32 -> 0 fix), and decide `bury` vs `none` for the tall vent/chimney features;
11. inspect both custom cave carvers for frequency, cave-mouth exposure, aquifer flooding and bedrock interaction;
12. verify all eight core and five optional abyssal structures resolve with `/structure_map` where applicable;
13. inspect `OCEAN_FLOOR_WG` projection, burial, open-breach flooding and chest accessibility;
14. inspect cold-seep, fracture-vent and hadal-vent bubble behavior;
15. run both slope-return voyages and both deep expedition branches end-to-end;
16. verify the seabed features scale by depth rather than making fracture/hadal terrain visually busy;
17. verify FTB mobs remain out of starter water and scale by depth;
18. assess submarine clearance through deformed slope/fracture terrain and cave entrances;
19. measure generation cost.

Continentalness-based deformation proved too shallow (the `-0.2222` offset-spline
plateau). The response was the narrowly East/West + ocean-corridor + depth-band
gated `minecraft:overworld/depth` contribution described under **Direct
seabed-depth channel** above — the sanctioned escape hatch, applied as a
`depth`/`offset` delta rather than a raw `final_density` term so aquifers and the
preliminary surface stay consistent. Global Overworld deepening remains
prohibited: `abyssal_floor_depression` is identically `0` outside the gated
abyss.
