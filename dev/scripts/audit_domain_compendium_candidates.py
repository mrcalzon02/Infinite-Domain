"""Deterministic candidate inventory for the Domain Compendium collection chapter.

For every registered item and block this classifies:

* obtainable_via  - recipe output / loot / worldgen target in the acquisition graph
* textured        - the item or block model resolves to textures that actually exist
                    in the loaded asset set (mod jars + kubejs/assets + the Last Days
                    resource pack that options.txt has enabled)
* auto_variant    - allthecompressed / exdeorum / rechiseled* bulk-generated family

It emits:

* docs/domain-compendium/candidate-inventory.csv   - one row per registered id
* docs/domain-compendium/candidate-summary.txt     - namespace + decision rollups
* docs/domain-compendium/allthecompressed-families.csv - the 199 ATC families,
      base texture, whether it resolves, and the resulting tier count

Nothing here writes quest files. It is the data layer the chapter generator and
its validator consume.  Run:  python scripts/audit_domain_compendium_candidates.py
"""

from __future__ import annotations

import csv
import json
import re
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/registry-inventory"
GRAPH_EDGES = ROOT / "docs/progression-graph/graph-edges.csv"
KUBEJS_ASSETS = ROOT / "kubejs/assets"
MODS = ROOT / "mods"
RESOURCEPACKS = ROOT / "resourcepacks"
OUT_DIR = ROOT / "docs/domain-compendium"
# The vanilla client jar is not under mods/; it supplies minecraft: models and
# textures that mod models inherit from. Path mirrors audit_authored_asset_references.py.
VANILLA_JAR = ROOT.parents[1] / "Install/versions/1.21.1/1.21.1.jar"

# Resource packs options.txt has enabled, highest priority last. "vanilla",
# "fabric", "mod_resources" and "moonlight:merged_pack" are the jars themselves
# or a runtime-generated pack; the only extra on-disk pack is the Last Days zip.
ENABLED_DISK_PACKS = ["LAST_DAYS_INFINITE_DOMAIN_1.21.1.zip"]

OBTAINMENT_EDGE_KINDS = {"recipe_output", "loot", "worldgen_block"}
AUTO_VARIANT_NAMESPACES = {"allthecompressed", "exdeorum", "rechiseled", "rechiseledcreate"}
MAX_PARENT_DEPTH = 12


def read_ids(name: str) -> list[str]:
    path = REGISTRY / name
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8-sig").splitlines()
        if line.strip() and ":" in line
    ]


def load_obtainable() -> dict[str, set[str]]:
    """id -> set of obtainment kinds (recipe / loot / worldgen)."""
    kinds: dict[str, set[str]] = {}
    with GRAPH_EDGES.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["edge_kind"] not in OBTAINMENT_EDGE_KINDS:
                continue
            target = row["to"].strip()
            if ":" not in target or target.startswith(("#", "recipe:", "loot:")):
                continue
            bucket = kinds.setdefault(target, set())
            bucket.add(row["edge_kind"].replace("recipe_output", "recipe").replace("worldgen_block", "worldgen"))
    return kinds


