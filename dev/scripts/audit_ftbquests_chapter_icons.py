#!/usr/bin/env python3
"""Fail loudly if any FTB Quests chapter would fall back to a cycling icon.

Three ways a chapter ends up cycling through every quest icon in the chapter
(``Chapter.getAltIcon()`` -> ``IconAnimation.fromList(...)``):

1. No top-level ``icon:`` field at all.
2. ``icon:`` written as a bare string.  FTB Quests reads it with
   ``nbt.getCompound("icon")``, which yields an empty compound for a StringTag,
   so the icon is dropped at load and then *deleted from the file* on the next
   save.  This is the regression that keeps coming back -- treat any string-form
   icon as a hard failure, not a style nit.
3. ``icon: { id: ... }`` naming an item that does not exist, which resolves to
   ``ftbquests:missing_item``.

Run this after any tool touches config/ftbquests/quests/chapters/.

    python dev/scripts/audit_ftbquests_chapter_icons.py

Exits 0 clean, 1 with findings.
"""
from __future__ import annotations

import os
import re
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CHAPTERS = os.path.join(REPO, "config", "ftbquests", "quests", "chapters")

sys.path.insert(0, os.path.join(REPO, "dev", "scripts", "generators"))
from apply_ftbquests_chapter_icons import build_item_index  # noqa: E402

STRING_FORM = re.compile(r'^\ticon:\s*"')
COMPOUND_ID = re.compile(r'^\ticon:\s*\{\s*id:\s*"([^"]+)"\s*\}\s*$')
QUEST_STRING = re.compile(r'^\t\t\ticon:\s*"([^"]+)"\s*$', re.M)
QUEST_COMPOUND = re.compile(r'^\t\t\ticon:\s*\{\s*id:\s*"([^"]+)"\s*\}\s*$', re.M)
ITEM_ID = re.compile(r"^[a-z0-9_.-]+:[a-z0-9_./-]+$")


def audit_quest_icons(index: set[str]) -> tuple[list[str], list[str], int]:
    """Quest-level icons share the chapter icon's storage format and bug.

    Hard failures: the bare-string form (FTB Quests deletes it on save) and a
    non-namespaced value (an FTB Quests object id mistakenly written as an item).
    Unresolvable kubejs:-namespace ids are only reported as unverified, because
    KubeJS registers those at runtime from template literals and no static index
    can see them.
    """
    findings: list[str] = []
    unverified: set[str] = set()
    total = 0
    for fn in sorted(f for f in os.listdir(CHAPTERS) if f.endswith(".snbt")):
        text = open(os.path.join(CHAPTERS, fn), encoding="utf-8").read()
        stem = fn[:-5]
        for m in QUEST_STRING.finditer(text):
            findings.append(
                "%s: a quest icon is a STRING (%s); FTB Quests deletes that form on save"
                % (stem, m.group(1)))
        for m in QUEST_COMPOUND.finditer(text):
            total += 1
            item = m.group(1)
            if not ITEM_ID.match(item):
                findings.append("%s: quest icon %r is not an item id" % (stem, item))
            elif item not in index:
                if item.startswith("kubejs:"):
                    unverified.add(item)
                else:
                    findings.append(
                        "%s: quest icon %s does not resolve -- renders as missing_item"
                        % (stem, item))
    return findings, sorted(unverified), total


def main() -> int:
    index = build_item_index()
    findings: list[str] = []
    ok = 0

    for fn in sorted(f for f in os.listdir(CHAPTERS) if f.endswith(".snbt")):
        path = os.path.join(CHAPTERS, fn)
        stem = fn[:-5]
        lines = open(path, encoding="utf-8").read().splitlines()
        icon_lines = [l for l in lines if l.startswith("\ticon:")]

        if not icon_lines:
            findings.append(
                "%s: NO chapter icon -- the chapter button will cycle every quest icon" % stem)
            continue

        line = icon_lines[0]
        if STRING_FORM.match(line):
            findings.append(
                "%s: icon is a STRING (%s). FTB Quests cannot read this and will delete it "
                "on the next save. Use icon: { id: \"...\" }." % (stem, line.strip()))
            continue

        m = COMPOUND_ID.match(line)
        if not m:
            # Multi-line compound is legal SNBT; only flag it as unnormalized.
            if line.strip() == "icon: {":
                body = lines[lines.index(line) + 1].strip()
                m2 = re.match(r'^id:\s*"([^"]+)"$', body)
                if m2:
                    item = m2.group(1)
                    if item not in index:
                        findings.append("%s: icon item %s does not exist" % (stem, item))
                    else:
                        ok += 1
                    continue
            findings.append("%s: unrecognized icon form: %s" % (stem, line.strip()))
            continue

        item = m.group(1)
        if item not in index:
            findings.append(
                "%s: icon item %s does not resolve -- renders as ftbquests:missing_item"
                % (stem, item))
        else:
            ok += 1

    qfindings, unverified, qtotal = audit_quest_icons(index)
    findings.extend(qfindings)

    print("%d chapters with a valid fixed icon; %d quest icons checked; %d findings"
          % (ok, qtotal, len(findings)))
    if unverified:
        print("%d quest icons are KubeJS runtime-registered and could not be verified "
              "statically (expected, not an error):" % len(unverified))
        for item in unverified[:5]:
            print("    %s" % item)
        if len(unverified) > 5:
            print("    ... and %d more" % (len(unverified) - 5))
    for f in findings:
        print("  ! %s" % f, file=sys.stderr)
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
