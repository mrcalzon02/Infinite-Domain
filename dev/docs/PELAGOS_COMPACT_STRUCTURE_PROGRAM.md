# Infinite Domain — Pelagos Compact Structural Conversion Program

Status: **planning only. No geometry, no data files, no generator code has been written against this document. Nothing here is implemented, approved, or measured in-world.**

Sibling document: [`docs/KARSIC_DIRECTORATE_STRUCTURE_PROGRAM.md`](KARSIC_DIRECTORATE_STRUCTURE_PROGRAM.md). The two are deliberately self-contained so either can be worked in isolation; the only content they share is the **Shared regional contract** (§3), which is stated identically in both and must be changed in both or neither.

---

## 1. Authority and precedence

| Rank | Source | Role |
|---|---|---|
| 1 | `old_world_narrative/source/01_CANON_AND_NONNEGOTIABLES.md` | Immutable world facts. |
| 2 | `old_world_narrative/source/03_STRUCTURE_REVISION_PROGRAM_UPDATED.md` §"Alternative structures — regional faction architecture" | Defines the Pelagos Compact, its design language, its hemisphere, and the regional-equivalency rule. **This document implements that section; it does not replace it.** |
| 3 | `structure_library/STRUCTURE_REBUILD_SYSTEM_V2.md` | Binding geometry doctrine and QA gate. Every Pelagos asset is subject to §3.1–3.8 and §4 exactly as central-continent assets are. |
| 4 | `docs/HEAVY_REBUILD_DOCTRINE.md` | Rebuild standard, visual gates A/B/C, the five scales of detail, collapse-state layering. |
| 5 | `CODEX_STRUCTURE_PIPELINE.md` | Pipeline stages, repository discipline, usage-conserving family policy. |
| 6 | **This document** | Pelagos-specific cultural specification: strata, material profile, massing grammar, plan grammar, settlement grammar, conversion passes, generator architecture, structure roster, Lost Cities wiring. |

Precedent for format and tone: `docs/ABYSSAL_OCEAN_PROGRAM.md`, which already governs the Karsic/Pelagos split below sea level. This document is its surface counterpart and must not contradict it.

Future work updates this file rather than creating a parallel plan.

---

## 2. Hemisphere binding — read this before doing anything

**Canonical binding, confirmed against live pack data: the Pelagos Compact is the WESTERN region (−X).**

Evidence, all currently in the repository:

| Source | Statement |
|---|---|
| `03_STRUCTURE_REVISION_PROGRAM_UPDATED.md` §World placement | "The Pelagos Compact: preferentially spawn on the **left/western side of the world map**." |
| `docs/ABYSSAL_OCEAN_PROGRAM.md` §Regional identity | "**Western Abyss — Pelagos.**" |
| `kubejs/data/infinite_domain/tags/worldgen/structure/western_*_sites.json` | All four western site tags contain only `infinite_domain:abyssal/pelagos_*` structures. |
| `tools/abyssal_worldgen/abyssal_factional_debris_catalog.json` `pool_contract` | `"pelagos_pool_must_stay_western_only": true`. |
| `kubejs/data/minecraft/worldgen/world_preset/normal.json` | `infinite_domain:western_*` biomes are all gated on `humidity [-1.0, -0.2]`, the **negative** (western, −X) side of `custom_worldgen:east_west_gradient`. |
| `config/ftbquests/quests/lang/en_us.snbt` | "Take the pressure-capable submarine beyond the **western** shelf… the **Pelagos**-facing continental slope." |

The planning request that produced this document described the arrangement the other way round (English-inspired culture in the **East**, Russian-inspired culture in the **West**). That is the opposite of every artefact listed above. This document therefore uses the **pack-canonical** binding — Pelagos = West — and is named by **faction**, not by hemisphere, so a later reversal is a routing change rather than a rewrite.

### 2.1 If the binding is deliberately reversed

Nothing in §4–§12 changes; the culture is defined by faction, not by compass. Reversal touches exactly five things, all outside this file:

1. `kubejs/data/minecraft/worldgen/world_preset/normal.json` — swap the `humidity` bands on the Pelagos and Karsic **land** rules added by §12.
2. `kubejs/data/infinite_domain/tags/worldgen/biome/pelagos_region_biomes.json` — repoint at the eastern biome set.
3. The `biomes` matcher on the Pelagos city-style selectors in the worldstyle (§11.5).
4. The `abyssal_factional_debris_catalog.json` `pool_contract` flags plus the eight `eastern_*`/`western_*` abyssal site tags — **this drags the entire implemented deep-ocean program with it**, and is the expensive part.
5. Existing quest text in `config/ftbquests/quests/lang/en_us.snbt` naming the western shelf as Pelagos-facing.

**Recommendation: keep West = Pelagos and treat the planning-request wording as a slip.** If the reversal is genuinely wanted, do it as its own dedicated change before any Pelagos surface geometry exists, not after.

---

## 3. Shared regional contract

*(C1–C10 are stated identically in both regional programs. Change both or neither.)*

**C1 — Regional readability precedes narrative.** A player must be able to name the region from silhouette, planning logic, material, utilities, defensive assumptions, and interior organisation **before** reading any sign or book.

**C2 — Identity lives in common structures.** A region whose identity is carried only by rare landmarks has failed. Houses, sheds, shops, utility kiosks, and roadside furniture carry the language at least as strongly as the landmarks.

**C3 — No recolours.** A regional variant that changes only the block palette is not a variant. Per `03_STRUCTURE_REVISION_PROGRAM_UPDATED.md` §Codex implementation rule, a conversion must materially change regional identity *in addition to* passing the normal four-of-six revision acceptance test.

**C4 — Regional equivalency, not taxonomy explosion.** Gameplay role is preserved across regions; silhouette, circulation, infrastructure, environmental storytelling, and loot presentation change. A hospital stays a hospital.

**C5 — Rarity is inherited.** A regional variant inherits the rarity of the underlying gameplay function unless there is a specific narrative reason to change it.

**C6 — Cross-regional appearances are deliberate and explain themselves.** A displaced structure must communicate *why* it is there. Random mixing is prohibited.

**C7 — V2 doctrine is not relaxed for regional work.** Encased stairwells, openings as wall operations, authored damage, site-specific ground, real foundations, area-scaled detail, edge transitions. `scripts/structure_geometry_lint.py` checks 1–3 must report zero hard-fail findings.

**C8 — Determinism.** Every generator run is reproducible byte-for-byte from `(culture, structure_id, pass_id, variant)`. No wall-clock, no process entropy, no unordered-set iteration in any code path that reaches geometry.

**C9 — The Old World must look worth saving.** Per canon §"Artistic rule". Some regional interiors must read as warm, competent, and humane before they read as ruined.

**C10 — Never put the complete explanation in one building.**

---

## 4. Cultural thesis

### 4.1 The one-sentence reading

**The Pelagos Compact never got to start again — every solution had to fit inside the last three.**

The Compact is a society that ran out of land before it ran out of ideas. Its plot boundaries are older than its buildings; its buildings are older than their functions; its functions are older than the services threaded through them. Nothing was ever cleared and rebuilt from zero, so everything carries the shape of what it replaced. A player who steps into a Pelagos laboratory, looks up, and sees a cast-iron beam from a warehouse two centuries older has understood the Compact correctly.

Where the Directorate's identity is **the standard applied everywhere**, the Compact's identity is **the accumulation visible in one place**. That is the whole contrast, and every design rule below is downstream of it.

### 4.2 Prohibited shortcuts

Banned outright. Presence is a hard review failure, not a note.

- Faux-medieval fantasy: thatched cottages as a default, crooked timber for charm, castle motifs. Canon is explicit — "not faux-medieval Britain, fantasy cottages, or an endless field of Victorian buildings."
- A wall-to-wall Victorian region. P-II and P-III are two strata out of six, not the whole vocabulary.
- Flags, crowns, lions, or any national emblem used as decoration.
- Red boxes and kiosks used as a punchline. They belong in the street-furniture set as *ordinary municipal equipment*, at ordinary frequency, and nowhere else.
- Tea, bowler hats, and comparable set dressing. The culture is in the fabric, not the props.
- Single-stratum buildings. See §4.4 — the two-stratum rule is not optional.

### 4.3 The ten legibility carriers

Ranked by regional identity delivered per block placed. Generator budget follows this order.

| # | Carrier | Why it reads |
|---|---|---|
| 1 | **Pitched roof, party wall, chimney rhythm** | A run of pitched roofs interrupted by raised party parapets and regular stacks is instantly, unmistakably not Karsic. Cheap, and visible from a distance. |
| 2 | **Brick, and brick as texture** | Brick is the default wall for two thirds of the roster. Bonding, string courses, segmental arches, and corbelled detail are the ornament. |
| 3 | **The attached unit with its own front door** | Terraces and semis: repetition, but of *houses*, each with a door on the street. Karsic repeats a building; Pelagos repeats a home. |
| 4 | **Colonised railway arches** | A brick viaduct with workshops, lock-ups, and shutters filling the arches. One of the most distinctive urban forms available, and almost free in blocks. |
| 5 | **Older shell, newer function** | A visible mismatch between what a building looks like and what it was last used for. The strongest single carrier of the §4.1 thesis. |
| 6 | **Narrow rear service alley** | Back access, outbuildings, gates, yards. Turns a terrace from a wall into a neighbourhood. |
| 7 | **High-street frontage** | Shopfront glazing between piers, a fascia band, an awning, residential floors above with a different window rhythm. |
| 8 | **Inherited irregular geometry** | Plot lines that do not agree with each other; buildings that follow an older road; corner sites cut at odd angles. |
| 9 | **Retrofitted services** | Surface-mounted pipes, cable trays, plant squeezed into a rear yard or onto a roof, a duct chased through a wall that never expected it. |
| 10 | **Municipal street furniture** | Bollards, railings, lamp standards, post box, kiosk, bus shelter, notice board — the same handful of items, everywhere, quietly. |

### 4.4 The six Pelagos strata

**The Pelagos rule: every structure declares at least TWO strata.** This is the direct counterpart of the Karsic single-primary-stratum rule, and it is where the two cultures diverge most cleanly at the generator level. Karsic puts one stratum in a building and a system around it; Pelagos puts two or more strata *inside* one building.

| ID | Name | Period role | Materials | Signature |
|---|---|---|---|---|
| **P-0** | *Londinium substrate* | The deepest layer. Two thousand years older than everything else, and encountered only from above. | Ragstone rubble with red bonding-tile courses, opus signinum floors, hypocaust pilae. | A wall fragment in a cellar; a road alignment a modern street still follows; a tessellated floor under a lift pit. **Never a complete building.** See §4.6. |
| **P-I** | *Old fabric* | Pre-industrial survivals. | Rubble stone, early brick, timber framing and daub, steep tiled roofs, thick walls. | Small openings, deep window seats, irregular plan, massive chimney breast. |
| **P-II** | *Estate brick* | The classical brick town. | Brick with stone dressings, slate roof, iron railings. | Regular tall-window rhythm, parapet or eaves cornice, string course, sunken area with railings, stacks on party walls. |
| **P-III** | *Industrial brick* | Mills, warehouses, viaducts, works. | Brick, cast and wrought iron, timber floors, slate and glass roofs. | Segmental arches, iron columns, loading doors at every floor, wall crane, tall chimney, sawtooth sheds. |
| **P-IV** | *Post-war civic* | Reconstruction and the precinct era. | Concrete frame, panel and tile infill, mosaic spandrels, patent glazing. | Deck access, undercroft, subway underpass, ramped car park, exposed-aggregate panels. |
| **P-V** | *Contemporary graft* | The last thirty years. | Glass, steel, rainscreen cladding, sealed units. | Atrium connectors between older wings, retained façades propped from behind, rooftop plant enclosures, a new entrance that ignores the old one. |

**Stratum pairing.** Any two strata may be paired, and three is common and encouraged for institutional buildings — that is the Compact's whole character. The only constrained stratum is **P-0**, capped at nine structures (§4.6).

### 4.5 The Compact collapse thesis

From canon: *"interdependence, constrained space, and successive retrofits overwhelming systems that were already layered and tightly coupled."* Expressed structurally:

- **The newest layer failed first.** Sealed modern systems died while the Victorian shell around them stood untouched. Brick outlives its services.
- **Contamination used the old routes.** New containment was fitted to buildings whose drains, ducts, and cellars predated the idea of containment by a century. The barrier held; the forgotten culvert did not.
- **Nothing could be isolated.** Quarantine lines had to follow street patterns laid out before anyone imagined needing to seal a district.
- **Institutions expanded into their neighbours.** Hospitals took schools, then halls, then stations. Each absorption is visible as a connection made in a hurry.
- **Concentration became the danger.** Rail and ferry were the evacuation arteries and therefore the worst places to be.
- **Improvisation happened at street level**, because no central facility could physically absorb the demand.

### 4.6 The Londinium doctrine

The oldest Pelagos stratum is Roman, and it is the region's most distinctive asset — a depth axis the Karsic side does not have. Handled badly it becomes fantasy ruins in a field. Four rules keep it honest:

1. **Never a complete Roman building.** Always a fragment: a length of wall, a corner, a floor, a run of pilae.
2. **Always encountered from above** — through a modern cellar floor, a lift pit, a service trench, a bomb crater, a railway cutting, or the foreshore at low water. The player looks *down* into it.
3. **Always accompanied by a modern intervention.** Steel props, a scaffold walkway, a survey grid chalked on the stone, spray-marked levels, a glazed display panel in an office lobby, a notice board. Somebody found this and made arrangements around it.
4. **Exactly one landmark** where the substrate is the point rather than the surprise: `pel_090_londinium_wall_fragment`.

**Cap: nine structures carry P-0**, named in the roster (§10.11). Beyond nine it stops being a stratum and becomes a theme.

The material signature is specific and buildable: **ragstone rubble with red bonding-tile courses** — `minecraft:cobblestone` and `minecraft:mossy_cobblestone` walling interrupted every four courses by a course of `minecraft:brick_slab`. That grey-and-red banding is what a player learns to recognise, and it appears nowhere else in either region.

---

## 5. Material system

Every block ID below was verified present in `docs/registry-inventory/block-ids.txt` for this instance on 2026-08-26. **Any addition to these tables must be verified the same way before it reaches a generator.**

### 5.1 Structural roles by stratum

The generator never names a block directly. It names a **role**; the Pelagos material profile resolves the role to a block for the active stratum. This is what makes Pass P3 (§8) a single deterministic substitution rather than a hand edit of thousands of coordinates.

