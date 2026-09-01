from __future__ import annotations

import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = {
    "prologue": ROOT / "config/ftbquests/quests/chapters/another_lost_soul.snbt",
    "era0": ROOT / "config/ftbquests/quests/chapters/lets_get_started_shall_we.snbt",
    "era4": ROOT / "config/ftbquests/quests/chapters/era_04_the_electrical_grid.snbt",
}
CHAPTER_GROUPS = ROOT / "config/ftbquests/quests/chapter_groups.snbt"
LANG = ROOT / "config/ftbquests/quests/lang/en_us.snbt"
OUT = ROOT / "docs/quest-progression/era0-pack-basics-audit.csv"
INTRO = "3AFBE38263D3351E"
QUEST_IDS = [f"600210000000{number:04X}" for number in range(1, 10)]
TASK_IDS = [f"600220000000{number:04X}" for number in range(1, 10)]


chapters = {name: path.read_text(encoding="utf-8") for name, path in CHAPTERS.items()}
language = LANG.read_text(encoding="utf-8")
placement = {
    1: ("prologue", "6F01000000000002", False, True),
    2: ("prologue", QUEST_IDS[0], False, True),
    3: ("era0", INTRO, True, False),
    4: ("era4", "4410000000000004", True, False),
    5: ("prologue", QUEST_IDS[1], True, False),
    6: ("prologue", QUEST_IDS[4], True, False),
    7: ("era0", INTRO, True, False),
    8: ("era0", INTRO, True, False),
    9: ("prologue", QUEST_IDS[1], False, False),
}
rows = []
for index, (quest_id, task_id) in enumerate(zip(QUEST_IDS, TASK_IDS), start=1):
    chapter_name, expected_dependency, expected_optional, reward_allowed = placement[index]
    chapter = chapters[chapter_name]
    id_position = chapter.find(f'\n\t\t\tid: "{quest_id}"')
    start = chapter.rfind("\n\t\t{", 0, id_position) if id_position >= 0 else -1
    end = chapter.find("\n\t\t}", id_position) if id_position >= 0 else -1
    block = chapter[start:end + 4] if start >= 0 and end >= 0 else ""
    checks = {
        "present": bool(block),
        "optional_ok": ("optional: true" in block) == expected_optional,
        "checkmark_task": f'id: "{task_id}"' in block and 'type: "checkmark"' in block,
        "dependency_ok": f'"{expected_dependency}"' in block,
        "reward_policy": (reward_allowed or "rewards:" not in block) and "can_repeat:" not in block,
        "localized": all(
            token in language
            for token in (
                f"quest.{quest_id}.title:",
                f"quest.{quest_id}.quest_desc:",
                f"task.{task_id}.title:",
            )
        ),
    }
    rows.append({
        "quest_number": index,
        "chapter": chapter_name,
        "quest_id": quest_id,
        **{key: str(value) for key, value in checks.items()},
        "status": "PASS" if all(checks.values()) else "FAIL",
    })

required_language = [
    "My Team",
    "shared by your FTB party",
    "Press M",
    "C for the Claim Manager",
    "Left-click",
    "Shift-left-click",
    "500-chunk ceiling",
    "25 chunks",
    "0,64,0",
    "7×7-chunk",
    "Quartermaster Echo",
    "twelve survival and repair offers",
    "physical Numismatics coins",
    "Early Livestock Exchange",
    "one spawn egg per purchase",
    "share the waypoint",
]
missing_language = [token for token in required_language if token not in language]

spawn_claim = (ROOT / "kubejs/server_scripts/admin_spawn_claim.js").read_text(encoding="utf-8")
hostile_protection = (ROOT / "kubejs/server_scripts/spawn_hub_hostile_protection.js").read_text(encoding="utf-8")
login_script = (ROOT / "kubejs/server_scripts/main.js").read_text(encoding="utf-8")
spawn_bootstrap = (ROOT / "kubejs/data/infinite_domain/function/admin/bootstrap_spawn_hospital.mcfunction").read_text(encoding="utf-8")
arrival_function = (ROOT / "kubejs/data/infinite_domain/function/admin/complete_pending_spawn_arrival.mcfunction").read_text(encoding="utf-8")
book_cleanup = (ROOT / "kubejs/data/infinite_domain/function/admin/remove_obsolete_starting_book.mcfunction").read_text(encoding="utf-8")
safe_zone_biome = json.loads((ROOT / "kubejs/data/infinite_domain/worldgen/biome/safe_zone.json").read_text(encoding="utf-8"))
safe_zone_mask = (ROOT / "datapacks/gradient_ocean_pack/data/custom_worldgen/worldgen/density_function/start_city_mask.json").read_text(encoding="utf-8")
safe_zone_mask_json = json.loads(safe_zone_mask)


