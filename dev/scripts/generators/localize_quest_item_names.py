"""Replace registry identifiers in FTB Quests prose with localized display names.

Quest/task SNBT is deliberately untouched. This edits only the English language
file, preserving exact registry IDs in machine-readable objective data.
"""

from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LANG = ROOT / "config" / "ftbquests" / "quests" / "lang" / "en_us.snbt"
ID_RE = re.compile(r"(?<![A-Za-z0-9_.-])([a-z0-9_.-]+):([a-z0-9_./-]*[a-z0-9_/-])")


def title_case(path: str) -> str:
    special = {
        "ae2": "AE2",
        "me": "ME",
        "qpu": "QPU",
        "xp": "XP",
        "tfmg": "TFMG",
        "mv": "MV",
        "hv": "HV",
        "lv": "LV",
    }
    words = path.rsplit("/", 1)[-1].split("_")
    return " ".join(special.get(word, word.capitalize()) for word in words)


def load_names() -> dict[str, str]:
    names: dict[str, str] = {}
    for jar in sorted((ROOT / "mods").glob("*.jar")):
        try:
            with zipfile.ZipFile(jar) as archive:
                entries = [n for n in archive.namelist() if re.fullmatch(r"assets/[^/]+/lang/en_us\.json", n)]
                for entry in entries:
                    try:
                        data = json.loads(archive.read(entry).decode("utf-8-sig"))
                    except (UnicodeDecodeError, json.JSONDecodeError):
                        continue
                    for key, value in data.items():
                        match = re.fullmatch(r"(?:item|block)\.([a-z0-9_.-]+)\.([a-z0-9_./-]+)", key)
                        if match and isinstance(value, str) and "%" not in value:
                            names.setdefault(f"{match.group(1)}:{match.group(2)}", value)
        except (OSError, zipfile.BadZipFile):
            continue
    return names


def main() -> None:
    names = load_names()
    text = LANG.read_text(encoding="utf-8")
    replacements: dict[str, str] = {}
    output: list[str] = []

    for line in text.splitlines(keepends=True):
        # Protect localization keys on keyed lines; only rewrite their values.
        split = line.find(": ")
        protected = line[: split + 2] if split >= 0 else ""
        prose = line[split + 2 :] if split >= 0 else line

        def replace(match: re.Match[str]) -> str:
            registry_id = match.group(0)
            display = names.get(registry_id, title_case(match.group(2)))
            replacements[registry_id] = display
            return display

        output.append(protected + ID_RE.sub(replace, prose))

    LANG.write_text("".join(output), encoding="utf-8", newline="\n")
    print(f"Localized {len(replacements)} distinct registry IDs in quest prose.")
    for registry_id, display in sorted(replacements.items()):
        print(f"  {registry_id} -> {display}")


if __name__ == "__main__":
    main()
