#!/usr/bin/env python3
"""Make a short Spooky promo: open the app, enable Candy Cursor, use it."""

from __future__ import annotations

import math
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
MEDIA = ROOT / "docs" / "media"
VIDEO = MEDIA / "cursor-toggle-flow.mp4"
POSTER = MEDIA / "cursor-toggle-flow-poster.png"
BACKGROUND = MEDIA / "cursor-browser-background.png"
W, H, FPS, SECONDS = 1280, 720, 24, 10
PANEL_CROP = (78, 60, 1618, 1590)
PANEL_W, PANEL_H = 650, 645
PANEL_X, PANEL_Y = 315, 38
TOGGLE = (513, 515, 586, 550)  # Position within the cropped, scaled app image.
MENU_POINT = (1080, 19)
TOGGLE_POINT = (PANEL_X + 550, PANEL_Y + 533)
CLOSE_POINT = (PANEL_X + 582, PANEL_Y + 67)
FONT = "/System/Library/Fonts/SFNS.ttf"


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT, size)


def browser_background() -> Image.Image:
    """Draw an original, light Safari-style planner based on the supplied mood reference."""
    image = Image.new("RGBA", (W, H), "#eceef1")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, W, 36), fill="#f8f8f9")
    draw.text((24, 8), "●", font=font(17), fill="#20252a")
    draw.text((60, 8), "Safari    File    Edit    View    History    Bookmarks    Window    Help",
              font=font(16), fill="#2e343a")
    draw.text((1137, 8), "◉  12:28", font=font(15), fill="#5c6570")

    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle((54, 69, 1235, 699), radius=31,
                                             fill=(32, 40, 55, 70))
    image = Image.alpha_composite(image, shadow.filter(ImageFilter.GaussianBlur(24)))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((55, 60, 1225, 687), radius=29, fill="#f3f4f8",
                           outline="#d7dce5", width=2)
    draw.rounded_rectangle((55, 60, 1225, 137), radius=29, fill="#fafbfc")
    draw.rectangle((55, 103, 1225, 137), fill="#fafbfc")
    for x, color in ((87, "#ff5f57"), (112, "#ffbd2e"), (137, "#28c840")):
        draw.ellipse((x, 89, x + 16, 105), fill=color)
    draw.rounded_rectangle((190, 79, 262, 115), radius=15, fill="#ffffff", outline="#edf0f3")
    draw.text((211, 85), "‹  ›", font=font(22), fill="#8f99a4")
    draw.rounded_rectangle((405, 76, 866, 118), radius=20, fill="#ffffff", outline="#e8ebf0")
    draw.text((565, 88), "autumn.page", font=font(17), fill="#68727e")
    draw.text((1015, 85), "↓    ↑    +", font=font(24), fill="#64707d")
    draw.rounded_rectangle((1147, 86, 1175, 108), radius=5, outline="#64707d", width=2)

    draw.rounded_rectangle((70, 150, 345, 671), radius=23, fill="#edf1fb")
    draw.rounded_rectangle((355, 150, 862, 671), radius=23, fill="#ffffff")
    draw.rounded_rectangle((872, 150, 1210, 671), radius=23, fill="#faf8fb")

    # Library column.
    draw.text((91, 173), "Autumn Planner", font=font(24), fill="#222c38")
    draw.rounded_rectangle((90, 221, 325, 259), radius=19, fill="#dee5f1")
    draw.rounded_rectangle((93, 224, 207, 256), radius=16, fill="#ffffff")
    draw.text((128, 229), "Today", font=font(17), fill="#29333d")
    draw.text((244, 229), "All", font=font(17), fill="#788492")
    draw.text((93, 283), "OCTOBER", font=font(14), fill="#8994a1")
    rows = (("Morning notes", "09:00"), ("Design review", "10:00"),
            ("A little break", "12:30"), ("Moodboard", "14:00"),
            ("Share preview", "16:00"))
    for i, (name, time) in enumerate(rows):
        y = 324 + i * 58
        if i == 1:
            draw.rounded_rectangle((83, y - 8, 333, y + 39), radius=12, fill="#ffffff")
        draw.ellipse((96, y + 3, 116, y + 23), fill="#f6c9a8" if i == 1 else "#d8e0ed")
        draw.text((128, y), name, font=font(17), fill="#3a4652")
        draw.text((285, y + 2), time, font=font(13), fill="#9aa4af", anchor="ra")
    draw.text((93, 626), "A calmer day, one note at a time", font=font(14), fill="#9aa5b1")

    # Calendar column.
    draw.text((385, 176), "FRIDAY 16", font=font(15), fill="#d86857")
    draw.text((385, 205), "Make room for autumn", font=font(29), fill="#1f2731")
    draw.text((385, 244), "A simple plan for today", font=font(17), fill="#7c8793")
    for i, hour in enumerate(("09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00")):
        y = 301 + i * 50
        draw.line((445, y, 835, y), fill="#ebedf0", width=2)
        if hour != "12:00":
            draw.text((381, y - 9), hour, font=font(14), fill="#a1aab4")
    draw.rounded_rectangle((463, 346, 704, 441), radius=13, fill="#fff0e6",
                           outline="#f2bd99", width=2)
    draw.text((484, 365), "Design review", font=font(18), fill="#c45d2e")
    draw.text((484, 393), "10:00 - 11:30", font=font(15), fill="#a57261")
    draw.rounded_rectangle((612, 498, 818, 575), radius=12, fill="#f1f3f8")
    draw.text((630, 516), "Notes & ideas", font=font(17), fill="#526273")
    draw.text((630, 544), "A fresh perspective", font=font(14), fill="#91a0ad")
    draw.line((444, 467, 836, 467), fill="#f28b51", width=3)
    draw.rounded_rectangle((383, 450, 445, 483), radius=15, fill="#ef8249")
    draw.text((393, 457), "12:20", font=font(16), fill="#ffffff")

    # Context column.
    draw.text((897, 176), "TODAY", font=font(15), fill="#9b8e96")
    draw.text((897, 208), "Little moments", font=font(28), fill="#282a34")
    draw.text((897, 241), "make the season.", font=font(28), fill="#282a34")
    draw.text((897, 296), "A few good things to finish", font=font(17), fill="#7d8792")
    draw.line((897, 337, 1180, 337), fill="#e6e4e9", width=2)
    tasks = ("Polish the prototype", "Pick a soundtrack", "Share a preview")
    for i, task in enumerate(tasks):
        y = 363 + i * 65
        draw.ellipse((900, y, 922, y + 22), outline="#dd996f", width=2)
        if i == 0:
            draw.line((905, y + 11, 911, y + 16, 919, y + 6), fill="#d77c42", width=3)
        draw.text((936, y - 1), task, font=font(17), fill="#565d68")
        draw.line((897, y + 48, 1180, y + 48), fill="#e9e7eb", width=1)
    draw.rounded_rectangle((897, 582, 1183, 637), radius=15, fill="#fff4ec")
    draw.text((916, 597), "A little seasonal magic", font=font(17), fill="#ac633f")

    web = Image.open(ROOT / "macos" / "WebDecor" / "wide-web.png").convert("RGBA")
    web = web.resize((W, round(web.height * W / web.width)), Image.Resampling.LANCZOS)
    image.alpha_composite(web, (0, 0))
    image.save(BACKGROUND, optimize=True)
    return image