| Role | P-0 Londinium | P-I Old fabric | P-II Estate brick | P-III Industrial brick | P-IV Post-war civic | P-V Contemporary |
|---|---|---|---|---|---|---|
| `wall_primary` | `minecraft:cobblestone` | `minecraft:cobblestone` | `minecraft:bricks` | `minecraft:bricks` | `immersiveengineering:concrete` | `immersiveengineering:sheetmetal_aluminum` |
| `wall_secondary` | `minecraft:mossy_cobblestone` | `supplementaries:daub` | `quark:polished_limestone` | `quark:cobblestone_bricks` | `immersiveengineering:concrete_tile` | `minecraft:tinted_glass` |
| `wall_banding` | `minecraft:brick_slab` | — | `quark:limestone_bricks` | `minecraft:brick_slab` | `minecraft:white_terracotta` | — |
| `wall_frame` | — | `supplementaries:timber_frame` | — | `create:metal_girder` | `immersiveengineering:concrete_pillar` | `create:metal_girder` |
| `wall_brace` | — | `supplementaries:timber_cross_brace` | — | — | — | — |
| `dressing_stone` | — | `minecraft:stone_bricks` | `quark:limestone_bricks` | `quark:limestone` | `immersiveengineering:concrete_chiseled` | `quark:polished_limestone` |
| `plinth` | `minecraft:cobblestone` | `minecraft:cobblestone` | `quark:polished_limestone` | `minecraft:stone_bricks` | `tfmg:gray_rebar_concrete` | `quark:polished_shale` |
| `floor_slab` | `minecraft:red_terracotta` | `minecraft:oak_planks` | `minecraft:oak_planks` | `minecraft:oak_planks` | `immersiveengineering:concrete` | `immersiveengineering:concrete` |
| `floor_finish_public` | `minecraft:red_terracotta` | `supplementaries:stone_tile` | `supplementaries:stone_tile` | `tfmg:factory_floor` | `immersiveengineering:concrete_tile` | `quark:polished_jasper` |
| `floor_finish_service` | — | `minecraft:cobblestone` | `minecraft:stone_bricks` | `tfmg:factory_floor` | `tfmg:factory_floor` | `the_wasteland_reworked:aluminium_grate` |
| `roof_covering` | — | `quark:brown_shingles` | `quark:gray_shingles` | `quark:black_shingles` | `immersiveengineering:concrete_sheet` | `immersiveengineering:sheetmetal_aluminum` |
| `roof_structure` | — | `minecraft:oak_log` | `minecraft:oak_log` | `create:metal_girder` | `immersiveengineering:concrete_pillar` | `create:metal_girder` |
| `internal_column` | `minecraft:brick_wall` | `minecraft:oak_fence` | `minecraft:oak_log` | `create:metal_girder` | `immersiveengineering:concrete_pillar` | `create:metal_girder` |
| `chimney` | — | `minecraft:bricks` | `minecraft:bricks` | `tfmg:brick_smokestack` | `tfmg:metal_smokestack` | `tfmg:metal_smokestack` |
| `arch_head` | `minecraft:brick_slab` | `minecraft:stone_brick_stairs` | `quark:limestone_bricks_stairs` | `minecraft:brick_stairs` | — | — |

#### 5.1.1 Derivative naming is not uniform, and this matters

Measured against `docs/registry-inventory/block-ids.txt` on 2026-08-26, and confirmed while authoring the Karsic profile:

- **Immersive Engineering uses a prefix form** — `immersiveengineering:slab_concrete`, `stairs_concrete`, `wall_concrete`. It does **not** provide `concrete_slab`. A generator assuming the suffix form finds nothing.
- **Vanilla, Quark, TFMG and Supplementaries use the suffix form**, with irregular vanilla pluralisation (`minecraft:bricks` yields `minecraft:brick_slab`).
- Within Immersive Engineering the set is uneven: `concrete`, `concrete_brick`, `concrete_tile` and `concrete_leaded` have slab + stairs + wall; `concrete_reinforced` and every `sheetmetal_*` have **slab only**; `concrete_sprayed`, `concrete_chiseled`, `concrete_pillar` and `concrete_sheet` have **none**.

Pelagos is less exposed to this than Karsic because its dominant materials are brick, limestone, shingles and stone, all of which carry complete suffix-form sets. The exposure is concentrated in **P-IV**, which is the only stratum leaning on Immersive Engineering concrete.

The profile declares `derivative_schemes` tried in order, per-stratum `derivative_overrides` for the gaps, and per-role `needs` so a role is never failed for lacking a derivative it would not use. Verification is a P3 gate condition (§8.4), enforced by `scripts/validate_material_profile.py`, and is **never** a runtime fallback.

### 5.2 Openings

Pelagos openings are **vertically proportioned** — the single cheapest separator from Karsic's square punched grid.

| Role | Block | Notes |
|---|---|---|
| `glazing_domestic` | `minecraft:glass_pane` | Plain sash glazing, 1 wide × 3 high. The Pelagos default. |
| `glazing_shopfront` | `quark:white_framed_glass` | Full-width between piers, ground floor only. |
| `glazing_institutional` | `quark:brown_framed_glass` | P-II/P-III institutional. |
| `glazing_industrial` | `create:framed_glass` | Mills, sheds, patent glazing, sawtooth roof lights. |
| `glazing_contemporary` | `minecraft:tinted_glass` | P-V only, flush. |
| `glazing_failed` | `quark:dirty_glass_pane` | Collapse phase D/E substitution. |
| `door_domestic` | `minecraft:oak_door` | One per plot, on the street. Vary the colour reading via `dark_oak_door` on alternating plots. |
| `door_domestic_alt` | `minecraft:dark_oak_door` | The individuality of the terrace, cheaply. |
| `door_public` | `minecraft:dark_oak_door` | Institutional main entrance, usually paired. |
| `door_service` | `the_wasteland_reworked:industrial_door` | Yards, plant, loading. |
| `door_hardened` | `the_wasteland_reworked:containment_door` | Late containment retrofits only. |
| `shutter` | `minecraft:iron_trapdoor` | Arch units, lock-ups, shopfronts out of hours. |
| `railing` | `minecraft:iron_bars` | Area railings, area guards, park boundaries. **Extremely high-frequency Pelagos element.** |
| `area_grate` | `minecraft:copper_grate` | Pavement lights, coal-hole covers, area drainage. |

### 5.3 Municipal street kit

Legibility carrier #10. Where the Karsic kit reads as *state issue*, the Pelagos kit reads as *municipal* — the same small set of items maintained by a town, at ordinary frequency, never as a joke.

| Role | Block |
|---|---|
| `lamp_street` | `supplementaries:blackstone_lamp` |
| `lamp_street_post` | `minecraft:cobblestone_wall` (column) + `minecraft:lantern` |
| `lamp_interior` | `minecraft:lantern` |
| `lamp_service` | `immersiveengineering:cagelamp` |
| `bollard` | `quark:limestone_wall` |
| `railing` | `minecraft:iron_bars` |
| `gate_pedestrian` | `supplementaries:iron_gate` |
| `fence_yard` | `minecraft:oak_fence` |
| `fence_allotment` | `supplementaries:wicker_fence` |
| `fence_secure` | `the_wasteland_reworked:mesh_fence` |
| `awning` | `supplementaries:awning_green`, `_red`, `_blue`, `_black` (per shop, deterministic from seed) |
| `fascia_band` | `minecraft:dark_oak_planks` |
| `notice_board` | `supplementaries:notice_board` |
| `way_sign` | `supplementaries:way_sign` |
| `doormat` | `supplementaries:doormat` |
| `flower_box` | `supplementaries:flower_box` |
| `planter` | `supplementaries:planter` |
| `chain_barrier` | `minecraft:chain` |
| `rope` | `supplementaries:rope` |
| `platform_rail` | `bellsandwhistles:station_platform` |
| `transit_cladding` | `bellsandwhistles:metro_panel` |
| `transit_casing` | `bellsandwhistles:metro_casing` |
| `transit_window` | `bellsandwhistles:metro_window` |
| `wall_crane` | `create:metal_girder` + `minecraft:chain` |
| `cable_tray` | `the_wasteland_reworked:pipe_block` |
| `surface_pipe` | `tfmg:industrial_pipe` |
| `hazard_marking` | `tfmg:yellow_caution_block` |
| `scaffold_prop` | `immersiveengineering:steel_scaffolding_standard` |

`scaffold_prop` deserves a note: **propping is a Pelagos signature.** Steel rakers holding up a retained façade, props inside an arch, a scaffold walkway over an excavation. Wherever a Pelagos structure is doing something difficult with an inherited building, the props should be visible.

### 5.4 Ground contexts

`ground_plate()` in `scripts/structure_geometry_primitives_v2.py` takes a `site_context` from a fixed set. Pelagos needs three additions to `_GROUND_PALETTES`; this is a prerequisite listed in §14.3.

| Context | Status | Palette |
|---|---|---|
| `urban_paved` | existing | unchanged |
| `industrial_hardstanding` | existing | unchanged |
| `rural_worked` | existing | unchanged |
| `wilderness_undisturbed` | existing | unchanged |
| `waterfront` | existing | unchanged |
| **`pelagos_pavement`** | **new** | `minecraft:stone_bricks`, `minecraft:andesite`, `supplementaries:stone_tile`, `tfmg:asphalt` — flagged footway beside a metalled carriageway. Narrower and more finished than any Karsic surface. |
| **`pelagos_cobbled_yard`** | **new** | `minecraft:cobblestone`, `minecraft:mossy_cobblestone`, `supplementaries:raked_gravel`, `minecraft:gravel` — rear yards, mews, wharf setts, arch frontages. |
| **`pelagos_foreshore`** | **new** | `minecraft:gravel`, `minecraft:sand`, `minecraft:mud`, `minecraft:mossy_cobblestone` — tidal river edge below the embankment wall. **The one context where P-0 substrate may appear at grade** (rule 2 of §4.6 is satisfied because the player descends steps to reach it). |

### 5.5 Decay ladder

Collapse phases map to material substitutions. Applied in Pass P8 only, never earlier.

| Phase | Wall | Glazing | Roof | Ground |
|---|---|---|---|---|
| A — normal | profile as authored | as authored | as authored | as authored |
| B — early anomaly | as authored; first `minecraft:mossy_cobblestone` at wall base | as authored | first slipped slate: 1 in 20 `roof_covering` to air | moss at kerb lines |
| C — active containment | modern sealant patches over old fabric; `the_wasteland_reworked:lead_plating` at service penetrations | some `quark:dirty_glass_pane`; shutters down | as authored | `the_wasteland_reworked:hazard_concrete` on quarantine routes; `chain_barrier` across alleys |
| D — late containment | `railing` and `shutter` across ground openings; `barricade` at street mouths | mostly `quark:dirty_glass_pane`, some boarded in `minecraft:dark_oak_planks` | scorch course; more slipped slate | flood boards, sandbag lines, painted route markings |
| E — post-collapse | brick stands; render and cladding gone; heavy moss and `minecraft:vine`; P-V cladding fallen away to reveal the P-II/P-III shell beneath | empty frames, surviving `railing` | roof gone in patches, structure exposed, `minecraft:gravel` apron below | reclamation through pavement joints; silt at the tide line |

**The Pelagos decay rule.** Decay proceeds **newest stratum first**. At phase E, a P-II ⊕ P-V building should have lost its glass box entirely and be standing as brick, with the graft's fixings still visible on the old wall. That inversion — the modern layer dying while the old one survives — *is* the Compact's collapse thesis, expressed in material rather than in text.

### 5.6 The Londinium palette

Used only by the nine P-0 structures. Kept separate so it stays rare and instantly recognisable.

| Element | Blocks |
|---|---|
| Ragstone walling | `minecraft:cobblestone`, `minecraft:mossy_cobblestone` |
| **Bonding-tile course** | `minecraft:brick_slab` — one course every four, unbroken across the fragment. The signature. |
| Opus signinum floor | `minecraft:red_terracotta` |
| Tessellated panel | `minecraft:red_terracotta` + `minecraft:white_terracotta` + `minecraft:black_terracotta` in a simple border pattern |
| Hypocaust pilae | `minecraft:brick_wall` columns under a `minecraft:smooth_stone_slab` suspended floor |
| Burn layer | `supplementaries:ash` |
| Modern intervention | `immersiveengineering:steel_scaffolding_standard` props, `minecraft:chain` barrier, `supplementaries:notice_board`, `minecraft:glass_pane` display panel |

---

## 6. Massing grammar

### 6.1 The plot, not the bay — and no storey module at all

**Horizontal: the Pelagos plot is 5 blocks.**

The Compact has no panel grid because it has no catalogue. Its repeating unit is the **plot** — a house frontage, a shop frontage, a warehouse bay — and plots are separated by **party walls**, not by joints. A terrace is N plots long; a high street is a run of plots of slightly different heights and materials sharing party walls.

Five is chosen precisely *because* it does not divide into the converter's 16-block chunk cell. The Karsic program picks 4 so its panel joints never disagree across a converted seam (see that document §6.1); Pelagos has no continuous façade rhythm to disagree with. A chunk seam falls inside a room or on a party wall, where a full-height wall already interrupts everything. **The irregularity is free, and it is the point.**

**Vertical: Pelagos has no storey module, and does not use Lost Cities floor repetition.**

`convert_nbt_to_lostcities.py` slices into fixed 6-block bands and Lost Cities re-stacks the last authored band when `maxfloors` exceeds the authored count. The Karsic program exploits that to get a whole range of block heights from one authored panel block. **Pelagos deliberately does not.** Every Pelagos master is authored at its true height and converted with `minfloors = maxfloors = authored`, so no band is ever repeated.

This is not a limitation, it is the cultural contrast made mechanical:

| | Karsic | Pelagos |
|---|---|---|
| Source of height variety | Lost Cities floor repetition on one asset | plot composition and stratum mixing across many assets |
| Storey module | fixed 6, enforced by validator | none; true heights |
| Repeated band | required to be silhouette-identical | never repeated |

Working storey heights: **domestic 5**, commercial/institutional ground **6**, upper commercial **5**, industrial free-span **7–9**, P-IV civic **5**. These are authored values, not constraints — a Pelagos building whose program calls for a mezzanine or a half-landing simply has one.

### 6.2 Wall construction by stratum

| Stratum | Thickness | Reveal | Notes |
|---|---|---|---|
| P-0 | 2–3, irregular | — | Ragstone rubble with a `wall_banding` course every 4. Never squared off; the fragment has a broken end. |
| P-I | 2 | 1 | Timber frame with `daub` infill above a masonry base course. Irregular openings. |
| P-II | 2 | 1 | Brick with `dressing_stone` at openings and a string course at each floor line. Parapet or eaves cornice at the top. |
| P-III | 2 | 1 | Brick with segmental `arch_head` over every opening; `internal_column` grid inside; loading door stack on one elevation. |
| P-IV | 1 frame + 1 infill | 0 | Concrete `wall_frame` grid with panel infill; spandrel band in `wall_secondary`. |
| P-V | 1 cladding, standing 1 block clear of the host | 0 | Flush glazing. Fixings visible on the host wall so the graft reads as added — and so it reads correctly when it falls away at phase E. |

