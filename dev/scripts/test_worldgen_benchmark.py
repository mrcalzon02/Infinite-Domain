from __future__ import annotations

import json
import re
import tempfile
from pathlib import Path

from analyze_worldgen_benchmark import analyze, validate_matrix


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    validate_matrix(root / "scripts" / "worldgen_benchmark_matrix.json")
    launcher_source = (root / "scripts" / "run_worldgen_benchmark.ps1").read_text(
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
    assert "var loaded = {}" in controller_source
    assert "var snapshotRegistryKeys = Java.loadClass" in controller_source
    assert "var startRegistryKeys = Java.loadClass" in controller_source
    assert controller_source.count("var tile = config.tiles[tileIndex]") == 1
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
                "chunks": 16, "elapsedMs": 2000, "chunksPerSecond": 8.0,
            },
            {
                "event": "benchmark_completed", "runId": "self-test-r01", "generationMs": 2000,
                "wallClockMs": 7000, "chunksPerSecond": 8.0,
            },
        ]
        log = "\n".join(
            f"[00:00:00] [Server thread/INFO] [KubeJS/]: [ID-WORLDGEN-BENCH] {json.dumps(marker)}"
            for marker in markers
        )
        (temp / "latest.log").write_text(log, encoding="utf-8")
        result = analyze(temp / "latest.log", temp / "manifest.json")
        assert result["status"] == "complete"
        assert result["seed"] == "-7046029254386353131"
        assert result["seedValidation"] == "rhino_double_equivalent"
        assert result["completedChunks"] == 16
        assert result["chunksPerSecond"] == 8.0
        assert result["tileP95Ms"] == 2000
    print("Worldgen benchmark self-test passed")


if __name__ == "__main__":
    main()
