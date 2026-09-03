#!/usr/bin/env python3
"""Run the complete deterministic OWS-009 Gate-A r2 preflight suite.

This is the single fail-fast entrypoint for machine-resolvable Gate-A checks.
It deliberately does not render review imagery and cannot approve visual quality,
Minecraft runtime placement, Lost Cities coexistence, generated-world terrain
adaptation, shipping-NBT placement/transform behavior, gameplay hooks, or final
production admission.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = ROOT / "dev/scripts"
CHECKS = (
    "verify_ows009_gate_a_static.py",
    "verify_ows009_gate_a_vehicle_access.py",
    "verify_ows009_gate_a_transforms.py",
    "verify_ows009_gate_a_articulation.py",
    "verify_ows009_gate_a_load_paths.py",
    "verify_ows009_gate_a_foundation_grade.py",
)


def _assert_suite_files_present() -> None:
    missing = [name for name in CHECKS if not (SCRIPT_DIR / name).is_file()]
    if missing:
        raise AssertionError(f"OWS-009 Gate-A suite is incomplete; missing: {missing}")


def main() -> None:
    _assert_suite_files_present()

    failures: list[tuple[str, int]] = []
    for name in CHECKS:
        path = SCRIPT_DIR / name
        print(f"[OWS-009 Gate-A r2] RUN {name}", flush=True)
        result = subprocess.run(
            [sys.executable, str(path)],
            cwd=ROOT,
            check=False,
        )
        if result.returncode != 0:
            failures.append((name, result.returncode))
            print(
                f"[OWS-009 Gate-A r2] FAIL {name} (exit {result.returncode}); "
                "remaining deterministic checks are not promoted as a suite pass.",
                file=sys.stderr,
                flush=True,
            )
            break
        print(f"[OWS-009 Gate-A r2] PASS {name}", flush=True)

    if failures:
        name, code = failures[0]
        raise SystemExit(
            f"OWS-009 Gate-A r2 deterministic suite FAILED at {name} "
            f"(exit {code})."
        )

    print(
        "OWS-009 Gate-A r2 deterministic suite PASS: source provenance, template "
        "bounds, protected terrain edges, circulation, vehicle swept volumes, "
        "rotation/mirroring coordinate safety, architectural articulation, "
        "structural load paths, and foundation/grade interfaces all passed their "
        "repository-local preflights. This does NOT constitute Gate-A visual "
        "acceptance, Minecraft runtime/new-world acceptance, Lost Cities "
        "coexistence, shipping-NBT transform/placement acceptance, gameplay-hook "
        "validation, or production admission."
    )


if __name__ == "__main__":
    main()
