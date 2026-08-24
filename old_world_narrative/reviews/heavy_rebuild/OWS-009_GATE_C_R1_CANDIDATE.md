# [SYSTEM REPORT] OWS-009 Gate C r1 — Damage-State Candidate

**Target:** OWS-009 — Atlas Roadside Automated Repair Depot  
**Procedure:** `docs/HEAVY_REBUILD_DOCTRINE.md`  
**Input authority:** independently passed Gate-B r1  
**Gate manifest:** `old_world_narrative/reviews/heavy_rebuild/visual/OWS-009/gate_c_damage_states/r1/gate_c_manifest.json`  
**Comparison:** `old_world_narrative/reviews/heavy_rebuild/visual/OWS-009/gate_c_damage_states/r1/damage_comparison.png`  
**Fixed camera set:** `ows009_fixed_v1`  
**Dimensions:** 49 x 18 x 41  
**Builder SHA-256:** `649f7bf8a4347463714b40a3a2fd6198caaf9a7fb9fa8de4812863c58d4fa39e`  
**Status:** **REVIEW NEEDED — no worker visual decision**

## State provenance

| State | Review-model SHA-256 | Delta from D0 | Meaning |
|---|---|---:|---|
| D0 | `c2c850549694cfa28e898fbe7019841e1c358b5534c1a53136f87f243d90c0a9` | 0 | Exact accepted Gate-B r1 intact depot |
| D1 | `07287dc213c5dff0b47ab80c5b24d415474e90c3601e192ea99359de66ce5faf` | 281 | Ordinary late-operation maintenance and calibration-recheck backlog |
| D3 | `42835cb4b926a8445b66016fa5d21f5219ec38386bc4dc2b941585ab5924b578` | 510 | Causal drain/flashing failure and restrained long abandonment |

D2 is omitted because no distinct acute event separates the operating maintenance backlog from long abandonment. A fourth state would only interpolate the same roof-drain and flashing failure.

Each state contains four exterior quarters, roof/top view, identical Y<=6 interior cutaway, floor slices, contact sheet and manifest. The comparison uses the same four diagnostic views for all states.

## Historical and damage case

- D1 retains a fully operating depot while adding cell-specific recheck datums, three removable drain/service collars, a temporary overhead diagnostic bypass, comparison pads, staged replacement parts and a removed-core backlog.
- Late-generation Bay-03 and parts-roof flashing remains intact but visibly patched in D1.
- D3 grows moisture, corrosion and vegetation only along the rear/east drain network, Bay-03 branch, parts edge and core return.
- Bay-03 monitor, parts-roof and core-canopy panels fail locally; their primary frames survive, weathered edges remain supported and fragments land below on calibration edges, parts stacks/service strip or the core yard.
- Bay 01 and the public frontage remain comparatively preserved because they are upstream and remote from the causal failure.

## Gameplay, loot and proof

- exactly one canonical proof chest at `(37,2,29)` uses `infinite_domain:chests/old_world/ows_009_atlas_roadside_repair_depot`;
- the live table is asserted to contain exactly one guaranteed `kubejs:atlas_service_plate` and exactly one `kubejs:atlas_transfer_maintenance_manual` entry;
- the proof node occupies the controlled records side with clear headroom and east approach;
- three bounded D3 encounters occupy the Bay-01 service edge, Bay-02 staging edge and isolated core/rework buffer;
- D0 and D1 contain no proof chest or spawners;
- no shared loot, quest, item or registry contract was changed.

## Freeze and mechanical evidence

- D0 is serialized and checked byte-identical to accepted Gate-B r1 before rendering and again after state rendering;
- Gate-B dimensions, massing anchors, three-cell identities, controlled doors, circulation, utilities, systems and Atlas identity are asserted in D0, D1 and pre-gameplay D3;
- final D3 rechecks all 36 controlled door blocks and every vehicle, transverse, technician, customer, parts and records/core route;
- exact proof count/table/access, encounter count/separation, surviving service-pipe coverage, primary steel structure and institutional-sign density are asserted;
- shipping remains unchanged at SHA-256 `d80dfca574d8f96eca633ac515e810f02f52e7eab2f36195977b42708068fe0d` and Git blob `4b2df6f6d8bcb5a58511318f0fe78f9f5fc1d44a`;
- all temporary review NBT files are removed.

## Independent reviewer obligations

Inspect the labeled comparison, all three contact sheets, all principal fixed-camera views and floor slices. Decide whether:

1. D0 exactly and visibly preserves the accepted intact architecture, three-cell workflow, routes, utilities and Atlas identity;
2. D1 reads as competent ordinary maintenance and recheck escalation rather than emergency conversion or decorative clutter;
3. the three recheck/collar sequences remain tied to diagnostics, heavy repair and calibration;
4. D3 moisture and corrosion follow the real rear/east drain and flashing path rather than appearing randomly;
5. localized roof/canopy openings retain support and all debris is gravity-consistent;
6. public/Bay-01 preservation versus Bay-03/support-edge damage is causally believable;
7. all vehicle and staff routes, cell identities, equipment, utilities, records approach and proof access remain readable;
8. three encounters remain bounded and the single proof node remains recoverable;
9. D2 omission is appropriate;
10. no over-ruin, floating debris, unsupported panel, blocked route or major narrative inconsistency requires revision.

Pass 19 and authoritative synchronization remain blocked pending an independent `PASSED` decision for this exact artifact.

**OWS-009 GATE C r1: REVIEW NEEDED.**