### 6.3 Standard elements

**Party wall, parapet, stack.** At every plot boundary in a terrace or high-street run: a full-height wall, carried **above the roof line** as a raised parapet 1 block proud of the roof plane, with a chimney stack seated on it — 2×1 in plan, rising 3 above the ridge. One stack per plot boundary. This assembly is legibility carrier #1 and it is mandatory on every P-I/P-II/P-III attached master.

**Pitched roof.** 45°, ridge parallel to the street for attached runs, gables at the ends of a run and at every change of height. `roof_covering` per stratum; `roof_structure` visible in the roof space where the program opens one. Flat roofs occur only on P-IV and P-V and only where the stratum justifies them.

**Sunken area.** P-II townhouses and institutional buildings get a 1-block sunken area across the street frontage, `railing` along its street edge, and steps down to a basement `door_service`. This one element does more to make a street read as Pelagos than any amount of brick detail.

**Shopfront.** Ground floor of high-street plots: `wall_primary` piers at the plot edges, full-width `glazing_shopfront` between them, a `fascia_band` course above, an `awning` over the pavement, and a recessed door. The upper floors keep the domestic 1×3 window rhythm, so the frontage reads as *shop below, home above*.

**Rear outshut.** Attached houses get a rear extension one plot wide and 3–4 deep, one storey lower than the main block, with its own lean-to roof. Behind it, a walled yard with a gate to the alley.

**Rear service alley.** Two-block-wide unpaved way behind every terrace run, walled on both sides, with gates, outbuildings, and bins. Reaches the template edge so consecutive placements connect.

**Retained façade.** Where a P-V graft is declared on a P-II/P-III host, the option exists to keep only the street wall and prop it: `scaffold_prop` rakers at 4-block spacing behind the façade, with the new structure standing clear behind. Reserve this for a small number of masters — it is a strong image and loses force if it is everywhere.

### 6.4 Silhouette rules by class

| Class | Rule |
|---|---|
| **Terrace run** | 4–8 plots. Every plot boundary gets a party wall, parapet, and stack. Ridge continuous, **eaves height varying by up to 1 block between plots** — a terrace that is perfectly level reads as a single building, which is wrong. |
| **Semi-detached pair** | Two plots, mirrored, shared party wall and stack, gap to the next pair, bay window on each front. |
| **High-street block** | 3–6 plots, differing heights and materials, shopfronts continuous at ground, upper floors individual. At least two strata across the run. |
| **Institutional campus** | Two or three wings of different strata, physically connected by a link corridor or bridge, arranged around a yard rather than on an axis. **Never symmetrical about a central axis** — that is the Karsic move. |
| **Mill / warehouse** | Rectangular multi-storey brick block, loading door stack on one elevation, wall crane, tall `chimney`, plus a lower sawtooth shed alongside. |
| **Viaduct** | Repeating brick arches on a straight or gently curved line, at least 6 arches, with arch units fitted into some and shuttered on others. |
| **Landmark** | Same rules as its class. Landmark status is expressed by **size, accretion, and approach**, never by adding ornament. |

---

## 7. Plan grammar

### 7.1 Circulation

Pelagos circulation is **narrow and awkward**, because it is what was left after the rooms. This is the direct inverse of the Karsic double-loaded 3-wide corridor.

| Element | Pelagos value | Notes |
|---|---|---|
| Domestic circulation | **1-wide hall**, stair against the party wall | A terrace house has no corridor, only a hall and a stair. |
| Institutional corridor | **2 wide**, single-loaded where the plan forces it | Rooms on one side, windows on the other, and a change of level or width where two building generations meet. |
| Link corridor / bridge | **2 wide**, glazed | Connects wings of different strata. **Every institutional campus must have at least one.** |
| Industrial floor | open, `internal_column` grid at 5 | Circulation is between columns, not in a corridor. |
| Cellar | **2 wide, 3 high**, brick barrel-vaulted | Under the pavement where the plot allows, with an area grate above. |
| Stairs | `encased_stairwell()`, never bare | V2 §3.2. Domestic stairs are width 1 in a shaft against the party wall; institutional are width 2. |

**The junction rule.** Wherever two strata meet inside one building, the circulation must *show* it: a step up or down of 1 block, a change of corridor width, a doorway cut through what is obviously a former external wall, or a short ramp. A Pelagos building whose interior flows smoothly between its strata has failed the central design thesis.

### 7.2 Room modules

| Module | Size | Used by |
|---|---|---|
| Terrace front room | 1 plot × 5 deep (5×5) | Domestic, ground and first floor. |
| Terrace back room | 1 plot × 4 deep (5×4) | Domestic. |
| Outshut | 1 plot × 4 deep, 1 storey | Kitchen, scullery, bathroom. |
| Shop unit | 1 plot × 8 deep | Ground floor of high-street plots; back half is store and staff. |
| Institutional room | 2 plots × 5 deep (10×5) | Classrooms, wards, offices, reading rooms. |
| Hall | 3 plots × 9 deep, 2 storeys clear | Church halls, assembly halls, baths, market halls. |
| Warehouse floor | free, 5-block column grid | Mills, warehouses, arch units. |
| Arch unit | 5 wide × 9 deep × 5 high, barrel-vaulted | `pel_086`. Fitted into a viaduct arch; workshop, lock-up, or café. |
| Plant squeeze | 3×3 minimum, in a leftover | Rear yard, roof, cellar corner. **Never in a purpose-built plant room** unless the stratum is P-IV or P-V. |

### 7.3 Mandatory interior facts

A Pelagos structure that omits an applicable item fails review.

1. **At least two strata are visible from inside.** Not just on the elevation — a player standing in the building must be able to see the join.
2. **Services are visibly retrofitted.** `cable_tray` and `surface_pipe` run on wall faces, around corners, through holes that were clearly cut later. Concealed services are a P-IV/P-V privilege only, and even then only in the newest wing.
3. **Every institutional campus has at least one link corridor or bridge** between wings of different strata.
4. **Every attached domestic run has a rear yard and alley access.**
5. **Cellars where the plot allows** — brick-vaulted, under the pavement, with an area grate or coal-hole cover visible at street level above. Not universal (unlike Karsic basements), but common.
6. **Storage in every leftover niche**, per canon: "storage in every leftover niche once supply chains begin failing." Understairs, landings, corridor ends, yard sheds.
7. **Furniture is mixed, not standardised.** This is the exact inverse of the Karsic rule. Use the `zvhouses:*` family across *several* wood types within one building, because the fittings arrived at different times.

### 7.4 Front-of-house / back-of-house

Pelagos back-of-house is **behind and squeezed** — a rear yard reached down a side passage, plant in whatever space was left, a staff entrance off the alley rather than off a service road. There is rarely enough room for a proper service yard, and that shortage should be visible: a delivery bay that a modern vehicle plainly could not use, bins in a passage, a fire escape crossing a light well.

For **P-IV** only, back-of-house may be **below**, in an undercroft or service basement — that was the era that could plan for it.

---

## 8. The conversion pass system

Nine ordered passes convert one base clean master into one Pelagos master. Each pass has a stable ID, a declared input and output artefact, an idempotency guarantee, a derived seed, and a validator. **Passes run in order and never skip.** A pass may be re-run at any time and must produce byte-identical output.

### 8.0 Determinism contract

```
seed(structure_id, pass_id, variant) =
    zlib.crc32(f"pelagos|{structure_id}|{pass_id}|{variant}".encode("utf-8")) & 0x7FFFFFFF
```

- No `random.random()` without an explicit `random.Random(seed)` instance.
- No iteration over `set` or `dict` where order affects placement; sort first.
- No wall-clock, no `os.urandom`, no PID, no environment.
- Worldgen placement salts, which must be literal integers in JSON, come from the reserved Pelagos range **79200000–79209999**. Verified unused against every existing `structure_set` salt in the pack as of 2026-08-26. Karsic holds 79100000–79109999.

Pelagos has one determinism hazard Karsic does not: **variation is part of the design.** Eaves heights vary between plots, door colours alternate, awning colours differ per shop, and furniture wood types are mixed within one building. Every one of those choices must be drawn from a seeded `random.Random`, never from an unseeded call, or the region will not be reproducible. Make the plot index part of the draw:

```
plot_rng = random.Random(seed(structure_id, "P2", variant) ^ (plot_index * 0x9E3779B1))
```

### 8.1 P0 — Regional assignment

| | |
|---|---|
| **Input** | `structure_library/catalog.json` (85 clean masters) |
| **Output** | `structure_library/regional/pelagos-assignment.json` |
| **Writes geometry** | No |
| **Validator** | `validate_regional_assignment.py` |

Assigns every base clean master one of four **conversion classes**:

- **N — Native.** The Compact builds this type as a core part of its identity. Full pass run, high pass intensity.
- **A — Adapted.** An equivalent exists but the program differs materially. Full pass run; P5 does the heavy lifting.
- **F — Foreign.** Appears rarely and deliberately, and must communicate why it is there (contract C6).
- **X — Excluded.** A named native substitute takes its slot.

**Pelagos excludes nothing. All 85 base masters convert.** That asymmetry with Karsic (which excludes three) is a finding, not an oversight, and it is worth stating plainly: the Directorate declined to build cul-de-sac suburbia, detached split-levels, and trailer parks because a planning authority decided not to. The Compact has no such filter — it built, converted, or absorbed every one of those forms at some point, because it never had the room or the authority to refuse. **"Excludes nothing" is itself a characterisation of the culture.**

The complete assignment is §10.

### 8.2 P1 — Program authoring

| | |
|---|---|
| **Input** | P0 assignment + base program where one exists |
| **Output** | `structure_library/programs/pel_<nnn>_<slug>.json` |
| **Writes geometry** | No |
| **Validator** | `validate_structure_programs.py`, extended with a Pelagos schema check |

Per V2 §3.1 the program file is a **required generation input**, not documentation written afterwards. A Pelagos program adds these fields:

```json
{
  "structure_id": "infinite_domain:pel_069_terraced_street",
  "culture": "pelagos",
  "conversion_class": "N",
  "strata": ["P-II", "P-V"],
  "londinium_substrate": false,
  "plot_count": 6,
  "repeatable_storey": false,
  "site_context": "pelagos_pavement",
  "foundation_profile": "partial_basement",
  "back_of_house": "behind_squeezed",
  "rear_alley": true,
  "retained_facade": false,
  "junction_expression": "step_down_at_party_wall_4",
  "signage_series": "ALBION TERRACE",
  "archetype": "...",
  "orientation": { ... },
  "<domain>_program": [ ... ],
  "damage_constraints": [ ... ],
  "review_gate": { ... }
}
```

`strata` is a **list with a minimum length of 2** (§4.4). `repeatable_storey` is `false` for every Pelagos master without exception (§6.1); the schema should reject `true`.

**No geometry pass may run for a structure whose program file is absent or fails schema validation.** This is the most important sequencing rule in the document — V2 §3.1 exists because the previous 84 assets were built without it.

### 8.3 P2 — Massing conversion

| | |
|---|---|
| **Input** | P1 program; base footprint/height from `catalog.json` |
| **Output** | Regenerated shell in `kubejs/data/infinite_domain/structure/pelagos/masters/<slug>_clean_master.nbt` |
| **Writes geometry** | **Yes — first geometry pass** |
| **Gate** | Visual Gate A equivalent (`HEAVY_REBUILD_DOCTRINE.md` §VII-A) |

Operations, in order:

1. Divide the frontage into `plot_count` plots of 5 blocks; the remainder becomes a corner return or an entry passage, **not** an evenly distributed adjustment. Real plot series do not divide neatly.
2. Assign each plot a stratum from the program's `strata` list, in contiguous runs of 1–3 plots, drawn from `plot_rng`.
3. Author true storey heights per plot (§6.1). Vary eaves height by up to 1 block between adjacent plots.
4. `terrain_footing()` with the program's `foundation_profile`.
5. Extrude each plot; carry the party wall full height at every boundary; raise the parapet 1 proud of the roof plane; seat one stack per boundary.
6. Pitch the roof at 45°, ridge parallel to the street, gables at run ends and at every eaves-height change.
7. Cut the sunken area on the street frontage where a P-II plot faces the street.
8. Add the rear outshut and walled yard; cut the rear alley to the template edge where `rear_alley` is true.
9. For institutional campuses: place wings of differing strata around a yard and connect them with a link corridor or bridge. **Do not make it symmetrical.**

**Footprint drift budget.** The Pelagos footprint may differ from its base master by at most **±20 %** in either axis; beyond that, re-derive `minimum_lot` in `catalog.json` and re-check the settlement archetypes in §11, because Lost Cities lot fitting is driven from those numbers. Drift beyond ±20 % is allowed but must be recorded in the roster with a reason.

Note that Pelagos will drift *negative* more often than Karsic drifts positive: the Compact's whole character is doing the same job in less space. Several A-class conversions should legitimately come out smaller than their base master.

### 8.4 P3 — Fabric conversion

| | |
|---|---|
| **Input** | P2 shell; `structure_library/regional/pelagos-material-profile.json` |
| **Output** | Same NBT, every structural block resolved from role → block |
| **Writes geometry** | Yes (substitution only, no shape change) |
| **Validator** | Profile completeness + registry existence |

Two gate conditions:

1. **Completeness.** Every role referenced by any Pelagos generator resolves for every stratum in the roster. A missing role is a hard failure, never a silent fallback.
2. **Registry existence.** Every block string, including every slab/stair/wall derivative, exists in `docs/registry-inventory/block-ids.txt`:

```bash
python scripts/validate_material_profile.py --culture pelagos --registry docs/registry-inventory/block-ids.txt
```

Pelagos has a third condition Karsic does not: **the profile must resolve per-plot, not per-building.** A high-street run with P-II and P-V plots resolves two profiles inside one master, and the resolver must key on the plot's stratum rather than the structure's.

#### 8.4.1 The retrofit path for already-converted assets

The 11,940 part files under `kubejs/data/infinite_domain/lostcities/parts/converted/` each carry a **local palette** that overrides the Lost Cities style palette. A style/palette change (§11.2) therefore **cannot** re-tint an already-converted building interior.

That gives a cheaper P3 path for assets not worth regenerating from NBT: a **palette remap manifest** rewriting only the `block` values in each part's local palette, leaving `slices` untouched.

```
scripts/remap_lostcities_palette.py \
    --manifest structure_library/regional/pelagos-palette-remap.json \
    --src kubejs/data/infinite_domain/lostcities/parts/converted \
    --dst kubejs/data/infinite_domain/lostcities/parts/pelagos
```

**This path is explicitly NOT a conversion.** Used alone it violates contract C3, and it is *especially* misleading for Pelagos, because re-tinting a building to brick produces something that looks superficially British while having none of the plot rhythm, party walls, pitched roof, or stratum layering that actually carry the identity. Permitted only for:

