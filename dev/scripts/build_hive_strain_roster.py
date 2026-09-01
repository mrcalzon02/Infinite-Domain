"""Generate docs/hive-strain/roster-manifest.json for the Hive World Verdant Strain.

Authority: docs/HIVE_WORLD_VERDANT_STRAIN.md (section 4).

Deterministic and idempotent: same repository state -> byte-identical output.
No runtime, no network, no RNG. Reads only:

  - docs/registry-inventory/entity-ids.txt   (the 79 spore: entity ids - ground truth)
  - config/spore-startup.toml, config/spore-common.toml   (base max-health values)
  - mods/spore_*.jar                          (entity texture index)

The band taxonomy mirrors kubejs/server_scripts/spore_analysis_samples.js.
"""

from __future__ import annotations

import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENTITY_IDS = ROOT / "docs" / "registry-inventory" / "entity-ids.txt"
TOML_FILES = [
    ROOT / "config" / "spore-startup.toml",
    ROOT / "config" / "spore-common.toml",
]
OUT = ROOT / "docs" / "hive-strain" / "roster-manifest.json"
TEXTURE_ROOT = "assets/spore/textures/entity/"

# --------------------------------------------------------------------------- #
# Exclusion patterns: projectiles, thrown objects, detached body-parts, and
# pure FX entities never receive a Verdant Strain variant. Kept as an explicit
# list so scripts/validate_hive_strain_assets.py can re-check it (check 2).
# --------------------------------------------------------------------------- #
EXCLUDE_EXACT = {
    "spore:acid",           # fluid entity
    "spore:acid_ball",
    "spore:bile",
    "spore:harpoon",
    "spore:spit",
    "spore:wave",
    "spore:illusion",
    "spore:corpse_piece",
    "spore:arena_tendril",
    "spore:tumoroid_nuke",
    "spore:hevoker_arm",
    "spore:howit_arm",
    "spore:verfall_head",
    "spore:sieger_tail",
    "spore:hohlfresser_seg",
    "spore:leviathan_seg",
    "spore:thrown_spear",
    "spore:thrown_tool",
    "spore:thrown_tumor",
}
EXCLUDE_SUFFIX = ("_arm", "_head", "_seg", "_tail", "_round")
EXCLUDE_PREFIX = ("thrown_",)

# --------------------------------------------------------------------------- #
# Band taxonomy - transcribed from spore_analysis_samples.js. An id not listed
# here lands in "unclassified" and is flagged for manual review in the spec.
# --------------------------------------------------------------------------- #
BANDS: dict[str, list[str]] = {
    "infected": [
        "inf_human", "inf_husk", "inf_drowned", "inf_villager", "inf_diseased_villager",
        "inf_wanderer", "inf_witch", "inf_pillager", "inf_vindicator", "inf_evoker",
        "inf_hazmat", "inf_player",
    ],
    "evolved": [
        "knight", "griefer", "braiomil", "busser", "thorn", "jagd", "scavenger",
        "bloater", "naiad", "leaper", "slasher", "spitter", "volatile", "mephitic",
        "gorgon", "howler", "stalker", "brute", "nuclea", "protector", "gargoyle",
        "conductor", "chemist", "inebriater", "bairn", "saugling", "scamper",
        "plagued", "lacerator", "biobloob", "nuckelave", "claw", "licker",
    ],
    "hyper_evolved": [
        "inquisitor", "brot", "hollen", "grober", "wendigo", "ogre", "hvindicator",
        "hevoker", "axtwerfer", "hexenmeister", "brotkatze", "specter", "reaper",
        "vanguard", "inf_contruct",
    ],
    "organoid": [
        "mound", "umarmed", "usurper", "vigil", "braurei", "verva", "delusioner",
        "reconstructor", "hivetumor", "womb", "verwa", "scent",
    ],
    "calamity": [
        "sieger", "howitzer", "stahl", "hohlfresser", "gazenbreacher", "kraken",
        "leviathan", "hindenburg", "verfall", "graken", "gastgaber", "phayres",
    ],
    "hivemind": ["proto"],
}

