# OWS-007 Gate D r1 — Final Authoritative Shipping Candidate

**Target:** OWS-007 — Verdant Continuum Foods EP-7 Agricultural Development Laboratory  
**Procedure authority:** `docs/HEAVY_REBUILD_DOCTRINE.md`  
**Artifact:** `old_world_narrative/reviews/heavy_rebuild/visual/OWS-007/gate_d_final/r1/review_manifest.json`  
**Contact sheet:** `old_world_narrative/reviews/heavy_rebuild/visual/OWS-007/gate_d_final/r1/contact_sheet.png`  
**Authoritative synchronization:** `old_world_narrative/reviews/heavy_rebuild/visual/OWS-007/gate_d_final/r1/authoritative_sync.json`  
**Visual regression metrics:** `old_world_narrative/reviews/heavy_rebuild/visual/OWS-007/gate_d_final/r1/visual_regression_metrics.json`  
**Revision:** `gate-d-r1@local`  
**Fixed camera set:** `ows007_fixed_v1`  
**Status:** **REVIEW NEEDED — independent Gate-D inspection required**

## Authoritative-source proof

The candidate was rendered directly from:

`kubejs/data/infinite_domain/structure/wasteland/old_world/ows_007_vcf_ep7_agricultural_development_laboratory.nbt`

The target-local Gate-D renderer resolves production dispatch to `old_world_ows007_final.build_007`, invokes the canonical production Python, applies normal `base.stabilize_door_pairs`, serializes a temporary probe and compares it to shipping.

- stabilized builder serialized SHA-256: `0ef9d164449226a53c766a96ead39b0df4d454e369c545974b4d5bbb2acb3436`;
- shipping NBT SHA-256: `0ef9d164449226a53c766a96ead39b0df4d454e369c545974b4d5bbb2acb3436`;
- exact serialized-byte match: **true**;
- builder and shipping decompressed SHA-256: `b515674b364b1afec34070ea8f2dd88b6b47040825770f54c6fcff393d3d10fa`;
- exact decompressed-byte match: **true**;
- serialized size: `139,214` bytes;
- decompressed size: `1,737,237` bytes;
- render source: **shipping NBT**;
- dimensions: `73 x 33 x 63`.

## Final mechanical evidence

- the required `minecraft:mycelium` correction is serialized at `(61,1,42)`;
- normal production stabilization restores the rear Chamber-B iron-door half at `(23,2,45)`;
- the one canonical proof chest remains at `(43,2,55)` with exactly one canonical loot-table reference;
- the accepted three-spawner encounter topology remains present;
- all nine Pass-19 details are represented in the shipping serialization.

## Visual-regression evidence

Comparison against the independently accepted Gate-C r1 D3 fixed-camera views reports:

- mean visible-change ratio across six principal views: `0.0`;
- exterior-view mean: `0.0`;
- maximum single-view ratio: `0.0`;
- exterior, roof and cutaway foreground-silhouette ratios: exactly `1.0`;
- automated decision: `IMAGE_LEVEL_REGRESSION_CHECKS_PASSED_PENDING_INDEPENDENT_REVIEW`.

The zero image delta is a renderer limitation, not evidence that serialization did not change: the nine localized Pass-19 cells and restored interior door half are occluded or sub-voxel in the primitive projections. Exact NBT position checks independently prove those changes. Regression metrics only establish that final shipping has not caused visible macro drift.

## Independent reviewer obligations

Inspect all four exterior views, roof/top oblique, interior cutaway, floor slices and contact sheet. Confirm:

1. all eight aspects frozen at Gate C remain visually intact;
2. the corrected white-mullion/light-gray-beam observation facade remains supported and unbroken;
3. Pass-19 detail does not broaden the west-plant, Chamber-B, wash/decon or rotunda-humidity damage zones;
4. the stabilized rear door introduces no clipping, floating element or route obstruction;
5. the public threshold, three trial chambers, phenotyping hinge, service lane, bridge, rotunda, proof approach and VCF identity remain legible;
6. roof openings and landed debris retain the accepted causal freeze/thaw and water-ingress history;
7. all four elevations, roof composition, ground transition, entrances and hero spaces remain free of major defects, accidental repetition and excessive detail;
8. the final ruin still reads as a high-quality agricultural development laboratory rather than a decorated box.

No target-worker visual decision is recorded. Gate D, Pass 20, quality scoring and promotion remain blocked until an independent reviewer dispositions this exact r1 artifact.
