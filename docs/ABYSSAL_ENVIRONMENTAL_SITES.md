# Infinite Domain — Abyssal Environmental Sites

Parent authority: `docs/ABYSSAL_OCEAN_PROGRAM.md`

Status: **five optional environmental structures mechanically implemented, systemic abyssal deformation and custom deep cave carvers active / runtime appearance unmeasured**

These structures and terrain systems add sparse non-critical seabed scenes around the eight core abyssal expedition sites. They do not carry story-critical evidence, do not gate quests, and may not provide progression-breaking machinery or materials.

## Terrain-forming geological layer

The abyss is no longer limited to ordinary ocean terrain decorated with structures. The six supplied reference-noise motifs are treated as a geological vocabulary and are implemented through `custom_worldgen:abyssal_pattern_depression`, which feeds the already isolated East/West continentalness-depression chain. The protected central-continent branch and global `final_density` router remain untouched.

Reference-pattern roles:
- cellular rounded fields → `custom_worldgen:abyssal_cellular_basin_pattern` for broad basin/pillow-lava-like floor variation;
- coarse connected cracks → `custom_worldgen:abyssal_coarse_fracture_pattern` for shelf gullies and major fault corridors;
- diffuse speckled field → `custom_worldgen:abyssal_diffuse_roughness_pattern` for low-amplitude seabed roughness;
- mottled collapse field → `custom_worldgen:abyssal_mottled_collapse_pattern` for irregular plain collapse/pockmark zones;
- radial/central disturbance → `custom_worldgen:abyssal_vent_caldera_pattern` for rare hadal vent/collapse provinces;
- fine crack mesh → `custom_worldgen:abyssal_fine_fracture_pattern` for secondary faulting within deep plain/fracture terrain.

The patterns use pack-owned noise parameters `abyssal_cells`, `abyssal_faults`, `abyssal_roughness`, and `abyssal_vents`. They deepen existing ocean continentalness rather than directly rewriting final density. Exact visual resemblance, physical depth and generation cost remain runtime-unmeasured.

## Deep cave systems

Two configured cave carvers supplement vanilla caves only in abyssal-owned biomes:
- `custom_worldgen:abyssal_slope_cave` on both continental slopes, probability `0.045`, configured vertical range `Y -48 .. 40`, with wider horizontal radius intended to create shelf/cliff sea caves and submerged galleries;
- `custom_worldgen:abyssal_fracture_cave` on both fracture fields and both hadal trenches, probability `0.065`, configured vertical range `Y -56 .. 16`, with larger/deeper chambers intended to form abyssal fissure caves.

Aquifers remain enabled by the Wastelands noise settings, so the design intent is flooded cave development where aquifer logic permits it. Actual flooding, cave-mouth exposure and submarine navigability are deferred runtime observations.

## Active discrete sites

### `infinite_domain:abyssal/pelagos_sensor_debris`
Western abyssal-plain Pelagos survey debris. A broken prismarine/copper sensor pad with collapsed instrument arms and amethyst sensing elements. Contains one existing `abyssal_plain_salvage` chest and no unique evidence. Placement: western abyssal plain, spacing 112 chunks, separation 56, salt `78064401`.

### `infinite_domain:abyssal/karsic_pipeline_breach`
Eastern abyssal-plain Karsic pipeline rupture. Two severed oxidized-copper pipe runs, armored deepslate supports, rupture debris and magma leakage. Contains one existing `abyssal_plain_salvage` chest and no unique evidence. Placement: eastern abyssal plain, spacing 112 chunks, separation 56, salt `78064402`.

### `infinite_domain:abyssal/abyssal_cold_seep`
Neutral low-relief abyssal-plain geological site built from clay, mud, calcite and sparse soul-sand seep points. No chest and no quest contract. Placement: both abyssal-plain families, spacing 160 chunks, separation 80, salt `78064501`.

### `infinite_domain:abyssal/fracture_vent_field`
Neutral fracture-field black-smoker analogue using magma, basalt, blackstone, polished basalt and very sparse crying obsidian. No chest and no quest contract. Placement: both fracture families, spacing 176 chunks, separation 88, salt `78064601`.

### `infinite_domain:abyssal/hadal_vent_complex`
Rare large hadal hydrothermal province. The deterministic 31 × 18 × 31 template forms a broken basalt/blackstone caldera ring, central magma field, eight irregular smoker chimneys, calcite mineralization, sparse pointed-dripstone mineral fans, and very limited crying obsidian. It contains no chest and no quest contract. Placement: both hadal families, spacing 224 chunks, separation 112, salt `78064602`.

This creates two geological vent scales: smaller fracture-field smoker clusters and uncommon major hadal vent provinces.

## Materialization authority

`tools/abyssal_rebuild/generate_abyssal_environmental_sites.py` is the deterministic NBT authority for all five discrete environmental sites. It imports the shared structure serializer from the core abyssal generator, embeds expected Git blob hashes, and is verified by the existing Abyssal Assets workflow before generated NBTs may be committed. The hadal vent complex has locked Git blob `cc17b36102636467d7fa10986e86cabb86e59b57`.

Semantic tags:
- `#infinite_domain:abyssal_plain_environmental_sites`
- `#infinite_domain:fracture_environmental_sites`
- `#infinite_domain:hadal_environmental_sites`
- `#infinite_domain:abyssal_hydrothermal_sites`
- `#infinite_domain:abyssal_environmental_sites`

## Design boundary

Environmental sites are atmosphere and exploration texture, not progression nodes. Terrain deformation should remain low-amplitude outside fracture/hadal masks, and discrete structures must remain sparse enough that the abyss is dominated by empty scale rather than structure spam. Additional variants may later add collapsed cables, inactive relay pylons, trench-wall debris, methane-mound variants, mineral chimneys, or alternate seep shapes.

Runtime still must verify density-function loading, pattern scale, actual seabed deformation, cave flooding and entrances, placement projection, burial, bubble behavior, visual density, submarine clearance, and generation cost.
