from __future__ import annotations

import json
import sys
import zipfile
from collections import defaultdict
from pathlib import Path

from convert_nbt_to_lostcities import load_structure


ROOT = Path(__file__).resolve().parents[2]
STRUCTURES = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland"
VANILLA_JAR = ROOT.parent.parent / "Install" / "versions" / "1.21.1" / "1.21.1.jar"
REPORT = ROOT / "dev/docs" / "generated-structure-state-audit.json"
BLOCK_REGISTRY = ROOT / "dev/docs" / "registry-inventory" / "block-ids.txt"

BOOL = {"true", "false"}
HORIZONTAL = {"north", "east", "south", "west"}


def explicit_domain(block: str, prop: str) -> set[str] | None:
    path = block.split(":", 1)[1] if ":" in block else block
    if block == "minecraft:brewing_stand" and prop.startswith("has_bottle_"):
        return BOOL
    if block == "minecraft:composter" and prop == "level":
        return {str(value) for value in range(9)}
    if path.endswith("_bed"):
        return {"foot", "head"} if prop == "part" else (HORIZONTAL if prop == "facing" else (BOOL if prop == "occupied" else None))
    if prop == "waterlogged" and (
        path.endswith(("_slab", "_stairs", "_trapdoor"))
        or block in {"minecraft:chest", "minecraft:ladder", "minecraft:lantern", "minecraft:lightning_rod", "minecraft:rail", "minecraft:campfire"}
    ):
        return BOOL
    if prop == "powered" and (path.endswith(("_door", "_trapdoor")) or block in {"minecraft:bell", "minecraft:lectern"}):
        return BOOL
    if path.endswith("_leaves"):
        return BOOL if prop == "persistent" else ({str(value) for value in range(1, 8)} if prop == "distance" else None)
    fixed = {
        ("minecraft:campfire", "signal_fire"): BOOL,
        ("minecraft:chest", "facing"): HORIZONTAL,
        ("minecraft:chest", "type"): {"single", "left", "right"},
        ("minecraft:fire", "age"): {str(value) for value in range(16)},
        ("minecraft:lectern", "has_book"): BOOL,
        ("minecraft:skeleton_skull", "rotation"): {str(value) for value in range(16)},
        ("minecraft:target", "power"): {str(value) for value in range(16)},
        ("minecraft:water", "level"): {str(value) for value in range(16)},
    }
    return fixed.get((block, prop))


def parse_state(value: str) -> tuple[str, dict[str, str]]:
    if "[" not in value:
        return value, {}
    block, raw = value[:-1].split("[", 1)
    return block, dict(pair.split("=", 1) for pair in raw.split(","))


def collect_condition_values(condition: object, values: dict[str, set[str]]) -> None:
    if isinstance(condition, list):
        for child in condition:
            collect_condition_values(child, values)
        return
    if not isinstance(condition, dict):
        return
    for key, value in condition.items():
        if key in {"OR", "AND"}:
            collect_condition_values(value, values)
        elif isinstance(value, str):
            values[key].update(value.split("|"))


def allowed_values(document: dict[str, object]) -> tuple[dict[str, set[str]], bool]:
    values: dict[str, set[str]] = defaultdict(set)
    variants = document.get("variants", {})
    has_default_selector = isinstance(variants, dict) and "" in variants
    if isinstance(variants, dict):
        for selector in variants:
            if not selector:
                continue
            for pair in selector.split(","):
                key, value = pair.split("=", 1)
                values[key].update(value.split("|"))
    multipart = document.get("multipart", [])
    has_unconditional_part = False
    if isinstance(multipart, list):
        for entry in multipart:
            if isinstance(entry, dict):
                if "when" in entry:
                    collect_condition_values(entry["when"], values)
                else:
                    has_unconditional_part = True
    return values, has_default_selector or has_unconditional_part


