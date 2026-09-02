"""Reproducible build for the Wasteland Hex Caves runtime mod.

The 1.0.0 jar that shipped on 2026-08-31 was compiled against the wrong
Minecraft classes: its constant pool referenced `net/minecraft/core/ResourceKey`
while NeoForge 21.1.248 provides `net/minecraft/resources/ResourceKey`, so
`NeoForgeRegistries.Keys.BIOME_MODIFIER_SERIALIZERS` failed to resolve and mod
construction died with NoSuchFieldError on both client and dedicated server.
The Java source was always correct - only the binary was wrong - so this script
exists to make the binary a reproducible function of the source.

It compiles against the *same* pinned NeoForge 21.1.248 dedicated-server
installation the worldgen benchmark already bootstraps
(`benchmark_runs/.launcher-cache/`), so the descriptors the mod is compiled
against are by construction the ones present at runtime. No network access and
no Gradle: the classpath is the launcher cache's own library tree.

The jar is written with fixed entry order and a fixed timestamp, so rebuilding
unchanged sources reproduces the same bytes.

Run:  python dev/scripts/build_wasteland_hex_caves.py
      python dev/scripts/build_wasteland_hex_caves.py --check   (verify only)
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "dev/packdev/wasteland-hex-caves"
SOURCES = PROJECT / "src/main/java"
RESOURCES = PROJECT / "src/main/resources"
OUTPUT = ROOT / "mods/infinite-domain-wasteland-hex-caves-1.0.0.jar"

NEOFORGE_VERSION = "21.1.248"
LAUNCHER = ROOT / f"benchmark_runs/.launcher-cache/neoforge-{NEOFORGE_VERSION}-server"
LIBRARIES = LAUNCHER / "libraries"
# NeoForge 1.20.2+ runs on Mojang-official names; the installer's "-srg" server
# jar is the artifact that actually carries them (verified: it is the only one
# containing net/minecraft/resources/ResourceKey.class).
MINECRAFT_JAR = (
    LIBRARIES / "net/minecraft/server/1.21.1-20240808.144430"
    / "server-1.21.1-20240808.144430-srg.jar"
)

RELEASE = "21"
# A fixed DOS timestamp keeps rebuilds byte-identical.
ZIP_TIMESTAMP = (2026, 1, 1, 0, 0, 0)

MANIFEST = (
    "Manifest-Version: 1.0\r\n"
    "Implementation-Title: Infinite Domain Wasteland Hex Caves\r\n"
    "Implementation-Version: 1.0.0\r\n"
    "\r\n"
)

# The symbol whose mis-resolution broke the shipped jar, and the package it must
# resolve to. Asserted on every build so the failure cannot silently return.
REQUIRED_REF = b"net/minecraft/resources/ResourceKey"
FORBIDDEN_REF = b"net/minecraft/core/ResourceKey"


def find_javac() -> Path:
    candidates: list[Path] = []
    if shutil.which("javac"):
        candidates.append(Path(shutil.which("javac")))
    for base in (Path(r"C:/Program Files/Java"), Path(r"C:/Program Files/Eclipse Adoptium")):
        if base.is_dir():
            candidates.extend(sorted(base.glob("*/bin/javac.exe"), reverse=True))
    for candidate in candidates:
        try:
            out = subprocess.run(
                [str(candidate), "-version"], capture_output=True, text=True, check=True
            )
        except (OSError, subprocess.CalledProcessError):
            continue
        version = (out.stdout + out.stderr).split()[-1]
        major = int(version.split(".")[0])
        if major >= int(RELEASE):
            return candidate
    raise SystemExit(
        f"no javac capable of --release {RELEASE} found; install a JDK {RELEASE}+"
    )


def classpath() -> str:
    if not MINECRAFT_JAR.is_file():
        raise SystemExit(
            f"missing {MINECRAFT_JAR}\n"
            "Bootstrap the pinned server first:\n"
            "  powershell -File dev/scripts/bootstrap_worldgen_benchmark_server.ps1"
        )
    jars = [MINECRAFT_JAR] + sorted(LIBRARIES.rglob("*.jar"))
    seen, ordered = set(), []
    for jar in jars:
        if jar not in seen:
            seen.add(jar)
            ordered.append(str(jar))
    return ";" .join(ordered) if sys.platform == "win32" else ":".join(ordered)


def compile_classes(target: Path) -> list[Path]:
    javac = find_javac()
    sources = sorted(SOURCES.rglob("*.java"))
    if not sources:
        raise SystemExit(f"no sources under {SOURCES}")
    cmd = [
        str(javac),
        "--release", RELEASE,
        "-nowarn",
        "-classpath", classpath(),
        "-d", str(target),
        *[str(s) for s in sources],
    ]
    print(f"javac : {javac}")
    print(f"sources: {len(sources)} file(s)")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        sys.stderr.write(result.stdout + result.stderr)
        raise SystemExit("compilation failed")
    if result.stderr.strip():
        print(result.stderr.strip())
    return sorted(target.rglob("*.class"))


def verify_descriptors(classes: list[Path]) -> None:
    """The exact regression that shipped: assert it cannot ship again."""
    blob = b"".join(p.read_bytes() for p in classes)
    if FORBIDDEN_REF in blob:
        raise SystemExit(
            f"built classes still reference {FORBIDDEN_REF.decode()} - "
            "the compile classpath is wrong, refusing to write the jar"
        )
    if REQUIRED_REF not in blob:
        raise SystemExit(
            f"built classes never reference {REQUIRED_REF.decode()} - "
            "unexpected; refusing to write the jar"
        )
    print(f"verified: references {REQUIRED_REF.decode()}, "
          f"never {FORBIDDEN_REF.decode()}")


def package(classes_root: Path, classes: list[Path], destination: Path) -> None:
    entries: list[tuple[str, bytes]] = [("META-INF/MANIFEST.MF", MANIFEST.encode())]
    for path in classes:
        entries.append((path.relative_to(classes_root).as_posix(), path.read_bytes()))
    if RESOURCES.is_dir():
        for path in sorted(RESOURCES.rglob("*")):
            if path.is_file():
                entries.append((path.relative_to(RESOURCES).as_posix(), path.read_bytes()))
    entries.sort(key=lambda item: item[0])

    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, payload in entries:
            info = zipfile.ZipInfo(name, date_time=ZIP_TIMESTAMP)
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, payload)
    print(f"wrote  : {destination.relative_to(ROOT)} ({destination.stat().st_size:,} bytes, "
          f"{len(entries)} entries)")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true",
        help="compile and verify descriptors without replacing the jar",
    )
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp)
        classes = compile_classes(target)
        print(f"classes: {len(classes)}")
        verify_descriptors(classes)
        if args.check:
            print("check only - jar not written")
            return
        package(target, classes, OUTPUT)


if __name__ == "__main__":
    main()
