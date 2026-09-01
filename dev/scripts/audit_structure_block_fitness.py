from __future__ import annotations

import json
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

from audit_generated_state_values import ROOT, VANILLA_JAR, allowed_values, parse_state
from convert_nbt_to_lostcities import load_structure


# Scan EVERY authored structure category, not just wasteland.
#
# This gate was written for the wasteland corpus and its path was pinned to
# it, so the deep-sea corpus -- which now places modded blocks of its own --
# was never inspected at all. That is how a live `minecraft:blast_furnace`
# survived in three deep-sea assets after docs/RUINED_FUNCTIONAL_BLOCKS.md
# declared the rule retroactive: the corpus was outside the scan path, and the
# block was vanilla so the modded-only filter below would have skipped it even
# if it had not been.
STRUCTURES = ROOT / "kubejs" / "data" / "infinite_domain" / "structure"
REPORT = ROOT / "dev/docs" / "structure-block-fitness-audit.json"
ALLOWLIST = ROOT / "dev/structure_library" / "approved-functional-block-exceptions.json"
DIRECTIONAL = {"facing", "axis", "orientation", "horizontal_facing", "face"}
FUNCTIONAL_TERMS = {
    "basin", "bearing", "boiler", "burner", "cable", "capacitor", "chute", "compressor",
    "conveyor", "controller", "depot", "drill", "engine", "fan", "furnace", "generator",
    "gearbox", "lathe", "mixer", "motor", "press", "pump", "reactor", "saw", "shaft",
    "tank", "turbine", "valve",
}
CONNECTIVE_TERMS = {"fence", "girder", "pipe", "scaffold", "truss", "wall"}
# Rule 2 of docs/RUINED_FUNCTIONAL_BLOCKS.md names these explicitly, and they
# are vanilla, so the modded-only sweep below cannot see them. They are the
# small-scale version of the same tech-skip problem: a player who mines a
# working blast furnace out of a ruin skips the progression it gates.
VANILLA_FORBIDDEN = {
    "minecraft:furnace", "minecraft:smoker", "minecraft:blast_furnace",
    "minecraft:brewing_stand", "minecraft:beacon", "minecraft:conduit",
}


def structure_label(path: Path) -> str:
    return path.relative_to(STRUCTURES).with_suffix("").as_posix()


def main() -> None:
    files = sorted(STRUCTURES.rglob("*.nbt"))
    usage: dict[str, Counter[str]] = defaultdict(Counter)
    states: dict[str, set[str]] = defaultdict(set)
    all_blocks: set[str] = set()
    for path in files:
        label = structure_label(path)
        _size, blocks = load_structure(path)
        for state, _tag in blocks.values():
            block, _properties = parse_state(state)
            all_blocks.add(block)
            usage[block][label] += 1
            states[block].add(state)

    resources = {
        f"assets/{block.split(':', 1)[0]}/blockstates/{block.split(':', 1)[1]}.json": block
        for block in all_blocks
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

    records = []
    implicit_directional = []
    connective = []
    for block in sorted(block for block in all_blocks if not block.startswith("minecraft:")):
        selector_properties: set[str] = set()
        for document in definitions.get(block, []):
            values, _non_exhaustive = allowed_values(document)
            selector_properties.update(values)
        directional_properties = sorted(selector_properties & DIRECTIONAL)
        block_states = sorted(states[block])
        implicit = []
        for state in block_states:
            _name, properties = parse_state(state)
            missing = sorted(set(directional_properties) - set(properties))
            if missing:
                implicit.append({"state": state, "missing": missing})
                implicit_directional.append({"block": block, "state": state, "missing": missing})
        path = block.split(":", 1)[1]
        terms = set(path.replace("/", "_").split("_"))
        functional = bool(terms & FUNCTIONAL_TERMS)
        is_connective = bool(terms & CONNECTIVE_TERMS)
        if is_connective:
            connective.append(block)
        records.append({
            "block": block,
            "placements": sum(usage[block].values()),
            "structures": sorted(usage[block]),
            "states": block_states,
            "selector_properties": sorted(selector_properties),
            "functional_or_machine": functional,
            "connective_material": is_connective,
            "implicit_directional_states": implicit,
        })

    allowlist_document = json.loads(ALLOWLIST.read_text(encoding="utf-8")) if ALLOWLIST.exists() else {"approved_exceptions": []}
    allowed = {
        entry["block"]: entry
        for entry in allowlist_document.get("approved_exceptions", [])
    }
    failures = []
    violations = []
    for record in records:
        if not record["functional_or_machine"]:
            continue
        exception = allowed.get(record["block"])
        if exception is None:
            violations.append({
                "block": record["block"],
                "placements": record["placements"],
                "structures": record["structures"],
                "reason": "live-functional/machine block used as structure set dressing with no approved exception on file",
            })
            continue
        allowed_structures = set(exception.get("structures", []))
        unlisted = sorted(set(record["structures"]) - allowed_structures) if allowed_structures else []
        if unlisted:
            violations.append({
                "block": record["block"],
                "placements": record["placements"],
                "structures": unlisted,
                "reason": f"placed in structures not covered by its approved exception (approved for: {sorted(allowed_structures) or 'none listed'})",
            })
    for block in sorted(all_blocks & VANILLA_FORBIDDEN):
        exception = allowed.get(block)
        structures = sorted(usage[block])
        if exception is not None:
            allowed_structures = set(exception.get("structures", []))
            structures = sorted(set(structures) - allowed_structures) if allowed_structures else []
        if structures:
            violations.append({
                "block": block,
                "placements": sum(usage[block].values()),
                "structures": structures,
                "reason": "live-functional vanilla block named in docs/RUINED_FUNCTIONAL_BLOCKS.md rule 2 "
                          "placed as set dressing; use the infinite_domain:ruined_* equivalent",
            })

    if violations:
        failures.append(
            f"{len(violations)} live-functional/machine block type(s) are placed as structure set dressing without an "
            f"approved exception in {ALLOWLIST.relative_to(ROOT).as_posix()} "
            "(see docs/RUINED_FUNCTIONAL_BLOCKS.md for the required vanilla/ruined-equivalent stand-ins)"
        )

    report = {
        "templates_scanned": len(files),
        "modded_block_types": len(records),
        "categories_scanned": sorted({p.relative_to(STRUCTURES).parts[0] for p in files}),
        "policy": "Vanilla stable blocks are the default. No live-functional/machine block may be placed as structure set dressing "
                  "unless it has an explicit, structure-scoped exception in approved-functional-block-exceptions.json; the "
                  "required default is a vanilla proxy or, where one exists, an infinite_domain:ruined_* decorative equivalent. "
                  "Modded directional, connective, kinetic, fluid and block-entity blocks otherwise require an explicit purpose "
                  "and verified state.",
        "implicit_directional_states": implicit_directional,
        "connective_block_types": sorted(connective),
        "functional_block_violations": violations,
        "gate_passed": not failures,
        "modded_usage": records,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Scanned {len(files)} templates containing {len(records)} modded block types")
    print(f"Implicit directional states: {len(implicit_directional)}")
    print(f"Connective modded block types requiring placement review: {len(connective)}")
    print(f"Functional/machine block violations: {len(violations)}")
    if failures:
        raise SystemExit("Structure block-fitness gate failed:\n- " + "\n- ".join(failures))


if __name__ == "__main__":
    main()
