# [SYSTEM REPORT] OWS-010 Gate C r1 — Damage-State Candidate

**Target:** OWS-010 — Atlas Conveyor Transfer Hall  
**Procedure:** `docs/HEAVY_REBUILD_DOCTRINE.md`  
**Input authority:** independently passed Gate-B r1  
**Gate manifest:** `old_world_narrative/reviews/heavy_rebuild/visual/OWS-010/gate_c_damage_states/r1/gate_c_manifest.json`  
**Comparison:** `old_world_narrative/reviews/heavy_rebuild/visual/OWS-010/gate_c_damage_states/r1/damage_comparison.png`  
**Fixed camera set:** `ows010_fixed_v1`  
**Dimensions:** 49 x 16 x 43  
**Builder SHA-256:** `f03808145903a4dfe96ed5f1996668d1b25c5e0b3eb0b09284192e585e5973fb`  
**Status:** **REVIEW NEEDED — no worker visual decision**

## State provenance

| State | Review-model SHA-256 | Delta from D0 | Meaning |
|---|---|---:|---|
| D0 | `ef8c4ea3281f70270c0507f78610ffc44cd100c02fb1b4f387055a15b51e2603` | 0 | Exact accepted Gate-B r1 intact hall |
| D1 | `6fd40660424bb51506edeb3b59fb8db1cb73428548ca356d4e39b175bf58dd7e` | 145 | Lane-04 cannibalization and maintenance shortage |
| D3 | `29b9efa13b9ae71cf210aa3630cba224c31d4410d3aea5a4a97d772aa8ef5fc8` | 283 | Localized Lane-04/service decay and current ruin |

D2 is omitted because no materially distinct acute event separates the gradual operating cannibalization from shutdown and long abandonment. A fourth state would only interpolate the same unresolved monitor/service leakage.

Each state contains four exterior quarters, roof/top view, identical Y<=10 interior cutaway, floor slices, contact sheet and manifest. The comparison uses the same four diagnostic views for all states.

## Historical and environmental case

- D1 locks out Lane 04 while retaining its bed, endpoints, number and structural bay.
- Four replaceable roller/depot modules and two drive clusters are removed; matching modules are staged at east parts issue and added at the service faces of Lanes 01–03.
- A temporary overhead service bypass prioritizes the three maintained lines.
- Shortage, stock and work-order signs connect the intervention to real equipment and rooms.
- D3 opens only the patched Lane-04 monitor and connected east clerestory/service edge.
- Primary rails and supported weathered edges survive; fragments land on the isolated lane or exterior strip below.
- Moisture, moss, corrosion, cobwebs and vegetation follow Lane 04, the east drain and drive trench rather than spreading randomly.
- Dock hierarchy, three maintained lines, trunk, return, gallery, catwalk, control/records, utilities and Atlas identity remain readable.

## Gameplay, loot, proof and LOR

- exactly one canonical proof chest at `(9,11,17)` uses `infinite_domain:chests/old_world/ows_010_atlas_conveyor_transfer_hall`;
- the live table is asserted to contain exactly one guaranteed `kubejs:atlas_transfer_maintenance_card`;
- the live table contains zero `kubejs:atlas_transfer_maintenance_manual` entries;
- both empty accepted LOR shelves survive at `(9,10,16)` and `(10,10,16)`;
- proof headroom and east interaction face remain clear;
- three bounded D3 encounters occupy the inbound-buffer edge, isolated Lane-04 service edge and damp east parts edge;
- D0 and D1 contain no proof chest or spawners;
- no shared loot, quest, item or registry contract changed.

## Freeze and mechanical evidence

- D0 is serialized byte-identical to accepted Gate-B r1 before and after rendering;
- Lanes 01–03 remain exact at every transfer module in D1/D3;
- Lane 04 retains thirteen declared modules plus bed, input and output anatomy;
- both inbound tongues, destination trunk, east return and both outbound buffers remain continuous in all states;
- gallery, catwalk, maintenance routes, both controlled external doors and 28 stair blocks survive;
- exact empty LOR shelves and absence of the manual item are asserted in every state;
- final D3 asserts one proof table/node, three vanilla spawners and minimum separation from proof;
- primary steel, connected utilities and Atlas wayfinding remain above frozen coverage thresholds;
- shipping remains unchanged at SHA-256 `5e9390d3d41663f1baef6ad017e941dbf6153d168bb9100a8a5fd46193d9035a` and Git blob `be2ab341c2d252c975711caa93e92c965f943007`;
- all temporary review NBT files are removed.

## Independent reviewer obligations

Inspect the labeled comparison, all three contact sheets, principal fixed-camera views and floor slices. Decide whether:

1. D0 exactly and visibly preserves the accepted four-lane architecture, routes, utilities and Atlas identity;
2. D1 clearly reads as Lane-04 cannibalization sustaining Lanes 01–03 rather than arbitrary prop change;
3. removed modules, staged spares, replacement drives and temporary bypass form one causal maintenance-shortage story;
4. D3 damage grows from the starved Lane-04 monitor/east service edge and remains gravity-consistent;
5. the three maintained lines, material chain, circulation and institutional identity survive strongly enough;
6. three encounters remain bounded and the single records proof node is recoverable;
7. both LOR shelves remain visibly spatial-only without manual duplication;
8. D2 omission is appropriate;
9. no over-ruin, floating debris, blocked route, unsupported panel or major narrative inconsistency requires revision.

Pass 19 and authoritative synchronization remain blocked pending an independent `PASSED` decision for this exact artifact.

**OWS-010 GATE C r1: REVIEW NEEDED.**
