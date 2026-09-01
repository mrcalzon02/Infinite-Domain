# 10 — Heavy Rebuild and Institutional Style Standard

## Purpose

This document governs the dedicated **heavy schematic rebuild** of OWS-001 through OWS-064 after functional Old World coverage has been established.

The heavy rebuild is not a second functional-implementation pass and it must never erase or blur the distinction between functional status, runtime status, and schematic quality. A structure may already generate valid NBT, carry deterministic proof loot, have a prepared quest, and still remain `schematic_revision_pending` until this procedure is completed.

The objective is to replace overlay-style donor conversions with structures that read as coherent places designed for a specific institution, purpose, workflow, historical moment, and collapse event.

## Non-negotiable execution order

Rebuild **one OWS target at a time in numeric order**, beginning with OWS-001. Do not bulk-convert families and do not revise ten sites in parallel. A later site may be inspected for reference, but the active target remains the only site whose heavy-rebuild status advances.

One target normally equals one deliberate reconstruction commit, followed by a corrective commit only when validation identifies a concrete defect. Do not use a broad mutation pass that touches many completed targets merely to enforce a new style rule. If a later improvement is discovered, record it as a future consistency pass unless it fixes a functional defect.

The sequence for every site is:

1. donor audit;
2. institutional identity contract;
3. operational-program definition;
4. architectural reconstruction;
5. circulation and access reconstruction;
6. machinery and furnishing pass;
7. signage and wayfinding pass;
8. historical-damage pass;
9. narrative-evidence and practical-loot pass;
10. micro-detail and environmental-storytelling pass;
11. static render review;
12. mechanical/static validation;
13. quality-status promotion.

Do not skip directly from donor audit to decoration.

## Pass 1 — Donor audit

Before editing, record what the donor actually contributes:

- footprint and overall dimensions;
- exterior massing;
- entrances and emergency exits;
- loading/service access;
- floor count and vertical circulation;
- useful room shells;
- utility spaces;
- roof access and rooftop plant;
- terrain interface;
- existing damage;
- any donor feature that contradicts the target function.

Classify each major donor feature as **retain**, **rebuild**, **remove**, or **repurpose**. The donor is raw material, not authority. A structure must not preserve a supermarket, office, hotel, warehouse, hospital, or factory layout merely because that is where the generator began.

## Pass 2 — Institutional identity contract

Before room placement, state the full institution name, abbreviation, building subtype, and visual language. The company must be identifiable before the player reads quest text.

Every primary corporate structure must include at minimum:

- one exterior identity installation carrying the **full company/institution name**;
- one abbreviated identity mark or repeated color/material motif readable from another exterior angle;
- one internal directory, department marker, or operational identity sign;
- institution-specific floor, wall, furniture, lighting, barrier, and utility treatment;
- institution-specific wording rather than generic `LAB`, `WAREHOUSE`, or `DANGER` signs everywhere.

A sign-only reskin does not count. Institutional identity must also be expressed by architecture, workflow, equipment, room proportions, access control, materials, and maintenance assumptions.

## Pass 3 — Operational program

Write the building's normal workflow as a physical chain before rebuilding rooms. Example:

`delivery -> receiving -> inspection -> cold storage -> public issue -> returns -> sanitation -> service exit`

Every major workflow stage should have a physically understandable location. Rooms may be compact, combined, damaged, or partially inaccessible, but the building should still answer:

- What entered here?
- Who handled it?
- Where was it stored?
- What process happened next?
- Where did staff move differently from the public?
- Where were waste, returns, maintenance, power, water, data, or hazardous materials handled?
- How did goods, patients, samples, vehicles, or information leave?

Purpose should drive the plan rather than the donor's existing empty volume.

## Pass 4 — Architectural reconstruction

Heavy rebuild means the target may alter the donor's walls, doors, room sizes, roofline, facade, windows, secondary structures, service yard, loading apron, stairs, catwalks, or vertical circulation where needed.

Required considerations:

- credible primary entrance;
- credible staff/service entrance where appropriate;
- loading access for freight-heavy structures;
- stairs/lifts/catwalks that actually connect occupied levels;
- corridors sized for the building's function;
- believable room adjacency;
- useful dead-end rooms only when their purpose is clear;
- exterior massing that communicates function at a distance;
- roof and utility volumes consistent with the facility's machinery;
- terrain edges that do not leave floating doors, buried loading bays, or inaccessible proof areas.

Do not preserve nonsensical donor circulation for lineage purity.

## Pass 5 — Circulation and access

Trace at least three routes where applicable:

1. visitor/public route;
2. staff/technical route;
3. freight/service/emergency route.

A small site may legitimately merge routes. A large industrial, medical, logistics, research, or aerospace facility generally should not.

The proof chest/evidence location must be reachable through a route that makes narrative sense. It must not be placed in a random corner solely because a coordinate was available.

## Pass 6 — Machinery, furniture, and purpose-specific fixtures

Populate rooms according to actual use. Prefer readable clusters over random decorative noise.

Examples include:

- receiving desks beside loading areas;
- pallet staging beside dispatch doors;
- sample racks near test cells;
- control desks with sightlines to machinery;
- pumps beside pipe runs and tanks;
- patient preparation near treatment spaces;
- cold storage connected to insulated transfer routes;
- repair benches beside parts stock;
- server/service aisles beside power and cooling support;
- launch-control hardware separated from assembly or fueling areas.

A quest-grade structure should contain multiple purpose-specific fixtures, not one token machine surrounded by colored concrete.

## Pass 7 — Signage and wayfinding

Signage is a functional information layer, not decorative flavor text.

Every rebuilt site should carry signage in several classes as appropriate:

### Identity signs

Use the full institution name on a primary exterior sign. Abbreviations may be used on secondary markings.

Examples:

- `VERDANT CONTINUUM FOODS`
- `ATLAS KINETIC INDUSTRIES`
- `POLYCORE ADVANCED MATERIALS`
- `PLEROMA DISTRIBUTION GROUP`
- `AEVUM THERAPEUTICS`
- `HELION ENERGY SYSTEMS`
- `BLACKGLASS INFORMATION SYSTEMS`
- `ASTERION ORBITAL INDUSTRIES`
- `CONTINUITY`

### Facility-name signs

The site's actual function should be named where a real organization would identify it, for example `NEIGHBORHOOD CULTURE SERVICE DEPOT`, `REGIONAL POWER OPERATIONS CENTER`, or `INTERMODAL INSPECTION YARD`.

### Directional signs

Wayfinding must correspond to real rooms and routes: `RECEIVING`, `CULTURE ISSUE`, `COLD LOCKERS`, `RETURNS`, `STAFF ONLY`, `SERVICE`, `WARD B`, `CONTROL`, `DISPATCH`, `TEST CELLS`, `LOADING 1-4`, etc.

### Process signs

Use labels that explain workflow: batch numbers, lane numbers, chamber numbers, service intervals, quarantine status, cold-chain temperature classes, material classes, controller banks, launch sectors, treatment bays, and cargo routing.

### Safety and emergency signs

Warnings must match the facility and collapse phase. Use specific language such as `BIOLOGIC MATERIAL RETURN`, `LOCKOUT BEFORE SERVICE`, `CERAMIC BARRIER TEST`, `ESSENTIAL LOAD`, `ENCRYPTED CORE`, or `PROPELLANT SERVICE` instead of generic apocalypse warnings.

### Collapse-overprint signs

Later phases may overlay normal signage with temporary notices, military restrictions, handwritten substitutions, quarantine tape/marking, closure instructions, rationing, evacuation arrows, bypass notices, or firebreak authority.

The original operational sign should often remain partially visible underneath the emergency layer.

### Signage density targets

These are minimum design targets, not excuses to spam text blocks:

- Common: 5+ distinct purposeful signs/markers;
- Uncommon: 8+;
- Rare: 12+;
- Landmark: 16+.

At least one sign or spatial marker should help the player understand the major story point **without opening a book**.

If the current NBT helper cannot safely author text-bearing signs for the target Minecraft version, do not fake completion with blank sign blocks. First implement and validate a reusable sign/block-entity helper, then use it consistently.

## Pass 8 — Institution build languages

### Verdant Continuum Foods — VCF

Full name: **Verdant Continuum Foods**.

Architecture: hygienic agro-industrial and food-service design; green/white identity; clean glass; refrigeration; washable surfaces; culture lockers; nutrient infrastructure; cultivation, packing, cold-chain, and food-quality spaces.

Spatial logic: product and biological material should move through controlled receiving, growth/storage, sanitation, packaging/issue, return, and waste/service paths.

Sign language: `CULTURE ISSUE`, `RETURN CULTURES`, `NUTRIENT RETURN`, `COLD LOCKERS`, `SANITATION`, `BATCH`, `QUALITY HOLD`, `EVERCROP`.

Failure language: contamination at drains, joints, filters, seals, gaskets, service conduits, and allegedly separated cultivation systems.

### Atlas Kinetic Industries

