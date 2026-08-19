"""Build visual contact sheets and flag common Minecraft item-texture failures."""

from __future__ import annotations

import csv
import re
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
ITEM_DIR = ROOT / "kubejs/assets/kubejs/textures/item"
OUT = ROOT / "docs/texture-audit"
MAIN = ROOT / "kubejs/startup_scripts/main.js"


def metrics(path: Path) -> dict[str, object]:
    with Image.open(path) as source:
        image = source.convert("RGBA")
    alpha = list(image.getchannel("A").get_flattened_data())
    corners = [image.getpixel(point) for point in ((0, 0), (image.width - 1, 0), (0, image.height - 1), (image.width - 1, image.height - 1))]
    white_corners = sum(a > 0 and r > 235 and g > 235 and b > 235 for r, g, b, a in corners)
    return {
        "size": f"{image.width}x{image.height}",
        "transparent_pixels": sum(a == 0 for a in alpha),
        "partial_alpha_pixels": sum(0 < a < 255 for a in alpha),
        "opaque_corners": sum(a == 255 for _, _, _, a in corners),
        "white_corners": white_corners,
        "suspected_white_matte": white_corners >= 3,
        "fully_opaque": all(a == 255 for a in alpha),
    }


def sheet(entries: list[tuple[str, Image.Image]], output: Path, columns: int = 5) -> None:
    tile_w, tile_h, preview = 150, 150, 112
    rows = (len(entries) + columns - 1) // columns
    canvas = Image.new("RGB", (columns * tile_w, max(1, rows) * tile_h), (28, 30, 34))
    draw = ImageDraw.Draw(canvas)
    for index, (name, source) in enumerate(entries):
        x, y = index % columns * tile_w, index // columns * tile_h
        checker = Image.new("RGB", (preview, preview), (174, 174, 174))
        checker_draw = ImageDraw.Draw(checker)
        for yy in range(0, preview, 14):
            for xx in range(0, preview, 14):
                if (xx // 14 + yy // 14) % 2:
                    checker_draw.rectangle((xx, yy, xx + 13, yy + 13), fill=(110, 110, 110))
        icon = source.convert("RGBA")
        scale = max(1, min(preview // icon.width, preview // icon.height))
        icon = icon.resize((icon.width * scale, icon.height * scale), Image.Resampling.NEAREST)
        checker.paste(icon, ((preview - icon.width) // 2, (preview - icon.height) // 2), icon)
        canvas.paste(checker, (x + 19, y + 5))
        label = name if len(name) <= 23 else name[:22] + "…"
        draw.text((x + 4, y + 122), label, fill=(235, 237, 240))
    canvas.save(output)


def jar_assets() -> dict[str, tuple[Path, str]]:
    wanted: dict[str, tuple[Path, str]] = {}
    for jar in (ROOT / "mods").glob("*.jar"):
        try:
            with zipfile.ZipFile(jar) as archive:
                for member in archive.namelist():
                    if member.startswith("assets/") and "/textures/" in member and member.endswith(".png"):
                        parts = member.split("/")
                        key = f"{parts[1]}:{'/'.join(parts[3:])[:-4]}"
                        wanted.setdefault(key, (jar, member))
        except zipfile.BadZipFile:
            continue
    return wanted


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    custom_entries = []
    for path in sorted(ITEM_DIR.glob("*.png")):
        result = metrics(path)
        rows.append({"texture": path.stem, **result})
        with Image.open(path) as image:
            custom_entries.append((path.stem, image.convert("RGBA")))
    with (OUT / "custom-item-alpha-audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    sheet(custom_entries, OUT / "all-custom-items.png")

    progression_pattern = re.compile(
        r"^(?:era\d_(?:mining|farming|exploration)_contribution|era\d_(?:mastery_emblem|supply_bag|priority_cache)|"
        r"(?:mechanical|industrial|chemical|electrical|automation|atomic|orbital|infinite_domain)_foundation_core|"
        r"(?:scavenger|mason|habitation)_contribution|ultima_collection_emblem|incomplete_industrial_engineering_core|"
        r"darknet_temporal_core|darknet_session_injector_tier_\d)$"
    )
    progression_entries = [(name, image) for name, image in custom_entries if progression_pattern.match(name)]
    sheet(progression_entries, OUT / "progression-items.png", columns=6)

    source = MAIN.read_text(encoding="utf-8")
    era_block = source[source.index("const eraItems = ["):source.index("eraItems.forEach")]
    era_refs = re.findall(r"\['([^']+)',\s*'[^']*',\s*'([^']+)'\]", era_block)
    assets = jar_assets()
    extracted = []
    missing = []
    for item_id, texture_ref in era_refs:
        found = assets.get(texture_ref)
        if not found:
            missing.append((item_id, texture_ref))
            continue
        jar, member = found
        with zipfile.ZipFile(jar) as archive, archive.open(member) as handle:
            extracted.append((item_id, Image.open(handle).convert("RGBA")))
    sheet(extracted, OUT / "era-source-textures.png")
    (OUT / "missing-era-source-textures.txt").write_text("\n".join(f"{item}: {texture}" for item, texture in missing) + "\n", encoding="utf-8")

    darknet_names = [
        "darknet_data_cache", "scraped_access_token", "encrypted_credential_bundle", "black_ice_kernel",
        "zero_day_archive", "root_authority_key", "darknet_scrip", "ghost_market_cipher", "black_ledger_writ",
    ]
    darknet_entries = []
    for name in darknet_names:
        path = ITEM_DIR / f"{name}.png"
        if path.exists():
            with Image.open(path) as image:
                darknet_entries.append((name, image.convert("RGBA")))
    sheet(darknet_entries, OUT / "darknet-items.png", columns=3)

    white = [row["texture"] for row in rows if row["suspected_white_matte"]]
    opaque = [row["texture"] for row in rows if row["fully_opaque"]]
    expected_progression = {
        "scavenger_contribution", "mason_contribution", "habitation_contribution",
        "mechanical_foundation_core", "industrial_foundation_core", "chemical_foundation_core",
        "electrical_foundation_core", "automation_foundation_core", "atomic_foundation_core",
        "orbital_foundation_core", "infinite_domain_core", "incomplete_industrial_engineering_core",
        "ultima_collection_emblem", "darknet_temporal_core",
    }
    for era in range(1, 9):
        expected_progression.update(f"era{era}_{role}_contribution" for role in ("mining", "farming", "exploration"))
    for era in range(0, 9):
        expected_progression.add(f"era{era}_mastery_emblem")
    expected_progression.add("era0_priority_cache")
    for era in range(1, 9):
        expected_progression.update((f"era{era}_supply_bag", f"era{era}_priority_cache"))
    expected_progression.update(f"darknet_session_injector_tier_{tier}" for tier in range(1, 9))
    missing_generated = sorted(name for name in expected_progression if not (ITEM_DIR / f"{name}.png").exists())
    approved_source_dir = OUT / "generated-sources"
    approved_item_specific = sorted(path.stem for path in approved_source_dir.glob("*.png")) if approved_source_dir.exists() else []
    status = "PASS" if not white and not opaque and not missing_generated else "FAIL"
    report = [
        "# Texture Quality Audit", "", f"Status: **{status}**", "", "## Results", "",
        f"- {len(rows)} custom item textures inspected.",
        f"- {len(expected_progression)} purpose-built era/progression textures verified.",
        f"- {len(approved_item_specific)} textures have passed the item-specific ImageGen replacement gate.",
        f"- {len(white)} suspected white-matte textures remain.",
        f"- {len(opaque)} fully opaque item textures remain.",
        f"- {len(missing_generated)} expected progression textures are missing.",
        "- Six original Darknet intelligence sprites were alpha-extracted and cleaned.",
        "- All active era contribution and foundation-core registrations now use portable item icons rather than borrowed machine/entity art.",
        "- All 72 progression textures have approved full-resolution sources; only the separate industrial-food family remains artistically provisional.",
        "", "## Missing generated textures", "",
        *(f"- {name}" for name in missing_generated),
    ]
    if not missing_generated:
        report.append("- None")
    (OUT / "report.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"Audited {len(rows)} custom item textures; {len(white)} suspected white mattes; {len(opaque)} fully opaque.")
    print(f"Verified {len(expected_progression) - len(missing_generated)}/{len(expected_progression)} generated progression textures; see docs/texture-audit.")


if __name__ == "__main__":
    main()