def main() -> None:
    files = sorted(STRUCTURES.rglob("*.nbt"))
    occurrences: dict[str, set[tuple[str, tuple[tuple[str, str], ...]]]] = defaultdict(set)
    all_blocks: set[str] = set()
    for path in files:
        _size, blocks = load_structure(path)
        for state, _tag in blocks.values():
            block, properties = parse_state(state)
            all_blocks.add(block)
            if properties:
                occurrences[block].add((state, tuple(sorted(properties.items()))))

    resources = {
        f"assets/{block.split(':', 1)[0]}/blockstates/{block.split(':', 1)[1]}.json": block
        for block in occurrences
    }
    definitions: dict[str, list[dict[str, object]]] = defaultdict(list)
    archives = [VANILLA_JAR, *sorted((ROOT / "mods").glob("*.jar"))]
    for archive in archives:
        if not archive.is_file():
            continue
        try:
            with zipfile.ZipFile(archive) as jar:
                names = set(jar.namelist())
                for resource, block in resources.items():
                    if resource in names:
                        definitions[block].append(json.loads(jar.read(resource)))
        except (OSError, zipfile.BadZipFile, json.JSONDecodeError):
            continue

    invalid: list[tuple[str, str, str, list[str]]] = []
    non_exhaustive: set[tuple[str, str, str]] = set()
    unrepresented: set[tuple[str, str, str]] = set()
    missing_definitions: set[str] = set()
    unresolved: set[tuple[str, str, str]] = set()
    explicit_values_checked = 0
    checked_values = 0
    for block, states in occurrences.items():
        allowed: dict[str, set[str]] = defaultdict(set)
        has_default_selector = False
        for document in definitions.get(block, []):
            document_values, document_has_default = allowed_values(document)
            has_default_selector = has_default_selector or document_has_default
            for key, values in document_values.items():
                allowed[key].update(values)
        for state, properties_tuple in states:
            for key, value in properties_tuple:
                # An empty variant selector or unconditional multipart commonly
                # represents a valid default value omitted from named selectors
                # (for example composter level 0), so the resource is not an
                # exhaustive value list.
                if key in allowed and not has_default_selector:
                    checked_values += 1
                    if value not in allowed[key]:
                        invalid.append((state, key, value, sorted(allowed[key])))
                elif key in allowed:
                    non_exhaustive.add((block, key, value))
                    domain = explicit_domain(block, key)
                    if domain is None:
                        unresolved.add((block, key, value))
                    else:
                        explicit_values_checked += 1
                        if value not in domain:
                            invalid.append((state, key, value, sorted(domain)))
                else:
                    unrepresented.add((block, key, value))
                    if block not in definitions:
                        missing_definitions.add(block)
                    domain = explicit_domain(block, key)
                    if domain is None:
                        unresolved.add((block, key, value))
                    else:
                        explicit_values_checked += 1
                        if value not in domain:
                            invalid.append((state, key, value, sorted(domain)))

    registered_blocks = {
        line.strip() for line in BLOCK_REGISTRY.read_text(encoding="utf-8").splitlines() if line.strip()
    }
    unknown_blocks = sorted(all_blocks - registered_blocks)

    report = {
        "templates_scanned": len(files),
        "property_bearing_block_types": len(occurrences),
        "strict_property_values_checked": checked_values,
        "explicit_domain_values_checked": explicit_values_checked,
        "invalid": [
            {"state": state, "property": key, "value": value, "allowed": allowed}
            for state, key, value, allowed in invalid
        ],
        "non_exhaustive_selector_uses": [
            {"block": block, "property": key, "value": value}
            for block, key, value in sorted(non_exhaustive)
        ],
        "unrepresented_property_uses": [
            {"block": block, "property": key, "value": value}
            for block, key, value in sorted(unrepresented)
        ],
        "property_bearing_blocks_without_definition": sorted(missing_definitions),
        "unresolved_property_uses": [
            {"block": block, "property": key, "value": value}
            for block, key, value in sorted(unresolved)
        ],
        "unknown_block_ids": unknown_blocks,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print(f"Scanned {len(files)} generated NBT templates and {len(occurrences)} property-bearing block types")
    print(f"Checked {checked_values} property values represented by installed blockstate definitions")
    print(f"Checked {explicit_values_checked} selector-omitted values against explicit block domains")
    print(f"Non-exhaustive selector uses requiring domain review: {len(non_exhaustive)}")
    print(f"Properties absent from rendering selectors requiring registry review: {len(unrepresented)}")
    print(f"Property-bearing blocks without an installed definition: {len(missing_definitions)}")
    print(f"Unresolved property uses: {len(unresolved)}")
    print(f"Unknown block IDs: {len(unknown_blocks)}")
    if invalid:
        for state, key, value, allowed in invalid:
            print(f"INVALID {state}: {key}={value}; allowed={','.join(allowed)}")
        raise SystemExit(f"Found {len(invalid)} definitely invalid generated block-state values")
    if unresolved or unknown_blocks:
        for block, key, value in sorted(unresolved):
            print(f"UNRESOLVED {block}[{key}={value}]")
        for block in unknown_blocks:
            print(f"UNKNOWN_BLOCK {block}")
        raise SystemExit("Generated block-state audit has unresolved entries")
    print("No definitely invalid generated block-state values found")


if __name__ == "__main__":
    main()
