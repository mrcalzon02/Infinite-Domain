"""Floor-slice render evidence for Lyran Research.

One plate per level plus a north-south section, so the build can be reviewed
without loading the world.  Slices are taken at head height (y+3) so doors,
props and circulation read, not just the floor slab.
"""

from __future__ import annotations

import sys

from PIL import Image, ImageDraw

sys.path.insert(0, ".")
import lyran_research as LR

CELL = 7
PAD = 26
NON_SOLID = {"minecraft:air", "minecraft:cave_air", "minecraft:void_air"}

COLOURS = {
    "rock": (14, 12, 16),
    "air": (233, 228, 224),
    "wall": (58, 52, 62),
    "wall_cracked": (78, 66, 72),
    "floor": (150, 142, 148),
    "door": (196, 86, 60),
    "stair": (240, 176, 64),
    "ladder": (240, 176, 64),
    "lamp": (255, 224, 130),
    "chest": (120, 200, 140),
    "portal": (120, 100, 220),
    "lava": (226, 88, 34),
    "prop": (110, 150, 190),
}


def classify(name: str | None) -> str:
    if name is None:
        return "rock"
    if name in NON_SOLID:
        return "air"
    if "end_portal_frame" in name:
        return "portal"
    if "lava" in name or "magma" in name:
        return "lava"
    if "_door" in name:
        return "door"
    if "stairs" in name:
        return "stair"
    if "ladder" in name:
        return "ladder"
    if "lantern" in name or "shroomlight" in name:
        return "lamp"
    if "chest" in name or "barrel" in name:
        return "chest"
    if "cracked" in name:
        return "wall_cracked"
    if "blackstone" in name or "basalt" in name or "netherrack" in name:
        return "wall"
    return "prop"


def main() -> None:
    t, report = LR.build()
    grid = {pos: t.palette[st]["Name"] for pos, (st, _n) in t.blocks.items()}
    n = LR.N

    plates = []
    for level in reversed(LR.LEVELS):          # top level first, as drawn
        y = level["y"] + 2
        img = Image.new("RGB", (n * CELL, n * CELL), COLOURS["rock"])
        d = ImageDraw.Draw(img)
        for z in range(n):
            for x in range(n):
                kind = classify(grid.get((x, y, z)))
                if kind == "air":
                    kind = "floor" if grid.get((x, level["y"], z)) else "rock"
                    if kind == "floor":
                        col = COLOURS["air"]
                    else:
                        col = COLOURS["rock"]
                else:
                    col = COLOURS[kind]
                d.rectangle([x * CELL, z * CELL, x * CELL + CELL - 1, z * CELL + CELL - 1], fill=col)
        plates.append((level["title"], f"y {level['y']}–{level['y'] + 7}  (world {level['y'] + 10}–{level['y'] + 17})", img))

    cols = 3
    rows = (len(plates) + cols - 1) // cols
    pw, ph = n * CELL, n * CELL
    sheet = Image.new("RGB", (cols * (pw + PAD) + PAD, rows * (ph + PAD * 2) + PAD), (24, 22, 26))
    sd = ImageDraw.Draw(sheet)
    for i, (title, sub, img) in enumerate(plates):
        cx = PAD + (i % cols) * (pw + PAD)
        cy = PAD + (i // cols) * (ph + PAD * 2)
        sheet.paste(img, (cx, cy + PAD))
        sd.text((cx, cy + 4), title, fill=(240, 236, 232))
        sd.text((cx, cy + 15), sub, fill=(150, 145, 150))
    sheet.save("/tmp/lyran/lyran_levels.png")

    # North–south section through the Gate Chamber's x, showing the vertical
    # stack and the ascent shaft breaking the lava-sea plane.
    gx = 35
    sec = Image.new("RGB", (n * CELL, (LR.SHAFT_TOP + 1) * CELL), COLOURS["rock"])
    sd2 = ImageDraw.Draw(sec)
    for y in range(LR.SHAFT_TOP + 1):
        for z in range(n):
            kind = classify(grid.get((gx, y, z)))
            col = COLOURS["air"] if kind == "air" else COLOURS[kind]
            py = (LR.SHAFT_TOP - y) * CELL
            sd2.rectangle([z * CELL, py, z * CELL + CELL - 1, py + CELL - 1], fill=col)
    lava_y = (LR.SHAFT_TOP - (64 - 10)) * CELL      # world Y=64 lava sea
    sd2.line([0, lava_y, n * CELL, lava_y], fill=COLOURS["lava"], width=2)
    sec.save("/tmp/lyran/lyran_section.png")

    sec2 = Image.new("RGB", (n * CELL, (LR.SHAFT_TOP + 1) * CELL), COLOURS["rock"])
    sd3 = ImageDraw.Draw(sec2)
    for y in range(LR.SHAFT_TOP + 1):
        for z in range(n):
            kind = classify(grid.get((56, y, z)))
            col = COLOURS["air"] if kind == "air" else COLOURS[kind]
            py = (LR.SHAFT_TOP - y) * CELL
            sd3.rectangle([z * CELL, py, z * CELL + CELL - 1, py + CELL - 1], fill=col)
    sd3.line([0, lava_y, n * CELL, lava_y], fill=COLOURS["lava"], width=2)
    sec2.save("/tmp/lyran/lyran_section_shaft.png")
    print("wrote /tmp/lyran/lyran_levels.png, lyran_section.png, lyran_section_shaft.png")


if __name__ == "__main__":
    main()
