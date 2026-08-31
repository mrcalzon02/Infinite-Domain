# Fixed-seed world-generation benchmark

This regimen measures fresh chunk generation without opening a client or manually creating a world. Every run starts an isolated NeoForge dedicated server, creates the same world from seed `-7046029254386353131`, generates the same chunk tiles in the same order, records timings, stops cleanly, and removes its disposable runtime after successful analysis.

The ordinary instance, `saves`, configurations, and mod jars are never modified. A failed run keeps its isolated runtime for diagnosis.

## First smoke test

From the instance directory:

```powershell
.\scripts\run_worldgen_benchmark.ps1 -Variant baseline -Suite smoke
```

The smoke suite generates one 4x4 central-wasteland tile. It validates server startup, fixed-seed enforcement, datapack loading, automatic chunk generation, log extraction, and shutdown. It is a plumbing test, not a performance conclusion.

## Comparable measurements

Use at least three repetitions of the standard suite:

```powershell
.\scripts\run_worldgen_benchmark.ps1 -Variant baseline -Suite standard -Repetitions 3
.\scripts\run_worldgen_benchmark.ps1 -Variant optimized_heightmap -Suite standard -Repetitions 3
```

Each command creates a timestamped batch beneath `benchmark_runs/`. `summary.csv` reports median chunks per second. Individual `result.json` files retain per-region measurements.

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
5. Reject a performance win if worldgen logs contain registry errors, failed datapacks, timeouts, or missing regions.
6. Follow performance testing with visual and gameplay regression checks; the benchmark proves throughput, not terrain correctness.

Use `-KeepRuntime` when the generated world or complete server directory is needed for inspection. Otherwise only the manifest, logs, results, and summaries are retained.
