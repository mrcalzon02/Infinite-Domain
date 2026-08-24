# Structure Schematic Rebuild System — Ground-Up Revision (v2)

Status: **authoritative**. This supersedes the architectural-quality guidance in
`structure_library/generated-structure-refinement-policy.json` and the "heavy
rebuild" language in `CODEX_STRUCTURE_PIPELINE.md` Stage B. It does not
replace the corpus/licensing machinery (Phases 10–18, provenance, donor
intake), which stands as written. It replaces how structures are designed,
generated, and mechanically gated before a human ever looks at them.

This document exists because the first real player-scale review of the
"rebuilt" corpus — the review this repository's own blocker
(`.codex/structure_pipeline_blocked.md`) has been waiting on since 2026‑08‑19 —
found the corpus is not what its own status fields claimed. All three review
ledgers in `structure_library/review/*.csv` are still 100% `pending`, yet
`structure_library/rebuild-family-roadmap.json` reports `remaining_assets: 0`
and `rebuilt_candidates: 84`. Those two facts are not in tension by accident:
nothing in the pipeline between "script exited 0" and "candidate_for_in_world_review"
ever looked at the geometry. This document closes that gap.

## 1. What the manual review found

Recorded in the reviewer's own words, organized by defect class:

- **Vertical circulation failure.** Stairs float in open air with no room to
  actually climb them; multi-floor buildings have no enclosed stairwell, only
  a diagonal run of stair blocks in open space.
- **Floating architecture.** Windows hang in open air with no wall around
  them. Floors and roofs float disconnected from their supporting structure.
  Slab roofs intrude into wall volumes, leaving structural gaps instead of a
  weather-tight junction.
- **Incoherent damage.** "Damage" is either a clean rectangular cube of
  missing blocks (no fracture, no rubble, no story), or a random per-block
  deletion that leaves a hazy, grid-like scatter of floating remnants instead
  of a believable collapse.
- **Fake ground.** Lots for buildings that should read as real terrain —
  trading posts, farms, wilderness sites — are surfaced with the same
  asphalt-with-lane-lines-and-gravel roadside pad regardless of context.
- **Undifferentiated mass.** Large volumes of the interior remain solid or
  hollow cuboid with no detailing, no fixtures, and no legible purpose.
- **No terrain accommodation.** Structures meant to sit partially or mostly
  below grade don't seat into the actual terrain height; there's no
  basement/cellar or sewer/utility connection logic, and no believable
  transition zone from surrounding land into the lot (road access or
  otherwise).
- **Purpose not expressed spatially.** Even where a building's name and
  intended use are clear, the interior doesn't read as that use. Floor plans
  don't come from an inferred, believable program — they come from whatever
  the shared box-stamping code produces.

## 2. Root cause, traced to code — this is not a vague quality complaint

Every item above traces to a specific mechanism in
`scripts/generate_wasteland_sites.py`, which is the shared geometry library
every family script (`scripts/habitation_family.py`,
`scripts/urban_commercial_family.py`, `scripts/transit_family.py`,
`scripts/rural_processing_family.py`, `scripts/extraction_family.py`,
`scripts/utility_technology_family.py`) calls into through the `A.*` API
(`configure(api)` at the top of each family module). Because it's shared,
every defect below reproduces across dozens of otherwise-unrelated buildings.

