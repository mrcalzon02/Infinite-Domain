# Wasteland Structure — Detailed Rebuild Audit

Status: **active, in progress**. This is the per-building execution record for the
Stage A.5 clean-master rebuild required by
`structure_library/STRUCTURE_REBUILD_SYSTEM_V2.md`. It does not restate the v2
doctrine; it applies it one building at a time and records what was found and
what was changed.

## 1. Authority and precedence

| Rank | Document | Governs |
|---|---|---|
| 1 | `structure_library/STRUCTURE_REBUILD_SYSTEM_V2.md` | design doctrine, the mechanical QA gate, the v2 primitives, disposition of the existing corpus |
| 2 | `CODEX_STRUCTURE_PIPELINE.md` Stage A.5 | the family-by-family regeneration order and checkpoint waves |
| 3 | **this document** | the per-building audit method, the defect taxonomy below, and the ledger in §6 |
| 4 | `structure_library/programs/<id>.json` | the declared room / circulation / damage program each rebuild must satisfy |

Where this document and a higher row disagree, the higher row wins. This
document never relaxes the v2 gate; it only adds detail and a running record.

## 2. Honest status line

- The mechanical gate `scripts/structure_geometry_lint.py` (checks 1–3) is wired
  into `scripts/generate_wasteland_sites.py::generate()` and is the production
  admission bar. As of the last full audit run, **29 / 84** wasteland structures
  pass it; **55** still have hard-fail geometry.
- The v2 replacement primitives in `scripts/structure_geometry_primitives_v2.py`
  are **not yet wired corpus-wide**. They are being introduced one building at a
  time as each building is rebuilt under this audit.
- `scripts/audit_wasteland_structure.py` (added with this document) is the
  per-building deep-audit driver. It runs the lint against clean master **and**
  variant, wires the master↔variant damage-coherence comparison, and adds the
  three detectors in §4.B–D. Its per-building reports live in
  `docs/wasteland-rebuild-audit/<id>.json`.
- No structure is marked done here on a green exit code alone (project standing
  rule). "Done" requires: zero lint hard-fail on master and variant, zero
  `terrain_mismatch_damage` and zero `slab_wall_penetration` audit flags, the
  `structure_library/programs/<id>.json` program still satisfied, and the
  rebuilt `.nbt` regenerated and re-audited from disk.

## 3. Rebase rule

Audit and rebuild the **clean master** (`.../structure/wasteland/masters/<id>_clean_master.nbt`,
built by `<id>_clean_master()` in the generator). If no clean master exists for a
structure, the **damage variant is the rebase source** — audit it in the
master's place, author a clean master from it, then re-derive the variant.
(Owner instruction, 2026‑08‑26.)

## 4. Defect taxonomy

### 4.A Mechanical hard-fail (from `structure_geometry_lint.py`, checks 1–3)

Non-negotiable. Any hit blocks production.

- **structural_connectivity** — a solid block not reachable through solid
  6-connected geometry from the template's ground course. Catches floating
  floors, floating roofs, unsupported catwalks, and fragments a damage pass
  orphaned.
- **stair_enclosure / stair_landing** — a stair run with no lateral wall on
  either side, or that does not terminate on a real walkable floor.
- **ladder_backing / sign_backing** — a ladder or wall sign with no solid block
  behind its attachment face.
- **opening_wall_coupling** — glass or a door with no wall material framing it;
  a "floating window".

### 4.B Massing monotony  *(audit detector: `massing_monotony`)*

The building still reads as a **flat unarticulated cuboid**: one flat roof
plane, and 3+ facades that are ≥ 88 % a single wall plane — no setback, no
projecting bay, no pitched or stepped roofline, no depth relief. Segmented
per building (not per site) so a perimeter fence does not mask a boxy building
inside it. Review-flag severity; must be resolved before a building is marked
done.

### 4.C Slab / stair intruding into a wall volume  *(audit detector: `slab_wall_penetration`)*

A slab or stair block **fully boxed in by wall material on all six faces** — a
half-block block where a full wall block belongs. This is the v2 doctrine's
"slab roofs intruding into wall volumes, leaving structural gaps": a roof or
shed slab pass drawn straight through a wall that was placed by a different
call, leaving a permanent half-block void / weather gap in the wall. Review-flag
severity; must be resolved.

### 4.D Coherent damage vs. terrain-generation mismatch  *(audit detector: `terrain_mismatch_damage`)*

