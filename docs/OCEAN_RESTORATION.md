# Wasteland Ocean Restoration

The built-in KubeJS data pack now overrides `wastelands:wasteland` without modifying the Wastelands mod JAR.

The original preset retained overworld terrain noise, water as its default fluid, and sea level 48, but assigned every climate point to one of only five Wastelands biomes. The override reserves the two oceanic continentalness bands for vanilla ocean biomes:

- `-1.2` through `-0.455`: deep oceans
- `-0.455` through `-0.19`: ordinary oceans

Temperature selects frozen, cold, temperate, lukewarm, or warm water. Everything landward of the ocean band continues to use the original five Wastelands climate points and the original `wastelands:wasteland` noise settings.

This restores membership in `#minecraft:is_ocean`, which Dungeons Arise: Seven Seas uses for its ship structures. Other ocean content using vanilla biome tags benefits automatically.

This is intentionally a new-world change. A world's dimension generator is serialized when the world is created, so an existing save will not reliably adopt the revised biome source. Create a fresh Wastelands world for validation and for the eventual production server.

Validation checklist:

1. Create a new world using the Wastelands preset.
2. Use `/locate biome minecraft:ocean` and `/locate biome minecraft:deep_ocean`.
3. Confirm broad connected seas on a map, not isolated ponds.
4. Confirm ocean mobs appear in newly generated ocean chunks under their normal spawn conditions.
5. Confirm Wastelands land biomes still dominate continents.
