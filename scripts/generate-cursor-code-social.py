#!/usr/bin/env python3
"""Render a short social clip featuring Spooky's exact candy cursor asset."""

from __future__ import annotations

import math
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
MEDIA = ROOT / "docs" / "media"
BACKGROUND = MEDIA / "cursor-code-background.png"
CURSOR = ROOT / "macos" / "CandyCursor.png"
VIDEO = MEDIA / "cursor-code-social.mp4"
POSTER = MEDIA / "cursor-code-social-poster.png"

WIDTH, HEIGHT = 1280, 720
FPS, SECONDS = 24, 8
FRAMES = FPS * SECONDS


def ease(value: float) -> float:
    value = max(0.0, min(1.0, value))
    return value * value * (3 - 2 * value)


def tween(t: float, start: float, end: float) -> float:
    return ease((t - start) / (end - start))


def camera(image: Image.Image, t: float) -> Image.Image:
    # A small push into the editor keeps the interface legible and the motion calm.
    drift = math.sin(math.pi * t / SECONDS)
    zoom = 1.0 + 0.024 * drift
    crop_width = WIDTH / zoom
    crop_height = HEIGHT / zoom
    cx = WIDTH / 2 + 13 * drift
    cy = HEIGHT / 2 - 6 * drift
    return image.crop((
        round(cx - crop_width / 2), round(cy - crop_height / 2),
        round(cx + crop_width / 2), round(cy + crop_height / 2),
    )).resize((WIDTH, HEIGHT), Image.Resampling.BICUBIC)


def position(t: float) -> tuple[int, int]:
    if t < 1.7:
        p = tween(t, 0.35, 1.7)
        x = 1360 + (790 - 1360) * p
        y = 166 + (188 - 166) * p
    elif t < 3.1:
        x = 790 + 9 * math.sin((t - 1.7) * 2.2)
        y = 188 + 6 * math.sin((t - 1.7) * 3.2)
    elif t < 5.1:
        p = tween(t, 3.1, 5.1)
        x = 790 - 115 * p
        y = 188 + 102 * p
    else:
        p = tween(t, 5.1, 6.75)
        x = 675 + 97 * p
        y = 290 - 82 * p
        x += 5 * math.sin((t - 5.1) * 2.8)
        y += 4 * math.sin((t - 5.1) * 3.4)
    return round(x), round(y)


def make_frame(base: Image.Image, candy: Image.Image, shadow: Image.Image, t: float) -> Image.Image:
    frame = base.copy()
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # A brief line highlight follows the cursor, like a real editor hover.
    glow = round(24 * tween(t, 0.75, 1.5) * (1 - tween(t, 6.8, 7.7)))
    if glow:
        draw.rounded_rectangle((369, 208, 1204, 234), radius=4, fill=(239, 121, 43, glow))
        draw.rectangle((369, 208, 372, 234), fill=(239, 121, 43, min(160, glow * 5)))
    frame = Image.alpha_composite(frame, overlay)
    frame = camera(frame, t)

    x, y = position(t)
    if x < WIDTH and x + candy.width > 0:
        # Shadow is a separate layer; the candy artwork itself remains unaltered.
        visibility = 1 - tween(t, 7.1, 7.95)
        if visibility > 0:
            if visibility == 1:
                frame.alpha_composite(shadow, (x + 10, y + 13))
                frame.alpha_composite(candy, (x, y))
            else:
                faded_shadow = shadow.copy()
                faded_shadow.putalpha(shadow.getchannel("A").point(lambda a: round(a * visibility)))
                faded_candy = candy.copy()
                faded_candy.putalpha(candy.getchannel("A").point(lambda a: round(a * visibility)))
                frame.alpha_composite(faded_shadow, (x + 10, y + 13))
                frame.alpha_composite(faded_candy, (x, y))

    # One restrained click pulse makes the cursor's action clear in motion.
    pulse = (t - 3.0) / 0.7
    if 0 <= pulse <= 1:
        ring = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        ring_draw = ImageDraw.Draw(ring)
        radius = 18 + 38 * ease(pulse)
        px, py = x + 49, y + 229
        ring_draw.ellipse((px-radius, py-radius, px+radius, py+radius),
                          outline=(239, 121, 43, round(175 * (1-pulse))), width=3)
        frame = Image.alpha_composite(frame, ring)
    return frame.convert("RGB")


def main() -> None:
    if not BACKGROUND.exists():
        subprocess.run(["python3", str(ROOT / "scripts" / "generate-cursor-code-hero.py")], check=True)
    base = Image.open(BACKGROUND).convert("RGBA").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    # Nearest-neighbor retains the original pixel artwork at social-video size.
    candy = Image.open(CURSOR).convert("RGBA").resize((440, 461), Image.Resampling.NEAREST)
    shadow = Image.new("RGBA", (candy.width + 48, candy.height + 48), (0, 0, 0, 0))
    shadow.alpha_composite(candy, (15, 15))
    shadow.putalpha(shadow.getchannel("A").point(lambda alpha: round(alpha * 0.28)))
    shadow = shadow.filter(ImageFilter.GaussianBlur(15))

    command = [
        "ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-vcodec", "rawvideo",
        "-pix_fmt", "rgb24", "-s", f"{WIDTH}x{HEIGHT}", "-r", str(FPS), "-i", "-",
        "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(VIDEO),
    ]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    assert process.stdin is not None
    try:
        for index in range(FRAMES):
            frame = make_frame(base, candy, shadow, index / FPS)
            if index == 112:
                frame.save(POSTER, optimize=True)
            process.stdin.write(frame.tobytes())
    finally:
        process.stdin.close()
    if process.wait() != 0:
        raise RuntimeError("ffmpeg could not encode the social clip")
    print(VIDEO)
    print(POSTER)


if __name__ == "__main__":
    main()
