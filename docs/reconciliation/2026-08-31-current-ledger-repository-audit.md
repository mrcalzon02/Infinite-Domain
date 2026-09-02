# Infinite Domain Current Reconciliation Ledger

Date: 2026-08-31  
Branch: `main`  
Method: DEEFM (`INTENT -> EXECUTE -> OBSERVE -> VERIFY -> CLAIM`)

## Scope

This ledger records only Infinite Domain implementation, validation, packaging, and runtime evidence present in the authoritative Infinite Domain repository. Conversation intent, sandbox-only work, local-only changes, and state belonging outside this repository are not promoted into Infinite Domain completion claims.

The post-reconciliation repository boundary is defined by `REPOSITORY_SCOPE.md` and `.gitignore`. Local worlds, logs, saves, screenshots, benchmark output, caches, build products, dependency caches, ordinary third-party mod binaries, and unrelated repository state are excluded from Infinite Domain release-source state unless an Infinite Domain artifact is deliberately imported and committed here.

## 1. Visible fractally occluded hex-grid wasteland caves

The authoritative implementation now supplies literal repeated hexagonal corridor
loops and chamber cells through the project-owned
`infinite_domain_worldgen:hex_grid_cave` density codec. Three bounded cave strata
are integrated directly into `wastelands:wasteland` final density. A world-seeded
four-octave NormalNoise barrier locally occludes the grid without replacing its
geometry; the land gate excludes all ocean bands and the codec protects radius
288 around the Spawn Hospital.

Generic cave carvers, an invisible organizational hex scaffold, or a stamped source image do not satisfy this requirement.

Static and geometric validation passes 8/8 and the pack-wide geography gate owns
the integration as `OG-13`. Isolated NeoForge smoke run
`20260831-193211_baseline_smoke-r01` loaded the codec and generated a fresh 4x4
remote Overworld tile before clean shutdown. Fixed-seed visual legibility, coast
termination, and comparative performance evidence remain intentionally separate.

**Status:** IMPLEMENTED + RUNTIME LOAD VERIFIED — fresh-world visual acceptance still required.

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

The apparent 84-vs-64 discrepancy is resolved as two adjacent but distinct
corpora. `structure_library/corpus-manifest.json` owns 84 authoritative
Wasteland source templates. The canon-pinned Old World revision matrix and
`structure_targets.json` deliberately own 64 narrative descendants,
`OWS-001` through `OWS-064`. There are no missing `OWS-065` through `OWS-084`
targets. Static validation now asserts both counts and their separate roles.

`OWS-001` through `OWS-007` are recorded as statically completed, `OWS-008` is
the active target, and no entries are currently recorded in
`runtime_quality_approved`. Existing structures must still proceed through the
production-admission path rather than remaining permanently at static
validation.

The active OWS-008 builder and authoritative shipping NBT now match exactly in
both serialized and decompressed form. A block-level comparison against the
prior committed artifact proved that the command/archive stair repair was
already present in shipping geometry; the eight route cells are therefore
verified, not newly changed. The actual shipping delta is limited to eight
brewing stands and three filled cauldrons replaced with the pack's inert ruined
variants, closing a progression/loot bypass without changing geometry. The
target retains its mountain-only biome selector from the 64-site worldgen-role
registry.

A state audit also found that Gate-A r1 was recorded as passed even though its
persisted review says `REVISION REQUIRED`. The exact Gate-A r2 artifact is now
independently passed. Passes 7–12 and the repaired Gate-B r2 intact candidate
subsequently exposed and corrected 54 hidden shell-overlap obstructions across
the declared public, treatment-cell and service aisles while preserving the
authoritative shipping NBT byte-for-byte. The hash-bound Gate-B r2 fixed-camera
review is passed; Pass 13 historical layering is now the next legal stage. No
runtime-quality approval was inferred.

The focused scope/worldgen gate passes. The legacy full serialized-block mode
still reports seven pre-existing targets (`OWS-001`, `OWS-006`, `OWS-011`,
`OWS-028`, `OWS-029`, `OWS-030`, and `OWS-032`) whose valid vanilla functional
props predate the current inert ruined-block policy. OWS-008 is no longer in
that queue. Those targets were not bulk-regenerated here because the Heavy
Rebuild doctrine requires sequential target ownership.

**Status:** SCOPE RESOLVED / ADMISSION OPEN — continue sequential final production admission from `OWS-008` with retained runtime-quality evidence.

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

Smoke run `20260831-193211_baseline_smoke-r01` is authoritative evidence that the
official NeoForge runtime boots the pack and completes fresh Overworld chunk
generation. Its optional Arise/Lost Cities acceptance probes encountered Rhino
local-declaration errors; the post-run controller fix passes static validation but
has not yet received a retained runtime rerun. Those probe-dependent claims are
therefore still withheld.

**Status:** PARTIAL — official runtime generation observed; broad acceptance-probe rerun still pending.

## 7. Repository scope integrity

Infinite Domain completion claims are restricted to Infinite Domain-side artifacts and evidence committed to authoritative `main`. Work outside this repository is not counted as Infinite Domain implementation state unless the required Infinite Domain artifact is deliberately incorporated here.

No named external project belongs in this ledger or in Infinite Domain repository-scope documentation.

**Status:** VERIFIED — repository-local scope rule established.

## Reconciliation and merge recovery

The locally reconciled history has reached the authoritative repository. The merge sequence incorporated local development state with the reconciliation commits rather than discarding that work. During inspection, `docs/worldgen-benchmark/README.md` was found to contain literal Git conflict markers left by that merge; those markers were subsequently resolved while preserving both valid sides of the documentation.

The reconciliation process must continue from the current authoritative `main`, not from the earlier `b2879ef0...` checkpoint.

## Next executable work

### Repository implementation track

The Wasteland hex-grid implementation omission is closed with static geometry and
runtime load/chunk-generation evidence; visual approval remains open. The Old
World 84-source/64-descendant scope distinction is now explicit and guarded.
OWS-008 Gate A r2 and the repaired Gate B r2 intact model are now independently
passed. The next repository implementation priority is Passes 13–18, followed
by a Gate-C r2 damage-state set whose D0 exactly preserves the accepted intact
model. Do not populate runtime-quality approvals without retained in-world evidence.

### Runtime evidence track

On the authoritative Minecraft instance, execute:

```powershell
.\scripts\run_worldgen_benchmark.ps1 -Variant baseline -Suite standard -Repetitions 1 -KeepRuntime
```

Retain the runtime and `result.json`. Use observed evidence to advance items 6, 5, and 3 in that order. Do not convert registry presence into natural-generation proof and do not convert headless Lost Cities load success into visual-quality approval.

### Heavy Rebuild track

Continue OWS-008 with Passes 13–18 and render Gate C r2 only after those records
are verified. Its D0 state must exactly preserve the accepted Gate-B r2 model;
D1/D3 must add causal history and damage without resealing circulation or moving
mandatory proof. The 84-entry Wasteland source corpus and 64-entry Old World
narrative registry are separate validated scopes. Runtime-quality approvals must
be backed by retained evidence rather than automatically populated.
