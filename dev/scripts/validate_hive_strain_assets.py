"""Validator for the Hive World Verdant Strain authoring pass.

Authority: docs/HIVE_WORLD_VERDANT_STRAIN.md. Every rule in that spec names this
script. Exit code 0 = all checks pass; 1 = at least one failure.

Checks (see the spec, section 10):

  1  every roster id exists in docs/registry-inventory/entity-ids.txt
  2  no excluded (projectile / body-part / FX) id leaked into the roster
  3  every roster texture path exists in the installed spore jar
  4  every recoloured base PNG: same size as source; pixels outside the mycelial
     band are byte-identical to source; changed pixels stay in the green hue
     envelope; alpha channel unchanged
  5  every glow PNG: same size as its base; emissive coverage within budget;
     only the three declared ARGB values plus full transparency
  6  idempotence - re-running both generators reproduces byte-identical output
  7  palette-map.json self-consistency

The band-mask logic is imported from generate_hive_strain_textures so the
generator and validator can never diverge.
"""

from __future__ import annotations

import hashlib
import io
import json
import subprocess
import sys
import zipfile
from pathlib import Path

from PIL import Image, ImageChops

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_hive_strain_textures import (  # noqa: E402
    TEXTURE_ROOT,
    band_mask,
    hex_rgb,
    load_rule,
)

ROOT = Path(__file__).resolve().parents[2]
ENTITY_IDS = ROOT / "dev/docs" / "registry-inventory" / "entity-ids.txt"
MANIFEST = ROOT / "dev/docs" / "hive-strain" / "roster-manifest.json"
PALETTE = ROOT / "dev/docs" / "hive-strain" / "palette-map.json"
BUILD = ROOT / "build" / "hive_strain" / "assets" / "infinite_domain" / "textures" / "entity"
BASE_DIR = BUILD / "hive_strain"
GLOW_DIR = BUILD / "hive_strain_glow"
GENERATOR = ROOT / "dev/scripts" / "generate_hive_strain_textures.py"

EXCLUDE_SUFFIX = ("_arm", "_head", "_seg", "_tail", "_round")
EXCLUDE_PREFIX = ("thrown_",)

failures: list[str] = []


def fail(check: str, msg: str) -> None:
    failures.append(f"[{check}] {msg}")


def spore_ids() -> set[str]:
    return {
        s.strip() for s in ENTITY_IDS.read_text(encoding="utf-8").splitlines()
        if s.strip().startswith("spore:")
    }


def tree_hash(root: Path) -> str:
    h = hashlib.sha256()
    for p in sorted(root.rglob("*.png")):
        h.update(p.relative_to(root).as_posix().encode())
        h.update(p.read_bytes())
    return h.hexdigest()


def check_1_2_3(manifest: dict, jar: Path) -> None:
    ids = spore_ids()
    with zipfile.ZipFile(jar) as z:
        jar_textures = {
            n[len(TEXTURE_ROOT):] for n in z.namelist()
            if n.startswith(TEXTURE_ROOT) and n.endswith(".png")
        }
    for rec in manifest["roster"]:
        if rec["id"] not in ids:
            fail("1", f"roster id {rec['id']} not in entity-ids.txt")
        stem = rec["id"].split(":", 1)[1]
        if (rec["id"] in manifest["excluded_non_creatures"]
                or stem.startswith(EXCLUDE_PREFIX) or stem.endswith(EXCLUDE_SUFFIX)):
            fail("2", f"excluded-pattern id {rec['id']} present in roster")
        for tex in rec["textures"]:
            if tex not in jar_textures:
                fail("3", f"{rec['id']} texture {tex} missing from jar")
    for ex in manifest["excluded_non_creatures"]:
        if ex not in ids:
            fail("2", f"excluded id {ex} not a real spore entity")


def _changed_bbox(a: Image.Image, b: Image.Image) -> tuple | None:
    diff = ImageChops.difference(a, b)
    merged = None
    for band in diff.split():
        merged = band if merged is None else ImageChops.lighter(merged, band)
    return merged.getbbox()


