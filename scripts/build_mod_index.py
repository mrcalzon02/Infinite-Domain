"""Rebuild docs/MOD_LIST.md, docs/registry-inventory/mod-jar-index.json, and
docs/registry-inventory/entity-ids.txt from the jars actually present in mods/.

Run this whenever mods are added, removed, or updated, so the project index
stays accurate instead of going stale. Does not require a running instance —
reads modid/name/entity data directly out of each jar plus minecraftinstance.json.
"""
import json
import re
import tomllib
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODS = ROOT / "mods"
REGISTRY_DIR = ROOT / "docs" / "registry-inventory"

# Project-built jars -> their tracked source directory under packdev/.
PROJECT_SOURCES = {
    "infinite-domain-create-nuclear-balance-1.0.0.jar": "packdev/create-nuclear-balance",
    "infinite-domain-cyberware-mastery-1.0.0.jar": "packdev/cyberware-mastery-expansion",
    "infinite-domain-darknet-worldgen-1.8.0.jar": "packdev/darknet-worldgen-patch",
    "infinite-domain-echo-economy-1.0.0.jar": "packdev/echo-numismatics-bridge",
    "infinite-domain-lostcities-highway-compat-1.0.0.jar": "packdev/lostcities-highway-compat",
    "infinite-domain-stellaris-industry-1.0.0.jar": "packdev/stellaris-space-industry",
    "infinite-domain-unified-radiation-1.0.0.jar": "packdev/unified-radiation",
}


def load_instance_manifest():
    inst = json.loads((ROOT / "minecraftinstance.json").read_text(encoding="utf-8"))
    by_file = {}
    for addon in inst["installedAddons"]:
        fn = addon.get("fileNameOnDisk")
        if fn:
            by_file[fn] = {
                "name": addon.get("name"),
                "author": addon.get("primaryAuthor"),
                "url": addon.get("webSiteURL"),
            }
    return by_file


def read_toml_modids(zf):
    ids = []
    for candidate in ("META-INF/neoforge.mods.toml", "META-INF/mods.toml"):
        try:
            data = zf.read(candidate)
        except KeyError:
            continue
        try:
            parsed = tomllib.loads(data.decode("utf-8", errors="replace"))
            for mod in parsed.get("mods", []):
                mid = mod.get("modId")
                if mid and mid not in ("minecraft", "forge", "neoforge"):
                    ids.append(mid)
        except Exception:
            text = data.decode("utf-8", errors="replace")
            for m in re.finditer(r'modId\s*=\s*"([a-z0-9_\-]+)"', text):
                if m.group(1) not in ("minecraft", "forge", "neoforge"):
                    ids.append(m.group(1))
    seen = []
    for i in ids:
        if i not in seen:
            seen.append(i)
    return seen


def read_entity_ids(zf):
    """Entity registry names inferred from `entity.<namespace>.<name>` lang keys.
    Not exhaustive (misses entities with no translation override) but needs no
    running instance, unlike the item/block dump which came from a live KubeJS audit.
    """
    entities = {}
    for name in zf.namelist():
        m = re.match(r"assets/([a-z0-9_\-]+)/lang/en_us\.json$", name)
        if not m:
            continue
        try:
            lang = json.loads(zf.read(name).decode("utf-8", errors="replace"))
        except Exception:
            continue
        for key in lang:
            parts = key.split(".")
            if len(parts) >= 3 and parts[0] == "entity":
                entities.setdefault(parts[1], set()).add(".".join(parts[2:]))
    return entities


def load_namespace_counts():
    import csv

    counts = {}
    path = REGISTRY_DIR / "namespace-summary.csv"
    if not path.exists():
        return counts
    with open(path, encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            counts[row["namespace"]] = (row["item_count"], row["block_count"])
    return counts


def main():
    by_file = load_instance_manifest()
    jar_records = []
    all_entities = {}

    for jar in sorted(MODS.glob("*.jar")):
        record = {"file": jar.name, **by_file.get(jar.name, {"name": None, "author": None, "url": None})}
        try:
            with zipfile.ZipFile(jar) as zf:
                record["modids"] = read_toml_modids(zf)
                for ns, names in read_entity_ids(zf).items():
                    all_entities.setdefault(ns, set()).update(names)
        except zipfile.BadZipFile:
            record["modids"] = []
        jar_records.append(record)

    REGISTRY_DIR.mkdir(parents=True, exist_ok=True)
    (REGISTRY_DIR / "mod-jar-index.json").write_text(
        json.dumps(jar_records, indent=2), encoding="utf-8"
    )

    entity_count = 0
    with open(REGISTRY_DIR / "entity-ids.txt", "w", encoding="utf-8") as f:
        for ns in sorted(all_entities):
            for name in sorted(all_entities[ns]):
                f.write(f"{ns}:{name}\n")
                entity_count += 1

    ns_counts = load_namespace_counts()
    rows = []
    for r in jar_records:
        modid = r["modids"][0] if r["modids"] else ""
        extra_ids = r["modids"][1:]
        name = r.get("name") or r["file"]
        author = r.get("author") or ("Infinite Domain project" if r["file"] in PROJECT_SOURCES else "")
        items, blocks = ns_counts.get(modid, ("", ""))
        rows.append({
            "name": name, "modid": modid, "extra_ids": extra_ids, "author": author,
            "file": r["file"], "items": items, "blocks": blocks,
            "source": PROJECT_SOURCES.get(r["file"], ""),
        })
    rows.sort(key=lambda r: r["name"].lower())

    lines = [
        "# Mod List — Infinite Domain",
        "",
        f"*Generated by `scripts/build_mod_index.py` from `mods/*.jar` (reading each jar's "
        f"`neoforge.mods.toml`/`mods.toml`), cross-referenced with `minecraftinstance.json` for "
        f"display name/author. {len(rows)} jars total: {len(rows) - len(PROJECT_SOURCES)} third-party "
        f"+ {len(PROJECT_SOURCES)} project-built. Re-run the script whenever mods are added, removed, or updated.*",
        "",
        "Item/block counts (where available) are from `docs/registry-inventory/namespace-summary.csv`, "
        "keyed by the mod's primary namespace — a mod can register under a different namespace than its "
        "file name suggests, and mods that add no items/blocks (pure libraries, mixin patches, API shims) "
        "show blank counts.",
        "",
        "| Mod | Mod ID | Author | Items | Blocks | Jar file | Source (if project-built) |",
        "|---|---|---|---:|---:|---|---|",
    ]
    for r in rows:
        extra = f" (+{', '.join(r['extra_ids'])})" if r["extra_ids"] else ""
        lines.append(
            f"| {r['name']} | `{r['modid']}`{extra} | {r['author']} | {r['items']} | {r['blocks']} | "
            f"`{r['file']}` | {r['source']} |"
        )

    lines += ["", f"## Project-built mods ({len(PROJECT_SOURCES)})", "",
              "These are the Infinite Domain project's own compiled mods — never reacquired from "
              "CurseForge, sources tracked under `packdev/`:", ""]
    for fn, src in PROJECT_SOURCES.items():
        modid = next(r["modids"][0] for r in jar_records if r["file"] == fn)
        lines.append(f"- `{fn}` (`{modid}`) — source: `{src}/`")

    (ROOT / "docs" / "MOD_LIST.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"jars: {len(jar_records)}")
    print(f"entity ids: {entity_count} across {len(all_entities)} namespaces")
    print("wrote docs/MOD_LIST.md, docs/registry-inventory/mod-jar-index.json, "
          "docs/registry-inventory/entity-ids.txt")


if __name__ == "__main__":
    main()
