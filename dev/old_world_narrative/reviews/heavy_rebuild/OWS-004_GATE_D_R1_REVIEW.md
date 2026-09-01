# [SYSTEM REPORT] OWS-004 Gate D r1 — Final Multi-Angle Visual Review

**Target:** OWS-004 — Verdant Continuum Foods Mycological Vertical Farm Tower  
**Procedure authority:** `docs/HEAVY_REBUILD_DOCTRINE.md`  
**Artifact:** `old_world_narrative/reviews/heavy_rebuild/visual/OWS-004/gate_d_final/r1/review_manifest.json`  
**Synchronization:** `old_world_narrative/reviews/heavy_rebuild/visual/OWS-004/gate_d_final/r1/authoritative_sync.json`  
**Regression metrics:** `old_world_narrative/reviews/heavy_rebuild/visual/OWS-004/gate_d_final/r1/visual_regression_metrics.json`  
**Static workflow run:** `32545469189`  
**Fixed camera set:** `ows004_fixed_v1`  
**Decision:** **PASSED**

## Authoritative synchronization

Gate D rebuilt OWS-004 through `old_world_narrative_core.BUILDERS["OWS-004"]`, which resolves directly to `old_world_ows004_final.build_004`, applied normal production door stabilization, and compared that serialization against the generated shipping structure before rendering the shipping NBT itself.

Verified result:

- dimensions: **51 x 47 x 47**;
- decompressed NBT: **1,505,368 bytes**;
- authoritative-builder SHA-256: `3c75be18613208a59daa0bb90d5810f10564fa018d77b87870f413d01d890b62`;
- shipping-NBT SHA-256: `3c75be18613208a59daa0bb90d5810f10564fa018d77b87870f413d01d890b62`;
- exact decompressed-NBT match: **true**;
- final render source: **shipping NBT**.

There is therefore no review-versus-shipping geometry gap.

## Manual fixed-camera review

The exact persisted Gate-D contact sheet, floor-slice sheet and fixed-camera shipping-NBT images from static run `32545469189` were inspected directly.

**Front-left:** PASSED. The tower preserves the accepted stepped production hierarchy, framed cultivation bands, east service spine, lower public/logistics podium and damaged greenhouse crown. Pass-19 detail does not alter the silhouette or introduce a new historical event.

**Rear-left:** PASSED. The west egress/service mass remains visually subordinate to the main production tower while remaining identifiable. Rear service architecture and the accepted upper deterioration pattern remain coherent.

**Rear-right:** PASSED. Production floors retain repeated agricultural-industrial rhythm, service anatomy and reconstructable vertical organization. No final detail obscures the intact-to-containment-to-abandonment chronology.

**Front-right:** PASSED. The public/demo base remains distinct from the heavier service/logistics side, and the tall service spine reads as part of the controlled-environment system rather than an unrelated annex.

**Roof/top:** PASSED. The greenhouse/environmental crown retains the Gate-C r4 failure geometry, surviving service organization and roof access relationships. Pass 19 remains local and does not change the accepted roof/site outline.

**Interior cutaway / floor review:** PASSED. The fixed cutaway remains biased toward the low podium at roughly Y=7, as already documented, while the persisted floor slices provide the required higher-level evidence. The four cultivation decks, protected staff circulation, freight/service core, west secondary egress and upper containment/disruption layer remain legible and distinct.

## Post-Gate-C regression check

The image-level guard confirms that Pass 19 stayed genuinely microdetail-scale relative to the manually approved Gate-C r4 D3 state:

- front-left visible change: **0%**;
- rear-left: ~**0.0340%**;
- rear-right: ~**0.0254%**;
- front-right: **0%**;
- roof/top: ~**0.0440%**;
- interior cutaway: **0%**;
- average all-view change: ~**0.0172%**;
- average exterior change: ~**0.0149%**;
- maximum single-view change: ~**0.0440%**;
- silhouette retention: **1.0 in every analyzed view**.

These values are far below the regression rejection thresholds and confirm that the final builder is not a disguised redesign after Gate C.

## Progression, circulation and evidence check

The final generated structure record and authoritative builder preserve:

- the principal production-staff stair from podium through cultivation levels to the crown;
- the separate west secondary egress ladder;
- the distinct east freight/material-transfer function;
- environmental risers and floor-level service branches;
- four repeated cultivation decks and surviving mycological production evidence;
- exactly **two** optional vanilla D3 encounter spawners;
- canonical proof chest at `(32, 2, 12)`;
- canonical proof loot table `infinite_domain:chests/old_world/ows_004_vcf_mycological_vertical_farm_tower`;
- canonical proof item `kubejs:evercrop_cultivation_handbook`;
- runtime/worldgen approval as **deferred**, not inferred from this static review.

The synchronized generated structure is **51 x 47 x 47**, contains **41,516 placed blocks**, **63 palette states**, **5,683 modded blocks**, **2 spawners**, **24 working doors**, **0 orphan door halves**, **297 functional fixtures**, and a **37-block vertical-access span**, with structural lint reporting no issues.

## Gate-D r1 decision

**OWS-004 GATE D r1: PASSED.**

The final preview is synchronized exactly to authoritative shipping NBT, visually preserves the accepted Gate-C r4 architecture and history, and adds only restrained Pass-19 microdetail. OWS-004 may proceed to final static-quality scoring and guarded promotion. This decision does not grant runtime/worldgen approval.
