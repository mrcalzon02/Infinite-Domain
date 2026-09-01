# Infinite Domain Current Reconciliation Ledger

Date: 2026-08-31  
Branch: `main`  
Method: DEEFM (`INTENT -> EXECUTE -> OBSERVE -> VERIFY -> CLAIM`)

## Scope

This ledger records only Infinite Domain implementation, validation, packaging, and runtime evidence present in the authoritative Infinite Domain repository. Conversation intent, sandbox-only work, local-only changes, and state belonging outside this repository are not promoted into Infinite Domain completion claims.

The post-reconciliation repository boundary is defined by `REPOSITORY_SCOPE.md` and `.gitignore`. Local worlds, logs, saves, screenshots, benchmark output, caches, build products, dependency caches, ordinary third-party mod binaries, and unrelated repository state are excluded from Infinite Domain release-source state unless an Infinite Domain artifact is deliberately imported and committed here.

## 1. Visible fractally occluded hex-grid wasteland caves

The required doctrine remains unfulfilled in authoritative worldgen evidence. Wasteland caves must preserve recognizable hexagonal corridors and cells as literal carved geometry. Deterministic seed-driven fractal/plasma fields may interrupt, occlude, thicken, thin, distort, and locally erase portions of the grid, but the hex geometry must remain visibly legible in the resulting cave system.

Generic cave carvers, an invisible organizational hex scaffold, or a stamped source image do not satisfy this requirement.

**Status:** OPEN — authoritative implementation and fixed-seed in-world evidence still required.

## 2. Planetary worlds: 30 sites / 15 major sites each

This requirement is implemented in the authoritative repository.

Commit `e70fce3b5f9bd08632a40c55a87f65d42366f074` established the earlier planetary inventory. Commit `920b0d75598177ff381690eb5a8b8a470b3bbe57` added the missing major/minor expansion pools, worldgen structures, and structure sets.

| Planet | Major | Minor | Total |
|---|---:|---:|---:|
| Moon | 15 | 15 | 30 |
| Mars | 15 | 15 | 30 |
| Venus | 15 | 15 | 30 |
| Mercury | 15 | 15 | 30 |
| Jupiter | 15 | 15 | 30 |

**Status:** VERIFIED — registered inventory/worldgen requirement is complete. Live placement quality remains a separate runtime concern.

## 3. Lost Cities runtime/new-world generation acceptance

Static integration is materially present, including resource resolution, semantic conversion, collision avoidance, and regional isolation work.

Runtime acceptance instrumentation is committed:

- `3c1e0cd1ad1de2df676f4fa0d29f6dad4936c258` records actual mod loading, runtime registries, and generated structure starts during isolated fixed-seed world generation.
- `5fd9089de0936243afe0d1f60d0364319ac87a1c` analyzes those observations into the machine-readable `acceptance` section of `result.json`.
- `b2879ef0f561ecf96c7a7b580174919ff63bc685` defines the retained runtime evidence contract.

Headless runtime success must not be promoted into skyline, rotation, terrain-seating, frequency, or visual-distribution approval.

**Status:** OPEN — retained fresh-world runtime run plus visual/distribution inspection required.

## 4. Heavy Rebuild final production admission

The authoritative Heavy Rebuild population is the **84-structure wasteland rebuild corpus**, not the Old World `OWS-*` narrative series. The previous 84-vs-64 discrepancy in this ledger was a category error caused by treating `OWS-001` through `OWS-064` as the Heavy Rebuild registry.

`dev/docs/WASTELAND_STRUCTURE_REBUILD_AUDIT.md` records the actual Heavy Rebuild state: **29 / 84** wasteland structures pass the mechanical geometry gate and **55** still have hard-fail geometry. The same audit records `decayed_logging_camp` as the first structure rebuilt, regenerated, and re-audited from disk under the v2 doctrine. `dev/structure_library/rebuild-phases.json` remains deliberately conservative: every phase is `requires_regeneration_v2` and `production_approvals` is still empty.

