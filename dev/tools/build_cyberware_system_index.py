from __future__ import annotations

import csv
import json
import re
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
JAR = ROOT / "mods" / "createcybernetics-0.5.1-neoforge-1.21.1-HOTFIX.jar"
JAVAP = ROOT / "tmp" / "moditems-javap.txt"
OUT = ROOT / "docs" / "cyberware-index" / "create-cybernetics-current-index.csv"
MARKDOWN_OUT = ROOT / "docs" / "CURRENT_CYBERWARE_INDEX.md"

PREFIX_TO_SLOT = {
    "basecyberware_rightleg": "Right leg",
    "basecyberware_leftleg": "Left leg",
    "basecyberware_rightarm": "Right arm",
    "basecyberware_leftarm": "Left arm",
    "basecyberware_cybereyes": "Eyes",
    "basecyberware_linearframe": "Bone",
    "eyeupgrades_": "Eyes",
    "armupgrades_": "Either arm",
    "legupgrades_": "Either leg",
    "boneupgrades_": "Bone",
    "brainupgrades_": "Brain",
    "heartupgrades_": "Heart",
    "lungsupgrades_": "Lungs",
    "organsupgrade": "Organs",
    "skinupgrades_": "Skin",
    "muscleupgrades_": "Muscle",
}

WETWARE_SLOTS = {
    "wetware_blubber": "Skin",
    "wetware_firebreathinglungs": "Lungs",
    "wetware_waterbreathinglungs": "Lungs",
    "wetware_guardianeye": "Eyes",
    "wetware_polarbearfur": "Skin",
    "wetware_ravagertendons": "Muscle",
    "wetware_sculklungs": "Lungs",
    "wetware_tacticalinksac": "Organs",
    "wetware_aerostasisgyrobladder": "Organs",
    "wetware_grassfedstomach": "Organs",
    "wetware_webshootingintestines": "Organs",
    "wetware_webshooting_leftarm": "Left arm",
    "wetware_webshooting_rightarm": "Right arm",
    "wetware_spidereyes": "Eyes",
    "wetware_blastemaskeleton": "Bone",
    "wetware_dragonskin": "Skin",
    "wetware_wardenantlers": "Brain",
    "wetware_sculkheart": "Heart",
    "wetware_gooeymuscle": "Muscle",
    "wetware_electrocytemuscle": "Muscle",
}

BODY_PART_SLOTS = {
    "bodypart_rightleg": "Right leg", "bodypart_leftleg": "Left leg",
    "bodypart_rightarm": "Right arm", "bodypart_leftarm": "Left arm",
    "bodypart_skeleton": "Bone", "bodypart_brain": "Brain", "bodypart_eyeballs": "Eyes",
    "bodypart_heart": "Heart", "bodypart_lungs": "Lungs", "bodypart_liver": "Organs",
    "bodypart_intestines": "Organs", "bodypart_muscle": "Muscle", "bodypart_skin": "Skin",
    "bodypart_guardianretina": "Eyes", "bodypart_wardenesophagus": "Lungs",
    "bodypart_gyroscopicbladder": "Organs", "bodypart_spinnerette": "Organs",
    "bodypart_firegland": "Organs", "bodypart_gills": "Lungs",
    "bodypart_axolotlmarrow": "Bone", "bodypart_dragonscale": "Skin",
    "bodypart_sculkrightleg": "Right leg", "bodypart_sculkleftleg": "Left leg",
    "bodypart_sculkrightarm": "Right arm", "bodypart_sculkleftarm": "Left arm",
    "bodypart_sculkbrain": "Brain", "bodypart_sculkliver": "Organs",
    "bodypart_sculkintestines": "Organs", "bodypart_sculkmuscle": "Muscle",
    "bodypart_sculkskin": "Skin",
}

HARVESTED_PRECURSORS = {
    "bodypart_guardianretina", "bodypart_wardenesophagus", "bodypart_gyroscopicbladder",
    "bodypart_spinnerette", "bodypart_firegland", "bodypart_gills", "bodypart_axolotlmarrow",
    "bodypart_dragonscale",
}

OPTIONAL_INTEGRATIONS = {
    "eyeupgrades_navigationchip": "JourneyMap",
    "boneupgrades_elytra": "Caelus",
    "brainupgrades_consciousnesstransmitter": "Respawn/continuity system",
    "brainupgrades_corticalstack": "Respawn/continuity system",
    "brainupgrades_spelljammer": "Iron's Spells 'n Spellbooks",
    "organsupgrades_manabattery": "Iron's Spells 'n Spellbooks",
    "skinupgrades_manaskin": "Iron's Spells 'n Spellbooks",
    "heartupgrades_anomaly": "Iron's Spells 'n Spellbooks",
    "skinupgrades_sweat": "Cold Sweat",
    "skinupgrades_ultraviolent": "Vampirism",
}


