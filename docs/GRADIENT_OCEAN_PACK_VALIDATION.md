# Gradient Ocean Pack — Isekai API Migration

Source specification: `C:\Users\Admin\Downloads\gradient_ocean_datapack_spec.pdf`

The original vanilla-only scaffold has been migrated to Isekai API 2.1.0 for NeoForge 1.21.1. The installed dependency is:

`mods/isekai-api-2.1.0-neoforge-1.21.1.jar`

## What is active

- `isekai_api:coordinate` supplies the missing raw Z coordinate.
- Isekai arithmetic, clamp, absolute-value, step, and lerp functions replace the nonexistent vanilla codecs.
- The median mask is 1 at Z=0 and reaches 0 at Z=-750 and Z=750.
- The center blends toward large, land-biased continents and retains only Wastelands land biomes.
- The central terrain is radial, not a north-south strip. Radius 3,200 through 3,900 is reserved as a continuous `wastelands:mountains` annulus. The expanded central continent remains guaranteed land through radius 4,000 and blends toward the outer ocean by radius 4,800, preserving the original central geography at exactly 2x linear scale.
- The outer zones blend toward smaller, ocean-biased continents.
- Direction now distinguishes the infinite outer world: east and west blend toward recurring large, land-preferred continents and force the wasteland climate band, while north and south retain small, ocean-preferred continents. The diagonal boundaries use an approximately 500-block transition instead of a hard seam.
- Northern land is exclusively cold-facing terrain: snowy plains and taiga, groves, old-growth taiga, ice spikes, snowy slopes and beaches, frozen rivers, and frozen/jagged peaks. Northern ocean bands are exclusively frozen, deep-frozen, cold, and deep-cold water so biome-specific outer expeditions such as the Spore iceberg mines remain possible.
- Southern land contains every vanilla hot-biome family: Desert; all three Badlands variants; Savanna, Savanna Plateau, and Windswept Savanna; Jungle, Sparse Jungle, and Bamboo Jungle; and Mangrove Swamp. It also includes the installed Wastelands biome families. Southern ocean bands use Warm Ocean and Deep Lukewarm Ocean.
- `data/minecraft/worldgen/density_function/overworld/continents.json` connects the result to terrain that consumes the vanilla overworld continentalness density function, including the Wastelands noise settings.
- Moonlight's global datapack folder now points at the instance `datapacks` directory, so the pack is offered to every world rather than sitting unused at instance level.

## Central-continent expansion

The authoritative radial geometry has been expanded without changing biome ownership or the outer directional regime:

- guaranteed central land: radius 2,000 -> 4,000;
- shoreline/outer blend: radius 2,000-2,400 -> 4,000-4,800;
- mountain annulus: radius 1,600-1,950 -> 3,200-3,900;
- central-continent mask falloff multiplier: 0.0025 -> 0.00125 so the transition width scales from 400 to 800 blocks rather than changing shape.

The spawn buffer, north/south temperature logic, east/west directional preference, abyssal depth zoning, and recurring outer continents are not rescaled; they serve different geographic roles and remain authoritative outside the enlarged center.

## Deliberately not claimed complete

`custom_worldgen:south_lava_mask` is a valid Z-gated Isekai density function, but it is not yet connected to the active Wastelands noise router. Minecraft's `noise_router.lava` controls lava aquifer selection; it is not documented as a general replacement for the global `default_fluid` sea. Connecting the mask without an in-game generation test could produce scattered lava aquifers instead of a continuous southern lava ocean.

The removed `custom_worldgen:overworld` noise-settings file was invalid and unreferenced. It omitted a surface rule, used constant final density, and could not generate the requested terrain.

## New-world validation

Worldgen changes only affect newly generated chunks. Create a disposable world using the Wastelands preset, then run:

1. `/isekai validate custom_worldgen`
2. `/tp @s 0 100 -1500`
3. `/tp @s 0 100 0`
4. `/tp @s 0 100 1500`

Expected at this stage: the directional climate logic remains intact inside the enlarged central landmass. Northern and southern biome selection should retain the established cold/hot families while the radial central-continent mask keeps terrain land-biased until the expanded shoreline transition.

Validate the mountain ring at representative compass points: `/tp @s 3500 140 0`, `/tp @s -3500 140 0`, `/tp @s 0 140 3500`, and `/tp @s 0 140 -3500`. Each surface location should resolve to Wasteland Mountains. Also sample just inside and outside the band (for example radius 3,100 and 4,000) to confirm the annulus terminates cleanly.

Validate the shoreline transition at radius 4,000, 4,400, and 4,800 on all four cardinal axes. The central mask should be fully land-biased at radius 4,000, partially blended at 4,400, and fully handed off to the established outer regime by radius 4,800.

Validate the infinite directional regimes safely beyond the expanded central shoreline with `/tp @s 7000 160 0` and `/tp @s -7000 160 0` for east/west large Wastelands continents. Compare those with `/tp @s 0 160 7000` and `/tp @s 0 160 -7000`, which should remain dominated by ocean and smaller hot/cold continents. Large continents are preferred rather than guaranteed at each exact coordinate, so an east/west test point may still land in the ocean separating two large continents.

## Remaining engineering decision

A guaranteed continuous lava sea south of Z=750 still needs one of these:

- a coordinate-sensitive replacement for the sea-level fluid picker in a small companion mod; or
- a proven Isekai/Minecraft noise-router construction after disposable-world testing confirms that the lava aquifer signal fills the open southern basin continuously.

Isekai API solves the terrain-coordinate and blending half of the design. It does not document a per-coordinate `default_fluid` override.
