# Lyran Research — Infernal Continuity Facility

*Design bible and build specification for the structure that replaces the relocated
Nether stronghold as the pack's End-portal landmark.*

Governed by `structure_library/STRUCTURE_REBUILD_SYSTEM_V2.md` (authoring doctrine
and QA gate) and consistent with the Old World canon in
`old_world_narrative/source/01_CANON_AND_NONNEGOTIABLES.md`. Built entirely from
project-owned data — no third-party jar is modified and no third-party content is
redistributed.

---

## 1. Why this structure exists

`docs/SOUTHERN_ANCIENT_CITIES_AND_NETHER_STRONGHOLDS.md` relocated
`minecraft:stronghold` into the Nether by retagging its biome lists, and recorded
one unresolved risk in plain terms: *vanilla stronghold assembly was tuned for
Overworld vertical conditions*, and if pieces generate too high, too low, or
mostly outside terrain, the relocation has to be replaced with a Nether-tuned
structure. `docs/NETHER_PROGRESSION_GATE.md` then made End progression depend on
finding one.

That is a load-bearing dependency resting on a structure that was never designed
for the dimension it now generates in. Lyran Research resolves it by replacing the
route rather than patching it: a purpose-built, Nether-native complex that carves
its own envelope out of the rock, seals itself against the lava ocean, and holds
the End portal in a chamber built for the purpose.

The vanilla stronghold is removed from the Nether biome tags at the same time, so
exactly one structure owns the End route.

---

## 2. Narrative

### The premise

Continuity — the cross-disciplinary containment network of the Old World canon —
never had one contingency plan. It had many, funded separately, run by people who
mostly did not know about each other. `docs/continuity-offworld.md` already
records one of them: the Far-Side Redoubt on the Moon, a pressurised fallback
built beyond the reach of the terrestrial failure.

**Lyran** was another. Where the off-world programme moved contingency *outward*,
the Lyran programme moved it *sideways* — an extradimensional continuity facility,
on the theory that a reservoir distributed across every logistics chain on Earth
could not follow personnel across a dimensional boundary.

The theory was correct. The transit was not reversible.

### What the players find

Lyran Research is not the original facility. The original transit team arrived,
confirmed they could not return, and began building. What survives is what their
**descendants** built: generations of a small, closed, increasingly desperate
civilisation excavated into infernal rock, organised entirely around one
institutional purpose — the **Egress Programme**, the search for a way out.

They did not build a laboratory that happened to be trapped. They built a trapped
society that was entirely a laboratory. Every room in the complex is either
Egress work, or the life-support that keeps Egress work possible, or the
administration that decides who does which.

### The Gate

They did not build the End portal. They **found** it — an existing dimensional
aperture in the rock, discovered during the third generation's deep survey. The
entire Concourse level was re-excavated to radiate around it. Room 21 is the
reason the complex has the shape it has.

And they could never open it. The frame wanted eyes; eyes wanted ender pearls and
blaze powder in quantities and with a metallurgy the colony's founders had not
thought to write down, because on Earth nobody had needed to. Twelve sockets. The
colony, at its peak, filled some of them. The rest of its history is the story of
a society that reorganised itself permanently around a door it could see and could
not use.

The player arrives with eyes of ender in a pouch and finishes, in an afternoon,
the work of four hundred years. That is the intended emotional beat. Nothing in
the structure should state it. The Long Roster, the Rotunda of Returns, the
Crèche, and the Last Ward should be enough.

### Vocabulary for signs, books and room names

| Term | Meaning |
|---|---|
| **The Egress Programme** | The colony's entire institutional purpose |
| **The Gate** | The End portal in Room 21 |
| **Cycle** | Their unit of time; a Cycle is one full rotation of the duty roster |
| **The Long Roster** | The complete list of every person born in the facility |
| **Warden of Records** | The senior surviving office; the last one wrote the terminal log |
| **The Return** | The doctrine that the Gate leads home. It does not. |
| **Reliquary** | Where the eyes were kept, and from which they were lost |
| **Sounding** | An attempt to measure the Gate; hundreds are logged |

Never put the complete explanation in one room — canon rule from
`01_CANON_AND_NONNEGOTIABLES.md`. The Registry has rosters, the Cartography has
soundings, the Reliquary has an inventory with entries struck through, the Last
Ward has the ending. None of them has the whole story.

---

## 3. Reference plan and how it was used

The supplied map (*Lyran Research 01, Level 1*, gargantuan 91 × 91, superior
masonry, natural stone floor) is the authoritative plan for the **Concourse** —
the facility's main level.

