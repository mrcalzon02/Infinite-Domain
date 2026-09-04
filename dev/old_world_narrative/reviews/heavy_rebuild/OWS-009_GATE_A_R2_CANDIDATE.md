# [SYSTEM REPORT] OWS-009 Gate A r2 — Massing Candidate

**Target:** OWS-009 — Atlas Roadside Automated Repair Depot  
**Procedure authority:** `docs/HEAVY_REBUILD_DOCTRINE.md`  
**Artifact:** `dev/old_world_narrative/reviews/heavy_rebuild/visual/OWS-009/gate_a_massing/r2/review_manifest.json`  
**Contact sheet:** `dev/old_world_narrative/reviews/heavy_rebuild/visual/OWS-009/gate_a_massing/r2/contact_sheet.png`  
**Builder:** `dev/scripts/render_ows009_gate_a_massing.py`  
**Deterministic suite:** `dev/scripts/verify_ows009_gate_a_suite.py`  
**Revision:** `massing-r2@local`  
**Fixed camera set:** `ows009_fixed_v1`  
**Dimensions:** 49 x 18 x 41  
**Review-model SHA-256 at persisted r2 render:** `cbcdb6151de083cb81fd8e3aa52f81c5741901e4b97c3fe977fa15409e05de83`  
**Renderer SHA-256 at persisted r2 render:** `4eabfdc2916c464a7f27d4717a0a7b40acad3852957c26858e139c48f5d02c62`  
**Changed positions from r1:** 1,902  
**Status:** **R2 DETERMINISTIC EXECUTION + FIXED-CAMERA REVIEW PENDING — no Gate-A acceptance**

## Revision basis

The independent r1 reviewer froze the compact envelope, three service openings, north recovery apron, separate customer approach, east support footprint, protected internal movement fields, attached roadside blade, aligned rear plant and absence of downstream content. R2 changes only the reopened Pass-6 failures.

## R2 response to blocking findings

1. **Side/rear wall depth:** cell- and service-spine-aligned steel piers project beyond the shell; lower wall fields recess between them; clerestories receive deep frames rather than thin applied strips.
2. **Roof hierarchy:** Bay 01 now carries a low shallow diagnostic monitor, Bay 02 the tallest transverse exchange monitor integrated with the roadside blade, and Bay 03 an offset calibration monitor.
3. **Threshold identity:** Bay 01 uses a low diagnostic hood, Bay 02 a tall exchange portal and Bay 03 a wider lower release canopy.
4. **Support thresholds:** clean parts receiving has a separately framed east delivery portal; removed cores/rework use a charcoal south portal opening onto the isolated collection yard.
5. **Atlas architecture:** an attached rear steel/orange service header, projected structural rhythm, deep charcoal frames and operational orange beams establish building-scale identity beyond facade color.
6. **Terrain-interface repair:** north recovery/customer hardscape stops short of Z0; the east service strip preserves X48 as a seam-control band; Z40 remains rear transition capacity; a four-block east maneuvering strip remains available.
7. **Construction plausibility:** deterministic contracts now cover structural load paths for portal frames, cell-line piers, roof monitors/plant housings, projected facade frames, annex roofs/canopy and the Atlas architectural blade.
8. **Operational access:** deterministic contracts now cover two-block-high supported interior circulation and vehicle-sized swept access from the recovery apron through all three service thresholds.
9. **Transform safety:** all four Y rotations and X-mirrored variants have dedicated coordinate-safety contracts for bounds, inventory preservation and transformed protected edges.
10. **Grade/foundation interface:** deterministic contracts now cover the site datum, supported y=1 construction, public landing/door threshold separation, all three hardened vehicle approaches, east service grade and protected transition-edge overrun.

## Deterministic Gate-A suite

`dev/scripts/verify_ows009_gate_a_suite.py` is the single fail-fast entrypoint for the repository-local Gate-A checks. It currently invokes:

- `verify_ows009_gate_a_static.py` — prerequisite records, frozen shipping-source provenance, template bounds, cell hierarchy and connected operational circulation;
- `verify_ows009_gate_a_vehicle_access.py` — supported vehicle swept volumes for all three repair cells;
- `verify_ows009_gate_a_transforms.py` — rotation/mirroring coordinate safety and protected-edge transform behavior;
- `verify_ows009_gate_a_articulation.py` — differentiated roof/portal hierarchy, projected facade rhythm, stepped east annex, clerestory breakup and Atlas physical identity;
- `verify_ows009_gate_a_load_paths.py` — structural connectivity to foundation/floor datum;
- `verify_ows009_gate_a_foundation_grade.py` — complete site datum, supported shell contact, customer/vehicle approaches, service grade and terrain-edge protection.

The suite is intentionally narrower than production admission. A deterministic suite PASS does **not** approve visual quality, Minecraft runtime/new-world placement, Lost Cities coexistence, generated-world terrain adaptation, shipping-NBT placement/transform behavior, quest/loot/evidence hooks or final production admission.

## Provenance

- untouched shipping SHA-256 before/after the persisted r2 render: `d80dfca574d8f96eca633ac515e810f02f52e7eab2f36195977b42708068fe0d`;
- frozen/live shipping Git blob at the persisted r2 render: `4b2df6f6d8bcb5a58511318f0fe78f9f5fc1d44a`;
- authoritative shipping modified by the Gate-A r2 review model: no;
- production dispatch, shared state, common registries and generated shipping sets modified by the Gate-A r2 review model: no.

The hashes above identify the persisted r2 render artifact; they are not silently promoted to describe later renderer edits. The current deterministic suite must be executed against the authoritative checkout before a new artifact/manifest is accepted.

## Remaining Gate-A obligations

1. Execute `dev/scripts/verify_ows009_gate_a_suite.py` against an authoritative `main` checkout and resolve every deterministic failure rather than waiving it.
2. Regenerate the complete fixed-camera r2 artifact set and manifest from the current accepted r2 builder after deterministic checks pass.
3. Inspect every exact r2 view against r1 using the unchanged fixed cameras and issue an explicit Gate-A r2 visual decision.
4. Reject any remaining floating, clipped, excessively repetitive, construction-implausible or misleading geometry discovered by the fixed-camera review.
5. Keep Passes 7–12 blocked until this exact Gate-A revision is explicitly accepted.

## Independent reviewer obligations

Inspect every exact r2 view and compare r1 using the unchanged fixed cameras. Decide whether:

1. the formerly broad flush side/rear planes now read as structurally articulated cell and service bays;
2. Bay 01, Bay 02 and Bay 03 have distinct functional roof/portal silhouettes without becoming roof clutter;
3. parts delivery and removed-core/rework collection are clearly separate from opposing quarters;
4. the attached header and projected frame establish Atlas heavy-industrial identity without relying on signs;
5. the compact common-site scale, recovery/customer separation and accepted support footprint remain intact;
6. the model has no new floating, clipped, excessive, repetitive or misleading detail.

The reviewer must issue an explicit Gate-A r2 decision and freeze accepted aspects or state exact revision obligations. Passes 7–12 remain blocked until this exact artifact is independently passed.

## Production-admission state

**NOT ADMITTED.** Runtime placement, Lost Cities coexistence, rotation acceptance in Minecraft, shipping-NBT equality, quest/loot/evidence behavior, structure detection and final production admission remain unclaimed until separately evidenced.