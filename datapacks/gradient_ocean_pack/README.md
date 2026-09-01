# Gradient Ocean Pack

Infinite Domain's Z-axis continent gradient for Minecraft 1.21.1 NeoForge.

Requires `Isekai API 2.1.0` or a compatible release. The pack overrides `minecraft:overworld/continents`, so it is intended for the Wastelands world preset and affects only newly generated chunks.

- Beyond the central continent, north and south prefer small, ocean-separated continents.
- Beyond the central continent, east and west prefer recurring large continents and retain Wastelands climate selection.
- A 500-block-wide blend around each diagonal transitions between the east/west land regime and north/south ocean regime without a hard square seam.

The central continent is radial around `(0,0)`. A guaranteed Wasteland Mountains annulus occupies radius 3,200 through 3,900, enclosing the expanded central wasteland before the radius-4,000 to 4,800 transition toward the outer ocean. This is the original central geography at exactly 2x linear scale: the guaranteed central-land diameter expands from 4,000 to 8,000 blocks and the complete central transition diameter expands from 4,800 to 9,600 blocks.

Inside the central continent, mountains are confined to that ring. `overworld/erosion` is overridden through `custom_worldgen:central_interior_mask` so the erosion parameter cannot enter the `wastelands:mountains` band anywhere inside radius 4,650 except the ring itself; the interior fills with the other Wasteland land biomes and Lost Cities can generate there. See `docs/GRADIENT_OCEAN_PACK_VALIDATION.md`.

The complete file-backed geography contract is checked by `python scripts/validate_overworld_geography.py`. It locks the canonical `minecraft:normal` activation, radial center, north/south climate zones, east/west continents and Abyssal corridors, Karsic land routing, cache coverage, and quest-independent multiplayer structure ownership.

The same canonical `wastelands:wasteland` noise router now consumes
`custom_worldgen:wasteland_hex_caves`: a land-only, three-stratum honeycomb of
literal hexagonal corridors and chambers, selectively closed by world-seeded
four-octave plasma noise. It preserves the previous vanilla cave graph, returns
solid-preserving density in all ocean bands, and excludes radius 288 around the
Spawn Hospital. See `docs/WASTELAND_HEX_CAVE_SYSTEM.md` and run
`python scripts/validate_wasteland_hex_caves.py`.

`overworld/depth` is overridden to subtract `custom_worldgen:abyssal_floor_depression`, the direct seabed-depth channel for the East/West abyssal ocean. Continentalness pressure alone cannot deepen the plain/fracture/hadal bands (the vanilla offset spline is a flat plateau there), so real floor relief is applied as a `depth` delta, gated by the same East/West + ocean-corridor + depth-band masks and clamped for a bedrock margin. It is `0` outside the abyssal corridor. See `docs/ABYSSAL_OCEAN_DEPTH_IMPLEMENTATION.md`.

The square from X/Z -192 through 191 is reserved for the authored Spawn Hospital. It uses `infinite_domain:safe_zone`, a visually matching open-wasteland biome with no decoration features and no structure tags, so world generation cannot place roads, ruins, vegetation, or other structures beneath the hub before its template is installed.

The southern ocean is ordinary warm water by design (Warm Ocean / Deep Lukewarm Ocean), and the southern islands carry the full warm/hot biome set. An earlier "southern lava sea" concept has been dropped; the `south_lava_mask` density function was removed rather than left disconnected.

## Nether lava oceans

The Wasteland world preset now selects `infinite_domain:lava_ocean_nether`, supplied by the built-in KubeJS datapack. It retains vanilla Nether biomes, surface rules, features, and structure registration while raising the lava sea level from Y=32 to Y=48 and applying a `-0.03` final-density bias. The design target is approximately 70% open lava-ocean coverage with surviving islands, shelves, caverns, and a bedrock roof.

This is a terrain-generation target rather than an exact per-seed guarantee. Validate it in newly generated Nether chunks; existing chunks will not change. If testing shows too much land, make the bias more negative. If the Nether becomes too empty, move it closer to zero and regenerate a fresh test dimension.
