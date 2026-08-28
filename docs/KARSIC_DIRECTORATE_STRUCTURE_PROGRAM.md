# Infinite Domain — Karsic Directorate Structural Conversion Program

Status: **planning only. No geometry, no data files, no generator code has been written against this document. Nothing here is implemented, approved, or measured in-world.**

Sibling document: [`docs/PELAGOS_COMPACT_STRUCTURE_PROGRAM.md`](PELAGOS_COMPACT_STRUCTURE_PROGRAM.md). The two are deliberately self-contained so either can be worked in isolation; the only content they share is the **Shared regional contract** (§3), which is stated identically in both and must be changed in both or neither.

---

## 1. Authority and precedence

| Rank | Source | Role |
|---|---|---|
| 1 | `old_world_narrative/source/01_CANON_AND_NONNEGOTIABLES.md` | Immutable world facts. |
| 2 | `old_world_narrative/source/03_STRUCTURE_REVISION_PROGRAM_UPDATED.md` §"Alternative structures — regional faction architecture" | Defines the Karsic Directorate, its design language, its hemisphere, and the regional-equivalency rule. **This document implements that section; it does not replace it.** |
| 3 | `structure_library/STRUCTURE_REBUILD_SYSTEM_V2.md` | Binding geometry doctrine and QA gate. Every Karsic asset is subject to §3.1–3.8 and §4 exactly as central-continent assets are. |
| 4 | `docs/HEAVY_REBUILD_DOCTRINE.md` | Rebuild standard, visual gates A/B/C, the five scales of detail, collapse-state layering. |
| 5 | `CODEX_STRUCTURE_PIPELINE.md` | Pipeline stages, repository discipline, usage-conserving family policy. |
| 6 | **This document** | Karsic-specific cultural specification: strata, material profile, massing grammar, plan grammar, settlement grammar, conversion passes, generator architecture, structure roster, Lost Cities wiring. |

Precedent for format and tone: `docs/ABYSSAL_OCEAN_PROGRAM.md`, which already governs the Karsic/Pelagos split below sea level. This document is its surface counterpart and must not contradict it.

Future work updates this file rather than creating a parallel plan.

---

## 2. Hemisphere binding — read this before doing anything

**Canonical binding, confirmed against live pack data: the Karsic Directorate is the EASTERN region (+X).**

Evidence, all currently in the repository:

| Source | Statement |
|---|---|
| `03_STRUCTURE_REVISION_PROGRAM_UPDATED.md` §World placement | "The Karsic Directorate: preferentially spawn on the **right/eastern side of the world map**." |
| `docs/ABYSSAL_OCEAN_PROGRAM.md` §Regional identity | "**Eastern Abyss — Karsic.**" |
| `kubejs/data/infinite_domain/tags/worldgen/structure/eastern_*_sites.json` | All four eastern site tags contain only `infinite_domain:abyssal/karsic_*` structures. |
| `tools/abyssal_worldgen/abyssal_factional_debris_catalog.json` `pool_contract` | `"karsic_pool_must_stay_eastern_only": true`. |
| `kubejs/data/wastelands/worldgen/world_preset/wasteland.json` | `infinite_domain:eastern_*` biomes are all gated on `humidity [0.2, 1.0]`, which is the **positive** (eastern, +X) side of `custom_worldgen:east_west_gradient`. |
| `config/ftbquests/quests/lang/en_us.snbt` | "Repeat the deep-water survey on the **Karsic-facing eastern slope**." |

The planning request that produced this document described the arrangement the other way round (Russian-inspired culture in the **West**, English-inspired culture in the **East**). That is the opposite of every artefact listed above. This document therefore uses the **pack-canonical** binding — Karsic = East — and this file is named by **faction**, not by hemisphere, so that a later reversal is a routing change rather than a rewrite.

### 2.1 If the binding is deliberately reversed

Nothing in §4–§12 of this document changes; the culture is defined by faction, not by compass. Reversal touches exactly five things, and all five live outside this file:

1. `kubejs/data/wastelands/worldgen/world_preset/wasteland.json` — swap the `humidity` bands on the Karsic and Pelagos **land** rules added by §12.
2. `kubejs/data/infinite_domain/tags/worldgen/biome/karsic_region_biomes.json` — repoint at the western biome set.
3. The `biomes` matcher on the Karsic city-style selectors in the worldstyle (§11.4).
4. The `abyssal_factional_debris_catalog.json` `pool_contract` flags, plus the eight `eastern_*`/`western_*` abyssal site tags — **note this drags the entire implemented deep-ocean program with it**, which is the expensive part.
5. Existing quest text in `config/ftbquests/quests/lang/en_us.snbt` that names the Karsic-facing slope as eastern.

Items 4 and 5 are the reason to decide this once, now, and not later: the seabed program is already built against East = Karsic. **Recommendation: keep East = Karsic and treat the planning-request wording as a slip.** If the reversal is genuinely wanted, do it as its own dedicated change before any Karsic surface geometry exists, not after.

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

**The Karsic Directorate built systems, not buildings — and the standard was the statement.**

Where another society would have let a thousand owners each solve their own problem, the Directorate issued a design, a series number, and a schedule, then applied it from the capital to the last mining settlement on the permafrost. The recurrence is not laziness on the part of whoever built the world; it is the *content* of the culture. A player who walks from one Karsic town to the next and thinks *"I have seen this stair, this door, this lamp, this fence before"* has understood the Directorate correctly.

This is the honest reading of the phrase used in the planning request — a state that **performed its own identity as policy**. It is not a joke at the Directorate's expense and it is not a collection of national symbols. It is a civilisation that made its own idiom compulsory, at continental scale, and then could not maintain what it had built.

### 4.2 Prohibited shortcuts

Banned outright. Presence is a hard review failure, not a note.

- Onion domes, red stars, hammer-and-sickle motifs, bear iconography, or any other national emblem used as decoration.
- Cyrillic-shaped block art or "foreign-looking" glyph signage. Signage is English; the *grammar* of the signage carries the culture (§9.2).
- Universal grey brutalism. Per canon: "Avoid making every Directorate site uniformly brutalist." Five strata coexist (§4.4).
- Snow as a substitute for cold engineering. Cold is expressed in vestibules, plinth heights, insulated pipe runs, and roof forms — not in a white block layer.
- Comedy scale. Monumental means large and flat, not cartoonish.

### 4.3 The ten legibility carriers

Ranked by regional identity delivered per block placed. Generator budget follows this order.

| # | Carrier | Why it reads |
|---|---|---|
| 1 | **Visible module joints** | Prefabricated panel construction shows its seams. A façade divided into identical repeating rectangles with expressed joint lines is the single strongest Karsic signal, and it is cheap in blocks. |
| 2 | **Flat roof, parapet, bulkhead** | No pitch, no gable, no chimney rhythm. A hard horizontal top edge with a small plant bulkhead behind it. |
| 3 | **Above-ground service infrastructure** | Insulated heating mains on concrete saddles running *between* buildings across open ground, stepping over roads on gantries. Infrastructure is street furniture, not something buried. |
| 4 | **The courtyard district** | Buildings placed to form shared outdoor rooms. Roads pass around the group; footpaths pass through it. |
| 5 | **Double vestibule at every entrance** | Two doors with a small unheated lobby between, and a canopy over the outer leaf. Cold engineering, visible from outside as a projecting porch. |
| 6 | **Rail spine** | Anything industrial is organised along a siding, not a road frontage. Loading happens under a gantry over track. |
| 7 | **Axial institutional approach** | Civic buildings terminate an axis: broad forecourt, wide flight of steps, flat entablature band, no crown. |
| 8 | **Standard-issue site kit** | The same fence, lamp standard, bollard, service door, and stair rail recur across unrelated sites. |
| 9 | **Plinth/body distinction** | A darker, heavier ground storey under identical upper floors. |
| 10 | **Oversize relative to survivors** | Built scale exceeds anything the surviving population could maintain. Half a building lives; the rest is dark. |

### 4.4 The five Karsic strata

Every Karsic structure declares **one primary stratum**, and most declare **one secondary stratum** visible as an earlier core or a later graft. The generator treats this as an enum; the roster (§10) assigns it per structure.

| ID | Name | Period role | Materials | Signature |
|---|---|---|---|---|
| **K-I** | *Foundry Brick* | Oldest surviving industrial and civic fabric. | Red/ochre brick, cast iron, timber roof trusses, stone plinths. | Segmental arched windows, corbelled cornices, internal iron columns, tall square brick chimneys. |
| **K-II** | *First Standard* | The first national catalogue. Rendered masonry, symmetric, modest. | Rendered brick, painted stucco, steel small-pane windows, tiled hipped roofs. | Symmetrical façade, central entrance, string courses, shallow hipped roof. Ordinal numbering begins here. |
| **K-III** | *State Series* | **The dominant stratum.** Prefabricated concrete panel; the catalogue at continental scale. | Precast panel, in-situ frame, concrete block infill, steel windows. | Visible panel joints, punched or ribbon glazing, flat roof and parapet, contrasting plinth, external stair tower. |
| **K-IV** | *Directorate Monumental* | Institutional and ceremonial. Reserved. | Cast in-place concrete, stone facing, bronze/copper gone green, granite steps. | Pilaster order, deep reveals, ceremonial stair, flat entablature, oversized forecourt, no crown. |
| **K-V** | *Late Retrofit* | The last thirty years before collapse, grafted onto everything above. | Aluminium and steel rainscreen, plastic glazing, glazed connectors, bolted-on plant. | Glass link bridges between older blocks, cladding over K-II/K-III shells, security grilles, roof dishes and condensers. |

**Stratum pairing rule.** A secondary stratum, where present, is **adjacent** in the table (K-I⊕K-II, K-III⊕K-II, K-III⊕K-IV, K-IV⊕K-V, …), *except* for the deliberate **K-I⊕K-V** pair, reserved for the handful of structures where an old brick works was still running under modern cladding when it failed. The roster limits that pair to four entries.

### 4.5 The Directorate collapse thesis

From canon: *"systems continuing far beyond the point at which the society operating them was healthy enough to sustain them."* Expressed structurally:

- **The machine outran its margins.** Nothing shattered at once. A boiler house kept four blocks alive while six froze. A substation was cannibalised to keep a hospital lit.
- **Centralisation became the failure mode.** One heating main serves a district; when it went, the district went, all at once, in a single winter.
- **The technical basement outlived the public building.** Sealed plant rooms, pipe galleries, and shelters stayed dry and functional long after the halls above were open to the sky.
- **Evacuation depended on trains, buses, and assembly points** that stopped being possible.
- **The last inhabitants occupied a fraction.** One warm wing of an enormous institute, partitioned off from the rest.

---

## 5. Material system

Every block ID below was verified present in `docs/registry-inventory/block-ids.txt` for this instance on 2026-08-26. **Any addition to these tables must be verified the same way before it reaches a generator.**

### 5.1 Structural roles by stratum

The generator never names a block directly. It names a **role**; the Karsic material profile resolves the role to a block for the active stratum. This is what makes Pass P3 (§8) a single deterministic substitution rather than a hand edit of thousands of coordinates.

