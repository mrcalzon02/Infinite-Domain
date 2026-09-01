# Northern Biome Restoration Plan

## Finding

The installed pack does require ordinary biomes for full content coverage. A static audit of 170 mod JARs plus vanilla 1.21.1 found:

- 228 structure definitions with biome selectors
- 299 biome-modifier selector fields affecting features, vegetation, ores, or spawns
- 68 modded biome definitions
- 1,688 biome-tag memberships

The source-level results are in `docs/biome-gating-audit/`.

This proves that ocean restoration alone is insufficient. Many structures explicitly require plains, forests, taigas, deserts, savannas, jungles, swamps, mountains, or their associated biome tags.

## Recommended geography

Keep the median and southern design unchanged. Make the northern archipelago a recovering biosphere divided by X:

### Northwest — cold and temperate recovery

- plains
- forest
- birch forest
- dark forest
- taiga
- snowy taiga
- grove
- snowy plains
- old-growth pine taiga
- old-growth spruce taiga
- cold, frozen, and temperate oceans

These biomes permit 122 audited structure definitions across 15 source mods.

### Northeast — warm, dry, and wet recovery

- plains
- jungle
- sparse jungle
- swamp
- mangrove swamp
- flower forest
- meadow
- temperate, lukewarm, and warm oceans

These biomes permit 123 audited structure definitions across 15 source mods.

Together, the two northern palettes permit 137 distinct audited structure definitions. Deserts, badlands, savannas, and every Wastelands biome are reserved for the south. The remainder includes Nether, End, ocean-only, cave-only, extraterrestrial, or highly specialized biome targets and should not all appear on northern land.

The X=0 division should be noise-jittered rather than a straight seam. Islands near the dividing line can mix plains, meadow, forest, and savanna as transitional biomes.

## Important progression consequence

Biome restoration and structure permission must be treated separately. Ordinary northern biomes enable desirable trees, crops, animals, villages, and exploration content, but also reactivate high-value structures:

- Create Cybernetics labs can generate in most proposed northern biomes.
- Ripper clinics can generate in plains, desert, savanna, and badlands families.
- AE2 meteorites are allowed in nearly every Overworld biome.
- AE2LT starships and Stellaris Earth structures can expose advanced or space-tier loot.
- When Dungeons Arise, Graveyard, Ice and Fire, Create structure packs, and vanilla structures regain compatible biomes, a large amount of loot-bearing content returns at once.

The tattooist hut is limited to the Nether warped forest and is unaffected by northern restoration.

Recommended policy:

1. Restore normal northern biomes for ecology and compatibility.
2. Audit or replace early loot in Cybernetics, AE2LT, Stellaris, and other milestone-bearing structures.
3. Keep AE2 machines, cells, and valuable cyberware quest-gated even if their structures can appear.
4. Treat the journey north as exploration access, not automatic technology-tier access.

## Implementation constraint

Isekai API provides the required X and Z density coordinates, but its rule biome source does not expose X-below, X-above, Z-below, or Z-above biome-zone predicates. The robust implementation is therefore:

1. Feed Z into one climate axis to distinguish north, median, and south.
2. Feed X into a second climate axis to distinguish northwest and northeast.
3. Use an Isekai climate-zone biome source or a compatible multi-noise mapping to select the palettes.
4. Preserve `custom_worldgen:continents` as the terrain-shape signal.
5. Preserve vanilla ocean biome IDs so ocean structures and mobs continue using `#minecraft:is_ocean`.

This requires a complete, valid override of the active Wastelands noise settings and biome source. It should be introduced only after the current continent-density pack passes registry loading, so codec failures and biome-layout failures remain independently diagnosable.

## Audit limitations

The audit covers data-driven JSON contained in installed JARs. A mod can also gate generation through Java code or external configuration, so the final world must still be checked with `/locate structure`, `/locate biome`, and controlled chunk generation. Structure counts indicate biome compatibility, not actual frequency.
