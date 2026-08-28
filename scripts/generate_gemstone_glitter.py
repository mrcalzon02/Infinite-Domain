"""Generate the render-only "glitter" overlay for More Ores More Gems gemstone
blocks and gem ore blocks.

For every target block this emits, into the project resource overlay
``kubejs/assets/more_ores_more_gems/``:

* ``textures/block/glint/<sprite>_glint.png`` - a 32px, FRAMES-frame vertical
  strip that is fully transparent except for a few bright twinkle pixels, plus a
  ``.png.mcmeta`` whose frame ``time`` list is irregular (seeded per block) so no
  two gems pulse in lockstep.
* ``models/block/<model>.json`` - a two-element cube replacing the mod's
  ``cube_all`` model: element 1 is the untouched base texture with normal
  lighting and cullfaces; element 2 is the glint texture pushed ``PROUD`` proud,
  ``shade:false``, with ``neoforge_data.block_light`` on every face so the
  twinkle pixels render full-bright.

Nothing else is touched - not the base textures, not the Last Days pack, not the
More Ores More Gems derived-texture manifests.

Authority: docs/GEMSTONE_GLITTER_EFFECT.md
Verify:    python scripts/validate_gemstone_glitter.py
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import random
from pathlib import Path
from zipfile import ZipFile

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "mods" / "momg-1.1.9-release-neoforge-1.21.1.jar"
NAMESPACE = "more_ores_more_gems"
SCOPE = ROOT / "docs" / "more-ores-more-gems-texture-scope.csv"
LEDGER = ROOT / "docs" / "more-ores-more-gems-derived-textures.csv"
LAST_DAYS_TEX = (
    ROOT
    / "resourcepacks"
    / "LAST_DAYS_INFINITE_DOMAIN_1_21_1"
    / "assets"
    / NAMESPACE
    / "textures"
)
OVERLAY = ROOT / "kubejs" / "assets" / NAMESPACE
GLINT_DIR = OVERLAY / "textures" / "block" / "glint"
MODEL_DIR = OVERLAY / "models" / "block"
MANIFEST = ROOT / "docs" / "gemstone-glitter-manifest.json"

# ---- parameters (see docs/GEMSTONE_GLITTER_EFFECT.md) -----------------------
GLINT_RES = 32
FRAMES = 6
SITES_BASE = 8
SITES_JITTER = 3
GLINT_BLOCK_LIGHT = 15
GLINT_SKY_LIGHT = 15
STORAGE_BASE_BLOCK_LIGHT = 0
PROUD = 0.008
MCMETA_STEPS = 10
MCMETA_FRAMETIME = 3
INTEREST_MIN_FRACTION = 0.03  # ore mask fallback threshold

# metal storage block mis-categorised upstream as gem_storage_block
GEM_STORAGE_EXCLUDE = {"blockof_titanium"}


# ---- target discovery ------------------------------------------------------
def load_targets(mod: ZipFile) -> list[dict]:
    names = set(mod.namelist())

    gem_ore_ids = [
        row["RegistryId"].split(":", 1)[1]
        for row in csv.DictReader(LEDGER.open(encoding="utf-8"))
        if "gem containment" in row["Method"]
    ]
    storage_ids = [
        row["RegistryId"].split(":", 1)[1]
        for row in csv.DictReader(SCOPE.open(encoding="utf-8"))
        if row["Category"] == "gem_storage_block"
        and row["RegistryId"].split(":", 1)[1] not in GEM_STORAGE_EXCLUDE
    ]

    targets: list[dict] = []
    for category, ids in (("gem_ore", gem_ore_ids), ("gem_storage_block", storage_ids)):
        for short in ids:
            bs_path = f"assets/{NAMESPACE}/blockstates/{short}.json"
            if bs_path not in names:
                raise RuntimeError(f"no blockstate for {NAMESPACE}:{short}")
            blockstate = json.loads(mod.read(bs_path))
            model_ids = _models_in_blockstate(blockstate)
            if len(model_ids) != 1:
                raise RuntimeError(f"{short}: expected 1 model, got {sorted(model_ids)}")
            model_id = next(iter(model_ids))
            model_short = model_id.split(":")[-1].split("/", 1)[1]
            model = json.loads(mod.read(f"assets/{NAMESPACE}/models/block/{model_short}.json"))
            if model.get("parent") not in ("block/cube_all", "minecraft:block/cube_all"):
                raise RuntimeError(f"{short}: unexpected parent {model.get('parent')}")
            base_ref = model["textures"]["all"]
            sprite = base_ref.split(":", 1)[1].split("/", 1)[1]
            targets.append(
                {
                    "registry_id": f"{NAMESPACE}:{short}",
                    "category": category,
                    "model_short": model_short,
                    "sprite": sprite,
                    "base_ref": base_ref,
                }
            )
    targets.sort(key=lambda t: (t["category"], t["registry_id"]))
    return targets


def _models_in_blockstate(blockstate: dict) -> set[str]:
    models: set[str] = set()
    for value in blockstate.get("variants", {}).values():
        for entry in value if isinstance(value, list) else [value]:
            models.add(entry["model"])
    for part in blockstate.get("multipart", []):
        apply = part.get("apply")
        for entry in apply if isinstance(apply, list) else [apply] if apply else []:
            models.add(entry["model"])
    return models


# ---- base texture (for twinkle placement only) ----------------------------
def load_base_first_frame(mod: ZipFile, sprite: str) -> tuple[Image.Image, str]:
    disk = LAST_DAYS_TEX / "block" / f"{sprite}.png"
    if disk.is_file():
        image = Image.open(disk)
        source = "last_days"
    else:
        image = Image.open(io.BytesIO(mod.read(f"assets/{NAMESPACE}/textures/block/{sprite}.png")))
        source = "jar"
    image = image.convert("RGBA")
    frame_h = image.width if image.height % image.width == 0 else image.height
    first = image.crop((0, 0, image.width, min(frame_h, image.height)))
    return first.resize((GLINT_RES, GLINT_RES), Image.Resampling.NEAREST), source


def interest_sites(base: Image.Image, category: str, rng: random.Random, count: int) -> list[tuple[int, int]]:
    """Weighted twinkle-site picks. Storage blocks: uniform over the whole gem
    face. Ore blocks: weighted toward the most saturated/bright pixels (the
    contained gem) so twinkles land on the crystal, not the chassis."""
    pixels = base.load()
    whole_face = category == "gem_storage_block"
    weighted: list[tuple[tuple[int, int], float]] = []
    for y in range(GLINT_RES):
        for x in range(GLINT_RES):
            r, g, b, a = pixels[x, y]
            if a < 24:
                continue
            if whole_face:
                weighted.append(((x, y), 1.0))
                continue
            high, low = max(r, g, b), min(r, g, b)
            sat = 0.0 if high == 0 else (high - low) / high
            val = high / 255
            if sat > 0.28 and val > 0.22:
                weighted.append(((x, y), (sat ** 2) * val))

    if sum(w for _, w in weighted) <= 0 or len(weighted) < INTEREST_MIN_FRACTION * GLINT_RES * GLINT_RES:
        weighted = [
            ((x, y), 1.0)
            for y in range(GLINT_RES)
            for x in range(GLINT_RES)
            if pixels[x, y][3] >= 24
        ]
    if not weighted:
        weighted = [((x, y), 1.0) for y in range(GLINT_RES) for x in range(GLINT_RES)]

    positions = [p for p, _ in weighted]
    weights = [w for _, w in weighted]
    sites: list[tuple[int, int]] = []
    guard = 0
    while len(sites) < count and guard < count * 40:
        guard += 1
        pos = rng.choices(positions, weights=weights, k=1)[0]
        if all(abs(pos[0] - s[0]) + abs(pos[1] - s[1]) >= 2 for s in sites):
            sites.append(pos)
    while len(sites) < count:  # tiny interest region: allow closer packing
        sites.append(rng.choices(positions, weights=weights, k=1)[0])
    return sites


# ---- glint strip ---------------------------------------------------------
def build_glint(base: Image.Image, category: str, seed: bytes) -> Image.Image:
    rng = random.Random(seed)
    site_count = SITES_BASE + rng.randrange(SITES_JITTER + 1)
    sites = interest_sites(base, category, rng, site_count)
    base_px = base.load()

    specs = []
    for pos in sites:
        r, g, b, _ = base_px[pos[0], pos[1]]
        # mostly white, a hint of the local gem hue
        tint = (
            round(255 * 0.75 + r * 0.25),
            round(255 * 0.75 + g * 0.25),
            round(255 * 0.75 + b * 0.25),
        )
        specs.append(
            {
                "pos": pos,
                "phase": rng.randrange(FRAMES),
                "fast": rng.random() < 0.35,
                "width": rng.choice([1, 1, 1, 2]),
                "tint": tint,
                "gain": rng.uniform(0.75, 1.0),
            }
        )

    strip = Image.new("RGBA", (GLINT_RES, GLINT_RES * FRAMES), (0, 0, 0, 0))
    for frame in range(FRAMES):
        canvas = Image.new("RGBA", (GLINT_RES, GLINT_RES), (0, 0, 0, 0))
        px = canvas.load()
        for spec in specs:
            offset = (frame - spec["phase"]) % FRAMES
            if spec["fast"]:
                intensity = 1.0 if offset == 0 else 0.0
            else:
                intensity = {0: 1.0, 1: 0.65}.get(offset, 0.0)
            if intensity <= 0.0:
                continue
            intensity *= spec["gain"]
            x0, y0 = spec["pos"]
            _plot(px, x0, y0, spec["tint"], round(235 * intensity))
            if spec["width"] >= 2:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    _plot(px, x0 + dx, y0 + dy, spec["tint"], round(105 * intensity))
        strip.paste(canvas, (0, frame * GLINT_RES))
    return strip


def _plot(px, x: int, y: int, rgb: tuple[int, int, int], alpha: int) -> None:
    if not (0 <= x < GLINT_RES and 0 <= y < GLINT_RES) or alpha <= 0:
        return
    er, eg, eb, ea = px[x, y]
    a = min(255, max(ea, alpha))
    px[x, y] = (
        max(er, rgb[0]) if ea else rgb[0],
        max(eg, rgb[1]) if ea else rgb[1],
        max(eb, rgb[2]) if ea else rgb[2],
        a,
    )


def build_mcmeta(seed: bytes) -> dict:
    rng = random.Random(seed + b"mcmeta")
    frames: list[dict] = []
    for _ in range(MCMETA_STEPS):
        frames.append(
            {
                "index": rng.randrange(FRAMES),
                "time": rng.choice([1, 2, 2, 3, 3, 4, 5]),
            }
        )
    if len({f["index"] for f in frames}) < 2:
        frames = [{"index": i, "time": 3} for i in range(FRAMES)]
    return {"animation": {"interpolate": True, "frametime": MCMETA_FRAMETIME, "frames": frames}}


# ---- model override ----------------------------------------------------
_DIRS = ("north", "south", "east", "west", "up", "down")


def build_model(target: dict) -> dict:
    base_ref = target["base_ref"]
    glint_ref = f"{NAMESPACE}:block/glint/{target['sprite']}_glint"
    base_faces = {
        d: {"texture": "#base", "uv": [0, 0, 16, 16], "cullface": d} for d in _DIRS
    }
    base_light = (
        STORAGE_BASE_BLOCK_LIGHT if target["category"] == "gem_storage_block" else 0
    )
    if base_light:
        for face in base_faces.values():
            face["neoforge_data"] = {"block_light": base_light}
    glint_faces = {
        d: {
            "texture": "#glint",
            "uv": [0, 0, 16, 16],
            "neoforge_data": {"block_light": GLINT_BLOCK_LIGHT, "sky_light": GLINT_SKY_LIGHT},
        }
        for d in _DIRS
    }
    return {
        "__comment__": "generated by scripts/generate_gemstone_glitter.py - see docs/GEMSTONE_GLITTER_EFFECT.md",
        "parent": "minecraft:block/block",
        "render_type": "cutout_mipped",
        "textures": {"base": base_ref, "glint": glint_ref, "particle": base_ref},
        "elements": [
            {"from": [0, 0, 0], "to": [16, 16, 16], "faces": base_faces},
            {
                "from": [-PROUD, -PROUD, -PROUD],
                "to": [16 + PROUD, 16 + PROUD, 16 + PROUD],
                "shade": False,
                "faces": glint_faces,
            },
        ],
    }


# ---- driver ----------------------------------------------------------
def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    previous: set[str] = set()
    if MANIFEST.is_file():
        previous = {e["path"] for e in json.loads(MANIFEST.read_text())["files"]}

    with ZipFile(MOD) as mod:
        targets = load_targets(mod)
        bases = {t["sprite"]: load_base_first_frame(mod, t["sprite"]) for t in targets}

    GLINT_DIR.mkdir(parents=True, exist_ok=True)
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    written: set[str] = set()
    entries: list[dict] = []
    source_counts = {"last_days": 0, "jar": 0}

    for target in targets:
        sprite = target["sprite"]
        base, source = bases[sprite]
        source_counts[source] += 1
        seed = hashlib.blake2b(target["registry_id"].encode(), digest_size=16).digest()

        glint = build_glint(base, target["category"], seed)
        glint_path = GLINT_DIR / f"{sprite}_glint.png"
        glint.save(glint_path, optimize=True)

        mcmeta_path = GLINT_DIR / f"{sprite}_glint.png.mcmeta"
        mcmeta_path.write_text(json.dumps(build_mcmeta(seed), indent=2) + "\n", encoding="utf-8")

        model_path = MODEL_DIR / f"{target['model_short']}.json"
        model_path.write_text(json.dumps(build_model(target), indent=2) + "\n", encoding="utf-8")

        for path in (glint_path, mcmeta_path, model_path):
            rel = path.relative_to(ROOT).as_posix()
            written.add(rel)
            entries.append({"path": rel, "sha256": _sha256(path)})

        target["glint"] = glint_path.relative_to(ROOT).as_posix()
        target["mcmeta"] = mcmeta_path.relative_to(ROOT).as_posix()
        target["model"] = model_path.relative_to(ROOT).as_posix()
        target["base_source"] = source

    # drop files from a previous run whose target went away
    for rel in sorted(previous - written):
        stale = ROOT / rel
        if stale.is_file() and stale.is_relative_to(OVERLAY):
            stale.unlink()
            print(f"removed stale {rel}")

    manifest = {
        "generator": "scripts/generate_gemstone_glitter.py",
        "authority": "docs/GEMSTONE_GLITTER_EFFECT.md",
        "namespace": NAMESPACE,
        "parameters": {
            "glint_res": GLINT_RES,
            "frames": FRAMES,
            "sites_base": SITES_BASE,
            "sites_jitter": SITES_JITTER,
            "glint_block_light": GLINT_BLOCK_LIGHT,
            "glint_sky_light": GLINT_SKY_LIGHT,
            "storage_base_block_light": STORAGE_BASE_BLOCK_LIGHT,
            "proud": PROUD,
            "mcmeta_steps": MCMETA_STEPS,
        },
        "counts": {
            "targets": len(targets),
            "gem_ore": sum(t["category"] == "gem_ore" for t in targets),
            "gem_storage_block": sum(t["category"] == "gem_storage_block" for t in targets),
            "base_from_last_days": source_counts["last_days"],
            "base_from_jar": source_counts["jar"],
        },
        "targets": [
            {
                k: t[k]
                for k in (
                    "registry_id",
                    "category",
                    "sprite",
                    "base_ref",
                    "model",
                    "glint",
                    "mcmeta",
                    "base_source",
                )
            }
            for t in targets
        ],
        "files": sorted(entries, key=lambda e: e["path"]),
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    print(f"targets       {len(targets)} ({manifest['counts']['gem_ore']} ore + "
          f"{manifest['counts']['gem_storage_block']} storage)")
    print(f"base textures  last_days={source_counts['last_days']} jar={source_counts['jar']}")
    print(f"files written  {len(written)}")
    print(f"manifest       {MANIFEST.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
