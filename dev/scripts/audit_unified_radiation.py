from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "dev/packdev" / "unified-radiation"
RESOURCES = PROJECT / "src" / "main" / "resources"
SOURCE = PROJECT / "src" / "main" / "java" / "infinitedomain" / "radiation" / "InfiniteDomainRadiation.java"
OUTPUT = ROOT / "mods" / "infinite-domain-unified-radiation-1.0.0.jar"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"PASS  {message}")


def main() -> int:
    source = SOURCE.read_text(encoding="utf-8")
    config = (ROOT / "config" / "wastelands-common.toml").read_text(encoding="utf-8")

    installed = {
        "Wastelands": list((ROOT / "mods").glob("wastelands-*.jar")),
        "The Wasteland Reworked": list((ROOT / "mods").glob("the_wasteland_reworked-*.jar")),
        "Create: New Age": list((ROOT / "mods").glob("create-new-age-*.jar")),
        "Create Nuclear": list((ROOT / "mods").glob("createnuclear-*.jar")),
    }
    for name, matches in installed.items():
        require(len(matches) == 1, f"exactly one installed {name} jar")

    require("[radiation]" in config and "enabled = false" in config,
            "native Wastelands exposure loop is disabled after audit")
    require("RadiationManager.add" in source and "RadiationManager.remove" in source
            and "RadiationManager.get" in source and "RadiationManager.set" in source,
            "one Wastelands-backed persistent dose API")
    require(all(effect in source for effect in (
        'id("create_new_age", "radiation_poisoning")',
        'id("createnuclear", "radiation")',
        'id("the_wasteland_reworked", "radiation_poisoning")',
    )), "all foreign biological-effect paths are translated")
    require("player.removeEffect(effect)" in source and "LAST_EFFECT_DOSE" in source,
            "foreign effects are suppressed and translated at a bounded rate")
    require("Math.min(12, reading.ambient() + reading.contamination())" in source,
            "combined source intensity has one anti-overlap cap")
    require("WastelandConfig.RADIATION_EXPOSURE_INTERVAL.get()" in source
            and "WastelandConfig.RADIATION_DECAY_INTERVAL.get()" in source
            and "exposureInterval = 1200" in config,
            "unified adapter uses the configured sixty-second exposure interval")
    require("dx = -12; dx <= 12" in source and "dy = -6; dy <= 6" in source,
            "bounded per-player environmental scan")
    require("Math.floorMod(player.getId(), exposureInterval)" in source,
            "multiplayer scans are staggered")
    require("exposedToSky && level.getBiome(pos).is(RADIOACTIVE_AMBIENT)" in source,
            "roofed structures suppress radioactive-biome background exposure")

    tag_files = list((RESOURCES / "data" / "infinite_domain_radiation" / "tags").rglob("*.json"))
    require(len(tag_files) >= 16, "source, contamination, PPE, detector, shielding and biome tags exist")
    for path in tag_files:
        data = json.loads(path.read_text(encoding="utf-8"))
        require(isinstance(data.get("values"), list), f"valid tag values: {path.relative_to(RESOURCES)}")

    require(OUTPUT.is_file(), "compiled compatibility jar exists")
    with zipfile.ZipFile(OUTPUT) as jar:
        names = set(jar.namelist())
        required_entries = {
            "META-INF/neoforge.mods.toml",
            "infinitedomain/radiation/InfiniteDomainRadiation.class",
            "data/infinite_domain_radiation/tags/item/radiation_detectors.json",
            "data/infinite_domain_radiation/tags/worldgen/biome/radioactive_ambient.json",
            "data/create_new_age/tags/item/hazmat_suit.json",
            "data/create_new_age/tags/block/stops_radiation.json",
        }
        require(required_entries <= names, "compiled jar contains code and cross-mod tag adapters")

    print("\nUnified radiation static audit passed.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, OSError, ValueError, zipfile.BadZipFile) as exc:
        print(f"FAIL  {exc}", file=sys.stderr)
        raise SystemExit(1)
