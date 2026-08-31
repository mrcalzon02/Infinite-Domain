from __future__ import annotations

import json
import tempfile
from pathlib import Path

from analyze_worldgen_benchmark import analyze, validate_matrix


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    validate_matrix(root / "scripts" / "worldgen_benchmark_matrix.json")
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
                "seed": "-7046029254386353131", "plannedChunks": 16,
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
        assert result["completedChunks"] == 16
        assert result["chunksPerSecond"] == 8.0
        assert result["tileP95Ms"] == 2000
    print("Worldgen benchmark self-test passed")


if __name__ == "__main__":
    main()
