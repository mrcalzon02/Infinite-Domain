"""Extract the Lyran Research 01 reference map into a machine-readable plan.

Input : the printed 91x91 dungeon map (Lyran Research 01, "Level 1").
Output: lyran_level1_plan.json  — occupancy grid, doorways, stair markers,
        and per-room cell sets keyed by the room number printed on the map.

The map is pure line art: room floors are white, rock/wall is black, and
door / archway / portcullis / secret glyphs are small marks drawn into the
wall line, which sample as *partially* dark open cells.  That difference is
what door detection keys on -- it is measured from the page, not guessed.
"""

from __future__ import annotations

import json
from collections import deque

import numpy as np
from PIL import Image

N = 91
MAP_BOX = (348, 2550, 229, 2430)  # y0, y1, x0, x1 in page-1.png at 300dpi

# Room-number label centroids, read off the annotated quadrant crops.
# (room number -> (x, z) grid cell of the printed label)
LABELS: dict[int, tuple[int, int]] = {
    1: (37, 5),   2: (47, 5),   3: (56, 4),   4: (36, 15),  5: (46, 15),
    6: (55, 15),  7: (55, 24),  8: (36, 25),  9: (46, 24),  10: (45, 34),
    11: (53, 34), 12: (7, 35),  13: (16, 34), 14: (26, 35), 15: (35, 34),
    16: (61, 34), 17: (70, 34), 18: (79, 34), 19: (87, 35), 20: (16, 42),
    21: (36, 44), 22: (46, 42), 23: (55, 43), 24: (64, 43), 25: (74, 42),
    26: (7, 45),  27: (25, 45), 28: (84, 45), 29: (16, 51), 30: (45, 51),
    31: (53, 51), 32: (73, 51), 33: (34, 52), 34: (61, 52), 35: (5, 55),
    36: (81, 55), 37: (36, 61), 38: (46, 61), 39: (55, 61), 40: (35, 70),
    41: (45, 71), 42: (54, 70), 43: (35, 79), 44: (53, 78), 45: (43, 80),
    46: (52, 86),
}

# Vertical-circulation glyphs ("Up" / "Down" combs in the legend), read off
# the same crops.  (kind, x1, z1, x2, z2)
STAIR_MARKERS = [
    ("up",   53, 8, 59, 10),   # north arm, off room 3      (marker 'a')
    ("down",  1, 47,  2, 49),  # west edge of room 26
    ("down", 59, 58, 64, 59),  # south of room 34
]


def sample_grid(page: str) -> tuple[np.ndarray, np.ndarray]:
    a = np.array(Image.open(page).convert("L")).astype(float)
    y0, y1, x0, x1 = MAP_BOX
    h, w = y1 - y0 + 1, x1 - x0 + 1
    cell = w / N
    grid = np.zeros((N, N), dtype=np.uint8)
    mean = np.zeros((N, N))
    for gz in range(N):
        for gx in range(N):
            cy0, cx0 = y0 + gz * h / N, x0 + gx * w / N
            cy1, cx1 = y0 + (gz + 1) * h / N, x0 + (gx + 1) * w / N
            patch = a[int(cy0 + cell * 0.30):int(cy1 - cell * 0.30) + 1,
                      int(cx0 + cell * 0.30):int(cx1 - cell * 0.30) + 1]
            m = float(patch.mean())
            mean[gz, gx] = m
            grid[gz, gx] = 1 if m > 140 else 0
    return grid, mean


def detect_doors(grid: np.ndarray, mean: np.ndarray) -> list[tuple[int, int, str]]:
    """An open, partially-darkened cell pinched between two walls is a doorway."""
    doors = []
    for z in range(1, N - 1):
        for x in range(1, N - 1):
            if not grid[z, x] or mean[z, x] >= 249:
                continue
            ns = not grid[z - 1, x] and not grid[z + 1, x]
            ew = not grid[z, x - 1] and not grid[z, x + 1]
            if ns and not ew:
                doors.append((x, z, "x"))   # opening faces east/west
            elif ew and not ns:
                doors.append((x, z, "z"))   # opening faces north/south
    return doors


def segment_rooms(grid: np.ndarray, doors: list[tuple[int, int, str]]) -> dict[int, list[tuple[int, int]]]:
    """Flood-fill each printed label outward, treating doorways as boundaries."""
    blocked = {(x, z) for x, z, _ in doors}
    owner: dict[tuple[int, int], int] = {}
    frontier: deque[tuple[int, int, int]] = deque()
    for room, (lx, lz) in LABELS.items():
        if not grid[lz, lx]:
            raise SystemExit(f"label for room {room} at ({lx},{lz}) is not on open floor")
        owner[(lx, lz)] = room
        frontier.append((lx, lz, room))
    # Simultaneous BFS from every label, so a shared corridor splits fairly
    # between the rooms that open onto it instead of being swallowed whole.
    while frontier:
        x, z, room = frontier.popleft()
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, nz = x + dx, z + dz
            if not (0 <= nx < N and 0 <= nz < N):
                continue
            if not grid[nz, nx] or (nx, nz) in owner or (nx, nz) in blocked:
                continue
            owner[(nx, nz)] = room
            frontier.append((nx, nz, room))
    rooms: dict[int, list[tuple[int, int]]] = {r: [] for r in LABELS}
    for (x, z), room in owner.items():
        rooms[room].append((x, z))
    return rooms


def main() -> None:
    grid, mean = sample_grid("page-1.png")
    doors = detect_doors(grid, mean)
    rooms = segment_rooms(grid, doors)

    unassigned = [(x, z) for z in range(N) for x in range(N)
                  if grid[z, x] and not any((x, z) in set(c) for c in ())]
    assigned = {c for cells in rooms.values() for c in cells}
    orphan = [(x, z) for z in range(N) for x in range(N)
              if grid[z, x] and (x, z) not in assigned and (x, z) not in {(d[0], d[1]) for d in doors}]

    plan = {
        "size": N,
        "open_cells": int(grid.sum()),
        "grid": ["".join("." if grid[z, x] else "#" for x in range(N)) for z in range(N)],
        "doors": [{"x": x, "z": z, "axis": a} for x, z, a in doors],
        "stairs": [{"kind": k, "x1": a, "z1": b, "x2": c, "z2": d} for k, a, b, c, d in STAIR_MARKERS],
        "rooms": {
            str(r): {
                "label": list(LABELS[r]),
                "cells": sorted(cells),
                "area": len(cells),
                "bounds": [min(x for x, _ in cells), min(z for _, z in cells),
                           max(x for x, _ in cells), max(z for _, z in cells)],
            }
            for r, cells in sorted(rooms.items())
        },
        "orphan_cells": orphan,
    }
    with open("lyran_level1_plan.json", "w", encoding="utf-8") as fh:
        json.dump(plan, fh, indent=1)

    print(f"open cells   : {plan['open_cells']}")
    print(f"doorways     : {len(doors)}")
    print(f"rooms        : {len(rooms)}")
    print(f"orphan cells : {len(orphan)}  (secret passages / unlabelled voids)")
    areas = sorted(((len(c), r) for r, c in rooms.items()), reverse=True)
    print("largest rooms:", ", ".join(f"R{r}={a}" for a, r in areas[:8]))
    print("smallest     :", ", ".join(f"R{r}={a}" for a, r in areas[-6:]))


if __name__ == "__main__":
    main()
