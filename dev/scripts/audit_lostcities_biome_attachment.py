#!/usr/bin/env python3
"""Guard the Lost Cities -> biome attachment.

THE BUG CLASS. Lost Cities injects its generator with a NeoForge biome modifier
gated on ``#minecraft:is_overworld`` (data/lostcities/neoforge/biome_modifier/
lostcities.json, step raw_generation). Vanilla's ``is_overworld`` tag lists only
vanilla biomes, and neither the Wastelands mods nor this pack add their biomes to
it. The Infinite Domain overworld is almost entirely ``wastelands:apocalypse``
and friends, so Lost Cities' feature was never attached to the biomes the world
actually generates and **no city ever generated anywhere**, despite a complete
custom profile, worldstyle, city styles, highway parts and a bespoke highway
compat mod all being in place.

This is the same failure mode already documented for EnviroMine's gas pockets in
dev/docs/ENVIRONMENTAL_SURVIVAL_ENGINEERING.md. Any mod that gates a biome
modifier on ``#minecraft:is_overworld`` is inert in this pack until its biomes
are named explicitly.

The fix is kubejs/data/infinite_domain/neoforge/biome_modifier/
lostcities_cities.json, attaching ``lostcities:lostcities`` to
``#infinite_domain:lostcities_city_biomes``.

This audit fails if a modded overworld biome in the live world preset is neither
in that tag nor in the explicit exclusion list below -- i.e. it catches a newly
added biome silently losing city generation.

    python dev/scripts/audit_lostcities_biome_attachment.py
"""
from __future__ import annotations

import json
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

# The preset new worlds actually use (the normal.json override). The wastelands
# preset is checked too so the two cannot silently diverge.
PRESETS = [
    os.path.join(REPO, "kubejs", "data", "minecraft", "worldgen", "world_preset", "normal.json"),
    os.path.join(REPO, "kubejs", "data", "wastelands", "worldgen", "world_preset", "wasteland.json"),
]
CITY_TAG = os.path.join(REPO, "kubejs", "data", "infinite_domain", "tags", "worldgen",
                        "biome", "lostcities_city_biomes.json")
MODIFIER = os.path.join(REPO, "kubejs", "data", "infinite_domain", "neoforge",
                        "biome_modifier", "lostcities_cities.json")

# Modded overworld biomes that must NOT receive the Lost Cities feature, and why.
# Anything modded in a preset that is neither here nor in the tag is a finding.
DELIBERATE_EXCLUSIONS = {
    "infinite_domain:safe_zone":
        "protected ~128-diameter spawn disc; a city here would overwrite the start area",
    "infinite_domain:western_continental_slope": "ocean floor",
    "infinite_domain:eastern_continental_slope": "ocean floor",
    "infinite_domain:western_abyssal_plain": "ocean floor",
    "infinite_domain:eastern_abyssal_plain": "ocean floor",
    "infinite_domain:western_fracture_field": "ocean floor",
    "infinite_domain:eastern_fracture_field": "ocean floor",
    "infinite_domain:western_hadal_trench": "ocean floor",
    "infinite_domain:eastern_hadal_trench": "ocean floor",
}


def preset_overworld_biomes(path: str) -> tuple[str, list[str]]:
    data = json.load(open(path, encoding="utf-8"))
    src = data["dimensions"]["minecraft:overworld"]["generator"]["biome_source"]
    biomes: list[str] = []
    fallback = src.get("fallback")
    if fallback:
        biomes.append(fallback)
    for rule in src.get("rules", []):
        b = rule.get("biome")
        if b and b not in biomes:
            biomes.append(b)
    return fallback, biomes


def main() -> int:
    findings: list[str] = []

    for path, label in ((CITY_TAG, "city biome tag"), (MODIFIER, "biome modifier")):
        if not os.path.exists(path):
            findings.append("missing %s: %s" % (label, os.path.relpath(path, REPO)))
    if findings:
        for f in findings:
            print("  ! %s" % f, file=sys.stderr)
        return 1

    mod = json.load(open(MODIFIER, encoding="utf-8"))
    if mod.get("type") != "neoforge:add_features":
        findings.append("modifier type is %r, expected neoforge:add_features" % mod.get("type"))
    if mod.get("features") != "lostcities:lostcities":
        findings.append("modifier features is %r, expected lostcities:lostcities"
                        % mod.get("features"))
    if mod.get("step") != "raw_generation":
        findings.append("modifier step is %r; Lost Cities' own modifier uses raw_generation"
                        % mod.get("step"))
    if mod.get("biomes") != "#infinite_domain:lostcities_city_biomes":
        findings.append("modifier biomes is %r, expected #infinite_domain:lostcities_city_biomes"
                        % mod.get("biomes"))

    tagged = set(json.load(open(CITY_TAG, encoding="utf-8"))["values"])

    for preset in PRESETS:
        if not os.path.exists(preset):
            findings.append("preset missing: %s" % os.path.relpath(preset, REPO))
            continue
        fallback, biomes = preset_overworld_biomes(preset)
        rel = os.path.relpath(preset, REPO)
        modded = [b for b in biomes if not b.startswith("minecraft:")]
        for b in modded:
            if b in tagged or b in DELIBERATE_EXCLUSIONS:
                continue
            findings.append(
                "%s: modded overworld biome %s is in neither "
                "#infinite_domain:lostcities_city_biomes nor the exclusion list -- "
                "Lost Cities will not generate there" % (rel, b))
        if fallback and fallback not in tagged and fallback not in DELIBERATE_EXCLUSIONS:
            findings.append(
                "%s: the biome-source FALLBACK %s is not attached; that is the bulk of the "
                "overworld and would produce zero cities" % (rel, fallback))

    for b in sorted(tagged):
        if b in DELIBERATE_EXCLUSIONS:
            findings.append("%s is both tagged for cities and listed as a deliberate exclusion"
                            % b)

    print("Lost Cities attachment: %d biomes tagged, %d deliberate exclusions, %d findings"
          % (len(tagged), len(DELIBERATE_EXCLUSIONS), len(findings)))
    for f in findings:
        print("  ! %s" % f, file=sys.stderr)
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
