#!/usr/bin/env python3
"""Apply a conservative LAST DAYS baseline palette to untouched imported compatibility textures.

This is intentionally a broad, low-detail alignment pass. It is NOT authored texture
conversion and must not be counted as completed art.

Safety gates:
- Reads docs/last-days-mod-reference-assets.csv as the import authority.
- Only rows with Kind=png and Status=imported are eligible.
- Current file SHA-256 must still match the originally imported SourceSha256.
- Previously palette-aligned outputs are recognized from the generated report.
- Data maps (normal/specular/roughness/etc.) and protected first-party namespaces are skipped.
- Dimensions and alpha values are preserved exactly.
- .png.mcmeta files are never touched.

Color behavior:
- Most pixels are quantized by luminance into a dark gray/olive industrial palette.
- Strong or sparse vivid pixels are treated as functional/hazard/emissive signals:
  hue is preserved, while brightness/saturation are clamped and mixed toward the
  structural palette so they remain readable without looking neon-clean.
"""

from __future__ import annotations

import argparse
import colorsys
import csv
import hashlib
import io
import math
import sys
from collections import Counter
from pathlib import Path

try:
    from PIL import Image
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Pillow is required: python -m pip install Pillow") from exc


REPO_ROOT = Path(__file__).resolve().parents[1]
PACK_ROOT = REPO_ROOT / "resourcepacks" / "LAST_DAYS_INFINITE_DOMAIN_1_21_1"
IMPORT_LEDGER = REPO_ROOT / "docs" / "last-days-mod-reference-assets.csv"
REPORT_CSV = REPO_ROOT / "docs" / "last-days-baseline-palette-pass.csv"
REPORT_MD = REPO_ROOT / "docs" / "last-days-baseline-palette-pass.md"

# Flat, deliberately restrained LAST DAYS baseline. Source luminance selects the step.
STRUCTURAL_PALETTE: tuple[tuple[int, int, int], ...] = (
    (12, 14, 13),
    (17, 20, 18),
    (23, 27, 24),
    (30, 35, 31),
    (37, 43, 37),
    (45, 52, 44),
    (54, 62, 52),
    (64, 72, 60),
    (75, 83, 69),
    (87, 95, 79),
    (101, 108, 91),
    (116, 122, 103),
)

# First-party/authority namespaces should never receive the generic imported-mod pass.
PROTECTED_NAMESPACES = {
    "minecraft",
    "cyberworld",
    "darknet",
    "infinite_domain",
    "kubejs",
}

# These images usually encode data rather than visible albedo color. Palette-swapping them
# can break shaders/material interpretation.
DATA_MAP_TOKENS = (
    "_normal",
    "_norm",
    "_specular",
    "_spec",
    "_roughness",
    "_rough",
    "_metallic",
    "_metalness",
    "_height",
    "_displacement",
    "_parallax",
    "_ambient_occlusion",
    "_occlusion",
    "_rma",
    "_mer",
    "_pbr",
)
DATA_MAP_SUFFIXES = ("_n.png", "_s.png")
DATA_MAP_SEGMENTS = (
    "/normal/",
    "/normals/",
    "/specular/",
    "/roughness/",
    "/metallic/",
    "/heightmap/",
    "/heightmaps/",
    "/masks/",
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def looks_like_data_map(asset_path: str) -> bool:
    p = asset_path.replace("\\", "/").lower()
    name = Path(p).name
    if name.endswith(DATA_MAP_SUFFIXES):
        return True
    stem = name[:-4] if name.endswith(".png") else name
    if any(token in stem for token in DATA_MAP_TOKENS):
        return True
    return any(segment in p for segment in DATA_MAP_SEGMENTS)


def structural_color_from_luma(luma: float) -> tuple[int, int, int]:
    # Gamma < 1 preserves enough middle-value separation to keep source structure readable
    # while still keeping the whole pack notably darker than most source mod art.
    t = max(0.0, min(1.0, luma / 255.0))
    t = math.pow(t, 0.78)
    idx = int(round(t * (len(STRUCTURAL_PALETTE) - 1)))
    return STRUCTURAL_PALETTE[max(0, min(len(STRUCTURAL_PALETTE) - 1, idx))]


def rgb_to_hsv255(r: int, g: int, b: int) -> tuple[float, float, float]:
    return colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)


