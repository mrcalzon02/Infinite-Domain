#!/usr/bin/env python3
"""Import the approved Old World package and build its data-driven first slice."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROGRAM = ROOT / "old_world_narrative"
SOURCE = PROGRAM / "source"
REGISTRY = PROGRAM / "registry"
QUESTS = ROOT / "config" / "ftbquests" / "quests"
CHAPTER = QUESTS / "chapters" / "old_world_investigation.snbt"
LANG = QUESTS / "lang" / "en_us.snbt"
CHAPTER_GROUPS = QUESTS / "chapter_groups.snbt"
STARTUP = ROOT / "kubejs" / "startup_scripts" / "old_world_narrative_items.js"

CANON_SHA256 = "eec4d3149e5e5823b330d5b01127b8f6e592d1938ef4e491f719617e507bf182"
GROUP_ID = "4F574E0000000001"
CHAPTER_ID = "4F574E0000000002"
LANG_BEGIN = "\t// BEGIN GENERATED OLD WORLD NARRATIVE"
LANG_END = "\t// END GENERATED OLD WORLD NARRATIVE"

PACKAGE_TEXT_FILES = (
    "README_FIRST.md",
    "PACKAGE_INDEX.md",
    "01_CANON_AND_NONNEGOTIABLES.md",
    "02_TRANSITION_FROM_STRUCTURE_REVIEW.md",
    "03_STRUCTURE_REVISION_PROGRAM_UPDATED.md",
    "04_STRUCTURE_REVISION_MATRIX.csv",
    "04A_STRUCTURE_REVISION_MATRIX_GUIDE.md",
    "05_WRITTEN_LORE_NOVELS_AND_TEXTS.md",
    "05A_LORE_CORPUS_SEED.csv",
    "06_EXPLORATION_QUEST_INTEGRATION.md",
    "07_IMPLEMENTATION_AND_VALIDATION.md",
    "08_ADMIN_RECOVERY_AND_MULTIPLAYER.md",
    "09_AUTOMATION_STATE_TEMPLATE.json",
)

QUEST_SPINE = [
    ("OWQ-01", "THEY WERE HERE FIRST", "early Create/automation", ["OWS-009", "OWS-010", "OWS-012"]),
    ("OWQ-02", "FOOD FOR A BILLION", "farming/early industry", ["OWS-004"]),
    ("OWQ-03", "THE PERFECT CROP", "Food for a Billion", ["OWS-006", "OWS-007"]),
    ("OWQ-04", "UNEXPECTED MAINTENANCE", "early industrial recovery", ["OWS-015", "OWS-016", "OWS-034", "OWS-056"]),
    ("OWQ-05", "BOTH SIDES OF THE WALL", "midgame exploration", ["OWS-045"]),
    ("OWQ-06", "CONTINUITY", "Both Sides of the Wall", ["OWS-052"]),
    ("OWQ-07", "THE PERIMETER NEVER EXISTED", "multiple evidence families", ["OWS-053"]),
    ("OWQ-08", "A CURE FOR AGE", "advanced chemistry/medicine", ["OWS-029", "OWS-030", "OWS-032"]),
    ("OWQ-09", "THE GREY BLOOM", "Perfect Crop plus containment evidence", ["OWS-008", "OWS-047"]),
    ("OWQ-10", "FIREBREAK", "nuclear era", ["OWS-048", "OWS-049", "OWS-050"]),
    ("OWQ-11", "STOP BURNING IT", "Firebreak", ["OWS-051", "OWS-052"]),
    ("OWQ-12", "NINETEEN KILOMETERS", "Stop Burning It", ["OWS-051"]),
    ("OWQ-13", "THE FIREBREAK WARS", "Darknet capability", ["OWS-041", "OWS-042", "OWS-043"]),
]


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    path.write_text(normalized, encoding="utf-8", newline="\n")


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def import_package(package_root: Path) -> None:
    missing = [name for name in PACKAGE_TEXT_FILES if not (package_root / name).is_file()]
    if missing:
        raise FileNotFoundError("Old World package is missing: " + ", ".join(missing))
    SOURCE.mkdir(parents=True, exist_ok=True)
    for name in PACKAGE_TEXT_FILES:
        source_text = (package_root / name).read_text(encoding="utf-8-sig").rstrip() + "\n"
        write_text(SOURCE / name, source_text)

    canon = package_root / "source" / "Infinite Domain — Complete Old World Narrative and World-Integration Bible — CANON.docx"
    if not canon.is_file():
        raise FileNotFoundError(f"Missing canonical narrative bible: {canon}")
    actual = sha256(canon)
    if actual != CANON_SHA256:
        raise ValueError(f"Canonical narrative checksum mismatch: expected {CANON_SHA256}, found {actual}")

    write_json(
        SOURCE / "source-manifest.json",
        {
            "format_version": 1,
            "canon_docx_sha256": actual,
            "canon_docx_stored_in_repository": False,
            "canon_docx_note": "The supplied binary canon is checksum-pinned but remains outside the distributable source repository.",
            "imported_text_files": [
                {"path": name, "sha256": sha256(SOURCE / name)} for name in PACKAGE_TEXT_FILES
            ],
        },
    )


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def build_registries() -> None:
    matrix_path = SOURCE / "04_STRUCTURE_REVISION_MATRIX.csv"
    lore_path = SOURCE / "05A_LORE_CORPUS_SEED.csv"
    if not matrix_path.is_file() or not lore_path.is_file():
        raise FileNotFoundError("Import the supplied package before building Old World registries")

    targets = load_csv(matrix_path)
    if len(targets) != 64 or [row["id"] for row in targets] != [f"OWS-{index:03d}" for index in range(1, 65)]:
        raise ValueError("Structure revision matrix must contain the stable OWS-001 through OWS-064 sequence")

    for row in targets:
        row["implementation_status"] = "approved_for_mapping"
        row["mapped_source_structure"] = None
        row["narrative_structure"] = None
        row["acceptance_dimensions"] = []
        row["runtime_validation"] = "deferred"
    ows009 = targets[8]
    ows009.update(
        {
            "implementation_status": "implemented_static_runtime_deferred",
            "mapped_source_structure": "infinite_domain:service_garage_clean_master",
            "narrative_structure": "infinite_domain:old_world/ows_009_atlas_roadside_repair_depot",
            "narrative_source_template": "kubejs/data/infinite_domain/structure/wasteland/old_world/ows_009_atlas_roadside_repair_depot.nbt",
            "acceptance_dimensions": [
                "silhouette_exterior_identity",
                "interior_zoning_circulation",
                "functional_machinery_props",
                "institutional_identity",
                "narrative_evidence_loot",
            ],
        }
    )

    write_json(
        REGISTRY / "structure_targets.json",
        {
            "format_version": 1,
            "canon_sha256": CANON_SHA256,
            "target_count": len(targets),
            "source_inventory_approved_by_user": True,
            "targets": targets,
        },
    )

    lore = load_csv(lore_path)
    if len(lore) != 36:
        raise ValueError(f"Expected 36 required lore anchors, found {len(lore)}")
    write_json(
        REGISTRY / "lore_seed.json",
        {"format_version": 1, "minimum_completion_count": 96, "seed_count": len(lore), "records": lore},
    )

    write_json(
        REGISTRY / "quest_spine.json",
        {
            "format_version": 1,
            "major_quest_count": len(QUEST_SPINE),
            "quests": [
                {"id": qid, "title": title, "prerequisite": prerequisite, "target_structures": targets}
                for qid, title, prerequisite, targets in QUEST_SPINE
            ],
        },
    )

    write_json(
        REGISTRY / "implementation_state.json",
        {
            "format_version": 1,
            "canon_sha256": CANON_SHA256,
            "structure_handoff": {
                "catalog_count": 84,
                "reviewed_and_approved_by_user": True,
                "approval_date": "2026-08-19",
            },
            "targets_total": 64,
            "static_implemented": ["OWS-009"],
            "static_render_reviewed": ["OWS-009"],
            "runtime_verified": [],
            "current_wave": "representative_common_structure",
            "deferred_runtime_checks": [
                "fresh-world structure placement",
                "structure-map acquisition and destination",
                "FTB structure-task completion",
                "guaranteed proof chest acquisition",
                "multiplayer proof and quest behavior",
            ],
            "next_targets": ["OWS-001", "OWS-010", "OWS-015"],
        },
    )


def build_startup_items() -> None:
    write_text(
        STARTUP,
        """// Generated by scripts/build_old_world_narrative.py.
