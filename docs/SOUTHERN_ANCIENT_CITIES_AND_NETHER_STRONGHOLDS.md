# Expanded Ancient Cities and Nether Strongholds

## Ancient cities

`minecraft:has_structure/ancient_city` now covers thirteen underground surface-climate conditions: Deep Dark; Jagged, Frozen and Stony Peaks; Snowy Slopes; all three Badlands variants; Wasteland Mountains, Ruined City and Apocalypse; Sulfuric Valley; and Radioactive Wasteland.

The structure keeps its vanilla Y=-27 start height. Placement changes from vanilla 24/8 spacing to 20/7, producing roughly 44% more candidate regions before biome and terrain checks. Ancient Cities remain major underground landmarks rather than common dungeons.

Test in newly generated terrain:

1. Travel to Wasteland Mountains, Ruined City, Apocalypse, Radioactive Wasteland, Sulfuric Valley, or one of the listed rugged vanilla biomes.
2. `/locate structure minecraft:ancient_city`
3. Spectate underground and verify that the city remains embedded around its vanilla Y=-27 level.

## Strongholds

Both `minecraft:has_structure/stronghold` and `minecraft:stronghold_biased_to` now contain only `#minecraft:is_nether`. This removes strongholds from Overworld biome eligibility and gives the concentric-ring placement system valid preferred targets in all five vanilla Nether biomes.

The stronghold structure and its 128-ring structure set are otherwise untouched. This is intentionally the least invasive relocation method and preserves End portal generation.

Test in a new world:

1. In the Overworld, `/locate structure minecraft:stronghold` should fail to find a nearby eligible structure.
2. Enter the Nether.
3. Run `/locate structure minecraft:stronghold`.
4. Spectate to the result and verify that the pieces are embedded in reachable Nether terrain and that the portal room exists.

The unresolved risk is terrain fit: vanilla stronghold assembly was tuned for Overworld vertical conditions. If pieces generate too high, too low, or mostly outside terrain, revert the two stronghold biome-tag overrides and replace the structure definition or placement set with a Nether-tuned copy.
