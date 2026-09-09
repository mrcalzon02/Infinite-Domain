#!/usr/bin/env python3
"""Find mod jars that ship tag definitions at pre-1.21 (plural) directory paths.

Minecraft 1.21 renamed the datapack tag directories to the singular form
(`tags/items` -> `tags/item`, `tags/blocks` -> `tags/block`, and so on). A jar
that still ships a tag at the plural path silently loads that tag as **empty**,
and any code that reads it via `ItemTags.create` / `BlockTags.create` sees
nothing. There is no warning in the log.

Two live examples in this pack, both of which broke real gameplay:

- `deepnether:portal_igniter` at `data/deepnether/tags/items/` -- the Echo Stone
  could not ignite the Deep Nether portal, so the Nether was unreachable.
- the six `lostcities:*` block tags (`foliage`, `rotatable`, `easybreakable`,
  `notbreakable`, `lights`, `needspoi`) at `data/lostcities/tags/blocks/` --
  `LostTags` creates all six TagKeys, so Lost Cities' foliage avoidance, ruin
  breakability, rotation and POI handling all ran against empty tags.

Both are fixed by supplying the same tag at the singular path from
`kubejs/data/...`, additively (`"replace": false`), which stays harmless if the
mod is ever fixed upstream.

**A legacy path is not by itself a bug.** Most mods that migrated to 1.21 wrote
the new singular file and left the old plural one behind, so the same jar ships
both and the tag loads fine; the stale copy is inert because nothing scans
`tags/items` any more. Others left behind a plural file with no values at all.
Porting those would add dead files to the pack, so this script separates the
harmless cases from the ones that actually load empty:

    harmless/same-jar   the jar also ships the singular path with the same values
    harmless/empty      the legacy file has no `values` and no `remove`
    ported              a pack file at the singular path covers the jar's values
    SUSPECT             jar ships both paths but the values differ
    BROKEN              nothing supplies the tag at the singular path

A pack file merely *existing* at the singular path is not a fix either: for a
shared tag like `minecraft:mineable/pickaxe` the pack's own file is there for
unrelated reasons and does not contain the mod's entries, so that still counts
as BROKEN (reported as a partial port).

    python dev/scripts/audit_legacy_tag_paths.py [--all]

Exits 0 when nothing is BROKEN or SUSPECT, 1 otherwise.
"""
from __future__ import annotations

import json
import os
import re
import sys
import zipfile

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
MODS = os.path.join(REPO, "mods")
PACK_DATA = os.path.join(REPO, "kubejs", "data")

# pre-1.21 plural directory -> the 1.21 singular directory
RENAMED = {
    "blocks": "block",
    "items": "item",
    "entity_types": "entity_type",
    "fluids": "fluid",
    "game_events": "game_event",
    "functions": "function",
    "damage_types": "damage_type",
    "banner_patterns": "banner_pattern",
    "cat_variants": "cat_variant",
    "enchantments": "enchantment",
    "instruments": "instrument",
    "painting_variants": "painting_variant",
    "point_of_interest_types": "point_of_interest_type",
}

TAG_PATH = re.compile(r"^data/([^/]+)/tags/([^/]+)/(.+)\.json$")


def pack_format(jar: zipfile.ZipFile) -> int | None:
    try:
        meta = json.loads(jar.read("pack.mcmeta").decode("utf-8-sig"))
        return int(meta["pack"]["pack_format"])
    except Exception:
        return None


def load(raw: bytes) -> dict:
    try:
        body = json.loads(raw.decode("utf-8-sig"))
        return body if isinstance(body, dict) else {}
    except Exception:
        return {}


def entries(body: dict, key: str = "values") -> set[str]:
    """Normalised tag entries. Values may be plain ids or {"id": ..} objects."""
    out = set()
    for v in body.get(key) or []:
        if isinstance(v, str):
            out.add(v)
        elif isinstance(v, dict) and isinstance(v.get("id"), str):
            out.add(v["id"])
    return out


