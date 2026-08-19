"""Classify current runtime recipe warnings as pack-authored overlays or upstream content."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "logs/latest.log"
OUT = ROOT / "docs/custom-content-audit/runtime-recipe-warnings.csv"


def main() -> int:
    text = LOG.read_text(encoding="utf-8", errors="replace")
    recipe_pattern = re.compile(r"(?:parse|scan) recipe '?([a-z0-9_.-]+:[a-z0-9_./-]+)(?:\[[^\]]+\])?'?", re.IGNORECASE)
    rows: list[dict] = []
    seen: set[str] = set()
    for line in text.splitlines():
        match = recipe_pattern.search(line)
        if not match:
            continue
        recipe_id = match.group(1).lower()
        if recipe_id in seen:
            continue
        seen.add(recipe_id)
        namespace, path = recipe_id.split(":", 1)
        overlay = ROOT / "kubejs/data" / namespace / "recipe" / f"{path}.json"
        rows.append(
            {
                "recipe_id": recipe_id,
                "owner": "PACK_OVERLAY" if overlay.is_file() else "UPSTREAM_MOD",
                "overlay_path": overlay.relative_to(ROOT).as_posix() if overlay.is_file() else "",
                "log_line": line,
            }
        )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]) if rows else ["recipe_id", "owner", "overlay_path", "log_line"])
        writer.writeheader()
        writer.writerows(rows)
    pack = [row for row in rows if row["owner"] == "PACK_OVERLAY"]
    upstream = [row for row in rows if row["owner"] == "UPSTREAM_MOD"]
    print(f"Runtime recipe warnings: {len(rows)} unique; pack overlays={len(pack)}, upstream={len(upstream)}.")
    for row in pack:
        print(f"PACK {row['recipe_id']} -> {row['overlay_path']}")
    return 1 if pack else 0


if __name__ == "__main__":
    raise SystemExit(main())