This is the distinction the owner has called out specifically. It is the
difference between *destruction* and a *procedural artifact that merely
subtracts and backfills*.

**Coherent damage** — reads as *an event happened here*:

- an **irregular fracture boundary** — jagged, not a flat rectangular face on
  every side;
- **debris that obeys gravity** — rubble drapes and slopes *below and outward*
  from the breach, thinning with distance, piling against surviving walls; it
  is not a filled box;
- the breach **exposes interior** — broken floor edges, snapped studs/rebar,
  torn cladding, glass shattered to the sill;
- the structure's **declared routes and rooms survive** per
  `programs/<id>.json` `damage_constraints`.

**Terrain-generation mismatch / procedural artifact** — NOT damage, and flagged:

1. **Clean rectangular excision.** A removed volume that fills ≥ 92 % of its
   bounding box with ≥ 5 of 6 flat axis-aligned faces — an `t.clear()` box, not
   a fracture.
2. **Pile-block cuboid backfill.** A block of added "debris" that is ≥ 75 % one
   pile material (gravel, dirt, coarse_dirt, cobblestone, sand, blackstone,
   scrap…), fills ≥ 70 % of its bounding box, has a flat top (≥ 70 % one Y),
   and sits ≥ 55 % inside the building footprint. *This is the "I removed part
   of the roof and put a pile of gravel in there" pattern — a solid cube of
   terrain material dropped into the structure. It is a terrain-gen mismatch,
   not collapse debris.*
3. **Roof punched then capped.** A roof hole whose columns are filled from above
   by pile-block material — the roof was cut and the void patched with terrain,
   rather than left open with debris fallen to the floor below.
4. **Subtraction-only damage.** Blocks removed vs. the master, zero debris
   added: no rubble, no story.

The v2 replacement is `fracture_breach()` (irregular boundary + gravity-
consistent apron + `retrofit_window_for_breach`), never raw `t.clear()` +
`t.fill(..., "minecraft:gravel")`.

## 5. Per-building procedure

For each building, in the `CODEX_STRUCTURE_PIPELINE.md` Stage A.5 wave order
(or worst-first within a wave):

1. `python scripts/audit_wasteland_structure.py <id>` — capture the baseline
   report to `docs/wasteland-rebuild-audit/<id>.json`.
2. Read `<id>_clean_master()` / `<id>()` in `scripts/generate_wasteland_sites.py`
   and `structure_library/programs/<id>.json`. Write the findings table into §6
   with block coordinates and defect class.
3. Rebuild the clean master: swap the defective shared primitives
   (`shell` flat lids, `window`, `stair_flight`, `cracked_pad`/`roadside_apron`,
   the modulo speckle grounds) for the v2 primitives at those call sites only;
   add the massing articulation and support geometry the findings call for;
   keep the building's identity, silhouette and program.
4. Re-derive the variant with `fracture_breach()` against the
   `damage_constraints` in the program file. No raw box clears, no gravel
   cuboids.
5. Verify in-memory (build the two `Template`s, run the lint + the audit
   detectors) until: 0 lint hard-fail on both, 0 `terrain_mismatch_damage`,
   0 `slab_wall_penetration`, `massing_monotony` clear, `assess_fidelity` green.
6. Emit **only** that building's `.nbt` and `masters/<id>_clean_master.nbt`;
   re-run the audit from disk; paste the after-numbers into §6.
7. Leave commits to a deliberate batch — the working tree currently carries
   unrelated uncommitted generator work (ruined functional blocks, regional
   program, separation tuning). See `.codex/structure_pipeline_state.md`.

## 6. Ledger

Legend: **HF** = lint checks 1–3 hard-fail count (master / variant).
**TMD** = `terrain_mismatch_damage` flags. **SWP** = `slab_wall_penetration`
flags. **MM** = `massing_monotony` flags.