class AssetIndex:
    """Lazily reads model json and records which texture paths exist."""

    def __init__(self) -> None:
        self.texture_paths: set[str] = set()
        self.model_entry: dict[str, tuple[str, str]] = {}
        self._zip_cache: dict[str, zipfile.ZipFile] = {}
        self._model_cache: dict[str, dict | None] = {}
        self._loose_root: Path | None = None

    # ---- index construction -------------------------------------------------
    def add_zip(self, path: Path) -> None:
        try:
            archive = zipfile.ZipFile(path)
        except (OSError, zipfile.BadZipFile):
            return
        key = str(path)
        self._zip_cache[key] = archive
        for name in archive.namelist():
            if not name.startswith("assets/") or name.endswith("/"):
                continue
            if name.endswith(".png") and "/textures/" in name:
                self.texture_paths.add(name)
            elif name.endswith(".json") and "/models/" in name:
                self.model_entry.setdefault(name, (key, name))

    def add_loose(self, assets_root: Path) -> None:
        if not assets_root.is_dir():
            return
        self._loose_root = assets_root.parent
        for path in assets_root.rglob("*"):
            if not path.is_file():
                continue
            rel = f"assets/{path.relative_to(assets_root).as_posix()}"
            if path.suffix == ".png" and "/textures/" in rel:
                self.texture_paths.add(rel)
            elif path.suffix == ".json" and "/models/" in rel:
                self.model_entry[rel] = ("<loose>", rel)  # loose overrides jars

    # ---- lookups ----------------------------------------------------------
    def read_model(self, asset_path: str) -> dict | None:
        if asset_path in self._model_cache:
            return self._model_cache[asset_path]
        entry = self.model_entry.get(asset_path)
        result: dict | None = None
        if entry:
            source, name = entry
            try:
                if source == "<loose>" and self._loose_root is not None:
                    raw = (self._loose_root / asset_path).read_bytes()
                else:
                    raw = self._zip_cache[source].read(name)
                result = json.loads(raw.decode("utf-8-sig"))
            except (OSError, KeyError, ValueError):
                result = None
        self._model_cache[asset_path] = result
        return result

    def texture_exists(self, ref: str) -> bool:
        namespace, path = ref.split(":", 1) if ":" in ref else ("minecraft", ref)
        return f"assets/{namespace}/textures/{path}.png" in self.texture_paths


def model_asset_path(kind: str, ref: str) -> str:
    namespace, path = ref.split(":", 1) if ":" in ref else ("minecraft", ref)
    return f"assets/{namespace}/models/{path}.json"


def _deref(var: str, merged: dict[str, str]) -> str | None:
    """Follow a chain of #refs through the merged texture map to a terminal value."""
    seen: set[str] = set()
    value = var
    while isinstance(value, str) and value.startswith("#"):
        key = value[1:]
        if key in seen or key not in merged:
            return None
        seen.add(key)
        value = merged[key]
    return value if isinstance(value, str) else None


def _used_texture_vars(model: dict) -> set[str]:
    """The #vars a model's own elements / layers actually paint with."""
    used: set[str] = set()
    for element in model.get("elements") or []:
        for face in (element.get("faces") or {}).values():
            texture = face.get("texture") if isinstance(face, dict) else None
            if isinstance(texture, str):
                used.add(texture)
    for key in (model.get("textures") or {}):
        if re.fullmatch(r"layer\d+", key):
            used.add(f"#{key}")
    return used


def resolve_textures(index: AssetIndex, start_ref: str) -> tuple[str, list[str]]:
    """Walk a model's parent chain; return (status, missing_texture_refs).

    Only the textures the model chain actually *paints with* (element faces,
    generated layers, particle) must resolve - texture slots that are declared
    but unused (common in AE2 parts and Blockbench exports) are ignored.

    status: 'ok'         - every painted texture resolves to a png
            'missing'    - a painted texture ref does not resolve
            'no_texture' - the chain paints with nothing inspectable
            'no_model'   - the starting model file is absent
    """
    asset_path = model_asset_path("models", start_ref)
    if asset_path not in index.model_entry:
        return "no_model", []

    merged: dict[str, str] = {}
    used_vars: set[str] = set()
    seen: set[str] = set()
    ref = start_ref
    generated = False
    for _ in range(MAX_PARENT_DEPTH):
        asset_path = model_asset_path("models", ref)
        if asset_path in seen:
            break
        seen.add(asset_path)
        model = index.read_model(asset_path)
        if model is None:
            break
        for key, value in (model.get("textures") or {}).items():
            merged.setdefault(key, value)
        used_vars |= _used_texture_vars(model)
        parent = model.get("parent")
        if not isinstance(parent, str):
            break
        short = parent.split(":")[-1]
        if parent.startswith("builtin/") or short in {"generated", "handheld"}:
            generated = True
            break
        ref = parent

    if generated:
        used_vars |= {f"#{key}" for key in merged if re.fullmatch(r"layer\d+", key)}
    if "particle" in merged:
        used_vars.add("#particle")

    if not used_vars:
        # no elements captured anywhere (blockstate-only template, odd export):
        # fall back to requiring every concrete declared texture.
        concrete = [v for v in merged.values() if isinstance(v, str) and not v.startswith("#")]
        if not concrete:
            return "no_texture", []
        missing = sorted({v for v in concrete if not _sentinel(v) and not index.texture_exists(v)})
        return ("missing", missing) if missing else ("ok", [])

    painted: list[str] = []
    missing: list[str] = []
    for var in used_vars:
        terminal = _deref(var, merged)
        if terminal is None or _sentinel(terminal):
            continue
        painted.append(terminal)
        if not index.texture_exists(terminal):
            missing.append(terminal)

    if not painted:
        return "no_texture", []
    if missing:
        return "missing", sorted(set(missing))
    return "ok", []


