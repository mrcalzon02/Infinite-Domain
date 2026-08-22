# Infinite Domain — East/West Abyssal Ocean Program

Status: **promoted for continued development under an explicit runtime-validation waiver. East/West terrain shaping, depth-specific biome routing, FTB Ocean Mobs population/loot, bilateral submarine recovery voyages, recovery-site contracts, and regional salvage loot contracts are implemented. Purpose-built abyssal structures, final quest localization, ecological feature passes, and measured seabed Y-level proof remain outstanding.**

## Authority and gate disposition

This is the design/program authority for Infinite Domain abyssal-ocean work.

- Program/design authority: `docs/ABYSSAL_OCEAN_PROGRAM.md`
- Mechanical terrain/depth record: `docs/ABYSSAL_OCEAN_DEPTH_IMPLEMENTATION.md`

Future work should update these files rather than create a competing planning authority.

On **2026-08-22**, fresh-world/runtime validation was unavailable. Development was explicitly directed to continue **as if the gate had passed**. That promotes the implementation for downstream development, but it is not fabricated test evidence. No file should claim measured seabed Y-levels, verified aquifer behavior, proven submarine clearance, or measured generation performance until those observations actually exist.

Deferred validation is therefore a regression ledger, not a current blocker.

## Program purpose

Infinite Domain uses a strong east/west continental axis and several underused marine systems, including Create Submarine, Create Aquatic Ambitions, Dungeons Arise: Seven Seas, and FTB Ocean Mobs. The abyssal program turns deep-water gaps between recurring eastern and western Wasteland continents into a distinct submarine exploration layer rather than interchangeable vanilla ocean.

The established world generator remains authoritative. This program extends its directional climate/continentalness system; it does not introduce a second world preset or replace the central continent, mountain annulus, north/south climate regimes, or ordinary ocean band.

## Regional identity

### Western Abyss — Pelagos-facing

Western content emphasizes maritime science, oceanography, subsea power and communications, drowned ports, survey sites, naval/scientific wreckage, relay stations, and research habitats. Western geography should generally favor broad navigable approaches and evidence-heavy scientific salvage.

### Eastern Abyss — Karsic-facing

Eastern content emphasizes industrial/military logistics, pipelines, drilling infrastructure, listening stations, strategic research, submarine patrol wrecks, coastal-defense remnants, and freight fields. Eastern terrain/content may become sharper and more hostile while preserving equivalent progression value.

## Authoritative directional routing

The active Wastelands climate source reuses the existing east/west humidity authority:

- negative humidity / west-facing gradient -> Western family;
- positive humidity / east-facing gradient -> Eastern family;
- humidity `-0.2 .. 0.2` -> vanilla `minecraft:deep_ocean` transition seam.

`custom_worldgen:east_west_ocean_corridor_mask` derives from the existing east/west continent mask and suppresses abyssal pressure in north/south-dominant geography.

Far-northern frozen/deep-cold ocean and far-southern deep-lukewarm/warm ocean rules retain separate ownership.

## Active terrain shaping

Reusable functions:

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

`custom_worldgen:continents` uses the abyssal outer function only outside the protected central-continent branch.

Initial continentalness pressure:

1. slope/ocean depression: `0.05`;
2. abyssal-plain depression: `0.12`;
3. fracture/hadal depression: `0.28`.

Low-frequency shifted erosion noise drives the fracture stage so the strongest terrain pressure forms uncommon canyon/trench corridors instead of one flat bottomed-out ocean.

## Implemented depth biome families

### Western

- `infinite_domain:western_continental_slope` — continentalness `-0.60 .. -0.455`
- `infinite_domain:western_abyssal_plain` — `-0.82 .. -0.60`
- `infinite_domain:western_fracture_field` — `-1.02 .. -0.82`
- `infinite_domain:western_hadal_trench` — `-1.20 .. -1.02`

### Eastern

- `infinite_domain:eastern_continental_slope` — `-0.60 .. -0.455`
- `infinite_domain:eastern_abyssal_plain` — `-0.82 .. -0.60`
- `infinite_domain:eastern_fracture_field` — `-1.02 .. -0.82`
- `infinite_domain:eastern_hadal_trench` — `-1.20 .. -1.02`

The original `western_abyssal_ocean` and `eastern_abyssal_ocean` IDs remain compatibility members rather than being destructively removed.

## Biome targeting contracts

Regional parents:

- `#infinite_domain:western_abyssal_biomes`
- `#infinite_domain:eastern_abyssal_biomes`

Depth parents:

- `#infinite_domain:abyssal_slope_biomes`
- `#infinite_domain:abyssal_plain_biomes`
- `#infinite_domain:abyssal_fracture_biomes`
- `#infinite_domain:hadal_biomes`

Each depth has independent East/West subtags for structures, mobs, loot, evidence, and quests. All current abyssal biomes append to vanilla ocean/deep-ocean tags with `replace: false`.

## FTB Ocean Mobs integration

Infinite Domain owns spawn weights for the nine ordinary FTB Ocean Mobs types that upstream permits to spawn naturally:

- `riftling_observer`
- `abyssal_winged`
- `corrosive_craig`
- `mossback_goliath`
- `abyssal_sludge`
- `shadow_beast`
- `rift_minotaur`
- `tentacled_horror`
- `rift_demon`

`rift_weaver` and `sludgeling` remain excluded because upstream explicitly registers them with no-natural-spawn rules.

