# Current Reconciliation Ledger — Repository Audit

Date: 2026-08-31
Branch: `main`
Baseline: `98b4a64d05ade7e92a72bacf01fc7e406d946edc` (`updates`)
Method: DEEFM (`INTENT -> EXECUTE -> OBSERVE -> VERIFY -> CLAIM`)

## Scope

This record audits the current reconciliation ledger against the authoritative `mrcalzon02/Infinite-Domain` repository after the large local-to-Git reconciliation commit. It records only evidence visible in the authoritative repository. Conversation intent, sandbox files, and work belonging to other repositories are not promoted to Infinite Domain implementation state.

## Repository and packaging boundary

The authoritative repository is Infinite Domain on branch `main`. The repository scope and `.gitignore` establish a release-source boundary: local player/runtime state, caches, crash reports, logs, saves, screenshots, benchmark outputs, nested scratch checkouts, build products, dependency caches, ordinary third-party mod binaries, and local authoring/recovery payloads are excluded. Only project-owned `infinite-domain-*` mod artifacts are explicitly retained under `mods/`.

The baseline commit payload was checked for the principal high-risk runtime-state paths. No additions were observed under:

- `saves/`
- `logs/`
- `benchmark_runs/`
- `screenshots/`
- third-party `mods/`

The repository also contains `docs/worldgen-benchmark/README.md`, whose fixed-seed benchmark contract creates an isolated disposable NeoForge runtime and explicitly avoids modifying the ordinary instance, saves, configurations, or mod jars. Failed isolated runtimes are retained only for diagnosis.

**Claim:** the post-reconciliation repository passes the static package/load-boundary audit for the inspected high-risk categories. This is a repository/package claim only; it does not prove a successful client or dedicated-server load.

## Ledger reconciliation

### 1. Visible fractally occluded hex-grid wasteland caves

No repository evidence reviewed in this audit is sufficient to claim that the conversation doctrine has been implemented and accepted in active Wasteland cave generation. The required doctrine remains: recognizable white/void hexagonal cave corridors and cells must survive as visible geometry while fractal/plasma noise occludes, interrupts, thickens, thins, and distorts them.

**Status:** OPEN — implementation/runtime evidence required.

### 2. Planetary worlds: 30 sites / 15 major sites each

This item is implemented in the authoritative repository.

Commit `e70fce3b5f9bd08632a40c55a87f65d42366f074` established the pre-expansion per-planet inventory after adding the first minor-site families: Moon 15 total from a 3-site major baseline, Mars 10 from 2, Venus 10 from 2, Mercury 5 from 1, and Jupiter 5 from 1. That means the retained pre-expansion split was:

| Planet | Existing major | Existing minor |
|---|---:|---:|
| Moon | 3 | 12 |
| Mars | 2 | 8 |
| Venus | 2 | 8 |
| Mercury | 1 | 4 |
| Jupiter | 1 | 4 |

Commit `920b0d75598177ff381690eb5a8b8a470b3bbe57` then added separate `*_major_expansion` and `*_minor_expansion` template pools, structure registrations, and random-spread structure sets for all five planetary worlds. Current `main` contains the following expansion-pool counts:

| Planet | Added major | Added minor | Final major | Final minor | Final total |
|---|---:|---:|---:|---:|---:|
| Moon | 12 | 3 | 15 | 15 | 30 |
| Mars | 13 | 7 | 15 | 15 | 30 |
| Venus | 13 | 7 | 15 | 15 | 30 |
| Mercury | 14 | 11 | 15 | 15 | 30 |
| Jupiter | 14 | 11 | 15 | 15 | 30 |

The expansion pools are wired into planetary jigsaw structures and structure sets on `main`; this claim is about committed inventory/worldgen registration, not live placement frequency or terrain quality in an actual generated world.

**Status:** VERIFIED — 30 registered sites per planet, including 15 major and 15 minor per planet.

### 3. Lost Cities runtime/new-world generation acceptance

The repository contains substantial static Lost Cities activation evidence, including Karsic resource resolution, semantic conversion, collision avoidance, and regional isolation checks. Those gates explicitly retain fresh-world frequency, rotation, terrain seating, skyline/distribution, visual quality, and/or performance as runtime checks.

Runtime evidence instrumentation is now committed. Commit `3c1e0cd1ad1de2df676f4fa0d29f6dad4936c258` records whether `lostcities` loads in the isolated NeoForge runtime while fresh fixed-seed chunks are generated. Commit `5fd9089de0936243afe0d1f60d0364319ac87a1c` promotes those observations into the machine-readable `acceptance` section of `result.json`. Commit `b2879ef0f561ecf96c7a7b580174919ff63bc685` defines the retained acceptance contract and explicitly prevents headless load success from being misrepresented as visual/distribution approval.

**Status:** OPEN — acceptance machinery is committed, but an actual retained runtime run and subsequent Lost Cities visual/distribution review are still required.

### 4. Heavy Rebuild final production admission

The authoritative Heavy Rebuild state currently scopes `OWS-001` through `OWS-064`, not 84 targets. `OWS-001` through `OWS-007` are recorded as statically completed, `OWS-008` is the active target, and `runtime_quality_approved` is empty. Therefore neither the conversation count of 84 nor final production admission can be promoted without additional authoritative evidence.

**Status:** OPEN — first reconcile the 84-vs-64 scope discrepancy, then complete production/runtime admission evidence. No runtime quality approvals are currently recorded.

### 5. Arise / Arise 7 Seas natural generation