- **F-class** structures, where staying close to the base form is the point;
- **interim previews**, so a district can be looked at in-world before its geometry exists;
- **prop-scale and vehicle assets** whose identity really is carried by material.

Every asset taking the remap path alone is marked `fabric_only: true` in the roster and is barred from production approval until it has had a full P2–P8 run.

### 8.5 P4 — Envelope conversion

| | |
|---|---|
| **Input** | P3 fabric |
| **Output** | Openings and roof authored |
| **Validator** | `structure_geometry_lint.py` check 3 |

Per V2 §3.3 an opening is placed by the **same operation** that establishes the wall segment framing it. Use `wall_window()`; never place glass by coordinate.

Pelagos opening rhythm:

- Domestic: **1 wide × 3 high**, two per plot per storey, symmetric about the plot centre, `dressing_stone` jambs on P-II. This vertical proportion is the primary separator from Karsic's 2×2 grid and must never be compromised for convenience.
- Ground-floor domestic: one window plus one `door_domestic`, the door alternating between oak and dark oak by plot index.
- Shopfront: the §6.3 assembly — piers, full-width glazing, fascia, awning, recessed door.
- P-III: segmental `arch_head` over every opening, loading doors stacked vertically on one elevation with a `wall_crane` above the top one.
- P-IV: horizontal bands, spandrel panels between, no reveal.
- P-V: flush curtain glazing, standing clear of the host wall.
- Roof lights: P-III sawtooth sheds get `glazing_industrial` on the steep face, always facing the same way across the whole shed.

**Roofs are pitched by default.** Flat roofs only on P-IV and P-V. A Pelagos master with a flat roof and no P-IV/P-V stratum declared is a validator failure (§13.4, PV-9).

### 8.6 P5 — Plan conversion

| | |
|---|---|
| **Input** | P4 envelope; P1 program's room lists |
| **Output** | Interior zoning, circulation, partitions, vertical circulation |
| **Validator** | `structure_geometry_lint.py` checks 1–2, check 6 program-conformance ledger |

This is where an A-class Pelagos conversion becomes legitimately different from its base master. Operations:

1. Subdivide by plot first, circulation second. Party walls are structure, not partition.
2. Place stairs against party walls, in `encased_stairwell()` shafts, landing-connected at both ends.
3. Lay rooms per §7.2 within each plot.
4. **Author the stratum junctions** (§7.1 junction rule): step, width change, or a doorway cut through a former external wall, wherever two strata meet.
5. Route services on the surface — `cable_tray` and `surface_pipe` on wall faces, around corners, through cut holes.
6. Cut cellars where the plot allows, vaulted, with area grates at street level above.
7. Fill leftover niches with storage.
8. Dress each declared room so its purpose is legible at player scale (V2 §3.7 — per-room minimum, not a whole-building count).

**Check 6 is the real gate.** The generated room ledger must diff cleanly against the program's declared rooms.

### 8.7 P6 — Site conversion

| | |
|---|---|
| **Input** | P5 interior |
| **Output** | Lot surface, boundary, approach, external services |
| **Validator** | `structure_geometry_lint.py` check 5 |

1. `ground_plate()` with the program's `site_context` (§5.4).
2. `terrain_footing()` skirt — confirm it survived P2–P5 intact.
3. Boundary: `railing` on a low `plinth` wall for street frontages, `fence_yard` for rear yards, `fence_allotment` for allotments, `fence_secure` only for genuinely restricted sites.
4. **The pavement.** A 2-block `pelagos_pavement` strip along the street frontage, kerbed, with `bollard` at 6-block spacing, `lamp_street` at 12, and area grates where a cellar runs under it. This strip is to Pelagos what the heating main is to Karsic: the element that makes separate buildings read as one place.
5. Street furniture from §5.3, sparingly and consistently.
6. Rear alley cut to the template edge where declared, walled, with gates per plot.
7. Approach: no forecourt, no axis. The building meets the pavement directly, or is set back by exactly the depth of its sunken area.
8. Rail: where the program declares it, a brick retaining wall or embankment rather than a level siding — Pelagos rail is usually at a different level from the street.

### 8.8 P7 — Institutional dressing

| | |
|---|---|
| **Input** | P6 site |
| **Output** | Signage, naming, furniture, lighting, awnings, colour |
| **Validator** | Signage-grammar lint (§9.2) + `backed_sign()` backing check |

See §9. Every sign uses `backed_sign()`; an unbacked sign is a hard lint failure.

### 8.9 P8 — Collapse authoring

| | |
|---|---|
| **Input** | P7 dressed clean master (**immutable from here**) |
| **Output** | `kubejs/data/infinite_domain/structure/pelagos/<slug>.nbt` and, where declared, an occupation variant |
| **Validator** | `structure_geometry_lint.py` check 4 |

Per V2 §3.4 damage is an **authored event**. Never `t.clear()` on a box; never per-block random deletion as a primary method. Use `fracture_breach()`, which internally calls `retrofit_window_for_breach()`.

The Pelagos damage grammar, derived from §4.5:

| Damage archetype | Where it applies | Reads as |
|---|---|---|
| **Layered failure** | Any two-or-more-stratum building | The newest layer is gone; the oldest stands. P-V cladding lies in the yard with its fixings still on the P-II wall. **The default Pelagos archetype.** |
| **Legacy bypass** | Labs, hospitals, containment retrofits | Modern containment intact and sealed — and growth coming up through a Victorian drain, a coal chute, or a party-wall cavity that nobody mapped. The barrier is *undamaged*; that is the point. |
| **Overwhelmed conversion** | Warehouses, halls, civic buildings | Four uses stacked in one shell — commercial storage, ration depot, medical supply, evacuation shelter — with the fourth abandoned mid-fit-out. Signage from all four still up. |
| **Blocked artery** | Stations, ferry terminals, viaducts, bus stations | The evacuation route became the concentration point. Barriers, queue rails, abandoned luggage, a train or ferry still at the platform. |
| **Tidal breach** | Waterfront, embankment, dock, pumping station | Defence overtopped. A tide line on the brick 2 blocks up, silt inside, a failed gate, and the pump that could not keep up still in place. |
| **Retained façade** | High street, department store, office | The street wall standing on `scaffold_prop` rakers with sky behind it. Use sparingly. |
| **Neighbourhood improvisation** | Terraces, high streets, halls | Street-level self-organisation: alley mouths barricaded, a shared standpipe, painted notices, a school hall turned into a ward by people who lived nearby. |

**A Pelagos damage variant must preserve** at least one complete plot in any attached run, the rear alley route, and the visible junction between its strata, unless the program's `damage_constraints` explicitly says otherwise.

### 8.10 P9 — Assembly and integration

| | |
|---|---|
| **Input** | P8 variants |
| **Output** | Catalog entries, Lost Cities assets, citystyle and worldstyle wiring, tags |
| **Validator** | Full existing validator suite (§13) |

1. Append catalog entries to `structure_library/catalog.json` — `clean_master` + `damage_variant` per structure, following `structure-metadata.schema.json` exactly.
2. Run the existing converter against the Pelagos output tree:
   ```bash
   python scripts/convert_nbt_to_lostcities.py --all
   ```
   producing `parts/pelagos/`, `buildings/pelagos/`, `multibuildings/pelagos/`, `scattered/pelagos/`. Confirm every generated building carries `minfloors == maxfloors` (§6.1).
3. Author Pelagos palettes and style (§11.2), citystyles (§11.3), worldstyle selectors (§11.5).
4. Author biome tags and placement (§12).
5. Run the full gate.

**Nothing is production-approved until §13 passes.** `structure_library/production-approvals.json` is the only place approval is recorded.

---

## 9. Institutional identity, signage, and evidence

### 9.1 The naming grammar

The Directorate numbers things. **The Compact names them, and the names are inherited** — after what used to be on the site, after the family that built it, after a saint, a wharf, a field, or a road that no longer exists. Names outlive their referents, which is exactly the §4.1 thesis expressed in words.

```
<PLACE> <TYPE>          ALBION TERRACE  ·  GRANARY WHARF  ·  KILN ROW
THE <NOUN>              THE MALTINGS  ·  THE OLD BREWERY  ·  THE ARCHES
<NAME> AND SONS         HARLOW AND SONS  ·  BRAITHWAITE BROTHERS
<SAINT> <TYPE>          ST BRIDE'S HALL  ·  ST ANNE'S ROW
<TENANT>, <SHELL>       VCF — THE MALTINGS, UNIT 4
```

The last form is the important one. Existing project institutions — VCF, Atlas, PolyCore, Pleroma, Aevum, Helion, Blackglass, Asterion, Continuity — appear in Compact territory as **tenants of an older shell**, never as owners of a purpose-built campus. Where the Karsic rule subordinates the corporate name to a state ordinal, the Pelagos rule subordinates it to a *building that predates it*. Both readings say the same thing about the corporation's place in that society, and they say it differently.

Names are drawn deterministically from a fixed word-list per component, seeded per structure. Keep the lists short — a region with forty distinct place-name stems reads as a region; one with four hundred reads as a generator.

### 9.2 Signage rules

1. Every sign uses `backed_sign()`. An unbacked sign is a hard lint failure (check 2).
2. **Building names go on the frontage or the gable**, at first-floor level or above — not on a plinth beside the door. Karsic labels the entrance; Pelagos labels the building.
3. **Wayfinding uses room names and directions**, not section letters and floor numbers: `WARD 3`, `TO THE HALL`, `GOODS`, `PRIVATE`, `NO THOROUGHFARE`.
4. **At least two generations of signage coexist** on every institutional master. An older painted name, a mid-period enamel plate, a recent printed notice — all still up, because nobody took the old ones down.
5. **Ghost signs.** A faded painted advertisement on a gable end for a business that closed generations before the collapse. This is the single strongest Pelagos signage element and costs almost nothing: a rectangle of `minecraft:white_terracotta` weathered into the brick, with a `backed_sign` beneath it. **Put one on roughly one gable in six across the region.**
6. **No signage is decorative.** If a sign does not name a real thing that exists, or *used to exist and left the name behind*, it does not go up. The second clause is a Pelagos-only licence and it must be used honestly — the referent should be inferable.

### 9.3 Furniture

The Karsic rule is that the kit is fixed and reused verbatim. **The Pelagos rule is the inverse: fittings are mixed, because they arrived at different times.**

| Fitting | Blocks |
|---|---|
| Domestic seating and tables | `zvhouses:*_arm_chair`, `*_table`, `*_bench` — **two or three different wood types within one building** |
| Counters and shopfittings | `zvhouses:*_counter`, `*_countertop`, `*_countertop_drawer` |
| Shelving | `supplementaries:item_shelf` in short broken runs, not wall-to-wall |
| Shutters | `zvhouses:*_shutter` on domestic windows, matched per plot, varied between plots |
| Records and books | `minecraft:bookshelf`, `supplementaries:book_pile`, `supplementaries:blackboard` |
| Notice and display | `supplementaries:notice_board`, `supplementaries:way_sign` |
| Yard and allotment | `supplementaries:wicker_fence`, `supplementaries:planter`, `supplementaries:flower_box`, `supplementaries:jar` |
| Public house interior | `zvhouses:*_counter` bar run, `supplementaries:goblet`, `supplementaries:jar`, mixed stools |

The mixing must still be **deterministic** (§8.0): draw the wood type from `plot_rng`, never from an unseeded call.

### 9.4 Environmental evidence

Per canon §"Environmental evidence first", at least one major story point per quest-grade Pelagos structure must be readable without opening a book. Pelagos-specific examples, all buildable:

- Modern containment sheeting, sealed and intact, with growth coming up through a Victorian floor drain three metres behind it. **The barrier is undamaged.**
- A hall with four generations of signage still on the walls: parish notices, a ration schedule, a medical supply inventory, and an evacuation list — in that order, on the same wall.
- A hospital corridor that steps down one block and narrows, where a modern wing was joined to a school taken over next door.
- A ghost sign for a brewery on a gable, with a Pleroma cold-store retrofit visible through the same wall's later loading door.
- A tide line on brick two blocks above the floor, silt inside, and a flood gate stopped half-closed.
- A retained façade propped by steel rakers with nothing behind it, and the props themselves rusted through.
- A railway arch fitted out as a workshop, then as a shelter, with bunks against a wall that still has a lathe bolted to it.
- A cellar floor broken through to a ragstone wall with red bonding courses, a scaffold walkway over it, and a survey grid chalked on the stone.

### 9.5 Loot doctrine

Loot tables follow the pack convention: `infinite_domain:chests/pelagos/<slug>`.

- **Most Pelagos structures carry no chest.** Identity is carried by geometry; loot is not the reward for recognising a region.
- **Guaranteed evidence chests** exist only where a quest depends on the item, matching the abyssal program's precedent.
- **No progression shortcuts**, mirroring `pool_contract.no_progression_breaking_loot` in the abyssal catalog and `docs/WASTELAND_CITY_PROGRESSION_BYPASS_AUDIT.md`.
- **Regional presentation differs even where contents do not.** Karsic supplies arrive in numbered depot crates and sealed technical stores; the same items in Pelagos arrive in mixed commercial packaging, in a back room that was a shop before it was a store. Presentation is a P7 concern, contents are a balance concern, decided separately.

---

## 10. The Pelagos roster

**100 masters: all 85 base clean masters converted, none excluded, plus 15 native additions.**

Class key: **N** native · **A** adapted · **F** foreign/displaced. (No **X** entries — see §8.1.)
Strata use the §4.4 IDs; every entry declares at least two. `⊕` separates them.
Damage archetypes are from §8.9. **P-0** marks a Londinium-substrate carrier (nine total, §10.12).

### 10.1 Agricultural

| Base master | Cls | Pelagos ID | Pelagos identity | Strata | Damage | Note |
|---|---|---|---|---|---|---|
| `abandoned_orchard_cannery` | A | `pel_001_orchard_canning_works` | Orchard and Canning Works | P-I ⊕ P-III | overwhelmed conversion | Orchard, brick canning works, drying kiln with a cowl. |
| `decayed_farm` | A | `pel_002_mixed_farm` | Mixed Farm | P-I ⊕ P-II | neighbourhood improvisation | Stone farmhouse, barn, Dutch barn, yard, walled kitchen garden. |
| `decayed_ranch` | A | `pel_003_upland_stock_farm` | Upland Stock Farm | P-I ⊕ P-IV | layered failure | Drystone walls, field barns, one modern steel shed that fails first. |
| `ruined_grain_elevator` | A | `pel_004_maltings_grain_store` | Maltings and Grain Store | P-III ⊕ P-V | overwhelmed conversion | Brick maltings with a lucam hoist and kiln cowls. **Deliberately not a concrete elevator** — the contrast with `kar_004` carries a lot of regional reading. |
| `shattered_greenhouse_nursery` | N | `pel_005_glasshouse_range` | Glasshouse Range | P-II ⊕ P-V | layered failure | Victorian glasshouse range, modern polytunnels, brick potting sheds. |

