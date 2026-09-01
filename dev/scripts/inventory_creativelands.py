from __future__ import annotations

import hashlib
import json
import re
import zipfile
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR = ROOT / "dev/structure_library" / "sources" / "quarantine" / "creativelands_cc0"
COMMIT = "e47d755a90437a881afb3fd410e63cff8eba894c"
ARCHIVE = SOURCE_DIR / f"creativelands-{COMMIT}.zip"
JSON_REPORT = SOURCE_DIR / "inventory.json"
MARKDOWN_REPORT = SOURCE_DIR / "INVENTORY.md"
ROOT_PREFIX = f"creativelands-{COMMIT}/"
BLOCK = re.compile(
    r'block\(\s*([^,]+)\s*,\s*([^,]+)\s*,\s*([^,]+)\s*,\s*"([^"]+)"\s*(?:,\s*(?:true|false))?\s*\)\s*;'
)
CHECK = re.compile(r'^\s*if\s*\(\s*check\(\s*(-?\d+)\s*,\s*y(?:\s*([+-])\s*(\d+))?\s*,\s*(-?\d+)')
NAMESPACE = re.compile(r"^([a-z0-9_.-]+):")


def coordinate(expression: str, axis_variable: str | None = None) -> int | None:
    expression = expression.strip()
    if re.fullmatch(r"-?\d+", expression):
        return int(expression)
    if axis_variable and expression == axis_variable:
        return 0
    if axis_variable:
        match = re.fullmatch(rf"{axis_variable}\s*([+-])\s*(-?\d+)", expression)
        if match:
            sign, amount = match.groups()
            return int(amount) * (-1 if sign == "-" else 1)
    return None


