#!/usr/bin/env python3
"""[SYSTEM REPORT] Image-level QA for OWS-003 Gate-C r3 D0/D1/D3 renders.

Reads only the exact persisted Gate-C r3 PNGs and writes numeric review metrics.
It NEVER changes heavy_rebuild_state.json and NEVER approves Gate C. The manual
fixed-camera review remains authoritative.
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[2]
REVIEW_ROOT = ROOT / "dev/old_world_narrative" / "reviews" / "heavy_rebuild" / "visual" / "OWS-003" / "gate_c_damage_states" / "r3"
REPORT_PATH = REVIEW_ROOT / "visual_metrics.json"
BACKGROUND = (26, 28, 30)
CAMERAS = ("front_left", "rear_left", "rear_right", "front_right", "interior_cutaway")
EXTERIOR = CAMERAS[:4]
TITLE_CROP_Y = 27
STRUCTURE_SIZE_X = 59
STRUCTURE_SIZE_Z = 51
FLOOR_CELL = 5
FLOOR_PANEL_W = STRUCTURE_SIZE_X * FLOOR_CELL + 24
FLOOR_PANEL_H = STRUCTURE_SIZE_Z * FLOOR_CELL + 44
FLOOR_MAP_X0 = 12
FLOOR_MAP_Y0 = 30
FLOOR_MAP_W = STRUCTURE_SIZE_X * FLOOR_CELL
FLOOR_MAP_H = STRUCTURE_SIZE_Z * FLOOR_CELL


def _load(state: str, view: str, *, crop_title: bool = True) -> Image.Image:
    path = REVIEW_ROOT / state / f"{view}.png"
    if not path.is_file():
        raise AssertionError(f"missing OWS-003 Gate-C r3 render: {path}")
    image = Image.open(path).convert("RGB")
    if crop_title:
        if image.height <= TITLE_CROP_Y:
            raise AssertionError(f"unexpectedly short Gate-C render: {path} {image.size}")
        cropped = image.crop((0, TITLE_CROP_Y, image.width, image.height))
        image.close()
        return cropped
    return image


def _foreground_count(image: Image.Image) -> int:
    return sum(1 for pixel in image.getdata() if pixel != BACKGROUND)


def _changed_ratio(a: Image.Image, b: Image.Image) -> float:
    if a.size != b.size:
        raise AssertionError(f"render dimensions differ: {a.size} != {b.size}")
    diff = ImageChops.difference(a, b)
    changed = sum(1 for pixel in diff.getdata() if pixel != (0, 0, 0))
    union = sum(1 for pa, pb in zip(a.getdata(), b.getdata()) if pa != BACKGROUND or pb != BACKGROUND)
    if not union:
        raise AssertionError("camera contains no rendered foreground")
    return changed / union


def _floor_ratio(a: Image.Image, b: Image.Image) -> float:
    if a.size != b.size:
        raise AssertionError(f"floor-slice dimensions differ: {a.size} != {b.size}")
    changed = 0
    union = 0
    for y in range(a.height):
        local_y = y % FLOOR_PANEL_H
        if not FLOOR_MAP_Y0 <= local_y < FLOOR_MAP_Y0 + FLOOR_MAP_H:
            continue
        for x in range(a.width):
            local_x = x % FLOOR_PANEL_W
            if not FLOOR_MAP_X0 <= local_x < FLOOR_MAP_X0 + FLOOR_MAP_W:
                continue
            pa, pb = a.getpixel((x, y)), b.getpixel((x, y))
            if pa != BACKGROUND or pb != BACKGROUND:
                union += 1
            if pa != pb:
                changed += 1
    if not union:
        raise AssertionError("floor maps contain no rendered foreground")
    return changed / union


def main() -> None:
    manifest_path = REVIEW_ROOT / "gate_c_manifest.json"
    if not manifest_path.is_file():
        raise SystemExit("OWS-003 Gate-C r3 manifest does not exist; no image analysis performed")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not str(manifest.get("revision", "")).startswith("gate-c-r3@"):
        raise AssertionError(f"expected r3 manifest, got {manifest.get('revision')!r}")
    if manifest.get("d1_changed_positions_from_d0") != 19:
        raise AssertionError("r3 manifest does not preserve accepted D1 delta of 19")
    if int(manifest.get("d3_changed_positions_from_d0", 0)) < 550:
        raise AssertionError("r3 manifest does not meet the strengthened D3 source-change floor")

    ratios = {"d1_from_d0": {}, "d3_from_d0": {}}
    silhouette = {"d1_vs_d0": {}, "d3_vs_d0": {}}
    for view in CAMERAS:
        d0 = _load("d0", view)
        d1 = _load("d1", view)
        d3 = _load("d3", view)
        try:
            ratios["d1_from_d0"][view] = _changed_ratio(d0, d1)
            ratios["d3_from_d0"][view] = _changed_ratio(d0, d3)
            base_fg = _foreground_count(d0)
            if not base_fg:
                raise AssertionError(f"D0 {view} has no foreground")
            silhouette["d1_vs_d0"][view] = _foreground_count(d1) / base_fg
            silhouette["d3_vs_d0"][view] = _foreground_count(d3) / base_fg
        finally:
            d0.close(); d1.close(); d3.close()

    f0 = _load("d0", "floor_slices", crop_title=False)
    f1 = _load("d1", "floor_slices", crop_title=False)
    f3 = _load("d3", "floor_slices", crop_title=False)
    try:
        floor = {"d1_from_d0": _floor_ratio(f0, f1), "d3_from_d0": _floor_ratio(f0, f3)}
    finally:
        f0.close(); f1.close(); f3.close()

    d1_avg = sum(ratios["d1_from_d0"].values()) / len(CAMERAS)
    d3_avg = sum(ratios["d3_from_d0"].values()) / len(CAMERAS)
    d1_ext = sum(ratios["d1_from_d0"][v] for v in EXTERIOR) / len(EXTERIOR)
    d3_ext = sum(ratios["d3_from_d0"][v] for v in EXTERIOR) / len(EXTERIOR)

    # Broad safeguards only. These reject invisible history or demolition-scale
    # drift but intentionally do not decide whether the architecture looks good.
    if max(ratios["d1_from_d0"]["interior_cutaway"], floor["d1_from_d0"]) < 0.001:
        raise AssertionError("accepted D1 became visually imperceptible in both internal review modes")
    if d1_avg > 0.10 or floor["d1_from_d0"] > 0.12:
        raise AssertionError("D1 is too visually invasive for an early anomaly")
    if d3_avg <= d1_avg or floor["d3_from_d0"] <= floor["d1_from_d0"]:
        raise AssertionError("D3 is not visually stronger than D1")
    if d3_avg > 0.35 or floor["d3_from_d0"] > 0.40:
        raise AssertionError("D3 changes too much of the reconstructable facility")
    visible_exteriors = sum(1 for v in EXTERIOR if ratios["d3_from_d0"][v] >= 0.01)
    if visible_exteriors < 2:
        raise AssertionError(f"D3 is not visibly legible from enough exterior cameras: {ratios['d3_from_d0']}")
    for view in EXTERIOR:
        if not 0.95 <= silhouette["d1_vs_d0"][view] <= 1.08:
            raise AssertionError(f"D1 exterior silhouette changed implausibly in {view}")
        if not 0.80 <= silhouette["d3_vs_d0"][view] <= 1.15:
            raise AssertionError(f"D3 no longer preserves the facility silhouette in {view}")

    report = {
        "target": "OWS-003",
        "gate": "gate_c_damage_states",
        "revision": manifest["revision"],
        "analysis": "actual r3 rendered PNG pixels; isometric title bars cropped and floor-map labels excluded",
        "fixed_camera_set": manifest.get("fixed_camera_set", "ows003_fixed_v1"),
        "source_changed_positions": {
            "d1_from_d0": manifest["d1_changed_positions_from_d0"],
            "d3_from_d0": manifest["d3_changed_positions_from_d0"],
        },
        "visible_change_ratio": ratios,
        "floor_map_visible_change_ratio": floor,
        "foreground_silhouette_ratio": silhouette,
        "averages": {
            "d1_all_isometric_views": d1_avg,
            "d3_all_isometric_views": d3_avg,
            "d1_exterior": d1_ext,
            "d3_exterior": d3_ext,
        },
        "checks": {
            "d1_visibly_present_in_internal_review": True,
            "d1_restrained": True,
            "d3_visibly_stronger_than_d1": True,
            "d3_visible_from_multiple_exterior_cameras": True,
            "d1_exterior_silhouette_retained": True,
            "d3_exterior_silhouette_retained": True,
        },
        "decision": "IMAGE_LEVEL_CHECKS_PASSED_PENDING_MANUAL_REVIEW",
        "note": "This report is a regression safeguard only and cannot approve Gate C.",
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(
        "OWS-003 Gate-C r3 image checks passed: "
        f"D1 cameras={d1_avg:.4f}, floors={floor['d1_from_d0']:.4f}; "
        f"D3 cameras={d3_avg:.4f}, floors={floor['d3_from_d0']:.4f}; exterior={d3_ext:.4f}."
    )


if __name__ == "__main__":
    main()
