# Infinite Domain — Post-Calamity Blueprint Phase 1

Parent authority: `docs/POST_CALAMITY_EVENT_STRUCTURES_PLAN.md`

Status: **blueprint authoring active / implementation not yet promoted to worldgen**

This file converts the first production families into buildable specifications. These are blueprint contracts for later schematic/NBT authoring and Heavy Rebuild execution. They do not yet claim active structures.

## Shared blueprint rules

Every blueprint must preserve the original human purpose before damage and Spore growth are added. Vehicle lines must follow roadway geometry. Camp functions must have entrances, circulation, aid/medical areas and sanitation/logistics. Farm damage must follow plausible fire, collapse and abandonment patterns.

Each large blueprint should support at least three damage/contamination states:
- **A — emergency/failing:** human organization still readable, limited fungal breach;
- **B — overrun:** control lost, heavy damage, active biomass spread;
- **C — reclaimed:** structure remains readable but fungal material dominates.

Where the structure joins Lost Cities, connector dimensions and road elevation must be parameterized rather than hard-coded until the installed Lost Cities profile is inspected.

# PCE-003 — Intercity Highway Collapse Family

## PCE-003-A — Stalled Evacuation Artery
Target footprint: **48–64 blocks long × 24–32 wide**.
Purpose: multilane civilian evacuation queue that stopped permanently.
Required modules:
- two directional carriageways with median/barrier logic;
- 12–24 vehicle silhouettes in staggered stopped positions;
- one bus or evacuation coach;
- one emergency/service vehicle;
- abandoned luggage/supply scatter;
- one shoulder triage or breakdown area;
- fungus beginning in drainage/underbody zones and spreading into vehicle cabins at higher damage states.
Damage variants:
- A: largely intact traffic line with isolated abandonment;
- B: several collisions, burned vehicles, emergency lane blocked;
- C: biomass connects multiple vehicles into one continuous fungal mass.
Loot/evidence: ration remnants, evacuation paperwork, small medical salvage, personal evidence, no advanced machines.
Connector requirement: flat road-edge interfaces at both ends for Lost Cities adjacency.

## PCE-003-B — Jackknifed Freight Burn
Target footprint: **40–56 × 24–30**.
Purpose: freight truck collision that triggered fuel/cargo fire and blocked evacuation.
Required modules:
- tractor/trailer diagonal across lanes;
- spilled cargo field;
- scorched pavement and barrier damage;
- 4–8 secondary vehicle impacts;
- burned emergency-response position;
- fungus exploiting cargo, drainage and corpse/organic accumulation.
Variant hook: chemical/food/industrial cargo themes may alter environmental storytelling but must not create hazardous real-world chemistry instructions.
Primary narrative: logistics failure becomes a physical roadblock.

## PCE-003-C — Quarantine Checkpoint Collapse
Target footprint: **48–64 × 28–36**.
Purpose: military/civic checkpoint that transitioned from controlled screening to total failure.
Required modules:
- lane chicanes and concrete barriers;
- inspection tents or booths;
- decontamination lane;
- command trailer;
- fenced holding area;
- at least one breached perimeter;
- abandoned emergency vehicles;
- final-defense firing/observation positions;
- Spore breach concentrated first in holding/medical areas, then spreading through the lane system.
Evidence: checkpoint orders, screening records, failed evacuation routing, limited ammunition only if progression-compatible.

## PCE-003-D — Collapsed Overpass Evacuation
Target footprint: **48–72 × 36–48**, vertical range **12–24**.
Purpose: failed grade-separated evacuation route.
Required modules:
- lower road;
- partial upper deck;
- broken support/abutment;
- vehicle fall/collision scene;
- hanging barrier and fractured pavement;
- blocked alternate route;
- fungal growth rising from the shadowed lower crash field into the collapsed deck.
Heavy Rebuild emphasis: load paths and collapse geometry must be structurally readable rather than random missing blocks.

# PCE-002 — Overrun Refugee Camp Family

## PCE-002-A — Organized Emergency Camp
Target footprint: **48–64 square**.
Purpose: functioning but overcrowded temporary civilian camp shortly before systemic failure.
Zones:
- controlled entrance;
- registration/intake;
- 12–20 shelter/tent pads;
- field kitchen/ration line;
- water point;
- medical/triage;
- generator/lighting;
- sanitation edge;
- small body-collection area;
- perimeter barriers.
Spore state: early contamination only, focused near drainage, medical waste or body handling.
Use: establishes what later overrun variants used to look like.

