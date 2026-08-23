# Infinite Domain — Abyssal Environmental Sites

Parent authority: `docs/ABYSSAL_OCEAN_PROGRAM.md`

Status: **five optional environmental structures mechanically implemented, systemic abyssal deformation and custom deep cave carvers active / runtime appearance unmeasured. A second required environmental/geology family is now committed below as the authoritative future-additions backlog.**

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

The derived vertical-relief layer is also active: shelf-edge slump fields, exposed continental-break cuts, hadal trench-wall scarps, and hydrothermal uplift/caldera rims are generated from the existing masks and reference-pattern vocabulary. These processes remain behind the same East/West ocean corridor ownership and are protected by `tools/abyssal_worldgen/validate_abyssal_deformation.py`.

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

## Required future environmental and deep-geology backlog

The following additions were discussed as the next Abyssal population layer but had not previously been promoted into a required committed backlog. They are now authoritative future work. Planning IDs are stable for discussion and implementation tracking; they are not yet Minecraft registry IDs.

### AGE-001 — Methane / cold-seep mound fields
**Type:** terrain-adjacent environmental structure or configured/placed feature family  
**Target:** both abyssal plains, with rare fracture-edge variants  
Low rounded mud/clay/carbonate mounds around seep points, with irregular depressions and limited bubble-producing blocks only where behavior is known to be safe. Variants should range from dormant carbonate mounds to active seep clusters. These should be materially distinct from the existing flat `abyssal_cold_seep` template rather than simple copies.

### AGE-002 — Mineral chimney clusters
**Type:** environmental structure family  
**Target:** fracture fields and hadal trenches  
Small-to-medium mineralized chimney groups separate from the existing black-smoker field and large hadal vent complex. Use basalt/blackstone/calcite/dripstone/mineral-fan language with several height and collapse variants. No unique evidence and no high-tier ore reward.

### AGE-003 — Trench-wall collapse debris
**Type:** environmental structure family  
**Target:** both hadal trench families, preferentially conceptually associated with `abyssal_trench_scarp_pattern` regions  
Angular collapsed wall slabs, fractured columns, rubble aprons and displaced rock masses representing recent or ancient scarp failure. This should visually reinforce the systemic trench-wall deformation rather than look like an unrelated ruin.

### AGE-004 — Scarp talus fields
**Type:** geological placed-feature / small-structure family  
**Target:** continental slopes, fracture boundaries and hadal scarps  
Broad but sparse aprons of gravel, deepslate, tuff, basalt and stone debris beneath steep relief. Talus should concentrate visual material at the base of cliffs/scarps and leave navigable channels between deposits. Avoid uniform carpet placement.

### AGE-005 — Exposed abyssal rock faces
**Type:** surface/geological feature family  
**Target:** continental-break cliffs, fracture terrain and trench walls  
Patchy exposed stone/deepslate/tuff/basalt faces intended to make the new cliff and scarp deformation visibly read as rock rather than ordinary sediment-covered ocean floor. This is a surface-expression system, not a freestanding building.

### AGE-006 — Collapsed subsea cable runs
**Type:** faction-neutral / Pelagos-biased environmental structure variants  
**Target:** continental slope through abyssal plain  
Broken cable segments, anchor blocks, severed relay junctions, collapsed supports and sections disappearing into sediment or over cliff edges. No intact advanced machinery. Rare modest salvage may be allowed only after progression review.

### AGE-007 — Inactive relay pylons
**Type:** Pelagos environmental structure family  
**Target:** western continental slope and western abyssal plain  
Dead or toppled communications/survey pylons, isolated from the quest-critical Pelagos relay. Variants should include upright-but-dead, snapped, leaning and sediment-buried states. These provide regional history without duplicating the core evidence site.

### AGE-008 — Alternate Pelagos sensor-debris fields
**Type:** Pelagos environmental structure variants  
**Target:** western abyssal plain and selected fracture approaches  
Additional wreckage layouts derived from failed oceanographic instrumentation: broken hydrophone grids, detached sensor booms, instrument sleds and scattered survey frames. Use the existing generic abyssal salvage doctrine where a chest is justified; most variants should contain no chest.

### AGE-009 — Karsic pipeline-collapse variants
**Type:** Karsic environmental structure variants  
**Target:** eastern abyssal plain, fracture approaches and selected trench margins  
Collapsed pipe spans, ruptured manifolds, unsupported pipeline bridges, buried line sections and broken armored junctions. These expand the existing `karsic_pipeline_breach` into a family without introducing intact functional machinery.

### AGE-010 — Trench-wall infrastructure remnants
**Type:** factional environmental structure family  
**Target:** fracture fields and hadal trench walls  
Sparse anchor stations, snapped ladders/gantries, observation brackets, pipe/cable anchors and partial wall-mounted platforms suggesting failed attempts to instrument or exploit the trench. Pelagos and Karsic variants should remain visually distinct.

