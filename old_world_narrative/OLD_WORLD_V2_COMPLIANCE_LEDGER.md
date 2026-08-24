# Old World Site Reauthoring — Structure Rebuild System v2 Disposition Ledger

Scope: the ten statically implemented Old World narrative sites.
Gate: `scripts/structure_geometry_lint.py` checks 1–3, run standalone against
the saved `.nbt` corpus and in-process during generation.
Doctrine: `structure_library/STRUCTURE_REBUILD_SYSTEM_V2.md`.

## Disposition: repair in place, do not regenerate

v2 Section 6 tells the pipeline to rebuild the existing 84 "rebuilt" assets
from the v2 primitives rather than patch them. That instruction is right for
the wasteland family clean masters, which were produced end-to-end by the
pre-v2 shared geometry library and carry no authorship worth preserving.

These ten are not those. Each is a reviewed clean master plus a substantial
hand-authored narrative revision layer — VCF / Atlas / PolyCore institutional
identity, re-zoned interiors, purpose-specific machinery, deterministic proof
loot — which `source/02_TRANSITION_FROM_STRUCTURE_REVIEW.md` explicitly
requires be carried forward rather than rebuilt. Measured against the real
lint baseline rather than assumed, their defects were small and localised:
eight of ten sites were within a few dozen findings, and two already passed
untouched.

So the disposition for this wave is the repository's own core architectural
rule — `reuse → repair → refine` — not `discard → regenerate`.

## Baseline, and why the old numbers were wrong

Every site's registry entry previously recorded `structural_lint_passed: true`
from `base.assess_fidelity()`. That function counts door halves, glass blocks
and fixture keywords, and says in its own docstring that it makes no visual
quality claim. All ten sites passed it while carrying the defects below. The
generator now gates on the geometry lint instead; `assess_fidelity` is
retained in each entry as `legacy_assess_fidelity`, as supplementary record
only.

| Site | Before | After | Defects found | Work done |
| --- | ---: | ---: | --- | --- |
| OWS-001 depot | 0 | 0 | — | none; untouched, byte-identical |
| OWS-015 seal-failure station | 0 | 0 | — | none; untouched, byte-identical |
| OWS-010 conveyor hall | 5 | 0 | open stair run, unseated press | retrofit |
| OWS-003 cold-chain nursery | 11 | 0 | two unframed glazed panels | retrofit + authored vault access |
| OWS-006 PT-9 laboratory | 11 | 0 | open stair run, three sealed chambers | retrofit + authored airlocks |
| OWS-002 grow hall | 19 | 0 | 16 unbacked ladders, 2 unframed doors, floating roof hatch | retrofit + authored hatch curb |
| OWS-016 exposure array | 24 | 0 | two open stair runs, unframed doors and glazing | retrofit + authored chamber airlocks |
| OWS-009 repair depot | 63 | 0 | unsupported roofline service blade | retrofit |
| OWS-004 farm tower | 130 | 0 | four open stair stacks, unseated nutrient tanks, 22 unframed doors | retrofit + authored greenhouse access |
| OWS-012 crushing plant | 2731 | 0 | entire site stood at grade with no ground beneath it | authored site grade + process deck |

## What "retrofit" means here

`scripts/old_world_v2_compliance.py` reads the gate's findings and repairs
only the coordinates it named. Operators are additive — they write into empty
cells and never overwrite authored geometry unless explicitly asked — and
idempotent, so a site with no findings is left byte-identical. Measured across
the whole wave after this first pass:

* **0 authored blocks removed.**
* **20 blocks overwritten**, all of them glass converted into door frames and
  door halves where a sealed chamber needed an entrance.
* Two sites untouched entirely.

(The detail-density pass below raised the overwrite count to 63, on the same
terms: still nothing removed, still only glass giving way to doors.)

Casing every stair run in every site would have written roughly 900 blocks
into structures that were already compliant, burying decorative and exterior
stairs that were never defective. That is why repair is finding-driven rather
than blanket.

## Authored decisions, written longhand

Several fixes were design decisions, not mechanical ones, and live as
`_authored_*` functions in `scripts/generate_old_world_narrative_structures.py`
so they can be read and argued with:

**OWS-002 — roof hatch curb.** The escape ladder's trapdoor sat one course
above the copper deck with nothing beside it. A four-block curb ring ties it
back into the deck, which is what a real roof hatch has anyway.

