# OWS-001 Pass 7 — Structural System

## Scope

This pass converts the Gate-A r2 massing into one coherent structural concept before detailed room furnishing begins.

**Approved Gate-A envelope:** 39 x 13 x 33  
**Approved massing revision:** r2  
**Damage state for this pass:** D0 intact / normal operation

This is not structural engineering simulation. The objective is visual and spatial plausibility at Minecraft's one-block scale: roofs need support logic, large openings need frames, ceiling heights must correspond to room functions, and the rooftop plant must appear supported by the building below.

## Structural family

OWS-001 is a neighborhood commercial-service building that VCF either purpose-built or heavily standardized around an ordinary local construction type.

The structural language therefore combines:

- durable masonry/concrete exterior walls;
- steel or reinforced lintels at larger service openings;
- repeated 5–6 block facade/workplace bays;
- lower-span public/service rooms rather than giant clear-span halls;
- locally reinforced cold-chain/mechanical zones;
- a more industrial rear receiving frame than the public frontage;
- lightweight but visibly supported entrance canopies.

It must not look like a secret laboratory bunker or an unframed warehouse cube.

## Primary structural zones

### 1. Public pavilion

Approximate bounds inherited from Gate A:

- X 12–26
- Z 3–12
- roof around Y 7

Structural intent:

- front glazing occurs between masonry/white structural piers;
- double public entrance sits in a framed central bay;
- entrance canopy transfers visually into edge piers/columns rather than floating;
- roof span is modest enough for a neighborhood commercial pavilion;
- later full VCF identity can attach to a real parapet/sign band rather than an unsupported plate.

Target rhythm:

- major verticals around X 12/14, 19–20 entrance core, 24/26;
- side walls remain solid enough to support the roof and separate public/service functions.

### 2. Front workplace block

Approximate bounds:

- X 8–26
- Z 8–20
- roof around Y 8

Structural intent:

- 5–6 block bays along the long direction;
- internal partitions should align to at least some column/wall lines;
- public-facing openings occur only where the rooms behind them justify glazing;
- roof/ceiling zone should allow a shallow service plenum above issue/locker support.

This block should feel more open than the return annex, but it is not one unbroken hall.

### 3. Rear process block

Approximate bounds:

- X 10–29
- Z 18–27
- lower roof around Y 7

Structural intent:

- tighter service/workplace bay rhythm;
- wall/column lines support receiving, stock, consolidation and staff circulation;
- rear process roof steps below the front workplace roof so the approved Gate-A silhouette survives;
- later ceiling/service runs can be visible or partially exposed in receiving zones.

### 4. West return/sanitation annex

Approximate bounds:

- X 3–12
- Z 12–24
- roof around Y 7

Structural intent:

- lower masonry/cleanable annex;
- external service-bay frame at the west wall becomes a real lintel/post system around a staff/service opening;
- return/sanitation partitions should connect to structural wall lines rather than float arbitrarily;
- quality-hold room should use a normal permanent enclosure in D0; D1 temporary barriers/markings come later.

### 5. East clean cold-chain block

Approximate bounds:

- X 26–35
- Z 10–25
- roof around Y 9

Structural intent:

- strongest local vertical support because rooftop cold-chain equipment sits above/adjacent;
- repeated perimeter piers and at least one interior/support line where the plant mass crosses the roof;
- service opening/frame on east wall aligned to maintenance access;
- sufficient uninterrupted wall area for insulation/cold-room reading;
- glazing is limited and purposeful.

### 6. Rear receiving/dispatch volume

Approximate bounds:

- X 12–29
- Z 23–31
- roof around Y 7

Structural intent:

- rear freight opening around X 17–20 receives a full steel lintel/post frame;
- loading canopy aligns directly with that frame;
- adjacent wall bays remain structurally solid;
- receiving floor is durable factory/service material;
- the rear apron visibly meets the loading threshold rather than the entire back wall.

### 7. Supervisor/records bump-out

Approximate bounds:

- X 24–33
- Z 25–29
- roof around Y 6

Structural intent:

- lower office/support volume rather than a second warehouse bay;
- modest glazing may face the service operation;
- no heroic architectural treatment; its importance comes from what happened there, not its scale.

## Roof structure and ceiling strategy

### Public pavilion

- finished ceiling target around Y 6;
- roof around Y 7;
- lighting/identity infrastructure can sit within that shallow zone.

### Front workplace / culture interface

- finished or semi-finished ceiling around Y 7;
- primary roof around Y 8;
- cold-chain/service interfaces can expose limited conduit/vent routing where useful.

### Return/sanitation and rear process

- ceiling around Y 6;
- roof around Y 7;
- more utilitarian finish than public space.

### Cold-chain block

- occupied ceiling/service zone around Y 7–8;
- roof around Y 9;
- local support/penetrations for refrigeration plant above.

The building must not have a single continuous ceiling height across every function.

## Roof-plant support

The Gate-A r2 equipment cluster is conceptually accepted, but Pass 7 requires its load/support story to be visible.

Required relationships:

- roof equipment should align over the cold-chain/workplace support zone;
- at least two major support lines below should plausibly transfer the equipment mass into perimeter/interior structure;
- a maintenance route must reach the plant from the service side;
- equipment should not sit directly above delicate public glazing without an obvious transfer/support condition;
- partial screens must attach to roof frames/parapets rather than float.

## Entrance canopy structure

The r2 canopy width is accepted.

Pass 7 must preserve:

- two edge supports/pier relationships;
- a shallow beam/slab thickness appropriate to its span;
- a clear visual connection to the entrance pavilion;
- enough headroom for player approach.

The canopy may be refined, but it must not return to the r1 full-front slab.

## Rear loading frame

The loading opening is approximately four blocks wide.

Structural minimum:

- two side posts;
- one top lintel/beam;
- canopy tied to that frame;
- apron aligned to the bay;
- adjacent rear wall remains intact enough to support the opening.

## Structural rhythm

Target bay rhythm is approximately **5–6 blocks**, but it should bend around function rather than become a decorative grid.

The structural/facade system should create future anchors for:

- public glazing;
- issue/return counter locations;
- cold-bank service aisle;
- side service doors;
- rear loading bay;
- office windows;
- roof mechanical supports.

## Materials

Preferred structural palette for the D0 intact interpretation:

- `minecraft:stone_bricks` / durable masonry for ordinary neighborhood shell;
- `minecraft:white_concrete` / clean institutional cladding at public and cold-chain zones;
- `minecraft:light_gray_concrete` for service/roof fields;
- `tfmg:cinder_block` for industrial back-of-house enclosure;
- `tfmg:steel_block` or another stable full steel block for major frames/lintels/support posts;
- `create:framed_glass` for controlled public/process glazing.

Final decorative finish decisions remain Pass 9/10 work.

## Structural rejection conditions

Pass 7 fails if:

- large doors/openings have no visible frame;
- roof plant appears unsupported;
- all rooms share one arbitrary ceiling height;
- the structural grid ignores the approved room/program adjacency;
- public canopy floats;
- side service frames remain purely decorative;
- rear loading canopy is not tied to the freight opening;
- interior partitions later would have to cut randomly through windows/columns;
- structural treatment makes the common site look like a fortified bunker.

## Pass 7 result

**STRUCTURAL SYSTEM: DEFINED.**

The next pass will lay out exact public, staff, freight, clean-stock, and dirty-return circulation inside these structural zones. Gate B remains closed until structure, circulation, exterior/interior architecture, operational systems, and VCF identity have all been implemented into one intact D0 review model.
