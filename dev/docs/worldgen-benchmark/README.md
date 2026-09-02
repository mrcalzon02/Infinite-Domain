# Fixed-seed world-generation benchmark

This regimen measures fresh chunk generation without opening a client or manually creating a world. Every run starts an isolated NeoForge dedicated server, creates the same world from seed `-7046029254386353131`, generates the same chunk tiles in the same order, records timings, stops cleanly, and removes its disposable runtime after successful analysis.

The ordinary instance, `saves`, configurations, and mod jars are never modified. A failed run keeps its isolated runtime for diagnosis.

## One-time dedicated-server bootstrap

The CurseForge client installation does not contain NeoForge's patched dedicated-server jar or authoritative server argument file. Following the [official NeoForge server installation contract](https://docs.neoforged.net/user/docs/server/), install the pinned 21.1.248 runtime once before the first benchmark:

```powershell
.\scripts\bootstrap_worldgen_benchmark_server.ps1
.\scripts\run_worldgen_benchmark.ps1 -ValidateLauncher
python .\scripts\validate_worldgen_benchmark_launcher.py --output .\docs\worldgen-benchmark\launcher-validation.json
```

The bootstrap downloads the official NeoForge installer, verifies its pinned SHA-256, and installs into ignored `benchmark_runs/.launcher-cache/`. Benchmark runs hard-link that immutable library tree into each isolated runtime; they do not improvise a classpath from client artifacts and do not modify the playable instance. Use `-ServerLauncherRoot` only to point at an equivalent official 21.1.248 server installation.

The PowerShell preflight verifies the required launch arguments and every referenced library. The Python audit additionally checks ZIP integrity and the Minecraft server, BootstrapLauncher, and ModLauncher entry points. These are static launcher checks; only a completed smoke run with benchmark markers proves pack bootstrap, datapack loading, and chunk generation.

The isolated server does not blindly load client-only bootstrap services. Evidenced headless incompatibilities live in `scripts/worldgen_benchmark_server_mod_policy.json`; every exclusion needs a single matching local jar, a reason, and observed failure evidence. The current policy removes Sodium because its early rendering service loads LWJGL before NeoForge can apply ordinary distribution guards, and Barebones McQoy because its mod-construction subscriber loads a client GUI class on the dedicated-server distribution. Benchmark manifests record the policy hash and every omitted jar, so server-side content cannot disappear silently. Variant-specific omissions remain separate and are labelled as such.

In addition to timing data, every run records runtime acceptance evidence needed by the Infinite Domain reconciliation ledger. The controller records whether `lostcities`, `dungeons_arise`, and `dungeons_arise_seven_seas` were actually loaded by NeoForge; snapshots the live `STRUCTURE` and `STRUCTURE_SET` registries for both Arise namespaces; and inspects every generated benchmark chunk for valid structure starts, grouped by namespace. A tile is only probed once every one of its chunks is present at full status, which each `tile_completed` marker records as `loadedChunks`. `result.json` preserves those observations under `acceptance`.

KubeJS evaluates server scripts through a shared Rhino environment. The controller is isolated in an IIFE and uses function-scoped declarations in re-entered scheduled and guarded callbacks; `scripts/test_worldgen_benchmark.py` protects those compatibility choices. Three engine constraints have each cost a run, so they are worth restating. A `const` is never rebound when its block is re-entered: inside a loop it silently keeps the first iteration's value, and inside a `try` it raises "redeclaration of var" on the second entry, so declare in the function body and assign in the block. Where KubeJS remaps one of its own `kjs$` members onto a vanilla method name, the two overloads become ambiguous and Rhino refuses to dispatch; name the wanted one with its explicit signature, as the controller does for `getLevel(net.minecraft.resources.ResourceKey)`. And `runCommandSilent` returns void, so no command can report a result back to the controller: the tile gate reads the chunk source directly instead. Any `acceptance_probe_error` still invalidates probe-dependent conclusions even when the main generation marker completes.

## First smoke test

From the instance directory:

```powershell
.\scripts\run_worldgen_benchmark.ps1 -Variant baseline -Suite smoke
```

The smoke suite generates one 4x4 central-wasteland tile. It validates server startup, fixed-seed enforcement, datapack loading, automatic chunk generation, runtime acceptance instrumentation, log extraction, and shutdown. It is a plumbing test, not a performance or world-distribution conclusion.

## Reconciliation acceptance run

Use the standard suite for the retained evidence pass:

