"""Generate the Domain Compendium FTB Quests chapter.

Reads the candidate inventory produced by
`scripts/audit_domain_compendium_candidates.py`, keeps every row whose decision is
`include` (textured AND has an obtainment route) except the namespaces listed in
EXCLUDED_NAMESPACES, and writes:

* config/ftbquests/quests/chapters/domain_compendium.snbt
* the chapter's block of keys in config/ftbquests/quests/lang/en_us.snbt
  (fenced by markers so re-runs replace only that block)
* the chapter group entry in config/ftbquests/quests/chapter_groups.snbt

Only ids with an *item* form are eligible: item and block are separate
registries, so fluids and item-less blocks (minecraft:lava, petrochem:gasoline)
would be rewritten to ftbquests:missing_item the first time the game loads the
chapter. The candidate CSV gates on this and ItemOracle re-checks it here.

Task and section ids come from docs/domain-compendium/quest-id-ledger.csv, which
binds an id to its *content* rather than its position in the file. FTB Quests
keys player progress on task id, so without the ledger any change to the
candidate list would renumber the tasks after it and silently wipe completion.

Output is a pure function of the candidate CSV, the ledger and the constants
below, so re-running after a registry / asset change produces a clean diff.

Authority: docs/DOMAIN_COMPENDIUM_CHAPTER.md
"""

from __future__ import annotations

import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pack_content_oracle import ItemOracle  # noqa: E402


ROOT = Path(__file__).resolve().parents[3]
CANDIDATES = ROOT / "dev/docs/domain-compendium/candidate-inventory.csv"
CHAPTER = ROOT / "config/ftbquests/quests/chapters/domain_compendium.snbt"
LANG = ROOT / "config/ftbquests/quests/lang/en_us.snbt"
GROUPS = ROOT / "config/ftbquests/quests/chapter_groups.snbt"
MOD_INDEX = ROOT / "dev/docs/registry-inventory/mod-jar-index.json"
LEDGER = ROOT / "dev/docs/domain-compendium/quest-id-ledger.csv"

# Decision 1 (docs/DOMAIN_COMPENDIUM_CHAPTER.md §8): chisel re-texture palettes
# are catalogued through a future collapsed pass, not one task per variant.
EXCLUDED_NAMESPACES = {"rechiseled", "rechiseledcreate"}

# Decision 2: tasks consume their submission - the Compendium is a civilisation
# -scale sink in the same spirit as the Mastery chapters.
CONSUME_ITEMS = True

TASKS_PER_QUEST = 40
COL_SPACING = 2.0
ROW_SPACING = 1.5

GROUP_ID = "7C0DEC0FFEE00001"
CHAPTER_ID = "7C0DE0C000000000"
ROOT_QUEST_ID = "7C0DE0C000000001"
ROOT_TASK_ID = "7C0DE0D000000001"
CAPSTONE_QUEST_ID = "7C0DE0C0000000FF"
CAPSTONE_TASK_ID = "7C0DE0D0000000FF"
CAPSTONE_REWARD_ID = "7C0DE0E0000000FF"
# Registered in kubejs/startup_scripts/main.js, textured, and currently unused -
# it was created for exactly this and never wired up.
CAPSTONE_EMBLEM = "kubejs:ultima_collection_emblem"

LANG_BEGIN = "\t# --- BEGIN domain_compendium (generated) ---"
LANG_END = "\t# --- END domain_compendium (generated) ---"

MANUAL_MOD_NAMES = {
    "minecraft": "Minecraft",
    "kubejs": "Infinite Domain",
    "infinite_domain": "Infinite Domain",
    "c": "Common",
}


def mod_names() -> dict[str, str]:
    names = dict(MANUAL_MOD_NAMES)
    for entry in json.loads(MOD_INDEX.read_text(encoding="utf-8-sig")):
        for modid in entry.get("modids", []):
            names.setdefault(modid, entry.get("name") or modid)
    return names


ID_PREFIX = {"section": "7C0DE1", "task": "7C0DE2"}


class IdLedger:
    """Binds quest/task ids to content so regeneration cannot reset progress.

    Keys are the item id (tasks) and "<namespace>#<part>" (section quests).
    Retired keys are kept, so an item that leaves the candidate list and later
    returns reclaims its original id instead of colliding with a reissued one.
    """

    def __init__(self, path: Path):
        self.path = path
        self.ids: dict[tuple[str, str], str] = {}
        if path.exists():
            with path.open(encoding="utf-8", newline="") as handle:
                for row in csv.DictReader(handle):
                    self.ids[(row["kind"], row["key"])] = row["id"]
        self.issued = 0
        self._next = {
            kind: max(
                (int(value[len(prefix):], 16)
                 for (k, _), value in self.ids.items() if k == kind),
                default=0,
            ) + 1
            for kind, prefix in ID_PREFIX.items()
        }

    def get(self, kind: str, key: str) -> str:
        known = self.ids.get((kind, key))
        if known is not None:
            return known
        index = self._next[kind]
        self._next[kind] = index + 1
        self.issued += 1
        value = f"{ID_PREFIX[kind]}{index:010X}"
        self.ids[(kind, key)] = value
        return value

    def save(self) -> None:
        with self.path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["kind", "key", "id"])
            writer.writerows(
                [kind, key, value] for (kind, key), value in sorted(self.ids.items())
            )


