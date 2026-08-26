# Infinite Domain — East/West Abyssal Ocean Program

Status: **promoted under the 2026-08-22 runtime-validation waiver. Terrain shaping, six reference-pattern seabed motifs plus four derived vertical-relief processes, custom slope/fracture cave carvers, eight depth biomes, depth-graded seabed ecology/geology, FTB Ocean Mobs population/loot, two slope recovery wrecks, six accessible rebuilt deep expedition structures, physical site-specific evidence recovery, complete abyssal quest localization, and five optional environmental sites are implemented. Runtime terrain and placement observations remain deferred.**

## Authority

- Program/design authority: `docs/ABYSSAL_OCEAN_PROGRAM.md`
- Terrain/depth implementation record: `docs/ABYSSAL_OCEAN_DEPTH_IMPLEMENTATION.md`
- Core structure blueprint authority: `docs/ABYSSAL_SITE_BLUEPRINTS.md`
- Optional environmental-site authority: `docs/ABYSSAL_ENVIRONMENTAL_SITES.md`

Future work should update these authorities rather than create parallel plans.

## Gate disposition

Fresh-world validation was unavailable on 2026-08-22 and development was explicitly directed to continue as if the gate had passed. This permits downstream implementation to depend on the established IDs. It does not create fictional measurements. Seabed Y, aquifer behavior, actual placement quality, submarine clearance, encounter density, terrain-pattern appearance, and generation performance remain unmeasured.

## Regional identity

### Western Abyss — Pelagos
Maritime science, oceanography, subsea power/communications, survey systems, observation facilities and research salvage. Builds favor copper/prismarine, readable instrumentation and navigable approaches.

### Eastern Abyss — Karsic
Industrial/military logistics, pipelines, passive surveillance, strategic research, patrol wreckage and restricted facilities. Builds favor deepslate armor, iron barriers, red warning systems, pipelines and heavier protected volumes.

## Active geography

The established Wastelands worldgen remains authoritative. Abyssal intervention uses the existing East/West gradient and `custom_worldgen:east_west_ocean_corridor_mask`; north/south oceans and the protected central continent retain separate ownership.

Current continentalness bands:
- slope: `-0.60 .. -0.455`
- abyssal plain: `-0.82 .. -0.60`
- fracture field: `-1.02 .. -0.82`
- hadal trench: `-1.20 .. -1.02`

West uses negative regional humidity, East positive regional humidity, and `-0.2 .. 0.2` remains a vanilla deep-ocean transition seam.

The seafloor is no longer shaped only by uniform depth pressure. `custom_worldgen:abyssal_pattern_depression` is added inside the existing Western and Eastern depth-depression functions, after which `abyssal_outer_continents` continues to feed `custom_worldgen:continents`. The datapack-owned `minecraft:overworld/continents` override delegates to that same custom signal, allowing vanilla Overworld terrain-density functions such as `minecraft:overworld/sloped_cheese` to consume the deformation chain. The global Wastelands `final_density` router itself remains unchanged.

## Systemic terrain-deformation vocabulary

The six supplied black/white reference-noise motifs are implemented as distinct geological processes rather than one generic noise field:

- **Cellular basins / pillow-lava fields:** `custom_worldgen:abyssal_cellular_basin_pattern`
- **Coarse rift/fault networks:** `custom_worldgen:abyssal_coarse_fracture_pattern`
- **Diffuse rough seabed:** `custom_worldgen:abyssal_diffuse_roughness_pattern`
- **Mottled collapse / pockmark provinces:** `custom_worldgen:abyssal_mottled_collapse_pattern`
- **Vent/caldera provinces:** `custom_worldgen:abyssal_vent_caldera_pattern`
- **Fine secondary crack networks:** `custom_worldgen:abyssal_fine_fracture_pattern`

Pack-owned noise parameters are `custom_worldgen:abyssal_cells`, `abyssal_faults`, `abyssal_roughness`, and `abyssal_vents`. `abyssal_slope_band_mask` limits shelf/slope roughening, while the existing plain and hadal masks concentrate stronger effects at depth.

### Derived vertical-relief layer

Four additional processes recombine those base motifs around depth boundaries so the abyss can produce actual relief transitions instead of only horizontally mottled depth:

