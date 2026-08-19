"""Resolve model, texture, override, and animation references in authored assets."""

from __future__ import annotations

import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "kubejs/assets"


def resource_path(kind: str, value: str, default_namespace: str, suffix: str) -> str:
    namespace, path = value.split(":", 1) if ":" in value else (default_namespace, value)
    return f"assets/{namespace}/{kind}/{path}{suffix}"


def main() -> int:
    available = {
        f"assets/{path.relative_to(ASSETS).as_posix()}"
        for path in ASSETS.rglob("*") if path.is_file()
    }
    archives = list((ROOT / "mods").glob("*.jar"))
    client_jar = ROOT.parents[1] / "Install/versions/1.21.1/1.21.1.jar"
    if client_jar.is_file():
        archives.append(client_jar)
    for jar_path in archives:
        try:
            with zipfile.ZipFile(jar_path) as jar:
                available.update(name for name in jar.namelist() if name.startswith("assets/") and not name.endswith("/"))
        except (OSError, zipfile.BadZipFile):
            continue

    failures: list[str] = []
    models = sorted(ASSETS.glob("*/models/**/*.json"))
    for path in models:
        namespace = path.relative_to(ASSETS).parts[0]
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        parent = data.get("parent")
        if isinstance(parent, str) and not parent.startswith("builtin/"):
            expected = resource_path("models", parent, "minecraft", ".json")
            if expected not in available:
                failures.append(f"{path.relative_to(ROOT)}: missing parent {parent}")
        for texture in data.get("textures", {}).values():
            if isinstance(texture, str) and not texture.startswith("#"):
                expected = resource_path("textures", texture, namespace, ".png")
                if expected not in available:
                    failures.append(f"{path.relative_to(ROOT)}: missing texture {texture}")
        for override in data.get("overrides", []):
            model = override.get("model") if isinstance(override, dict) else None
            if isinstance(model, str):
                expected = resource_path("models", model, namespace, ".json")
                if expected not in available:
                    failures.append(f"{path.relative_to(ROOT)}: missing override model {model}")

    metadata = sorted(ASSETS.rglob("*.png.mcmeta"))
    for path in metadata:
        png = path.with_suffix("")
        if not png.is_file():
            failures.append(f"{path.relative_to(ROOT)}: animation metadata has no PNG")

    if failures:
        print("\n".join(f"FAIL {failure}" for failure in failures))
        return 1
    print(f"Authored asset audit passed: {len(models)} models and {len(metadata)} animations resolve all parents, textures, and overrides.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
