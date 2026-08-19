from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "structure_library" / "reviews" / "creativelands_cc0" / "catalog.json"
OUTPUT = ROOT / "structure_library" / "refinement" / "phase16-selection.json"
MARKDOWN = ROOT / "structure_library" / "refinement" / "PHASE16_SELECTION.md"


def disposition(entry: dict) -> tuple[str, str, int]:
    structure_id = entry["structure_id"]
    category = entry["category"]
    if structure_id == "creativelands_cc0:houses/mansion":
        return (
            "reference_only",
            "layout reference only: useful interior zoning, but not aligned enough with the wasteland urban/industrial program to justify normalization",
            90,
        )
    if category == "houses":
        return (
            "reference_only",
            "generic residential reference with insufficient value to displace purpose-built inbuilt rebuilding",
            91,
        )
    if category == "structures/village" and not structure_id.endswith("/village2"):
        return (
            "reference_only",
            "generic village shell; retain only as low-priority reference rather than normalization input",
            92,
        )
    if category == "decorations":
        return (
            "module_quarry",
            "terrain-detail geometry; classify footprint and terrain connector before module admission",
            4,
        )
    if category == "ruins":
        return (
            "module_quarry",
            "masonry damage and overgrowth vocabulary; do not treat as a complete building",
            5,
        )
    if category == "ruined_portal":
        return (
            "reference_only",
            "Nether-specific geometry does not justify a module-extraction pass for the wasteland program",
            96,
        )
    if category == "structures/swamp":
        return (
            "reference_only",
            "generic stilt geometry offers insufficient value for purpose-specific rebuilding",
            97,
        )
    return (
        "reference_only",
        "vanilla-fantasy, monolithic, connector-only or otherwise outside the wasteland architectural program",
        99,
    )


def main() -> None:
    entries = json.loads(CATALOG.read_text(encoding="utf-8"))["entries"]
    selections = []
    for entry in entries:
        status, reason, priority = disposition(entry)
        selections.append(
            {
                "structure_id": entry["structure_id"],
                "source_category": entry["category"],
                "dimensions": entry["dimensions"],
                "blocks": entry["blocks"],
                "disposition": status,
                "priority": priority,
                "reason": reason,
                "normalization_status": "pending" if status == "architectural_clean_reference" else "not_scheduled",
                "module_status": "candidate_not_extracted" if status == "module_quarry" else "not_applicable",
                "production_approved": False,
            }
        )
    selections.sort(key=lambda item: (item["priority"], item["structure_id"]))
    counts = Counter(item["disposition"] for item in selections)
    document = {
        "format_version": 1,
        "purpose": "Phase 16 retention/module selection. This is not production approval.",
        "source_catalog": "structure_library/reviews/creativelands_cc0/catalog.json",
        "existing_inbuilt_rebuild_queue": "structure_library/rebuild-phases.json",
        "queue_rule": "External references inform but do not displace the inbuilt gas-station/freight-depot rebuild queue.",
        "counts": dict(sorted(counts.items())),
        "production_approved": 0,
        "selections": selections,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Phase 16 Creative Lands Selection",
        "",
        "Every converted CC0 review asset has exactly one disposition. No disposition is production approval.",
        "",
        f"- Architectural clean references: {counts.get('architectural_clean_reference', 0)}",
        f"- Module quarries: {counts.get('module_quarry', 0)}",
        f"- Reference only: {counts.get('reference_only', 0)}",
        "- Production approvals: 0",
        "",
        "No Creative Lands asset is scheduled for normalization. The inbuilt Phase 2 gas-station/freight-depot queue remains authoritative.",
        "",
        "| Priority | ID | Disposition | Reason |",
        "|---:|---|---|---|",
    ]
    for item in selections:
        lines.append(
            f"| {item['priority']} | `{item['structure_id']}` | `{item['disposition']}` | {item['reason']} |"
        )
    MARKDOWN.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Classified {len(selections)} Creative Lands review assets for Phase 16: {dict(counts)}")


if __name__ == "__main__":
    main()