```powershell
.\scripts\run_worldgen_benchmark.ps1 -Variant baseline -Suite standard -Repetitions 1 -KeepRuntime
```

The resulting `result.json` is the machine-readable evidence record. Interpret the acceptance fields conservatively:

- `acceptance.loadedMods` proves the named mod was loaded in the fresh isolated NeoForge runtime.
- `acceptance.arise.<namespace>.runtimeRegistryReady` requires the mod to be loaded and to expose both structure and structure-set registrations. This proves that the mod's natural-generation registrations reached the live runtime; it does not prove that a particular fixed-seed region happened to contain one.
- `acceptance.arise.<namespace>.naturalGenerationObserved` becomes true only when at least one valid generated structure start from that namespace is actually present in the generated benchmark tiles. That is direct natural-generation observation for the tested world and regions.
- `acceptance.lostCities.runtimeLoadAccepted` proves Lost Cities was loaded while a new fixed-seed world successfully generated benchmark chunks without an acceptance-probe failure. It does not approve skyline quality, rotation, terrain seating, frequency, or visual distribution.
- `acceptance.structureStartsByNamespace` and each tile's `structureStartsByNamespace` retain the actual structure-start inventory observed in generated chunks.
- `acceptance.probeErrors` must be empty before any acceptance claim based on the instrumentation is made.

Lost Cities final new-world acceptance therefore still requires retained visual/distribution review of the kept runtime. Do not turn the headless load result into a visual-quality claim.

## Comparable measurements

Use at least three repetitions of the standard suite:

```powershell
.\scripts\run_worldgen_benchmark.ps1 -Variant baseline -Suite standard -Repetitions 3
.\scripts\run_worldgen_benchmark.ps1 -Variant optimized_heightmap -Suite standard -Repetitions 3
```

Each command creates a timestamped batch beneath `benchmark_runs/`. `summary.csv` reports median chunks per second. Individual `result.json` files retain per-region measurements and acceptance evidence.

For a comparison table spanning several batches:

```powershell
python .\scripts\analyze_worldgen_benchmark.py aggregate --root .\benchmark_runs --csv .\benchmark_runs\summary.csv --json .\benchmark_runs\summary.json
```

## Suites

- `smoke`: one 16-chunk central tile; verifies automation only.
- `terrain`: four 256-chunk tiles covering the mountain ring, east/west abyssal corridors, and an unaffected northern ocean control.
- `standard`: seven 256-chunk tiles covering the central wasteland, mountain ring, east/west outer continents, both abyssal corridors, and the northern ocean control.

The regions follow the authoritative coordinates already used by the gradient-ocean validation documentation. Each tile is at most 256 chunks because that is Minecraft's force-load limit.

## Variants

- `baseline`: current configuration.
- `optimized_heightmap`: enables Lost Cities' alternate heightmap algorithm.
- `height_sample_6`: raises Lost Cities' height sampling grid from 3 to 6.
- `no_adjacent_avoidance`: disables adjacent structure and village avoidance.
- `no_abyssal_structures`: removes only Abyssal structure sets from the isolated datapack.
- `no_custom_structures`: removes all Infinite Domain structure sets from the isolated datapack.
- `no_gradient_ocean`: omits the external gradient-ocean datapack.
- `no_lostcities`: omits the Lost Cities jar from the isolated mod directory.
- `no_lostcities_assets`: removes the pack's whole `kubejs/data/infinite_domain/lostcities` tree.
- `no_lostcities_parts`: removes only the `parts` subtree.

The last two leave the Lost Cities jar loaded while taking away the assets its worldstyle and citystyles reference, so a run is only useful for the `serverPhases` timings taken before generation. Do not read city quality, structure counts or acceptance fields from them.

These are diagnostic isolation variants, not proposed production settings. A faster result identifies where to investigate; it does not automatically authorize the corresponding gameplay change.

## What the tile timer can and cannot measure (2026-09-01)

A tile is timed between the forceload command and the poll that first observes every chunk present. The controller schedules that poll in server ticks, and a tick that is itself generating chunks can run for seconds, so the poll interval sets the resolution of the whole measurement.

Until 2026-09-01 that interval was 20 ticks, and every recorded tile — five runs, five different pack revisions — reported `polls: 1`. A tile accepted on its first poll was never observed running: its `elapsedMs` is the time 20 ticks took, which bounds generation from above and does not measure it. That is how a 16-chunk smoke tile came to report 0.111 chunks/s in `summary.csv` while vanilla generated the spawn area of the same world in 46 seconds.

