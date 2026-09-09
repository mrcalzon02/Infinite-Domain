#!/usr/bin/env python3
"""Apply fixed chapter icons to every FTB Quests chapter, in the only form FTB
Quests can actually read back.

Background
----------
FTB Quests 2101.1.30 reads the chapter icon in
``QuestObjectBase.readData`` as::

    this.rawIcon = singleItemOrMissingFromNBT(nbt.getCompound("icon"), provider);

``CompoundTag.getCompound`` returns an *empty* compound when the stored tag is
not a compound.  So ``icon: "create:andesite_alloy"`` (a StringTag) yields an
empty compound -> ``ItemStack.EMPTY`` -> and ``writeData`` only emits the field
when ``!rawIcon.isEmpty()``.  The icon is therefore silently deleted from the
.snbt the first time the quest file is written back, and
``Chapter.getAltIcon()`` falls back to
``IconAnimation.fromList(<every quest icon in the chapter>)`` -- the endless
icon cycling on the chapter buttons.

The compound form ``icon: { id: "<item id>" }`` matches
``ItemStack.SINGLE_ITEM_CODEC`` and round-trips cleanly, so it survives play
sessions.

This generator is idempotent: run it as often as you like.

Usage
-----
    python dev/scripts/generators/apply_ftbquests_chapter_icons.py [--check]

``--check`` reports what would change and exits non-zero if anything is off,
without writing.  That is the mode the audit script uses.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import zipfile

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
MANIFEST = os.path.join(REPO, "dev", "docs", "ftbquests-chapter-icons.json")
LOCKFILE = os.path.join(REPO, "dev", "docs", "ftbquests-chapter-icons.lock.json")
CHAPTERS = os.path.join(REPO, "config", "ftbquests", "quests", "chapters")

# Top-level chapter keys are indented with exactly one tab; quest-level keys
# sit three tabs deep.  Anchoring on a single leading tab is what keeps this
# from ever touching a quest's own icon.
TOP_ICON = re.compile(r"^\ticon:", re.M)
TOP_ID = re.compile(r'^\tid: "', re.M)


def build_item_index() -> set[str]:
    """Best-effort set of valid item ids.

    The checked-in registry inventory is authoritative but goes stale whenever a
    mod jar is added, so it is unioned with the item models shipped by every jar
    and by kubejs/assets.
    """
    ids: set[str] = set()

    inv = os.path.join(REPO, "dev", "docs", "registry-inventory", "item-ids.txt")
    if os.path.exists(inv):
        with open(inv, encoding="utf-8") as fh:
            ids.update(line.strip() for line in fh if line.strip())

    model = re.compile(r"^assets/([^/]+)/models/item/(.+)\.json$")
    mods = os.path.join(REPO, "mods")
    if os.path.isdir(mods):
        for name in sorted(os.listdir(mods)):
            if not name.endswith(".jar"):
                continue
            try:
                jar = zipfile.ZipFile(os.path.join(mods, name))
            except Exception:
                continue
            for entry in jar.namelist():
                m = model.match(entry)
                if m:
                    ids.add("%s:%s" % (m.group(1), m.group(2)))

    assets = os.path.join(REPO, "kubejs", "assets")
    for dirpath, _dirs, files in os.walk(assets):
        rel = os.path.relpath(dirpath, assets).replace("\\", "/").split("/")
        if len(rel) >= 3 and rel[1] == "models" and rel[2] == "item":
            ns, sub = rel[0], "/".join(rel[3:])
            for fn in files:
                if fn.endswith(".json"):
                    stem = (sub + "/" if sub else "") + fn[:-5]
                    ids.add("%s:%s" % (ns, stem))

    ids |= kubejs_startup_ids()
    return ids


# KubeJS items are registered at runtime in kubejs/startup_scripts, so they never
# appear in a jar or as an asset file.  Two idioms are recoverable statically:
# a literal event.create('name'), and the catalog-table idiom
# [['name', 'Display Name', 'texture', 'tooltip'], ...].  Anything built from a
# template literal (event.create(`${metal.id}_mineral_dust`)) cannot be resolved
# without executing KubeJS, which is why callers treat an unresolved
# kubejs:-namespace id as UNVERIFIED rather than as an error.
CREATE_LITERAL = re.compile(r"""\.create\(\s*['"]([a-z0-9_./:]+)['"]""")
CATALOG_ROW = re.compile(r"""\[\s*['"]([a-z0-9_]+)['"]\s*,\s*['"][A-Z0-9]""")


def kubejs_startup_ids() -> set[str]:
    ids: set[str] = set()
    base = os.path.join(REPO, "kubejs", "startup_scripts")
    if not os.path.isdir(base):
        return ids
    for dirpath, _dirs, files in os.walk(base):
        for fn in files:
            if not fn.endswith(".js"):
                continue
            try:
                src = open(os.path.join(dirpath, fn), encoding="utf-8").read()
            except Exception:
                continue
            for m in CREATE_LITERAL.finditer(src):
                name = m.group(1)
                ids.add(name if ":" in name else "kubejs:" + name)
            for m in CATALOG_ROW.finditer(src):
                ids.add("kubejs:" + m.group(1))
    return ids


def value_extent(lines: list[str], start: int) -> int:
    """Return the index one past the last line of the icon value starting at `start`.

    Handles both ``icon: { id: "x" }`` and the multi-line brace form.
    """
    depth = 0
    for i in range(start, len(lines)):
        depth += lines[i].count("{") - lines[i].count("}")
        if depth <= 0:
            return i + 1
    return start + 1


def apply(check_only: bool) -> int:
    manifest = json.load(open(MANIFEST, encoding="utf-8"))["chapters"]
    index = build_item_index()

    problems: list[str] = []
    changed: list[str] = []
    resolved: dict[str, str] = {}
    unchanged = 0

    files = sorted(f for f in os.listdir(CHAPTERS) if f.endswith(".snbt"))
    seen = set()

    for fn in files:
        stem = fn[:-5]
        seen.add(stem)
        path = os.path.join(CHAPTERS, fn)
        spec = manifest.get(stem)
        if spec is None:
            problems.append("%s: no entry in ftbquests-chapter-icons.json" % stem)
            continue

        chosen = next((c for c in spec["candidates"] if c in index), None)
        if chosen is None:
            problems.append("%s: none of %s resolve to a real item" % (stem, spec["candidates"]))
            continue

        resolved[stem] = chosen
        text = open(path, encoding="utf-8").read()
        lines = text.splitlines(keepends=True)
        want = '\ticon: { id: "%s" }\n' % chosen

        icon_at = next((i for i, l in enumerate(lines) if l.startswith("\ticon:")), None)
        if icon_at is None:
            id_at = next((i for i, l in enumerate(lines) if l.startswith('\tid: "')), None)
            if id_at is None:
                problems.append("%s: no top-level id: line, cannot place icon" % stem)
                continue
            new = lines[:id_at] + [want] + lines[id_at:]
            note = "added %s" % chosen
        else:
            end = value_extent(lines, icon_at)
            current = "".join(lines[icon_at:end])
            if current == want:
                unchanged += 1
                continue
            new = lines[:icon_at] + [want] + lines[end:]
            was_string = re.match(r'^\ticon: "', current) is not None
            note = ("repaired unreadable string form -> %s" % chosen) if was_string \
                else ("normalized -> %s" % chosen)

        changed.append("%s: %s" % (stem, note))
        if not check_only:
            with open(path, "w", encoding="utf-8", newline="") as fh:
                fh.write("".join(new))

    for stem in sorted(set(manifest) - seen):
        problems.append("%s: manifest entry has no chapter file" % stem)

    # The lockfile is how other tooling (ensure_ftbquest_icons.js) learns the
    # resolved icon without having to scan every mod jar itself.  It keeps this
    # generator the single authority for chapter icons.
    if not check_only and not problems:
        with open(LOCKFILE, "w", encoding="utf-8", newline="\n") as fh:
            json.dump({"_generated_by": "dev/scripts/generators/apply_ftbquests_chapter_icons.py",
                       "chapters": dict(sorted(resolved.items()))}, fh, indent=2)
            fh.write("\n")

    verb = "would change" if check_only else "changed"
    for line in changed:
        print("  %s %s" % ("~" if check_only else "+", line))
    print("%d %s, %d already correct, %d problems" % (len(changed), verb, unchanged, len(problems)))
    for p in problems:
        print("  ! %s" % p, file=sys.stderr)

    if problems:
        return 2
    if check_only and changed:
        return 1
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="report without writing")
    args = ap.parse_args()
    sys.exit(apply(args.check))