def main() -> None:
    archive_bytes = ARCHIVE.read_bytes()
    with zipfile.ZipFile(ARCHIVE) as archive:
        members = archive.namelist()
        license_member = ROOT_PREFIX + "LICENSE"
        license_bytes = archive.read(license_member)
        structure_members = sorted(
            member
            for member in members
            if member.startswith(ROOT_PREFIX + "structures/data/") and member.endswith(".tesf")
        )
        structures = {}
        categories = Counter()
        direct_categories = Counter()
        namespaces = Counter()
        all_blocks = Counter()
        parse_failures = []
        for member in structure_members:
            relative = member.removeprefix(ROOT_PREFIX + "structures/data/")
            category = relative.split("/", 1)[0]
            categories[category] += 1
            raw = archive.read(member)
            text = raw.decode("utf-8", errors="replace")
            positions = []
            blocks = Counter()
            check_count = 0
            block_like_lines = 0
            dynamic_coordinate_blocks = 0
            conditional_block_statements = 0
            for line_number, line in enumerate(text.splitlines(), start=1):
                if "block(" in line:
                    block_like_lines += 1
                match = BLOCK.search(line)
                if match:
                    x_expression, y_expression, z_expression, state = match.groups()
                    position = [
                        coordinate(x_expression),
                        coordinate(y_expression, "y"),
                        coordinate(z_expression),
                    ]
                    if all(value is not None for value in position):
                        positions.append(position)
                    else:
                        dynamic_coordinate_blocks += 1
                    if line[: match.start()].strip():
                        conditional_block_statements += 1
                    block_id = state.split("[", 1)[0]
                    blocks[block_id] += 1
                    all_blocks[block_id] += 1
                    namespace = NAMESPACE.match(block_id)
                    namespaces[namespace.group(1) if namespace else "unqualified"] += 1
                elif "block(" in line and not line.lstrip().startswith("//"):
                    parse_failures.append({"file": relative, "line": line_number, "text": line.strip()})
                if CHECK.match(line):
                    check_count += 1
            bounds = None
            size = None
            if positions:
                low = [min(position[axis] for position in positions) for axis in range(3)]
                high = [max(position[axis] for position in positions) for axis in range(3)]
                bounds = {"min": low, "max": high}
                size = [high[axis] - low[axis] + 1 for axis in range(3)]
            direct_extractable = (
                sum(blocks.values()) > 0
                and dynamic_coordinate_blocks == 0
                and conditional_block_statements == 0
            )
            if direct_extractable:
                direct_categories[category] += 1
            structures[relative] = {
                "sha256": hashlib.sha256(raw).hexdigest(),
                "bytes": len(raw),
                "category": category,
                "block_statements": sum(blocks.values()),
                "block_like_lines": block_like_lines,
                "dynamic_coordinate_block_statements": dynamic_coordinate_blocks,
                "conditional_block_statements": conditional_block_statements,
                "check_statements": check_count,
                "bounds": bounds,
                "size": size,
                "unique_block_ids": len(blocks),
                "block_counts": dict(sorted(blocks.items())),
                "conversion_status": (
                    "direct_geometry_extract_candidate"
                    if direct_extractable
                    else "requires_terra_script_interpreter_or_manual_rebuild"
                ),
                "production_approved": False,
            }

    report = {
        "format_version": 1,
        "source": {
            "project": "Creative Lands",
            "author": "Crysillion",
            "url": "https://github.com/Crysillion/creativelands",
            "commit": COMMIT,
            "license": "CC0-1.0",
            "license_member": license_member,
            "license_sha256": hashlib.sha256(license_bytes).hexdigest(),
            "archive": str(ARCHIVE.relative_to(ROOT)).replace("\\", "/"),
            "archive_bytes": len(archive_bytes),
            "archive_sha256": hashlib.sha256(archive_bytes).hexdigest(),
        },
        "format": "Terra .tesf script",
        "structure_count": len(structures),
        "non_tree_structure_count": len(structures) - categories.get("trees", 0),
        "categories": dict(sorted(categories.items())),
        "direct_extractable_categories": dict(sorted(direct_categories.items())),
        "direct_extractable_count": sum(direct_categories.values()),
        "direct_extractable_non_tree_count": sum(
            count for category, count in direct_categories.items() if category != "trees"
        ),
        "block_statement_count": sum(all_blocks.values()),
        "unique_block_ids": len(all_blocks),
        "block_namespaces": dict(sorted(namespaces.items())),
        "block_counts": dict(sorted(all_blocks.items())),
        "unparsed_block_like_lines": parse_failures,
        "structures": structures,
        "license_gate": "passed_cc0_archive_contains_license",
        "conversion_gate": "pending",
        "visual_gate": "pending",
        "production_approved": False,
    }
    JSON_REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Creative Lands CC0 Inventory",
        "",
        f"- Source commit: `{COMMIT}`",
        f"- Archive SHA-256: `{report['source']['archive_sha256']}`",
        f"- Bundled LICENSE SHA-256: `{report['source']['license_sha256']}`",
        "- License gate: **passed — CC0-1.0 file is bundled in the pinned archive**",
        f"- Terra `.tesf` files: **{len(structures)}**",
        f"- Non-tree files: **{report['non_tree_structure_count']}**",
        f"- Direct-extraction candidates: **{report['direct_extractable_count']}** total / **{report['direct_extractable_non_tree_count']}** non-tree",
        f"- Parsed block statements: **{report['block_statement_count']}**",
        f"- Unique block IDs: **{report['unique_block_ids']}**",
        f"- Unparsed block-like lines: **{len(parse_failures)}**",
        "- Conversion gate: **pending**",
        "- Visual/production approval: **0**",
        "",
        "| Category | Files | Direct-extraction candidates |",
        "|---|---:|---:|",
    ]
    for category, count in sorted(categories.items()):
        lines.append(f"| `{category}` | {count} | {direct_categories.get(category, 0)} |")
    lines.extend(
        [
            "",
            "All parsed block IDs are retained in `inventory.json` with per-file hashes, bounds, sizes and palettes. License approval does not imply Minecraft 1.21.1 compatibility or acceptable build quality.",
        ]
    )
    MARKDOWN_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        f"Inventoried {len(structures)} CC0 Terra structures ({report['non_tree_structure_count']} non-tree); "
        f"{len(parse_failures)} unparsed block-like lines; 0 production approvals"
    )


if __name__ == "__main__":
    main()
