# Infinite Domain — Post-Calamity Blueprint Phase 2

Parent authority: `docs/POST_CALAMITY_EVENT_STRUCTURES_PLAN.md`

Status: **blueprint authoring active / implementation not yet promoted to worldgen**

Phase 2 defines the high-impact catastrophe structures that explain the terminal collapse itself: blast/containment craters, mass-casualty disposal systems, destroyed urban blocks, and the microstructure vocabulary that makes the final conflict visible between major landmarks.

Exact Spore block/entity registry IDs must be inspected from the installed mod before implementation. The blueprint language below defines function, morphology, encounter pressure, and contamination state without inventing registry names.

## Shared Phase 2 rules

- Damage must have an interpretable cause: blast pressure, fire, structural collapse, deliberate demolition, vehicle impact, excavation, containment burning, or biological overrun.
- Spore growth follows plausible pathways such as drainage, bodies/organic material, basements, ventilation, buried waste, cracked containment and low wet ground.
- A structure must remain recognizable enough that a player can infer its pre-collapse purpose.
- Major sites should include at least one evidence position and one progression-safe salvage position.
- Stage D biomass-reclaimed versions may be visually extreme, but should still retain structural clues.
- No blueprint is promoted to natural worldgen before its exact structure ID, NBT/schematic, loot contract, Spore state and Heavy Rebuild review exist.

# PCE-001 — Fungal-Choked Catastrophe Craters

## PCE-001-A — Containment Demolition Crater
Target footprint: **48–72 blocks diameter**, depth **8–18**.
Purpose: a deliberate final-conflict demolition intended to destroy an infected facility or block a transmission corridor.

Required features:
- asymmetrical crater bowl rather than a perfect circle;
- recognizable fragments of the destroyed facility at the rim and within the ejecta field;
- broken road, utility conduit or perimeter fencing proving the crater cut through a functioning site;
- scorched inner ring and collapsed outer debris;
- surviving warning/checkpoint fragments;
- fungal growth concentrated in protected cracks and crater-low points before spreading outward;
- one evidence cache suggesting an intentional containment action without forcing a single universal explanation for all craters.

Damage states:
- A: recent demolition, sparse contamination, readable blast perimeter;
- B: water/debris accumulation and expanding Spore colonies;
- C: crater floor becoming a connected biomass basin.

## PCE-001-B — Industrial Secondary-Explosion Crater
Target footprint: **40–64 diameter**, depth **6–14**.
Purpose: fuel, ammunition, pressure-vessel, industrial-storage or infrastructure failure during the evacuation period.

Required features:
- partial industrial slab or yard around one side of the crater;
- pipe/conduit fragments terminating at the blast zone;
- collapsed storage or service structure;
- thrown freight/equipment silhouettes;
- scorched vehicle or service access;
- drainage channel feeding contamination into the crater;
- fungus exploiting buried cargo and organic debris.

Narrative function: distinguish infrastructure collapse from military bombardment and show cascading industrial failure.

## PCE-001-C — Fungal Sink / Biomass Crater
Target footprint: **36–60 diameter**, depth **10–20**.
Purpose: an older crater or collapse depression transformed into a major fungal reservoir.

Required features:
- very high Stage C/D Spore coverage;
- visible remnants of pre-overrun crater geometry under biomass;
- submerged or half-consumed vehicle/structure fragments;
- dense growth in the deepest center;
- radial fungal spread into drainage or cracked road;
- limited intact loot but strong biological/research value;
- encounter pressure among the highest normal terrestrial Spore sites.

This is a calamity landmark, not a routine resource farm.

## PCE-001-D — Cratered Evacuation Junction
Target footprint: **56–80 × 40–64**.
Purpose: combine an evacuation roadway/checkpoint with a major blast interruption.

Required features:
- road approach and lane markings surviving on at least two sides;
- stopped or wrecked traffic approaching the crater;
- emergency reroute/barricade evidence;
- one destroyed checkpoint/service position;
- vehicle debris below rim level;
- Spore spread from the crater into stalled traffic.

