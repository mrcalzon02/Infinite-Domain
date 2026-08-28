"""Validate the More Ores More Gems gemstone glitter overlay.

Checks, for the 107 target blocks:

* every target has a glint strip, a ``.png.mcmeta`` and a model override;
* the strip is ``GLINT_RES`` wide and ``GLINT_RES * FRAMES`` tall, RGBA;
* the mcmeta parses, ``interpolate`` is on, every frame index is in range and at
  least two distinct frames are used;
* the model parses, is a two-element cube, keeps the upstream base texture,
  points ``#glint`` at this target's strip, uses a cutout render type, and puts
  ``neoforge_data.block_light`` on all six glint faces;
* the overlay directory contains nothing the manifest does not list;
* re-running the generator in memory reproduces identical glint **pixels** and an
  identical model dict for every target (encoder-agnostic determinism check).

Exit code 0 = clean, 1 = one or more failures.

Authority: docs/GEMSTONE_GLITTER_EFFECT.md
"""

from __future__ import annotations

import io
import json
from pathlib import Path
from zipfile import ZipFile

from PIL import Image

import generate_gemstone_glitter as gen

ROOT = gen.ROOT
OVERLAY = gen.OVERLAY
MANIFEST = gen.MANIFEST
DIRS = gen._DIRS


def main() -> int:
    failures: list[str] = []

    def check(cond: bool, message: str) -> None:
        if not cond:
            failures.append(message)

    if not MANIFEST.is_file():
        print("FAIL  manifest missing - run scripts/generate_gemstone_glitter.py")
        return 1
    manifest = json.loads(MANIFEST.read_text())

    with ZipFile(gen.MOD) as mod:
        targets = gen.load_targets(mod)
        bases = {t["sprite"]: gen.load_base_first_frame(mod, t["sprite"]) for t in targets}

    manifest_ids = {t["registry_id"] for t in manifest["targets"]}
    live_ids = {t["registry_id"] for t in targets}
    check(manifest_ids == live_ids, f"manifest/target drift: {manifest_ids ^ live_ids}")

    expected_files = {e["path"] for e in manifest["files"]}
    actual_files = {
        p.relative_to(ROOT).as_posix()
        for p in OVERLAY.rglob("*")
        if p.is_file()
    }
    check(
        not (actual_files - expected_files),
        f"unlisted files in overlay: {sorted(actual_files - expected_files)}",
    )
    check(
        not (expected_files - actual_files),
        f"manifest files missing on disk: {sorted(expected_files - actual_files)}",
    )

    for target in targets:
        rid = target["registry_id"]
        sprite = target["sprite"]
        seed = gen.hashlib.blake2b(rid.encode(), digest_size=16).digest()
        glint_path = gen.GLINT_DIR / f"{sprite}_glint.png"
        mcmeta_path = gen.GLINT_DIR / f"{sprite}_glint.png.mcmeta"
        model_path = gen.MODEL_DIR / f"{target['model_short']}.json"

        if not (glint_path.is_file() and mcmeta_path.is_file() and model_path.is_file()):
            check(False, f"{rid}: missing output file(s)")
            continue

        # --- strip geometry + determinism ---
        disk = Image.open(glint_path).convert("RGBA")
        check(
            disk.size == (gen.GLINT_RES, gen.GLINT_RES * gen.FRAMES),
            f"{rid}: strip size {disk.size} != {(gen.GLINT_RES, gen.GLINT_RES * gen.FRAMES)}",
        )
        rebuilt = gen.build_glint(bases[sprite][0], target["category"], seed)
        check(disk.tobytes() == rebuilt.tobytes(), f"{rid}: glint pixels not reproducible")
        check(
            disk.getchannel("A").getbbox() is not None,
            f"{rid}: glint strip is fully transparent",
        )

        # --- mcmeta ---
        try:
            meta = json.loads(mcmeta_path.read_text())["animation"]
        except Exception as exc:  # noqa: BLE001
            check(False, f"{rid}: mcmeta unreadable ({exc})")
        else:
            check(meta.get("interpolate") is True, f"{rid}: mcmeta interpolate not true")
            idx = [f["index"] if isinstance(f, dict) else f for f in meta["frames"]]
            check(all(0 <= i < gen.FRAMES for i in idx), f"{rid}: mcmeta frame index out of range")
            check(len(set(idx)) >= 2, f"{rid}: mcmeta uses a single frame")
            check(meta == gen.build_mcmeta(seed)["animation"], f"{rid}: mcmeta not reproducible")

        # --- model ---
        try:
            model = json.loads(model_path.read_text())
        except Exception as exc:  # noqa: BLE001
            check(False, f"{rid}: model unreadable ({exc})")
            continue
        check(model == gen.build_model(target), f"{rid}: model not reproducible")
        check(
            "cutout" in str(model.get("render_type", "")),
            f"{rid}: model render_type is not a cutout type",
        )
        check(
            model.get("textures", {}).get("base") == target["base_ref"],
            f"{rid}: model #base {model.get('textures', {}).get('base')} != {target['base_ref']}",
        )
        check(
            model.get("textures", {}).get("glint") == f"{gen.NAMESPACE}:block/glint/{sprite}_glint",
            f"{rid}: model #glint ref wrong",
        )
        elements = model.get("elements", [])
        check(len(elements) == 2, f"{rid}: model has {len(elements)} elements, expected 2")
        if len(elements) == 2:
            glint_faces = elements[1].get("faces", {})
            check(set(glint_faces) == set(DIRS), f"{rid}: glint element missing faces")
            for direction, face in glint_faces.items():
                check(
                    face.get("texture") == "#glint"
                    and face.get("neoforge_data", {}).get("block_light") == gen.GLINT_BLOCK_LIGHT,
                    f"{rid}: glint face {direction} not emissive #glint",
                )
            check(elements[1].get("shade") is False, f"{rid}: glint element not shade:false")

    # --- manifest hashes still match disk ---
    for entry in manifest["files"]:
        path = ROOT / entry["path"]
        if path.is_file():
            check(
                gen._sha256(path) == entry["sha256"],
                f"{entry['path']}: sha256 differs from manifest (regenerate)",
            )

    print(f"targets checked   {len(targets)}")
    print(f"files in manifest {len(manifest['files'])}")
    if failures:
        print(f"\nFAIL  {len(failures)} problem(s):")
        for message in failures:
            print(f"  - {message}")
        return 1
    print("\nOK  gemstone glitter overlay is consistent and reproducible")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
