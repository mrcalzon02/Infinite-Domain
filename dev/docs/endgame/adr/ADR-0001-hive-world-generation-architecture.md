# ADR-0001 — Hive World generation architecture

**Authority:** `docs/Endgame.md` §10 checkpoint `EG-P00-S03-C0005`.
**Status:** ACCEPTED 2026-08-27.
**Supersedes:** none. **Superseded by:** none.
**Depends on:** C0001 inventory, C0002 capability boundary, C0003 identity, C0004 spatial metrics.

## Context

`docs/Endgame.md` §2.7 requires that generation systems own *mass* (planetary crust,
stack envelopes, major voids, broad horizontal masks) while structures own *legibility*
(readable architecture, circulation, landmarks, rooms, damage, encounters). §2.7 also
states explicitly that a single enormous NBT, an ordinary random-spread city, or a Lost
Cities profile alone is **not** the world generator.

The C0002 capability audit fixed these ownership boundaries: the Hive datapack owns
dimension/type JSON, noise and density graphs, biome-source configuration, features,
structures, sets, pools, and tags; a dedicated companion module owns transactional
travel and recovery, dimension-scoped atmosphere interoperability, PPE adapters, custom
client effects, and telemetry; Isekai is an optional codec/provider layer pending
isolated tests; Lost Cities is a potential donor grammar only after live acceptance.

## Decision

Adopt a **four-layer hybrid generator**:

| Layer | Owns | Implementation | Determinism |
|---|---|---|---|
| 1. Mass & mask | planetary crust, dead-waste terrain, stack-core/apron masks, stack envelope density, major-void reservations, vertical-strata field | density functions + noise settings in the Hive datapack (`infinite_domain:hive_world` noise settings; density graph under `worldgen/density_function/hive_world/`) | seed-deterministic by construction |
| 2. Macro placement | stack-cluster centres, trunk-axis routes between clusters, district anchors, landmark slots | Hive-owned deterministic placement logic (datapack structure-set spacing for cluster centres; a Hive-owned cross-chunk planner for trunk axes, `EG-P04-S05-C0062`) | seed-deterministic; never vanilla random spread for axes |
| 3. Module assembly | readable rooms, thresholds, circulation, damage states, encounters, ornament inside bounded cells | vanilla jigsaw + template pools + processors, configured by the Hive datapack; bounded to a cell, never planning the city | seed-deterministic within a placed cell |
| 4. Runtime services | transactional entry/return/recovery, dimension-scoped atmosphere, PPE adapters, client sky/fog/effects, telemetry | dedicated NeoForge companion module `packdev/hive-world-companion` (optional, graceful absence), built from C0009/C0011 | server-authoritative, transactional |

**Optional providers, each gated behind its own acceptance spike, none owning identity
or macro planning:**

- **Isekai API** — may supply climate/rule biome sources or surface-rule codecs if the
  `EG-P01-S02-C0016` routing spike and a codec-reload test pass. Fallback: vanilla
  multi-noise for broad routing.
- **Lost Cities** — may supply donor ruin parts or a bounded ruin grammar *inside cells
  only*, after a live codec/palette/rotation/terrain/performance acceptance spike.
  Never owns the top-level generator or the grid. Fallback: feed selected donor NBT to
  vanilla template pools with no Lost Cities generation.

## Alternatives considered and rejected

| # | Alternative | Why rejected |
|---|---|---|
| A | One enormous authored NBT for a stack | Not seedable or variable; catastrophic chunk-generation and memory cost; no macro determinism; fails §2.7 explicitly. |
| B | Pure Lost Cities profile | Surface-city / grid model conflicts with full-height envelopes; runtime codec gate still pending (C0002); cannot guarantee vertical strata, trunk axes, or below-sea placement. Fails §2.7 explicitly. |
| C | Pure random-spread jigsaw city | Random spread cannot guarantee long aligned axes, continuous circulation, or exact district joins (C0002 structure-infrastructure row). Owns legibility but not mass. |
| D | Pure density function, no structures | Density shapes mass and voids but not readable rooms, thresholds, damage states, or encounters. Owns mass but not legibility. |
| E | Isekai `AssembledStructure` / `GroundedTemplateStructure` as the city builder | C0002 classified `AssembledStructure` **unsuitable** (surface-centred, rejects Y at/below sea level); `GroundedTemplateStructure` is one-template surface placement and cannot assemble a city. |
| F | **Four-layer hybrid (this ADR)** | **Chosen.** Matches §2.7 and the C0002 ownership boundary exactly; each layer is independently testable and reversible. |

## Consequences

**Positive:** seed-deterministic; testable layer by layer (Phase 3 proves layers 1–2,
Phase 4 proves layer 3, Phase 5–6 prove layer 4); each subsystem is independently
ownable, rollback-able, and gate-able; the design consumes only capabilities the C0002
audit verified.

**Negative:** requires a Hive-owned macro-placement code path that does not exist yet
(the trunk-axis planner, `EG-P04-S05-C0062`); more moving parts than any single
approach; the density-to-structure seam is the principal technical risk and is
explicitly gated at the P03→P04 boundary.

**Neutral:** Isekai and Lost Cities stay optional behind their own spikes; the companion
module is optional with graceful absence.

## Rollback

- The dimension is **additive** and fully removable; `EG-P01-S06-C0023` proves removal
  without damaging other dimensions (diff/path audit).
- The companion module is **optional** with graceful absence, following the
  `unified-radiation` and `lostcities-highway-compat` precedents.
- Each generation layer reverts independently: disable layer 3 → a bare massed dimension
  still loads; revert layer 1 customisation → vanilla noise fallback; remove layer 4 →
  a data-only dimension with an operator-command travel fallback (C0002 entry-travel
  fallback row).
