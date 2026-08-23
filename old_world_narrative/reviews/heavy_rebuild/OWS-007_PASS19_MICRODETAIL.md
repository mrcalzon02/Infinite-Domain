# OWS-007 Pass 19 — Localized Microdetail and Production Handoff

**Target:** OWS-007 — Verdant Continuum Foods EP-7 Agricultural Development Laboratory  
**Authority:** accepted Gate-C r1 D3, SHA-256 `62b146b0cb46af49ceaf6fced34785b32c9c9278ae482a5af8ca54513928f54c`  
**Status:** implemented in target-local pure production builder; coordinator integration required

## Pure production geometry

`scripts/old_world_ows007_final.py` imports only the common structure-construction library and Python `math`. It performs no rendering, serialization, registry mutation or gate decision. `build_accepted_d3()` reproduces the accepted Gate-C r1 D3 bytes exactly. `build_007()` adds only the Pass-19 overlay and returns the final template without I/O.

## Restrained overlay

Exactly nine localized cells are changed, all inside accepted D3 damage zones:

- west environmental-plant leak: cobweb `(5,3,45)` and brown mushroom `(6,2,42)`;
- Chamber-B water path: cobweb `(18,3,42)` and brown mushroom `(18,2,43)`;
- wash/decon roof leak: cobweb `(31,3,55)` and brown mushroom `(34,2,54)`;
- rotunda humidity-sector leak: cobweb `(59,4,40)` and brown mushroom `(59,2,42)`.
- rotunda humidity-sector ground seam: one accepted mossy-stone-brick cell at `(61,1,42)` becomes `minecraft:mycelium`, satisfying OWS-007's declared serialized mycelial-test material contract without enlarging the wet zone.

The overlay does not broaden the damage footprint, alter massing, modify D1 evidence, touch the corrected mullion-and-beam facade, occupy a protected route, move the proof chest, add loot, or change the accepted three-spawner topology.

## Hashes and contracts

- accepted D3 reproduction: `62b146b0cb46af49ceaf6fced34785b32c9c9278ae482a5af8ca54513928f54c`;
- raw D3 + Pass-19 builder: `ab08bdccd9643a8927315bd0f313b9b7a9a47d734379410f5bc298241b82ab28`;
- normal production-stabilized builder: `3efa15b3836b327d1c98b916bcf3688305c86fde783df073abacaf61b7536dbd`.

Raw geometry retains the accepted Gate-C door topology: 44 working doors and one orphaned rear Chamber-B door half where the phenotyping depot overwrote `(23,2,45)`. Normal `base.stabilize_door_pairs` restores that cell from `create:depot` to `minecraft:iron_door`, yielding 45 working doors and zero orphan halves. No other named block changes during stabilization. This standard production correction must be included in authoritative generation and inspected at Gate D.

Mechanical contracts confirm 73 x 33 x 63 bounds, exactly one canonical proof chest at `(43,2,55)`, exactly three bounded spawners, preserved primary thresholds, preserved facade frames, at least 170 environmental pipes, at least 65 rich-soil cells, at least one serialized mycelium cell and at least 22 institutional signs. Target-local serialization now contains all five OWS-007 required blocks and passes structural lint with 45 working doors and zero orphan halves after normal stabilization.

## Serialized coordinator mutations requested

The coordinator has already staged the required import and dispatch route in the live working tree:

- `import old_world_ows007_final as ows007_final`;
- `"OWS-007": ows007_final.build_007,`.

No further shared source mutation is requested for this correction. The legacy local `build_007` may remain unreachable.

## Authoritative generation steps

1. Re-read live `main` and confirm the staged import/dispatch route still points to `ows007_final.build_007`.
2. Rerun `scripts/generate_old_world_narrative_structures.py`; allow the normal generator to stabilize door pairs and replace the stale missing-mycelium shipping output.
3. Build `ows007_final.build_007()`, apply `base.stabilize_door_pairs`, serialize a target-local comparison NBT, and prove decompressed byte equivalence with `kubejs/data/infinite_domain/structure/wasteland/old_world/ows_007_vcf_ep7_agricultural_development_laboratory.nbt`.
4. Confirm the stabilized authoritative target hash and all proof/spawner/bounds/route contracts, then run `scripts/validate_old_world_narrative.py` and relevant structural lint.
5. Render Gate D from the authoritative shipping NBT with `ows007_fixed_v1`, persist exact provenance, and request independent visual review.
6. Only after Gate D passes may the coordinator serialize static-quality promotion.

This record does not claim Gate D or shipping synchronization.
