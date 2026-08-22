# Infinite Domain — Abyssal Ocean Depth Implementation

Authoritative parent plan: `docs/ABYSSAL_OCEAN_PROGRAM.md`

Status: **East/West depth shaping is statically implemented and active through continentalness; actual seabed Y-levels remain runtime-unverified.**

## Purpose

This document records the implementation layer that follows the East/West Abyssal Ocean Program. It is intentionally subordinate to `ABYSSAL_OCEAN_PROGRAM.md` and exists so future work can distinguish the intended design from the current mechanical state.

The implementation keeps Infinite Domain's existing world generator authoritative. It does not introduce a second world preset, a parallel continent generator, or a global ocean replacement.

## Regional corridor gate

A new `custom_worldgen:east_west_ocean_corridor_mask` derives from the existing `east_west_continent_mask`. It suppresses abyssal intervention in north/south-dominant geography and ramps toward full strength only in the east/west continental wedges.

`custom_worldgen:regional_east_west_gradient` multiplies the signed east/west gradient by that corridor mask. `city_humidity` now uses this regionalized gradient outside the protected start and mountain masks. This keeps the Western/Eastern abyss biome routing tied to the same geographic wedge used by the continent system and prevents the regional abyss identity from leaking unnecessarily into northern and southern seas.

## Depth masks

The active depth layer is decomposed into reusable masks rather than a single opaque expression:

- `custom_worldgen:abyssal_ocean_mask` begins below the existing ocean shoreline threshold and ramps toward full strength with increasingly negative outer continentalness.
- `custom_worldgen:abyssal_plain_mask` begins at the vanilla deep-ocean threshold and becomes stronger in established deep-water gaps.
- `custom_worldgen:abyssal_fracture_mask` uses low-frequency shifted erosion noise to select irregular fracture/canyon corridors instead of turning the whole abyss into a uniformly flat pit.
- `custom_worldgen:hadal_trench_mask` is the product of the abyssal-plain and fracture masks, so trench pressure exists only inside genuinely deep oceanic terrain.

These masks deliberately operate from `outer_directional_continents`, avoiding recursion through the final `custom_worldgen:continents` function.

## Separate Eastern and Western files

The depth depression is regionally split at the implementation level:

- `custom_worldgen:western_depth_depression`
- `custom_worldgen:eastern_depth_depression`

The two files currently use the same initial strength curve, but they are independent assets. Future tuning can therefore make the Western Abyss broader, more terraced, or more scientifically navigable while making the Eastern Abyss sharper, more industrial, or more trench-dense without rewriting shared worldgen.

Each regional depression is gated by both its directional selector and the east/west corridor mask. The active curve contains three additive pressures:

1. ocean/slope depression: `0.05`;
2. abyssal-plain depression: `0.12`;
3. fracture/hadal depression: `0.28`.

The strongest possible depression therefore occurs only where deep ocean, fracture noise, east/west corridor membership, and the correct regional selector all overlap.

## Active continentalness integration

`custom_worldgen:abyssal_outer_continents` subtracts the stronger of the Eastern or Western depth depressions from the existing `outer_directional_continents`, then clamps the result to the existing climate domain `-1.2 .. 1.0`.

`custom_worldgen:continents` now uses `abyssal_outer_continents` only on the outer-world side of `central_continent_mask`. The central protected continent retains its previous branch unchanged.

This means the depth system is now mechanically connected to the same continentalness signal consumed by the Wastelands noise settings. It is not merely a reserved scaffold.

## What is NOT yet proven

Static implementation does **not** prove that the strongest trench reaches Y -56 or the bedrock cap. Vanilla terrain response to continentalness is nonlinear, and the final result must be measured in a fresh world.

Do not mark any of the following complete until runtime evidence exists:

- bedrock-depth hadal trenches;
- acceptable shelf-to-slope transition geometry;
- safe cave/aquifer interaction;
- submarine navigation clearance;
- acceptable chunk-generation cost;
- structure placement reliability on steep abyssal terrain.

If continentalness alone cannot drive the seabed sufficiently deep, the next revision may add a narrowly gated final-density contribution using the existing hadal masks. That must remain east/west- and ocean-gated rather than becoming a global Overworld density mutation.

## Fresh-world validation

Use a disposable newly generated Wastelands world.

1. Run `/isekai validate custom_worldgen` and confirm all new density functions resolve.
2. Locate `infinite_domain:western_abyssal_ocean` and `infinite_domain:eastern_abyssal_ocean` and verify that each remains in the correct east/west wedge.
3. Inspect representative east and west ocean gaps and record actual seabed Y at shelf, slope, abyssal plain, and deepest fracture locations.
4. Verify the central continent and mountain annulus are unchanged.
5. Verify far northern and far southern seas do not inherit the abyssal depression profile.
6. Verify existing outer east/west continents remain large landmasses rather than being eroded into island chains by the ocean-only depression mask.
7. Check steep transitions for exposed caves, broken aquifers, floating structures, excessive ravines, or bedrock damage.
8. Measure whether the deepest fracture corridors approach the desired hadal target. If they remain too shallow, tune the regional depression or add a narrowly gated final-density stage rather than globally increasing depth.

## Next integration boundary

After this gate passes, expand the current Western/Eastern biome families into independently targetable slope, abyssal-plain, and hadal tags/biomes as needed, then configure FTB Ocean Mobs and regional structures against those explicit depth groups. Create Submarine quest integration remains an Era 3–4 objective and should point to a validated deep-water recovery destination rather than a merely theoretical coordinate.