### 10.2 Civic

| Base master | Cls | Pelagos ID | Pelagos identity | Strata | Damage | Note |
|---|---|---|---|---|---|---|
| `ae2_records_archive` | A | `pel_006_county_record_office` | County Record Office | P-III ⊕ P-V | legacy bypass | Converted institute with a modern strongroom inserted. |
| `emergency_relief_shelter` | A | `pel_007_hall_relief_centre` | Hall Relief Centre | P-I ⊕ P-IV | neighbourhood improvisation | A hall pressed into service by the people who lived around it. |
| `fire_station` | N | `pel_008_fire_station` | Fire Station | P-II ⊕ P-IV | blocked artery | Brick appliance-bay arches, hose tower, later flat-roof extension. |
| `roadside_church_cemetery` | N | `pel_009_parish_church_yard` | Parish Church and Churchyard | **P-0** ⊕ P-I | layered failure | Stone church, tower, lychgate, yew, walled yard, table tombs. **P-0 carrier:** the church stands on a Roman alignment; ragstone with bonding courses shows in the crypt. |
| `ruined_city_school` | N | `pel_010_board_school` | Board School | P-II ⊕ P-IV | overwhelmed conversion | Three-decker brick, separate entrances carved in stone, asphalt yard, later prefab classrooms in the playground. |
| `ruined_community_center` | N | `pel_011_community_hall` | Village and Community Hall | P-I ⊕ P-IV | neighbourhood improvisation | |
| `ruined_courthouse` | N | `pel_012_town_hall` | Town Hall and Magistrates' Court | P-II ⊕ P-V | blocked artery | Portland stone portico, clock, council chamber, modern rear extension. |
| `ruined_cyberware_clinic` | A | `pel_013_high_street_clinic` | High Street Clinic | P-II ⊕ P-V | legacy bypass | Aevum as a tenant in a converted bank (§9.1). |
| `ruined_hospital` | N | `pel_014_accreted_hospital` | Accreted Hospital | **P-II ⊕ P-IV ⊕ P-V** | overwhelmed conversion | Victorian block, interwar wing, 1970s tower, modern atrium, all connected. **The flagship three-stratum asset**; if only one Pelagos building is ever built to full quality, build this one. |
| `ruined_police_precinct` | N | `pel_015_police_station` | Police Station | P-II ⊕ P-IV | blocked artery | Brick front, lamp, custody wing, rear yard. |
| `ruined_ranger_station` | A | `pel_016_ranger_base` | Country Park Ranger Base | P-I ⊕ P-V | layered failure | |

### 10.3 Commercial

| Base master | Cls | Pelagos ID | Pelagos identity | Strata | Damage | Note |
|---|---|---|---|---|---|---|
| `abandoned_truck_stop` | A | `pel_017_motorway_services` | Motorway Services | P-IV ⊕ P-V | blocked artery | **Bridge restaurant spanning the carriageway.** Distinctive and instantly readable. |
| `bombed_hotel` | A | `pel_018_station_hotel` | Station Hotel | P-II ⊕ P-V | retained façade | Brick and render, bay windows, later tower behind. |
| `buried_bank_vault` | N | `pel_019_high_street_bank` | High Street Bank | P-II ⊕ **P-0** | legacy bypass | Stone-faced branch; the basement strongroom was cut into a Roman wall and built around it. **P-0 carrier.** |
| `cratered_downtown_intersection` | A | `pel_020_market_square` | Market Square | P-I ⊕ P-II ⊕ P-IV | neighbourhood improvisation | Market cross, war memorial, bollards, crater. |
| `grocery` | N | `pel_021_corner_shop` | Corner Shop | P-II | neighbourhood improvisation | Shop with a flat above, on a corner plot cut at an angle. **Core common structure — this one must be everywhere.** |
| `motel` | A | `pel_022_roadside_inn_lodge` | Roadside Inn and Lodge | P-I ⊕ P-V | layered failure | An old inn with a modern lodge block behind it. The lodge fails; the inn does not. |
| `ruined_department_store` | N | `pel_023_department_store` | Department Store | P-III ⊕ P-V | retained façade | Steel frame, faience façade, atrium, later cladding. |
| `ruined_mixed_use_block` | N | `pel_024_high_street_block` | High Street Block | P-II ⊕ P-III ⊕ P-V | overwhelmed conversion | **The everyday Pelagos street building.** Shopfronts continuous, upper floors individual, three strata across the run. |
| `ruined_office_tower` | A | `pel_025_podium_tower` | Podium Tower | P-IV ⊕ P-V | layered failure | 1960s tower on a podium; curtain wall and concrete fins. |
| `ruined_roadside_diner` | A | `pel_026_transport_cafe` | Transport Café | P-IV | neighbourhood improvisation | Single storey, flat roof, lorry parking. |
| `ruined_shopping_mall` | A | `pel_027_shopping_precinct` | Shopping Precinct | P-IV ⊕ P-V | blocked artery | 1970s precinct with a subway underpass and a multi-storey deck above. |
| `sunken_city_front` | N | `pel_028_river_frontage` | River Frontage | **P-0** ⊕ P-III | tidal breach | Embankment wall, stairs to the foreshore, flood gate. **P-0 carrier:** a Roman quay timber line shows at low water. |
| `toppled_skyscraper` | A | `pel_029_toppled_tower` | Toppled Tower on a Terrace | P-II ⊕ P-V | retained façade | The tower came down across a terraced street. |
| `trade_outpost` | A | `pel_030_market_cross_auction_mart` | Market Cross and Auction Mart | P-I ⊕ P-III | overwhelmed conversion | |

### 10.4 Highway

| Base master | Cls | Pelagos ID | Pelagos identity | Strata | Damage | Note |
|---|---|---|---|---|---|---|
| `delivery_van` | N | `pel_031_delivery_van` | Delivery Van | prop | — | Short-wheelbase panel van. |
| `destroyed_refugee_convoy` | N | `pel_032_coach_convoy` | Coach Convoy | P-IV kit | blocked artery | Coaches and vans nose-to-tail on a dual carriageway that had nowhere to go. |
| `gas_station` | N | `pel_033_petrol_station` | Petrol Station | P-IV ⊕ P-V | layered failure | Canopy, shop, air and water bay, forecourt. |
| `mountain_pass_terminator` | A | `pel_034_moorland_road_end` | Moorland Road End | P-I ⊕ P-IV | neighbourhood improvisation | Cattle grid, drystone wall, passing place, a gate that stops the road. |
| `ruined_bus_terminal` | N | `pel_035_bus_station` | Bus Station | P-IV | blocked artery | Sawtooth stands, travel office, concrete canopy. |
| `sunken_highway_interchange` | A | `pel_036_motorway_junction` | Motorway Junction | P-IV | blocked artery | Roundabout and slip roads over a cutting. |
| `wasteland_weigh_station` | A | `pel_037_lay_by_check_area` | Lay-by Check Area | P-IV | blocked artery | Weighbridge, portacabin, lay-by off the carriageway. |
| `wrecked_sedan` | N | `pel_038_saloon_car` | Saloon Car | prop | — | |

### 10.5 Industrial

| Base master | Cls | Pelagos ID | Pelagos identity | Strata | Damage | Note |
|---|---|---|---|---|---|---|
| `abandoned_oil_field` | A | `pel_039_coastal_oil_terminal` | Coastal Oil Terminal | P-IV ⊕ P-V | tidal breach | Pipeline landfall, tank farm, jetty. Compact oil is offshore; this is where it came ashore. |
| `abandoned_quarry` | N | `pel_040_stone_slate_quarry` | Stone and Slate Quarry | P-I ⊕ P-III | layered failure | Inclines, processing shed, spoil runs. |
| `bombed_data_center` | N | `pel_041_exchange_colocation` | Telephone Exchange and Colocation | P-II ⊕ **P-0** | legacy bypass | Modern racks in an Edwardian shell; the basement plant room was cut into a Roman cellar. **P-0 carrier** — data infrastructure sitting literally on the oldest infrastructure. |
| `cold_industrial_mountain_port` | A | `pel_042_northern_fishing_port` | Northern Fishing Port | P-I ⊕ P-III | tidal breach | Harbour wall, ice house, net lofts. |
| `collapsed_mine_entrance` | N | `pel_043_colliery` | Colliery | P-III ⊕ P-IV | overwhelmed conversion | Brick winding house, headgear, spoil tip, pit baths. |
| `corporate_warehouse` | N | `pel_044_distribution_shed` | Distribution Shed | P-IV ⊕ P-V | overwhelmed conversion | Estate shed, dock levellers, office snout at the front corner. |
| `crashed_cargo_airship` | A | `pel_045_downed_cargo_airship` | Downed Cargo Airship | prop | blocked artery | |
| `create_factory` | N | `pel_046_converted_mill` | Converted Mill | **P-III ⊕ P-V** | layered failure | A modern production line inside a brick mill. **The flagship "older shell, newer function" asset** — legibility carrier #5 at full strength. |
| `decayed_logging_camp` | A | `pel_047_plantation_yard` | Forestry Plantation Yard | P-I ⊕ P-IV | layered failure | |
| `excavator_pit` | A | `pel_048_aggregates_pit` | Aggregates Pit | P-IV ⊕ P-V | layered failure | Conveyor, wash plant, settling ponds. |
| `industrial_facility` | N | `pel_049_estuary_chemical_works` | Estuary Chemical Works | P-III ⊕ P-V | tidal breach | |
| `municipal_incinerator` | N | `pel_050_energy_from_waste` | Energy-from-Waste Plant | P-IV ⊕ P-V | layered failure | Clad stack, tipping hall, visitor viewing gallery nobody used. |
| `nuclear_research_annex` | N | `pel_051_coastal_station_annex` | Coastal Station Annex | P-IV ⊕ P-V | tidal breach | Sea-water intake, hard perimeter, shingle bank. |
| `remote_sawmill` | A | `pel_052_estate_sawmill` | Estate Sawmill | P-I ⊕ P-III | layered failure | |
| `ruined_fuel_depot` | N | `pel_053_coastal_tank_farm` | Coastal Tank Farm | P-IV | tidal breach | Bunded tanks, jetty pipeline, foam monitors. |
| `scrapyard` | N | `pel_054_breakers_yard` | Breaker's Yard | P-III ⊕ P-IV | overwhelmed conversion | Behind and between railway arches. |
| `service_garage` | N | `pel_055_arch_garage` | Arch Garage | P-III | overwhelmed conversion | An MOT garage fitted into a viaduct arch or a brick lock-up. |
| `warm_industrial_mountain_port` | A | `pel_056_southern_commercial_port` | Southern Commercial Port | P-III ⊕ P-V | tidal breach | |

### 10.6 Military

| Base master | Cls | Pelagos ID | Pelagos identity | Strata | Damage | Note |
|---|---|---|---|---|---|---|
| `battle_tank` | N | `pel_057_compact_tank` | Compact Tank | prop | — | |
| `bunker_network` | N | `pel_058_regional_seat_of_government` | Regional Seat of Government | P-IV | legacy bypass | Hardened sub-surface complex, plant, map room, a surface entrance that looks like nothing. |
| `military_checkpoint` | N | `pel_059_road_control_point` | Road Control Point | P-IV | blocked artery | |
| `mountain_biohazard_lab` | A | `pel_060_isolated_research_establishment` | Isolated Research Establishment | P-II ⊕ P-IV ⊕ P-V | legacy bypass | A plateau establishment grown from an interwar site. Three strata; containment fitted to a building that predates the concept. |
| `mountain_military_complex` | A | `pel_061_former_airfield_depot` | Former Airfield Depot | P-IV ⊕ P-V | overwhelmed conversion | Hangars, hardstanding, watch office, later civilian occupation. |

### 10.7 Miscellaneous and railway

| Base master | Cls | Pelagos ID | Pelagos identity | Strata | Damage | Note |
|---|---|---|---|---|---|---|
| `collapsed_airship_terminal` | N | `pel_062_airship_shed_mast` | Airship Shed and Mast | P-III ⊕ P-IV | blocked artery | An enormous riveted shed with a mooring mast alongside. Genuinely a Compact form. |
| `survivor_cache` | A | `pel_063_allotment_shed_cache` | Allotment Shed Cache | P-I | neighbourhood improvisation | |
| `collapsed_subway_station` | N | `pel_064_underground_station` | Underground Station | **P-0** ⊕ P-II ⊕ P-IV | blocked artery | Street ticket hall, cut-and-cover box, tiled platforms. **P-0 carrier:** the deepest running tunnel met a Roman wall and was diverted around it — the diversion is walkable. Landmark. |
| `elevated_rail_collapse` | N | `pel_065_viaduct_collapse` | Viaduct Collapse | P-III | blocked artery | **Brick arches with a collapsed span.** The defining Pelagos motif; treat as a priority asset. |
| `freight_depot` | N | `pel_066_goods_shed` | Goods Shed | P-III ⊕ P-IV | overwhelmed conversion | Wagon turntable, brick office, wall crane. |

### 10.8 Residential

| Base master | Cls | Pelagos ID | Pelagos identity | Strata | Damage | Note |
|---|---|---|---|---|---|---|
| `abandoned_culdesac` | N | `pel_067_suburban_close` | Suburban Close | P-IV ⊕ P-V | layered failure | Semis, garages, turning head, conservatories added later. The Directorate refused to build this; the Compact built thousands. |
| `blown_apartment_complex` | A | `pel_068_council_tower_deck` | Council Tower and Deck | P-IV | layered failure | Tower on a podium with deck access, drying areas, and a shop unit at the base. |
| `bungalow` | N | `pel_069_interwar_bungalow` | Interwar Bungalow | P-II ⊕ P-IV | layered failure | Bay window, hipped roof, front garden, later rear extension. |
| `ruined_rowhouse_block` | N | `pel_070_terraced_street` | Terraced Street | **P-II ⊕ P-V** | neighbourhood improvisation | **The Pelagos flagship.** Party walls, stack rhythm, rear alley, outhouses, and one plot re-fronted in the last decade. Should be the most common structure in the region by a wide margin. |
| `shattered_luxury_condo` | A | `pel_071_warehouse_apartments` | Warehouse Conversion Apartments | P-III ⊕ P-V | layered failure | Loading doors glazed in, wall crane retained as a feature, new balconies bolted on. |
| `split_level_house` | A | `pel_072_semi_detached_pair` | Semi-Detached Pair | P-II ⊕ P-IV | layered failure | Mirrored plan, shared stack, bay windows, differing extensions. |
| `tenement_courtyard` | A | `pel_073_model_dwellings` | Model Dwellings | P-II ⊕ P-IV | neighbourhood improvisation | Philanthropic block around a court, external balcony access, shared laundry. |
| `trailer_park` | A | `pel_074_static_caravan_park` | Static Caravan Park | P-IV ⊕ P-V | tidal breach | Coastal holiday park: rows of statics, a clubhouse, a sea wall that failed. |

