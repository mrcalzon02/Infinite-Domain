from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import re
import zipfile
from pathlib import Path


NEOFORGE_VERSION = "21.1.248"
MINECRAFT_VERSION = "1.21.1"
ARGUMENT_RELATIVE = Path(
    "libraries/net/neoforged/neoforge"
) / NEOFORGE_VERSION / "win_args.txt"
SERVER_JAR_RELATIVE = Path(
    "libraries/net/neoforged/neoforge"
) / NEOFORGE_VERSION / f"neoforge-{NEOFORGE_VERSION}-server.jar"
REQUIRED_ARGUMENTS = (
    "-DlegacyClassPath=",
    "cpw.mods.bootstraplauncher.BootstrapLauncher",
    "--launchTarget forgeserver",
    f"--fml.neoForgeVersion {NEOFORGE_VERSION}",
    f"--fml.mcVersion {MINECRAFT_VERSION}",
)
JAR_REFERENCE = re.compile(r"libraries/[A-Za-z0-9_.+@/-]+\.jar")
REPOSITORY = Path(__file__).resolve().parents[2]
SERVER_MOD_POLICY = REPOSITORY / "dev/scripts" / "worldgen_benchmark_server_mod_policy.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inspect_zip(path: Path, display_path: str, required_entries: tuple[str, ...]) -> dict[str, object]:
    with zipfile.ZipFile(path) as archive:
        corrupt = archive.testzip()
        names = set(archive.namelist())
    missing = [entry for entry in required_entries if entry not in names]
    return {
        "path": display_path,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "zip_integrity": corrupt is None,
        "missing_entries": missing,
    }


def inspect_server_mod_policy() -> dict[str, object]:
    payload = json.loads(SERVER_MOD_POLICY.read_text(encoding="utf-8"))
    mods = sorted((REPOSITORY / "mods").glob("*.jar"), key=lambda path: path.name.lower())
    exclusions = payload.get("exclusions", [])
    errors: list[str] = []
    matches: list[dict[str, object]] = []
    claimed: dict[str, str] = {}
    if payload.get("schemaVersion") != 1:
        errors.append("schemaVersion must be 1")
    if not isinstance(exclusions, list) or not exclusions:
        errors.append("exclusions must be a non-empty list")
        exclusions = []
    for index, entry in enumerate(exclusions):
        if not isinstance(entry, dict):
            errors.append(f"exclusions[{index}] must be an object")
            continue
        pattern = entry.get("pattern")
        reason = entry.get("reason")
        evidence = entry.get("evidence")
        if not all(isinstance(value, str) and value.strip() for value in (pattern, reason, evidence)):
            errors.append(f"exclusions[{index}] requires non-empty pattern, reason, and evidence")
            continue
        selected = [path for path in mods if fnmatch.fnmatchcase(path.name.lower(), pattern.lower())]
        if len(selected) != 1:
            errors.append(f"{pattern!r} matched {len(selected)} jars; expected exactly one")
        for path in selected:
            prior = claimed.get(path.name)
            if prior is not None:
                errors.append(f"{path.name} is claimed by both {prior!r} and {pattern!r}")
            claimed[path.name] = pattern
            integrity = None
            try:
                with zipfile.ZipFile(path) as archive:
                    integrity = archive.testzip()
            except (OSError, zipfile.BadZipFile) as exc:
                integrity = str(exc)
            if integrity is not None:
                errors.append(f"excluded archive {path.name} failed ZIP integrity: {integrity}")
            matches.append({
                "pattern": pattern,
                "jar": path.name,
                "reason": reason,
                "evidence": evidence,
                "sha256": sha256(path),
            })
    if not any(row["jar"].lower().startswith("sodium-neoforge-") for row in matches):
        errors.append("policy must exclude the evidenced Sodium dedicated-server bootstrap failure")
    return {
        "path": SERVER_MOD_POLICY.relative_to(REPOSITORY).as_posix(),
        "schema_version": payload.get("schemaVersion"),
        "source_mod_count": len(mods),
        "excluded_mod_count": len(matches),
        "matches": matches,
        "errors": errors,
        "sha256": sha256(SERVER_MOD_POLICY),
    }


