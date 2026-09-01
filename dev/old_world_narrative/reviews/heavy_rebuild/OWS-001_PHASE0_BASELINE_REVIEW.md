# OWS-001 Phase-0 Baseline Review

## Authority and scope

**Target:** OWS-001 — Verdant Continuum Foods Neighborhood Culture Service Depot  
**Procedure authority:** `docs/HEAVY_REBUILD_DOCTRINE.md` at procedure revision `2b6fa9637771f059b65a4bd095c876036ff2f7cd`  
**Baseline source commit:** `283bcb310f5bbd3c595129fedadbee3018e079a2`  
**Fixed-camera set:** `ows001_fixed_v1`  
**Baseline artifact set:** `old_world_narrative/reviews/heavy_rebuild/visual/OWS-001/baseline/r0_pre_heavy_rebuild/`  
**Dimensions:** 39 x 13 x 33

This review restarts OWS-001 from the top. It does not inherit visual approval from the previous `c145ed6` heavy-rebuild attempt. The already-shipped functional IDs, proof item, worldgen relationships and quest hooks remain protected independently from schematic quality.

## Baseline review method

The fixed-camera Phase-0 set has been generated from the exact historical NBT and retained as the visual comparison baseline. Findings below are cross-checked against the exact historical `build_001()` so no design feature is credited merely because a colored block happens to read ambiguously in the primitive renderer.

The baseline builder preserves `grocery_clean_master()` almost completely and adds only:

- a white/lime facade patch and shallow front identity volume;
- six `oritech:cooler_block` fixtures in one line;
- a crate cluster;
- a lime block cluster;
- a pallet cluster;
- one yellow quality-hold field and barred area;
- the deterministic evidence chest.

That makes the baseline useful as a record of the old implementation, not as architecture to preserve wholesale.

## Phase-0 visual and spatial findings

### 1. Massing and silhouette

**Finding: rebuild required.**

The underlying building remains the low rectangular grocery donor. The VCF overlay does not materially change the silhouette, service massing, roofline, or relationship between public and industrial functions. From a distance the building is still fundamentally an ordinary commercial box with a colored identity patch.

The neighborhood scale itself is appropriate. The problem is not that the structure is small; the problem is that the existing volume has not been architecturally reinterpreted around biological culture service.

### 2. Entrance hierarchy

**Finding: partially useful donor geometry, rebuild required.**

The existing front approach and threshold position are useful because OWS-001 should feel like mundane neighborhood infrastructure. The entrance does not yet have a strong VCF service-depot hierarchy, clear public issue sequence, separate returns cue, or architectural distinction between customer and staff/service access.

### 3. Corporate identity

**Finding: failed baseline condition.**

VCF identity is communicated primarily through lime/white color placement. The baseline does not provide the full **VERDANT CONTINUUM FOODS** name, a proper **NEIGHBORHOOD CULTURE SERVICE DEPOT** identity installation, or a company-specific architectural grammar. This matches the institutional anti-pattern explicitly forbidden by the build-style registry: `supermarket plus green stripe`.

### 4. Roof composition and service infrastructure

**Finding: rebuild required.**

The baseline inherits the donor roof rather than showing an intentionally composed cold-chain service roof. There is no convincing visible relationship between refrigeration fixtures below and rooftop refrigeration, ventilation, maintenance access, pipe/conduit routing, or protected service equipment.

The existing roof envelope is usable as raw geometry. Its final composition is not.

### 5. Public / staff / freight separation

**Finding: failed baseline condition.**

The historical builder does not reconstruct the grocery floor plan. Public issue, public returns, staff handling, freight receiving, clean stock, dirty returns, sanitation, quality hold, crate consolidation, and dispatch therefore do not exist as a coherent architectural sequence.

This is the central reason the baseline cannot survive as the final layout.

### 6. Cold-chain architecture

**Finding: failed baseline condition.**

Six cooler blocks form a fixture line, not a refrigerated culture-locker hall. There is no controlled staff aisle, clean-holding hierarchy, batch-check handoff, service relationship, or visible mechanical support.

### 7. Return / sanitation / quality-hold story

**Finding: rebuild required.**

The yellow field and barred zone correctly suggest that one local problem has been isolated rather than the entire depot collapsing. That historical scale is worth preserving.

However, the baseline does not physically explain how returned cultures reach that bay, how they are inspected or washed, how clean and dirty materials stay apart, or why this particular hold zone exists where it does. The anomaly is therefore a marker rather than a workflow consequence.

### 8. Rear service relationship

**Finding: donor relationship worth preserving; architecture must be rebuilt.**

The rear receiving/loading relationship is appropriate for a neighborhood depot and should remain the main freight side. It needs explicit delivery threshold, batch/temperature inspection, clean stock staging, returned-crate consolidation, service dispatch, and staff-only control.

### 9. Evidence placement

**Finding: mechanics preserved, architectural placement must be rebuilt.**

The deterministic evidence chest is mechanically correct but the baseline does not build a convincing supervisor, batch-records, dispatch-control, or secured records station around it. The final container should remain deterministic while moving only if necessary to a place where the records naturally belong.

### 10. Damage-state readability

**Finding: useful restraint, insufficient causal layering.**

OWS-001 should remain an early-anomaly site. The baseline correctly avoids generalized apocalypse. Keep that restraint.

The final historical sequence must nevertheless show causality: normal return service -> repeated failed quality check -> local bay isolation / temporary operating workaround -> later abandonment and long decay. D1 cannot simply be yellow concrete added to D0.

## Donor disposition after Phase 0

### Retain

- 39 x 13 x 33 neighborhood scale, provisionally;
- street/parking relationship;
- primary front-approach orientation;
- rear loading/service relationship;
- useful masonry shell portions;
- roof envelope as raw space for a redesigned cold-chain plant;
- ordinary commercial context, because VCF should feel ubiquitous rather than secret.

### Rebuild

- complete front facade hierarchy;
- entrance canopy / public threshold;
- side and rear institutional articulation;
- roof composition and mechanical plant;
- entire supermarket sales-floor program;
- all public/staff/freight circulation;
- cold locker hall;
- receiving and batch inspection;
- clean stock;
- return intake;
- sanitation and inspection;
- quality hold;
- return-crate consolidation;
- service dispatch;
- supervisor / batch records;
- lighting, ceiling and utility systems;
- purposeful signage and wayfinding;
- final collapse/decay layers.

### Remove as inherited identity

- supermarket checkout logic;
- retail browsing aisles;
- produce/bakery/gondola identity;
- retail merchandising logic;
- generic grocery cooler-wall reading;
- corporate identity expressed mainly through green blocks.

## Phase-0 decision

**Baseline review result: COMPLETE — REBUILD REQUIRED.**

This is not a quality pass. It is a successful baseline gate because the old condition is now preserved and its defects are recorded before reconstruction.

OWS-001 may proceed to Pass 2 only under these constraints:

1. the neighborhood scale remains provisional rather than sacred;
2. no room survives merely because it existed in the grocery donor;
3. VCF identity must be architectural before it is decorative;
4. clean product and returned biological material must have different physical routes;
5. the early anomaly remains local and operationally understandable;
6. Gate A must review a new **D0 massing-only** interpretation before interior detail is allowed to hide macro defects;
7. OWS-002 remains locked until OWS-001 completes all blocking visual gates and the final quality threshold.
