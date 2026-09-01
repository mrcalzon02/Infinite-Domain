from __future__ import annotations

import hashlib
import json
import re
import zipfile
from pathlib import Path

from generate_wasteland_sites import DATA_VERSION, NbtList, TAG_COMPOUND, TAG_INT, write_nbt
from inventory_creativelands import ARCHIVE, BLOCK, COMMIT, ROOT, ROOT_PREFIX, coordinate


INVENTORY = ROOT / "dev/structure_library" / "sources" / "quarantine" / "creativelands_cc0" / "inventory.json"
OUTPUT_ROOT = ROOT / "dev/structure_library" / "extracted" / "creativelands_cc0"
REPORT = OUTPUT_ROOT / "conversion-report.json"
PROVENANCE = ROOT / "dev/structure_library" / "licensing" / "creativelands-extracted-provenance.json"
SAFE = re.compile(r"[^a-z0-9_./-]+")


def parse_state(state: str) -> tuple[str, dict[str, str]]:
    if "[" not in state:
        return state, {}
    if not state.endswith("]"):
        raise ValueError(f"Malformed block state {state!r}")
    name, raw_properties = state[:-1].split("[", 1)
    properties = {}
    for item in raw_properties.split(","):
        key, value = item.split("=", 1)
        properties[key] = value
    return name, properties


def resource_path(relative: str) -> str:
    stem = str(Path(relative).with_suffix("")).replace("\\", "/").lower()
    return SAFE.sub("_", stem)


def main() -> None:
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    candidates = {
        relative: entry
        for relative, entry in inventory["structures"].items()
        if entry["category"] != "trees" and entry["conversion_status"] == "direct_geometry_extract_candidate"
    }
    records = []
    results = {}
    seen_ids = set()
    with zipfile.ZipFile(ARCHIVE) as archive:
        for relative, inventory_entry in sorted(candidates.items()):
            member = ROOT_PREFIX + "structures/data/" + relative
            source_raw = archive.read(member)
            text = source_raw.decode("utf-8", errors="strict")
            placements: dict[tuple[int, int, int], tuple[str, dict[str, str]]] = {}
            statements = 0
            for line_number, line in enumerate(text.splitlines(), start=1):
                match = BLOCK.search(line)
                if not match:
                    continue
                if line[: match.start()].strip():
                    raise ValueError(f"{relative}:{line_number}: conditional block escaped inventory gate")
                x_expression, y_expression, z_expression, state = match.groups()
                position = (
                    coordinate(x_expression),
                    coordinate(y_expression, "y"),
                    coordinate(z_expression),
                )
                if any(value is None for value in position):
                    raise ValueError(f"{relative}:{line_number}: dynamic coordinate escaped inventory gate")
                placements[position] = parse_state(state)
                statements += 1
            if not placements:
                raise ValueError(f"{relative}: no deterministic block placements")
            low = [min(position[axis] for position in placements) for axis in range(3)]
            high = [max(position[axis] for position in placements) for axis in range(3)]
            size = [high[axis] - low[axis] + 1 for axis in range(3)]
            palette = []
            palette_ids = {}
            blocks = []
            for position, (name, properties) in sorted(placements.items(), key=lambda row: (row[0][1], row[0][2], row[0][0])):
                key = (name, tuple(sorted(properties.items())))
                if key not in palette_ids:
                    palette_entry = {"Name": name}
                    if properties:
                        palette_entry["Properties"] = dict(sorted(properties.items()))
                    palette_ids[key] = len(palette)
                    palette.append(palette_entry)
                shifted = [position[axis] - low[axis] for axis in range(3)]
                blocks.append({"pos": NbtList(TAG_INT, shifted), "state": palette_ids[key]})
            document = {
                "DataVersion": DATA_VERSION,
                "size": NbtList(TAG_INT, size),
                "palette": NbtList(TAG_COMPOUND, palette),
                "blocks": NbtList(TAG_COMPOUND, blocks),
                "entities": NbtList(TAG_COMPOUND, []),
            }
            safe_path = resource_path(relative)
            structure_id = f"creativelands_cc0:{safe_path}"
            if structure_id in seen_ids:
                raise ValueError(f"Resource ID collision: {structure_id}")
            seen_ids.add(structure_id)
            output = OUTPUT_ROOT / f"{safe_path}.nbt"
            write_nbt(output, document)
            output_raw = output.read_bytes()
            output_relative = str(output.relative_to(ROOT)).replace("\\", "/")
            record = {
                "structure_id": structure_id,
                "source_kind": "extracted",
                "source_project": "Creative Lands",
                "source_author": "Crysillion",
                "source_url": "https://github.com/Crysillion/creativelands",
                "source_license": "CC0-1.0",
                "license_classification": "approved_for_redistribution",
                "required_attribution": "none (source retained voluntarily)",
                "commercial_use_allowed": True,
                "modification_allowed": True,
                "redistribution_allowed": True,
                "original_minecraft_version": "1.16",
                "original_format": "Terra .tesf script",
                "original_filename": relative,
                "source_archive": str(ARCHIVE.relative_to(ROOT)).replace("\\", "/"),
                "source_member": member,
                "sha256": hashlib.sha256(source_raw).hexdigest(),
                "converted_filename": output_relative,
                "converted_sha256": hashlib.sha256(output_raw).hexdigest(),
                "file_size_bytes": len(output_raw),
                "conversion_history": [
                    f"extracted from pinned Creative Lands commit {COMMIT}",
                    "deterministic Terra block calls converted to Minecraft 1.21.1 compressed structure NBT",
                ],
                "our_modifications": [
                    "shifted source coordinate bounds to a zero-based NBT origin",
                    "preserved source block IDs and block-state properties",
                    "excluded Terra runtime-condition and dynamic-coordinate files",
                    "did not carry Terra placement preconditions into the review NBT",
                ],
                "integration_status": "review_only_converted_pending_render_and_1_21_1_validation",
                "dimensions": size,
                "source_block_statements": statements,
                "unique_output_positions": len(placements),
                "overwritten_source_positions": statements - len(placements),
                "production_approved": False,
            }
            records.append(record)
            results[structure_id] = {
                "source_member": member,
                "output": output_relative,
                "dimensions": size,
                "palette_entries": len(palette),
                "blocks": len(blocks),
                "sha256": record["converted_sha256"],
                "status": record["integration_status"],
            }

    provenance_document = {
        "format_version": 1,
        "source_archive_sha256": inventory["source"]["archive_sha256"],
        "license": "CC0-1.0",
        "records": records,
    }
    PROVENANCE.write_text(json.dumps(provenance_document, indent=2) + "\n", encoding="utf-8")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(
        json.dumps(
            {
                "format_version": 1,
                "purpose": "Review-only deterministic Terra-to-NBT extraction; not production integration.",
                "converted_count": len(results),
                "results": results,
                "production_approved": False,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Converted {len(results)} deterministic non-tree CC0 structures to review-only NBT; 0 production approvals")


if __name__ == "__main__":
    main()
