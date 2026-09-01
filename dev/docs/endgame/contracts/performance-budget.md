# Endgame — performance budget

**Authority:** `docs/Endgame.md` §8 completeness axis and checkpoint `EG-P00-S04-C0008`.
**Status:** ACCEPTED 2026-08-27 as an initial budget. Every threshold is provisional;
proven at `EG-P02-S06-C0035` (greybox), tightened/verified at Phase 7
(`C0106` generation, `C0107` client, `C0108` server).

## Measurement method

| Surface | Tool | When |
|---|---|---|
| Chunk generation time | `spark profiler` during a fixed-seed pregeneration (Chunky or `/forceload` sweep) over the Hive at spawn radius 512; per-chunk timing histogram | Phase 2, Phase 3 (`C0049`), Phase 7 (`C0106`) |
| Server tick | `spark tps` + `spark healthreport` on a dedicated server, 0 players and N players in the Hive | Phase 5 (`C0071`, `C0081`), Phase 7 (`C0108`) |
| Client frame time | F3 + `Ctrl+F3` frame graph + `spark` client profiler at fixed cameras and a representative stack-core location | Phase 2 (`C0035`), Phase 7 (`C0107`) |
| Memory | `spark healthreport` heap + GC; dimension-loaded overhead vs. baseline | Phase 2, Phase 7 |
| Fluids / block entities | `spark` + `/data`/`/execute` counts per chunk in the structure QA world | Phase 3 (`C0044`), Phase 4 (`C0067`), Phase 7 (`C0104`) |

**Baseline:** a pre-Hive capture is taken at `EG-P01-S05-C0021` (fresh client + dedicated
server, no Hive content loaded). Every budget below is **both** an absolute ceiling
**and** a "no regression worse than +X% vs. this baseline" rule, whichever is stricter.
The dev-machine baseline hardware is recorded in the C0021 evidence file.

## Budgets

### Chunk generation (dev baseline, fresh Hive pregen, radius 512)

| Metric | Initial ceiling |
|---|---|
| p50 per-chunk generation | ≤ 25 ms |
| p95 per-chunk generation | ≤ 60 ms |
| p99 per-chunk generation | ≤ 120 ms |
| worst single chunk | < 500 ms (no hitch spikes) |
| regression vs. baseline Overworld-wasteland pregen | ≤ +50 % p95 |

### Block entities

| Metric | Initial ceiling |
|---|---|
| average ticking BE per chunk inside a stack core | ≤ 8 |
| peak ticking BE in any single chunk | ≤ 24 |
| live production machinery in set dressing | 0 — inert equivalents only (`EG-P04-S06-C0064`) |

### Fluids

| Metric | Initial ceiling |
|---|---|
| acid fluid ticks during chunk generation | ≤ 64 per chunk |
| ongoing acid fluid updates in a settled, loaded chunk | 0 (acid features are pre-settled source blocks with no un-updated flowing edge) |

### Ticking code — Hive companion module (server-side)

| Metric | Initial ceiling |
|---|---|
| atmosphere + shelter service per online player in the Hive | ≤ 0.30 ms/tick |
| service cost with 0 players in the Hive | ≤ 0.05 ms/tick |
| complexity | O(players in the Hive), never O(all players) or O(loaded chunks) |

### Particles

| Metric | Initial ceiling |
|---|---|
| ambient particle spawn rate | ≤ the vanilla Nether ambient budget |
| storm-event particle rate (`EG-P05-S05-C0077`) | ≤ 2× ambient, time-boxed |
| client-side | respect the client particle setting; hard cap enforced |

### Structure scale (per module — corpus budget set at `EG-P04-S08-C0067`)

| Metric | Initial ceiling |
|---|---|
| module footprint | ≤ 128 × 128 blocks |
| module height | ≤ 96 blocks |
| non-air blocks per module | ≤ 48,000 |
| block entities per module | ≤ 6 |
| NBT file size | ≤ 2 MB |
| a placed district assembly | fits within its generated cell; no cross-cell spill |

### Memory / client

| Metric | Initial ceiling |
|---|---|
| Hive loaded-dimension heap overhead (12-chunk radius, 1 player) | ≤ 512 MB additional |
| client FPS in a representative stack core vs. Overworld wasteland at equal settings | ≥ 90 % |

## Deferred

Final tuned thresholds, the recorded baseline hardware, and per-camera client numbers
→ `C0021`, `C0035`, and Phase 7. Seed-sweep generation distribution → `EG-P03-S06-C0048`
/ `EG-P07-S02-C0103`.
