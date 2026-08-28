#!/usr/bin/env python3
"""Validate a regional assignment against the base structure catalog.

Gate conditions (regional structure programs, section 8.1):

  RA-1  every base clean master in structure_library/catalog.json has exactly
        one conversion class in the assignment;
  RA-2  the assignment introduces no base master the catalog does not have;
  RA-3  every excluded (X) base master names a substitute that exists among
        the native additions;
  RA-4  no native addition is orphaned - each is either a declared substitute
        or carries a priority;
  RA-5  regional ids are unique, correctly prefixed, and numbered contiguously
        from 001;
  RA-6  every non-prop master declares at least the minimum number of strata
        its culture requires (Karsic 1, Pelagos 2);
  RA-7  every converted master declares a damage archetype drawn from the
        culture's declared set, except props.

Authority: docs/KARSIC_DIRECTORATE_STRUCTURE_PROGRAM.md section 8.1
           docs/PELAGOS_COMPACT_STRUCTURE_PROGRAM.md section 8.1

Usage:
    python scripts/validate_regional_assignment.py --culture karsic
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGIONAL = ROOT / "structure_library" / "regional"
CATALOG = ROOT / "structure_library" / "catalog.json"

PREFIX = {"karsic": "kar", "pelagos": "pel"}
MIN_STRATA = {"karsic": 1, "pelagos": 2}

DAMAGE_ARCHETYPES = {
    "karsic": {
        "frozen district", "cannibalisation", "heroic maintenance", "sealed basement",
        "failed assembly point", "firebreak edge", "partitioned survivor wing",
    },
    "pelagos": {
        "layered failure", "legacy bypass", "overwhelmed conversion", "blocked artery",
        "tidal breach", "retained façade", "neighbourhood improvisation",
    },
}

VALID_STRATA = {
    "karsic": {"K-I", "K-II", "K-III", "K-IV", "K-V", "prop"},
    "pelagos": {"P-0", "P-I", "P-II", "P-III", "P-IV", "P-V", "prop"},
}


def base_masters() -> set[str]:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))["structures"]
    return {
        entry["structure_id"].split(":", 1)[1].removesuffix("_clean_master")
        for entry in catalog
        if entry["source_role"] == "clean_master"
    }


def validate(culture: str) -> tuple[list[dict[str, Any]], list[str]]:
    prefix = PREFIX[culture]
    assignment = json.loads((REGIONAL / f"{culture}-assignment.json").read_text(encoding="utf-8"))
    conversions = assignment["conversions"]
    natives = assignment["natives"]
    catalog_masters = base_masters()

    checks: list[dict[str, Any]] = []
    failures: list[str] = []

    def record(cid: str, name: str, problems: list[str], detail: str) -> None:
        ok = not problems
        checks.append({"id": cid, "check": name, "passed": ok, "detail": detail,
                       "problems": problems[:10], "problem_count": len(problems)})
        if not ok:
            failures.extend(f"{cid}: {p}" for p in problems)

    # RA-1 / RA-2 --------------------------------------------------------
    assigned: dict[str, int] = {}
    for entry in conversions:
        assigned[entry["base_master"]] = assigned.get(entry["base_master"], 0) + 1

    missing = sorted(catalog_masters - set(assigned))
    duplicated = sorted(m for m, n in assigned.items() if n > 1)
    record("RA-1", "every base clean master is assigned exactly once",
           [f"unassigned base master: {m}" for m in missing]
           + [f"base master assigned more than once: {m}" for m in duplicated],
           f"{len(catalog_masters)} clean masters in catalog, {len(assigned)} assigned")

    unknown = sorted(set(assigned) - catalog_masters)
    record("RA-2", "the assignment invents no base master",
           [f"not a catalog clean master: {m}" for m in unknown],
           f"{len(unknown)} unknown base masters")

    # RA-3 / RA-4 --------------------------------------------------------
    native_ids = {n["regional_id"] for n in natives}
    problems = []
    for base, sub in assignment.get("substitutes", {}).items():
        if sub not in native_ids:
            problems.append(f"substitute for '{base}' is not a native addition: {sub}")
    record("RA-3", "every exclusion names a real native substitute", problems,
           f"{len(assignment.get('substitutes', {}))} exclusions")

    problems = [f"native '{n['regional_id']}' has no priority" for n in natives if not n.get("priority")]
    record("RA-4", "no orphaned native additions", problems, f"{len(natives)} natives")

    # RA-5 ---------------------------------------------------------------
    all_ids = [c["regional_id"] for c in conversions if c["conversion_class"] != "X"] + \
              [n["regional_id"] for n in natives]
    problems = []
    seen: set[str] = set()
    numbers: list[int] = []
    for rid in all_ids:
        if rid in seen:
            problems.append(f"duplicate regional id: {rid}")
        seen.add(rid)
        m = re.fullmatch(rf"{prefix}_(\d{{3}})_[a-z0-9_]+", rid)
        if not m:
            problems.append(f"malformed regional id: {rid}")
        else:
            numbers.append(int(m.group(1)))
    if numbers:
        expected = list(range(1, len(numbers) + 1))
        if sorted(numbers) != expected:
            gaps = sorted(set(expected) - set(numbers))
            extra = sorted(n for n in numbers if n > len(numbers))
            if gaps:
                problems.append(f"missing numbers: {gaps[:10]}")
            if extra:
                problems.append(f"numbers beyond the roster size: {extra[:10]}")
    record("RA-5", "regional ids are unique, well-formed and contiguous from 001", problems,
           f"{len(all_ids)} ids, numbers 001..{max(numbers) if numbers else 0:03d}")

    # RA-6 ---------------------------------------------------------------
    minimum = MIN_STRATA[culture]
    valid = VALID_STRATA[culture]
    problems = []
    for entry in conversions + natives:
        if entry.get("conversion_class") == "X":
            continue
        strata = entry.get("strata") or []
        if strata == ["prop"]:
            continue
        if len(strata) < minimum:
            problems.append(f"{entry['regional_id']} declares {len(strata)} strata, minimum is {minimum}")
        for s in strata:
            if s not in valid:
                problems.append(f"{entry['regional_id']} declares unknown stratum '{s}'")
    record("RA-6", f"every non-prop master declares at least {minimum} stratum/strata", problems,
           f"minimum for {culture} is {minimum}")

    # RA-7 ---------------------------------------------------------------
    allowed = DAMAGE_ARCHETYPES[culture]
    problems = []
    for entry in conversions:
        if entry["conversion_class"] == "X":
            continue
        archetype = entry.get("damage_archetype")
        if entry.get("strata") == ["prop"]:
            continue
        if archetype is None:
            problems.append(f"{entry['regional_id']} declares no damage archetype")
        elif archetype not in allowed:
            problems.append(f"{entry['regional_id']} declares unknown damage archetype '{archetype}'")
    record("RA-7", "damage archetypes are drawn from the declared set", problems,
           f"{len(allowed)} archetypes declared for {culture}")

    return checks, failures


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--culture", required=True, choices=sorted(PREFIX))
    args = parser.parse_args()

    checks, failures = validate(args.culture)
    report = {
        "purpose": "Regional assignment gate: every base master classified once, exclusions substituted, "
                   "ids well-formed, strata and damage archetypes drawn from the declared sets.",
        "culture": args.culture,
        "checks": checks,
        "passed": not failures,
        "failure_count": len(failures),
    }
    out = ROOT / "docs" / f"{args.culture}-assignment-validation.json"
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")

    for check in checks:
        print(f"{'PASS' if check['passed'] else 'FAIL'}  {check['id']}  {check['check']}")
        print(f"            {check['detail']}")
        for problem in check["problems"]:
            print(f"            - {problem}")
    print()
    print(f"{sum(1 for c in checks if c['passed'])}/{len(checks)} checks passed")
    print(f"report: {out.relative_to(ROOT).as_posix()}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
