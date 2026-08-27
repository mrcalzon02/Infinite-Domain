#!/usr/bin/env python3
"""Spike removal helper for the Hive World.

Endgame checkpoint EG-P01-S06-C0023. Procedure: docs/endgame/test-strategy.md section 9.

Lists (default) or deletes (--apply) every file that belongs to the Phase 1 spike, so
the dimension can be removed without touching any other content. Also writes the
current manifest to docs/endgame/hive-world-path-manifest.txt.

    python scripts/endgame/remove_hive_world_spike.py          # list + refresh manifest
    python scripts/endgame/remove_hive_world_spike.py --apply  # actually delete

After --apply: relaunch a fresh client and a dedicated server and confirm the
Overworld / Nether / End load unchanged with no registry or datapack errors and no
orphaned infinite_domain:hive_world entry in existing level data (C0010 section 9).
"""
from __future__ import annotations

import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]

# Every path the spike owns. Globs are expanded relative to REPO.
SPIKE_GLOBS = [
    "kubejs/data/infinite_domain/dimension/hive_world.json",
    "kubejs/data/infinite_domain/dimension_type/hive_world.json",
    "kubejs/data/infinite_domain/worldgen/noise_settings/hive_world.json",
    "kubejs/data/infinite_domain/worldgen/biome/hive_world_*.json",
    "kubejs/data/infinite_domain/worldgen/configured_feature/hive_world_*.json",
    "kubejs/data/infinite_domain/worldgen/placed_feature/hive_world_*.json",
    "kubejs/data/infinite_domain/worldgen/density_function/hive_world_*.json",
    "kubejs/data/infinite_domain/function/hive_world/*.mcfunction",
    "kubejs/data/infinite_domain/advancement/hive_world/*.json",
    "kubejs/server_scripts/hive_world_expedition.js",
    "kubejs/server_scripts/hive_world_atmosphere_proto.js",
    "kubejs/startup_scripts/hive_world_items.js",
    "scripts/endgame/generate_hive_world_noise.py",
    "scripts/endgame/generate_hive_world_biomes.py",
    "scripts/endgame/generate_hive_world_acid.py",
]

# Paths that keep the dimension out of the game but are NOT deleted by --apply
# (they are docs / tooling that should outlive the spike):
KEEP_NOTE = [
    "scripts/endgame/validate_hive_world_smoke.py  (repurposed for the real dimension)",
    "docs/endgame/**  (all contracts and gate evidence)",
]

MANIFEST = REPO / "docs/endgame/hive-world-path-manifest.txt"


def resolve() -> list[pathlib.Path]:
    found: list[pathlib.Path] = []
    for g in SPIKE_GLOBS:
        if "*" in g:
            found.extend(sorted(REPO.glob(g)))
        else:
            p = REPO / g
            if p.is_file():
                found.append(p)
    return found


def main() -> int:
    apply = "--apply" in sys.argv
    files = resolve()

    lines = [
        "# Hive World Phase 1 spike - path manifest (EG-P01-S06-C0023)",
        "# Regenerate: python scripts/endgame/remove_hive_world_spike.py",
        f"# {len(files)} spike files as of this run",
        "",
    ]
    lines += [str(p.relative_to(REPO)).replace("\\", "/") for p in files]
    lines += ["", "# kept (not deleted by --apply):"]
    lines += [f"#   {k}" for k in KEEP_NOTE]
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"manifest -> {MANIFEST.relative_to(REPO)} ({len(files)} files)")

    for p in files:
        print(("DELETE " if apply else "would remove ") + str(p.relative_to(REPO)).replace("\\", "/"))
        if apply:
            p.unlink()

    if apply:
        print("\nspike files removed. Now relaunch a fresh client + dedicated server and")
        print("verify Overworld/Nether/End load unchanged (docs/endgame/test-strategy.md section 9).")
    else:
        print("\ndry run - pass --apply to delete. Empty parent dirs are left for git to prune.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
