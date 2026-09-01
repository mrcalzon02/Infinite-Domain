# Wasteland Hex-Cave Source Implementation Reconciliation

Date: 2026-08-31  
Branch: `main`  
Method: DEEFM (`INTENT -> EXECUTE -> OBSERVE -> VERIFY -> CLAIM`)

## INTENT

Advance current reconciliation item 1 without inventing a generic overworld noise-router replacement or modifying either third-party Wasteland jar. The required geometry is a literal, recognizable hexagonal cave lattice whose carved corridors/cells survive while deterministic world-seed fractal/plasma fields warp, widen, occlude, interrupt, and locally open the lattice.

## EXECUTE

A dedicated project-owned NeoForge source module now lives at `dev/packdev/wasteland-hex-caves/`.

The implementation:

- registers `infinite_domain_wasteland_hex_caves:hex_caves` as a custom `Feature<NoneFeatureConfiguration>`;
- registers a custom biome-modifier serializer that adds the placed feature only when the biome registry namespace is `the_wasteland_reworked` or `wastelands`;
- derives all geometry and noise from world coordinates plus `WorldGenLevel#getSeed()`;
- constructs the visible lattice from axial hex coordinates and the two-nearest-center Voronoi boundary rather than stamping an image;
- uses fBm fields for spatial warp, corridor-width variation, macro occlusion, plasma-scale interruption, depth variation, and larger low-noise chambers;
- keeps the cave at least ten blocks below the world-generation surface;
- replaces only ordinary overworld base stone, dirt, or gravel and refuses fluids, block entities, and non-natural structure materials.

The custom namespace biome modifier intentionally avoids a compile-time dependency on either Wasteland mod's internal classes or individual biome IDs.

## OBSERVE

The exact source/resource payload was checked with the retained deterministic validator `dev/scripts/validate_wasteland_hex_caves.py`. The validator mirrors Java signed-`long` overflow and unsigned-shift behavior so the reference noise field matches the committed Java implementation rather than a Python-only approximation.

Deterministic reference field: seed `123456789`, 512 x 512 block domain sampled every two blocks.

Observed coverage:

| Measurement | Result |
|---|---:|
| raw literal hex-grid corridor field | 28.5% |
| surviving visible grid after fractal/plasma occlusion | 22.5% |
| actually occluded/interrupted grid | 6.0% |
| larger fractal chamber field | 4.3% |

The validation also parses the configured-feature, placed-feature, and biome-modifier JSON and checks the world-seed, literal-hex, surface-margin, natural-material, target-namespace, and underground-generation source contracts. Commit `1bc11942ea7cbec454f5b6b849406442237732fd` contains the final occlusion/chamber tuning used by the retained validator.

## VERIFY

Static/reference validation result: **PASS**.

The implementation shape was cross-checked against NeoForge 1.21.1's documented `BiomeModifier`, `MapCodec`, `DeferredRegister`, `PlacedFeature`, `FeaturePlaceContext`, and `WorldGenLevel#getSeed()` APIs.

This environment does not expose the authoritative Minecraft/NeoForge compiler/runtime. The repository's existing `dev/packdev/*` custom-mod modules are also source-only and do not contain per-module Gradle wrappers/build metadata. Therefore this pass does not claim bytecode compilation, JAR installation, mod loading, fresh-world generation, or visual acceptance.

## CLAIM

**Source implementation is present and statically/reference validated. Runtime acceptance remains OPEN.**

The reconciliation item must not be marked complete until this source is compiled into the project-owned runtime JAR outside `dev/`, loaded in the authoritative NeoForge 1.21.1 instance, generated in a fresh fixed-seed Wasteland world/region, and visually verified to retain recognizable hex corridors/cells without surface, fluid, or structure regressions.