def clean(value: str) -> str:
    value = re.sub(r"§.", "", value)
    return " ".join(value.replace("\n", " / ").split())


def decode_int(op: str, arg: str | None) -> int | None:
    if op.startswith("iconst_"):
        suffix = op.removeprefix("iconst_")
        return -1 if suffix == "m1" else int(suffix)
    if op in {"bipush", "sipush"} and arg is not None:
        return int(arg)
    return None


def humanity_by_registry_id(text: str) -> dict[str, int]:
    # Registration uses InvokeDynamic #N; its supplier is lambda$static$(N-1).
    registration: dict[str, int] = {}
    lines = text.splitlines()
    for i, line in enumerate(lines):
        m = re.search(r"// String ([a-z0-9_]+)$", line)
        if not m:
            continue
        for following in lines[i + 1 : i + 4]:
            dyn = re.search(r"InvokeDynamic #(\d+):get", following)
            if dyn:
                registration[m.group(1)] = int(dyn.group(1)) - 1
                break

    methods: dict[int, int] = {}
    blocks = re.split(r"(?=  private static net\.minecraft\.world\.item\.Item lambda\$static\$\d+\(\);)", text)
    for block in blocks:
        head = re.match(r"  private static net\.minecraft\.world\.item\.Item lambda\$static\$(\d+)\(\);", block)
        if not head or "stacksTo:(I)" not in block:
            continue
        after_stack = block.split("stacksTo:(I)", 1)[1].split("areturn", 1)[0]
        for op, arg in re.findall(r"\d+:\s+(iconst_[a-z0-9]+|bipush|sipush)(?:\s+(-?\d+))?", after_stack):
            value = decode_int(op, arg or None)
            if value is not None:
                methods[int(head.group(1))] = value
                break
    return {item_id: methods[lambda_id] for item_id, lambda_id in registration.items() if lambda_id in methods}


def slot_for(item_id: str) -> str:
    if item_id in BODY_PART_SLOTS:
        return BODY_PART_SLOTS[item_id]
    if item_id in WETWARE_SLOTS:
        return WETWARE_SLOTS[item_id]
    for prefix, slot in PREFIX_TO_SLOT.items():
        if item_id.startswith(prefix):
            return slot
    return "Unverified"


def family_for(item_id: str) -> str:
    if item_id in HARVESTED_PRECURSORS:
        return "Harvested wetware precursor"
    if item_id.startswith("bodypart_"):
        return "Biological body part"
    if item_id.startswith("basecyberware_"):
        return "Base replacement"
    if item_id.startswith("wetware_"):
        return "Wetware"
    return "Cyberware upgrade"


def fallback_detail(item_id: str) -> str:
    if item_id.startswith("bodypart_sculk"):
        return "Sculk-altered surgical body part; biological replacement and wetware precursor; no separate localized active effect"
    if item_id.startswith("bodypart_") and item_id not in {
        "bodypart_rightleg", "bodypart_leftleg", "bodypart_rightarm", "bodypart_leftarm",
        "bodypart_skeleton", "bodypart_brain", "bodypart_eyeballs", "bodypart_heart",
        "bodypart_lungs", "bodypart_liver", "bodypart_intestines", "bodypart_muscle", "bodypart_skin",
    }:
        return "Harvested donor tissue used as a surgical/wetware precursor; no separate localized active effect"
    if item_id.startswith("bodypart_"):
        return "Baseline biological replacement; functions as the default organ/body part and repairs biologically"
    if "rightarm" in item_id or "leftarm" in item_id:
        return "Arm replacement and arm-upgrade prerequisite; 10 energy/tick; cyberlimb repair; 2,200 durability in its correct side"
    if "rightleg" in item_id or "leftleg" in item_id:
        return "Leg replacement and leg-upgrade prerequisite; 10 energy/tick; cyberlimb repair; 2,200 durability in its correct side"
    if item_id == "basecyberware_cybereyes":
        return "Eye replacement and cybereye-module prerequisite; 5 energy/tick; loss of powered vision when offline"
    if item_id == "basecyberware_linearframe":
        return "Skeleton replacement and frame-upgrade prerequisite; 10 energy/tick; weakness and slowness when offline"
    return "No dedicated localized effect text; verify from implementation"


