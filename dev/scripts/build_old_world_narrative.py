#!/usr/bin/env python3
"""[SYSTEM REPORT] Authoritative Old World package/quest builder entrypoint.

The historical package import and hand-authored quest implementation is preserved
in old_world_narrative_package_core.py. This wrapper keeps canonical proof IDs,
structure mappings, and the full staged 64-site exploration layer synchronized
with the sole authoritative structure generator.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import old_world_narrative_package_core as core
from generate_old_world_narrative_structures import (
    CONTROLLED_WORLDGEN_TARGETS,
    DARKNET_RETURN_TARGETS,
    SPECS,
)

ROOT = Path(__file__).resolve().parents[2]
PROGRAM = ROOT / "dev/old_world_narrative"
REGISTRY = PROGRAM / "registry"
PREPARED_QUEST_DIR = PROGRAM / "quests"
PREPARED_SITE_QUESTS = PREPARED_QUEST_DIR / "prepared_site_surveys.snbt"
PREPARED_SITE_LANG = PREPARED_QUEST_DIR / "prepared_site_surveys_lang.snbt"
SITE_QUEST_CATALOG = REGISTRY / "site_quest_catalog.json"
CANONICAL_PROOF_REGISTRY = ROOT / "kubejs" / "config" / "old_world_evidence.json"
CANONICAL_PROOF_STARTUP = ROOT / "kubejs" / "startup_scripts" / "old_world_evidence_items.js"
SUPPLEMENTAL_STARTUP = ROOT / "kubejs" / "startup_scripts" / "old_world_narrative_items.js"

SITE_QUEST_BASE = int("4F58000000000000", 16)
SITE_STRUCTURE_TASK_BASE = int("4F58100000000000", 16)
SITE_PROOF_TASK_BASE = int("4F58200000000000", 16)
SITE_LEAD_QUEST_ID = "4F58F00000000000"
SITE_LEAD_TASK_ID = "4F58F10000000000"

# Extend the preserved package builder's implementation mapping from the same
# structure specs used by the authoritative generator. A package rebuild may
# never reset a later implemented target back to approved_for_mapping.
for spec in SPECS:
    core.IMPLEMENTED_TARGETS[spec.target] = {
        "source": spec.source_id,
        "name": spec.name,
        "dimensions": list(spec.dimensions),
    }

# OWS-017 is supporting evidence for BOTH SIDES OF THE WALL. The major quest's
# later continuity landmark remains OWS-045; this additive target records the
# PolyCore material-barrier evidence without replacing the canonical spine.
for qid, _title, _prerequisite, target_structures in core.QUEST_SPINE:
    if qid == "OWQ-05" and "OWS-017" not in target_structures:
        target_structures.insert(0, "OWS-017")

_original_build_registries = core.build_registries
_original_build_chapter_wave = core.build_chapter_wave


def _ftb_id(base: int, target: str) -> str:
    return f"{base + int(target[-3:]):016X}"


def _map_reward_id(target: str) -> str:
    return "71E" + hashlib.sha256(f"old-world-site-map:{target}".encode()).hexdigest()[:13].upper()


def build_registries() -> None:
    _original_build_registries()
    state_path = REGISTRY / "implementation_state.json"
    targets_path = REGISTRY / "structure_targets.json"
    if not state_path.is_file() or not targets_path.is_file():
        return

    state = json.loads(state_path.read_text(encoding="utf-8"))
    targets_document = json.loads(targets_path.read_text(encoding="utf-8"))
    targets = targets_document["targets"]
    implemented = sorted(spec.target for spec in SPECS)
    implemented_set = set(implemented)

    # Functional completion and schematic quality are deliberately separate.
    # Full source/quest authoring is allowed to move forward while every site
    # remains queued for the dedicated later architectural rebuild.
    for row in targets:
        if row["id"] in implemented_set:
            row["functional_status"] = "static_source_implemented"
            row["quality_status"] = "schematic_revision_pending"
        else:
            row["functional_status"] = "not_yet_implemented"
            row["quality_status"] = "not_yet_assessed"
    targets_path.write_text(
        json.dumps(targets_document, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    state["static_source_implemented"] = implemented
    state["schematic_revision_pending"] = implemented
    state["quest_spine_targets"] = sorted({
        target
        for _qid, _title, _prerequisite, target_structures in core.QUEST_SPINE
        for target in target_structures
        if target in implemented_set
    })
    state["quest_authored"] = []
    state["quest_live"] = []
    state["quest_activation_pending"] = implemented

    render_manifest = PROGRAM / "reviews" / "render-manifest.json"
    rendered = set()
    if render_manifest.is_file():
        rendered = {
            entry["structure_id"]
            for entry in json.loads(render_manifest.read_text(encoding="utf-8")).get("structures", [])
        }
    state["static_render_reviewed"] = sorted(
        spec.target for spec in SPECS if spec.structure_id in rendered
    )
    state["current_wave"] = "full_64_site_quest_authoring_and_static_generation"
    state["next_targets"] = []
    state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")


def build_startup_items() -> None:
    """Validate, but never regenerate, the split proof/lore startup registries."""
    if not CANONICAL_PROOF_REGISTRY.is_file() or not CANONICAL_PROOF_STARTUP.is_file():
        raise FileNotFoundError("Canonical Old World proof registry/registration is missing")
    if not SUPPLEMENTAL_STARTUP.is_file():
        raise FileNotFoundError("Supplemental Old World lore startup file is missing")

    proof_ids = {
        item["id"]
        for item in json.loads(CANONICAL_PROOF_REGISTRY.read_text(encoding="utf-8"))["items"]
    }
    if len(proof_ids) != 64:
        raise ValueError(f"Canonical proof registry must contain 64 unique IDs, found {len(proof_ids)}")

    supplemental = SUPPLEMENTAL_STARTUP.read_text(encoding="utf-8-sig")
    collisions = [
        item_id for item_id in sorted(proof_ids)
        if f"event.create('{item_id}')" in supplemental or f'event.create("{item_id}")' in supplemental
    ]
    if collisions:
        raise ValueError("Supplemental startup file duplicates canonical proof IDs: " + ", ".join(collisions))


def build_prepared_site_quests() -> None:
    """Author every staged site quest without prematurely injecting it live.

    The resulting SNBT fragment is ready to materialize after each structure is
    promoted into worldgen. Until then, the live hand-authored chapter remains
    limited to destinations whose current activation state can support it.
    """
    targets_document = json.loads((REGISTRY / "structure_targets.json").read_text(encoding="utf-8"))
    target_rows = {row["id"]: row for row in targets_document["targets"]}
    proof_document = json.loads(CANONICAL_PROOF_REGISTRY.read_text(encoding="utf-8"))
    evidence_rows = {entry["site"]: entry for entry in proof_document["items"]}

    if set(evidence_rows) != {spec.target for spec in SPECS}:
        raise ValueError("Prepared site quest layer requires one canonical evidence row for every implemented OWS target")

    institution_order: list[str] = []
    institution_sites: dict[str, list[str]] = {}
    for spec in SPECS:
        institution = evidence_rows[spec.target]["institution"]
        if institution not in institution_sites:
            institution_order.append(institution)
            institution_sites[institution] = []
        institution_sites[institution].append(spec.target)

    major_hooks: dict[str, list[str]] = {spec.target: [] for spec in SPECS}
    for qid, title, _prerequisite, target_structures in core.QUEST_SPINE:
        for target in target_structures:
            if target in major_hooks:
                major_hooks[target].append(f"{qid}:{title}")

    entries: list[dict[str, object]] = []
    quest_blocks: list[str] = []
    lang_entries: list[str] = []

    first_sites = [institution_sites[institution][0] for institution in institution_order]
    lead_rewards = []
    for target in first_sites:
        spec = next(spec for spec in SPECS if spec.target == target)
        lead_rewards.append(
            '{ command: "execute in minecraft:overworld run structure_map '
            + f'{spec.structure_id} 2" feedback_message: "infinite_domain.reward.explorer_map" '
            + f'id: "{_map_reward_id(target)}" permission_level: 2 silent: true type: "command" }}'
        )

    quest_blocks.append(
        '\t\t{\n'
        '\t\t\tdependencies: ["4F57000000000001"]\n'
        f'\t\t\tid: "{SITE_LEAD_QUEST_ID}"\n'
        '\t\t\trewards: [' + ' '.join(lead_rewards) + ']\n'
        '\t\t\tshape: "gear"\n'
        f'\t\t\ttasks: [{{ id: "{SITE_LEAD_TASK_ID}" item: {{ count: 1, id: "minecraft:compass" }} type: "item" }}]\n'
        '\t\t\tx: 0.0d\n'
        '\t\t\ty: 21.0d\n'
        '\t\t}'
    )
    lang_entries.extend([
        f'quest.{SITE_LEAD_QUEST_ID}.title: "Old World Regional Leads"',
        f'quest.{SITE_LEAD_QUEST_ID}.quest_desc: ["This staged survey root contains the first locator handoff for every institution. Locator rewards remain activation-gated until their structures enter world generation."]',
        f'task.{SITE_LEAD_TASK_ID}.title: "Carry a Compass"',
    ])

    for institution_index, institution in enumerate(institution_order):
        sites = institution_sites[institution]
        x = -42.0 + institution_index * 6.0
        for site_index, target in enumerate(sites):
            spec = next(spec for spec in SPECS if spec.target == target)
            row = target_rows[target]
            previous = sites[site_index - 1] if site_index else None
            next_target = sites[site_index + 1] if site_index + 1 < len(sites) else None
            quest_id = _ftb_id(SITE_QUEST_BASE, target)
            structure_task_id = _ftb_id(SITE_STRUCTURE_TASK_BASE, target)
            proof_task_id = _ftb_id(SITE_PROOF_TASK_BASE, target)
            dependency = _ftb_id(SITE_QUEST_BASE, previous) if previous else SITE_LEAD_QUEST_ID
            rewards = ""
            if next_target:
                next_spec = next(spec for spec in SPECS if spec.target == next_target)
                rewards = (
                    '\n\t\t\trewards: [{ command: "execute in minecraft:overworld run structure_map '
                    + f'{next_spec.structure_id} 2" feedback_message: "infinite_domain.reward.explorer_map" '
                    + f'id: "{_map_reward_id(next_target)}" permission_level: 2 silent: true type: "command" }}]'
                )

            y = 24.0 + site_index * 3.0
            quest_blocks.append(
                '\t\t{\n'
                f'\t\t\tdependencies: ["{dependency}"]\n'
                f'\t\t\ticon: "{spec.proof}"\n'
                f'\t\t\tid: "{quest_id}"'
                + rewards + '\n'
                '\t\t\tshape: "diamond"\n'
                '\t\t\ttasks: [\n'
                f'\t\t\t\t{{ id: "{structure_task_id}" structure: "{spec.structure_id}" type: "structure" }}\n'
                f'\t\t\t\t{{ id: "{proof_task_id}" item: {{ count: 1, id: "{spec.proof}" }} type: "item" }}\n'
                '\t\t\t]\n'
                f'\t\t\tx: {x:.1f}d\n'
                f'\t\t\ty: {y:.1f}d\n'
                '\t\t}'
            )

            narrative_function = row.get("narrative_function", "Recover and correlate the site's physical evidence")
            lang_entries.extend([
                f'quest.{quest_id}.title: "{target} — {row["variant_name"]}"',
                f'quest.{quest_id}.quest_desc: ["{narrative_function}" "Enter the registered structure and recover its deterministic evidence item before treating the site as complete."]',
                f'task.{structure_task_id}.title: "Enter {target}"',
                f'task.{proof_task_id}.title: "Recover {evidence_rows[target]["name"]}"',
            ])

            entries.append({
                "target_id": target,
                "institution": institution,
                "variant_name": row["variant_name"],
                "collapse_phase": row["collapse_phase"],
                "quest_id": quest_id,
                "dependency_quest_id": dependency,
                "predecessor_target": previous,
                "next_target": next_target,
                "structure_task_id": structure_task_id,
                "proof_task_id": proof_task_id,
                "structure_id": spec.structure_id,
                "proof_item": spec.proof,
                "locator_command": f"/structure_map {spec.structure_id} 2",
                "locator_reward_id": _map_reward_id(target),
                "locator_reward_source": SITE_LEAD_QUEST_ID if previous is None else _ftb_id(SITE_QUEST_BASE, previous),
                "major_quest_hooks": major_hooks[target],
                "requires_worldgen_activation": target not in CONTROLLED_WORLDGEN_TARGETS,
                "darknet_return_reserved": target in DARKNET_RETURN_TARGETS,
                "activation_state": "controlled_probe_ready" if target in CONTROLLED_WORLDGEN_TARGETS else "authored_staged_not_live",
            })

    PREPARED_QUEST_DIR.mkdir(parents=True, exist_ok=True)
    core.write_text(
        PREPARED_SITE_QUESTS,
        "{\n\tquests: [\n" + "\n".join(quest_blocks) + "\n\t]\n}\n",
    )
    core.write_text(
        PREPARED_SITE_LANG,
        "{\n\t" + "\n\t".join(lang_entries) + "\n}\n",
    )
    core.write_json(
        SITE_QUEST_CATALOG,
        {
            "format_version": 1,
            "status": "fully_authored_activation_gated",
            "site_count": len(entries),
            "lead_quest_id": SITE_LEAD_QUEST_ID,
            "institution_count": len(institution_order),
            "institutions": institution_order,
            "sites": entries,
        },
    )

    live_chapter = core.CHAPTER.read_text(encoding="utf-8")
    live_targets = sorted(spec.target for spec in SPECS if f'structure: "{spec.structure_id}"' in live_chapter)
    all_targets = sorted(spec.target for spec in SPECS)
    state_path = REGISTRY / "implementation_state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["quest_authored"] = all_targets
    state["quest_live"] = live_targets
    state["quest_activation_pending"] = sorted(set(all_targets) - set(live_targets))
    state["quest_layer_status"] = "full_64_site_catalog_authored_activation_gated"
    state["next_targets"] = []
    state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8", newline="\n")


def build_chapter_wave() -> None:
    _original_build_chapter_wave()
    build_prepared_site_quests()


core.build_registries = build_registries
core.build_startup_items = build_startup_items
core.build_chapter_wave = build_chapter_wave

# Compatibility exports for scripts that imported the original builder directly.
IMPLEMENTED_TARGETS = core.IMPLEMENTED_TARGETS
QUEST_SPINE = core.QUEST_SPINE
CANON_SHA256 = core.CANON_SHA256
import_package = core.import_package


def main() -> None:
    core.main()
    print(
        f"Built Old World package registries with {len(SPECS)} static structure mappings, "
        "64 staged site surveys, and canonical proof-registry separation."
    )


if __name__ == "__main__":
    main()
