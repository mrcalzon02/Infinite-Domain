# OWS-008 Gate D r2 — Repaired Authoritative Shipping Candidate

**Target:** OWS-008 — Emergency Investigation & Persistence Lab  
**Procedure authority:** `docs/HEAVY_REBUILD_DOCTRINE.md`  
**Planned artifact:** `old_world_narrative/reviews/heavy_rebuild/visual/OWS-008/gate_d_final/r2/review_manifest.json`  
**Planned contact sheet:** `old_world_narrative/reviews/heavy_rebuild/visual/OWS-008/gate_d_final/r2/contact_sheet.png`  
**Planned authoritative synchronization:** `old_world_narrative/reviews/heavy_rebuild/visual/OWS-008/gate_d_final/r2/authoritative_sync.json`  
**Renderer:** `scripts/render_ows008_gate_d_final.py`  
**Fixed camera set:** `ows008_fixed_v1`  
**Status:** **BLOCKED — Gate B r2 and Gate C r2 must pass first**

## Why r2 is required

Gate D r1 was independently visually passed, but later static validation proved
that the west command/archive stair was not executable. A z=21 partition replaced
two stair treads and their headroom, and later landing slabs occupied both flight
tops. Because the mandatory proof is in the upper archive, this is a progression-
blocking circulation defect and r1 final provenance cannot remain authoritative.

## Repaired authoritative source

The pure target-local builder now reapplies the accepted west dogleg stair only
after its conflicting partition and landing writes. The synchronized shipping NBT
has:

- serialized SHA-256 `62f7246e8d93d2a4bba9bba4224c4ca7131eccce63d9537b5ecab79a0e63b55a`;
- decompressed SHA-256 `6ce17cf96dd3e806f6e1854edc42ce297c7cb3f8d6b0ba72795929f388c05fd3`;
- `84,679` serialized bytes and `1,071,664` decompressed bytes;
- exact stabilized-builder/shipping equivalence;
- exactly eight named-block changes from r1 shipping, all stair tread/headroom
  cells recorded in `OWS-008_PASS8_CIRCULATION_R2.md`.

Target-local validation proves 20 exact treads, two-block headroom above each,
and a supported stepwise route from `(4,2,18)` to the canonical proof approach
at `(12,14,28)`. The proof chest remains exactly once at `(12,14,29)`.

## Frozen aspects to inspect

After Gate B r2 and Gate C r2 independently pass, the Gate-D r2 reviewer must inspect the exact persisted r2 artifact and
confirm that the repair preserves every accepted Gate-C/Gate-D visual aspect:

1. accepted Gate-B D0 architecture and stepped laboratory massing;
2. D1 collars, diagnostic bypass, watch modules and professional containment;
3. rear joint/drain and Cell-D recurrence path;
4. local rear/east failures and gravity-consistent landed debris;
5. public/clean preservation and dirty/service-side damage concentration;
6. Cells A-D, pressure boundaries, thresholds, inspection spine, stairs,
   command/archive, proof approach and service circulation;
7. one upper proof node and three bounded encounter areas;
8. restrained fungal/moisture footprint and Pass-19 microdetail.

The reviewer must also confirm that the reopened two-wide stair reads correctly
in the fixed cutaway and slices, and that the repaired openings create no clipping,
floating geometry, malformed landing, visual noise or architecture drift.

No worker visual decision is recorded. The Gate-D r2 renderer explicitly refuses
to run unless authoritative state and an independent review record both say
Gate C r2 passed. Static promotion and final quality approval remain blocked.

**OWS-008 GATE D r2: BLOCKED ON GATE B r2 AND GATE C r2.**