The interval is now one tick, and the analyzer records the resolution it actually achieved:

- `tiles[].measurementSaturated` — this tile was accepted on its first poll.
- `saturatedTiles`, `measurementQuality` — `measured`, `partial`, or `unmeasured` for the run.
- `aggregate` refuses to compute `speedupVsBaseline` unless both the variant and its baseline are `measured`, and `summary.csv` carries the quality column.

A tile still has to be large enough to span several ticks. The smoke suite's 16 chunks is not, and never was: use it for plumbing only, exactly as this document already said, and read the two phase timings below instead.

## Phase timings

Vanilla times two phases itself, independently of the controller and of the tick loop, and the analyzer harvests both from `latest.log` into `result.json` under `serverPhases`:

- `levelPrepMs` — `Preparing level` to `Preparing start region`. This is **dimension construction**, not the server resource reload: recipes, loot and tags finish earlier (`Loaded 18041 recipes` lands about nine seconds *before* `Preparing level`). What happens inside it is the worldgen dynamic-registry load — biomes, placed features, structures, structure sets, and modded registries such as Lost Cities' `parts` and `buildings` — followed by biome-source and chunk-generator construction and the per-generator feature sort, for every dimension the pack defines. Four baseline runs spanned 179.5–183.6 s, a 2.3% range, which makes it the lowest-noise number this harness produces.
- `spawnPrepMs` — vanilla's own fixed spawn-area generation timing. Baselines spanned 44.0–46.5 s (5.7%).

Roughly 94% of `levelPrepMs` is a single block with no log output at all — 166 s of 177 s in the 2026-09-01 reference run. Nothing inside it is attributable from logs, so narrowing it needs either a profiler on the isolated server or the differential variants below. The ~11 s tail after it is Biolith rejecting about ten dimensions it has no dimension type for, at ~1.4 s each.

### What that block is not (2026-09-01)

Two candidates are measured out, which matters because both would have implied the pack simply carries too much custom content:

- **Not the Lost Cities asset registries.** They are by far the largest body of worldgen data the pack ships — 15,349 JSON files, 12,550 of them `parts`, about 69 MB. The `no_lostcities_assets` variant removes all of it, and both repetitions came in **above** the baseline band rather than below it: `levelPrepMs` 186.4 s and 192.0 s against a 177.1–183.6 s baseline, with `spawnPrepMs` mid-band at 45.1 s and 46.8 s. Removing the pack's largest body of custom worldgen data buys nothing. Do not infer otherwise from log ordering — with the assets gone, the Sable overworld line moves to within 16 ms of `Preparing level` and the silent block simply relocates after it, which looks like a win and is not one.
- **Not dead or unreferenced data.** Every one of the 12,550 `parts` is reachable from a building, multibuilding or citystyle; the orphan count is zero. Three `structure_set` files do carry an empty `structures` list (`hive_world_district`, `deep_sea/akula_wreck_aft`, `deep_sea/akula_wreck_forward`), but a set with no structures is dropped from `possibleStructureSets` before generation, so they cost nothing at runtime and are left in place.

The remaining candidates inside the block are the biome, placed-feature and structure registry decode (the Isekai scan reports 577 placed features and 483 structure placements), the per-generator feature sort, and per-dimension construction across the ~15 dimensions the pack defines. Separating those needs a profiler; log-derived attribution has already been wrong twice here.

### `optimizedHeightmap` is not a win, and how the session nearly said it was (2026-09-02)

Run the variants **interleaved**, never in blocks. This machine drifts faster as a session goes on — six runs in time order gave `spawnPrepMs` 51.2, 45.1, 44.8, 39.9, 43.8, 41.3 s, about 20% end to end, which is far larger than the effect being looked for.

Three baselines followed by three `optimized_heightmap` runs made the variant look 11.6% faster on `spawnPrepMs` and below the baseline minimum. It was drift. The tell was that `levelPrepMs` improved by a similar 9% in the same runs, and `optimizedHeightmap` is a Lost Cities chunk-generation setting that cannot affect dimension construction. When an unrelated metric moves with the one under test, suspect the machine.

The drift-controlled comparison is a single adjacent pair: `optimized_heightmap` at 09:12 gave 43,751 ms, `baseline` at 09:21 gave 41,263 ms — the **baseline 5.7% faster than the variant**. Pooled ranges overlap completely (baseline 41.3–51.2 s, variant 39.9–43.8 s). There is no measurable benefit, so the setting stays `false` and the pack avoids Lost Cities' own warning that it "might not be 100% compatible with some other terrain generation mods" — which matters here, given custom noise settings, custom density functions and an `isekai_api` biome source.

