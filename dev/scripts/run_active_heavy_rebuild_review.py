#!/usr/bin/env python3
"""[SYSTEM REPORT] Render the first unresolved visual gate for the active OWS target.

This is execution plumbing only. It NEVER creates a visual approval decision and
NEVER promotes schematic quality. It discovers the newest authored review
renderer for the active target, runs it only when that revision's persisted
artifact is absent, and optionally runs a matching image-level analyzer.

Gate D is intentionally excluded: final synchronized Gate-D rendering belongs to
the static shipping workflow after authoritative NBT regeneration.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
STATE_PATH = ROOT / "old_world_narrative" / "registry" / "heavy_rebuild_state.json"
VISUAL_ROOT = ROOT / "old_world_narrative" / "reviews" / "heavy_rebuild" / "visual"


def _run(*args: str) -> None:
    command = [sys.executable, *args]
    print("+", " ".join(command))
    subprocess.run(command, cwd=ROOT, check=True)


def _passed(status: str) -> bool:
    value = str(status or "").lower()
    return value.startswith("passed") or value in {
        "complete",
        "reviewed_rebuild_required",
        "peak_quality_static_approved",
    }


def _declared_renderer_revision(path: Path, default: int) -> int:
    """Resolve a renderer's authored output revision without renaming its source file.

    Older renderers used an unsuffixed filename for r1. Newer repair passes may keep
    that authoritative filename while advancing OUTPUT_DIR to r2/r3. Treating every
    unsuffixed renderer as r1 causes the dispatcher to mistake an old persisted r1
    artifact for the current repaired candidate and permanently block rerendering.
    """
    try:
        source = path.read_text(encoding="utf-8")
    except OSError:
        return default

    explicit = re.search(r"(?m)^\s*REVIEW_REVISION\s*=\s*(\d+)\s*$", source)
    if explicit:
        return int(explicit.group(1))

    output_dir = re.search(
        r"(?m)^\s*OUTPUT_DIR\s*=.*?/\s*[\"']r(\d+)[\"']\s*$",
        source,
    )
    if output_dir:
        return int(output_dir.group(1))

    return default


def _revisioned_renderer(target_slug: str, stem: str) -> tuple[int, Path] | None:
    """Return newest authored renderer, honoring its declared output revision."""
    base = SCRIPTS / f"render_{target_slug}_{stem}.py"
    candidates: list[tuple[int, Path]] = []
    if base.is_file():
        candidates.append((_declared_renderer_revision(base, 1), base))
    pattern = f"render_{target_slug}_{stem}_r*.py"
    for path in SCRIPTS.glob(pattern):
        match = re.search(r"_r(\d+)\.py$", path.name)
        if match:
            candidates.append((int(match.group(1)), path))
    if not candidates:
        return None
    return max(candidates, key=lambda item: item[0])


def _gate_artifact(target: str, gate_dir: str, revision: int, filename: str) -> Path:
    return VISUAL_ROOT / target / gate_dir / f"r{revision}" / filename


def _render_revisioned_gate(
    *,
    target: str,
    target_slug: str,
    script_stem: str,
    gate_dir: str,
    manifest_name: str,
    analyzer_name: str | None = None,
) -> bool:
    resolved = _revisioned_renderer(target_slug, script_stem)
    if resolved is None:
        print(f"No authored renderer yet for {target} {script_stem}; review remains blocked.")
        return False
    revision, renderer = resolved
    manifest = _gate_artifact(target, gate_dir, revision, manifest_name)
    if manifest.is_file():
        print(f"{target} {gate_dir} r{revision} already rendered; manual review remains authoritative.")
        return False
    _run(str(renderer.relative_to(ROOT)))
    if not manifest.is_file():
        raise SystemExit(f"Renderer completed but expected manifest was not created: {manifest}")
    if analyzer_name:
        analyzer = SCRIPTS / analyzer_name
        if analyzer.is_file():
            _run(str(analyzer.relative_to(ROOT)))
    return True


def main() -> None:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    target = state.get("active_target")
    if not target or not re.fullmatch(r"OWS-\d{3}", target):
        raise SystemExit(f"Invalid active_target in heavy rebuild state: {target!r}")
    target_slug = target.lower().replace("-", "")
    gates = state.get("visual_review_gates", {})

    baseline = gates.get("baseline", {})
    if not _passed(baseline.get("status", "")):
        manifest = baseline.get("artifact_manifest")
        if manifest and (ROOT / manifest).is_file():
            print(f"{target} baseline artifact already exists; waiting for manual review bookkeeping.")
            return
        _run("scripts/render_old_world_heavy_rebuild_review.py", "--target", target, "--gate", "baseline")
        return

    gate_a = gates.get("gate_a_massing", {})
    if not _passed(gate_a.get("status", "")):
        _render_revisioned_gate(
            target=target,
            target_slug=target_slug,
            script_stem="gate_a_massing",
            gate_dir="gate_a_massing",
            manifest_name="review_manifest.json",
        )
        return

    gate_b = gates.get("gate_b_intact_state", {})
    if not _passed(gate_b.get("status", "")):
        _render_revisioned_gate(
            target=target,
            target_slug=target_slug,
            script_stem="gate_b_intact",
            gate_dir="gate_b_intact",
            manifest_name="review_manifest.json",
        )
        return

    gate_c = gates.get("gate_c_damage_states", {})
    if not _passed(gate_c.get("status", "")):
        _render_revisioned_gate(
            target=target,
            target_slug=target_slug,
            script_stem="gate_c_damage_states",
            gate_dir="gate_c_damage_states",
            manifest_name="gate_c_manifest.json",
            analyzer_name=f"analyze_{target_slug}_gate_c_visuals.py",
        )
        return

    gate_d = gates.get("gate_d_final_multi_angle", {})
    if not _passed(gate_d.get("status", "")):
        print(
            f"{target} Gate C is complete; Gate D remains blocked/owned by the static shipping workflow. "
            "No review-only Gate-D render was started."
        )
        return

    print(f"{target}: all review gates are already recorded as passed/complete; nothing to render.")


if __name__ == "__main__":
    main()