| Reported defect | Root cause |
| --- | --- |
| Floating stairs, no room to function | `stair_flight()` (line ~391) places one stair block per step and clears a 2‑tall headroom column above each tread. It builds no side walls, no shaft, no landing at either end, and never checks that the top step actually reaches a real floor. It is a bare diagonal line of blocks, not a stairwell. |
| Floating windows | `window()` (line ~314) and `framed_window_north()` (line ~345) place glass unconditionally at whatever coordinates the caller computes. Nothing checks a wall exists there. Wall coordinates and window coordinates are computed independently (e.g. `city_floor_plan()` picks window x‑positions from a fixed stride while `ruined_massing()` separately carves random blast bites out of the same wall) — when the two disagree, glass ends up floating where the wall was never rebuilt, or a later damage pass removes the wall out from under an already‑placed window. |
| Slab roofs intruding on walls | `roof()` and `shell()` are called repeatedly at different heights for each wing of a building (see `ruined_massing()`), and nothing reconciles overlaps where one wing's roof plane crosses another wing's wall volume. |
| Damage as a clean missing cube | `ruined_massing()` and the city collapse passes use `t.clear(a, b)` — an axis‑aligned box of air — as the primary destruction operator. There is no fracture boundary, no partial-block transition, no rubble underneath most breaches. |
| Random hazy block-grid damage | `scatter()` (line ~212) drops single blocks at uniformly random `(x, z)` with no support or clustering logic — by construction this produces an evenly speckled, ungrouped scatter rather than a debris field. |
| Fake asphalt-and-gravel ground everywhere | `roadside_apron()` → `cracked_pad()` (lines ~212–223, ~492–504) is called by **every** family's `site()` helper regardless of context. `cracked_pad` picks asphalt/gravel/coarse_dirt per block with `(x*37+z*17) % 19` — a deterministic speckle, not a ground surface, and it is the *only* ground kit that exists. A wilderness ranger station and a highway service plaza get the identical lot. |
| No terrain seating / no basements / no sewer connections | `Template` coordinates are purely local to the structure (`size: (sx, sy, sz)`, floor at a fixed internal `y`). Nothing in the generator references the real world heightmap at placement time, and grep across the generator turns up the word "feathering" only in five code comments describing *intent* — there is no general foundation, grade-transition, or basement/utility operator that any family script actually calls. |
| Undifferentiated solid/hollow cubes | `shell()` produces a hollow box with a floor and roof and nothing else; most callers add only a handful of named fixtures per wing (a bed, a barrel, a desk) against interior volumes that can be hundreds of blocks. There is no rule tying fixture density to floor area. |
| Purpose not expressed in the floor plan | `structure_library/programs/*.json` (26 files — most buildings don't even have one) contain exactly the kind of purpose-driven room/circulation/damage narrative this review is asking for (see `ruined_hospital_clean_master.json`: distinct ambulance/public entrances, named clinical departments, two stair stacks, a gravity-led rubble apron). **No script in the repository reads this directory.** It is disconnected documentation. The geometry is produced by hand-written coordinate arithmetic per building (`generate_wasteland_sites.py`, 7,500+ lines) that has no mechanism to consume or be checked against the declared program. |

The mechanical gate that was supposed to catch this,
`assess_fidelity()` in `generate_wasteland_sites.py` (~line 7191), says so
itself in its own docstring: *"Mechanical lint only; this deliberately makes
no visual-quality claim."* It checks: door halves are paired, glass block
count is ≥ 1 anywhere in the whole structure, "functional fixture" keyword
count is ≥ 2, and the y‑span between any stair/ladder block is ≥ 2 for
multi-story buildings. None of that can detect a floating window, an
unsupported stair, a rectangular damage cube, a speckled parking lot, or an
empty room. A structure can fail every complaint in Section 1 and still pass
`assess_fidelity` cleanly, because the gate was never asked those questions.
That is the actual, mechanical reason 84 assets reached
`candidate_for_in_world_review` status while every human review row was still
`pending`.

## 3. New non-negotiable design doctrine

These rules are binding for every clean master, damage variant, and
occupation variant going forward, and retroactively disqualify any existing
asset that doesn't meet them (Section 6 covers disposition of the existing
84 "rebuilt" assets).

### 3.1 Purpose-first floor planning

A structure's `structure_library/programs/<id>.json` file is no longer
optional documentation — it is a **required generation input**, and every
one of the ~150 corpus entries needs one before its geometry is (re)written,
not after. The program must be authored from: the structure's name, its
inferred real-world purpose, its declared `category`/`settlement_types`/
`road_connection` in `structure-metadata.schema.json`, and reference material
for comparable real buildings. Geometry generation reads the program's
`ground_program`/`upper_program`/`circulation`/`damage_constraints` lists and
must produce a room ledger (Section 4.4) that a validator can diff against
those declared rooms. A building whose interior can't be matched back to its
own declared program fails review regardless of block count or fixture
count.

### 3.2 Vertical circulation

