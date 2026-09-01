#!/usr/bin/env python3
"""Target-local mechanical validation for the pure OWS-010 final builder."""
from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import generate_wasteland_sites as base
import old_world_ows010_final as final


ROOT = Path(__file__).resolve().parents[2]
TEMP_DIR = ROOT / "kubejs/data/infinite_domain/structure/wasteland"


def name_at(t: base.Template, pos: tuple[int, int, int]) -> str | None:
    row = t.blocks.get(pos)
    return None if row is None else t.palette[row[0]]["Name"]


def serialize_hash(t: base.Template, name: str) -> str:
    path = TEMP_DIR / f"{name}.nbt"
    t.save(name)
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    finally:
        path.unlink(missing_ok=True)


def main() -> None:
    source_path = ROOT / "dev/scripts/old_world_ows010_final.py"
    source = source_path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module or "")
    forbidden = [name for name in imports if name.startswith("render_") or "review" in name]
    if forbidden:
        raise AssertionError(f"production builder imports render/review modules: {forbidden}")
    allowed = {"__future__", "generate_wasteland_sites"}
    unexpected = [name for name in imports if name not in allowed]
    if unexpected:
        raise AssertionError(f"production builder has unexpected imports: {unexpected}")

    accepted = final.build_accepted_d3()
    final._assert_accepted_d3_contracts(accepted)
    accepted_hash = serialize_hash(accepted, "_validate_ows010_accepted_d3")
    if accepted_hash != final.ACCEPTED_GATE_C_D3_SHA256:
        raise AssertionError(
            f"pure accepted-D3 reproduction drifted: {accepted_hash} != {final.ACCEPTED_GATE_C_D3_SHA256}"
        )

    built = final.build_010()
    final._assert_final_contracts(built)
    raw_hash = serialize_hash(built, "_validate_ows010_final_raw")

    all_positions = set(accepted.blocks) | set(built.blocks)
    delta = {pos for pos in all_positions if name_at(accepted, pos) != name_at(built, pos)}
    if delta != set(final.PASS19_MICRODETAIL):
        raise AssertionError(f"Pass-19 delta drifted: {sorted(delta)}")
    for pos in delta:
        if name_at(accepted, pos) not in final.AIR:
            raise AssertionError(f"Pass-19 replaced accepted D3 at {pos}")
    modded_additions = {
        pos: block for pos, block in final.PASS19_MICRODETAIL.items()
        if not block.startswith("minecraft:")
    }
    if modded_additions:
        raise AssertionError(f"Pass-19 must remain vanilla-only: {modded_additions}")

    stabilized = final.build_010()
    before = {pos: name_at(stabilized, pos) for pos in stabilized.blocks}
    base.stabilize_door_pairs(stabilized)
    stabilization_delta = {
        pos for pos in set(before) | set(stabilized.blocks)
        if before.get(pos) != name_at(stabilized, pos)
    }
    stabilized_hash = serialize_hash(stabilized, "_validate_ows010_final_stabilized")
    metrics = base.fidelity_metrics(stabilized)
    lint = base.assess_fidelity("corporate_warehouse", stabilized)
    if metrics["orphan_door_halves"] != 0:
        raise AssertionError(f"OWS-010 door lint drifted: {metrics}")
    if not lint["structural_lint_passed"] or lint["issues"]:
        raise AssertionError(f"OWS-010 structural lint failed: {lint}")
    for block in final.PRODUCTION_REQUIRED_BLOCKS:
        if final._count(stabilized, block) < 1:
            raise AssertionError(f"required block missing after stabilization: {block}")
    if any(not (0 <= x < 49 and 0 <= y < 16 and 0 <= z < 43) for x, y, z in stabilized.blocks):
        raise AssertionError("stabilized OWS-010 exceeds accepted bounds")
    final._assert_final_contracts(stabilized)

    print("OWS-010 pure final builder validation passed")
    print(f"accepted_d3_sha256={accepted_hash}")
    print(f"final_raw_sha256={raw_hash}")
    print(f"final_stabilized_sha256={stabilized_hash}")
    print(f"pass19_additions={len(delta)} replacements=0 modded_additions=0")
    print(f"stabilization_delta={len(stabilization_delta)} positions={sorted(stabilization_delta)}")
    print(f"source_sha256={hashlib.sha256(source_path.read_bytes()).hexdigest()}")
    print(f"metrics={metrics}")
    print(f"structural_lint={lint}")
    print("required_blocks=" + ",".join(
        f"{block}:{final._count(stabilized, block)}" for block in final.PRODUCTION_REQUIRED_BLOCKS
    ))
    print(f"proof={final.PROOF_POS}:{final.PROOF_LOOT_TABLE}")
    print(f"spawners={final.SPAWNERS}")
    print(f"lor_shelves={final.LOR_SHELVES} manual_absent=True")


if __name__ == "__main__":
    main()