| Role | K-I Foundry Brick | K-II First Standard | K-III State Series | K-IV Monumental | K-V Late Retrofit |
|---|---|---|---|---|---|
| `wall_primary` | `minecraft:bricks` | `immersiveengineering:concrete_sprayed` | `immersiveengineering:concrete` | `immersiveengineering:concrete_reinforced` | `immersiveengineering:sheetmetal_aluminum` |
| `wall_secondary` | `quark:cobblestone_bricks` | `minecraft:white_terracotta` | `immersiveengineering:concrete_tile` | `immersiveengineering:concrete_chiseled` | `immersiveengineering:sheetmetal_steel` |
| `wall_panel_field` | — | — | `immersiveengineering:concrete_sheet` | — | `tfmg:industrial_aluminum_casing` |
| `panel_joint` | — | — | `immersiveengineering:concrete_brick` | `immersiveengineering:concrete_pillar` | `create:metal_girder` |
| `plinth` | `minecraft:stone_bricks` | `minecraft:polished_andesite` | `tfmg:gray_rebar_concrete` | `quark:polished_shale` | `tfmg:gray_rebar_concrete` |
| `pilaster` | `minecraft:brick_wall` | `immersiveengineering:concrete_pillar` | `immersiveengineering:concrete_pillar` | `immersiveengineering:concrete_pillar` | `create:metal_girder` |
| `floor_slab` | `minecraft:bricks` | `immersiveengineering:concrete` | `immersiveengineering:concrete` | `immersiveengineering:concrete_reinforced` | `immersiveengineering:concrete` |
| `floor_finish_public` | `minecraft:polished_andesite` | `supplementaries:stone_tile` | `immersiveengineering:concrete_tile` | `quark:polished_jasper` | `immersiveengineering:concrete_reinforced_tile` |
| `floor_finish_service` | `tfmg:factory_floor` | `tfmg:factory_floor` | `tfmg:factory_floor` | `tfmg:factory_floor` | `the_wasteland_reworked:aluminium_grate` |
| `roof_deck` | `minecraft:bricks` | `quark:gray_shingles` | `immersiveengineering:concrete_sheet` | `immersiveengineering:concrete_reinforced` | `immersiveengineering:sheetmetal_aluminum` |
| `internal_column` | `create:metal_girder` | `immersiveengineering:concrete_pillar` | `immersiveengineering:concrete_pillar` | `immersiveengineering:concrete_pillar` | `create:metal_girder` |
| `stair_core_wall` | `minecraft:bricks` | `immersiveengineering:concrete_sprayed` | `immersiveengineering:concrete_brick` | `immersiveengineering:concrete_reinforced` | `immersiveengineering:concrete_brick` |

Four further roles name a **derivative block directly**, because they are always used as a slab, a stair, or a wall and never as a full cube:

| Role | Kind | K-I | K-II | K-III | K-IV | K-V |
|---|---|---|---|---|---|---|
| `parapet_cap` | slab | `minecraft:brick_slab` | `minecraft:smooth_stone_slab` | `immersiveengineering:slab_concrete` | `quark:polished_shale_slab` | `immersiveengineering:slab_sheetmetal_aluminum` |
| `stair_tread` | stairs | `minecraft:brick_stairs` | `minecraft:stone_brick_stairs` | `immersiveengineering:stairs_concrete` | `immersiveengineering:stairs_concrete` | `immersiveengineering:stairs_concrete_brick` |
| `coping` | wall | `minecraft:brick_wall` | `minecraft:stone_brick_wall` | `immersiveengineering:wall_concrete` | `immersiveengineering:wall_concrete` | `immersiveengineering:wall_concrete_brick` |
| `debris_accent` | block | `quark:cobblestone_bricks` | `minecraft:white_terracotta` | `immersiveengineering:concrete_brick_cracked` | `immersiveengineering:concrete_chiseled` | `immersiveengineering:sheetmetal_steel` |

#### 5.1.1 Derivative naming is not uniform, and this matters

Measured against `docs/registry-inventory/block-ids.txt` on 2026-08-26:

- **Immersive Engineering uses a prefix form** — `immersiveengineering:slab_concrete`, `stairs_concrete`, `wall_concrete`. It does **not** provide `concrete_slab`. Any generator that assumes the suffix form will silently find nothing.
- **Vanilla, Quark, TFMG and Supplementaries use the suffix form** — `brick_slab`, `gray_shingles_slab`, `gray_rebar_concrete_slab`, `stone_tile_slab`. Vanilla also pluralises irregularly: `minecraft:bricks` yields `minecraft:brick_slab`.
- Within Immersive Engineering the set is **incomplete and uneven**. `concrete`, `concrete_brick`, `concrete_tile` and `concrete_leaded` have slab + stairs + wall. `concrete_reinforced`, `concrete_reinforced_tile` and every `sheetmetal_*` have **slab only**. `concrete_sprayed`, `concrete_chiseled`, `concrete_pillar` and `concrete_sheet` have **none at all**.

The profile therefore declares three `derivative_schemes`, tried in order, plus per-stratum `derivative_overrides` for the gaps. It also declares, **per role, which derivative kinds the generator is allowed to request** (`needs`) — so a role that is only ever a full cube is never failed for lacking stairs it would not use.

Two overrides are currently required, both recorded in `structure_library/regional/karsic-material-profile.json`:

| Role | Stratum | Base has no slab | Override |
|---|---|---|---|
| `wall_primary` | K-II | `immersiveengineering:concrete_sprayed` | `immersiveengineering:slab_concrete` |
| `roof_deck` | K-III | `immersiveengineering:concrete_sheet` | `immersiveengineering:slab_concrete` |

Verification is a P3 gate condition (§8.4), enforced by `scripts/validate_material_profile.py`, and is **never** a runtime fallback. A generator that silently substitutes a block produces a region nobody can reason about.

### 5.2 Openings

| Role | Block | Notes |
|---|---|---|
| `glazing_residential` | `quark:gray_framed_glass` | The Karsic default. Cool, framed, institutional. |
| `glazing_residential_pane` | `quark:gray_framed_glass_pane` | Always recessed one block behind the wall face — the deep reveal is a legibility carrier. |
| `glazing_institutional` | `quark:white_framed_glass` | K-IV and better K-III. |
| `glazing_industrial` | `create:framed_glass` | Machine halls, stair towers. |
| `glazing_retrofit` | `minecraft:tinted_glass` | K-V only. |
| `glazing_failed` | `quark:dirty_glass_pane` | Collapse phase D/E substitution. |
| `door_public` | `minecraft:iron_door` | Heavy, institutional. |
| `door_service` | `the_wasteland_reworked:industrial_door` | Plant rooms, basements, shops. |
| `door_hardened` | `the_wasteland_reworked:containment_door` | Shelters, hot cells, restricted sites. |
| `door_domestic` | `minecraft:spruce_door` | Apartments, dachas, village cottages. |
| `vestibule_inner` | `minecraft:oak_door` | Inner leaf of the double vestibule. |
| `window_guard` | `tfmg:cast_iron_bars` | Ground floors and K-V retrofits. |

### 5.3 Standard-issue site and street kit

Legibility carrier #8, and the cheapest identity per block in the whole system. These blocks recur across otherwise unrelated Karsic sites **by design**; that recurrence *is* the culture.

| Role | Block |
|---|---|
| `heating_main` | `tfmg:concrete_encased_industrial_pipe` |
| `heating_main_bare` | `tfmg:industrial_pipe` |
| `pipe_saddle` | `immersiveengineering:concrete_pillar` |
| `pipe_service` | `the_wasteland_reworked:pipe_block` |
| `service_gantry` | `tfmg:steel_truss` |
| `catwalk` | `immersiveengineering:steel_catwalk` |
| `stack_industrial` | `tfmg:concrete_smokestack` |
| `stack_brick` | `tfmg:brick_smokestack` |
| `stack_metal` | `tfmg:metal_smokestack` |
| `fence_standard` | `the_wasteland_reworked:mesh_fence` |
| `fence_secure` | `immersiveengineering:steel_fence` |
| `fence_post` | `immersiveengineering:steel_post` |
| `barrier_road` | `the_wasteland_reworked:barricade` |
| `lamp_street` | `tfmg:gas_lamp` |
| `lamp_service` | `immersiveengineering:cagelamp` |
| `lamp_flood` | `immersiveengineering:floodlight` |
| `lamp_interior` | `tfmg:modern_light` |
| `lamp_interior_public` | `tfmg:circular_light` |
| `ladder_service` | `immersiveengineering:metal_ladder_steel` |
| `scaffold` | `immersiveengineering:steel_scaffolding_standard` |
| `support_beam` | `the_wasteland_reworked:support_beam` |
| `vent_plant` | `the_wasteland_reworked:bunker_fan` |
| `hazard_marking` | `tfmg:yellow_caution_block` |
| `hazard_marking_restricted` | `tfmg:red_caution_block` |
| `hazard_surface` | `the_wasteland_reworked:hazard_concrete` |
| `radiation_sign` | `the_wasteland_reworked:radiation_hazard_sign` |
| `road_sign` | `the_wasteland_reworked:road_sign` |
| `notice_board` | `supplementaries:notice_board` |
| `platform_rail` | `bellsandwhistles:station_platform` |
| `transit_cladding` | `bellsandwhistles:metro_panel` |
| `transit_cladding_corrugated` | `bellsandwhistles:corrugated_metro_panel` |
| `transit_casing` | `bellsandwhistles:metro_casing` |
| `transit_window` | `bellsandwhistles:metro_window` |

### 5.4 Ground contexts

`ground_plate()` in `scripts/structure_geometry_primitives_v2.py` takes a `site_context` from a fixed set (`urban_paved`, `rural_worked`, `industrial_hardstanding`, `wilderness_undisturbed`, `waterfront`). Karsic needs three additions to `_GROUND_PALETTES`; this is a prerequisite listed in §13.

| Context | Status | Palette |
|---|---|---|
| `urban_paved` | existing | unchanged |
| `industrial_hardstanding` | existing | unchanged |
| `rural_worked` | existing | unchanged |
| `wilderness_undisturbed` | existing | unchanged |
| `waterfront` | existing | unchanged |
| **`karsic_district_yard`** | **new** | `tfmg:asphalt`, `minecraft:gray_concrete`, `minecraft:coarse_dirt`, `minecraft:gravel` — the worn communal courtyard: paving that gave up and reverted to bare ground in the middle. |
| **`karsic_rail_ballast`** | **new** | `minecraft:gravel`, `tfmg:asphalt`, `minecraft:cobblestone`, `minecraft:coarse_dirt` — trackside working surface. |
| **`karsic_frozen_ground`** | **new** | `minecraft:coarse_dirt`, `minecraft:packed_ice`, `minecraft:gravel`, `quark:permafrost_bricks` — northern extremity only. Assigned per roster entry, never a default. |

### 5.5 Decay ladder

Collapse phases (canon §"Collapse-phase visual overlays") map to material substitutions. Applied in Pass P8 only, never earlier.

| Phase | Wall | Glazing | Roof | Ground |
|---|---|---|---|---|
| A — normal | profile as authored | as authored | as authored | as authored |
| B — early anomaly | `immersiveengineering:concrete_brick_cracked` at 1 panel in 12 | as authored | as authored | as authored |
| C — active containment | patched panels; `the_wasteland_reworked:lead_plating` over service penetrations | some `quark:dirty_glass_pane` | as authored | `the_wasteland_reworked:hazard_concrete` on screening routes |
| D — late containment | `tfmg:cast_iron_bars` in openings; `the_wasteland_reworked:barricade` at lanes | mostly `quark:dirty_glass_pane`, some empty | scorch course | hazard concrete, blast scour |
| E — post-collapse | `the_wasteland_reworked:rusted_lead_plating`; gravel rubble aprons; moss on brick strata only | empty frames; surviving bars | breached, gravel apron below | `minecraft:coarse_dirt`, `the_wasteland_reworked:wasteland_moss` |

**Moss rule.** Organic reclamation attaches to K-I brick and K-II render readily, to K-III concrete slowly, and to K-IV stone almost never. A small detail that does disproportionate work: it keeps the strata legible even in total ruin.

---

## 6. Massing grammar

### 6.1 The two dimensional modules, and why they are what they are

**Horizontal: the Karsic panel bay is 4 blocks.**

Real prefabricated panel construction expresses a joint at every panel edge, and that joint rhythm is legibility carrier #1. Four is chosen over three because `convert_nbt_to_lostcities.py` slices every structure into **16×16 chunk cells**: at a 4-block bay the joint line lands exactly on the cell boundary, so panel joints can never disagree across a converted seam. At a 3-block bay the rhythm walks across the seam and any per-cell rounding shows up as a visible kink in the façade. Four bays per cell, four cells per common slab length.

**Vertical: the Karsic storey is 6 blocks.**

`FLOOR_HEIGHT = 6` is hard-coded in `convert_nbt_to_lostcities.py`, and Lost Cities re-stacks the last authored band when `maxfloors` exceeds the authored count. A Karsic panel block is *the* archetypal "repeat one storey N times" building, so making the storey module equal the converter's band height buys a real feature: **one authored asset yields a five-storey and a nine-storey block from the same parts**, purely through `buildingsettings.minfloors`/`maxfloors`.

The consequence is binding: for every structure marked **repeatable** in the roster (§10), the second storey band must be *silhouette-identical* to every band above it — same wall plane, same opening positions, same joint columns. A validator check for this is specified in §13.4. Ground/plinth bands and roof bands are exempt and are authored separately.

Storey budget inside the 6-block band: 1 slab + 4 clear + 1 service void (pipe run / ceiling zone).

