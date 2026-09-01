# OWS-006 Pass 19 — Localized Microdetail

**Target:** OWS-006 — Verdant Continuum Foods PT-9 Symbiosis Pilot Laboratory  
**Authority:** independently accepted Gate-C r2 D3, SHA-256 `8c9d3e31c0d3cdfcee0a45bdc7bf5156184a05521babdd8665f47e6d6e5f6e09`  
**Status:** implemented in target-local production builder; coordinator integration required

The side-effect-free production builder `scripts/old_world_ows006_final.py` reconstructs the accepted r2 D3 model byte-for-byte without importing any render or review module. The Pass-19 final candidate serializes to SHA-256 `1ed922f2de4ea0e90d0edd90fab922986f9d0a266ec3c5db94f04f834a97b0a4`.

Pass 19 adds exactly eight non-functional weathering details, all within already accepted D3 damage zones:

- east material-hold breach: cobwebs `(52,4,34)` and `(53,4,36)`;
- Chamber-B service edge: cobweb `(36,4,37)` and brown mushroom `(35,2,34)`;
- failed rear-manifold deck: cobwebs `(29,18,43)` and `(32,17,45)`;
- accepted rear water path: brown mushrooms `(49,2,45)` and `(51,2,46)`.

The overlay does not broaden the accepted damage footprint, change massing or structural support, alter D0/D1 history, obstruct any protected route, move the proof node, add loot, or change the three-spawner encounter topology. All eight Gate-C r2 accepted aspects remain frozen.

## Serialized coordinator integration request

Apply this exact shared mutation to `scripts/generate_old_world_narrative_structures.py`:

```diff
 import old_world_narrative_core as core
 import old_world_later_waves as later
 import old_world_ows005_final as ows005_final
+import old_world_ows006_final as ows006_final

 core.BUILDERS.update({
     "OWS-005": ows005_final.build_005,
+    "OWS-006": ows006_final.build_006,
     "OWS-007": build_007,
```

After serialized dispatch integration, the coordinator must run authoritative generation, prove stabilized production-builder/shipping-NBT byte equivalence, and request Gate D rendering from the actual shipping NBT. This record does not modify shipping or claim Gate D.