def classify(jar: zipfile.ZipFile, names: set[str], ns: str, singular: str,
             path: str, values: set[str], removes: set[str]) -> tuple[str, set[str], bool]:
    """Return (state, missing entries, whether a pack file was present but partial)."""
    if not values and not removes:
        return "harmless/empty", set(), False

    sibling = "data/%s/tags/%s/%s.json" % (ns, singular, path)
    if sibling in names:
        sib = entries(load(jar.read(sibling)))
        if values <= sib:
            return "harmless/same-jar", set(), False
        return "SUSPECT", values - sib, False

    override = os.path.join(PACK_DATA, ns, "tags", singular, *path.split("/")) + ".json"
    if os.path.exists(override):
        with open(override, "rb") as fh:
            packed = entries(load(fh.read()))
        if values <= packed:
            return "ported", set(), False
        return "BROKEN", values - packed, True

    return "BROKEN", values, False


ORDER = ["BROKEN", "SUSPECT", "ported", "harmless/same-jar", "harmless/empty"]

BLURB = {
    "BROKEN": "nothing supplies this tag at the singular path -- it loads EMPTY",
    "SUSPECT": "jar ships both paths, but the legacy file has values the singular one lacks",
    "ported": "a pack file at the singular path covers the jar's values",
    "harmless/same-jar": "same jar also ships the singular path, covering these values",
    "harmless/empty": "the legacy file has no values and no removes -- inert",
}


def main() -> int:
    show_all = "--all" in sys.argv[1:]
    found: list[dict] = []

    for name in sorted(os.listdir(MODS)):
        if not name.endswith(".jar"):
            continue
        try:
            jar = zipfile.ZipFile(os.path.join(MODS, name))
        except Exception:
            continue
        pf = pack_format(jar)
        names = set(jar.namelist())
        for entry in sorted(names):
            m = TAG_PATH.match(entry)
            if not m:
                continue
            ns, kind, path = m.group(1), m.group(2), m.group(3)
            if kind not in RENAMED:
                continue
            singular = RENAMED[kind]
            legacy = load(jar.read(entry))
            state, missing, partial = classify(
                jar, names, ns, singular, path,
                entries(legacy), entries(legacy, "remove"))
            found.append({
                "jar": name, "pf": pf, "ns": ns, "path": path, "kind": kind,
                "singular": singular, "state": state, "missing": missing,
                "partial": partial,
            })

    by_state: dict[str, list[dict]] = {s: [] for s in ORDER}
    for rec in found:
        by_state[rec["state"]].append(rec)

    print("legacy-path tag files found: %d" % len(found))
    for state in ORDER:
        print("  %5d  %-18s %s" % (len(by_state[state]), state, BLURB[state]))

    for state in ORDER:
        rows = by_state[state]
        if not rows:
            continue
        if state not in ("BROKEN", "SUSPECT") and not show_all:
            continue
        print("\n%s -- %s" % (state, BLURB[state]))
        by_jar: dict[str, list[str]] = {}
        for rec in sorted(rows, key=lambda r: (r["jar"], r["ns"], r["path"])):
            line = "%s:%s  tags/%s -> tags/%s" % (
                rec["ns"], rec["path"], rec["kind"], rec["singular"])
            if rec["partial"]:
                line += "  [pack file exists but does not cover it]"
            if rec["missing"] and state in ("BROKEN", "SUSPECT"):
                shown = sorted(rec["missing"])
                line += "\n          missing: %s" % ", ".join(shown[:6])
                if len(shown) > 6:
                    line += ", ... (%d more)" % (len(shown) - 6)
            by_jar.setdefault("%s (pack_format=%s)" % (rec["jar"], rec["pf"]), []).append(line)
        for jar in sorted(by_jar):
            print("  %s" % jar)
            for line in by_jar[jar]:
                print("      %s" % line)

    bad = len(by_state["BROKEN"]) + len(by_state["SUSPECT"])
    if bad:
        print("\nA tag only matters if the mod's code actually reads it (grep the jar for the")
        print("tag name near ItemTags.create / BlockTags.create). Where it does, add")
        print("kubejs/data/<ns>/tags/<singular>/<path>.json with \"replace\": false.")
    if not show_all:
        print("\n(--all also lists the harmless and already-ported entries.)")

    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
