"""Repair path resolution after the development archive moved under `dev/`.

Every audit and generator script was authored when it lived at `<instance>/scripts/`,
so `Path(__file__).resolve().parents[1]` resolved to the instance root. The archive
now lives at `<instance>/dev/`, which shifts that anchor down one level and silently
repoints every pack-data path at a directory that does not exist.

Two mechanical corrections restore the original meaning:

1. Bump the `parents[N]` anchor by one so `ROOT` again names the instance root.
2. Prefix `dev/` onto the path literals whose first segment moved into the archive,
   so archive-owned reads and writes follow the content.

Run with no arguments for a dry run; pass --apply to write.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

DEV_ROOT = Path(__file__).resolve().parents[1]

# Root-level names that moved into `dev/`. Everything else (kubejs, config, mods,
# datapacks, saves, logs, build, ROOT_tools, ...) stayed at the instance root.
ARCHIVE_SEGMENTS = (
    "docs",
    "old_world_narrative",
    "structure_library",
    "scripts",
    "packdev",
    "tools",
    "schematics",
    "Start",
    "CODEX_STRUCTURE_PIPELINE.md",
    "PROJECT_INDEX.md",
    "README.md",
    "REPOSITORY_SCOPE.md",
    "run_codex_structure_pipeline.ps1",
    "structure-geometry-lint-report.json",
)

# Only these identifiers name the instance root. `\b` keeps OUTPUT_ROOT,
# REVIEW_ROOT and friends out of the rewrite.
ROOT_VARS = ("ROOT", "REPO", "REPOSITORY")

ANCHOR_RE = re.compile(
    r"^(?P<var>" + "|".join(ROOT_VARS) + r") = Path\(__file__\)\.resolve\(\)\.parents\[(?P<depth>\d+)\]",
    re.MULTILINE,
)

LITERAL_RE = re.compile(
    r"\b(?P<var>" + "|".join(ROOT_VARS) + r")(?P<sep> / )(?P<quote>[\"'])"
    r"(?P<seg>" + "|".join(re.escape(s) for s in ARCHIVE_SEGMENTS) + r")"
    r"(?=[\"'/])"
)


def repair(source: str) -> tuple[str, int, int]:
    """Return (new_source, anchors_bumped, literals_prefixed)."""
    anchors = 0

    def bump(match: re.Match[str]) -> str:
        nonlocal anchors
        anchors += 1
        depth = int(match.group("depth")) + 1
        return f"{match.group('var')} = Path(__file__).resolve().parents[{depth}]"

    source = ANCHOR_RE.sub(bump, source)

    literals = 0

    def prefix(match: re.Match[str]) -> str:
        nonlocal literals
        literals += 1
        q = match.group("quote")
        return f"{match.group('var')}{match.group('sep')}{q}dev/{match.group('seg')}"

    source = LITERAL_RE.sub(prefix, source)
    return source, anchors, literals


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="write changes to disk")
    args = parser.parse_args()

    targets = sorted(DEV_ROOT.glob("scripts/**/*.py"))
    targets = [p for p in targets if "__pycache__" not in p.parts]
    targets = [p for p in targets if p.resolve() != Path(__file__).resolve()]

    changed = 0
    total_anchors = 0
    total_literals = 0
    for path in targets:
        original = path.read_text(encoding="utf-8")
        # This migration is one-shot: bumping an anchor that already points at
        # the instance root would walk past it. A file that already reads from
        # dev/ has been migrated, so leave it alone.
        already_migrated = 'dev/' in original and 'parents[1]' not in original
        if already_migrated:
            continue
        updated, anchors, literals = repair(original)
        if updated == original:
            continue
        changed += 1
        total_anchors += anchors
        total_literals += literals
        rel = path.relative_to(DEV_ROOT.parent).as_posix()
        print(f"{'apply' if args.apply else 'would fix'} {rel}: anchors={anchors} literals={literals}")
        if args.apply:
            path.write_text(updated, encoding="utf-8")

    verb = "Repaired" if args.apply else "Would repair"
    print(
        f"\n{verb} {changed} of {len(targets)} archive scripts "
        f"({total_anchors} root anchors bumped, {total_literals} archive path literals prefixed)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
