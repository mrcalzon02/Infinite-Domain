# OWS-001 Heavy Rebuild Plan

## Target

**OWS-001 — Verdant Continuum Foods Neighborhood Culture Service Depot**

Institution: **Verdant Continuum Foods (VCF)**

Donor: `grocery_clean_master()`

Current quality status: `schematic_revision_pending`

Heavy rebuild status: `heavy_rebuild_planning`

## Why OWS-001 needs a heavy rebuild

The current implementation preserves almost the entire supermarket donor and overlays VCF identity, cooler blocks, crates, a pallet/return area, a quarantine patch, and the evidence chest. That proves the site mechanically, but the inherited sales-floor plan still dominates the building.

The heavy rebuild must make this location read as a neighborhood biological-food service depot built around routine culture distribution and returns, not a grocery store that later received green concrete.

## Donor audit

### Retain

- Overall 39 x 13 x 33 neighborhood-scale footprint.
- Street/parking relationship and compact commercial massing.
- Front vestibule position as the public entrance.
- Rear receiving apron and loading access.
- Rooftop mechanical volume as a basis for refrigeration/HVAC plant.
- Brick/masonry neighborhood shell where it helps the site read as an ordinary local commercial service building rather than a secret laboratory.
- Back-of-house service access concept.

### Rebuild

- Main facade identity and sign blade.
- Entrance canopy and public threshold.
- Entire supermarket sales floor.
- Checkout-lane geometry.
- Produce department.
- Bakery/deli department.
- Grocery gondola shelving.
- East-wall retail cooler arrangement.
- Public restroom adjacency if it interferes with service flow.
- Rear room boundaries so receiving, quarantine/sanitation, crate consolidation, staff records, and dispatch are distinct.
- Roof plant so the visible equipment supports cold-chain service rather than generic commercial HVAC.

### Remove

- Supermarket checkout identity.
- Produce crate merchandising.
- Bakery/deli cooking identity.
- Retail gondola aisles that do not support culture issue/return workflow.
- Retail-oriented customer-service layout.
- Decorative remnants whose only purpose is to preserve the donor as a supermarket.

### Repurpose

- Front customer-service zone -> **Culture Issue / Account Service**.
- Former checkout zone -> controlled public queue and issue stations.
- Former produce/bakery edge -> **Return Intake / Sanitation**.
- Former gondola area -> refrigerated culture locker banks and short-duration holding.
- Former rear stockroom -> sealed return-crate consolidation and clean stock.
- Former management office -> depot supervisor / batch records / deterministic evidence location.
- Rear receiving -> inbound culture delivery and temperature inspection.
- Rooftop plant -> refrigeration, ventilation, and cold-chain service equipment.

## Operational workflow

Primary material flow:

`culture delivery -> rear receiving -> temperature/batch inspection -> refrigerated holding -> culture locker/issue staging -> public issue counter`

Return flow:

`public return intake -> quarantine hold -> sanitation/inspection -> reusable crate consolidation -> rear service dispatch`

Staff route:

`staff entry -> supervisor/records -> receiving -> cold holding -> issue support -> returns/sanitation -> service dispatch`

Public route:

`front vestibule -> account/queue -> culture issue -> optional return desk -> exit`

The public should not walk through receiving, sanitation, quarantine, or crate consolidation.

## Architectural reconstruction targets

### Exterior

- Replace supermarket branding with a full-width VCF identity field.
- Primary exterior text must include **VERDANT CONTINUUM FOODS**.
- Secondary facility text must include **NEIGHBORHOOD CULTURE SERVICE DEPOT**.
- Preserve neighborhood scale; this is not a research campus.
- Use green/white hygienic corporate treatment over a durable masonry neighborhood shell.
- Make the loading/service side visually distinct from the public frontage.
- Give the cold-chain function visible rooftop/service equipment.

### Public zone

- A real vestibule and queue spine.
- 2-3 issue/account stations rather than supermarket checkouts.
- Controlled pickup area tied to refrigerated lockers.
- Separate return counter with visible route toward quarantine/sanitation.
- Small waiting/information area is acceptable; broad retail browsing is not.

