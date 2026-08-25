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

The active queue is also represented in `tools/abyssal_worldgen/abyssal_feature_catalog.json`. `tools/abyssal_worldgen/validate_abyssal_feature_catalog.py` rejects missing structural metadata, duplicate IDs, invalid footprints, lost biome/depth ownership, live structure/worldgen mismatches, missing deterministic sources, unsafe loot policy, false runtime-validation claims, invalid parent-pool component relationships and disconnected systemic terrain implementations. `.codex/agents/abyssal-feature-validator.toml` applies the same independent-validator discipline used by the Old World structure program.

## Current active seabed feature audit

### SF-REVIEW-001 — `infinite_domain:abyssal/abyssal_cold_seep`
**Biome:** both abyssal plains via `#infinite_domain:abyssal_plain_biomes`  
**Placement:** `OCEAN_FLOOR_WG`, terrain adaptation `bury`, spacing/separation `160/80`  
**Refinement completed 2026-08-23:** authoritative generator expanded from `17×5×17` to `25×7×25` with an irregular clay/mud/gravel sediment apron, multiple low mud/carbonate mounds, a central pockmark bowl, broken carbonate rim, four irregular active seep points, short carbonate chimney/concretion forms, inactive mineral scars and localized gravel scour streaks. Registry ID, biome tag, placement and spacing remain unchanged.

**Materialization:** generated Git blob `9729cc302901704dd5a2815ec37ead56ef77be46`.

**State:** **REFINED / STATIC-MECHANICAL COMPLETE.** Bubble behavior, burial appearance and visual scale remain runtime-unmeasured.

### SF-REVIEW-002 — `infinite_domain:abyssal/fracture_vent_field`
**Biome:** both fracture-field families through `#infinite_domain:abyssal_fracture_biomes`  
**Placement:** `OCEAN_FLOOR_WG`, terrain adaptation `bury`, spacing/separation `176/88`, salt `78064601`  
**Refinement completed 2026-08-24:** authoritative generator expanded from `21×13×21` to `29×16×27` with four discontinuous mineralized aprons, four active smokers with distinct heights/materials/branch directions, three extinct or broken chimneys with rubble and no magma source, three low diffuse vent patches, broken mineral fans and preserved open-water lanes.

**Materialization authority:** Git blob `34b0d8504173772f406398fcc67a7d30932121e5`.

**State:** **REFINED / STATIC-MECHANICAL COMPLETE.** Active-versus-extinct readability, bubble-column behavior, burial appearance, submarine approach and visual scale remain runtime-unmeasured.

### SF-REVIEW-003 — `infinite_domain:abyssal/hadal_vent_complex`
**Biome:** both hadal families through `#infinite_domain:hadal_biomes`  
**Placement:** `OCEAN_FLOOR_WG`, terrain adaptation `bury`, spacing/separation `224/112`, salt `78064602`  
**Refinement completed 2026-08-24:** footprint and external worldgen contracts remain unchanged. The authoritative generator now builds an asymmetric caldera with an uplifted north/east arc and collapsed south-west sector, broken altered-crust hydrothermal floor, five active smokers with distinct heights/materials/branch patterns, four extinct or collapsed chimney zones with outward rubble, a connected east/north mineral apron and preserved swim lanes.

**Materialization authority:** Git blob `7a5fa3ad2cbe5ee8b190d2045606441418aa0e49`.

**State:** **REFINED / STATIC-MECHANICAL COMPLETE.** Bubble-column behavior, burial appearance, submarine approach, visual scale and actual correlation with systemic vent-rim deformation remain runtime-unmeasured.

### SF-REVIEW-004 — Vanilla seabed geology decoration in custom depth biomes
**Current implementation:** `minecraft:underwater_magma`, `disk_sand`, `disk_clay`, `disk_gravel` with vegetation reduced by depth.  
**Assessment:** mechanically useful baseline texture. AGE-018 augments it rather than destructively replacing it.

**State:** augmentation in progress.

### SF-REVIEW-005 — Continental-slope seabed expression
**Current implementation:** systemic shelf/slump/cliff deformation plus vanilla sediment/magma decoration, `abyssal_slope_cave`, OSF-023 process-specific sand-wave fields and OSF-027 slope-to-plain turbidity transport.  
**Assessment:** terrain shape now has both current-driven bedforms and a connected erosional/depositional transport process. OSF-024/031/033-style scarps, slump blocks and talus remain future additions.

**State:** active augmentation.

### SF-REVIEW-006 — Fracture/hadal surface expression
**Current implementation:** fracture/scarp/caldera deformation, custom deep cave carver, generic gravel/magma decoration, refined vent structures, OSF-005 pillow-lava fields and the OSF-006/007 lava-tube family.  
**Assessment:** volcanic surface vocabulary is materially stronger. Fissure ridges, exposed hardground and cave-mouth/fault debris remain later additions.

**State:** first volcanic tranche complete.

## First AGE-018 implementation tranche

The tranche has machine-readable structural/feature specifications in `tools/abyssal_worldgen/abyssal_feature_catalog.json`.

