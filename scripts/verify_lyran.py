"""Playability verification for Lyran Research.

The geometry lint proves the building is well-formed.  This proves it is
*playable*: that the End portal is a real, completable vanilla portal, that
the envelope has no hole a Nether lava ocean could pour through, and that a
player entering at the shaft mouth can actually walk to the Gate Chamber.

Run after scripts/lyran_research.py.  Exit code 0 means every assertion held.
"""

from __future__ import annotations

import sys
from collections import deque

sys.path.insert(0, ".")

import lyran_research as LR
from convert_nbt_to_lostcities import load_structure

PASSABLE_PREFIXES = ("minecraft:air",)
PASSABLE_SUBSTRINGS = ("_door", "ladder", "_sign", "lantern", "shroomlight", "torch")
# Blocks a player can occupy or pass through while walking/climbing.
NON_SOLID = {"minecraft:air", "minecraft:cave_air", "minecraft:void_air", "minecraft:water"}

failures: list[str] = []
notes: list[str] = []


def check(cond: bool, msg: str) -> None:
    if cond:
        notes.append(f"  PASS  {msg}")
    else:
        failures.append(f"  FAIL  {msg}")


def name_of(entry) -> str:
    return entry[0] if isinstance(entry, tuple) else entry


# The lostcities loader strips air blocks, which makes it the wrong model for
# a seal or reachability test: "no block here" would be indistinguishable from
# "air here", and the two mean opposite things inside a sealed complex.  So
# geometry checks run against the authored template, where air is explicit;
# the disk file is separately confirmed to round-trip in lint_lyran.py.
template, gen_report = LR.build()
size = template.size
sx, sy, sz = size
grid: dict[tuple[int, int, int], str] = {}
props: dict[tuple[int, int, int], dict] = {}
for pos, (state, _nbt) in template.blocks.items():
    entry = template.palette[state]
    grid[pos] = entry["Name"]
    props[pos] = entry.get("Properties", {})

disk_size, disk_blocks = load_structure(LR.OUT_NBT)
print(f"template: size={size} placed={len(grid)}")
print(f"disk    : size={disk_size} non-air={len(disk_blocks)}")
if tuple(disk_size) != tuple(size):
    failures.append(f"  FAIL  saved NBT size {disk_size} != template size {size}")

# ---------------------------------------------------------------------------
# 1. The End portal must be a real, completable vanilla portal.
# ---------------------------------------------------------------------------
cx, cz = 35, 43
py = LR.LEVEL_BY_KEY["concourse"]["y"] + 1

expected = {}
for d in (-1, 0, 1):
    expected[(cx + d, py, cz - 2)] = "south"
    expected[(cx + d, py, cz + 2)] = "north"
    expected[(cx - 2, py, cz + d)] = "east"
    expected[(cx + 2, py, cz + d)] = "west"

ring_ok = True
eyes = 0
for pos, facing in expected.items():
    nm = grid.get(pos)
    if nm != "minecraft:end_portal_frame":
        ring_ok = False
        failures.append(f"  FAIL  portal frame missing at {pos} (found {nm})")
        continue
    if props[pos].get("facing") != facing:
        ring_ok = False
        failures.append(f"  FAIL  portal frame at {pos} faces {props[pos].get('facing')}, expected {facing}")
    if props[pos].get("eye") == "true":
        eyes += 1

check(ring_ok, "End portal is a correct 12-frame vanilla ring, all frames facing inward")
check(len(expected) == 12, "portal ring has exactly 12 frame positions")
check(0 < eyes < 12, f"portal generates partially completed ({eyes} of 12 eyes seated, {12 - eyes} left for the player)")

interior_clear = all(
    grid.get((cx + dx, py, cz + dz), "minecraft:air") in NON_SOLID
    for dx in (-1, 0, 1) for dz in (-1, 0, 1)
)
check(interior_clear, "the 3x3 portal interior is clear, so the portal can actually form")

corners_empty = all(
    grid.get((cx + dx, py, cz + dz)) != "minecraft:end_portal_frame"
    for dx in (-2, 2) for dz in (-2, 2)
)
check(corners_empty, "ring corners are empty, matching vanilla portal geometry")

# ---------------------------------------------------------------------------
# 2. Envelope seal: no interior air may touch an unplaced cell.
#    An unplaced cell is whatever the Nether already had there — netherrack,
#    or lava.  A single missing block is a flooded facility.
# ---------------------------------------------------------------------------
shaft_x1, shaft_z1, shaft_x2, shaft_z2 = LR.SHAFT_RECT
mouth_top = LR.SHAFT_TOP


