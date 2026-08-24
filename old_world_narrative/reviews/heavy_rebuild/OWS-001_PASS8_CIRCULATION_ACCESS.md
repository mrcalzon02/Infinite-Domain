# OWS-001 Pass 8 — Circulation and Access

## Scope

Gate A approved the r2 macro shell. Pass 8 assigns **actual circulation geometry** inside it before detailed exterior/interior furnishing begins.

The core rule is operational separation:

- customers should understand where to go immediately;
- clean cultures should never need to pass through dirty-return processing;
- returned material should not cross clean stock;
- freight should not cross the public queue;
- staff should be able to move between work zones without repeatedly entering public space;
- maintenance staff need a plausible route to roof/mechanical equipment.

## Coordinate convention

- front/public: low Z
- rear/service: high Z
- west/left: return/sanitation side
- east/right: clean cold-chain side

The exact coordinates below are working design coordinates for the D0 intact review model. Minor one-block adjustments are allowed during implementation if they improve structural alignment without changing the circulation logic.

## Public route

### Primary entry

Target entrance:

- double door centered approximately X 18–19, Z 3
- front pavilion vestibule roughly X 15–23, Z 4–7

The vestibule should immediately reveal two customer choices:

- **RETURN CULTURES** to the west/left;
- **CULTURE ISSUE** to the east/right.

The customer should never need to infer that one of those functions is hidden behind the other.

### Public queue / information spine

Target clear zone:

- roughly X 15–23, Z 5–9
- minimum 3-block usable center aisle where possible

Functions:

- entry/information;
- short issue queue;
- visual access to service counters;
- no direct access into cold stock, sanitation, freight, or records.

### Issue counter

Target:

- east half of pavilion/rear threshold, approximately X 20–24, Z 9–11

Relationship:

`public queue -> issue counter -> staff-side issue staging -> cold locker/service zone`

The public stops at the counter. Clean cultures move forward from staff space.

### Return counter

Target:

- west half, approximately X 13–17, Z 9–11

Relationship:

`public return -> return counter -> contained staff-side transfer -> west return-processing route`

Returned containers/material never travel through the public queue after handoff.

## Staff circulation spine

The principal staff route should run behind the public counters and connect the entire operational building.

Proposed spine:

- east-west handoff corridor immediately behind issue/return service: approximately Z 11–13;
- north-south operational spine through center/rear: approximately X 17–20, Z 12–27;

Target width:

- 2 blocks minimum;
- 3 blocks through the busiest central segment where possible.

This spine connects:

- issue support;
- cold locker hall;
- clean stock;
- receiving/batch check;
- supervisor/records;
- sanitation branch;
- return-crate consolidation;
- rear dispatch.

It should read as a workplace route through connected operational rooms, not a long dungeon hallway.

## Clean product route

### Receiving

Rear freight opening:

- approximately X 17–20, Z 31

Receiving staging:

- roughly X 14–21, Z 25–30

The clean inbound path begins here.

### Batch / temperature check

Immediately inside receiving:

- target X 17–22, Z 24–27

This is the decision point before product enters clean storage.

### Clean cold holding

Target cluster:

- east/rear process and cold block, approximately X 24–33, Z 18–25

Access:

- staff-only from batch check and staff spine;
- no customer route through it;
- no dirty-return route through it.

### Issue staging and locker service

Target:

- east/front workplace, approximately X 21–31, Z 11–19

Flow:

`clean hold -> issue staging -> locker/service aisle -> issue counter`

A customer-facing pickup/locker face may be visible from public space, but staff/service access remains behind or beside it.

## Dirty-return route

### Transfer from return counter

Return handoff should enter west processing directly behind the counter:

- approximately X 10–16, Z 10–14

A controlled door/opening carries staff/material toward sanitation.

### Sanitation / inspection

Target:

- west annex center, approximately X 4–11, Z 14–20

Dirty-in and cleaned/accepted-out movement should be perceptible within the room.

### Quality decision split

After inspection:

**normal accepted return** -> return-crate consolidation

or