### 6.2 Wall construction by stratum

| Stratum | Wall thickness | Window reveal | Notes |
|---|---|---|---|
| K-I | 2 | 1 (inside the 2) | Segmental head expressed with stair blocks over the opening. |
| K-II | 1 | 1 (recess the glass) | String course slab at every floor line. |
| K-III | 1 | 1 (recess the glass) | `panel_joint` column every 4; `panel_joint` course at every floor line. The grid must be continuous and unbroken across the whole façade. |
| K-IV | 2 | 2 — deep reveal is the point | `pilaster` at every second bay, full height, 1 block proud. |
| K-V | 1 cladding over the host wall | 0 — flush glazing | Cladding starts one block proud of the host, so the graft reads as added. |

### 6.3 Standard elements

**Plinth.** The ground storey is `plinth` material and sits **1 block proud** of the upper wall plane on all elevations. This single offset is the cheapest and most reliable Karsic read in the entire system; it is mandatory on every K-II/K-III/K-IV structure over one storey.

**Parapet and bulkhead.** Flat `roof_deck`, parapet 2 blocks above deck capped with `parapet_cap`, and exactly one bulkhead (3×3 minimum, 5×5 for institutional) three blocks tall, seated **over the stair core** — never arbitrarily placed. Roof plant (`vent_plant`, dishes for K-V) clusters against the bulkhead, not scattered.

**Double vestibule.** Every principal entrance: a projecting porch 5 wide × 3 deep × 4 high, canopy slab at +4 oversailing by 1, `door_public` outer double leaf, `vestibule_inner` inner leaf, and a 2-block unheated lobby between them. Three risers up from grade to plinth level. This is cold engineering made visible from the street and it is mandatory on every heated Karsic building.

**Stair tower.** `encased_stairwell()` from `scripts/structure_geometry_primitives_v2.py`, width 2, `wall=stair_core_wall`, expressed on the exterior as a shallow projection with a **continuous vertical glazing slot** in `glazing_industrial` running the full height. On slabs, one tower per 4 bays of length; minimum two per building.

**Chimney/stack.** Only where there is a real combustion or process reason. `stack_brick` for K-I, `stack_industrial` for K-III/K-IV, `stack_metal` for K-V retrofits. A Karsic stack is tall and slender, standing clear of the roof mass, not a decorative stub.

### 6.4 Silhouette rules by class

| Class | Rule |
|---|---|
| **Residential slab** | Length ≥ 3× height. Single extruded prism above the plinth — **no setbacks, no varied top**. The building has no crown. |
| **Residential point block** | Square-ish plan, 8–14 storeys, single central core, identical floors, one bulkhead. |
| **Institutional (K-IV)** | Symmetric about a central axis. Entrance dead-centre. Forecourt depth ≥ building height. Flat entablature band at the top, above the last window head, with no cornice projection greater than 1. |
| **Industrial hall** | One dominant clear-span volume with a clerestory glazing band under the eaves, one attached low ancillary block (offices/amenities), one stack, and a rail-side gantry. |
| **Utility kiosk** | Single storey, windowless or one high slot, flat roof, no plinth offset, ventilation louvre, standard fence 3 blocks clear on all sides. |
| **Landmark** | Same rules as its class; landmark status is expressed by **size and approach**, never by adding ornament. |

---

## 7. Plan grammar

### 7.1 Circulation

| Element | Karsic value | Notes |
|---|---|---|
| Institutional corridor | **3 wide**, double-loaded | Rooms both sides, stair cores at both ends, no dead ends. |
| Residential access | **2-wide gallery** or a 2×2 landing per core | Slabs use stair cores serving 2–4 doors per landing; the long open gallery is reserved for the courtyard block type. |
| Industrial access lane | **4 wide** | Machine access; must run the full length of the hall and reach a door at each end. |
| Basement pipe gallery | **3 wide, 3 high** | Runs the building's long axis; connects to the exterior heating main. |
| Stairs | `encased_stairwell()`, never bare | V2 §3.2. Bare ladders only for tank access, roof plant, and watchtowers. |

### 7.2 Room modules

| Module | Size | Used by |
|---|---|---|
| Cellular office / classroom | 1 bay × 5 deep (4×5) | Administration, institutes, schools. |
| Double room / ward / lab | 2 bays × 5 deep (8×5) | Hospitals, laboratories, dormitories. |
| Apartment | 2 bays × 7 deep (8×7) | One living/kitchen zone, one bed zone, one bath/store zone, entered from a landing. |
| Assembly hall | 5 bays × 11 deep, 2 storeys clear | Schools, palaces of culture, institutes. |
| Machine hall | free span, 5+ bays, 3+ storeys clear | Industry. Crane rail at eaves. |
| Control room | 2 bays × 4 deep, mezzanine | Glazed to the volume it controls. Mandatory on every process building. |
| Changing + wash block | 3 bays × 5 deep | **Mandatory on every industrial building**, adjacent to the workers' entrance, per canon. |

### 7.3 Mandatory interior facts

These are not suggestions; a Karsic structure that omits an applicable item fails review.

1. **Every heated building has a basement service level** — pipe gallery, electrical room, and store — connected to the exterior heating main. This is where most of the collapse story lives.
2. **Every industrial building has the changing/wash block** at the workers' entrance.
3. **Every process building has a control room overlooking its volume** through glazing at mezzanine level.
4. **Every institution numbers itself** — see §9.2.
5. **Standardised furniture recurs.** The same desk arrangement, the same shelf run, the same bench, the same locker bank, across unrelated institutions. Use the `zvhouses:*` counter/shelf/bench family and `supplementaries:item_shelf` consistently so the repetition is real.
6. **Modernisation is layered, not total.** Where a K-V secondary stratum is declared, the new equipment sits *inside* older fabric: new terminals in an old control room, a modern lab spliced into a legacy utility tunnel, upgraded doors in original concrete frames.

### 7.4 Front-of-house / back-of-house

For **K-III**, back-of-house is **behind** — service yard, loading, plant, and staff entrance on the opposite elevation from the public entrance, at the same level.

For **K-IV**, back-of-house is **below** — service access is from a basement yard or a rear ramp, keeping the ceremonial elevation clean.

This split is a per-stratum generator parameter, not a per-building decision.

---

## 8. The conversion pass system

This is the core of the program. Nine ordered passes convert one base clean master into one Karsic master. Each pass has a stable ID, a declared input and output artefact, an idempotency guarantee, a derived seed, and a validator. **Passes run in order and never skip.** A pass may be re-run at any time and must produce byte-identical output.

### 8.0 Determinism contract

```
seed(structure_id, pass_id, variant) =
    zlib.crc32(f"karsic|{structure_id}|{pass_id}|{variant}".encode("utf-8")) & 0x7FFFFFFF
```

- No `random.random()` without an explicit `random.Random(seed)` instance.
- No iteration over `set` or `dict` where order affects placement; sort first.
- No wall-clock, no `os.urandom`, no PID, no environment.
- Worldgen placement salts (which must be literal integers in JSON) are allocated from the reserved Karsic range **79100000–79109999**. Verified unused against every existing `structure_set` salt in the pack as of 2026-08-26. Pelagos holds 79200000–79209999.

### 8.1 P0 — Regional assignment

| | |
|---|---|
| **Input** | `structure_library/catalog.json` (85 clean masters) |
| **Output** | `structure_library/regional/karsic-assignment.json` |
| **Writes geometry** | No |
| **Validator** | `validate_regional_assignment.py`: every base master has exactly one class; every `X` has a named substitute that exists in the roster; no orphan substitutes. |

Assigns every base clean master one of four **conversion classes**:

- **N — Native.** The Directorate builds this type as a core part of its identity. Full pass run, high pass intensity.
- **A — Adapted.** An equivalent exists but the program differs materially. Full pass run; P5 (plan) does the heavy lifting.
- **F — Foreign.** Appears rarely and deliberately, and must communicate why it is there (contract C6). Kept close to the base form; P7 dressing carries the "this is not ours" reading.
- **X — Excluded.** The Directorate does not build this. A **named native substitute** takes its slot in the citystyle selectors so no gameplay role is left unfilled.

The complete assignment is §10.

### 8.2 P1 — Program authoring

| | |
|---|---|
| **Input** | P0 assignment + base program (where one exists in `structure_library/programs/`) |
| **Output** | `structure_library/programs/kar_<nnn>_<slug>.json` |
| **Writes geometry** | No |
| **Validator** | `validate_structure_programs.py` (existing), extended with a Karsic schema check |

Per V2 §3.1, the program file is a **required generation input**, not documentation written afterwards. A Karsic program adds these fields to the existing schema:

```json
{
  "structure_id": "infinite_domain:kar_017_state_series_panel_block",
  "culture": "karsic",
  "conversion_class": "N",
  "primary_stratum": "K-III",
  "secondary_stratum": "K-II",
  "repeatable_storey": true,
  "site_context": "karsic_district_yard",
  "foundation_profile": "full_basement",
  "back_of_house": "behind",
  "district_role": "courtyard_slab",
  "rail_served": false,
  "heating_main_connection": "north_basement",
  "signage_series": "SERIES 4 / BLOCK 12",
  "archetype": "...",
  "orientation": { ... },
  "<domain>_program": [ ... ],
  "damage_constraints": [ ... ],
  "review_gate": { ... }
}
```

**No geometry pass may run for a structure whose program file is absent or fails schema validation.** This is the single most important sequencing rule in the document — V2 §3.1 exists because the previous 84 assets were built without it.

### 8.3 P2 — Massing conversion

| | |
|---|---|
| **Input** | P1 program; base master footprint/height from `catalog.json` |
| **Output** | Regenerated shell in `kubejs/data/infinite_domain/structure/karsic/masters/<slug>_clean_master.nbt` (shell only) |
| **Writes geometry** | **Yes — first geometry pass** |
| **Gate** | Visual Gate A equivalent (`HEAVY_REBUILD_DOCTRINE.md` §VII-A): massing and scale review |

Operations, in order:

1. Snap the footprint to the bay module: `W = 4n`, `D = 4m`, then add the plinth offset ring.
2. Snap the height to the storey module: `H = 6 × storeys`, plus roof band.
3. Establish `terrain_footing()` with the program's `foundation_profile`.
4. Extrude the body as a single prism; establish the plinth ring 1 proud.
5. Place stair-core projections per §6.3 (one per 4 bays, minimum two).
6. Place the vestibule porch on the declared public elevation.
7. Establish parapet, cap, bulkhead over the core.
8. For industrial: clear-span hall + ancillary block + stack position.

**Footprint drift budget.** The Karsic footprint may differ from its base master by at most **±20 %** in either axis; beyond that, the `minimum_lot` in `catalog.json` must be re-derived and the settlement archetypes in §11 re-checked, because Lost Cities lot fitting is driven from those numbers. Drift beyond ±20 % is allowed but must be recorded in the roster with a reason.

### 8.4 P3 — Fabric conversion

| | |
|---|---|
| **Input** | P2 shell; `structure_library/regional/karsic-material-profile.json` |
| **Output** | Same NBT, every structural block resolved from role → block |
| **Writes geometry** | Yes (substitution only, no shape change) |
| **Validator** | Profile completeness + registry existence |

This is the deterministic material layer. Two gate conditions:

1. **Completeness.** Every role referenced by any Karsic generator resolves for every stratum the roster uses. A missing role is a hard failure, never a silent fallback.
2. **Registry existence.** Every block string in the profile — including every slab/stair/wall derivative — exists in `docs/registry-inventory/block-ids.txt`. Run this as a standalone check before P3 executes:

```bash
python scripts/validate_material_profile.py --culture karsic --registry docs/registry-inventory/block-ids.txt
```

#### 8.4.1 The retrofit path for already-converted assets

The 11,940 part files under `kubejs/data/infinite_domain/lostcities/parts/converted/` each carry a **local palette** — a `palette.palette` array of concrete `{char, block}` entries. Local palettes override the Lost Cities style palette, which means a style/palette change (§11.2) **cannot** re-tint an already-converted building interior.

That gives a second, much cheaper P3 path for assets not worth regenerating from NBT: a **palette remap manifest** that rewrites only the `block` values in each part's local palette, leaving `slices` untouched.

```
scripts/remap_lostcities_palette.py \
    --manifest structure_library/regional/karsic-palette-remap.json \
    --src kubejs/data/infinite_domain/lostcities/parts/converted \
    --dst kubejs/data/infinite_domain/lostcities/parts/karsic
```

