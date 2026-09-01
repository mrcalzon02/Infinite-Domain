# Endgame — progress audit

**As of:** 2026-08-31 (module-geometry coverage pass); base roll-up 2026-08-27, 22 `endgame(...)` commits on `main` (5df1ea34 → f15b1701), all
path-scoped; the repository's pre-existing staged work is untouched.

**Authority:** `docs/Endgame.md` §11 ledger is the source of truth for state; this file
is a human-readable roll-up. Where they disagree, the ledger wins.

---

## Headline

| | |
|---|---|
| Formal phase | still **P00** (contracts done, gate under review) |
| What actually exists | a loadable dimension with a **full-height stratified megastructure**, 3 band biomes, a carved circulation network + shafts + a monumental hall, a jigsaw room/corridor/stair district, a reversible entry/return mechanic, an air-hazard + acid prototype, and P02/P04 contracts |
| How | by repeated owner direction the "Phase 1 spike" was built out through Phase 2/3/4 territory ahead of the gates |
| Blocking everything downstream | **P00-GATE** (C0012) and **P01-GATE** (C0024) are `REVIEW_NEEDED` — each needs an independent review the coordinator cannot self-do, plus an in-client runtime run |

## Phase 0 — Program contract and capability audit

| Checkpoint | Status | Evidence |
|---|---|---|
| C0001 source inventory | **COMPLETE** | `docs/Endgame.md` §10 |
| C0002 capability audit | **COMPLETE** | `docs/Endgame.md` §10 (22-row table) |
| C0003 identity contract | **COMPLETE** | `docs/endgame/identity/placeholder-terms.md` |
| C0004 spatial metrics | **COMPLETE** | `docs/endgame/contracts/spatial-metrics.md` |
| C0005 architecture ADR | **COMPLETE** | `docs/endgame/adr/ADR-0001-*.md` |
| C0006 height decision | **COMPLETE** | `docs/endgame/contracts/height-contract.md` |
| C0007 hazard contract | **COMPLETE** | `docs/endgame/contracts/hazard-contract.md` |
| C0008 performance budget | **COMPLETE** | `docs/endgame/contracts/performance-budget.md` |
| C0009 namespace / layout | **COMPLETE** | `docs/endgame/contracts/namespace-layout.md` |
| C0010 test strategy | **COMPLETE** | `docs/endgame/test-strategy.md` |
| C0011 Phase 1 backlog | **COMPLETE** | `docs/endgame/phase-1-backlog.md` |
| **C0012 P00-GATE** | **`REVIEW_NEEDED`** | `docs/endgame/gates/P00-GATE-evidence.md` — mechanical review PASS; needs an **independent integration review** + 4 open items (flavour names, canon hook, arrival anchor, taller-height decision) |

**Verdict:** Phase 0 authoring is done. The gate is a human decision.

## Phase 1 — Minimal technical dimension spike

| Checkpoint | Status | Notes |
|---|---|---|
| C0013 registry skeleton | EVIDENCE_READY | dimension + type, `-64..319`; datapack loaded clean on the owner's 2026-08-27 run |
| C0014 baseline generator | EVIDENCE_READY | now a full density graph (see Phase 3 below) |
| C0015 spike biomes | EVIDENCE_READY | 3 band biomes (sump / works / vault) |
| C0016 3D routing | EVIDENCE_READY | `multi_noise` depth split, 3-way |
| C0017 acid feature | EVIDENCE_READY | bounded static-acid lake in the sump |
| C0018 air-hazard prototype | EVIDENCE_READY | `hive_world_atmosphere_proto.js`; **superseded this phase by the Phase 5 system** |
| C0019 reversible entry | EVIDENCE_READY | operator descent/return marker + lodestone, full recovery; IIFE-fixed after a runtime error |
| C0020 safe arrival | EVIDENCE_READY | carved entry hall + climbable shaft + stub tunnels |
| C0021 client baseline | EVIDENCE_READY (capture pending) | Nether-effects placeholder; owner captures cameras + the pre-Hive perf baseline |
| C0022 smoke validator | EVIDENCE_READY | `validate_hive_world_smoke.py`, 10 assertions, PASS |
| C0023 spike removal test | EVIDENCE_READY (run pending) | `remove_hive_world_spike.py` + path manifest, dry run clean |
| **C0024 P01-GATE** | **`REVIEW_NEEDED`** | `docs/endgame/gates/P01-GATE-evidence.md` — needs the owner's in-client runtime table + an independent review |

**Verdict:** all spike authoring done and mechanically green. Needs the owner's in-client
run (codec load ✓ already; still: generation, `/locate biome`, district assembly
connectivity, round trip, recovery matrix, acid contact, exposure meter) and the two
gate reviews. Nothing here is `COMPLETE` until P00-GATE + P01-GATE pass.

## Phase 2 — Full-height greybox proof

The spike leapfrogged this. Instead of hand-placed greybox slices there is a **generated
full-height megastructure**. The Phase 2 *contract* was written:

| Checkpoint | Status |
|---|---|
| C0025 slice / massing contract | EVIDENCE_READY — `docs/endgame/contracts/massing-contract.md` |
| C0026-C0032 greybox kit + band slices | N/A — replaced by the generator; band identity is delivered by surface-rule palettes plus six core and two exterior biomes |
| C0033 full route | pending in-client — the carved network + shafts + hall exist but continuity is untested |
| C0034 sightline / fog | partial — distinct fallback fog per band exists; in-client visibility and transition tuning remain Phase 5 |
| C0035 greybox performance | pending in-client — the density graph is **untuned**, carve fractions unmeasured |
| **C0036 P02-GATE** | **not started** — needs an independent visual/experiential review of the megastructure in-game; on acceptance it **freezes** the massing per `massing-contract.md` §7 |

**Verdict:** massing exists and has a contract; it is not frozen. P02-GATE is the next
real review milestone.

## Phase 3 — Planetary and hive-mass generator

Spike-scale, by owner direction (`generate_hive_world_density.py`):

| Piece | Status |
|---|---|
| solid engineered mass + sealed roof/floor | DONE (spike) |
| carved circulation network (spaghetti noise) | DONE (spike, untuned) |
| full-height vertical shafts | DONE (spike, noise-placed not deterministic) |
| monumental hall + column lattice | DONE (spike, noise-gated / partial) |
| 6 band palettes (surface rule) | DONE (spike) |
| **stack_core / apron / trunk_axis macro layer** | **NOT STARTED** — needs ADR-0001 layer 2; the spike is single-core with no wastes (C0038-C0040) |
| 3D biome source refinement | EVIDENCE_READY static candidate — Wastes/Apron plus six exact core bands, six matching districts, complete generator ownership, 8/8 routing gate; runtime codec/seam sampling pending (C0046) |
| seed sweep + determinism + generation optimization | NOT STARTED (C0048-C0049) |
| **C0050 P03-GATE** | not started |

**Verdict:** the *within-a-core* mass model is prototyped; the *planetary* layer (multiple
cores, wastes, aligned axes) is entirely future work and is the biggest single gap.

## Phase 4 — Modular architectural grammar

Spike-scale, by owner direction:

| Piece | Status |
|---|---|
| C0051 module schema | EVIDENCE_READY — `docs/endgame/contracts/module-schema.md` |
| C0052 connector validator | EVIDENCE_READY — `validate_hive_world_modules.py`, 10 checks, PASS on **all 37 modules** (7 legacy + 30 band) and 21 pools; negative-tested |
| compatibility jigsaw district (7 modules, 3 pools, structure + loot) | DONE (spike) — definition retained, placement set now inert; `generate_hive_world_structures.py` |
| C0053-C0054 structural + vertical circulation kits | partial — modules reuse a shared palette; `stair_shaft` uses a ladder |
| C0055-C0060 per-band module families | EVIDENCE_READY static candidate — 30 authored NBT modules, 18 generated pools, six generated structures/unique-salt sets; **geometry now schema-validated (2026-08-31)**; assembly/runtime review pending |
| C0061 apron / wasteland kit | NOT STARTED (needs the macro layer) |
| C0062 axis placement system | NOT STARTED |
| C0063 damage-state system | partial — inherited `kubejs:ruined_*` replacement gives a derelict read for free |
| C0064 inert-machine policy | partial — satisfied for free by the above |
| C0065-C0067 district assembly, landmarks, optimization | NOT STARTED |
| **C0068 P04-GATE** | not started — needs in-client assembly connectivity + independent visual review |

**Verdict:** the grammar mechanism works and has a schema + validator; the per-band
families and the macro-scale axis system are future work.

## Phase 5 — Environment and ambience — **NEXT**

| Piece | Status |
|---|---|
| C0018 air-hazard prototype | done (Phase 1 stub) |
| C0069-C0074 exposure model, PPE, filter economy, ventilation/shelter, acid contact | **starting now** |
| C0075-C0078 sky/light, fog volumes, particles/weather, soundscape | partial (biome effects); custom sky needs the companion module |
| C0079-C0082 feedback, failure/recovery, optimization, P05-GATE | NOT STARTED |

## Phases 6-8

Not started. **Phase 6 (gameplay: craftable entry, navigation, enemy roster, loot
tiers, factions, capstone, quest integration)** is what turns the explorable
megastructure into a *destination*; it formally depends on P03+P04+P05.

## What the coordinator can do without a running client

- Phase 5 environment systems that are datapack + KubeJS (exposure, filter, shelter,
  acid contact, per-band ambience) — **doing now**.
- Phase 6 documentation checkpoints (C0083 progression contract, C0093 factions/narrative).
- Tighten the density graph and module families against the contracts.

## What needs the owner

- **P00-GATE + P01-GATE reviews** (independent + in-client runtime run).
- **P02-GATE** — the in-game visual/experiential review that freezes the massing.
- The 4 P00-GATE open items (flavour names, canon hook, arrival anchor, taller height).
- The C0021 pre-Hive performance baseline capture.
- A truly custom dimension sky/renderer (requires the `packdev/hive-world-companion`
  NeoForge module — a build step, not a datapack).