**questionable batch** -> quality-hold bay.

The split should occur at the rear side of sanitation, not at the public counter.

### Quality hold

Target:

- west/rear annex, approximately X 4–11, Z 20–24

D0 state:

- normal permanent controlled room;
- not yet covered in emergency yellow markings.

D1 later:

- temporary signage/markings isolate one problematic batch/equipment segment while normal service continues.

### Returned-crate consolidation

Target:

- west/rear process area, approximately X 10–16, Z 21–27

Flow:

`sanitation accepted output -> reusable crates/pallets -> rear dispatch`

It remains separated from clean cold holding.

## Freight circulation

### Exterior approach

Rear high-Z apron remains the only routine freight face.

### Inbound

`rear apron -> freight opening -> receiving -> check -> clean holding`

### Outbound/backhaul

`returned-crate consolidation -> rear dispatch staging -> freight opening -> rear apron`

Inbound and outbound can share the same neighborhood-scale dock because volumes are modest, but internal staging positions must remain distinguishable.

## Supervisor / records access

Target lower rear/east bump-out:

- approximately X 25–32, Z 25–29

Access:

- staff route only;
- directly adjacent to receiving/batch-check decisions;
- reasonable sightline or short route to stock and dispatch;
- evidence storage/workstation belongs here.

The office should not require a player to traverse an arbitrary maze to find the proof item. Its narrative importance comes from logical placement.

## Maintenance and roof access

### Building mechanical access

Preferred route:

`rear service side -> cold-chain service zone -> vertical maintenance access -> roof plant`

A ladder/stair/service-hatch solution may be used, but it must:

- stay out of public circulation;
- emerge near the roof equipment service spine;
- not require walking through quality hold;
- remain visually plausible from the intact-state review.

### East service access

The Gate-A east-side service frame/opening may become a controlled refrigeration-maintenance door if it improves the route.

This creates a second service option without turning the east side into a public entrance.

## Door and threshold hierarchy

### Public

- front double door: obvious primary entrance;
- counters form controlled handoffs rather than doors into back-of-house.

### Staff

- one controlled door behind issue/return transition;
- staff doors between return processing, clean operations, records, and rear service as needed;
- doors should align to actual partitions and structural bays.

### Freight

- rear loading opening: 3–4 blocks wide;
- not a standard personnel door;
- service frame/canopy already approved in massing.

### Controlled biological zones

- sanitation: staff-controlled threshold;
- quality hold: enclosed controlled threshold;
- clean cold hold: staff-only threshold;
- records: staff-only/secure threshold.

## Player exploration route in D3

The final ruin may break or open some original barriers, but the D0 design must first be coherent.

Later D3 exploration should preserve at least two understandable ways through the building:

1. public approach into the issue/return interface and onward into work zones;
2. service/rear approach into receiving and operations.

The quest evidence path should reward understanding the operational structure rather than requiring arbitrary wall-breaking.

## Accessibility / gameplay clearances

- principal routes: target 2–3 blocks wide;
- public queue: 3 blocks where possible;
- work aisles around cold equipment: 2–3 blocks;
- doors: standard 1–2 block width as function requires;
- freight bay: 3–4 blocks;
- avoid one-block choke corridors except at intentionally controlled small doors;
- no essential evidence behind geometry that becomes impossible to traverse after damage.

## Circulation rejection conditions

Pass 8 fails if:

- return material crosses clean cold stock;
- customers can walk directly into receiving or sanitation;
- freight crosses the public vestibule;
- the staff spine degenerates into a narrow maze;
- the evidence room is disconnected from the operational decision points it documents;
- maintenance access to rooftop refrigeration has no plausible route;
- a side/rear exterior door opens into a room unrelated to its visible facade treatment;
- later D3 would require destroying major architecture just to reach mandatory proof.

## Pass 8 result

**CIRCULATION AND ACCESS: DEFINED.**

The next pass can develop the exterior architecture against these room/circulation responsibilities. Windows, doors, facade depth, loading treatment and VCF identity must correspond to real spaces behind them rather than being decorative surface patterns.
