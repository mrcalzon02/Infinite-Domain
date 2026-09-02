#!/usr/bin/env python3
"""Detect feature-order cycles caused by duplicate biome-modifier injection.

Minecraft sorts every placed feature into a single global order per generation
step. It derives that order from the per-biome feature lists: if biome P lists
feature A before feature B, the sorter records the edge A -> B. When two biomes
disagree, or when one biome lists the same feature twice with a third between
the copies, the constraints are unsatisfiable and `FeatureSorter` fails.

That failure is not fatal here, because Biolith catches it and retries with a
resilient indexer that drops cycle-forming edges. It is expensive and silent:
the pack shipped one such cycle from 2026-08-30 to 2026-09-01 and the only
evidence was a single WARN line inside a three-minute level-prep block.

The cycle came from two `neoforge:add_features` modifiers adding the *same*
placed feature to *overlapping* biome sets, so eight biomes received it twice at
different positions in `underground_ores`. NeoForge does not deduplicate, so
those biomes also generated the ore at double density.

This validator reads every biome modifier the pack ships and every modifier in
the installed mod jars, resolves biome tags to concrete biomes, and reports any
placed feature injected more than once into the same biome at the same step.

    python dev/scripts/validate_biome_feature_order.py

Exit status is non-zero when a duplicate injection is found.
"""

from __future__ import annotations

import argparse
import json
import sys
import zipfile
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

MODIFIER_DIR_PARTS = ("neoforge", "biome_modifier")
ADD_FEATURES = "neoforge:add_features"
# A modifier whose biome selector this validator cannot resolve is reported
# separately rather than silently treated as matching nothing: an unresolved
# selector could be hiding exactly the overlap being looked for.
UNRESOLVED = "<unresolved>"
# `neoforge:any` matches every biome, so it overlaps every other selector. It is
# resolved to this sentinel rather than to a biome list, because the complete
# biome set is not knowable from files alone - mods register biomes in code.
# Treating it as a concrete member keeps the overlap test exact where it
# matters: two modifiers adding one feature, at least one of them to `any`.
ALL_BIOMES = "<any>"


def iter_json_resources(root: Path, mods: Path) -> Iterable[tuple[str, str, dict[str, Any]]]:
    """Yield (origin, resource_path, parsed) for loose pack data then mod jars.

    Loose files come first so a pack override of a mod resource is seen before
    the jar copy it replaces, matching datapack resolution order.
    """
    for path in sorted(root.rglob("*.json")):
        parts = path.relative_to(root).as_posix().split("/")
        if len(parts) < 4:
            continue
        yield "pack", "/".join(parts), _load(path.read_bytes(), path.as_posix())

    if not mods.is_dir():
        return
    for jar in sorted(mods.glob("*.jar")):
        try:
            archive = zipfile.ZipFile(jar)
        except (zipfile.BadZipFile, OSError):
            continue
        with archive:
            for name in archive.namelist():
                if not name.endswith(".json") or not name.startswith("data/"):
                    continue
                yield jar.name, name, _load(archive.read(name), f"{jar.name}!{name}")


def _load(data: bytes, where: str) -> dict[str, Any]:
    try:
        parsed = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return {}
    return parsed if isinstance(parsed, dict) else {}


def resource_id(resource_path: str, category: tuple[str, ...]) -> str | None:
    """Map `data/<ns>/<category...>/<path>.json` to `<ns>:<path>`."""
    parts = resource_path.split("/")
    if parts and parts[0] == "data":
        parts = parts[1:]
    if len(parts) < len(category) + 2:
        return None
    namespace, rest = parts[0], parts[1:]
    if tuple(rest[: len(category)]) != category:
        return None
    tail = "/".join(rest[len(category) :])
    if not tail.endswith(".json"):
        return None
    return f"{namespace}:{tail[:-5]}"


def collect(root: Path, mods: Path) -> tuple[dict[str, dict[str, Any]], dict[str, list[str]]]:
    """Return the effective biome modifiers and the raw biome-tag contents."""
    modifiers: dict[str, dict[str, Any]] = {}
    tags: dict[str, list[str]] = {}
    tag_replaces: dict[str, bool] = {}

    for _origin, path, parsed in iter_json_resources(root, mods):
        modifier_id = resource_id(path, MODIFIER_DIR_PARTS)
        if modifier_id is not None:
            # First writer wins: loose pack data overrides the jar copy.
            modifiers.setdefault(modifier_id, parsed)
            continue
        tag_id = resource_id(path, ("tags", "worldgen", "biome"))
        if tag_id is None:
            continue
        values = [v for v in parsed.get("values", []) if isinstance(v, str)]
        if parsed.get("replace") and not tag_replaces.get(tag_id):
            tags[tag_id] = list(values)
            tag_replaces[tag_id] = True
        else:
            tags.setdefault(tag_id, []).extend(values)
    return modifiers, tags