- **Shelf-edge slump fields:** `custom_worldgen:abyssal_shelf_slump_pattern` uses a new `abyssal_slope_edge_mask` multiplied by the mottled-collapse field. The edge mask is approximately `4 × slope × (1 - slope)`, concentrating failed-shelf bowls and scalloped sediment collapse around the continental break.
- **Exposed continental-break faces:** `custom_worldgen:abyssal_exposed_cliff_pattern` applies the stronger of the coarse/fine fracture contours across the slope band, creating line-like gullies and fault cuts through the descending shelf/cliff region.
- **Hadal trench-wall scarps:** `custom_worldgen:abyssal_trench_scarp_pattern` uses a new `hadal_edge_mask`, approximately `4 × hadal × (1 - hadal)`, multiplied by the stronger fracture contour. This deepens selected portions of trench boundaries rather than uniformly lowering the hadal floor.
- **Hydrothermal uplift/caldera rims:** `custom_worldgen:abyssal_vent_rim_pattern` is approximately `4 × vent × (1 - vent)`. It surrounds the strongest vent/caldera peaks and enters the depression mix with a negative coefficient, producing relative uplift around the still-positive depressed caldera core.

The combined amplitudes are intentionally conservative:
- slope base roughness/fault terms: `+0.008` and `+0.012`;
- shelf-edge slump: `+0.018`;
- exposed continental-break fault/cliff cuts: `+0.014`;
- abyssal-plain cellular/roughness/collapse/coarse/fine terms: `+0.025`, `+0.008`, `+0.012`, `+0.035`, `+0.012`;
- hadal vent/caldera core: `+0.065`;
- hydrothermal raised rim: `-0.018`;
- trench-wall scarp cuts: `+0.040`.

Positive terms increase the regional depth-depression contribution. The negative vent-rim term reduces the local depression and therefore creates relative uplift. These are logical density-function amplitudes, not measured block-depth claims.

### Static integrity protection

`tools/abyssal_worldgen/validate_abyssal_deformation.py` now verifies the entire static chain: all four noise registrations, all six reference motifs, both boundary helper masks, all four derived vertical processes, the shared depression mix, East/West ocean gating, the protected central-continent branch, the `minecraft:overworld/continents` terrain bridge, the active Wastelands router connection, and the band-specific cave-carver attachments.

`.github/workflows/abyssal-deformation-integrity.yml` runs the validator whenever the relevant worldgen or biome files change. This is a static connectivity gate only; it does not replace fresh-world visual validation.

## Deep cave systems

Two custom configured cave carvers add actual cave geometry in addition to surface deformation:

- `custom_worldgen:abyssal_slope_cave` is appended only to both continental-slope biomes. Probability `0.045`, configured `Y -48 .. 40`, broad horizontal multiplier `1.2 .. 2.2`. Its purpose is cliff caves, shelf caverns and submerged galleries.
- `custom_worldgen:abyssal_fracture_cave` is appended only to both fracture-field and both hadal biomes. Probability `0.065`, configured `Y -56 .. 16`, horizontal multiplier `1.1 .. 2.4`. Its purpose is deeper fissure caverns and fracture-connected voids.

They supplement rather than replace the vanilla cave/canyon carvers. Aquifers remain responsible for fluid behavior; flooded appearance and cave-mouth accessibility remain runtime-unmeasured.

## Biome families

Western:
- `western_continental_slope`
- `western_abyssal_plain`
- `western_fracture_field`
- `western_hadal_trench`

Eastern:
- `eastern_continental_slope`
- `eastern_abyssal_plain`
- `eastern_fracture_field`
- `eastern_hadal_trench`

Compatibility IDs `western_abyssal_ocean` and `eastern_abyssal_ocean` remain retained.

## Seabed ecology and geology profile

The custom depth biomes no longer carry empty feature arrays. Only verified vanilla 1.21.1 placed-feature IDs are used in the first population pass.

- **Continental slopes:** `underwater_magma`, sand/clay/gravel disks, deep seagrass and cold kelp. Pelagos uses `seagrass_deep_cold`; Karsic uses `seagrass_deep`.
- **Abyssal plains:** `underwater_magma`, clay/gravel disks, and sparse deep seagrass. Kelp is absent.
- **Fracture fields:** `underwater_magma` plus gravel disks; no vegetation.
- **Hadal trenches:** `underwater_magma` only; no vegetation or sediment-disk decoration.

This intentionally strips biological clutter with depth instead of copying ordinary deep-ocean decoration downward. Live density and visual quality remain unmeasured under the waiver.

## FTB Ocean Mobs

Nine upstream-normal Rift mobs are depth-routed by Infinite Domain. `rift_weaver` and `sludgeling` remain excluded from natural spawning. Risk rises from rare slope incursions to the strongest normal mixtures in hadal terrain. Entity loot is pack-owned under `kubejs/data/ftboceanmobs/loot_table/entities/` and remains progression-safe.

