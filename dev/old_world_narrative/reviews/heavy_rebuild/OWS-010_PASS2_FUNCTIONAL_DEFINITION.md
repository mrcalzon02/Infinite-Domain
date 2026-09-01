# [SYSTEM REPORT] OWS-010 Pass 2 — Functional Definition

**Target:** OWS-010 — Atlas Conveyor Transfer Hall  
**Institution:** Atlas Kinetic Industries  
**Narrative phase:** Pre-crisis to early anomaly  
**Status:** COMPLETE

## Actual institutional purpose

OWS-010 is a **regional industrial cross-dock and automated transfer hall**. It receives mixed crates, packaged components and machine assemblies from road vehicles, identifies and meters them into four parallel transfer lanes, routes conforming loads through a common destination trunk, diverts exceptions to manual rework, and accumulates sorted loads for outbound dispatch.

It is not a long-term warehouse, a parcel-post megahub or an assembly factory. Storage is short-duration buffering around a continuous transfer process. The player should recognize Create-like mechanical principles at an institutional scale: induction, metering, transfer, routing, inspection, rework, output and maintainable drives.

The central operating question is:

> How did Atlas move mixed industrial loads through one compact road hub while keeping every lane reachable, isolatable and replaceable?

## Primary operating workflow

The normal material chain is:

`inbound docks 01–02 -> receiving buffer -> identification / size check -> metered induction -> four parallel transfer lanes -> destination cross-transfer trunk -> outbound accumulation -> docks 03–04`

Exceptions follow a separate loop:

`identification reject or lane fault -> manual exception spur -> inspection / rework -> re-induction or controlled hold`

Maintenance follows a parallel chain:

`east service entry -> parts issue -> lockout desk -> guarded drive/service trench -> lane isolation point -> overhead maintenance catwalk -> control room / maintenance records`

No normal freight route may pass through the office annex, control room, proof-records node or parts issue. Operators need guarded crossing points rather than walking on conveyors or squeezing between drive casings.

## Four transfer lanes

The four lanes share a structural and control rhythm but require distinct operational identities:

1. **Lane 01 — standard crates:** primary-volume line for regular pallet/crate loads.
2. **Lane 02 — packaged components:** closer metering and inspection for smaller mixed consignments.
3. **Lane 03 — machine assemblies:** slower line with heavier transfer points and wider service clearance.
4. **Lane 04 — overflow / exception-capable line:** a full normal-operation lane whose later partial cannibalization keeps Lanes 01–03 running.

Each lane requires:

- an input buffer or depot;
- a visible directional belt/transfer run;
- one readable drive/gearbox cluster connected to the run;
- an inspection or routing decision point;
- an output merge into the cross-transfer trunk;
- a local stop/lockout station;
- reachable side or below-grade service clearance;
- lane numbering readable from both operator floor and catwalk.

The four modules cannot be represented by repeated colored strips with isolated presses. Their shared feeds, different load functions and common output must be physically continuous.

## Required functional zones

### South truck court and receiving/dispatch

- four retained dock portals under Atlas-orange lane crowns;
- Docks 01–02 visibly coded inbound and Docks 03–04 outbound;
- sheltered dock controls, bumpers and clear freight thresholds;
- inbound checking and temporary receiving buffer immediately inside Docks 01–02;
- outbound accumulation sized to avoid blocking the transfer lanes;
- truck-court markings that keep vehicle maneuvering separate from the east maintenance entry.

### Induction and exception handling

- a transverse inbound conveyor/crossfeed serving all four lanes;
- identification, size/weight check and controlled metering before induction;
- manual exception spur for unreadable, oversized or damaged loads;
- inspection/rework bench, short controlled hold and re-induction point;
- operator station with sightlines to induction and the first lane transfer points.

### Transfer hall

- four parallel north-south lane modules;
- a protected operator gallery and at least one guarded cross aisle;
- common north destination cross-transfer trunk;
- an east-side outbound return/drop route connecting the trunk to Docks 03–04;
- visible structural bays and roof/truss rhythm aligned with machinery rather than donor racks;
- no long-term pallet-rack forest occupying the process floor.

