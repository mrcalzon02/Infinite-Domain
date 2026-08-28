#!/usr/bin/env python3
"""[SYSTEM REPORT] Static contract validator for the abyssal feature build queue."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "tools/abyssal_worldgen/abyssal_feature_catalog.json"
STRUCTURES = ROOT / "kubejs/data/infinite_domain/worldgen/structure/abyssal"
STRUCTURE_SETS = ROOT / "kubejs/data/infinite_domain/worldgen/structure_set/abyssal"
TEMPLATE_POOLS = ROOT / "kubejs/data/infinite_domain/worldgen/template_pool/abyssal"
NBT = ROOT / "kubejs/data/infinite_domain/structure/abyssal"

EXPECTED_ORDER = [
    "SF-REVIEW-002", "SF-REVIEW-003",
    "OSF-005", "OSF-006", "OSF-007", "OSF-019", "OSF-023",
    "OSF-027", "OSF-037", "OSF-045", "OSF-049",
    "OSF-008", "OSF-009", "OSF-010", "OSF-011", "OSF-012",
    "OSF-024", "OSF-028", "OSF-029", "OSF-031", "OSF-033",
    "OSF-001", "OSF-014", "OSF-015", "OSF-032", "OSF-046", "OSF-050",
    "AGE-004", "AGE-011", "AGE-001", "AGE-002", "AGE-012", "AGE-003", "AGE-013", "AGE-014", "AGE-015",
    "OSF-013", "OSF-016", "OSF-017", "OSF-018", "OSF-020", "OSF-021", "OSF-022",
    "OSF-034", "OSF-035", "OSF-036", "OSF-038", "OSF-039", "OSF-040", "OSF-041", "OSF-042",
    "OSF-044", "OSF-047", "OSF-048", "OSF-051", "OSF-052", "OSF-053", "OSF-054", "OSF-055", "OSF-056",
]
REQUIRED = {
    "planning_id", "name", "registry_id", "faction", "state",
    "implementation_type", "source_path", "target_selectors", "depth_zones",
    "footprint", "projection", "terrain_adaptation", "placement", "palette",
    "geometry_contract", "hazards", "loot_policy", "runtime_validation",
}


def fail(message: str) -> None:
    print(f"[ABYSSAL FEATURE CATALOG FAIL] {message}", file=sys.stderr)
    raise SystemExit(1)


def load(path: Path):
    if not path.is_file():
        fail(f"missing required file: {path.relative_to(ROOT)}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")


def serialized(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def validate_footprint(fid: str, footprint: dict) -> None:
    if all(k in footprint for k in ("x", "y", "z")):
        dims = [footprint[k] for k in ("x", "y", "z")]
        if any(not isinstance(v, int) or v <= 0 or v > 128 for v in dims):
            fail(f"{fid} has invalid fixed footprint {dims}")
        return
    for axis in ("x_range", "y_range", "z_range"):
        rng = footprint.get(axis)
        if not isinstance(rng, list) or len(rng) != 2 or any(not isinstance(v, int) for v in rng):
            fail(f"{fid} missing valid {axis}")
        if rng[0] <= 0 or rng[1] < rng[0] or rng[1] > 256:
            fail(f"{fid} has invalid {axis}: {rng}")


def require_source(feature: dict) -> None:
    fid = feature["planning_id"]
    source = feature.get("source_path")
    if not source or not (ROOT / source).is_file():
        fail(f"{fid} source_path is not an existing authoritative source")


def validate_live_structure(feature: dict) -> None:
    fid = feature["planning_id"]
    registry = feature["registry_id"]
    if not registry or not registry.startswith("infinite_domain:abyssal/"):
        fail(f"{fid} live structure lacks stable abyssal registry ID")
    name = registry.rsplit("/", 1)[-1]
    structure_path = STRUCTURES / f"{name}.json"
    set_path = STRUCTURE_SETS / f"{name}.json"
    structure = load(structure_path)
    structure_set = load(set_path)

    assets = feature.get("materialized_assets")
    if assets is not None:
        if not isinstance(assets, list) or not assets:
            fail(f"{fid} materialized_assets must be a non-empty list")
        pool_id = feature.get("template_pool_id")
        if not pool_id or not pool_id.startswith("infinite_domain:abyssal/"):
            fail(f"{fid} multi-variant structure lacks a stable template_pool_id")
        if structure.get("start_pool") != pool_id:
            fail(f"{fid} structure start_pool disagrees with catalog template_pool_id")
        pool_name = pool_id.rsplit("/", 1)[-1]
        pool = load(TEMPLATE_POOLS / f"{pool_name}.json")
        locations = set()
        for member in pool.get("elements", []):
            element = member.get("element", {})
            if isinstance(element, dict) and element.get("location"):
                locations.add(element["location"])
        for asset in assets:
            if not isinstance(asset, str) or not asset.startswith("infinite_domain:abyssal/"):
                fail(f"{fid} has invalid materialized asset ID {asset!r}")
            asset_name = asset.rsplit("/", 1)[-1]
            nbt_path = NBT / f"{asset_name}.nbt"
            if not nbt_path.is_file():
                fail(f"{fid} missing materialized variant NBT {nbt_path.relative_to(ROOT)}")
            if asset not in locations:
                fail(f"{fid} materialized variant {asset} is absent from template pool {pool_id}")
    else:
        nbt_path = NBT / f"{name}.nbt"
        if not nbt_path.is_file():
            fail(f"{fid} missing materialized NBT {nbt_path.relative_to(ROOT)}")

    if structure.get("project_start_to_heightmap") != feature["projection"]:
        fail(f"{fid} projection disagrees with live structure JSON")
    if structure.get("terrain_adaptation") != feature["terrain_adaptation"]:
        fail(f"{fid} terrain adaptation disagrees with live structure JSON")
    selectors = feature["target_selectors"]
    if structure.get("biomes") not in selectors:
        fail(f"{fid} catalog selectors omit live biome selector {structure.get('biomes')}")
    placement = structure_set.get("placement", {})
    expected = feature["placement"]
    for catalog_key, live_key in (("spacing_chunks", "spacing"), ("separation_chunks", "separation"), ("salt", "salt")):
        if expected.get(catalog_key) != placement.get(live_key):
            fail(f"{fid} {catalog_key} disagrees with live structure set")
    members = structure_set.get("structures", [])
    if not any(member.get("structure") == registry for member in members):
        fail(f"{fid} structure set no longer references {registry}")
    require_source(feature)


def validate_parent_component(feature: dict, known_registries: set[str]) -> None:
    fid = feature["planning_id"]
    parent = feature.get("parent_registry_id")
    component = feature.get("component_asset")
    if not parent or parent not in known_registries:
        fail(f"{fid} parent_registry_id is missing or does not reference an earlier live catalog structure")
    if not component or not component.startswith("infinite_domain:abyssal/"):
        fail(f"{fid} component_asset must be a stable abyssal asset ID")
    component_name = component.rsplit("/", 1)[-1]
    parent_name = parent.rsplit("/", 1)[-1]
    nbt_path = NBT / f"{component_name}.nbt"
    if not nbt_path.is_file():
        fail(f"{fid} missing materialized component NBT {nbt_path.relative_to(ROOT)}")
    pool = load(TEMPLATE_POOLS / f"{parent_name}.json")
    locations = []
    for member in pool.get("elements", []):
        element = member.get("element", {})
        if isinstance(element, dict):
            locations.append(element.get("location"))
    if component not in locations:
        fail(f"{fid} component asset {component} is not present in parent template pool {parent_name}")
    if parent not in serialized(load(STRUCTURE_SETS / f"{parent_name}.json")):
        fail(f"{fid} parent structure is no longer live in its structure set")
    require_source(feature)


def validate_systemic_feature(feature: dict) -> None:
    fid = feature["planning_id"]
    require_source(feature)
    refs = feature.get("systemic_references")
    if not isinstance(refs, dict) or not refs:
        fail(f"{fid} implemented-systemic feature lacks systemic_references")
    for rel, tokens in refs.items():
        if not isinstance(tokens, list) or not tokens:
            fail(f"{fid} systemic reference {rel} has no required tokens")
        text = serialized(load(ROOT / rel))
        missing = [token for token in tokens if token not in text]
        if missing:
            fail(f"{fid} systemic reference {rel} lost: {', '.join(missing)}")


catalog = load(CATALOG)
if catalog.get("catalog_version") != 2:
    fail("catalog_version must be 2")
if catalog.get("process_order") != EXPECTED_ORDER:
    fail("process_order no longer matches the approved review/tranche sequence")
contract = catalog.get("feature_contract", {})
for flag in (
    "neutral_features_must_not_mix_faction_pools",
    "no_progression_breaking_loot",
    "preserve_existing_registry_ids_when_refining",
    "submarine_clearance_is_required_runtime_evidence",
):
    if contract.get(flag) is not True:
        fail(f"feature contract lost required flag {flag}")

features = catalog.get("features")
if not isinstance(features, list) or not features:
    fail("features must be a non-empty list")
ids = [f.get("planning_id") for f in features]
if ids != EXPECTED_ORDER:
    fail("feature records must exist exactly once and in process_order")
if len(set(ids)) != len(ids):
    fail("duplicate planning IDs")

registry_ids: list[str] = []
for feature in features:
    fid = feature.get("planning_id", "<missing>")
    missing = sorted(REQUIRED.difference(feature))
    if missing:
        fail(f"{fid} missing fields: {', '.join(missing)}")
    if feature["faction"] != "neutral":
        fail(f"{fid} entered the neutral AGE-018 queue with faction={feature['faction']}")
    if not feature["target_selectors"] or not feature["depth_zones"]:
        fail(f"{fid} lacks biome/depth ownership")
    validate_footprint(fid, feature["footprint"])
    if len(feature["palette"]) < 3:
        fail(f"{fid} palette is too underspecified")
    if len(feature["geometry_contract"]) < 3:
        fail(f"{fid} geometry contract is too underspecified")
    runtime = feature["runtime_validation"]
    if runtime.get("status") != "deferred":
        fail(f"{fid} improperly claims runtime validation")
    checks = set(runtime.get("checks", []))
    for required_check in ("submarine clearance", "chunk-generation cost"):
        if required_check not in checks:
            fail(f"{fid} runtime ledger omits {required_check}")
    registry = feature["registry_id"]
    if registry:
        if registry in registry_ids:
            fail(f"duplicate registry ID {registry}")
        registry_ids.append(registry)
        validate_live_structure(feature)
    elif feature["state"] == "implemented-component":
        validate_parent_component(feature, set(registry_ids))
    elif feature["state"] == "implemented-systemic":
        validate_systemic_feature(feature)
    elif feature["state"] not in {"specified", "planned"}:
        fail(f"{fid} has no registry ID but state={feature['state']}")
    if "ore" in feature["loot_policy"] and feature["loot_policy"] != "no-progression-material":
        fail(f"{fid} loot policy risks progression bypass")

print(
    f"[ABYSSAL FEATURE CATALOG PASS] {len(features)} queued features have structural metadata, "
    "neutral ownership, geometry contracts, runtime deferrals, and validated live, "
    "variant-family, component, or systemic implementation links where implemented"
)
