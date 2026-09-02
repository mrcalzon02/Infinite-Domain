from __future__ import annotations

import json
import re
import tempfile
from pathlib import Path

from analyze_worldgen_benchmark import PREFIX, analyze, validate_matrix


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    matrix_path = root / "dev/scripts" / "worldgen_benchmark_matrix.json"
    validate_matrix(matrix_path)
    # Tile timing is only as fine as the poll that observes completion, and a
    # tick spent generating chunks can itself run for seconds. At 20 ticks every
    # recorded tile was accepted on its first poll, so no run ever measured
    # generation. One tick is the finest bracket this design can offer.
    matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    assert matrix["defaults"]["pollIntervalTicks"] == 1, (
        "a coarser poll interval silently turns tile timings back into upper bounds"
    )
    launcher_source = (root / "dev/scripts" / "run_worldgen_benchmark.ps1").read_text(
        encoding="utf-8"
    )
    assert "$benchmarkWorldName = [string]$matrix.worldName" in launcher_source
    assert "level-name=$benchmarkWorldName" in launcher_source
    assert "Join-Path $benchmarkWorldName 'datapacks'" in launcher_source
    assert "level-name=world" not in launcher_source
    assert "server-port=0" in launcher_source
    controller_source = (
        root / "kubejs" / "server_scripts" / "worldgen_benchmark.js"
    ).read_text(encoding="utf-8")
    assert "java.lang.Runtime" not in controller_source
    assert "maxHeapBytes" not in controller_source
    assert ".reduce(" not in controller_source
    assert "plannedChunks += Number(config.tiles[plannedTileIndex].widthChunks)" in controller_source
    assert "const plannedTile" not in controller_source
    assert controller_source.lstrip().startswith("// Headless")
    assert "(() => {" in controller_source and controller_source.rstrip().endswith("})()")
    assert "Platform.isLoaded(modId)" in controller_source
    assert "net.neoforged.fml.ModList" not in controller_source
    # The three acceptance probes must declare at function scope. A `var` inside
    # their try blocks hoists out and collides with the binding left by the
    # previous entry when a scheduled callback re-enters, which Rhino reports as
    # "redeclaration of var" - silently zeroing every probe-dependent result.
    assert "let loaded = {}" in controller_source
    assert "let snapshotRegistryKeys, snapshotAccess" in controller_source
    assert "let startRegistryKeys, startResourceKey" in controller_source
    for probe in ("worldgenBenchmarkModSnapshot",
                  "worldgenBenchmarkRegistrySnapshot",
                  "worldgenBenchmarkStructureStarts"):
        start = controller_source.index("function " + probe)
        body = controller_source[start:controller_source.index(chr(10) + "function ", start + 1)]
        assert "var " not in body, probe + " reintroduced a try-block var"
    assert controller_source.count("var tile = config.tiles[tileIndex]") == 1
    # KubeJS' Rhino never gives a `const` a fresh binding when its block is
    # re-entered: in a loop body it silently keeps the first iteration's value, and
    # in a try body it raises "redeclaration of var" on the second entry. Only
    # function bodies rebind, so every const must sit directly in one.
    body_indents: list[int] = []
    for number, line in enumerate(controller_source.splitlines(), 1):
        stripped = line.strip()
        if not stripped:
            continue
        indent = len(line) - len(line.lstrip())
        while body_indents and indent < body_indents[-1]:
            body_indents.pop()
        if stripped.startswith("const "):
            assert body_indents and indent == body_indents[-1], (
                f"controller line {number} declares a const inside a re-entered block, "
                f"which this engine does not rebind: {stripped}"
            )
        if stripped == "(() => {":
            body_indents.append(indent)
        elif stripped.endswith("{") and (
            stripped.startswith("function ") or "=> {" in stripped or "function (" in stripped
        ):
            body_indents.append(indent + 4)
    assert "var completionElapsedMs" in controller_source
    declarations = re.findall(r"\b(?:const|let|var)\s+([A-Za-z_$][A-Za-z0-9_$]*)", controller_source)
    duplicates = sorted(name for name in set(declarations) if declarations.count(name) > 1)
    assert duplicates == [], f"Rhino-incompatible duplicate controller declarations: {duplicates}"
    with tempfile.TemporaryDirectory() as temporary:
        temp = Path(temporary)
        manifest = {
            "runId": "self-test-r01",
            "batchId": "self-test",
            "repetition": 1,
            "seed": "-7046029254386353131",
            "configurationFingerprint": "abc123",
        }
        (temp / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        markers = [
            {
                "event": "benchmark_started", "runId": "self-test-r01", "variant": "baseline",
                "suite": "smoke", "worldName": "Infinite Domain - Worldgen Benchmark",
                "seed": "-7046029254386353000", "plannedChunks": 16,
            },
            {
                "event": "tile_completed", "runId": "self-test-r01", "tile": "central_wasteland_smoke",
                "chunks": 16, "elapsedMs": 2000, "chunksPerSecond": 8.0, "polls": 9,
            },
            {
                "event": "benchmark_completed", "runId": "self-test-r01", "generationMs": 2000,
                "wallClockMs": 7000, "chunksPerSecond": 8.0,
            },
        ]
        log = "\n".join(
            [
                '[01Sep2026 11:33:56.090] [Server thread/INFO] [DedicatedServer/]: '
                'Preparing level "Infinite Domain - Worldgen Benchmark"',
                "[01Sep2026 11:34:16.090] [Server thread/INFO] [MinecraftServer/]: "
                "Preparing start region for dimension minecraft:overworld",
                "[01Sep2026 11:35:01.855] [Server thread/INFO] [ChunkProgressListener/]: "
                "Time elapsed: 45765 ms",
            ]
            + [
                f"[01Sep2026 11:35:02.000] [Server thread/INFO] [KubeJS/]: {PREFIX}{json.dumps(marker)}"
                for marker in markers
            ]
        )
        (temp / "latest.log").write_text(log, encoding="utf-8")
        result = analyze(temp / "latest.log", temp / "manifest.json")
        assert result["status"] == "complete"
        assert result["seed"] == "-7046029254386353131"
        assert result["seedValidation"] == "rhino_double_equivalent"
        assert result["completedChunks"] == 16
        assert result["chunksPerSecond"] == 8.0
        assert result["tileP95Ms"] == 2000
        assert result["measurementQuality"] == "measured"
        assert result["saturatedTiles"] == 0
        assert result["tiles"][0]["measurementSaturated"] is False
        # Vanilla times these two phases itself, independently of the tick loop
        # the controller rides on, so they survive a saturated tile.
        assert result["serverPhases"]["levelPrepMs"] == 20_000
        assert result["serverPhases"]["spawnPrepMs"] == 45_765

        # A tile accepted on its first poll must never be reported as a rate.
        saturated = json.loads(json.dumps(markers))
        saturated[1]["polls"] = 1
        (temp / "saturated.log").write_text(
            "\n".join(
                f"[01Sep2026 11:35:02.000] [Server thread/INFO] [KubeJS/]: {PREFIX}{json.dumps(marker)}"
                for marker in saturated
            ),
            encoding="utf-8",
        )
        degraded = analyze(temp / "saturated.log", temp / "manifest.json")
        assert degraded["measurementQuality"] == "unmeasured"
        assert degraded["saturatedTiles"] == 1
        assert degraded["tiles"][0]["measurementSaturated"] is True
    print("Worldgen benchmark self-test passed")


if __name__ == "__main__":
    main()
