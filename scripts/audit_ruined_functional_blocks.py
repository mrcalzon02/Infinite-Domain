#!/usr/bin/env python3
"""Audit/apply inert ruined workstations in authored terrestrial structures.

The equivalence targets are registered by
``kubejs/startup_scripts/ruined_worldgen_furnaces.js``. This tool validates
that every mapped target is present in that KubeJS index, then audits the
already-serialized surface NBT corpus and Lost Cities converted part palettes.

Run without arguments for a read-only gate. Use ``--apply`` to normalize the
assets and write the durable audit report.
"""
from __future__ import annotations

import argparse
import gzip
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

from build_structure_qa_world import NbtList, Reader, Tag, payload, utf
from generate_wasteland_sites import (
    RUINED_FUNCTIONAL_BLOCK_PROPERTIES,
    RUINED_FUNCTIONAL_BLOCK_REPLACEMENTS,
)

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "kubejs" / "data" / "infinite_domain"
KUBEJS_INDEX = ROOT / "kubejs" / "startup_scripts" / "ruined_worldgen_furnaces.js"
REPORT = ROOT / "docs" / "ruined-functional-block-structure-audit.json"
NBT_ROOTS = (
    DATA / "structure" / "wasteland",
    DATA / "structure" / "karsic",
)
LOST_CITIES_PART_ROOT = DATA / "lostcities" / "parts" / "converted"
STATE_RE = re.compile(r"^([^\[]+)(?:\[(.*)\])?$")
RUINED_TARGETS = frozenset(RUINED_FUNCTIONAL_BLOCK_REPLACEMENTS.values())


def properties_from_tag(state: dict[str, Tag]) -> dict[str, str]:
    properties = state.get("Properties")
    if properties is None:
        return {}
    return {key: value.value for key, value in properties.value.items()}


def normalized_state(name: str, properties: dict[str, str]) -> tuple[str, dict[str, str]]:
    target = RUINED_FUNCTIONAL_BLOCK_REPLACEMENTS.get(name, name)
    if target == name:
        return name, properties
    allowed = RUINED_FUNCTIONAL_BLOCK_PROPERTIES.get(target, frozenset())
    return target, {key: value for key, value in properties.items() if key in allowed}


def state_key(name: str, properties: dict[str, str]) -> tuple[str, tuple[tuple[str, str], ...]]:
    return name, tuple(sorted(properties.items()))


def set_state_tag(state: dict[str, Tag], name: str, properties: dict[str, str]) -> None:
    state["Name"] = Tag(8, name)
    if properties:
        state["Properties"] = Tag(10, {key: Tag(8, value) for key, value in sorted(properties.items())})
    else:
        state.pop("Properties", None)


def encode_root(root_name: str, root: Tag) -> bytes:
    return bytes([10]) + utf(root_name) + payload(root)