### Refrigerated culture zone

- Locker/bank geometry should be denser and more deliberate than a grocery cooler wall.
- Separate clean issue stock from returned material.
- Provide service access behind or beside locker banks where footprint permits.
- Include batch/temperature inspection points.

### Receiving and service

- Rear delivery threshold with pallet/crate staging.
- Temperature-check/inspection station immediately after receiving.
- Clean stock staging separated from returned stock.
- Return crate consolidation next to rear dispatch rather than in the public path.

### Quarantine/sanitation

- Small but unmistakable controlled room or screened bay.
- Yellow early-anomaly isolation overlay should be local, not apocalyptic.
- Physical story: a recurring return problem has forced one cooler/return segment out of normal service.
- The site is still functioning.

### Supervisor/records

- Small office or secure records point overlooking or adjacent to the service floor.
- The deterministic evidence chest belongs here or in an equally plausible dispatch/records position.

## Machinery and fixture targets

Minimum operational fixtures for the rebuild:

- multiple refrigeration/culture-locker banks;
- receiving temperature/batch check station;
- sealed clean culture crates;
- distinct returned-culture crates;
- issue counters;
- return counter;
- sanitation/wash point;
- crate consolidation/pallet staging;
- rooftop/service refrigeration plant;
- supervisor records point;
- locally quarantined cooler/return bay.

Fixtures should form readable work clusters rather than being distributed as decoration.

## Signage plan

Minimum purposeful sign count for this common structure: **5**, but OWS-001 should target **8-10** because it establishes VCF's visual grammar for later sites.

Required signs/markers:

1. `VERDANT CONTINUUM FOODS`
2. `NEIGHBORHOOD CULTURE SERVICE DEPOT`
3. `CULTURE ISSUE`
4. `RETURN CULTURES`
5. `COLD LOCKERS`
6. `RECEIVING / STAFF ONLY`
7. `SANITATION`
8. `QUALITY HOLD` or `QUARANTINE RETURN BAY`

Optional useful markers:

- `BATCH CHECK`
- `CLEAN STOCK`
- `RETURN CRATES`
- `SERVICE DISPATCH`
- locker/bay numbers;
- cold-chain handling instruction;
- normal optimistic Evercrop service wording.

The early anomaly should be communicated by a temporary quality-hold notice over otherwise normal VCF signage, not by generalized disaster warnings.

## Environmental story

The player should be able to infer without opening a book that:

- this was a routine neighborhood service;
- biological culture products were issued at ordinary local scale;
- customers returned culture containers/material;
- the company expected those returns to be sanitized and recirculated;
- one return/cold-chain segment began failing quality checks;
- workers isolated the problem while continuing normal service.

## Evidence placement

Primary proof: `kubejs:vcf_culture_service_manifest`

Supporting lore: `kubejs:vcf_return_crate_log`

The deterministic container should be placed at the supervisor/batch-records or dispatch station, not hidden in an arbitrary retail corner.

## Validation gate for OWS-001

OWS-001 cannot advance to `heavy_rebuild_static_passed` until all answers are yes:

- Does the exterior read as Verdant Continuum Foods before quest text?
- Does the full company name appear on the primary identity installation?
- Does the facility read as a culture-service depot rather than a supermarket?
- Can the culture-delivery route be traced?
- Can the public issue route be traced?
- Can the return/quarantine/sanitation route be traced?
- Are clean and returned culture materials physically separated?
- Does the quarantine anomaly remain local and consistent with an early anomaly?
- Is the evidence container in a plausible records/dispatch location?
- Are at least five purposeful signs/markers present, with a target of eight to ten?
- Is the supermarket donor identity subordinate rather than dominant?
- Do static generation, proof-loot, and NBT validation still pass?

## Next implementation action

Re-author `build_001()` directly in the authoritative Old World generator path. Do not add a second mutation layer. The new builder should reconstruct the internal program and facade while preserving only the donor features classified `retain` above.