**This path is explicitly NOT a conversion.** It changes materials and nothing else, and therefore violates contract C3 on its own. It is permitted only for:

- **F-class** structures, where staying close to the base form is the point;
- **interim previews**, so a district can be looked at in-world before its geometry is authored;
- **prop-scale and vehicle assets** whose identity really is carried by material.

Every asset that goes through the remap path alone must be marked `fabric_only: true` in the roster and is barred from production approval until it has been through a full P2–P8 run.

### 8.5 P4 — Envelope conversion

| | |
|---|---|
| **Input** | P3 fabric |
| **Output** | Openings and roof authored |
| **Validator** | `structure_geometry_lint.py` check 3 (window/door wall-coupling) |

Per V2 §3.3, an opening is placed by the **same operation** that establishes the wall segment framing it. Use `wall_window()` from the v2 primitives; never place glass by coordinate.

Karsic opening rhythm:

- One opening per bay, centred, 2 wide × 2 high, sill at slab + 1, recessed per §6.2.
- Ribbon option (K-III institutional and K-IV): a continuous 2-high band with a `panel_joint` mullion at each bay line.
- Ground storey openings are the same width but 1 block shorter, and receive `window_guard` where the program declares a secure or retail ground floor.
- Stair towers take the continuous vertical slot, never punched openings.
- Industrial halls take a clerestory band in the top 2 blocks of the wall, plus loading openings sized to the program.

Roof: flat deck, parapet, cap, one bulkhead. No pitched roof on K-III/K-IV under any circumstances. K-I and K-II may take a shallow hipped roof in `quark:gray_shingles`; that is the only pitched roof the Directorate builds.

### 8.6 P5 — Plan conversion

| | |
|---|---|
| **Input** | P4 envelope; P1 program's room lists |
| **Output** | Interior zoning, circulation, partitions, vertical circulation |
| **Validator** | `structure_geometry_lint.py` checks 1–2 + check 6 (program-conformance ledger) |

This is the pass that makes an **A-class** conversion legitimately different from its base master, and it is where most of the review risk sits. Operations:

1. Lay the circulation spine per §7.1 before any room.
2. Place stair cores as *rooms* (`encased_stairwell` inside a walled shaft), landing-connected at both ends.
3. Subdivide into the §7.2 modules along the bay grid — room partitions land on bay lines, never mid-bay.
4. Insert the mandatory interior facts from §7.3 that apply.
5. Cut the basement service level and connect it to the exterior heating main stub.
6. Dress each declared room to make its purpose legible at player scale (V2 §3.7 — per-room minimum, not a whole-building count).

**Check 6 is the real gate here.** The generated room ledger must diff cleanly against the program's declared rooms. A Karsic building whose interior cannot be matched back to its own program fails regardless of block count.

### 8.7 P6 — Site conversion

| | |
|---|---|
| **Input** | P5 interior |
| **Output** | Lot surface, boundary, approach, external services |
| **Validator** | `structure_geometry_lint.py` check 5 (ground-context validator) |

1. `ground_plate()` with the program's `site_context` (§5.4).
2. `terrain_footing()` grade-transition skirt — confirm it survived P2–P5 intact.
3. Boundary: `fence_standard` on posts for ordinary sites, `fence_secure` for military/restricted, **nothing** for courtyard-district sites where the buildings themselves make the enclosure.
4. **The heating main.** Where the program declares `heating_main_connection`, run an above-ground insulated main on `pipe_saddle` supports from the building's basement stub to the lot edge, at saddle height 2–3, stepping to a `service_gantry` where it crosses a road. This runs *off the lot* and terminates at the template edge so neighbouring Karsic structures visually connect. **This is legibility carrier #3 and it is what makes a Karsic district read as a system rather than a set of buildings.**
5. Standard site kit: `lamp_street` at 12-block spacing along the approach, `notice_board` beside the vestibule, `road_sign` at the lot entry, bollards at the forecourt edge.
6. Approach: for K-IV, an axial forecourt ≥ building height in depth, paved, with a symmetrical stair. For K-III residential, a footpath entering the courtyard from the road ring.
7. Rail: where `rail_served` is true, a siding stub reaching the template edge, ballast in `karsic_rail_ballast`, and a gantry or loading dock over it.

### 8.8 P7 — Institutional dressing

| | |
|---|---|
| **Input** | P6 site |
| **Output** | Signage, numbering, standard furniture, lighting, colour accents |
| **Validator** | Signage-grammar lint (§9.2) + `backed_sign()` backing check (lint check 2) |

See §9 in full. Every sign uses `backed_sign()`; an unbacked sign is a hard lint failure.

### 8.9 P8 — Collapse authoring

| | |
|---|---|
| **Input** | P7 dressed clean master (**immutable from here**) |
| **Output** | `kubejs/data/infinite_domain/structure/karsic/<slug>.nbt` (damage variant) and, where the roster declares one, an occupation variant |
| **Validator** | `structure_geometry_lint.py` check 4 (damage coherence) |

Per V2 §3.4, damage is an **authored event**. Never `t.clear()` on a box; never per-block random deletion as a primary method. Use `fracture_breach()`, which internally calls `retrofit_window_for_breach()` so a breach can never leave a floating window.

The Karsic damage grammar, derived from §4.5:

| Damage archetype | Where it applies | Reads as |
|---|---|---|
| **Frozen district** | Residential slabs, schools, clinics | Heating main severed at one saddle; the buildings *downstream* of the break show burst risers, ice, and boarded windows while the upstream ones do not. **The break must be visible on the lot.** |
| **Cannibalisation** | Substations, plant rooms, machine halls | One facility stripped of switchgear/pumps, with cut cable ends and drag marks, to keep a neighbour alive. The absence is the story. |
| **Heroic maintenance** | Boiler houses, pump stations, rail sheds | The same pump or seal repaired many times: a stack of replacement parts beside the failed unit, a wall of tally marks, a workbench that never got tidied. |
| **Sealed basement** | Any building with a service level | Public floors open to the sky; the basement dry, lit, and still holding stores. The contrast is the point. |
| **Failed assembly point** | Bus stations, rail stations, squares | Queue barriers, abandoned baggage, a departure board frozen mid-update, vehicles that never left. |
| **Firebreak edge** | Military, restricted, and one landmark | Scorch course on the exposed elevation, blast scour on the ground, intact fabric on the sheltered side. |
| **Partitioned survivor wing** | Institutes, hospitals, palaces of culture | One wing sealed with improvised partitions, stove flue punched through a window, everything else dark. |

The roster assigns each structure one primary and at most one secondary archetype. **A Karsic damage variant must preserve** both stair cores where two exist, the basement route, and at least one intact vestibule, unless the program's `damage_constraints` explicitly says otherwise.

### 8.10 P9 — Assembly and integration

| | |
|---|---|
| **Input** | P8 variants |
| **Output** | Catalog entries, Lost Cities assets, citystyle and worldstyle wiring, tags |
| **Validator** | The full existing validator suite (§13) |

1. Append catalog entries to `structure_library/catalog.json` — `clean_master` + `damage_variant` per structure, following the existing schema exactly (`structure-metadata.schema.json`).
2. Run the existing converter, pointed at the Karsic output tree:
   ```bash
   python scripts/convert_nbt_to_lostcities.py --all
   ```
   producing `parts/karsic/`, `buildings/karsic/`, `multibuildings/karsic/`, `scattered/karsic/`.
3. Author Karsic palettes and style (§11.2), citystyles (§11.3), worldstyle selectors (§11.4).
4. Author biome tags and placement (§12).
5. Run the full gate.

**Nothing is production-approved until §13 passes.** `structure_library/production-approvals.json` is the only place approval is recorded, and its `required_checks` list applies to Karsic assets unchanged.

---

## 9. Institutional identity, signage, and evidence

### 9.1 The naming grammar

The Directorate does not name things; it **numbers** them. Institutional identity is carried by a consistent ordinal grammar, not by exotic vocabulary or foreign script. Every Karsic institution resolves to:

```
<FUNCTION> <ORDINAL>            e.g.  DISTRICT HEATING STATION 2
<FUNCTION> <ORDINAL> / SECTION <LETTER>
<FUNCTION> <ORDINAL> / SHOP <N>          (industrial)
<FUNCTION> <ORDINAL> / BLOCK <N>         (residential, medical)
SERIES <N>                               (a catalogue design, not a place)
```

Ordinals are **not globally unique** — that is deliberate. Two different regions each having a "District Heating Station 2" is exactly the reading we want: the numbering is local to an administration, and the administration is one of many. The generator assigns ordinals deterministically from the structure seed within a small range (1–9 for stations, 1–24 for shops, 1–48 for blocks).

Institution words in use (English, plain, institutional):
`ADMINISTRATION`, `COMBINE`, `DEPOT`, `DIRECTORATE`, `INSTITUTE`, `SECTION`, `SHOP`, `STATION`, `TRUST`, `WORKS`, `YARD`, `CORDON`, `POST`, `HOUSE OF CULTURE`, `SANATORIUM`, `POLYCLINIC`, `TECHNICUM`.

### 9.2 Signage rules

1. Every sign uses `backed_sign()` from the v2 primitives. An unbacked sign is a hard lint failure (check 2).
2. **Building identification goes on the plinth**, beside the vestibule, at eye height — one sign, the full institutional name.
3. **Wayfinding is by section, floor, and technical function**, not by room name: `SECTION B`, `FLOOR 3`, `PIPE GALLERY`, `SWITCHROOM`, `CHANGING`, `SHOP 4`.
4. **Safety language is imperative and impersonal**: `AUTHORISED PERSONS ONLY`, `KEEP CLEAR OF TRACK`, `HELMET AREA`, `NO ADMITTANCE WITHOUT PERMIT`.
5. Existing project institutions (VCF, Atlas, PolyCore, Pleroma, Aevum, Helion, Blackglass, Asterion, Continuity) appear in Karsic territory as **licensed local operations under Directorate numbering** — the corporate name is present but subordinate to the ordinal:
   `HELION / DISTRICT HEATING STATION 2` rather than a corporate campus sign.
6. **No signage is decorative.** If a sign does not name a real thing that exists in that building, it does not go up.

### 9.3 Standard furniture

Repetition is the culture (§4.1), so the furniture kit is fixed and reused verbatim across unrelated institutions:

| Fitting | Blocks |
|---|---|
| Office desk run | `zvhouses:*_counter` + `zvhouses:*_countertop` (spruce family throughout Karsic) |
| Institutional shelving | `supplementaries:item_shelf` in continuous runs, always full-height wall to wall |
| Bench (corridor, changing, waiting) | `zvhouses:spruce_bench` |
| Locker bank | `minecraft:barrel[facing=north]` in a solid run at floor + 1 |
| Notice board | `supplementaries:notice_board` beside every entrance and at every corridor junction |
| Records / archive | `minecraft:bookshelf` runs + `supplementaries:book_pile` |
| Canteen | `zvhouses:spruce_table` + `zvhouses:spruce_chair` in a fixed 2×4 repeating unit |

The spruce family is chosen and then **never varied by building**. A Karsic school and a Karsic pump house have the same bench.

### 9.4 Environmental evidence

Per canon §"Environmental evidence first", at least one major story point per quest-grade Karsic structure must be readable without opening a book. Karsic-specific examples, all buildable:

- The heating main severed at one saddle, with frost damage visible **only** on the buildings downstream of the break.
- A maintenance log board with dozens of tally marks against one pump, and a stack of replacement seals beside it that were never fitted.
- A substation stripped bare, with cable ends cut clean and a drag trail leading toward a hospital that still has lights.
- A basement store, dry and intact, under a hall open to the sky.
- An evacuation assembly point with a numbered boarding order painted on the ground and no vehicles.
- A sealed survivor wing: improvised partitions, a stove flue punched through a window, and a heat map of soot showing which rooms stayed warm.
- Modern lab equipment cabled through a fifty-year-old utility tunnel, because there was nowhere else to route it.

### 9.5 Loot doctrine

Loot tables follow the established pack path convention: `infinite_domain:chests/karsic/<slug>`.

