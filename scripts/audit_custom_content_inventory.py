"""Inventory and baseline validation for every Infinite Domain authored content file."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import zipfile
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/custom-content-audit"
RESOURCE_PATH = re.compile(r"^[a-z0-9_.-]+(?:/[a-z0-9_.-]+)*$")
CUSTOM_JAR_PREFIX = "infinite-domain-"


class DuplicateKeyError(ValueError):
    pass


def unique_object(pairs: list[tuple[str, object]]) -> dict:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inventory_tree(root: Path, area: str) -> tuple[list[dict], list[dict]]:
    rows: list[dict] = []
    findings: list[dict] = []
    if not root.exists():
        return rows, findings
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        relative = path.relative_to(root).as_posix()
        parts = relative.split("/")
        namespace = parts[0] if parts else ""
        content_type = parts[1] if len(parts) > 2 else "(root)"
        suffix = path.suffix.lower()
        rows.append(
            {
                "area": area,
                "namespace": namespace,
                "content_type": content_type,
                "path": path.relative_to(ROOT).as_posix(),
                "extension": suffix,
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
        if not RESOURCE_PATH.fullmatch(relative):
            findings.append(
                {
                    "severity": "ERROR",
                    "code": "INVALID_RESOURCE_PATH",
                    "path": path.relative_to(ROOT).as_posix(),
                    "detail": "Resource-pack paths must be lowercase and contain only valid resource characters.",
                }
            )
        if suffix == ".json":
            try:
                parsed = json.loads(path.read_text(encoding="utf-8-sig"), object_pairs_hook=unique_object)
            except (UnicodeError, json.JSONDecodeError, DuplicateKeyError) as exc:
                findings.append(
                    {
                        "severity": "ERROR",
                        "code": "INVALID_JSON",
                        "path": path.relative_to(ROOT).as_posix(),
                        "detail": str(exc),
                    }
                )
                continue
            if area == "data" and content_type == "recipe" and isinstance(parsed, dict):
                recipe_type = parsed.get("type")
                if recipe_type in {"minecraft:crafting_shaped", "minecraft:crafting_shapeless"}:
                    category = parsed.get("category")
                    valid_categories = {None, "building", "redstone", "equipment", "misc"}
                    if category not in valid_categories:
                        findings.append(
                            {
                                "severity": "ERROR",
                                "code": "INVALID_CRAFTING_CATEGORY",
                                "path": path.relative_to(ROOT).as_posix(),
                                "detail": f"{category!r} is not a Minecraft 1.21 crafting-book category.",
                            }
                        )
                    result = parsed.get("result")
                    if isinstance(result, dict) and "item" in result and "id" not in result:
                        findings.append(
                            {
                                "severity": "ERROR",
                                "code": "LEGACY_CRAFTING_RESULT",
                                "path": path.relative_to(ROOT).as_posix(),
                                "detail": "Minecraft 1.21 crafting results use the 'id' field, not 'item'.",
                            }
                        )
    return rows, findings


def script_inventory() -> list[dict]:
    rows: list[dict] = []
    for area in ("kubejs/startup_scripts", "kubejs/server_scripts", "kubejs/client_scripts", "scripts"):
        root = ROOT / area
        for path in sorted(p for p in root.rglob("*") if p.is_file()):
            rows.append(
                {
                    "area": area,
                    "path": path.relative_to(ROOT).as_posix(),
                    "extension": path.suffix.lower(),
                    "bytes": path.stat().st_size,
                    "sha256": sha256(path),
                }
            )
    return rows


def jar_inventory() -> tuple[list[dict], list[dict]]:
    rows: list[dict] = []
    findings: list[dict] = []
    for path in sorted((ROOT / "mods").glob(f"{CUSTOM_JAR_PREFIX}*.jar")):
        with zipfile.ZipFile(path) as jar:
            names = jar.namelist()
            manifest_name = "META-INF/neoforge.mods.toml"
            if manifest_name not in names:
                findings.append(
                    {
                        "severity": "ERROR",
                        "code": "MISSING_MOD_MANIFEST",
                        "path": path.relative_to(ROOT).as_posix(),
                        "detail": manifest_name,
                    }
                )
                manifest = ""
            else:
                manifest = jar.read(manifest_name).decode("utf-8")
            primary_section = manifest.split("[[dependencies.", 1)[0]
            mod_ids = re.findall(r'^modId\s*=\s*"([a-z0-9_.-]+)"', primary_section, re.MULTILINE)
            versions = re.findall(r'^version\s*=\s*"([^"]+)"', primary_section, re.MULTILINE)
            rows.append(
                {
                    "path": path.relative_to(ROOT).as_posix(),
                    "bytes": path.stat().st_size,
                    "sha256": sha256(path),
                    "entries": len(names),
                    "classes": sum(name.endswith(".class") for name in names),
                    "json": sum(name.endswith(".json") for name in names),
                    "png": sum(name.endswith(".png") for name in names),
                    "mod_ids": ";".join(mod_ids),
                    "versions": ";".join(versions),
                }
            )
            invalid_entries = [
                name
                for name in names
                if not name.endswith("/")
                and name.startswith(("assets/", "data/"))
                and not RESOURCE_PATH.fullmatch(name)
            ]
            for name in invalid_entries:
                findings.append(
                    {
                        "severity": "ERROR",
                        "code": "INVALID_JAR_RESOURCE_PATH",
                        "path": f"{path.relative_to(ROOT).as_posix()}!/{name}",
                        "detail": "Invalid packaged resource path.",
                    }
                )
    return rows, findings


def write_csv(path: Path, rows: list[dict], fieldnames: list[str] | None = None) -> None:
    columns = fieldnames or (list(rows[0]) if rows else [])
    with path.open("w", encoding="utf-8", newline="") as handle:
        if not columns:
            return
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    data_rows, data_findings = inventory_tree(ROOT / "kubejs/data", "data")
    asset_rows, asset_findings = inventory_tree(ROOT / "kubejs/assets", "assets")
    scripts = script_inventory()
    jars, jar_findings = jar_inventory()
    findings = data_findings + asset_findings + jar_findings

    write_csv(OUT / "resource-inventory.csv", data_rows + asset_rows)
    write_csv(OUT / "script-inventory.csv", scripts)
    write_csv(OUT / "companion-mod-inventory.csv", jars)
    write_csv(
        OUT / "baseline-findings.csv",
        findings,
        ["severity", "code", "path", "detail"],
    )

    namespace_counts = Counter(row["namespace"] for row in data_rows)
    data_type_counts: dict[str, Counter] = defaultdict(Counter)
    for row in data_rows:
        data_type_counts[row["namespace"]][row["content_type"]] += 1

    lines = [
        "# Infinite Domain Custom Content Inventory",
        "",
        "This report is generated by `scripts/audit_custom_content_inventory.py`.",
        "It inventories authored overlays as well as native Infinite Domain namespaces.",
        "",
        "## Scope totals",
        "",
        f"- Datapack files: {len(data_rows)}",
        f"- Asset files: {len(asset_rows)}",
        f"- Active KubeJS and maintenance scripts: {len(scripts)}",
        f"- Installed Infinite Domain companion mods: {len(jars)}",
        f"- Baseline path/JSON/manifest findings: {len(findings)}",
        "",
        "## Datapack namespaces",
        "",
        "| Namespace | Files | Principal content types |",
        "|---|---:|---|",
    ]
    for namespace, count in sorted(namespace_counts.items()):
        types = ", ".join(f"{name} ({amount})" for name, amount in data_type_counts[namespace].most_common(5))
        lines.append(f"| `{namespace}` | {count} | {types} |")
    lines.extend(["", "## Companion mods", "", "| Archive | Mod ID | Entries | Classes | JSON | PNG |", "|---|---|---:|---:|---:|---:|"])
    for row in jars:
        lines.append(f"| `{Path(row['path']).name}` | `{row['mod_ids']}` | {row['entries']} | {row['classes']} | {row['json']} | {row['png']} |")
    lines.extend(["", "## Baseline findings", ""])
    if findings:
        for finding in findings:
            lines.append(f"- **{finding['severity']} {finding['code']}** — `{finding['path']}`: {finding['detail']}")
    else:
        lines.append("No invalid JSON, duplicate JSON keys, invalid resource paths, or missing companion manifests were found.")
    (OUT / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(
        f"Inventory complete: {len(data_rows)} data files, {len(asset_rows)} assets, "
        f"{len(scripts)} scripts, {len(jars)} companion mods, {len(findings)} baseline findings."
    )
    for finding in findings:
        print(f"{finding['severity']} {finding['code']}: {finding['path']} — {finding['detail']}")
    return 1 if any(finding["severity"] == "ERROR" for finding in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