def audit_nbt(path: Path, apply: bool, violations: list[dict[str, Any]]) -> dict[str, Any] | None:
    root_name, root = Reader(gzip.decompress(path.read_bytes())).root()
    document = root.value
    palette_values = document["palette"].value.values
    source_by_index: dict[int, str] = {}
    name_by_index: dict[int, str] = {}
    normalized: list[tuple[str, dict[str, str]]] = []
    for index, state_tag in enumerate(palette_values):
        state = state_tag.value
        source = state["Name"].value
        props = properties_from_tag(state)
        name_by_index[index] = source
        if source.startswith("infinite_domain:ruined_"):
            violations.append({"path": path.relative_to(ROOT).as_posix(), "reason": f"nonexistent legacy ruined ID {source}"})
        if source in RUINED_TARGETS:
            unsupported = sorted(set(props) - RUINED_FUNCTIONAL_BLOCK_PROPERTIES.get(source, frozenset()))
            if unsupported:
                violations.append({"path": path.relative_to(ROOT).as_posix(), "reason": f"{source} has unsupported properties {unsupported}"})
        target, target_props = normalized_state(source, props)
        normalized.append((target, target_props))
        if target != source:
            source_by_index[index] = source

    if not source_by_index:
        return None

    instances = Counter()
    stripped_block_entities = 0
    for block_tag in document["blocks"].value.values:
        block = block_tag.value
        old_index = int(block["state"].value)
        if name_by_index[old_index] in RUINED_TARGETS and "nbt" in block:
            violations.append({"path": path.relative_to(ROOT).as_posix(), "reason": f"{name_by_index[old_index]} retains block-entity NBT"})
        source = source_by_index.get(old_index)
        if source is not None:
            instances[source] += 1
            if "nbt" in block:
                stripped_block_entities += 1
                if apply:
                    block.pop("nbt", None)

    if apply:
        new_palette: list[Tag] = []
        key_to_index: dict[tuple[str, tuple[tuple[str, str], ...]], int] = {}
        old_to_new: dict[int, int] = {}
        for old_index, (name, props) in enumerate(normalized):
            key = state_key(name, props)
            if key not in key_to_index:
                state: dict[str, Tag] = {}
                set_state_tag(state, name, props)
                key_to_index[key] = len(new_palette)
                new_palette.append(Tag(10, state))
            old_to_new[old_index] = key_to_index[key]
        document["palette"] = Tag(9, NbtList(10, new_palette))
        for block_tag in document["blocks"].value.values:
            state = block_tag.value["state"]
            state.value = old_to_new[int(state.value)]
        path.write_bytes(gzip.compress(encode_root(root_name, root), mtime=0))

    return {
        "path": path.relative_to(ROOT).as_posix(),
        "format": "structure_nbt",
        "source_palette_states": len(source_by_index),
        "block_instances": sum(instances.values()),
        "stripped_block_entity_payloads": stripped_block_entities,
        "by_source": dict(sorted(instances.items())),
    }


def parse_state(value: str) -> tuple[str, dict[str, str]]:
    match = STATE_RE.fullmatch(value)
    if not match:
        raise ValueError(f"invalid block-state string: {value}")
    name, raw = match.groups()
    properties: dict[str, str] = {}
    if raw:
        for pair in raw.split(","):
            key, item = pair.split("=", 1)
            properties[key] = item
    return name, properties


def format_state(name: str, properties: dict[str, str]) -> str:
    if not properties:
        return name
    return name + "[" + ",".join(f"{key}={properties[key]}" for key in sorted(properties)) + "]"


def palette_instance_count(document: dict[str, Any], char: str) -> int:
    return sum(row.count(char) for layer in document.get("slices", []) for row in layer)


def audit_lost_cities_part(path: Path, apply: bool, violations: list[dict[str, Any]]) -> dict[str, Any] | None:
    document = json.loads(path.read_text(encoding="utf-8"))
    palette = document.get("palette", {}).get("palette", [])
    instances = Counter()
    changed_states = 0
    stripped_tags = 0
    for entry in palette:
        source, props = parse_state(entry["block"])
        if source.startswith("infinite_domain:ruined_"):
            violations.append({"path": path.relative_to(ROOT).as_posix(), "reason": f"nonexistent legacy ruined ID {source}"})
        if source in RUINED_TARGETS:
            unsupported = sorted(set(props) - RUINED_FUNCTIONAL_BLOCK_PROPERTIES.get(source, frozenset()))
            if unsupported:
                violations.append({"path": path.relative_to(ROOT).as_posix(), "reason": f"{source} has unsupported properties {unsupported}"})
            if "tag" in entry:
                violations.append({"path": path.relative_to(ROOT).as_posix(), "reason": f"{source} retains block-entity tag data"})
        target, target_props = normalized_state(source, props)
        if target == source:
            continue
        changed_states += 1
        instances[source] += palette_instance_count(document, entry["char"])
        if "tag" in entry:
            stripped_tags += 1
        if apply:
            entry["block"] = format_state(target, target_props)
            entry.pop("tag", None)
    if not changed_states:
        return None
    if apply:
        path.write_text(json.dumps(document, indent=2, ensure_ascii=True) + "\n", encoding="utf-8", newline="\n")
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "format": "lost_cities_part",
        "source_palette_states": changed_states,
        "block_instances": sum(instances.values()),
        "stripped_block_entity_payloads": stripped_tags,
        "by_source": dict(sorted(instances.items())),
    }


