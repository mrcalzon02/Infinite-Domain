#!/usr/bin/env python3
"""Authoritative generator for the Hive World density graph.

Endgame: advances C0037/C0041/C0042/C0043 (Phase 3 mass, strata, void fields) at
spike scale, by owner direction ("build the dimension out into a real place").
Authority: docs/Endgame.md §3, docs/endgame/contracts/spatial-metrics.md,
docs/endgame/adr/ADR-0001 (generation owns mass, structures own legibility).

Emits (do not hand-edit):
  kubejs/data/infinite_domain/worldgen/noise/hive_world_*.json          (4 noise defs)
  kubejs/data/infinite_domain/worldgen/density_function/hive_world/*.json

Model: the whole dimension is one engineered mass, solid from Y-64 to ~Y292, with
a bedrock-capped roof. Voids are carved OUT of it:
  * a spaghetti-style tunnel/room network (mid-scale noise near zero) - "choked,
    indecipherable" circulation (mission §1);
  * full-height vertical circulation shafts (large-scale noise, no Y variation);
  * one monumental release hall in the Vaulting band Y~200-246, minus support
    columns (mission §2.2 compression -> release);
  * a guaranteed-solid floor and roof so nothing breaches the world edges.
Band palettes are applied by the noise-settings surface rule (see
generate_hive_world_noise.py).
"""
from __future__ import annotations

import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
NOISE_DIR = REPO / "kubejs/data/infinite_domain/worldgen/noise"
DF_DIR = REPO / "kubejs/data/infinite_domain/worldgen/density_function/hive_world"

NS = "infinite_domain"


def ref(name: str) -> str:
    return f"{NS}:hive_world/{name}"


# --- custom noise definitions --------------------------------------------------
NOISES = {
    "hive_world_network": {"firstOctave": -7, "amplitudes": [1.0, 0.6, 0.3, 0.15]},
    "hive_world_shaft": {"firstOctave": -8, "amplitudes": [1.0, 0.4]},
    "hive_world_hall": {"firstOctave": -9, "amplitudes": [1.0]},
    "hive_world_columns": {"firstOctave": -5, "amplitudes": [1.0, 0.5]},
}


def y_grad(from_y, from_value, to_y, to_value):
    return {
        "type": "minecraft:y_clamped_gradient",
        "from_y": from_y, "to_y": to_y,
        "from_value": from_value, "to_value": to_value,
    }


def noise_df(noise_id, xz, y):
    return {"type": "minecraft:noise", "noise": f"{NS}:{noise_id}", "xz_scale": xz, "y_scale": y}


def range_keep(input_ref, half_width):
    """-1 (void) when the noise is within +-half_width of zero, else +1 (solid)."""
    return {
        "type": "minecraft:range_choice",
        "input": input_ref,
        "min_inclusive": -half_width,
        "max_inclusive": half_width,
        "when_in_range": -1.0,
        "when_out_of_range": 1.0,
    }


# --- density function graph ---------------------------------------------------
DFS = {
    # solid everywhere below ~Y292, ramp to void by the roof line
    "mass": y_grad(278, 1.0, 306, -1.0),
    # forced-solid bedrock-ish roof and floor so voids never breach the edges
    "roof": y_grad(300, -1.0, 316, 1.0),
    "floor": y_grad(-64, 1.0, -46, -1.0),

    # the circulation network: carve where the mid-scale noise crosses zero
    "network_noise": noise_df("hive_world_network", 0.55, 0.34),
    # full-height vertical shafts: large-scale noise with NO vertical variation
    "shaft_noise": noise_df("hive_world_shaft", 0.14, 0.0),
    # monumental hall distribution and its support-column lattice
    "vault_noise": noise_df("hive_world_hall", 0.09, 0.05),
    "column_noise": noise_df("hive_world_columns", 0.42, 0.0),
}

DFS["network_keep"] = range_keep(ref("network_noise"), 0.16)
DFS["shaft_keep"] = range_keep(ref("shaft_noise"), 0.055)

# a Y window that is +1 inside the Vaulting hall band, -1 outside
DFS["vault_window"] = {
    "type": "minecraft:min",
    "argument1": y_grad(192, -1.0, 204, 1.0),
    "argument2": y_grad(238, 1.0, 250, -1.0),
}
# +1 at a column, -1 between columns
DFS["column_field"] = range_keep(ref("column_noise"), 0.12)
# carve the hall: void inside the window where the broad noise is high, keep columns
DFS["vault_keep"] = {
    "type": "minecraft:max",
    "argument1": {
        "type": "minecraft:max",
        # +1 outside the band window
        "argument1": {"type": "minecraft:mul", "argument1": -1.0, "argument2": ref("vault_window")},
        # +1 where the broad hall noise is low (not carved)
        "argument2": {"type": "minecraft:mul", "argument1": -1.0, "argument2": ref("vault_noise")},
    },
    # ...but always keep the columns
    "argument2": ref("column_field"),
}

# combine: start from the mass, intersect every "keep" field, then force edges solid
DFS["carved"] = {
    "type": "minecraft:min",
    "argument1": {
        "type": "minecraft:min",
        "argument1": {"type": "minecraft:min", "argument1": ref("mass"), "argument2": ref("network_keep")},
        "argument2": ref("shaft_keep"),
    },
    "argument2": ref("vault_keep"),
}
DFS["final"] = {
    "type": "minecraft:max",
    "argument1": {"type": "minecraft:max", "argument1": ref("carved"), "argument2": ref("roof")},
    "argument2": ref("floor"),
}


def main() -> int:
    NOISE_DIR.mkdir(parents=True, exist_ok=True)
    DF_DIR.mkdir(parents=True, exist_ok=True)
    for name, data in NOISES.items():
        (NOISE_DIR / f"{name}.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    for name, data in DFS.items():
        (DF_DIR / f"{name}.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(NOISES)} noise defs, {len(DFS)} density functions")
    return 0


if __name__ == "__main__":
    sys.exit(main())