| # | Building | Before (HF m/v · TMD · SWP · MM) | After (HF m/v · TMD · SWP · MM) | Status | Notes |
|---|---|---|---|---|---|
| 1 | `decayed_logging_camp` | 41 / 41 · 2 · 16 · 0 | **0 / 0 · 0 · 0 · 0** | **done, regenerated & re-audited from disk** | Floating sawmill catwalk (40+ blocks), drying-shed slab through the garage wall, 6 gravel-cuboid "piles" + 2 box-cuts in the variant, speckle forest floor — all resolved. 5 residual `room_composition` review_flags = the 3 roof-monitor clerestory voids (a light well is not doored; same false-positive class as the baseline's fuel-tank silos). Massing enrichment (D6) deferred, see below. |

### Building 1 — `decayed_logging_camp`

Site: intact forest logging operation, `Template(61, 23, 55)`. Program:
`structure_library/programs/decayed_logging_camp_clean_master.json`. Generator:
`scripts/generate_wasteland_sites.py::decayed_logging_camp_clean_master()` (≈ line 2605)
and `decayed_logging_camp()` (≈ line 2737).

**Clean-master findings**

| ID | Class (§4) | Location | Description | Root cause |
|---|---|---|---|---|
| D1 | 4.A structural_connectivity | x29–55, y8, z23–25 (deck) + y9 z22 (rail) | The sawmill service catwalk (`minecraft:polished_andesite` deck + `oxidized_copper_grate` rail) is a 27×3 platform floating mid-hall with **no columns** down to the floor. 40 + blocks flagged. The `stair_flight` that should serve it stops at (54,7,22) — one block below and one block short of the deck at (54,8,23). | hand-authored `t.fill` catwalk, no support pass; `stair_flight` primitive does no landing check |
| D2 | 4.C slab_wall_penetration | x35–36, y8, z35–51 | The finished-lumber drying-shed roof slab (`t.fill((25,8,35),(36,8,51),"dark_oak_slab")`) is drawn **straight through the maintenance-garage west wall** (garage `shell` at x35, y2–10). Result: a continuous half-block void in the garage wall for the shed's full 16-block length. | shed roof pass written after, and overlapping, the garage `shell`, with no reconciliation |
| D3 | 4.D §3.5 (ground) | whole 61×55 pad, y0 | Ground is a per-block `(x*23 + z*11) % 19` podzol / coarse_dirt / gravel speckle — an inlined `cracked_pad` clone. Not a forest floor; reads as static. | modulo speckle ground, the v2 doctrine's named anti-pattern |
| D4 | 4.A room_composition (review) | 3 pockets | Three enclosed pockets flagged (sealed or undersized). To be resolved with the plan rework. | `partition_*` layout |
| D5 | 4.A (latent) | dispatch, bunkhouse, catwalk stair | `window()` places glass with no wall check; `stair_flight()` builds no shaft, landing or headroom over the run width. Not all currently hard-failing but all disqualified under v2 §3.2–3.3. | defective shared primitives |
| D6 | 4.B massing (manual) | dispatch, bunkhouse, garage | Each `shell` + `gable_roof_x` box is a plain rectangle with a plain gable and flat facades; only the sawmill hall has silhouette interest (roof monitors — themselves defective, see D1-adjacent). Needs porches/canopies, a loading awning on the sawmill, log-stack lean-tos breaking the wall planes. |

**Variant findings** (`decayed_logging_camp()` vs. the master)

| ID | Class (§4) | Location | Description |
|---|---|---|---|
| V1 | 4.D #1 clean excision | `t.clear((47,7,3),(59,21,17))` — 13×15×15 | A flat-faced rectangular box removed from the east sawmill bay + roof monitor #3. No fracture edge, no exposed structure. |
| V2 | 4.D #1 clean excision | `t.clear((2,6,31),(11,20,44))` — 10×15×14 | Flat-faced rectangular box removed from the SW bunk room. |
| V3 | 4.D #2 pile-cuboid backfill | (49,8,3),(52,11,5),(55,14,2) and (4,34,2),(7,37,4),(9,40,2) | Six solid **gravel cuboids** (3×3×3 / 3×5×3 / 3×2×3 / 2×N×2) filled in as "rubble" — flat tops, 76–100 % box fill, single material, inside the footprint. **The exact pattern the owner named.** Detector caught 2 directly; the rest are below the size floor but are the same construction. |
| V4 | 4.D #4 subtraction-only | breach faces | The removed volumes have no gravity-consistent debris apron adjacent; damage is a cut plus a few interior cubes, not a collapse. |
| V5 | 4.A structural_connectivity | catwalk | D1 float carried through unchanged. |

**Rebuild plan**

- **Ground (D3)** → `ground_plate(..., "forest_camp", patch_size=6)` (new context: podzol / coarse_dirt / dirt_path / gravel in coherent patches) + `terrain_footing` skirt on each building; keep the authored haul-road / loader-loop / branch strips on top.
- **Catwalk (D1, V5)** → carry the deck on real posts: `tfmg:steel_block` / `stripped_dark_oak_log` columns every 4 blocks from the floor at y2 up to the deck at y8, tied into the rear partition wall; replace `stair_flight` with `encased_stairwell` landing flush on the deck; grate rail backed by a solid top rail.
- **Drying-shed slab through garage wall (D2)** → pull the shed footprint clear of the garage (end the shed roof at x34, leave a 1-block gap), or carry the shed on its own posts with its ridge below the garage eave; the garage `shell` wall stays full-height and unbroken.
- **Massing (D6)** → dispatch gains a covered check-in porch on the yard side; bunkhouse gains a mess-deck lean-to; the sawmill hall gains a full-width infeed canopy on the log-deck side and a loading canopy over the east door; garage gains a projecting parts-store bay. Roof monitors rebuilt as properly seated clerestories (walls tied to the hall roof, glazed with `wall_window`, capped with a stair-course ridge, not a floating slab lid).
- **Openings (D5)** → every `window()` → `wall_window(..., wall_block=<the shell's wall>)`.
- **Damage (V1–V4)** → `fracture_breach()` for the east sawmill-bay failure and the SW bunk-room collapse, per the program's `damage_constraints` ("East sorting-bay/roof failure and southwest bunk-room collapse remain separate while the central timber workflow and required routes survive"). Debris = irregular apron of `stripped_*_log` splinters + broken `weathered_cut_copper` roofing + a *thin, sloped* gravel/soil wash below each breach — never a filled cube. Preserve the three production cells, the catwalk, both stair routes, the dispatch office and the garage.

**What changed in the generator** (`scripts/generate_wasteland_sites.py`,
`decayed_logging_camp_clean_master()` / `decayed_logging_camp()`):

- **D3** ground: the `(x*23+z*11)%19` modulo speckle → `v2_ground_plate(..., "forest_camp", patch_size=6)` (new context added to `structure_geometry_primitives_v2.py::_GROUND_PALETTES`: podzol / coarse_dirt / dirt_path / gravel / rooted_dirt in 6-block patches), plus a `v2_terrain_footing` cobblestone footing course + coarse-dirt grade skirt under each of the four buildings. The authored haul-road / loader-loop / branch strips are re-laid on top, unchanged.
- **D1** catwalk: the deck now runs to z26 so its whole south edge is tied into the rear hall wall; four `stripped_dark_oak_log` posts carry it to the floor; the rail sits on the deck; the `stair_flight` → `v2_encased_stairwell(t, 30, 2, 16, 7, "south", …)` whose top landing lands flush on the deck.
- **D2** drying-shed roof slab clamped from x36 → x33; the maintenance-garage west wall (x35) is intact and full height again.
- **monitor-lid**: the flat `dark_oak_slab type=top` lid → a planked deck + a `stripped_dark_oak_log` ridge.
- **D5** openings: the four dispatch/bunkhouse `window()` calls → `v2_wall_window(..., wall_block=<shell wall>)` so glass and jamb/sill are placed by one call.
- **V1–V4** damage: the two `t.clear()` boxes + six `t.fill(…, "minecraft:gravel")` cuboids → two `v2_fracture_breach(…, jaggedness=…, apron_floor_y=2, debris_blocks=(…))` calls — irregular boundary, orphan-shed pass, and mixed timber / roofing / cobble debris drifted onto the mill and bunk floors as a thinning sloped pile.

**v2-primitive improvements made while doing this building** (recorded so the
next building inherits them, per the "update the authority tool, don't fork"
rule):

- `structure_geometry_primitives_v2.py::fracture_breach` gained `apron_floor_y`
  (drift debris onto a real floor for elevated breaches instead of leaving it
  mid-air), `debris_blocks` (varied pile material), and an internal
  `_shed_breach_orphans()` pass that clears any solid cell the breach just
  disconnected from the structure or ground — so a fracture can no longer lint
  as floating blocks.
- `structure_geometry_lint.py::check_damage_coherence` now also scans straight
  down from each removed cell for settled debris before reporting "no rubble" —
  a wall/roof breach leaves its rubble on the floor, not welded to the lip.

**After (verified from disk, `docs/wasteland-rebuild-audit/decayed_logging_camp.json`)**

| | clean master | variant |
|---|---|---|
| lint checks 1–3 hard-fail | **0** (was 41) | **0** (was 41) |
| `terrain_mismatch_damage` | — | **0** (was 2 detected; 6 cuboids total) |
| `slab_wall_penetration` | **0** (was 16) | **0** |
| `massing_monotony` | 0 | 0 |
| `assess_fidelity` | pass | pass |
| residual `room_composition` (review) | 3 (clerestory voids) | 2 |

**Deferred for building 1 (tracked, not done):**

- **D6 massing enrichment.** The four buildings are still plain `shell` +
  `gable_roof_x` boxes (the site as a whole is not flat — 4 structures, gables,
  roof monitors, log decks — and it does not trip `massing_monotony`, but the
  individual buildings would read better with a dispatch check-in porch, a
  bunkhouse mess lean-to, a sawmill infeed canopy and a projecting garage
  parts-bay). Left out of this pass to keep the change verifiable; add on a
  second sweep once the whole family is at zero hard-fail.
- **D4 room composition.** The 3 pre-existing sealed pockets are the roof-monitor
  clerestory voids and are correctly left un-doored.

## 7. Risks and open decisions

| ID | Item | Disposition |
|---|---|---|
| R-A | The working tree carries uncommitted generator work (`RUINED_FUNCTIONAL_BLOCK_REPLACEMENTS`, the regional/Karsic program, `FAMILIES` separation tuning). A full `generate()` run would entangle this audit's diff with all of it and, per `.codex` notes, trips `validate_structure_programs.py` on the hospital. | This audit emits **only the building it is working on** (`<id>.nbt` + `masters/<id>_clean_master.nbt`) via a targeted save, never a full `generate()`. Commits are deferred to the owner / a deliberate batch. |
| R-B | `masters/` NBTs are currently ~180 files stale vs. the pending ruined-functional-block pass. Rebuilt masters emitted here will carry the ruined-block swap (the pending intended behaviour). | Acceptable and correct; noted so the eventual full regen diff is expected, not a surprise. |
| R-C | `massing_monotony` requires per-building segmentation and is conservative (fires on 3 buildings corpus-wide). It can miss a boxy building joined to others above fence height. | Manual massing review (row "4.B (manual)") is done for every building regardless of the detector. |
| R-D | `slab_wall_penetration` fires heavily (≈ 48 buildings) because it is a shared-primitive artifact reproduced across the corpus, exactly as the v2 doctrine predicts. Not a false-positive rate — a real backlog. | Each is fixed at rebuild time; corpus count tracked in §2. |
| R-E | Regional (Karsic/Pelagos) program may eventually supersede some of these 84 structures. | Out of scope here. This audit fixes the live corpus; if a structure is later retired, the fix is not wasted (its master feeds the regional massing grammar). |

## 8. Corpus deep-audit baseline (all 84, last full run)

`terrain_mismatch_damage`: **51 structures / 121 findings**. Worst:
`sunken_city_front` (8), `cratered_downtown_intersection` (6),
`ruined_shopping_mall` (6), `abandoned_oil_field` / `blown_apartment_complex` /
`crashed_cargo_airship` / `ruined_mixed_use_block` / `shattered_luxury_condo` /
`toppled_skyscraper` (4).

`slab_wall_penetration`: **48 structures**, many capped at the 30-report limit —
`blown_apartment_complex`, `bombed_hotel`, `emergency_relief_shelter`,
`municipal_incinerator`, `ruined_city_school`, `ruined_community_center`,
`ruined_department_store`, `ruined_mixed_use_block`, `ruined_office_tower`,
`ruined_ranger_station`, `ruined_roadside_diner`, `ruined_rowhouse_block`,
`ruined_shopping_mall`, `shattered_luxury_condo`, `tenement_courtyard`.

`massing_monotony`: `city_water_treatment_plant`, `excavator_pit`.

Combined worst-first (lint HF + audit flags): `bombed_hotel` (184),
`blown_apartment_complex` (168), `ruined_office_tower` (151),
`ruined_mixed_use_block` (133), `sunken_city_front` (122),
`ruined_shopping_mall` (121), `cratered_downtown_intersection` (119),
`ruined_rowhouse_block` (116), `tenement_courtyard` / `nuclear_research_annex`
(104), `decayed_logging_camp` (102).
