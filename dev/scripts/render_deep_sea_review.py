from __future__ import annotations

import gzip
import hashlib
import io
import struct
import sys
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw

# Lightweight, self-contained render-evidence generator for the deep-sea
# corpus. It does not attempt to match the full four-view isometric
# treatment scripts/render_structure_review.py gives the land corpus; it
# gives each asset one isometric exterior view and one mid-height floor
# slice, which is enough to satisfy the audit checklist's requirement for
# actual rendered evidence rather than a parse-only pass. A closer parity
# pass with the land renderer is future work, noted in the ledger.

ROOT = Path(__file__).resolve().parents[2]
STRUCTURE_DIR = ROOT / "kubejs" / "data" / "infinite_domain" / "structure" / "deep_sea"
OUTPUT_DIR = ROOT / "dev/structure_library" / "audit_renders" / "deep_sea"

TILE_W = 10
TILE_H = 6
WATER_ALPHA = 140


class Reader:
    def __init__(self, data: bytes):
        self.stream = io.BytesIO(data)

    def unpack(self, fmt: str) -> Any:
        size = struct.calcsize(fmt)
        return struct.unpack(fmt, self.stream.read(size))[0]

    def string(self) -> str:
        return self.stream.read(self.unpack(">H")).decode("utf-8")

    def payload(self, kind: int) -> Any:
        if kind == 3:
            return self.unpack(">i")
        if kind == 8:
            return self.string()
        if kind == 9:
            item_kind = self.unpack(">B")
            length = self.unpack(">i")
            return [self.payload(item_kind) for _ in range(length)]
        if kind == 10:
            result: dict[str, Any] = {}
            while True:
                child_kind = self.unpack(">B")
                if child_kind == 0:
                    return result
                child_name = self.string()
                result[child_name] = self.payload(child_kind)
        raise ValueError(f"Unsupported NBT tag type in renderer: {kind}")

    def root(self) -> dict[str, Any]:
        kind = self.unpack(">B")
        self.string()
        return self.payload(kind)


def load_structure(path: Path) -> tuple[tuple[int, int, int], dict[tuple[int, int, int], str]]:
    raw = path.read_bytes()
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    root = Reader(raw).root()
    size = tuple(int(v) for v in root["size"])
    palette = [p["Name"] for p in root["palette"]]
    blocks = {tuple(b["pos"]): palette[b["state"]] for b in root["blocks"]}
    return size, blocks  # type: ignore[return-value]


