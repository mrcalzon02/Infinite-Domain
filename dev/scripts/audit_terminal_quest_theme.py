from __future__ import annotations

import re
import struct
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
THEME = ROOT / "kubejs/assets/ftbquests/ftb_quests_theme.txt"
BACKGROUND = ROOT / "kubejs/assets/infinite_domain/textures/gui/quests/terminal_background.png"
PROLOGUE = ROOT / "config/ftbquests/quests/chapters/another_lost_soul.snbt"
LANG = ROOT / "config/ftbquests/quests/lang/en_us.snbt"
FTBQ_JAR = next((ROOT / "mods").glob("ftb-quests-*.jar"))
SEMANTIC_CHAPTERS = {
    "the_rot_spore_threat_dossier.snbt": "terminal_critical",
    "mutant_and_mekanite_threat_dossier.snbt": "terminal_warning",
    "darknet_draconic_convergence.snbt": "terminal_classified",
}
GENERATOR_SUBTITLE_OWNERS = {
    "generate_mastery_quests.js": "masterySubtitles",
    "build_spore_threat_quests.py": "chapter.5F0A5E0000000002.subtitle",
    "build_mutant_mekanite_threat_quests.py": ".subtitle:",
    "build_cyberspace_darknet_campaign.py": ".subtitle:",
    "build_quest_expansion.js": "chapter.2DFAD86142B7D28D.subtitle",
}
GENERATOR_CHAPTER_ICON_OWNERS = {
    "generate_eras_2_8.js": '\\ticon: "${data.icon}"',
    "generate_mastery_quests.js": '\\ticon: "${data.icon}"',
    "build_quest_expansion.js": '\\ticon: "${ch.icon}"',
    "build_spore_threat_quests.py": '\\ticon: \\"spore:gas_mask\\"',
    "build_mutant_mekanite_threat_quests.py": 'icon: "mutantmonsters:hulk_hammer"',
    "build_cyberspace_darknet_campaign.py": 'icon: "cyberspace:netcracker"',
    "build_coffee_tea_quests.py": 'icon: "kubejs:coffee_cherries"',
    "build_industrial_food_quests.py": 'icon: "farmersdelight:cooking_pot"',
    "generate_stellaris_space_industry.py": 'icon: \\"infinite_domain_space:emergency_helmet\\"',
}

GUIDE_QUESTS = [f"6F010000000000{number:02X}" for number in range(0x20, 0x27)]
GUIDE_TASKS = [f"6F020000000000{number:02X}" for number in range(0x20, 0x27)]
EXPECTED_ICONS = {
    "6F01000000000020": "ftbquests:book",
    "6F01000000000021": "ftbquests:screen_3",
    "6F01000000000022": "ftbquests:task_screen_configurator",
    "6F01000000000023": "ftbquests:detector",
    "6F01000000000024": "ftbquests:barrier",
    "6F01000000000025": "ftbquests:loot_crate_opener",
    "6F01000000000026": "ftbquests:screen_1",
}


def quest_block(source: str, quest_id: str) -> str:
    marker = f'\n\t\t\tid: "{quest_id}"'
    position = source.find(marker)
    if position < 0:
        return ""
    start = source.rfind("\n\t\t{", 0, position)
    end = source.find("\n\t\t}", position)
    return source[start : end + 4] if start >= 0 and end >= 0 else ""


theme = THEME.read_text(encoding="utf-8")
prologue = PROLOGUE.read_text(encoding="utf-8")
language = LANG.read_text(encoding="utf-8")
failures: list[str] = []

chapter_titles = set(
    re.findall(r"^\s*chapter\.([0-9A-F]{16})\.title:", language, flags=re.MULTILINE)
)
chapter_subtitles = set(
    re.findall(r"^\s*chapter\.([0-9A-F]{16})\.subtitle:", language, flags=re.MULTILINE)
)
missing_subtitles = sorted(chapter_titles - chapter_subtitles)
if missing_subtitles:
    failures.append(
        "chapter subtitles missing: " + ", ".join(missing_subtitles)
    )

for filename, semantic_tag in SEMANTIC_CHAPTERS.items():
    source = (PROLOGUE.parent / filename).read_text(encoding="utf-8")
    quest_count = len(re.findall(r'^\t\t\tid:\s*"[0-9A-F]{16}"', source, flags=re.MULTILINE))
    tag_count = source.count(f'tags: ["{semantic_tag}"]')
    if quest_count == 0 or tag_count != quest_count:
        failures.append(
            f"semantic quest styling incomplete in {filename}: "
            f"{tag_count}/{quest_count} use {semantic_tag}"
        )

for filename, ownership_token in GENERATOR_SUBTITLE_OWNERS.items():
    generator = (ROOT / "scripts" / filename).read_text(encoding="utf-8")
    if ownership_token not in generator:
        failures.append(f"chapter subtitle is not generator-owned: {filename}")