def ease(p: float) -> float:
    p = max(0.0, min(1.0, p))
    return p * p * (3 - 2 * p)


def phase(t: float, start: float, end: float) -> float:
    return ease((t - start) / (end - start))


def blend(a: float, b: float, p: float) -> float:
    return a + (b - a) * p


def mix_color(a: tuple[int, int, int], b: tuple[int, int, int], p: float) -> tuple[int, int, int]:
    return tuple(round(blend(x, y, p)) for x, y in zip(a, b))


def prepare_panel() -> Image.Image:
    source = Image.open(ROOT / "docs" / "mac-app-window.png").convert("RGBA")
    # Remove the screenshot's active switch. Its replacement animates below.
    draw = ImageDraw.Draw(source)
    for y in range(1276, 1371):
        draw.line((1288, y, 1473, y), fill=source.getpixel((1250, y)))
    panel = source.crop(PANEL_CROP).resize((PANEL_W, PANEL_H), Image.Resampling.LANCZOS)
    mask = Image.new("L", (PANEL_W, PANEL_H), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, PANEL_W - 1, PANEL_H - 1), radius=52, fill=255)
    panel.putalpha(mask)
    return panel


def draw_switch(panel: Image.Image, progress: float) -> Image.Image:
    panel = panel.copy()
    left, top, right, bottom = TOGGLE
    switch = Image.new("RGBA", (right - left + 1, bottom - top + 1), (0, 0, 0, 0))
    width, height = switch.size
    gradient = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    gradient_draw = ImageDraw.Draw(gradient)
    for y in range(height):
        f = y / max(1, height - 1)
        dark = (62 - round(34 * f),) * 3
        orange = (255 - round(19 * f), 156 - round(67 * f), 49 - round(43 * f))
        color = mix_color(dark, orange, progress)
        gradient_draw.line((0, y, width, y), fill=color)
    mask = Image.new("L", (width, height), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, width - 1, height - 1), radius=height // 2, fill=255)
    gradient.putalpha(mask)
    switch.alpha_composite(gradient)
    d = ImageDraw.Draw(switch)
    d.rounded_rectangle((0, 0, width - 1, height - 1), radius=height // 2,
                        outline=mix_color((80, 80, 80), (255, 183, 93), progress), width=1)
    knob = height - 6
    kx = round(blend(4, width - knob - 4, progress))
    d.ellipse((kx + 1, 5, kx + knob + 1, knob + 5), fill=(0, 0, 0, 95))
    d.ellipse((kx, 3, kx + knob, 3 + knob), fill="#f8f9fa", outline="#d5d8da", width=1)
    panel.alpha_composite(switch, (left, top))
    return panel


