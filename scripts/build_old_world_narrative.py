#!/usr/bin/env python3
"""[SYSTEM REPORT] Authoritative Old World package/quest builder entrypoint.

The historical package import and quest authoring implementation is preserved in
old_world_narrative_package_core.py. This wrapper prevents that older code from
re-registering canonical proof IDs and keeps its structure registry synchronized
with the single authoritative structure generator.
"""
from __future__ import annotations

import json
from pathlib import Path

import old_world_narrative_package_core as core
from generate_old_world_narrative_structures import SPECS

ROOT = Path(__file__).resolve().parents[1]
PROGRAM = ROOT / "old_world_narrative"
REGISTRY = PROGRAM / "registry"
CANONICAL_PROOF_REGISTRY = ROOT / "kubejs" / "config" / "old_world_evidence.json"
CANONICAL_PROOF_STARTUP = ROOT / "kubejs" / "startup_scripts" / "old_world_evidence_items.js"
SUPPLEMENTAL_STARTUP = ROOT / "kubejs" / "startup_scripts" / "old_world_narrative_items.js"

# Extend the preserved package builder's implementation mapping from the same
# structure specs used by the authoritative generator. This prevents a package
# rebuild from resetting later implemented targets back to approved_for_mapping.
for spec in SPECS:
    core.IMPLEMENTED_TARGETS[spec.target] = {
        "source": spec.source_id,
        "name": spec.name,
        "dimensions": list(spec.dimensions),
    }

# OWS-017 is supporting evidence for BOTH SIDES OF THE WALL. The major quest's
# later continuity landmark remains OWS-045; this additive target records the
# PolyCore material-barrier evidence without pretending the later site exists.
for qid, _title, _prerequisite, target_structures in core.QUEST_SPINE:
    if qid == "OWQ-05" and "OWS-017" not in target_structures:
        target_structures.insert(0, "OWS-017")

_original_build_registries = core.build_registries


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
    # Current Old World builds are allowed to move progression forward while all
    # remain queued for the dedicated later architectural/schematic rebuild.
    for row in targets:
        if row["id"] in implemented_set:
            row["functional_status"] = "static_implemented"
            row["quality_status"] = "schematic_revision_pending"
        else:
            row["functional_status"] = "not_yet_implemented"
            row["quality_status"] = "not_yet_assessed"
    targets_path.write_text(
        json.dumps(targets_document, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    state["static_implemented"] = implemented
    state["schematic_revision_pending"] = implemented

    quest_targets = {
        target
        for _qid, _title, _prerequisite, target_structures in core.QUEST_SPINE
        for target in target_structures
    }
    state["quest_integrated"] = sorted(implemented_set & quest_targets)

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
    state["current_wave"] = "polycore_static_coverage_ows_017_onward"
    state["next_targets"] = [
        row["id"] for row in targets
        if row["id"] not in implemented_set and row.get("implementation_status") == "approved_for_mapping"
    ][:5]
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


core.build_registries = build_registries
core.build_startup_items = build_startup_items

# Compatibility exports for scripts that imported the original builder directly.
IMPLEMENTED_TARGETS = core.IMPLEMENTED_TARGETS
QUEST_SPINE = core.QUEST_SPINE
CANON_SHA256 = core.CANON_SHA256
import_package = core.import_package


def main() -> None:
    core.main()
    print(f"Built Old World package registries with {len(SPECS)} static structure mappings and canonical proof-registry separation.")


if __name__ == "__main__":
    main()
