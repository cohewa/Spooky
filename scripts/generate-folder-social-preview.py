#!/usr/bin/env python3
"""Render a short, quiet macOS desktop preview of the six folder styles."""

from functools import lru_cache
from pathlib import Path
import math
import subprocess

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "media"
OUT.mkdir(parents=True, exist_ok=True)
VIDEO = OUT / "folders-social.mp4"
POSTER = OUT / "folders-social-poster.png"
W, H, FPS, SECONDS = 1200, 675, 24, 9
FONT = "/System/Library/Fonts/SFNS.ttf"
NAMES = ("Maple", "Pumpkin", "Knit", "Stripes", "Bat", "Kitten")
ICONS = [Image.open(ROOT / "macos" / "FolderStyles" / f"{name.lower()}.png").convert("RGBA") for name in NAMES]
DOCK_ICONS = [Image.open(ROOT / "macos" / "PreviewScene" / f"{name}.png").convert("RGBA")
              for name in ("finder", "safari", "calendar", "notes", "settings")]
POSITIONS = [(300, 196), (600, 196), (900, 196), (300, 419), (600, 419), (900, 419)]


@lru_cache
def font(size, bold=False):
    return ImageFont.truetype(FONT, size)


def ease(value):
    value = max(0.0, min(1.0, value))
    return 1 - (1 - value) ** 3


def background():
    image = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(image)
    for y in range(H):
        p = y / H
        draw.line((0, y, W, y), fill=(int(232 - 21*p), int(234 - 20*p), int(235 - 18*p)))
    haze = Image.new("RGBA", (W, H))
    hd = ImageDraw.Draw(haze)
    hd.ellipse((-180, 70, 660, 840), fill=(255, 255, 255, 84))
    hd.ellipse((660, -280, 1540, 450), fill=(248, 237, 226, 75))
    haze = haze.filter(ImageFilter.GaussianBlur(85))
    image = Image.alpha_composite(image.convert("RGBA"), haze)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, W, 37), fill=(255, 255, 255, 145))
    draw.text((28, 9), "●", font=font(15), fill="#202124")
    draw.text((64, 9), "Finder    File    Edit    View    Go    Window    Help", font=font(16), fill="#22252a")
    draw.text((1030, 9), "◉   9:41", font=font(15), fill="#3f4549")
    dock = Image.new("RGBA", (430, 64))
    ImageDraw.Draw(dock).rounded_rectangle((0, 0, 429, 63), radius=20,
                                           fill=(255, 255, 255, 118), outline=(255, 255, 255, 185), width=2)
    image.alpha_composite(dock, (385, 594))
    for i, icon in enumerate(DOCK_ICONS):
        small = icon.resize((44, 44), Image.Resampling.LANCZOS)
        image.alpha_composite(small, (425 + i*75, 603))
    return image


BASE = background()


def cursor(draw, x, y):
    shape = [(x, y), (x, y+27), (x+7, y+21), (x+13, y+32),
             (x+18, y+29), (x+12, y+18), (x+23, y+18)]
    draw.polygon(shape, fill="#ffffff")
    draw.line(shape + [shape[0]], fill="#1d2024", width=2, joint="curve")


def frame(t):
    image = BASE.copy()
    selected = -1
    if 3.55 <= t < 7.95:
        selected = min(5, int((t - 3.55) / 0.72))
    for i, (name, asset, (cx, cy)) in enumerate(zip(NAMES, ICONS, POSITIONS)):
        visible = ease((t - 0.35 - i*0.40) / 0.48)
        if visible <= 0:
            continue
        pulse = 0.045 * math.sin(math.pi * min(1, (t - 3.55 - i*0.72) / 0.72)) if selected == i else 0
        size = round(151 * (0.76 + 0.24*visible + pulse))
        tile = asset.resize((size, size), Image.Resampling.LANCZOS)
        tile.putalpha(tile.getchannel("A").point(lambda a: round(a * visible)))
        y = round(cy + 15*(1-visible))
        image.alpha_composite(tile, (round(cx-size/2), round(y-size/2)))
        label = Image.new("RGBA", (180, 32))
        ld = ImageDraw.Draw(label)
        if selected == i:
            box = ld.textbbox((0, 0), name, font=font(20))
            width = box[2] - box[0] + 25
            ld.rounded_rectangle(((180-width)/2, 0, (180+width)/2, 30), radius=7, fill=(44, 107, 215, 236))
        ld.text((90, 15), name, anchor="mm", font=font(20),
                fill=(255, 255, 255, round(255*visible)) if selected == i else (36, 40, 44, round(255*visible)))
        image.alpha_composite(label, (cx-90, cy+79))
    if selected >= 0:
        cx, cy = POSITIONS[selected]
        draw = ImageDraw.Draw(image)
        cursor(draw, cx+43, cy+44)
    return image.convert("RGB")


def main():
    command = ["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
               "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-an", "-vf", "scale=1280:720:flags=lanczos", "-c:v", "libx264",
               "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(VIDEO)]
    with subprocess.Popen(command, stdin=subprocess.PIPE) as encoder:
        for index in range(FPS * SECONDS):
            encoder.stdin.write(frame(index / FPS).tobytes())
    if encoder.returncode != 0:
        raise RuntimeError("Could not encode folder preview")
    frame(6.8).resize((1280, 720), Image.Resampling.LANCZOS).save(POSTER, optimize=True)
    print(VIDEO)
    print(POSTER)


if __name__ == "__main__":
    main()