**OWS-006 — chamber airlocks.** The three PT-9 symbiosis chambers were sealed
glass boxes containing soil, cultures and reagent stations: legible from
outside, impossible to enter. The site's own acceptance dimension calls for
the chambers to be *separated*, which means a controlled door, not a wall.
Each now has a framed iron airlock on its corridor face and a threshold step
up to the raised chamber deck.

**OWS-012 — the quarry's missing ground.** This one site accounted for 2,731
of the wave's findings, and not because it was badly built. The template
modelled only what was excavated; the haul road, service house, crushing plant
and timber headframe all stood at natural grade with nothing beneath them.
Three fixes: an industrial-hardstanding working yard laid at grade in coherent
patches (v2 doctrine 3.5 and 3.6, which nothing in this asset previously
satisfied); the process deck carried south so bulk feed, crushing, milling,
mixing and dust extraction stand on one continuous structure, as the site's
acceptance dimension already claimed; and an overhead gantry for the
mechanical mixer, because the mixer must hang above its basin with the span
between them clear — a support column under it would have satisfied the
geometry gate and broken the machine.

## Lint change: explicit grade declarations

`check_structural_connectivity` anchors on a template's lowest solid layer.
For a pit that is the excavated floor, tens of blocks below the grade the
site's buildings stand on, so every at-grade structure reads as floating. The
check's own docstring anticipates this ("unless a caller explicitly knows
better"); `lint_structure` now accepts `ground_y`, and
`structure_library/structure-grade-declarations.json` records the declaration
so the standalone scan reaches the same verdict as the generator.

A declaration names the grade plane. It does not waive the requirement to
build ground there: a structure hovering above its declared plane is reported
exactly as before, and this file must never be used as a suppression list.

## Detail-density pass (v2 doctrine 3.7)

The first pass cleared checks 1–3. A second pass took the check 4–6
advisories, which is where "level of detail and quality compliance" actually
lives. Eight enclosed voids were flagged. Each was examined rather than
auto-filled, because whether a void wants furnishing, subdivision, access or
deliberate ruin is authorship:

| Site | Void | Reading | Action |
| --- | --- | --- | --- |
| OWS-003 | glazed cold vault, 86 floor cells | working room holding the cooler banks and culture crates — visible, unreachable | east-face airlock, on the receiving-to-dispatch axis the site already runs |
| OWS-004 | rooftop greenhouse, 42 floor cells | the tower's crown, named in its own silhouette dimension, sealed shut | south-face door onto the roof deck |
| OWS-006 | roof void, 155 floor cells | not a crawl plenum — a rooftop plant room standing on the deck | dressed as one: duct runs hung from the ceiling slab, air handlers, a door off the roof, a service ladder down into the lab |
| OWS-016 ×4 | exposure chambers, 14 floor cells each | same defect as the PT-9 chambers: sealed cells holding the polymer coupons that are the site's whole evidence | four clean-corridor airlocks |
| OWS-015 | water tower tank, 1,503 air blocks | a sealed tank is what a water tower *is* | verified, left alone |

OWS-006's plant room is the one worth dwelling on. Filling a roof void with
furniture to satisfy a heuristic would be dishonest — but in a building whose
entire purpose is sealed containment chambers, the air handling that keeps
those chambers sealed is arguably the most load-bearing room in it. Dressing
it as plant makes the volume legible *and* tells the site's story.

OWS-015 is the counter-case, and deliberately so. Its finding is still
reported rather than suppressed, so the next reader re-checks the judgement
instead of inheriting a silent exemption. The same principle governs
`structure-grade-declarations.json`: name the thing, never hide it.

After both passes, wave-wide: **0 authored blocks removed**, 63 overwritten —
all glass becoming door frames and door halves, plus one wall block becoming
a ladder. Every site's required narrative blocks and proof chest verified
present.

## What is still open

Passing checks 1–3 is not production approval, and this ledger does not claim
it is. Section 6 point 4 still requires a human QA-world walkthrough and a
`pass` row in `structure_library/review/*.csv` with reviewer and timestamp.

Advisory findings (checks 4–6) deliberately still report, and are recorded per
site under `structural_lint.review_findings`:

* One advisory remains, by decision: OWS-015's water tank (see the
  detail-density table above). Everything else in checks 4–6 is clear.

Also noted, unrelated to this work: OWS-003's base master
(`abandoned_orchard_cannery_clean_master`) drifted upstream by 42 bricks since
the wave was first generated. The regenerated site reflects current upstream.

Runtime validation remains deferred by user: fresh-world placement,
structure-map acquisition, FTB structure-task completion, guaranteed proof
chest acquisition, and multiplayer behaviour are all still unverified.
