from __future__ import annotations

import json
import math
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[2]
PROVENANCE = ROOT / "dev/structure_library" / "licensing" / "creativelands-extracted-provenance.json"
REVIEW_ROOT = ROOT / "dev/structure_library" / "reviews" / "creativelands_cc0"
RENDER_MANIFEST = REVIEW_ROOT / "render-manifest.json"
VALIDATION = ROOT / "dev/structure_library" / "extracted" / "creativelands_cc0" / "validation-report.json"
JSON_CATALOG = REVIEW_ROOT / "catalog.json"
MARKDOWN_CATALOG = REVIEW_ROOT / "CATALOG.md"
CONTACT_SHEET = REVIEW_ROOT / "contact_sheet.png"


def category_for(filename: str) -> str:
    parts = Path(filename).parts
    if parts[0] != "structures" or len(parts) < 3:
        return parts[0]
    return f"structures/{parts[1]}"


def main() -> None:
    records = json.loads(PROVENANCE.read_text(encoding="utf-8"))["records"]
    renders = {
        entry["structure_id"]: entry
        for entry in json.loads(RENDER_MANIFEST.read_text(encoding="utf-8"))["structures"]
    }
    validation = json.loads(VALIDATION.read_text(encoding="utf-8"))["structures"]
    entries = []
    for record in records:
        structure_id = record["structure_id"]
        render = renders[structure_id]
        entries.append(
            {
                "structure_id": structure_id,
                "display_name": Path(record["original_filename"]).stem.replace("_", " ").title(),
                "category": category_for(record["original_filename"]),
                "dimensions": record["dimensions"],
                "blocks": validation[structure_id]["blocks"],
                "palette_entries": validation[structure_id]["palette_entries"],
                "source_project": record["source_project"],
                "source_author": record["source_author"],
                "source_license": record["source_license"],
                "source_member": record["source_member"],
                "converted_filename": record["converted_filename"],
                "validation_status": "static_nbt_passed",
                "refinement_status": "unreviewed_source_geometry",
                "renders": render["renders"],
                "visual_approval": False,
                "production_approved": False,
            }
        )
    entries.sort(key=lambda entry: (entry["category"], entry["structure_id"]))
    JSON_CATALOG.write_text(
        json.dumps(
            {
                "format_version": 1,
                "purpose": "Browsable review catalog; inclusion is not visual or production approval.",
                "entries": entries,
                "production_approved": 0,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    lines = [
        "# Creative Lands CC0 Review Catalog",
        "",
        "These are mechanically converted source geometries awaiting architectural review. None are production-approved.",
        "",
        "| Preview | ID | Category | Size | Blocks | Status |",
        "|---|---|---|---:|---:|---|",
    ]
    for entry in entries:
        preview = (ROOT / entry["renders"]["exterior_a"]).relative_to(REVIEW_ROOT).as_posix()
        lines.append(
            f"| ![{entry['display_name']}]({preview}) | `{entry['structure_id']}` | `{entry['category']}` | "
            f"{'×'.join(str(value) for value in entry['dimensions'])} | {entry['blocks']} | review only |"
        )
    MARKDOWN_CATALOG.write_text("\n".join(lines) + "\n", encoding="utf-8")

    columns = 5
    tile_width, tile_height = 250, 205
    rows = math.ceil(len(entries) / columns)
    sheet = Image.new("RGB", (columns * tile_width, rows * tile_height), (20, 22, 24))
    draw = ImageDraw.Draw(sheet)
    for index, entry in enumerate(entries):
        x = (index % columns) * tile_width
        y = (index // columns) * tile_height
        preview_path = ROOT / entry["renders"]["exterior_a"]
        with Image.open(preview_path) as source:
            preview = source.convert("RGB")
            preview.thumbnail((tile_width - 12, tile_height - 43))
            px = x + (tile_width - preview.width) // 2
            py = y + 4
            sheet.paste(preview, (px, py))
        label = entry["structure_id"].split(":", 1)[1]
        if len(label) > 37:
            label = "…" + label[-36:]
        draw.text((x + 7, y + tile_height - 34), label, fill=(238, 238, 238))
        draw.text((x + 7, y + tile_height - 18), entry["category"], fill=(170, 181, 188))
        draw.rectangle((x, y, x + tile_width - 1, y + tile_height - 1), outline=(65, 70, 74))
    sheet.save(CONTACT_SHEET)
    print(f"Built Creative Lands review catalog and contact sheet for {len(entries)} candidates; 0 production approvals")


if __name__ == "__main__":
    main()
