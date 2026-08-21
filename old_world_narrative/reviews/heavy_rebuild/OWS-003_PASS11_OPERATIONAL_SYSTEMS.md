# [SYSTEM REPORT] OWS-003 Pass 11 — Operational Systems

**Target:** OWS-003 — Verdant Continuum Foods Cold-Chain Culture Nursery  
**Status:** COMPLETE

## Operational objective

The facility must visibly function as a biological cold-chain node. Equipment density should be high enough that the player can reconstruct refrigeration, batch handling and distribution, but every system must explain a real workflow.

## Refrigerated storage system

Primary block vocabulary:

- `oritech:cooler_block` for repeated cold-storage equipment;
- white/light-gray insulated shells around cold rooms;
- framed glass only at monitoring/inspection interfaces;
- crates/pallets for handled culture loads.

Gate B should contain substantially more refrigerated evidence than the legacy 11-fixture overlay.

Target:

- multiple cooler banks in receiving hold, main vault, nursery cells and outbound staging;
- enough repeated equipment to make refrigeration the building's dominant operation.

## Refrigeration distribution

Use a coherent service network:

- `create:fluid_pipe` as visible refrigeration/service trunk analogue;
- primary roof/east plant headers;
- vertical risers down the technical side;
- branch lines toward vault/nursery groups;
- no random pipe forest.

Pipes should follow structural/service corridors and terminate at served systems.

## Roof plant

Use separated masses such as:

- `immersiveengineering:sheetmetal_steel` equipment bodies;
- `oritech:cooler_block` or other established cooling-related blocks at selected service points;
- steel support/walkway elements;
- service pipes/riser connections;
- access landing.

The five Gate-A equipment masses should become identifiable units rather than remaining undifferentiated gray boxes.

## Receiving/check equipment

Use:

- `create:depot` at inbound inspection/handoff;
- counter/bench blocks for inspection;
- crates and pallets staged beside, not inside, the transfer lane;
- cooler blocks in conditioned receiving hold;
- radio/records point where useful.

## Nursery-cell equipment

Each nursery compartment should contain a coherent subset of:

- cooler blocks;
- shelves/crates/barrels representing sealed culture batches;
- observation glazing;
- local service pipe branch;
- monitoring/control position;
- clear internal access.

Do not turn the nursery into crop-growing rows; OWS-003 stores/stabilizes cultures rather than growing food at scale.

## Quality-hold / seal-repack equipment

D0 normal infrastructure:

- one inspection/repack counter;
- one or more cooler positions keeping suspect stock conditioned;
- sealed crate/barrel positions;
- replacement packaging/seal stock;
- yellow floor/threshold marking limited to the actual hold zone.

D1 later adds increased replacement stock and temporary rerouting, not a new permanent room.

## Release and packing equipment

Release inspection:

- depot/inspection bench;
- batch record/lectern or equivalent;
- small controlled stock positions.

Packing:

- parallel counters/work benches;
- crates/pallets/shipping racks;
- packaging material along walls;
- central route kept clear.

Outbound staging:

- repeated cooler/shipping positions;
- destination rows at sides of clear dispatch lane.

## Batch/licensing records

Use:

- lecterns/bookshelves/records storage;
- supervisor desk/counter;
- radio/communications;
- route/destination board expressed through signs and physical lane relationships.

The guaranteed evidence chest should ultimately sit here or immediately adjacent.

## Lighting

Lighting should correspond to use:

- brighter clean lighting at intake, inspection, records and packing;
- repeated aisle lighting in cold vault/nursery service corridors;
- industrial/service lighting in maintenance/plant areas.

Avoid uniform light grids unrelated to room geometry.

## Vertical maintenance system

Gate B must include:

- continuous ladder or industrial stair analogue inside the maintenance tower;
- roof landing/trapdoor/door;
- clear plant walkway;
- accessible equipment gaps.

## D0 quality-hold principle

Quality hold exists in normal operation.

Yellow marking at D0 means **ordinary operational exception handling**, not “the apocalypse has begun.”

Historical D1 will later add temporary signs, more suspect stock and rerouted batches.

## Operational density guards for Gate B

The intact renderer should enforce minimum evidence such as:

- substantial cooler count across multiple zones;
- substantial connected service-pipe count;
- multiple crates/pallet groups at real handoff points;
- purposeful signage count;
- working receiving, internal controlled and dispatch thresholds;
- nonzero vertical-access span in final production metrics once authoritative.

Exact thresholds belong in executable assertions, not only this document.

## Pass 11 decision

**OPERATIONAL SYSTEMS: COMPLETE.**

Gate B must prove the plant, refrigerated rooms, receiving/check, quality hold, release/packing, records and maintenance systems as one continuous operating facility.