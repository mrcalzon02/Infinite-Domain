#!/usr/bin/env python3
"""[SYSTEM REPORT] Authoritative Old World narrative generation core.

Structure specifications and legacy builders are preserved in
_old_world_narrative_structure_core.py. OWS-001 through OWS-003 are dispatched
through their reviewed final heavy-rebuild builders so shipping NBT and Gate-D
previews consume one source of truth per completed/reviewed target.

This module owns generated output, including deterministic proof loot and the
Continuity audio-diary books. The audio diary registry is authoritative metadata.
Canonical book payloads live under old_world_narrative/audio_diary_books so
regeneration never depends on already-generated runtime loot tables.
"""
from __future__ import annotations

import copy
import gzip
import json
from pathlib import Path

from _old_world_narrative_structure_core import *  # noqa: F401,F403
import old_world_ows001_final as ows001_final
import old_world_ows002_final as ows002_final
import old_world_ows003_final as ows003_final

# Compose reviewed per-target final builders at the authoritative core boundary.
# This is not a runtime mutation layer: BUILDERS is the single generation dispatch
# table consumed by generate(), copied once from the preserved legacy source.
BUILDERS = dict(BUILDERS)
BUILDERS["OWS-001"] = ows001_final.build_001
BUILDERS["OWS-002"] = ows002_final.build_002
BUILDERS["OWS-003"] = ows003_final.build_003

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "kubejs" / "data" / "infinite_domain"
AUDIO_DIARY_REGISTRY = ROOT / "kubejs" / "config" / "old_world_audio_diaries.json"
AUDIO_DIARY_BOOK_DIR = ROOT / "old_world_narrative" / "audio_diary_books"


def _book_cover(entry: dict) -> tuple[str, str]:
    if entry.get("type") != "minecraft:item" or entry.get("name") != "minecraft:written_book":
        raise ValueError("audio diary pool contains a non-written-book entry")
    functions = entry.get("functions", [])
    if len(functions) != 1 or functions[0].get("function") != "minecraft:set_components":
        raise ValueError("audio diary pool entry does not contain the canonical component payload")
    components = functions[0].get("components", {})
    content = components.get("minecraft:written_book_content", {})
    title = content.get("title", {}).get("raw")
    author = content.get("author")
    if not isinstance(title, str) or not title or not isinstance(author, str) or not author:
        raise ValueError("audio diary pool entry is missing title/author metadata")
    return title, author


def _is_audio_diary_entry(entry: dict) -> bool:
    try:
        _book_cover(entry)
    except (KeyError, TypeError, ValueError):
        return False
    return True


