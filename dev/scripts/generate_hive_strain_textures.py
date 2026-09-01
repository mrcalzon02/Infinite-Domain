"""Generate the Hive World Verdant Strain entity textures.

Authority: docs/HIVE_WORLD_VERDANT_STRAIN.md (sections 5-6) and the rule file
docs/hive-strain/palette-map.json.

For every entity texture in the installed Fungal Infection: Spore jar this writes
two derivatives into a gitignored staging tree:

  build/hive_strain/assets/infinite_domain/textures/entity/hive_strain/<rel>
      base texture with the mycelial red/magenta band remapped to a deep->bright
      green ramp; every other pixel copied unchanged; alpha preserved.

  build/hive_strain/assets/infinite_domain/textures/entity/hive_strain_glow/<rel>
      emissive spore/mycelium overlay (mostly transparent).

Deterministic and idempotent: fixed-seed Mersenne Twister only, no timestamps,
no network. Re-running on the same jar produces byte-identical output. These
derivatives are NOT committed (licensing hold - see the spec, section 11).
"""

from __future__ import annotations

import io
import json
import random
import sys
import zipfile
from pathlib import Path

from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[2]
PALETTE = ROOT / "dev/docs" / "hive-strain" / "palette-map.json"
OUT_ROOT = ROOT / "build" / "hive_strain" / "assets" / "infinite_domain" / "textures" / "entity"
TEXTURE_ROOT = "assets/spore/textures/entity/"

FNV_OFFSET = 2166136261
FNV_PRIME = 16777619
FNV_MASK = 0xFFFFFFFF


def fnv1a(text: str) -> int:
    h = FNV_OFFSET
    for byte in text.encode("utf-8"):
        h = ((h ^ byte) * FNV_PRIME) & FNV_MASK
    return h


def hex_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16)


def argb_to_rgba(value: int) -> tuple[int, int, int, int]:
    return (value >> 16) & 0xFF, (value >> 8) & 0xFF, value & 0xFF, (value >> 24) & 0xFF


def build_ramp_luts(stops: list[dict]) -> tuple[list[int], list[int], list[int]]:
    """Three 256-entry LUTs indexed by source HSV value -> green channel, linear sRGB."""
    pts = sorted(((s["t"], hex_rgb(s["hex"])) for s in stops), key=lambda p: p[0])
    lut_r, lut_g, lut_b = [], [], []
    for i in range(256):
        t = i / 255.0
        lo, hi = pts[0], pts[-1]
        for a, b in zip(pts, pts[1:]):
            if a[0] <= t <= b[0]:
                lo, hi = a, b
                break
        span = hi[0] - lo[0]
        f = 0.0 if span <= 0 else (t - lo[0]) / span
        lut_r.append(round(lo[1][0] + (hi[1][0] - lo[1][0]) * f))
        lut_g.append(round(lo[1][1] + (hi[1][1] - lo[1][1]) * f))
        lut_b.append(round(lo[1][2] + (hi[1][2] - lo[1][2]) * f))
    return lut_r, lut_g, lut_b


def load_rule() -> dict:
    rule = json.loads(PALETTE.read_text(encoding="utf-8"))
    band = rule["recolour"]["mycelial_band"]
    # HSV thresholds in PIL's 0..255 space.
    rule["_hue_lo"] = round(min(hi for _, hi in band["hue_ranges_deg"] if hi <= 180) / 360 * 255)
    rule["_hue_hi"] = round(min(lo for lo, _ in band["hue_ranges_deg"] if lo >= 180) / 360 * 255)
    rule["_sat_min"] = round(float(band["saturation_min"]) * 255)
    rule["_val_min"] = round(float(band["value_min"]) * 255)
    rule["_luts"] = build_ramp_luts(rule["recolour"]["green_ramp"]["stops"])
    ov = rule["overlay"]["layers"]
    rule["_glow"] = argb_to_rgba(int(ov[0]["argb"], 16))
    rule["_speckle"] = argb_to_rgba(int(ov[1]["argb"], 16))
    rule["_speckle_period"] = int(ov[1]["period"])
    rule["_core"] = argb_to_rgba(int(ov[2]["argb"], 16))
    rule["_core_period"] = int(ov[2]["period"])
    rule["_excluded"] = set(rule["source"]["excluded_basenames"])
    return rule