// Narrative evidence is non-craftable and structure-bound.
StartupEvents.registry('item', event => {
    event.create('atlas_service_plate')
        .displayName('Atlas Kinetic Service Plate')
        .texture('create:item/precision_mechanism')
        .rarity('uncommon')
        .glow(true)
        .maxStackSize(1)
        .tooltip('§6OWS-009 // Roadside Automated Repair Depot')
        .tooltip('§7Stamped to an Atlas Kinetic service frame recovered in situ')
        .tooltip('§8Quest proof — return this evidence to Charles')

    event.create('atlas_transfer_maintenance_manual')
        .displayName('Automated Transfer Maintenance Manual')
        .texture('minecraft:item/written_book')
        .rarity('uncommon')
        .maxStackSize(1)
        .tooltip('§6Atlas Kinetic Industries // Field Edition 6')
        .tooltip('§7Service lanes, transfer gearing, lockout procedure, and spare-shaft tolerances')
        .tooltip('§8LOR-006 // Early Old World industrial record')
})
""",
    )


def build_chapter() -> None:
    write_text(
        CHAPTER,
        f'''{{
\tdefault_hide_dependency_lines: false
\tdefault_quest_shape: "diamond"
\tfilename: "old_world_investigation"
\tgroup: "{GROUP_ID}"
\ticon: "kubejs:atlas_service_plate"
\tid: "{CHAPTER_ID}"
\timages: [ ]
\torder_index: 0
\tquest_links: [ ]
\tquests: [
\t\t{{
\t\t\tid: "4F57000000000001"
\t\t\trewards: [{{
\t\t\t\tcommand: "execute in minecraft:overworld run structure_map infinite_domain:old_world/ows_009_atlas_roadside_repair_depot 2"
\t\t\t\tfeedback_message: "infinite_domain.reward.explorer_map"
\t\t\t\tid: "70E823B42224CCBE"
\t\t\t\tpermission_level: 2
\t\t\t\tsilent: true
\t\t\t\ttype: "command"
\t\t\t}}]
\t\t\tshape: "gear"
\t\t\ttasks: [{{
\t\t\t\tid: "4F57800000000001"
\t\t\t\titem: {{ count: 1, id: "create:wrench" }}
\t\t\t\ttype: "item"
\t\t\t}}]
\t\t\tx: 0.0d
\t\t\ty: 0.0d
\t\t}}
\t\t{{
\t\t\tdependencies: ["4F57000000000001"]
\t\t\tid: "4F57000000000002"
\t\t\ttasks: [{{
\t\t\t\tid: "4F57800000000002"
\t\t\t\tstructure: "infinite_domain:old_world/ows_009_atlas_roadside_repair_depot"
\t\t\t\ttype: "structure"
\t\t\t}}]
\t\t\tx: 0.0d
\t\t\ty: 3.0d
\t\t}}
\t\t{{
\t\t\tdependencies: ["4F57000000000002"]
\t\t\ticon: "kubejs:atlas_service_plate"
\t\t\tid: "4F57000000000003"
\t\t\trewards: [
\t\t\t\t{{
\t\t\t\t\tid: "4F57900000000002"
\t\t\t\t\titem: {{ count: 4, id: "numismatics:cog" }}
\t\t\t\t\ttype: "item"
\t\t\t\t}}
\t\t\t\t{{
\t\t\t\t\tid: "4F57900000000003"
\t\t\t\t\titem: {{ count: 1, id: "create:precision_mechanism" }}
\t\t\t\t\ttype: "item"
\t\t\t\t}}
\t\t\t]
\t\t\tshape: "octagon"
\t\t\ttasks: [
\t\t\t\t{{
\t\t\t\t\tconsume_items: true
\t\t\t\t\tid: "4F57800000000003"
\t\t\t\t\titem: {{ count: 1, id: "kubejs:atlas_service_plate" }}
\t\t\t\t\ttype: "item"
\t\t\t\t}}
\t\t\t\t{{
\t\t\t\t\tid: "4F57800000000004"
\t\t\t\t\titem: {{ count: 1, id: "kubejs:atlas_transfer_maintenance_manual" }}
\t\t\t\t\ttype: "item"
\t\t\t\t}}
\t\t\t]
\t\t\tx: 0.0d
\t\t\ty: 6.0d
\t\t}}
\t]
}}
''',
    )

    groups = CHAPTER_GROUPS.read_text(encoding="utf-8-sig")
    if GROUP_ID not in groups:
        marker = "\t]\n}"
        if marker not in groups:
            raise ValueError("Could not find chapter_groups insertion point")
        groups = groups.replace(marker, f'\t\t{{ id: "{GROUP_ID}" }}\n{marker}')
        write_text(CHAPTER_GROUPS, groups)

    lang_entries = [
        f'\tchapter_group.{GROUP_ID}.title: "Old World Investigation"',
        f'\tchapter.{CHAPTER_ID}.title: "Old World Investigation"',
        f'\tchapter.{CHAPTER_ID}.subtitle: "Recover evidence where it was left; let the structures make the first argument."',
        '\tquest.4F57000000000001.title: "An Older Machine Language"',
        '\tquest.4F57000000000001.quest_desc: ["Build or recover a Create wrench before beginning the investigation. Familiar tools are the difference between archaeology and staring at a gearbox." "I have located an unusually intact roadside repair depot. Take the map. Do not dismantle the first machine you see merely because it has excellent brass fittings. — Charles"]',
        '\ttask.4F57800000000001.title: "Obtain a Create Wrench"',
        '\tquest.4F57000000000002.title: "Roadside Automated Repair Depot"',
        '\tquest.4F57000000000002.quest_desc: ["Travel to the mapped Atlas Kinetic depot and enter the registered structure." "Read the building before opening its records: three service lanes, inspection trenches, controlled parts storage, and mechanical transfer equipment. This was ordinary roadside infrastructure, not a secret laboratory."]',
        '\ttask.4F57800000000002.title: "Enter OWS-009"',
        '\tquest.4F57000000000003.title: "THEY WERE HERE FIRST"',
        '\tquest.4F57000000000003.quest_desc: ["Recover the stamped Atlas service plate and the transfer-maintenance manual from the depot records cage. The plate is consumed when submitted; the manual remains yours." "So. You are not inventing these principles from nothing. Atlas technicians standardized shafts, transfer lanes, service access, and lockout procedure long before the roads emptied. Recover their competence, not their complacency. — Charles"]',
        '\ttask.4F57800000000003.title: "Return the Atlas Service Plate to Charles"',
        '\ttask.4F57800000000004.title: "Recover the Atlas Maintenance Manual"',
    ]
    lang = LANG.read_text(encoding="utf-8-sig")
    if LANG_BEGIN in lang and LANG_END in lang:
        before, remainder = lang.split(LANG_BEGIN, 1)
        _, after = remainder.split(LANG_END, 1)
        lang = before.rstrip() + "\n" + after.lstrip("\n")
    closing = lang.rfind("}")
    if closing < 0:
        raise ValueError("FTB Quest language file has no closing compound")
    generated = LANG_BEGIN + "\n" + "\n".join(lang_entries) + "\n" + LANG_END + "\n"
    write_text(LANG, lang[:closing].rstrip() + "\n" + generated + lang[closing:])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-root", type=Path, help="Extracted package root to import before building")
    args = parser.parse_args()
    if args.package_root:
        import_package(args.package_root.resolve())
    build_registries()
    build_startup_items()
    build_chapter()
    print("Built Old World registries and representative OWS-009 quest/item slice.")


if __name__ == "__main__":
    main()
