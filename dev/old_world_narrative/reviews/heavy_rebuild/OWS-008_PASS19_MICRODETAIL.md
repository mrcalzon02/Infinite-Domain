# OWS-008 Pass 19 — Localized Microdetail and Production Handoff

**Target:** OWS-008 — Emergency Investigation & Persistence Lab  
**Authority:** accepted Gate-C r1 D3, SHA-256 `6de9ee39cde02c1ea298a7352c9b4eb6502a21ff6696b6c972795769efc33f36`  
**Status:** implemented in target-local pure production builder; coordinator integration required

## Pure production geometry

`scripts/old_world_ows008_final.py` imports only `generate_wasteland_sites`, the common structure-construction library. It performs no rendering, serialization, filesystem access, registry/state mutation, shipping write or gate decision.

`build_accepted_d3()` reproduces the accepted Gate-C r1 D3 bytes exactly. `build_008()` adds only the Pass-19 overlay and returns the final template without I/O.

## Restrained overlay

Exactly eight previously-air cells are changed, all inside accepted D3 recurrence or moisture zones:

- Cell-D failed inspection edge: cobweb `(7,3,38)` and brown mushroom `(9,2,38)`;
- west/central rear joint seam: red mushroom `(18,2,42)`, cobweb `(28,3,41)` and brown mushroom `(36,2,42)`;
- dirty east seam/wash edge: red mushroom `(48,2,40)`, cobweb `(49,3,36)` and brown mushroom `(50,2,40)`.

The overlay does not broaden the accepted damage footprint, replace D1 collars, alter massing, change roof/canopy failures, touch a controlled door or protected route, move the proof chest, add loot, or change the accepted three-spawner topology.

## Hashes and deltas

- accepted D3 reproduction: `6de9ee39cde02c1ea298a7352c9b4eb6502a21ff6696b6c972795769efc33f36`;
- raw D3 + Pass-19 builder: `adc773b17c1269d671c74a9043875c0e76bb9ad25437d9deb109fb45bfc62357`;
- canonical production-stabilized builder: `3dcf761116820064dee5a2071254f2b2255a7faa1c2312f7b74057320980c7ff`;
- production-builder source SHA-256: `ef28d081c8d0b929d227335087fc7f7a8c49e32e2f9e054ac806097ba4cbc27c`;
- Pass-19 named-block delta from accepted D3: exactly 8 additions and no replacements/removals.

Normal `base.stabilize_door_pairs` changes zero cells. Raw and stabilized outputs both retain 59 working doors and zero orphan halves.

## Mechanical contracts

Target-local checks confirm:

- exact 55 x 22 x 49 bounds with no out-of-envelope positions;
- exactly one canonical proof chest at `(12,14,29)`, correct loot table, clear north approach and clear headroom;
- exactly three bounded spawners at the accepted dirty-exam, Cell-D and rear-joint positions;
- all accepted principal door families and threshold boundaries remain complete;
- at least 480 service pipes, 140 fluid tanks, 36 stair blocks and 24 institutional signs remain;
- all declared required blocks remain present: lime concrete, yellow concrete, framed glass, fluid pipe, mycelium and brown mushroom;
- final counts include 617 fluid pipes, 84 mycelium blocks, 17 brown mushrooms and 878 framed-glass blocks;
- standard structural metrics remain 59 working doors, zero orphan halves, 878 windows, 694 functional fixtures, 13-block vertical-access span, 17 dense floor levels and 20 footprint variants.

## Serialized coordinator mutations requested

The coordinator must serialize the shared authoritative handoff in `scripts/generate_old_world_narrative_structures.py`:

1. add `import old_world_ows008_final as ows008_final` beside the other target-local final-builder imports;
2. change the `core.BUILDERS.update` entry from `"OWS-008": build_008,` to `"OWS-008": ows008_final.build_008,`.

The legacy local `build_008` may remain unreachable. No second dispatch table, wrapper builder or alternate source of truth is requested.

The coordinator should then serialize heavy-rebuild state as:

- `active_status`: `pass19_complete_shipping_sync_ready`;
- `active_target_passes.micro_detail`: `complete`;
- `planning_records.pass_19_micro_detail`: `old_world_narrative/reviews/heavy_rebuild/OWS-008_PASS19_MICRODETAIL.md`;
- Gate D remains `pending` and must not claim authoritative-byte equality until generation and shipping verification complete.

## Authoritative generation steps

1. Re-read live `main` and apply the import/dispatch mutation above as the coordinator's serialized shared write.
2. Run `scripts/generate_old_world_narrative_structures.py`; allow its normal `base.stabilize_door_pairs` call and authoritative shipping/registry writes.
3. Build `ows008_final.build_008()`, apply `base.stabilize_door_pairs`, serialize a target-local comparison NBT, and prove decompressed byte equivalence with `kubejs/data/infinite_domain/structure/wasteland/old_world/ows_008_vcf_emergency_persistence_investigation_lab.nbt`.
4. Confirm the expected canonical production SHA-256 `3dcf761116820064dee5a2071254f2b2255a7faa1c2312f7b74057320980c7ff`, exact proof/spawner/bounds/route contracts, all six required blocks and structural lint. The earlier `adc773...` value is the same decompressed model serialized by the review runtime, not the canonical production gzip stream.
5. Run `scripts/validate_old_world_narrative.py` and any target-relevant structure lint after shared integration.
6. Render Gate D from the authoritative shipping NBT with `ows008_fixed_v1`, persist exact provenance, and request independent visual review.
7. Only after Gate D passes may static validation and quality promotion continue.

This record does not claim Gate D, shipping synchronization, static approval or runtime approval.