### Spawning index

Spawns are declared directly in each depth biome's `spawners.monster` array (no separate spawn-placement/biome-modifier layer). `minecraft:drowned` is always present as the baseline monster; `creature_spawn_probability` falls with depth (`0.1` slope → `0.04` hadal), and West (Pelagos) and East (Karsic) draw slightly different mixes at the same depth tier.

| Biome | Region | Depth tier | Rift monster spawns (weight) |
|---|---|---|---|
| `western_continental_slope` | Pelagos | Slope | `riftling_observer` (1), `abyssal_winged` (1) |
| `eastern_continental_slope` | Karsic | Slope | `corrosive_craig` (1), `riftling_observer` (1) |
| `western_abyssal_plain` | Pelagos | Plain | `riftling_observer` (2), `mossback_goliath` (1), `shadow_beast` (1) |
| `eastern_abyssal_plain` | Karsic | Plain | `corrosive_craig` (2), `mossback_goliath` (1), `abyssal_sludge` (1) |
| `western_fracture_field` | Pelagos | Fracture | `abyssal_sludge` (2), `shadow_beast` (2), `tentacled_horror` (1) |
| `eastern_fracture_field` | Karsic | Fracture | `corrosive_craig` (2), `shadow_beast` (2), `rift_minotaur` (1) |
| `western_hadal_trench` | Pelagos | Hadal | `tentacled_horror` (2), `rift_demon` (1), `rift_minotaur` (1), `abyssal_winged` (1) |
| `eastern_hadal_trench` | Karsic | Hadal | `rift_demon` (2), `tentacled_horror` (2), `rift_minotaur` (1), `abyssal_sludge` (1) |
| `western_abyssal_ocean` / `eastern_abyssal_ocean` (compat IDs) | — | — | none; vanilla drowned/cod/salmon/squid/dolphin only |

Per-mob depth range (shallowest → deepest biome it appears in):

| Mob | Depth range | Notes |
|---|---|---|
| `riftling_observer` | Slope → Plain | Both regions; scout/scanner archetype |
| `abyssal_winged` | Slope → Hadal (West only) | Skips Plain/Fracture; flies between shallow and deep |
| `corrosive_craig` | Slope → Fracture (East only) | Karsic-exclusive corrosive line |
| `mossback_goliath` | Plain only | Both regions; mid-depth organic tank |
| `abyssal_sludge` | Plain (East) → Fracture (West) → Hadal (East) | Widest depth spread |
| `shadow_beast` | Plain (West) → Fracture (both) | Mid-to-deep |
| `tentacled_horror` | Fracture (West) → Hadal (both) | Deep ambush specialist |
| `rift_minotaur` | Fracture (East) → Hadal (both) | Deep specialist, Karsic-leaning |
| `rift_demon` | Hadal only (both) | Deepest, most dangerous; hadal-exclusive |

### Chemical production loot families

Beyond vanilla/ocean drops, each of the nine spawning mobs also carries a small `petrochem` byproduct pool so hadal-tier hunting feeds the Petrochemical Civilization chain (Mekanism is not installed in this pack; `petrochem:sulfur_dust` and `petrochem:salt_dust` are the established cross-mod chemistry hub items, already sold Era-3-gated through the Chemical Cooperative echo trader and bridged 1:1 into `immersiveengineering:dust_sulfur`, `tfmg:sulfur_dust`, and `the_wasteland_reworked:sulfur_dust`). Two families:

- **Sulfur/vent line** (`petrochem:sulfur_dust`, rare `petrochem:petroleum_coke` on the two deepest predators) — corrosive, brimstone, and smoke-themed mobs: `corrosive_craig`, `abyssal_winged`, `shadow_beast`, `rift_minotaur`, `tentacled_horror`, `rift_demon`.
- **Brine/salt line** (`petrochem:salt_dust`) — ooze, sediment, and filter-feeder mobs: `abyssal_sludge`, `mossback_goliath`, `riftling_observer`, `rift_minotaur`.

Chance and count scale with depth tier (shallow specialists ~0.15 chance ×1, hadal specialists up to ~0.5 chance ×2-3, with `petroleum_coke` capped at 0.08-0.12 chance ×1), matching the reward-bag Era 3 tuning for the same items. These are raw feedstock drops only — no fluid buckets, finished chemicals, or machines — consistent with the loot doctrine below.

