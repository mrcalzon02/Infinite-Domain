# Gradient Ocean Pack

Infinite Domain's Z-axis continent gradient for Minecraft 1.21.1 NeoForge.

Requires `Isekai API 2.1.0` or a compatible release. The pack overrides `minecraft:overworld/continents`, so it is intended for the Wastelands world preset and affects only newly generated chunks.

- Beyond the central continent, north and south prefer small, ocean-separated continents.
- Beyond the central continent, east and west prefer recurring large continents and retain Wastelands climate selection.
- A 500-block-wide blend around each diagonal transitions between the east/west land regime and north/south ocean regime without a hard square seam.

The central continent is radial around `(0,0)`. A guaranteed Wasteland Mountains annulus occupies radius 1,600 through 1,950, enclosing the central wasteland before the radius-2,000 to 2,400 transition toward the outer ocean.

The square from X/Z -192 through 191 is reserved for the authored Spawn Hospital. It uses `infinite_domain:spawn_buffer`, a visually matching wasteland-city biome with no decoration features and no structure tags, so world generation cannot place roads, ruins, vegetation, or other structures beneath the hub before its template is installed.

The southern lava mask is defined but intentionally not connected yet. See `docs/GRADIENT_OCEAN_PACK_VALIDATION.md` in the modpack project for the fluid limitation and test plan.

## Nether lava oceans

The Wasteland world preset now selects `infinite_domain:lava_ocean_nether`, supplied by the built-in KubeJS datapack. It retains vanilla Nether biomes, surface rules, features, and structure registration while raising the lava sea level from Y=32 to Y=48 and applying a `-0.03` final-density bias. The design target is approximately 70% open lava-ocean coverage with surviving islands, shelves, caverns, and a bedrock roof.

This is a terrain-generation target rather than an exact per-seed guarantee. Validate it in newly generated Nether chunks; existing chunks will not change. If testing shows too much land, make the bias more negative. If the Nether becomes too empty, move it closer to zero and regenerate a fresh test dimension.
