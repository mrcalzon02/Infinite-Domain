# [SYSTEM REPORT] OWS-001 — Final Heavy-Rebuild Report

**Structure ID:** OWS-001  
**Structure name:** Neighborhood Culture Service Depot  
**Organization:** Verdant Continuum Foods (VCF)  
**Building type:** compact public biological-food culture issue/return depot with controlled cold-chain back-of-house processing  
**Original dimensions:** 39 x 13 x 33  
**Revised dimensions:** 39 x 13 x 33  
**Quality status:** peak-quality static schematic approved; runtime validation remains separate  

## Real-world precedent types studied

The rebuild used workflow lessons from:

- a consolidated blood-bank facility combining public/donor, processing, receiving, support and administration functions;
- automated liquid-biobank infrastructure emphasizing standardized processing, managed cold storage, staff aisle/service access and records;
- WHO pharmaceutical warehouse / storage-facility guidance separating receiving, cold storage, staging, loading, dispensing, waste and returns;
- WHO warehouse/stock-management guidance covering inbound checks, controlled storage, dispatch, records, quarantine/quality hold, pallets and reusable containers.

The references were used for adjacency and process logic, not copied literally. OWS-001 remained a neighborhood-scale VCF service facility rather than becoming a hospital, research headquarters or high-security biobank.

## Major architectural changes

The old grocery-derived overlay was rebuilt into a purpose-driven VCF depot while preserving the useful neighborhood scale and front/rear site relationships.

The final building includes:

- a distinct public entrance pavilion and canopy;
- stepped operational masses rather than one undifferentiated retail box;
- separate west return/sanitation and east clean/cold-service zones;
- a protected central staff spine;
- a rear receiving/service frame;
- a supervisor/batch-record room tied to actual process decisions;
- a composed rooftop cold plant with visible service relationship to the refrigeration system;
- clear public, staff, clean-stock, dirty-return and freight/service boundaries.

## Major interior changes

The supermarket sales-floor program was removed.

The final interior now contains a reconstructable operational sequence:

`receiving -> batch/temperature check -> clean stock/cold hold -> culture lockers -> public issue`

and a distinct reverse stream:

`public return -> sanitation/inspection -> quality hold -> crate consolidation -> service dispatch`.

The culture-locker hall is now a repeated refrigeration system with a protected three-block service aisle instead of a decorative cooler line.

The records room, receiving station, sanitation area, quality hold, clean stock and public handoff spaces all have separate functional identities.

## Corporate identity elements

VCF identity is carried by architecture and workflow as well as palette/signage:

- bright white/lime public-facing frontage;
- cleaner public issue side contrasted with more industrial back-of-house service areas;
- visible controlled biological cold-chain architecture;
- return/reuse infrastructure integrated into normal business operations;
- full `VERDANT CONTINUUM FOODS` identity;
- full `NEIGHBORHOOD CULTURE SERVICE DEPOT` identity;
- operational wayfinding for returns, issue, lockers, sanitation, quality hold, receiving, clean stock, records and cold plant.

The final structure no longer reads as “supermarket plus green stripe.”

## Historical/collapse story represented

### D0 — normal operation

A successful, approachable neighborhood VCF depot issues refrigerated cultures and accepts reusable returns as ordinary infrastructure.

### D1 — early anomaly

Operational strain appears internally rather than as apocalypse imagery:

- localized quality/inspection coding;
- increased suspect/replacement return stock;
- extra cold-service maintenance attention;
- batch/temperature exceptions at receiving.

The Gate-C floor-map comparison measured D1 as a restrained 1.66% visible internal change from D0.

### D3 — centuries-later ruin

Decay follows specific causes:

- localized roof/cold-plant water ingress;
- one failed cooler/service segment;
- wet-service deterioration at the west return annex;
- rear receiving weather exposure;
- limited glazing loss;
- localized cracked/mossy masonry;
- interrupted service infrastructure.

The building remains reconstructable and identifiable rather than becoming random rubble.

## Environmental evidence

Before reading the proof item, the player can infer:

- refrigerated biological cultures were issued to ordinary residents;
- returned/reusable material was a normal part of the economy;
- dirty returns and clean stock followed separate routes;
- refrigeration required real rooftop/service infrastructure;
- one ordinary quality-control problem began consuming unusual maintenance attention;
- the final ruin was produced primarily by abandonment, water and failed service systems rather than a generic explosion.

## Spawner encounters

No mandatory deterministic spawner was added.

OWS-001 is intentionally a common narrative-discovery site rather than a combat arena. Ambient hostiles remain sufficient. The west quality-hold/return annex and rear receiving area remain plausible low-intensity occupation/tension pockets if a later pack-wide encounter system requires explicit placement.

## Loot tables used

The existing canonical Old World structure loot table remains authoritative:

`infinite_domain:chests/old_world/ows_001_vcf_neighborhood_culture_service_depot`

No replacement corporate loot system was invented during the rebuild.

## Quest evidence location

The guaranteed proof chest is in the supervisor/batch-record room at the final records position.

Canonical proof item:

`kubejs:vcf_culture_service_manifest`

Associated local lore:

`kubejs:vcf_return_crate_log`

The proof remains deterministic and reachable without destructive excavation.

## Functional validation

The rebuilt authoritative generator has already passed the existing Old World structural/static pipeline.

Generated structural record after the rebuild reports:

- working doors: 11;
- orphan door halves: 0;
- functional fixtures: 81;
- vertical-access span: 7;
- structural lint issues: none.

Final builder assertions additionally protect:

- public entry;
- public approach;
- central three-block staff spine;
- culture-locker three-block aisle;
- clean-stock route and controlled door;
- records route and controlled door;
- rear receiving exit;
- VCF identity signage;
- canonical proof chest/loot table;
- surviving refrigeration evidence;
- functional roof-access ladder.

Runtime world placement/detection is not inferred from this static approval.

## Visual baseline artifact

`old_world_narrative/reviews/heavy_rebuild/visual/OWS-001/baseline/r0_pre_heavy_rebuild/review_manifest.json`

Baseline decision: **REBUILD REQUIRED**.

## Visual Gate A massing artifact

Accepted revision:

`old_world_narrative/reviews/heavy_rebuild/visual/OWS-001/gate_a_massing/r2/review_manifest.json`

Gate-A result: **PASSED r2** after the first massing review was rejected and revised.

## Visual Gate A findings/corrections

The rebuild moved away from the low grocery-donor rectangle toward a stepped neighborhood service building with explicit public threshold, side service identities, rear receiving and roof cold-plant massing.

## Visual Gate B intact-state artifact

Accepted revision:

`old_world_narrative/reviews/heavy_rebuild/visual/OWS-001/gate_b_intact/r3/review_manifest.json`

Gate-B result: **PASSED r3**.

## Visual Gate B findings/corrections

r1 exposed:

- a one-block locker service aisle where three were required;
- a receiving pinch on the central staff spine;
- unusable roof access;
- invalid wall-sign mounting.

r2 then exposed:

- a records doorway opening directly against a process wall;
- no continuous accepted-goods crossing to clean stock.

r3 corrected both crossings explicitly:

- accepted goods cross the process boundary at z=22 into controlled clean stock;
- records access crosses at z=26 into the supervisor room;
- the obsolete z=24 crossing is sealed.

These routes are executable assertions in the final builder.

## Damage states rendered

- D0 intact / normal operation;
- D1 early anomaly / operational strain;
- D3 centuries-later causal ruin.

A separate D2 state was intentionally unnecessary for this small early-anomaly site; its canon does not require the depot to impersonate a major containment battle.

## Visual Gate C comparison artifact

`old_world_narrative/reviews/heavy_rebuild/visual/OWS-001/gate_c_damage_states/r1/gate_c_manifest.json`

Gate-C result: **PASSED r1**.

## Visual Gate C findings/corrections

Measured visible state separation confirmed the intended history:

- D1 floor-map change from D0: ~1.66%;
- D3 floor-map change from D0: ~4.88%;
- D3 visible from every exterior camera;
- building silhouette essentially fully retained.

The damage pass therefore reads as historical transformation rather than random subtraction.

## Visual Gate D final multi-angle artifact

`old_world_narrative/reviews/heavy_rebuild/visual/OWS-001/gate_d_final/r1/review_manifest.json`

