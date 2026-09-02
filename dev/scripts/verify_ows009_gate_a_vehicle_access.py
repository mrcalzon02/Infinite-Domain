#!/usr/bin/env python3
"""Deterministic vehicle-access preflight for OWS-009 Gate-A r2.

This supplements verify_ows009_gate_a_static.py. It does not approve visual
quality, runtime placement, Lost Cities coexistence, transforms, shipping-NBT
equivalence, gameplay hooks, or production admission.
"""
from __future__ import annotations

import render_ows009_gate_a_massing as gate


def _assert_vehicle_swept_paths(t: gate.base.Template) -> None:
    """Prove each repair cell has a supported, unobstructed vehicle approach."""
    paths = {
        "diagnostic cell": ((7, 10), 2, 22, 5),
        "heavy-intervention cell": ((18, 21), 2, 22, 7),
        "recommissioning cell": ((29, 31), 2, 22, 6),
    }

    for label, ((x1, x2), z1, z2, top_y) in paths.items():
        for x in range(x1, x2 + 1):
            for z in range(z1, z2 + 1):
                floor_y = 1 if z >= 7 else 0

                if gate._name(t, (x, floor_y, z)) in gate.AIR:
                    raise AssertionError(
                        f"OWS-009 {label} vehicle approach lacks support at {(x, floor_y, z)}"
                    )

                for y in range(floor_y + 1, top_y + 1):
                    if gate._name(t, (x, y, z)) not in gate.AIR:
                        raise AssertionError(
                            f"OWS-009 {label} vehicle swept path clipped at {(x, y, z)}"
                        )


def main() -> None:
    model = gate.build_gate_a_massing()
    gate._assert_contracts(model)
    _assert_vehicle_swept_paths(model)

    print(
        "OWS-009 Gate-A r2 vehicle-access preflight PASS: all three repair cells "
        "retain supported, unobstructed swept volumes from the recovery apron "
        "through their thresholds into usable work-cell depth. Runtime, Lost "
        "Cities, transform, visual, gameplay, shipping-NBT, and production gates "
        "remain pending."
    )


if __name__ == "__main__":
    main()
