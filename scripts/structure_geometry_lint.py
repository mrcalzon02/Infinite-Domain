"""Structure Rebuild System v2 — geometric QA gate.

Replaces `assess_fidelity()` in `generate_wasteland_sites.py` as the
production lint. That function only counted door halves, glass blocks and
"functional fixture" keywords anywhere in a structure; it never inspected
whether anything was actually supported, enclosed, or coherent. This module
inspects the geometry itself.

Design notes
------------
Every check operates on a normalized representation:

    positions: dict[(x, y, z)] -> (block_name: str, properties: dict[str, str])
    size: (sx, sy, sz)

Two adapters are provided so this runs both in-process against a live
`Template` during generation, and standalone against saved `.nbt` files via
the existing `convert_nbt_to_lostcities.load_structure` loader (the same
loader `audit_structure_block_fitness.py` already uses).

`positions_from_load_structure` assumes `load_structure` returns
`(size, blocks)` where `blocks` maps position to `(state_string, tag)` and
`state_string` looks like `"minecraft:oak_stairs[facing=north,...]"` (this
matches how `audit_structure_block_fitness.py` consumes it via
`parse_state`). If the real return shape differs, adjust
`positions_from_load_structure` accordingly — the rest of this module only
depends on the normalized `positions`/`size` contract above, not on either
loader's internals.

This module intentionally has zero third-party dependencies so it can run
anywhere Python 3.10+ runs.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

Pos = tuple[int, int, int]

# ---------------------------------------------------------------------------
# Adapters
# ---------------------------------------------------------------------------


def positions_from_template(t: Any) -> tuple[tuple[int, int, int], dict[Pos, tuple[str, dict[str, str]]]]:
    """Normalize a live generate_wasteland_sites.Template instance."""
    out: dict[Pos, tuple[str, dict[str, str]]] = {}
    for pos, (state_idx, _nbt) in t.blocks.items():
        entry = t.palette[state_idx]
        out[pos] = (entry["Name"], dict(entry.get("Properties", {})))
    return tuple(t.size), out


_STATE_RE = re.compile(r"^(?P<name>[a-z0-9_.\-]+:[a-z0-9_./\-]+)(\[(?P<props>.*)\])?$")


def parse_state_string(state: str) -> tuple[str, dict[str, str]]:
    match = _STATE_RE.match(state)
    if not match:
        return state, {}
    name = match.group("name")
    props_raw = match.group("props") or ""
    props: dict[str, str] = {}
    if props_raw:
        for pair in props_raw.split(","):
            if "=" in pair:
                key, value = pair.split("=", 1)
                props[key] = value
    return name, props


def positions_from_load_structure(size: tuple[int, int, int], blocks: dict[Pos, tuple[str, Any]]) -> dict[Pos, tuple[str, dict[str, str]]]:
    """Normalize the (size, blocks) pair returned by convert_nbt_to_lostcities.load_structure.

    Verify this against the real loader before relying on it in production —
    see the module docstring.
    """
    out: dict[Pos, tuple[str, dict[str, str]]] = {}
    for pos, (state, _tag) in blocks.items():
        out[pos] = parse_state_string(state)
    return out


# ---------------------------------------------------------------------------
# Block classification
# ---------------------------------------------------------------------------

AIR_LIKE = {"minecraft:air", "minecraft:cave_air", "minecraft:void_air"}
LIQUID = {"minecraft:water", "minecraft:lava"}

# Blocks that are legitimately self-supporting against a single face rather
# than needing full connectivity to the ground graph. Ladders/signs are
# checked for backing separately (see check_ladders_and_signs); torches,
# vines, etc. are excluded from the connectivity scan entirely because
# Minecraft attaches them to a neighbor face, not to the ground graph.
FACE_ATTACHED = {
    "minecraft:ladder", "minecraft:wall_torch", "minecraft:torch",
    "minecraft:redstone_wall_torch", "minecraft:vine", "minecraft:lantern",
}


def _is_solid(name: str) -> bool:
    return name not in AIR_LIKE and name not in LIQUID


def _is_face_attached(name: str) -> bool:
    return name in FACE_ATTACHED or name.endswith("_sign") or name.endswith("_wall_sign")


def _is_glass(name: str) -> bool:
    return "glass" in name or name.endswith("stained_glass_pane")


def _is_door(name: str) -> bool:
    return name.endswith("_door")


def _is_stair(name: str) -> bool:
    return name.endswith("_stairs")


def _is_wall_material(name: str, properties: dict[str, str]) -> bool:
    """A rough but useful classifier for "counts as a wall segment".

    Deliberately excludes glass (a window is not its own frame) and stairs
    (a stair block is circulation, not a wall).
    """
    if not _is_solid(name):
        return False
    if _is_glass(name) or _is_stair(name) or _is_door(name):
        return False
    if _is_face_attached(name):
        return False
    return True


NEIGHBORS_6 = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]


@dataclass
class Finding:
    check: str
    severity: str  # "hard_fail" | "review_flag"
    position: Pos | None
    detail: str


@dataclass
class LintResult:
    structure_id: str
    findings: list[Finding] = field(default_factory=list)

    @property
    def hard_fail_count(self) -> int:
        return sum(1 for f in self.findings if f.severity == "hard_fail")

    @property
    def passed(self) -> bool:
        return self.hard_fail_count == 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "structure_id": self.structure_id,
            "passed": self.passed,
            "hard_fail_count": self.hard_fail_count,
            "findings": [
                {
                    "check": f.check,
                    "severity": f.severity,
                    "position": list(f.position) if f.position else None,
                    "detail": f.detail,
                }
                for f in self.findings
            ],
        }


# ---------------------------------------------------------------------------
# Check 1 — structural connectivity (floating geometry)
# ---------------------------------------------------------------------------


def check_structural_connectivity(
    size: tuple[int, int, int],
    positions: dict[Pos, tuple[str, dict[str, str]]],
    *,
    ground_y: tuple[int, ...] | None = None,
    max_reported: int = 40,
) -> list[Finding]:
    """Flood-fill solid blocks from the base plate; anything unreached floats.

    This single check is what catches floating floors, floating roofs, and
    any stair/wall fragment a damage pass has orphaned. Face-attached
    decorations (ladders, signs, torches) are excluded — they are checked
    for backing separately, not for ground connectivity.

    ``ground_y`` is derived per template, not fixed at (0, 1): quarry/mine/
    pit/oil-field style templates build their real rim and road at a
    "surface" y that can be well above 0 (8, 10, 12...), and place nothing
    at all at y=0 or y=1. A fixed (0, 1) anchor set finds zero anchors for
    those templates and flags every solid block in them as floating, which
    is a lint false positive, not a real defect. The template's own lowest
    solid layer is, by this codebase's own convention (roadside_apron,
    cracked_pad, rim_road all build their ground-contact course as the
    lowest fill in the template), the intended footing course, so anchor
    off of it unless a caller explicitly knows better.
    """
    solid: set[Pos] = {
        pos for pos, (name, _props) in positions.items()
        if _is_solid(name) and not _is_face_attached(name)
    }
    if not solid:
        return []

    if ground_y is None:
        min_y = min(pos[1] for pos in solid)
        ground_y = (min_y, min_y + 1)

    anchors = {pos for pos in solid if pos[1] in ground_y}
    visited: set[Pos] = set()
    stack = list(anchors)
    visited.update(anchors)
    while stack:
        x, y, z = stack.pop()
        for dx, dy, dz in NEIGHBORS_6:
            npos = (x + dx, y + dy, z + dz)
            if npos in solid and npos not in visited:
                visited.add(npos)
                stack.append(npos)

    floating = sorted(solid - visited)
    findings = [
        Finding(
            check="structural_connectivity",
            severity="hard_fail",
            position=pos,
            detail=f"{positions[pos][0]} at {pos} is not connected to the ground plate through solid geometry",
        )
        for pos in floating[:max_reported]
    ]
    if len(floating) > max_reported:
        findings.append(
            Finding(
                check="structural_connectivity",
                severity="hard_fail",
                position=None,
                detail=f"{len(floating) - max_reported} additional floating blocks not individually listed ({len(floating)} total)",
            )
        )
    return findings


# ---------------------------------------------------------------------------
# Check 2 — stair / ladder / sign validator
# ---------------------------------------------------------------------------

_STAIR_FACING_DELTA = {"north": (0, 0, -1), "south": (0, 0, 1), "east": (1, 0, 0), "west": (-1, 0, 0)}
_LADDER_BACKING_DELTA = {  # the block a ladder is mounted against sits opposite its facing
    "north": (0, 0, 1), "south": (0, 0, -1), "east": (-1, 0, 0), "west": (1, 0, 0),
}


def _group_stair_runs(positions: dict[Pos, tuple[str, dict[str, str]]]) -> list[list[Pos]]:
    stairs_by_facing: dict[str, list[Pos]] = defaultdict(list)
    for pos, (name, props) in positions.items():
        if _is_stair(name) and props.get("shape", "straight") == "straight":
            stairs_by_facing[props.get("facing", "north")].append(pos)

    runs: list[list[Pos]] = []
    for facing, cells in stairs_by_facing.items():
        dx, dy, dz = _STAIR_FACING_DELTA[facing]
        remaining = set(cells)
        while remaining:
            start = next(iter(remaining))
            run = [start]
            remaining.discard(start)
            cursor = start
            while True:
                nxt = (cursor[0] + dx, cursor[1] + dy, cursor[2] + dz)
                if nxt in remaining:
                    run.append(nxt)
                    remaining.discard(nxt)
                    cursor = nxt
                else:
                    break
            runs.append(run)
    return runs


def check_stairs_ladders_signs(
    size: tuple[int, int, int],
    positions: dict[Pos, tuple[str, dict[str, str]]],
) -> list[Finding]:
    findings: list[Finding] = []

    # -- stairs: lateral support + landing at both ends --------------------
    for run in _group_stair_runs(positions):
        if len(run) < 2:
            continue
        run = sorted(run, key=lambda p: p[1])  # order by rise
        facing = None
        for pos, (name, props) in positions.items():
            if pos == run[0] and _is_stair(name):
                facing = props.get("facing", "north")
                break
        if facing is None:
            continue
        dx, dy, dz = _STAIR_FACING_DELTA[facing]
        # lateral axis is perpendicular to travel
        lateral = (0, 0, 1) if dx else (1, 0, 0)

        supported_sides = 0
        for side in (lateral, (-lateral[0], -lateral[1], -lateral[2])):
            side_solid = True
            for pos in run:
                check_pos = (pos[0] + side[0], pos[1] + side[1] + 1, pos[2] + side[2])
                name, _ = positions.get(check_pos, ("minecraft:air", {}))
                if not _is_wall_material(name, {}):
                    side_solid = False
                    break
            if side_solid:
                supported_sides += 1
        if supported_sides == 0:
            findings.append(Finding(
                check="stair_enclosure",
                severity="hard_fail",
                position=run[0],
                detail=f"stair run of {len(run)} steps facing {facing} has no lateral wall support on either side (not an encased stairwell)",
            ))

        # landing check: the cell one step beyond each end of the run,
        # at tread height, must rest on solid ground (a real floor), not air.
        for end, direction in ((run[0], (-dx, -1, -dz)), (run[-1], (dx, 1, dz))):
            landing = (end[0] + direction[0], end[1] + direction[1] - 1, end[2] + direction[2])
            name, _ = positions.get(landing, ("minecraft:air", {}))
            if not _is_solid(name):
                findings.append(Finding(
                    check="stair_landing",
                    severity="hard_fail",
                    position=end,
                    detail=f"stair run facing {facing} does not terminate on a solid landing at {landing}",
                ))

    # -- ladders: backing block required ------------------------------------
    for pos, (name, props) in positions.items():
        if name != "minecraft:ladder":
            continue
        facing = props.get("facing", "north")
        bx, by, bz = _LADDER_BACKING_DELTA.get(facing, (0, 0, 0))
        backing_pos = (pos[0] + bx, pos[1] + by, pos[2] + bz)
        backing_name, _ = positions.get(backing_pos, ("minecraft:air", {}))
        if not _is_solid(backing_name):
            findings.append(Finding(
                check="ladder_backing",
                severity="hard_fail",
                position=pos,
                detail=f"ladder facing {facing} at {pos} has no solid backing block at {backing_pos}",
            ))

    # -- wall signs: backing block required; standing signs: floor required -
    for pos, (name, props) in positions.items():
        if name.endswith("_wall_sign") or name.endswith("_wall_hanging_sign"):
            facing = props.get("facing", "north")
            bx, by, bz = _LADDER_BACKING_DELTA.get(facing, (0, 0, 0))
            backing_pos = (pos[0] + bx, pos[1] + by, pos[2] + bz)
            backing_name, _ = positions.get(backing_pos, ("minecraft:air", {}))
            if not _is_solid(backing_name):
                findings.append(Finding(
                    check="sign_backing",
                    severity="hard_fail",
                    position=pos,
                    detail=f"wall sign at {pos} has no solid backing block at {backing_pos}",
                ))
        elif name.endswith("_sign"):
            below = (pos[0], pos[1] - 1, pos[2])
            below_name, _ = positions.get(below, ("minecraft:air", {}))
            if not _is_solid(below_name):
                findings.append(Finding(
                    check="sign_backing",
                    severity="hard_fail",
                    position=pos,
                    detail=f"standing sign at {pos} has no solid floor block at {below}",
                ))

    return findings


# ---------------------------------------------------------------------------
# Check 3 — window / door wall-coupling
# ---------------------------------------------------------------------------


def _door_wall_coupled(pos: Pos, positions: dict[Pos, tuple[str, dict[str, str]]]) -> bool:
    x, y, z = pos
    x_axis_neighbors = [positions.get((x - 1, y, z), ("minecraft:air", {})), positions.get((x + 1, y, z), ("minecraft:air", {}))]
    z_axis_neighbors = [positions.get((x, y, z - 1), ("minecraft:air", {})), positions.get((x, y, z + 1), ("minecraft:air", {}))]
    framed_on_x = any(_is_wall_material(n, p) for n, p in x_axis_neighbors)
    framed_on_z = any(_is_wall_material(n, p) for n, p in z_axis_neighbors)
    all_horizontal_air = all(n in AIR_LIKE for n, _ in (*x_axis_neighbors, *z_axis_neighbors))
    return not all_horizontal_air and (framed_on_x or framed_on_z)


_GLASS_NEIGHBORS = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]


def check_openings_wall_coupled(
    size: tuple[int, int, int],
    positions: dict[Pos, tuple[str, dict[str, str]]],
    *,
    max_reported: int = 40,
) -> list[Finding]:
    """Doors are checked individually. Glass is checked as contiguous panes,
    not per-block: a whole window (or a curtain wall / greenhouse glazing
    run) only needs wall/jamb material touching it SOMEWHERE on its
    boundary, not on every single pane. Checking per-block would flag every
    pane in a legitimate multi-block window or glasshouse as "floating"
    since panes next to panes are never themselves wall material — that
    produced a large false-positive count in the first version of this
    check and is the reason for this component-based rewrite.
    """
    findings: list[Finding] = []

    for pos, (name, _props) in positions.items():
        if _is_door(name) and not _door_wall_coupled(pos, positions):
            findings.append(Finding(
                check="opening_wall_coupling",
                severity="hard_fail",
                position=pos,
                detail=f"{name} at {pos} has no framing wall material on either horizontal axis (floating door)",
            ))

    glass_positions = {pos for pos, (name, _props) in positions.items() if _is_glass(name)}
    visited: set[Pos] = set()
    unframed_components = 0
    unframed_examples: list[Pos] = []
    for start in glass_positions:
        if start in visited:
            continue
        component = [start]
        visited.add(start)
        stack = [start]
        touches_wall = False
        while stack:
            cx, cy, cz = stack.pop()
            for dx, dy, dz in _GLASS_NEIGHBORS:
                npos = (cx + dx, cy + dy, cz + dz)
                nname, nprops = positions.get(npos, ("minecraft:air", {}))
                if npos in glass_positions and npos not in visited:
                    visited.add(npos)
                    component.append(npos)
                    stack.append(npos)
                elif _is_wall_material(nname, nprops):
                    touches_wall = True
        if not touches_wall:
            unframed_components += 1
            unframed_examples.append(start)
            if len(unframed_examples) <= max_reported:
                findings.append(Finding(
                    check="opening_wall_coupling",
                    severity="hard_fail",
                    position=start,
                    detail=f"glazed pane/run of {len(component)} block(s) starting at {start} has no wall material touching its boundary anywhere (floating window)",
                ))
    if unframed_components > max_reported:
        findings.append(Finding(
            check="opening_wall_coupling",
            severity="hard_fail",
            position=None,
            detail=f"{unframed_components - max_reported} additional unframed glazed components not individually listed",
        ))
    return findings


# ---------------------------------------------------------------------------
# Check 4 (heuristic) — damage coherence between a clean master and a variant
# ---------------------------------------------------------------------------


def check_damage_coherence(
    clean_positions: dict[Pos, tuple[str, dict[str, str]]],
    variant_positions: dict[Pos, tuple[str, dict[str, str]]],
    *,
    rubble_terms: tuple[str, ...] = ("gravel", "rubble", "cobblestone", "scrap", "debris", "blackstone"),
) -> list[Finding]:
    """Flags removed volumes that look like a clean rectangular cut with no
    debris nearby — a proxy for "cube of missing blocks" rather than an
    authored fracture. This is a heuristic feeding the human review pass,
    not a hard fail (see Section 4 of the spec document).
    """
    removed = {
        pos for pos, (name, _props) in clean_positions.items()
        if _is_solid(name) and pos not in variant_positions
    }
    if not removed:
        return []

    xs = [p[0] for p in removed]
    ys = [p[1] for p in removed]
    zs = [p[2] for p in removed]
    bbox_volume = (max(xs) - min(xs) + 1) * (max(ys) - min(ys) + 1) * (max(zs) - min(zs) + 1)
    fill_ratio = len(removed) / bbox_volume if bbox_volume else 0

    findings: list[Finding] = []
    if fill_ratio > 0.97:
        findings.append(Finding(
            check="damage_coherence",
            severity="review_flag",
            position=None,
            detail=(
                f"removed volume fills {fill_ratio:.0%} of its bounding box "
                "(reads as a clean rectangular cut, not an authored fracture) "
                f"across {len(removed)} blocks"
            ),
        ))

    nearby_rubble = 0
    for pos in list(removed)[:2000]:  # bounded scan for very large diffs
        found = False
        for dx, dy, dz in NEIGHBORS_6:
            name, _ = variant_positions.get((pos[0] + dx, pos[1] + dy, pos[2] + dz), ("minecraft:air", {}))
            if any(term in name for term in rubble_terms):
                found = True
                break
        # Debris obeys gravity: a wall/roof breach leaves its rubble on the
        # floor below, not welded to the breach lip. Scan straight down from
        # each removed cell for a settled debris pile before concluding the
        # damage added none.
        if not found:
            for drop in range(1, 25):
                name, _ = variant_positions.get((pos[0], pos[1] - drop, pos[2]), ("minecraft:air", {}))
                if any(term in name for term in rubble_terms):
                    found = True
                    break
                if _is_solid(name) and name not in AIR_LIKE:
                    break  # hit a real floor/obstruction first
        if found:
            nearby_rubble += 1
    if nearby_rubble == 0:
        findings.append(Finding(
            check="damage_coherence",
            severity="review_flag",
            position=None,
            detail="no rubble/debris blocks found adjacent to or fallen below the removed volume",
        ))
    return findings


# ---------------------------------------------------------------------------
# Check 5 (heuristic) — ground-plane speckle / context detector
# ---------------------------------------------------------------------------


def check_ground_plane(
    size: tuple[int, int, int],
    positions: dict[Pos, tuple[str, dict[str, str]]],
    *,
    allowed_by_context: dict[str, set[str]] | None = None,
    site_context: str | None = None,
    ground_y: int = 0,
) -> list[Finding]:
    findings: list[Finding] = []
    ground_blocks = {
        (x, z): name
        for (x, y, z), (name, _props) in positions.items()
        if y == ground_y and _is_solid(name)
    }
    if not ground_blocks:
        return findings

    counts = Counter(ground_blocks.values())
    # A short-period alternation between 3+ materials is the signature of a
    # modulo-based speckle selector (cracked_pad's (x*37+z*17)%19 pattern),
    # not a real ground surface, which tends to occur in coherent patches.
    if len(counts) >= 3:
        transitions = 0
        total = 0
        sorted_cells = sorted(ground_blocks)
        for (x, z), name in zip(sorted_cells, [ground_blocks[c] for c in sorted_cells]):
            right = ground_blocks.get((x + 1, z))
            if right is not None:
                total += 1
                if right != name:
                    transitions += 1
        speckle_ratio = transitions / total if total else 0
        if speckle_ratio > 0.5:
            findings.append(Finding(
                check="ground_plane_speckle",
                severity="review_flag",
                position=None,
                detail=(
                    f"ground layer changes material on {speckle_ratio:.0%} of adjacent cell pairs "
                    f"across {len(counts)} materials — reads as speckle noise, not a real ground surface"
                ),
            ))

    if allowed_by_context and site_context:
        allowed = allowed_by_context.get(site_context, set())
        disallowed_used = {name for name in counts if allowed and name not in allowed}
        if allowed and disallowed_used:
            findings.append(Finding(
                check="ground_plane_context",
                severity="review_flag",
                position=None,
                detail=f"site_context={site_context!r} used out-of-context ground materials: {sorted(disallowed_used)}",
            ))
    return findings


# ---------------------------------------------------------------------------
# Check 6 — room composition: sealed rooms and undersized rooms
# ---------------------------------------------------------------------------


def _enclosed_air_components(
    size: tuple[int, int, int],
    positions: dict[Pos, tuple[str, dict[str, str]]],
) -> list[list[Pos]]:
    """Return every connected pocket of air that does NOT reach the template boundary.

    Flood-fills air from the outer shell of the template's bounding box first
    (a proxy for "outdoors" — the box is always much larger than any single
    building on the site). Whatever air is left unreached partitions into
    enclosed pockets: interior rooms, corridors, sealed voids. Doors are NOT
    air — they are solid blocks in this model — so a room behind a closed
    door is correctly a separate component from the outside air, and the
    door itself shows up as a solid boundary block that can be checked for.
    """
    sx, sy, sz = size

    def is_air(pos: Pos) -> bool:
        entry = positions.get(pos)
        if entry is None:
            return True
        return not _is_solid(entry[0])

    exterior: set[Pos] = set()
    stack: list[Pos] = []
    for x in range(sx):
        for y in range(sy):
            for z in (0, sz - 1):
                p = (x, y, z)
                if is_air(p):
                    stack.append(p)
    for x in range(sx):
        for z in range(sz):
            for y in (0, sy - 1):
                p = (x, y, z)
                if is_air(p):
                    stack.append(p)
    for y in range(sy):
        for z in range(sz):
            for x in (0, sx - 1):
                p = (x, y, z)
                if is_air(p):
                    stack.append(p)
    exterior.update(stack)
    while stack:
        x, y, z = stack.pop()
        for dx, dy, dz in NEIGHBORS_6:
            nx, ny, nz = x + dx, y + dy, z + dz
            if 0 <= nx < sx and 0 <= ny < sy and 0 <= nz < sz:
                n = (nx, ny, nz)
                if n not in exterior and is_air(n):
                    exterior.add(n)
                    stack.append(n)

    visited = set(exterior)
    components: list[list[Pos]] = []
    for x in range(sx):
        for y in range(sy):
            for z in range(sz):
                p = (x, y, z)
                if p in visited or not is_air(p):
                    continue
                comp = [p]
                visited.add(p)
                frontier = [p]
                while frontier:
                    cx, cy, cz = frontier.pop()
                    for dx, dy, dz in NEIGHBORS_6:
                        nx, ny, nz = cx + dx, cy + dy, cz + dz
                        if 0 <= nx < sx and 0 <= ny < sy and 0 <= nz < sz:
                            n = (nx, ny, nz)
                            if n not in visited and is_air(n):
                                visited.add(n)
                                comp.append(n)
                                frontier.append(n)
                components.append(comp)
    return components


# Blocks that signal "a person was meant to use this space" — distinct from
# pure structural/material blocks (walls, floors, roof stairs, planks).
# Two legitimate architectural patterns produce large sealed (doorless) air
# pockets that are NOT bugs: roof/attic cavities above a gable roof's wall
# plate, and intentionally sealed vessels (round_tank fuel/grain silos).
# Neither contains any of this furniture, so a sealed pocket that also
# contains none of it is far more likely to be one of those than a real
# unreachable room, and is downgraded to review_flag instead of hard_fail.
FURNISHING_MARKERS = (
    "chest", "barrel", "smoker", "furnace", "cauldron", "item_shelf",
    "the_wasteland_reworked:radio", "lever", "_bed", "mechanical_",
    "scrap_pile", "redstone_lamp", "sea_lantern", "lightning_rod",
    "brewing_stand", "loom", "cartography_table", "grindstone",
    "blast_furnace", "campfire", "beacon", "spawner",
)


def _is_furnishing(name: str) -> bool:
    return any(marker in name for marker in FURNISHING_MARKERS)


def check_room_composition(
    size: tuple[int, int, int],
    positions: dict[Pos, tuple[str, dict[str, str]]],
    *,
    min_room_floor_cells: int = 4,
    min_room_height: int = 2,
    max_reported: int = 40,
) -> list[Finding]:
    """Flag enclosed rooms that are unreachable or too small to serve their purpose.

    Fitness-of-purpose failures this catches:
      - sealed_room: a room-sized enclosed air pocket (>= min_room_floor_cells
        floor cells, >= min_room_height tall) with no door anywhere on its
        boundary. Nothing else can open a sealed room, since by definition an
        enclosed pocket has no other gap to the outside — a walkthrough
        cannot reach it. Reported as hard_fail only when the pocket also
        borders a furnishing block (see FURNISHING_MARKERS), which is strong
        evidence the space was authored to be entered (a loot chest, a
        machine, a bed) rather than incidental voids like a roof cavity or a
        deliberately sealed storage tank; an unfurnished sealed pocket is
        still reported, but as review_flag, since either interpretation is
        plausible without a human glance.
      - undersized_room: an enclosed room that DOES have a door (so it is
        clearly intended as an occupiable space) but whose floor footprint
        is below min_room_floor_cells — too small to be fit for any stated
        purpose (a "bedroom" narrower than a bed, a "hallway" a player
        cannot turn around in).

    Tiny incidental air pockets (gaps between rubble, a single missing
    block) are not treated as rooms at all: both checks require the pocket
    to be at least min_room_height tall, which rubble gaps essentially never
    are.
    """
    findings: list[Finding] = []
    components = _enclosed_air_components(size, positions)

    sealed_furnished = 0
    sealed_unfurnished = 0
    undersized = 0
    for comp in components:
        ys = [p[1] for p in comp]
        min_y, max_y = min(ys), max(ys)
        height = max_y - min_y + 1
        if height < min_room_height:
            continue
        floor_cells = {(p[0], p[2]) for p in comp if p[1] == min_y}
        if len(floor_cells) < 1:
            continue
        has_door = False
        has_furnishing = False
        for (cx, cy, cz) in comp:
            for dx, dy, dz in NEIGHBORS_6:
                n = (cx + dx, cy + dy, cz + dz)
                entry = positions.get(n)
                if entry is not None:
                    if _is_door(entry[0]):
                        has_door = True
                    if _is_furnishing(entry[0]):
                        has_furnishing = True
            if has_door and has_furnishing:
                break

        anchor = min(comp)
        if not has_door and len(floor_cells) >= min_room_floor_cells:
            severity = "hard_fail" if has_furnishing else "review_flag"
            if has_furnishing:
                sealed_furnished += 1
                count_so_far = sealed_furnished
            else:
                sealed_unfurnished += 1
                count_so_far = sealed_unfurnished
            if count_so_far <= max_reported:
                furnish_note = "borders a furnishing block" if has_furnishing else "no furnishing found — may be a roof cavity or an intentionally sealed vessel, verify"
                findings.append(Finding(
                    check="room_composition",
                    severity=severity,
                    position=anchor,
                    detail=(
                        f"enclosed room of {len(comp)} air blocks ({len(floor_cells)} floor cells, "
                        f"{height} tall) near {anchor} has no door anywhere on its boundary — unreachable ({furnish_note})"
                    ),
                ))
        elif has_door and len(floor_cells) < min_room_floor_cells:
            undersized += 1
            if undersized <= max_reported:
                findings.append(Finding(
                    check="room_composition",
                    severity="review_flag",
                    position=anchor,
                    detail=(
                        f"doored room near {anchor} has only {len(floor_cells)} floor cells "
                        f"({height} tall) — too small to be fit for a stated purpose"
                    ),
                ))

    if sealed_furnished > max_reported:
        findings.append(Finding(
            check="room_composition",
            severity="hard_fail",
            position=None,
            detail=f"{sealed_furnished - max_reported} additional furnished sealed (doorless) rooms not individually listed ({sealed_furnished} total)",
        ))
    if sealed_unfurnished > max_reported:
        findings.append(Finding(
            check="room_composition",
            severity="review_flag",
            position=None,
            detail=f"{sealed_unfurnished - max_reported} additional unfurnished sealed (doorless) pockets not individually listed ({sealed_unfurnished} total)",
        ))
    if undersized > max_reported:
        findings.append(Finding(
            check="room_composition",
            severity="review_flag",
            position=None,
            detail=f"{undersized - max_reported} additional undersized doored rooms not individually listed ({undersized} total)",
        ))
    return findings


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------


def lint_structure(
    structure_id: str,
    size: tuple[int, int, int],
    positions: dict[Pos, tuple[str, dict[str, str]]],
    *,
    clean_master_positions: dict[Pos, tuple[str, dict[str, str]]] | None = None,
    site_context: str | None = None,
    allowed_ground_by_context: dict[str, set[str]] | None = None,
    ground_y: tuple[int, ...] | None = None,
) -> LintResult:
    """`ground_y` is the caller's explicit declaration of the template's real
    grade level, passed through to `check_structural_connectivity`.

    That check's default — anchor on the template's own lowest solid layer —
    is right for ordinary buildings but wrong for a template that models an
    excavation. In a quarry or open pit the lowest solid layer is the *pit
    floor*, tens of blocks below the grade the site's yard buildings, haul
    road and plant actually stand on, so every at-grade structure is reported
    as floating. The check's docstring already anticipates this ("anchor off
    of it unless a caller explicitly knows better"); this parameter is how a
    caller says so, and it is the only supported way to do it — a site that
    declares a grade must still build a real ground course at that level, or
    the structures on it are floating above a declared plane and the check
    reports them exactly as before.
    """
    result = LintResult(structure_id=structure_id)
    result.findings.extend(check_structural_connectivity(size, positions, ground_y=ground_y))
    result.findings.extend(check_stairs_ladders_signs(size, positions))
    result.findings.extend(check_openings_wall_coupled(size, positions))
    result.findings.extend(check_ground_plane(size, positions, allowed_by_context=allowed_ground_by_context, site_context=site_context))
    result.findings.extend(check_room_composition(size, positions))
    if clean_master_positions is not None:
        result.findings.extend(check_damage_coherence(clean_master_positions, positions))
    return result


def _main(argv: list[str]) -> int:
    """Standalone entry point: lint every .nbt under a structures directory.

    Usage: python structure_geometry_lint.py <structures_dir> [report.json]

    Requires convert_nbt_to_lostcities.load_structure to be importable
    (run from the repository's scripts/ directory, matching how
    audit_structure_block_fitness.py already imports it) and its return
    shape to match `positions_from_load_structure`'s assumption — adjust
    that adapter first if it does not.
    """
    if len(argv) < 2:
        print(__doc__)
        return 2
    structures_dir = Path(argv[1])
    report_path = Path(argv[2]) if len(argv) > 2 else Path("structure-geometry-lint-report.json")

    try:
        from convert_nbt_to_lostcities import load_structure  # type: ignore
    except ImportError as exc:  # pragma: no cover - environment-dependent
        print(f"error: could not import convert_nbt_to_lostcities.load_structure ({exc})", file=sys.stderr)
        print("run this from the repository's scripts/ directory", file=sys.stderr)
        return 1

    # Grade declarations for templates that model an excavation. Without these
    # the standalone scan re-derives grade from the lowest solid layer, which
    # for a pit template is the excavated floor, and reports the entire
    # at-grade site as floating. See the file's own rationale block: a
    # declaration names the plane, it does not waive the requirement to build
    # ground there.
    declarations: dict[str, Any] = {}
    for candidate in (
        Path(__file__).resolve().parents[1] / "structure_library" / "structure-grade-declarations.json",
    ):
        if candidate.is_file():
            declarations = json.loads(candidate.read_text(encoding="utf-8")).get("declarations", {})
            break

    results: list[dict[str, Any]] = []
    hard_fail_structures = 0
    for path in sorted(structures_dir.rglob("*.nbt")):
        structure_id = path.relative_to(structures_dir).with_suffix("").as_posix()
        size, blocks = load_structure(path)  # type: ignore[misc]
        positions = positions_from_load_structure(size, blocks)
        declared = declarations.get(structure_id) or declarations.get(Path(structure_id).name)
        ground_y = tuple(declared["ground_y"]) if declared else None
        result = lint_structure(structure_id, size, positions, ground_y=ground_y)
        if not result.passed:
            hard_fail_structures += 1
        results.append(result.to_dict())

    report_path.write_text(json.dumps({
        "templates_scanned": len(results),
        "structures_with_hard_fail": hard_fail_structures,
        "results": results,
    }, indent=2) + "\n", encoding="utf-8")
    print(f"scanned {len(results)} structures; {hard_fail_structures} have hard-fail geometry findings")
    print(f"report written to {report_path}")
    return 1 if hard_fail_structures else 0


if __name__ == "__main__":
    raise SystemExit(_main(sys.argv))
