# Infinite Domain — East/West Abyssal Ocean Program

Status: **regional biome split implemented; terrain-depth, FTB Ocean Mobs, abyssal structures, and loot integration pending runtime validation**.

## Purpose

Infinite Domain has a strong east/west continental axis and several marine systems, including Create Submarine, Create Aquatic Ambitions, Dungeons Arise: Seven Seas, and FTB Ocean Mobs. The abyssal-ocean program turns the deep-water gaps between recurring eastern and western Wasteland continents into a distinct submarine exploration domain rather than treating every sea as interchangeable vanilla ocean.

The world generator remains authoritative over geography. The abyssal program extends the existing directional climate system; it does not replace the central continent, mountain annulus, north/south climate regimes, or restored vanilla ocean membership.

## Implemented regional split

Two first-class biome families now exist:

- `infinite_domain:western_abyssal_ocean`
- `infinite_domain:eastern_abyssal_ocean`

Their family tags are intentionally separate:

- `#infinite_domain:western_abyssal_biomes`
- `#infinite_domain:eastern_abyssal_biomes`
- combined: `#infinite_domain:abyssal_oceans`

Both biomes are appended to `#minecraft:is_ocean` and `#minecraft:is_deep_ocean`, preserving compatibility with systems that discover valid ocean biomes through vanilla tags.

The active Wastelands climate source already receives `custom_worldgen:east_west_gradient` through its humidity channel outside the protected start and mountain masks. The abyss split reuses that existing geography instead of creating a second coordinate convention:

- negative humidity / west-facing gradient -> Western Abyssal Ocean;
- positive humidity / east-facing gradient -> Eastern Abyssal Ocean;
- a narrow `-0.2 .. 0.2` transition remains vanilla `minecraft:deep_ocean` rather than creating a hard east/west seam.

Only the temperate deep-ocean continentalness band (`-1.2 .. -0.455`) is routed to the new abyss biomes. The far-northern frozen/deep-cold ocean regime and far-southern deep-lukewarm/warm regime remain intact.

## Directional density selectors

The gradient datapack now also exposes two separate reusable selector files:

- `custom_worldgen:eastern_abyss_selector`
- `custom_worldgen:western_abyss_selector`

These are **directional selectors, not terrain carving by themselves**. Each converts the existing signed east/west gradient into a `0 .. 1` regional intensity. Future seabed shaping can combine the appropriate selector with deep-ocean continentalness and central-continent exclusion without duplicating east/west coordinate math.

## Reserved biome-family expansion

The current two abyssal-ocean biomes establish identity and routing. Later depth work should expand each side independently rather than making one shared pool. Reserved design roles are:

### Western family

- Western continental slope
- Western abyssal plain
- Western fracture/canyon field
- Western hadal trench
- Western vent or seep field where appropriate

Western content emphasis: Pelagos-facing maritime infrastructure, scientific/oceanographic stations, subsea power and communications, drowned ports, survey sites, and naval/scientific wreckage.

### Eastern family

- Eastern continental slope
- Eastern abyssal plain
- Eastern industrial fracture field
- Eastern hadal trench
- Eastern vent or seep field where appropriate

Eastern content emphasis: Karsic-facing heavy industry, military logistics, pipelines, drilling infrastructure, listening stations, strategic research facilities, submarine wrecks, and industrial freight fields.

Shared ecological or geological content may appear on both sides, but regional structures, loot pools, mob weights, and evidence tables should be independently targetable through the east/west biome tags.

## Depth target — not yet claimed implemented

The eventual seabed profile remains:

1. littoral / continental shelf;
2. continental slope;
3. abyssal plain;
4. abyssal valleys and fracture zones;
5. hadal trenches reaching toward the bedrock cap near world minimum Y.

Sea level remains 48 and Overworld minimum Y remains -64. The deepest trench implementation must leave the bedrock floor intact and must be tested against caves, aquifers, structures, and submarine physics before promotion.

Do **not** mark bedrock-depth terrain complete merely because the regional biomes are now active. `final_density` has not yet been modified for the abyssal depth profile.

## Ocean-content integration sequence

1. Validate that both new biome IDs load and route on a fresh Wastelands world.
2. Add east/west-aware seabed density shaping and prove the shelf -> slope -> abyss -> trench profile.
3. Populate each biome family with deliberate vanilla/Aquatic Ambitions features rather than leaving the initial sparse scaffold as final ecology.
4. Wire FTB Ocean Mobs into explicit biome/depth groups with Infinite Domain-owned spawn weights and loot tables.
5. Add regional abyssal structures and salvage pools, with separate Western and Eastern target tags.
6. Connect the first Era 3-4 submarine recovery voyage to a validated deep-water destination.
7. Add deeper repeatable expeditions only after submarine navigation, recovery, and return are reliable in runtime.

## Current Abyssal Ocean mod status

The current repository inventory does not expose an `abyssal_ocean` registry namespace and the checked-in `mods/` listing did not show an Abyssal Ocean jar during this implementation pass. Therefore this stage is deliberately owned by the `infinite_domain` and `custom_worldgen` namespaces and does not make a false dependency claim. If the compatible Abyssal Ocean mod is added later, its terrain/features can be evaluated as an implementation ingredient without surrendering Infinite Domain's east/west geography or biome-family ownership.

## Fresh-world validation gate

Worldgen changes require newly generated chunks; use a disposable fresh Wastelands world.

1. Run `/isekai validate custom_worldgen`.
2. Run `/locate biome infinite_domain:western_abyssal_ocean` and confirm the result is west of the central continent in a genuine deep-water continentalness gap.
3. Run `/locate biome infinite_domain:eastern_abyssal_ocean` and confirm the result is east of the central continent in a genuine deep-water continentalness gap.
4. Confirm both resolve as ocean/deep-ocean tagged biomes for ocean structures and compatibility systems.
5. Inspect the X-axis around representative outer-continent gaps (for example near `x=-5000` and `x=5000`) and verify Western and Eastern IDs never swap sides.
6. Inspect north and south outer oceans and confirm frozen/cold and warm/lukewarm regimes were not consumed by the abyss routing.
7. Confirm the central continent and mountain annulus remain unchanged.

Only after this gate passes should the abyss selector files be connected to terrain depth or additional marine content be promoted as implemented.