### 10.9 Utility and infrastructure

| Base master | Cls | Pelagos ID | Pelagos identity | Strata | Damage | Note |
|---|---|---|---|---|---|---|
| `broken_solar_field` | A | `pel_075_solar_farm` | Solar Farm | P-IV ⊕ P-V | layered failure | On former farmland with the hedge lines retained — the field boundaries are older than the panels. |
| `city_electrical_substation` | N | `pel_076_brick_substation` | Brick Substation | P-II ⊕ P-IV | layered failure | Brick enclosure with a lattice gantry over it. |
| `city_water_treatment_plant` | N | `pel_077_filter_beds_works` | Filter Beds and Works | P-III ⊕ P-V | legacy bypass | Victorian filter beds beside modern plant, sharing a culvert nobody mapped. |
| `district_heating_station` | A | `pel_078_energy_centre` | Energy Centre | P-IV ⊕ P-V | layered failure | A small CHP energy centre in a regeneration scheme. **Deliberately minor** — the contrast with `kar_075`, a landmark every Karsic district is built around, is one of the sharpest regional readings available. |
| `hydroelectric_refuge_dam` | A | `pel_079_reservoir_dam` | Upland Reservoir Dam | P-II ⊕ P-IV | tidal breach | Masonry dam, valve tower, draw-off, a drowned village showing at low water. |
| `pancaked_parking_structure` | N | `pel_080_multi_storey_car_park` | Multi-Storey Car Park | P-IV | layered failure | Spiral ramp, exposed aggregate, pedestrian bridge to the precinct. |
| `radio_mast` | N | `pel_081_relay_station` | Relay Station | P-IV | layered failure | Guyed mast, equipment hut, compound fence. |
| `shattered_wind_farm` | N | `pel_082_wind_farm` | Wind Farm | P-IV ⊕ P-V | layered failure | **The Compact builds these.** The contrast with Karsic's F-class "imported wind array" tells the story of two energy politics without a word of text. |
| `wasteland_fire_lookout` | A | `pel_083_coastguard_lookout` | Coastguard Lookout | P-II ⊕ P-V | tidal breach | |
| `wasteland_water_tower` | N | `pel_084_brick_water_tower` | Brick Water Tower | P-II ⊕ P-IV | layered failure | Brick shaft, corbelled top, enclosed tank. Contrast with `kar_081`'s bare steel column. |
| `wilderness_substation` | N | `pel_085_rural_substation` | Rural Substation | P-II ⊕ P-IV | layered failure | |

### 10.10 Native additions

The structures the base set does not contain but the culture requires. **Without at least the first five, the region reads as a reskin.**

| Pelagos ID | Pelagos identity | LC target | Strata | Priority | Note |
|---|---|---|---|---|---|
| `pel_086_railway_arch_units` | Railway Arch Units | multibuilding | P-III ⊕ P-V | **Mandatory** | Viaduct arches fitted out as workshops, lock-ups, and a café, some shuttered. Legibility carrier #4 at full strength and one of the cheapest high-impact assets in either program. Must tile with `pel_065`. |
| `pel_087_public_house` | Public House | building | P-I ⊕ P-II | **Mandatory** | Corner site, painted name board, bay windows, a yard, a cellar with a pavement drop hatch. Its absence would be conspicuous. |
| `pel_088_street_furniture_set` | Street Furniture Set | scattered | P-II ⊕ P-IV | **Mandatory** | Post box, kiosk, bollards, bench, litter bin, lamp standard. Ordinary municipal equipment at ordinary frequency (§4.2). Highest-frequency identity carrier in the program. |
| `pel_089_bus_shelter_and_stop` | Bus Shelter | scattered | P-IV ⊕ P-V | **Mandatory** | Small, glazed, with a timetable case. |
| `pel_090_londinium_wall_fragment` | Londinium Wall Fragment | multibuilding | **P-0** ⊕ P-V | **Mandatory** | The landmark where the substrate is the point rather than the surprise (§4.6 rule 4). A length of ragstone wall with red bonding courses in a sunken enclosure, scaffold walkway over it, survey grid chalked on the stone, notice boards, and a modern building stopped short around it. **P-0 carrier.** |
| `pel_091_war_memorial_cross` | War Memorial | scattered | P-II ⊕ P-IV | High | Stone cross or obelisk on a plinth with a name panel, railings, small paved setting. The Compact's equivalent of `kar_092` at a fraction of the scale — which is itself the point. |
| `pel_092_public_library` | Public Library | multibuilding | **P-0** ⊕ P-II ⊕ P-V | High | Endowed brick-and-stone library with a modern rear extension and a Roman fragment displayed behind glass in the entrance hall. **P-0 carrier.** |
| `pel_093_allotments` | Allotments | multibuilding | P-I ⊕ P-IV | High | Plots, sheds of scavenged material, wicker fences, water butts, a communal hut. Reads as ordinary life continuing, which canon's "worth saving" rule explicitly asks for. |
| `pel_094_canal_lock_and_wharf` | Canal Lock and Wharf | multibuilding | **P-0** ⊕ P-II ⊕ P-III | Medium | Lock chamber, gates, lock-keeper's cottage, brick wharf and crane. The cutting exposed a Roman road in the bank. **P-0 carrier.** |
| `pel_095_seawall_and_promenade` | Sea Wall and Promenade | multibuilding | P-II ⊕ P-IV | Medium | Curved sea wall, promenade, shelters, steps to the beach, a flood gate. The tidal-breach archetype at its clearest. |
| `pel_096_victorian_pumping_station` | Pumping Station | multibuilding | P-III ⊕ P-V | Medium | Ornate brick engine house with a tall chimney and decorative ironwork inside. One of the finest forms in the vocabulary; worth building well. |
| `pel_097_market_hall` | Market Hall | multibuilding | P-III ⊕ P-V | Medium | Iron-and-glass roof over a brick shell, stalls below, a later mezzanine. |
| `pel_098_prefab_estate` | Prefab Estate | multibuilding | P-IV ⊕ P-V | Medium | Post-war prefabricated bungalows on a grid, gardens grown wild, each individualised by its occupants. |
| `pel_099_almshouse_row` | Almshouse Row | multibuilding | P-I ⊕ P-II | Medium | Low row around a court with a chapel at one end and a founder's plaque. |
| `pel_100_municipal_baths` | Municipal Baths | multibuilding | **P-0** ⊕ P-II ⊕ P-IV | Medium | Brick and glazed brick, pool hall with a barrel roof, slipper baths, later filtration plant. Built over a spring the Romans also used. **P-0 carrier.** |

### 10.11 Roster accounting

| | Count |
|---|---|
| Base clean masters in `catalog.json` | 85 |
| Converted (N + A + F) | 85 |
| — of which N (native) | 48 |
| — of which A (adapted) | 37 |
| — of which F (foreign) | 0 |
| Excluded (X) | **0** |
| Native additions | 15 |
| **Pelagos masters total** | **100** |
| Pelagos damage variants (1 per master) | 100 |
| **Catalog entries added** | **200** |

Two asymmetries with Karsic are deliberate and should be kept:

- **Pelagos excludes nothing; Karsic excludes three.** §8.1 explains why. The Directorate had a planning authority that could decline a building type; the Compact never did.
- **Pelagos has no F-class entries; Karsic has two.** The Compact absorbed foreign forms rather than fencing them off, so foreign influence in Pelagos appears as *a stratum inside a building*, never as a separate structure behind a wire fence. Karsic structures appearing in Pelagos territory are handled separately in §12.5.

### 10.12 Londinium substrate carriers

Nine, capped (§4.6):

`pel_009_parish_church_yard` · `pel_019_high_street_bank` · `pel_028_river_frontage` · `pel_041_exchange_colocation` · `pel_064_underground_station` · `pel_090_londinium_wall_fragment` · `pel_092_public_library` · `pel_094_canal_lock_and_wharf` · `pel_100_municipal_baths`

Note the spread: a church, a bank, a river edge, a data facility, a station, a landmark, a library, a canal, and a bath house. Sacred, commercial, tidal, technical, transit, civic, and infrastructural — the substrate is under *everything*, which is the reading. A tenth dilutes it; validator check PV-10 enforces the cap.

---

## 11. Lost Cities integration

### 11.1 File layout

```
structure_library/regional/
    pelagos-assignment.json            # P0
    pelagos-material-profile.json      # P3, resolves per plot stratum
    pelagos-massing-grammar.json       # P2 constants: plot=5, thicknesses, roof pitch
    pelagos-name-lists.json            # P7 deterministic name components
    pelagos-palette-remap.json         # P3 retrofit path only
structure_library/programs/
    pel_<nnn>_<slug>.json              # P1, one per master

kubejs/data/infinite_domain/structure/pelagos/
    masters/<slug>_clean_master.nbt    # P2-P7 output, immutable after P7
    <slug>.nbt                         # P8 damage variant

kubejs/data/infinite_domain/lostcities/
    styles/pelagos_standard.json
    palettes/pelagos_*.json
    citystyles/pelagos_*.json
    parts/pelagos/...                  # P9, generated
    buildings/pelagos/...              # P9, generated
    multibuildings/pelagos/...         # P9, generated
    scattered/pelagos/...              # P9, generated

kubejs/data/lostcities/lostcities/worldstyles/standard.json   # extended, not replaced

scripts/regional/
    pelagos_material_profile.py        # per-plot role -> block resolution
    pelagos_massing.py                 # P2 plot/party-wall/roof primitives
    pelagos_plan.py                    # P5 room modules, junction expression
    pelagos_dressing.py                # P7 signage, naming, awnings, furniture
    pelagos_damage.py                  # P8 archetype operators
    londinium_substrate.py             # P-0 fragment generator, used by 9 masters
scripts/generate_pelagos_sites.py      # the driver
scripts/validate_regional_structures.py
scripts/validate_material_profile.py
scripts/remap_lostcities_palette.py
```

**Nothing under `converted/` is modified.** Pelagos assets live in their own sibling trees so the existing 14,585-file corpus stays byte-stable and diffable.

`londinium_substrate.py` is deliberately its own module rather than a branch inside `pelagos_massing.py`: it is used by only nine masters, it has its own palette (§5.6), and its four rules (§4.6) are easier to enforce in one place than to re-check at nine call sites.

### 11.2 Style and palettes

Verified from `mods/lostcities-1.21-8.4.1.jar`: a Lost Cities **style** is a list of palette *slots*, each a weighted choice among palettes; a **palette** maps a character to a block, optionally with `damaged` and `variant`. `citystyle.style` selects the style.

`infinite_domain:pelagos_standard` takes five slots, mirroring `lostcities:standard`:

| Slot | Purpose | Palettes |
|---|---|---|
| 0 | common | `pelagos_common` — filler `#`, rubble `}`, ironbars, glowstone |
| 1 | default | `pelagos_default` — street, border, wall, streetbase, streetvariant |
| 2 | wall family | `pelagos_estate_brick`, `pelagos_industrial_brick`, `pelagos_old_fabric`, `pelagos_postwar_civic`, `pelagos_contemporary` — weighted 4 / 3 / 2 / 2 / 1 |
| 3 | glazing | `pelagos_glass_sash`, `pelagos_glass_shopfront`, `pelagos_glass_industrial` |
| 4 | glazing side-variant | `pelagos_glass_side_brick`, `pelagos_glass_side_stone` |

Compare the slot-2 weighting with Karsic's 6/1/2/2, which lets K-III win six times out of eleven so its between-building fabric is monotonous on purpose. Pelagos spreads 4/3/2/2/1 across five palettes, so **no wall family wins outright**. Two neighbouring blocks in a Pelagos city will usually not match, and that is the mechanical expression of §4.1.

**Critical limitation, stated once so it is not rediscovered later.** Converted parts carry a **local palette** (`palette.palette` in each part JSON), and a local palette overrides the style. The style/palette layer above governs *Lost-Cities-generated fabric* — streets, borders, filler, rubble, corridors, parks, rails, the between-building world — and **not** the interiors of converted buildings. Building fabric comes from P3, at the NBT level. Both layers are required; neither substitutes for the other.

### 11.3 Citystyles

Eight Pelagos district archetypes, each inheriting a shared `infinite_domain:pelagos` base (which itself inherits `lostcities:citystyle_common`), following the existing `wasteland_*` pattern.

| Citystyle | District | Draws from |
|---|---|---|
| `pelagos_terraced_district` | Dense inner residential | `pel_070`, `pel_073`, `pel_021`, `pel_087`, `pel_010`, `pel_088`, `pel_091`, `pel_055` |
| `pelagos_high_street` | Mixed-use commercial core | `pel_024`, `pel_021`, `pel_023`, `pel_019`, `pel_087`, `pel_013`, `pel_097`, `pel_088` |
| `pelagos_industrial_estate` | Industry and works | `pel_044`, `pel_046`, `pel_049`, `pel_054`, `pel_050`, `pel_066`, `pel_076`, `pel_096` |
| `pelagos_rail_quarter` | Viaducts, arches, goods | `pel_065`, `pel_086`, `pel_066`, `pel_055`, `pel_054`, `pel_035`, `pel_064`, `pel_018` |
| `pelagos_dockside` | Port and waterfront | `pel_028`, `pel_056`, `pel_042`, `pel_053`, `pel_071`, `pel_094`, `pel_095`, `pel_096` |
| `pelagos_civic_campus` | Institutional | `pel_014`, `pel_012`, `pel_092`, `pel_100`, `pel_008`, `pel_015`, `pel_006`, `pel_009` |
| `pelagos_suburban_estate` | Outer residential | `pel_067`, `pel_072`, `pel_069`, `pel_098`, `pel_080`, `pel_093`, `pel_089`, `pel_033` |
| `pelagos_village_and_coast` | Small settlement and coast | `pel_002`, `pel_009`, `pel_087`, `pel_099`, `pel_083`, `pel_095`, `pel_074`, `pel_034` |

`structure_library/settlement-archetypes.json` gains eight matching archetype records so `scripts/validate_settlement_archetypes.py` can compile the selectors from evidence rather than by hand.

### 11.4 Settings that carry the culture

Not cosmetic knobs; each encodes a stated rule, and each is chosen against its Karsic counterpart.