def panel_layer(panel: Image.Image, t: float) -> Image.Image:
    if t > 6.2:
        return Image.new("RGBA", (W, H), (0, 0, 0, 0))
    on = phase(t, 3.4, 3.92)
    current = draw_switch(panel, on)
    leaving = phase(t, 5.50, 6.2)
    size_factor = blend(1.0, 0.90, leaving)
    pw, ph = round(PANEL_W * size_factor), round(PANEL_H * size_factor)
    if (pw, ph) != (PANEL_W, PANEL_H):
        current = current.resize((pw, ph), Image.Resampling.LANCZOS)
    alpha = round(255 * (1 - leaving))
    if alpha != 255:
        current.putalpha(current.getchannel("A").point(lambda a: round(a * alpha / 255)))
    cx = PANEL_X + PANEL_W / 2
    cy = PANEL_Y + PANEL_H / 2
    cx = blend(cx, MENU_POINT[0], leaving)
    cy = blend(cy, MENU_POINT[1], leaving)
    x, y = round(cx - pw / 2), round(cy - ph / 2)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle((x + 10, y + 15, x + pw + 10, y + ph + 15),
                                              radius=round(52 * size_factor), fill=(13, 18, 23, round(85 * alpha / 255)))
    layer = Image.alpha_composite(layer, shadow.filter(ImageFilter.GaussianBlur(25)))
    layer.alpha_composite(current, (x, y))
    return layer


def arrow_at(t: float) -> tuple[float, float]:
    p = phase(t, 0.45, 3.0)
    return blend(610, TOGGLE_POINT[0], p), blend(300, TOGGLE_POINT[1], p)


def candy_at(t: float) -> tuple[float, float]:
    if t < 5.25:
        p = phase(t, 4.28, 5.25)
        return blend(TOGGLE_POINT[0], CLOSE_POINT[0], p), blend(TOGGLE_POINT[1], CLOSE_POINT[1], p)
    if t < 6.3:
        p = phase(t, 5.55, 6.3)
        return blend(CLOSE_POINT[0], 750, p), blend(CLOSE_POINT[1], 365, p)
    if t < 8.2:
        p = phase(t, 6.3, 8.2)
        return blend(750, 970, p), blend(365, 397, p) + 15 * math.sin(p * math.pi)
    p = phase(t, 8.2, 9.25)
    return blend(970, 827, p), blend(397, 350, p) + 5 * math.sin(t * 3)


def pointer(image: Image.Image, x: float, y: float, opacity: float) -> None:
    if opacity <= 0:
        return
    cursor = Image.new("RGBA", (42, 57), (0, 0, 0, 0))
    d = ImageDraw.Draw(cursor)
    points = [(2, 2), (2, 45), (13, 35), (22, 54), (31, 49), (22, 31), (38, 30)]
    d.polygon([(px + 2, py + 3) for px, py in points], fill=(0, 0, 0, 75))
    d.polygon(points, fill="white")
    d.line(points + [points[0]], fill="#121416", width=3, joint="curve")
    d.polygon([(6, 9), (6, 37), (14, 29), (24, 47), (26, 46), (17, 27), (31, 26)], fill="#151719")
    cursor.putalpha(cursor.getchannel("A").point(lambda a: round(a * opacity)))
    image.alpha_composite(cursor, (round(x), round(y)))


