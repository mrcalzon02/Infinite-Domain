from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path

from PIL import Image, ImageFilter


def is_pale_background(pixel: tuple[int, int, int]) -> bool:
    low = min(pixel)
    high = max(pixel)
    return low >= 215 and high - low <= 14


def is_black_background(pixel: tuple[int, int, int]) -> bool:
    return max(pixel) <= 24


def extract(source: Path, background: str) -> None:
    image = Image.open(source).convert("RGBA")
    rgb = image.convert("RGB")
    width, height = image.size
    pixels = rgb.load()
    visited = bytearray(width * height)
    queue: deque[tuple[int, int]] = deque()

    predicate = is_black_background if background == "black" else is_pale_background

    def enqueue(x: int, y: int) -> None:
        index = y * width + x
        if not visited[index] and predicate(pixels[x, y]):
            visited[index] = 1
            queue.append((x, y))

    for x in range(width):
        enqueue(x, 0)
        enqueue(x, height - 1)
    for y in range(height):
        enqueue(0, y)
        enqueue(width - 1, y)

    while queue:
        x, y = queue.popleft()
        if x:
            enqueue(x - 1, y)
        if x + 1 < width:
            enqueue(x + 1, y)
        if y:
            enqueue(x, y - 1)
        if y + 1 < height:
            enqueue(x, y + 1)

    alpha = Image.new("L", image.size, 255)
    alpha_pixels = alpha.load()
    for y in range(height):
        row = y * width
        for x in range(width):
            if visited[row + x]:
                alpha_pixels[x, y] = 0

    alpha = alpha.filter(ImageFilter.GaussianBlur(0.65))
    image.putalpha(alpha)
    image.save(source, optimize=True)


def keep_largest_component(source: Path) -> None:
    image = Image.open(source).convert("RGBA")
    alpha = image.getchannel("A")
    width, height = image.size
    pixels = alpha.load()
    visited = bytearray(width * height)
    largest: list[int] = []
    for start in range(width * height):
        if visited[start] or pixels[start % width, start // width] <= 32:
            continue
        visited[start] = 1
        queue = deque([start])
        component: list[int] = []
        while queue:
            index = queue.popleft()
            component.append(index)
            x, y = index % width, index // width
            for neighbor in (
                index - 1 if x else -1,
                index + 1 if x + 1 < width else -1,
                index - width if y else -1,
                index + width if y + 1 < height else -1,
            ):
                if neighbor >= 0 and not visited[neighbor]:
                    nx, ny = neighbor % width, neighbor // width
                    if pixels[nx, ny] > 32:
                        visited[neighbor] = 1
                        queue.append(neighbor)
        if len(component) > len(largest):
            largest = component
    keep = bytearray(width * height)
    for index in largest:
        keep[index] = 1
    cleaned = Image.new("L", image.size)
    cleaned_pixels = cleaned.load()
    for index, retained in enumerate(keep):
        if retained:
            x, y = index % width, index // width
            cleaned_pixels[x, y] = pixels[x, y]
    image.putalpha(cleaned.filter(ImageFilter.GaussianBlur(0.35)))
    image.save(source, optimize=True)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract border-connected pale checkerboard from a generated PNG."
    )
    parser.add_argument("sources", nargs="+", type=Path)
    parser.add_argument(
        "--background",
        choices=("pale", "black"),
        default="pale",
        help="Border-connected background family to convert to alpha.",
    )
    parser.add_argument(
        "--largest-component",
        action="store_true",
        help="After extraction, discard disconnected alpha specks.",
    )
    args = parser.parse_args()
    for source in args.sources:
        extract(source, args.background)
        if args.largest_component:
            keep_largest_component(source)
        print(source)


if __name__ == "__main__":
    main()
