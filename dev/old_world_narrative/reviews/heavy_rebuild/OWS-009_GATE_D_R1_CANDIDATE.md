# OWS-009 Gate D r1 — Final Authoritative Shipping Candidate

**Target:** OWS-009 — Atlas Roadside Automated Repair Depot  
**Procedure authority:** `docs/HEAVY_REBUILD_DOCTRINE.md`  
**Artifact:** `old_world_narrative/reviews/heavy_rebuild/visual/OWS-009/gate_d_final/r1/review_manifest.json`  
**Contact sheet:** `old_world_narrative/reviews/heavy_rebuild/visual/OWS-009/gate_d_final/r1/contact_sheet.png`  
**Authoritative synchronization:** `old_world_narrative/reviews/heavy_rebuild/visual/OWS-009/gate_d_final/r1/authoritative_sync.json`  
**Visual regression metrics:** `old_world_narrative/reviews/heavy_rebuild/visual/OWS-009/gate_d_final/r1/visual_regression_metrics.json`  
**Revision:** `gate-d-r1@74a229a6`  
**Fixed camera set:** `ows009_fixed_v1`  
**Status:** **REVIEW NEEDED — independent Gate-D inspection required**

## Authoritative-source proof

The candidate was rendered directly from:

`kubejs/data/infinite_domain/structure/wasteland/old_world/ows_009_atlas_roadside_repair_depot.nbt`

The target-local Gate-D renderer resolves production dispatch to `old_world_ows009_final.build_009`, invokes the canonical production Python, applies normal `base.stabilize_door_pairs`, asserts the final production contracts, serializes a temporary probe and compares it to shipping.

- stabilized builder serialized SHA-256: `261ad9b53740a55a791fa0f7f06915123f95e347704e5a8238efa25bebbeafd9`;
- shipping NBT SHA-256: `261ad9b53740a55a791fa0f7f06915123f95e347704e5a8238efa25bebbeafd9`;
- exact serialized-byte match: **true**;
- builder and shipping decompressed SHA-256: `d2159e70caa0a801ff0d69ad199824760931c38c4c4b07a1d8114d9099893450`;
- exact decompressed-byte match: **true**;
- serialized size: `51,907` bytes;
- decompressed size: `650,218` bytes;
- render source: **shipping NBT**;
- dimensions: `49 x 18 x 41` with every serialized position in bounds.

## Final mechanical evidence

- all nine Pass-19 additions are present at their declared east/rear service and machine-support positions, with no replacement or removal relative to accepted Gate-C D3;
- exactly one contract-required `create:andesite_casing` remains at `(34,2,28)`, grounded on the accepted Bay-03 rear-service floor and connected to the adjacent service wall; all other Pass-19 additions are vanilla cobwebs or mushrooms;
- exactly one canonical proof chest remains at `(37,2,29)`, with exactly one serialized reference to `infinite_domain:chests/old_world/ows_009_atlas_roadside_repair_depot`;
- exactly three bounded spawners remain at `(6,2,21)`, `(23,2,21)` and `(43,2,33)`;
- all 967 cells across the eight protected route regions remain clear;
- required-block counts are 1 andesite casing, 1,961 steel blocks, 387 framed glass, 246 fluid pipes, 169 oxidized copper grates, 27 moss blocks and 35 weathered cut copper blocks;
- structural lint passes with 19 working doors, zero orphan halves, 387 window blocks, 263 functional fixtures, 15 dense levels and 17 footprint variants.

## Visual-regression evidence

Comparison against the independently accepted Gate-C r1 D3 fixed-camera views reports:

- mean visible-change ratio across six principal views: `0.00303996170420283`;
- exterior-view mean: `0.002537842769735763`;
- maximum single-view ratio: `0.0056434860934943655`, in the fixed Y<=6 interior cutaway;
- foreground-silhouette ratio: exactly `1.0` in all six principal views;
- automated decision: `IMAGE_LEVEL_REGRESSION_CHECKS_PASSED_PENDING_INDEPENDENT_REVIEW`.

The small visible deltas are consistent with the nine localized Pass-19 additions, while the unchanged silhouettes demonstrate no massing or damage-footprint expansion. Exact NBT position checks independently prove the final additions. Regression metrics do not constitute visual approval.

## Independent reviewer obligations

Inspect all four exterior quarters, roof/top oblique, fixed Y<=6 interior cutaway, floor slices and contact sheet. Confirm the six Gate-C-frozen aspects remain intact:

1. exact accepted D0 architecture;
2. D1 repair plates, recheck datums, service collars, bypasses and parts/core backlog;
3. D3 east/rear moisture path and localized Bay-03, parts-roof and core-canopy degradation;
4. gravity-consistent landed material;
5. all three repair cells, principal routes, utilities, records/proof approach and Atlas identity;
6. bounded encounters and single controlled proof node.

Also confirm Pass-19 detail remains restrained inside the accepted east/rear degradation zones; the sole required casing reads as grounded, connected machine support; vanilla cobweb/mushroom additions create no visual noise, obstruction, floating element, accidental repetition, damage-footprint expansion or loss of roadside repair-depot identity.

No target-worker visual decision is recorded. Gate D, Pass 20, quality scoring and promotion remain blocked until an independent reviewer dispositions this exact r1 artifact.

**OWS-009 GATE D r1: REVIEW NEEDED.**
