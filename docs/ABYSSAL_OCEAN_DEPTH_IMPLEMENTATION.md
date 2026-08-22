# Infinite Domain — Abyssal Ocean Depth Implementation

Authoritative parent plan: `docs/ABYSSAL_OCEAN_PROGRAM.md`

Status: **East/West depth shaping, explicit depth biomes, FTB Ocean Mobs integration, bilateral recovery quests, and salvage contracts are implemented. Runtime validation was unavailable on 2026-08-22 and explicitly waived for forward development, so terrain measurements remain unobserved rather than falsely marked proven.**

## Gate disposition

The ordinary fresh-world validation pass could not be executed during this implementation cycle. Project direction was to continue as though it had passed.

That means implementation may be promoted and downstream systems may depend on its IDs/contracts. It does **not** create fictional measurements. Seabed Y, aquifer behavior, submarine clearance, structure placement quality, encounter density, and generation cost remain deferred observations.

## Regional corridor and terrain chain

`custom_worldgen:east_west_ocean_corridor_mask` derives from the established east/west continent system and suppresses abyssal intervention in north/south-dominant geography.

The depth system uses:

- `custom_worldgen:abyssal_ocean_mask`
- `custom_worldgen:abyssal_plain_mask`
- `custom_worldgen:abyssal_fracture_mask`
- `custom_worldgen:hadal_trench_mask`
- `custom_worldgen:western_depth_depression`
- `custom_worldgen:eastern_depth_depression`
- `custom_worldgen:abyssal_outer_continents`

`custom_worldgen:continents` uses the abyssal outer function only outside the protected `central_continent_mask` branch.

Current pressure curve:

1. slope/ocean `0.05`;
2. abyssal plain `0.12`;
3. fracture/hadal `0.28`.

Fracture selection uses low-frequency shifted erosion noise. The hadal mask is constrained by both deep-water and fracture membership so the strongest depression remains localized.

## Active biome routing

| Role | Continentalness | West | East |
| --- | --- | --- | --- |
| Continental slope | `-0.60 .. -0.455` | `western_continental_slope` | `eastern_continental_slope` |
| Abyssal plain | `-0.82 .. -0.60` | `western_abyssal_plain` | `eastern_abyssal_plain` |
| Fracture field | `-1.02 .. -0.82` | `western_fracture_field` | `eastern_fracture_field` |
| Hadal trench | `-1.20 .. -1.02` | `western_hadal_trench` | `eastern_hadal_trench` |

Every band uses humidity `-1.0 .. -0.2` for West, `-0.2 .. 0.2` for the vanilla deep-ocean transition seam, and `0.2 .. 1.0` for East.

Normal ocean and extreme north/south ocean climates retain their pre-existing ownership.

## Targeting tags

Regional parents:

- `#infinite_domain:western_abyssal_biomes`
- `#infinite_domain:eastern_abyssal_biomes`

Combined depth groups:

- `#infinite_domain:abyssal_slope_biomes`
- `#infinite_domain:abyssal_plain_biomes`
- `#infinite_domain:abyssal_fracture_biomes`
- `#infinite_domain:hadal_biomes`

Each combined group is composed from separate West/East subtags. All current abyssal biomes append to vanilla ocean/deep-ocean tags with `replace: false`.

## FTB Ocean Mobs population

Nine upstream-normal Rift mobs are used; upstream no-natural-spawn entities (`rift_weaver`, `sludgeling`) remain excluded.

Western encounter progression:

- slope: rare `riftling_observer`, `abyssal_winged`;
- plain: `riftling_observer`, rare `mossback_goliath`, rare `shadow_beast`;
- fracture: `abyssal_sludge`, `shadow_beast`, rare `tentacled_horror`;
- hadal: `tentacled_horror`, rare `rift_demon`, `rift_minotaur`, `abyssal_winged`.

Eastern encounter progression:

- slope: rare `corrosive_craig`, `riftling_observer`;
- plain: `corrosive_craig`, rare `mossback_goliath`, `abyssal_sludge`;
- fracture: `corrosive_craig`, `shadow_beast`, rare `rift_minotaur`;
- hadal: `rift_demon`, `tentacled_horror`, rare `rift_minotaur`, `abyssal_sludge`.

