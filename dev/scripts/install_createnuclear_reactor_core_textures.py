from __future__ import annotations

import hashlib
import json
from pathlib import Path
from zipfile import ZipFile

from PIL import Image, ImageEnhance, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "ROOT_tools" / "createnuclear_authored_sources"
TARGET = (
    ROOT
    / "resourcepacks"
    / "LAST_DAYS_INFINITE_DOMAIN_1_21_1"
    / "assets"
    / "createnuclear"
    / "textures"
    / "block"
    / "reactor"
    / "core"
)
SIZE = 128
FRAMES = 6
FRAME_TIME = 5
MANIFEST = ROOT / "docs" / "last-days-createnuclear-derived-textures.json"
MODEL_PATH = "assets/createnuclear/models/block/reactor/core/block.json"
MODEL_TEXTURES = {
    "1": "createnuclear:block/reactor/core/reactor_core_casing",
    "2": "createnuclear:block/reactor/core/reactor_core_center",
    "3": "createnuclear:block/reactor/core/reactor_core_bars",
    "particle": "createnuclear:block/reactor/core/reactor_core_center",
}


def square_source(path: Path) -> Image.Image:
    image = Image.open(path).convert("RGB")
    edge = min(image.size)
    left = (image.width - edge) // 2
    top = (image.height - edge) // 2
    return image.crop((left, top, left + edge, top + edge))


def reduced(name: str) -> Image.Image:
    image = square_source(SOURCE / name).resize(
        (SIZE, SIZE), Image.Resampling.LANCZOS
    )
    return image.filter(ImageFilter.UnsharpMask(radius=0.8, percent=85, threshold=2))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_model_contract() -> Path:
    jars = sorted((ROOT / "mods").glob("createnuclear-*.jar"))
    if len(jars) != 1:
        raise RuntimeError(f"Expected one Create Nuclear jar, found: {jars}")
    with ZipFile(jars[0]) as archive:
        model = json.loads(archive.read(MODEL_PATH))
    if model.get("textures") != MODEL_TEXTURES:
        raise RuntimeError(
            "Create Nuclear reactor-core texture bindings changed; review the model "
            "before deriving replacement art."
        )
    return jars[0]


def record_manifest(mod_jar: Path, derived: list[tuple[Path, Path]]) -> None:
    sources = []
    for source in sorted(SOURCE.glob("*.png")):
        with Image.open(source) as image:
            size = list(image.size)
        sources.append(
            {
                "path": source.relative_to(ROOT).as_posix(),
                "sha256": sha256(source),
                "size": size,
                "role": "authoritative_full_resolution_source_art",
            }
        )

    outputs = []
    for output, source in derived:
        with Image.open(output) as image:
            size = list(image.size)
        outputs.append(
            {
                "path": output.relative_to(ROOT).as_posix(),
                "sha256": sha256(output),
                "size": size,
                "derived_from": source.relative_to(ROOT).as_posix(),
            }
        )

    manifest = {
        "authority": "full-resolution source art; runtime PNGs are derived outputs",
        "installed_mod": mod_jar.relative_to(ROOT).as_posix(),
        "model_contract": {
            "path_inside_mod": MODEL_PATH,
            "texture_bindings": MODEL_TEXTURES,
            "model_override_added": False,
            "uv_space": "16x16 normalized Minecraft block-model UVs",
        },
        "animation_contract": {
            "texture": "createnuclear:block/reactor/core/reactor_core_center",
            "frames": FRAMES,
            "frametime": FRAME_TIME,
            "method": "one authored center surface with restrained brightness phases",
        },
        "sources": sources,
        "derived_outputs": outputs,
        "installer": "scripts/install_createnuclear_reactor_core_textures.py",
        "model_aware_review": "scripts/render_createnuclear_reactor_core_face.py",
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    mod_jar = validate_model_contract()
    TARGET.mkdir(parents=True, exist_ok=True)

    casing = reduced("reactor_core_casing_material_master.png")
    bars = reduced("reactor_core_bars_material_master.png")
    center = reduced("reactor_core_center_material_master.png")

    casing.save(TARGET / "reactor_core_casing.png", optimize=True)
    bars.save(TARGET / "reactor_core_bars.png", optimize=True)

    # A restrained breathing cycle: preserve one authored surface and vary only
    # energy intensity, avoiding frame-to-frame detail chatter on the 3D model.
    phases = (0.78, 0.88, 1.00, 1.08, 1.00, 0.88)
    if len(phases) != FRAMES:
        raise RuntimeError("Animation phase count disagrees with compatibility contract")
    sheet = Image.new("RGB", (SIZE, SIZE * len(phases)))
    for index, brightness in enumerate(phases):
        frame = ImageEnhance.Brightness(center).enhance(brightness)
        sheet.paste(frame, (0, index * SIZE))
    sheet.save(TARGET / "reactor_core_center.png", optimize=True)

    (TARGET / "reactor_core_center.png.mcmeta").write_text(
        json.dumps({"animation": {"frametime": FRAME_TIME}}, indent=2) + "\n",
        encoding="utf-8",
    )

    record_manifest(
        mod_jar,
        [
            (
                TARGET / "reactor_core_casing.png",
                SOURCE / "reactor_core_casing_material_master.png",
            ),
            (
                TARGET / "reactor_core_bars.png",
                SOURCE / "reactor_core_bars_material_master.png",
            ),
            (
                TARGET / "reactor_core_center.png",
                SOURCE / "reactor_core_center_material_master.png",
            ),
        ],
    )

    print(f"installed={TARGET}")
    print(f"casing={casing.size}")
    print(f"bars={bars.size}")
    print(f"center={sheet.size} frames={len(phases)}")
    print(f"manifest={MANIFEST}")


if __name__ == "__main__":
    main()
