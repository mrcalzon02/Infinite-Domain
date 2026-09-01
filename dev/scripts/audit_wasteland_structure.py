"""Per-building deep audit for the Wasteland structure rebuild pass.

`structure_geometry_lint.py` (checks 1-6) is the mechanical production gate and
stays authoritative for pass/fail. This module is the *detailed rebuild audit*
layer on top of it: it runs the lint against a structure's clean master AND its
damage variant, wires the master<->variant damage-coherence comparison the
standalone lint runner never invokes, and adds three detectors aimed at the
defect classes a human reviewer keeps reporting that the lint's connectivity /
opening / stair checks do not see:

  A. massing monotony      - the building still reads as a flat unarticulated
                             cuboid: one roof plane, one wall plane per face,
                             no setback / projection / step.
  B. slab-in-wall clipping - a slab or stair block buried inside a wall volume
                             (v2 doc S1: "slab roofs intruding into wall
                             volumes, leaving structural gaps").
  C. terrain-gen-mismatch  - "damage" that is a clean axis-aligned box cut, or a
     damage                  void backfilled with a compact single-material
                             pile-block cuboid with a flat top. That is not a
                             collapse; it is a procedural / terrain-generation
                             artifact. Real collapse debris drapes, slopes and
                             spills below a breach - it is not a filled cube.

Authority: docs/WASTELAND_STRUCTURE_REBUILD_AUDIT.md
Usage:     python scripts/audit_wasteland_structure.py <structure_id> [<id> ...]
           python scripts/audit_wasteland_structure.py --all
Run from the repository's scripts/ directory (same as audit_structure_block_fitness.py).
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import structure_geometry_lint as L

Pos = tuple[int, int, int]

REPO = Path(__file__).resolve().parents[2]
WASTELAND = REPO / "kubejs" / "data" / "infinite_domain" / "structure" / "wasteland"
MASTERS = WASTELAND / "masters"
OUT_DIR = REPO / "dev/docs" / "wasteland-rebuild-audit"

# Damage / collapse debris that is legitimately loose granular material. A
# component made almost entirely of these, if it is also compact and flat-
# topped, is the "pile of gravel that is just a cube" artifact.
PILE_MATERIALS = (
    "gravel", "sand", "coarse_dirt", "rooted_dirt", "dirt", "clay", "mud",
    "cobblestone", "mossy_cobblestone", "blackstone", "tuff", "scoria",
    "rubble", "scrap", "debris", "ash", "soul_sand", "soul_soil",
)

NEIGHBORS_6 = L.NEIGHBORS_6


# ---------------------------------------------------------------------------
# loading
# ---------------------------------------------------------------------------


def _load(path: Path) -> tuple[tuple[int, int, int], dict[Pos, tuple[str, dict[str, str]]]]:
    from convert_nbt_to_lostcities import load_structure  # type: ignore

    size, blocks = load_structure(path)
    return tuple(size), L.positions_from_load_structure(size, blocks)


def resolve_paths(structure_id: str) -> tuple[Path | None, Path | None, str]:
    """Return (clean_master_path, variant_path, rebase_note).

    Per docs/WASTELAND_STRUCTURE_REBUILD_AUDIT.md: if no clean master exists,
    the damage variant is the rebase source and is audited in its place.
    """
    variant = WASTELAND / f"{structure_id}.nbt"
    variant = variant if variant.is_file() else None

    for stem in (f"{structure_id}_clean_master", f"{structure_id.removeprefix('abandoned_').removeprefix('ruined_').removeprefix('decayed_').removeprefix('dilapidated_')}_clean_master"):
        cand = MASTERS / f"{stem}.nbt"
        if cand.is_file():
            return cand, variant, ""
        cand = WASTELAND / f"{stem}.nbt"
        if cand.is_file():
            return cand, variant, ""
    return None, variant, "no clean master on disk - damage variant used as rebase source"


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def _solid(positions: dict[Pos, tuple[str, dict[str, str]]]) -> set[Pos]:
    return {p for p, (n, _) in positions.items() if L._is_solid(n) and not L._is_face_attached(n)}


def _components(cells: set[Pos]) -> list[list[Pos]]:
    seen: set[Pos] = set()
    out: list[list[Pos]] = []
    for start in cells:
        if start in seen:
            continue
        comp = [start]
        seen.add(start)
        stack = [start]
        while stack:
            x, y, z = stack.pop()
            for dx, dy, dz in NEIGHBORS_6:
                n = (x + dx, y + dy, z + dz)
                if n in cells and n not in seen:
                    seen.add(n)
                    comp.append(n)
                    stack.append(n)
        out.append(comp)
    return out


def _bbox(cells: list[Pos] | set[Pos]) -> tuple[Pos, Pos, int]:
    xs = [p[0] for p in cells]
    ys = [p[1] for p in cells]
    zs = [p[2] for p in cells]
    lo = (min(xs), min(ys), min(zs))
    hi = (max(xs), max(ys), max(zs))
    vol = (hi[0] - lo[0] + 1) * (hi[1] - lo[1] + 1) * (hi[2] - lo[2] + 1)
    return lo, hi, vol


def _is_pile(name: str) -> bool:
    return any(term in name for term in PILE_MATERIALS)


# ---------------------------------------------------------------------------
# A. massing monotony
# ---------------------------------------------------------------------------


def analyze_massing(size: tuple[int, int, int], positions: dict[Pos, tuple[str, dict[str, str]]]) -> list[dict[str, Any]]:
    """Per-building (not per-site) flat-cuboid detector.

    A site's perimeter fence, pads and separate buildings all touch at grade,
    so connectivity over every wall block yields one site-spanning component
    that is never "flat". Segment instead on wall material at y >= 4 (above
    fence height, below which buildings are joined only by ground), then test
    each building-sized component for a single flat roof plane plus flat
    facades.
    """
    findings: list[dict[str, Any]] = []
    upper_walls = {p for p, (n, pr) in positions.items() if L._is_wall_material(n, pr) and p[1] >= 4}
    if len(upper_walls) < 150:
        return findings
    for comp in _components(upper_walls):
        if len(comp) < 400:
            continue
        lo, hi, _ = _bbox(comp)
        fx, fz, height = hi[0] - lo[0] + 1, hi[1] - lo[1] + 1, hi[2] - lo[2] + 1
        if not (12 <= fx <= 44 and 12 <= fz <= 44 and height >= 5):
            continue

        top_y: dict[tuple[int, int], int] = {}
        for (x, y, z) in comp:
            if y > top_y.get((x, z), -1):
                top_y[(x, z)] = y
        if len(top_y) < 90:
            continue
        rc = Counter(top_y.values())
        modal_roof, modal_roof_n = rc.most_common(1)[0]
        roof_flat = modal_roof_n / len(top_y)

        def face_flat(vary_axis: int, face_axis: int, side: str) -> tuple[float, int]:
            depth: dict[tuple[int, int], int] = {}
            for p in comp:
                k = (p[vary_axis], p[1])
                d = p[face_axis] if side == "min" else -p[face_axis]
                if k not in depth or d < depth[k]:
                    depth[k] = d
            if len(depth) < 40:
                return 0.0, 0
            cc = Counter(depth.values())
            return cc.most_common(1)[0][1] / len(depth), len(depth)

        faces = {
            "north": face_flat(0, 2, "min"), "south": face_flat(0, 2, "max"),
            "west": face_flat(2, 0, "min"), "east": face_flat(2, 0, "max"),
        }
        flat_faces = {f: fr for f, (fr, n) in faces.items() if fr >= 0.88 and n >= 40}

        if roof_flat >= 0.88 and len(flat_faces) >= 3:
            findings.append({
                "check": "massing_monotony", "severity": "review_flag", "position": list(lo),
                "detail": (
                    f"building mass {fx}x{height}x{fz} at {tuple(lo)} reads as a flat cuboid: roof {roof_flat:.0%} one "
                    f"plane (y={modal_roof}); {len(flat_faces)}/4 facades >=88% a single wall plane "
                    f"({', '.join(f'{k} {v:.0%}' for k, v in sorted(flat_faces.items()))}). "
                    "Needs setbacks, projecting bays, a pitched/stepped roofline or depth relief."
                ),
            })
        elif roof_flat >= 0.95 and len(flat_faces) >= 1:
            findings.append({
                "check": "massing_monotony", "severity": "review_flag", "position": list(lo),
                "detail": f"roof of the {fx}x{fz} building at {tuple(lo)} is {roof_flat:.0%} a single flat plane (y={modal_roof}) with {len(flat_faces)} flat facade(s) - little roofline/facade articulation.",
            })
    return findings


# ---------------------------------------------------------------------------
# B. slab / stair buried in a wall volume
# ---------------------------------------------------------------------------


def analyze_slab_wall_penetration(positions: dict[Pos, tuple[str, dict[str, str]]], *, max_reported: int = 30) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    hits: list[Pos] = []
    for (x, y, z), (name, _pr) in positions.items():
        is_slab = name.endswith("_slab")
        is_stair = name.endswith("_stairs")
        if not (is_slab or is_stair):
            continue
        up = positions.get((x, y + 1, z), ("minecraft:air", {}))
        dn = positions.get((x, y - 1, z), ("minecraft:air", {}))
        # A slab/stair fully enclosed by wall material - above, below and on 3+
        # of the 4 horizontal sides - is not a ledge, step, eave or string
        # course (all of which leave the outward face open). It is a slab
        # occupying a cell where a full wall block belongs: the "slab roof
        # intruding into the wall volume" defect, leaving a half-block gap.
        if L._is_wall_material(up[0], up[1]) and L._is_wall_material(dn[0], dn[1]):
            n_wall = sum(
                1 for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1))
                if L._is_wall_material(*positions.get((x + dx, y, z + dz), ("minecraft:air", {})))
            )
            if n_wall == 4:
                hits.append((x, y, z))
    for p in sorted(hits)[:max_reported]:
        findings.append({
            "check": "slab_wall_penetration",
            "severity": "review_flag",
            "position": list(p),
            "detail": f"{positions[p][0]} at {p} is fully boxed in by wall material on all 6 faces - a slab where a full wall block belongs, leaving a half-block void in the wall.",
        })
    if len(hits) > max_reported:
        findings.append({
            "check": "slab_wall_penetration",
            "severity": "review_flag",
            "position": None,
            "detail": f"{len(hits) - max_reported} further slab/stair-in-wall hits not listed ({len(hits)} total).",
        })
    return findings


# ---------------------------------------------------------------------------
# C. terrain-generation-mismatch damage
# ---------------------------------------------------------------------------


def analyze_terrain_mismatch_damage(
    clean: dict[Pos, tuple[str, dict[str, str]]],
    variant: dict[Pos, tuple[str, dict[str, str]]],
) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    clean_solid = _solid(clean)
    variant_solid = _solid(variant)

    removed = clean_solid - variant_solid
    added = variant_solid - clean_solid

    # --- C1: clean rectangular excisions (box cut, not a fracture) ----------
    for comp in _components(removed):
        if len(comp) < 24:
            continue
        lo, hi, vol = _bbox(comp)
        fill = len(comp) / vol
        if fill < 0.92:
            continue
        cs = set(comp)
        faces_flat = 0
        for axis in range(3):
            for bound in (lo[axis], hi[axis]):
                plane = [p for p in comp if p[axis] == bound]
                # every in-plane cell of the bbox present on this face?
                oa = [i for i in range(3) if i != axis]
                span = (hi[oa[0]] - lo[oa[0]] + 1) * (hi[oa[1]] - lo[oa[1]] + 1)
                if len(plane) >= 0.9 * span:
                    faces_flat += 1
        if faces_flat >= 5:
            findings.append({
                "check": "terrain_mismatch_damage",
                "severity": "review_flag",
                "position": list(lo),
                "detail": (
                    f"removed volume {lo}->{hi} ({len(comp)} blocks) fills {fill:.0%} of its box with "
                    f"{faces_flat}/6 flat axis-aligned faces - a clean rectangular excision (t.clear box), "
                    "not an authored fracture with an irregular boundary."
                ),
            })

    # --- C2: compact single-material pile-block backfill -------------------
    footprint = {(p[0], p[2]) for p in clean_solid}
    clean_top: dict[tuple[int, int], int] = {}
    for (x, y, z) in clean_solid:
        if y > clean_top.get((x, z), -1):
            clean_top[(x, z)] = y

    for comp in _components(added):
        if len(comp) < 12:
            continue
        names = Counter(variant[p][0] for p in comp)
        top_name, top_n = names.most_common(1)[0]
        mono = top_n / len(comp)
        if not (_is_pile(top_name) and mono >= 0.75):
            continue
        lo, hi, vol = _bbox(comp)
        fill = len(comp) / vol
        # flat top?
        col_top: dict[tuple[int, int], int] = {}
        for (x, y, z) in comp:
            if y > col_top.get((x, z), -1):
                col_top[(x, z)] = y
        tc = Counter(col_top.values())
        flat_top = tc.most_common(1)[0][1] / len(col_top)
        # inside / above the building footprint, not draped at its base?
        inside = sum(1 for (x, y, z) in comp if (x, z) in footprint) / len(comp)
        above_grade = sum(1 for (x, y, z) in comp if y >= clean_top.get((x, z), 0) - 1) / len(comp)

        if fill >= 0.7 and flat_top >= 0.7 and inside >= 0.55:
            findings.append({
                "check": "terrain_mismatch_damage",
                "severity": "review_flag",
                "position": list(lo),
                "detail": (
                    f"added debris {lo}->{hi} is {mono:.0%} {top_name}, fills {fill:.0%} of its box, "
                    f"top is {flat_top:.0%} one Y, {inside:.0%} inside the footprint, {above_grade:.0%} at/above roof line - "
                    "reads as a solid pile-block cuboid dropped into the structure (procedural backfill), not gravity-settled collapse debris."
                ),
            })

    # --- C3: roof punched then capped with a pile block -------------------
    roof_removed = {p for p in removed if p[1] >= clean_top.get((p[0], p[2]), 0) - 2}
    for comp in _components(roof_removed):
        if len(comp) < 6:
            continue
        lo, hi, _ = _bbox(comp)
        capped = 0
        for (x, y, z) in comp:
            for yy in range(y, y + 4):
                nm = variant.get((x, yy, z), ("minecraft:air", {}))[0]
                if L._is_solid(nm) and _is_pile(nm):
                    capped += 1
                    break
        if capped >= 0.4 * len(comp):
            findings.append({
                "check": "terrain_mismatch_damage",
                "severity": "review_flag",
                "position": list(lo),
                "detail": (
                    f"roof hole {lo}->{hi} ({len(comp)} blocks) is capped/filled by pile-block material on "
                    f"{capped}/{len(comp)} columns - the roof was cut and the void patched with terrain material "
                    "rather than left open with debris fallen to the floor below."
                ),
            })

    # --- C4: does any breach have a gravity-consistent apron at all? ------
    if removed and not added:
        findings.append({
            "check": "terrain_mismatch_damage",
            "severity": "review_flag",
            "position": None,
            "detail": f"{len(removed)} blocks removed vs clean master but the variant adds zero debris - subtraction-only damage, no rubble, no story.",
        })
    return findings


# ---------------------------------------------------------------------------
# runner
# ---------------------------------------------------------------------------


def audit(structure_id: str) -> dict[str, Any]:
    master_path, variant_path, rebase_note = resolve_paths(structure_id)
    report: dict[str, Any] = {
        "structure_id": structure_id,
        "clean_master": master_path.relative_to(REPO).as_posix() if master_path else None,
        "variant": variant_path.relative_to(REPO).as_posix() if variant_path else None,
        "rebase_note": rebase_note,
        "clean_master_lint": None,
        "variant_lint": None,
        "audit_findings": [],
    }

    mpos = None
    if master_path:
        msize, mpos = _load(master_path)
        mres = L.lint_structure(f"{structure_id}_clean_master", msize, mpos)
        report["clean_master_lint"] = mres.to_dict()
        report["audit_findings"] += analyze_massing(msize, mpos)
        report["audit_findings"] += analyze_slab_wall_penetration(mpos)

    if variant_path:
        vsize, vpos = _load(variant_path)
        vres = L.lint_structure(structure_id, vsize, vpos, clean_master_positions=mpos)
        report["variant_lint"] = vres.to_dict()
        if mpos is None:
            report["audit_findings"] += analyze_massing(vsize, vpos)
            report["audit_findings"] += analyze_slab_wall_penetration(vpos)
        else:
            report["audit_findings"] += analyze_terrain_mismatch_damage(mpos, vpos)

    report["summary"] = _summarize(report)
    return report


def _summarize(report: dict[str, Any]) -> dict[str, Any]:
    def hf(lint: dict[str, Any] | None) -> int:
        return lint["hard_fail_count"] if lint else 0

    by_check: Counter[str] = Counter()
    for f in report["audit_findings"]:
        by_check[f["check"]] += 1
    for key in ("clean_master_lint", "variant_lint"):
        for f in (report[key]["findings"] if report[key] else []):
            by_check[f"lint:{f['check']}:{f['severity']}"] += 1
    return {
        "clean_master_hard_fail": hf(report["clean_master_lint"]),
        "variant_hard_fail": hf(report["variant_lint"]),
        "audit_flag_count": len(report["audit_findings"]),
        "by_check": dict(by_check.most_common()),
    }


def _all_ids() -> list[str]:
    return sorted(p.stem for p in WASTELAND.glob("*.nbt"))


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    ids = _all_ids() if argv[1] == "--all" else argv[1:]
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    worst: list[tuple[int, str]] = []
    for sid in ids:
        rep = audit(sid)
        (OUT_DIR / f"{sid}.json").write_text(json.dumps(rep, indent=2) + "\n", encoding="utf-8")
        s = rep["summary"]
        worst.append((s["clean_master_hard_fail"] + s["variant_hard_fail"] + s["audit_flag_count"], sid))
        print(f"\n=== {sid} ===")
        if rep["rebase_note"]:
            print(f"  ! {rep['rebase_note']}")
        print(f"  clean-master hard-fail: {s['clean_master_hard_fail']}   variant hard-fail: {s['variant_hard_fail']}   audit flags: {s['audit_flag_count']}")
        for k, v in s["by_check"].items():
            print(f"    {v:4}  {k}")
        for f in rep["audit_findings"]:
            print(f"    - [{f['check']}] {f['detail']}")
    if len(ids) > 1:
        print("\n--- worst first ---")
        for score, sid in sorted(worst, reverse=True):
            print(f"  {score:5}  {sid}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
