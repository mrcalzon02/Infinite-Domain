from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "dev/docs" / "wasteland-site-manifest.json"
REPORT = ROOT / "dev/docs" / "structure-performance-budget.json"

BUDGETS = {
    "placed_blocks": 180_000,
    "palette_states": 128,
    "compressed_nbt_bytes": 2_000_000,
    "footprint_chunks": 36,
}


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    failures = []
    records = {}
    for name, metadata in manifest["structures"].items():
        width, height, depth = metadata["size"]
        nbt = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland" / f"{name}.nbt"
        metrics = {
            "size": [width, height, depth],
            "placed_blocks": metadata["placed_blocks"],
            "palette_states": metadata["palette_states"],
            "compressed_nbt_bytes": nbt.stat().st_size,
            "footprint_chunks": math.ceil(width / 16) * math.ceil(depth / 16),
        }
        issues = []
        for metric, limit in BUDGETS.items():
            if metrics[metric] > limit:
                issues.append(f"{metric} {metrics[metric]} exceeds {limit}")
        metrics["issues"] = issues
        metrics["static_budget_passed"] = not issues
        failures.extend(f"{name}: {issue}" for issue in issues)
        records[name] = metrics

    family_density = {
        name: {
            "spacing_chunks": data["spacing_chunks"],
            "separation_chunks": data["separation_chunks"],
            "theoretical_starts_per_1024_square_before_biome_filter": round((64 / data["spacing_chunks"]) ** 2, 3),
        }
        for name, data in manifest["families"].items()
    }
    report = {
        "scope": "Static/precomputed structure placement cost. This does not substitute for timed runtime pregeneration.",
        "budgets": BUDGETS,
        "structures_profiled": len(records),
        "static_budget_passed": not failures,
        "failures": failures,
        "largest_by_placed_blocks": sorted(records, key=lambda name: records[name]["placed_blocks"], reverse=True)[:10],
        "largest_by_compressed_nbt": sorted(records, key=lambda name: records[name]["compressed_nbt_bytes"], reverse=True)[:10],
        "family_density": family_density,
        "runtime_benchmark_status": "pending_in_game_representative_region_pregeneration",
        "structures": records,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if failures:
        raise SystemExit("Static structure performance budget failed:\n- " + "\n- ".join(failures))
    print(f"Profiled {len(records)} structures; all pass static placement, palette, NBT and footprint budgets")


if __name__ == "__main__":
    main()