It was not eyeballed. `scripts/lyran_extract_plan.py` samples the printed page at
300 dpi into a 91 × 91 occupancy grid, detects doorways from the partially-darkened
cells where door / archway / portcullis glyphs are drawn into the wall line, and
flood-fills each printed room number outward to recover per-room cell sets. The
result is `structure_library/programs/lyran_research_level1_plan.json`:

- **3,300 open floor cells** of 8,281
- **46 rooms**, matching the printed numbering exactly
- **93 doorways**
- **3 vertical-circulation markers** — one *Up* (north arm, off Room 3), two
  *Down* (west of Room 26; south of Room 34)
- **one isolated 17-cell passage** behind Room 44, unreachable through any
  doorway — the map's *Secret* glyph, kept as a secret passage
- **99.5%** of open floor in a single connected component

Scale is **1 map cell = 1 block**. The printed walls are one cell thick and stay
one block thick, which is also how vanilla strongholds read.

---

## 4. Vertical program

Five levels, each 8 blocks of pitch (1 floor slab, 6 clear interior, 1 ceiling
slab), plus an armoured ascent shaft that breaks the surface of the lava ocean.

The excavation is widest at the Concourse and tapers in both directions — the
colony dug outward from the Gate and never finished either extreme.

| Level | Name | Footprint | y (local) | Purpose |
|---|---|---|---|---|
| **L5** | **The Anchorage** | north arm | 32–39 | Arrival, blast locks, the Watch, dead mooring |
| **L4** | **Habitation Terraces** | north arm + band | 24–31 | Dormitories, farms, crèche annex, Gate gallery |
| **L3** | **The Concourse** | **full map** | 16–23 | Administration, archive, clinic — **and the Gate** |
| **L2** | **The Laboratories** | band + south arm | 8–15 | Containment, metrology, blaze crucible |
| **L1** | **Deep Works** | south arm | 0–7 | Geothermal tap, foundry, reclamation, the Sink |
| — | **Ascent Shaft** | 7 × 7 core | 40–71 | Armoured climb to a bastion head above the lava |

All five levels reuse the **same 91 × 91 structural grid**. This is deliberate
and is the architectural argument of the building: the facility was cut as a
single bearing lattice, and each stratum opens a different subset of the same
plan. Shared walls line up floor to floor, vertical shafts land on real rooms at
both ends, and the labyrinth reads as one excavation rather than five unrelated
maps stacked together.

Placed at world **Y = 10**, so the Deep Works floor sits at Y 10, the Anchorage
ceiling at Y 49, and the bastion head emerges from the Y 64 lava sea as a black
tower standing in the fire — visible from a distance, which is what a landmark
gating End progression needs to be.

### Vertical circulation

| Shaft | Grid position | Connects | Source |
|---|---|---|---|
| **North Ascent** | x 53–59, z 8–10 | L3 → L4 → L5 → shaft | map *Up* marker |
| **West Descent** | x 1–2, z 47–49 | L3 → L2 | map *Down* marker |
| **East Descent** | x 59–64, z 58–59 | L3 → L2 | map *Down* marker |
| **Deep Descent** | south arm, Room 42/43 | L2 → L1 | derived |

Every shaft is an `encased_stairwell` — walls, headroom and real landings at both
ends — never a bare diagonal of stair blocks.

### The Gate Chamber is double height

Room 21 is a nine-block-diameter circle. On the Concourse it holds the portal.
On the Habitation level directly above, its footprint receives **no floor slab** —
instead a gallery ring runs around the void, so the Gate is visible from the level
above and the rotunda reads as the monumental space the colony treated it as.

---

## 5. Room program — L3, The Concourse

Room numbers are the printed numbers on the reference map. Bounds are grid cells
`[x1, z1, x2, z2]`.

### North arm — Administration and the Ascent

| # | Bounds | Room | Contents |
|---|---|---|---|
| 1 | 33,1–41,9 | **The Muster Ring** (circle) | Roll-call rotunda; the Long Roster carved around the wall on backed signs |
| 2 | 43,1–51,9 | **Chapter House** (pentagon) | Five seats for five founding disciplines; council table, lectern |
| 3 | 53,1–59,7 | **Ascent Hall** | Head of the North Ascent stairwell |
| 4 | 33,11–41,19 | **The Registry** | Roster archive: lecterns, barrels, data banks |
| 5 | 41,11–49,19 | **Rotunda of Returns** (circle) | Memorial to expedition crews lost attempting egress |
| 6 | 52,11–59,18 | **Warden's Office** | Desk, chest, private records |
| 7 | 51,19–59,27 | **The Signal Ring** (circle) | Dimensional listening array — "the Ear" |
| 8 | 33,21–41,29 | **Records Vault** | Deep archive; loot chests |
| 9 | 41,21–49,28 | **Dispatch** | Work assignment; duty boards |