| Setting | Pelagos | Karsic | Encodes |
|---|---|---|---|
| `streetblocks.width` | **6** | 10 | Inherited street widths. The Compact's streets were laid out before the vehicles that had to use them. **Runtime-unverified — check in-world before locking.** |
| `buildingsettings.buildingchance` | **0.55** | 0.40 | Pelagos is denser in *coverage* — attached buildings with no gaps — while being smaller in mass per building. |
| `buildingsettings.mincellars` | **0** | 1 | Cellars are common but not universal (§7.3 rule 5), unlike Karsic basements which are doctrine. |
| `buildingsettings.maxcellars` | 2 | 2 | Vaulted cellar plus a sub-cellar where the plot allows. |
| `buildingsettings.minfloors` / `maxfloors` | **2 / 4** | 3 / 9 | A nominal range only. **Every Pelagos building JSON pins `minfloors == maxfloors` to its authored height (§6.1), so the citystyle range never actually engages.** It is set narrow anyway so that any future asset which forgets to pin cannot produce a nine-storey terrace. |
| `explosionchance` | **0.06** | 0.02 | Higher. Blast damage in dense inherited fabric is part of the Compact's story in a way it is not for the Directorate. |
| `parkblocks.parkchance` | low, `avoidfoliage: false` | moderate | Squares and churchyards, not courtyards. Small, planted, enclosed. |
| `multisettings.correctstylefactor` | **0.75** | 0.95 | **The single most important setting in this table.** Pelagos mixes; the Directorate does not. Lowering style coherence here is the mechanical expression of §4.1. |
| `settings.railwayavoidance` | `ignore` | `ignore` | Rail runs through both regions — but in Pelagos it runs *above* the street on a viaduct, which is a geometry decision, not a setting. |
| `stuff_tags` | `rubble` | `rubble` | Unchanged. |

### 11.5 Worldstyle wiring

`CityStyleSelector` in the Lost Cities jar carries an optional **`biomes`** field of type `BiomeMatcher` (`if_all` / `if_any` / `excluding`). That is the whole mechanism — no mod change, no mixin, no fork.

Extend the existing `kubejs/data/lostcities/lostcities/worldstyles/standard.json` `citystyles` array. Do **not** create a second worldstyle; the profile selects exactly one.

```json
{ "factor": 1.0, "citystyle": "infinite_domain:pelagos_terraced_district",
  "biomes": { "if_any": ["#infinite_domain:pelagos_region_biomes"] } },
{ "factor": 1.0, "citystyle": "infinite_domain:pelagos_high_street",
  "biomes": { "if_any": ["#infinite_domain:pelagos_region_biomes"] } }
```

…and add `"excluding": ["#infinite_domain:karsic_region_biomes", "#infinite_domain:pelagos_region_biomes"]` to each of the seven existing `wasteland_*` selectors, so central-continent styles stop appearing inside either regional territory.

**That `excluding` edit is the single point where the two regional programs touch the same file.** Sequence it so whichever program lands first makes that edit, and the second only appends its own selectors. Doing it twice will produce a duplicated or conflicting matcher.

Weighting note: `pelagos_terraced_district` should carry a **higher factor than any other Pelagos citystyle** — 2.0 against 1.0 for the rest. The terraced street is the region's flagship (§10.8) and a Compact that does not feel predominantly terraced has failed carrier #3.

---

## 12. Placement and worldgen

### 12.1 The geography, as it actually exists

Read out of `datapacks/gradient_ocean_pack/data/custom_worldgen/worldgen/density_function/`:

| Region | Condition | Function |
|---|---|---|
| Start city | `start_city_mask` | humidity forced to 2.0 |
| Mountain ring | `3200 <= r < 3900` | `mountain_ring_mask`, humidity forced to 1.25 |
| Central continent | `r <= 4000`, feathering to 0 at `r = 4800` | `central_continent_mask` |
| **East / West land lobes** | `abs(x) > abs(z)` — full strength at `abs(x) - abs(z) >= 250` | `east_west_continent_mask` selects `large_continents + 0.08` |
| North / South ocean corridors | `abs(z) > abs(x)` | `small_continents - 0.42` — the abyssal program's territory |
| East/West sign | `x*0.002 + vegetation_noise*0.35`, clamped to -1..1 | `east_west_gradient`; **West is −X** |

Two consequences worth stating plainly:

1. **The world is a compass rose.** A central disc, a mountain annulus, two land lobes east and west, two ocean corridors north and south. The Pelagos surface region is the western lobe.
2. **The diagonals are already neutral.** Where `abs(x)` approaches `abs(z)`, `east_west_ocean_corridor_mask` falls to zero and the culture gradient returns to the seam value. The four diagonal quadrant boundaries are therefore *naturally* soft transition zones — exactly what contract C6 and canon's "not so absolute that every border becomes mechanically perfect" ask for. **No extra work is required to create the transition areas; they already exist.**

The western lobe also has one geographic asset the eastern lobe does not: it is the lobe that faces the **western abyssal ocean**, where the Pelagos deep-sea program is already implemented. A Pelagos coastline is therefore continuous with an existing body of implemented content — `pel_028`, `pel_042`, `pel_056`, `pel_095`, and the tidal-breach damage archetype all sit at that junction. **Prefer coastal siting for the Compact's landmark assets;** it is the one place in the world where two finished programs already meet.

### 12.2 The gap, and the one worldgen change required

`kubejs/data/minecraft/worldgen/world_preset/normal.json` routes the **ocean** bands by humidity — West `[-1.0, -0.2]`, seam `[-0.2, 0.2]`, East `[0.2, 1.0]` — which is how the abyssal program achieves its East/West split. The **land** rules at the end of the rule list carry **no humidity gate at all**:

```
wastelands:mountains    erosion [-1.0, -0.55]
wastelands:city         erosion [-0.55, -0.15]
wastelands:forest       erosion [-0.15,  0.20]
wastelands:city         erosion [ 0.20,  0.50]
wastelands:apocalypse   erosion [ 0.50,  1.00]
```

So today, West and East land are identical. That is the gap this program has to close.

**The naive fix does not work.** Gating new land rules on `humidity [-1.0, -0.2]` also captures the western half of the *central continent*: at `x = -2000, z = 0`, `east_west_continent_mask = 1.0`, `east_west_ocean_corridor_mask` is about `0.99`, and `east_west_gradient` saturates at `-1.0`, so `city_humidity` lands near `-0.99` — squarely inside the West band. Half the central continent would become Pelagos.

**Recommended fix: one new density function, one edited reference.** *(This is the same change described in the Karsic document §12.2. It is authored once and serves both regions — do not implement it twice.)*

Add `custom_worldgen:regional_culture_gradient`:

```json
{
  "type": "isekai_api:multiply",
  "a": "custom_worldgen:regional_east_west_gradient",
  "b": {
    "type": "isekai_api:add",
    "a": { "type": "isekai_api:constant", "value": 1.0 },
    "b": {
      "type": "isekai_api:negate",
      "f": "custom_worldgen:central_continent_mask"
    }
  }
}
```

Then, inside `custom_worldgen:city_humidity`, replace the innermost `"custom_worldgen:regional_east_west_gradient"` reference with `"custom_worldgen:regional_culture_gradient"`. Nothing else in that function changes.

Why this is safe:

- Inside `r <= 4000` the culture gradient goes to 0 — the neutral seam — so central-continent land keeps using the existing ungated rules and **the central continent is untouched**.
- Between `r = 4000` and `r = 4800` the mask feathers, producing a graded cultural approach rather than a hard line. This is the "immediate transition zone" canon describes.
- Outside `r >= 4800`, `central_continent_mask` is 0, the multiplier is 1, and the function is **identical to today**. The entire implemented abyssal program is unaffected — that property is what makes the change acceptable at this stage.
- `start_city_mask` (forcing 2.0) and `mountain_ring_mask` (forcing 1.25) are lerped in *after* this term, so the safe zone, `wastelands:city`, and `wastelands:mountains` routing are untouched.

This needs a companion assertion in the existing abyssal deformation-integrity validator: `regional_culture_gradient` must be referenced by `city_humidity` and by nothing else.

### 12.3 Pelagos land biomes

Five biomes mirroring the existing temperate land erosion bands, gated on `humidity [-1.0, -0.2]` and `continentalness [-0.19, 1.2]`, inserted **before** the ungated temperate rules and **after** the `safe_zone` / `city` / `mountains` rules:

| Biome | Erosion band | Mirrors | Role |
|---|---|---|---|
| `infinite_domain:pelagos_moorland` | `[-1.0, -0.55]` | `wastelands:mountains` | Upland, drystone walls, quarries, reservoirs. |
| `infinite_domain:pelagos_town` | `[-0.55, -0.15]` | `wastelands:city` | **Primary settlement biome.** Terraces, high streets, viaducts. |
| `infinite_domain:pelagos_wooded_vale` | `[-0.15, 0.20]` | `wastelands:forest` | Estates, plantations, villages, canals. |
| `infinite_domain:pelagos_estuary_belt` | `[0.20, 0.50]` | `wastelands:city` | **Secondary settlement biome**, industry and dockside-weighted. Sited toward the coast. |
| `infinite_domain:pelagos_coastal_waste` | `[0.50, 1.00]` | `wastelands:apocalypse` | Exposed coast, sea walls, holiday parks, wind. |

Tags:

- `#infinite_domain:pelagos_region_biomes` — all five. Used by the Lost Cities `BiomeMatcher` (§11.5) and by every Pelagos structure set.
- `#infinite_domain:pelagos_settlement_biomes` — `pelagos_town` + `pelagos_estuary_belt`.
- `#infinite_domain:pelagos_rural_biomes` — `pelagos_wooded_vale` + `pelagos_coastal_waste`.
- `#infinite_domain:pelagos_upland_biomes` — `pelagos_moorland`.

`citybiomemultipliers` in the worldstyle gains `pelagos_town` at **1.35** and `pelagos_estuary_belt` at **1.2**, matching how `wastelands:city` is already boosted.

Biome definitions should be authored as near-clones of their `wastelands:` counterparts, differing only in surface/vegetation tuning and in their `features` / `spawners` lists. **Do not invent new terrain behaviour here.** The point of the Pelagos region is architecture, not a new biome ecology, and inventing one would conflict with `docs/NORTHERN_BIOME_RESTORATION.md` and the Wastelands mod's routing.

One tuning note that pays for itself: `pelagos_wooded_vale` and `pelagos_town` should carry **hedgerow-like field boundaries** in their feature lists where the mod set allows. Field boundaries older than the buildings they surround is §4.1 written into the terrain, and it costs one feature entry.

### 12.4 Scattered and standalone placement

The four mandatory native assets — `pel_086` arch units, `pel_087` public house, `pel_088` street furniture, `pel_089` bus shelter — are what make a Pelagos region feel inhabited *between* the Lost Cities blocks. They are placed twice:

1. **Lost Cities `scattered`**, via the worldstyle `scattered.list`, so they appear inside and around generated districts. Requires `scattered/pelagos/*.json` wrappers.
2. **Worldgen structure sets**, for open country between districts, using `random_spread` with salts from the reserved Pelagos range **79200000–79209999** and `#infinite_domain:pelagos_region_biomes` as the biome filter.

Any Pelagos asset placed through a worldgen structure set rather than Lost Cities must **also** be added to `avoidStructures` in `defaultconfigs/lostcities-server.toml`, exactly as the 64 `ows_*` structures already are, or Lost Cities will generate a district on top of it.

Two assets carry extra placement requirements:

- **`pel_065_viaduct_collapse` and `pel_086_railway_arch_units` must tile with each other.** A viaduct that stops after one placement is worse than no viaduct. Author them against a shared arch pitch and a shared template-edge profile, and validate tiling explicitly (§13.4, PV-11).
- **`pel_090_londinium_wall_fragment` is a single-instance landmark.** Place it with a very large spacing and a low count, or through a dedicated structure set with `separation` close to `spacing`. Finding a second one an hour after the first destroys it.

### 12.5 Cross-regional appearances

Per contract C6, a small number of Pelagos structures may appear in the eastern lobe and in the central continent's transition band. The permitted list is short, and each entry must explain itself in-world:

| Structure | Where | Why it is there |
|---|---|---|
| `pel_030_market_cross_auction_mart` | Central transition band | A Compact trading post established under a pre-collapse agreement, with its own bilingual signage. |
| `pel_083_coastguard_lookout` | Eastern lobe coast, very rare | A joint maritime-safety installation, maintained by whichever side had a vessel nearby. Should read as *shared*, not as an intrusion. |
| `pel_045_downed_cargo_airship` | Central transition band | It did not choose where to come down. |
| `pel_063_allotment_shed_cache` | Central transition band | Refugee cultivation on ground nobody claimed. Reads as people, not as a state. |

Four entries, all deliberately legible as foreign. Anything beyond this list weakens regional readability and is prohibited.

Note the tonal difference from the Karsic cross-regional list, which is a trade mission, a listening post, pre-positioned stores, and a failed convoy — three of the four are *state* objects. Three of Pelagos's four are commercial, shared, or civilian. Neither list is longer than the other; they simply say different things about who crossed the border and why.

---

## 13. Validation

### 13.1 Existing validators, applied unchanged

Pelagos assets get **no relaxation**. These run exactly as they do for central-continent assets:

| Validator | Gate role |
|---|---|
| `scripts/structure_geometry_lint.py` checks 1–3 | **Hard fail.** Floating geometry; stair/ladder/sign backing; window/door wall coupling. |
| `scripts/structure_geometry_lint.py` checks 4–6 | Recorded findings: damage coherence, ground context, program conformance. |
| `scripts/validate_structure_programs.py` | Every master has a schema-valid program. |
| `scripts/validate_lostcities_conversion.py` | Conversion integrity. |
| `scripts/validate_settlement_archetypes.py` | Citystyle selectors compile from evidence. |
| `scripts/validate_modular_structure_kits.py` | Shared-module reuse without cloning. |
| `scripts/audit_structure_block_fitness.py` | Block choices suit their role. |
| `scripts/build_structure_provenance.py` | Provenance and licensing records exist. |
| `scripts/compile_production_structure_pools.py` | Only approved assets reach production pools. |

Production admission is recorded only in `structure_library/production-approvals.json`, whose `required_checks` list applies to Pelagos unchanged.

**One note on check 1 (structural connectivity).** Pelagos will trip this more often than Karsic, because arches, viaducts, propped façades, wall cranes, and cantilevered rear extensions all *look* like floating geometry to a flood-fill. They are not exempt — every one of them must genuinely connect through solid blocks to something resting on the base plate. An arch that reads as an arch but is not structurally continuous is a real defect, not a false positive, and the fix is to build the arch properly rather than to weaken the check.

### 13.2 New validators required

| Script | Checks |
|---|---|
| `scripts/validate_material_profile.py` | Every role resolves for every stratum in use; every block string, derivatives included, exists in `docs/registry-inventory/block-ids.txt`; **the resolver keys on plot stratum, not structure stratum** (§8.4). Runs before P3. |
| `scripts/validate_regional_assignment.py` | Every base master has exactly one conversion class; roster counts match §10.11. |
| `scripts/validate_regional_structures.py` | The Pelagos-specific geometry checks in §13.4. |

### 13.3 Gate sequence per structure

