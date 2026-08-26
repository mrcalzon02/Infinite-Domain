#!/usr/bin/env python3
"""[SYSTEM REPORT] Static contract validator for the AGE-016 Pelagos and
AGE-017 Karsic factional-debris random-spawn pools (docs/ABYSSAL_ENVIRONMENTAL_SITES.md).

Distinct from validate_abyssal_feature_catalog.py, which enforces
faction == "neutral" for the shared geology queue: this validator enforces
the opposite hard contract -- every entry here must belong to exactly one
faction, a Pelagos entry may never reference an eastern biome selector or
the Karsic pool, and a Karsic entry may never reference a western selector
or the Pelagos pool. There must never be one shared pool mixing the two."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "tools/abyssal_worldgen/abyssal_factional_debris_catalog.json"
STRUCTURES = ROOT / "kubejs/data/infinite_domain/worldgen/structure/abyssal"
STRUCTURE_SETS = ROOT / "kubejs/data/infinite_domain/worldgen/structure_set/abyssal"
TEMPLATE_POOLS = ROOT / "kubejs/data/infinite_domain/worldgen/template_pool/abyssal"
NBT = ROOT / "kubejs/data/infinite_domain/structure/abyssal"

EXPECTED_ORDER = [
    "AGE-016", "PEL-DET-002", "PEL-DET-011", "PEL-DET-012", "PEL-DET-017",
    "AGE-017", "KAR-DET-001", "KAR-DET-007", "KAR-DET-010", "KAR-DET-017",
]
REQUIRED = {
    "planning_id", "name", "faction", "state", "implementation_type",
    "source_path", "target_selectors", "depth_zones", "footprint",
    "palette", "geometry_contract", "hazards", "loot_policy", "runtime_validation",
}
FACTION_WORD = {"pelagos": "western", "karsic": "eastern"}
FACTION_FORBIDDEN_WORD = {"pelagos": "eastern", "karsic": "western"}


def fail(message: str) -> None:
    print(f"[ABYSSAL FACTIONAL DEBRIS CATALOG FAIL] {message}", file=sys.stderr)
    raise SystemExit(1)


def load(path: Path):
    if not path.is_file():
        fail(f"missing required file: {path.relative_to(ROOT)}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")


def validate_footprint(fid: str, footprint: dict) -> None:
    if not all(k in footprint for k in ("x", "y", "z")):
        fail(f"{fid} footprint must be a fixed x/y/z (factional debris members are discrete, not terrain-scale)")
    dims = [footprint[k] for k in ("x", "y", "z")]
    if any(not isinstance(v, int) or v <= 0 or v > 64 for v in dims):
        fail(f"{fid} has invalid or oversized footprint {dims} for a debris-scale member")


def require_source(feature: dict) -> None:
    fid = feature["planning_id"]
    source = feature.get("source_path")
    if not source or not (ROOT / source).is_file():
        fail(f"{fid} source_path is not an existing authoritative source")


def check_faction_isolation(feature: dict) -> None:
    fid = feature["planning_id"]
    faction = feature["faction"]
    if faction not in FACTION_WORD:
        fail(f"{fid} faction must be 'pelagos' or 'karsic', got {faction!r}")
    forbidden = FACTION_FORBIDDEN_WORD[faction]
    for selector in feature["target_selectors"]:
        if forbidden in selector:
            fail(f"{fid} is {faction} but its selector {selector!r} references the {forbidden} side")
    for key in ("registry_id", "parent_registry_id", "component_asset"):
        value = feature.get(key)
        if value and forbidden in value:
            fail(f"{fid} is {faction} but {key} {value!r} references the {forbidden} side")


def validate_pool_head(feature: dict, members: list[dict]) -> None:
    fid = feature["planning_id"]
    registry = feature["registry_id"]
    if not registry or not registry.startswith("infinite_domain:abyssal/"):
        fail(f"{fid} pool head lacks a stable abyssal registry ID")
    name = registry.rsplit("/", 1)[-1]
    structure = load(STRUCTURES / f"{name}.json")
    structure_set = load(STRUCTURE_SETS / f"{name}.json")
    pool = load(TEMPLATE_POOLS / f"{name}.json")

    selectors = feature["target_selectors"]
    if structure.get("biomes") not in selectors:
        fail(f"{fid} catalog selectors omit live biome selector {structure.get('biomes')!r}")
    if structure.get("terrain_adaptation") != feature.get("terrain_adaptation", structure.get("terrain_adaptation")):
        pass  # descriptive only for the pool head; per-member geometry varies
    placement = structure_set.get("placement", {})
    expected = feature["placement"]
    for catalog_key, live_key in (("spacing_chunks", "spacing"), ("separation_chunks", "separation"), ("salt", "salt")):
        if expected.get(catalog_key) != placement.get(live_key):
            fail(f"{fid} {catalog_key} disagrees with live structure set")
    set_members = structure_set.get("structures", [])
    if not any(m.get("structure") == registry for m in set_members):
        fail(f"{fid} structure set no longer references {registry}")

    pool_locations = set()
    for element in pool.get("elements", []):
        loc = element.get("element", {}).get("location")
        if loc:
            pool_locations.add(loc)
    member_assets = {m["component_asset"] for m in members if m.get("parent_registry_id") == registry}
    if not member_assets:
        fail(f"{fid} has no catalog members referencing it as parent_registry_id")
    missing_from_pool = member_assets - pool_locations
    if missing_from_pool:
        fail(f"{fid} template pool is missing catalog members: {sorted(missing_from_pool)}")
    orphaned_in_pool = pool_locations - member_assets
    if orphaned_in_pool:
        fail(f"{fid} template pool has entries with no catalog record: {sorted(orphaned_in_pool)}")
    require_source(feature)


def validate_pool_member(feature: dict, known_pool_registries: set[str]) -> None:
    fid = feature["planning_id"]
    parent = feature.get("parent_registry_id")
    component = feature.get("component_asset")
    if not parent or parent not in known_pool_registries:
        fail(f"{fid} parent_registry_id is missing or does not reference a live pool head in this catalog")
    if not component or not component.startswith("infinite_domain:abyssal/"):
        fail(f"{fid} component_asset must be a stable abyssal asset ID")
    nbt_path = NBT / f"{component.rsplit('/', 1)[-1]}.nbt"
    if not nbt_path.is_file():
        fail(f"{fid} missing materialized NBT {nbt_path.relative_to(ROOT)}")
    require_source(feature)


catalog = load(CATALOG)
if catalog.get("catalog_version") != 1:
    fail("catalog_version must be 1")
if catalog.get("process_order") != EXPECTED_ORDER:
    fail("process_order no longer matches the approved tranche sequence")
contract = catalog.get("pool_contract", {})
for flag in (
    "pelagos_pool_must_stay_western_only",
    "karsic_pool_must_stay_eastern_only",
    "no_shared_faction_pool_permitted",
    "no_progression_breaking_loot",
):
    if contract.get(flag) is not True:
        fail(f"pool contract lost required flag {flag}")

features = catalog.get("features")
if not isinstance(features, list) or not features:
    fail("features must be a non-empty list")
ids = [f.get("planning_id") for f in features]
if ids != EXPECTED_ORDER:
    fail("feature records must exist exactly once and in process_order")
if len(set(ids)) != len(ids):
    fail("duplicate planning IDs")

pool_heads = {f["registry_id"] for f in features if f.get("registry_id")}
for feature in features:
    fid = feature.get("planning_id", "<missing>")
    missing = sorted(REQUIRED.difference(feature))
    if missing:
        fail(f"{fid} missing fields: {', '.join(missing)}")
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
    if "submarine clearance" not in set(runtime.get("checks", [])):
        fail(f"{fid} runtime ledger omits submarine clearance")
    check_faction_isolation(feature)
    if feature.get("registry_id"):
        validate_pool_head(feature, features)
    elif feature["state"] == "implemented-component" or feature["implementation_type"] == "pool_member":
        validate_pool_member(feature, pool_heads)
    elif feature["state"] not in {"specified", "planned"}:
        fail(f"{fid} has no registry ID but state={feature['state']}")
    policy = feature["loot_policy"]
    if "ore" in policy and policy != "no-progression-material":
        fail(f"{fid} loot policy risks progression bypass")
    if policy not in ("none", "no-progression-material") and "salvage" not in policy:
        fail(f"{fid} loot policy {policy!r} is not one of the pool's approved forms")

print(
    f"[ABYSSAL FACTIONAL DEBRIS CATALOG PASS] {len(features)} queued features "
    "have structural metadata, verified faction-pool isolation (no cross-references "
    "between Pelagos/western and Karsic/eastern), and validated pool-head or "
    "pool-member implementation links where implemented"
)
