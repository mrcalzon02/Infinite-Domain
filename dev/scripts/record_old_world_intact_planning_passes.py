#!/usr/bin/env python3
"""[SYSTEM REPORT] Record completed Old World Passes 7-12 and open Gate B.

This utility does no visual approval. It verifies that Gate A is already passed and
that the active target has explicit completed Pass 7-12 records, then opens intact-
state implementation only when Gate B has not already advanced farther.

State transitions are monotonic: a rendered, rejected, rerender-required, or passed
Gate-B state is never downgraded back to planning-ready by a later workflow run.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STATE_PATH = ROOT / "dev/old_world_narrative" / "registry" / "heavy_rebuild_state.json"

PASS_RECORDS = {
    "structural_system": (7, "structural_system"),
    "circulation_and_access": (8, "circulation_and_access"),
    "exterior_architecture": (9, "exterior_architecture"),
    "interior_architecture": (10, "interior_architecture"),
    "operational_systems": (11, "operational_systems"),
    "institutional_identity": (12, "institutional_identity"),
}

OPENABLE_GATE_B_STATES = {
    "blocked_by_gate_a",
    "blocked_by_phase_0_and_planning",
    "blocked_by_passes_7_12",
    "pending",
    "ready_for_intact_implementation",
    "ready_to_render",
}


def _resolve_record(raw_path: str) -> Path:
    """Resolve both current dev-relative ledger paths and older repo-relative paths."""
    rel = Path(raw_path)
    candidates = (ROOT / rel, ROOT / "dev" / rel)
    for path in candidates:
        if path.is_file():
            return path
    raise AssertionError(f"Missing intact-planning record: {raw_path}")


def _assert_explicit_completion(path: Path, pass_number: int, target: str) -> None:
    text = path.read_text(encoding="utf-8")
    if f"**Target:** {target} " not in text and f"**Target:** {target} —" not in text:
        raise AssertionError(f"Pass {pass_number} record target mismatch: {path}")
    if "**Status:** COMPLETE FOR GATE-B R1 REVIEW" not in text:
        raise AssertionError(f"Pass {pass_number} record lacks explicit COMPLETE status: {path}")
    marker = rf"(?m)^\*\*PASS {pass_number}: COMPLETE FOR INDEPENDENT GATE-B REVIEW\.\*\*\s*$"
    if re.search(marker, text) is None:
        raise AssertionError(f"Pass {pass_number} record lacks explicit completion marker: {path}")


def main() -> None:
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    target = state.get("active_target")
    if not target:
        raise AssertionError("Heavy-rebuild state has no active target")

    gate_a = state.get("visual_review_gates", {}).get("gate_a_massing", {})
    if not str(gate_a.get("status", "")).startswith("passed_"):
        raise AssertionError(f"{target} Passes 7-12 cannot advance before Gate A passes")

    records = state.setdefault("planning_records", {})
    resolved: dict[str, str] = {}
    for pass_key, (pass_number, record_key) in PASS_RECORDS.items():
        raw_path = str(records.get(record_key, ""))
        if not raw_path:
            raise AssertionError(f"{target} ledger has no planning record for {record_key}")
        path = _resolve_record(raw_path)
        _assert_explicit_completion(path, pass_number, target)
        resolved[pass_key] = str(path.relative_to(ROOT)).replace("\\", "/")

    # OWS-008's original Pass-8 review predates a later-discovered eight-position
    # stair/headroom repair. Require the ledger's deterministic repair evidence
    # before treating that circulation definition as eligible for Gate-B r2.
    if target == "OWS-008":
        repair = state.get("active_shipping_repairs", {}).get("west_command_archive_stair", {})
        if not (
            str(repair.get("status", "")).startswith("verified_")
            and repair.get("upper_proof_route_connected") is True
            and repair.get("synthetic_pre_repair_delta_positions") == 8
        ):
            raise AssertionError("OWS-008 Pass 8 cannot reopen Gate B until the route repair is deterministically verified")

    # Preserve the authored paths already in the ledger while normalizing only
    # records that were absent; do not rewrite review evidence locations casually.
    for pass_key, (_, record_key) in PASS_RECORDS.items():
        if not records.get(record_key):
            records[record_key] = resolved[pass_key]

    gate_b = state["visual_review_gates"]["gate_b_intact_state"]
    current_gate_status = str(gate_b.get("status", ""))

    # The planning records may always be verified, but Gate-B execution/review
    # state is authoritative once it has moved beyond the planning-ready boundary.
    if current_gate_status not in OPENABLE_GATE_B_STATES:
        STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")
        print(
            f"Verified {target} Passes 7-12 planning records; preserved advanced Gate-B state "
            f"{current_gate_status!r} without downgrade."
        )
        return

    passes = state["active_target_passes"]
    for pass_key in PASS_RECORDS:
        passes[pass_key] = "defined_ready_for_gate_b_r2_implementation"
    passes["visual_gate_b_intact_state"] = "ready_for_intact_r2_implementation"

    gate_b["status"] = "ready_for_intact_r2_implementation"
    gate_b["rule"] = (
        "D0 r2 must prove the active target's complete intact operating architecture after all verified repairs: structural system, "
        "usable public/staff/service circulation, exterior and interior program, connected operational systems, institutional "
        "identity, maintenance access and all pre-existing boundaries needed by later history before damage, encounters or loot layers begin."
    )
    state["visual_review_gates"]["gate_b_intact_state"] = gate_b
    if not str(state.get("active_status", "")).startswith(("gate_b_r", "peak_quality_", "gate_c_")):
        state["active_status"] = "gate_b_r2_intact_ready_to_implement"

    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Verified {target} Passes 7-12 and repair prerequisites; Gate-B r2 intact implementation is ready.")


if __name__ == "__main__":
    main()
