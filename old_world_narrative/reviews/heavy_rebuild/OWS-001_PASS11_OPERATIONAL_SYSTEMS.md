# OWS-001 Pass 11 — Operational Systems

## Intent

Operational systems must prove that the rooms defined in Pass 10 actually perform the facility's work.

Props and machinery are not decoration. Every cluster should answer one of these questions:

- where does clean product arrive?
- where is it checked?
- where is it kept cold?
- how is it staged for issue?
- where do customers receive it?
- where do returns enter?
- where are returns washed and inspected?
- where do accepted containers accumulate for backhaul?
- where does questionable material wait?
- what keeps the cold chain operating?
- where are batch decisions recorded?

## Public service systems

### Culture issue stations

Target 2–3 stations along the issue counter.

Use:

- durable counters/work surfaces;
- one or more `create:depot`-style handoff/staging points where they read correctly;
- clean crate/package staging behind staff;
- no supermarket checkout belts.

The counter should read as controlled dispensing/account service rather than retail purchase.

### Return handoff

Use a physically separate counter and one contained transfer position.

Returned material moves immediately toward the west return-processing route.

Do not mirror the issue counter exactly; the functions are related but operationally different.

## Culture-locker / cold-bank hero system

Use repeated `oritech:cooler_block` or equivalent stable cold-storage blocks in deliberate banks.

Target layout:

- 3–4 locker/freezer banks;
- repeated modules rather than random isolated coolers;
- 2–3 block staff aisles;
- one service edge/backside;
- issue staging connected to the public counter;
- clean holding connected toward the rear/east.

The equipment must read as standardized VCF infrastructure.

## Receiving / batch check

Immediately inside the freight bay:

- pallet/crate staging positions;
- one inspection/check workstation;
- one communications/records aid where useful;
- clear route from freight opening to the inspection point;
- clear route onward to clean storage only after that point.

Suitable vocabulary may include:

- `immersiveengineering:crate`;
- `jaffabricate:pallet_full` where already supported;
- `create:depot` as inspection/work handoff;
- counter/workbench blocks already used elsewhere in the pack;
- a radio/records device where appropriate.

Avoid arbitrary laboratory apparatus.

## Clean cold holding

Use denser cold-storage geometry than the issue-facing lockers.

Required relationship:

- batch check -> clean cold hold -> issue/locker service.

Clean stock should be visually distinct from returned crates through room placement, container type/orientation, and signage—not merely color.

## Sanitation / inspection system

The return room should include a complete compact wash/inspection cluster:

- two wash points or equivalent;
- visible `create:fluid_pipe` supply/service run;
- `minecraft:water_cauldron` or another stable wash-fixture representation;
- inspection/work counter;
- one incoming returned-crate position;
- one accepted/cleaned outbound position.

The wash fixtures should sit where water/service routing can plausibly reach them from a utility wall or floor/ceiling run.

## Quality-hold system — D0

D0 quality hold is a normal contingency space.

Use:

- one controlled rack/crate area;
- sparse capacity rather than a packed disaster zone;
- normal professional permanent signage only;
- no emergency yellow field yet.

D1 will later add the specific problematic batch, temporary isolation markings, and revised operating procedure.

## Returned-crate consolidation

Use:

- repeated returned crate stacks;
- at least one pallet position;
- enough clear floor for staff movement;
- direct route to rear dispatch.

This area should look like reverse logistics rather than stock awaiting sale.

## Supervisor / batch-record station

Required operational elements:

- work counter/desk;
- records storage/bookshelf or equivalent;
- radio/communications point;
- view or short route to receiving;
- space reserved for the deterministic evidence container in the final authoritative build.

The eventual proof item remains:

- `kubejs:vcf_culture_service_manifest`

Supporting record:

- `kubejs:vcf_return_crate_log`

The review-stage D0 model may use a placeholder chest only if the review is clearly marked non-authoritative. The final authoritative builder must use the existing deterministic loot table.

## Cold-chain rooftop plant

Gate-A r2 accepted four separated equipment masses. Pass 11 turns those masses into an operational system.

Required visible logic:

- multiple refrigeration/cooling units rather than one generic HVAC box;
- `oritech:cooler_block` or equivalent equipment faces where useful;
- `create:fluid_pipe` or similarly stable service runs connecting units/roof penetrations;
- maintenance walkway/spine preserved;
- service gaps around equipment;
- partial steel/support frames retained;
- at least one vertical service path toward the east cold-chain zone;
- access from a staff/service route, ladder/stair/hatch representation as appropriate.

Do not create a fully simulated Create machine unless its block behavior is stable in generated structures. Spatial plausibility matters more than pretending every pipe is live.

## Electrical / lighting system

### Public pavilion

- regular calm ceiling lighting;
- no industrial clutter hanging over customers.

### Locker / clean service zone

- brighter repeated lighting aligned to equipment aisles;
- service runs organized rather than random.

### Sanitation / receiving

- utilitarian lighting;
- brighter inspection/work positions;
- service conduit/pipe may be visible.

Lighting fixtures should repeat with bay rhythm instead of being scattered randomly.

## Fire / safety / maintenance cues

Without over-detailing, D0 may reserve positions for:

- maintenance cupboard;
- cleaning supplies;
- controlled service shutoff/utility point;
- handling instructions;
- staff-only access marker.

These reinforce professional operation but should not dominate a common site.

## Operational rejection conditions

Pass 11 fails if:

- cooler blocks are placed as decoration with no aisle/service relationship;
- receiving stock bypasses batch inspection;
- dirty-return fixtures share clean issue work surfaces;
- sanitation has wash fixtures but no supply/service logic;
- returned crates accumulate far from rear dispatch;
- rooftop equipment cannot plausibly support cold spaces below;
- records/evidence station has no operational relationship to receiving/stock decisions;
- machinery density makes the building look like a factory rather than a neighborhood service depot;
- props block the 2–3 block circulation clearances defined earlier.

## Pass 11 result

**OPERATIONAL SYSTEMS: DEFINED FOR D0.**

The next pass applies Verdant Continuum Foods institutional identity through architecture, signage, wayfinding, material hierarchy and staff/customer messaging. Identity must explain the operation; it may not substitute for it.
