# [SYSTEM REPORT] OWS-005 Gate D r1 — Final Shipping Candidate

**Target:** OWS-005 — Verdant Continuum Foods Harvest & Packaging Annex  
**Procedure authority:** `docs/HEAVY_REBUILD_DOCTRINE.md`  
**Artifact:** `old_world_narrative/reviews/heavy_rebuild/visual/OWS-005/gate_d_final/r1/review_manifest.json`  
**Contact sheet:** `old_world_narrative/reviews/heavy_rebuild/visual/OWS-005/gate_d_final/r1/contact_sheet.png`  
**Authoritative synchronization:** `old_world_narrative/reviews/heavy_rebuild/visual/OWS-005/gate_d_final/r1/authoritative_sync.json`  
**Visual regression metrics:** `old_world_narrative/reviews/heavy_rebuild/visual/OWS-005/gate_d_final/r1/visual_regression_metrics.json`  
**Revision:** `gate-d-r1@local`  
**Fixed camera set:** `ows005_fixed_v1`  
**Status:** **REVIEW NEEDED — independent Gate-D inspection required**

## Authoritative-source proof

The candidate was rendered from the actual shipping NBT:

`kubejs/data/infinite_domain/structure/wasteland/old_world/ows_005_vcf_harvest_packaging_annex.nbt`

The target-local renderer resolves the production dispatch to `old_world_ows005_final.build_005`, applies the same `base.stabilize_door_pairs` operation used by normal generation, and serializes a temporary probe. Production stabilization restores the door halves at `(20,3,6)` and `(27,2,38)`.

- stabilized builder serialized SHA-256: `3f11c4d6af6b09507e6a05c018d57d408b1ce71244914e619160ff3916ad1208`;
- shipping NBT SHA-256: `3f11c4d6af6b09507e6a05c018d57d408b1ce71244914e619160ff3916ad1208`;
- exact serialized-byte match: **true**;
- decompressed NBT SHA-256: `2a514f626ed51e689b6b03ec920eabf67f453ae9d0858822c96449fa81182dfa`;
- exact decompressed-byte match: **true**;
- decompressed NBT size: `1,073,724` bytes;
- render source: **shipping NBT**;
- dimensions: `59 x 24 x 51`.

## Mechanical regression evidence

The fixed-camera comparison against independently accepted Gate-C r1 D3 reports:

- mean visible-change ratio across six principal views: `0.0009327`;
- exterior-view mean: `0.0005354`;
- maximum single-view ratio: `0.0027526` in the interior cutaway;
- exterior, roof and interior foreground silhouette ratios: exactly `1.0` in every compared view;
- image-level regression decision: `IMAGE_LEVEL_REGRESSION_CHECKS_PASSED_PENDING_INDEPENDENT_REVIEW`.

These are automated drift guards only. They demonstrate that the shipping transition remains at microdetail/stabilization scale and do not constitute visual approval.

## Independent reviewer obligations

Inspect all four exterior views, roof/top oblique, interior cutaway, floor slices and contact sheet. Confirm:

1. all nine aspects frozen at Gate C remain visually intact;
2. Pass-19 weathering stays localized to accepted damage zones and does not broaden the ruin footprint;
3. the restored door halves are correctly formed and introduce no clipping, floating geometry or route obstruction;
4. the public pavilion, line 01, cold hold A, freight thresholds, central process routes, QA/proof route and VCF identity remain legible;
5. wet-line-02, rear-monitor/packing-line-02, refrigeration-B/cold-hold-B and receiving-bay-02 causal damage remains coherent;
6. roof composition, ground transition, main entrances, hero spaces and all four elevations remain free of major defects, accidental repetition or excessive detail;
7. the final ruin still reads as a high-quality harvest and packaging annex rather than a decorated box.

No target worker visual decision is recorded. Gate D, Pass 20, quality scoring and promotion remain blocked until an independent reviewer dispositions this exact r1 artifact.
