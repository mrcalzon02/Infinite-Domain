# OWS-005 Pass 19 — Localized Microdetail

**Target:** OWS-005 — Verdant Continuum Foods Harvest & Packaging Annex  
**Authority:** accepted Gate-C r1 D3, SHA-256 `b5abd645c32f43ce8c40315f9801d41aa0f33361bfd8c8dd9bd7b6826a58ca2f`  
**Status:** implemented in target-local production builder; coordinator integration required

Using the project review runtime, the pure target-local geometry module reproduces accepted Gate-A, Gate-B and Gate-C D0/D1/D3 bytes exactly. Production then applies normal `base.stabilize_door_pairs`, restoring door halves at `(20,3,6)` and `(27,2,38)`. The stabilized Pass-19 builder is byte-identical to shipping at SHA-256 `3f11c4d6af6b09507e6a05c018d57d408b1ce71244914e619160ff3916ad1208`.

Pass 19 adds eight non-functional weathering details, all inside already accepted D3 damage zones:

- wet-line-02 breach: cobweb `(27,3,37)`;
- reject-exit water path: brown mushroom `(25,2,43)`;
- rear-monitor / packing-line-02 breach: cobweb `(45,4,36)` and brown mushroom `(46,2,37)`;
- refrigeration-B / cold-hold-B breach: cobweb `(54,6,25)` and brown mushroom `(53,5,23)`;
- receiving-bay-02 canopy-loss field: cobweb `(6,3,36)` and brown mushroom `(7,2,38)`.

The overlay does not broaden the accepted damage footprint, alter structure massing, obscure the D1 intervention, move the proof container, add loot or encounters, or occupy protected circulation. The accepted three-spawner topology and the single deep QA proof node remain unchanged.

## Serialized coordinator integration request

In `scripts/generate_old_world_narrative_structures.py`:

1. add `import old_world_ows005_final as ows005_final` beside the other implementation-component imports;
2. change the existing dispatch row from `"OWS-005": build_005,` to `"OWS-005": ows005_final.build_005,`.

The legacy local `build_005` may remain temporarily unreachable or be removed in the same serialized coordinator edit. After dispatch integration, the coordinator must run authoritative generation, prove shipping-NBT byte equivalence to the target-local final builder, and request an independent shipping-NBT Gate-D render/review. This record does not claim Gate D.