# Curated real-approximation colors for every block this corpus is known to
# place. This is audit evidence -- an uncalibrated color is a false
# rendering of what the structure actually looks like in-game, which is
# exactly the kind of defect the size/visual-composition audit stage in
# docs/DEEP_SEA_STRUCTURE_AND_GEOLOGICAL_FEATURE_STANDARDS.md exists to
# catch. Keep this table current: every asset_class's placed palette should
# resolve here, not through the hash fallback below. The same table (by
# name) is checked for completeness in validate_deep_sea_structures.py's
# render-color-fidelity check -- update both together.
KNOWN_BLOCK_COLORS: dict[str, tuple[int, int, int, int]] = {
    "minecraft:air": (0, 0, 0, 0),
    "minecraft:water": (40, 110, 200, WATER_ALPHA),
    "minecraft:spawner": (25, 28, 30, 255),
    "minecraft:chest": (150, 110, 40, 255),
    "minecraft:barrel": (137, 100, 62, 255),
    "minecraft:crafting_table": (120, 86, 56, 255),
    "minecraft:lectern": (130, 95, 60, 255),
    "minecraft:ladder": (150, 120, 80, 255),
    "minecraft:campfire": (196, 92, 30, 255),
    "minecraft:iron_block": (222, 222, 226, 255),
    "minecraft:iron_bars": (150, 150, 155, 255),
    "minecraft:iron_trapdoor": (200, 200, 205, 255),
    "minecraft:gray_concrete": (54, 57, 61, 255),
    "minecraft:mud_bricks": (89, 68, 51, 255),
    "minecraft:stone": (125, 125, 125, 255),
    "minecraft:gravel": (131, 127, 126, 255),
    "minecraft:basalt": (65, 64, 70, 255),
    "minecraft:blackstone": (42, 36, 40, 255),
    "minecraft:polished_basalt": (78, 77, 83, 255),
    "minecraft:smooth_basalt": (58, 58, 62, 255),
    "minecraft:magma_block": (168, 82, 24, 255),
    "minecraft:glass_pane": (205, 224, 227, 200),
    "minecraft:blast_furnace": (108, 108, 113, 255),
    "minecraft:hopper": (68, 68, 73, 255),
    "minecraft:lever": (112, 100, 88, 255),
    "minecraft:chain": (95, 95, 100, 255),
    "minecraft:redstone_lamp": (153, 112, 68, 255),
    "minecraft:lantern": (95, 84, 60, 255),
    "minecraft:soul_lantern": (72, 96, 108, 255),
    "minecraft:sea_lantern": (176, 224, 224, 255),
    "minecraft:glow_lichen": (108, 196, 120, 255),
    "minecraft:blue_bed": (63, 82, 156, 255),
    "minecraft:gray_bed": (120, 120, 125, 255),
    # Wave 3 (akula_project971) materials. Same rule as everything above:
    # a real approximation of the block's in-game appearance, never a
    # placeholder -- the render-color-fidelity gate in
    # validate_deep_sea_structures.py fails on anything that falls through
    # to the hash below, and RENDER_COLOR_CURATED_EXACT there must be kept
    # in sync with these keys.
    "minecraft:deepslate_tiles": (54, 54, 57, 255),
    "minecraft:deepslate_tile_slab": (54, 54, 57, 255),
    "minecraft:polished_deepslate": (72, 72, 76, 255),
    "minecraft:cobbled_deepslate": (77, 77, 82, 255),
    "minecraft:black_concrete": (8, 10, 15, 255),
    "minecraft:polished_blackstone": (49, 44, 51, 255),
    "minecraft:light_gray_concrete": (125, 125, 115, 255),
    "minecraft:smooth_stone": (159, 159, 159, 255),
    "minecraft:copper_block": (192, 107, 79, 255),
    "minecraft:copper_grate": (169, 96, 71, 255),
    "minecraft:oxidized_cut_copper": (82, 162, 132, 255),
    "minecraft:oxidized_cut_copper_slab": (82, 162, 132, 255),
    "minecraft:dispenser": (107, 107, 107, 255),
    "minecraft:red_concrete": (142, 32, 32, 255),
    "minecraft:tuff": (108, 109, 102, 255),
    # A jigsaw block is a placement marker, not a material: it is replaced by
    # its final_state the moment the structure generates and is never visible
    # in world. Rendering it as a solid colour would put a block in the
    # evidence that does not exist in the game, so it is transparent -- and it
    # is listed here, rather than left to the hash fallback, so the
    # render-color-fidelity gate treats it as a deliberate decision.
    "minecraft:jigsaw": (0, 0, 0, 0),
    # Wave 3c: the pack's wasteland/radiation vocabulary. Every value here was
    # MEASURED -- the mean of the opaque pixels of that block's texture in the
    # LAST DAYS resource pack, which is this project's own authored art, not
    # the mod's. Nothing was eyeballed and no third-party texture is copied
    # into this repository; only the derived triple lives here.
    "create_new_age:solid_corium": (103, 225, 229, 255),
    "create_new_age:corium": (123, 235, 238, 255),
    "the_wasteland_reworked:waste_barrel": (212, 179, 34, 255),
    "the_wasteland_reworked:rusted_barrel": (130, 40, 13, 255),
    "the_wasteland_reworked:hazard_concrete": (138, 112, 18, 255),
    "the_wasteland_reworked:lead_plating": (76, 92, 90, 255),
    "the_wasteland_reworked:rusted_lead_plating": (97, 77, 58, 255),
    "the_wasteland_reworked:cut_lead_plating": (89, 103, 101, 255),
    "the_wasteland_reworked:radiation_hazard_sign": (119, 112, 69, 225),
    "the_wasteland_reworked:aluminium_grate": (67, 85, 83, 225),
    "the_wasteland_reworked:broken_aluminium_grate": (65, 84, 81, 225),
    "the_wasteland_reworked:support_beam": (58, 78, 75, 225),
    # Our own ruined stand-in: the vanilla blast-furnace colour already in
    # this table, composited under the pack's own damage_scorched overlay at
    # that overlay's real per-pixel alpha.
    "infinite_domain:ruined_blast_furnace": (86, 85, 87, 255),
}


