"""Place the Old World sites that must stand alone, grouped by biome so they share a grid.

Two independent lines of evidence say which of the 64 Old World sites need to be
locatable structures rather than jigsaw pieces inside someone else's structure:

  * `dev/docs/old-world/structure-worldgen-roles.json` marks 11 of them
    INDEPENDENT_MOUNTAIN, INDEPENDENT_LANDMARK or COASTAL_TERMINAL; and
  * the `old_world_investigation` chapter hands out `structure_map` rewards for
    10 sites and gates quests on `structure` tasks for the same ones. Both of
    those fail outright unless a structure set places the target, so the quest
    tree is itself an authority on what must be placed.

Together that is 20 sites. OWS-006 already has the hand-authored
`controlled_pt9_probe` set and is left alone, leaving 19 to place here.

They are grouped into one set per biome restriction rather than one set per
structure. A structure set owns a placement grid, so N singleton sets give N
independent grids that happily land on the same chunk - which is exactly the
overlap the wasteland tier consolidation (30 sets down to 5) was done to fix.
Sharing a grid makes group members compete for each slot instead.

Spacing follows the existing wasteland tiers: the landmark tier (72/34) for
inland narrative sites, the coastal tier (176/72) for the port interface pair.

Salt is derived from the set name with SHA-256, so output is byte-identical run
to run and no two groups share a grid.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

ROLES = ROOT / "dev/docs/old-world/structure-worldgen-roles.json"
STRUCTURE_DIR = ROOT / "kubejs/data/infinite_domain/worldgen/structure/old_world"
SET_DIR = ROOT / "kubejs/data/infinite_domain/worldgen/structure_set/old_world"

INDEPENDENT_ROLES = {"INDEPENDENT_MOUNTAIN", "INDEPENDENT_LANDMARK", "COASTAL_TERMINAL"}

# Sites the quest tree makes locatable with a structure_map reward or a
# structure task. Kept explicit so a quest edit that drops one is visible here.
QUEST_LOCATABLE = {
    "OWS-001", "OWS-002", "OWS-003", "OWS-004", "OWS-006",
    "OWS-009", "OWS-010", "OWS-012", "OWS-015", "OWS-016",
}

# Already placed by a hand-authored set; not ours to move.
ALREADY_PLACED = {"OWS-006"}

# Biome restriction -> (set file name, spacing, separation). Spacing mirrors the
# wasteland tier the group's footprint belongs to.
GROUPS = {
    "wastelands:city": ("old_world_city_sites", 72, 34),
    "#infinite_domain:wasteland_rural_biomes": ("old_world_rural_sites", 72, 34),
    "#infinite_domain:wasteland_mountain_military_biomes": ("old_world_mountain_sites", 72, 34),
    "#infinite_domain:wasteland_site_biomes": ("old_world_landmark_sites", 72, 34),
    "#infinite_domain:wasteland_port_interface_biomes": ("old_world_port_sites", 176, 72),
}


def salt_for(name: str) -> int:
    return int(hashlib.sha256(name.encode("utf-8")).hexdigest()[:8], 16) % (2 ** 31)


def main() -> int:
    roles = json.loads(ROLES.read_text(encoding="utf-8"))["roles"]
    SET_DIR.mkdir(parents=True, exist_ok=True)

    # Remove the singleton sets an earlier revision of this generator wrote, so
    # rerunning converges instead of leaving both shapes on disk.
    for stale in sorted(SET_DIR.glob("ows_*.json")):
        stale.unlink()
        print("removed singleton " + stale.name)

    members: dict[str, list[str]] = {}
    skipped: list[tuple[str, str]] = []
    for key in sorted(roles):
        meta = roles[key]
        needed = meta["role"] in INDEPENDENT_ROLES or key in QUEST_LOCATABLE
        if not needed or key in ALREADY_PLACED:
            continue
        if not (STRUCTURE_DIR / meta["file"]).exists():
            skipped.append((key, "no structure definition"))
            continue
        biome = json.loads(
            (STRUCTURE_DIR / meta["file"]).read_text(encoding="utf-8-sig")
        ).get("biomes")
        biome = biome if isinstance(biome, str) else (biome or [None])[0]
        if biome not in GROUPS:
            skipped.append((key, "no group for biome " + str(biome)))
            continue
        members.setdefault(biome, []).append(
            "infinite_domain:old_world/" + meta["file"][:-len(".json")]
        )

    for biome in sorted(members):
        name, spacing, separation = GROUPS[biome]
        ids = sorted(members[biome])
        payload = {
            "structures": [{"structure": sid, "weight": 1} for sid in ids],
            "placement": {
                "type": "minecraft:random_spread",
                "spacing": spacing,
                "separation": separation,
                "salt": salt_for(name),
            },
        }
        (SET_DIR / (name + ".json")).write_text(
            json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(name + ": " + str(len(ids)) + " sites, " + str(spacing) + "/"
              + str(separation) + ", biome " + biome)
        for sid in ids:
            print("    " + sid.split("/")[-1])

    print("\nWrote " + str(len(members)) + " grouped sets covering "
          + str(sum(len(v) for v in members.values())) + " sites into "
          + SET_DIR.relative_to(ROOT).as_posix())
    for key, why in skipped:
        print("  skipped " + key + ": " + why)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
