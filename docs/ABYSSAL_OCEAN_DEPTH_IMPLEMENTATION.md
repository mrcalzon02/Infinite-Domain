# Infinite Domain — Abyssal Ocean Depth Implementation

Authoritative parent plan: `docs/ABYSSAL_OCEAN_PROGRAM.md`

Status: **East/West depth shaping is active; depth-specific biomes, FTB Ocean Mobs integration, and the first submarine recovery voyage are implemented. Runtime validation was unavailable on 2026-08-22 and explicitly waived for forward development, so physical Y-level claims remain unmeasured rather than falsely marked proven.**

## Development gate disposition

The ordinary fresh-world gate was not executable during this implementation pass. Project direction was to continue as if the gate were positive.

For status purposes this means:

- implementation may be promoted and extended;
- downstream content may depend on the new biome/depth contracts;
- unavailable runtime observations are retained in the deferred validation ledger;
- no fabricated terrain measurements or performance claims are permitted.

This document therefore separates **implemented** from **measured**.

## Regional corridor gate

`custom_worldgen:east_west_ocean_corridor_mask` derives from the established east/west continent system. It suppresses abyssal intervention in north/south-dominant geography and ramps toward full strength in the east/west continental wedges.

`custom_worldgen:regional_east_west_gradient` regionalizes the signed east/west gradient before it feeds the normal humidity authority outside protected start and mountain masks.

The result is one geographic authority for both terrain and biome identity rather than duplicated coordinate logic.

## Active depth masks

The current depth chain is decomposed into reusable functions:

- `custom_worldgen:abyssal_ocean_mask`
- `custom_worldgen:abyssal_plain_mask`
- `custom_worldgen:abyssal_fracture_mask`
- `custom_worldgen:hadal_trench_mask`

The fracture mask uses low-frequency shifted erosion noise. The hadal mask is constrained by established deep-water terrain plus fracture selection so the strongest depression is intended to form uncommon trench corridors rather than a uniformly bottomed-out ocean.

These masks operate from `outer_directional_continents`, avoiding recursion through the final `custom_worldgen:continents` function.

## Separate Eastern and Western depression files

Regional terrain pressure is independently addressable through:

- `custom_worldgen:western_depth_depression`
- `custom_worldgen:eastern_depth_depression`

Both currently use the same initial pressure curve:

1. ocean/slope: `0.05`;
2. abyssal plain: `0.12`;
3. fracture/hadal: `0.28`.

They remain separate so later tuning can broaden/terrace the Western seabed and sharpen or increase trench density in the Eastern seabed without replacing the shared masks.

## Continentalness integration

`custom_worldgen:abyssal_outer_continents` subtracts the stronger applicable regional depression from `outer_directional_continents`, then clamps the result to `-1.2 .. 1.0`.

`custom_worldgen:continents` uses `abyssal_outer_continents` only for the outer-world branch of `central_continent_mask`. The protected central-continent branch is unchanged.

This is an active terrain integration, not a reserved scaffold.

## Active biome routing bands

The temperate deep-ocean continentalness range is subdivided as follows:

| Role | Continentalness | West | East |
| --- | --- | --- | --- |
| Continental slope | `-0.60 .. -0.455` | `western_continental_slope` | `eastern_continental_slope` |
| Abyssal plain | `-0.82 .. -0.60` | `western_abyssal_plain` | `eastern_abyssal_plain` |
| Fracture field | `-1.02 .. -0.82` | `western_fracture_field` | `eastern_fracture_field` |
| Hadal trench | `-1.20 .. -1.02` | `western_hadal_trench` | `eastern_hadal_trench` |

For every band:

- humidity `-1.0 .. -0.2` routes West;
- humidity `-0.2 .. 0.2` remains vanilla `minecraft:deep_ocean` as a transition seam;
- humidity `0.2 .. 1.0` routes East.

Normal temperate ocean above the deep-ocean boundary remains vanilla. The extreme north/south ocean rules retain their pre-existing climate ownership.

## Targeting tags

Depth and region are both first-class targeting dimensions.

Regional parents:

- `#infinite_domain:western_abyssal_biomes`
- `#infinite_domain:eastern_abyssal_biomes`

Combined depth groups:

- `#infinite_domain:abyssal_slope_biomes`
- `#infinite_domain:abyssal_plain_biomes`
- `#infinite_domain:abyssal_fracture_biomes`
- `#infinite_domain:hadal_biomes`

Each combined depth group is built from corresponding independent Eastern and Western subtags.

