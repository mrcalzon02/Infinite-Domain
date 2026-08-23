# Infinite Domain — East/West Abyssal Ocean Program

Status: **promoted under the 2026-08-22 runtime-validation waiver. Terrain shaping, eight depth biomes, FTB Ocean Mobs population/loot, two slope recovery wrecks, six rebuilt deep expedition structures, physical site-specific evidence recovery, and bilateral submarine quest progression are implemented. Runtime terrain and placement observations remain deferred.**

## Authority

- Program/design authority: `docs/ABYSSAL_OCEAN_PROGRAM.md`
- Terrain/depth implementation record: `docs/ABYSSAL_OCEAN_DEPTH_IMPLEMENTATION.md`
- Structure blueprint authority: `docs/ABYSSAL_SITE_BLUEPRINTS.md`

Future work should update these authorities rather than create parallel plans.

## Gate disposition

Fresh-world validation was unavailable on 2026-08-22 and development was explicitly directed to continue as if the gate had passed. This permits downstream implementation to depend on the established IDs. It does not create fictional measurements. Seabed Y, aquifer behavior, actual placement quality, submarine clearance, encounter density, and generation performance remain unmeasured.

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

## FTB Ocean Mobs

Nine upstream-normal Rift mobs are depth-routed by Infinite Domain. `rift_weaver` and `sludgeling` remain excluded from natural spawning. Risk rises from rare slope incursions to the strongest normal mixtures in hadal terrain. Entity loot is pack-owned under `kubejs/data/ftboceanmobs/loot_table/entities/` and remains progression-safe.

## Active structure program

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

All eight are first-class Infinite Domain IDs with structure definitions, template pools, structure sets and semantic tags. The six deep-installation NBTs were deterministically regenerated and committed by `tools/abyssal_rebuild/generate_abyssal_sites.py`; their live Git blob hashes match the generator authority. Each deep installation now contains one site-specific evidence chest and one secondary salvage chest.

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

## Quest progression

`config/ftbquests/quests/chapters/abyssal_recovery.snbt` depends on Air/Sea quest `5E00000000000006` (`Ballast and Propulsion`).

The first two voyages recover physical evidence from the Western and Eastern slope wrecks and return it to `infinite_domain:spawn_buffer`.

After both are complete, the chapter splits into independent deep expeditions:
- Pelagos: abyssal plain → relay + physical bathymetric log → fracture observatory + physical sensor core → hadal probe + physical pressure record.
- Karsic: abyssal plain → pipeline station + physical telemetry → fracture listening post + physical sonar archive → hadal blacksite + physical cipher.

Maps lead to the next destination. Deep evidence is no longer issued by quest completion: every deep site quest requires the matching structure and the item from its guaranteed evidence chest. The final milestone requires both hadal records and produces the comparative dossier with only modest currency.

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

Evidence tables guarantee the required record and add modest salvage. No site should provide intact advanced machines, diamonds, netherite or direct era bypasses.

## Create Aquatic Ambitions disposition

The verified 1.21.1 upstream addon is processing/automation content, not a natural marine-worldgen provider. Verified registry content includes `create_aquatic_ambitions:mechanical_conduit`, `create_aquatic_ambitions:prismarine_alloy_block`, `create_aquatic_ambitions:prismarine_alloy`, `create_aquatic_ambitions:prismarine_alloy_rod`, `create_aquatic_ambitions:calcium_rich_powder`, `create_aquatic_ambitions:spiky_shell`, and `create_aquatic_ambitions:suspicious_rock`.

Do not scatter these as natural abyssal geology or free intact technology. Future use should be controlled through recipes, intentionally ruined/non-dropping structure props, or era-compatible salvage after progression review.

## Remaining work

1. Heavy Rebuild visual refinement on the two slope wrecks and six deep installations while retaining all stable IDs and evidence contracts.
2. Populate sparse biome feature lists with pack-owned marine/geological features built from verified vanilla primitives.
3. Add polished quest localization and bespoke evidence-item textures without changing stable quest IDs.
4. Add additional optional wreck/vent/seep variants only after the core eight remain mechanically stable.
5. Revisit Create Aquatic Ambitions only for controlled recovered-technology integration, not natural worldgen.
6. When runtime access returns, execute the deferred validation ledger rather than retroactively claiming it already happened.

## Deferred observations

Still unmeasured:
- actual seabed Y by depth band;
- hadal approach to the intended near-bedrock target;
- caves/aquifers/bedrock behavior;
- floor projection and burial appearance;
- dry-room flooding behavior;
- submarine navigation clearance;
- actual mob-cap encounter density;
- structure-map behavior;
- chunk-generation cost.