```
P1 program schema valid  (strata list length >= 2; repeatable_storey == false)
  -> P2 massing     -> footprint drift within +/-20%, or a recorded exception
  -> P3 fabric      -> material profile validation passes
  -> P4 envelope    -> lint check 3 clean
  -> P5 plan        -> lint checks 1-2 clean; check 6 ledger diffs clean
  -> P6 site        -> lint check 5 clean
  -> P7 dressing    -> signage grammar clean; sign backing clean
  -> P8 collapse    -> lint check 4 recorded; damage constraints honoured
  -> P9 assembly    -> conversion, archetype and provenance validators clean;
                       every generated building has minfloors == maxfloors
  -> production approval
```

Per the usage-conserving policy in `CODEX_STRUCTURE_PIPELINE.md`, per-structure checks run per structure; the **expensive global gates** — full corpus, provenance, all-render, QA world, performance budget — run only at the wave boundaries in §14.

### 13.4 Pelagos-specific checks

These enforce *this document* rather than general doctrine. All belong in `validate_regional_structures.py`.

| ID | Check | Rule enforced |
|---|---|---|
| **PV-1** | **Two-stratum minimum.** Every master's program declares at least two strata, and at least two are actually present in the geometry. | §4.4. The single most important Pelagos check — without it every conversion degrades into a brick recolour. |
| **PV-2** | **Visible junction.** Wherever two strata meet inside a building, the interior shows it: a 1-block level change, a corridor width change, or a doorway cut through a former external wall. | §7.1 junction rule. |
| **PV-3** | **No repeated storey band.** Every generated building has `minfloors == maxfloors`, and no storey band is byte-identical to the one below it. | §6.1. The exact inverse of Karsic KV-1, and the reason the two regions cannot share a massing validator. |
| **PV-4** | **Party wall, parapet, stack.** Every attached P-I/P-II/P-III master carries a full-height wall at every plot boundary, a parapet 1 proud of the roof plane, and one stack per boundary. | §6.3; legibility carrier #1. |
| **PV-5** | **Eaves variation.** In any attached run of 3 or more plots, at least two distinct eaves heights occur. | §6.4. A perfectly level terrace reads as one building, which is wrong. |
| **PV-6** | **Window proportion.** Domestic openings are 1 wide by 3 high. No 2x2 punched openings on any P-I/P-II/P-III master. | §8.5. The primary separator from Karsic. |
| **PV-7** | **Rear alley continuity.** Every master with `rear_alley: true` has a walled 2-wide way reaching the template edge at both ends. | §6.3; legibility carrier #6. |
| **PV-8** | **Surface services.** Every master with a P-IV or later stratum shows `cable_tray` or `surface_pipe` running on a wall face of an older stratum. | §7.3 rule 2; legibility carrier #9. |
| **PV-9** | **Roof discipline.** A flat roof requires a declared P-IV or P-V stratum. Every other master is pitched. | §8.5. |
| **PV-10** | **Londinium cap and rules.** Exactly nine masters carry P-0. Each has no complete Roman room, is entered from above, and has at least one modern-intervention fixture within 6 blocks of the fragment. | §4.6, §10.12. |
| **PV-11** | **Viaduct tiling.** `pel_065` and `pel_086` share an arch pitch and a template-edge profile, and tile with each other in both directions. | §12.4. |
| **PV-12** | **Signage generations.** Every institutional master carries signage from at least two different periods. | §9.2 rule 4. |
| **PV-13** | **Determinism of variation.** No unseeded `random` call in any Pelagos generator module. Static analysis over `scripts/regional/pelagos_*.py`. | §8.0. Pelagos varies deliberately; unseeded variation would make the region irreproducible. |
| **PV-14** | **Prohibited-motif scan.** No national emblem shapes; no fantasy-medieval silhouettes; kiosks and post boxes at ordinary frequency, never clustered. | §4.2. Partly automatable; the remainder is a review item. |

---

## 14. Work order

Structured as families and waves, matching the model used by `structure_library/rebuild-family-roadmap.json` and the usage-conserving policy in `CODEX_STRUCTURE_PIPELINE.md`. **Every family member is completed and locally validated before the family is batched; global gates run only at wave boundaries.** Each family and each wave is an independently resumable stop point.

### 14.1 Families

| Family | Members | Count | Shared systems built here |
|---|---|---|---|
| **PF1 — Terrace and Plot** | `pel_021`, `pel_069`, `pel_070`, `pel_072`, `pel_073`, `pel_087`, `pel_099` | 7 | Plot module; party wall / parapet / stack assembly; pitched-roof system; sunken area and railings; rear outshut; rear alley; shopfront assembly. |
| **PF2 — Street Kit and Props** | `pel_031`, `pel_038`, `pel_045`, `pel_057`, `pel_081`, `pel_084`, `pel_088`, `pel_089`, `pel_091` | 9 | Pavement and kerb; bollard / railing / lamp set; notice and way signs; awning system; vehicle chassis modules. |
| **PF3 — Arch and Viaduct** | `pel_054`, `pel_055`, `pel_065`, `pel_066`, `pel_086` | 5 | Brick arch geometry; viaduct tiling profile; arch-unit fit-out; retaining wall and embankment; wall crane. **Highest identity-per-block family in the program.** |
| **PF4 — Mill and Works** | `pel_004`, `pel_040`, `pel_043`, `pel_044`, `pel_046`, `pel_048`, `pel_049`, `pel_050`, `pel_052`, `pel_096`, `pel_097` | 11 | Segmental arch head; iron column grid; loading-door stack; sawtooth shed; tall chimney; patent glazing; ornate engine house. |
| **PF5 — Dockside and Water** | `pel_028`, `pel_039`, `pel_042`, `pel_053`, `pel_056`, `pel_071`, `pel_074`, `pel_083`, `pel_094`, `pel_095` | 10 | Embankment and quay wall; foreshore steps; flood gate; tide-line damage operator; jetty; lock chamber. |
| **PF6 — Civic Accretion** | `pel_006`, `pel_007`, `pel_008`, `pel_010`, `pel_011`, `pel_012`, `pel_014`, `pel_015`, `pel_092`, `pel_100` | 10 | Link corridor and bridge; multi-wing campus layout; stone dressing; hall module; ward and classroom modules; junction expression. |
| **PF7 — High Street and Commerce** | `pel_013`, `pel_018`, `pel_019`, `pel_020`, `pel_023`, `pel_024`, `pel_026`, `pel_027`, `pel_030` | 9 | Continuous shopfront run; fascia and awning; faience façade; retained-façade prop system; precinct and undercroft. |
| **PF8 — Suburb and Estate** | `pel_017`, `pel_032`, `pel_033`, `pel_035`, `pel_036`, `pel_037`, `pel_067`, `pel_068`, `pel_076`, `pel_080`, `pel_085`, `pel_098` | 12 | Semi and close geometry; garage block; deck access; ramped deck; forecourt canopy; carriageway and slip road. |
| **PF9 — Rural, Coast and Margin** | `pel_001`, `pel_002`, `pel_003`, `pel_005`, `pel_009`, `pel_016`, `pel_034`, `pel_047`, `pel_063`, `pel_075`, `pel_079`, `pel_082`, `pel_093` | 13 | Farmstead modules; drystone wall; glasshouse range; churchyard kit; allotment kit; hedgerow boundary. |
| **PF10 — Restricted and Technical** | `pel_041`, `pel_051`, `pel_058`, `pel_059`, `pel_060`, `pel_061`, `pel_062`, `pel_064`, `pel_077`, `pel_078` | 10 | Containment retrofit; hardened envelope; plant hall; filter beds; sub-surface complex; cut-and-cover box; tiled platform. |
| **PF11 — Londinium** | `pel_090`, plus substrate inserts into `pel_009`, `pel_019`, `pel_028`, `pel_041`, `pel_064`, `pel_092`, `pel_094`, `pel_100` | 1 new + 8 inserts | Ragstone-with-bonding-course walling; opus signinum floor; hypocaust pilae; modern-intervention kit. Built once as `londinium_substrate.py` and inserted into eight masters that already exist. |
| **PF12 — Set Pieces** | `pel_022`, `pel_025`, `pel_029` | 3 | Toppled-mass operator; podium-tower geometry; lodge block. |
| | **Total** | **100** | |

### 14.2 Waves

| Wave | Families | Why this order |
|---|---|---|
| **P-A — Foundation** | PF1, PF2, PF3 | These build every shared system the rest reuses: the plot module, the party-wall assembly, the pitched roof, the street kit, and the arch geometry. **Nothing else should start until P-A is done.** They also deliver carriers #1, #3, #4, and #10 — after P-A alone, the region is already unmistakable. |
| **P-B — The worked region** | PF4, PF5, PF10 | Mills, works, dockside, and technical sites. Second, because the coast is where Pelagos meets the already-implemented western abyssal program (§12.1), and because these establish the tidal-breach and legacy-bypass damage vocabulary. |
| **P-C — The inhabited region** | PF6, PF7, PF8, PF9 | Civic, commerce, suburb, and countryside — the bulk of the roster, and the part that reads best once the infrastructure exists. |
| **P-D — Depth and set pieces** | PF11, PF12 | Londinium last, deliberately. The eight substrate inserts modify masters that must already exist and be validated, and the landmark lands better once the region is legible — the player should already know what a Pelagos street is before finding something two thousand years older underneath it. |

At each wave boundary, and only there: full corpus validation, provenance, complete Lost Cities conversion, render batch, QA-world rebuild, and the performance-budget check.

**Note on PF11.** It is the only family in either program that *modifies existing validated masters* rather than producing new ones. That breaks the usual immutability assumption, so treat each insert as a fresh P2–P8 run on that master with the substrate included, re-validating from scratch — not as a patch applied to an approved asset.

### 14.3 Prerequisites, before any geometry

1. **Decide the hemisphere binding** (§2). The only genuinely blocking decision in this document.
2. Add the three Pelagos ground contexts to `_GROUND_PALETTES` in `scripts/structure_geometry_primitives_v2.py` (§5.4).
3. Author and validate `pelagos-material-profile.json`, including every slab/stair/wall derivative **and the per-plot resolver** (§8.4).
4. Author `pelagos-assignment.json` from §10 and validate it.
5. Land the `regional_culture_gradient` worldgen change and its validator assertion (§12.2) — **once, shared with the Karsic program** — before any regional biome or structure set exists.
6. Author the five Pelagos biomes and their tags (§12.3).
7. Author `pelagos-name-lists.json` (§9.1). Keep the stems short: forty reads as a region, four hundred reads as a generator.
8. Write `scripts/validate_regional_structures.py` with PV-1..PV-14 **before** PF1 geometry, not after.

Item 8 is the lesson of `STRUCTURE_REBUILD_SYSTEM_V2.md` §6: 84 assets were built against primitives that were defective by construction, and every completion claim had to be reset to zero. The cost of writing the checks first is a few hours. The cost of writing them last was the entire previous corpus.

---

## 15. Risks and open decisions

| # | Item | Status | Notes |
|---|---|---|---|
| 1 | **Hemisphere binding** | **Blocking** | §2. Pack canon and all live data say Pelagos = West; the planning request said the opposite. Decide before anything else. Reversing later drags the entire implemented abyssal program with it. |
| 2 | **Scope against the existing backlog** | **Open** | `rebuild-family-roadmap.json` currently reports `remaining_assets: 57` and `production_approvals: 0`, with all v1 progress reset. Pelagos adds 100 masters and 200 catalog entries; Karsic adds 94 and 188. Together the two regions are roughly **three times** the outstanding central-continent work. Decide explicitly whether the regions run after, in parallel with, or instead of finishing the centre. This document does not assume an answer. |
| 3 | **Structural connectivity vs. Pelagos forms** | **Accepted risk** | §13.1. Arches, viaducts, propped façades, wall cranes, and cantilevers all resemble floating geometry to lint check 1. They must genuinely connect; the fix is always to build the form properly, never to weaken the check. Expect this family of findings to dominate PF3 and PF7. |
| 4 | **Street width 6** | **Unverified** | §11.4. Chosen for inherited-street scale but never measured in-world. Lost Cities street width interacts with lot fitting; verify before locking. A width of 6 may also affect the highway-compat mixin in `packdev/lostcities-highway-compat/` — check that first. |
| 5 | **Fresh-world validation availability** | **Known constraint** | `docs/ABYSSAL_OCEAN_PROGRAM.md` records that fresh-world validation was unavailable on 2026-08-22 and work proceeded under a waiver. The `city_humidity` change in §12.2 is a real terrain-routing mutation and **should not** inherit that waiver silently. If validation is still unavailable, say so explicitly in the implementation record rather than assuming it passed. |
| 6 | **Biome count** | **Open** | Pelagos adds 5 land biomes, Karsic 5 more. Check the total against `docs/biome-gating-audit` and any mod-side limits before authoring. |
| 7 | **Performance budget** | **Open** | 100 additional masters against `docs/structure-performance-budget.json`. Terraces are cheap per building but extremely common; the accreted hospital and the viaduct set are expensive. Measure at wave boundaries, not at the end. |
| 8 | **Two material layers, not one** | **Documented** | §11.2. Lost Cities styles and palettes govern between-building fabric; converted parts carry local palettes that override them. Anyone assuming one job covers both will produce a half-converted region. |
| 9 | **The remap shortcut is more dangerous here** | **Controlled** | §8.4.1. Re-tinting a base master to brick produces something that looks superficially like the Compact while having none of the plot rhythm, party walls, pitched roofs, or stratum layering that actually carry the identity. Assets taking that path are marked `fabric_only: true` and barred from production approval. |
| 10 | **Londinium tone** | **Open, worth a second look** | §4.6. The Roman substrate is the strongest idea in this document and the easiest to overplay. Nine carriers, four rules, and PV-10 are the guard rails as specified — but this is the one area where a review pass after PF11 is worth the cost, because getting it wrong is more damaging than not doing it at all. |
| 11 | **Name-list scale** | **Open** | §9.1. Deterministic naming needs enough stems to avoid obvious repetition and few enough that the region feels like one place. Forty is the working figure; it has not been tested. |
| 12 | **Mob and spawn profile** | **Out of scope** | Whether the Compact gets its own hostile or ambient profile is a separate decision owned by the spawn documents. Flagged so it is not silently assumed. |
| 13 | **Quest integration** | **Out of scope, but expected** | Canon §"Exploration and quest integration" asks for regional discovery objectives. Those belong in the quest documents once the roster is real. The Londinium landmark is an obvious quest anchor. |
| 14 | **Shared edit collision** | **Sequencing** | §11.5. The `excluding` matcher on the seven `wasteland_*` selectors is the one file edit both regional programs need. Whichever lands first makes it; the second only appends. |

---

## 16. Change log

| Date | Change |
|---|---|
| 2026-08-26 | Document created. Planning only; nothing implemented. Roster fixed at 100 masters (85 conversions, 0 exclusions, 15 native additions), with the Londinium substrate capped at nine carriers. Hemisphere binding recorded as Pelagos = West per pack canon, with the conflicting planning-request wording and a reversal procedure both documented in §2. |