def in_shaft_mouth(x: int, y: int, z: int) -> bool:
    # The bastion head and its open mouth are the one intended opening.
    return y >= mouth_top - 4 and shaft_x1 - 3 <= x <= shaft_x2 + 3 and shaft_z1 - 3 <= z <= shaft_z2 + 3


leaks = []
for (x, y, z), nm in grid.items():
    if nm not in NON_SOLID:
        continue
    for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
        n = (x + dx, y + dy, z + dz)
        if not (0 <= n[0] < sx and 0 <= n[1] < sy and 0 <= n[2] < sz):
            continue
        if n in grid:
            continue
        if in_shaft_mouth(*n):
            continue
        leaks.append((x, y, z))
        break

check(not leaks, f"envelope is lava-tight: no interior air cell borders unplaced world rock ({len(leaks)} leaks)")
if leaks:
    for p in leaks[:10]:
        failures.append(f"        leak at {p}")

# ---------------------------------------------------------------------------
# 3. Reachability: walk from the shaft mouth to the Gate Chamber.
#    A cell is standable when the player's feet and head are clear and the
#    block underfoot is solid; ladders let a player move vertically.
# ---------------------------------------------------------------------------
def clear_at(p) -> bool:
    nm = grid.get(p)
    if nm is None:
        return False              # unplaced = solid world rock
    return nm in NON_SOLID or "_door" in nm or nm.endswith("_sign") or "ladder" in nm


def is_ladder(p) -> bool:
    return grid.get(p, "") == "minecraft:ladder"


def supported(p) -> bool:
    below = grid.get((p[0], p[1] - 1, p[2]))
    return below is not None and below not in NON_SOLID


start = None
for y in range(mouth_top, mouth_top - 8, -1):
    for x in range(shaft_x1 + 1, shaft_x2):
        for z in range(shaft_z1 + 1, shaft_z2):
            if clear_at((x, y, z)) and clear_at((x, y + 1, z)) if y + 1 < sy else False:
                start = (x, y, z)
                break
        if start:
            break
    if start:
        break

if start is None:
    failures.append("  FAIL  could not find an entry cell at the shaft mouth")
else:
    seen = {start}
    q = deque([start])
    while q:
        x, y, z = q.popleft()
        cands = []
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            for dy in (0, 1, -1, -2, -3):      # step up one, drop a few
                cands.append((x + dx, y + dy, z + dz))
        cands.append((x, y + 1, z))            # climb
        cands.append((x, y - 1, z))            # descend / fall
        for n in cands:
            if n in seen:
                continue
            if not (0 <= n[0] < sx and 0 <= n[1] < sy and 0 <= n[2] < sz):
                continue
            if not clear_at(n) or not clear_at((n[0], n[1] + 1, n[2])):
                continue
            vertical = n[0] == x and n[2] == z
            if vertical and not (is_ladder(n) or is_ladder((x, y, z))):
                if n[1] > y:
                    continue
            if not vertical and not supported(n) and not is_ladder(n) and n[1] >= y:
                continue
            seen.add(n)
            q.append(n)

    gate_cells = {(x, py, z) for x, z in LR.Plan(LR.PLAN_PATH).rooms[21]["cells"]}
    reached_gate = gate_cells & seen
    check(bool(reached_gate),
          f"a player entering at the shaft mouth can walk to the Gate Chamber ({len(reached_gate)} of {len(gate_cells)} chamber cells reached)")

    for lv in LR.LEVELS:
        lvy = lv["y"] + 1
        on_level = {p for p in seen if p[1] == lvy}
        check(len(on_level) > 40, f"level '{lv['key']}' is reachable ({len(on_level)} standing cells reached at y={lvy})")

    check(len(seen) > 3000, f"reachable interior volume is substantial ({len(seen)} cells)")

# ---------------------------------------------------------------------------
# 4. No iron doors — they need redstone a generated structure cannot supply.
# ---------------------------------------------------------------------------
iron_doors = [p for p, nm in grid.items() if nm == "minecraft:iron_door"]
check(not iron_doors, f"no iron doors (would be unopenable) — found {len(iron_doors)}")

# ---------------------------------------------------------------------------
print()
for line in notes:
    print(line)
if failures:
    print()
    for line in failures:
        print(line)
    print(f"\n{len(failures)} FAILURES")
    sys.exit(1)
print(f"\nall {len(notes)} checks passed")
