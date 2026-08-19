from __future__ import annotations

import gzip
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

from build_structure_qa_world import NbtList, Reader, Tag
from convert_nbt_to_lostcities import state_string, tag_value
from generate_wasteland_sites import STRUCTURE_BLOCK_REPLACEMENTS, Template
import extract_modular_structure_kits as extractor

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "structure_library" / "modules" / "structure-kits.json"
MAIN_CATALOG = ROOT / "structure_library" / "catalog.json"
REPORT = ROOT / "docs" / "structure-kit-validation.json"
CONNECTOR = re.compile(r"^[a-z]+_(north|east|south|west|any)$")

REQUIRED_ROLE_PREFIXES = {
    "port_dock": {"wharf", "warehouse", "dockmaster", "road_rail", "fuel_tank", "fuel_loading"},
    "marketplace": {"specialist", "covered", "public"},
    "industrial": {"administration", "truck", "warehouse", "rail", "freight", "sequential", "utility"},
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def normalize(value):
    if isinstance(value, NbtList):
        return [normalize(item) for item in value.values]
    if isinstance(value, dict):
        return {key: normalize(item) for key, item in value.items()}
    if isinstance(value, list):
        return [normalize(item) for item in value]
    return value


def expected_snapshot(template: Template):
    values = {}
    for pos, (index, nbt) in template.blocks.items():
        state = template.palette[index]
        encoded = state["Name"]
        if state.get("Properties"):
            encoded += "[" + ",".join(f"{key}={state['Properties'][key]}" for key in sorted(state["Properties"])) + "]"
        values[pos] = (encoded, normalize(nbt) if nbt else None)
    return values


def actual_snapshot(path: Path):
    _, root = Reader(gzip.decompress(path.read_bytes())).root()
    document = root.value
    size = tuple(int(value.value) for value in document["size"].value.values)
    palette = [state_string(value) for value in document["palette"].value.values]
    values = {}
    for block_tag in document["blocks"].value.values:
        block = block_tag.value
        pos = tuple(int(value.value) for value in block["pos"].value.values)
        nbt = tag_value(block["nbt"]) if "nbt" in block else None
        values[pos] = (palette[int(block["state"].value)], nbt)
    return size, values


def role_prefix(role: str) -> str:
    for prefix in ("specialist", "warehouse", "dockmaster", "road_rail", "fuel_tank", "fuel_loading", "wharf", "covered", "public", "administration", "truck", "rail", "freight", "sequential", "utility"):
        if role.startswith(prefix):
            return prefix
    return role.split("_", 1)[0]


def main() -> None:
    document = load(CATALOG)
    main_catalog = {record["structure_id"]: record for record in load(MAIN_CATALOG)["structures"]}
    records = document["modules"]
    failures = []
    results = {}
    if document.get("production_approvals"):
        failures.append("module kits must remain quarantined until assembly review")
    if len(document.get("required_approval_checks", [])) != 4:
        failures.append("module production approval contract is incomplete")
    spec_by_id = {f"infinite_domain:{spec.module_id}": spec for spec in extractor.SPECS}
    if set(spec_by_id) != {record["module_id"] for record in records}:
        failures.append("module catalog and extraction specification disagree")
    kit_roles: dict[str, set[str]] = {kit: set() for kit in REQUIRED_ROLE_PREFIXES}
    for record in records:
        issues = []
        spec = spec_by_id.get(record["module_id"])
        if not spec:
            continue
        source_id = record["source_clean_master"]
        source_record = main_catalog.get(source_id)
        if not source_record or source_record.get("source_role") != "clean_master":
            issues.append("source is not a registered clean master")
        x1, y1, z1, x2, y2, z2 = record["source_bounds_inclusive"]
        source = spec.builder()
        sx, sy, sz = source.size
        if not (0 <= x1 <= x2 < sx and 0 <= y1 <= y2 < sy and 0 <= z1 <= z2 < sz):
            issues.append("extraction bounds leave the source template")
        expected = extractor.crop(source, tuple(record["source_bounds_inclusive"]))
        path = ROOT / record["source_template"]
        size, actual = actual_snapshot(path)
        if size != tuple(record["size"]) or size != expected.size:
            issues.append("catalog, source crop and output NBT dimensions disagree")
        if actual != expected_snapshot(expected):
            issues.append("output NBT is not an exact stabilized crop of the declared clean master")
        if hashlib.sha256(path.read_bytes()).hexdigest() != record.get("source_sha256"):
            issues.append("output NBT hash disagrees with catalog")
        palette = {state.split("[", 1)[0] for state, _nbt in actual.values()}
        prohibited = sorted(palette & set(STRUCTURE_BLOCK_REPLACEMENTS))
        if prohibited:
            issues.append("prohibited programmatic-placement blocks: " + ", ".join(prohibited))
        if len(actual) < 12:
            issues.append("module is effectively empty")
        if not record["connectors"] or len(record["connectors"]) != len(set(record["connectors"])):
            issues.append("connector list is empty or duplicated")
        if any(not CONNECTOR.fullmatch(connector) for connector in record["connectors"]):
            issues.append("connector name does not declare a semantic class and face")
        if record.get("source_license") != "Infinite Domain original work; distributable with the modpack":
            issues.append("module redistribution license is missing")
        if record["role"] == "road_rail_mountain_connector":
            if record.get("placement_context") != "terrain_embedded" or record.get("terrain_adaptation_requirement") != "bury_or_mountain_mask":
                issues.append("mountain tunnel casing is not explicitly constrained to terrain-embedded placement")
        elif record.get("placement_context") != "surface_module":
            issues.append("ordinary kit module has an unexpected placement context")
        kit_roles.setdefault(record["kit"], set()).add(role_prefix(record["role"]))
        failures.extend(f"{record['module_id']}: {issue}" for issue in issues)
        results[record["module_id"]] = {
            "kit": record["kit"],
            "role": record["role"],
            "source_clean_master": source_id,
            "size": list(size),
            "placed_records_including_air": len(actual),
            "palette_blocks": len(palette),
            "issues": issues,
        }
    for kit, required in REQUIRED_ROLE_PREFIXES.items():
        missing = sorted(required - kit_roles.get(kit, set()))
        if missing:
            failures.append(f"{kit}: missing representative module roles: {', '.join(missing)}")
    report = {
        "scope": "Exact clean-master crop, stabilized palette, connector declaration, licensing and representative kit-role validation.",
        "kits_checked": len(kit_roles),
        "modules_checked": len(records),
        "source_clean_masters": len({record["source_clean_master"] for record in records}),
        "modules_by_kit": dict(sorted(Counter(record["kit"] for record in records).items())),
        "static_module_contracts_passed": not failures,
        "production_approvals": len(document.get("production_approvals", [])),
        "runtime_status": "pending_in_game_boundary_rotation_and_multi_module_assembly",
        "known_source_limitations": document.get("known_source_limitations", []),
        "failures": failures,
        "modules": results,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if failures:
        raise SystemExit("Structure-kit validation failed:\n- " + "\n- ".join(failures))
    print(f"Validated {len(records)} exact clean-master modules across {len(kit_roles)} reusable kits")


if __name__ == "__main__":
    main()
