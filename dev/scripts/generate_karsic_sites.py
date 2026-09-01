#!/usr/bin/env python3
"""Generate Karsic Directorate clean masters from their program files.

Mirrors scripts/generate_wasteland_sites.py in role: it is the driver that
turns authored data into .nbt structures. Everything it needs comes from files
that already passed their own gates:

    structure_library/regional/karsic-assignment.json        (P0, validated)
    structure_library/programs/kar_*.json                    (P1, validated)
    structure_library/regional/karsic-material-profile.json  (P3, validated)
    structure_library/regional/karsic-massing-grammar.json   (P2 constants)

Passes P2 (massing) and P4 (envelope) are implemented in
scripts/regional/karsic_massing.py. Building types without a builder yet are
reported as pending rather than emitted as placeholder geometry - a placeholder
that reaches the corpus is exactly how the previous 84 assets had to be reset.

Authority: docs/KARSIC_DIRECTORATE_STRUCTURE_PROGRAM.md sections 8, 11.1, 14

Usage:
    python scripts/generate_karsic_sites.py --list
    python scripts/generate_karsic_sites.py --family KF1 KF2
    python scripts/generate_karsic_sites.py --id kar_067_series_panel_block
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "dev/scripts"))

import generate_wasteland_sites as base  # noqa: E402  (Template + NBT writer)
import convert_nbt_to_lostcities as converter  # noqa: E402
from regional import BuildContext, MaterialProfile, load_grammar, load_program  # noqa: E402
from regional import karsic_massing as massing  # noqa: E402
from regional import karsic_damage as damage  # noqa: E402
from build_regional_programs import KARSIC_FAMILIES  # noqa: E402

CULTURE = "karsic"
OUT_MASTERS = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "karsic" / "masters"
OUT_VARIANTS = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "karsic"
REPORT = ROOT / "dev/docs" / "karsic-generation-report.json"
ASSIGNMENT = ROOT / "dev/structure_library" / "regional" / f"{CULTURE}-assignment.json"


def assert_converter_contract(grammar: dict[str, Any]) -> None:
    """The repeatable-storey feature is built on a constant in the converter.

    If FLOOR_HEIGHT ever changes, every Karsic residential asset silently
    breaks, so fail loudly here rather than discovering it in-world.
    """
    expected = int(grammar["modules"]["converter_floor_height_assertion"])
    if converter.FLOOR_HEIGHT != expected:
        raise SystemExit(
            f"convert_nbt_to_lostcities.FLOOR_HEIGHT is {converter.FLOOR_HEIGHT}, "
            f"but the Karsic massing grammar is built on {expected}. "
            f"Fix the grammar or the converter before generating."
        )


def size_for(ctx: BuildContext, program: dict[str, Any]) -> None:
    meta = program.get("source_metadata") or {}
    footprint = meta.get("base_footprint") or {}
    width = int(footprint.get("width", 40))
    depth = int(footprint.get("depth", 36))
    height = int(meta.get("base_height", 18))
    building_type = program["building_type"]

    if building_type == "kiosk":
        ctx.bays_x, ctx.bays_z, ctx.storeys, ctx.ground_y = 2, 2, 1, 0
        ctx.size = (ctx.bays_x * ctx.bay + 2 * massing.MARGIN + 6,
                    12,
                    ctx.bays_z * ctx.bay + 2 * massing.MARGIN + 6)
    elif building_type == "bus_shelter":
        # Thirteen blocks of open frontage on a shallow shelter bay, with
        # enough lot behind it for terrain adaptation and the route post.
        ctx.bays_x, ctx.bays_z, ctx.storeys, ctx.ground_y = 3, 1, 1, 0
        ctx.size = (ctx.bays_x * ctx.bay + 2 * massing.MARGIN + 1,
                    10,
                    ctx.bays_z * ctx.bay + 2 * massing.MARGIN + 5)
    elif building_type == "linear_infrastructure":
        ctx.bays_x, ctx.bays_z, ctx.storeys, ctx.ground_y = 8, 4, 1, 0
        ctx.size = (32, 14, 16)
    elif building_type == "mast_tower":
        # Preserve the compact relay lot while allowing the water tower's
        # deliberately broad civic compound.
        lot = max(27, min(45, max(width, depth)))
        ctx.bays_x = ctx.bays_z = max(4, (lot - 8) // ctx.bay)
        ctx.storeys, ctx.ground_y = 1, 0
        ctx.size = (lot, max(34, min(48, height + 8)), lot)
    elif building_type == "retail_plinth":
        massing.size_retail_plinth(ctx, width, depth, height)
    else:
        massing.size_panel_slab(ctx, width, depth, height)


def write_template(path: Path, template: Any, size: tuple[int, int, int]) -> Counter[str]:
    path.parent.mkdir(parents=True, exist_ok=True)
    root = {
        "DataVersion": base.DATA_VERSION,
        "size": base.NbtList(base.TAG_INT, list(size)),
        "palette": base.NbtList(base.TAG_COMPOUND, template.palette),
        "blocks": base.NbtList(base.TAG_COMPOUND, [
            {"pos": base.NbtList(base.TAG_INT, list(pos)), "state": state,
             **({"nbt": nbt} if nbt else {})}
            for pos, (state, nbt) in sorted(template.blocks.items(),
                                            key=lambda row: (row[0][1], row[0][2], row[0][0]))
        ]),
        "entities": base.NbtList(base.TAG_COMPOUND, template.entities),
    }
    base.write_nbt(path, root)
    return Counter(template.palette[state]["Name"] for state, _ in template.blocks.values())


def generate_one(structure_id: str, profile: MaterialProfile, grammar: dict[str, Any]) -> dict[str, Any]:
    program = load_program(structure_id)
    building_type = program["building_type"]
    builder = massing.builder_for(structure_id, building_type)
    if builder is None:
        return {"structure_id": structure_id, "building_type": building_type, "status": "pending_builder"}

    ctx = BuildContext(
        culture=CULTURE,
        structure_id=structure_id,
        program=program,
        profile=profile,
        grammar=grammar,
        variant="clean_master",
    )
    size_for(ctx, program)
    template = base.Template(ctx.size)
    builder(ctx, template)

    path = OUT_MASTERS / f"{structure_id}_clean_master.nbt"
    counts = write_template(path, template, ctx.size)
    result = {
        "structure_id": structure_id,
        "building_type": building_type,
        "status": "generated",
        "primary_stratum": ctx.primary,
        "size": list(ctx.size),
        "bays": [ctx.bays_x, ctx.bays_z],
        "storeys": ctx.storeys,
        "ground_y": ctx.ground_y,
        "repeatable_storey": program.get("repeatable_storey", False),
        "placed_blocks": len(template.blocks),
        "palette_states": len(template.palette),
        "modded_blocks": sum(c for b, c in counts.items() if not b.startswith("minecraft:")),
        "path": path.relative_to(ROOT).as_posix(),
    }
    if damage.supports(structure_id):
        variant_ctx = BuildContext(
            culture=CULTURE,
            structure_id=structure_id,
            program=program,
            profile=profile,
            grammar=grammar,
            variant="damage_variant",
        )
        size_for(variant_ctx, program)
        variant = base.Template(variant_ctx.size)
        builder(variant_ctx, variant)
        damage.apply(variant_ctx, variant)
        variant_path = OUT_VARIANTS / f"{structure_id}.nbt"
        variant_counts = write_template(variant_path, variant, variant_ctx.size)
        result.update({
            "damage_variant_path": variant_path.relative_to(ROOT).as_posix(),
            "damage_variant_blocks": len(variant.blocks),
            "damage_variant_palette_states": len(variant.palette),
            "damage_variant_modded_blocks": sum(
                count for block, count in variant_counts.items() if not block.startswith("minecraft:")
            ),
        })
    return result


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--family", nargs="*", help="families to build, e.g. KF1 KF2")
    parser.add_argument("--id", nargs="*", help="explicit structure ids")
    parser.add_argument("--list", action="store_true", help="show builder coverage and exit")
    args = parser.parse_args()

    assignment = json.loads(ASSIGNMENT.read_text(encoding="utf-8"))
    all_ids = [e["regional_id"] for e in assignment["conversions"] if e["conversion_class"] != "X"]
    all_ids += [n["regional_id"] for n in assignment["natives"]]
    all_ids.sort()

    if args.list:
        pending: Counter[str] = Counter()
        ready: Counter[str] = Counter()
        for sid in all_ids:
            bt = load_program(sid)["building_type"]
            (ready if massing.builder_for(sid, bt) is not None else pending)[bt] += 1
        print(f"building types with a builder ({sum(ready.values())} masters):")
        for name, count in sorted(ready.items()):
            print(f"  {name:<24} {count}")
        print(f"\nbuilding types still pending ({sum(pending.values())} masters):")
        for name, count in sorted(pending.items(), key=lambda kv: (-kv[1], kv[0])):
            print(f"  {name:<24} {count}")
        return 0

    selected: list[str] = []
    if args.id:
        selected += args.id
    if args.family:
        prefixes: set[str] = set()
        for family in args.family:
            members = KARSIC_FAMILIES.get(family)
            if members is None:
                parser.error(f"unknown family {family}")
            prefixes.update(members)
        selected += [sid for sid in all_ids if "_".join(sid.split("_")[:2]) in prefixes]
    if not selected:
        selected = all_ids
    selected = sorted(dict.fromkeys(selected))

    grammar = load_grammar(CULTURE)
    assert_converter_contract(grammar)
    profile = MaterialProfile(CULTURE)

    results = [generate_one(sid, profile, grammar) for sid in selected]
    selected_generated = [r for r in results if r["status"] == "generated"]
    selected_pending = [r for r in results if r["status"] == "pending_builder"]

    # The record is durable: a run that builds one structure must not erase the
    # record of the others, or downstream validators lose their metadata.
    previous: dict[str, Any] = {}
    if REPORT.exists():
        previous = {r["structure_id"]: r
                    for r in json.loads(REPORT.read_text(encoding="utf-8")).get("results", [])}
    for result in results:
        previous[result["structure_id"]] = result
    results = [previous[key] for key in sorted(previous)]
    durable_generated = [r for r in results if r["status"] == "generated"]
    durable_pending = [r for r in results if r["status"] == "pending_builder"]

    report = {
        "purpose": "Karsic clean-master generation record. Generation is not production approval; "
                   "assets must still pass scripts/structure_geometry_lint.py checks 1-3 and the "
                   "regional structure checks before any approval is recorded.",
        "authority": "docs/KARSIC_DIRECTORATE_STRUCTURE_PROGRAM.md",
        "culture": CULTURE,
        "selected": len(selected),
        "generated": len(durable_generated),
        "pending_builder": len(durable_pending),
        "pending_building_types": sorted({r["building_type"] for r in durable_pending}),
        "results": results,
    }
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8", newline="\n")

    # Console output describes this invocation; the JSON remains the durable
    # union used by downstream validators.
    for result in selected_generated:
        print(f"OK      {result['structure_id']:<40} {result['building_type']:<22} "
              f"{'x'.join(str(v) for v in result['size']):<14} "
              f"{result['placed_blocks']:>6} blocks  {result['palette_states']:>3} states")
    for result in selected_pending:
        print(f"PENDING {result['structure_id']:<40} {result['building_type']} (no builder yet)")
    print()
    print(
        f"generated {len(selected_generated)}, pending {len(selected_pending)}, "
        f"of {len(selected)} selected"
    )
    print(f"report: {REPORT.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
