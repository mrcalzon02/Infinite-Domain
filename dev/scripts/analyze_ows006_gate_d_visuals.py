#!/usr/bin/env python3
"""Image-regression guard for OWS-006 Gate-D r1; never approves the gate."""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageChops


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "dev/old_world_narrative" / "reviews" / "heavy_rebuild" / "visual" / "OWS-006"
GATE_C = BASE / "gate_c_damage_states" / "r2" / "d3"
GATE_D = BASE / "gate_d_final" / "r1"
SYNC_PATH = GATE_D / "authoritative_sync.json"
REPORT_PATH = GATE_D / "visual_regression_metrics.json"
BACKGROUND = (26, 28, 30)
TITLE_CROP_Y = 27
VIEWS = ("front_left", "rear_left", "rear_right", "front_right", "roof_top_oblique", "interior_cutaway")
EXTERIOR = VIEWS[:4]


def _load(root: Path, view: str) -> Image.Image:
    image = Image.open(root / f"{view}.png").convert("RGB")
    return image.crop((0, TITLE_CROP_Y, image.width, image.height))


def _foreground(image: Image.Image) -> int:
    return sum(pixel != BACKGROUND for pixel in image.getdata())


def _changed(a: Image.Image, b: Image.Image) -> float:
    if a.size != b.size:
        raise AssertionError(f"fixed-camera dimensions changed: {a.size} != {b.size}")
    changed = sum(pixel != (0, 0, 0) for pixel in ImageChops.difference(a, b).getdata())
    union = sum(pa != BACKGROUND or pb != BACKGROUND for pa, pb in zip(a.getdata(), b.getdata()))
    if not union:
        raise AssertionError("empty fixed-camera comparison")
    return changed / union


def main() -> None:
    sync = json.loads(SYNC_PATH.read_text(encoding="utf-8"))
    if not sync.get("exact_serialized_nbt_match") or not sync.get("exact_decompressed_nbt_match"):
        raise AssertionError("OWS-006 exact shipping synchronization proof is missing")
    if sync.get("render_source") != "shipping_nbt":
        raise AssertionError("OWS-006 Gate D was not rendered from shipping NBT")

    changed: dict[str, float] = {}
    silhouette: dict[str, float] = {}
    for view in VIEWS:
        gate_c, gate_d = _load(GATE_C, view), _load(GATE_D, view)
        try:
            changed[view] = _changed(gate_c, gate_d)
            baseline = _foreground(gate_c)
            if not baseline:
                raise AssertionError(f"empty Gate-C view: {view}")
            silhouette[view] = _foreground(gate_d) / baseline
        finally:
            gate_c.close()
            gate_d.close()

    average = sum(changed.values()) / len(changed)
    exterior_average = sum(changed[v] for v in EXTERIOR) / len(EXTERIOR)
    maximum = max(changed.values())
    if average > 0.08 or maximum > 0.16:
        raise AssertionError(f"post-Gate-C drift exceeds microdetail scale: average={average:.4f}, max={maximum:.4f}")
    for view in EXTERIOR:
        if not 0.95 <= silhouette[view] <= 1.05:
            raise AssertionError(f"exterior silhouette drift in {view}: {silhouette[view]:.4f}")
    if not 0.90 <= silhouette["roof_top_oblique"] <= 1.10:
        raise AssertionError(f"roof/site silhouette drift: {silhouette['roof_top_oblique']:.4f}")

    report = {
        "target": "OWS-006",
        "gate": "gate_d_final",
        "revision": "r1",
        "comparison": "Gate-D stabilized shipping-NBT renders vs accepted Gate-C r2 D3 renders",
        "fixed_camera_set": "ows006_fixed_v1",
        "authoritative_sync": {
            "exact_serialized_nbt_match": True,
            "exact_decompressed_nbt_match": True,
            "shipping_nbt_sha256": sync["shipping_nbt_sha256"],
            "render_source": "shipping_nbt",
        },
        "visible_change_ratio_from_gate_c_r2_d3": changed,
        "foreground_silhouette_ratio_from_gate_c_r2_d3": silhouette,
        "averages": {"all_views": average, "exterior": exterior_average, "maximum_single_view": maximum},
        "checks": {
            "post_gate_c_changes_remain_microdetail_scale": True,
            "exterior_silhouette_retained": True,
            "roof_site_silhouette_retained": True,
            "authoritative_shipping_sync_retained": True,
        },
        "decision": "IMAGE_LEVEL_REGRESSION_CHECKS_PASSED_PENDING_INDEPENDENT_REVIEW",
        "note": "Regression guard only; independent Gate-D visual approval remains required.",
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"OWS-006 Gate-D regression passed: average={average:.4f}, exterior={exterior_average:.4f}, max={maximum:.4f}")


if __name__ == "__main__":
    main()
