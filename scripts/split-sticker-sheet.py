#!/usr/bin/env python3
"""Package original Spooky artwork as independent transparent stickers."""
from collections import deque
from pathlib import Path
from PIL import Image, ImageChops, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "art/source"
STICKERS = ROOT / "macos/Stickers"
OBJECTS = STICKERS / "Objects"

# Several output filenames are legacy position keys; preserve them so an app
# update does not discard existing saved Desktop sticker placements.
SHEETS = [("stickers-01.png", 4, 4), ("stickers-02.png", 4, 4),
          ("stickers-03.png", 4, 4), ("stickers-04.png", 2, 2)]
STATIC = {
    "scorpio": (1, 11), "taurus": (2, 5), "axe-ghost": (3, 12),
    "pumpkin-ghost": (2, 6), "virgo-stamp": (3, 0),
    "treat-ghost": (3, 3), "leo-stamp": (2, 13), "pixel-cat": (3, 8),
}
OBJECT_NAMES = (
    "pumpkin-cookies", "sheet-ghost", "iron-cauldron", "spirit-board",
    "ghost-candle", "blood-bottle", "dried-rose", "pumpkin-candies",
    "enamel-mug", "witch-hat", "jack-o-lantern", "frog", "wax-seal",
    "raven", "skull", "pumpkin-spice-candle", "moon", "pumpkin",
    "ghost-cocoa", "black-cat", "mushroom", "black-cauldron", "pumpkin-pair",
    "peppermint", "coffee-cup", "oak-leaf", "autumn-leaf", "candy-corn",
    "star", "halloween-mug", "cinnamon-roll", "dagger", "caramels",
    "witch-hazel", "heart-cookie", "pinecone", "sweet-bread",
    "pumpkin-pie-slice", "cat-latte", "ghost-cookie", "acorn", "muffin",
    "ice-cream", "pumpkin-pie",
)
PREFERRED = {
    "pumpkin-cookies": (1, 12), "sheet-ghost": (1, 1),
    "iron-cauldron": (1, 3), "spirit-board": (2, 10),
    "ghost-candle": (3, 11), "blood-bottle": (2, 3),
    "dried-rose": (1, 13), "pumpkin-candies": (1, 14),
    "enamel-mug": (1, 9), "witch-hat": (1, 8),
    "jack-o-lantern": (1, 2), "frog": (4, 0),
    "wax-seal": (2, 8), "raven": (2, 0), "skull": (4, 1),
    "pumpkin-spice-candle": (3, 2), "moon": (3, 10),
    "pumpkin": (2, 1), "ghost-cocoa": (4, 2),
    "black-cat": (1, 4), "mushroom": (2, 2),
    "black-cauldron": (2, 7), "pumpkin-pair": (3, 1),
    "coffee-cup": (3, 6), "oak-leaf": (3, 15),
    "autumn-leaf": (1, 6), "candy-corn": (4, 3),
    "star": (1, 0), "cinnamon-roll": (2, 12),
    "dagger": (1, 5), "pinecone": (3, 4),
    "pumpkin-pie-slice": (3, 14), "ghost-cookie": (2, 15),
    "acorn": (1, 10),
}

def cut_sheet(sheet, columns, rows):
    # The generated drawings do not follow perfectly rigid grid boundaries.
    # Find connected transparent cutouts across the whole sheet so neighboring
    # stickers never leave slivers in one another's files.
    small = sheet.copy()
    small.thumbnail((650, 650))
    alpha = small.getchannel("A").point(lambda value: 255 if value > 30 else 0)
    alpha = alpha.filter(ImageFilter.MaxFilter(3))
    width, height = alpha.size
    remaining = bytearray(alpha.tobytes())
    components = []
    for seed in range(width * height):
        if not remaining[seed]:
            continue
        remaining[seed] = 0
        queue = deque([seed])
        area = 0
        left, top, right, bottom = width, height, 0, 0
        while queue:
            point = queue.popleft()
            y, x = divmod(point, width)
            area += 1
            left, right = min(left, x), max(right, x)
            top, bottom = min(top, y), max(bottom, y)
            for neighbor in (point - 1 if x else -1,
                             point + 1 if x < width - 1 else -1,
                             point - width if y else -1,
                             point + width if y < height - 1 else -1):
                if neighbor >= 0 and remaining[neighbor]:
                    remaining[neighbor] = 0
                    queue.append(neighbor)
        if area > 100:
            components.append((left, top, right + 1, bottom + 1))
    if len(components) != columns * rows:
        raise ValueError(f"Expected {columns * rows} cutouts, found {len(components)}")
    output = {}
    for left, top, right, bottom in components:
        center_x, center_y = (left + right) / 2, (top + bottom) / 2
        col = min(columns - 1, int(center_x * columns / width))
        row = min(rows - 1, int(center_y * rows / height))
        bounds = (max(0, round(left * sheet.width / width) - 4),
                  max(0, round(top * sheet.height / height) - 4),
                  min(sheet.width, round(right * sheet.width / width) + 4),
                  min(sheet.height, round(bottom * sheet.height / height) + 4))
        key = row * columns + col
        if key in output:
            raise ValueError(f"Two cutouts occupy grid cell {key}")
        output[key] = ImageOps.expand(clean_cutout(sheet.crop(bounds)), border=6, fill=(0, 0, 0, 0))
    return output

def clean_cutout(image):
    """Keep the main drawing and discard tiny parts of adjacent grid items."""
    width, height = image.size
    alpha = image.getchannel("A")
    remaining = bytearray(alpha.point(lambda value: 255 if value > 30 else 0)
                          .filter(ImageFilter.MaxFilter(3)).tobytes())
    largest = []
    for seed in range(width * height):
        if not remaining[seed]:
            continue
        remaining[seed] = 0
        queue = deque([seed])
        pixels = []
        while queue:
            point = queue.popleft()
            pixels.append(point)
            y, x = divmod(point, width)
            for neighbor in (point - 1 if x else -1,
                             point + 1 if x < width - 1 else -1,
                             point - width if y else -1,
                             point + width if y < height - 1 else -1):
                if neighbor >= 0 and remaining[neighbor]:
                    remaining[neighbor] = 0
                    queue.append(neighbor)
        if len(pixels) > len(largest):
            largest = pixels
    mask = bytearray(width * height)
    for point in largest:
        mask[point] = 255
    mask_image = Image.frombytes("L", image.size, bytes(mask)).filter(ImageFilter.MaxFilter(5))
    image.putalpha(ImageChops.multiply(alpha, mask_image))
    return image

all_art = {}
for sheet_number, (name, columns, rows) in enumerate(SHEETS, 1):
    image = Image.open(SOURCE / name).convert("RGBA")
    for index, cutout in cut_sheet(image, columns, rows).items():
        all_art[(sheet_number, index)] = cutout

selected = dict(STATIC)
selected.update(PREFERRED)
if len(set(selected.values())) != len(selected):
    raise ValueError("Two output names refer to the same original illustration")
available = iter(key for key in all_art if key not in selected.values())
for name in OBJECT_NAMES:
    if name not in selected:
        selected[name] = next(available)
if len(selected) != 52 or set(selected.values()) != set(all_art):
    raise ValueError("Every original illustration must be packaged exactly once")

OBJECTS.mkdir(parents=True, exist_ok=True)
for name, artwork in selected.items():
    destination = STICKERS if name in STATIC else OBJECTS
    all_art[artwork].save(destination / f"{name}.png", optimize=True)
print(f"Saved {len(selected)} separate original stickers")