### Band, west — Life support and works

| # | Bounds | Room | Contents |
|---|---|---|---|
| 12 | 2,32–9,38 | **West Reclamation** | Soul-sand condensers, tanks |
| 13 | 11,32–19,38 | **Culture Hall** | Fungal growth racks — the colony's Evercrop-descended food crop |
| 14 | 21,31–29,39 | **Cistern Ring** (circle) | Magma-heated water ring |
| 15 | 31,31–39,37 | **Concourse Well** (circle) | Junction rotunda immediately north of the Gate |
| 20 | 11,41–19,48 | **Provisioning** | Barrels, shelving |
| 26 | 2,43–9,50 | **West Stair Hall** | Head of the West Descent |
| 27 | 21,41–30,50 | **Machine Hall** | Shafts, gearboxes, drive train |
| 29 | 9,47–19,57 | **The Kiln Ring** (circle) | Smelting and ceramics |
| 33 | 30,51–38,58 | **Cartography** | The Soundings — dimensional survey maps |
| 35 | 1,51–9,58 | **Waste Sorting** | Reclamation intake |

### Band, centre — the Gate

| # | Bounds | Room | Contents |
|---|---|---|---|
| 10 | 41,32–49,38 | **The Clinic** | Beds, brewing stands |
| 11 | 49,31–57,38 | **Apothecary / APL Ward** | The Aevum lineage's last regenerative work |
| **21** | **31,39–39,48** | **★ THE GATE CHAMBER** (circle) | **The End portal**, on a raised dais over lava, ringed by a walkway; monitoring stations; double height |
| 22 | 41,41–49,48 | **Gate Antechamber** | Vesting room; armour stands, chests |
| 23 | 51,39–57,44 | **The Eye Reliquary** (pentagon) | Twelve empty sockets; the inventory with entries struck through |
| 30 | 40,51–48,58 | **Gate Control** | Instrumentation facing the chamber |
| 31 | 49,51–57,58 | **Instrument Shop** | Benches, tools |
| 34 | 58,51–64,53 | **East Stair Hall** | Head of the East Descent |

### Band, east — Refectory, stores, containment

