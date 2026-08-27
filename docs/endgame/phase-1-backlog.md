# Endgame — Phase 1 backlog (expanded)

**Authority:** `docs/Endgame.md` Phase 1 table and checkpoint `EG-P00-S06-C0011`.
**Status:** ACCEPTED 2026-08-27. Expands C0013–C0024 into exact owned paths,
dependencies, and evidence. No checkpoint here exceeds the §4.5 atomic sizing rules.

**Fixed Phase 1 constants** (so mutually-dependent checkpoints can proceed in parallel):

- Arrival anchor: `infinite_domain:hive_world` at `(8, 64, 8)`, facing +X (provisional;
  refined against real terrain at `EG-P03-S06-C0047`).
- Client effects: reuse `minecraft:the_nether` for Phase 1 (C0002 fallback).
- Entry gate for the spike: an **operator/creative item + command** — no crafting recipe,
  no automation. The real constructible access mechanism is Phase 6 `C0084`.

---

## C0013 — Registry skeleton `EG-P01-S01-C0013`

| | |
|---|---|
| Owned paths | `kubejs/data/infinite_domain/dimension/hive_world.json`, `kubejs/data/infinite_domain/dimension_type/hive_world.json` |
| Depends on | C0006 (height), C0009 (layout) |
| Atomic output | a minimal dimension + dimension_type that load with no error |
| Evidence | datapack loads clean; `/forge dimensions` lists `infinite_domain:hive_world`; `dimension_type` bounds equal the C0006 contract |
| Validation | `validate_hive_world_smoke.py` assertions 1, 3, 4; in-client `/execute in infinite_domain:hive_world run tp @s 8 64 8` |
| Not in scope | biomes beyond one placeholder ref, structures, hazards |

## C0014 — Baseline generator `EG-P01-S01-C0014`

| | |
|---|---|
| Owned paths | `kubejs/data/infinite_domain/worldgen/noise_settings/hive_world.json`; `.../worldgen/density_function/hive_world/*.json` (minimal); `scripts/endgame/generate_hive_world_noise.py`; manifest entry |
| Depends on | C0013, C0005, C0006 |
| Atomic output | simple noise settings producing safe solid terrain near `(8,64,8)`, respecting `-64..319`, `sea_level -40` |
| Evidence | fresh chunk generation at spawn; height probes at the six band midpoints; no void/lava at the arrival anchor |
| Validation | smoke validator; `/execute in … tp`; informal `spark` chunk-gen sample within the C0008 budget |

## C0015 — Spike biomes `EG-P01-S02-C0015`

| | |
|---|---|
| Owned paths | `worldgen/biome/hive_world_dead_waste.json`, `worldgen/biome/hive_world_stack_test.json`; `scripts/endgame/generate_hive_world_biomes.py`; manifest |
| Depends on | C0013 |
| Atomic output | one wasteland biome + one stack test biome, both registered and legal |
| Evidence | registry lists both; `/locate biome infinite_domain:hive_world_dead_waste` succeeds |
| Validation | smoke validator assertion 2; `/locate biome` |

## C0016 — 3D routing `EG-P01-S02-C0016`

| | |
|---|---|
| Owned paths | biome source block in `dimension/hive_world.json`; `worldgen/density_function/hive_world/biome_mask.json` |
| Depends on | C0014, C0015 |
| Atomic output | vertical or mask-based separation placing `hive_world_stack_test` inside a core mask and `hive_world_dead_waste` outside, or by Y band |
| Evidence | biome sampled at the §3 probe coordinates across X/Y/Z matches intent |
| Validation | scripted `/data`/`/locate` sweep over the reserved seeds; optional Isekai routing spike (fallback: vanilla `multi_noise`) |

## C0017 — Acid feature `EG-P01-S03-C0017`

| | |
|---|---|
| Owned paths | `worldgen/configured_feature/hive_world/acid_pool.json`, `worldgen/placed_feature/hive_world/acid_pool.json`; biome feature reference |
| Depends on | C0014, C0015; uses the verified block `the_wasteland_reworked:acid` |
| Atomic output | a bounded acid pool feature in The Drown / low wastes, pre-settled source blocks |
| Evidence | pool generates; **no runaway fluid updates** (0 ongoing updates in a settled chunk, C0008); entity-contact damage observed and recorded |
| Validation | `spark` fluid-tick check; `/tick freeze` inspection; entity walk-in test |

## C0018 — Air hazard prototype `EG-P01-S03-C0018`

| | |
|---|---|
| Owned paths | `kubejs/server_scripts/hive_world_atmosphere_proto.js` |
| Depends on | C0013 |
| Atomic output | dimension-scoped periodic exposure applied only in `infinite_domain:hive_world`, honouring the C0007 shape (rate, PPE reduction stub, sealed-volume gate stub) |
| Evidence | protected vs. unprotected test; per-tick cost measured (C0008 companion budget as the target even though this is the KubeJS stand-in) |
| Validation | `spark` tick sample; toggle test with a stub filter item |