def candy_cursor(image: Image.Image, source: Image.Image, t: float) -> None:
    appear = phase(t, 4.02, 4.42)
    if appear <= 0:
        return
    x, y = candy_at(t)
    reveal = phase(t, 6.35, 7.15)
    size = round(blend(116, 290, reveal))
    sprite = source.resize((size, round(size * source.height / source.width)), Image.Resampling.NEAREST)
    # The supplied PNG is unchanged; only its size and position animate.
    px, py = round(x - sprite.width * 0.50), round(y - sprite.height * 0.50)
    if appear < 1:
        sprite.putalpha(sprite.getchannel("A").point(lambda a: round(a * appear)))
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shadow.alpha_composite(sprite, (px + 8, py + 13))
    shadow.putalpha(shadow.getchannel("A").point(lambda a: round(a * 0.25)))
    image.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(13)))
    image.alpha_composite(sprite, (px, py))


def camera(image: Image.Image, t: float) -> Image.Image:
    focus = phase(t, 2.08, 3.08) * (1 - phase(t, 4.38, 5.25))
    zoom = 1 + 0.52 * focus
    cx = blend(W / 2, 810, focus)
    cy = blend(H / 2, 470, focus)
    cw, ch = W / zoom, H / zoom
    return image.crop((round(cx - cw / 2), round(cy - ch / 2),
                       round(cx + cw / 2), round(cy + ch / 2))).resize((W, H), Image.Resampling.BICUBIC)


def click_ring(image: Image.Image, x: float, y: float, t: float, at: float) -> None:
    p = (t - at) / 0.48
    if 0 <= p <= 1:
        draw = ImageDraw.Draw(image)
        radius = 9 + 22 * ease(p)
        alpha = round(140 * (1 - p))
        draw.ellipse((x - radius, y - radius, x + radius, y + radius),
                     outline=(255, 126, 29, alpha), width=3)


def make_frame(t: float, background: Image.Image, panel: Image.Image,
               candy: Image.Image, pumpkin: Image.Image) -> Image.Image:
    frame = background.copy()
    frame.alpha_composite(pumpkin, (1066, 5))
    frame = Image.alpha_composite(frame, panel_layer(panel, t))

    if t < 4.42:
        x, y = arrow_at(t)
        pointer(frame, x, y, 1 - phase(t, 4.02, 4.42))
    if t >= 4.02:
        candy_cursor(frame, candy, t)
    frame = camera(frame, t)

    # A quiet pulse marks each actual click, without adding UI to the app.
    if 3.4 <= t < 3.88:
        focus = phase(t, 2.08, 3.08)
        zx = (TOGGLE_POINT[0] - blend(W/2, 810, focus)) * (1 + .52*focus) + W/2
        zy = (TOGGLE_POINT[1] - blend(H/2, 470, focus)) * (1 + .52*focus) + H/2
        click_ring(frame, zx, zy, t, 3.4)
    return frame.convert("RGB")


def main() -> None:
    MEDIA.mkdir(parents=True, exist_ok=True)
    background = browser_background()
    panel = prepare_panel()
    candy = Image.open(ROOT / "macos" / "CandyCursor.png").convert("RGBA")
    pumpkin = Image.open(ROOT / "macos" / "Stickers" / "Objects" / "jack-o-lantern.png").convert("RGBA")
    pumpkin = pumpkin.resize((28, 29), Image.Resampling.LANCZOS)

    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-vcodec", "rawvideo",
           "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-an",
           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
           "-movflags", "+faststart", str(VIDEO)]
    encoder = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    assert encoder.stdin is not None
    try:
        for i in range(FPS * SECONDS):
            frame = make_frame(i / FPS, background, panel, candy, pumpkin)
            if i == 0:
                frame.save(POSTER, optimize=True)
            encoder.stdin.write(frame.tobytes())
    finally:
        encoder.stdin.close()
    if encoder.wait() != 0:
        raise RuntimeError("Could not encode cursor toggle video")
    print(VIDEO)
    print(POSTER)


if __name__ == "__main__":
    main()
