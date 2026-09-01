# Wasteland Hex-Cave Runtime Implementation Reconciliation

Date: 2026-08-31  
Branch: `main`  
Method: DEEFM (`INTENT -> EXECUTE -> OBSERVE -> VERIFY -> CLAIM`)

## INTENT

Implement the Wasteland cave doctrine as a shipping Infinite Domain runtime component, not as source-only development material. Wasteland caves must preserve a literal recognizable hexagonal corridor/cell lattice as carved cave geometry while deterministic world-seed fractal/plasma fields warp, widen, occlude, interrupt, and locally open that lattice.

## EXECUTE

The project-owned NeoForge source remains at `dev/packdev/wasteland-hex-caves/`, while the actual game-facing runtime artifact now ships outside `dev/` at:

`mods/infinite-domain-wasteland-hex-caves-1.0.0.jar`

The runtime JAR contains the compiled Java 21 implementation plus its NeoForge metadata and data-driven worldgen registrations:

- `infinitedomain/wastelandhexcaves/HexCaveFeature.class` and its geometry records;
- `infinitedomain/wastelandhexcaves/WastelandHexCaves.class`;
- `infinitedomain/wastelandhexcaves/WastelandNamespaceBiomeModifier.class`;
- `META-INF/neoforge.mods.toml`;
- configured feature `infinite_domain_wasteland_hex_caves:hex_caves`;
- placed feature `infinite_domain_wasteland_hex_caves:hex_caves`;
- NeoForge biome modifier `infinite_domain_wasteland_hex_caves:wasteland_namespace`.

The implementation:

- registers `infinite_domain_wasteland_hex_caves:hex_caves` as a custom `Feature<NoneFeatureConfiguration>`;
- injects the placed feature only when the biome registry namespace is `the_wasteland_reworked` or `wastelands`;
- derives geometry and noise from world coordinates plus `WorldGenLevel#getSeed()`;
- constructs the visible lattice from axial hex coordinates and the two-nearest-center Voronoi boundary rather than stamping an image;
- uses fBm fields for spatial warp, corridor-width variation, macro occlusion, plasma-scale interruption, depth variation, and larger low-noise chambers;
- keeps cave carving at least ten blocks below the world-generation surface;
- replaces only ordinary natural overworld material and refuses fluids, block entities, and non-natural structure materials.

The biome-modifier codec is the direct single-field `PlacedFeature.CODEC.fieldOf("feature").xmap(...)` mapping, keeping the runtime serialization contract minimal and identical to the JSON resource.

## OBSERVE

Compiled artifact observations:

| Measurement | Result |
|---|---|
| runtime path | `mods/infinite-domain-wasteland-hex-caves-1.0.0.jar` |
| artifact size | 13,889 bytes |
| Git blob SHA | `6b4a78dfbd33fefc6f1b7496f65d978210213cff` |
| SHA-256 | `b046e705662e7a03e61e815529ad0e1ad55dd871b273697ad928756b3f749a91` |
| Java target | Java 21 |
| development/stub classes packaged | none |

The retained deterministic validator `dev/scripts/validate_wasteland_hex_caves.py` mirrors Java signed-`long` overflow and unsigned-shift behavior. For seed `123456789` over a 512 x 512 reference field sampled every two blocks it measures:

| Measurement | Result |
|---|---:|
| raw literal hex-grid corridor field | 28.5% |
| surviving visible grid after fractal/plasma occlusion | 22.5% |
| actually occluded/interrupted grid | 6.0% |
| larger fractal chamber field | 4.3% |

## VERIFY

The compiled class linkage was inspected after build. The emitted descriptors for NeoForge registration, `BiomeModifier`, biome generation settings, `PlacedFeature.CODEC`, `FeaturePlaceContext`, `WorldGenLevel`, block-state access, and worldgen block replacement match the NeoForge/Minecraft 1.21.1 API contracts used by the authoritative pack. The shipped JAR was then read back from GitHub at the exact runtime path and its Git blob SHA matches the locally built artifact.

This environment does not provide the full authoritative Minecraft instance process, so this record does not invent a claim that NeoForge has launched the JAR or that a fresh fixed-seed world has already been visually inspected.

## CLAIM

**IMPLEMENTED AND PACKAGED — the Wasteland hex-cave system now has a compiled project-owned runtime JAR in the shipping `mods/` boundary.**

Fresh-world runtime loading and visual/distribution inspection remain acceptance evidence to collect; they are no longer an implementation or packaging prerequisite left undone.