- **Most Karsic structures carry no chest.** Identity is carried by geometry; loot is not the reward for recognising a region.
- **Guaranteed evidence chests** exist only where a quest depends on the item, matching the abyssal program's precedent.
- **No progression shortcuts.** A Karsic industrial site must not hand out a tier the player has not earned; this mirrors `pool_contract.no_progression_breaking_loot` in the abyssal catalog and the standing rule in `docs/WASTELAND_CITY_PROGRESSION_BYPASS_AUDIT.md`.
- **Regional loot presentation differs even where contents do not.** Karsic supplies arrive in numbered depot crates and sealed technical stores; the same items in Pelagos arrive in mixed commercial packaging. Presentation is a P7 concern, contents are a balance concern, and the two are decided separately.

---

## 10. The Karsic roster

**94 masters: 82 conversions of the 85 base clean masters, 3 base masters excluded, and 12 native additions (3 of which are the mandatory substitutes for the exclusions).**

Class key: **N** native · **A** adapted · **F** foreign/displaced · **X** excluded, substitute named.
Strata use the §4.4 IDs; `⊕` marks a declared secondary stratum.
Damage archetypes are from §8.9.

### 10.1 Agricultural

| Base master | Cls | Karsic ID | Karsic identity | Strata | Damage | Note |
|---|---|---|---|---|---|---|
| `abandoned_orchard_cannery` | A | `kar_001_fruit_processing_combine` | Fruit Processing Combine | K-I ⊕ K-III | heroic maintenance | Brick canning works with a later concrete cold store bolted on; rail-fed. |
| `decayed_farm` | A | `kar_002_state_farm_unit` | State Farm Unit | K-II ⊕ K-III | frozen district | Long barn rows, machine yard, silo bank, and a workers' block — all on one axis, all one design. |
| `decayed_ranch` | A | `kar_003_livestock_station` | Livestock Station | K-II | heroic maintenance | Heated barn with its own boiler stub, feed silo, veterinary hut. |
| `ruined_grain_elevator` | N | `kar_004_grain_reception_point` | Grain Reception Point | K-III | cannibalisation | Concrete silo bank, rail scale house, conveyor gallery. Horizon silhouette. |
| `shattered_greenhouse_nursery` | N | `kar_005_heated_greenhouse_block` | Heated Greenhouse Block | K-III ⊕ K-V | frozen district | Steam-heated ranges fed from a boiler **on the lot** — the break is visible. |

### 10.2 Civic

| Base master | Cls | Karsic ID | Karsic identity | Strata | Damage | Note |
|---|---|---|---|---|---|---|
| `ae2_records_archive` | A | `kar_006_state_archive_repository` | State Archive Repository | K-IV ⊕ K-V | sealed basement | Hardened deep stacks beneath a monumental reading hall. |
| `emergency_relief_shelter` | A | `kar_007_civil_defence_shelter` | Civil Defence Shelter | K-III | failed assembly point | Half-buried, blast doors, filter plant, bunk bays, assembly yard. |
| `fire_station` | A | `kar_008_fire_rescue_detachment` | Fire and Rescue Detachment | K-II ⊕ K-III | cannibalisation | Appliance bays, drill/hose tower, dormitory above. |
| `roadside_church_cemetery` | A | `kar_009_memorial_and_chapel` | Memorial and Chapel | K-I ⊕ K-IV | partitioned survivor wing | Walled cemetery, small brick chapel, and a concrete obelisk on an axis. Civic memory, not religion, carries the site. |
| `ruined_city_school` | N | `kar_010_school_series_block` | School (Series) | K-III | frozen district | Symmetric catalogue school, gymnasium wing, assembly hall, asphalt yard. |
| `ruined_community_center` | N | `kar_011_house_of_culture` | House of Culture | K-IV | partitioned survivor wing | **The Karsic civic landmark type.** Colonnade, auditorium, club rooms, oversized forecourt. |
| `ruined_courthouse` | A | `kar_012_district_administration` | District Administration | K-IV | failed assembly point | Axial approach, flat entablature, council chamber, records basement. Administration, not a court. |
| `ruined_cyberware_clinic` | A | `kar_013_prosthetics_institute` | Prosthetics and Rehabilitation Institute | K-III ⊕ K-V | sealed basement | Aevum-linked under Directorate numbering (§9.2 rule 5). |
| `ruined_hospital` | N | `kar_014_district_hospital` | District Hospital | K-III ⊕ K-II | frozen district | Separate *korpus* blocks linked by **heated galleries** — the enclosed link is the identity. |
| `ruined_police_precinct` | A | `kar_015_militia_district_station` | Militia District Station | K-II ⊕ K-III | cannibalisation | Duty room, holding block, vehicle yard. |
| `ruined_ranger_station` | A | `kar_016_forestry_cordon` | Forestry Cordon | K-I ⊕ K-II | heroic maintenance | Remote timber-and-brick cordon, watch mast, garage. |

### 10.3 Commercial

| Base master | Cls | Karsic ID | Karsic identity | Strata | Damage | Note |
|---|---|---|---|---|---|---|
| `abandoned_truck_stop` | A | `kar_017_highway_service_point` | Highway Service Point | K-III | failed assembly point | Canteen, driver rest block, fuel, inspection pit. |
| `bombed_hotel` | A | `kar_018_state_hotel` | State Hotel | K-III ⊕ K-IV | partitioned survivor wing | Monumental plinth under a repeating slab tower. |
| `buried_bank_vault` | A | `kar_019_state_bank_branch` | State Bank Branch | K-IV | sealed basement | Stone-faced branch, basement strongroom. |
| `cratered_downtown_intersection` | A | `kar_020_administrative_square` | Administrative Square | K-IV ⊕ K-III | firebreak edge | Axial boulevard, memorial, trolleybus catenary, crater. |
| `grocery` | N | `kar_021_gastronom` | Gastronom | K-III | frozen district | State grocery in the glazed ground floor of a panel slab. **Core common structure — this one must be everywhere.** |
| `motel` | A | `kar_022_roadside_rest_house` | Roadside Rest House | K-II | failed assembly point | Dormitory rest house with a shared canteen. No individual car doors — the Directorate does not build motels. |
| `ruined_department_store` | N | `kar_023_univermag` | Univermag | K-III ⊕ K-V | cannibalisation | Concrete frame, ribbon glazing, escalator hall, later cladding graft. |
| `ruined_mixed_use_block` | N | `kar_024_panel_block_service_premises` | Panel Block with Service Premises | K-III | frozen district | The everyday Karsic street building. |
| `ruined_office_tower` | A | `kar_025_design_institute_tower` | Design Institute Tower | K-III ⊕ K-V | partitioned survivor wing | Drawing halls, brise-soleil, repeated bays. |
| `ruined_roadside_diner` | A | `kar_026_roadside_canteen` | Roadside Canteen | K-II | heroic maintenance | Serving line and communal tables. No booths. |
| `ruined_shopping_mall` | A | `kar_027_trade_centre` | Trade Centre | K-III | failed assembly point | Concrete-frame market hall with skylights and a covered arcade. |
| `sunken_city_front` | A | `kar_028_embankment_front` | Embankment Front | K-I ⊕ K-III | frozen district | Granite retaining wall, flooded ground floors, mooring rings. |
| `toppled_skyscraper` | A | `kar_029_toppled_institute_tower` | Toppled Institute Tower | K-III | firebreak edge | The tower fell across a courtyard district; the courtyard is part of the asset. |
| `trade_outpost` | A | `kar_030_supply_point` | Directorate Supply Point | K-II ⊕ K-III | cannibalisation | Fenced, rail- or river-fed, numbered stores. |

### 10.4 Highway

| Base master | Cls | Karsic ID | Karsic identity | Strata | Damage | Note |
|---|---|---|---|---|---|---|
| `delivery_van` | N | `kar_031_service_van` | Service Van | prop | — | Cab-over box van. Prop-scale, fabric-led. |
| `destroyed_refugee_convoy` | N | `kar_032_evacuation_convoy` | Evacuation Convoy | K-III kit | failed assembly point | Buses and trucks with a **numbered boarding order painted on the road** — the plan existed and failed. |
| `gas_station` | N | `kar_033_fuel_station` | Fuel Station | K-III | heroic maintenance | Canopy on concrete columns, kiosk, tank inspection covers. |
| `mountain_pass_terminator` | N | `kar_034_avalanche_gallery` | Pass Avalanche Gallery | K-III | firebreak edge | Concrete gallery closing the road end. Cold engineering at road scale. |
| `ruined_bus_terminal` | N | `kar_035_bus_station` | Bus Station | K-III ⊕ K-IV | failed assembly point | Cantilevered concrete canopy over sawtooth stands, departure board, ticket hall. |
| `sunken_highway_interchange` | A | `kar_036_grade_separated_interchange` | Grade-Separated Interchange | K-III | firebreak edge | |
| `wasteland_weigh_station` | A | `kar_037_traffic_inspection_post` | Traffic Inspection Post | K-II | failed assembly point | Barrier, weighbridge, glazed observation post. |
| `wrecked_sedan` | N | `kar_038_state_sedan` | State Sedan | prop | — | Boxy three-box saloon. |

### 10.5 Industrial

| Base master | Cls | Karsic ID | Karsic identity | Strata | Damage | Note |
|---|---|---|---|---|---|---|
| `abandoned_oil_field` | N | `kar_039_oil_field` | Oil Field | K-III | cannibalisation | |
| `abandoned_quarry` | N | `kar_040_stone_quarry` | Stone Quarry | K-II ⊕ K-III | heroic maintenance | Incline, crusher house, rail loading. |
| `bombed_data_center` | A | `kar_041_computing_centre` | Computing Centre | K-III ⊕ K-V | sealed basement | Cabinet hall on a raised floor, suppression bottles, hardened envelope. |
| `cold_industrial_mountain_port` | N | `kar_042_northern_industrial_port` | Northern Industrial Port | K-III | frozen district | Ice-class quay, heated warehouse, rail apron. Uses `karsic_frozen_ground`. |
| `collapsed_mine_entrance` | N | `kar_043_mine_headframe` | Mine Headframe | K-I ⊕ K-III | cannibalisation | Lattice headframe, winding house, and a full **pit bathhouse** — the changing/wash block at its largest. |
| `corporate_warehouse` | N | `kar_044_bonded_warehouse` | Bonded Warehouse | K-III | cannibalisation | Rail-served, numbered bays, gantry. |
| `crashed_cargo_airship` | A | `kar_045_downed_cargo_airship` | Downed Cargo Airship | prop | firebreak edge | |
| `create_factory` | N | `kar_046_machine_hall` | Machine Hall | **K-I ⊕ K-V** | heroic maintenance | Brick hall with a crane rail, modern line inside. K-I⊕K-V pair 1 of 4. |
| `decayed_logging_camp` | N | `kar_047_timber_combine` | Timber Combine | K-II | cannibalisation | Narrow-gauge rail, barracks, sawmill shed. |
| `excavator_pit` | N | `kar_048_dragline_pit` | Dragline Pit | K-III | cannibalisation | Walking dragline, conveyor bridge, spoil ridges. Landmark silhouette. |
| `industrial_facility` | N | `kar_049_industrial_combine` | Industrial Combine | K-III ⊕ K-V | heroic maintenance | Multi-shop combine on a numbered shop grid. |
| `municipal_incinerator` | A | `kar_050_waste_incineration_plant` | Waste Incineration Plant | K-III | cannibalisation | Tipping hall, furnace hall, tall stack. |
| `nuclear_research_annex` | N | `kar_051_reactor_service_annex` | Reactor Service Annex | K-IV ⊕ K-V | sealed basement | Hot cells, stack, hardened control, restricted fence. |
| `remote_sawmill` | N | `kar_052_forest_sawmill` | Forest Sawmill | K-I ⊕ K-II | heroic maintenance | |
| `ruined_fuel_depot` | N | `kar_053_fuel_depot` | Fuel Depot | K-III | firebreak edge | Tank farm, bunded walls, rail loading rack. |
| `scrapyard` | N | `kar_054_scrap_reclamation_yard` | Scrap Reclamation Yard | K-II | cannibalisation | **Where the cannibalised parts went.** Cross-reference this site's contents against nearby stripped facilities. |
| `service_garage` | N | `kar_055_motor_pool` | Motor Pool | K-II ⊕ K-III | heroic maintenance | Inspection pits, parts store, dispatcher's office. |
| `warm_industrial_mountain_port` | N | `kar_056_southern_industrial_port` | Southern Industrial Port | K-III | cannibalisation | |