Runtime verification instrumentation is now committed. Commit `3c1e0cd1ad1de2df676f4fa0d29f6dad4936c258` records whether `dungeons_arise` and `dungeons_arise_seven_seas` are loaded, snapshots each namespace in the live `STRUCTURE` and `STRUCTURE_SET` registries, and inventories valid generated structure starts by namespace in every generated benchmark tile. Commit `5fd9089de0936243afe0d1f60d0364319ac87a1c` distinguishes `runtimeRegistryReady` from `naturalGenerationObserved`, so registry presence cannot be mistaken for actual placement. Commit `b2879ef0f561ecf96c7a7b580174919ff63bc685` documents the evidence standard.

**Status:** OPEN — the instrumentation is complete, but direct natural-generation observation still requires the retained fixed-seed runtime run. Only `naturalGenerationObserved: true` is sufficient direct placement evidence for the tested region.

### 6. Runtime packaging/load-boundary audit after reconciliation

The static repository/package half is completed by this audit: high-risk runtime/local paths were checked against the baseline payload and repository exclusion policy; the isolated worldgen harness preserves the ordinary instance boundary.

The same retained runtime evidence path now records mod loading and acceptance-probe failures during fresh isolated world generation, providing the missing live-load evidence channel without contaminating the ordinary instance.

**Status:** PARTIAL — STATIC PACKAGE/LOAD BOUNDARY VERIFIED; live-load instrumentation is committed; ACTUAL RETAINED LIVE LOAD ACCEPTANCE PENDING.

### 7. Continuity Works separation

Continuity Works is a separate repository obligation. Nothing performed or recorded here counts Continuity Works work as an Infinite Domain implementation or commit. Infinite Domain repository scope remains limited to Infinite Domain-owned release content and supporting project records.

The boundary is now also explicit in `REPOSITORY_SCOPE.md`: Continuity Works tools, base NBT corpus, audits, commits, issues, release state, and other obligations are not Infinite Domain implementation state unless the required Infinite Domain-side change/evidence exists here; Infinite Domain commits likewise cannot be presented as satisfying Continuity Works obligations.

**Status:** VERIFIED — repository boundary preserved and explicitly enforced by the scope contract.

## Process endpoint and resume contract

### Last verified authoritative endpoint

The reconciliation process last reached and verified authoritative `main` at commit `b2879ef0f561ecf96c7a7b580174919ff63bc685` (`docs: define retained runtime acceptance evidence`). The immediately preceding runtime-acceptance commits are:

1. `3c1e0cd1ad1de2df676f4fa0d29f6dad4936c258` — retain runtime structure acceptance evidence in the benchmark controller.
2. `5fd9089de0936243afe0d1f60d0364319ac87a1c` — analyze the evidence and emit conservative acceptance state in `result.json`.
3. `b2879ef0f561ecf96c7a7b580174919ff63bc685` — define the retained runtime acceptance contract and the one-pass reconciliation run.

No later Wasteland hex-cave implementation commit was observed after that endpoint when this handoff was reconstructed. Any cave geometry discussed or prepared outside the repository must therefore be treated as uncommitted working material until it is reconstructed against the authoritative generation path, committed, and read back from `main`.

### What the process was allowed to advance without a live Minecraft instance

Repository-only access was sufficient to:

- reconcile and correct the planetary structure inventory;
- enforce the Infinite Domain / Continuity Works repository boundary;
- perform the static packaging/load-boundary audit;
- add the runtime evidence probes and analysis required for Lost Cities, Arise, Arise 7 Seas, and live-load verification;
- define a retained fixed-seed acceptance run that does not alter the ordinary instance.

Repository-only access was **not** sufficient to claim:

- actual Lost Cities fresh-world visual/distribution acceptance;
- actual Arise or Seven Seas natural structure placement;
- actual client/dedicated-server load acceptance;
- runtime production admission for Heavy Rebuild structures;
- visible in-world conformance of the Wasteland hex-cave doctrine.

Those claims require execution and observation in a real NeoForge/Minecraft runtime.

### Intended progress from the endpoint

**Runtime track — first executable action on the authoritative instance:**

```powershell
.\scripts\run_worldgen_benchmark.ps1 -Variant baseline -Suite standard -Repetitions 1 -KeepRuntime
```

Retain the resulting runtime and `result.json`. Use it to advance, in order:

1. item 6 live-load acceptance if the run completes with no acceptance-probe errors;
2. item 5 Arise / Seven Seas registry readiness and, only where observed starts exist, natural-generation verification;
3. item 3 Lost Cities headless fresh-world load acceptance, followed by visual/distribution inspection of the retained runtime before final acceptance.

**Repository implementation track — strongest outstanding code omission:**

Implement item 1 directly in the authoritative Wasteland cave-generation path. The generated cave network must preserve recognizable hexagonal cells/corridors as literal carved geometry while deterministic seed-driven fractal/plasma fields interrupt, occlude, thicken, thin, distort, and locally erase portions of that geometry. Do not substitute generic cave carvers, an invisible hex organizational scaffold, or a stamped source image. Do not attach speculative cave assets until their authoritative biome/worldgen registration path is identified and validated.

**Heavy Rebuild track:**

After or alongside the runtime evidence pass, reconcile the requested 84-target scope against the current authoritative 64-target Heavy Rebuild registry. Do not silently invent targets or call 64 equal to 84. Once scope is authoritative, continue sequential production admission from the current active target and require retained runtime-quality evidence before adding entries to `runtime_quality_approved`.

## Next executable priority

The strongest immediate action depends on environment capability:

- **If the authoritative Minecraft instance is available:** run the retained one-pass benchmark above, because it can advance items 3, 5, and 6 simultaneously.
- **If only repository access is available:** locate and implement the actual Wasteland cave-generation path for item 1, then commit only after static validation and authoritative read-back.

Until those runtime observations exist, no static record should promote Lost Cities, Arise/Arise 7 Seas, Heavy Rebuild runtime admission, or live-load acceptance to complete.
