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

    python dev/scripts/audit_legacy_tag_paths.py

Exits 0 when every legacy tag found already has a pack-side override, 1 otherwise.
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


def main() -> int:
    legacy: list[tuple[str, str, str, str, str, int | None]] = []

    for name in sorted(os.listdir(MODS)):
        if not name.endswith(".jar"):
            continue
        try:
            jar = zipfile.ZipFile(os.path.join(MODS, name))
        except Exception:
            continue
        pf = pack_format(jar)
        for entry in jar.namelist():
            m = TAG_PATH.match(entry)
            if not m:
                continue
            ns, kind, path = m.group(1), m.group(2), m.group(3)
            if kind not in RENAMED:
                continue
            legacy.append((name, ns, kind, RENAMED[kind], path, pf))

    unfixed = []
    fixed = []
    for jarname, ns, kind, singular, path, pf in legacy:
        override = os.path.join(PACK_DATA, ns, "tags", singular, *path.split("/"))
        override += ".json"
        (fixed if os.path.exists(override) else unfixed).append(
            (jarname, ns, kind, singular, path, pf))

    print("legacy-path tag files found: %d (%d have a pack file at the singular path, %d do not)"
          % (len(legacy), len(fixed), len(unfixed)))

    if fixed:
        # NOTE: this only means a file exists at the singular path. For a shared
        # tag like minecraft:mineable/pickaxe the pack's own file will not contain
        # the mod's entries, so those remain effectively lost -- only a
        # deliberately ported tag (matching values) is actually repaired.
        print("\na pack file exists at the singular path (ported, or merely coincident):")
        for jarname, ns, kind, singular, path, _pf in sorted(fixed):
            print("  %-24s %s:%s  (tags/%s -> tags/%s)" % (jarname[:24], ns, path, kind, singular))

    if unfixed:
        print("\nNOT fixed -- these tags load empty at runtime:")
        by_jar: dict[str, list[str]] = {}
        for jarname, ns, kind, singular, path, pf in sorted(unfixed):
            by_jar.setdefault("%s (pack_format=%s)" % (jarname, pf), []).append(
                "%s:%s  tags/%s -> tags/%s" % (ns, path, kind, singular))
        for jar in sorted(by_jar):
            print("  %s" % jar)
            for line in by_jar[jar]:
                print("      %s" % line)
        print("\nA tag only matters if the mod's code actually reads it (grep the jar for the")
        print("tag name near ItemTags.create / BlockTags.create). Where it does, add")
        print("kubejs/data/<ns>/tags/<singular>/<path>.json with \"replace\": false.")

    return 1 if unfixed else 0


if __name__ == "__main__":
    sys.exit(main())
