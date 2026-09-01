from __future__ import annotations

import hashlib
import json
import re
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "structure_library" / "licensing" / "provenance.json"
RESOURCE_ID = re.compile(r"^[a-z0-9_.-]+:[a-z0-9_./-]+$")
REQUIRED = {
    "structure_id", "source_kind", "source_project", "source_author", "source_url",
    "source_license", "license_classification", "required_attribution",
    "commercial_use_allowed", "modification_allowed", "redistribution_allowed",
    "original_minecraft_version", "original_format", "original_filename", "sha256",
    "conversion_history", "our_modifications", "integration_status",
}
CLASSIFICATIONS = {
    "approved_for_redistribution", "approved_with_attribution", "modification_only",
    "permission_required", "reference_only", "rejected",
}


def main() -> None:
    document = json.loads(MANIFEST.read_text(encoding="utf-8"))
    records = document.get("records", [])
    issues: list[str] = []
    seen: set[str] = set()
    for index, record in enumerate(records):
        label = record.get("structure_id", f"record[{index}]")
        missing = sorted(REQUIRED - set(record))
        if missing:
            issues.append(f"{label}: missing fields {missing}")
            continue
        if not RESOURCE_ID.fullmatch(record["structure_id"]):
            issues.append(f"{label}: invalid resource ID")
        if label in seen:
            issues.append(f"{label}: duplicate record")
        seen.add(label)
        if record["license_classification"] not in CLASSIFICATIONS:
            issues.append(f"{label}: invalid license classification")
        if record["license_classification"] in {"approved_for_redistribution", "approved_with_attribution"}:
            if not record["redistribution_allowed"] or not record["modification_allowed"]:
                issues.append(f"{label}: approved classification conflicts with permission flags")
        if "source_archive" in record and "source_member" in record:
            archive_path = (ROOT / record["source_archive"]).resolve()
            try:
                archive_path.relative_to(ROOT.resolve())
            except ValueError:
                issues.append(f"{label}: source archive escapes repository")
                continue
            if not archive_path.is_file():
                issues.append(f"{label}: source archive missing")
                continue
            try:
                with zipfile.ZipFile(archive_path) as archive:
                    source_raw = archive.read(record["source_member"])
            except (KeyError, OSError, zipfile.BadZipFile) as error:
                issues.append(f"{label}: unreadable source archive member ({error})")
                continue
            digest = hashlib.sha256(source_raw).hexdigest()
            converted_path = (ROOT / record.get("converted_filename", "")).resolve()
            if not converted_path.is_file():
                issues.append(f"{label}: converted file missing")
            elif hashlib.sha256(converted_path.read_bytes()).hexdigest() != record.get("converted_sha256"):
                issues.append(f"{label}: converted SHA-256 no longer matches")
        else:
            relative = Path(record["original_filename"])
            path = (ROOT / relative).resolve()
            try:
                path.relative_to(ROOT.resolve())
            except ValueError:
                issues.append(f"{label}: source path escapes repository")
                continue
            if not path.is_file():
                issues.append(f"{label}: source file missing")
                continue
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != record["sha256"]:
            issues.append(f"{label}: SHA-256 no longer matches source")
        if "converted_filename" in record:
            converted_path = (ROOT / record["converted_filename"]).resolve()
            try:
                converted_path.relative_to(ROOT.resolve())
            except ValueError:
                issues.append(f"{label}: converted path escapes repository")
            else:
                if not converted_path.is_file():
                    issues.append(f"{label}: converted file missing")
                elif hashlib.sha256(converted_path.read_bytes()).hexdigest() != record.get("converted_sha256"):
                    issues.append(f"{label}: converted SHA-256 no longer matches")
        if not isinstance(record["conversion_history"], list) or not record["conversion_history"]:
            issues.append(f"{label}: conversion history is empty")
        if not isinstance(record["our_modifications"], list):
            issues.append(f"{label}: modifications must be a list")

    if len(records) < 87:
        issues.append(f"expected at least 87 provenance records, found {len(records)}")
    if issues:
        raise SystemExit("\n".join(issues))
    print(f"Validated {len(records)} structure provenance records, source/converted hashes, permissions and paths")


if __name__ == "__main__":
    main()
