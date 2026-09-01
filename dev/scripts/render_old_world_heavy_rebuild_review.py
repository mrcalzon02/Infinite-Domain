#!/usr/bin/env python3
"""[SYSTEM REPORT] Multi-stage 3D review renderer for Old World heavy rebuilds.

This tool is deliberately separate from mechanical validation. It produces
spatially truthful primitive review images and records them as pending manual
visual review. Rendering an image never marks a gate passed.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw

from render_structure_review import floor_slices, isometric, unpack_structure


ROOT = Path(__file__).resolve().parents[2]
STATE_PATH = ROOT / "dev/old_world_narrative" / "registry" / "heavy_rebuild_state.json"
TARGETS_PATH = ROOT / "dev/old_world_narrative" / "registry" / "structure_targets.json"
OUTPUT_ROOT = ROOT / "dev/old_world_narrative" / "reviews" / "heavy_rebuild" / "visual"
AIR = {"minecraft:air", "minecraft:cave_air", "minecraft:void_air", "minecraft:structure_void"}

CAMERAS = (
    ("front_left", 0),
    ("rear_left", 1),
    ("rear_right", 2),
    ("front_right", 3),
)


def rotate_quarter(
    size: tuple[int, int, int],
    blocks: dict[tuple[int, int, int], str],
    quarter_turns: int,
) -> tuple[tuple[int, int, int], dict[tuple[int, int, int], str]]:
    """Rotate a structure around Y in exact 90-degree increments."""
    q = quarter_turns % 4
    sx, sy, sz = size
    if q == 0:
        return size, dict(blocks)
    rotated: dict[tuple[int, int, int], str] = {}
    if q == 1:
        for (x, y, z), name in blocks.items():
            rotated[(z, y, sx - 1 - x)] = name
        return (sz, sy, sx), rotated
    if q == 2:
        for (x, y, z), name in blocks.items():
            rotated[(sx - 1 - x, y, sz - 1 - z)] = name
        return size, rotated
    for (x, y, z), name in blocks.items():
        rotated[(sz - 1 - z, y, x)] = name
    return (sz, sy, sx), rotated


def top_projection(
    size: tuple[int, int, int],
    blocks: dict[tuple[int, int, int], str],
    title: str,
) -> Image.Image:
    """Simple roof/site plan showing the highest occupied block at each X/Z."""
    from render_structure_review import color_for

    sx, _, sz = size
    cell = max(3, min(8, 600 // max(sx, sz, 1)))
    width = sx * cell + 40
    height = sz * cell + 70
    image = Image.new("RGB", (width, height), (26, 28, 30))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, 28), fill=(10, 11, 12))
    draw.text((10, 8), title, fill=(235, 235, 235))
    highest: dict[tuple[int, int], tuple[int, str]] = {}
    for (x, y, z), name in blocks.items():
        current = highest.get((x, z))
        if current is None or y >= current[0]:
            highest[(x, z)] = (y, name)
    ox, oy = 20, 42
    for (x, z), (_, name) in highest.items():
        draw.rectangle(
            (ox + x * cell, oy + z * cell, ox + (x + 1) * cell - 1, oy + (z + 1) * cell - 1),
            fill=color_for(name),
        )
    draw.rectangle((ox - 1, oy - 1, ox + sx * cell, oy + sz * cell), outline=(175, 175, 175))
    return image


def cutaway_level(size: tuple[int, int, int], blocks: dict[tuple[int, int, int], str]) -> int:
    """Pick an interior-revealing level without pretending it is an approval metric."""
    sx, sy, sz = size
    area = sx * sz
    counts = {y: sum(1 for _, py, _ in blocks if py == y) for y in range(sy)}
    dense = [
        y for y in range(3, sy - 1)
        if counts[y] >= max(12, int(area * 0.12))
        and counts[y] > counts[y - 1] * 1.5
    ]
    if dense:
        return max(2, min(dense) - 1)
    return max(2, min(sy - 1, int(sy * 0.62)))


def contact_sheet(
    images: list[tuple[str, Path]],
    output: Path,
    *,
    target: str,
    gate: str,
    revision: str,
    damage_state: str,
    dimensions: tuple[int, int, int],
    camera_set: str,
) -> None:
    """Build a labeled fixed-camera review sheet while keeping individual views."""
    loaded: list[tuple[str, Image.Image]] = [(label, Image.open(path).convert("RGB")) for label, path in images]
    thumb_w = 520
    margin = 18
    header_h = 86
    label_h = 24
    resized: list[tuple[str, Image.Image]] = []
    for label, image in loaded:
        ratio = thumb_w / max(1, image.width)
        thumb = image.resize((thumb_w, max(1, int(image.height * ratio))), Image.Resampling.LANCZOS)
        resized.append((label, thumb))
    row_heights = []
    for row in range((len(resized) + 1) // 2):
        pair = resized[row * 2: row * 2 + 2]
        row_heights.append(max(img.height for _, img in pair) + label_h)
    sheet_w = margin * 3 + thumb_w * 2
    sheet_h = header_h + margin + sum(row_heights) + margin * max(0, len(row_heights) - 1) + margin
    sheet = Image.new("RGB", (sheet_w, sheet_h), (20, 22, 24))
    draw = ImageDraw.Draw(sheet)
    draw.text((margin, 12), f"{target} — {gate}", fill=(245, 245, 245))
    draw.text(
        (margin, 34),
        f"revision={revision}  damage={damage_state}  dimensions={dimensions[0]}x{dimensions[1]}x{dimensions[2]}",
        fill=(210, 210, 210),
    )
    draw.text((margin, 56), f"fixed_camera_set={camera_set}  status=PENDING MANUAL VISUAL REVIEW", fill=(225, 190, 84))
    y = header_h
    for index, (label, image) in enumerate(resized):
        row = index // 2
        col = index % 2
        if col == 0 and index > 0:
            y = header_h + sum(row_heights[:row]) + margin * row
        x = margin + col * (thumb_w + margin)
        draw.text((x, y), label, fill=(235, 235, 235))
        sheet.paste(image, (x, y + label_h))
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output)
    for _, image in loaded:
        image.close()


def extract_historical_nbt(commit: str, path: str) -> Path:
    """Extract exact historical binary NBT from git history for baseline comparison."""
    proc = subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise SystemExit(
            f"Could not extract historical baseline {commit}:{path}: "
            + proc.stderr.decode("utf-8", errors="replace")
        )
    handle = tempfile.NamedTemporaryFile(prefix="old-world-baseline-", suffix=".nbt", delete=False)
    handle.write(proc.stdout)
    handle.flush()
    handle.close()
    return Path(handle.name)


def target_record(target: str) -> dict[str, Any]:
    registry = json.loads(TARGETS_PATH.read_text(encoding="utf-8"))
    for record in registry["targets"]:
        if record.get("id") == target or record.get("target") == target:
            return record
    raise SystemExit(f"Unknown Old World target: {target}")


def source_template_path(record: dict[str, Any]) -> str:
    path = record.get("narrative_source_template")
    if path:
        return path
    structure_id = record.get("narrative_structure", "")
    if not structure_id:
        raise SystemExit("Target has no narrative source template or narrative structure")
    name = structure_id.split("/", 1)[-1]
    return f"kubejs/data/infinite_domain/structure/wasteland/old_world/{name}.nbt"


def render_review_set(
    *,
    target: str,
    gate: str,
    revision: str,
    damage_state: str,
    source_commit: str,
    source_path: str,
    size: tuple[int, int, int],
    blocks: dict[tuple[int, int, int], str],
    output_dir: Path,
    camera_set: str,
) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    views: list[tuple[str, Path]] = []
    manifest_views: dict[str, str] = {}

    for label, quarter in CAMERAS:
        rotated_size, rotated_blocks = rotate_quarter(size, blocks, quarter)
        path = output_dir / f"{label}.png"
        isometric(
            rotated_size,
            rotated_blocks,
            False,
            f"{target} — {gate} — {damage_state} — {label}",
        ).save(path)
        views.append((label, path))
        manifest_views[label] = str(path.relative_to(ROOT)).replace("\\", "/")

    top_path = output_dir / "roof_top_oblique.png"
    top_projection(size, blocks, f"{target} — {gate} — {damage_state} — roof/top").save(top_path)
    views.append(("roof_top_oblique", top_path))
    manifest_views["roof_top_oblique"] = str(top_path.relative_to(ROOT)).replace("\\", "/")

    cutoff = cutaway_level(size, blocks)
    cutaway_blocks = {pos: name for pos, name in blocks.items() if pos[1] <= cutoff}
    cut_path = output_dir / "interior_cutaway.png"
    isometric(size, cutaway_blocks, False, f"{target} — {gate} — interior cutaway Y<={cutoff}").save(cut_path)
    views.append(("interior_cutaway", cut_path))
    manifest_views["interior_cutaway"] = str(cut_path.relative_to(ROOT)).replace("\\", "/")

    floors_path = output_dir / "floor_slices.png"
    floor_slices(size, blocks, f"{target} — {gate} — {damage_state}").save(floors_path)
    manifest_views["floor_slices"] = str(floors_path.relative_to(ROOT)).replace("\\", "/")

    sheet_path = output_dir / "contact_sheet.png"
    contact_sheet(
        views,
        sheet_path,
        target=target,
        gate=gate,
        revision=revision,
        damage_state=damage_state,
        dimensions=size,
        camera_set=camera_set,
    )
    manifest_views["contact_sheet"] = str(sheet_path.relative_to(ROOT)).replace("\\", "/")

    manifest = {
        "target": target,
        "gate": gate,
        "revision": revision,
        "damage_state": damage_state,
        "source_commit": source_commit,
        "source_path": source_path,
        "dimensions": list(size),
        "fixed_camera_set": camera_set,
        "visual_review_status": "rendered_pending_manual_review",
        "visual_findings": [],
        "significant_findings_corrected_or_justified": False,
        "final_preview_synchronized_with_authoritative_nbt": gate == "gate_d_final",
        "cutaway_y": cutoff,
        "views": manifest_views,
    }
    manifest_path = output_dir / "review_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n")
    return manifest


def render_baseline(target: str) -> dict[str, Any]:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if target != state.get("active_target"):
        raise SystemExit(f"Heavy rebuild is locked to active target {state.get('active_target')}; refused {target}")
    gate_status = state.get("visual_review_gates", {}).get("baseline", {}).get("status", "pending_render")
    if gate_status == "passed" or gate_status == "complete" or gate_status.startswith("reviewed_"):
        manifest_path = state["visual_review_gates"]["baseline"].get("artifact_manifest")
        if not manifest_path:
            raise SystemExit("Baseline is marked reviewed/passed but no artifact manifest is recorded")
        return json.loads((ROOT / manifest_path).read_text(encoding="utf-8"))
    record = target_record(target)
    source_path = source_template_path(record)
    baseline_commit = state["baseline_source_commit"]
    baseline_file = extract_historical_nbt(baseline_commit, source_path)
    try:
        size, blocks = unpack_structure(baseline_file)
    finally:
        baseline_file.unlink(missing_ok=True)

    camera_set = state["visual_review_gates"]["baseline"]["fixed_camera_set"]
    output_dir = OUTPUT_ROOT / target / "baseline" / "r0_pre_heavy_rebuild"
    manifest = render_review_set(
        target=target,
        gate="baseline",
        revision=f"pre-heavy-rebuild@{baseline_commit[:8]}",
        damage_state="historical rough implementation",
        source_commit=baseline_commit,
        source_path=source_path,
        size=size,
        blocks=blocks,
        output_dir=output_dir,
        camera_set=camera_set,
    )

    state["active_status"] = "phase_0_baseline_rendered_pending_review"
    state["active_target_passes"]["baseline_3d_review"] = "rendered_pending_manual_review"
    state["visual_review_gates"]["baseline"]["status"] = "rendered_pending_manual_review"
    state["visual_review_gates"]["baseline"]["artifact_manifest"] = str(
        (output_dir / "review_manifest.json").relative_to(ROOT)
    ).replace("\\", "/")
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True)
    parser.add_argument("--gate", choices=("baseline",), required=True)
    args = parser.parse_args()
    if args.gate == "baseline":
        manifest = render_baseline(args.target)
    else:
        raise SystemExit(f"Unsupported gate: {args.gate}")
    print(
        f"Rendered {manifest['target']} {manifest['gate']} with four fixed exterior cameras, "
        "roof/top view, interior cutaway, floor slices, and labeled contact sheet. "
        "Visual approval remains pending."
    )


if __name__ == "__main__":
    main()