Each of the nine mobs also carries one low-chance Era 3 process-equipment component (0.06-0.2 chance, matching the Era Reward Bag doctrine of "useful inputs and subassemblies, never complete gateway machines"), giving hunting a secondary payoff beyond raw dusts:

| Mob | Component drop |
|---|---|
| `riftling_observer` | `petrochem:tin_nugget` |
| `abyssal_winged` | `petrochem:tin_nugget` |
| `corrosive_craig` | `petrochem:steel_sheet` |
| `mossback_goliath` | `petrochem:bronze_sheet` |
| `abyssal_sludge` | `petrochem:steel_fluid_valve` |
| `shadow_beast` | `petrochem:bronze_sheet` |
| `rift_minotaur` | `petrochem:steel_fluid_pipe` |
| `tentacled_horror` | `petrochem:steel_fluid_pipe` |
| `rift_demon` | `petrochem:steel_fluid_tank` (rarest, 0.06 chance — the deepest/most dangerous mob yields the most valuable salvage) |

## Core structure program

Slope recovery:
- `infinite_domain:abyssal/pelagos_survey_wreck`
- `infinite_domain:abyssal/karsic_patrol_wreck`

Abyssal plain:
- `infinite_domain:abyssal/pelagos_abyssal_relay`
- `infinite_domain:abyssal/karsic_abyssal_pipeline_station`

Fracture field:
- `infinite_domain:abyssal/pelagos_fracture_observatory`
- `infinite_domain:abyssal/karsic_fracture_listening_post`

Hadal:
- `infinite_domain:abyssal/pelagos_hadal_probe_station`
- `infinite_domain:abyssal/karsic_hadal_blacksite`

All eight are first-class Infinite Domain IDs with structure definitions, template pools, structure sets and semantic tags.

The six deep installations are deterministically generated by `tools/abyssal_rebuild/generate_abyssal_sites.py`. The generator contains the authoritative expected Git blob hashes and the materialization workflow calls its `--verify` path before publishing binaries. Every current deep installation has an intentional 3 × 3 underwater swim-through opening; the Karsic blacksite additionally opens its inner archive vault. These are flooded/open-breach ruins, not claimed dry habitats.

## Optional environmental site family

The non-critical environmental family is active and intentionally separate from the evidence quest chain:

- `infinite_domain:abyssal/pelagos_sensor_debris` — Western abyssal-plain scientific debris with one generic plain-salvage chest; spacing/separation `112/56`.
- `infinite_domain:abyssal/karsic_pipeline_breach` — Eastern abyssal-plain industrial rupture with one generic plain-salvage chest; spacing/separation `112/56`.
- `infinite_domain:abyssal/abyssal_cold_seep` — neutral clay/mud/calcite/soul-sand seep across both abyssal plains; no chest; spacing/separation `160/80`.
- `infinite_domain:abyssal/fracture_vent_field` — neutral magma/basalt/blackstone black-smoker field across both fracture families; no chest; spacing/separation `176/88`.
- `infinite_domain:abyssal/hadal_vent_complex` — rare 31 × 18 × 31 caldera and eight-chimney hydrothermal province across both hadal families; no chest; spacing/separation `224/112`.

The two vent structures provide different geological scales rather than duplicate scenery: commoner small fracture vents versus uncommon major hadal provinces.

These are generated by `tools/abyssal_rebuild/generate_abyssal_environmental_sites.py`, which imports the shared NBT serializer from the core generator and verifies five expected blob hashes. The hadal vent complex is locked to Git blob `cc17b36102636467d7fa10986e86cabb86e59b57`.

Environmental semantic tags:
- `#infinite_domain:abyssal_plain_environmental_sites`
- `#infinite_domain:fracture_environmental_sites`
- `#infinite_domain:hadal_environmental_sites`
- `#infinite_domain:abyssal_hydrothermal_sites`
- `#infinite_domain:abyssal_environmental_sites`

Their purpose is to give the abyss occasional geological and historical texture without making the deep ocean feel crowded. They do not carry unique evidence or quest dependencies.

## Evidence progression

Slope wreck evidence:
- `kubejs:abyssal_navigation_core`
- `kubejs:karsic_subsea_data_recorder`

Deep Pelagos evidence:
- `kubejs:pelagos_bathymetric_log`
- `kubejs:pelagos_fracture_sensor_core`
- `kubejs:pelagos_hadal_pressure_record`

Deep Karsic evidence:
- `kubejs:karsic_pipeline_telemetry`
- `kubejs:karsic_sonar_archive`
- `kubejs:karsic_hadal_blacksite_cipher`

