#!/usr/bin/env python3
"""[SYSTEM REPORT] Image-level regression guard for synchronized OWS-003 Gate D.

Compares final shipping-NBT renders with the manually approved Gate-C r3 D3 set.
The check may reject reconstruction drift but cannot approve Gate D visually.
"""
from __future__ import annotations

import json
from pathlib import Path
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[2]
STATE_PATH = ROOT / "dev/old_world_narrative" / "registry" / "heavy_rebuild_state.json"
BASE = ROOT / "dev/old_world_narrative" / "reviews" / "heavy_rebuild" / "visual" / "OWS-003"
GATE_C = BASE / "gate_c_damage_states" / "r3" / "d3"
GATE_D = BASE / "gate_d_final" / "r1"
SYNC_PATH = GATE_D / "authoritative_sync.json"
REPORT_PATH = GATE_D / "visual_regression_metrics.json"
BACKGROUND = (26, 28, 30)
TITLE_CROP_Y = 27
VIEWS = ("front_left", "rear_left", "rear_right", "front_right", "roof_top_oblique", "interior_cutaway")
EXTERIOR = VIEWS[:4]


def _load(root: Path, view: str) -> Image.Image:
    path = root / f"{view}.png"
    if not path.is_file():
        raise AssertionError(f"missing review render: {path}")
    image = Image.open(path).convert("RGB")
    return image.crop((0, TITLE_CROP_Y, image.width, image.height))


def _foreground_count(image: Image.Image) -> int:
    return sum(1 for pixel in image.getdata() if pixel != BACKGROUND)


def _changed_ratio(a: Image.Image, b: Image.Image) -> float:
    if a.size != b.size:
        raise AssertionError(f"fixed-camera dimensions changed: {a.size} != {b.size}")
    diff = ImageChops.difference(a, b)
    changed = sum(1 for pixel in diff.getdata() if pixel != (0, 0, 0))
    union = sum(1 for pa, pb in zip(a.getdata(), b.getdata()) if pa != BACKGROUND or pb != BACKGROUND)
    if union == 0:
        raise AssertionError("review camera contains no structure pixels")
    return changed / union


def main() -> None:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    if state.get("active_target") != "OWS-003":
        print(f"OWS-003 Gate-D visual regression skipped: active target is {state.get('active_target')}")
        return
    gate = state.get("visual_review_gates", {}).get("gate_d_final_multi_angle", {})
    if gate.get("status") not in {
        "r1_rendered_authoritative_sync_verified_pending_manual_review",
        "r1_image_checks_passed_pending_manual_review",
    }:
        print(f"OWS-003 Gate-D visual regression skipped: status={gate.get('status')}")
        return

    sync = json.loads(SYNC_PATH.read_text(encoding="utf-8"))
    if not sync.get("exact_decompressed_nbt_match") or sync.get("render_source") != "shipping_nbt":
        raise AssertionError("OWS-003 Gate-D exact shipping synchronization proof is missing")

    changed: dict[str, float] = {}
    silhouette: dict[str, float] = {}
    for view in VIEWS:
        gate_c = _load(GATE_C, view)
        gate_d = _load(GATE_D, view)
        try:
            changed[view] = _changed_ratio(gate_c, gate_d)
            baseline = _foreground_count(gate_c)
            if baseline == 0:
                raise AssertionError(f"Gate-C r3 {view} contains no foreground pixels")
            silhouette[view] = _foreground_count(gate_d) / baseline
        finally:
            gate_c.close(); gate_d.close()

    average = sum(changed.values()) / len(changed)
    exterior_average = sum(changed[v] for v in EXTERIOR) / len(EXTERIOR)
    maximum = max(changed.values())
    if average > 0.08:
        raise AssertionError(f"OWS-003 Gate-D drift too large for Pass-19 microdetail: average={average:.4f}")
    if maximum > 0.16:
        raise AssertionError(f"OWS-003 Gate-D single-view drift too large: max={maximum:.4f}")
    for view in EXTERIOR:
        if not 0.95 <= silhouette[view] <= 1.05:
            raise AssertionError(f"OWS-003 Gate-D exterior silhouette drifted in {view}: {silhouette[view]:.4f}")
    if not 0.90 <= silhouette["roof_top_oblique"] <= 1.10:
        raise AssertionError(f"OWS-003 Gate-D roof/site silhouette drifted: {silhouette['roof_top_oblique']:.4f}")

    report = {
        "target": "OWS-003",
        "gate": "gate_d_final",
        "revision": "r1",
        "comparison": "Gate-D authoritative shipping NBT renders vs Gate-C r3 approved D3 renders",
        "fixed_camera_set": gate.get("fixed_camera_set", "ows003_fixed_v1"),
        "authoritative_sync": {
            "exact_decompressed_nbt_match": True,
            "shipping_nbt_sha256": sync.get("shipping_nbt_sha256"),
            "render_source": "shipping_nbt",
        },
        "visible_change_ratio_from_gate_c_r3_d3": changed,
        "foreground_silhouette_ratio_from_gate_c_r3_d3": silhouette,
        "averages": {"all_views": average, "exterior": exterior_average, "maximum_single_view": maximum},
        "checks": {
            "post_gate_c_changes_remain_microdetail_scale": True,
            "exterior_silhouette_retained": True,
            "roof_site_silhouette_retained": True,
            "authoritative_shipping_sync_retained": True,
        },
        "decision": "IMAGE_LEVEL_REGRESSION_CHECKS_PASSED_PENDING_MANUAL_REVIEW",
        "note": "Regression guard only; manual Gate-D visual approval remains required.",
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")

    state["active_status"] = "gate_d_r1_image_checks_passed_authoritative_sync_verified_pending_review"
    state["active_target_passes"]["visual_gate_d_final_multi_angle"] = "r1_image_checks_passed_authoritative_sync_verified_pending_manual_review"
    gate["status"] = "r1_image_checks_passed_pending_manual_review"
    gate["r1_visual_regression_metrics"] = str(REPORT_PATH.relative_to(ROOT)).replace("\\", "/")
    gate["image_level_checks"] = "passed_pending_manual_review"
    state["visual_review_gates"]["gate_d_final_multi_angle"] = gate
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"OWS-003 Gate-D image regression passed: average={average:.4f}, exterior={exterior_average:.4f}, max={maximum:.4f}.")


if __name__ == "__main__":
    main()
