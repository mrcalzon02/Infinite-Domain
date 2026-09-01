"""Verify installed Infinite Domain companion JARs against their source projects."""

from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECTS = {
    "create-nuclear-balance": "infinite-domain-create-nuclear-balance-1.0.0.jar",
    "cyberware-mastery-expansion": "infinite-domain-cyberware-mastery-1.0.0.jar",
    "darknet-worldgen-patch": "infinite-domain-darknet-worldgen-1.8.0.jar",
    "echo-numismatics-bridge": "infinite-domain-echo-economy-1.0.0.jar",
    "hive-world-companion": "infinite-domain-hive-world-companion-0.1.0.jar",
    "lostcities-highway-compat": "infinite-domain-lostcities-highway-compat-1.0.0.jar",
    "overworld-terrain-companion": "infinite-domain-overworld-terrain-1.0.0.jar",
    "stellaris-space-industry": "infinite-domain-stellaris-industry-1.0.0.jar",
    "unified-radiation": "infinite-domain-unified-radiation-1.0.0.jar",
}


def installed_mod_ids() -> set[str]:
    result = {"minecraft", "neoforge"}
    for jar_path in (ROOT / "mods").glob("*.jar"):
        try:
            with zipfile.ZipFile(jar_path) as jar:
                name = "META-INF/neoforge.mods.toml"
                if name not in jar.namelist():
                    continue
                text = jar.read(name).decode("utf-8", errors="replace")
                primary = text.split("[[dependencies.", 1)[0]
                result.update(re.findall(r'(?m)^modId\s*=\s*"([a-z0-9_.-]+)"', primary))
        except (OSError, zipfile.BadZipFile):
            continue
    return result


def main() -> int:
    failures: list[str] = []
    summaries: list[str] = []
    available_mods = installed_mod_ids()
    for project_name, jar_name in PROJECTS.items():
        project = ROOT / "dev/packdev" / project_name
        jar_path = ROOT / "mods" / jar_name
        resource_root = project / "src/main/resources"
        java_root = project / "src/main/java"
        if not jar_path.is_file():
            failures.append(f"{project_name}: installed JAR missing: {jar_name}")
            continue
        if not resource_root.is_dir() or not java_root.is_dir():
            failures.append(f"{project_name}: source tree incomplete")
            continue
        with zipfile.ZipFile(jar_path) as jar:
            entries = {name for name in jar.namelist() if not name.endswith("/")}
            resource_files = [path for path in resource_root.rglob("*") if path.is_file()]
            stale_resources: list[str] = []
            missing_resources: list[str] = []
            for path in resource_files:
                member = path.relative_to(resource_root).as_posix()
                if member == "META-INF/MANIFEST.MF":
                    continue
                if member not in entries:
                    missing_resources.append(member)
                elif jar.read(member) != path.read_bytes():
                    stale_resources.append(member)
            if missing_resources:
                failures.append(f"{project_name}: resources absent from installed JAR: {', '.join(missing_resources)}")
            if stale_resources:
                failures.append(f"{project_name}: installed resources differ from source: {', '.join(stale_resources)}")

            java_files = [path for path in java_root.rglob("*.java")]
            missing_classes: list[str] = []
            for path in java_files:
                source = path.read_text(encoding="utf-8")
                package = re.search(r"(?m)^package\s+([a-zA-Z0-9_.]+);", source)
                public_type = re.search(r"(?m)^public\s+(?:final\s+)?(?:class|interface|enum|record)\s+([A-Za-z0-9_]+)", source)
                if not package or not public_type:
                    continue
                member = package.group(1).replace(".", "/") + "/" + public_type.group(1) + ".class"
                if member not in entries:
                    missing_classes.append(member)
            if missing_classes:
                failures.append(f"{project_name}: compiled classes absent from installed JAR: {', '.join(missing_classes)}")

            manifest = "META-INF/neoforge.mods.toml"
            if manifest not in entries:
                failures.append(f"{project_name}: NeoForge manifest missing")
                mod_id = "missing"
            else:
                manifest_text = jar.read(manifest).decode("utf-8")
                primary_mod_section = manifest_text.split("[[dependencies.", 1)[0]
                ids = re.findall(r'(?m)^modId\s*=\s*"([a-z0-9_.-]+)"', primary_mod_section)
                if len(ids) != 1:
                    failures.append(f"{project_name}: expected one manifest modId, found {ids}")
                mod_id = ids[0] if ids else "missing"
                if 'license=' not in manifest_text.replace(" ", ""):
                    failures.append(f"{project_name}: manifest license missing")
                for dependency in re.findall(r'(?m)^modId\s*=\s*"([a-z0-9_.-]+)"', manifest_text.split("[[dependencies.", 1)[1] if "[[dependencies." in manifest_text else ""):
                    if dependency not in available_mods:
                        failures.append(f"{project_name}: declared dependency is not installed: {dependency}")

                declared_mixins = re.findall(r'(?m)^config\s*=\s*"([a-z0-9_.-]+\.mixins\.json)"', manifest_text)
                jar_manifest = jar.read("META-INF/MANIFEST.MF").decode("utf-8", errors="replace") if "META-INF/MANIFEST.MF" in entries else ""
                declared_mixins.extend(re.findall(r"(?m)^MixinConfigs:\s*([^\r\n]+)", jar_manifest))
                declared_mixins = [name.strip() for group in declared_mixins for name in group.split(",")]
                packaged_mixins = sorted(name for name in entries if name.endswith(".mixins.json"))
                if sorted(set(declared_mixins)) != packaged_mixins:
                    failures.append(
                        f"{project_name}: mixin declarations do not match packaged configs: "
                        f"declared={sorted(set(declared_mixins))}, packaged={packaged_mixins}"
                    )
                for config_name in packaged_mixins:
                    config = json.loads(jar.read(config_name))
                    if config.get("required") is not True or config.get("compatibilityLevel") != "JAVA_21":
                        failures.append(f"{project_name}: unsafe mixin policy in {config_name}")
                    package = config.get("package", "").replace(".", "/")
                    for side in ("mixins", "client", "server"):
                        for class_name in config.get(side, []):
                            member = f"{package}/{class_name.replace('.', '/')}.class"
                            if member not in entries:
                                failures.append(f"{project_name}: declared mixin class missing: {member}")
            summaries.append(
                f"{project_name}: mod={mod_id}, source_resources={len(resource_files)}, "
                f"java_sources={len(java_files)}, jar_entries={len(entries)}"
            )

    for summary in summaries:
        print(f"PASS {summary}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        return 1
    print(f"Companion package audit passed for {len(PROJECTS)} installed projects.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