### 10.6 Military

| Base master | Cls | Karsic ID | Karsic identity | Strata | Damage | Note |
|---|---|---|---|---|---|---|
| `battle_tank` | N | `kar_057_directorate_tank` | Directorate Tank | prop | — | |
| `bunker_network` | N | `kar_058_hardened_command_bunker` | Hardened Command Bunker | K-IV | sealed basement | Blast doors, filter plant, map room. |
| `military_checkpoint` | N | `kar_059_control_post` | Control Post | K-III | firebreak edge | Barrier, guard block, vehicle inspection bay. |
| `mountain_biohazard_lab` | N | `kar_060_isolated_biological_institute` | Isolated Biological Institute | K-III ⊕ K-V | sealed basement | Decontamination suite, incinerator, restricted perimeter. |
| `mountain_military_complex` | N | `kar_061_mountain_garrison` | Mountain Garrison | K-II ⊕ K-III | cannibalisation | Barrack rows, vehicle sheds, parade ground. |

### 10.7 Miscellaneous and railway

| Base master | Cls | Karsic ID | Karsic identity | Strata | Damage | Note |
|---|---|---|---|---|---|---|
| `collapsed_airship_terminal` | A | `kar_062_airship_mooring_terminal` | Airship Mooring Terminal | K-IV | failed assembly point | Mooring mast, hangar, passenger hall. |
| `survivor_cache` | A | `kar_063_civil_defence_stores_cache` | Civil Defence Stores Cache | K-III | sealed basement | Buried numbered stores. |
| `collapsed_subway_station` | N | `kar_064_deep_metro_station` | Deep Metro Station | K-IV | failed assembly point | **Surface vestibule pavilion + escalator incline + deep platform hall with a pilaster order.** One of the strongest types in the roster; treat as landmark. |
| `elevated_rail_collapse` | A | `kar_065_rail_overpass_collapse` | Rail Overpass Collapse | K-III | firebreak edge | |
| `freight_depot` | N | `kar_066_classification_yard` | Classification Yard | K-II ⊕ K-III | cannibalisation | Hump yard, control tower, wagon repair shed. |

### 10.8 Residential

| Base master | Cls | Karsic ID | Karsic identity | Strata | Damage | Note |
|---|---|---|---|---|---|---|
| `blown_apartment_complex` | N | `kar_067_series_panel_block` | Series Panel Block | K-III | frozen district | **The flagship repeatable-storey asset** (§6.1). One authored building must yield 5-, 7-, and 9-storey variants via `minfloors`/`maxfloors`. |
| `bungalow` | A | `kar_068_dacha` | Dacha | K-I ⊕ K-II | heroic maintenance | Small detached, stove chimney, veranda, garden plot, fence of scrap boards. The Directorate's one informal building. |
| `ruined_rowhouse_block` | A | `kar_069_workers_barrack_row` | Workers' Barrack Row | K-I | frozen district | Two-storey brick barracks, external stairs, shared outbuildings, a single standpipe in the yard. |
| `shattered_luxury_condo` | A | `kar_070_nomenklatura_block` | Nomenklatura Block | K-II ⊕ K-IV | partitioned survivor wing | Better-finished brick block with balconies and a gated courtyard. Privilege expressed as *finish*, never as ornament. |
| `tenement_courtyard` | N | `kar_071_courtyard_block` | Courtyard Block | K-II | frozen district | Perimeter block around an enclosed yard, entered through a single arched gateway. |
| `abandoned_culdesac` | **X** | → `kar_086_courtyard_housing_group` | — | — | — | The Directorate does not build cul-de-sac suburbia. Substituted. |
| `split_level_house` | **X** | → `kar_087_village_cottage` | — | — | — | Substituted. |
| `trailer_park` | **X** | → `kar_088_construction_camp` | — | — | — | Substituted. |

### 10.9 Utility and infrastructure

| Base master | Cls | Karsic ID | Karsic identity | Strata | Damage | Note |
|---|---|---|---|---|---|---|
| `broken_solar_field` | **F** | `kar_072_imported_solar_array` | Imported Solar Array | K-V | cannibalisation | Foreign equipment, late, small, behind a Directorate fence with an import plate on the gate. Must communicate *why it is here* (contract C6). |
| `city_electrical_substation` | N | `kar_073_district_substation` | District Substation | K-III | cannibalisation | |
| `city_water_treatment_plant` | N | `kar_074_water_treatment_works` | Water Treatment Works | K-II ⊕ K-III | heroic maintenance | |
| `district_heating_station` | N | `kar_075_district_heating_station` | District Heating Station | K-III ⊕ K-I | frozen district | **The signature Karsic building.** Boiler hall, fuel yard, tall stack, and the origin point of the whole heating-main network. Landmark-adjacent; every Karsic district should be within sight of one. |
| `hydroelectric_refuge_dam` | N | `kar_076_hydroelectric_works` | Hydroelectric Works | K-IV | heroic maintenance | Landmark. |
| `pancaked_parking_structure` | A | `kar_077_institute_garage_deck` | Institute Garage Deck | K-III | cannibalisation | The *uncommon* Karsic form; see `kar_089_garage_cooperative` for the common one. |
| `radio_mast` | N | `kar_078_relay_mast` | Relay Mast | K-III | cannibalisation | |
| `shattered_wind_farm` | **F** | `kar_079_imported_wind_array` | Imported Wind Array | K-V | cannibalisation | As `kar_072`. |
| `wasteland_fire_lookout` | A | `kar_080_forestry_watchtower` | Forestry Watchtower | K-II | heroic maintenance | |
| `wasteland_water_tower` | N | `kar_081_steel_water_tower` | Steel Water Tower | K-III | frozen district | Slender column-and-tank tower. **Iconic, cheap, and should be very common** — a top-tier identity-per-block asset. |
| `wilderness_substation` | N | `kar_082_remote_substation` | Remote Substation | K-III | cannibalisation | |

### 10.10 Native additions

These are the structures the base set does not contain but the culture requires. **Without at least the first four, the region reads as a reskin.**

| Karsic ID | Karsic identity | LC target | Strata | Priority | Note |
|---|---|---|---|---|---|
| `kar_083_district_heating_main` | District Heating Main | scattered | K-III | **Mandatory** | An above-ground insulated run on saddles with a road gantry. This is what stitches separate buildings into a *system*, and it is the highest-value single asset in the roster. Must tile: template edges align so consecutive placements read as one continuous main. |
| `kar_084_transformer_kiosk` | Transformer Kiosk | scattered | K-II / K-III | **Mandatory** | A tiny freestanding kiosk, windowless, louvred, fenced 3 clear. Highest-frequency identity carrier in the whole program. |
| `kar_085_bus_shelter_and_stop` | Bus Shelter | scattered | K-III | **Mandatory** | Concrete shelter with a panelled back and a numbered route plate. Extremely cheap, extremely legible. |
| `kar_086_courtyard_housing_group` | Courtyard Housing Group | multibuilding | K-III | **Mandatory** (substitute) | Three slabs around a courtyard with a playground, drying frames, and a boiler stub. Replaces `abandoned_culdesac`. This asset *is* legibility carrier #4. |
| `kar_087_village_cottage` | Village Cottage | building | K-I ⊕ K-II | Mandatory (substitute) | Single storey, stove, veranda, garden. Replaces `split_level_house`. |
| `kar_088_construction_camp` | Construction Camp | multibuilding | K-III ⊕ K-V | Mandatory (substitute) | Cabins on blocks, canteen cabin, generator, drying shed. Replaces `trailer_park`; also carries the "expedition settlement" reading canon asks for. |
| `kar_089_garage_cooperative` | Garage Cooperative | multibuilding | K-III | High | Rows of individual metal garages behind a gate. Very common in reality; excellent as scatter and as courtyard-district edge. |
| `kar_090_kindergarten_block` | Kindergarten (Series) | multibuilding | K-III | High | Low two-storey catalogue building with a fenced play yard. Completes the mikrorayon service set with the school and clinic. |
| `kar_091_technical_institute` | Technical Institute | multibuilding | K-III ⊕ K-IV | Medium | Lecture block, workshop wing, dormitory. |
| `kar_092_memorial_complex` | Memorial Complex | multibuilding | K-IV | Medium | Standalone obelisk, wall of names, eternal-flame plinth on a paved terrace. Civic gravity without national emblems. |
| `kar_093_seed_storage_bunker` | Seed Storage Bunker | multibuilding | K-III | Medium | VCF-linked, hardened, half-buried, cold. Directly serves the EP-7 narrative. |
| `kar_094_tracking_station` | Tracking Station | multibuilding | K-IV ⊕ K-V | Medium | Dish array, hardened telemetry block, isolated logistics apron. Asterion-linked; explicitly requested by canon §Directorate institutional variants. |

### 10.11 Roster accounting

*Counts are extracted from the tables above by `scripts/build_regional_assignment.py` into `structure_library/regional/karsic-assignment.json`. If they disagree, the tables win and this block is regenerated.*

| | Count |
|---|---|
| Base clean masters in `catalog.json` | 85 |
| Converted (N + A + F) | 82 |
| — of which N (native) | 45 |
| — of which A (adapted) | 35 |
| — of which F (foreign) | 2 |
| Excluded (X) | 3 |
| Native additions | 12 |
| **Karsic masters total** | **94** |
| Karsic damage variants (1 per master) | 94 |
| **Catalog entries added** | **188** |

`kar_072` and `kar_079` are the only F-class entries, and both are the same story told twice — imported renewable equipment the Directorate never really adopted. That is deliberate: two sightings make it a pattern, one would read as an accident, and three would dilute it.

---

## 11. Lost Cities integration

### 11.1 File layout

```
structure_library/regional/
    karsic-assignment.json            # P0
    karsic-material-profile.json      # P3
    karsic-massing-grammar.json       # P2 constants: bay=4, storey=6, thicknesses
    karsic-palette-remap.json         # P3 retrofit path only
structure_library/programs/
    kar_<nnn>_<slug>.json             # P1, one per master

kubejs/data/infinite_domain/structure/karsic/
    masters/<slug>_clean_master.nbt   # P2-P7 output, immutable after P7
    <slug>.nbt                        # P8 damage variant

kubejs/data/infinite_domain/lostcities/
    styles/karsic_standard.json
    palettes/karsic_*.json
    citystyles/karsic_*.json
    parts/karsic/...                  # P9, generated
    buildings/karsic/...              # P9, generated
    multibuildings/karsic/...         # P9, generated
    scattered/karsic/...              # P9, generated

kubejs/data/lostcities/lostcities/worldstyles/standard.json   # extended, not replaced

scripts/regional/
    karsic_material_profile.py        # role -> block resolution
    karsic_massing.py                 # P2 primitives layered over structure_geometry_primitives_v2
    karsic_plan.py                    # P5 room modules and circulation
    karsic_dressing.py                # P7 signage, furniture, lighting
    karsic_damage.py                  # P8 archetype operators
scripts/generate_karsic_sites.py      # the driver, mirroring generate_wasteland_sites.py
scripts/validate_regional_structures.py
scripts/validate_material_profile.py
scripts/remap_lostcities_palette.py
```

**Nothing under `converted/` is modified.** Karsic assets live in their own sibling trees so the existing 14,585-file corpus stays byte-stable and diffable.

### 11.2 Style and palettes

Verified from `mods/lostcities-1.21-8.4.1.jar`: a Lost Cities **style** is a list of palette *slots*, each a weighted choice among palettes; a **palette** maps a character to a block, optionally with `damaged` and `variant`. `citystyle.style` selects the style.

`infinite_domain:karsic_standard` takes five slots, mirroring `lostcities:standard`:

| Slot | Purpose | Palettes |
|---|---|---|
| 0 | common | `karsic_common` — filler `#`, rubble `}`, ironbars, glowstone |
| 1 | default | `karsic_default` — street, border, wall, streetbase, streetvariant |
| 2 | wall family | `karsic_concrete_series`, `karsic_concrete_monumental`, `karsic_foundry_brick`, `karsic_first_standard` — the four wall families, weighted 6 / 1 / 2 / 2 so K-III dominates |
| 3 | glazing | `karsic_glass_gray`, `karsic_glass_white`, `karsic_glass_industrial` |
| 4 | glazing side-variant | `karsic_glass_side_concrete`, `karsic_glass_side_panel` |

