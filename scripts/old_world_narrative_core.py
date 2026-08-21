#!/usr/bin/env python3
"""[SYSTEM REPORT] Authoritative Old World narrative generation core.

Structure specifications and legacy builders are preserved in
_old_world_narrative_structure_core.py. OWS-001 is now dispatched through the
reviewed final heavy-rebuild builder in old_world_ows001_final.py so the shipping
NBT and Gate-D preview consume one source of truth.

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

# Compose reviewed per-target final builders at the authoritative core boundary.
# This is not a runtime mutation layer: BUILDERS is the single generation dispatch
# table consumed by generate(), copied once from the preserved legacy source.
BUILDERS = dict(BUILDERS)
BUILDERS["OWS-001"] = ows001_final.build_001

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "kubejs" / "data" / "infinite_domain"
AUDIO_DIARY_REGISTRY = ROOT / "kubejs" / "config" / "old_world_audio_diaries.json"
AUDIO_DIARY_BOOK_DIR = ROOT / "old_world_narrative" / "audio_diary_books"


def _book_cover(entry: dict) -> tuple[str, str]:
    if entry.get("type") != "minecraft:item" or entry.get("name") != "minecraft:written_book":
        raise ValueError("audio diary pool contains a non-written-book entry")
    cover = next(
        (fn for fn in entry.get("functions", []) if fn.get("function") == "minecraft:set_book_cover"),
        None,
    )
    pages = next(
        (fn for fn in entry.get("functions", []) if fn.get("function") == "minecraft:set_written_book_pages"),
        None,
    )
    if not cover or not cover.get("title") or not cover.get("author"):
        raise ValueError("audio diary written_book is missing set_book_cover metadata")
    if not pages or not pages.get("pages"):
        raise ValueError(f'audio diary "{cover.get("title", "<unknown>")}" has no written pages')
    return cover["title"], cover["author"]


def _load_audio_diary_registry() -> tuple[dict[str, tuple[dict, ...]], dict[str, tuple[str, ...]]]:
    document = json.loads(AUDIO_DIARY_REGISTRY.read_text(encoding="utf-8"))
    bindings = document.get("bindings", [])
    expected_count = int(document.get("diary_count", 0))
    expected_locations = int(document.get("location_count", 0))

    ids = [row.get("id") for row in bindings]
    if expected_count != 54 or len(bindings) != expected_count:
        raise ValueError(
            f"Old World audio diary registry must contain 54 bindings; "
            f"declares {expected_count}, contains {len(bindings)}"
        )
    if len(ids) != len(set(ids)) or any(not diary_id for diary_id in ids):
        raise ValueError("Old World audio diary registry contains missing or duplicate diary IDs")

    bindings_by_site: dict[str, list[dict]] = {}
    for row in bindings:
        for key in ("id", "site", "title", "author", "era"):
            if not row.get(key):
                raise ValueError(f"audio diary binding {row!r} is missing {key}")
        bindings_by_site.setdefault(row["site"], []).append(row)

    if expected_locations != 27:
        raise ValueError(f"Old World audio diary registry must declare 27 locations, got {expected_locations}")

    pools_by_site: dict[str, tuple[dict, ...]] = {}
    ids_by_site: dict[str, tuple[str, ...]] = {}
    total_books = 0

    for site, site_bindings in bindings_by_site.items():
        source_path = AUDIO_DIARY_BOOK_DIR / f"{site.lower()}.json"
        if not source_path.is_file():
            raise ValueError(f"missing canonical audio diary book source for {site}: {source_path}")

        source = json.loads(source_path.read_text(encoding="utf-8"))
        books: dict[tuple[str, str], dict] = {}
        for pool in source.get("pools", []):
            if pool.get("rolls") != 1:
                continue
            entries = pool.get("entries", [])
            if len(entries) != 1 or entries[0].get("name") != "minecraft:written_book":
                continue
            title, author = _book_cover(entries[0])
            key = (title, author)
            if key in books:
                raise ValueError(f"duplicate canonical audio diary book {title!r} by {author!r} at {site}")
            books[key] = pool

        expected_keys = [(row["title"], row["author"]) for row in site_bindings]
        missing = [key for key in expected_keys if key not in books]
        extras = [key for key in books if key not in expected_keys]
        if missing or extras:
            raise ValueError(
                f"{site} audio diary source does not match registry; missing={missing}, extras={extras}"
            )

        ordered = []
        for row in site_bindings:
            pool = copy.deepcopy(books[(row["title"], row["author"])])
            pages_fn = next(
                fn for fn in pool["entries"][0]["functions"]
                if fn.get("function") == "minecraft:set_written_book_pages"
            )
            header = str(pages_fn["pages"][0])
            if f"ERA {row['era']}" not in header:
                raise ValueError(
                    f'{site} diary {row["id"]} "{row["title"]}" page header does not match era {row["era"]}'
                )
            ordered.append(pool)

        pools_by_site[site] = tuple(ordered)
        ids_by_site[site] = tuple(row["id"] for row in site_bindings)
        total_books += len(ordered)

    if total_books != expected_count:
        raise ValueError(f"loaded {total_books} canonical audio diary books; expected {expected_count}")

    return pools_by_site, ids_by_site


AUDIO_DIARY_POOLS_BY_SITE, AUDIO_DIARY_IDS_BY_SITE = _load_audio_diary_registry()


def loot_table(spec):
    items = list(dict.fromkeys([spec.proof] + ([spec.lore] if spec.lore else [])))
    pools = [
        {"rolls": 1, "entries": [{"type": "minecraft:item", "name": item}]}
        for item in items
    ]

    # Each diary receives an independent one-roll singleton pool, matching the
    # deterministic acquisition semantics of the quest proof item.
    pools.extend(copy.deepcopy(AUDIO_DIARY_POOLS_BY_SITE.get(spec.target, ())))

    extra = [{"type": "minecraft:item", "name": "create:andesite_alloy", "weight": 8}]
    if spec.target == "OWS-009":
        extra += [
            {"type": "minecraft:item", "name": "create:shaft", "weight": 10},
            {"type": "minecraft:item", "name": "create:cogwheel", "weight": 8},
        ]
    extra += [
        {"type": "minecraft:item", "name": "minecraft:iron_ingot", "weight": 10},
        {"type": "minecraft:item", "name": "immersiveengineering:component_iron", "weight": 5},
    ]
    pools.append(
        {
            "rolls": {
                "type": "minecraft:uniform",
                "min": 3 if spec.target == "OWS-009" else 2,
                "max": 6 if spec.target == "OWS-009" else 4,
            },
            "entries": extra,
        }
    )
    return {"type": "minecraft:chest", "random_sequence": spec.loot_id, "pools": pools}


def generate(spec):
    template = BUILDERS[spec.target]()
    base.stabilize_door_pairs(template)
    metrics = base.assess_fidelity(spec.source_profile, template)
    if not metrics["structural_lint_passed"]:
        raise ValueError(f"{spec.target} failed structural lint: " + "; ".join(metrics["issues"]))

    nbt_path = DATA / "structure" / "wasteland" / "old_world" / f"{spec.name}.nbt"
    previous_nbt = nbt_path.read_bytes() if nbt_path.is_file() else None
    statistics = template.save(f"old_world/{spec.name}")
    if previous_nbt is not None:
        generated_nbt = nbt_path.read_bytes()
        if gzip.decompress(previous_nbt) == gzip.decompress(generated_nbt):
            nbt_path.write_bytes(previous_nbt)

    base.write_json(
        DATA / "worldgen" / "template_pool" / "old_world" / f"{spec.name}.json",
        {
            "fallback": "minecraft:empty",
            "elements": [
                {
                    "weight": 1,
                    "element": {
                        "location": f"infinite_domain:wasteland/old_world/{spec.name}",
                        "processors": "minecraft:empty",
                        "projection": "rigid",
                        "element_type": "minecraft:single_pool_element",
                    },
                }
            ],
        },
    )
    base.write_json(
        DATA / "worldgen" / "structure" / "old_world" / f"{spec.name}.json",
        {
            "type": "minecraft:jigsaw",
            "biomes": "#infinite_domain:wasteland_site_biomes",
            "step": "surface_structures",
            "spawn_overrides": {},
            "terrain_adaptation": "beard_box",
            "start_pool": f"infinite_domain:old_world/{spec.name}",
            "size": 1,
            "start_height": {"absolute": 0},
            "max_distance_from_center": 80,
            "use_expansion_hack": False,
            "liquid_settings": "ignore_waterlogging",
            "project_start_to_heightmap": "WORLD_SURFACE_WG",
        },
    )
    base.write_json(
        DATA / "loot_table" / "chests" / "old_world" / f"{spec.name}.json",
        loot_table(spec),
    )
    base.write_json(
        ROOT / "old_world_narrative" / "structures"
        / f"{spec.target.lower()}-{spec.name[8:].replace('_', '-')}.json",
        {
            "format_version": 1,
            "target_id": spec.target,
            "structure_id": spec.structure_id,
            "source_structure": spec.source_id,
            "collapse_phase": spec.phase,
            "acceptance_dimensions": spec.dimensions,
            "proof_item": spec.proof,
            "lore_record": spec.lore,
            "audio_diary_ids": list(AUDIO_DIARY_IDS_BY_SITE.get(spec.target, ())),
            "audio_diary_loot": "deterministic_same_as_proof_item"
            if spec.target in AUDIO_DIARY_IDS_BY_SITE else None,
            "loot_table": spec.loot_id,
            "locator_command": f"/structure_map {spec.structure_id} 2",
            "statistics": statistics,
            "structural_lint": metrics,
            "static_render_review": "generated_and_inspected_not_runtime_approval",
            "runtime_validation": "deferred_by_user",
        },
    )


def main():
    for spec in SPECS:
        generate(spec)
    for set_name, spacing, separation, salt in (
        ("common_sites", 48, 24, 90310009),
        ("uncommon_sites", 96, 48, 90310016),
        ("rare_sites", 160, 80, 90310006),
    ):
        members = [spec for spec in SPECS if spec.set_name == set_name]
        base.write_json(
            DATA / "worldgen" / "structure_set" / "old_world" / f"{set_name}.json",
            {
                "structures": [{"structure": spec.structure_id, "weight": 1} for spec in members],
                "placement": {
                    "type": "minecraft:random_spread",
                    "spacing": spacing,
                    "separation": separation,
                    "salt": salt,
                },
            },
        )
    print(
        f"Generated {len(SPECS)} approved Old World sites with deterministic proof "
        f"loot and {sum(len(v) for v in AUDIO_DIARY_POOLS_BY_SITE.values())} audio diaries."
    )


if __name__ == "__main__":
    main()