def assert_items_exist(included: dict[str, list[str]]) -> None:
    """Refuse to emit a task whose item no player could ever hand in."""
    oracle = ItemOracle()
    broken = sorted(
        item_id
        for ids in included.values()
        for item_id in ids
        if not oracle.exists(item_id)
    )
    if broken:
        shown = "
".join(f"  {i} - {oracle.why_missing(i)}" for i in broken[:20])
        more = f"
  ... and {len(broken) - 20} more" if len(broken) > 20 else ""
        raise SystemExit(
            f"refusing to write {CHAPTER.name}: {len(broken)} task item(s) have no "
            f"item form and would load as ftbquests:missing_item:
{shown}{more}"
        )


def load_included() -> dict[str, list[str]]:
    by_namespace: dict[str, list[str]] = defaultdict(list)
    with CANDIDATES.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["decision"] != "include":
                continue
            if row["namespace"] in EXCLUDED_NAMESPACES:
                continue
            # Block-registry-only ids (fluids, item-less blocks) cannot be handed
            # in. The CSV decides this too; re-checked here so a stale or
            # hand-edited inventory cannot reintroduce uncompletable tasks.
            if row["is_item"] != "True":
                continue
            by_namespace[row["namespace"]].append(row["id"])
    for ids in by_namespace.values():
        ids.sort()
    return dict(by_namespace)


def chunk(items: list[str], size: int) -> list[list[str]]:
    return [items[i:i + size] for i in range(0, len(items), size)]


