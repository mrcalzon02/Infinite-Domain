#!/usr/bin/env python3
"""[SYSTEM REPORT] Mirror an explicit active-target Gate-B review into state.

This script NEVER decides visual quality. It only records an already-authored
Gate-B PASSED or REVISION REQUIRED decision after confirming the exact persisted
revision artifact exists. The same guarded bookkeeping works for later OWS targets.

It can also recover from an older workflow bug that downgraded a rendered Gate-B
state back to planning-ready: recovery is permitted only when the newest persisted
Gate-B manifest has a matching explicit review. An older review is never applied
over a newer unreviewed artifact or over a state that explicitly requires a newer
Gate-B revision.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "old_world_narrative" / "registry" / "heavy_rebuild_state.json"
REVIEW_ROOT = ROOT / "old_world_narrative" / "reviews" / "heavy_rebuild"
VISUAL_ROOT = REVIEW_ROOT / "visual"
INTACT_PASSES = (
    "structural_system",
    "circulation_and_access",
    "exterior_architecture",
    "interior_architecture",
    "operational_systems",
    "institutional_identity",
)


def _manifest_revisions(target: str) -> list[int]:
    root = VISUAL_ROOT / target / "gate_b_intact"
    if not root.is_dir():
        return []
    revisions: list[int] = []
    for path in root.glob("r*/review_manifest.json"):
        match = re.fullmatch(r"r(\d+)", path.parent.name)
        if match:
            revisions.append(int(match.group(1)))
    return sorted(set(revisions))


def _review_revisions(target: str) -> list[int]:
    revisions: list[int] = []
    for path in REVIEW_ROOT.glob(f"{target}_GATE_B_R*_REVIEW.md"):
        match = re.fullmatch(rf"{re.escape(target)}_GATE_B_R(\d+)_REVIEW\.md", path.name)
        if match:
            revision = int(match.group(1))
            manifest = VISUAL_ROOT / target / "gate_b_intact" / f"r{revision}" / "review_manifest.json"
            if manifest.is_file():
                revisions.append(revision)
    return sorted(set(revisions))


def _resolve_revision(target: str, status: str) -> int | None:
    pending = re.fullmatch(r"r(\d+)_rendered_pending_manual_review", status)
    if pending:
        return int(pending.group(1))

    # A state that explicitly demands revision N is a hard provenance barrier.
    # Do not fall back to an older manifest/review pair merely because it is the
    # newest pair currently persisted. This is what previously resurrected an
    # OWS-008 Gate-B r1 PASS while r2 was required after the stair-route repair.
    required = re.search(r"revision_required_r(\d+)", status)
    if required:
        revision = int(required.group(1))
        manifests = _manifest_revisions(target)
        reviews = _review_revisions(target)
        if revision not in manifests or revision not in reviews:
            return None
        return revision

    manifests = _manifest_revisions(target)
    reviews = _review_revisions(target)
    if not manifests or not reviews:
        return None

    latest_manifest = max(manifests)
    latest_review = max(reviews)
    if latest_manifest > latest_review:
        # Never let an older decision govern a newer artifact merely because some
        # other workflow damaged the state field.
        return None
    if latest_review != latest_manifest:
        return None
    return latest_review


def main() -> None:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    target = state.get("active_target", "")
    if not re.fullmatch(r"OWS-\d{3}", target):
        raise AssertionError(f"Invalid active target: {target!r}")

    gate = state.get("visual_review_gates", {}).get("gate_b_intact_state", {})
    status = str(gate.get("status", ""))
    if status.startswith("passed_"):
        print(f"{target} Gate B already recorded as {status}")
        return

    revision = _resolve_revision(target, status)
    if revision is None:
        manifests = _manifest_revisions(target)
        reviews = _review_revisions(target)
        print(
            f"{target} Gate-B recorder skipped: status={status}; "
            f"persisted_manifests={manifests}; reviewed_manifests={reviews}"
        )
        return

    manifest_path = VISUAL_ROOT / target / "gate_b_intact" / f"r{revision}" / "review_manifest.json"
    review_path = REVIEW_ROOT / f"{target}_GATE_B_R{revision}_REVIEW.md"
    if not manifest_path.is_file() or not review_path.is_file():
        print(
            f"{target} Gate-B explicit review/manifest not both present; "
            f"manifest={manifest_path.is_file()} review={review_path.is_file()}"
        )
        return

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("target") != target or manifest.get("gate") != "gate_b_intact":
        raise AssertionError(f"{target} Gate-B manifest identity mismatch: {manifest}")
    if f"intact-r{revision}@" not in str(manifest.get("revision", "")):
        raise AssertionError(f"{target} Gate-B manifest revision mismatch: {manifest.get('revision')}")

    review = review_path.read_text(encoding="utf-8")
    normalized = review.upper()
    passed = "**DECISION:** **PASSED**" in normalized
    revision_required = "**DECISION:** **REVISION REQUIRED**" in normalized
    if passed == revision_required:
        raise AssertionError(
            f"{target} Gate-B review must contain exactly one explicit PASSED or REVISION REQUIRED decision"
        )

    rel_review = str(review_path.relative_to(ROOT)).replace("\\", "/")
    gate[f"r{revision}_review_record"] = rel_review
    gate[f"r{revision}_decision"] = "PASSED" if passed else "REVISION REQUIRED"
    state.setdefault("planning_records", {})[f"gate_b_r{revision}_review"] = rel_review

    if revision_required:
        gate["status"] = "rerender_required"
        gate["decision"] = "REVISION REQUIRED"
        gate["significant_findings_corrected_or_justified"] = False
        state["active_target_passes"]["visual_gate_b_intact_state"] = f"revision_required_r{revision}"
        state["active_status"] = f"gate_b_r{revision}_revision_required"
        state["visual_review_gates"]["gate_b_intact_state"] = gate
        STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")
        print(f"Recorded explicit {target} Gate B r{revision} REVISION REQUIRED decision; rerender is authorized.")
        return

    expected = f"**{target} GATE B R{revision}: PASSED"
    if expected not in normalized:
        raise AssertionError(f"{target} Gate-B PASSED review lacks target/revision pass marker")

    gate["status"] = f"passed_r{revision}"
    gate["decision"] = "PASSED"
    gate["significant_findings_corrected_or_justified"] = True
    state["visual_review_gates"]["gate_b_intact_state"] = gate
    for key in INTACT_PASSES:
        state["active_target_passes"][key] = f"complete_gate_b_r{revision}"
    state["active_target_passes"]["visual_gate_b_intact_state"] = f"passed_r{revision}"
    if state["active_target_passes"].get("historical_layering") == "pending":
        state["active_target_passes"]["historical_layering"] = "ready"
    state["active_status"] = f"gate_b_r{revision}_passed_history_ready"

    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Recorded explicit {target} Gate B r{revision} PASSED decision; history passes may begin.")


if __name__ == "__main__":
    main()
