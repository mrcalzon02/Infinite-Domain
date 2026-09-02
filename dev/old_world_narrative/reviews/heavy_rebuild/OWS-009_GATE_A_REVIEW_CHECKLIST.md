# [SYSTEM REPORT] OWS-009 Visual Gate A — Massing Review Checklist

## Gate purpose

Gate A judges whether the **D0 intact macro architecture and site occupation** of OWS-009 are strong enough to justify structural, circulation, interior and operational development. A successful render or deterministic build is not automatically a pass.

**Target:** OWS-009 — Atlas Roadside Automated Repair Depot  
**Candidate envelope:** 49 x 18 x 41  
**Fixed camera set:** `ows009_fixed_v1`  
**Candidate record:** `dev/old_world_narrative/reviews/heavy_rebuild/OWS-009_GATE_A_R1_CANDIDATE.md`  
**Review artifacts:** `dev/old_world_narrative/reviews/heavy_rebuild/visual/OWS-009/gate_a_massing/r1/`

Passes 7–12 and all damage/loot/encounter production work remain blocked until Gate A is independently recorded as passed.

## Blocking visual questions

### Functional read

- Does the building unmistakably read as a roadside repair depot rather than a warehouse, factory, gas station or generic commercial box?
- Are all three service cells legible as distinct but connected automotive functions?
- Is the customer/service bar visibly subordinate to the vehicle-service hall while still presenting a clear pedestrian entrance?
- Are parts receiving, rear technician movement and secure records/calibration support readable as service architecture rather than decorative annexes?

### Scale and proportions

- Does 49 x 18 x 41 still read as a common roadside facility rather than an Atlas factory or regional distribution center?
- Are the three service thresholds wide and tall enough for believable vehicle access without becoming hangar doors?
- Does the tall center cell justify its extra height through heavy-service function rather than arbitrary silhouette variation?
- Are the customer bar, support bar and roof plant proportionate to the repair hall they serve?

### Silhouette and facade depth

- Do the stepped cell roofs, public bar, rear support bar and roadside blade create a coherent silhouette from all four exterior quadrants?
- Is Atlas identity carried by architecture and hierarchy rather than orange/black surface treatment alone?
- Do side and rear faces contain massing-level depth tied to real functions, avoiding blank slabs whose only variation is material color?
- Does the roadside blade grow from a credible structural datum instead of appearing pasted onto or floating above the building?

### Vehicle and pedestrian circulation

- Can the three recovery/service approaches be read independently from the customer walk?
- Is pedestrian entry protected from active vehicle movement rather than routed through the bay apron?
- Does the east delivery strip plausibly reach parts receiving without crossing the public threshold?
- Is removed-core / waste collection visibly separable from the customer side?
- Does the site leave credible turning and staging room without becoming an undifferentiated full-lot slab?

### Roof and service anatomy

- Do the three roof/process housings correspond to the service cells below and read as physically connected equipment support rather than decorative rooftop boxes?
- Is the longitudinal header believable as a shared service spine at massing scale?
- Is there enough roof access and separation to support later drainage, ventilation, exhaust and maintenance logic?
- Are the roof masses subordinate to the roadside building rather than making the site monumental?

### Interior/cutaway capacity

- Does the cutaway preserve the asserted transverse movement field and rear technician spine?
- Can the three service cells accept later lifts, benches, diagnostic equipment and vehicle working clearances without destroying circulation?
- Can the lower public bar accept reception/waiting/parts-counter functions without spilling into the service hall?
- Can the support bar later contain parts, records/calibration, staff, utilities and evidence without becoming dead or inaccessible space?

## Placement and compatibility blockers

These are required for Gate-A acceptance even where the fixed-camera review can only establish design capacity rather than runtime proof.

### Terrain interface

- The apron, pedestrian threshold, parts-delivery edge and rear collection edge must each have enough bounded transition space for foundation, ramp, drainage or retaining treatment.
- No entrance or bay threshold may require broad terrain flattening to avoid being buried or floating.
- The 49 x 41 site envelope must not imply unbounded hardscape beyond the structure footprint.

### Lost Cities coexistence

- OWS-009 remains additive worldgen only.
- Placement must reject/skip Lost Cities city, road and rail footprints rather than replacing, erasing, tunneling through or flattening them.
- The massing must leave enough perimeter clearance that later bounded terrain adaptation cannot create hard seams against Lost Cities roads/buildings.
- No new or parallel road/worldgen authority may be introduced to make the garage fit.

### Rotation / mirroring

- Every supported rotation must preserve a usable relationship among road-facing recovery apron, pedestrian entrance, parts delivery and rear service/collection edge.
- A rotation that faces the service approaches into protected infrastructure, impossible terrain or an adjacent structure is an invalid placement and must be rejected by conditioning.
- Mirroring is not assumed. If the authoritative placement path does not demonstrably mirror OWS-009, mirror acceptance remains out of scope rather than inferred.

## Hook-preservation contract

Later passes must preserve these authoritative gameplay/narrative hooks while geometry evolves:

- corporation: `infinite_domain:atlas_motor_works`
- evidence object: `infinite_domain:atlas_contract_fragment`
- advancement: `infinite_domain:lost_world/atlas_roadside_repair_depot`
- encounter class: `medium`
- loot class: `corp_failed`
- production mode: additive `new_worldgen`

Gate A does not place final loot, encounters or evidence. It must prove that the shell provides believable future locations for them without blocking traversal or exposing proof on the exterior.

## Automatic Gate-A rejection conditions

Reject and revise if any of the following remain:

- generic single-box garage massing with bay doors pasted onto one elevation;
- service cells that cannot be distinguished from exterior or cutaway views;
- customer access competing directly with vehicle recovery lanes;
- toy-scale vehicle thresholds or implausibly shallow working depth;
- roof plant detached from the service functions below;
- Atlas branding doing the architectural work instead of the building form;
- giant untreated side/rear planes;
- full-lot paving with no distinct public, service, delivery and collection zones;
- floating/buried threshold assumptions or no room for bounded grade adaptation;
- any required Lost Cities road/rail/building overlap;
- a supported rotation that destroys frontage/access relationships;
- detailed machinery, loot, rubble, signage density or damage used to disguise weak massing.

## Gate record requirements

The independent review must record findings for front-left, front-right, rear-left, rear-right, roof/top, interior cutaway and floor slices; compare against the Phase-0 donor; explicitly accept or reopen the 49 x 18 x 41 envelope; freeze accepted massing aspects; identify any required r2 revisions; and end with exactly one decision: `PASSED` or `REVISION REQUIRED`.

A Gate-A pass approves macro massing only. It does not approve structural spans, final facade, interiors, utilities, damage, encounters, loot, evidence placement, rotation implementation, Lost Cities runtime coexistence, shipping-NBT equivalence or production admission.