def block_color(name: str) -> tuple[int, int, int, int]:
    if name in KNOWN_BLOCK_COLORS:
        return KNOWN_BLOCK_COLORS[name]
    if "sand" in name:
        return (194, 178, 128, 255)
    if "sea_pickle" in name or "kelp" in name:
        return (60, 130, 60, 255)
    if "prismarine" in name:
        return (99, 156, 136, 255)
    if "copper" in name:
        return (90, 150, 130, 255)
    if name.endswith("_bed"):
        return (130, 100, 110, 255)
    # Uncalibrated fallback: visible evidence exists but its color is not a
    # real approximation of the in-game block. Flagged loudly rather than
    # silently accepted, because this is the exact failure mode that made
    # the Wave 1/2 renders unreliable as audit evidence.
    print(f"WARNING: no curated render color for {name!r}; using a hash placeholder")
    digest = hashlib.sha256(name.encode("utf-8")).digest()
    return (60 + digest[0] % 160, 60 + digest[1] % 160, 60 + digest[2] % 160, 255)


def isometric_render(size: tuple[int, int, int], blocks: dict[tuple[int, int, int], str], out_path: Path) -> None:
    sx, sy, sz = size
    width = (sx + sz) * (TILE_W // 2) + TILE_W * 2
    height = (sx + sz) * (TILE_H // 2) + sy * TILE_H + TILE_H * 2
    image = Image.new("RGBA", (width, height), (18, 30, 46, 255))
    draw = ImageDraw.Draw(image, "RGBA")

    ordered = sorted(
        ((pos, name) for pos, name in blocks.items() if name != "minecraft:air"),
        key=lambda item: (item[0][1], item[0][0] + item[0][2]),
    )
    origin_x = (sz) * (TILE_W // 2) + TILE_W
    for (x, y, z), name in ordered:
        color = block_color(name)
        if color[3] == 0:
            continue
        screen_x = origin_x + (x - z) * (TILE_W // 2)
        screen_y = height - TILE_H * 2 - (x + z) * (TILE_H // 2) - y * TILE_H
        top = [
            (screen_x, screen_y - TILE_H // 2),
            (screen_x + TILE_W // 2, screen_y),
            (screen_x, screen_y + TILE_H // 2),
            (screen_x - TILE_W // 2, screen_y),
        ]
        shade = tuple(max(0, c - 25) if isinstance(c, int) else c for c in color[:3])
        draw.polygon(top, fill=color)
        draw.polygon(
            [(screen_x - TILE_W // 2, screen_y), (screen_x, screen_y + TILE_H // 2), (screen_x, screen_y + TILE_H // 2 + TILE_H), (screen_x - TILE_W // 2, screen_y + TILE_H)],
            fill=(*shade, color[3]),
        )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(out_path)


def floor_slice(size: tuple[int, int, int], blocks: dict[tuple[int, int, int], str], y: int, out_path: Path) -> None:
    sx, sy, sz = size
    scale = 12
    image = Image.new("RGB", (sx * scale, sz * scale), (18, 30, 46))
    draw = ImageDraw.Draw(image)
    for x in range(sx):
        for z in range(sz):
            name = blocks.get((x, y, z), "minecraft:air")
            color = block_color(name)
            if color[3] == 0:
                continue
            draw.rectangle([x * scale, z * scale, x * scale + scale - 1, z * scale + scale - 1], fill=color[:3])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(out_path)


# ---------------------------------------------------------------------------
# Depth-band lighting and the hero-asset view set
# ---------------------------------------------------------------------------
#
# The audit checklist in the standards document requires evidence captured
# "under the declared depth-band lighting, not the render pipeline's default
# lighting", and judges facade/silhouette coherence "at typical underwater
# fog/render distance". The two-view isometric+slice pass above satisfies the
# minimum bar; these views exist for assets whose silhouette IS the design --
# a 113-block submarine cannot be audited from one fixed isometric angle,
# and its single defining features (sail rake, towed-array pod, screw,
# compartment sequence) are each occluded in at least one of them.
#
# DEPTH_BANDS gives each band its ambient water color and how fast contrast
# is lost with distance, so a deep_floor asset is reviewed at deep_floor
# legibility rather than at a flattering full-daylight one.

DEPTH_BANDS: dict[str, tuple[tuple[int, int, int], float]] = {
    "shelf": ((46, 104, 128), 0.0072),
    "open_floor": ((28, 68, 92), 0.0135),
    "deep_floor": ((12, 30, 46), 0.0225),
    "abyssal": ((5, 12, 20), 0.0340),
}


def band_fog(color: tuple[int, int, int], band: str, distance: float) -> tuple[int, int, int]:
    """Attenuate a block color toward the band's ambient water color with
    distance, the way underwater fog actually removes contrast."""
    ambient, rate = DEPTH_BANDS.get(band, DEPTH_BANDS["open_floor"])
    mix = 1.0 - pow(2.718281828, -rate * max(0.0, distance))
    return tuple(int(round(c * (1.0 - mix) + a * mix)) for c, a in zip(color, ambient))


def _band_background(band: str) -> tuple[int, int, int]:
    ambient, _ = DEPTH_BANDS.get(band, DEPTH_BANDS["open_floor"])
    return tuple(max(0, c - 6) for c in ambient)


def elevation(
    size: tuple[int, int, int],
    blocks: dict[tuple[int, int, int], str],
    out_path: Path,
    axis: str = "x",
    band: str = "open_floor",
    scale: int = 6,
) -> None:
    """Orthographic elevation. axis='x' gives the port/starboard profile
    (the view a submarine's whole design is drawn against); axis='z' gives
    the bow-on section-shape view."""
    sx, sy, sz = size
    if axis == "x":
        w, h, depth_extent = sz, sy, sx
    else:
        w, h, depth_extent = sx, sy, sz
    image = Image.new("RGB", (w * scale, h * scale), _band_background(band))
    draw = ImageDraw.Draw(image)
    for u in range(w):
        for v in range(h):
            hit = None
            for d in range(depth_extent):
                pos = (d, v, u) if axis == "x" else (u, v, d)
                name = blocks.get(pos, "minecraft:air")
                if name in ("minecraft:air", "minecraft:water"):
                    continue
                hit = (name, d)
                break
            if hit is None:
                continue
            color = block_color(hit[0])
            if color[3] == 0:
                continue
            shaded = band_fog(color[:3], band, hit[1] * 1.6)
            y0 = (h - 1 - v) * scale
            draw.rectangle([u * scale, y0, u * scale + scale - 1, y0 + scale - 1], fill=shaded)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(out_path)


def plan(
    size: tuple[int, int, int],
    blocks: dict[tuple[int, int, int], str],
    out_path: Path,
    band: str = "open_floor",
    scale: int = 6,
) -> None:
    """Top-down plan: the highest non-air, non-water block over each column."""
    sx, sy, sz = size
    image = Image.new("RGB", (sx * scale, sz * scale), _band_background(band))
    draw = ImageDraw.Draw(image)
    for x in range(sx):
        for z in range(sz):
            for y in range(sy - 1, -1, -1):
                name = blocks.get((x, y, z), "minecraft:air")
                if name in ("minecraft:air", "minecraft:water"):
                    continue
                color = block_color(name)
                if color[3] == 0:
                    break
                shaded = band_fog(color[:3], band, (sy - y) * 1.1)
                draw.rectangle([x * scale, z * scale, x * scale + scale - 1, z * scale + scale - 1], fill=shaded)
                break
    out_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(out_path)


def longitudinal_section(
    size: tuple[int, int, int],
    blocks: dict[tuple[int, int, int], str],
    x: int,
    out_path: Path,
    scale: int = 6,
) -> None:
    """Centreline cutaway (y-z at one x). For a programmed interior this is
    the view that actually proves the compartment sequence, deck heights and
    vertical traversal exist -- a floor slice alone cannot."""
    sx, sy, sz = size
    image = Image.new("RGB", (sz * scale, sy * scale), (18, 30, 46))
    draw = ImageDraw.Draw(image)
    for z in range(sz):
        for y in range(sy):
            name = blocks.get((x, y, z), "minecraft:air")
            color = block_color(name)
            if color[3] == 0:
                continue
            y0 = (sy - 1 - y) * scale
            draw.rectangle([z * scale, y0, z * scale + scale - 1, y0 + scale - 1], fill=color[:3])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(out_path)


def transverse_section(
    size: tuple[int, int, int],
    blocks: dict[tuple[int, int, int], str],
    z: int,
    out_path: Path,
    scale: int = 14,
) -> None:
    """Frame section (x-y at one z): the view that shows a double hull is
    actually double, with the ballast annulus between the two skins."""
    sx, sy, sz = size
    image = Image.new("RGB", (sx * scale, sy * scale), (18, 30, 46))
    draw = ImageDraw.Draw(image)
    for x in range(sx):
        for y in range(sy):
            name = blocks.get((x, y, z), "minecraft:air")
            color = block_color(name)
            if color[3] == 0:
                continue
            y0 = (sy - 1 - y) * scale
            draw.rectangle([x * scale, y0, x * scale + scale - 1, y0 + scale - 1], fill=color[:3])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(out_path)


def silhouette(
    size: tuple[int, int, int],
    blocks: dict[tuple[int, int, int], str],
    out_path: Path,
    band: str = "open_floor",
    axis: str = "x",
    scale: int = 5,
) -> None:
    """Pure range silhouette: every solid block collapsed to one mass against
    the band's ambient water. This is the honest test of standards point 4 --
    does the asset read as a structure, or as a lump of seafloor."""
    sx, sy, sz = size
    if axis == "x":
        w, h, depth_extent = sz, sy, sx
    else:
        w, h, depth_extent = sx, sy, sz
    ambient, _ = DEPTH_BANDS.get(band, DEPTH_BANDS["open_floor"])
    mass = tuple(max(0, int(c * 0.30)) for c in ambient)
    image = Image.new("RGB", (w * scale, h * scale), ambient)
    draw = ImageDraw.Draw(image)
    for u in range(w):
        for v in range(h):
            solid = False
            for d in range(depth_extent):
                pos = (d, v, u) if axis == "x" else (u, v, d)
                name = blocks.get(pos, "minecraft:air")
                if name in ("minecraft:air", "minecraft:water"):
                    continue
                solid = True
                break
            if solid:
                y0 = (h - 1 - v) * scale
                draw.rectangle([u * scale, y0, u * scale + scale - 1, y0 + scale - 1], fill=mass)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(out_path)


def render_akula_assembly(out_dir: Path, band: str = "open_floor") -> dict[str, Any]:
    """Composite the jigsaw assembly the way the game will build it and render
    it as one scene.

    The offsets come from resolving the jigsaw blocks in the shipped NBT, not
    from the numbers the generator intended, so this render doubles as visual
    confirmation that the joints line up. Reviewing the three pieces
    separately cannot show the thing the assembly exists to show: that the
    outcrop sits between the two halves and explains them."""
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from validate_deep_sea_structures import resolve_akula_assembly
    except ImportError:
        return {}
    layout = resolve_akula_assembly()
    world: dict[tuple[int, int, int], str] = {}
    for name, piece in layout.items():
        if name.startswith("_"):
            continue
        ox, oy, oz = piece["origin"]
        for (x, y, z), material in piece["cells"].items():
            if material == "minecraft:jigsaw":
                continue
            world[(x + ox, y + oy, z + oz)] = material
    if not world:
        return {}
    xs = [p[0] for p in world]
    ys = [p[1] for p in world]
    zs = [p[2] for p in world]
    shift = (-min(xs), -min(ys), -min(zs))
    size = (max(xs) - min(xs) + 1, max(ys) - min(ys) + 1, max(zs) - min(zs) + 1)
    blocks = {(x + shift[0], y + shift[1], z + shift[2]): m for (x, y, z), m in world.items()}
    spine_origin_z = layout["akula_wreck_spine"]["origin"][2] + shift[2]
    views = {
        "profile": out_dir / "akula_wreck_site_profile.png",
        "silhouette": out_dir / "akula_wreck_site_silhouette.png",
        "plan": out_dir / "akula_wreck_site_plan.png",
        "centreline_cutaway": out_dir / "akula_wreck_site_centreline_cutaway.png",
    }
    elevation(size, blocks, views["profile"], axis="x", band=band, scale=7)
    silhouette(size, blocks, views["silhouette"], band=band, axis="x", scale=5)
    plan(size, blocks, views["plan"], band=band, scale=5)
    longitudinal_section(size, blocks, size[0] // 2, views["centreline_cutaway"], scale=7)
    return {
        "assembled_size": list(size),
        "spine_origin_z_in_composite": spine_origin_z,
        **{k: str(v.relative_to(ROOT)) for k, v in views.items()},
    }


def render_all() -> dict[str, Any]:
    manifest: dict[str, Any] = {}
    slice_heights = {
        "coastal_patrol_wreck_clean_master": 1,
        "coastal_patrol_wreck_damaged": 1,
        "coastal_patrol_wreck": 1,
        "coastal_patrol_debris_field": 1,
        "flooded_relay_shelter_clean_master": 2,
        "flooded_relay_shelter": 2,
        "abyssal_mining_rig_clean_master": 5,
        "abyssal_mining_rig": 5,
        "abyssal_vent_field": 1,
        "akula_project971_clean_master": 6,
        "akula_wreck_forward_damaged": 9,
        "akula_wreck_aft_damaged": 9,
        "akula_wreck_forward": 9,
        "akula_wreck_aft": 9,
        "akula_debris_field": 1,
        "akula_wreck_spine": 8,
    }
    # Assets whose design IS their silhouette and their compartment sequence
    # get the full hero view set, at their own declared depth band. One fixed
    # isometric angle cannot audit a 113-block submarine: the standards
    # require the defining functional feature to be identifiable in at least
    # one required render, and for this family that means the sail rake, the
    # towed-array pod, the screw and the double hull each need a view that
    # actually carries them.
    hero_views = {
        "akula_project971_clean_master": ("open_floor", 8),
        "akula_wreck_forward_damaged": ("open_floor", 12),
        "akula_wreck_aft_damaged": ("open_floor", 12),
        "akula_wreck_forward": ("open_floor", 12),
        "akula_wreck_aft": ("open_floor", 12),
        "akula_wreck_spine": ("open_floor", 12),
    }
    frame_sections = {
        "akula_project971_clean_master": {
            "c1_torpedo_room": 26, "c2_command_post": 48,
            "c4_reactor": 77, "c5_turbine": 89,
        },
    }
    for path in sorted(STRUCTURE_DIR.glob("*.nbt")):
        name = path.stem
        size, blocks = load_structure(path)
        iso_path = OUTPUT_DIR / f"{name}_isometric.png"
        slice_path = OUTPUT_DIR / f"{name}_floor_slice_y{slice_heights.get(name, 1)}.png"
        isometric_render(size, blocks, iso_path)
        floor_slice(size, blocks, slice_heights.get(name, 1), slice_path)
        entry = {
            "size": list(size),
            "isometric": str(iso_path.relative_to(ROOT)),
            "floor_slice": str(slice_path.relative_to(ROOT)),
        }
        if name in hero_views:
            band, scale = hero_views[name]
            views = {
                "profile": lambda p: elevation(size, blocks, p, axis="x", band=band, scale=scale),
                "bow_on": lambda p: elevation(size, blocks, p, axis="z", band=band, scale=scale + 2),
                "plan": lambda p: plan(size, blocks, p, band=band, scale=scale),
                "silhouette": lambda p: silhouette(size, blocks, p, band=band, axis="x", scale=max(4, scale - 4)),
                "centreline_cutaway": lambda p: longitudinal_section(size, blocks, size[0] // 2, p, scale=scale),
            }
            for view, draw in views.items():
                out = OUTPUT_DIR / f"{name}_{view}.png"
                draw(out)
                entry[view] = str(out.relative_to(ROOT))
            entry["depth_band"] = band
        for label, z in frame_sections.get(name, {}).items():
            out = OUTPUT_DIR / f"{name}_frame_{label}_z{z}.png"
            transverse_section(size, blocks, z, out, scale=14)
            entry[f"frame_{label}"] = str(out.relative_to(ROOT))
        manifest[name] = entry
    assembly = render_akula_assembly(OUTPUT_DIR)
    if assembly:
        manifest["_akula_wreck_site_assembly"] = assembly
    return manifest


if __name__ == "__main__":
    import json

    result = render_all()
    print(json.dumps(result, indent=2))