Architecture: orange/charcoal industrial identity; machinery visible and maintainable; large access lanes; gantries; service cages; standardized machine cells; parts storage; repair infrastructure.

Spatial logic: feed -> process -> inspection -> rework -> output, with separate maintenance access wherever scale allows.

Sign language: `CELL 01`, `TRANSFER`, `SERVICE ACCESS`, `LOCKOUT`, `MANUAL BYPASS`, `PARTS ISSUE`, `CALIBRATION`, `OUTBOUND`.

Failure language: machines remain mechanically recognizable while maintenance intervals collapse, operators disappear, and functioning lines cannibalize failed ones.

### PolyCore Advanced Materials

Architecture: magenta/white research identity; controlled test cells; mineral/ceramic/metal retrofit layers; observation corridors; sample stores; isolation vestibules.

Spatial logic: specimen intake -> preparation -> exposure/test -> observation -> failure quarantine -> records/material substitution.

Sign language: `SPECIMEN INTAKE`, `EXPOSURE CELL`, `BARRIER CLASS`, `FAILED MATERIAL`, `CERAMIC`, `COMPOSITE`, `SUBSTITUTION`, `ISOLATION`.

Failure language: room order should physically demonstrate escalation from ordinary polymers to increasingly exotic barrier materials.

### Pleroma Distribution Group

Architecture: cyan/white logistics identity; broad freight lanes; repeated bay geometry; loading courts; cold-chain infrastructure; container fields; customs/inspection; standardized cargo modules.

Spatial logic: inbound -> manifest/inspection -> sort -> storage/cold hold -> outbound, with quarantined or rejected cargo visibly interrupting the flow in later phases.

Sign language: `INBOUND`, `DISPATCH`, `BAY`, `ROUTE`, `COLD CHAIN`, `CUSTOMS`, `CERTIFIED`, `REJECTED`, `QUARANTINE CARGO`, `OUTBOUND`.

Failure language: throughput backs up, quarantine categories multiply, cargo becomes barriers, and a system designed for constant movement becomes physically clogged.

### Aevum Therapeutics

Architecture: calm premium clinical spaces; purple/white identity; smooth quartz/glass; privacy; preparation and recovery areas; controlled biologic storage; careful patient circulation.

Spatial logic: reception -> assessment -> preparation -> treatment -> monitoring -> recovery/follow-up, with staff supply and cold-chain routes behind the patient-facing sequence.

Sign language: `RECEPTION`, `TREATMENT`, `RECOVERY`, `BIOLOGIC PREPARATION`, `MONITORING`, `COLD STORAGE`, `PATIENT ACCESS`, `CLINICAL SUPPLY`.

Failure language: good medicine becomes dangerous to interrupt; supply rationing and overflow should appear before generalized ruin.

### Helion Energy Systems

Architecture: cyan/light-blue and white utility identity; heavy safety zoning; switchgear; substations; pumps; coolant systems; high-voltage compounds; control rooms; service corridors.

Spatial logic: generation/intake -> conversion -> distribution -> control -> isolation/maintenance, with emergency power and essential-load handling legible.

Sign language: `HIGH VOLTAGE`, `FEEDER`, `SWITCHYARD`, `COOLANT`, `PUMP`, `ESSENTIAL LOAD`, `MANUAL SWITCHING`, `OUTAGE PRIORITY`, `SHUTDOWN`.

Failure language: tiny insulation, seal, or coolant problems cascade into manual switching, rolling outages, and emergency stabilization.

### Blackglass Information Systems

Architecture: black/white secure infrastructure; sparse cyan routing marks; hardened utility rooms; controlled entrances; server/data halls; archive cores; backup power; physical security layers.

Spatial logic: access control -> network intake -> routing/compute -> archive -> protected utility -> physical data handoff.

Sign language: `AUTHORIZED ACCESS`, `ROUTING`, `CORE`, `ARCHIVE`, `SECURE`, `BACKUP POWER`, `NETWORK EXCHANGE`, `PHYSICAL MEDIA`.

Failure language: facilities may remain physically valuable while meaning becomes inaccessible. Preserve later Darknet reasons to return.

### Asterion Orbital Industries

Architecture: clean aerospace production; black/white technical identity with mission-specific markings; large assembly clearances; tracking/communications; launch logistics; specialized cargo; controlled clean areas.

Spatial logic: component receiving -> clean assembly -> integration/test -> mission control/tracking -> launch/service logistics.

