"""Validate threat coverage and progression boundaries for the combined dossier."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
CHAPTER = ROOT / "config/ftbquests/quests/chapters/mutant_and_mekanite_threat_dossier.snbt"
ITEMS = set((ROOT / "dev/docs/registry-inventory/item-ids.txt").read_text(encoding="utf-8").splitlines())
text = CHAPTER.read_text(encoding="utf-8")

mutants = {
    "mutantmonsters:mutant_zombie", "mutantmonsters:mutant_skeleton",
    "mutantmonsters:mutant_creeper", "mutantmonsters:mutant_enderman",
    "mutantmonsters:mutant_snow_golem", "mutantmonsters:spider_pig",
}
mekanites = {
    "mekanite_mobs:drone", "mekanite_mobs:mekanite_creeper", "mekanite_mobs:mekanite_enderman",
    "mekanite_mobs:mekanite_illusioner", "mekanite_mobs:mekanite_ravager",
    "mekanite_mobs:mekanite_skeleton", "mekanite_mobs:mekanite_slime",
    "mekanite_mobs:mekanite_slime_medio", "mekanite_mobs:mekanite_slime_small",
    "mekanite_mobs:mekanite_spider", "mekanite_mobs:mekanite_vindicator",
    "mekanite_mobs:mekanite_witch", "mekanite_mobs:mekanite_zombie",
    "mekanite_mobs:mekanite_zombie_drowned", "mekanite_mobs:mekanite_zombie_husk",
}
entities = set(re.findall(r'entity: "([^"]+)"', text))
missing = (mutants | mekanites) - entities
if missing:
    raise SystemExit("Missing kill coverage: " + ", ".join(sorted(missing)))

icons = re.findall(r'\n\s*icon: "([^"]+)"', text)
bad_icons = sorted(set(icons) - ITEMS)
if bad_icons:
    raise SystemExit("Invalid icons: " + ", ".join(bad_icons))

# The first mutant quest must be immediately visible; Mekanite roots must be Era 8 plus geography gated.
first = text.split('\n\t\t{', 2)[1]
if "dependencies:" in first:
    raise SystemExit("Mutant entry quest is not always accessible")
for required in ("5810000000000001", "5D0000000000000F", "5D00000000000015", "5D00000000000013"):
    if required not in text:
        raise SystemExit(f"Missing Mekanite gate {required}")

quest_count = len(re.findall(r'^\s*id: "5F20', text, re.MULTILINE))
kill_count = len(re.findall(r'type: "kill"', text))
print(f"Audit passed: {quest_count} quests, {kill_count} kill objectives, "
      f"{len(mutants)} mutant types, and {len(mekanites)} Mekanite types covered.")
