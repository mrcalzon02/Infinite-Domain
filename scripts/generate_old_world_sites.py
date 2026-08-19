"""Generate Old World narrative structures without mutating the accepted base corpus.

The base generator is imported as the authoritative Template/material API. This
script does not call generate_wasteland_sites.generate(), so rebuilding Old World
content cannot reset the project-owner visual acceptance ledger.

Default mode authors structure NBT, template pools and structure definitions but
NO natural-placement structure sets. Pass --activate-test to register only PT-9
(OWS-006) for controlled end-to-end generation. Pass --activate-vcf after runtime
validation to register both VCF placement families.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import generate_wasteland_sites as G
import old_world_vcf_family as VCF

VCF.configure(G)
DATA = ROOT / "kubejs" / "data" / "infinite_domain"

COMMON = [
    "ows_001_culture_service_depot",
    "ows_002_emergency_grow_annex",
    "ows_003_culture_batch_warehouse",
    "ows_004_mycological_vertical_farm_tower",
    "ows_005_packaging_quality_plant",
]
RESEARCH = [
    "ows_006_pt9_symbiosis_pilot_lab",
    "ows_007_ep7_agricultural_development_lab",
    "ows_008_persistence_incident_lab",
]


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")


def structure_definition(name: str) -> dict:
    return {
        "type": "minecraft:jigsaw",
        "biomes": "#infinite_domain:wasteland_site_biomes",
        "step": "surface_structures",
        "spawn_overrides": {},
        "terrain_adaptation": "beard_box",
        "start_pool": f"infinite_domain:old_world/vcf/{name}",
        "size": 1,
        "start_height": {"absolute": 0},
        "max_distance_from_center": 80,
        "use_expansion_hack": False,
        "liquid_settings": "ignore_waterlogging",
        "project_start_to_heightmap": "WORLD_SURFACE_WG",
    }


def pool(name: str) -> dict:
    return {
        "fallback": "minecraft:empty",
        "elements": [{
            "weight": 1,
            "element": {
                "location": f"infinite_domain:old_world/vcf/{name}",
                "processors": "minecraft:empty",
                "projection": "rigid",
                "element_type": "minecraft:single_pool_element",
            },
        }],
    }


def structure_set(name: str, members: list[str], spacing: int, separation: int, salt: int) -> dict:
    return {
        "structures": [{"structure": f"infinite_domain:old_world/vcf/{member}", "weight": 1} for member in members],
        "placement": {"type": "minecraft:random_spread", "spacing": spacing, "separation": separation, "salt": salt},
    }


def generate(mode: str = "staged") -> None:
    statistics = {}
    for name, builder in VCF.BUILDERS.items():
        template = builder()
        G.stabilize_door_pairs(template)
        lint = G.assess_fidelity(name, template)
        if not lint["structural_lint_passed"]:
            raise ValueError(f"{name} failed structural lint: {'; '.join(lint['issues'])}")
        statistics[name] = template.save(f"old_world/vcf/{name}")
        statistics[name]["structural_lint"] = lint
        write_json(DATA / "worldgen" / "template_pool" / "old_world" / "vcf" / f"{name}.json", pool(name))
        write_json(DATA / "worldgen" / "structure" / "old_world" / "vcf" / f"{name}.json", structure_definition(name))

    set_dir = DATA / "worldgen" / "structure_set" / "old_world" / "vcf"
    if mode == "activate-test":
        write_json(set_dir / "pt9_runtime_test.json", structure_set("pt9_runtime_test", [RESEARCH[0]], 72, 36, 9071006))
    elif mode == "activate-vcf":
        write_json(set_dir / "vcf_common.json", structure_set("vcf_common", COMMON, 54, 28, 9071001))
        write_json(set_dir / "vcf_research.json", structure_set("vcf_research", RESEARCH, 86, 43, 9071002))
    elif mode != "staged":
        raise ValueError(f"unknown mode: {mode}")

    write_json(ROOT / "docs" / "old-world" / "vcf-generated-manifest.json", {
        "schema_version": 1,
        "mode": mode,
        "structures_authored": len(VCF.BUILDERS),
        "natural_generation_active": mode in {"activate-test", "activate-vcf"},
        "runtime_test_target": "OWS-006" if mode == "activate-test" else None,
        "structures": statistics,
    })
    print(f"Generated {len(VCF.BUILDERS)} VCF Old World structures in mode={mode}")


if __name__ == "__main__":
    mode = "staged"
    if len(sys.argv) > 1:
        flag = sys.argv[1]
        mode = {"--activate-test": "activate-test", "--activate-vcf": "activate-vcf"}.get(flag, flag)
    generate(mode)
