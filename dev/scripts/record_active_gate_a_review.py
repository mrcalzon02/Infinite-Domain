#!/usr/bin/env python3
"""[SYSTEM REPORT] Mirror an explicit active-target Gate-A PASSED review into state.

This script never authors a visual decision. It records only an already-authored
PASSED review for the active target after confirming the exact persisted Gate-A
manifest/revision. It is intentionally generic so later OWS targets can reuse the
same guarded bookkeeping boundary.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STATE_PATH = ROOT / "dev/old_world_narrative" / "registry" / "heavy_rebuild_state.json"
REVIEW_ROOT = ROOT / "dev/old_world_narrative" / "reviews" / "heavy_rebuild"
VISUAL_ROOT = REVIEW_ROOT / "visual"


def _resolve_review_path(target: str, revision: int) -> Path | None:
    """Return the persisted explicit review without inventing a decision.

    Newer gate reviews live beside their exact rendered artifact so the review and
    immutable evidence remain inseparable. Legacy root-level review records remain
    supported for older targets.
    """
    candidates = (
        VISUAL_ROOT / target / "gate_a_massing" / f"r{revision}" / "INDEPENDENT_REVIEW.md",
        REVIEW_ROOT / f"{target}_GATE_A_R{revision}_REVIEW.md",
    )
    return next((path for path in candidates if path.is_file()), None)


def _review_is_explicit_pass(review: str, target: str, revision: int) -> bool:
    legacy_summary = f"**{target} GATE A r{revision}: PASSED.**"
    explicit_decision = (
        "**Decision:** **PASSED**" in review
        or re.search(r"(?mi)^Decision:\s*\*\*PASSED\*\*\s*$", review) is not None
    )
    identity = (
        legacy_summary in review
        or (
            re.search(rf"(?mi)^#\s*{re.escape(target)}\b.*Gate A r{revision}\b", review) is not None
            and re.search(rf"(?mi)^Revision:\s*\*\*r{revision}\*\*\s*$", review) is not None
        )
    )
    return explicit_decision and identity


def main() -> None:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    target = state.get("active_target", "")
    if not re.fullmatch(r"OWS-\d{3}", target):
        raise AssertionError(f"Invalid active target: {target!r}")

    gate = state.get("visual_review_gates", {}).get("gate_a_massing", {})
    status = str(gate.get("status", ""))
    if status.startswith("passed"):
        print(f"{target} Gate A already recorded as {status}")
        return

    match = re.fullmatch(r"r(\d+)_rendered_pending_manual_review", status)
    if not match:
        print(f"{target} Gate-A recorder skipped: status={status}")
        return
    revision = int(match.group(1))

    manifest_path = VISUAL_ROOT / target / "gate_a_massing" / f"r{revision}" / "review_manifest.json"
    review_path = _resolve_review_path(target, revision)
    if not manifest_path.is_file() or review_path is None:
        print(
            f"{target} Gate-A explicit review/manifest not both present; "
            f"manifest={manifest_path.is_file()} review={review_path is not None}"
        )
        return

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("target") != target or manifest.get("gate") != "gate_a_massing":
        raise AssertionError(f"{target} Gate-A manifest identity mismatch: {manifest}")
    if f"massing-r{revision}@" not in str(manifest.get("revision", "")):
        raise AssertionError(f"{target} Gate-A manifest revision mismatch: {manifest.get('revision')}")

    review = review_path.read_text(encoding="utf-8")
    if not _review_is_explicit_pass(review, target, revision):
        raise AssertionError(f"{target} Gate-A review lacks explicit PASSED decision or revision identity")

    passes = state["active_target_passes"]
    passes["massing"] = f"complete_gate_a_r{revision}"
    passes["visual_gate_a_massing"] = f"passed_r{revision}"
    if passes.get("structural_system") == "pending":
        passes["structural_system"] = "ready"

    review_rel = str(review_path.relative_to(ROOT)).replace("\\", "/")
    gate.update({
        "status": f"passed_r{revision}",
        "decision": "PASSED",
        f"r{revision}_review_record": review_rel,
        "significant_findings_corrected_or_justified": True,
    })
    state["visual_review_gates"]["gate_a_massing"] = gate
    state["visual_review_gates"]["gate_b_intact_state"]["status"] = "blocked_by_passes_7_12"
    state.setdefault("planning_records", {})[f"gate_a_r{revision}_review"] = review_rel
    state["active_status"] = f"gate_a_r{revision}_passed_pass_7_structural_system_ready"

    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Recorded explicit {target} Gate A r{revision} PASSED decision; Pass 7 is ready.")


if __name__ == "__main__":
    main()