def validate(root: Path) -> dict[str, object]:
    root = root.resolve()
    argument_file = root / ARGUMENT_RELATIVE
    server_jar = root / SERVER_JAR_RELATIVE
    if not argument_file.is_file():
        raise FileNotFoundError(f"Missing NeoForge server argument file: {argument_file}")
    if not server_jar.is_file():
        raise FileNotFoundError(f"Missing patched NeoForge server jar: {server_jar}")

    argument_text = argument_file.read_text(encoding="utf-8")
    missing_arguments = [token for token in REQUIRED_ARGUMENTS if token not in argument_text]
    references = sorted(set(JAR_REFERENCE.findall(argument_text)))
    missing_libraries = [reference for reference in references if not (root / reference).is_file()]
    modlauncher_references = [reference for reference in references if "/modlauncher/" in reference]
    bootstrap_references = [reference for reference in references if "/bootstraplauncher/" in reference]

    artifacts: dict[str, object] = {
        "argument_file": {
            "path": ARGUMENT_RELATIVE.as_posix(),
            "bytes": argument_file.stat().st_size,
            "sha256": sha256(argument_file),
        },
        "server_jar": inspect_zip(
            server_jar,
            SERVER_JAR_RELATIVE.as_posix(),
            (
                "net/minecraft/server/Main.class",
                "net/minecraft/world/level/chunk/ChunkAccess.class",
            ),
        ),
    }
    if len(modlauncher_references) == 1:
        artifacts["modlauncher"] = inspect_zip(
            root / modlauncher_references[0],
            modlauncher_references[0],
            (
                "cpw/mods/modlauncher/BootstrapLaunchConsumer.class",
                "module-info.class",
            ),
        )
    if len(bootstrap_references) == 1:
        artifacts["bootstraplauncher"] = inspect_zip(
            root / bootstrap_references[0],
            bootstrap_references[0],
            (
                "cpw/mods/bootstraplauncher/BootstrapLauncher.class",
                "module-info.class",
            ),
        )

    artifact_failures = [
        label
        for label, artifact in artifacts.items()
        if isinstance(artifact, dict)
        and (artifact.get("zip_integrity") is False or artifact.get("missing_entries"))
    ]
    server_mod_policy = inspect_server_mod_policy()
    checks = {
        "required_arguments": not missing_arguments,
        "referenced_libraries": bool(references) and not missing_libraries,
        "single_modlauncher": len(modlauncher_references) == 1,
        "single_bootstraplauncher": len(bootstrap_references) == 1,
        "artifact_integrity": not artifact_failures,
        "server_mod_policy": not server_mod_policy["errors"],
    }
    report = {
        "schema_version": 1,
        "neoforge_version": NEOFORGE_VERSION,
        "minecraft_version": MINECRAFT_VERSION,
        "status": "pass" if all(checks.values()) else "fail",
        "checks": checks,
        "referenced_library_count": len(references),
        "missing_arguments": missing_arguments,
        "missing_libraries": missing_libraries,
        "artifact_failures": artifact_failures,
        "artifacts": artifacts,
        "server_mod_policy": server_mod_policy,
        "scope": "archive, official argument contract, and evidenced headless-mod exclusions; does not claim a server boot or world-generation result",
    }
    if report["status"] != "pass":
        raise RuntimeError(json.dumps(report, indent=2))
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the pinned worldgen benchmark server launcher")
    parser.add_argument(
        "--root",
        type=Path,
        default=REPOSITORY / "benchmark_runs" / ".launcher-cache" / f"neoforge-{NEOFORGE_VERSION}-server",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = validate(args.root)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(
        f"Worldgen benchmark launcher passed {sum(report['checks'].values())}/{len(report['checks'])} checks "
        f"across {report['referenced_library_count']} referenced libraries"
    )


if __name__ == "__main__":
    main()
