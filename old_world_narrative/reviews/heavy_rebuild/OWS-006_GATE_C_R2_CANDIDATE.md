# [SYSTEM REPORT] OWS-006 Gate C r2 — Independent Review Candidate

**Target:** OWS-006 — Verdant Continuum Foods PT-9 Symbiosis Pilot Laboratory  
**Gate:** Visual Gate C — narrow D3 revision  
**Artifact manifest:** `old_world_narrative/reviews/heavy_rebuild/visual/OWS-006/gate_c_damage_states/r2/gate_c_manifest.json`  
**Comparison artifact:** `old_world_narrative/reviews/heavy_rebuild/visual/OWS-006/gate_c_damage_states/r2/damage_comparison.png`  
**Revised D3 contact sheet:** `old_world_narrative/reviews/heavy_rebuild/visual/OWS-006/gate_c_damage_states/r2/d3/contact_sheet.png`  
**Fixed camera set:** `ows006_fixed_v1`  
**Review-stage source:** `scripts/render_ows006_gate_c_damage_states.py`  
**Author status:** **REVIEW NEEDED — independent visual decision required**

## Frozen provenance

- **D0 SHA-256:** `fb1a6c530a3731794547c429e56ab47d93e7082b1157ca255f2790b900a5749e` — exact accepted Gate-B model, unchanged from r1.
- **D1 SHA-256:** `387221cfeaebaf0da5376bda89a05f4d39e896924b99b37da016e2166aa2ad6e` — exact accepted r1 early-anomaly state, unchanged.
- **Rejected r1 D3 SHA-256:** `f94137e898b545aa024804d1bc8a8571cf1c044eafb7e2a26250f3184756df4a`.
- **Candidate r2 D3 SHA-256:** `8c9d3e31c0d3cdfcee0a45bdc7bf5156184a05521babdd8665f47e6d6e5f6e09`.
- **r1-to-r2 D3 delta:** exactly 17 positions.

The r2 comparison reuses the persisted r1 D0 and D1 artifacts and combines them with a complete newly rendered r2 D3 fixed-camera set.

## Narrow correction

The only D3 revision is at the independently identified rear environmental-plant defect:

- removed the detached 4 x 3 light-gray service cap at local X29–32, Y25, Z43–45;
- placed five matching light-gray debris blocks on the surviving service deck directly below at Y17–18;
- did not widen the damaged footprint or alter any other r1-D3 position.

The renderer reconstructs the rejected r1 D3 byte-for-byte, asserts its prior hash, and then asserts the exact 17-position allowlist before rendering r2.

## Frozen accepted aspects

All ten aspects frozen by the independent r1 review remain unchanged, including exact D0, localized D1, the east material-hold/Chamber-B/manifold causal path, A/C intact controls, circulation, proof, encounter topology, VCF identity, restrained damage and the justified D2 omission.

## Independent review questions

The reviewer must determine from the complete r2 D3 set and same-camera comparison whether:

1. the unsupported floating rear service cap is gone;
2. the five-block debris scatter reads as restrained, gravity-consistent material on the surviving deck;
3. no damage has broadened beyond the reviewed rear-plant correction;
4. all ten r1-frozen aspects remain visually intact.

No Gate C decision is recorded here. Pass 19 and Gate D remain blocked pending independent review of this exact r2 candidate.