## PCE-002-B — Triage Collapse Camp
Target footprint: **48–64 square**.
Purpose: same functional camp archetype after casualty load exceeds medical capacity.
Required changes:
- expanded triage;
- overflow cots;
- disrupted ration/water logistics;
- abandoned treatment equipment;
- improvised barricades inside the camp;
- first large biomass breach near medical/body zones.
Narrative: institutional failure before complete military collapse.

## PCE-002-C — Final-Defense Refugee Camp
Target footprint: **56–72 square**.
Purpose: camp converted into a defensive enclave.
Required modules:
- reinforced perimeter;
- blocked vehicle entrances;
- improvised firing/observation positions;
- emergency supply consolidation;
- burned outer shelter line;
- breached sector with concentrated Spore creatures/biomass;
- evacuation route that visibly failed.
Loot: survival remnants and evidence; no intact late-era fabrication equipment.

## PCE-002-D — Biomass-Reclaimed Camp
Target footprint: **48–64 square**.
Purpose: late-stage aftermath where camp functions remain barely readable beneath fungal reclamation.
Required language:
- tent/shelter frames protruding through biomass;
- collapsed fencing embedded in growth;
- medical area transformed into dense fungal focus;
- body/disposal zone merged into biomass;
- generator or lighting remnants partially swallowed;
- minimal intact supplies.
This should be one of the strongest ordinary Spore-overrun scenes short of mass-grave/crater sites.

# PCE-005 — Burned Farmstead Family

## PCE-005-A — Quarantine-Burn Farmhouse
Target footprint: **32–48 × 32–48**.
Purpose: inhabited farm deliberately burned or partially burned during containment.
Required modules:
- recognizable farmhouse;
- porch/mudroom;
- well or water point;
- small equipment shed;
- firebreak or burned field edge;
- emergency burn evidence;
- fungal regrowth from cellar, well/drainage or unburned organic areas.
Damage must distinguish intentional containment burning from ordinary age decay.

## PCE-005-B — Barn and Livestock Overrun
Target footprint: **40–56 × 40–56**.
Purpose: livestock/agricultural barn overwhelmed before or during evacuation.
Required modules:
- main barn volume;
- stalls/pens;
- feed/hay storage;
- loading access;
- machinery/equipment corner;
- breached livestock enclosure;
- concentrated biomass in feed/manure/organic zones;
- partial roof collapse.
Narrative: agricultural biological load accelerates fungal takeover.

## PCE-005-C — Silo and Machinery Collapse
Target footprint: **36–52 × 36–52**, vertical range **18–32**.
Purpose: grain/storage and machinery complex damaged by fire, blast or abandonment.
Required modules:
- one or more silo forms;
- loading auger/conveyor interpretation;
- machine shed;
- truck/loading apron;
- spilled crop/material field;
- fungal growth climbing storage structures and filling low points.
Heavy Rebuild emphasis: believable agricultural process flow.

## PCE-005-D — Rural Quarantine Checkpoint
Target footprint: **32–48 × 24–36**.
Purpose: improvised road/farm-lane control point attempting to isolate rural infection.
Required modules:
- road barrier;
- inspection shelter;
- burned vehicle or equipment;
- field-edge fence;
- contaminated ditch/drainage;
- small evidence cache;
- one breached side route.
This blueprint doubles as a reusable transition microstructure between rural collapse sites.

# Phase 1 implementation order

1. PCE-003-A Stalled Evacuation Artery
2. PCE-003-C Quarantine Checkpoint Collapse
3. PCE-002-A Organized Emergency Camp
4. PCE-002-C Final-Defense Refugee Camp
5. PCE-005-A Quarantine-Burn Farmhouse
6. PCE-005-B Barn and Livestock Overrun
7. remaining Phase 1 variants

The first six should establish the structural language before mass-producing variants.

# Promotion gate

Before any Phase 1 blueprint enters natural worldgen:
- establish its stable `infinite_domain` structure ID;
- create at least one pack-owned NBT/schematic;
- assign appropriate biome/road context;
- attach progression-safe loot/evidence;
- define Spore stage and encounter pressure;
- run Heavy Rebuild visual review;
- only then add structure-set density.

Runtime validation may be deferred when unavailable, but the deferral must be recorded rather than reported as a pass.