def band_mask(src_rgba: Image.Image, hsv: Image.Image, rule: dict) -> Image.Image:
    """L-mode 0/255 mask of the mycelial band. Pure PIL channel ops."""
    h, s, v = hsv.split()
    a = src_rgba.getchannel("A")
    hue_lo, hue_hi = rule["_hue_lo"], rule["_hue_hi"]
    m_h = h.point(lambda p: 255 if (p <= hue_lo or p >= hue_hi) else 0)
    m_s = s.point(lambda p: 255 if p >= rule["_sat_min"] else 0)
    m_v = v.point(lambda p: 255 if p >= rule["_val_min"] else 0)
    m_a = a.point(lambda p: 255 if p > 0 else 0)
    return ImageChops.multiply(ImageChops.multiply(m_h, m_s), ImageChops.multiply(m_v, m_a))


def process(rel: str, src: Image.Image, rule: dict) -> tuple[Image.Image, Image.Image]:
    src = src.convert("RGBA")
    w, ht = src.size
    excluded = rel.rsplit("/", 1)[-1] in rule["_excluded"]

    hsv = src.convert("RGB").convert("HSV")
    mask = Image.new("L", (w, ht), 0) if excluded else band_mask(src, hsv, rule)

    # --- base: green ramp where masked, source elsewhere, alpha preserved ---
    value = hsv.getchannel(2)
    lut_r, lut_g, lut_b = rule["_luts"]
    green = Image.merge("RGB", (value.point(lut_r), value.point(lut_g), value.point(lut_b)))
    base_rgb = Image.composite(green, src.convert("RGB"), mask)
    base = Image.merge("RGBA", (*base_rgb.split(), src.getchannel("A")))

    # --- overlay: glow from mask + deterministic sampled speckle/core ---
    over = Image.composite(
        Image.new("RGBA", (w, ht), rule["_glow"]),
        Image.new("RGBA", (w, ht), (0, 0, 0, 0)),
        mask,
    )
    if not excluded:
        px = over.load()
        # Speckle only where the creature is actually drawn (opaque source texel),
        # so no emissive dots float in the model's empty UV space.
        alpha = list(src.getchannel("A").getdata())
        opaque = [i for i, a in enumerate(alpha) if a != 0]
        rng = random.Random(fnv1a(rel))
        for _ in range(len(opaque) // rule["_speckle_period"]):
            i = opaque[rng.randrange(len(opaque))]
            px[i % w, i // w] = rule["_speckle"]
        for _ in range(len(opaque) // rule["_core_period"]):
            i = opaque[rng.randrange(len(opaque))]
            px[i % w, i // w] = rule["_core"]
    return base, over


def main() -> None:
    jars = sorted(ROOT.glob("mods/spore_*.jar"))
    if not jars:
        sys.exit("no mods/spore_*.jar found")
    jar = jars[-1]
    rule = load_rule()

    with zipfile.ZipFile(jar) as z:
        names = sorted(
            n for n in z.namelist()
            if n.startswith(TEXTURE_ROOT) and n.endswith(".png")
        )
        base_root = OUT_ROOT / "hive_strain"
        glow_root = OUT_ROOT / "hive_strain_glow"
        for n, name in enumerate(names, 1):
            rel = name[len(TEXTURE_ROOT):]
            src = Image.open(io.BytesIO(z.read(name)))
            base, over = process(rel, src, rule)
            for root, img in ((base_root, base), (glow_root, over)):
                dest = root / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                img.save(dest, "PNG", optimize=False)
            if n % 40 == 0 or n == len(names):
                print(f"  {n}/{len(names)}")

    print(f"wrote {len(names)} base + {len(names)} glow textures under "
          f"{base_root.parent.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