Sign language: `ASSEMBLY`, `CLEAN ACCESS`, `INTEGRATION`, `TELEMETRY`, `TRACKING`, `MISSION CONTROL`, `LAUNCH SERVICE`, `PROPELLANT`, `FLIGHT HARDWARE`.

Failure language: interrupted launches, evacuation, off-world continuity, abandoned mission hardware, and records surviving outside ordinary terrestrial information systems.

### Continuity

Continuity is not a normal corporation and must not receive one sleek corporate palette.

Architecture: appropriated offices, field laboratories, command rooms, archives, temporary secure zones, mixed equipment from the institutions above, military overlays, handwritten cross-reference boards, and rapidly improvised data synthesis.

Spatial logic: evidence intake -> correlation -> command decision -> communications -> secure archive/evacuation, often reusing a building never designed for the purpose.

Sign language should identify working groups, evidence boards, clearance levels, firebreak sectors, atmospheric monitoring, evacuation routes, archive categories, and cross-institution data sources rather than pretending Continuity had decades of standardized facilities.

Failure language: escalating synthesis and urgency. The tragedy is that the pieces are finally understood while capacity to act disappears.

## Pass 9 — Historical damage chronology

Damage must be authored after the normal facility is understandable.

Do not scatter random rubble first and invent a story afterward. Establish what the building looked like in normal use, then apply the target collapse phase.

A damage event should identify:

- origin;
- direction or affected system;
- operational consequence;
- emergency response;
- later weather/scavenger/biological effects.

The player should be able to distinguish maintenance failure, contamination, quarantine, evacuation, deliberate firebreak damage, combat, long-term decay, and later scavenging.

## Pass 10 — Narrative evidence and practical loot

Mandatory proof remains deterministic. Its container placement must be purpose-driven: records office, supervisor station, secure archive, dispatch booth, test review desk, clinic records point, control room, mission desk, etc.

Practical loot should reflect the building's former function without making every quest site a jackpot. Evidence and useful salvage should reinforce each other.

## Pass 11 — Micro-detail pass

Only after rooms and routes work, add detail that makes occupation believable:

- lighting and ceiling treatment;
- desks, counters, lockers, shelves, benches;
- conduit/pipe runs;
- floor markings;
- pallets and return stock;
- maintenance carts and spare parts;
- break areas and staff support;
- wash/decontamination points;
- office clutter;
- inspection stations;
- barriers and temporary partitions;
- local signage;
- exterior service equipment;
- drainage, vents, roof plant, and utility penetrations;
- environmental storytelling tied to a specific event.

Do not substitute hundreds of random props for coherent layout.

## Pass 12 — Static review gate

Before quality promotion, review all available renders and answer:

- Is the building's purpose obvious from outside?
- Is the institution obvious without quest text?
- Does the entrance look like an entrance?
- Can the operational workflow be traced?
- Are stairs/lifts/catwalks coherent?
- Are service/freight routes plausible?
- Are machinery clusters attached to believable utilities and work areas?
- Does signage point to things that actually exist?
- Does the full institution name appear appropriately?
- Is the collapse event spatially understandable?
- Is mandatory evidence located where records/evidence plausibly belong?
- Are there empty dead volumes that still read like untouched donor space?
- Does the structure still look like a renamed donor?

Any `yes` to the last two questions blocks completion.

## Pass 13 — Validation and quality-status promotion

Run the existing static generation, render, registry, loot, NBT, block-ID, and quest-reference checks. Heavy rebuild must not regress functional correctness.

A completed site's quality status may advance only through explicit states such as:

- `schematic_revision_pending`
- `heavy_rebuild_planning`
- `heavy_rebuild_in_progress`
- `heavy_rebuild_static_review`
- `heavy_rebuild_static_passed`
- `runtime_quality_review_pending`
- `runtime_quality_approved`

Runtime approval remains a separate later event. `heavy_rebuild_static_passed` does **not** mean worldgen/runtime approved.

## Current sequence

The heavy rebuild begins at **OWS-001 — Verdant Continuum Foods Neighborhood Culture Service Depot** and proceeds sequentially through OWS-064.

OWS-001 must be rebuilt as a genuine neighborhood culture-service depot rather than a supermarket with VCF overlays. Its first planning workflow is:

`culture delivery -> receiving/temperature check -> refrigerated culture lockers -> public issue counter -> customer return intake -> return quarantine/sanitation -> crate consolidation -> service dispatch`

Its exterior primary identity should explicitly read **VERDANT CONTINUUM FOODS** and the facility subtype should be legible as a **NEIGHBORHOOD CULTURE SERVICE DEPOT**.
