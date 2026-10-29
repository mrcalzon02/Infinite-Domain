"""Validate first-party placement probes against retained spawner-at-air errors.

This is a *consumer*, not a runtime hook. Never attribute an r4 error to a
structure from coordinate proximity or from a different benchmark run.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / "dev/docs/boot-dimension-audit/revision-4"
RESOURCE = re.compile(r"^[a-z0-9_.-]+:[a-z0-9_./-]+$")
ROTATIONS = {"none", "clockwise_90", "180", "counterclockwise_90"}
MIRRORS = {"none", "front_back", "left_right"}


def coordinates(value, label):
    if not isinstance(value, dict) or set(value) != {"x", "y", "z"}:
        raise ValueError(f"{label} must have exactly x/y/z")
    if any(type(value[axis]) is not int for axis in ("x", "y", "z")):
        raise ValueError(f"{label} coordinates must be integers")
    return value


def transformed(local, origin, rotation, mirror):
    """NBT local position transformed about the template's zero pivot.

    This is the mathematical pivot transform, NOT proof of Minecraft's final
    worldgen clipping or a specific /place command's bounding-box adjustment.
    """
    x, z = local["x"], local["z"]
    if mirror == "front_back":
        x = -x
    elif mirror == "left_right":
        z = -z
    if rotation == "clockwise_90":
        x, z = -z, x
    elif rotation == "180":
        x, z = -x, -z
    elif rotation == "counterclockwise_90":
        x, z = z, -x
    return {"x": origin["x"] + x, "y": origin["y"] + local["y"],
            "z": origin["z"] + z}


def validate_event(event):
    """Require exact, same-run placement provenance; reject guessed owners."""
    if not isinstance(event, dict) or event.get("schema_version") != 1:
        raise ValueError("placement event must use schema_version=1")
    required = ("run_id", "dimension", "hook_id", "placement_owner", "structure_id",
                "piece_id", "placement_origin", "template_local_position",
                "world_position", "rotation", "mirror", "expected_block_state",
                "spawner_nbt", "observed_block_state", "observed_block_entity_nbt")
    missing = [key for key in required if key not in event]
    if missing:
        raise ValueError("placement event missing: " + ", ".join(missing))
    for key in ("run_id", "hook_id", "piece_id"):
        if not isinstance(event[key], str) or not event[key].strip():
            raise ValueError(f"{key} must be a nonempty string")
    for key in ("dimension", "placement_owner", "structure_id"):
        if not isinstance(event[key], str) or not RESOURCE.fullmatch(event[key]):
            raise ValueError(f"{key} must be a namespaced resource ID")
    if event["rotation"] not in ROTATIONS or event["mirror"] not in MIRRORS:
        raise ValueError("unsupported rotation/mirror")
    for key in ("placement_origin", "template_local_position", "world_position"):
        coordinates(event[key], key)
    if event["expected_block_state"] != "minecraft:spawner":
        raise ValueError("event must describe an expected minecraft:spawner")
    nbt = event["spawner_nbt"]
    if not isinstance(nbt, dict) or nbt.get("id") != "minecraft:mob_spawner":
        raise ValueError("spawner_nbt must include minecraft:mob_spawner id")
    if not isinstance(event["observed_block_state"], str) or not event["observed_block_state"]:
        raise ValueError("observed_block_state must be explicit")
    observed = event["observed_block_entity_nbt"]
    if observed is not None and not isinstance(observed, dict):
        raise ValueError("observed_block_entity_nbt must be a compound or null")
    expected = transformed(event["template_local_position"], event["placement_origin"],
                           event["rotation"], event["mirror"])
    if expected != event["world_position"]:
        raise ValueError("world_position disagrees with source-local pivot transform")
    result = dict(event)
    result["chunk"] = {"x": expected["x"] // 16, "z": expected["z"] // 16}
    result["state_mismatch"] = event["observed_block_state"] != event["expected_block_state"]
    return result


def correlate(report, runtime, events):
    """Same-run coordinate matches are evidence candidates, never ownership proof."""
    if report.get("runtime_spawner_at_air_errors") != 7:
        raise ValueError("retained r4 error report changed; inspect before correlation")
    run_id = runtime.get("runId")
    if not isinstance(run_id, str) or not run_id:
        raise ValueError("runtime report lacks a run ID")
    positions = report.get("positions", [])
    if len(positions) != 7:
        raise ValueError("retained r4 positions incomplete")
    validated = [validate_event(event) for event in events]
    hits = []
    for error in positions:
        pos = coordinates(error["position"], "error position")
        same_run = [e for e in validated if e["run_id"] == run_id and e["world_position"] == pos]
        hits.append({"log_line": error["log_line"], "position": pos,
                     "matching_same_run_event_count": len(same_run),
                     "candidate_owners_not_verified": sorted({e["placement_owner"] for e in same_run}),
                     "candidate_structures_not_verified": sorted({e["structure_id"] for e in same_run}),
                     "state_mismatch_observed": any(e["state_mismatch"] for e in same_run)})
    return {
        "schema_version": 1,
        "retained_run_id": run_id,
        "retained_errors": len(positions),
        "events_supplied": len(events),
        "same_run_events": sum(e["run_id"] == run_id for e in validated),
        "same_run_exact_coordinate_hits": sum(bool(h["matching_same_run_event_count"]) for h in hits),
        "coordinate_evidence": hits,
        "attribution": "unresolved",
        "runtime_capture_status": "unverified_external_events" if events else "no_runtime_events",
        "blocker": ("No verified first-party placement hook currently records the upstream "
                    "structure/piece/feature identity before chunk serialization. The existing "
                    "QA /place template commands describe deliberate QA placements only; "
                    "the seven r4 errors occurred during separate world preparation. "
                    "Neither static NBT nor coordinate matches prove natural-generation ownership."),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", type=Path, help="JSON Lines emitted by a verified placement probe (optional)")
    parser.add_argument("--provenance", type=Path, default=AUDIT / "spawner-runtime-provenance.json")
    parser.add_argument("--runtime", type=Path, default=AUDIT / "result.json")
    parser.add_argument("--out", type=Path, help="Write comparison JSON; default prints to stdout")
    args = parser.parse_args()
    events = []
    if args.events:
        with args.events.open(encoding="utf-8") as stream:
            events = [json.loads(line) for line in stream if line.strip()]
    comparison = correlate(json.loads(args.provenance.read_text(encoding="utf-8")),
                           json.loads(args.runtime.read_text(encoding="utf-8")), events)
    rendered = json.dumps(comparison, indent=2) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    print(f"Placement evidence: {comparison['same_run_exact_coordinate_hits']}/7 exact same-run positions; "
          f"attribution {comparison['attribution']}", file=__import__('sys').stderr)


if __name__ == "__main__":
    main()
