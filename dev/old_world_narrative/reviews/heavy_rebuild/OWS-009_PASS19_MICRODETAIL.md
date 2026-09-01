# OWS-009 Pass 19 — Localized Microdetail and Production Handoff

**Target:** OWS-009 — Atlas Roadside Automated Repair Depot  
**Authority:** accepted Gate-C r1 D3, SHA-256 `42835cb4b926a8445b66016fa5d21f5219ec38386bc4dc2b941585ab5924b578`  
**Status:** implemented in target-local pure production builder; coordinator integration required

## Pure production geometry

`scripts/old_world_ows009_final.py` imports only `generate_wasteland_sites`, the common structure-construction library. It performs no rendering, serialization, filesystem access, registry/state mutation, shipping write or gate decision.

`build_accepted_d3()` reproduces the accepted Gate-C r1 D3 serialization exactly. `build_009()` adds only the Pass-19 overlay and returns the final template without I/O.

## Restrained overlay

Exactly nine previously-air cells are changed, all inside accepted Bay-03/east/rear service or degradation zones:

- required machine-support casing at `(34,2,28)`, grounded on the accepted Bay-03 rear service floor and connected laterally to the existing service-wall edge;
- rear Bay-03 service/drain edge: cobwebs at `(32,3,33)` and `(34,3,26)`;
- core-buffer edge: cobweb `(41,3,33)`, red mushrooms `(37,1,37)` and `(44,1,36)`, and brown mushrooms `(40,1,38)` and `(41,1,37)`;
- east cracked service strip: brown mushroom `(46,1,28)`.

The casing is the only newly added modded block and exists solely because `create:andesite_casing` is an explicit serialized required-block contract. All discretionary details remain vanilla. The overlay does not broaden the accepted damage footprint, change D1 plates/collars/bypass/backlog, alter a roof or canopy failure, replace landed debris, touch primary structure, occupy a protected route, move proof, add loot or change the three-spawner topology.

## Hashes and deltas

- accepted D3 reproduction: `42835cb4b926a8445b66016fa5d21f5219ec38386bc4dc2b941585ab5924b578`;
- D3 plus Pass-19 raw builder: `a46a99092cd930690403017c71909c426ead5e5e1baf39510734a62566c10880`;
- canonical stabilized builder: `a46a99092cd930690403017c71909c426ead5e5e1baf39510734a62566c10880`;
- production-builder source SHA-256: `d3623e13582c26d4797f44049e5ce99a48b0df4a699fde776ac5ec67022c02b0`;
- Pass-19 named-block delta: exactly nine additions, zero replacements and zero removals;
- normal `base.stabilize_door_pairs` delta: zero positions.

## Mechanical and source contracts

`scripts/validate_ows009_final_builder.py` confirms:

- the production source imports neither `render_*` nor any review module and has no unexpected import beyond `__future__` and `generate_wasteland_sites`;
- exact 49 x 18 x 41 bounds with no out-of-envelope positions;
- exactly one canonical proof chest at `(37,2,29)`, correct loot table, clear headroom and clear east approach;
- exactly three bounded spawners at the accepted Bay-01 edge, Bay-02 edge and core/rework positions;
- all accepted controlled door families and protected vehicle/customer/parts/technician/records routes remain complete;
- the final model contains exactly one serialized `create:andesite_casing`; accepted D3 contains zero, proving it is isolated to the Pass-19 overlay;
- the casing has non-air support below and a non-air lateral connection, while remaining outside every protected route;
- all declared required blocks remain present: andesite casing, steel frame, framed glass, service pipe, copper drain grate, moss and weathered copper;
- final counts include one andesite casing, 1,961 steel blocks, 387 framed-glass blocks, 246 service pipes, 169 drain grates, 27 moss blocks and 35 weathered-cut-copper blocks;
- structural metrics remain 19 working doors, zero orphan halves, 387 windows, 263 functional fixtures, 15 dense floor levels and 17 footprint variants.

## Shared integration status

The coordinator has already serialized the authoritative import and dispatch: live `scripts/generate_old_world_narrative_structures.py` imports `old_world_ows009_final as ows009_final` at line 24 and maps `"OWS-009"` to `ows009_final.build_009` at line 582. No further shared source mutation is requested from this worker.

The pre-correction authoritative generation failed validation because the pure builder did not serialize the inherited required block `create:andesite_casing`. The target-local builder now supplies exactly one such block. Shared shipping, generated structure records and state must be refreshed only by the coordinator.

## Authoritative generation steps

1. Re-read live `main` and confirm the existing OWS-009 import/dispatch still targets `old_world_ows009_final.build_009`.
2. Run `scripts/generate_old_world_narrative_structures.py`, allowing its normal `base.stabilize_door_pairs` and authoritative shipping/registry writes.
3. Build `old_world_ows009_final.build_009()`, apply `base.stabilize_door_pairs`, serialize a target-local comparison and prove decompressed serialization equivalence with `kubejs/data/infinite_domain/structure/wasteland/old_world/ows_009_atlas_roadside_repair_depot.nbt`.
4. Confirm expected SHA-256 `a46a99092cd930690403017c71909c426ead5e5e1baf39510734a62566c10880`, dimensions, proof, three spawners, all protected routes, seven required-block families—including exactly one `create:andesite_casing`—and clean structural lint.
5. Confirm unrelated generated outputs remain unchanged except the expected OWS-009 shipping/structure-record refresh and normal generated metadata touched by the coordinator run.
6. Run `scripts/validate_old_world_narrative.py`; the prior `OWS-009 lacks required serialized block create:andesite_casing` failure must be absent. Run target-relevant corpus/structure lint as well.
7. Update shared heavy-rebuild state only after generation/equivalence checks succeed; Gate D remains pending.
8. Render Gate D from the actual authoritative shipping NBT with `ows009_fixed_v1`, persist builder/shipping equivalence and visual-regression evidence, then request independent review.
9. Only after Gate D passes may static validation and quality promotion continue.

This record does not claim Gate D, shipping synchronization, static approval or runtime approval.
