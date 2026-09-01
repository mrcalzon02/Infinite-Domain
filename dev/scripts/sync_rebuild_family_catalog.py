from __future__ import annotations

import argparse
import json
from pathlib import Path

from validate_structure_corpus import nbt_size


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "structure_library" / "catalog.json"
SPECS = ROOT / "structure_library" / "rebuild-family-catalog-specs.json"


def entry(spec: dict[str, object], *, master: bool) -> dict[str, object]:
    asset = str(spec["asset"])
    master_name = str(spec["master"])
    name = master_name if master else asset
    relative = (
        f"kubejs/data/infinite_domain/structure/wasteland/masters/{master_name}.nbt"
        if master
        else f"kubejs/data/infinite_domain/structure/wasteland/{asset}.nbt"
    )
    width, height, depth = nbt_size(ROOT / relative)
    result: dict[str, object] = {
        "structure_id": f"infinite_domain:{name}",
        "category": spec["category"],
        "source_role": "clean_master" if master else "damage_variant",
        "source_template": relative,
        "footprint": {"width": width, "depth": depth},
        "height": height,
        "main_entrance": spec["entrance"],
        "secondary_entrances": spec["secondary"],
        "road_connection": spec["road"],
        "minimum_lot": {"width": width + 8, "depth": depth + 8},
        "settlement_types": spec["settlements"],
        "supports_intact": True,
        "supports_damage_variants": True,
        "supports_occupation_variants": True,
        "refinement_intensity": "heavy",
        "source_license": {
            "origin": "Infinite Domain project-generated clean master" if master else "Infinite Domain project-generated source",
            "license": "project-owned",
            "redistributable": True,
        },
        "conversion_target": spec["target"],
        "production_status": "quarantined",
    }
    if master:
        result["derived_variants"] = [f"infinite_domain:{asset}"]
    else:
        result["clean_master"] = f"infinite_domain:{master_name}"
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Idempotently register one completed rebuild family in the structure catalog.")
    parser.add_argument("family")
    args = parser.parse_args()
    specs = json.loads(SPECS.read_text(encoding="utf-8"))["families"]
    if args.family not in specs:
        raise SystemExit(f"Unknown or unfinished catalog family: {args.family}")
    document = json.loads(CATALOG.read_text(encoding="utf-8"))
    additions = [entry(spec, master=variant) for spec in specs[args.family] for variant in (False, True)]
    ids = {row["structure_id"] for row in additions}
    document["structures"] = [row for row in document["structures"] if row.get("structure_id") not in ids] + additions
    CATALOG.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    print(f"Registered {len(additions)} catalog records for {args.family}; catalog now has {len(document['structures'])} records")


if __name__ == "__main__":
    main()
