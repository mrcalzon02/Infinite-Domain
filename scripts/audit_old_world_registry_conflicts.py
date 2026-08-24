#!/usr/bin/env python3
"""[SYSTEM REPORT] Guard the canonical Old World proof registry against duplicate startup registration."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "kubejs" / "config" / "old_world_evidence.json"
STARTUP = ROOT / "kubejs" / "startup_scripts"
AUTHORITATIVE = STARTUP / "old_world_evidence_items.js"
TEXTURES = ROOT / "kubejs" / "assets" / "kubejs" / "textures" / "item"
CREATE_RE = re.compile(r"event\.create\(\s*['\"]([^'\"]+)['\"]\s*\)")


def main() -> None:
    document = json.loads(REGISTRY.read_text(encoding="utf-8"))
    items = document.get("items", [])
    proof_ids = [item["id"] for item in items]
    if len(proof_ids) != 64 or len(set(proof_ids)) != 64:
        raise SystemExit(f"Canonical Old World registry must contain 64 unique IDs; found {len(proof_ids)} entries / {len(set(proof_ids))} unique")

    collisions: list[str] = []
    for path in sorted(STARTUP.glob("*.js")):
        if path == AUTHORITATIVE:
            continue
        text = path.read_text(encoding="utf-8-sig")
        for item_id in CREATE_RE.findall(text):
            if item_id in proof_ids:
                collisions.append(f"{path.relative_to(ROOT)} -> {item_id}")

    present_textures = [item_id for item_id in proof_ids if (TEXTURES / f"{item_id}.png").is_file()]
    print(f"Old World canonical proof IDs: {len(proof_ids)}/64")
    print(f"Proof IDs registered outside canonical startup file: {len(collisions)}")
    print(f"Authored proof textures present: {len(present_textures)}/64")

    if collisions:
        raise SystemExit("Duplicate Old World proof registration detected:\n" + "\n".join(collisions))


if __name__ == "__main__":
    main()