def _load_audio_diary_registry() -> dict:
    if not AUDIO_DIARY_REGISTRY.is_file():
        return {"records": []}
    payload = json.loads(AUDIO_DIARY_REGISTRY.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("old_world_audio_diaries.json must contain an object")
    records = payload.get("records", [])
    if not isinstance(records, list):
        raise ValueError("old_world_audio_diaries.json records must be a list")
    return payload


def _audio_diary_source_path(record: dict) -> Path:
    source = record.get("canonical_book_source")
    if isinstance(source, str) and source:
        path = ROOT / source
    else:
        diary_id = record.get("diary_id")
        if not isinstance(diary_id, str) or not diary_id:
            raise ValueError("audio diary registry record is missing diary_id")
        path = AUDIO_DIARY_BOOK_DIR / f"{diary_id}.json"
    if not path.is_file():
        raise FileNotFoundError(f"audio diary canonical source is missing: {path}")
    return path


def _load_audio_diary_entry(record: dict) -> dict:
    path = _audio_diary_source_path(record)
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not _is_audio_diary_entry(payload):
        raise ValueError(f"invalid canonical audio diary book payload: {path}")
    expected_title = record.get("title")
    expected_author = record.get("author")
    actual_title, actual_author = _book_cover(payload)
    if expected_title and actual_title != expected_title:
        raise ValueError(f"audio diary title mismatch for {record.get('diary_id')}: {actual_title!r} != {expected_title!r}")
    if expected_author and actual_author != expected_author:
        raise ValueError(f"audio diary author mismatch for {record.get('diary_id')}: {actual_author!r} != {expected_author!r}")
    return payload


def _loot_pool(entries: list[dict], *, rolls: int = 1) -> dict:
    return {"rolls": rolls, "entries": entries}


def _diary_pool(record: dict) -> dict:
    entry = _load_audio_diary_entry(record)
    return _loot_pool([entry])


def _target_loot_path(spec) -> Path:
    return DATA / "loot_table" / "chests" / "old_world" / f"{spec.name}.json"


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8", newline="\n")


def _loot_has_diary(payload: dict, record: dict) -> bool:
    expected_title = record.get("title")
    expected_author = record.get("author")
    for pool in payload.get("pools", []):
        for entry in pool.get("entries", []):
            if not _is_audio_diary_entry(entry):
                continue
            title, author = _book_cover(entry)
            if title == expected_title and author == expected_author:
                return True
    return False


def _inject_audio_diary_loot() -> None:
    registry = _load_audio_diary_registry()
    specs_by_target = {spec.target: spec for spec in SPECS}
    for record in registry.get("records", []):
        target = record.get("target")
        if target not in specs_by_target:
            continue
        spec = specs_by_target[target]
        path = _target_loot_path(spec)
        if not path.is_file():
            continue
        payload = _read_json(path)
        if _loot_has_diary(payload, record):
            continue
        payload.setdefault("pools", []).append(_diary_pool(record))
        _write_json(path, payload)


def _structure_file(spec) -> Path:
    return DATA / "structure" / "wasteland" / "old_world" / f"{spec.name}.nbt"


def _compress_json(payload: dict) -> bytes:
    return gzip.compress(json.dumps(payload, separators=(",", ":")).encode("utf-8"), mtime=0)


def _structure_record(spec, template) -> dict:
    lint = structural_lint(template, source_profile=spec.source_profile)
    stats = structure_statistics(template)
    return {
        "format_version": 1,
        "target_id": spec.target,
        "structure_id": spec.structure_id,
        "source_structure": spec.source_id,
        "collapse_phase": spec.phase,
        "acceptance_dimensions": spec.dimensions,
        "proof_item": spec.proof,
        "lore_record": spec.lore,
        "audio_diary_ids": [],
        "audio_diary_loot": None,
        "loot_table": spec.loot_id,
        "locator_command": f"/structure_map {spec.structure_id} 2",
        "statistics": stats,
        "structural_lint": lint,
        "static_render_review": "generated_and_inspected_not_runtime_approval",
        "runtime_validation": "deferred_by_user",
    }


def generate(*, only_targets: set[str] | None = None) -> None:
    selected = [spec for spec in SPECS if only_targets is None or spec.target in only_targets]
    for spec in selected:
        builder = BUILDERS[spec.target]
        template = builder()
        base.stabilize_door_pairs(template)
        lint = structural_lint(template, source_profile=spec.source_profile)
        if not lint["structural_lint_passed"]:
            raise RuntimeError(f"{spec.target} structural lint failed: {lint['issues']}")
        template.save(f"old_world/{spec.name}")
        record_path = ROOT / "old_world_narrative" / "structures" / f"{spec.target.lower()}-{spec.name.split('_', 2)[2].replace('_', '-')}.json"
        _write_json(record_path, _structure_record(spec, template))
    generate_loot_tables(selected)
    _inject_audio_diary_loot()


def _worldgen_structure_payload(spec) -> dict:
    return {
        "type": "minecraft:jigsaw",
        "biomes": "#infinite_domain:wasteland_structure_biomes",
        "step": "surface_structures",
        "spawn_overrides": {},
        "start_pool": f"infinite_domain:old_world/{spec.name}",
        "size": 1,
        "start_height": {"absolute": 0},
        "project_start_to_heightmap": "WORLD_SURFACE_WG",
        "max_distance_from_center": 80,
        "use_expansion_hack": False,
    }


def _worldgen_pool_payload(spec) -> dict:
    return {
        "name": f"infinite_domain:old_world/{spec.name}",
        "fallback": "minecraft:empty",
        "elements": [
            {
                "weight": 1,
                "element": {
                    "element_type": "minecraft:single_pool_element",
                    "location": spec.structure_id,
                    "processors": "minecraft:empty",
                    "projection": "rigid",
                },
            }
        ],
    }


def _worldgen_set_payload(spec) -> dict:
    return {
        "structures": [{"structure": spec.structure_id, "weight": 1}],
        "placement": {
            "type": "minecraft:random_spread",
            "salt": 9384471 + int(spec.target.split('-')[1]),
            "spacing": 48,
            "separation": 20,
            "spread_type": "triangular",
        },
    }


def generate_worldgen(*, only_targets: set[str] | None = None) -> None:
    selected = [spec for spec in SPECS if only_targets is None or spec.target in only_targets]
    for spec in selected:
        structure_path = DATA / "worldgen" / "structure" / "old_world" / f"{spec.name}.json"
        pool_path = DATA / "worldgen" / "template_pool" / "old_world" / f"{spec.name}.json"
        set_path = DATA / "worldgen" / "structure_set" / "old_world" / f"{spec.name}.json"
        _write_json(structure_path, _worldgen_structure_payload(spec))
        _write_json(pool_path, _worldgen_pool_payload(spec))
        if spec.target in CONTROLLED_WORLDGEN_TARGETS:
            _write_json(set_path, _worldgen_set_payload(spec))
        elif set_path.exists():
            set_path.unlink()


def generate_all() -> None:
    generate()
    generate_worldgen()


def load_generated_structure_json(spec) -> dict:
    path = _structure_file(spec)
    with gzip.open(path, "rb") as handle:
        return json.loads(handle.read().decode("utf-8"))


def clone_generated_structure_json(spec) -> dict:
    return copy.deepcopy(load_generated_structure_json(spec))