def index_targets() -> set[str]:
    text = KUBEJS_INDEX.read_text(encoding="utf-8")
    return {f"kubejs:{value}" for value in re.findall(r"\bid:\s*'([^']+)'", text)}


def validate_index() -> None:
    registered = index_targets()
    expected = set(RUINED_FUNCTIONAL_BLOCK_REPLACEMENTS.values())
    missing = sorted(expected - registered)
    if missing:
        raise SystemExit("ruined mapping targets absent from KubeJS index: " + ", ".join(missing))


def scan(apply: bool) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    findings: list[dict[str, Any]] = []
    violations: list[dict[str, Any]] = []
    for root in NBT_ROOTS:
        if root.is_dir():
            for path in sorted(root.rglob("*.nbt")):
                result = audit_nbt(path, apply, violations)
                if result:
                    findings.append(result)
    if LOST_CITIES_PART_ROOT.is_dir():
        for path in sorted(LOST_CITIES_PART_ROOT.rglob("*.json")):
            result = audit_lost_cities_part(path, apply, violations)
            if result:
                findings.append(result)
    return findings, violations


def aggregate(findings: list[dict[str, Any]]) -> dict[str, Any]:
    by_source = Counter()
    for finding in findings:
        by_source.update(finding["by_source"])
    by_target = Counter()
    for source, count in by_source.items():
        by_target[RUINED_FUNCTIONAL_BLOCK_REPLACEMENTS[source]] += count
    return {
        "assets_changed": len(findings),
        "source_palette_states_changed": sum(item["source_palette_states"] for item in findings),
        "block_instances_changed": sum(item["block_instances"] for item in findings),
        "block_entity_payloads_stripped": sum(item["stripped_block_entity_payloads"] for item in findings),
        "by_source": dict(sorted(by_source.items())),
        "by_target": dict(sorted(by_target.items())),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="rewrite affected NBT and Lost Cities part palettes")
    args = parser.parse_args()
    validate_index()
    findings, preexisting_target_violations = scan(args.apply)
    summary = aggregate(findings)
    if args.apply:
        residual, postcondition_violations = scan(False)
        report = {
            "purpose": "Audit and remediation record for inert ruined equivalents in authored terrestrial surface structures.",
            "authoritative_kubejs_index": KUBEJS_INDEX.relative_to(ROOT).as_posix(),
            "scope": {
                "nbt_roots": [path.relative_to(ROOT).as_posix() for path in NBT_ROOTS],
                "lost_cities_parts": LOST_CITIES_PART_ROOT.relative_to(ROOT).as_posix(),
                "excluded": ["abyssal/deep-sea structures", "offworld/alien/minor-planet structures", "licensed donor quarantine/extracted assets"],
            },
            "equivalences": dict(sorted(RUINED_FUNCTIONAL_BLOCK_REPLACEMENTS.items())),
            "summary": summary,
            "residual_functional_palette_states": len(residual),
            "preexisting_ruined_target_violations": preexisting_target_violations,
            "postcondition_violations": postcondition_violations,
            "assets": findings,
        }
        REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")
        print(f"updated {summary['assets_changed']} assets / {summary['block_instances_changed']} block instances")
        print(f"stripped {summary['block_entity_payloads_stripped']} incompatible block-entity payloads")
        print(f"residual affected assets: {len(residual)}")
        print(f"postcondition violations: {len(postcondition_violations)}")
        print(f"report: {REPORT.relative_to(ROOT).as_posix()}")
        return 1 if residual or postcondition_violations else 0
    print(f"affected assets: {summary['assets_changed']}")
    print(f"affected block instances: {summary['block_instances_changed']}")
    for source, count in summary["by_source"].items():
        print(f"  {source:<38} {count:>8} -> {RUINED_FUNCTIONAL_BLOCK_REPLACEMENTS[source]}")
    if preexisting_target_violations:
        print(f"ruined-target postcondition violations: {len(preexisting_target_violations)}")
        for violation in preexisting_target_violations[:20]:
            print(f"  {violation['path']}: {violation['reason']}")
    return 1 if findings or preexisting_target_violations else 0


if __name__ == "__main__":
    raise SystemExit(main())