### Maintenance and parts

- separate east service entrance;
- parts issue adjacent to, but outside, the freight path;
- lockout/tag station at each lane and a master isolation point;
- continuous guarded service trench or depressed drive gallery;
- two-block-clear maintenance catwalk with real stair and landings;
- accessible motors, shafts, casings and replacement modules;
- repair bench and staged critical spares close to Lane 04.

### Control, quality and records

- elevated control room overlooking induction, all four lanes and the cross-transfer trunk;
- quality/throughput desk receiving scan and lane-status information;
- dispatch/yard coordination linked to both dock banks;
- maintenance records room reached from staff/control circulation, not the freight floor;
- exactly one canonical proof node for `kubejs:atlas_transfer_maintenance_card`.

### Staff support and building services

- north staff/security threshold and small briefing/dispatch office;
- lockers, washroom and break support in the retained two-level annex;
- electrical/control plant connected to the drives;
- ventilation/heat-relief roof plant over the process hall;
- transformer/service yard at the east edge;
- independent emergency egress from hall and annex.

## People, material and information flows

- **Inbound freight:** south Docks 01–02 -> receive/check -> induction -> assigned lane.
- **Outbound freight:** cross-transfer trunk -> east return/drop -> accumulation -> south Docks 03–04.
- **Exception load:** check or lane reject -> west/manual spur -> inspect/rework -> re-induct or hold.
- **Operators:** north staff threshold -> lockers/briefing -> guarded operator gallery -> crossings/control positions -> exit.
- **Maintenance:** east service threshold -> parts/lockout -> trench/catwalk/lane drives -> records/control; no route through outbound staging.
- **Information:** scan and lane sensors -> floor operator stations -> elevated control/quality room -> maintenance records and dispatch.
- **Player:** staff/security entry -> overview -> operator gallery -> guarded cross aisle -> Lane 04 maintenance route -> control/records -> canonical proof.

## Institutional and historical identity

Atlas identity is maintainable heavy-industrial precision rather than orange paint. Black/charcoal machine frames, orange operational structure, steel service routes and yellow lockout zones must make replacement, calibration and safe access obvious. Full `ATLAS KINETIC INDUSTRIES` identity belongs at the truck court and north staff threshold; functional labels belong at docks, lanes, lockout stations, parts issue, rework and outbound.

The early-anomaly layer remains restrained. Lane 04 is still recognizable as a complete original lane, but selected drive casings, guard sections and spare modules have been removed and staged to sustain Lanes 01–03. Its lockout and work order are deliberate; the rest of the hall remains orderly and functional.

## Proof and LOR-006 integration constraint

- canonical proof: `kubejs:atlas_transfer_maintenance_card`;
- canonical loot table: `infinite_domain:chests/old_world/ows_010_atlas_conveyor_transfer_hall`;
- the proof belongs in the maintenance records/control suite after the player has read the four-lane system;
- it remains deterministic, accessible and independent of combat or optional destruction;
- current structure metadata declares `lore_record: null` and current OWS-010 loot guarantees only the proof card;
- although lore seed `LOR-006` declares placement at OWS-010, the live investigation quest currently obtains `kubejs:atlas_transfer_maintenance_manual` from OWS-009;
- therefore the target may reserve a non-loot manual/records shelf beside the proof node, but it must not duplicate, move or newly serialize LOR-006 without a coordinator-owned shared integration decision.

## Functional acceptance test

Before Gate B can pass, architecture alone must let a reviewer reconstruct:

`which docks receive -> how loads are checked and metered -> why four lanes differ -> where rejected loads go -> how output reaches dispatch -> how operators cross safely -> how technicians isolate and reach every drive -> why Lane 04 is being cannibalized -> where maintenance proof is secured.`

If that chain depends mainly on orange stripes, signs or isolated Create props, the facility is incomplete.

**FUNCTIONAL DEFINITION: COMPLETE.**