Encounter pressure rises with depth: rare slope incursions, sustained abyssal threats, dangerous fracture fields, and the strongest normal mixtures in hadal terrain. Western weighting leans scientific/rift-observation and deepwater fauna; Eastern weighting leans corrosive/heavy/military-feeling pressure.

Infinite Domain-owned entity loot lives under:

`kubejs/data/ftboceanmobs/loot_table/entities/`

Drops are modest biological/salvage materials rather than progression-breaking advanced equipment.

## Bilateral submarine recovery chapter

The first exploration implementation is:

`config/ftbquests/quests/chapters/abyssal_recovery.snbt`

It belongs to the existing **Global Logistics** group and cross-depends on Air/Sea quest `5E00000000000006` — **Ballast and Propulsion**. It does not create a competing submarine progression ladder.

### Western/Pelagos branch

1. reach `infinite_domain:western_continental_slope`;
2. receive an explorer map to `minecraft:ocean_ruin_cold`;
3. enter the recovery site;
4. obtain `kubejs:abyssal_navigation_core`;
5. carry the core back into `infinite_domain:spawn_buffer`.

### Eastern/Karsic branch

1. reach `infinite_domain:eastern_continental_slope`;
2. receive an explorer map to `minecraft:ocean_ruin_warm`;
3. enter the recovery site;
4. obtain `kubejs:karsic_subsea_data_recorder`;
5. carry the recorder back into `infinite_domain:spawn_buffer`.

A final convergence quest requires both recovered packages and provides only a modest currency reward. These artifacts are evidence/data, not production-chain skips.

Proof items are registered by `kubejs/startup_scripts/abyssal_recovery_items.js`. They intentionally reuse vanilla item textures in the mechanical-first pass; bespoke art is deferred polish.

### Temporary-site doctrine

The vanilla ocean ruins are explicitly temporary recovery-site stand-ins. They satisfy existence/integration/progression needs while purpose-built Pelagos and Karsic underwater wrecks are authored under the Heavy Rebuild Doctrine.

The biome compatibility scaffolds are already present:

- Western slope appended to `minecraft:has_structure/ocean_ruin_cold`;
- Eastern slope appended to `minecraft:has_structure/ocean_ruin_warm`.

Semantic structure contracts also exist:

- `#infinite_domain:western_abyssal_recovery_sites`
- `#infinite_domain:eastern_abyssal_recovery_sites`

Today those tags contain the respective vanilla ruin. Future bespoke structure IDs should replace or join those contracts rather than forcing downstream quest/content rewrites.

## Regional wreck/salvage loot contracts

The future custom wrecks already have owned loot-table contracts:

- `infinite_domain:chests/abyssal/pelagos_survey_recovery`
- `infinite_domain:chests/abyssal/karsic_patrol_recovery`
- `infinite_domain:chests/abyssal/abyssal_plain_salvage`
- `infinite_domain:chests/abyssal/hadal_salvage`

The Pelagos and Karsic recovery tables guarantee their corresponding proof artifacts and add modest salvage. Generic deeper tables increase unusual salvage slightly but still avoid advanced machines, diamonds, netherite, or direct era bypasses.

**These custom chest tables are not currently injected into vanilla ocean-ruin chests.** During the temporary-site phase the quest reward delivers the proof item. The tables are reserved for the custom wreck structures so unrelated vanilla ruins are not globally contaminated with story-critical evidence.

## Depth target and unmeasured boundary

Sea level remains 48 and Overworld minimum Y remains -64. Intended physical progression:

1. littoral / continental shelf;
2. continental slope;
3. abyssal plain;
4. abyssal valley/fracture field;
5. rare hadal trench approaching bedrock.

Because runtime measurement was waived, no specific seabed Y is marked proven. If later measurement shows continentalness is insufficient, use the existing East/West + ocean + hadal masks for a narrowly gated final-density correction. A global Overworld density mutation remains unacceptable.

## Deferred validation ledger

When runtime access returns, record:

1. density-function loading;
2. correct East/West biome routing;
3. intact north/south climate oceans;
4. intact central continent/mountain annulus;
5. measured seabed Y by depth band;
6. cave/aquifer/bedrock behavior;
7. practical submarine clearance;
8. actual ocean-ruin generation in slope biomes;
9. FTB mob density and starter-coast isolation;
10. both recovery branches and convergence completion;
11. chunk-generation performance.

A failed deferred check should trigger a focused correction rather than invalidating unrelated completed integration.

## Remaining development sequence

1. Author first-class Pelagos survey wreck and Karsic patrol wreck structure IDs, template pools, structure sets, and NBT/schematics; replace the temporary vanilla ruin targets without changing recovery proof contracts.
2. Bind the regional wreck loot tables to guaranteed evidence chests inside those structures.
3. Add deeper abyssal-plain, fracture, and hadal expedition structures with region-specific purposes.
4. Populate the sparse first-pass biome feature lists with verified marine/geological content and Create Aquatic Ambitions assets where useful.
5. Add polished localization for the new abyssal quest chapter without rewriting its stable IDs.
6. Revisit physical depth tuning when measurement is available.

## External Abyssal Ocean mod status

The checked repository did not expose an `abyssal_ocean` registry namespace/JAR when this program was established. Infinite Domain therefore owns the system through `infinite_domain` and `custom_worldgen`. A compatible third-party mod may later contribute features without surrendering East/West geography, biome-family ownership, or progression contracts.