# id stem -> config section display name (for max-health lookup). Only the
# confidently-resolved mappings; the rest are reported as "unresolved".
HEALTH_NAME = {
    "inf_human": "Infected Human", "inf_husk": "Infected Husk",
    "inf_drowned": "Infected Drowned", "inf_villager": "Infected Villager",
    "inf_pillager": "Infected Pillager", "inf_wanderer": "Infected Wandering Trader",
    "inf_witch": "Infected Witch", "inf_evoker": "Infected Evoker",
    "inf_vindicator": "Infected Vindicator", "inf_hazmat": "Infected Hazmat",
    "inf_player": "Infected Player", "inf_contruct": "Infested Construct",
    "claw": "Infected Claw", "scamper": "Scamper", "mephitic": "Mephetic",
    "knight": "Knight", "griefer": "Griefer", "braiomil": "Braiomil",
    "bloater": "Bloater", "naiad": "Naiad", "leaper": "Leaper", "slasher": "Slasher",
    "spitter": "Spiter", "volatile": "Volatile", "gorgon": "Gorgon",
    "howler": "Howler", "stalker": "Stalker", "brute": "Brute",
    "protector": "Protector", "gargoyle": "Gargoyle", "conductor": "Conductor",
    "chemist": "Chemist", "inebriater": "Inebrieter", "bairn": "Bairn",
    "saugling": "Saugling", "scavenger": "Scavenger", "jagd": "Jagdhund",
    "thorn": "Vervathorn", "nuckelave": "Nuckelave", "plagued": "Plagued",
    "lacerator": "Lacerator", "biobloob": "Bioblob", "phayres": "Phayres",
    "inquisitor": "Inquisitor", "wendigo": "Wendigo", "ogre": "Ogre",
    "grober": "Groberfub", "axtwerfer": "Axtwerfer", "hexenmeister": "Hexenmeister",
    "brotkatze": "Brotkatze", "hollen": "Hollenhound", "specter": "Specter",
    "reaper": "Reaper", "vanguard": "Vanguard",
    "mound": "Mound", "umarmed": "Umarmer", "usurper": "Usurper", "vigil": "Vigil",
    "braurei": "Braurei", "delusioner": "Delusioner", "hivetumor": "Hivetumor",
    "womb": "Womb", "verva": "Verwahrung", "verwa": "Verwahrung",
    "sieger": "Sieger", "howitzer": "Howitzer", "stahl": "Stahlmorder",
    "hohlfresser": "Hohlfresser", "gazenbreacher": "Gazenbreacher",
    "leviathan": "Leviathan", "hindenburg": "Hindenburg", "verfall": "Verfalldrache",
    "graken": "Grakensenker", "gastgaber": "Gastgeber",
    "proto": "Proto",
}


def load_spore_ids() -> list[str]:
    ids = []
    for line in ENTITY_IDS.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s.startswith("spore:"):
            ids.append(s)
    return sorted(set(ids))


def is_excluded(entity_id: str) -> bool:
    stem = entity_id.split(":", 1)[1]
    if entity_id in EXCLUDE_EXACT:
        return True
    if stem.startswith(EXCLUDE_PREFIX):
        return True
    if stem.endswith(EXCLUDE_SUFFIX):
        return True
    return False


def parse_health() -> dict[str, float]:
    """display-name -> max health, scraped from the spore TOML config."""
    out: dict[str, float] = {}
    # "[Sets ]<Name> Max health" = N   and   "Sets the base health of the <Name>" = N
    generic = re.compile(r'"(?:Sets )?([A-Za-z .]+?) Max health"\s*=\s*([0-9]+(?:\.[0-9]+)?)')
    base_of = re.compile(r'"Sets the base health of the ([A-Za-z]+)"\s*=\s*([0-9]+(?:\.[0-9]+)?)')
    for toml in TOML_FILES:
        if not toml.exists():
            continue
        text = toml.read_text(encoding="utf-8")
        for m in generic.finditer(text):
            out.setdefault(m.group(1).strip(), float(m.group(2)))
        for m in base_of.finditer(text):
            out.setdefault(m.group(1).strip(), float(m.group(2)))
    return out


def index_textures() -> list[str]:
    jars = sorted(ROOT.glob("mods/spore_*.jar"))
    if not jars:
        sys.exit("no mods/spore_*.jar found")
    with zipfile.ZipFile(jars[-1]) as z:
        return sorted(
            n[len(TEXTURE_ROOT):]
            for n in z.namelist()
            if n.startswith(TEXTURE_ROOT) and n.endswith(".png")
        )