def tone_signal(
    r: int,
    g: int,
    b: int,
    structural: tuple[int, int, int],
) -> tuple[int, int, int]:
    """Keep functional hue but dirty/darken it toward the structural baseline."""
    h, s, v = rgb_to_hsv255(r, g, b)
    # Cap neon saturation/brightness; do not erase the identity of red/yellow/blue/etc.
    s2 = min(0.62, max(0.26, s * 0.74))
    v2 = min(0.72, max(0.18, 0.05 + v * 0.68))
    rr, gg, bb = colorsys.hsv_to_rgb(h, s2, v2)
    signal = (int(round(rr * 255)), int(round(gg * 255)), int(round(bb * 255)))
    # A small structural mix makes retained signals feel painted/aged rather than clean neon.
    mix = 0.18
    return tuple(
        max(0, min(255, int(round(signal[i] * (1.0 - mix) + structural[i] * mix))))
        for i in range(3)
    )


def visible_vivid_ratio(rgba: Image.Image) -> tuple[float, int]:
    visible = 0
    vivid = 0
    for r, g, b, a in rgba.getdata():
        if a <= 8:
            continue
        visible += 1
        _, s, v = rgb_to_hsv255(r, g, b)
        if s >= 0.50 and v >= 0.36:
            vivid += 1
    return ((vivid / visible) if visible else 0.0, visible)


def transform_image(image: Image.Image) -> tuple[Image.Image, dict[str, int | float]]:
    rgba = image.convert("RGBA")
    vivid_ratio, visible_pixels = visible_vivid_ratio(rgba)

    output: list[tuple[int, int, int, int]] = []
    changed = 0
    signal_pixels = 0
    structural_pixels = 0

    for r, g, b, a in rgba.getdata():
        # Rec.709 luma keeps original shading/edge structure even though chroma is flattened.
        luma = 0.2126 * r + 0.7152 * g + 0.0722 * b
        structural = structural_color_from_luma(luma)
        _, s, v = rgb_to_hsv255(r, g, b)

        # Preserve strong signals everywhere, and moderately vivid color when it occupies only
        # a minority of the texture (typical ports, LEDs, hazard stripes, fluid gauges, etc.).
        is_signal = (
            a > 8
            and (
                (s >= 0.70 and v >= 0.42)
                or (vivid_ratio <= 0.22 and s >= 0.52 and v >= 0.36)
            )
        )

        if is_signal:
            nr, ng, nb = tone_signal(r, g, b, structural)
            signal_pixels += 1
        else:
            nr, ng, nb = structural
            structural_pixels += 1

        new_pixel = (nr, ng, nb, a)
        output.append(new_pixel)
        if new_pixel != (r, g, b, a):
            changed += 1

    out = Image.new("RGBA", rgba.size)
    out.putdata(output)
    return out, {
        "visible_pixels": visible_pixels,
        "vivid_ratio": vivid_ratio,
        "signal_pixels": signal_pixels,
        "structural_pixels": structural_pixels,
        "changed_pixels": changed,
    }


def encode_png(image: Image.Image, original: Image.Image) -> bytes:
    # Keep alpha topology exactly; metadata that can safely survive a color conversion is retained.
    buffer = io.BytesIO()
    save_kwargs: dict[str, object] = {"format": "PNG", "compress_level": 9}
    if original.info.get("icc_profile"):
        save_kwargs["icc_profile"] = original.info["icc_profile"]
    if original.info.get("dpi"):
        save_kwargs["dpi"] = original.info["dpi"]
    image.save(buffer, **save_kwargs)
    return buffer.getvalue()


