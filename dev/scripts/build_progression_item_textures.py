"""Generate cohesive 32px era/progression icons and repair Darknet alpha mattes."""

from __future__ import annotations

from collections import deque
from pathlib import Path

from PIL import Image, ImageDraw

from install_generated_item_texture import install


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "kubejs/assets/kubejs/textures/item"

ERA = {
    0: ((103, 91, 73), (170, 148, 105)),
    1: ((109, 72, 43), (218, 139, 55)),
    2: ((76, 82, 87), (190, 91, 55)),
    3: ((79, 74, 53), (224, 184, 51)),
    4: ((76, 66, 44), (245, 210, 69)),
    5: ((52, 83, 97), (104, 204, 225)),
    6: ((59, 83, 54), (139, 215, 83)),
    7: ((57, 74, 109), (116, 159, 234)),
    8: ((74, 55, 103), (187, 126, 231)),
}


def rgba(c, a=255): return (*c, a)
def shift(c, amount): return tuple(max(0, min(255, v + amount)) for v in c)


def base() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    return image, ImageDraw.Draw(image)


def charter(era: int, role: str) -> Image.Image:
    dark, accent = ERA[era]
    image, d = base()
    metal = (49, 55, 59)
    paper = shift(accent, 65)
    # Angled reinforced dossier/scroll, inspired by the approved concept sheet.
    d.polygon([(5,7),(22,4),(28,9),(25,25),(8,28),(3,22)], fill=rgba(shift(metal,-22)))
    d.polygon([(6,7),(22,5),(26,9),(23,23),(8,26),(5,21)], fill=rgba(metal))
    d.polygon([(9,8),(21,7),(23,10),(21,21),(9,23),(7,20)], fill=rgba(paper))
    d.line([(9,10),(20,9)], fill=rgba(shift(paper,-45)), width=2)
    d.line([(9,20),(20,18)], fill=rgba(shift(paper,-55)), width=1)
    d.rectangle((4,8,6,19), fill=rgba(shift(metal,45)))
    d.rectangle((23,10,26,20), fill=rgba(shift(metal,35)))
    if role == "mining":
        d.polygon([(12,12),(17,10),(20,13),(17,17),(12,17),(10,14)], fill=rgba(accent))
        d.line([(12,18),(19,11)], fill=rgba(dark), width=2)
    elif role == "farming":
        d.line([(15,19),(16,11)], fill=rgba(dark), width=2)
        d.polygon([(15,14),(10,11),(11,16)], fill=rgba(accent))
        d.polygon([(16,16),(21,12),(20,18)], fill=rgba(shift(accent,25)))
    else:
        d.ellipse((11,10,21,20), fill=rgba(shift(metal,-15)), outline=rgba(shift(metal,70)), width=1)
        d.polygon([(16,11),(18,16),(15,19),(14,15)], fill=rgba(accent))
        d.point((16,15), fill=(255,255,255,255))
    d.rectangle((7,24,11,26), fill=rgba(accent))
    d.rectangle((20,22,24,24), fill=rgba(shift(accent,-30)))
    return image


def core(era: int, incomplete: bool = False) -> Image.Image:
    dark, accent = ERA[era]
    image, d = base()
    shell = (48, 55, 62)
    d.polygon([(7,5),(23,4),(28,9),(27,23),(22,28),(8,27),(4,22),(4,9)], fill=rgba(shift(shell,-25)))
    d.polygon([(8,6),(22,6),(26,10),(25,22),(21,26),(9,25),(6,21),(6,10)], fill=rgba(shell))
    for box in ((6,7,10,10),(21,7,25,10),(6,21,10,24),(21,21,25,24)):
        d.rectangle(box, fill=rgba(shift(accent,-20)), outline=rgba(shift(shell,60)))
    d.ellipse((9,8,23,23), fill=rgba(shift(shell,-18)), outline=rgba(shift(shell,75)), width=2)
    d.ellipse((11,10,21,21), fill=rgba(shift(accent,-45)))
    d.ellipse((13,12,20,19), fill=rgba(accent))
    d.rectangle((15,13,17,17), fill=rgba(shift(accent,75)))
    d.point([(12,11),(20,11),(11,19),(21,18)], fill=rgba(shift(accent,55)))
    if incomplete:
        d.line([(7,24),(24,7)], fill=(20,20,22,255), width=3)
        d.line([(9,24),(24,9)], fill=rgba(accent), width=1)
    return image


def emblem(era: int, ultimate: bool = False) -> Image.Image:
    dark, accent = ERA[era]
    image, d = base()
    points = [(16,2),(20,8),(27,6),(25,13),(30,17),(24,21),(25,28),(18,25),(13,30),(10,24),(3,25),(6,18),(2,13),(9,11),(10,4)]
    d.polygon(points, fill=rgba(shift(dark,-35)))
    inner = [(16,5),(19,11),(25,9),(22,15),(27,18),(21,20),(22,25),(17,22),(13,26),(12,21),(6,22),(9,17),(6,14),(12,14),(12,8)]
    d.polygon(inner, fill=rgba(accent))
    d.ellipse((11,10,21,21), fill=rgba(shift(dark,-5)), outline=rgba(shift(accent,65)))
    d.rectangle((15,12,17,19), fill=rgba(shift(accent,75)))
    d.rectangle((12,15,20,17), fill=rgba(shift(accent,75)))
    if ultimate:
        d.point([(4,4),(27,3),(29,27),(3,28)], fill=(255,255,255,255))
    return image


