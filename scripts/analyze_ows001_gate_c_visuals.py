#!/usr/bin/env python3
"""[SYSTEM REPORT] Image-level QA for OWS-001 Gate-C D0/D1/D3 renders.

This pass reads the actual persisted PNG camera views. It does not approve Gate C.
It quantifies visible state separation and exterior silhouette retention so a
source-correct damage pass cannot quietly produce either an invisible D1 or an
over-destroyed D3 in the primitive 3D renderer.
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "old_world_narrative" / "registry" / "heavy_rebuild_state.json"
REVIEW_ROOT = ROOT / "old_world_narrative" / "reviews" / "heavy_rebuild" / "visual" / "OWS-001" / "gate_c_damage_states" / "r1"
REPORT_PATH = REVIEW_ROOT / "visual_metrics.json"
BACKGROUND = (26, 28, 30)
CAMERAS = ("front_left", "rear_left", "rear_right", "front_right", "interior_cutaway")
EXTERIOR = CAMERAS[:4]
TITLE_CROP_Y = 27


def _load(state: str, view: str) -> Image.Image:
    path = REVIEW_ROOT / state / f"{view}.png"
    if not path.is_file():
        raise AssertionError(f"missing Gate-C render: {path}")
    image = Image.open(path).convert("RGB")
    if image.height <= TITLE_CROP_Y:
        raise AssertionError(f"Gate-C render is unexpectedly short: {path} {image.size}")
    return image.crop((0, TITLE_CROP_Y, image.width, image.height))


def _foreground_count(image: Image.Image) -> int:
    return sum(1 for pixel in image.getdata() if pixel != BACKGROUND)


def _changed_ratio(a: Image.Image, b: Image.Image) -> float:
    if a.size != b.size:
        raise AssertionError(f"camera render dimensions changed across states: {a.size} != {b.size}")
    difference = ImageChops.difference(a, b)
    changed = sum(1 for pixel in difference.getdata() if pixel != (0, 0, 0))
    union_foreground = sum(
        1
        for pa, pb in zip(a.getdata(), b.getdata())
        if pa != BACKGROUND or pb != BACKGROUND
    )
    if union_foreground == 0:
        raise AssertionError("camera contains no rendered structure pixels")
    return changed / union_foreground


def main() -> None:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    gate = state.get("visual_review_gates", {}).get("gate_c_damage_states", {})
    if state.get("active_target") != "OWS-001":
        print(f"Gate-C visual analysis skipped: active target is {state.get('active_target')}")
        return
    if gate.get("status") not in {"r1_rendered_pending_manual_review", "r1_image_checks_passed_pending_manual_review"}:
        print(f"Gate-C visual analysis skipped: status={gate.get('status')}")
        return

    ratios: dict[str, dict[str, float]] = {"d1_from_d0": {}, "d3_from_d0": {}}
    silhouette: dict[str, dict[str, float]] = {"d1_vs_d0": {}, "d3_vs_d0": {}}

    for view in CAMERAS:
        d0 = _load("d0", view)
        d1 = _load("d1", view)
        d3 = _load("d3", view)
        try:
            ratios["d1_from_d0"][view] = _changed_ratio(d0, d1)
            ratios["d3_from_d0"][view] = _changed_ratio(d0, d3)
            d0_fg = _foreground_count(d0)
            if d0_fg == 0:
                raise AssertionError(f"D0 {view} contains no foreground pixels")
            silhouette["d1_vs_d0"][view] = _foreground_count(d1) / d0_fg
            silhouette["d3_vs_d0"][view] = _foreground_count(d3) / d0_fg
        finally:
            d0.close()
            d1.close()
            d3.close()

    d1_average = sum(ratios["d1_from_d0"].values()) / len(CAMERAS)
    d3_average = sum(ratios["d3_from_d0"].values()) / len(CAMERAS)
    d1_exterior = sum(ratios["d1_from_d0"][view] for view in EXTERIOR) / len(EXTERIOR)
    d3_exterior = sum(ratios["d3_from_d0"][view] for view in EXTERIOR) / len(EXTERIOR)

    # Broad visual guardrails. These reject invisible states and destructive
    # silhouette collapse without pretending a numeric metric can replace review.
    if max(ratios["d1_from_d0"].values()) < 0.002:
        raise AssertionError(f"D1 is visually imperceptible in every camera: {ratios['d1_from_d0']}")
    if d1_average > 0.12:
        raise AssertionError(f"D1 is too visually invasive for early anomaly: average={d1_average:.4f}")
    if d3_average <= d1_average:
        raise AssertionError(f"D3 is not visually stronger than D1: d1={d1_average:.4f}, d3={d3_average:.4f}")
    if d3_average > 0.35:
        raise AssertionError(f"D3 changes too much of the rendered structure: average={d3_average:.4f}")
    if sum(1 for view in EXTERIOR if ratios["d3_from_d0"][view] >= 0.01) < 2:
        raise AssertionError(f"D3 is not visibly legible from enough exterior cameras: {ratios['d3_from_d0']}")
    for view in EXTERIOR:
        d1_retention = silhouette["d1_vs_d0"][view]
        d3_retention = silhouette["d3_vs_d0"][view]
        if not 0.95 <= d1_retention <= 1.08:
            raise AssertionError(f"D1 exterior silhouette changed implausibly in {view}: {d1_retention:.4f}")
        if not 0.80 <= d3_retention <= 1.15:
            raise AssertionError(f"D3 exterior silhouette no longer preserves the building in {view}: {d3_retention:.4f}")

    report = {
        "target": "OWS-001",
        "gate": "gate_c_damage_states",
        "revision": "r1",
        "analysis": "actual rendered PNG pixels below the title band",
        "camera_set": gate.get("fixed_camera_set", "ows001_fixed_v1"),
        "visible_change_ratio": ratios,
        "foreground_silhouette_ratio": silhouette,
        "averages": {
            "d1_all_views": d1_average,
            "d3_all_views": d3_average,
            "d1_exterior": d1_exterior,
            "d3_exterior": d3_exterior,
        },
        "checks": {
            "d1_visibly_present_but_restrained": True,
            "d3_visibly_stronger_than_d1": True,
            "d3_visible_from_multiple_exterior_cameras": True,
            "d1_exterior_silhouette_retained": True,
            "d3_exterior_silhouette_retained": True,
        },
        "decision": "IMAGE_LEVEL_CHECKS_PASSED_PENDING_REVIEW",
        "note": "Numeric image QA is a blocking safeguard, not an automatic Gate-C visual approval.",
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")

    state["active_status"] = "gate_c_r1_image_checks_passed_pending_review"
    state["active_target_passes"]["visual_gate_c_damage_states"] = "r1_image_checks_passed_pending_manual_review"
    gate["status"] = "r1_image_checks_passed_pending_manual_review"
    gate["r1_visual_metrics"] = str(REPORT_PATH.relative_to(ROOT)).replace("\\", "/")
    gate["image_level_checks"] = "passed_pending_manual_review"
    state["visual_review_gates"]["gate_c_damage_states"] = gate
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")

    print(
        "OWS-001 Gate-C image checks passed: "
        f"D1 avg={d1_average:.4f}, D3 avg={d3_average:.4f}, "
        f"D1 exterior={d1_exterior:.4f}, D3 exterior={d3_exterior:.4f}."
    )


if __name__ == "__main__":
    main()