Drowned remain a baseline and FTB weights stay conservative. Threat density rises by depth rather than enabling Rift mobs globally.

Entity loot tables live under `kubejs/data/ftboceanmobs/loot_table/entities/` and provide modest salvage/biological drops.

## Recovery quest integration

`config/ftbquests/quests/chapters/abyssal_recovery.snbt` is mechanically attached to existing Air/Sea quest `5E00000000000006` (`Ballast and Propulsion`).

### Pelagos/Western branch

- visit `western_continental_slope`;
- map/enter `minecraft:ocean_ruin_cold`;
- recover `kubejs:abyssal_navigation_core`;
- return to `infinite_domain:spawn_buffer` with the core.

### Karsic/Eastern branch

- visit `eastern_continental_slope`;
- map/enter `minecraft:ocean_ruin_warm`;
- recover `kubejs:karsic_subsea_data_recorder`;
- return to `infinite_domain:spawn_buffer` with the recorder.

The convergence milestone requires both proof items. New IDs are stable mechanical contracts; polished quest localization may be added later without changing them.

`kubejs/startup_scripts/abyssal_recovery_items.js` registers both proof items using vanilla placeholder textures under the mechanical-first rule.

## Temporary recovery-site compatibility

Current stand-ins are enabled on their intended slope families:

- Western slope -> `minecraft:has_structure/ocean_ruin_cold`
- Eastern slope -> `minecraft:has_structure/ocean_ruin_warm`

Semantic structure tags abstract those temporary targets:

- `#infinite_domain:western_abyssal_recovery_sites`
- `#infinite_domain:eastern_abyssal_recovery_sites`

The current tag members are vanilla ruins. Purpose-built Infinite Domain structure IDs should later enter/replace these tags so downstream content can keep the same semantic contract.

## Wreck and deep-salvage loot contracts

Reserved custom-structure chest tables are implemented:

- `infinite_domain:chests/abyssal/pelagos_survey_recovery`
- `infinite_domain:chests/abyssal/karsic_patrol_recovery`
- `infinite_domain:chests/abyssal/abyssal_plain_salvage`
- `infinite_domain:chests/abyssal/hadal_salvage`

The two regional wreck tables guarantee the corresponding proof item and add modest salvage. Deeper generic tables add unusual materials at controlled rates without advanced-machine or late-era bypasses.

These tables are **not injected into vanilla ocean-ruin chests**. During the temporary phase the quest reward provides story proof. The custom chest contracts are intended for the bespoke wreck structures.

## Unmeasured physical boundary

Sea level remains 48; Overworld minimum Y remains -64. The intended physical order is shelf -> slope -> abyssal plain -> fracture field -> rare hadal trench.

Still unmeasured:

- actual seabed Y per band;
- whether strongest trenches reach approximately Y -56 to -60;
- shelf/slope visual quality;
- caves/aquifers/bedrock interaction;
- practical submarine clearance;
- structure placement on steep terrain;
- generation cost;
- live encounter density under mob caps.

If future measurement shows continentalness alone is insufficient, any final-density correction must be narrowly gated by East/West + ocean + hadal masks. No global Overworld depth mutation.

## Deferred validation ledger

When runtime access returns:

1. validate density-function loading;
2. verify East/West routing and transition seam;
3. verify central continent/mountain annulus and north/south oceans;
4. measure physical depth bands;
5. inspect bedrock/caves/aquifers;
6. verify cold/warm ruin generation on slope biomes;
7. run both recovery branches end-to-end;
8. verify FTB mobs remain out of starter coasts and scale acceptably;
9. assess submarine navigation;
10. measure generation performance.

## Next implementation boundary

1. Create first-class Pelagos survey wreck and Karsic patrol wreck worldgen structure IDs, template pools, structure sets, and NBT/schematics.
2. Bind the already-created regional wreck loot tables to guaranteed evidence chests.
3. Replace vanilla ruin quest/map targets with those stable custom structure IDs while retaining the semantic structure tags and proof item IDs.
4. Add abyssal-plain, fracture, and hadal expedition sites.
5. Populate sparse biome feature lists with verified marine/geological features.
6. Add polished quest localization and bespoke proof-item art after mechanical structure integration.