TEXTURE_ALIAS = {
    "inf_husk": "husk", "inf_pillager": "pillager", "inf_witch": "inf_witch",
    "inf_evoker": "inf_evoker", "inf_vindicator": "inf_vindicator",
    "inf_wanderer": "inf_wanderer", "inf_hazmat": "inf_hazmat", "inf_player": "inf_player",
    "inf_contruct": "broken_construct",
    "braiomil": "baio", "thorn": "vervathorn", "gazenbreacher": "gazen",
    "hohlfresser": "hohl", "umarmed": "umarmer", "hvindicator": "hindicator",
    "hevoker": "hyper_evoker", "verfall": "verfalldrache", "stahl": "stahlmorder",
    "jagd": "jagdhund", "hollen": "hollenhund", "scent": "incandescent",
    "graken": "grakensenker",
}


def match_textures(stem: str, all_textures: list[str]) -> list[str]:
    """Best-effort primary/variant textures whose *basename* equals the id stem,
    starts with it, or matches a known alias. The recolour pass in
    scripts/generate_hive_strain_textures.py covers every entity texture
    regardless of what this maps - this list is only for the spec roster table."""
    needles = {stem}
    if stem in TEXTURE_ALIAS:
        needles.add(TEXTURE_ALIAS[stem])

    def hit(path: str) -> bool:
        base = path.rsplit("/", 1)[-1][:-4].lower()  # strip dir + ".png"
        return any(base == n or base.startswith(n + "_") for n in needles)

    return sorted(t for t in all_textures if hit(t))


def display_name(stem: str) -> str:
    return HEALTH_NAME.get(stem, stem.replace("_", " ").title())


def main() -> None:
    spore_ids = load_spore_ids()
    health = parse_health()
    textures = index_textures()

    stem_to_band = {}
    for band, members in BANDS.items():
        for stem in members:
            stem_to_band[stem] = band

    included, excluded = [], []
    for entity_id in spore_ids:
        stem = entity_id.split(":", 1)[1]
        if is_excluded(entity_id):
            excluded.append(entity_id)
            continue
        band = stem_to_band.get(stem, "unclassified")
        cfg_name = HEALTH_NAME.get(stem)
        base_hp = health.get(cfg_name) if cfg_name else None
        record = {
            "id": entity_id,
            "band": band,
            "display_name": display_name(stem),
            "base_health": base_hp,
            "tripled_health": round(base_hp * 3.0, 2) if base_hp is not None else None,
            "health_source": f"config:{cfg_name}" if base_hp is not None else "unresolved",
            "textures": match_textures(stem, textures),
            "reskin": True,
        }
        included.append(record)

    included.sort(key=lambda r: (list(BANDS).index(r["band"]) if r["band"] in BANDS else 99, r["id"]))

    manifest = {
        "$schema_note": "Generated by scripts/build_hive_strain_roster.py. Do not hand-edit. Authority: docs/HIVE_WORLD_VERDANT_STRAIN.md.",
        "version": "verdant-strain-roster-v1",
        "working_name": "Verdant Strain",
        "dimension": "infinite_domain:hive_world",
        "hit_point_multiplier": 3.0,
        "source_jar": sorted(p.name for p in ROOT.glob("mods/spore_*.jar"))[-1],
        "entity_texture_count": len(textures),
        "counts": {
            "spore_entity_ids": len(spore_ids),
            "included_creatures": len(included),
            "excluded_non_creatures": len(excluded),
            "unresolved_health": sum(1 for r in included if r["health_source"] == "unresolved"),
            "unclassified_band": sum(1 for r in included if r["band"] == "unclassified"),
        },
        "band_taxonomy_source": "kubejs/server_scripts/spore_analysis_samples.js",
        "excluded_non_creatures": sorted(excluded),
        "roster": included,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")
    print(f"  {len(included)} creatures, {len(excluded)} excluded, "
          f"{manifest['counts']['unresolved_health']} unresolved health, "
          f"{manifest['counts']['unclassified_band']} unclassified band")


if __name__ == "__main__":
    main()