def _sentinel(value: str) -> bool:
    """AE2 and some mods use _bright_ / _dark_ style placeholders for 'no texture'."""
    return len(value) > 1 and value.startswith("_") and value.endswith("_") and ":" not in value


def textured_status(index: AssetIndex, identifier: str, is_block: bool) -> tuple[str, str]:
    """Return (verdict, detail). verdict in {yes, no, unknown}."""
    namespace, name = identifier.split(":", 1)
    candidates = [f"{namespace}:item/{name}"]
    if is_block:
        candidates.append(f"{namespace}:block/{name}")

    best = ("no_model", [])
    for cand in candidates:
        status, missing = resolve_textures(index, cand)
        if status == "ok":
            return "yes", cand
        # keep the most informative failure
        order = {"missing": 3, "no_texture": 2, "no_model": 1}
        if order.get(status, 0) > order.get(best[0], 0):
            best = (status, missing)

    if best[0] == "missing":
        return "no", f"missing:{','.join(best[1][:3])}"
    if best[0] == "no_texture":
        return "unknown", "model has no static texture (blockstate/runtime only)"
    return "unknown", "no model file found (runtime-generated or blockstate only)"


def allthecompressed_family_report(index: AssetIndex) -> list[dict]:
    jar = next(MODS.glob("allthecompressed-*.jar"), None)
    if jar is None:
        return []
    archive = zipfile.ZipFile(jar)
    families: dict[str, str] = {}
    for name in archive.namelist():
        match = re.search(r"/models/block/(.+?)_1x\.json$", name)
        if not match:
            continue
        model = json.loads(archive.read(name).decode("utf-8-sig"))
        base = (model.get("textures") or {}).get("all", "")
        families[match.group(1)] = base
    rows = []
    for family, base in sorted(families.items()):
        status, missing = resolve_textures(index, f"allthecompressed:block/{family}_1x")
        resolves = status == "ok"
        rows.append({
            "family": family,
            "base_texture": base,
            "resolve_status": status,
            "base_resolves": resolves,
            "missing_ref": ",".join(missing[:2]),
            "tiers_if_included": 9 if resolves else 0,
        })
    return rows


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    items = set(read_ids("item-ids.txt"))
    blocks = set(read_ids("block-ids.txt"))
    all_ids = sorted(items | blocks)

    obtainable = load_obtainable()

    index = AssetIndex()
    index.add_loose(KUBEJS_ASSETS)
    for pack in ENABLED_DISK_PACKS:
        index.add_zip(RESOURCEPACKS / pack)
    for jar in sorted(MODS.glob("*.jar")):
        index.add_zip(jar)
    if VANILLA_JAR.is_file():
        index.add_zip(VANILLA_JAR)
    else:
        print(f"WARNING: vanilla jar not found at {VANILLA_JAR}; minecraft: assets unverified", file=sys.stderr)
    print(f"indexed {len(index.texture_paths):,} textures and {len(index.model_entry):,} model files", file=sys.stderr)

    rows = []
    for identifier in all_ids:
        namespace = identifier.split(":", 1)[0]
        is_block = identifier in blocks
        is_item = identifier in items
        kinds = sorted(obtainable.get(identifier, set()))
        verdict, detail = textured_status(index, identifier, is_block)

        obtain_ok = bool(kinds)
        if verdict == "yes" and obtain_ok:
            decision, reason = "include", "textured + obtainable"
        elif verdict == "yes" and not obtain_ok:
            decision, reason = "review", "textured but no static obtainment route"
        elif verdict == "no":
            decision, reason = "exclude", f"missing texture ({detail})"
        elif not obtain_ok:
            decision, reason = "exclude", "no obtainment route and texture unverified"
        else:
            decision, reason = "review", f"texture unverified ({detail})"

        rows.append({
            "id": identifier,
            "namespace": namespace,
            "is_item": is_item,
            "is_block": is_block,
            "obtainable_via": "|".join(kinds) or "none",
            "textured": verdict,
            "texture_detail": detail,
            "auto_variant": namespace in AUTO_VARIANT_NAMESPACES,
            "decision": decision,
            "reason": reason,
        })

    inventory = OUT_DIR / "candidate-inventory.csv"
    with inventory.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    atc_rows = allthecompressed_family_report(index)
    if atc_rows:
        atc_csv = OUT_DIR / "allthecompressed-families.csv"
        with atc_csv.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(atc_rows[0].keys()))
            writer.writeheader()
            writer.writerows(atc_rows)

    # ---- rollups --------------------------------------------------------
    from collections import Counter

    by_ns: dict[str, Counter] = {}
    decision_total = Counter()
    for row in rows:
        decision_total[row["decision"]] += 1
        bucket = by_ns.setdefault(row["namespace"], Counter())
        bucket[row["decision"]] += 1
        bucket["total"] += 1

    lines = []
    lines.append("DOMAIN COMPENDIUM CANDIDATE INVENTORY")
    lines.append(f"registered ids: {len(all_ids):,}  (items {len(items):,}, blocks {len(blocks):,})")
    lines.append(f"with an obtainment route (recipe/loot/worldgen): {sum(1 for r in rows if r['obtainable_via'] != 'none'):,}")
    lines.append(f"textured=yes: {sum(1 for r in rows if r['textured'] == 'yes'):,}   "
                 f"no: {sum(1 for r in rows if r['textured'] == 'no'):,}   "
                 f"unknown: {sum(1 for r in rows if r['textured'] == 'unknown'):,}")
    lines.append("")
    lines.append("decision totals:")
    for decision, count in decision_total.most_common():
        lines.append(f"  {decision:9s} {count:6,}")
    lines.append("")
    lines.append("reason breakdown:")
    reason_total = Counter(row["reason"] for row in rows)
    for reason, count in reason_total.most_common():
        lines.append(f"  {count:6,}  {reason}")
    if atc_rows:
        included = sum(1 for r in atc_rows if r["base_resolves"])
        lines.append("")
        lines.append(f"AllTheCompressed families: {len(atc_rows)}  base texture resolves: {included}  "
                     f"-> {included * 9} tier blocks in, {(len(atc_rows) - included) * 9} out")
    lines.append("")
    lines.append(f"{'namespace':26s}{'total':>8s}{'include':>9s}{'review':>8s}{'exclude':>9s}")
    for namespace, bucket in sorted(by_ns.items(), key=lambda kv: -kv[1]["total"]):
        lines.append(f"{namespace:26s}{bucket['total']:8,}{bucket['include']:9,}{bucket['review']:8,}{bucket['exclude']:9,}")

    summary = OUT_DIR / "candidate-summary.txt"
    summary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"\nwrote {inventory.relative_to(ROOT)}")
    if atc_rows:
        print(f"wrote {(OUT_DIR / 'allthecompressed-families.csv').relative_to(ROOT)}")
    print(f"wrote {summary.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
