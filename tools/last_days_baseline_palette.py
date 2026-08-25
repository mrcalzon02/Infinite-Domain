#!/usr/bin/env python3
"""Apply the broad LAST DAYS baseline palette to untouched imported compatibility textures.

This pass is intentionally fast, flat, and temporary. It is NOT authored texture conversion
and must never be counted as completed art.

Safety gates:
- Authority is docs/last-days-mod-reference-assets.csv.
- Only Kind=png / Status=imported rows are eligible.
- Current SHA-256 must still equal the original SourceSha256.
- Previously palette-aligned outputs are recognized from the generated report.
- Known normal/specular/roughness/metallic/height/PBR data maps are skipped.
- First-party authority namespaces are skipped.
- Width, height, alpha values, paths, and .png.mcmeta animation metadata are preserved.

Color behavior:
- Ordinary RGB is quantized by source luminance into a narrow dark gray / olive-metal palette.
- Strong or sparse vivid pixels keep their source hue relationship but are darkened,
  desaturated, and mixed toward the structural palette for dirty functional accents.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import sys
from collections import Counter
from pathlib import Path

try:
    import numpy as np
    from PIL import Image
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Pillow and NumPy are required: python -m pip install Pillow numpy"
    ) from exc


REPO_ROOT = Path(__file__).resolve().parents[1]
PACK_ROOT = REPO_ROOT / "resourcepacks" / "LAST_DAYS_INFINITE_DOMAIN_1_21_1"
IMPORT_LEDGER = REPO_ROOT / "docs" / "last-days-mod-reference-assets.csv"
REPORT_CSV = REPO_ROOT / "docs" / "last-days-baseline-palette-pass.csv"
REPORT_MD = REPO_ROOT / "docs" / "last-days-baseline-palette-pass.md"

STRUCTURAL_PALETTE = np.asarray(
    (
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
    ),
    dtype=np.uint8,
)

PROTECTED_NAMESPACES = {
    "minecraft",
    "cyberworld",
    "darknet",
    "infinite_domain",
    "kubejs",
}

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


def transform_image(image: Image.Image) -> tuple[Image.Image, dict[str, int | float]]:
    """Vectorized palette conversion; alpha is copied byte-for-byte."""
    rgba = image.convert("RGBA")
    src = np.asarray(rgba, dtype=np.uint8)
    rgb = src[..., :3].astype(np.float32)
    alpha = src[..., 3]

    maxc = rgb.max(axis=2)
    minc = rgb.min(axis=2)
    delta = maxc - minc
    saturation = np.divide(
        delta,
        maxc,
        out=np.zeros_like(delta, dtype=np.float32),
        where=maxc > 0,
    )
    value = maxc / 255.0
    visible = alpha > 8
    vivid = visible & (saturation >= 0.50) & (value >= 0.36)
    visible_count = int(np.count_nonzero(visible))
    vivid_ratio = (
        float(np.count_nonzero(vivid)) / visible_count if visible_count else 0.0
    )

    strong_signal = visible & (saturation >= 0.70) & (value >= 0.42)
    minority_signal = (
        visible
        & (saturation >= 0.52)
        & (value >= 0.36)
        & (vivid_ratio <= 0.22)
    )
    signal_mask = strong_signal | minority_signal

    # Preserve source shading/edge structure through Rec.709 luminance, then quantize it
    # into the intentionally narrow pack-wide structural palette.
    luma = 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]
    tone = np.power(np.clip(luma / 255.0, 0.0, 1.0), 0.78)
    palette_index = np.rint(tone * (len(STRUCTURAL_PALETTE) - 1)).astype(np.int16)
    structural_rgb = STRUCTURAL_PALETTE[palette_index].astype(np.float32)

    out_rgb = structural_rgb.copy()

    if np.any(signal_mask):
        # Preserve hue relationship without expensive per-pixel HSV conversion:
        # move chroma toward its luma, clamp brightness, then dirty it with the structural tone.
        gray = luma[..., None]
        desaturated = gray + (rgb - gray) * 0.62

        original_peak = np.maximum(maxc, 1.0)
        target_peak = np.clip(13.0 + maxc * 0.68, 46.0, 184.0)
        brightness_scale = (target_peak / original_peak)[..., None]
        toned_signal = np.clip(desaturated * brightness_scale, 0.0, 255.0)

        mixed_signal = toned_signal * 0.82 + structural_rgb * 0.18
        out_rgb[signal_mask] = mixed_signal[signal_mask]

    out = np.empty_like(src)
    out[..., :3] = np.rint(np.clip(out_rgb, 0.0, 255.0)).astype(np.uint8)
    out[..., 3] = alpha

    changed_pixels = int(np.count_nonzero(np.any(out != src, axis=2)))
    signal_pixels = int(np.count_nonzero(signal_mask))
    structural_pixels = int(out.shape[0] * out.shape[1] - signal_pixels)

    return Image.fromarray(out, mode="RGBA"), {
        "visible_pixels": visible_count,
        "vivid_ratio": vivid_ratio,
        "signal_pixels": signal_pixels,
        "structural_pixels": structural_pixels,
        "changed_pixels": changed_pixels,
    }


def encode_png(image: Image.Image, original: Image.Image) -> bytes:
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
                if path and out_hash and status in {
                    "palette_aligned",
                    "already_baseline_aligned",
                }:
                    result[path] = out_hash
    except Exception:
        return {}
    return result


def write_reports(rows: list[dict[str, object]], apply: bool) -> None:
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
    changed = counts["palette_aligned"] + counts["would_palette_align"]

    palette_hex = " ".join(
        "#%02X%02X%02X" % tuple(int(x) for x in rgb) for rgb in STRUCTURAL_PALETTE
    )
    lines = [
        "# LAST DAYS baseline compatibility palette pass",
        "",
        f"Mode: **{'APPLIED' if apply else 'DRY RUN'}**",
        "",
        "This is a deliberately broad **baseline alignment layer**, not authored texture conversion.",
        "It makes untouched imported compatibility placeholders visually belong to the LAST DAYS",
        "family while detailed model-aware families continue to be rebuilt one at a time.",
        "",
        "## Safety contract",
        "",
        "- Eligible inputs are only `Kind=png`, `Status=imported` rows from `docs/last-days-mod-reference-assets.csv`.",
        "- The current file must still match its original imported `SourceSha256`.",
        "- Authored, repaired, or otherwise edited textures are protected automatically by the hash gate.",
        "- Width, height, path, and every alpha value are preserved.",
        "- Animation `.png.mcmeta` files are untouched.",
        "- Normal/specular/roughness/metallic/height/PBR data maps are skipped.",
        "- First-party authority namespaces are skipped.",
        "- Strong or sparse functional colors retain their color identity but are darkened/desaturated.",
        "- Ordinary color is quantized to dark gray, olive, and worn-metal structural steps.",
        "- `palette_aligned` is a temporary placeholder status, never `Authored`, `PASS`, or `Complete`.",
        "",
        "## Result counts",
        "",
    ]
    for key, value in sorted(counts.items()):
        lines.append(f"- `{key}`: {value}")
    lines += ["", f"Textures newly aligned in this run: **{changed}**", ""]

    if changed_by_namespace:
        lines += ["## Newly aligned namespaces", ""]
        for namespace, count in changed_by_namespace.most_common():
            lines.append(f"- `{namespace}`: {count}")
        lines.append("")

    lines += [
        "## Structural palette",
        "",
        "```text",
        palette_hex,
        "```",
        "",
        "Detailed authored conversions supersede this baseline whenever they are installed.",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--namespace", action="append", default=[])
    parser.add_argument("--limit", type=int, default=0)
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

            row: dict[str, object] = {
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
                row["Result"] = "skipped_protected_namespace"
                rows.append(row)
                continue
            if looks_like_data_map(asset_path):
                row["Result"] = "skipped_data_map"
                rows.append(row)
                continue

            path = PACK_ROOT / asset_path
            if not path.is_file():
                row["Result"] = "missing"
                row["Note"] = "Ledger path not present in editable pack"
                rows.append(row)
                continue

            current_sha = sha256_file(path)
            row["InputSha256"] = current_sha

            if previous_outputs.get(asset_path) == current_sha:
                row["Result"] = "already_baseline_aligned"
                row["OutputSha256"] = current_sha
                rows.append(row)
                continue

            if not source_sha or current_sha != source_sha:
                row["Result"] = "protected_non_source_change"
                row["Note"] = (
                    "Current bytes differ from original imported source; presumed authored/edited"
                )
                rows.append(row)
                continue

            if args.limit and transformed >= args.limit:
                row["Result"] = "skipped_limit"
                rows.append(row)
                continue

            try:
                with Image.open(path) as original:
                    original.load()
                    row["Width"], row["Height"] = original.size
                    row["OriginalMode"] = original.mode
                    transformed_image, stats = transform_image(original)
                    png_bytes = encode_png(transformed_image, original)
            except Exception as exc:
                row["Result"] = "error"
                row["Note"] = f"{type(exc).__name__}: {exc}"
                rows.append(row)
                continue

            row["VisiblePixels"] = stats["visible_pixels"]
            row["VividCandidateRatio"] = f"{stats['vivid_ratio']:.6f}"
            row["SignalPixels"] = stats["signal_pixels"]
            row["StructuralPixels"] = stats["structural_pixels"]
            row["ChangedPixels"] = stats["changed_pixels"]
            row["OutputSha256"] = sha256_bytes(png_bytes)

            if stats["changed_pixels"] == 0:
                row["Result"] = "unchanged"
            elif args.apply:
                path.write_bytes(png_bytes)
                row["Result"] = "palette_aligned"
                transformed += 1
            else:
                row["Result"] = "would_palette_align"
                transformed += 1

            rows.append(row)

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