All current abyssal depth biomes are appended to vanilla ocean/deep-ocean biome tags with `replace: false`.

## FTB Ocean Mobs population

The upstream FTB Ocean Mobs registry was checked before population work. Nine ordinary Rift mobs are eligible for normal placement; the Rift Weaver and sludgeling are explicitly no-natural-spawn entities and remain excluded.

Implemented encounter policy:

### Western slope

- drowned baseline
- rare `riftling_observer`
- rare `abyssal_winged`

### Western abyssal plain

- stronger drowned baseline
- `riftling_observer`
- rare `mossback_goliath`
- rare `shadow_beast`

### Western fracture field

- `abyssal_sludge`
- `shadow_beast`
- rare `tentacled_horror`

### Western hadal trench

- `tentacled_horror`
- rare `rift_demon`
- rare `rift_minotaur`
- rare `abyssal_winged`

### Eastern slope

- drowned baseline
- rare `corrosive_craig`
- rare `riftling_observer`

### Eastern abyssal plain

- `corrosive_craig`
- rare `mossback_goliath`
- rare `abyssal_sludge`

### Eastern fracture field

- `corrosive_craig`
- `shadow_beast`
- rare `rift_minotaur`

### Eastern hadal trench

- `rift_demon`
- `tentacled_horror`
- rare `rift_minotaur`
- rare `abyssal_sludge`

The spawn weights are intentionally conservative relative to drowned populations; risk increases by depth rather than making all oceans globally hostile.

## FTB Ocean Mobs loot ownership

Entity loot tables are now supplied by Infinite Domain under:

`kubejs/data/ftboceanmobs/loot_table/entities/`

All nine naturally placeable mobs receive modest material/salvage drops. The tables avoid advanced machines, diamonds, netherite, or other direct progression bypasses. Rare items such as nautilus shell, echo shard, or crying obsidian are low-probability trophies rather than guaranteed farm outputs.

Bespoke biological samples or research items can replace/extend these vanilla-material stand-ins later without changing spawn routing.

## First expedition contract

`config/ftbquests/quests/chapters/abyssal_recovery.snbt` implements the first submarine recovery line.

It cross-depends on existing Air/Sea quest `5E00000000000006` (`Ballast and Propulsion`) and therefore does not duplicate the submarine construction ladder.

Mechanical sequence:

1. visit `infinite_domain:western_continental_slope`;
2. receive a map to `minecraft:ocean_ruin_cold`;
3. enter the ruin;
4. receive `kubejs:abyssal_navigation_core`;
5. return to `infinite_domain:spawn_buffer` while possessing the core.

The proof item is registered in `kubejs/startup_scripts/abyssal_recovery_items.js` and currently uses a vanilla echo-shard texture as an intentional mechanical-first placeholder.

Western slope biomes are appended to `minecraft:has_structure/ocean_ruin_cold`; Eastern slope biomes are appended to `minecraft:has_structure/ocean_ruin_warm`, reserving a symmetric Eastern scaffold.

The vanilla ruin is temporary. A later Heavy Rebuild structure should replace the recovery destination without changing the quest's essential locate-descend-recover-return contract.

## What remains unmeasured

The following are not treated as blockers for this development pass, but remain unproven observations:

- actual seabed Y distribution;
- whether strongest trenches reach approximately Y -56 to -60;
- shelf/slope visual quality;
- cave and aquifer interaction;
- practical submarine clearance;
- structure placement quality on steep terrain;
- chunk-generation cost;
- actual encounter density under live mob-cap conditions.

If later measurement shows continentalness cannot reach the intended depth, add only a narrowly regional/ocean/hadal-gated final-density contribution. Do not globally mutate Overworld depth.

## Deferred validation ledger

When runtime access returns:

1. validate all density functions;
2. verify East/West routing and transition seam;
3. inspect central continent and mountain annulus for regression;
4. inspect north/south oceans for contamination;
5. measure physical depth bands;
6. inspect bedrock, caves, and aquifers;
7. verify slope ocean ruins generate and map correctly;
8. verify FTB Rift mobs stay out of starter waters and scale acceptably by depth;
9. complete the Western recovery voyage end-to-end;
10. measure navigation and chunk-generation performance.

## Next implementation boundary

Proceed with:

1. an Eastern/Karsic recovery branch;
2. purpose-built Western and Eastern wreck/installation structures replacing the vanilla ruin stand-ins;
3. region-owned salvage/evidence loot;
4. deeper repeatable submarine expeditions;
5. deliberate aquatic/geological feature population of the current sparse biomes;
6. runtime tuning when measurement becomes available.
