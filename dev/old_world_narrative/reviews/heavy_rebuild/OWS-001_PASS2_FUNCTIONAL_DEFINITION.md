# OWS-001 Pass 2 — Functional Definition

## Facility identity

**Structure:** OWS-001 — Verdant Continuum Foods Neighborhood Culture Service Depot  
**Institution:** Verdant Continuum Foods (VCF)  
**Narrative state for operational design:** D0, normal pre-crisis operation  
**Later historical overlay:** early-anomaly D1 local quality hold; final D3 long-abandoned worldgen state comes later

## What the building actually does

OWS-001 is a **neighborhood biological-food culture service depot**. It is not a supermarket, laboratory, greenhouse, hospital, or bulk warehouse.

VCF's Evercrop economy has made living agricultural/food cultures ordinary enough that households, local growers, kitchens, small institutions, and neighborhood food systems can receive culture packages locally, exchange controlled reusable containers, and return used or spent culture material for inspection, sanitation, recirculation, recovery, or disposal.

The depot therefore combines a calm public service counter with a compact cold-chain and biological-return operation behind it.

## Core operational promise

The building must visibly support two opposite material streams without allowing them to collapse into one another:

### Clean stream

`service delivery -> receiving -> documentation / batch and temperature check -> clean cold holding -> controlled issue staging -> customer issue`

### Return stream

`customer return -> contained return intake -> sanitation / visual inspection -> quality decision -> reusable return-crate consolidation OR quality hold -> rear service dispatch`

The clean stream is the ordinary business.

The return stream is why this particular building becomes narratively important: once material interfaces start failing, a routine reverse-logistics function becomes an early pathway through which staff notice that something is wrong.

## Building users

The architecture must plausibly accommodate:

- customers/account holders collecting cultures;
- customers returning culture containers/material;
- issue/account staff;
- cold-chain stock technicians;
- receiving/batch-check staff;
- sanitation/return staff;
- a depot supervisor / batch-record administrator;
- service couriers or freight handlers;
- maintenance/refrigeration technicians.

These roles do not all need separate rooms, but their paths and workstations must make sense.

## Required operational zones

### A. Public vestibule and information threshold

Purpose:

- weather/air lock and entry transition;
- orient customers before they reach controlled issue or returns;
- establish the full VCF identity immediately.

Requirements:

- clear primary entrance from the street/parking approach;
- direct sightline toward issue/account service;
- return function visible but physically separated;
- no direct opening into receiving, sanitation, cold stock, or freight spaces.

### B. Account / culture issue service

Purpose:

- verify account/order;
- hand cultures across a controlled counter;
- direct prepared orders toward the customer side.

Requirements:

- 2–3 service positions at Minecraft scale;
- direct staff-side connection to clean issue staging;
- short public queue that does not block return customers;
- corporate information/handling guidance near the counter.

### C. Refrigerated issue / culture-locker hall

Purpose:

- short-duration controlled holding of prepared cultures;
- support routine high-volume neighborhood pickup.

Requirements:

- repeated deliberate locker/freezer banks rather than one decorative cooler wall;
- 3-block or greater staff/service aisle where practical;
- connection to clean cold holding and issue counter;
- visible relationship to mechanical/refrigeration service above or behind the zone.

### D. Public return intake

Purpose:

- accept reusable containers and returned biological culture material without routing it through clean issue.

Requirements:

- its own counter/transfer point;
- immediate controlled back-of-house connection to sanitation/inspection;
- public users cannot carry returns through the clean locker hall;
- later D1 temporary quality-hold instructions can visibly modify this zone.

### E. Return sanitation and inspection

Purpose:

- wash/inspect returned containers;
- separate normal reusable material from suspicious or failed batches.

Requirements:

- cleanable surfaces;
- wash/cauldron/plumbing fixtures;
- visual inspection bench;
- dirty-in / clean-out logic;
- close adjacency to return intake, quality hold, and returned-crate consolidation.

### F. Local quality-hold bay

Purpose:

- isolate one questionable batch or return stream while the rest of the depot keeps operating.

Requirements:

