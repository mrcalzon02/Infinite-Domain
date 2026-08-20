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

IMPLEMENTED_TARGETS = {
    "OWS-001": {
        "source": "infinite_domain:grocery_clean_master",
        "name": "ows_001_vcf_neighborhood_culture_service_depot",
        "dimensions": ["silhouette_exterior_identity", "interior_zoning_circulation", "functional_machinery_props", "institutional_identity", "historical_damage_signature", "narrative_evidence_loot"],
    },
    "OWS-002": {
        "source": "infinite_domain:ruined_community_center_clean_master",
        "name": "ows_002_vcf_emergency_community_grow_hall",
        "dimensions": ["silhouette_exterior_identity", "interior_zoning_circulation", "functional_machinery_props", "institutional_identity", "historical_damage_signature", "narrative_evidence_loot"],
    },
    "OWS-003": {
        "source": "infinite_domain:abandoned_orchard_cannery_clean_master",
        "name": "ows_003_vcf_cold_chain_culture_nursery",
        "dimensions": ["silhouette_exterior_identity", "interior_zoning_circulation", "functional_machinery_props", "institutional_identity", "historical_damage_signature", "narrative_evidence_loot"],
    },
    "OWS-004": {
        "source": "infinite_domain:ruined_office_tower_clean_master",
        "name": "ows_004_vcf_mycological_vertical_farm_tower",
        "dimensions": ["silhouette_exterior_identity", "interior_zoning_circulation", "functional_machinery_props", "institutional_identity", "historical_damage_signature", "narrative_evidence_loot"],
    },
    "OWS-006": {
        "source": "infinite_domain:ruined_cyberware_clinic_clean_master",
        "name": "ows_006_vcf_pt9_symbiosis_pilot_laboratory",
        "dimensions": ["silhouette_exterior_identity", "interior_zoning_circulation", "functional_machinery_props", "institutional_identity", "historical_damage_signature", "narrative_evidence_loot"],
    },
    "OWS-009": {
        "source": "infinite_domain:service_garage_clean_master",
        "name": "ows_009_atlas_roadside_repair_depot",
        "dimensions": ["silhouette_exterior_identity", "interior_zoning_circulation", "functional_machinery_props", "institutional_identity", "narrative_evidence_loot"],
    },
    "OWS-010": {
        "source": "infinite_domain:corporate_warehouse_clean_master",
        "name": "ows_010_atlas_conveyor_transfer_hall",
        "dimensions": ["silhouette_exterior_identity", "interior_zoning_circulation", "functional_machinery_props", "institutional_identity", "historical_damage_signature", "narrative_evidence_loot"],
    },
    "OWS-012": {
        "source": "infinite_domain:abandoned_quarry_clean_master",
        "name": "ows_012_atlas_bulk_crushing_preparation_plant",
        "dimensions": ["silhouette_exterior_identity", "interior_zoning_circulation", "functional_machinery_props", "institutional_identity", "historical_damage_signature", "narrative_evidence_loot"],
    },
    "OWS-015": {
        "source": "infinite_domain:wasteland_water_tower_clean_master",
        "name": "ows_015_polycore_utility_seal_failure_station",
        "dimensions": ["silhouette_exterior_identity", "interior_zoning_circulation", "functional_machinery_props", "institutional_identity", "historical_damage_signature", "narrative_evidence_loot"],
    },
    "OWS-016": {
        "source": "infinite_domain:mountain_biohazard_lab_clean_master",
        "name": "ows_016_polycore_elastomer_exposure_array",
        "dimensions": ["silhouette_exterior_identity", "interior_zoning_circulation", "functional_machinery_props", "institutional_identity", "historical_damage_signature", "narrative_evidence_loot"],
    },
}


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
    for target_id, implementation in IMPLEMENTED_TARGETS.items():
        row = targets[int(target_id[-3:]) - 1]
        name = implementation["name"]
        row.update({
            "implementation_status": "implemented_static_runtime_deferred",
            "mapped_source_structure": implementation["source"],
            "narrative_structure": f"infinite_domain:old_world/{name}",
            "narrative_source_template": f"kubejs/data/infinite_domain/structure/wasteland/old_world/{name}.nbt",
            "acceptance_dimensions": implementation["dimensions"],
        })

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
            "static_implemented": list(IMPLEMENTED_TARGETS),
            "static_render_reviewed": list(IMPLEMENTED_TARGETS),
            "runtime_verified": [],
            "current_wave": "quest_critical_food_symbiosis_and_bulk_processing_wave",
            "deferred_runtime_checks": [
                "fresh-world structure placement",
                "structure-map acquisition and destination",
                "FTB structure-task completion",
                "guaranteed proof chest acquisition",
                "multiplayer proof and quest behavior",
            ],
            "next_targets": ["OWS-005", "OWS-007", "OWS-013"],
        },
    )