Use: transition asset between PCE-003 highway networks and large catastrophe sites.

# PCE-006 — Mass Grave / Biomass Disposal Family

## PCE-006-A — Organized Emergency Burial Trenches
Target footprint: **48–72 × 36–56**.
Purpose: institutional mass-casualty burial while civil organization still functioned.

Required features:
- multiple parallel trenches or clearly phased excavation rows;
- earth-moving access lane;
- temporary identification/record station;
- perimeter fencing or controlled approach;
- body-handling/staging zone represented environmentally rather than graphically;
- covered, partially filled and open trench states in the same site;
- early fungal intrusion beginning in wet/organic trench bottoms.

Narrative: the scale of casualties exceeds ordinary cemetery practice while procedure is still being attempted.

## PCE-006-B — Failed Cremation / Burn Yard
Target footprint: **40–64 × 40–64**.
Purpose: emergency mass disposal by burning after burial capacity or contamination control failed.

Required features:
- scorched earth pads or burn lanes;
- fuel/supply staging remnants;
- ash/debris collection area;
- abandoned equipment;
- collapsed perimeter control;
- evidence that operations stopped abruptly;
- fungal resurgence around incompletely sterilized margins and drainage.

Avoid gratuitous visual detail; scale, process and abandonment should communicate the event.

## PCE-006-C — Bulldozed Disposal Pit
Target footprint: **52–80 × 44–68**, depth **6–12**.
Purpose: desperate late-stage mass disposal with minimal record keeping.

Required features:
- broad excavated pit;
- bulldozer/earthmoving route or equipment silhouette;
- displaced earth berms;
- improvised fencing;
- vehicle unloading point;
- collapsed administrative/guard shelter;
- dense Stage B/C fungal growth across pit floor and berm drainage.

Narrative: institutional procedure has degraded into emergency volume handling.

## PCE-006-D — Biomass Reservoir Grave
Target footprint: **48–72 × 40–64**, depth **8–14**.
Purpose: a former burial/disposal site almost completely reclaimed into a fungal biomass reservoir.

Required features:
- trench/grid geometry still faintly readable beneath growth;
- extremely dense Spore material;
- collapsed fencing and earthmoving debris embedded in biomass;
- abandoned record station or warning mast at the edge;
- high-risk encounter zone;
- biological/research evidence rather than rich conventional loot.

This should be one of the strongest environmental demonstrations that mass casualties directly accelerated fungal expansion.

# PCE-004 — Destroyed Urban / Suburban Calamity Blocks

## PCE-004-A — Shattered Apartment Evacuation Block
Target footprint: **48–64 × 48–64**, vertical **24–48**.
Purpose: residential block damaged during evacuation/final conflict.

Required features:
- at least one partially standing apartment volume;
- collapsed stair/elevator/service core;
- barricaded ground-floor entrance;
- apartment interiors or room silhouettes readable through collapse;
- evacuation luggage/personal-effect zones;
- damaged street frontage with service vehicles;
- fungal growth beginning in basement/service areas and climbing through vertical shafts.

Heavy Rebuild emphasis: believable floor structure and collapse load paths.

## PCE-004-B — Quarantine Hospital Collapse
Target footprint: **56–80 × 48–72**, vertical **20–40**.
Purpose: hospital/clinic converted into an overwhelmed quarantine and treatment facility.

Required zones:
- ambulance/emergency approach;
- intake/triage;
- treatment ward remnants;
- isolation/quarantine wing;
- utility/generator/service area;
- casualty overflow or temporary external shelter;
- at least one sealed or barricaded internal boundary that failed;
- fungal growth concentrated first in isolation, waste, lower service and casualty-handling areas.

Evidence: medical logs, quarantine orders, last-shift records, biological samples and damaged supplies. No intact advanced production machinery.