This is what interpretation rule 2 is for. Honour it: baseline, variant, baseline.

### The `avoidStructures` list is not a per-chunk cost

`config/lostcities-server.toml` lists 74 structures to keep cities away from, and 44 of the 69 `infinite_domain` entries name structures that appear in no `structure_set` and therefore cannot generate at all. That looks like an obvious pruning target and is not one.

Lost Cities holds the list as a `HashSet<ResourceLocation>` (`Config.cacheAvoidedStructures`) and `StructureAvoidance` walks the structures *actually referenced in a chunk* — the `Map.Entry<Structure, LongSet>` from `getChunkWithStructureReferences` — testing each against that set, behind a `ConcurrentMap<FootprintKey, FootprintDecision>` cache. Cost is therefore O(structures present), with an O(1) lookup each, and is **independent of how long the list is**. Adding or removing entries changes nothing measurable.

Keep the inert 44. They are correct forward declarations: those structures not generating is a separate known defect, and pruning the list would silently drop protection that has to apply once that defect is fixed.

What *does* scale in this path is `avoidStructuresAdjacent`, which multiplies the chunk-reference lookups by nine. The `no_adjacent_avoidance` variant measures that, but it is diagnostic only — turning it off lets cities overlap the Old World sites the list exists to protect.

Both are durations only. The spawn area's chunk count is deliberately not inferred: `LoggerChunkProgressListener` throttles its progress lines, so the log cannot support a chunks-per-second figure.

Read them together. They measure unrelated work — data loading and chunk generation — so a change that inflates both by a similar proportion is machine contention, not a worldgen result. A run during concurrent analysis on this machine showed `levelPrepMs` 281.8 s with `spawnPrepMs` 70.1 s, both about 55% above baseline: nothing to do with the pack. Run benchmarks with the machine otherwise idle.

## Run time and the hard cap

A smoke run on this pack takes about **7 minutes** — roughly 2 for mod loading, 3 for dimension construction, 1 for generation, plus staging and shutdown. Budget accordingly: three repetitions is a little over 20 minutes, and the six-run comparison above took 45.

Every run is bounded by `-RunTimeoutMinutes` (default 25). The server is started detached and waited on with that deadline; on expiry it is killed, the run throws, the batch stops, and the runtime is kept for diagnosis. Before this existed the only timeout was `tileTimeoutSeconds` inside the KubeJS controller, which protects a run that already reached chunk generation and does nothing for a JVM that wedges during mod loading or the three-minute construction block — that run would have held the batch indefinitely.

Two notes for anyone editing that launch path. `Start-Process -PassThru` on Windows PowerShell 5.1 returns a process whose `ExitCode` stays `$null` even after `WaitForExit`, so `EnableRaisingEvents` must be set before the process exits or every run fails with `exited with code .`; and `Start-Process` cannot merge both streams into one file, so stderr lands in `server-console.err.log` and is appended to `server-console.log` afterwards.

A run killed by the cap, or failed by a launcher bug, may still have produced a complete `latest.log`. Check for the `benchmark_completed` marker and re-run the analyzer against it before discarding the run:

```powershell
python .\dev\scripts\analyze_worldgen_benchmark.py analyze --log <run>\latest.log --manifest <run>\manifest.json --output <run>\result.json
```

## Interpretation rules

1. Compare only runs with the same seed, suite, heap size, pack revision, and configuration fingerprint except for the intentional variant.
2. Run the baseline before and after a long experiment series to detect thermal throttling or background-load drift.
3. Use medians from at least three runs. Do not promote a change based on the smoke suite or one run.
4. Treat changes below 5% as noise until confirmed with five or more alternating runs.
5. Reject a performance win if worldgen logs contain registry errors, failed datapacks, timeouts, missing regions, or acceptance-probe errors.
6. Follow performance testing with visual and gameplay regression checks; the benchmark proves throughput and retained runtime facts, not terrain aesthetics.
7. For Arise / Seven Seas, distinguish registry readiness from observed natural placement. Only `naturalGenerationObserved: true` is direct placement evidence for the generated test region.
8. For Lost Cities, retain the generated runtime and inspect representative city/wasteland transitions before setting visual/distribution acceptance to complete.

Use `-KeepRuntime` when the generated world or complete server directory is needed for inspection. Otherwise only the manifest, logs, results, and summaries are retained.