chapter_files = sorted(PROLOGUE.parent.glob("*.snbt"))
for chapter_file in chapter_files:
    source = chapter_file.read_text(encoding="utf-8")
    if not re.search(r'^\ticon:\s*"[^"]+"', source, flags=re.MULTILINE):
        failures.append(f"chapter would use animated quest-icon fallback: {chapter_file.name}")

for filename, ownership_token in GENERATOR_CHAPTER_ICON_OWNERS.items():
    generator = (ROOT / "scripts" / filename).read_text(encoding="utf-8")
    if ownership_token not in generator:
        failures.append(f"fixed chapter icon is not generator-owned: {filename}")

required_theme_tokens = [
    "[*]",
    "background: infinite_domain:textures/gui/quests/terminal_background.png",
    "text_color: #67F58A",
    "chapter_panel_background:",
    "quest_view_background:",
    "dependency_line_completed_color:",
    "dependency_line_uncompleted_color:",
    "checkmark_task_active:",
    "[#terminal_warning]",
    "[#terminal_critical]",
    "[#terminal_classified]",
]
for token in required_theme_tokens:
    if token not in theme:
        failures.append(f"theme token missing: {token}")

if not BACKGROUND.is_file():
    failures.append("terminal background texture missing")
else:
    data = BACKGROUND.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        failures.append("terminal background is not a PNG")
    elif len(data) < 24:
        failures.append("terminal background PNG is truncated")
    else:
        width, height = struct.unpack(">II", data[16:24])
        if width < 512 or height < 512:
            failures.append(f"terminal background too small: {width}x{height}")

if 'autofocus_id: "7D194089522507AB"' not in prologue:
    failures.append("Prologue autofocus is not the first quest")

for index, (quest_id, task_id) in enumerate(zip(GUIDE_QUESTS, GUIDE_TASKS)):
    block = quest_block(prologue, quest_id)
    if not block:
        failures.append(f"guide quest missing: {quest_id}")
        continue
    if 'optional: true' not in block:
        failures.append(f"guide quest is not optional: {quest_id}")
    if f'icon: "{EXPECTED_ICONS[quest_id]}"' not in block:
        failures.append(f"guide quest icon mismatch: {quest_id}")
    if f'id: "{task_id}"' not in block:
        failures.append(f"guide task missing: {task_id}")
    for suffix in ("title", "quest_desc"):
        if f"quest.{quest_id}.{suffix}:" not in language:
            failures.append(f"guide localization missing: quest.{quest_id}.{suffix}")
    if f"task.{task_id}.title:" not in language:
        failures.append(f"guide task localization missing: {task_id}")
    if index == 0 and 'dependencies: ["6002100000000002"]' not in block:
        failures.append("terminal guide does not branch from the Prologue interface lesson")

final_block = quest_block(prologue, GUIDE_QUESTS[-1])
for token in (
    'item: { count: 1, id: "ftbquests:screen_1" }',
    'id: "ftbquests:task_screen_configurator"',
    '"6F01000000000023"',
    '"6F01000000000024"',
    '"6F01000000000025"',
):
    if token not in final_block:
        failures.append(f"field installation convergence missing: {token}")

required_guide_language = [
    "1×1, 3×3, 5×5, and 7×7",
    "Task Screen Configurator",
    "redstone output",
    "Quest Barriers",
    "Stage Barriers",
    "Loot Crate Opener",
    "permissions",
]
for token in required_guide_language:
    if token not in language:
        failures.append(f"hardware guide coverage missing: {token}")

with zipfile.ZipFile(FTBQ_JAR) as jar:
    names = set(jar.namelist())
for item_id in set(EXPECTED_ICONS.values()):
    namespace, path = item_id.split(":", 1)
    if namespace == "ftbquests" and f"assets/ftbquests/models/item/{path}.json" not in names:
        failures.append(f"guide icon has no packaged item model: {item_id}")

duplicate_ids = [
    quest_id
    for quest_id in GUIDE_QUESTS + GUIDE_TASKS
    if len(re.findall(rf'\bid:\s*"{quest_id}"', prologue)) != 1
]
if duplicate_ids:
    failures.append("duplicate or missing guide IDs: " + ", ".join(duplicate_ids))

if failures:
    for failure in failures:
        print(f"FAIL: {failure}")
    raise SystemExit(1)

print(
    f"Terminal quest theme audit passed: global terminal shell, 3 semantic alert selectors, "
    f"{len(chapter_titles)} chapter subtitles and {len(chapter_files)} fixed chapter icons, "
    "7 optional Prologue hardware records, "
    "7 explicit icons, three fully tagged threat dossiers, and the field-terminal convergence resolve."
)