Mechanical-gate success is not production admission. The governing rebuild doctrine requires the remaining structures to be rebuilt/re-audited and final production approval to be backed by the required human QA-world walkthrough/review evidence. No approval may be invented merely because a structure passes static lint.

**Status:** OPEN — scope reconciled to the authoritative 84-structure corpus; 29/84 currently pass the mechanical gate, 55 require further v2 rebuild work, and final production approvals remain at zero pending required QA-world evidence.

## 5. Arise / Arise 7 Seas natural generation

The benchmark now records:

- whether `dungeons_arise` and `dungeons_arise_seven_seas` actually load;
- each namespace's live `STRUCTURE` and `STRUCTURE_SET` registrations;
- valid generated structure starts by namespace in every benchmark tile;
- a distinction between `runtimeRegistryReady` and `naturalGenerationObserved`.

Registry presence is not direct natural-placement evidence. Only observed valid structure starts in generated chunks establish natural generation for the tested world/region.

**Status:** OPEN — execute retained fixed-seed runtime generation and preserve direct placement evidence.

## 6. Runtime packaging/load-boundary audit

The static repository/package audit is complete for the inspected high-risk categories. The isolated benchmark harness preserves the ordinary playable instance and creates disposable runtime state outside release-source paths.

The live-load evidence channel is also implemented through the retained benchmark instrumentation, but it has not yet been promoted to complete because an authoritative runtime result has not been observed here.

**Status:** PARTIAL — static package boundary verified; retained live NeoForge load acceptance still pending.

## 7. Repository scope integrity

Infinite Domain completion claims are restricted to Infinite Domain-side artifacts and evidence committed to authoritative `main`. Work outside this repository is not counted as Infinite Domain implementation state unless the required Infinite Domain artifact is deliberately incorporated here.

No named external project belongs in this ledger or in Infinite Domain repository-scope documentation.

**Status:** VERIFIED — repository-local scope rule established.

## Reconciliation and merge recovery

The locally reconciled history has reached the authoritative repository. The merge sequence incorporated local development state with the reconciliation commits rather than discarding that work. During inspection, the worldgen benchmark README was found to contain literal Git conflict markers left by that merge; those markers were subsequently resolved while preserving both valid sides of the documentation.

The reconciliation process must continue from the current authoritative `main`, not from the earlier `b2879ef0...` checkpoint.

## Next executable work

### Repository implementation track

The strongest unresolved implementation omission remains item 1. The current repository does not expose a generic wasteland `configured_carver` registration that can safely receive the doctrine as a drop-in asset. The overworld wasteland sits inside the existing overworld/gradient-worldgen and Lost Cities integration, while the custom density-function codec implementation currently present belongs to a different dimension. Do not transplant that dimension-specific machinery into the overworld merely to create a nominal implementation. The next implementation step is to identify the overworld noise-router/biome generation hook that owns wasteland cave carving, then integrate literal visible hex-grid geometry there and validate the resulting codec/resource graph before runtime acceptance.

### Runtime evidence track

On the authoritative Minecraft instance, execute:

```powershell
.\scripts\run_worldgen_benchmark.ps1 -Variant baseline -Suite standard -Repetitions 1 -KeepRuntime
```

Retain the runtime and `result.json`. Use observed evidence to advance items 6, 5, and 3 in that order. Do not convert registry presence into natural-generation proof and do not convert headless Lost Cities load success into visual-quality approval.

### Heavy Rebuild track

The population discrepancy is resolved: Heavy Rebuild is the 84-structure wasteland corpus. Continue the v2 rebuild/audit sequence from the authoritative audit state, reducing the remaining 55 hard-fail structures. Production approvals must remain empty until the required QA-world walkthrough/review evidence exists; after that evidence is available, admit structures incrementally rather than bulk-populating approvals.
