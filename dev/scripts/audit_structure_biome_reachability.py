"""Check that placed structures can reach a biome the main landmass actually has.

A structure set only places where the structure's own biome filter matches. That
filter is a tag, and a tag will happily list biomes that the world never
generates - so a structure can be fully authored, correctly tagged and still
never appear. Two ways that happens here:

  * a tag names a biome no climate rule ever produces, so the entry is inert; and
  * a tag names only biomes that live outside the central band, so the structure
    is exiled to whatever region does carry them.

The overworld biome source is `isekai_api:climate_zones`: an ordered rule list
matched on climate parameters, first match wins.

The central landmass is not a temperature band of its own. `regional_temperature`
lerps to a constant 0.0 wherever `wasteland_climate_mask` is set, so the whole
central continent reports temperature 0.0 and is served by the rules whose
temperature window spans zero (or that declare none at all). The [0.99, 1.0] and
[-1.0, -0.99] bands are the far-south and far-north outer regions, reached only
outside that mask where temperature falls back to z/750.

A structure is therefore central-continent reachable when some biome it accepts
belongs to a rule that can fire at temperature 0.0.

Deterministic: no network, no randomness, stable ordering.
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pack_content_oracle import ItemOracle  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]

PRESET = ROOT / "kubejs/data/wastelands/worldgen/world_preset/wasteland.json"
TAG_DIR = ROOT / "kubejs/data/infinite_domain/tags/worldgen/biome"
KUBEJS_DATA = ROOT / "kubejs/data"

# `regional_temperature` is pinned to this value across the central continent.
CENTRAL_TEMPERATURE = 0.0

OUT = ROOT / "dev/docs/quest-loot-attainability/structure-biome-reachability.json"


def load_tags(mod_tags: dict[str, list[str]]) -> dict[str, list[str]]:
    """Pack tags layered over the tags the installed jars provide.

    Structures routinely filter on a mod's biome tag (`#stellaris:mars_biomes`).
    Resolving only the pack's own tags makes every one of those look like it
    names no biome at all, which reads as a dead structure.
    """
    tags: dict[str, list[str]] = {k: list(v) for k, v in mod_tags.items()}
    for path in sorted(TAG_DIR.glob("**/*.json")):
        name = "infinite_domain:" + path.relative_to(TAG_DIR).as_posix()[: -len(".json")]
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
        values = [
            value if isinstance(value, str) else (value or {}).get("id")
            for value in payload.get("values", [])
        ]
        if payload.get("replace") is False and name in tags:
            tags[name] = tags[name] + [v for v in values if v and v not in tags[name]]
        else:
            tags[name] = values
    return tags


def flatten(tag: str, tags: dict[str, list[str]], seen: set[str] | None = None) -> set[str]:
    seen = seen or set()
    if tag in seen:
        return set()
    seen.add(tag)
    out: set[str] = set()
    for value in tags.get(tag, []):
        if not value:
            continue
        if value.startswith("#"):
            out |= flatten(value[1:], tags, seen)
        else:
            out.add(value)
    return out


def main() -> int:
    preset = json.loads(PRESET.read_text(encoding="utf-8-sig"))
    rules = preset["dimensions"]["minecraft:overworld"]["generator"]["biome_source"]["rules"]
    generated: set[str] = {r["biome"] for r in rules if isinstance(r.get("biome"), str)}
    def fires_on_central(rule: dict) -> bool:
        window = rule.get("temperature")
        if window is None:
            return True
        return window[0] <= CENTRAL_TEMPERATURE <= window[1]

    central: set[str] = {
        r["biome"] for r in rules
        if isinstance(r.get("biome"), str) and fires_on_central(r)
    }

    oracle = ItemOracle()
    tags = load_tags(oracle.mods.biome_tags)

    placed: dict[str, list[str]] = defaultdict(list)
    for path in sorted(KUBEJS_DATA.glob("*/worldgen/structure_set/**/*.json")):
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
        for entry in payload.get("structures", []) or []:
            target = entry.get("structure") if isinstance(entry, dict) else None
            if isinstance(target, str):
                placed[target].append(path.stem)

    findings: list[dict] = []
    rows: list[dict] = []
    for structure_id in sorted(placed):
        namespace, _, tail = structure_id.partition(":")
        path = KUBEJS_DATA / namespace / "worldgen/structure" / (tail + ".json")
        if not path.exists():
            continue  # mod-owned; its own data governs placement
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
        raw = payload.get("biomes")
        entries = [raw] if isinstance(raw, str) else (raw or [])

        resolved: set[str] = set()
        for entry in entries:
            resolved |= flatten(entry[1:], tags) if entry.startswith("#") else {entry}

        live = resolved & generated
        inert = sorted(resolved - generated)
        on_central = sorted(live & central)

        # A structure whose biomes the overworld never lists belongs to another
        # dimension (moon, mars, nether, hive world). The overworld rule list
        # says nothing about whether it can place, so it is out of scope here.
        if not live and resolved:
            continue

        rows.append({
            "structure": structure_id,
            "sets": sorted(placed[structure_id]),
            "biomes_declared": len(resolved),
            "biomes_generated": sorted(live),
            "biomes_central": on_central,
            "biomes_inert": inert,
        })

        if not resolved:
            findings.append({
                "code": "STRUCT-BIOME-UNFILTERED", "severity": "info",
                "structure": structure_id,
                "message": structure_id + ": declares no biome filter",
            })
        elif not live:
            findings.append({
                "code": "STRUCT-BIOME-DEAD", "severity": "critical",
                "structure": structure_id,
                "message": structure_id + ": no declared biome is ever generated - it cannot place",
            })
        elif not on_central:
            findings.append({
                "code": "STRUCT-BIOME-OFF-CONTINENT", "severity": "warning",
                "structure": structure_id,
                "message": structure_id + ": reachable only outside the central landmass ("
                           + ", ".join(sorted(live)) + ")",
            })
        if inert:
            findings.append({
                "code": "TAG-ENTRY-INERT", "severity": "info",
                "structure": structure_id,
                "message": structure_id + ": biome filter lists biomes no rule generates ("
                           + ", ".join(inert) + ")",
            })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "central_continent_temperature": CENTRAL_TEMPERATURE,
        "central_continent_biomes": sorted(central),
        "generated_biomes": len(generated),
        "structures_checked": len(rows),
        "findings": findings,
        "structures": rows,
    }, indent=2) + "\n", encoding="utf-8")

    print("Structure biome reachability")
    print("  central-continent biomes " + str(len(central)))
    print("  generated biomes       " + str(len(generated)))
    print("  placed pack structures " + str(len(rows)))
    counts: dict[str, int] = defaultdict(int)
    for finding in findings:
        counts[finding["code"]] += 1
    print()
    for code in sorted(counts):
        severity = next(f["severity"] for f in findings if f["code"] == code)
        print("  " + severity.ljust(8) + " " + code.ljust(28) + " " + str(counts[code]))
    print("\nFull report: " + OUT.relative_to(ROOT).as_posix())
    return 1 if any(f["severity"] == "critical" for f in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