def build_startup_items() -> None:
    write_text(
        STARTUP,
        """// Generated by scripts/build_old_world_narrative.py.
// Narrative evidence is non-craftable and structure-bound.
StartupEvents.registry('item', event => {
    event.create('vcf_culture_service_manifest')
        .displayName('VCF Neighborhood Culture-Service Manifest')
        .texture('minecraft:item/map').rarity('uncommon').glow(true).maxStackSize(1)
        .tooltip('§aOWS-001 // Controlled culture issue and return ledger')
        .tooltip('§7Evercrop cultures were neighborhood infrastructure, not rare prototypes')
        .tooltip('§8Quest proof — return this evidence to Charles')

    event.create('vcf_return_crate_log')
        .displayName('VCF Return-Crate Exception Log')
        .texture('minecraft:item/written_book').rarity('uncommon').maxStackSize(1)
        .tooltip('§aVCF Culture Services // early anomaly record')
        .tooltip('§7Spoiled seals and delayed returns begin appearing on an otherwise ordinary route')

    event.create('emergency_grow_authorization')
        .displayName('Municipal Emergency Grow Authorization')
        .texture('minecraft:item/map').rarity('uncommon').glow(true).maxStackSize(1)
        .tooltip('§aOWS-002 // VCF emergency community grow hall')
        .tooltip('§7Authorizes public relief cultivation using VCF Evercrop culture kits')
        .tooltip('§8Quest proof — return this evidence to Charles')

    event.create('vcf_culture_batch_record')
        .displayName('VCF Dormant Culture Batch Record')
        .texture('create:item/clipboard').rarity('rare').glow(true).maxStackSize(1)
        .tooltip('§aOWS-003 // cold-chain culture nursery')
        .tooltip('§7Tracks culture dormancy, seal inspection, quarantine, and global dispatch')
        .tooltip('§8Quest proof — return this evidence to Charles')

    event.create('vcf_global_licensing_brief')
        .displayName('VCF Global Licensing Brief')
        .texture('minecraft:item/written_book').rarity('rare').maxStackSize(1)
        .tooltip('§aLOR-005 // worldwide Evercrop distribution')
        .tooltip('§7The cultures crossed every perimeter before the crisis had a name')

    event.create('evercrop_cultivation_handbook')
        .displayName('EVERCROP Industrial Cultivation Handbook')
        .texture('minecraft:item/written_book').rarity('rare').glow(true).maxStackSize(1)
        .tooltip('§aOWS-004 / LOR-001 // Mycological Vertical Farm Tower')
        .tooltip('§7Benign optimism, extraordinary yield, and a production system built for billions')
        .tooltip('§8Quest-critical proof — return this evidence to Charles')

    event.create('pt9_symbiosis_report')
        .displayName('VCF PT-9 Symbiosis Report')
        .texture('create:item/clipboard').rarity('epic').glow(true).maxStackSize(1)
        .tooltip('§aOWS-006 / LOR-003 // PT-9 pilot laboratory')
        .tooltip('§7Bacterial protection confirmed; polymer degradation entered as an unresolved observation')
        .tooltip('§8Quest-critical proof — return this evidence to Charles')

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

    event.create('atlas_transfer_maintenance_card')
        .displayName('Atlas Transfer-Hall Maintenance Card')
        .texture('create:item/schedule').rarity('uncommon').glow(true).maxStackSize(1)
        .tooltip('§6OWS-010 // Conveyor Transfer Hall')
        .tooltip('§7Lane tolerances and lockout intervals match the machines you now build')
        .tooltip('§8Quest proof — return this evidence to Charles')

    event.create('atlas_bulk_process_manual')
        .displayName('Atlas Bulk Crushing and Preparation Manual')
        .texture('create:item/schedule').rarity('rare').glow(true).maxStackSize(1)
        .tooltip('§6OWS-012 // quarry bulk-preparation plant')
        .tooltip('§7Crushing, milling, mixing, dust control, and service intervals at industrial scale')
        .tooltip('§8Quest proof — return this evidence to Charles')

    event.create('polycore_seal_failure_report')
        .displayName('PolyCore Utility Seal Failure Report')
        .texture('minecraft:item/map').rarity('rare').glow(true).maxStackSize(1)
        .tooltip('§dOWS-015 // Utility Seal Failure Station')
        .tooltip('§7Routine gasket replacements accelerated into a system-wide material crisis')
        .tooltip('§8Quest proof — return this evidence to Charles')

    event.create('polycore_service_interval_board')
        .displayName('PolyCore Seal Replacement Interval Board')
        .texture('create:item/clipboard').rarity('rare').maxStackSize(1)
        .tooltip('§dLOR-008 // shrinking service intervals')
        .tooltip('§7Twelve months. Six. Three. Weekly. Then blank.')

    event.create('polycore_elastomer_exposure_test')
        .displayName('PolyCore Elastomer Exposure Authorization')
        .texture('create:item/clipboard').rarity('rare').glow(true).maxStackSize(1)
        .tooltip('§dOWS-016 // parallel exposure array')
        .tooltip('§7Four controlled chambers; four repetitions of the same biological degradation')
        .tooltip('§8Quest proof — return this evidence to Charles')

    event.create('polycore_exposure_test_04')
        .displayName('PolyCore Elastomer Exposure Test 04')
        .texture('minecraft:item/written_book').rarity('rare').maxStackSize(1)
        .tooltip('§dLOR-009 // repeat biological degradation')
        .tooltip('§7The fourth controlled repetition ended the argument about measurement error')
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


WAVE_QUESTS = '''
		{
			dependencies: ["4F57000000000003"]
			id: "4F57000000000004"
			tasks: [{ id: "4F57800000000005" structure: "infinite_domain:old_world/ows_010_atlas_conveyor_transfer_hall" type: "structure" }]
			x: 3.0d
			y: 6.0d
		}
		{
			dependencies: ["4F57000000000004"]
			icon: "kubejs:atlas_transfer_maintenance_card"
			id: "4F57000000000005"
			rewards: [{ command: "execute in minecraft:overworld run structure_map infinite_domain:old_world/ows_012_atlas_bulk_crushing_preparation_plant 2" feedback_message: "infinite_domain.reward.explorer_map" id: "70E2812D71B74803" permission_level: 2 silent: true type: "command" }]
			shape: "octagon"
			tasks: [{ consume_items: true id: "4F57800000000006" item: { count: 1, id: "kubejs:atlas_transfer_maintenance_card" } type: "item" }]
			x: 6.0d
			y: 6.0d
		}
		{
			id: "4F57000000000010"
			rewards: [{ command: "execute in minecraft:overworld run structure_map infinite_domain:old_world/ows_001_vcf_neighborhood_culture_service_depot 2" feedback_message: "infinite_domain.reward.explorer_map" id: "70E2F9EA683282B8" permission_level: 2 silent: true type: "command" }]
			shape: "gear"
			tasks: [{ id: "4F57800000000010" item: { count: 1, id: "minecraft:bread" } type: "item" }]
			x: -6.0d
			y: 0.0d
		}
		{
			dependencies: ["4F57000000000010"]
			id: "4F57000000000011"
			tasks: [{ id: "4F57800000000011" structure: "infinite_domain:old_world/ows_001_vcf_neighborhood_culture_service_depot" type: "structure" }]
			x: -6.0d
			y: 3.0d
		}
		{
			dependencies: ["4F57000000000011"]
			icon: "kubejs:vcf_culture_service_manifest"
			id: "4F57000000000012"
			rewards: [{ command: "execute in minecraft:overworld run structure_map infinite_domain:old_world/ows_002_vcf_emergency_community_grow_hall 2" feedback_message: "infinite_domain.reward.explorer_map" id: "70E24C220612D966" permission_level: 2 silent: true type: "command" }]
			shape: "octagon"
			tasks: [
				{ consume_items: true id: "4F57800000000012" item: { count: 1, id: "kubejs:vcf_culture_service_manifest" } type: "item" }
				{ id: "4F57800000000013" item: { count: 1, id: "kubejs:vcf_return_crate_log" } type: "item" }
			]
			x: -6.0d
			y: 6.0d
		}
		{
			dependencies: ["4F57000000000005"]
			id: "4F57000000000020"
			rewards: [{ command: "execute in minecraft:overworld run structure_map infinite_domain:old_world/ows_015_polycore_utility_seal_failure_station 2" feedback_message: "infinite_domain.reward.explorer_map" id: "70E3C732AD87E538" permission_level: 2 silent: true type: "command" }]
			shape: "gear"
			tasks: [{ id: "4F57800000000020" item: { count: 1, id: "create:fluid_pipe" } type: "item" }]
			x: 9.0d
			y: 6.0d
		}
		{
			dependencies: ["4F57000000000020"]
			id: "4F57000000000021"
			tasks: [{ id: "4F57800000000021" structure: "infinite_domain:old_world/ows_015_polycore_utility_seal_failure_station" type: "structure" }]
			x: 9.0d
			y: 9.0d
		}
		{
			dependencies: ["4F57000000000021"]
			icon: "kubejs:polycore_seal_failure_report"
			id: "4F57000000000022"
			rewards: [{ command: "execute in minecraft:overworld run structure_map infinite_domain:old_world/ows_016_polycore_elastomer_exposure_array 2" feedback_message: "infinite_domain.reward.explorer_map" id: "70E2EF3B1EB9AB6E" permission_level: 2 silent: true type: "command" }]
			shape: "octagon"
			tasks: [
				{ consume_items: true id: "4F57800000000022" item: { count: 1, id: "kubejs:polycore_seal_failure_report" } type: "item" }
				{ id: "4F57800000000023" item: { count: 1, id: "kubejs:polycore_service_interval_board" } type: "item" }
			]
			x: 12.0d
			y: 9.0d
		}
		{
			dependencies: ["4F57000000000012"]
			id: "4F57000000000013"
			tasks: [{ id: "4F57800000000014" structure: "infinite_domain:old_world/ows_002_vcf_emergency_community_grow_hall" type: "structure" }]
			x: -9.0d
			y: 6.0d
		}
		{
			dependencies: ["4F57000000000013"]
			icon: "kubejs:emergency_grow_authorization"
			id: "4F57000000000014"
			rewards: [{ command: "execute in minecraft:overworld run structure_map infinite_domain:old_world/ows_003_vcf_cold_chain_culture_nursery 2" feedback_message: "infinite_domain.reward.explorer_map" id: "70E8DC3599B8FE47" permission_level: 2 silent: true type: "command" }]
			shape: "octagon"
			tasks: [{ consume_items: true id: "4F57800000000015" item: { count: 1, id: "kubejs:emergency_grow_authorization" } type: "item" }]
			x: -12.0d
			y: 6.0d
		}
		{
			dependencies: ["4F57000000000014"]
			id: "4F57000000000015"
			tasks: [{ id: "4F57800000000016" structure: "infinite_domain:old_world/ows_003_vcf_cold_chain_culture_nursery" type: "structure" }]
			x: -12.0d
			y: 9.0d
		}
		{
			dependencies: ["4F57000000000015"]
			icon: "kubejs:vcf_culture_batch_record"
			id: "4F57000000000016"
			rewards: [{ command: "execute in minecraft:overworld run structure_map infinite_domain:old_world/ows_004_vcf_mycological_vertical_farm_tower 2" feedback_message: "infinite_domain.reward.explorer_map" id: "70E844D07AE3C4B6" permission_level: 2 silent: true type: "command" }]
			shape: "octagon"
			tasks: [
				{ consume_items: true id: "4F57800000000017" item: { count: 1, id: "kubejs:vcf_culture_batch_record" } type: "item" }
				{ id: "4F57800000000018" item: { count: 1, id: "kubejs:vcf_global_licensing_brief" } type: "item" }
			]
			x: -15.0d
			y: 9.0d
		}
		{
			dependencies: ["4F57000000000022"]
			id: "4F57000000000023"
			tasks: [{ id: "4F57800000000024" structure: "infinite_domain:old_world/ows_016_polycore_elastomer_exposure_array" type: "structure" }]
			x: 15.0d
			y: 9.0d
		}
		{
			dependencies: ["4F57000000000023"]
			icon: "kubejs:polycore_elastomer_exposure_test"
			id: "4F57000000000024"
			shape: "octagon"
			tasks: [
				{ consume_items: true id: "4F57800000000025" item: { count: 1, id: "kubejs:polycore_elastomer_exposure_test" } type: "item" }
				{ id: "4F57800000000026" item: { count: 1, id: "kubejs:polycore_exposure_test_04" } type: "item" }
			]
			x: 18.0d
			y: 9.0d
		}
		{
			dependencies: ["4F57000000000016"]
			id: "4F57000000000030"
			tasks: [{ id: "4F57800000000030" structure: "infinite_domain:old_world/ows_004_vcf_mycological_vertical_farm_tower" type: "structure" }]
			x: -18.0d
			y: 12.0d
		}
		{
			dependencies: ["4F57000000000030"]
			icon: "kubejs:evercrop_cultivation_handbook"
			id: "4F57000000000031"
			rewards: [{ command: "execute in minecraft:overworld run structure_map infinite_domain:old_world/ows_006_vcf_pt9_symbiosis_pilot_laboratory 2" feedback_message: "infinite_domain.reward.explorer_map" id: "70EB8196EC79CFD0" permission_level: 2 silent: true type: "command" }]
			shape: "octagon"
			tasks: [{ consume_items: true id: "4F57800000000031" item: { count: 1, id: "kubejs:evercrop_cultivation_handbook" } type: "item" }]
			x: -21.0d
			y: 12.0d
		}
		{
			dependencies: ["4F57000000000031"]
			id: "4F57000000000032"
			tasks: [{ id: "4F57800000000032" structure: "infinite_domain:old_world/ows_006_vcf_pt9_symbiosis_pilot_laboratory" type: "structure" }]
			x: -21.0d
			y: 15.0d
		}
		{
			dependencies: ["4F57000000000032"]
			icon: "kubejs:pt9_symbiosis_report"
			id: "4F57000000000033"
			shape: "octagon"
			tasks: [{ consume_items: true id: "4F57800000000033" item: { count: 1, id: "kubejs:pt9_symbiosis_report" } type: "item" }]
			x: -24.0d
			y: 15.0d
		}
		{
			dependencies: ["4F57000000000005"]
			id: "4F57000000000040"
			tasks: [{ id: "4F57800000000040" structure: "infinite_domain:old_world/ows_012_atlas_bulk_crushing_preparation_plant" type: "structure" }]
			x: 6.0d
			y: 9.0d
		}
		{
			dependencies: ["4F57000000000040"]
			icon: "kubejs:atlas_bulk_process_manual"
			id: "4F57000000000041"
			shape: "octagon"
			tasks: [{ consume_items: true id: "4F57800000000041" item: { count: 1, id: "kubejs:atlas_bulk_process_manual" } type: "item" }]
			x: 6.0d
			y: 12.0d
		}
'''

WAVE_LANG = [
    '\tquest.4F57000000000004.title: "The Hall Beyond the Garage"',
    '\tquest.4F57000000000004.quest_desc: ["Follow the Atlas map to a complete transfer hall. Its scale turns one roadside clue into an industrial system."]',
    '\ttask.4F57800000000005.title: "Enter OWS-010"',
    '\tquest.4F57000000000005.title: "Ordinary Automation"',
    '\tquest.4F57000000000005.quest_desc: ["Recover the maintenance card. Atlas treated transfer tolerances and lockout schedules as ordinary infrastructure." "The resemblance is exact enough to be uncomfortable. They were here first, and they had already made it routine. — Charles"]',
    '\ttask.4F57800000000006.title: "Return the Atlas Transfer Card"',
    '\tquest.4F57000000000010.title: "Food on Every Corner"',
    '\tquest.4F57000000000010.quest_desc: ["Bread is enough to begin asking how the old cities fed billions. Charles has marked a neighborhood VCF service depot."]',
    '\ttask.4F57800000000010.title: "Produce a Staple Food"',
    '\tquest.4F57000000000011.title: "Neighborhood Culture Service"',
    '\tquest.4F57000000000011.quest_desc: ["Enter the VCF depot. Read its cooler banks, issue counter and return route before taking its records."]',
    '\ttask.4F57800000000011.title: "Enter OWS-001"',
    '\tquest.4F57000000000012.title: "Food for a Billion — First Evidence"',
    '\tquest.4F57000000000012.quest_desc: ["The manifest proves Evercrop culture was mundane and everywhere. The exception log records the first failed seals and late returns."]',
    '\ttask.4F57800000000012.title: "Return the VCF Service Manifest"',
    '\ttask.4F57800000000013.title: "Recover the Return-Crate Log"',
    '\tquest.4F57000000000020.title: "Unexpected Maintenance"',
    '\tquest.4F57000000000020.quest_desc: ["A fluid pipe is enough context to understand the next record. Follow the PolyCore utility map."]',
    '\ttask.4F57800000000020.title: "Understand Basic Fluid Handling"',
    '\tquest.4F57000000000021.title: "Utility Seal Failure Station"',
    '\tquest.4F57000000000021.quest_desc: ["Enter the ordinary pump station. The crisis is written in replacement stock, isolation paint and shorter intervals—not spectacle."]',
    '\ttask.4F57800000000021.title: "Enter OWS-015"',
    '\tquest.4F57000000000022.title: "The Interval Collapses"',
    '\tquest.4F57000000000022.quest_desc: ["Twelve months. Six. Three. Weekly. Then blank. PolyCore knew the material was failing everywhere before anyone called it a catastrophe. — Charles"]',
    '\ttask.4F57800000000022.title: "Return the PolyCore Failure Report"',
    '\ttask.4F57800000000023.title: "Recover LOR-008"',
    '\tquest.4F57000000000013.title: "Emergency Community Grow Hall"',
    '\tquest.4F57000000000013.quest_desc: ["Enter the converted municipal hall. VCF racks and culture kits were deployed as public relief infrastructure during early containment."]',
    '\ttask.4F57800000000014.title: "Enter OWS-002"',
    '\tquest.4F57000000000014.title: "Authorized Emergency Abundance"',
    '\tquest.4F57000000000014.quest_desc: ["Recover the signed grow authorization. This was policy, not an isolated experiment: governments used Evercrop when ordinary food logistics began to fail."]',
    '\ttask.4F57800000000015.title: "Return the Emergency Grow Authorization"',
    '\tquest.4F57000000000015.title: "Cold-Chain Culture Nursery"',
    '\tquest.4F57000000000015.quest_desc: ["Follow the batch route into VCF cold storage. Dormant cultures moved from nursery vault to inspection to worldwide dispatch."]',
    '\ttask.4F57800000000016.title: "Enter OWS-003"',
    '\tquest.4F57000000000016.title: "The Crop Was Already Everywhere"',
    '\tquest.4F57000000000016.quest_desc: ["The batch record connects dormancy to logistics. LOR-005 lists global license regions; there was no clean perimeter left to defend. Keep that conclusion provisional until more institutions corroborate it. — Charles"]',
    '\ttask.4F57800000000017.title: "Return the VCF Culture Batch Record"',
    '\ttask.4F57800000000018.title: "Recover LOR-005"',
    '\tquest.4F57000000000023.title: "Elastomer Exposure Array"',
    '\tquest.4F57000000000023.quest_desc: ["Enter the PolyCore laboratory and compare its four parallel chambers. The experiment was built to eliminate excuses."]',
    '\ttask.4F57800000000024.title: "Enter OWS-016"',
    '\tquest.4F57000000000024.title: "Four Times Is a Result"',
    '\tquest.4F57000000000024.quest_desc: ["Recover the exposure authorization and Test 04. The same biological degradation repeated under controlled conditions. Unexpected maintenance had become a reproducible scientific fact."]',
    '\ttask.4F57800000000025.title: "Return the Exposure Authorization"',
    '\ttask.4F57800000000026.title: "Recover LOR-009"',
    '\tquest.4F57000000000030.title: "Mycological Vertical Farm Tower"',
    '\tquest.4F57000000000030.quest_desc: ["Enter the VCF tower and read it floor by floor: nutrient service below, cultivation above, then harvest, packaging and clean public-facing space."]',
    '\ttask.4F57800000000030.title: "Enter OWS-004"',
    '\tquest.4F57000000000031.title: "FOOD FOR A BILLION"',
    '\tquest.4F57000000000031.quest_desc: ["Recover LOR-001, the Evercrop cultivation handbook. The tower was not a prototype; it was a repeatable industrial recipe for feeding a dense city."]',
    '\ttask.4F57800000000031.title: "Return LOR-001 to Charles"',
    '\tquest.4F57000000000032.title: "PT-9 Symbiosis Pilot Laboratory"',
    '\tquest.4F57000000000032.quest_desc: ["Enter the pilot laboratory. Compare the culture chambers, bacterial-control rooms and polymer observation stations before disturbing the report."]',
    '\ttask.4F57800000000032.title: "Enter OWS-006"',
    '\tquest.4F57000000000033.title: "THE PERFECT CROP"',
    '\tquest.4F57000000000033.quest_desc: ["Recover LOR-003. PT-9 documented beneficial bacteria protecting the crop while another observation showed polymer degradation. The same symbiosis that made Evercrop resilient may have made containment impossible. — Charles"]',
    '\ttask.4F57800000000033.title: "Return LOR-003 to Charles"',
    '\tquest.4F57000000000040.title: "Bulk Crushing & Preparation Plant"',
    '\tquest.4F57000000000040.quest_desc: ["Enter the Atlas preparation plant. Crushers, mixers, feed lanes and dust handling turn the roadside transfer evidence into industrial-scale throughput."]',
    '\ttask.4F57800000000040.title: "Enter OWS-012"',
    '\tquest.4F57000000000041.title: "The Cost of Throughput"',
    '\tquest.4F57000000000041.quest_desc: ["Recover the bulk-process manual. Atlas documented service failures as routine production constraints; scale came from maintaining the whole system, not merely making machines faster."]',
    '\ttask.4F57800000000041.title: "Return the Atlas Bulk-Process Manual"',
]


def build_chapter_wave() -> None:
    build_chapter()
    chapter = CHAPTER.read_text(encoding="utf-8")
    reward_anchor = '\t\t\trewards: [\n\t\t\t\t{\n\t\t\t\t\tid: "4F57900000000002"'
    map_reward = '\t\t\trewards: [\n\t\t\t\t{ command: "execute in minecraft:overworld run structure_map infinite_domain:old_world/ows_010_atlas_conveyor_transfer_hall 2" feedback_message: "infinite_domain.reward.explorer_map" id: "70E14257335F6B58" permission_level: 2 silent: true type: "command" }\n\t\t\t\t{\n\t\t\t\t\tid: "4F57900000000002"'
    if reward_anchor not in chapter:
        raise ValueError("Could not attach the OWS-010 map to the THEY WERE HERE FIRST proof quest")
    chapter = chapter.replace(reward_anchor, map_reward, 1)
    close = "\t]\n}"
    if close not in chapter:
        raise ValueError("Could not extend Old World quest chapter")
    write_text(CHAPTER, chapter.replace(close, WAVE_QUESTS + close, 1))
    lang = LANG.read_text(encoding="utf-8")
    write_text(LANG, lang.replace(LANG_END, "\n".join(WAVE_LANG) + "\n" + LANG_END, 1))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-root", type=Path, help="Extracted package root to import before building")
    args = parser.parse_args()
    if args.package_root:
        import_package(args.package_root.resolve())
    build_registries()
    build_startup_items()
    build_chapter_wave()
    print(f"Built Old World registries and {len(IMPLEMENTED_TARGETS)}-site narrative wave.")


if __name__ == "__main__":
    main()
