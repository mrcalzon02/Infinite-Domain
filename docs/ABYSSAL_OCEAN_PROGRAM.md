# Infinite Domain — East/West Abyssal Ocean Program

Status: **promoted under the 2026-08-22 runtime-validation waiver. Terrain shaping, six-pattern systemic seabed deformation, custom slope/fracture cave carvers, eight depth biomes, depth-graded seabed ecology/geology, FTB Ocean Mobs population/loot, two slope recovery wrecks, six accessible rebuilt deep expedition structures, physical site-specific evidence recovery, complete abyssal quest localization, and five optional environmental sites are implemented. Runtime terrain and placement observations remain deferred.**

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

The seafloor is no longer shaped only by uniform depth pressure. `custom_worldgen:abyssal_pattern_depression` is now added inside the existing Western and Eastern depth-depression functions, after which `abyssal_outer_continents` continues to feed `custom_worldgen:continents`. The global Wastelands `final_density` router was deliberately left unchanged.

## Systemic terrain-deformation vocabulary

The six supplied black/white reference-noise motifs are implemented as distinct geological processes rather than one generic noise field:

- **Cellular basins / pillow-lava fields:** `custom_worldgen:abyssal_cellular_basin_pattern`
- **Coarse rift/fault networks:** `custom_worldgen:abyssal_coarse_fracture_pattern`
- **Diffuse rough seabed:** `custom_worldgen:abyssal_diffuse_roughness_pattern`
- **Mottled collapse / pockmark provinces:** `custom_worldgen:abyssal_mottled_collapse_pattern`
- **Vent/caldera provinces:** `custom_worldgen:abyssal_vent_caldera_pattern`
- **Fine secondary crack networks:** `custom_worldgen:abyssal_fine_fracture_pattern`

Pack-owned noise parameters are `custom_worldgen:abyssal_cells`, `abyssal_faults`, `abyssal_roughness`, and `abyssal_vents`. A separate `abyssal_slope_band_mask` limits shelf/slope roughening, while the existing plain and hadal masks concentrate stronger effects at depth.

The pattern amplitudes are intentionally conservative. Slope deformation contributes at most roughly `0.020` additional continentalness depression from diffuse roughness/coarse gullies; abyssal-plain pattern terms contribute cellular, roughness, collapse, coarse-fault and fine-fault components of `0.025`, `0.008`, `0.012`, `0.035`, and `0.012`; rare hadal vent provinces add an additional `0.065` term. These are logical density-function amplitudes, not measured block-depth claims.

## Deep cave systems

Two custom configured cave carvers now add actual cave geometry in addition to surface deformation:

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

## Create Aquatic Ambitions disposition

The verified 1.21.1 upstream addon is processing/automation content, not a natural marine-worldgen provider. Verified registry content includes `create_aquatic_ambitions:mechanical_conduit`, `create_aquatic_ambitions:prismarine_alloy_block`, `create_aquatic_ambitions:prismarine_alloy`, `create_aquatic_ambitions:prismarine_alloy_rod`, `create_aquatic_ambitions:calcium_rich_powder`, `create_aquatic_ambitions:spiky_shell`, and `create_aquatic_ambitions:suspicious_rock`.

Do not scatter these as natural abyssal geology or free intact technology. Future use should be controlled through recipes, intentionally ruined/non-dropping structure props, or era-compatible salvage after progression review.

## Remaining work

1. Heavy Rebuild visual refinement on the two slope wrecks and six core deep installations while retaining stable IDs, open recovery paths and evidence contracts.
2. Expand optional environmental variants conservatively: collapsed cables, alternate sensor debris, trench-wall remnants, methane mounds, additional mineral chimneys and seep variants.
3. Runtime-tune the six deformation amplitudes and two cave-carver rates only after visual observation; do not tune from assumed depths.
4. Add bespoke evidence-item textures after mechanical content remains stable.
5. Revisit Create Aquatic Ambitions only for controlled recovered-technology integration, not natural worldgen.
6. When runtime access returns, execute the deferred validation ledger rather than retroactively claiming it already happened.

## Deferred observations

Still unmeasured:
- actual seabed Y by depth band;
- visual scale/fidelity of the six systemic deformation patterns;
- hadal approach to the intended near-bedrock target;
- custom cave frequency, cave-mouth exposure and aquifer flooding behavior;
- floor projection and burial appearance;
- open-breach flooding appearance and chest interaction;
- cold-seep/fracture-vent/hadal-vent bubble behavior;
- submarine navigation clearance through caves and around terrain deformation;
- actual mob-cap encounter density;
- structure-map behavior;
- chunk-generation cost.
