# Infinite Domain — East/West Abyssal Ocean Program

Status: **regional biome split implemented; east/west depth shaping implementation is now active through continentalness; actual seabed Y-levels, FTB Ocean Mobs, abyssal structures, and loot integration remain pending runtime validation**.

## Purpose

Infinite Domain has a strong east/west continental axis and several marine systems, including Create Submarine, Create Aquatic Ambitions, Dungeons Arise: Seven Seas, and FTB Ocean Mobs. The abyssal-ocean program turns the deep-water gaps between recurring eastern and western Wasteland continents into a distinct submarine exploration domain rather than treating every sea as interchangeable vanilla ocean.

The world generator remains authoritative over geography. The abyssal program extends the existing directional climate system; it does not replace the central continent, mountain annulus, north/south climate regimes, or restored vanilla ocean membership.

## Authoritative reference paths

- Program/design authority: `docs/ABYSSAL_OCEAN_PROGRAM.md`
- Current depth implementation record: `docs/ABYSSAL_OCEAN_DEPTH_IMPLEMENTATION.md`

Future work should update these documents rather than creating parallel planning authorities.

## Implemented regional split

Two first-class biome families now exist:

- `infinite_domain:western_abyssal_ocean`
- `infinite_domain:eastern_abyssal_ocean`

Their family tags are intentionally separate:

- `#infinite_domain:western_abyssal_biomes`
- `#infinite_domain:eastern_abyssal_biomes`
- combined: `#infinite_domain:abyssal_oceans`

Both biomes are appended to `#minecraft:is_ocean` and `#minecraft:is_deep_ocean`, preserving compatibility with systems that discover valid ocean biomes through vanilla tags.

The active Wastelands climate source receives an east/west regional gradient through its humidity channel outside the protected start and mountain masks. The abyss split reuses the existing geography instead of creating a second coordinate convention:

- negative humidity / west-facing gradient -> Western Abyssal Ocean;
- positive humidity / east-facing gradient -> Eastern Abyssal Ocean;
- a narrow central transition remains vanilla `minecraft:deep_ocean` rather than creating a hard east/west seam.

The east/west signal is now additionally multiplied by `custom_worldgen:east_west_ocean_corridor_mask`, derived from the existing east/west continent mask. This suppresses abyss identity and terrain pressure in north/south-dominant geography.

Only the temperate deep-ocean continentalness band is routed to the current regional abyss biomes. The far-northern frozen/deep-cold ocean regime and far-southern deep-lukewarm/warm regime remain intact.

## Directional selectors and active depth shaping

The gradient datapack exposes reusable directional selectors:

- `custom_worldgen:eastern_abyss_selector`
- `custom_worldgen:western_abyss_selector`

The following active depth masks now exist:

- `custom_worldgen:east_west_ocean_corridor_mask`
- `custom_worldgen:abyssal_ocean_mask`
- `custom_worldgen:abyssal_plain_mask`
- `custom_worldgen:abyssal_fracture_mask`
- `custom_worldgen:hadal_trench_mask`

The regional depth functions are independently targetable:

- `custom_worldgen:western_depth_depression`
- `custom_worldgen:eastern_depth_depression`

They currently share the same initial strength curve but remain separate files so Western and Eastern seabed morphology can diverge later without rebuilding shared worldgen.

`custom_worldgen:abyssal_outer_continents` subtracts the appropriate east/west depression from the existing outer continentalness field while leaving the central-continent branch unchanged. This is now mechanically connected to `custom_worldgen:continents`.

The active initial pressure curve is:

1. ocean/slope depression: `0.05`;
2. abyssal-plain depression: `0.12`;
3. fracture/hadal depression: `0.28`.

The fracture stage uses low-frequency shifted erosion noise so the deepest terrain should form irregular canyon/trench corridors instead of one uniformly flat deep-ocean plane.

## Reserved biome-family expansion

The current two abyssal-ocean biomes establish identity and routing. Later depth-aware biome work should expand each side independently rather than making one shared pool. Reserved design roles are:

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

## Depth target — runtime proof still required

The intended seabed profile remains:

1. littoral / continental shelf;
2. continental slope;
3. abyssal plain;
4. abyssal valleys and fracture zones;
5. hadal trenches reaching toward the bedrock cap near world minimum Y.

Sea level remains 48 and Overworld minimum Y remains -64. The deepest trench implementation must leave the bedrock floor intact and must be tested against caves, aquifers, structures, and submarine physics before promotion.

The new continentalness depression is active, but it is **not yet proven** to produce Y -56 or bedrock-adjacent trenches. Vanilla terrain response to continentalness is nonlinear. If this stage remains too shallow, the next revision may add a narrowly east/west- and ocean-gated final-density contribution using the existing hadal masks. A global Overworld density mutation is not acceptable.

## Ocean-content integration sequence

1. Validate that both regional biome IDs and all new density functions load on a fresh Wastelands world.
2. Measure actual shelf, slope, abyss, and deepest fracture Y-levels and tune toward the bedrock-depth target.
3. Expand each East/West biome family into explicit slope, abyssal-plain, and hadal groups once the physical depth bands are known.
4. Populate each biome family with deliberate vanilla/Aquatic Ambitions features rather than leaving the initial sparse scaffold as final ecology.
5. Wire FTB Ocean Mobs into explicit biome/depth groups with Infinite Domain-owned spawn weights and loot tables.
6. Add regional abyssal structures and salvage pools, with separate Western and Eastern target tags.
7. Connect the first Era 3-4 submarine recovery voyage to a validated deep-water destination.
8. Add deeper repeatable expeditions only after submarine navigation, recovery, and return are reliable in runtime.

## Current Abyssal Ocean mod status

The current repository inventory does not expose an `abyssal_ocean` registry namespace and the checked-in `mods/` listing did not show an Abyssal Ocean jar during the implementation pass that established this program. Therefore this system is deliberately owned by the `infinite_domain` and `custom_worldgen` namespaces and does not make a false dependency claim. If a compatible Abyssal Ocean mod is added later, its terrain/features can be evaluated as an implementation ingredient without surrendering Infinite Domain's east/west geography or biome-family ownership.

## Fresh-world validation gate

Worldgen changes require newly generated chunks; use a disposable fresh Wastelands world.

1. Run `/isekai validate custom_worldgen`.
2. Run `/locate biome infinite_domain:western_abyssal_ocean` and confirm the result is west of the central continent in a genuine deep-water east/west corridor.
3. Run `/locate biome infinite_domain:eastern_abyssal_ocean` and confirm the result is east of the central continent in a genuine deep-water east/west corridor.
4. Confirm both resolve as ocean/deep-ocean tagged biomes for ocean structures and compatibility systems.
5. Inspect representative outer-continent gaps around both east and west and verify Western and Eastern IDs never swap sides.
6. Inspect north and south outer oceans and confirm frozen/cold and warm/lukewarm regimes were not consumed by abyss routing or depth shaping.
7. Confirm the central continent and mountain annulus remain unchanged.
8. Record actual seabed Y at shelf, slope, abyssal plain, fracture field, and deepest trench candidates.
9. Check for exposed caves, broken aquifers, floating structures, unacceptable cliff walls, or bedrock damage.
10. Confirm outer east/west continents remain substantial landmasses rather than being eroded into island chains.

Only after this gate passes should the terrain stage be considered mechanically validated or the FTB Ocean Mobs / abyssal structure layers be promoted as implemented.