- Every stair run must sit inside an **encased stairwell**: solid walls on
  both lateral sides for the full run, a floor-connected landing at the
  bottom and at the top (not a step that simply stops), and continuous
  headroom over the full width of the run, not just above each tread's
  centerline.
- No stair or ladder may terminate in open air. If it doesn't reach a real,
  walkable floor surface (or the roof, for a roof-access run), it is not
  finished.
- Multi-floor buildings need traversal that reads as **architecture**, not a
  service ladder bolted into a corridor — reserve bare ladders for genuine
  service/emergency shafts, tank access, watchtowers, and similar, per the
  program file's stated circulation.
- Every ladder must have a solid backing block behind its attached face.
  Every wall sign must have a solid backing block behind its attached face
  (standing signs need a solid floor block beneath them). This is a
  Minecraft attachment requirement as much as an aesthetic one — an
  unbacked ladder or sign is not just unsightly, it should not have been
  possible to place.

### 3.3 Openings are wall operations, not independent operations

A window or door is never placed by picking a coordinate and adding glass or
a door block — it is placed by the *same operation* that establishes (or
confirms) the wall segment framing it, so a wall and its opening cannot
disagree about whether the wall exists. If a later damage pass removes a
wall segment that carries a window or door, that pass must also resolve the
opening (convert to broken glass / rubble / open frame), never leave it
floating. Parallel windows on the same façade must land on a consistent wall
plane; if the structural definition of that wall changes (setback, taper,
damage), the window generation must re-derive its position from the current
wall geometry, not from a stale coordinate computed earlier.

### 3.4 Damage is an authored event, not a subtraction