## C0019 — Reversible entry `EG-P01-S04-C0019`

| | |
|---|---|
| Owned paths | `kubejs/server_scripts/hive_world_expedition.js`; `kubejs/data/infinite_domain/advancement/hive_world/*.json`; lang keys in `kubejs/assets/infinite_domain/lang/en_us.json` |
| Depends on | C0013, C0020 (arrival anchor + platform) |
| Atomic output | a gated operator teleport that: captures origin (dimension + exact pos + yaw), transfers to the arrival anchor, grants a return method, and handles death, disconnect-mid-transfer, and missing-destination-chunk |
| Evidence | round trip returns to the exact origin; death in the Hive → normal respawn with the transaction cleared; disconnect during transfer → safe, non-duplicated state on relog; destination chunk absent → player still lands safely (platform is force-built) |
| Validation | the C0002 travel test list: gate, missing level, unsafe/occupied target, passenger, repeat use, restart, permission failure |
| Not in scope | crafting recipe, automation, multiplayer stress (Phase 6 `C0084`, Phase 7 `C0110`) |

## C0020 — Safe arrival `EG-P01-S04-C0020`

| | |
|---|---|
| Owned paths | `kubejs/data/infinite_domain/function/hive_world/build_arrival.mcfunction` (and/or `structure/hive_world/arrival_platform.nbt`); referenced by the C0019 script |
| Depends on | C0014 |
| Atomic output | a deterministic non-lethal arrival platform / airlock at `(8, 64, 8)`, rebuilt if obstructed or missing |
| Evidence | repeated fresh arrivals land on solid ground with headroom and no suffocation/fall; place an obstruction, re-arrive, still safe |
| Validation | scripted repeat-arrival loop; obstruction test |

## C0021 — Client baseline `EG-P01-S05-C0021`

| | |
|---|---|
| Owned paths | `effects`, `ambient_light`, `fixed_time` fields in `dimension_type/hive_world.json`; `docs/endgame/evidence/EG-P01-S05-C0021/` |
| Depends on | C0013 |
| Atomic output | temporary fog/sky/ambient-light/sound assumptions (reusing `minecraft:the_nether` effects) **and the pre-Hive performance baseline capture** required by C0008 |
| Evidence | screenshots at `hive-cam-arrival-01` / `hive-cam-waste-01`; client log clean; baseline `spark` reports for client and dedicated server with no Hive content loaded |
| Validation | client-log check; baseline archived in the evidence dir |

## C0022 — Smoke validator `EG-P01-S05-C0022`

| | |
|---|---|
| Owned paths | `scripts/endgame/validate_hive_world_smoke.py` |
| Depends on | C0013–C0021 |
| Atomic output | the validator implementing the seven C0010 assertions |
| Evidence | clean pass from a fresh checkout |
| Validation | run it; it exits 0 with a JSON report in the evidence dir |

## C0023 — Spike removal test `EG-P01-S06-C0023`

| | |
|---|---|
| Owned paths | `docs/endgame/hive-world-path-manifest.txt`; `docs/endgame/evidence/EG-P01-S06-C0023/` |
| Depends on | C0013–C0022 |
| Atomic output | documented, verified removal of all Hive paths without damaging other dimensions (C0010 §9 procedure) |
| Evidence | diff/path audit; fresh client + dedicated server load Overworld/Nether/End unchanged with the Hive removed |
| Validation | the C0010 §9 five-step procedure |

## C0024 — Phase 1 gate `EG-P01-S06-C0024`

| | |
|---|---|
| Owned paths | `docs/endgame/gates/P01-GATE-evidence.md`; `docs/Endgame.md` ledger |
| Depends on | C0013–C0023 |
| Atomic output | technical-feasibility decision |
| Evidence | codec load, round-trip, hazard, acid, clean logs, and the §8 completeness matrix |
| Validation | independent integration review (§7.3) — cannot be self-approved |

---

## Sequencing note (user priority)

The owner has directed that the custom enter/exit mechanics be built **immediately
after the dimension is created**. The dependency graph permits it: C0019/C0020 need
only C0013 (registry) + C0014 (safe terrain) + the fixed arrival anchor above — not
C0015–C0018. The coordinator's Phase 1 order is therefore:

`C0013 → C0014 → C0020 → C0019` … then `C0015, C0016, C0017, C0018` … then
`C0021 → C0022 → C0023 → C0024`.

Biomes, 3D routing, acid, and the air-hazard prototype are not blockers for the
round-trip and are scheduled after it.