1. **OSF-005 — Pillow-lava fields — IMPLEMENTED / STATIC-MECHANICAL COMPLETE.** `infinite_domain:abyssal/pillow_lava_field` is a deterministic `33×6×33` structure template using overlapping basalt/smooth-basalt/blackstone lobes, broken pressure fronts, exposed hardground and deliberate sediment/water gaps. It contains no flowing lava, loot or progression-bearing materials. It spawns only through `#infinite_domain:volcanic_abyssal_biomes` using `OCEAN_FLOOR_WG`, `bury`, spacing/separation `72/36` and salt `78064701`. Git blob authority: `1df52c9d4ef7c9efcff10b2777b332b597bd0cae`.
2. **OSF-006 — Cooled lava / magma-tube systems — IMPLEMENTED / STATIC-MECHANICAL COMPLETE.** `infinite_domain:abyssal/cooled_lava_tube_system` is a deterministic `49×12×41` flooded arched tube network with a bent primary conduit, lateral branch, pressure ridges, old cooled-flow fronts and tuff/gravel sediment drapes. Omitted interior blocks preserve surrounding water. It is fracture-field only, uses `OCEAN_FLOOR_WG`, `bury`, spacing/separation `112/56`, salt `78064702`, and contains no lava or loot. Git blob authority: `6d9547a67c32c2dcf8dad6a9ac0aeebf087bfc6c`.
3. **OSF-007 — Lava-tube skylights and collapse windows — IMPLEMENTED COMPONENT / STATIC-MECHANICAL COMPLETE.** `infinite_domain:abyssal/cooled_lava_tube_with_skylight` is deliberately a full OSF-006 parent-tube variant rather than a standalone fake hole. It contains an irregular roof breach, broken elevated basalt rim, asymmetric tuff/blackstone/gravel rubble cone and preserved swim-through lane. The OSF-006 template pool selects intact tube versus collapse variant at `3:1`; the validator enforces the parent relationship. Git blob authority: `30af285e59d6e4a0b9b6c14bf9bfc67443c1aef7`.
4. **OSF-019 — Pockmark fields — IMPLEMENTED SYSTEMIC / STATIC-MECHANICAL COMPLETE.** No duplicate decorative NBT was added. `custom_worldgen:abyssal_mottled_collapse_pattern` is the authoritative non-grid pockmark/collapse pattern, mixed into `custom_worldgen:abyssal_pattern_depression` behind `custom_worldgen:abyssal_plain_mask`, then carried through the existing western/eastern depth-depression chains. The validator fails if those density-function references become disconnected. Runtime depression readability and surface-material expression remain unmeasured.
5. **OSF-023 — Shelf sand-wave / ripple fields — IMPLEMENTED / STATIC-MECHANICAL COMPLETE.** `infinite_domain:abyssal/shelf_sand_wave_field` is a deterministic `49×4×49` sand/gravel/clay structure containing curved broken primary crests, an oblique second current patch, varied crest heights, lee-side sediment toes and local scour interruptions. Because no authoritative shallow-shelf tag currently exists, the first implementation is intentionally restricted to `#infinite_domain:abyssal_slope_biomes` rather than inventing geography. It uses `OCEAN_FLOOR_WG`, `bury`, spacing/separation `64/32`, salt `78064703`. Git blob authority: `9cbe79e3e6a57619c9de18ab88b4a659af80653d`.
6. **OSF-027 — Turbidity-current channels — IMPLEMENTED SYSTEMIC / STATIC-MECHANICAL COMPLETE.** `custom_worldgen:abyssal_turbidity` drives a narrow `abyssal_turbidity_channel_pattern` and broader `abyssal_turbidity_levee_pattern`. The channel is masked across the continental-slope band and into the abyssal-plain transition, then mixed into `abyssal_pattern_depression` at `+0.055`; roughness-modulated shoulders are mixed at `-0.018` to produce a small opposing/depositional margin term. Both feed the existing western/eastern corridor-gated depth-depression chain, so the feature remains terrain-scale and cannot bypass central-continent protection. The deformation validator requires the noise, channel, levee, slope/plain masks and shared-depression references to remain connected. Runtime thalweg continuity, levee readability, scale and submarine navigation remain unmeasured.
7. **OSF-037 — Manganese/polymetallic nodule-field analogues — ACTIVE IMPLEMENTATION.** Deterministic generator staged as `tools/abyssal_rebuild/generate_nodule_field.py`; target is a `41×2×41` low-relief abyssal-plain field with five irregular provinces, broad native-sediment gaps and a current-scoured corridor. It uses gravel, blackstone, cobbled deepslate and sparse polished-blackstone-button accents only—no ore blocks, loot or progression material. Expected generated Git blob: `92ee54237b0fe4090e153c7b539012a3d484e7e7`. It remains non-spawning until materialization and registration gates finish.
8. **OSF-045 — Whale-fall sites.**
9. **OSF-049 — Wood-fall sites.**

Each specification records implementation class, target biome/depth selectors, footprint/vertical range, projection/terrain adaptation, density or spacing intent, palette, geometry contract, hazards, loot/progression policy and explicit deferred runtime checks. The validator supports independently registered structures, parent-correlated components and systemic terrain implementations without conflating their validation requirements.

## Deferred runtime checks

Static refinement does not prove live appearance. Runtime validation must eventually inspect bubble-column behavior, burial/projection, sediment transitions, vent silhouette, feature density, submarine clearance, terrain-feature correlation, flooding continuity and chunk-generation cost.
