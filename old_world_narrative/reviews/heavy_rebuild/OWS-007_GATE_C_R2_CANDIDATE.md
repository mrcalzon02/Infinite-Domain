# [SYSTEM REPORT] OWS-007 Gate C r2 — Narrow Revision Candidate

**Target:** OWS-007 — Verdant Continuum Foods EP-7 Agricultural Development Laboratory  
**Gate:** Visual Gate C — historical and damage-state comparison  
**Revision basis:** independent Gate-C r1 decision `REVISION REQUIRED`  
**Decision owner:** independent `ows-visual-reviewer`  
**Candidate status:** **REVIEW NEEDED**

## Exact persisted artifact

- gate manifest: `old_world_narrative/reviews/heavy_rebuild/visual/OWS-007/gate_c_damage_states/r2/gate_c_manifest.json`;
- comparison sheet: `old_world_narrative/reviews/heavy_rebuild/visual/OWS-007/gate_c_damage_states/r2/damage_comparison.png`;
- fixed camera set: `ows007_fixed_v1`;
- common D0/D1/D3 cutaway plane: Y <= 8;
- review builder SHA-256: `58db253cde1d7a91bb33156ed4308dd2bd8cabb93f347744ac8cd25d3b8847dc`;
- D0 SHA-256: `b116ad94acd595414ca670d4f5205bed69e4116724167a6397a8504acb0ba67a`;
- D1 SHA-256: `7bb865d6d06682dca0b986234c639cc859c7c15be47cd342215b21f3e2ef952f`;
- rejected r1 D3 SHA-256: `6d6e1743219299d34e23a3f385f597bff1b26c679490c8b43d31f4f82911cef4`;
- r2 D3 SHA-256: `d7c3b597af7e5c63a26ceb43f2e6a2e75865e60f2a197e1c0679b52d67c19283`;
- frozen shipping Git blob before and after rendering: `13c045293c5d40a939ee79bec6c894fd807b0970`.

## Exact r2 geometry scope

The r1 D3 model contained one completely detached `minecraft:white_concrete` fragment at local `(70, 22, 35)` beside the rotunda upper rear crown. A six-face connectivity audit confirmed that it formed a one-block component disconnected from the campus.

R2 changes exactly that one D3 position:

`(70, 22, 35): minecraft:white_concrete -> minecraft:air`

The fragment is removed rather than left floating. No support, route, room, debris field, facade, rotunda rib, crown mass, bridge, encounter, proof or other D3 position changes.

## Frozen aspects

- D0 is exactly identical to the accepted Gate-B r2 model and Gate-C r1 D0;
- D1 is exactly identical to Gate-C r1 commercial repeat validation;
- campus massing, VCF identity, chamber family, hinge, bridge and rotunda remain frozen except for the isolated fragment removal;
- routes, proof setting, encounter contract and every other localized D3 damage path remain frozen;
- proof remains the one canonical chest at `(43, 2, 56)`;
- the four non-explosive vanilla spawners remain unchanged.

## Common-cutaway correction

All three r2 state manifests record `cutaway_y: 8`, and every `interior_cutaway.png` is regenerated from blocks at Y <= 8. The r2 comparison sheet therefore presents D0, D1 and D3 at one directly comparable interior plane without changing any state geometry.

## Assertions

- persisted r1 D0/D1/D3 hashes must match expected provenance before r2 builds;
- D0 and D1 serialized hashes must remain exact r1 matches;
- D3 r1-to-r2 diff must be exactly `{(70,22,35)}`;
- the removed position must resolve to air in r2;
- proof, encounter, identity, service, crop and access contracts rerun on r2 D3;
- all three rendered manifests must record common cutaway Y <= 8;
- temporary review NBT is removed;
- shipping NBT remains unchanged.

No Gate-C approval is recorded here. Pass 19 and shipping synchronization remain blocked pending independent review of this exact r2 artifact.