def _safe_zone_is_compact_radial(node: object) -> bool:
    """The spawn safe-zone mask must be a radial (isekai_api:distance) falloff
    centred on the world origin, feathering to 0 well within the old +/-192
    square while still covering the 7x7-chunk admin claim (+/-56 blocks).
    A hard axis-step square (the pre-2026-08-26 shape) fails this."""
    if "isekai_api:distance" not in safe_zone_mask:
        return False
    if "isekai_api:coordinate" in safe_zone_mask or '"threshold"' in safe_zone_mask:
        return False  # axis-step square

    def find_distance_refs(n: object):
        if isinstance(n, dict):
            if n.get("type") == "isekai_api:distance":
                yield n
            for v in n.values():
                yield from find_distance_refs(v)
        elif isinstance(n, list):
            for v in n:
                yield from find_distance_refs(v)

    refs = list(find_distance_refs(node))
    if not refs:
        return False
    for r in refs:
        if (r.get("ref_x"), r.get("ref_z")) != (0.0, 0.0):
            return False
    # the largest constant in the mask is the outer feather radius; require it
    # to be a real shrink from 192 and at least the admin-claim half-extent.
    consts = [
        c["value"]
        for c in _iter_constants(node)
        if isinstance(c.get("value"), (int, float)) and c["value"] > 1.5
    ]
    outer = max(consts) if consts else 0
    return 56 <= outer <= 160


def _iter_constants(n: object):
    if isinstance(n, dict):
        if n.get("type") == "isekai_api:constant":
            yield n
        for v in n.values():
            yield from _iter_constants(v)
    elif isinstance(n, list):
        for v in n:
            yield from _iter_constants(v)
wasteland_preset = (ROOT / "kubejs/data/wastelands/worldgen/world_preset/wasteland.json").read_text(encoding="utf-8")
config = (ROOT / "config/ftbchunks-world.snbt").read_text(encoding="utf-8")
options = (ROOT / "options.txt").read_text(encoding="utf-8")
mods = ROOT / "mods"

source_checks = {
    "world_spawn": "setworldspawn 0 64 0 0" in spawn_claim,
    "automatic_lobby_bootstrap": "function infinite_domain:admin/bootstrap_spawn_hospital" in spawn_claim,
    "lobby_signature_guard": "unless block 20 95 20 spore:lab_block" in spawn_bootstrap,
    "lobby_places_once": "function infinite_domain:admin/place_spawn_hospital" in spawn_bootstrap,
    "pending_arrival_recorded": "teleport_next_arrival" in spawn_bootstrap,
    "pending_arrival_delayed": "complete_pending_spawn_arrival 1t replace" in login_script,
    "pending_arrival_position": all(token in arrival_function for token in ("spawnpoint @a", "tp @a", "0.5 64 0.5")),
    "momg_book_cleanup_delayed": "remove_obsolete_starting_book 1t replace" in login_script,
    "momg_book_removed": "clear @a[tag=infinite_domain_obsolete_book_cleanup] more_ores_more_gems:book_momg" in book_cleanup,
    "admin_claim_radius": (
        "manager.createServerTeam(" in spawn_claim
        and "for (let chunkX = -3; chunkX <= 3; chunkX++)" in spawn_claim
        and "for (let chunkZ = -3; chunkZ <= 3; chunkZ++)" in spawn_claim
    ),
    "admin_claim_verified": all(
        token in spawn_claim
        for token in ("verifiedClaims === 49", "claimedChunkManager.getChunk", "configureSpawnClaims(attempt + 1)")
    ),
    "safe_zone_selected": "infinite_domain:safe_zone" in wasteland_preset,
    "safe_zone_bounds": _safe_zone_is_compact_radial(safe_zone_mask_json),
    "safe_zone_has_no_features": all(not step for step in safe_zone_biome["features"]),
    "safe_zone_has_no_mobs": all(not entries for entries in safe_zone_biome["spawners"].values()),
    "admin_private": all(
        setting in spawn_claim
        for setting in ("BLOCK_EDIT_MODE", "BLOCK_INTERACT_MODE", "ENTITY_INTERACT_MODE", "$PrivacyMode.PRIVATE")
    ),
    "admin_hazard_settings": all(
        setting in spawn_claim
        for setting in ("ALLOW_EXPLOSIONS, false", "ALLOW_MOB_GRIEFING, false", "ALLOW_PVP, false")
    ),
    "hostile_bounds": all(
        token in hostile_protection
        for token in (
            "const MIN_X = -48",
            "const MAX_X_EXCLUSIVE = 64",
            "const MIN_Z = -48",
            "const MAX_Z_EXCLUSIVE = 64",
        )
    ),
    "hostile_dimension_api": "event.level.dimension.toString()" in hostile_protection and "dimension()" not in hostile_protection,
    "claim_limit": "max_claimed_chunks: 500" in config,
    "force_limit": "max_force_loaded_chunks: 25" in config,
    "party_limits": 'party_limit_mode: "largest"' in config,
    "map_key": "key_key.ftbchunks.map:key.keyboard.m" in options,
    "teams_key_unbound": "key_key.ftbteams.open_gui:key.keyboard.unknown" in options,
    "ftb_aeronautics_bridge_active": any(mods.glob("create_aeronautics_ftb_chunks-*.jar")),
    "opac_not_active": not any(mods.glob("open-parties-and-claims-*.jar")),
    "aeroclaims_not_active": not any(mods.glob("aeroclaims-*.jar")),
}

