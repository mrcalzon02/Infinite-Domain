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

The active queue is also represented in `tools/abyssal_worldgen/abyssal_feature_catalog.json`. `tools/abyssal_worldgen/validate_abyssal_feature_catalog.py` rejects missing structural metadata, duplicate IDs, invalid footprints, lost biome/depth ownership, live structure/worldgen mismatches, missing deterministic sources, unsafe loot policy, or false runtime-validation claims. `.codex/agents/abyssal-feature-validator.toml` applies the same independent-validator discipline used by the Old World structure program.

## Current active seabed feature audit

### SF-REVIEW-001 — `infinite_domain:abyssal/abyssal_cold_seep`
**Biome:** both abyssal plains via `#infinite_domain:abyssal_plain_biomes`  
**Placement:** `OCEAN_FLOOR_WG`, terrain adaptation `bury`, spacing/separation `160/80`  
**Original assessment:** first-pass active template was under-detailed: a flat rectangular clay/mud pad, five evenly arranged soul-sand seep points and sparse calcite markers. It communicated the concept but not an actual seep province.

**Refinement completed 2026-08-23:** authoritative generator expanded from `17×5×17` to `25×7×25` with an irregular clay/mud/gravel sediment apron, multiple low mud/carbonate mounds, a central pockmark bowl, broken carbonate rim, four irregular active seep points, short carbonate chimney/concretion forms, inactive mineral scars and localized gravel scour streaks. Registry ID, biome tag, placement and spacing remain unchanged.

**Materialization:** generated Git blob `9729cc302901704dd5a2815ec37ead56ef77be46`, confirmed live on `main` by the Abyssal Assets materializer.

**State:** **REFINED / STATIC-MECHANICAL COMPLETE.** Bubble behavior, burial appearance and visual scale remain runtime-unmeasured.

### SF-REVIEW-002 — `infinite_domain:abyssal/fracture_vent_field`
**Biome:** both fracture-field families through live selector `#infinite_domain:abyssal_fracture_biomes`  
**Placement:** `OCEAN_FLOOR_WG`, terrain adaptation `bury`, spacing/separation `176/88`, salt `78064601`  
**Original assessment:** active but under-detailed. The first deterministic template was essentially five isolated vertical basalt/blackstone chimney stacks with magma bases and two crying-obsidian accents.

**Refinement completed 2026-08-24:** authoritative generator expanded from `21×13×21` to `29×16×27`. The field now uses four discontinuous mineralized aprons, four active smokers with distinct heights/materials/branch directions, three extinct or broken chimneys with rubble and no magma source, three low diffuse vent patches, broken calcite/mineral fans, sparse anomalous material and deliberately preserved open-water lanes between clusters. Registry ID, biome ownership, projection, terrain adaptation, spacing, separation and salt remain unchanged.

**Materialization authority:** generated Git blob `34b0d8504173772f406398fcc67a7d30932121e5`. The catalog-integrity workflow regenerates the NBT, checks the embedded Git blob hash, and byte-compares it with the shipping template.

**State:** **REFINED / STATIC-MECHANICAL COMPLETE.** Active-versus-extinct readability, bubble-column behavior, burial appearance, submarine approach and visual scale remain runtime-unmeasured.

### SF-REVIEW-003 — `infinite_domain:abyssal/hadal_vent_complex`
**Biome:** both hadal families through live selector `#infinite_domain:hadal_biomes`  
**Placement:** `OCEAN_FLOOR_WG`, terrain adaptation `bury`, spacing/separation `224/112`, salt `78064602`  
**Original assessment:** the prior `31×18×31` template had a broken caldera ring, central magma field and eight chimneys, but its silhouettes and activity states were too uniform and the caldera/mineral apron relationship to the systemic vent-rim deformation was weak.

**Refinement completed 2026-08-24:** footprint and all external worldgen contracts remain unchanged. The authoritative generator now builds an asymmetric caldera with an uplifted north/east arc and collapsed south-west sector, broken altered-crust hydrothermal floor, five active smokers with distinct heights/materials/branch patterns, four extinct or collapsed chimney zones with outward rubble, a connected east/north mineral apron and preserved swim lanes through the province.