**Critical limitation, stated once so it is not rediscovered later.** Converted parts carry a **local palette** (`palette.palette` in each part JSON), and a local palette overrides the style. So the style/palette layer above governs *Lost-Cities-generated fabric* — streets, borders, filler, rubble, corridors, parks, rails, the between-building world — and **not** the interiors of converted buildings. Building fabric comes from P3, at the NBT level. Both layers are required; neither substitutes for the other.

The weighting in slot 2 is where the "the standard is the statement" thesis becomes mechanical: K-III wins six times out of eleven, so the between-building fabric of a Karsic city is monotonous **on purpose**, and the K-I/K-II sightings read as survivals.

### 11.3 Citystyles

Eight Karsic district archetypes, each inheriting a shared `infinite_domain:karsic` base (which itself inherits `lostcities:citystyle_common`), following the existing `wasteland_*` pattern exactly.

| Citystyle | District | Draws from |
|---|---|---|
| `karsic_mikrorayon` | Residential superblock | `kar_067`, `kar_071`, `kar_086`, `kar_089`, `kar_090`, `kar_010`, `kar_021`, `kar_075`, `kar_084` |
| `karsic_administrative_core` | Civic and institutional | `kar_011`, `kar_012`, `kar_006`, `kar_064`, `kar_092`, `kar_018`, `kar_023`, `kar_025` |
| `karsic_industrial_combine` | Heavy industry | `kar_049`, `kar_046`, `kar_044`, `kar_055`, `kar_054`, `kar_053`, `kar_050`, `kar_073` |
| `karsic_rail_settlement` | Rail town | `kar_066`, `kar_004`, `kar_044`, `kar_035`, `kar_069`, `kar_081`, `kar_083` |
| `karsic_utility_compound` | Energy and utilities | `kar_075`, `kar_074`, `kar_073`, `kar_082`, `kar_081`, `kar_078`, `kar_083`, `kar_084` |
| `karsic_highway_service` | Roadside | `kar_017`, `kar_033`, `kar_026`, `kar_037`, `kar_022`, `kar_059`, `kar_085` |
| `karsic_rural_settlement` | Village and state farm | `kar_002`, `kar_003`, `kar_068`, `kar_087`, `kar_016`, `kar_009`, `kar_005` |
| `karsic_garrison` | Military | `kar_061`, `kar_058`, `kar_059`, `kar_060`, `kar_007`, `kar_063` |

`structure_library/settlement-archetypes.json` gains eight matching archetype records so `scripts/validate_settlement_archetypes.py` can compile the selectors from evidence rather than by hand.

### 11.4 Settings that carry the culture

These are not cosmetic knobs; each encodes a stated rule.

| Setting | Karsic value | Encodes |
|---|---|---|
| `streetblocks.width` | **10** (vs. 8 in `wasteland`) | Boulevard scale. Directorate roads are oversized for their traffic. **Runtime-unverified — check in-world before locking.** |
| `buildingsettings.mincellars` | **1** | §7.3 rule 1 — every heated building has a basement service level. Setting this at citystyle level enforces the doctrine mechanically instead of relying on per-asset discipline. |
| `buildingsettings.maxcellars` | 2 | Pipe gallery + store. |
| `buildingsettings.minfloors` / `maxfloors` | **3 / 9** for `karsic_mikrorayon` | Exploits the repeatable 6-block storey (§6.1) so one authored panel block yields a whole range of block heights. |
| `buildingsettings.buildingchance` | **0.40** (vs. 0.22) | Karsic districts are dense in building and sparse in variety. |
| `explosionchance` | **0.02** | Low. The Karsic story is systems failing, not buildings exploding. Firebreak damage is authored per-asset in P8, not sprinkled by the generator. |
| `parkblocks.parkchance` | moderate, `avoidfoliage: false` | Courtyards are semi-public green, not manicured parks. |
| `multisettings.correctstylefactor` | **0.95** (vs. 0.9) | Stronger style coherence — the Directorate does not mix. |
| `settings.railwayavoidance` | `ignore` | Rail runs through, not around. |

### 11.5 Worldstyle wiring

`CityStyleSelector` in the Lost Cities jar carries an optional **`biomes`** field of type `BiomeMatcher` (`if_all` / `if_any` / `excluding`). That is the whole mechanism — no mod change, no mixin, no fork.

Extend the existing `kubejs/data/lostcities/lostcities/worldstyles/standard.json` `citystyles` array (do **not** create a second worldstyle; the profile selects exactly one):

```json
{ "factor": 1.0, "citystyle": "infinite_domain:karsic_mikrorayon",
  "biomes": { "if_any": ["#infinite_domain:karsic_region_biomes"] } },
{ "factor": 1.0, "citystyle": "infinite_domain:karsic_administrative_core",
  "biomes": { "if_any": ["#infinite_domain:karsic_region_biomes"] } }
```

…and add `"excluding": ["#infinite_domain:karsic_region_biomes", "#infinite_domain:pelagos_region_biomes"]` to each of the seven existing `wasteland_*` selectors, so central-continent styles stop appearing inside either regional territory. **That edit is the single point where the two regional programs touch the same file**; sequence it so one program lands it and the other only adds its own selectors.

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
| East/West sign | `x*0.002 + vegetation_noise*0.35`, clamped to -1..1 | `east_west_gradient`; **East is +X** |

Two consequences worth stating plainly:

1. **The world is a compass rose.** A central disc, a mountain annulus, two land lobes east and west, two ocean corridors north and south. The Karsic surface region is the eastern lobe.
2. **The diagonals are already neutral.** Where `abs(x)` approaches `abs(z)`, `east_west_ocean_corridor_mask` falls to zero and the culture gradient returns to the seam value. The four diagonal quadrant boundaries are therefore *naturally* soft transition zones — exactly what contract C6 and canon's "not so absolute that every border becomes mechanically perfect" ask for. **No extra work is required to create the transition areas; they already exist.**

### 12.2 The gap, and the one worldgen change required

`kubejs/data/wastelands/worldgen/world_preset/wasteland.json` routes the **ocean** bands by humidity — West `[-1.0, -0.2]`, seam `[-0.2, 0.2]`, East `[0.2, 1.0]` — which is how the abyssal program achieves its East/West split. The **land** rules at the end of the rule list carry **no humidity gate at all**:

```
wastelands:mountains    erosion [-1.0, -0.55]
wastelands:city         erosion [-0.55, -0.15]
wastelands:forest       erosion [-0.15,  0.20]
wastelands:city         erosion [ 0.20,  0.50]
wastelands:apocalypse   erosion [ 0.50,  1.00]
```

So today, East and West land are identical. That is the gap this program has to close.

**The naive fix does not work.** Gating new land rules on `humidity [0.2, 1.0]` also captures the eastern half of the *central continent*: at `x = 2000, z = 0`, `east_west_continent_mask = 1.0`, `east_west_ocean_corridor_mask` is about `0.99`, and `east_west_gradient` saturates at `1.0`, so `city_humidity` lands near `0.99` — squarely inside the East band. Half the central continent would become Karsic.

**Recommended fix: one new density function, one edited reference.**

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
- Outside `r >= 4800`, `central_continent_mask` is 0, the multiplier is 1, and the function is **identical to today**. The entire implemented abyssal program is unaffected — that property is what makes this change acceptable at this stage of the project.
- `start_city_mask` (forcing 2.0) and `mountain_ring_mask` (forcing 1.25) are lerped in *after* this term, so the safe zone, `wastelands:city`, and `wastelands:mountains` routing are untouched.

This needs a companion assertion in the existing abyssal deformation-integrity validator: `regional_culture_gradient` must be referenced by `city_humidity` and by nothing else.

### 12.3 Karsic land biomes

Five biomes mirroring the existing temperate land erosion bands, gated on `humidity [0.2, 1.0]` and `continentalness [-0.19, 1.2]`, inserted **before** the ungated temperate rules and **after** the `safe_zone` / `city` / `mountains` rules:

| Biome | Erosion band | Mirrors | Role |
|---|---|---|---|
| `infinite_domain:karsic_uplands` | `[-1.0, -0.55]` | `wastelands:mountains` | Mining and garrison country. |
| `infinite_domain:karsic_district` | `[-0.55, -0.15]` | `wastelands:city` | **Primary settlement biome.** |
| `infinite_domain:karsic_taiga_margin` | `[-0.15, 0.20]` | `wastelands:forest` | Timber combines, cordons, dachas. |
| `infinite_domain:karsic_industrial_belt` | `[0.20, 0.50]` | `wastelands:city` | **Secondary settlement biome**, industry-weighted. |
| `infinite_domain:karsic_steppe_waste` | `[0.50, 1.00]` | `wastelands:apocalypse` | Open, exposed, sparse. Rail lines and relay masts. |

Tags:

- `#infinite_domain:karsic_region_biomes` — all five. Used by the Lost Cities `BiomeMatcher` (§11.5) and by every Karsic structure set.
- `#infinite_domain:karsic_settlement_biomes` — `karsic_district` + `karsic_industrial_belt`.
- `#infinite_domain:karsic_rural_biomes` — `karsic_taiga_margin` + `karsic_steppe_waste`.
- `#infinite_domain:karsic_upland_biomes` — `karsic_uplands`.

`citybiomemultipliers` in the worldstyle gains `karsic_district` at **1.35** and `karsic_industrial_belt` at **1.2**, matching how `wastelands:city` is already boosted.

Biome definitions themselves should be authored as near-clones of their `wastelands:` counterparts, differing only in surface/vegetation tuning and in their `features` / `spawners` lists. **Do not invent new terrain behaviour here.** The point of the Karsic region is architecture, not a new biome ecology, and inventing one would put this program in conflict with `docs/NORTHERN_BIOME_RESTORATION.md` and with the Wastelands mod's own routing.

### 12.4 Scattered and standalone placement

The three mandatory native infrastructure assets — `kar_083` heating main, `kar_084` transformer kiosk, `kar_085` bus shelter — are what make a Karsic region feel inhabited *between* the Lost Cities blocks. They are placed twice:

1. **Lost Cities `scattered`**, via the worldstyle `scattered.list`, so they appear inside and around generated districts. Requires `scattered/karsic/*.json` wrappers.
2. **Worldgen structure sets**, for the open country between districts, using `random_spread` with salts from the reserved Karsic range **79100000–79109999** and `#infinite_domain:karsic_region_biomes` as the biome filter.

Any Karsic asset placed through a worldgen structure set rather than through Lost Cities must **also** be added to `avoidStructures` in `defaultconfigs/lostcities-server.toml`, exactly as the 64 `ows_*` structures already are, or Lost Cities will generate a district on top of it.

`kar_083_district_heating_main` carries an extra requirement: its template edges must align so that consecutive placements read as one continuous main rather than as disconnected fragments. Treat it as a tiling asset, and validate tiling explicitly (§13.4).

### 12.5 Cross-regional appearances

Per contract C6, a small number of Karsic structures may appear in the western lobe and in the central continent's transition band. The permitted list is short, and each entry must explain itself in-world:

| Structure | Where | Why it is there |
|---|---|---|
| `kar_030_supply_point` | Central transition band | A Directorate trade mission — fenced, self-contained, with import documentation. |
| `kar_078_relay_mast` | Western lobe, very rare | A listening installation on foreign ground. Must read as *placed*, not settled: no housing, no heating main, high fence. |
| `kar_063_civil_defence_stores_cache` | Central transition band | Pre-positioned stores from a joint containment agreement. |
| `kar_032_evacuation_convoy` | Central transition band | A convoy that got that far and no further. |

Four entries, all deliberately legible as foreign. Anything beyond this list weakens regional readability and is prohibited.

---

## 13. Validation

### 13.1 Existing validators, applied unchanged

Karsic assets get **no relaxation**. These run exactly as they do for central-continent assets:

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

Production admission is recorded only in `structure_library/production-approvals.json`, whose `required_checks` list applies to Karsic unchanged.

### 13.2 New validators required

| Script | Checks |
|---|---|
| `scripts/validate_material_profile.py` | Every role resolves for every stratum in use; every block string, derivatives included, exists in `docs/registry-inventory/block-ids.txt`. Runs **before** P3. |
| `scripts/validate_regional_assignment.py` | Every base master has exactly one conversion class; every `X` names a substitute that exists; no orphan substitutes; roster counts match §10.11. |
| `scripts/validate_regional_structures.py` | The Karsic-specific geometry checks in §13.4. |