Convergence:
- `kubejs:abyssal_comparative_dossier`

`kubejs/startup_scripts/abyssal_recovery_items.js` is the single registry authority for these items.

## Quest progression and localization

`config/ftbquests/quests/chapters/abyssal_recovery.snbt` depends on Air/Sea quest `5E00000000000006` (`Ballast and Propulsion`). The first two voyages recover physical evidence from the Western and Eastern slope wrecks and return it to `infinite_domain:spawn_buffer`.

After both are complete, the chapter splits into independent deep expeditions:
- Pelagos: abyssal plain → relay + physical bathymetric log → fracture observatory + physical sensor core → hadal probe + physical pressure record.
- Karsic: abyssal plain → pipeline station + physical telemetry → fracture listening post + physical sonar archive → hadal blacksite + physical cipher.

Maps lead to the next destination. Deep evidence is not issued by quest completion: every deep site quest requires the matching structure and the item from its guaranteed evidence chest. The final milestone requires both hadal records and produces the comparative dossier with only modest currency.

The chapter and all sixteen quest nodes now have explicit English titles/descriptions in the existing `config/ftbquests/quests/lang/en_us.snbt` authority. `tools/abyssal_rebuild/update_quest_localization.py` installs the block idempotently and refuses partial/conflicting overwrites.

## Loot doctrine

Site-specific chest tables:
- `pelagos_survey_recovery`
- `karsic_patrol_recovery`
- `pelagos_abyssal_relay`
- `pelagos_fracture_observatory`
- `pelagos_hadal_probe`
- `karsic_pipeline_station`
- `karsic_listening_post`
- `karsic_hadal_blacksite`

Shared salvage:
- `abyssal_plain_salvage`
- `hadal_salvage`

Evidence tables guarantee the required record and add modest salvage. Environmental faction debris reuses `abyssal_plain_salvage`; neutral geological sites contain no chest. No site should provide intact advanced machines, diamonds, netherite or direct era bypasses.

Entity loot (the nine spawning Rift mobs) follows the same doctrine: raw vanilla/ocean materials plus the two `petrochem` chemistry-family dusts described above, never fluid buckets, finished chemicals, or machine parts.

## Create Aquatic Ambitions disposition

The verified 1.21.1 upstream addon is processing/automation content, not a natural marine-worldgen provider. Verified registry content includes `create_aquatic_ambitions:mechanical_conduit`, `create_aquatic_ambitions:prismarine_alloy_block`, `create_aquatic_ambitions:prismarine_alloy`, `create_aquatic_ambitions:prismarine_alloy_rod`, `create_aquatic_ambitions:calcium_rich_powder`, `create_aquatic_ambitions:spiky_shell`, and `create_aquatic_ambitions:suspicious_rock`.

Do not scatter these as natural abyssal geology or free intact technology. Future use should be controlled through recipes, intentionally ruined/non-dropping structure props, or era-compatible salvage after progression review.

## Remaining work

1. Heavy Rebuild visual refinement on the two slope wrecks and six core deep installations while retaining stable IDs, open recovery paths and evidence contracts.
2. Expand optional environmental variants conservatively: collapsed cables, alternate sensor debris, trench-wall remnants, methane mounds, additional mineral chimneys and seep variants.
3. Runtime-tune the six base deformation motifs, four derived vertical-relief processes, and two cave-carver rates only after visual observation; do not tune from assumed depths.
4. Add bespoke evidence-item textures after mechanical content remains stable.
5. Revisit Create Aquatic Ambitions only for controlled recovered-technology integration, not natural worldgen.
6. When runtime access returns, execute the deferred validation ledger rather than retroactively claiming it already happened.

## Deferred observations

Still unmeasured:
- actual seabed Y by depth band;
- visual scale/fidelity of the six systemic reference motifs;
- shelf-edge slump frequency and the visual steepness of exposed continental-break faces;
- hadal trench-wall scarp scale and continuity;
- whether hydrothermal provinces visibly form a depressed core with a raised rim;
- hadal approach to the intended near-bedrock target;
- custom cave frequency, cave-mouth exposure and aquifer flooding behavior;
- floor projection and burial appearance;
- open-breach flooding appearance and chest interaction;
- cold-seep/fracture-vent/hadal-vent bubble behavior;
- submarine navigation clearance through caves and around terrain deformation;
- actual mob-cap encounter density;
- structure-map behavior;
- chunk-generation cost.
