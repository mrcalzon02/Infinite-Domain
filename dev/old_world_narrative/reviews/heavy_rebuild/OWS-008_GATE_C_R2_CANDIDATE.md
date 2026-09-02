# [SYSTEM REPORT] OWS-008 Gate C r2 — Damage-State Candidate Ready

**Target:** OWS-008 — Emergency Investigation & Persistence Lab  
**Procedure authority:** `docs/HEAVY_REBUILD_DOCTRINE.md` at recorded procedure revision `2b6fa9637771f059b65a4bd095c876036ff2f7cd`  
**Planned artifact:** `dev/old_world_narrative/reviews/heavy_rebuild/visual/OWS-008/gate_c_damage_states/r2/gate_c_manifest.json`  
**Renderer:** `dev/scripts/render_ows008_gate_c_damage_states.py`  
**Fixed camera set:** `ows008_fixed_v1`  
**Status:** **READY TO RENDER / INDEPENDENT GATE-C REVIEW REQUIRED**

## Authorization evidence

Gate-B r2 is no longer a blocker. The authoritative review record at
`dev/old_world_narrative/reviews/heavy_rebuild/OWS-008_GATE_B_R2_REVIEW.md`
records **OWS-008 GATE B R2: PASSED** for review-model SHA-256
`52a259170466c30e9d015b56b79a175962cabde352654f0f302e153a40201b86`.

Passes 13–18 are present and individually marked complete for Gate-C implementation:

- Pass 13 — historical layering;
- Pass 14 — environmental narrative;
- Pass 15 — encounter architecture;
- Pass 16 — loot architecture;
- Pass 17 — quest-proof architecture;
- Pass 18 — damage and decay.

The Gate-C renderer is already implemented as a review-only D0/D1/D3 chain. It
refuses to write shared state or authoritative shipping NBT and carries explicit
contracts for the accepted Gate-B source, the canonical proof table/item, the
secure archive proof position, and the three bounded D3 encounter sources.

## State chain to review

- **D0:** exact repaired Gate-B r2 intact operating model; no proof loot,
  encounters, abandonment damage or recurrence dressing.
- **D1:** competent professional escalation: cell-aligned inspection collars,
  concealed-joint comparison stations, continuous filter watch and the overhead
  diagnostic bypass. No proof node, spawners or abandonment damage.
- **D3:** long-abandoned recurrence following the investigated penetration/drain
  path; localized rear/east roof corrosion and water ingress; debris below the
  failed bay; restrained fungal/moisture occupation; one canonical archive proof
  node; three bounded encounter sources.

D2 remains intentionally omitted because there is no separate blast, acute
collapse, or materially distinct causal phase between investigation escalation
and long abandonment.

## Frozen preservation contract

The Gate-C candidate must retain:

1. the accepted 55 x 22 x 49 envelope and Gate-B massing hierarchy;
2. public, staff, treatment-cell and rear-service circulation;
3. all pressure thresholds and the repaired west command/archive stair;
4. the upper secure-proof approach;
5. recognizable Cells A–D, treatment machinery and rear service anatomy;
6. VCF identity beneath emergency containment markings;
7. physically causal damage with supported remaining structure and landed debris;
8. exactly one canonical proof node in D3 and zero in D0/D1;
9. exactly three bounded D3 encounter sources and zero in D0/D1;
10. no mutation of authoritative shipping NBT during visual review.

## Required execution and decision

Run `dev/scripts/render_ows008_gate_c_damage_states.py` in the repository runtime,
persist the fixed-camera D0/D1/D3 artifact bundle, inspect the actual contact
sheet and individual views, then write an explicit independent review decision.
Static contracts may reject an invalid candidate, but they must not auto-approve
Gate C.

A passed Gate C still does **not** establish runtime placement, Lost Cities
coexistence, terrain seating, door/collision behavior, shipping-NBT equivalence,
or production admission. Those remain later verified gates.

**OWS-008 GATE C r2: READY TO RENDER / REVIEW NEEDED.**
