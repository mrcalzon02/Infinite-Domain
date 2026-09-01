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

In addition to timing data, every run records runtime acceptance evidence needed by the Infinite Domain reconciliation ledger. The controller records whether `lostcities`, `dungeons_arise`, and `dungeons_arise_seven_seas` were actually loaded by NeoForge; snapshots the live `STRUCTURE` and `STRUCTURE_SET` registries for both Arise namespaces; and inspects every generated benchmark chunk for valid structure starts, grouped by namespace. `result.json` preserves those observations under `acceptance`.

KubeJS evaluates server scripts through a shared Rhino environment. The controller is isolated in an IIFE and uses function-scoped declarations in re-entered scheduled and guarded callbacks; `scripts/test_worldgen_benchmark.py` protects those compatibility choices. Any `acceptance_probe_error` still invalidates probe-dependent conclusions even when the main generation marker completes.

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

These are diagnostic isolation variants, not proposed production settings. A faster result identifies where to investigate; it does not automatically authorize the corresponding gameplay change.

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