### 13.3 Gate sequence per structure

```
P1 program schema valid
  -> P2 massing     -> footprint drift within +/-20%, or a recorded exception
  -> P3 fabric      -> material profile validation passes
  -> P4 envelope    -> lint check 3 clean
  -> P5 plan        -> lint checks 1-2 clean; check 6 ledger diffs clean
  -> P6 site        -> lint check 5 clean
  -> P7 dressing    -> signage grammar clean; sign backing clean
  -> P8 collapse    -> lint check 4 recorded; damage constraints honoured
  -> P9 assembly    -> conversion, archetype and provenance validators clean
  -> production approval
```

Per the usage-conserving policy in `CODEX_STRUCTURE_PIPELINE.md`, per-structure checks run per structure; the **expensive global gates** — full corpus, provenance, all-render, QA world, performance budget — run only at the wave boundaries in §14.

### 13.4 Karsic-specific checks

These enforce *this document* rather than general doctrine. All belong in `validate_regional_structures.py`.

| ID | Check | Rule enforced |
|---|---|---|
| **KV-1** | **Repeatable-storey identity.** For every master with `repeatable_storey: true`, storey bands 2..N are silhouette-identical: same wall plane, same opening positions, same joint columns. | §6.1. Without this the `minfloors`/`maxfloors` range in §11.4 produces visibly broken buildings. |
| **KV-2** | **Panel joint continuity.** On K-III elevations, `panel_joint` columns occur at every 4th column with no gaps and no drift, across the whole façade and across converted chunk-cell seams. | §6.1; legibility carrier #1. |
| **KV-3** | **Plinth offset.** Every K-II/K-III/K-IV master over one storey has a ground storey in `plinth` material projecting exactly 1 block on all elevations. | §6.3; legibility carrier #9. |
| **KV-4** | **Vestibule presence.** Every heated master has at least one double vestibule: outer leaf, inner leaf, unheated lobby between, canopy over. | §6.3; legibility carrier #5. |
| **KV-5** | **Basement service level.** Every master declaring `heating_main_connection` has a reachable basement containing a pipe gallery that connects to an exterior stub at the template edge. | §7.3 rule 1. |
| **KV-6** | **Changing/wash block.** Every industrial-category master has a changing and wash block adjacent to a workers' entrance. | §7.3 rule 2; canon. |
| **KV-7** | **Control-room overlook.** Every process master has a control room glazed onto the volume it controls. | §7.3 rule 3. |
| **KV-8** | **Signage grammar.** Every sign string matches §9.1 and names a thing that exists in that structure. | §9.2 rule 6. |
| **KV-9** | **Stratum pairing.** Declared secondary strata are adjacent in the §4.4 table, except at most **four** masters using the K-I ⊕ K-V pair. | §4.4. |
| **KV-10** | **Heating-main tiling.** `kar_083` template edges align so consecutive placements form a continuous run. | §12.4. |
| **KV-11** | **Prohibited-motif scan.** No national emblem shapes; no glyph-art signage. | §4.2. Partly automatable via block-pattern signatures; the remainder is a review item. |
| **KV-12** | **Roof discipline.** No pitched roof on any K-III/K-IV master. Pitched roofs only on K-I/K-II, only in `quark:gray_shingles`. | §8.5. |

---

## 14. Work order

Structured as families and waves, matching the model already used by `structure_library/rebuild-family-roadmap.json` and the usage-conserving policy in `CODEX_STRUCTURE_PIPELINE.md`. **Every family member is completed and locally validated before the family is batched; global gates run only at wave boundaries.** Each family and each wave is an independently resumable stop point.

### 14.1 Families

| Family | Members | Count | Shared systems built here |
|---|---|---|---|
| **KF1 — Panel Series** | `kar_010`, `kar_021`, `kar_024`, `kar_067`, `kar_069`, `kar_071`, `kar_086`, `kar_090` | 8 | Panel façade system, repeatable 6-block storey, double vestibule, stair tower, courtyard kit, plinth ring. |
| **KF2 — Standard Site Kit** | `kar_031`, `kar_038`, `kar_045`, `kar_057`, `kar_078`, `kar_081`, `kar_083`, `kar_084`, `kar_085`, `kar_089` | 10 | Kiosk shell, fence/post/gate system, lamp and bollard set, pipe-saddle run and road gantry, vehicle chassis modules. |
| **KF3 — Monumental Civic** | `kar_006`, `kar_011`, `kar_012`, `kar_018`, `kar_064`, `kar_070`, `kar_091`, `kar_092` | 8 | Pilaster order, ceremonial stair, forecourt, entablature band, deep reveal, below-grade back-of-house. |
| **KF4 — Combine and Works** | `kar_039`, `kar_040`, `kar_042`, `kar_043`, `kar_044`, `kar_046`, `kar_047`, `kar_048`, `kar_049`, `kar_050`, `kar_052`, `kar_053`, `kar_054`, `kar_055`, `kar_056` | 15 | Clear-span hall, crane rail, clerestory band, changing/wash block, control-room overlook, stack family, rail apron and gantry. |
| **KF5 — Utility and Energy** | `kar_051`, `kar_072`, `kar_073`, `kar_074`, `kar_075`, `kar_076`, `kar_077`, `kar_079`, `kar_082` | 9 | Plant hall, switchyard, boiler set, bunded tank, heating-main origin, hardened control. |
| **KF6 — Rail and Transit** | `kar_004`, `kar_034`, `kar_035`, `kar_036`, `kar_062`, `kar_065`, `kar_066` | 7 | Platform, cantilever canopy, siding and hump geometry, ticket hall, conveyor gallery. |
| **KF7 — Rural and Margin** | `kar_001`, `kar_002`, `kar_003`, `kar_005`, `kar_009`, `kar_016`, `kar_068`, `kar_080`, `kar_087`, `kar_088`, `kar_093` | 11 | Barn and shed modules, stove-house module, garden/plot kit, cordon kit, glasshouse range. |
| **KF8 — Garrison and Restricted** | `kar_007`, `kar_032`, `kar_058`, `kar_059`, `kar_060`, `kar_061`, `kar_063`, `kar_094` | 8 | Blast door, filter plant, hardened envelope, perimeter and guard block, decontamination suite. |
| **KF9 — Commerce, Service and Care** | `kar_008`, `kar_013`, `kar_014`, `kar_015`, `kar_017`, `kar_019`, `kar_022`, `kar_023`, `kar_025`, `kar_026`, `kar_027`, `kar_030`, `kar_033`, `kar_037`, `kar_041` | 15 | Ground-floor retail glazing, heated linking gallery, ward and consulting modules, canteen module, forecourt canopy. |
| **KF10 — Set Pieces** | `kar_020`, `kar_028`, `kar_029` | 3 | Boulevard and square geometry, embankment retaining wall, toppled-mass operator. |
| | **Total** | **94** | |

### 14.2 Waves

| Wave | Families | Why this order |
|---|---|---|
| **K-A — Foundation** | KF1, KF2 | These build every shared system the rest of the program reuses: panel façade, repeatable storey, vestibule, stair tower, and the whole standard site kit. **Nothing else should start until K-A is done**, or those systems get invented three times and diverge. K-A also delivers the highest identity-per-block assets in the roster, so the region becomes recognisable at the earliest possible point. |
| **K-B — The working region** | KF4, KF5, KF6 | Industry, utilities, and rail are the Directorate's actual substance and the largest block of work. Second, so the heating-main network, rail spine, and stack silhouettes exist before inhabited fabric is placed around them. |
| **K-C — The inhabited region** | KF3, KF7, KF9 | Civic, rural, commerce, care. These read best when the infrastructure they depend on is already there. |
| **K-D — Restricted and set pieces** | KF8, KF10 | Most narrative-dependent; benefits from the rest of the region existing. |

At each wave boundary, and only there: full corpus validation, provenance, complete Lost Cities conversion, render batch, QA-world rebuild, and the performance-budget check.

### 14.3 Prerequisites, before any geometry

1. **Decide the hemisphere binding** (§2). The only genuinely blocking decision in this document.
2. Add the three Karsic ground contexts to `_GROUND_PALETTES` in `scripts/structure_geometry_primitives_v2.py` (§5.4).
3. Author and validate `karsic-material-profile.json`, including every slab/stair/wall derivative (§8.4).
4. Author `karsic-assignment.json` from §10 and validate it.
5. Land the `regional_culture_gradient` worldgen change and its validator assertion (§12.2) **before** any Karsic biome or structure set exists, so the region has somewhere to be.
6. Author the five Karsic biomes and their tags (§12.3).
7. Write `scripts/validate_regional_structures.py` with KV-1..KV-12 **before** KF1 geometry, not after.

Item 7 is the lesson of `STRUCTURE_REBUILD_SYSTEM_V2.md` §6: 84 assets were built against primitives that were defective by construction, and every completion claim had to be reset to zero. The cost of writing the checks first is a few hours. The cost of writing them last was the entire previous corpus.

---

## 15. Risks and open decisions

| # | Item | Status | Notes |
|---|---|---|---|
| 1 | **Hemisphere binding** | **Blocking** | §2. Pack canon and all live data say Karsic = East; the planning request said the opposite. Decide before anything else. Reversing later drags the entire implemented abyssal program with it. |
| 2 | **Scope against the existing backlog** | **Open** | `rebuild-family-roadmap.json` currently reports `remaining_assets: 57` and `production_approvals: 0`, with all v1 progress reset. Karsic adds 94 masters and 188 catalog entries on top of that. Decide explicitly whether Karsic runs *after* the central rebuild, *in parallel*, or *instead of* finishing it. This document does not assume an answer. |
| 3 | **`FLOOR_HEIGHT = 6` dependency** | **Accepted risk** | The repeatable-storey feature (§6.1) is built on a constant hard-coded in `convert_nbt_to_lostcities.py`. If it ever changes, every Karsic residential asset breaks. Add a guard assertion in `generate_karsic_sites.py` that reads the constant and fails loudly if it is not 6. |
| 4 | **Street width 10** | **Unverified** | §11.4. Chosen for boulevard scale but never measured in-world. Verify before locking; Lost Cities street width interacts with lot fitting. |
| 5 | **Fresh-world validation availability** | **Known constraint** | `docs/ABYSSAL_OCEAN_PROGRAM.md` records that fresh-world validation was unavailable on 2026-08-22 and work proceeded under a waiver. The `city_humidity` change in §12.2 is a real terrain-routing mutation and **should not** inherit that waiver silently. If validation is still unavailable, say so explicitly in the implementation record rather than assuming it passed. |
| 6 | **Biome count** | **Open** | Karsic adds 5 land biomes; Pelagos adds 5 more. Check the total against `docs/biome-gating-audit` and any mod-side limits before authoring. |
| 7 | **Performance budget** | **Open** | 94 additional masters against `docs/structure-performance-budget.json`. The panel-block family is cheap per block but very common; the landmark set is expensive and rare. Measure at wave boundaries, not at the end. |
| 8 | **Two material layers, not one** | **Documented** | §11.2. Lost Cities styles/palettes govern between-building fabric; converted parts carry local palettes that override them. Anyone who assumes one job covers both will produce a half-converted region. |
| 9 | **Mob and spawn profile** | **Out of scope** | Whether the Directorate gets its own hostile/ambient profile is a separate decision, owned by the spawn documents, not by this one. Flagged so it is not silently assumed. |
| 10 | **Quest integration** | **Out of scope, but expected** | Canon §Exploration and quest integration asks for regional discovery objectives. Those belong in the quest documents once the roster is real. |
| 11 | **F-class dilution** | **Controlled** | Only `kar_072` and `kar_079` are foreign-class, telling the same story twice — imported renewable equipment the Directorate never really adopted. Two sightings make a pattern; one reads as an accident; three dilute the region. Resist adding more. |
| 12 | **Palette-remap shortcut** | **Controlled** | §8.4.1. The remap path is fast and tempting and, used alone, violates contract C3. Assets that take it must be marked `fabric_only: true` and are barred from production approval until they have had a full P2–P8 run. |

---

## 16. Change log

| Date | Change |
|---|---|
| 2026-08-26 | Document created. Planning only; nothing implemented. Roster fixed at 94 masters (82 conversions, 3 exclusions with substitutes, 12 native additions). Hemisphere binding recorded as Karsic = East per pack canon, with the conflicting planning-request wording and a reversal procedure both documented in §2. |