- small and controlled, not apocalyptic;
- physically connected to return inspection rather than appearing as an arbitrary hazard cage;
- temporary D1 overlays must remain distinguishable from permanent VCF architecture;
- preserve player readability in D3.

### G. Receiving / batch and temperature check

Purpose:

- accept clean inbound culture shipments;
- verify records, container condition, and temperature before stock enters clean holding.

Requirements:

- rear/service-side access;
- pallet/crate staging;
- inspection/check station immediately inside the receiving route;
- no freight path through the public lobby.

### H. Clean cold holding / stock

Purpose:

- hold incoming clean cultures before issue staging.

Requirements:

- separated from returned material;
- near receiving and issue lockers;
- tied to refrigeration plant;
- staff-only controlled access.

### I. Clean packing / issue staging

Purpose:

- assemble or stage orders between cold stock and the public issue counter.

Requirements:

- counter/depot/work surface cluster;
- short route to issue;
- does not share a bench with dirty returns.

### J. Returned-crate consolidation

Purpose:

- collect inspected reusable containers/crates before backhaul.

Requirements:

- near sanitation and rear service dispatch;
- separate from clean stock;
- pallet/crate geometry must explain actual reverse logistics.

### K. Rear service dispatch / dock

Purpose:

- inbound delivery and outbound return backhaul.

Requirements:

- visually distinct service elevation;
- freight-width opening or dock treatment;
- clear exterior apron/staging relationship;
- no need to imitate a giant warehouse dock; this is neighborhood scale.

### L. Supervisor / batch-record station

Purpose:

- inventory and batch records;
- incident/quality documentation;
- local dispatch/communications oversight;
- deterministic quest evidence location.

Requirements:

- adjacent to or overlooking service operations;
- secure enough that records placement feels deliberate;
- houses or directly controls the guaranteed `kubejs:vcf_culture_service_manifest` and supporting `kubejs:vcf_return_crate_log` loot path.

### M. Refrigeration / electrical / maintenance support

Purpose:

- keep cold-chain service operating;
- give the roof/service equipment a real reason to exist.

Requirements:

- visible roof plant or protected mechanical mass;
- serviceable route from back-of-house, not customer circulation;
- plausible vertical relationship to cold holding/lockers;
- later decay can damage this system without making D0 irrational.

### N. Minimal staff support

A compact staff washroom, locker nook, cleaning cupboard, or break alcove is desirable if space permits. These are subordinate to the operational program but prevent the building from feeling like a machine with no workers.

## Required circulation systems

### Public route

`primary entrance -> vestibule / information -> issue queue OR return counter -> exit`

The public route must remain short, calm and obvious.

### Staff route

`staff/service entry -> supervisor/records -> receiving / cold holding / issue support / return sanitation -> service dispatch`

Staff may cross controlled handoff points but should not repeatedly walk through customer space to do routine work.

### Freight route

`rear service apron -> receiving -> batch check -> clean stock`

and

`return consolidation -> rear service dispatch -> vehicle/backhaul`

Freight does not cross the public queue.

### Dirty-return route

`return counter -> sanitation/inspection -> quality decision -> consolidation or hold`

This route must never require transit through clean cold holding or clean issue staging.

## Functional hero space

OWS-001 is a common neighborhood site, so its hero space should not be monumentally oversized.

The intended memorable interior is the **culture-locker / issue interface**: a repeated cold-storage wall or bank visible from the controlled public service zone, with staff circulation and mechanical support making the operation legible.

The intended narrative secondary space is **return sanitation + quality hold**, where the player can understand how a mundane service process first exposed the material anomaly.

## Functional rejection conditions

Pass 2 fails if later design work does any of the following:

- turns the site back into retail browsing;
- routes returns through clean stock;
- places sanitation far from return intake;
- places receiving at the public facade without a compelling reason;
- creates refrigerated blocks with no service access or plant relationship;
- creates an office/evidence room unrelated to operations;
- treats quality hold as generalized disaster containment;
- omits a meaningful rear service route;
- requires customers to enter staff-only spaces to understand where to go.

## Pass 2 result

**Functional definition: COMPLETE.**

The building program is now sufficiently specific to begin real-world precedent revalidation and adjacency design. No massing changes are authorized until those passes are complete.
