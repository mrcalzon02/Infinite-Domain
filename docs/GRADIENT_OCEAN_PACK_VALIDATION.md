# Gradient Ocean Pack — Isekai API Migration

Source specification: `C:\Users\Admin\Downloads\gradient_ocean_datapack_spec.pdf`

The original vanilla-only scaffold has been migrated to Isekai API 2.1.0 for NeoForge 1.21.1. The installed dependency is:

`mods/isekai-api-2.1.0-neoforge-1.21.1.jar`

## What is active

- `isekai_api:coordinate` supplies the missing raw Z coordinate.
- Isekai arithmetic, clamp, absolute-value, step, and lerp functions replace the nonexistent vanilla codecs.
- The median mask is 1 at Z=0 and reaches 0 at Z=-750 and Z=750.
- The center blends toward large, land-biased continents and retains only Wastelands land biomes.
- The central terrain is radial, not a north-south strip. Radius 1,600 through 1,950 is reserved as a continuous `wastelands:mountains` annulus. The central continent remains guaranteed land through radius 2,000 and blends toward the outer ocean by radius 2,400, placing the mountain wall immediately inside the shoreline transition.
- The outer zones blend toward smaller, ocean-biased continents.
- Direction now distinguishes the infinite outer world: east and west blend toward recurring large, land-preferred continents and force the wasteland climate band, while north and south retain small, ocean-preferred continents. The diagonal boundaries use an approximately 500-block transition instead of a hard seam.
- Northern land is exclusively cold-facing terrain: snowy plains and taiga, groves, old-growth taiga, ice spikes, snowy slopes and beaches, frozen rivers, and frozen/jagged peaks. Northern ocean bands are exclusively frozen, deep-frozen, cold, and deep-cold water so biome-specific outer expeditions such as the Spore iceberg mines remain possible.
- Southern land contains every vanilla hot-biome family: Desert; all three Badlands variants; Savanna, Savanna Plateau, and Windswept Savanna; Jungle, Sparse Jungle, and Bamboo Jungle; and Mangrove Swamp. It also includes the installed Wastelands biome families. Southern ocean bands use Warm Ocean and Deep Lukewarm Ocean.
- `data/minecraft/worldgen/density_function/overworld/continents.json` connects the result to terrain that consumes the vanilla overworld continentalness density function, including the Wastelands noise settings.
- Moonlight's global datapack folder now points at the instance `datapacks` directory, so the pack is offered to every world rather than sitting unused at instance level.

## Deliberately not claimed complete

`custom_worldgen:south_lava_mask` is a valid Z-gated Isekai density function, but it is not yet connected to the active Wastelands noise router. Minecraft's `noise_router.lava` controls lava aquifer selection; it is not documented as a general replacement for the global `default_fluid` sea. Connecting the mask without an in-game generation test could produce scattered lava aquifers instead of a continuous southern lava ocean.

The removed `custom_worldgen:overworld` noise-settings file was invalid and unreferenced. It omitted a surface rule, used constant final density, and could not generate the requested terrain.

## New-world validation

Worldgen changes only affect newly generated chunks. Create a disposable world using the Wastelands preset, then run:

1. `/isekai validate custom_worldgen`
2. `/tp @s 0 100 -1500`
3. `/tp @s 0 100 0`
4. `/tp @s 0 100 1500`

Expected at this stage: ocean-biased terrain north and south, with a much more continuous Wastelands continental median. Northern islands should contain only cold-facing land and ocean biomes. Southern islands should contain the complete vanilla hot-biome set plus Wastelands biomes. The southern ocean remains water until a tested fluid-layer implementation is added.

Also validate the mountain ring at representative compass points: `/tp @s 1750 140 0`, `/tp @s -1750 140 0`, `/tp @s 0 140 1750`, and `/tp @s 0 140 -1750`. Each surface location should resolve to Wasteland Mountains. Warm and cold industrial ports are eligible in their respective outer-ocean bands and contain a self-supporting mountain abutment with a complete inland tunnel.

Validate the infinite directional regimes beyond the central shoreline with `/tp @s 5000 160 0` and `/tp @s -5000 160 0` for east/west large Wastelands continents. Compare those with `/tp @s 0 160 5000` and `/tp @s 0 160 -5000`, which should remain dominated by ocean and smaller hot/cold continents. Large continents are preferred rather than guaranteed at each exact coordinate, so an east/west test point may still land in the ocean separating two large continents.

## Remaining engineering decision

A guaranteed continuous lava sea south of Z=750 still needs one of these:

- a coordinate-sensitive replacement for the sea-level fluid picker in a small companion mod; or
- a proven Isekai/Minecraft noise-router construction after disposable-world testing confirms that the lava aquifer signal fills the open southern basin continuously.

Isekai API solves the terrain-coordinate and blending half of the design. It does not document a per-coordinate `default_fluid` override.
