"""Validate the generated Domain Compendium chapter against the candidate audit.

Checks structure, id hygiene, that every task item is a real registered id in the
`include` set (no phantom AllTheCompressed / Ex Deorum variants), exact coverage
(every eligible id catalogued exactly once), dependency wiring, and localisation.

Exit 0 = pass. Run after scripts/generators/build_domain_compendium_chapter.py.
Authority: docs/DOMAIN_COMPENDIUM_CHAPTER.md
"""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = ROOT / "docs/domain-compendium/candidate-inventory.csv"
CHAPTER = ROOT / "config/ftbquests/quests/chapters/domain_compendium.snbt"
LANG = ROOT / "config/ftbquests/quests/lang/en_us.snbt"
GROUPS = ROOT / "config/ftbquests/quests/chapter_groups.snbt"
REGISTRY = ROOT / "docs/registry-inventory"

EXCLUDED_NAMESPACES = {"rechiseled", "rechiseledcreate"}
GROUP_ID = "7C0DEC0FFEE00001"
CHAPTER_ID = "7C0DE0C000000000"
ROOT_QUEST_ID = "7C0DE0C000000001"
CAPSTONE_QUEST_ID = "7C0DE0C0000000FF"


def read_ids(name: str) -> set[str]:
    return {
        line.strip()
        for line in (REGISTRY / name).read_text(encoding="utf-8-sig").splitlines()
        if line.strip() and ":" in line
    }


def main() -> int:
    failures: list[str] = []
    chapter = CHAPTER.read_text(encoding="utf-8")
    lang = LANG.read_text(encoding="utf-8")
    groups = GROUPS.read_text(encoding="utf-8")

    # ---- expected id set -------------------------------------------------
    eligible: set[str] = set()
    with CANDIDATES.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["decision"] == "include" and row["namespace"] not in EXCLUDED_NAMESPACES:
                eligible.add(row["id"])

    registered = read_ids("item-ids.txt") | read_ids("block-ids.txt")

    # ---- structure ------------------------------------------------------
    if chapter.count("{") != chapter.count("}"):
        failures.append(f"brace mismatch: {chapter.count('{')} open vs {chapter.count('}')} close")
    if f'id: "{CHAPTER_ID}"' not in chapter:
        failures.append("chapter id missing")
    if f'group: "{GROUP_ID}"' not in chapter:
        failures.append("chapter not bound to the compendium group")
    if f'{{ id: "{GROUP_ID}" }}' not in groups:
        failures.append("compendium group not registered in chapter_groups.snbt")

    # ---- tasks --------------------------------------------------------
    task_pairs = re.findall(
        r'id: "(7C0DE2[0-9A-F]{10})", item: \{ count: 1, id: "([^"]+)" \}, type: "item"',
        chapter,
    )
    task_ids = [pair[0] for pair in task_pairs]
    task_items = [pair[1] for pair in task_pairs]
    all_task_id_tokens = re.findall(r'id: "(7C0DE2[0-9A-F]{10})"', chapter)
    quest_ids = re.findall(r'\n\t\t\tid: "([0-9A-F]{16})"', chapter)

    if len(all_task_id_tokens) != len(task_pairs):
        failures.append(
            f"task id / item mismatch: {len(all_task_id_tokens)} task ids, {len(task_pairs)} well-formed item tasks"
        )
    if len(set(task_ids)) != len(task_ids):
        failures.append("duplicate task ids")
    if len(set(quest_ids)) != len(quest_ids):
        failures.append("duplicate quest ids")

    catalogued = set(task_items)
    if len(catalogued) != len(task_items):
        dupes = [i for i in catalogued if task_items.count(i) > 1][:5]
        failures.append(f"item catalogued more than once (e.g. {dupes})")

    unregistered = sorted(i for i in catalogued if i not in registered)
    if unregistered:
        failures.append(f"{len(unregistered)} task items are not registered ids (e.g. {unregistered[:5]})")

    not_eligible = sorted(i for i in catalogued if i not in eligible)
    if not_eligible:
        failures.append(f"{len(not_eligible)} task items are not in the include set (e.g. {not_eligible[:5]})")

    missing = sorted(eligible - catalogued)
    if missing:
        failures.append(f"{len(missing)} eligible ids are not catalogued (e.g. {missing[:5]})")

    bad_ns = sorted({i.split(':', 1)[0] for i in catalogued} & EXCLUDED_NAMESPACES)
    if bad_ns:
        failures.append(f"excluded namespace present: {bad_ns}")

    phantom = sorted(
        i for i in catalogued
        if i.split(":", 1)[0] == "allthecompressed" and _atc_phantom(i)
    )
    if phantom:
        failures.append(f"AllTheCompressed phantom family catalogued (e.g. {phantom[:5]})")

    # ---- id hygiene --------------------------------------------------
    for identifier in set(task_ids) | set(quest_ids):
        if not re.fullmatch(r"[0-7][0-9A-F]{15}", identifier):
            failures.append(f"id not a positive 16-hex long: {identifier}")
            break

    # ---- dependency wiring -----------------------------------------
    section_ids = [q for q in quest_ids if q.startswith("7C0DE1")]
    if not section_ids:
        failures.append("no section quests found")
    capstone_block = _block(chapter, CAPSTONE_QUEST_ID)
    for sid in section_ids:
        if f'"{sid}"' not in capstone_block:
            failures.append(f"capstone does not depend on section {sid}")
            break
    for sid in section_ids[:1] + section_ids[-1:]:
        if f'dependencies: ["{ROOT_QUEST_ID}"]' not in _block(chapter, sid):
            failures.append(f"section {sid} does not depend on the root quest")

    # ---- localisation ---------------------------------------------
    for key in (
        f"chapter.{CHAPTER_ID}.title:",
        f"chapter.{CHAPTER_ID}.subtitle:",
        f"chapter_group.{GROUP_ID}.title:",
        f"quest.{ROOT_QUEST_ID}.title:",
        f"quest.{CAPSTONE_QUEST_ID}.title:",
    ):
        if key not in lang:
            failures.append(f"missing lang key {key}")
    for sid in section_ids:
        if f"quest.{sid}.title:" not in lang:
            failures.append(f"section {sid} has no title")
            break

    # ---- report --------------------------------------------------
    print(f"catalogued items:      {len(catalogued):,}")
    print(f"eligible (include set): {len(eligible):,}")
    print(f"section quests:        {len(section_ids)}")
    print(f"chapter file:          {len(chapter):,} bytes")
    if failures:
        print()
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1
    print("\nPASS: Domain Compendium chapter matches the candidate audit exactly.")
    return 0


_ATC_OK: set[str] | None = None


def _atc_phantom(identifier: str) -> bool:
    global _ATC_OK
    if _ATC_OK is None:
        path = ROOT / "docs/domain-compendium/allthecompressed-families.csv"
        _ATC_OK = set()
        if path.is_file():
            with path.open(encoding="utf-8", newline="") as handle:
                for row in csv.DictReader(handle):
                    if row["base_resolves"] == "True":
                        _ATC_OK.add(row["family"])
    match = re.fullmatch(r"allthecompressed:(.+)_\d+x", identifier)
    return bool(match) and match.group(1) not in _ATC_OK


def _block(text: str, quest_id: str) -> str:
    pos = text.find(f'id: "{quest_id}"')
    if pos < 0:
        return ""
    start = text.rfind("\n\t\t{", 0, pos)
    end = text.find("\n\t\t}", pos)
    return text[start:end + 4] if start >= 0 and end >= 0 else ""


if __name__ == "__main__":
    raise SystemExit(main())