Damage variants must read as *something happened here*, derived from the
program file's `damage_constraints`, not from `t.clear()` on an axis-aligned
box and not from per-block random deletion. Every breach needs: an irregular
fracture boundary (not a flat rectangular face on every side), a
gravity-consistent rubble/debris apron below and around it, and preservation
of the routes and rooms the program explicitly protects (e.g. "preserve both
stair stacks and surviving routes on every floor"). Random independent
per-block deletion (`scatter()`'s current use, and any similar noise-based
technique) is banned as a *primary* destruction method; it may only be used
for small secondary dressing (scorch specks, loose debris) layered on top of
an authored fracture, never as the fracture itself.

### 3.5 Ground is site-specific, not a universal pad

`cracked_pad`/`roadside_apron` stops being the only ground kit in the
codebase. Ground treatment is selected by the structure's actual context —
urban paved lot, rural worked ground (dirt/gravel/crop rows), industrial
hardstanding, wilderness undisturbed ground (leaf litter, exposed rock,
underbrush), waterfront — using the `category`/`settlement_types` fields
already defined in `structure-metadata.schema.json`. Asphalt with painted
lines is a *highway/main_road/local_road* material, and only appears where
`road_connection` actually justifies a paved surface at that lot.

### 3.6 Terrain and foundation accommodation

Every structure gets a real foundation course and a grade-transition skirt
so it doesn't read as a box dropped on the surface. Structures whose program
calls for partial or full below-grade siting (cellars, buried vaults,
subsided fronts, bunkers) get an explicit target depth and a feathering
ramp/retaining treatment into the surrounding grade, not a fixed internal
coordinate that happens to work only when the world's terrain height matches
by coincidence. Where the building category and setting plausibly call for
it, add basement/cellar space and a visible sewer/utility stub connection
(manhole, drain, service trench) rather than a building that simply stops at
its footprint with nothing below or beside it.

### 3.7 Detail density is tied to floor area, not a fixed low count

Replace the current "≥ 2 functional fixtures, anywhere in the whole
building" bar with a per-declared-room minimum: every room/zone named in the
structure's program must contain fixtures that make its purpose legible at
player scale, and no undressed shell volume may exceed a fixed block-count
threshold (Section 4 defines the exact check) without being subdivided,
furnished, or intentionally left as a legible ruin (which must itself show
rubble/debris, not empty air).

### 3.8 Site-to-surroundings transition

The lot's edge is not a hard cliff between "structure" and "world." Add a
believable transition — grading, planting, worn paths, or a road/driveway
tie-in per the structure's declared `road_connection` — and don't force road
access onto sites whose program says otherwise; a wilderness site can
transition via a foot trail instead, but it must transition, not just stop.

## 4. New automated QA gate

`assess_fidelity()` is retired as the production gate. It stays as one input
among several inside a new module, `scripts/structure_geometry_lint.py`
(delivered alongside this document), which actually inspects geometry
instead of counting keywords. It is designed to run both in-process against
a live `Template` during `generate()` and standalone against saved `.nbt`
files (reusing `convert_nbt_to_lostcities.load_structure`, the same loader
`audit_structure_block_fitness.py` already uses), so it can be pointed at
every existing corpus asset immediately.

What it checks, and why each check maps directly to Section 1:

1. **Structural connectivity (floating geometry).** Flood-fills solid,
   non-decorative blocks from every solid block resting on the template's
   base plate (`y == 0`/`y == 1`, matching how `roadside_apron`/`ground_plate`
   always establishes ground level). Any solid block not reachable through
   6‑connected solid neighbors is reported as floating — this single check
   catches floating floors, floating roofs, and any stair/wall fragment left
   disconnected by a damage pass.
2. **Stair/ladder/sign validator.** Groups adjacent same-facing stair blocks
   into runs and checks lateral wall support, headroom, and a landing on a
   real floor at both ends of the run. Checks every ladder and wall sign for
   a solid backing block on the attachment face.
3. **Window/door wall-coupling validator.** For every glass or door block,
   requires solid wall-category blocks framing the opening in-plane (not
   merely touching a floor), and cross-checks against the connectivity scan
   so an opening that reads as floating is flagged even if it technically
   touches something.
4. **Damage-coherence heuristic.** Compares a damage/occupation variant
   against its immutable clean master, flags removed volumes whose boundary
   is a perfect flat-faced rectangular prism with no debris nearby, and
   flags ground-plane regions whose palette alternates with the kind of
   short, regular period a modulo-based speckle produces.
5. **Ground-context validator.** Cross-references the structure's
   `category`/`settlement_types`/`road_connection` (from
   `structure-metadata.schema.json`) against the block palette actually used
   in the lot/apron layer, using an explicit allow-list per context.
6. **Program-conformance ledger.** If `structure_library/programs/<id>.json`
   exists, emits a room ledger from the generated geometry and reports which
   declared rooms have no matching enclosed, fixture-bearing volume.

A structure fails the gate if any check in 1–3 reports a hit; checks 4–6
report as required findings for the human visual review pass but do not
themselves hard-fail generation, since they're heuristic — a human still
makes the final call, matching the existing (correct) principle that
"automatic success never mutates" the approval set. What changes is that the
human reviewer now gets a findings report pointing at specific coordinates
and specific defect classes instead of walking blind.

## 5. New and replacement geometry primitives

Delivered alongside this document as `scripts/structure_geometry_primitives_v2.py`,
written against the exact same `Template` API (`t.set`, `t.fill`, `t.clear`,
`t.state`, `t.size`) already used throughout `generate_wasteland_sites.py`,
so they are drop-in replacements/additions, not a parallel system:

- `encased_stairwell(...)` replaces `stair_flight(...)` — builds the shaft
  walls, base and top landings, and headroom in one call instead of a bare
  stair line.
- `wall_window(...)` replaces `window(...)`/`framed_window_north(...)` —
  places jambs and glass together and refuses to place glass where no wall
  segment is being established in the same call.
- `retrofit_window_for_breach(...)` — must be called by any damage pass that
  clears a wall region, so windows caught in the breach resolve to broken
  glass/rubble instead of floating.
- `ladder_shaft(...)` replaces bare `t.set(..., "minecraft:ladder", ...)`
  calls — guarantees the backing wall exists before the ladder is placed.
- `backed_sign(...)` — same guarantee for signs.
- `ground_plate(...)` replaces `roadside_apron`/`cracked_pad` as the single
  universal lot kit — takes a `site_context` (`urban_paved`, `rural_worked`,
  `industrial_hardstanding`, `wilderness_undisturbed`, `waterfront`) and
  produces a coherent, patch-based surface instead of per-block speckle.
- `terrain_footing(...)` — foundation course, grade-transition skirt, and an
  optional basement cavity/sewer stub, parameterized by a
  `foundation_profile` (`surface`, `raised`, `partial_basement`,
  `full_basement`, `submerged`).
- `fracture_breach(...)` replaces raw `t.clear()` box damage — produces an
  irregular fracture boundary and a gravity-consistent rubble apron, and
  internally calls `retrofit_window_for_breach` so it can never leave a
  floating window behind.

None of these touch third-party mod code or assets; they are additions to
our own generator scripts, consistent with the project's distributability
scope.

## 6. Disposition of the existing 84 "rebuilt" assets

`rebuild-family-roadmap.json` currently reports all seven families complete
and `remaining_assets: 0`. Under the new gate that status is not accurate —
every one of those assets was produced by the primitives in Section 2's
table, so every one of them is expected to fail the new structural-
connectivity and opening-coupling checks by construction. Concretely:

1. Set every family's status in `rebuild-family-roadmap.json` from
   "completed" to `requires_regeneration_v2`; leave `production_approvals`
   at zero (it already is).
2. Do **not** re-derive damage/occupation variants from the current clean
   masters. Re-author each clean master's `structure_library/programs/<id>.json`
   first (Section 3.1) if it doesn't already meet the new bar, then rebuild
   the clean master using the v2 primitives, then re-derive variants from
   the new clean master.
3. Re-run families in the existing checkpoint-wave order (A: roadside
   mobility/security, habitation and community; B: urban commercial,
   transit and ports, rural processing, extraction sites; C: industrial
   utility and technology) — that grouping and its shared-systems reuse
   logic in `rebuild-family-roadmap.json` is sound and should be kept.
4. A structure only re-enters `candidate_for_in_world_review` once it passes
   `structure_geometry_lint.py` checks 1–3 with zero findings **and** an
   actual human has walked it in the QA world and marked the corresponding
   row in `structure_library/review/*.csv` `pass` with a reviewer and
   timestamp — matching the review manifest's own existing (and correct)
   gate schema in `structure_library/production-approvals.json`. A green
   script exit code is still not, and has never been, approval.

## 7. Pipeline instruction update

Append this as a new stage in `CODEX_STRUCTURE_PIPELINE.md`, run after Stage
A and before re-entering Stage B's remaining phases:

```text
# STAGE A.5 — Structural Rebuild System v2 Adoption

Before resuming or re-running any family rebuild:

1. Read structure_library/STRUCTURE_REBUILD_SYSTEM_V2.md in full.
2. Land scripts/structure_geometry_lint.py and
   scripts/structure_geometry_primitives_v2.py; wire the lint module into
   generate_wasteland_sites.py's generate() in place of (not merely beside)
   assess_fidelity(), and wire the v2 primitives in as the only sanctioned
   way to place stairs, ladders, signs, windows, ground plates, foundations,
   and damage breaches.
3. Run scripts/structure_geometry_lint.py in standalone mode against every
   existing corpus .nbt to establish the true baseline defect count. Do not
   trust rebuild-family-roadmap.json's prior "completed" status.
4. Set every family's status to requires_regeneration_v2 per Section 6 of
   the v2 document.
5. For each family, in the existing checkpoint-wave order: ensure every
   member has an authored structure_library/programs/<id>.json; rebuild the
   clean master with the v2 primitives; confirm zero lint findings on
   checks 1-3; re-derive damage/occupation variants with fracture_breach;
   confirm zero lint findings on the derivatives; render and record findings
   from checks 4-6 for human review.
6. Do not mark a family complete on script success alone. A family is
   complete only when every member has zero hard-fail lint findings.
   Production approval still requires the human QA-world walkthrough and
   review-ledger row per Section 6 point 4 - this stage does not shortcut
   that gate, it makes it meaningful.
```

## 8. Scope of this document

This is a specification and a first implementation of its enforcement
tooling (Sections 4–5), not a claim that all ~150 corpus assets have been
rebuilt. Rebuilding the full corpus against this doctrine is exactly the
multi-session, checkpointed work `CODEX_STRUCTURE_PIPELINE.md` already exists
to carry out — this document is what it should be carrying out now. The lint
module has not yet been run against the live corpus in this session; running
it against every `.nbt` under `kubejs/data/infinite_domain/structure/wasteland/`
is the correct first action for whoever executes Stage A.5.
