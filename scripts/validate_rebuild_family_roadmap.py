from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROADMAP = ROOT / "structure_library" / "rebuild-family-roadmap.json"
AUDIT = ROOT / "docs" / "inbuilt-structure-audit.json"


def main() -> None:
    roadmap = json.loads(ROADMAP.read_text(encoding="utf-8"))
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    audit_remaining = {
        name
        for name, record in audit["structures"].items()
        if record["audit_disposition"] == "quarantined_requires_purpose_built_rebuild"
    }
    completed_waves = set(roadmap.get("progress", {}).get("completed_checkpoint_waves", []))
    completed_families = set(roadmap.get("progress", {}).get("completed_families", []))
    assigned = [name for family in roadmap["families"] for name in family["assets"]]
    audited_remaining = [
        name
        for family in roadmap["families"]
        if family["checkpoint_wave"] not in completed_waves
        for name in family["assets"]
    ]
    locally_remaining = [
        name
        for family in roadmap["families"]
        if family["family_id"] not in completed_families
        for name in family["assets"]
    ]
    counts = Counter(assigned)
    duplicates = sorted(name for name, count in counts.items() if count != 1)
    missing = sorted(audit_remaining - set(audited_remaining))
    unexpected = sorted(set(audited_remaining) - audit_remaining)
    wave_assets = {
        wave["wave"]: sum(
            len(family["assets"])
            for family in roadmap["families"]
            if family["checkpoint_wave"] == wave["wave"]
        )
        for wave in roadmap["checkpoint_waves"]
    }
    declared_waves = {wave["wave"]: wave["asset_count"] for wave in roadmap["checkpoint_waves"]}
    issues: list[str] = []
    if duplicates:
        issues.append(f"duplicate assignments: {duplicates}")
    if missing:
        issues.append(f"unassigned rebuilds: {missing}")
    if unexpected:
        issues.append(f"audit/checkpoint assignments already rebuilt or unknown: {unexpected}")
    if len(assigned) != roadmap["baseline"]["remaining_assets"]:
        issues.append(f"roadmap declares {len(assigned)} assignments, expected {roadmap['baseline']['remaining_assets']}")
    if wave_assets != declared_waves:
        issues.append(f"wave counts differ: calculated {wave_assets}, declared {declared_waves}")
    if len(locally_remaining) != roadmap.get("progress", {}).get("remaining_assets"):
        issues.append(
            f"local progress declares {roadmap.get('progress', {}).get('remaining_assets')} remaining, "
            f"but incomplete families contain {len(locally_remaining)}"
        )
    if sum(wave["global_pipeline_runs"] for wave in roadmap["checkpoint_waves"]) != 3:
        issues.append("roadmap must retain exactly three global pipeline checkpoints")
    if issues:
        raise SystemExit("\n".join(issues))
    print(
        f"Validated rebuild roadmap: {len(assigned)} baseline assets, {len(audited_remaining)} audit-pending, "
        f"{len(locally_remaining)} locally unbuilt, {len(roadmap['families'])} families, "
        f"{len(roadmap['checkpoint_waves'])} global checkpoints"
    )


if __name__ == "__main__":
    main()
