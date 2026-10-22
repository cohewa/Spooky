#!/usr/bin/env python3
"""Render Spooky's original spiders descending over a minimal macOS desktop."""

from pathlib import Path
import math
import subprocess

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "media"
OUT.mkdir(parents=True, exist_ok=True)
VIDEO = OUT / "web-social.mp4"
POSTER = OUT / "web-social-poster.png"
W, H, FPS, SECONDS = 1200, 675, 24, 9
FONT = "/System/Library/Fonts/SFNS.ttf"
WEB_SOURCE = Image.open(ROOT / "macos" / "WebDecor" / "center-web.png").convert("RGBA")
SPIDER_SOURCE = Image.open(ROOT / "macos" / "WebDecor" / "spider.png").convert("RGBA")
SPIDER_LAYOUT = ((185, 193, 34, 180), (619, 326, 42, 210),
                 (1035, 422, 48, 192), (1518, 258, 39, 172))
SCALE = W / WEB_SOURCE.width
# Remove the baked-in spiders so their original silhouettes can descend separately.
web_without_spiders = WEB_SOURCE.copy()
erasure = ImageDraw.Draw(web_without_spiders)
SPIDERS = []
for cx, drop, radius, fringe in SPIDER_LAYOUT:
    native_scale = radius / 42
    width = round(SPIDER_SOURCE.width * native_scale)
    height = round(SPIDER_SOURCE.height * native_scale)
    erasure.rectangle((cx - 5, fringe, cx + 5, drop + height + 5), fill=(0, 0, 0, 0))
    erasure.rectangle((cx - width/2 - 5, drop - 2, cx + width/2 + 5, drop + height + 5), fill=(0, 0, 0, 0))
    SPIDERS.append((round(cx*SCALE), round(drop*SCALE), round(fringe*SCALE),
                    SPIDER_SOURCE.resize((round(width*SCALE), round(height*SCALE)), Image.Resampling.LANCZOS)))
WEB = web_without_spiders.resize((W, round(W * WEB_SOURCE.height / WEB_SOURCE.width)), Image.Resampling.LANCZOS)
DOCK_ICONS = [Image.open(ROOT / "macos" / "PreviewScene" / f"{name}.png").convert("RGBA")
              for name in ("finder", "safari", "calendar", "notes", "settings")]


def font(size):
    return ImageFont.truetype(FONT, size)


def ease(value):
    value = max(0.0, min(1.0, value))
    return value * value * (3 - 2 * value)