**Materialization authority:** generated Git blob `7a5fa3ad2cbe5ee8b190d2045606441418aa0e49`. The catalog-integrity workflow regenerated and byte-compared the shipping template successfully after the refinement commit.

**State:** **REFINED / STATIC-MECHANICAL COMPLETE.** Bubble-column behavior, burial appearance, submarine approach, visual scale and actual correlation with the systemic vent-rim deformation remain runtime-unmeasured.

### SF-REVIEW-004 — Vanilla seabed geology decoration in custom depth biomes
**Current implementation:** `minecraft:underwater_magma`, `disk_sand`, `disk_clay`, `disk_gravel` with vegetation reduced by depth.  
**Assessment:** mechanically useful but visually generic. These features should remain as baseline texture while AGE-018 progressively adds process-specific geology. Do not remove them until replacement coverage exists.

**State:** augmentation required, not immediate replacement.

### SF-REVIEW-005 — Continental-slope seabed expression
**Current implementation:** systemic shelf/slump/cliff deformation plus vanilla sediment/magma decoration and `abyssal_slope_cave`.  
**Assessment:** terrain shape exists, but the floor still needs physical surface expressions such as AGE-004/005/013 and OSF-023/024/031/033. The deformation should be made visually legible with exposed rock, talus, slump debris and shelf/current bedforms.

**State:** queued for AGE-018 surface-expression work.

### SF-REVIEW-006 — Fracture/hadal surface expression
**Current implementation:** fracture/scarp/caldera deformation, custom deep cave carver, generic gravel/magma decoration, the two refined vent structures and OSF-005 pillow-lava fields.  
**Assessment:** the volcanic surface vocabulary is now materially stronger, but cooled lava tubes, tube collapses, fissure ridges, exposed hardground and cave-mouth/fault debris remain incomplete.

**State:** AGE-018 implementation tranche active.

## First AGE-018 implementation tranche

The first tranche has machine-readable structural/feature specifications in `tools/abyssal_worldgen/abyssal_feature_catalog.json`.

1. **OSF-005 — Pillow-lava fields — IMPLEMENTED / STATIC-MECHANICAL COMPLETE.** `infinite_domain:abyssal/pillow_lava_field` is a deterministic `33×6×33` structure template using overlapping basalt/smooth-basalt/blackstone lobes, broken pressure fronts, exposed hardground and deliberate sediment/water gaps. It contains no flowing lava, loot or progression-bearing materials. It spawns only through `#infinite_domain:volcanic_abyssal_biomes`, which combines fracture and hadal biome families, using `OCEAN_FLOOR_WG`, `bury`, spacing/separation `72/36` and salt `78064701`. Generated Git blob authority: `1df52c9d4ef7c9efcff10b2777b332b597bd0cae`. Runtime density, terrain fit, seams, visual scale and submarine clearance remain unmeasured.
2. **OSF-006 — Cooled lava / magma-tube systems — NEXT.**
3. **OSF-007 — Lava-tube skylights and collapse windows.**
4. **OSF-019 — Pockmark fields.**
5. **OSF-023 — Shelf sand-wave / ripple fields.**
6. **OSF-027 — Turbidity-current channels.**
7. **OSF-037 — Manganese/polymetallic nodule-field analogues.**
8. **OSF-045 — Whale-fall sites.**
9. **OSF-049 — Wood-fall sites.**

Each specification records implementation class, target biome/depth selectors, footprint/vertical range, projection/terrain adaptation, density or spacing intent, palette, geometry contract, hazards, loot/progression policy and explicit deferred runtime checks. Registry IDs remain unset for unimplemented targets; the validator rejects falsely promoted states.

## Deferred runtime checks

Static refinement does not prove live appearance. Runtime validation must eventually inspect bubble-column behavior, burial/projection, sediment transitions, vent silhouette, feature density, submarine clearance, terrain-feature correlation and chunk-generation cost.