definitions = ROOT / "kubejs/data/infinite_domain/echo_definitions"
echo_files = sorted(definitions.glob("*.json"))
echo_checks = {
    "nine_echoes": len(echo_files) == 9,
    "twelve_offers_each": all(
        len(json.loads(path.read_text(encoding="utf-8"))["stages"][0]["shop_unlock"]) == 12
        for path in echo_files
    ),
    "quartermaster_era0": json.loads(
        (definitions / "quartermaster.json").read_text(encoding="utf-8")
    )["stages"][0]["required_stage"] == "infinite_domain:era_0",
}

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

failures = [row["quest_id"] for row in rows if row["status"] == "FAIL"]
failures += [f"missing language: {token}" for token in missing_language]
failures += [f"source check: {key}" for key, value in {**source_checks, **echo_checks}.items() if not value]

prologue = chapters["prologue"]
chapter_groups = CHAPTER_GROUPS.read_text(encoding="utf-8")
if 'autofocus_id: "7D194089522507AB"' not in prologue:
    failures.append("Prologue does not autofocus its first quest")
if 'order_index: 0' not in prologue:
    failures.append("Prologue is not first in the Civilization Eras group")
if chapter_groups.find('id: "346E9B7B176D7846"') > chapter_groups.find('id: "569AB980347C1123"'):
    failures.append("Civilization Eras is not the first chapter group")
starter_counts = {
    "wastelands:canned_food": 4,
    "wastelands:purified_water": 3,
    "minecraft:apple": 2,
    "supplementaries:sack": 1,
}
for item_id, expected in starter_counts.items():
    actual = prologue.count(f'id: "{item_id}"')
    if actual != expected:
        failures.append(f"starter reward count: {item_id} expected {expected}, found {actual}")

dialogue_ids = [f"6F010000000000{number:02X}" for number in range(0x10, 0x15)]
if not all(f'id: "{quest_id}"' in prologue and "optional: true" in prologue[prologue.rfind("\n\t\t{", 0, prologue.find(f'id: "{quest_id}"')):prologue.find("\n\t\t}", prologue.find(f'id: "{quest_id}"'))] for quest_id in dialogue_ids):
    failures.append("optional Charles dialogue chain")
if 'dependencies: ["6002100000000009"]' not in chapters["era0"]:
    failures.append("Era 0 intro is not gated by the prologue waypoint")
if 'id: "4B2A9ADF7B47B7EF"' not in chapters["era0"] or 'id: "4B2A9ADF7B47B7EF"' in prologue:
    failures.append("zombie lesson placement")

print(f"Era 0 Pack Basics: {sum(row['status'] == 'PASS' for row in rows)}/{len(rows)} quests pass.")
print(f"Pack evidence: {sum(source_checks.values())}/{len(source_checks)} claim/control checks and {sum(echo_checks.values())}/{len(echo_checks)} Echo checks pass.")
print("Prologue starter kit: 4 canned food, 3 purified water, 2 apples, and 1 sack.")
if failures:
    for failure in failures:
        print(f"FAIL: {failure}")
    raise SystemExit(1)