## PCE-004-C — Burned Civic Response Block
Target footprint: **48–72 × 48–72**, vertical **16–32**.
Purpose: fire/police/municipal emergency complex destroyed while supporting the final response.

Required features:
- recognizable apparatus/service bays;
- operations/dispatch area;
- burned vehicle positions;
- emergency supply storage;
- collapsed roof/floor section;
- roadblock equipment staged outside;
- fire and Spore damage visibly interacting rather than appearing as unrelated decoration.

## PCE-004-D — Barricaded Suburban Row
Target footprint: **64–96 × 32–48**.
Purpose: residential street converted into a local civilian defensive/containment line.

Required features:
- 3–6 distinct homes or partial homes;
- improvised vehicle/fence barricade;
- one burned house;
- one breached house with strong fungal intrusion;
- shared backyard/utility path allowing Spore spread behind the barricade;
- abandoned neighborhood supply point;
- failed escape route or blocked intersection.

This site should make low-density residential collapse as narratively legible as city-center destruction.

# PCE-007 — Calamity Indicator Microstructure Library

These are small repeatable structures intended to connect major sites into a continuous catastrophe landscape. They should generally occupy **5–20 blocks** per side and remain cheap enough for wider distribution.

## PCE-007-A — Emergency Roadblock
Concrete/vehicle barrier, warning sign position, small abandoned guard point and optional early contamination.

## PCE-007-B — Breached Quarantine Fence
Fence corridor with torn opening, discarded screening supplies and fungus concentrated at the breach.

## PCE-007-C — Burned Vehicle Pull-Off
One or two vehicle silhouettes, scorched shoulder, scattered luggage/supplies and drainage contamination.

## PCE-007-D — Abandoned Aid Drop
Pallet/crate/tarp interpretation, partially looted supplies, marker mast and optional Spore intrusion.

## PCE-007-E — Micro-Triage Point
Small canopy/shelter footprint, cots or treatment surfaces, medical-waste area and evacuation signage remnants.

## PCE-007-F — Collapsed Observation Post
Raised watch/traffic/containment position with damaged access, broken communications hardware and sightline over a road or perimeter.

## PCE-007-G — Barricaded House Entrance
Small house-front adjunct with furniture/debris barricade, emergency supplies and optional internal breach.

## PCE-007-H — Biohazard Disposal Skip
Waste-container/service-yard scene with concentrated early Spore growth; usable beside hospitals, camps, labs and industrial sites.

## PCE-007-I — Fungal Drainage Breach
Culvert, ditch, sewer or utility opening showing biomass emerging from below grade.

## PCE-007-J — Destroyed Communications Relay
Small mast/equipment base with blast/fire damage and salvage/evidence potential.

## PCE-007-K — Emergency Fuel Cache
Portable tank/drum/pump interpretation with fire damage or abandonment; loot must remain progression-safe.

## PCE-007-L — Final Field Position
Small sandbag/barrier/observation emplacement showing organized resistance without becoming a major military base.

# Phase 2 implementation priority

1. PCE-006-A organized emergency burial trenches
2. PCE-001-A containment demolition crater
3. PCE-004-B quarantine hospital collapse
4. PCE-001-D cratered evacuation junction
5. PCE-006-D biomass reservoir grave
6. PCE-004-A shattered apartment evacuation block
7. PCE-007-A, B, C and I microstructures
8. remaining Phase 2 variants

This order establishes the casualty, blast, urban-response and scatter vocabularies before expanding rare variants.

# Promotion boundary

Blueprint completion is not natural-worldgen completion. Each promoted structure still requires:
- stable `infinite_domain` ID;
- pack-owned NBT/schematic;
- inspected Spore registry IDs;
- structure-specific damage/contamination stage;
- progression-safe loot/evidence;
- encounter plan;
- Heavy Rebuild visual review;
- worldgen density/context assignment;
- deferred or completed runtime validation status recorded explicitly.