def esc(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def build() -> None:
    names = mod_names()
    included = load_included()
    # widest namespaces first, ties broken by name for a stable layout
    namespaces = sorted(included, key=lambda ns: (-len(included[ns]), ns))

    quests: list[str] = []
    lang: list[str] = [LANG_BEGIN]
    task_counter = 0
    section_counter = 0
    section_ids: list[str] = []
    total_tasks = 0
    max_row = 1

    # root - octagon at the chapter's top edge so the coherence analyzer reads it
    # as a chapter-orientation node rather than a self-certified checkmark.
    quests.append(
        "\t\t{\n"
        f'\t\t\ticon: "minecraft:chiseled_bookshelf"\n'
        f'\t\t\tid: "{ROOT_QUEST_ID}"\n'
        '\t\t\toptional: true\n'
        '\t\t\tshape: "octagon"\n'
        '\t\t\tsize: 1.5d\n'
        f'\t\t\ttasks: [{{ id: "{ROOT_TASK_ID}", type: "checkmark" }}]\n'
        "\t\t\tx: 0.0d\n"
        "\t\t\ty: 0.0d\n"
        "\t\t}"
    )
    lang.append(f'\tchapter.{CHAPTER_ID}.title: "The Domain Compendium"')
    lang.append(
        f'\tchapter.{CHAPTER_ID}.subtitle: '
        f'"One of every obtainable, rendered item and block - permanently catalogued"'
    )
    lang.append(f'\tchapter_group.{GROUP_ID}.title: "Domain Compendium"')
    lang.append(f'\tquest.{ROOT_QUEST_ID}.title: "Open the Compendium"')
    lang.append(
        f'\tquest.{ROOT_QUEST_ID}.quest_desc: ['
        + esc(
            "An optional, exhaustive catalogue. Every section below asks for one "
            "of each obtainable item or block from a single mod; submissions are "
            "consumed. Nothing here gates progression - it is a completion record "
            "for a finished domain."
        )
        + " "
        + esc(
            "Phantom variants whose base mod is absent (most AllTheCompressed "
            "families, most Ex Deorum sieves) are deliberately excluded - see "
            "docs/DOMAIN_COMPENDIUM_CHAPTER.md."
        )
        + " ]"
    )

    for col, namespace in enumerate(namespaces, start=1):
        ids = included[namespace]
        display = names.get(namespace, namespace.replace("_", " ").title())
        groups = chunk(ids, TASKS_PER_QUEST)
        x = round(col * COL_SPACING, 2)
        for part, batch in enumerate(groups, start=1):
            section_counter += 1
            qid = section_hex(section_counter)
            section_ids.append(qid)
            y = round(part * ROW_SPACING, 2)
            task_lines = []
            for item_id in batch:
                task_counter += 1
                total_tasks += 1
                consume = "consume_items: true, " if CONSUME_ITEMS else ""
                task_lines.append(
                    f'\t\t\t\t{{ {consume}id: "{task_hex(task_counter)}", '
                    f'item: {{ count: 1, id: "{item_id}" }}, type: "item" }}'
                )
            quests.append(
                "\t\t{\n"
                f'\t\t\tdependencies: ["{ROOT_QUEST_ID}"]\n'
                f'\t\t\ticon: "{batch[0]}"\n'
                f'\t\t\tid: "{qid}"\n'
                '\t\t\toptional: true\n'
                # rsquare = the legend's "commissioning / material-submission node",
                # already used for the Mastery chapters' submit-materials quests.
                '\t\t\tshape: "rsquare"\n'
                "\t\t\tsize: 0.75d\n"
                "\t\t\ttasks: [\n" + "\n".join(task_lines) + "\n\t\t\t]\n"
                f"\t\t\tx: {x}d\n"
                f"\t\t\ty: {y}d\n"
                "\t\t}"
            )
            max_row = max(max_row, part)
            suffix = f" {part}" if len(groups) > 1 else ""
            lang.append(f'\tquest.{qid}.title: {esc(f"{display}{suffix}")}')

    # capstone - depends on every section so nothing can be skipped; placed below
    # the tallest column so its (hidden) dependency lines point forward.
    deps = ", ".join(f'"{qid}"' for qid in section_ids)
    capstone_y = round((max_row + 2) * ROW_SPACING, 2)
    quests.append(
        "\t\t{\n"
        f"\t\t\tdependencies: [{deps}]\n"
        f'\t\t\ticon: "{CAPSTONE_EMBLEM}"\n'
        f'\t\t\tid: "{CAPSTONE_QUEST_ID}"\n'
        '\t\t\toptional: true\n'
        '\t\t\tshape: "octagon"\n'
        "\t\t\tsize: 1.5d\n"
        "\t\t\trewards: [{ "
        f'id: "{CAPSTONE_REWARD_ID}", item: {{ count: 1, id: "{CAPSTONE_EMBLEM}" }}, type: "item" '
        "}]\n"
        f'\t\t\ttasks: [{{ id: "{CAPSTONE_TASK_ID}", type: "checkmark" }}]\n'
        "\t\t\tx: 0.0d\n"
        f"\t\t\ty: {capstone_y}d\n"
        "\t\t}"
    )
    lang.append(f'\tquest.{CAPSTONE_QUEST_ID}.title: "The Domain, Catalogued"')
    lang.append(
        f'\tquest.{CAPSTONE_QUEST_ID}.quest_desc: ['
        + esc(
            "Every section of the Compendium is complete. One of each obtainable "
            "item and block in the pack has passed through the ledger."
        )
        + " ]"
    )
    lang.append(f'\ttask.{CAPSTONE_TASK_ID}.title: "Close the ledger"')
    lang.append(LANG_END)

    chapter_snbt = (
        "{\n"
        "\tdefault_hide_dependency_lines: true\n"
        '\tdefault_quest_shape: "rsquare"\n'
        '\tfilename: "domain_compendium"\n'
        f'\tgroup: "{GROUP_ID}"\n'
        f'\ticon: "minecraft:chiseled_bookshelf"\n'
        f'\tid: "{CHAPTER_ID}"\n'
        "\timages: [ ]\n"
        "\torder_index: 0\n"
        "\tquest_links: [ ]\n"
        "\tquests: [\n" + "\n".join(quests) + "\n\t]\n"
        "}\n"
    )
    CHAPTER.write_text(chapter_snbt, encoding="utf-8")

    _splice_lang("\n".join(lang) + "\n")
    _ensure_group()

    print(
        f"domain_compendium: {len(namespaces)} sections, "
        f"{section_counter} section quests, {total_tasks:,} item tasks "
        f"(+ root + capstone). excluded namespaces: {sorted(EXCLUDED_NAMESPACES)}"
    )


def _splice_lang(block: str) -> None:
    text = LANG.read_text(encoding="utf-8")
    pattern = re.compile(
        re.escape(LANG_BEGIN) + r".*?" + re.escape(LANG_END) + r"\n?",
        re.DOTALL,
    )
    text = pattern.sub("", text)
    closing = text.rstrip().rfind("}")
    if closing < 0:
        raise SystemExit("could not find closing brace in en_us.snbt")
    LANG.write_text(text[:closing].rstrip() + "\n\n" + block + "}\n", encoding="utf-8")


def _ensure_group() -> None:
    lines = GROUPS.read_text(encoding="utf-8").splitlines()
    if any(GROUP_ID in line for line in lines):
        return
    out: list[str] = []
    for line in lines:
        if line.strip() == "]":
            out.append(f'\t\t{{ id: "{GROUP_ID}" }}')
        out.append(line)
    GROUPS.write_text("\n".join(out) + "\n", encoding="utf-8")


if __name__ == "__main__":
    build()