Authoritative synchronization record:

`old_world_narrative/reviews/heavy_rebuild/visual/OWS-001/gate_d_final/r1/authoritative_sync.json`

Regression metrics:

`old_world_narrative/reviews/heavy_rebuild/visual/OWS-001/gate_d_final/r1/visual_regression_metrics.json`

Gate-D result: **PASSED r1**.

## Visual Gate D findings/corrections

The final synchronization problem was explicitly corrected before approval.

Gate D now:

1. builds through the production `old_world_narrative_core.BUILDERS["OWS-001"]` dispatch;
2. verifies that dispatch is exactly `old_world_ows001_final.build_001`;
3. applies production door stabilization;
4. serializes the same builder;
5. compares decompressed NBT bytes against shipping NBT;
6. refuses to render on mismatch;
7. renders from the shipping NBT itself.

Verified synchronization:

- decompressed NBT size: 265,063 bytes;
- builder SHA-256: `6241ebe9a5481acd31240c6ad6d917eeecba537cfd8df2eed81b9390ffa6d5c1`;
- shipping SHA-256: `6241ebe9a5481acd31240c6ad6d917eeecba537cfd8df2eed81b9390ffa6d5c1`;
- exact match: yes.

Pass-19 changes remain true microdetail:

- average Gate-D visual change from approved Gate-C D3: ~0.37%;
- average exterior change: ~0.17%;
- maximum single-view change: ~1.56%, in the interior cutaway;
- silhouette retention: exactly 1.0 across every analyzed view.

No new macro architectural or damage defect was introduced after Gate C.

## Known renderer substitutions/limitations

The primitive renderer uses deterministic proxy colors/material categories for many modded blocks. It is suitable for massing, circulation, damage-state and geometry comparison but is not a substitute for final in-game texture/lighting inspection.

This limitation is why runtime/in-game approval remains separate.

## Final preview synchronized with authoritative NBT

**YES.**

Gate D proves exact decompressed-NBT equality and renders the shipping NBT.

## Peak-quality rubric

### Functional architecture — 19/20

The facility now has coherent public, clean, dirty-return, receiving, records and mechanical programs. One point is retained because the compact scale necessarily abstracts staff-support functions found in a full real facility.

### Massing and exterior quality — 14/15

The stepped facility, public threshold, service edges, rear dock and roof plant produce a credible neighborhood-service silhouette. It intentionally remains compact rather than becoming a landmark.

### Interior architecture — 14/15

Rooms have clear functions and workflows with protected operational circulation. The small footprint constrains the breadth of secondary staff/support rooms.

### Corporate identity — 9/10

VCF is readable through clean biological cold-chain architecture, return/reuse workflow and service language as well as signage/color.

### Operational realism — 10/10

Material flows are explicit in both directions and the rooftop/service infrastructure explains the cold chain.

### Environmental storytelling — 9/10

The anomaly and later decay are physically legible without requiring text while remaining restrained enough for this early-story site.

### Exploration and encounter design — 8/10

Navigation has distinct operational routes and optional tension pockets, but the site deliberately does not use a complex deterministic encounter sequence because it is a common narrative-discovery location.

### Loot and quest integration — 5/5

Existing loot architecture is preserved and proof acquisition is deterministic, plausible and reachable.

### Damage and historical layering — 5/5

D0/D1/D3 progression is causal, measured and visually preserved through the fixed-camera review set.

## Quality score

**93 / 100 — PASSED**

Approval threshold: 90/100.

No major category is absent, all mandatory visual gates are complete, and Gate D is synchronized with the authoritative shipping schematic.

## Remaining limitations

- Runtime/fresh-world placement is not approved by this report.
- Terrain integration and structure-detection behavior remain part of the separate runtime program.
- Primitive review rendering cannot prove final in-game texture, shader, lighting or mod-model presentation.
- OWS-001 remains intentionally a common neighborhood site rather than a combat-heavy landmark.

## Final quality decision

**OWS-001 HEAVY SCHEMATIC REBUILD: PEAK-QUALITY STATIC APPROVED.**

The synchronization issue is resolved. The structure that passed the final review is the structure that ships from the authoritative generator.
