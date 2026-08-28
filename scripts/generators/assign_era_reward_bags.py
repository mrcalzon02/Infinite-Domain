"""Assign era bags to a restrained selection of optional technical lessons.

Era chapters (2-8): every ~third gear lesson without a bespoke reward gets a
common Supply Bag; the last eligible gear lesson gets a rare Priority Cache.

Side chapters: same cadence, but eligibility is "not a checkmark, not an
orientation octagon, and no bespoke *item* reward" (xp-only rewards still
qualify), and the bag tier follows the per-chapter era in SIDE_CHAPTERS. See
docs/ERA_REWARD_BAG_CONVENTION.md.

Deterministic and idempotent.
"""

from __future__ import annotations

import csv
import hashlib
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CHAPTERS = ROOT / "config/ftbquests/quests/chapters"
LANG = ROOT / "config/ftbquests/quests/lang/en_us.snbt"
REPORT = ROOT / "docs/era-reward-bags/reward-assignments.csv"
FORCED_COMMON = {
    # The refinery output bank is the explicit Era 3 multiblock lesson and
    # should demonstrate the common-bag convention even between cadence slots.
    3: {"4310000000000002"},
}
# Side chapter file stem -> the era whose bag tier fits its content.
SIDE_CHAPTERS = {
    "sustenance_medicine_habitation": 2,
    "scavenging_defense_containment": 2,
    "environmental_survival_engineering": 3,
    "parallel_factory_paths": 3,
    "brewery_and_winery": 1,
    "coffee_tea_economy": 1,
    "feeding_the_domain": 2,
    "early_livestock_exchange": 1,
    "undead_settlement_automation": 6,
    "air_sea_global_logistics": 4,
    "abyssal_recovery": 4,
    "old_world_investigation": 3,
}


def reward_id(quest_id: str) -> str:
    # 0x6A keeps the signed long positive; the digest makes collisions negligible.
    return "6A" + hashlib.sha256(("era-bag:" + quest_id).encode()).hexdigest()[:14].upper()


def rewards_have_item(block: str) -> bool:
    section = re.search(r"rewards:\s*\[([\s\S]*?)\]\s*\n\t\t\t(?:shape|tasks):", block)
    return bool(section) and 'type: "item"' in section.group(1)


def process_chapter(path: Path, era: int, side: bool, assignments: list) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [i for i, line in enumerate(lines) if line == "\t\t{"]
    blocks = []
    for number, start in enumerate(starts):
        end = starts[number + 1] if number + 1 < len(starts) else len(lines)
        blocks.append((start, end, "\n".join(lines[start:end])))

    def eligible(block: str) -> bool:
        if 'type: "checkmark"' in block:
            return False
        already_bagged = f"kubejs:era{era}_" in block
        if side:
            if 'shape: "octagon"' in block:
                return False
            return already_bagged or not rewards_have_item(block)
        return 'shape: "gear"' in block and ("rewards:" not in block or already_bagged)

    candidates = [b for b in blocks if eligible(b[2])]
    selected = {i for i in range(len(candidates)) if (i + 1) % 3 == 0}
    selected.update(
        i for i, (_, _, block) in enumerate(candidates)
        if any(qid in block for qid in FORCED_COMMON.get(era, set()))
    )
    if candidates:
        selected.add(len(candidates) - 1)

    splices = []  # (start_idx, end_idx_exclusive, replacement_lines)
    for index in sorted(selected):
        start, end, block = candidates[index]
        match = re.search(r'\n\t\t\tid:\s*"([0-9A-F]+)"', "\n" + block)
        if not match:
            continue
        qid = match.group(1)
        bag = f"kubejs:era{era}_{'priority_cache' if index == len(candidates) - 1 else 'supply_bag'}"
        existing_bag = re.search(rf'kubejs:era{era}_(?:supply_bag|priority_cache)', block)
        if existing_bag:
            if existing_bag.group(0) != bag:
                for line_index in range(start, end):
                    if existing_bag.group(0) in lines[line_index]:
                        lines[line_index] = lines[line_index].replace(existing_bag.group(0), bag)
                        break
            assignments.append((era, path.name, qid, bag))
            continue
        rid = reward_id(qid)
        entry = [f'\t\t\t\tid: "{rid}"',
                 f'\t\t\t\titem: {{ count: 1, id: "{bag}" }}',
                 '\t\t\t\ttype: "item"']
        r_open = next((i for i in range(start, end) if lines[i].startswith("\t\t\trewards:")), None)
        if r_open is None:                                   # no rewards -> new key
            anchor = next(i for i in range(start, end)
                          if lines[i].startswith(("\t\t\tshape:", "\t\t\ttasks:")))
            splices.append((anchor, anchor, ["\t\t\trewards: [{", *entry, "\t\t\t}]"]))
        elif lines[r_open].rstrip().endswith("[{"):          # rewards: [{ ... }] -> add element
            r_close = next(i for i in range(r_open, end) if lines[i].rstrip() == "\t\t\t}]")
            splices.append((r_close, r_close + 1, ["\t\t\t}", "\t\t\t{", *entry, "\t\t\t}]"]))
        else:                                               # rewards: [ \n {..} \n ] -> add element
            r_close = next(i for i in range(r_open, end) if lines[i].rstrip() == "\t\t\t]")
            splices.append((r_close, r_close, ["\t\t\t{", *entry, "\t\t\t}"]))
        assignments.append((era, path.name, qid, bag))

    for s, e, repl in sorted(splices, key=lambda x: -x[0]):
        lines[s:e] = repl
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    lang = LANG.read_text(encoding="utf-8-sig")
    titles = dict(re.findall(r'quest\.([0-9A-F]+)\.title:\s*"([^"]+)"', lang))
    assignments: list[tuple[int, str, str, str]] = []

    for era in range(1, 9):
        process_chapter(next(CHAPTERS.glob(f"era_0{era}_*.snbt")), era, side=False, assignments=assignments)
    for stem, era in SIDE_CHAPTERS.items():
        path = CHAPTERS / f"{stem}.snbt"
        if path.exists():
            process_chapter(path, era, side=True, assignments=assignments)

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    with REPORT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["era", "chapter", "quest_id", "quest_title", "reward_item"])
        writer.writerows((e, c, q, titles.get(q, ""), r) for e, c, q, r in assignments)
    print(f"Assigned {len(assignments)} era reward bags without replacing bespoke rewards.")


if __name__ == "__main__":
    main()
