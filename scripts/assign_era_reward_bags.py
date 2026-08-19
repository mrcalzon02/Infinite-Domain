"""Assign era bags to a restrained selection of optional technical lessons."""

from __future__ import annotations

import csv
import hashlib
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = ROOT / "config/ftbquests/quests/chapters"
LANG = ROOT / "config/ftbquests/quests/lang/en_us.snbt"
REPORT = ROOT / "docs/era-reward-bags/reward-assignments.csv"
FORCED_COMMON = {
    # The refinery output bank is the explicit Era 3 multiblock lesson and
    # should demonstrate the common-bag convention even between cadence slots.
    3: {"4310000000000002"},
}


def reward_id(quest_id: str) -> str:
    # 0x6A keeps the signed long positive; the digest makes collisions negligible.
    return "6A" + hashlib.sha256(("era-bag:" + quest_id).encode()).hexdigest()[:14].upper()


def main() -> None:
    lang = LANG.read_text(encoding="utf-8-sig")
    titles = dict(re.findall(r'quest\.([0-9A-F]+)\.title:\s*"([^"]+)"', lang))
    assignments: list[tuple[int, str, str, str, str]] = []

    for era in range(1, 9):
        path = next(CHAPTERS.glob(f"era_0{era}_*.snbt"))
        lines = path.read_text(encoding="utf-8").splitlines()
        starts = [i for i, line in enumerate(lines) if line == "\t\t{"]
        blocks: list[tuple[int, int, str]] = []
        for number, start in enumerate(starts):
            end = starts[number + 1] if number + 1 < len(starts) else len(lines)
            blocks.append((start, end, "\n".join(lines[start:end])))

        # Bespoke reward quests are excluded. Previously bagged quests remain in
        # the candidate sequence, making repeated runs stable and idempotent.
        candidates = [
            block for block in blocks
            if 'shape: "gear"' in block[2]
            and 'type: "checkmark"' not in block[2]
            and ('rewards:' not in block[2] or f'kubejs:era{era}_' in block[2])
        ]
        selected = {i for i in range(len(candidates)) if (i + 1) % 3 == 0}
        selected.update(
            i for i, (_, _, block) in enumerate(candidates)
            if any(qid in block for qid in FORCED_COMMON.get(era, set()))
        )
        if candidates:
            selected.add(len(candidates) - 1)

        insertions: list[tuple[int, list[str]]] = []
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
                assignments.append((era, path.name, qid, titles.get(qid, ""), bag))
                continue
            shape_line = next(i for i in range(start, end) if lines[i].startswith("\t\t\tshape:"))
            rid = reward_id(qid)
            reward_lines = [
                "\t\t\trewards: [{", f'\t\t\t\tid: "{rid}"',
                f'\t\t\t\titem: {{ count: 1, id: "{bag}" }}',
                "\t\t\t\ttype: \"item\"", "\t\t\t}]",
            ]
            insertions.append((shape_line, reward_lines))
            assignments.append((era, path.name, qid, titles.get(qid, ""), bag))

        for line_index, new_lines in reversed(insertions):
            lines[line_index:line_index] = new_lines
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    with REPORT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["era", "chapter", "quest_id", "quest_title", "reward_item"])
        writer.writerows(assignments)
    print(f"Assigned {len(assignments)} era reward bags without replacing bespoke rewards.")


if __name__ == "__main__":
    main()
