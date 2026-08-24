# Infinite Domain — Abyssal Seafloor Feature Review Ledger

Parent authorities:
- `docs/ABYSSAL_ENVIRONMENTAL_SITES.md`
- `docs/ABYSSAL_NEUTRAL_SEAFLOOR_FEATURE_POOL.md`

Status: **active incremental review ledger / not a replacement design authority**

Purpose: track the current `main` implementation against the committed neutral oceanographic feature catalog and process seabed features one at a time. Every reviewed feature keeps its existing biome ownership and registry/worldgen ID unless a concrete mechanical defect requires otherwise.

## Review method

For each feature, proceed in this order:
1. verify the current `main` structure/feature definition, biome selector, projection and spacing;
2. inspect the deterministic geometry or configured/placed-feature implementation;
3. identify whether it reads as a real oceanographic process rather than a simple block pattern;
4. revise only the authoritative generator/configuration;
5. calculate and lock deterministic generated-asset hashes where applicable;
6. materialize generated NBT before moving the feature to **refined**;
7. preserve runtime-unmeasured items in the deferred validation ledger rather than inventing visual results.

## Current active seabed feature audit

### SF-REVIEW-001 — `infinite_domain:abyssal/abyssal_cold_seep`
**Biome:** both abyssal plains via `#infinite_domain:abyssal_plain_biomes`  
**Placement:** `OCEAN_FLOOR_WG`, terrain adaptation `bury`, spacing/separation `160/80`  
**Current assessment:** first-pass active template was under-detailed: a flat rectangular clay/mud pad, five evenly arranged soul-sand seep points and sparse calcite markers. It communicated the concept but not an actual seep province.

**Refinement initiated 2026-08-23:** authoritative generator expanded from `17×5×17` to `25×7×25` with an irregular clay/mud/gravel sediment apron, multiple low mud/carbonate mounds, a central pockmark bowl, broken carbonate rim, four irregular active seep points, short carbonate chimney/concretion forms, inactive mineral scars and localized gravel scour streaks. Registry ID, biome tag, placement and spacing remain unchanged. Expected generated Git blob is `9729cc302901704dd5a2815ec37ead56ef77be46`.

**State:** generator refined; generated NBT must be confirmed materialized before final promotion.

### SF-REVIEW-002 — `infinite_domain:abyssal/fracture_vent_field`
**Biome:** both fracture-field families  
**Placement:** `OCEAN_FLOOR_WG`, sparse structure-set placement  
**Current assessment:** active but under-detailed. The current deterministic template is essentially five isolated vertical basalt/blackstone chimney stacks with magma bases and two crying-obsidian accents. It needs chimney branching, broken/dead stacks, mineralized aprons, diffuse vent patches, asymmetric field composition and varied chimney footprints while retaining navigable open water.

**State:** next feature to process.

### SF-REVIEW-003 — `infinite_domain:abyssal/hadal_vent_complex`
**Biome:** both hadal families  
**Placement:** `OCEAN_FLOOR_WG`, uncommon `224/112` structure-set placement  
**Current assessment:** active and more developed than the fracture field, with a broken caldera ring, central magma field and eight chimneys. Still needs review for chimney silhouette diversity, extinct-versus-active zones, collapsed chimney rubble, mineral apron continuity, caldera asymmetry and clearer relationship to the systemic hydrothermal uplift/caldera-rim deformation.

**State:** queued after fracture vent field.

### SF-REVIEW-004 — Vanilla seabed geology decoration in custom depth biomes
**Current implementation:** `minecraft:underwater_magma`, `disk_sand`, `disk_clay`, `disk_gravel` with vegetation reduced by depth.  
**Assessment:** mechanically useful but visually generic. These features should remain as baseline texture while AGE-018 progressively adds process-specific geology. Do not remove them until replacement coverage exists.

**State:** augmentation required, not immediate replacement.

### SF-REVIEW-005 — Continental-slope seabed expression
**Current implementation:** systemic shelf/slump/cliff deformation plus vanilla sediment/magma decoration and `abyssal_slope_cave`.  
**Assessment:** terrain shape exists, but the floor still needs physical surface expressions such as AGE-004/005/013 and OSF-023/024/031/033. The deformation should be made visually legible with exposed rock, talus, slump debris and shelf/current bedforms.

**State:** queued after the three existing neutral structure templates.

### SF-REVIEW-006 — Fracture/hadal surface expression
**Current implementation:** fracture/scarp/caldera deformation, custom deep cave carver, generic gravel/magma decoration and the two vent structures.  
**Assessment:** strong structural foundation but missing pillow lava, cooled lava-tube geology, volcanic rubble, fissure ridges, exposed hardground and cave-mouth/fault debris.

**State:** AGE-018 implementation tranche required.

## First AGE-018 implementation tranche after active-template review

Process these only after SF-REVIEW-001 through 003 are mechanically coherent:
1. **OSF-005 — Pillow-lava fields**
2. **OSF-006 — Cooled lava / magma-tube systems**
3. **OSF-007 — Lava-tube skylights and collapse windows**
4. **OSF-019 — Pockmark fields**
5. **OSF-023 — Shelf sand-wave / ripple fields**
6. **OSF-027 — Turbidity-current channels**
7. **OSF-037 — Manganese/polymetallic nodule-field analogues**
8. **OSF-045 — Whale-fall sites**
9. **OSF-049 — Wood-fall sites**

## Deferred runtime checks

Static refinement does not prove live appearance. Runtime validation must eventually inspect bubble-column behavior, burial/projection, sediment transitions, vent silhouette, feature density, submarine clearance, terrain-feature correlation and chunk-generation cost.