### AGE-011 — Alternate cold-seep shapes
**Type:** neutral geological structure variants  
**Target:** both abyssal plains  
Cratered seeps, linear fissure seeps, paired mound seeps, collapsed seep bowls and inactive mineralized seep scars. These are explicitly required to prevent the current single cold-seep template from becoming visibly repetitive.

### AGE-012 — Hydrothermal province variants
**Type:** neutral geological structure variants  
**Target:** fracture and hadal families  
Additional province layouts around the existing two vent scales: collapsed chimneys, extinct mineralized fields, asymmetric caldera rims, vent chains aligned along faults and mixed active/inactive fields. This extends the existing `fracture_vent_field` and `hadal_vent_complex`; it does **not** replace or duplicate their registry IDs.

### AGE-013 — Shelf-edge slump debris fields
**Type:** geological structure / placed-feature family  
**Target:** continental shelf-to-slope transition  
Sediment blocks, broken rock rafts, slump scar debris and partially buried material beneath the new `abyssal_shelf_slump_pattern`. This is the physical surface-expression companion to the systemic terrain deformation.

### AGE-014 — Cliff cave-mouth geology
**Type:** cave-mouth decoration / small geological feature family  
**Target:** both continental slopes  
Rockfall, gravel fans, exposed stone lips, sparse magma/mineral patches and collapsed entrance debris around suitable cave openings. The goal is to make `abyssal_slope_cave` openings read as real eroded continental-break caves rather than ordinary Overworld caves intersecting water.

### AGE-015 — Fracture cave-mouth / fissure fields
**Type:** cave-mouth decoration / small geological structure family  
**Target:** fracture fields and hadal trenches  
Fault-aligned fissure mouths, collapsed lips, basalt/deepslate rubble, mineral staining and sparse vent-associated geology around suitable `abyssal_fracture_cave` openings. Must not block every cave entrance or destroy submarine navigability.

## Production order for the future family

Implementation should proceed in this order unless a registry/runtime constraint requires otherwise:
1. AGE-004 scarp talus fields and AGE-005 exposed rock faces, because they make the already-active deformation readable;
2. AGE-001 methane/seep mounds and AGE-011 alternate seep shapes;
3. AGE-002 mineral chimney clusters and AGE-012 hydrothermal variants;
4. AGE-003 trench-wall collapse debris and AGE-013 shelf-edge slump debris;
5. AGE-014/015 cave-mouth geology once cave-mouth behavior can be inspected safely;
6. AGE-006 through AGE-010 factional debris/infrastructure variants.

All additions must remain sparse. Geological features should reinforce the terrain process that caused them, and built remnants should never make the abyss feel urbanized or crowded.

## Implementation rules

- Preserve the eight core expedition IDs and five existing environmental structure IDs.
- Do not attach quest-critical evidence to AGE-001–015.
- No diamonds, netherite, intact advanced machines, or era-bypass materials.
- Prefer deterministic generated NBTs for discrete structures, following the existing abyssal materialization workflow.
- Prefer configured/placed features or surface rules for genuinely geological scatter where those systems express the feature more naturally than a structure template.
- New terrain-sensitive features must remain restricted to their stated abyssal biome/depth families.
- Where practical, placement should visually correlate with the existing deformation vocabulary rather than uniformly scatter features throughout every eligible biome.
- Do not claim live bubble-column behavior, cave-mouth quality, terrain correlation, seabed depth or performance until runtime inspection exists.

## Materialization authority

`tools/abyssal_rebuild/generate_abyssal_environmental_sites.py` is the deterministic NBT authority for all five currently implemented discrete environmental sites. It imports the shared structure serializer from the core abyssal generator, embeds expected Git blob hashes, and is verified by the existing Abyssal Assets workflow before generated NBTs may be committed. The hadal vent complex has locked Git blob `cc17b36102636467d7fa10986e86cabb86e59b57`.

AGE-001–015 are planning commitments only until their implementation files, registry/worldgen references and generated assets are committed. As each is implemented, this document must be updated from **planned** to **active** without changing its planning ID.

Semantic tags currently implemented:
- `#infinite_domain:abyssal_plain_environmental_sites`
- `#infinite_domain:fracture_environmental_sites`
- `#infinite_domain:hadal_environmental_sites`
- `#infinite_domain:abyssal_hydrothermal_sites`
- `#infinite_domain:abyssal_environmental_sites`

## Design boundary

Environmental sites are atmosphere and exploration texture, not progression nodes. Terrain deformation should remain low-amplitude outside fracture/hadal masks, and discrete structures must remain sparse enough that the abyss is dominated by empty scale rather than structure spam.

Runtime still must verify density-function loading, pattern scale, actual seabed deformation, cave flooding and entrances, placement projection, burial, bubble behavior, visual density, submarine clearance, and generation cost.