def desktop():
    image = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(image)
    for y in range(H):
        p = y / H
        draw.line((0, y, W, y), fill=(int(232 - 21*p), int(234 - 20*p), int(235 - 18*p)))
    haze = Image.new("RGBA", (W, H))
    hd = ImageDraw.Draw(haze)
    hd.ellipse((-180, 70, 660, 840), fill=(255, 255, 255, 84))
    hd.ellipse((660, -280, 1540, 450), fill=(248, 237, 226, 75))
    image = Image.alpha_composite(image.convert("RGBA"), haze.filter(ImageFilter.GaussianBlur(85)))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, W, 37), fill=(255, 255, 255, 145))
    draw.text((28, 9), "●", font=font(15), fill="#202124")
    draw.text((64, 9), "Finder    File    Edit    View    Go    Window    Help", font=font(16), fill="#22252a")
    draw.text((1030, 9), "◉   9:41", font=font(15), fill="#3f4549")

    shadow = Image.new("RGBA", (W, H))
    sd = ImageDraw.Draw(shadow)
    for box in ((167, 184, 581, 479), (618, 184, 1033, 479)):
        sd.rounded_rectangle((box[0], box[1]+10, box[2], box[3]+10), radius=25, fill=(48, 54, 57, 39))
    image = Image.alpha_composite(image, shadow.filter(ImageFilter.GaussianBlur(20)))
    widgets = Image.new("RGBA", (W, H))
    wd = ImageDraw.Draw(widgets)
    wd.rounded_rectangle((170, 184, 580, 475), radius=25, fill=(250, 251, 250, 234), outline=(255, 255, 255, 250), width=2)
    wd.rounded_rectangle((620, 184, 1030, 475), radius=25, fill=(250, 249, 246, 234), outline=(255, 255, 255, 250), width=2)
    wd.text((200, 212), "56", font=font(63), fill="#283237")
    wd.text((201, 286), "Reminders", font=font(27), fill="#455259")
    wd.line((201, 333, 548, 333), fill="#cdd4d4", width=2)
    for j, label in enumerate(("Pick up pumpkins", "Plan a cozy weekend")):
        y = 354 + j * 48
        wd.ellipse((203, y+3, 222, y+22), outline="#a1aeb2", width=2)
        wd.text((237, y), label, font=font(20), fill="#566268")
    wd.text((650, 214), "WEDNESDAY", font=font(18), fill="#b16c53")
    wd.text((649, 244), "14", font=font(71), fill="#3f4141")
    wd.text((728, 292), "October", font=font(24), fill="#666565")
    wd.line((650, 348, 999, 348), fill="#d3d3d0", width=2)
    wd.text((650, 368), "Today", font=font(20), fill="#787b7b")
    image = Image.alpha_composite(image, widgets)
    dock = Image.new("RGBA", (430, 64))
    ImageDraw.Draw(dock).rounded_rectangle((0, 0, 429, 63), radius=20,
                                           fill=(255, 255, 255, 118), outline=(255, 255, 255, 185), width=2)
    image.alpha_composite(dock, (385, 594))
    for i, icon in enumerate(DOCK_ICONS):
        image.alpha_composite(icon.resize((44, 44), Image.Resampling.LANCZOS), (425 + i*75, 603))
    return image


BASE = desktop()


def frame(t):
    image = BASE.copy()
    closing = 1 - ease((t - 8.10) / 0.72)
    sweep = ease((t - 0.25) / 1.95)
    if sweep and closing:
        width = max(1, round(W * sweep))
        revealed = WEB.crop((0, 0, width, WEB.height))
        if closing < 1:
            revealed.putalpha(revealed.getchannel("A").point(lambda value: round(value * closing)))
        image.alpha_composite(revealed, (0, 0))
    for index, (cx, drop, fringe, sprite) in enumerate(SPIDERS):
        start = 0.85 + index * 0.46
        descent = ease((t - start) / 1.0)
        if descent <= 0 or closing <= 0:
            continue
        bob = math.sin((t - start - 1) * 3.1 + index) * 6 * descent
        sway = math.sin((t - start) * 2.5 + index) * 5 * descent
        x = round(cx + sway)
        y = round(fringe + (drop - fringe) * descent + bob)
        hanging = Image.new("RGBA", (W, H))
        ImageDraw.Draw(hanging).line((cx, fringe, x, y), fill=(12, 11, 12, 255), width=2)
        hanging.alpha_composite(sprite, (round(x - sprite.width/2), y))
        if closing < 1:
            hanging.putalpha(hanging.getchannel("A").point(lambda value: round(value * closing)))
        image.alpha_composite(hanging)
    return image.convert("RGB")


def main():
    command = ["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
               "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-an",
               "-vf", "scale=1280:720:flags=lanczos", "-c:v", "libx264", "-preset", "medium",
               "-crf", "19", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(VIDEO)]
    with subprocess.Popen(command, stdin=subprocess.PIPE) as encoder:
        for index in range(FPS * SECONDS):
            encoder.stdin.write(frame(index / FPS).tobytes())
    if encoder.returncode != 0:
        raise RuntimeError("Could not encode web preview")
    frame(4.5).resize((1280, 720), Image.Resampling.LANCZOS).save(POSTER, optimize=True)
    print(VIDEO)
    print(POSTER)


if __name__ == "__main__":
    main()