def check_4_5(manifest: dict, jar: Path, rule: dict) -> None:
    envelope = rule["recolour"]["green_ramp"]["hue_envelope_deg"]
    env_lo = round(envelope[0] / 360 * 255)
    env_hi = round(envelope[1] / 360 * 255)
    glow_rgba = _argb(rule["overlay"]["layers"][0]["argb"])
    speckle_rgba = _argb(rule["overlay"]["layers"][1]["argb"])
    core_rgba = _argb(rule["overlay"]["layers"][2]["argb"])
    allowed_glow = {(0, 0, 0, 0), glow_rgba, speckle_rgba, core_rgba}
    speckle_budget = rule["overlay"]["budget"]["max_speckle_core_fraction"]

    with zipfile.ZipFile(jar) as z:
        names = sorted(
            n for n in z.namelist()
            if n.startswith(TEXTURE_ROOT) and n.endswith(".png")
        )
        for name in names:
            rel = name[len(TEXTURE_ROOT):]
            src = Image.open(io.BytesIO(z.read(name))).convert("RGBA")
            base_path = BASE_DIR / rel
            glow_path = GLOW_DIR / rel
            if not base_path.exists() or not glow_path.exists():
                fail("4", f"missing output for {rel} - run generate_hive_strain_textures.py")
                continue
            base = Image.open(base_path).convert("RGBA")
            glow_img = Image.open(glow_path).convert("RGBA")
            if base.size != src.size:
                fail("4", f"{rel} base size {base.size} != source {src.size}")
                continue
            if glow_img.size != src.size:
                fail("5", f"{rel} glow size {glow_img.size} != source {src.size}")

            excluded = rel.rsplit("/", 1)[-1] in rule["_excluded"]
            mask = Image.new("L", src.size, 0) if excluded else band_mask(src, src.convert("RGB").convert("HSV"), rule)

            # changed pixels outside the band -> must be identical
            diff = ImageChops.difference(src, base)
            changed = None
            for band in diff.split():
                changed = band if changed is None else ImageChops.lighter(changed, band)
            changed = changed.point(lambda p: 255 if p else 0)
            outside_changed = ImageChops.subtract(changed, mask)
            if outside_changed.getbbox() is not None:
                fail("4", f"{rel} modified {_count(outside_changed)} pixel(s) outside the mycelial band")

            # alpha channel unchanged
            if ImageChops.difference(src.getchannel("A"), base.getchannel("A")).getbbox() is not None:
                fail("4", f"{rel} altered the alpha channel")

            # changed pixels must land in the green hue envelope
            if not excluded:
                hue = base.convert("RGB").convert("HSV").getchannel(0)
                out_of_env = hue.point(lambda p: 255 if not (env_lo <= p <= env_hi) else 0)
                bad = ImageChops.multiply(ImageChops.multiply(out_of_env, mask), changed)
                if bad.getbbox() is not None:
                    fail("4", f"{rel} has {_count(bad)} recoloured pixel(s) outside hue envelope {envelope}")

            # glow palette + budgets
            total = src.size[0] * src.size[1]
            colors = glow_img.getcolors(maxcolors=32)
            if colors is None:
                fail("5", f"{rel} glow has >32 distinct colours (expected <= 4)")
            else:
                counts = {rgba: cnt for cnt, rgba in colors}
                for rgba in counts:
                    if rgba not in allowed_glow:
                        fail("5", f"{rel} glow contains undeclared colour {rgba}")
                        break
                speckle_core = counts.get(speckle_rgba, 0) + counts.get(core_rgba, 0)
                if speckle_core / total > speckle_budget + 1e-9:
                    fail("5", f"{rel} speckle+core coverage {speckle_core / total:.3f} exceeds budget {speckle_budget}")
                # growth-glow wash must be a subset of the recoloured band
                band_px = _count(mask)
                if counts.get(glow_rgba, 0) > band_px:
                    fail("5", f"{rel} glow wash ({counts[glow_rgba]}) exceeds band pixel count ({band_px})")


def _argb(text: str) -> tuple[int, int, int, int]:
    v = int(text, 16)
    return (v >> 16) & 0xFF, (v >> 8) & 0xFF, v & 0xFF, (v >> 24) & 0xFF


def _count(mask: Image.Image) -> int:
    """Count of non-zero pixels in an 'L' mask."""
    return sum(mask.histogram()[1:])


def check_6_idempotence() -> None:
    if not BASE_DIR.exists():
        fail("6", "no output tree - run generate_hive_strain_textures.py first")
        return
    before = tree_hash(BASE_DIR) + tree_hash(GLOW_DIR)
    result = subprocess.run(
        [sys.executable, str(GENERATOR)], capture_output=True, text=True, cwd=ROOT
    )
    if result.returncode != 0:
        fail("6", f"generator re-run failed: {result.stderr.strip()[:200]}")
        return
    after = tree_hash(BASE_DIR) + tree_hash(GLOW_DIR)
    if before != after:
        fail("6", "generator output changed on re-run (not idempotent)")


def check_7_palette() -> None:
    rule = json.loads(PALETTE.read_text(encoding="utf-8"))
    stops = rule["recolour"]["green_ramp"]["stops"]
    ts = [s["t"] for s in stops]
    if ts != sorted(ts) or ts[0] != 0.0 or ts[-1] != 1.0:
        fail("7", f"green_ramp stops not monotonic 0..1: {ts}")
    vals = [max(hex_rgb(s["hex"])) for s in stops]
    if vals != sorted(vals):
        fail("7", f"green_ramp not monotonic in value: {vals}")
    for lo, hi in rule["recolour"]["mycelial_band"]["hue_ranges_deg"]:
        if not (0 <= lo <= hi <= 360):
            fail("7", f"bad hue range [{lo}, {hi}]")
    if not 0 <= rule["recolour"]["mycelial_band"]["saturation_min"] <= 1:
        fail("7", "saturation_min out of range")
    for layer in rule["overlay"]["layers"][1:]:
        if int(layer["period"]) <= 0:
            fail("7", f"overlay period must be > 0: {layer['name']}")
    if "seed_formula" not in rule["overlay"]["determinism"]:
        fail("7", "overlay determinism.seed_formula missing")


def main() -> None:
    jars = sorted(ROOT.glob("mods/spore_*.jar"))
    if not jars:
        sys.exit("no mods/spore_*.jar found")
    jar = jars[-1]
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    rule = load_rule()

    check_1_2_3(manifest, jar)
    check_4_5(manifest, jar, rule)
    check_7_palette()
    check_6_idempotence()  # last: it re-runs the generator

    if failures:
        print(f"FAIL - {len(failures)} problem(s):")
        for f in failures:
            print("  " + f)
        sys.exit(1)
    print("PASS - roster, exclusions, textures, recolour fidelity, glow budget, "
          "idempotence, and palette map all check out")


if __name__ == "__main__":
    main()
