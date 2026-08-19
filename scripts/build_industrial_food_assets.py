"""Generate hard-edged 16px food-industry assets from the authoritative config."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw

from install_generated_item_texture import install


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "kubejs/config/industrial_food.json"
ASSETS = ROOT / "kubejs/assets/kubejs"


def rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def shade(color: tuple[int, int, int], delta: int) -> tuple[int, int, int, int]:
    return tuple(max(0, min(255, channel + delta)) for channel in color) + (255,)


def item_icon(kind: str, color: tuple[int, int, int]) -> Image.Image:
    im = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    deep, dark, mid, light = shade(color, -85), shade(color, -45), shade(color, 0), shade(color, 58)
    steel_deep, steel, steel_hi = (42, 48, 52, 255), (91, 102, 108, 255), (196, 207, 211, 255)
    if kind in {"powder", "herb"}:
        d.ellipse((5,22,27,27), fill=steel_deep)
        d.polygon([(5,24),(8,18),(13,13),(19,12),(25,18),(28,24)], fill=deep)
        d.polygon([(7,23),(10,18),(15,14),(21,15),(26,23)], fill=mid)
        d.polygon([(12,18),(17,15),(21,17),(18,20)], fill=light)
        d.point([(10,21),(14,22),(20,20),(23,22),(17,24)], fill=dark)
        if kind == "herb":
            d.line([(16,21),(16,5)], fill=deep, width=2)
            d.polygon([(15,10),(8,6),(10,14)], fill=mid)
            d.polygon([(17,14),(25,8),(22,17)], fill=light)
            d.polygon([(15,17),(8,13),(10,20)], fill=dark)
    elif kind in {"packet", "pouch", "mre"}:
        d.polygon([(7,3),(24,4),(27,8),(25,28),(6,27),(4,23),(5,7)], fill=deep)
        d.polygon([(7,5),(23,6),(24,9),(22,25),(8,25),(7,22)], fill=mid)
        d.line((8,8,23,9), fill=light, width=2)
        d.line((7,22,22,23), fill=dark, width=2)
        d.rectangle((11,11,20,20), fill=dark, outline=light)
        d.polygon([(14,13),(19,15),(16,19),(12,17)], fill=light)
        d.point([(6,9),(6,13),(6,17),(24,12),(23,17),(23,21)], fill=steel_hi)
        if kind == "mre":
            d.rectangle((6,4,24,7), fill=steel)
            d.rectangle((9,6,21,8), fill=dark)
    elif kind in {"vial", "jar", "bottle"}:
        d.rectangle((12,2,20,5), fill=steel_deep)
        d.rectangle((13,2,19,4), fill=steel_hi)
        d.rectangle((12,5,20,10), fill=steel, outline=steel_deep)
        d.polygon([(11,8),(21,8),(24,13),(23,27),(8,27),(7,13)], fill=deep)
        d.polygon([(11,10),(20,10),(21,14),(20,25),(10,25),(9,14)], fill=mid)
        d.polygon([(11,11),(14,10),(13,24),(10,23)], fill=light)
        d.rectangle((9,17,22,23), fill=dark)
        d.rectangle((11,18,20,21), fill=light)
        if kind == "vial":
            d.rectangle((10,9,21,27), fill=deep)
            d.rectangle((12,11,19,24), fill=mid)
        if kind == "jar":
            d.rectangle((7,10,24,26), fill=deep)
            d.rectangle((9,12,22,24), fill=mid)
    elif kind in {"can", "can_empty"}:
        d.ellipse((8,3,24,8), fill=steel_hi, outline=steel_deep)
        d.rectangle((8,6,24,26), fill=steel, outline=steel_deep)
        d.ellipse((8,23,24,28), fill=steel_deep)
        d.ellipse((10,24,22,26), fill=steel_hi)
        d.ellipse((12,4,20,6), fill=steel_deep)
        d.rectangle((10,7,12,23), fill=(151,164,169,255))
        if kind == "can":
            d.polygon([(10,9),(23,8),(23,22),(10,23)], fill=dark)
            d.polygon([(12,10),(21,9),(21,15),(12,16)], fill=mid)
            d.polygon([(14,11),(19,10),(18,14),(13,15)], fill=light)
    elif kind in {"food_can", "food_can_empty"}:
        d.ellipse((4,9,28,14), fill=steel_hi, outline=steel_deep)
        d.rectangle((4,12,28,24), fill=steel, outline=steel_deep)
        d.ellipse((4,21,28,27), fill=steel_deep)
        d.ellipse((7,22,25,25), fill=steel_hi)
        d.line((7,13,7,22), fill=(160,172,176,255), width=2)
        if kind == "food_can":
            d.rectangle((6,15,26,21), fill=dark)
            d.polygon([(10,16),(22,16),(20,20),(9,20)], fill=mid)
            d.point([(12,18),(16,17),(20,18)], fill=light)
    elif kind == "meal":
        d.polygon([(3,12),(27,9),(29,14),(26,26),(6,28),(3,23)], fill=steel_deep)
        d.polygon([(5,13),(25,11),(27,14),(24,23),(7,25),(5,22)], fill=steel)
        d.line((15,12,15,24), fill=steel_deep, width=2)
        d.line((6,19,25,17), fill=steel_deep, width=2)
        d.polygon([(7,14),(13,13),(13,18),(7,18)], fill=mid)
        d.ellipse((17,12,24,17), fill=light)
        d.polygon([(8,20),(14,20),(12,23),(7,23)], fill=dark)
        d.point([(19,20),(21,19),(23,20),(20,22)], fill=mid)
    elif kind == "six_pack":
        for y in (7,11):
            for x in (7,14,21):
                d.ellipse((x-3,y-3,x+3,y+3), fill=steel_hi, outline=steel_deep)
                d.rectangle((x-3,y,x+3,24), fill=dark)
        d.polygon([(4,10),(27,9),(28,24),(6,27),(3,22)], fill=deep)
        d.polygon([(6,12),(25,11),(25,22),(7,24)], fill=mid)
        d.rectangle((12,7,19,12), fill=deep)
        d.rectangle((14,8,18,10), fill=light)
        d.line((8,15,23,14), fill=light, width=2)
    elif kind == "case":
        d.polygon([(3,10),(20,5),(29,11),(28,24),(11,29),(3,23)], fill=deep)
        d.polygon([(5,10),(20,7),(27,11),(11,16)], fill=light)
        d.polygon([(5,12),(10,17),(10,26),(5,22)], fill=dark)
        d.polygon([(11,17),(27,12),(26,22),(11,27)], fill=mid)
        d.line((15,15,15,26), fill=dark, width=2)
        d.rectangle((17,17,24,21), fill=dark, outline=light)
        d.line((6,20,9,22), fill=light, width=2)
    elif kind == "crate":
        d.polygon([(3,8),(20,4),(29,10),(28,25),(10,29),(3,23)], fill=deep)
        d.polygon([(5,10),(20,6),(27,11),(26,23),(10,27),(5,22)], fill=mid)
        d.line((7,12,24,22), fill=light, width=3)
        d.line((24,12,8,24), fill=light, width=3)
        d.line((10,9,10,27), fill=dark, width=3)
        d.line((25,10,25,23), fill=dark, width=3)
        d.polygon([(3,7),(20,3),(29,9),(27,12),(10,15),(3,11)], fill=dark)
    elif kind == "pallet":
        d.polygon([(3,10),(20,5),(29,10),(27,24),(10,28),(3,23)], fill=deep)
        d.polygon([(5,11),(20,7),(27,11),(25,21),(10,25),(5,21)], fill=mid)
        d.line((8,10,8,23), fill=light, width=2)
        d.line((14,8,14,24), fill=light, width=2)
        d.line((21,8,21,22), fill=light, width=2)
        d.line((5,15,26,10), fill=dark, width=2)
        d.line((5,21,25,16), fill=dark, width=2)
        d.polygon([(4,24),(10,27),(27,23),(27,27),(10,31),(4,28)], fill=dark)
        d.line((7,26,25,22), fill=light, width=2)
    else:
        d.polygon([(7,5),(24,7),(27,23),(21,28),(6,25),(4,10)], fill=deep)
        d.polygon([(8,7),(22,9),(24,22),(19,25),(8,23),(6,11)], fill=mid)
        d.rectangle((11,11,20,20), fill=light)
    return im


def fluid_texture(color: tuple[int, int, int], size: int, flowing: bool) -> Image.Image:
    im = Image.new("RGBA", (size, size), color + (220,))
    d = ImageDraw.Draw(im)
    dark, light = shade(color, -25), shade(color, 28)
    for y in range(0, size, 4):
        offset = (y // 4 * (2 if flowing else 1)) % 6
        for x in range(-6, size + 6, 6):
            d.line((x + offset, y, x + offset + 3, y), fill=light)
            d.line((x + offset + 3, y + 2, x + offset + 6, y + 2), fill=dark)
    return im


def main() -> None:
    data = json.loads(CONFIG.read_text(encoding="utf-8"))
    item_dir = ASSETS / "textures/item"
    model_dir = ASSETS / "models/item"
    block_texture_dir = ASSETS / "textures/block"
    fluid_dir = ASSETS / "textures/fluid"
    lang_dir = ASSETS / "lang"
    for path in (item_dir, model_dir, block_texture_dir, fluid_dir, lang_dir):
        path.mkdir(parents=True, exist_ok=True)

    items = list(data["items"])
    for flavor in data["flavors"]:
        items.extend([
            {"id": f"{flavor['id']}_fruit_pulp", "name": f"{flavor['name']} Pulp", "kind": "powder", "color": flavor["color"]},
            {"id": f"{flavor['id']}_juice_concentrate", "name": f"{flavor['name']} Juice Concentrate", "kind": "vial", "color": flavor["color"]},
            {"id": f"bottled_{flavor['id']}_juice", "name": f"Bottled {flavor['name']} Juice", "kind": "bottle", "color": flavor["accent"]},
            {"id": f"{flavor['id']}_soda_can", "name": f"{flavor['name']} Soda Can", "kind": "can", "color": flavor["color"]},
            {"id": f"{flavor['id']}_soda_six_pack", "name": f"{flavor['name']} Soda Six-Pack", "kind": "six_pack", "color": flavor["color"]},
            {"id": f"{flavor['id']}_soda_case", "name": f"{flavor['name']} Soda Case", "kind": "case", "color": flavor["color"]},
        ])

    language: dict[str, str] = {}
    rendered_items: list[tuple[str, Image.Image]] = []
    for item in items:
        item_id = item["id"]
        icon = item_icon(item["kind"], rgb(item["color"]))
        icon.save(item_dir / f"{item_id}.png")
        rendered_items.append((item_id, icon))
        (model_dir / f"{item_id}.json").write_text(json.dumps({
            "parent": "minecraft:item/generated",
            "textures": {"layer0": f"kubejs:item/{item_id}"},
        }, indent=2) + "\n", encoding="utf-8")
        language[f"item.kubejs.{item_id}"] = item["name"]
        if item["kind"] == "pallet":
            language[f"block.kubejs.{item_id}"] = item["name"]

    fluids = list(data["fluids"])
    for flavor in data["flavors"]:
        fluids.extend([
            {"id": f"pressed_{flavor['id']}_juice", "name": f"Pressed {flavor['name']} Juice", "color": flavor["color"]},
            {"id": f"prepared_{flavor['id']}_beverage", "name": f"Prepared {flavor['name']} Beverage", "color": flavor["accent"]},
            {"id": f"{flavor['id']}_soda_base", "name": f"{flavor['name']} Soda Base", "color": flavor["color"]},
            {"id": f"carbonated_{flavor['id']}_soda", "name": f"Carbonated {flavor['name']} Soda", "color": flavor["accent"]},
        ])
    for fluid in fluids:
        color = rgb(fluid["color"])
        fluid_texture(color, 16, False).save(fluid_dir / f"{fluid['id']}_still.png")
        fluid_texture(color, 32, True).save(fluid_dir / f"{fluid['id']}_flow.png")
        language[f"fluid.kubejs.{fluid['id']}"] = fluid["name"]

    (lang_dir / "en_us.json").write_text(json.dumps(language, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    # Restore approved full-resolution renders before building the review sheet so
    # the sheet reflects the textures that are actually deployed in-game.
    approved_sources = ROOT / "docs/texture-audit/generated-sources"
    approved_ids = {item["id"] for item in items}
    if approved_sources.exists():
        for source in approved_sources.glob("*.png"):
            if source.stem in approved_ids:
                install(source, source.stem)
        rendered_items = [
            (item_id, Image.open(item_dir / f"{item_id}.png").convert("RGBA"))
            for item_id, _icon in rendered_items
        ]

    # Nearest-neighbor review sheet: large enough to inspect silhouettes and alpha edges.
    review_dir = ROOT / "docs/industrial-food"
    review_dir.mkdir(parents=True, exist_ok=True)
    columns, tile_w, tile_h, scale = 6, 112, 94, 2
    rows = (len(rendered_items) + columns - 1) // columns
    sheet = Image.new("RGBA", (columns * tile_w, rows * tile_h), (25, 28, 30, 255))
    draw = ImageDraw.Draw(sheet)
    for index, (item_id, icon) in enumerate(rendered_items):
        x = (index % columns) * tile_w
        y = (index // columns) * tile_h
        large = icon.resize((32 * scale, 32 * scale), Image.Resampling.NEAREST)
        sheet.alpha_composite(large, (x + 24, y + 6))
        label = item_id if len(item_id) <= 18 else item_id[:17] + "…"
        draw.text((x + 4, y + 74), label, fill=(230, 233, 235, 255))
    sheet.convert("RGB").save(review_dir / "icon-contact-sheet.png")
    print(f"Generated {len(items)} inventory textures/models and {len(fluids) * 2} fluid textures from industrial_food.json.")


if __name__ == "__main__":
    main()
