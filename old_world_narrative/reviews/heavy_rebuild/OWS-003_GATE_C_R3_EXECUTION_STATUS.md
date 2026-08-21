# [SYSTEM REPORT] OWS-003 Gate C r3 — Execution Boundary

**Target:** OWS-003 — Verdant Continuum Foods Cold-Chain Culture Nursery  
**Procedure authority:** `docs/HEAVY_REBUILD_DOCTRINE.md`  
**Status:** R3 SOURCE AUTHORED — FIXED-CAMERA RENDER NOT YET PERSISTED — GATE C CLOSED

## Accepted state before r3

- Gate A: **PASSED r1**.
- Gate B intact state: **PASSED r7**.
- Gate C r2: **REVISION REQUIRED — D3 ONLY**.
- D0 from Gate B r7: accepted as Gate-C input.
- D1 early seal/gasket anomaly: accepted as Gate-C input.
- D3 r2: rejected because the building remained visually too pristine from several exterior cameras after centuries of abandonment.

## r3 source

The D3-only correction is implemented in:

`scripts/render_ows003_gate_c_damage_states_r3.py`

Source commit:

`fa795a74f311121a02734bfb1016e772ddbccfd3`

The r3 source preserves D0 and D1 and strengthens only the centuries-later state through causal damage at:

- east receiving upper service facade;
- south dispatch canopy / upper logistics edge;
- refrigeration service deck and pipe/service edge;
- additional roof-light/service penetration patches;
- corresponding wet brick/service zones below roof failures;
- a small rear service-wall breach.

The source re-runs the protected route, identity, proof, encounter-count, cooler-survival and pipe-survival assertions after the stronger decay layer. It raises the D3 change-density floor to 550 changed positions while requiring the already-accepted D1 to remain exactly 19 changed positions.

## Execution attempts

The revision-aware Gate-C workflow is:

`.github/workflows/old-world-ows003-gate-c.yml`

The workflow already chooses the numerically highest `render_ows003_gate_c_damage_states_r*.py` renderer, so r3 is the intended active revision.

Additional trigger attempts were made without modifying structure geometry or approval state:

- `93d4b0eb628a7d09dc502df2006c9a5c3b387e0a` — explicit r3 workflow watch / retrigger;
- `a4eb6cdd95522e84fdc1a8502a34d691ad14bdee` — empty ref-push trigger attempt;
- `4c0196b851b62b0ab7d397ae9173a5089cca229c` — normal Git-data ref push with a workflow-path-only trigger marker.

At the time this status was written, no new `gate_c_workflow_run.json` for r3 and no persisted `gate_c_damage_states/r3/` fixed-camera artifact had appeared. The latest persisted Gate-C provenance remained the earlier r2 run.

## Mandatory boundary

**DO NOT mark Gate C passed from source inspection, block counts, or expected behavior.**

The next valid step is:

1. execute the Gate-C workflow against current `main`;
2. require the r3 mechanical assertions to pass;
3. persist/download the exact `gate_c_damage_states/r3/` artifact;
4. inspect D0/D1/D3 fixed-camera exterior views, roof/top view, interior cutaway and floor slices;
5. write an explicit r3 visual review decision;
6. only if that decision is PASSED may Pass 19 microdetail begin.

Until those steps occur:

- `micro_detail` remains pending;
- Gate D remains blocked;
- authoritative OWS-003 shipping synchronization must not begin;
- OWS-003 must not enter `completed` / `static_review_passed`;
- OWS-004 must remain untouched;
- the reserved OWS-003 Darknet return hook remains reserved and inactive.
