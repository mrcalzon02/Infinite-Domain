# Infinite Domain — East/West Abyssal Ocean Program

Status: **promoted for continued development under an explicit runtime-validation waiver. East/West depth shaping, depth-specific biome routing, FTB Ocean Mobs population/loot, and the first submarine recovery voyage are implemented. Bespoke abyssal structures, ecological feature passes, and measured seabed Y-level proof remain outstanding.**

## Authority and validation status

This is the design/program authority for Infinite Domain's abyssal-ocean work.

- Program/design authority: `docs/ABYSSAL_OCEAN_PROGRAM.md`
- Mechanical depth record: `docs/ABYSSAL_OCEAN_DEPTH_IMPLEMENTATION.md`

Future work should update these files rather than create a competing planning authority.

On **2026-08-22**, fresh-world/runtime validation was unavailable. Development was explicitly directed to continue **as if the gate had passed**. That directive promotes the implementation for continued development, but it is not fabricated test evidence. No document should claim measured seabed Y-levels, verified aquifer behavior, proven submarine clearance, or proven chunk-generation performance until those observations are actually available.

The deferred validation ledger remains useful for later regression testing, but it is not a blocker for the current implementation sequence.

## Purpose

Infinite Domain has a strong east/west continental axis and several marine systems, including Create Submarine, Create Aquatic Ambitions, Dungeons Arise: Seven Seas, and FTB Ocean Mobs. The abyssal program turns the deep-water gaps between recurring eastern and western Wasteland continents into a submarine exploration domain rather than treating every sea as interchangeable vanilla ocean.

The existing world generator remains authoritative. The abyssal program extends the established directional climate/continentalness system; it does not introduce a second world preset or replace the central continent, mountain annulus, north/south climate regimes, or normal ocean band.

## Regional identity

### Western Abyss — Pelagos-facing

The Western Abyss emphasizes maritime science, oceanography, subsea power and communications, drowned ports, naval/scientific wreckage, survey stations, undersea relay sites, and research habitats. Its geography and encounter mix should generally support wider navigable approaches, scientific salvage, and evidence-heavy exploration.

### Eastern Abyss — Karsic-facing

The Eastern Abyss emphasizes military/industrial logistics, pipelines, drilling infrastructure, listening stations, strategic research, submarine patrol wrecks, coastal defense remnants, and freight fields. Its geography and encounter mix may become sharper, more industrialized, and more hostile than the Western side while preserving equivalent progression value.

## Authoritative east/west routing

The Wastelands climate source already uses the Infinite Domain east/west signal through its humidity channel outside protected start/mountain masks. Abyssal routing reuses that authority:

- negative humidity / west-facing gradient -> Western family;
- positive humidity / east-facing gradient -> Eastern family;
- narrow humidity band `-0.2 .. 0.2` -> vanilla `minecraft:deep_ocean` transition seam.

The east/west signal is multiplied by `custom_worldgen:east_west_ocean_corridor_mask`, derived from the existing east/west continent mask. This suppresses abyss identity and terrain pressure in north/south-dominant geography.

Far-northern frozen/deep-cold ocean and far-southern deep-lukewarm/warm ocean rules remain separate from the temperate abyss program.

## Active terrain shaping

The gradient datapack exposes these directional and depth functions:

- `custom_worldgen:eastern_abyss_selector`
- `custom_worldgen:western_abyss_selector`
- `custom_worldgen:east_west_ocean_corridor_mask`
- `custom_worldgen:abyssal_ocean_mask`
- `custom_worldgen:abyssal_plain_mask`
- `custom_worldgen:abyssal_fracture_mask`
- `custom_worldgen:hadal_trench_mask`
- `custom_worldgen:western_depth_depression`
- `custom_worldgen:eastern_depth_depression`
- `custom_worldgen:abyssal_outer_continents`

`custom_worldgen:continents` uses `abyssal_outer_continents` only on the outer-world side of `central_continent_mask`; the protected central branch remains unchanged.

Initial continentalness pressure remains:

1. ocean/slope depression: `0.05`;
2. abyssal-plain depression: `0.12`;
3. fracture/hadal depression: `0.28`.

The fracture stage uses low-frequency shifted erosion noise so the deepest terrain is intended to form irregular canyon/trench corridors rather than a flat world-bottom ocean.

## Implemented depth biome families

The active temperate deep-ocean continentalness band is now divided into first-class depth groups.

### Western

- `infinite_domain:western_continental_slope` — `-0.60 .. -0.455`
- `infinite_domain:western_abyssal_plain` — `-0.82 .. -0.60`
- `infinite_domain:western_fracture_field` — `-1.02 .. -0.82`
- `infinite_domain:western_hadal_trench` — `-1.20 .. -1.02`

### Eastern

- `infinite_domain:eastern_continental_slope` — `-0.60 .. -0.455`
- `infinite_domain:eastern_abyssal_plain` — `-0.82 .. -0.60`
- `infinite_domain:eastern_fracture_field` — `-1.02 .. -0.82`
- `infinite_domain:eastern_hadal_trench` — `-1.20 .. -1.02`

The original compatibility biomes `western_abyssal_ocean` and `eastern_abyssal_ocean` remain valid members of their regional families rather than being destructively removed.

## Biome targeting tags

Regional tags:

- `#infinite_domain:western_abyssal_biomes`
- `#infinite_domain:eastern_abyssal_biomes`

Depth tags:

- `#infinite_domain:abyssal_slope_biomes`
- `#infinite_domain:abyssal_plain_biomes`
- `#infinite_domain:abyssal_fracture_biomes`
- `#infinite_domain:hadal_biomes`

Each depth also has an independent East and West subtag so structures, spawn tables, loot, evidence, and quests can target a side without coordinate duplication.

All current abyssal biomes are appended to vanilla ocean/deep-ocean tags with `replace: false`.

## FTB Ocean Mobs integration

Infinite Domain now owns explicit natural-spawn weights for the nine ordinary FTB Ocean Mobs entity types that the mod permits to spawn naturally:

- `riftling_observer`
- `abyssal_winged`
- `corrosive_craig`
- `mossback_goliath`
- `abyssal_sludge`
- `shadow_beast`
- `rift_minotaur`
- `tentacled_horror`
- `rift_demon`

`rift_weaver` and `sludgeling` remain excluded from natural biome spawning because the upstream mod explicitly registers them with a no-natural-spawn placement rule.

Encounter pressure rises with depth rather than globally enabling Rift mobs in all oceans. Slopes have rare intrusions; abyssal plains introduce persistent threats; fracture fields are dangerous; hadal trenches carry the strongest normal encounter mixture.

Western weighting leans toward observation, abyssal fauna, sludge/shadow threats, and tentacled deepwater encounters. Eastern weighting leans toward corrosive/heavy threats, minotaurs, demons, and industrial-feeling hazard pressure.

Infinite Domain-owned entity loot tables now exist under `kubejs/data/ftboceanmobs/loot_table/entities/`. Rewards are deliberately modest salvage/biological materials rather than diamonds, netherite, advanced machines, or other progression bypasses.

## First submarine recovery voyage

The first mechanical submarine expedition is implemented in:

`config/ftbquests/quests/chapters/abyssal_recovery.snbt`

It is additive to the established `Air, Sea and Global Logistics` progression and depends on quest `5E00000000000006` — the existing **Ballast and Propulsion** submarine milestone.

Current voyage sequence:

1. reach `infinite_domain:western_continental_slope`;
2. receive an explorer map for `minecraft:ocean_ruin_cold`;
3. enter the mapped underwater ruin;
4. recover `kubejs:abyssal_navigation_core` as the expedition proof component;
5. carry the core back into `infinite_domain:spawn_buffer`;
6. receive the modest completion reward.

The custom proof item is registered by `kubejs/startup_scripts/abyssal_recovery_items.js`. It currently reuses the vanilla echo-shard texture intentionally; bespoke art is polish, not a mechanical blocker.

`minecraft:has_structure/ocean_ruin_cold` now includes the Western continental slope. `ocean_ruin_warm` includes the Eastern continental slope, reserving the same low-risk mechanical scaffolding for a later Eastern branch.

### Temporary-site doctrine

The cold ocean ruin is **not** the final Pelagos wreck. It is a temporary mechanically valid recovery destination used because existence/integration/progression correctness precede architectural polish. A future Heavy Rebuild pass should replace this stand-in with a purpose-built Pelagos survey/submarine wreck while preserving the quest contract and recovery proof item.

## Depth target

Sea level remains 48 and Overworld minimum Y remains -64. Intended physical progression remains:

1. littoral / continental shelf;
2. continental slope;
3. abyssal plain;
4. abyssal valleys/fracture fields;
5. rare hadal trenches approaching the bedrock cap.

Because runtime measurement was waived rather than performed, no specific seabed Y is marked proven. If a future measurement shows continentalness alone is too shallow, use the existing regional/ocean/hadal masks for a narrowly gated final-density correction. A global Overworld density mutation remains unacceptable.

## Deferred validation ledger

When runtime validation becomes available, record rather than assume:

1. all `custom_worldgen` density functions load;
2. Western/Eastern biome families remain on their intended sides;
3. north/south climate oceans remain intact;
4. central continent and mountain annulus remain unchanged;
5. actual seabed Y for slope, plain, fracture, and hadal candidates;
6. cave/aquifer behavior and bedrock integrity;
7. outer East/West continents remain substantial landmasses;
8. submarine clearance/navigation is practical;
9. ocean ruin stand-in structures actually generate in their intended slope biomes;
10. FTB Ocean Mobs encounter density is playable and does not spill into starter coasts;
11. recovery-voyage tasks and return proof complete correctly.

Failure of a deferred check should trigger a focused correction, not invalidate unrelated completed integration work.

## Next development sequence

1. Add a matching Eastern/Karsic recovery branch using the already-reserved Eastern slope structure compatibility.
2. Replace temporary vanilla ruin targets with distinct Western and Eastern abyssal structures under the Heavy Rebuild Doctrine.
3. Add region-owned structure loot/evidence pools and deeper repeatable expeditions.
4. Populate slope/plain/fracture/hadal biomes with deliberate marine/geological features instead of leaving the first-pass sparse feature scaffold final.
5. Add Create Aquatic Ambitions and other verified marine assets where they improve traversal, ecology, or salvage without bypassing progression.
6. Revisit physical depth tuning when runtime measurement is available.

## External Abyssal Ocean mod status

The checked repository did not expose an `abyssal_ocean` registry namespace/JAR during establishment of this program. Infinite Domain therefore owns this system through the `infinite_domain` and `custom_worldgen` namespaces. If a compatible third-party Abyssal Ocean mod is added later, it may contribute features without surrendering the pack's East/West geography, depth bands, or progression ownership.