def resolve(selector: Any, tags: dict[str, list[str]], seen: frozenset[str] = frozenset()) -> set[str]:
    """Expand a NeoForge biome selector into concrete biome ids.

    `neoforge:any` and unsupported selector objects resolve to UNRESOLVED, which
    the caller reports rather than treating as an empty set.
    """
    if isinstance(selector, str):
        if not selector.startswith("#"):
            return {selector if ":" in selector else f"minecraft:{selector}"}
        tag = selector[1:]
        if ":" not in tag:
            tag = f"minecraft:{tag}"
        if tag in seen:  # a tag cycle resolves to nothing rather than recursing
            return set()
        resolved: set[str] = set()
        for value in tags.get(tag, []):
            resolved |= resolve(value, tags, seen | {tag})
        return resolved
    if isinstance(selector, list):
        resolved = set()
        for entry in selector:
            resolved |= resolve(entry, tags, seen)
        return resolved
    if isinstance(selector, dict):
        kind = selector.get("type")
        if kind == "neoforge:any":
            return {ALL_BIOMES}
        if kind == "neoforge:and":
            parts = [resolve(v, tags, seen) for v in selector.get("values", [])]
            parts = [p for p in parts if UNRESOLVED not in p]
            return set.intersection(*parts) if parts else set()
        if kind == "neoforge:or":
            resolved = set()
            for value in selector.get("values", []):
                resolved |= resolve(value, tags, seen)
            return resolved
        if kind == "neoforge:tag":
            return resolve(selector.get("tag"), tags, seen)
    return {UNRESOLVED}


def find_duplicates(root: Path, mods: Path) -> tuple[list[str], list[str]]:
    modifiers, tags = collect(root, mods)
    # (biome, step, feature) -> modifiers that inject it there
    injections: dict[tuple[str, str, str], list[str]] = defaultdict(list)
    unresolved: list[str] = []

    for modifier_id, body in sorted(modifiers.items()):
        if body.get("type") != ADD_FEATURES:
            continue
        step = str(body.get("step", "<none>"))
        features = body.get("features")
        features = [features] if isinstance(features, str) else features
        if not isinstance(features, list):
            continue
        biomes = resolve(body.get("biomes"), tags)
        if UNRESOLVED in biomes:
            unresolved.append(modifier_id)
            biomes.discard(UNRESOLVED)
        for feature in features:
            if not isinstance(feature, str) or feature.startswith("#"):
                continue
            for biome in biomes:
                injections[(biome, step, feature)].append(modifier_id)

    by_conflict: dict[tuple[str, str, tuple[str, ...]], list[str]] = defaultdict(list)
    for (biome, step, feature), sources in injections.items():
        if len(sources) > 1:
            by_conflict[(feature, step, tuple(sorted(sources)))].append(biome)

    # `neoforge:any` never shares a key with a named biome, so a feature added
    # once to every biome and once to a tag has to be paired up separately.
    everywhere: dict[tuple[str, str], set[str]] = defaultdict(set)
    targeted: dict[tuple[str, str], set[str]] = defaultdict(set)
    for (biome, step, feature), sources in injections.items():
        bucket = everywhere if biome == ALL_BIOMES else targeted
        bucket[(feature, step)].update(sources)
    for key, wide in everywhere.items():
        narrow = targeted.get(key, set())
        combined = wide | narrow
        if len(combined) > 1:
            by_conflict[(key[0], key[1], tuple(sorted(combined)))].append(ALL_BIOMES)

    failures: list[str] = []
    for (feature, step, sources), biomes in sorted(by_conflict.items()):
        listed = ", ".join(sources)
        if biomes == [ALL_BIOMES]:
            scope = "every biome (one modifier targets neoforge:any)"
        else:
            sample = ", ".join(sorted(biomes)[:8])
            more = "" if len(biomes) <= 8 else f" (+{len(biomes) - 8} more)"
            scope = f"{len(biomes)} biome(s): {sample}{more}"
        failures.append(
            f"{feature} is injected at step '{step}' by {len(sources)} modifiers "
            f"[{listed}] into {scope}"
        )
    return failures, unresolved


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    default_root = Path(__file__).resolve().parents[2]
    parser.add_argument("--data", type=Path, default=default_root / "kubejs" / "data")
    parser.add_argument("--mods", type=Path, default=default_root / "mods")
    args = parser.parse_args()

    failures, unresolved = find_duplicates(args.data, args.mods)
    if unresolved:
        print(f"note: {len(unresolved)} modifier(s) use a selector this validator cannot narrow")
        for modifier_id in unresolved[:10]:
            print(f"  - {modifier_id}")
    if failures:
        print(f"\nFAIL: {len(failures)} duplicate feature injection(s) found.")
        print("Each one makes a biome list the same feature twice, which can make the")
        print("vanilla feature sorter unsatisfiable and doubles the feature's density.\n")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print("Biome feature-order validation passed: no feature is injected twice into any biome.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