def main() -> None:
    with zipfile.ZipFile(JAR) as jar:
        lang = json.loads(jar.read("assets/createcybernetics/lang/en_us.json"))

    humanity = humanity_by_registry_id(JAVAP.read_text(encoding="utf-8-sig"))
    item_pattern = re.compile(
        r"^item\.createcybernetics\."
        r"(basecyberware_|eyeupgrades_|armupgrades_|legupgrades_|boneupgrades_|brainupgrades_|"
        r"heartupgrades_|lungsupgrades_|organsupgrade|skinupgrades_|muscleupgrades_|wetware_|bodypart_)"
    )
    ids = []
    for key in lang:
        if not item_pattern.match(key) or "." in key.removeprefix("item.createcybernetics."):
            continue
        item_id = key.removeprefix("item.createcybernetics.")
        # Registry names, not generic category labels.
        if item_id.endswith("_tooltip"):
            continue
        ids.append(item_id)

    rows = []
    for item_id in sorted(set(ids), key=lambda x: (slot_for(x), x)):
        tooltip_prefix = f"tooltip.createcybernetics.{item_id}."
        detail = [clean(value) for key, value in lang.items() if key.startswith(tooltip_prefix)]
        # Mantis blade common details live under a shared prefix.
        if item_id.startswith("armupgrades_mantisblade_"):
            detail = [
                *[clean(value) for key, value in lang.items() if key.startswith("tooltip.createcybernetics.armupgrades_mantisblade.")],
                *detail,
            ]
        rows.append(
            {
                "registry_id": f"createcybernetics:{item_id}",
                "name": clean(lang[f"item.createcybernetics.{item_id}"]),
                "family": family_for(item_id),
                "slot": slot_for(item_id),
                "humanity_cost": humanity.get(item_id, "n/a" if item_id in HARVESTED_PRECURSORS else ""),
                "current_effect_and_constraints": " | ".join(dict.fromkeys(detail)) or fallback_detail(item_id),
                "optional_integration": OPTIONAL_INTEGRATIONS.get(item_id, ""),
                "has_scavenged_variant": "yes" if f"item.createcybernetics.scavenged_{item_id.split('_', 1)[-1]}" in lang else "no",
            }
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    slot_order = ["Brain", "Eyes", "Heart", "Lungs", "Organs", "Right arm", "Left arm", "Either arm", "Right leg", "Left leg", "Either leg", "Muscle", "Bone", "Skin"]
    md = [
        "# Current Create Cybernetics Implant Index",
        "",
        "This is the canonical installed-mod index for `createcybernetics` 0.5.1 HOTFIX in Infinite Domain. It is generated from the mod registry initialization, item tags, English localization, and implementation bytecode. Humanity costs are constructor values, not spawn-table weights.",
        "",
        f"The current system contains **{len(rows)} pristine surgery/wetware item IDs**: **159 installables** (18 base replacements, 99 cyberware upgrades, 20 functional wetware implants, and 22 biological/sculk body parts) plus 8 non-installable harvested wetware precursors. Symmetric limbs, plating variants, Multioptics cosmetics, and Mantis Blade materials are counted separately because they are separately registered choices. The mod also tags 95 scavenged copies; those are represented by the `has_scavenged_variant` field in the CSV rather than duplicated here.",
        "",
        "The machine-readable source is [`docs/cyberware-index/create-cybernetics-current-index.csv`](cyberware-index/create-cybernetics-current-index.csv).",
        "",
    ]
    for slot in slot_order:
        slot_rows = [row for row in rows if row["slot"] == slot]
        if not slot_rows:
            continue
        md.extend([f"## {slot}", "", "| Implant | Family | Humanity | Current effect, cost, or constraint |", "|---|---:|---:|---|"])
        for row in slot_rows:
            effect = row["current_effect_and_constraints"].replace("|", ";")
            optional = f" Integration: {row['optional_integration']}." if row["optional_integration"] else ""
            md.append(f"| {row['name']} (`{row['registry_id']}`) | {row['family']} | {row['humanity_cost']} | {effect}{optional} |")
        md.append("")
    MARKDOWN_OUT.write_text("\n".join(md), encoding="utf-8")
    print(f"wrote {len(rows)} canonical implants to {OUT}")
    print(f"wrote readable index to {MARKDOWN_OUT}")
    missing = [row["registry_id"] for row in rows if row["humanity_cost"] == ""]
    print(f"humanity unresolved: {len(missing)}")
    for item_id in missing:
        print(item_id)


if __name__ == "__main__":
    main()