def cache(era: int, rare: bool) -> Image.Image:
    dark, accent = ERA[era]
    image, d = base()
    d.polygon([(4,9),(20,5),(28,10),(27,24),(11,29),(4,23)], fill=rgba(shift(dark,-35)))
    d.polygon([(5,10),(20,7),(26,11),(25,22),(11,26),(6,22)], fill=rgba(dark))
    d.polygon([(6,10),(20,7),(26,11),(11,15)], fill=rgba(shift(dark,35)))
    d.line([(11,15),(11,26)], fill=rgba(shift(dark,-45)), width=2)
    d.rectangle((16,13,22,19), fill=rgba(shift(dark,-30)), outline=rgba(accent))
    d.rectangle((18,14,20,17), fill=rgba(shift(accent,55)))
    d.line([(7,20),(10,22)], fill=rgba(accent), width=2)
    if rare:
        d.rectangle((7,8,20,10), fill=rgba(accent))
        d.point([(4,5),(27,7),(28,26)], fill=rgba(shift(accent,75)))
    return image


def injector(tier: int) -> Image.Image:
    accent = ERA[min(8, max(1, tier))][1]
    image, d = base()
    d.polygon([(8,3),(22,3),(26,7),(24,24),(19,29),(8,27),(5,22),(6,7)], fill=(25,25,32,255))
    d.rectangle((9,5,21,9), fill=rgba(shift(accent,-55)), outline=(98,101,115,255))
    d.rectangle((9,9,22,22), fill=(47,48,61,255), outline=(116,119,135,255))
    d.rectangle((11,11,20,20), fill=rgba(shift(accent,-45)))
    d.line([(12,18),(14,13),(16,18),(19,12)], fill=rgba(shift(accent,70)), width=2)
    d.rectangle((10,24,20,27), fill=(83,85,98,255))
    for x in range(11, 11 + min(tier, 8)):
        d.point((x,25), fill=rgba(accent))
    return image


def keep_largest_foreground(image: Image.Image) -> Image.Image:
    image = image.convert("RGBA")
    pixels = image.load()
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]
            if r > 232 and g > 232 and b > 232:
                pixels[x, y] = (0, 0, 0, 0)
    points = {(x,y) for y in range(image.height) for x in range(image.width) if pixels[x,y][3] > 0}
    components = []
    while points:
        seed = points.pop(); comp = {seed}; queue = deque([seed])
        while queue:
            x, y = queue.popleft()
            for yy in range(max(0,y-1), min(image.height,y+2)):
                for xx in range(max(0,x-1), min(image.width,x+2)):
                    if (xx,yy) in points:
                        points.remove((xx,yy)); comp.add((xx,yy)); queue.append((xx,yy))
        components.append(comp)
    if components:
        keep = max(components, key=len)
        for y in range(image.height):
            for x in range(image.width):
                if pixels[x,y][3] and (x,y) not in keep:
                    pixels[x,y] = (0,0,0,0)
    return image


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    # Era 0 and Era 1 special registrations.
    for item_id, role in (("scavenger_contribution","exploration"),("mason_contribution","mining"),("habitation_contribution","farming")):
        charter(0, role).save(OUT / f"{item_id}.png")
    for role in ("mining", "farming", "exploration"):
        charter(1, role).save(OUT / f"era1_{role}_contribution.png")
    core(1).save(OUT / "mechanical_foundation_core.png")

    core_names = {2:"industrial",3:"chemical",4:"electrical",5:"automation",6:"atomic",7:"orbital"}
    for era in range(2, 9):
        for role in ("mining", "farming", "exploration"):
            charter(era, role).save(OUT / f"era{era}_{role}_contribution.png")
        core_id = "infinite_domain_core" if era == 8 else f"{core_names[era]}_foundation_core"
        core(era).save(OUT / f"{core_id}.png")
    core(2, incomplete=True).save(OUT / "incomplete_industrial_engineering_core.png")

    for era in range(0, 9):
        emblem(era).save(OUT / f"era{era}_mastery_emblem.png")
    emblem(8, True).save(OUT / "ultima_collection_emblem.png")

    reward_ids = ["era0_priority_cache"]
    for era in range(1, 9):
        reward_ids.extend([f"era{era}_supply_bag", f"era{era}_priority_cache"])
    for item_id in reward_ids:
        era = int(re.search(r"era(\d)", item_id).group(1))
        cache(era, "priority" in item_id).save(OUT / f"{item_id}.png")

    core(8).save(OUT / "darknet_temporal_core.png")
    for tier in range(1, 9):
        injector(tier).save(OUT / f"darknet_session_injector_tier_{tier}.png")

    matte_names = ["darknet_data_cache", "scraped_access_token", "encrypted_credential_bundle", "black_ice_kernel", "zero_day_archive", "root_authority_key"]
    for name in matte_names:
        path = OUT / f"{name}.png"
        with Image.open(path) as image:
            keep_largest_foreground(image).save(path)
    approved_sources = ROOT / "dev/docs/texture-audit/generated-sources"
    approved = 0
    if approved_sources.exists():
        for source in approved_sources.glob("*.png"):
            install(source, source.stem)
            approved += 1
    print(f"Generated fallback progression icons, repaired Darknet alpha mattes, and restored {approved} approved item-specific sources.")


if __name__ == "__main__":
    import re
    main()
