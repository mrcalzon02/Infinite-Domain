#!/usr/bin/env python3
"""Validate a regional material profile against the live block registry.

A material profile maps generator *roles* to blocks per architectural stratum.
This runs before any fabric pass (P3) and enforces two gate conditions from
the regional structure programs:

  1. Completeness  - every role resolves for every stratum the roster uses,
                     or is explicitly declared null for that stratum.
  2. Registry      - every block string, including every slab/stair/wall
                     derivative the generator is allowed to request, exists
                     in docs/registry-inventory/block-ids.txt.

A missing role or a missing derivative is a hard failure. There is no runtime
fallback: a generator that silently substitutes a block produces a region that
cannot be reasoned about.

Derivative naming is not uniform across this pack's mods. Immersive Engineering
uses a prefix form (slab_concrete); vanilla, Quark, TFMG and Supplementaries use
a suffix form (brick_slab). Both are declared in the profile's
`derivative_schemes` and tried in order, with `derivative_overrides` taking
precedence.

Authority: docs/KARSIC_DIRECTORATE_STRUCTURE_PROGRAM.md section 8.4
           docs/PELAGOS_COMPACT_STRUCTURE_PROGRAM.md section 8.4

Usage:
    python scripts/validate_material_profile.py --culture karsic
    python scripts/validate_material_profile.py --culture karsic --dump-resolution
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGIONAL = ROOT / "structure_library" / "regional"
DEFAULT_REGISTRY = ROOT / "docs" / "registry-inventory" / "block-ids.txt"

DERIVATIVE_KINDS = ("slab", "stairs", "wall")


def load_registry(path: Path) -> set[str]:
    return set(path.read_text(encoding="utf-8").split())


def singular(name: str) -> str:
    """bricks -> brick, shingles -> shingle, tiles -> tile."""
    return name[:-1] if name.endswith("s") else name


def resolve_derivative(block: str, kind: str, schemes: list[str], registry: set[str]) -> str | None:
    ns, _, name = block.partition(":")
    for scheme in schemes:
        candidate = scheme.format(ns=ns, name=name, singular=singular(name), kind=kind)
        if candidate in registry:
            return candidate
    return None


def validate(culture: str, registry_path: Path, dump: bool) -> tuple[dict[str, Any], list[str]]:
    profile_path = REGIONAL / f"{culture}-material-profile.json"
    if not profile_path.exists():
        return {}, [f"profile not found: {profile_path.relative_to(ROOT).as_posix()}"]

    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    registry = load_registry(registry_path)
    schemes: list[str] = profile["derivative_schemes"]
    strata: list[str] = profile["strata"]

    failures: list[str] = []
    resolution: dict[str, dict[str, Any]] = {}
    block_count = 0
    derivative_count = 0
    null_count = 0

    # --- roles, per stratum, with derivatives ------------------------------
    for role, spec in profile["roles"].items():
        by_stratum = spec.get("by_stratum", {})
        needs: list[str] = spec.get("needs", [])
        overrides: dict[str, dict[str, str]] = spec.get("derivative_overrides", {})

        for bad in set(needs) - set(DERIVATIVE_KINDS):
            failures.append(f"role '{role}' declares unknown derivative kind '{bad}'")

        missing_strata = [s for s in strata if s not in by_stratum]
        if missing_strata:
            failures.append(f"role '{role}' has no entry for stratum {missing_strata}")

        resolution[role] = {}
        for stratum in strata:
            block = by_stratum.get(stratum)
            if block is None:
                null_count += 1
                resolution[role][stratum] = None
                continue

            block_count += 1
            entry: dict[str, Any] = {"block": block}
            if block not in registry:
                failures.append(f"role '{role}' stratum {stratum}: block not in registry: {block}")

            for kind in needs:
                override = overrides.get(stratum, {}).get(kind)
                if override is not None:
                    if override not in registry:
                        failures.append(
                            f"role '{role}' stratum {stratum}: derivative override "
                            f"'{kind}' not in registry: {override}"
                        )
                    entry[kind] = override
                    entry.setdefault("overridden", []).append(kind)
                else:
                    found = resolve_derivative(block, kind, schemes, registry)
                    if found is None:
                        failures.append(
                            f"role '{role}' stratum {stratum}: no '{kind}' derivative for "
                            f"{block} under any declared scheme, and no override supplied"
                        )
                    entry[kind] = found
                derivative_count += 1

            resolution[role][stratum] = entry

    # --- flat block maps ---------------------------------------------------
    for section in ("openings", "site_kit", "furniture"):
        for name, block in profile.get(section, {}).items():
            block_count += 1
            if block not in registry:
                failures.append(f"{section}.{name}: block not in registry: {block}")

    # --- decay ladder ------------------------------------------------------
    for phase, entries in profile.get("decay", {}).items():
        for name, value in entries.items():
            if isinstance(value, str):
                block_count += 1
                if value not in registry:
                    failures.append(f"decay.{phase}.{name}: block not in registry: {value}")

    # --- ground contexts must exist in the primitives module ---------------
    primitives = (ROOT / "scripts" / "structure_geometry_primitives_v2.py").read_text(encoding="utf-8")
    for context in profile.get("ground_contexts", []):
        if f'"{context}"' not in primitives:
            failures.append(
                f"ground context '{context}' is not defined in "
                f"scripts/structure_geometry_primitives_v2.py _GROUND_PALETTES"
            )

    # --- moss affinity covers every stratum --------------------------------
    moss = profile.get("moss_affinity", {})
    for stratum in strata:
        if stratum not in moss:
            failures.append(f"moss_affinity has no entry for stratum {stratum}")

    report = {
        "purpose": "Material profile completeness and registry-existence gate. Runs before any fabric pass.",
        "authority": f"docs/{culture.upper()}_*_STRUCTURE_PROGRAM.md section 8.4",
        "culture": culture,
        "profile": profile_path.relative_to(ROOT).as_posix(),
        "registry": registry_path.relative_to(ROOT).as_posix(),
        "registry_block_count": len(registry),
        "strata": strata,
        "role_count": len(profile["roles"]),
        "blocks_checked": block_count,
        "derivatives_resolved": derivative_count,
        "null_role_slots": null_count,
        "passed": not failures,
        "failures": failures,
    }
    if dump:
        report["resolution"] = resolution
    return report, failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--culture", required=True, choices=["karsic", "pelagos"])
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--dump-resolution", action="store_true",
                        help="include the full role x stratum -> block resolution in the report")
    args = parser.parse_args()

    report, failures = validate(args.culture, args.registry, args.dump_resolution)
    out = ROOT / "docs" / f"{args.culture}-material-profile-validation.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")

    if not report:
        print("\n".join(failures))
        return 1

    print(f"culture              {report['culture']}")
    print(f"roles                {report['role_count']}")
    print(f"blocks checked       {report['blocks_checked']}")
    print(f"derivatives resolved {report['derivatives_resolved']}")
    print(f"null role slots      {report['null_role_slots']}")
    print()
    if failures:
        print(f"FAIL  {len(failures)} problem(s):")
        for failure in failures:
            print(f"  - {failure}")
    else:
        print("PASS  profile is complete and every block resolves against the registry")
    print(f"report: {out.relative_to(ROOT).as_posix()}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