| # | Bounds | Room | Contents |
|---|---|---|---|
| 16 | 58,31–64,38 | **Refectory** | Tables, kitchen |
| 17 | 65,31–73,38 | **The Long Hall** | Communal assembly |
| 18 | 74,31–82,38 | **Store Rooms** | Bulk storage |
| 19 | 83,31–89,40 | **East Magazine** | Blaze-rod stores — the Egress Programme's most guarded consumable |
| 24 | 59,41–67,48 | **Crucible Shop** | Blast furnaces, anvils |
| 25 | 68,41–76,48 | **Glass & Lens Works** | Optics for the Soundings |
| 28 | 82,42–89,50 | **East Reclamation** | Second condenser bank |
| 32 | 69,51–77,58 | **Quarantine Cells** | Isolation — old Continuity habit, kept out of doctrine |
| 36 | 77,51–83,59 | **The Warren** | Narrow service labyrinth (the map's comb pattern), unlit |

### South arm — the failing colony

| # | Bounds | Room | Contents |
|---|---|---|---|
| 37 | 21,49–39,65 | **The Commons** | Largest room in the facility; communal refectory |
| 38 | 41,60–49,67 | **Dormitory A** | Bunks |
| 39 | 51,60–59,67 | **Dormitory B** | Bunks |
| 40 | 31,68–39,76 | **The Crèche** | The children's hall |
| 41 | 41,68–49,77 | **Infirmary** | Beds, brewing |
| 42 | 49,68–59,76 | **Mortuary** | Preparation slabs |
| 43 | 31,76–39,84 | **The Ossuary** | Bone stacks; head of the Deep Descent |
| 44 | 49,74–59,81 | **Shrine of the Return** (pentagon) | The devotional cult that grew around the Gate |
| 45 | 40,78–48,84 | **Pilgrim Cells** | Small cells off the shrine |
| 46 | 47,83–55,89 | **The Last Ward** | The terminal chamber; the final record |
| — | x 57, z 79–86 | **The Warden's Bolt-hole** *(secret)* | The isolated passage; terminal log and the best loot, behind a secret door |

---

## 6. Room program — derived levels

### L5 — The Anchorage (north arm, y 32–39)

The arrival level. Everything here is about the boundary between the facility and
the hell outside it.

| Grid room | Purpose |
|---|---|
| 1 (circle) | **The Watch** — observation ring at the shaft foot |
| 2 (pentagon) | **Blast Lock** — the outer seal |
| 3 | **Shaft Head** — foot of the Ascent Shaft |
| 4 | **Decontamination** — a habit inherited from Earth-side Continuity and never dropped |
| 5 (circle) | **Muster Well** |
| 6 | **Watch Office** |
| 7 (circle) | **The Dead Mooring** — where cargo was to be received from a resupply that never came |
| 8, 9 | **Cargo Halls** — empty racking |

### L4 — Habitation Terraces (north arm + band, y 24–31)

| Region | Purpose |
|---|---|
| North arm | Dormitory terraces, washrooms, the crèche annex |
| Band, west | Fungal farm halls — the largest surviving food production |
| Band, centre | **Gate gallery** — the ring around Room 21's open void; married quarters |
| Band, east | Refectory annex, laundry, storage |

### L2 — The Laboratories (band + south arm, y 8–15)

The Egress Programme's actual working level.

| Region | Purpose |
|---|---|
| Band, west | Dimensional metrology, the Sounding benches |
| Band, centre | **Directly beneath the Gate**: the anchor works — the structure that holds the aperture stable |
| Band, east | Blaze crucible, specimen holds, containment cells |
| South arm | Sample stores, failed-apparatus graveyard |

### L1 — Deep Works (south arm, y 0–7)

| Region | Purpose |
|---|---|
| North of arm | **The Geothermal Tap** — lava channels feeding the whole complex |
| Centre | **The Foundry** |
| South | **The Sink** — waste, and the pit the colony stopped recording |

---

## 7. Palette

Nether-native, infernal-industrial. Vanilla plus mods already loaded by the pack.

| Element | Block |
|---|---|
| Structural wall | `minecraft:polished_blackstone_bricks` |
| Wall accent / pilaster | `minecraft:polished_blackstone` |
| Damaged wall | `minecraft:cracked_polished_blackstone_bricks` |
| Floor (public) | `minecraft:polished_basalt`, `minecraft:smooth_basalt` |
| Floor (service) | `minecraft:basalt`, `minecraft:blackstone` |
| Ceiling | `minecraft:blackstone` |
| Envelope / packing | `minecraft:netherrack`, `minecraft:basalt` |
| Gate Chamber dais | `minecraft:polished_blackstone_bricks` + `minecraft:chiseled_polished_blackstone` |
| Portal frame | `minecraft:end_portal_frame` (12, some with eyes) |
| Lighting | `minecraft:soul_lantern` (public), `minecraft:lantern` (works), `minecraft:shroomlight` (farms) |
| Glazing | `create:framed_glass`, `minecraft:tinted_glass` |
| Doors | `minecraft:crimson_door`, `minecraft:iron_door` (secure rooms) |
| Signage | `minecraft:crimson_wall_sign`, `minecraft:warped_wall_sign` |
| Growth | `minecraft:nether_wart_block`, `minecraft:warped_wart_block`, `minecraft:shroomlight` |

Soul lanterns for the administration and memorial spaces, plain lanterns for the
works, shroomlight for the farms. The lighting temperature is how the player tells
which part of the colony they are standing in.

---

## 8. Loot and progression

Reuses existing registered tables — no invented, unregistered loot-table IDs.

| Table | Placed in |
|---|---|
| `infinite_domain:chests/wasteland_data` | Registry, Records Vault, Cartography, Gate Control, Bolt-hole |
| `infinite_domain:chests/wasteland_industrial` | Machine Hall, Crucible Shop, Instrument Shop, Foundry |
| `infinite_domain:chests/wasteland_home` | Dormitories, Crèche, Pilgrim Cells |

The **Reliquary** (Room 23) is the progression beat: twelve sockets, the inventory
that records what happened to each eye, and a chest with the surviving fragments.
The portal in Room 21 generates with a **partial** set of eyes already seated —
the colony's own progress — leaving the rest for the player.

---

## 9. Build and QA requirements

1. Authored with the `Template` API in `scripts/generate_wasteland_sites.py`,
   using **only** `structure_geometry_primitives_v2` for stairs, ladders, signs,
   windows, footings and breaches. No `stair_flight`, no bare `t.set` ladders or
   signs, no `t.clear()` box damage.
2. The envelope is **sealed**: every level gets a full floor slab and ceiling slab
   across its footprint, and every open cell is bounded by placed wall blocks, so
   the Nether lava ocean cannot intrude into any interior space.
3. Zero hard-fail findings across all six `structure_geometry_lint.py` checks —
   verified in memory **and** after a real save → disk reload → re-lint round trip,
   matching how `docs/continuity-offworld.md` verified the last hero build.
4. Not folded into the 84-structure wasteland corpus. `corpus-manifest.json`
   counts are untouched. This follows the alien / Far-Side Redoubt precedent: one
   landmark NBT with direct jigsaw, structure_set and template_pool registration.
5. Every modded block and blockstate property used is verified against the mod's
   actually-registered blockstates before it ships, never guessed.

## 10. As built

Generated by `scripts/lyran_research.py`; evidence in
`docs/lyran-research-verification.json` and
`structure_library/reviews/lyran_research/`.

| | |
|---|---|
| Template size | 91 × 72 × 91 |
| Blocks placed | 122,159 (including the excavated air that carves the rooms) |
| Palette states | 60 — **all vanilla**, no modded block dependency |
| NBT on disk | 342 KB |
| Rooms furnished | 46 on the Concourse, 145 across all five levels |
| Loot chests | 79 |
| End portal frames | 24 (12 live in the Gate Chamber, 12 dead in the Reliquary) |
| Envelope backfill | 429 blocks |
| Reproducible | byte-identical across runs |

**Geometry lint** — `structure_geometry_lint.py`, all six checks, **0 hard-fail
and 0 review-flag**, confirmed both in memory and after a real
save → disk reload → re-lint round trip.

**Playability verification** — `scripts/verify_lyran.py`, 14/14:

- the End portal is a correct 12-frame vanilla ring, every frame facing
  inward, corners empty, 3×3 interior clear — it is a portal that actually
  forms;
- it generates with 4 of 12 eyes seated, leaving 8 for the player;
- the envelope is lava-tight: **zero** interior air cells border a cell this
  template does not place;
- a player entering at the shaft mouth can walk all the way to the Gate
  Chamber, and all five levels are reachable (11,665 standing cells);
- no iron doors anywhere — an iron door in a generated structure needs
  redstone the player cannot supply, so it is a room nobody can enter.

### Defects caught during the build, and what they teach

Recorded because the pipeline's own rule is that a successful exit code is
not evidence:

1. **The rooms were never excavated.** The shell pass built floors, ceilings
   and walls but placed no interior air. A structure template only removes
   what it explicitly places, so every "room" would have generated as solid
   Nether rock with a decorative wall grid buried in it. The geometry lint
   passed this build cleanly — it checks placed geometry, and unplaced cells
   read to it as air. Only the reachability test caught it.
2. **The ascent shaft's casing sealed the Anchorage.** Running the casing down
   through the arrival level put a 5 × 5 tube straight through it, walling the
   ladder off from the stair hall it opens onto.
3. **Pre-punched stairwell holes** left an eleven-block pit in the floor above.
   Stairs now cut their own openings via the primitive's headroom clearing.
4. **Non-deterministic output.** Seeding from Python's `hash()` produced a
   different building every run; a structure that cannot be regenerated
   byte-for-byte is not reviewable.
5. **Iron doors.** Flavourful, and completely unopenable.

Items 1, 2 and 5 were invisible to the geometry lint and would have shipped.
That is the argument for `verify_lyran.py` existing alongside it.

## 11. Worldgen integration

- `infinite_domain:nether/lyran_research` — jigsaw structure, `#minecraft:is_nether`,
  `underground_structures` step, `terrain_adaptation: none`, `start_height`
  absolute 10, `size: 1`, `max_distance_from_center: 116`.
- Structure set `random_spread`, spacing 40 / separation 16 chunks — a
  once-per-region landmark, not a dungeon.
- Added to `#minecraft:eye_of_ender_located` so eyes of ender track it.
- `minecraft:stronghold` removed from `#minecraft:has_structure/stronghold` and
  `#minecraft:stronghold_biased_to`, retiring the biome-tag relocation and its
  recorded terrain-fit risk.
- `docs/NETHER_PROGRESSION_GATE.md` and
  `docs/SOUTHERN_ANCIENT_CITIES_AND_NETHER_STRONGHOLDS.md` updated to describe the
  replacement route.