def load_previous_outputs() -> dict[str, str]:
    if not REPORT_CSV.exists():
        return {}
    result: dict[str, str] = {}
    try:
        with REPORT_CSV.open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                path = (row.get("AssetPath") or "").strip()
                out_hash = (row.get("OutputSha256") or "").strip().upper()
                status = (row.get("Result") or "").strip()
                if path and out_hash and status in {"palette_aligned", "already_baseline_aligned"}:
                    result[path] = out_hash
    except Exception:
        # A damaged old report must never expand scope. Hash-to-source safety still protects files.
        return {}
    return result


def write_reports(rows: list[dict[str, object]], apply: bool) -> None:
    REPORT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "AssetPath",
        "Namespace",
        "InputStatus",
        "Result",
        "Width",
        "Height",
        "OriginalMode",
        "VisiblePixels",
        "VividCandidateRatio",
        "SignalPixels",
        "StructuralPixels",
        "ChangedPixels",
        "InputSha256",
        "OutputSha256",
        "Note",
    ]
    with REPORT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    counts = Counter(str(row["Result"]) for row in rows)
    changed_by_namespace = Counter(
        str(row["Namespace"])
        for row in rows
        if row["Result"] in {"palette_aligned", "would_palette_align"}
    )
    eligible_changed = counts["palette_aligned"] + counts["would_palette_align"]

    lines = [
        "# LAST DAYS baseline compatibility palette pass",
        "",
        f"Mode: **{'APPLIED' if apply else 'DRY RUN'}**",
        "",
        "This is a deliberately broad **baseline alignment layer**, not authored texture conversion.",
        "It exists so untouched compatibility placeholders visually belong to the LAST DAYS pack while",
        "higher-detail texture families continue to be rebuilt one family at a time.",
        "",
        "## Safety contract",
        "",
        "- Only `Kind=png`, `Status=imported` rows from `docs/last-days-mod-reference-assets.csv` are eligible.",
        "- A file is changed only when its current SHA-256 still equals the originally imported mod texture SHA-256.",
        "- Previously authored or subsequently edited textures are protected automatically by that hash gate.",
        "- Native width, height, and every alpha value are preserved.",
        "- Animation `.png.mcmeta` files are untouched.",
        "- Normal/specular/roughness/metallic/height/PBR data maps are skipped.",
        "- First-party authority namespaces (`minecraft`, `cyberworld`, `darknet`, `infinite_domain`, `kubejs`) are skipped.",
        "- Strong or sparse vivid functional colors retain their hue but are darkened/desaturated into the pack's range.",
        "- All other color is flattened by luminance into a dark gray / olive / worn-metal palette.",
        "- `palette_aligned` means temporary baseline styling only. It must never be counted as `Authored` or `Complete`.",
        "",
        "## Result counts",
        "",
    ]
    for key, value in sorted(counts.items()):
        lines.append(f"- `{key}`: {value}")
    lines.extend(["", f"Textures newly aligned in this run: **{eligible_changed}**", ""])

    if changed_by_namespace:
        lines.extend(["## Newly aligned namespaces", ""])
        for namespace, count in changed_by_namespace.most_common():
            lines.append(f"- `{namespace}`: {count}")
        lines.append("")

    lines.extend(
        [
            "## Palette",
            "",
            "Structural steps:",
            "",
            "```text",
            " ".join("#%02X%02X%02X" % rgb for rgb in STRUCTURAL_PALETTE),
            "```",
            "",
            "Detailed authored conversions supersede this baseline whenever they are installed.",
            "",
        ]
    )
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write transformed PNGs. Without this flag the run is a dry-run report.",
    )
    parser.add_argument(
        "--namespace",
        action="append",
        default=[],
        help="Optional namespace filter; may be supplied more than once.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Optional maximum eligible textures to transform (0 = no limit).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    namespaces = {n.strip() for n in args.namespace if n.strip()}
    previous_outputs = load_previous_outputs()

    if not PACK_ROOT.is_dir():
        raise SystemExit(f"Missing editable pack: {PACK_ROOT}")
    if not IMPORT_LEDGER.is_file():
        raise SystemExit(f"Missing import ledger: {IMPORT_LEDGER}")

    rows: list[dict[str, object]] = []
    transformed = 0

    with IMPORT_LEDGER.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"AssetPath", "Namespace", "Kind", "Status", "SourceSha256"}
        missing = required.difference(reader.fieldnames or [])
        if missing:
            raise SystemExit(f"Import ledger missing columns: {sorted(missing)}")

        for source_row in reader:
            asset_path = (source_row.get("AssetPath") or "").replace("\\", "/").strip()
            namespace = (source_row.get("Namespace") or "").strip()
            kind = (source_row.get("Kind") or "").strip()
            status = (source_row.get("Status") or "").strip()
            source_sha = (source_row.get("SourceSha256") or "").strip().upper()

            if kind != "png" or status != "imported":
                continue
            if namespaces and namespace not in namespaces:
                continue

            result: dict[str, object] = {
                "AssetPath": asset_path,
                "Namespace": namespace,
                "InputStatus": status,
                "Result": "",
                "Width": "",
                "Height": "",
                "OriginalMode": "",
                "VisiblePixels": "",
                "VividCandidateRatio": "",
                "SignalPixels": "",
                "StructuralPixels": "",
                "ChangedPixels": "",
                "InputSha256": "",
                "OutputSha256": "",
                "Note": "",
            }

            if namespace in PROTECTED_NAMESPACES:
                result["Result"] = "skipped_protected_namespace"
                rows.append(result)
                continue
            if looks_like_data_map(asset_path):
                result["Result"] = "skipped_data_map"
                rows.append(result)
                continue

            path = PACK_ROOT / asset_path
            if not path.is_file():
                result["Result"] = "missing"
                result["Note"] = "Ledger path not present in editable pack"
                rows.append(result)
                continue

            current_sha = sha256_file(path)
            result["InputSha256"] = current_sha

            if previous_outputs.get(asset_path) == current_sha:
                result["Result"] = "already_baseline_aligned"
                result["OutputSha256"] = current_sha
                rows.append(result)
                continue

            if not source_sha or current_sha != source_sha:
                result["Result"] = "protected_non_source_change"
                result["Note"] = "Current bytes differ from original imported source; presumed authored/edited"
                rows.append(result)
                continue

            if args.limit and transformed >= args.limit:
                result["Result"] = "skipped_limit"
                rows.append(result)
                continue

            try:
                with Image.open(path) as original:
                    original.load()
                    result["Width"], result["Height"] = original.size
                    result["OriginalMode"] = original.mode
                    transformed_image, stats = transform_image(original)
                    png_bytes = encode_png(transformed_image, original)
            except Exception as exc:
                result["Result"] = "error"
                result["Note"] = f"{type(exc).__name__}: {exc}"
                rows.append(result)
                continue

            result["VisiblePixels"] = stats["visible_pixels"]
            result["VividCandidateRatio"] = f"{stats['vivid_ratio']:.6f}"
            result["SignalPixels"] = stats["signal_pixels"]
            result["StructuralPixels"] = stats["structural_pixels"]
            result["ChangedPixels"] = stats["changed_pixels"]
            output_sha = sha256_bytes(png_bytes)
            result["OutputSha256"] = output_sha

            if stats["changed_pixels"] == 0:
                result["Result"] = "unchanged"
            elif args.apply:
                path.write_bytes(png_bytes)
                result["Result"] = "palette_aligned"
                transformed += 1
            else:
                result["Result"] = "would_palette_align"
                transformed += 1

            rows.append(result)

    write_reports(rows, args.apply)

    counts = Counter(str(row["Result"]) for row in rows)
    print("LAST DAYS baseline compatibility palette")
    print(f"Mode: {'APPLY' if args.apply else 'DRY RUN'}")
    for key, value in sorted(counts.items()):
        print(f"{key}: {value}")

    if counts["error"]:
        print("One or more PNGs failed to process; refusing a clean exit.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
