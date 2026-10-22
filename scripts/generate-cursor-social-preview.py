#!/usr/bin/env python3
"""Render a social video showing Spooky's candy cursor over a quiet Mac desktop."""

from pathlib import Path
import math
import subprocess

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "media"
OUT.mkdir(parents=True, exist_ok=True)
VIDEO = OUT / "cursor-social.mp4"
POSTER = OUT / "cursor-social-poster.png"
W, H, FPS, SECONDS = 1200, 675, 24, 9
FONT = "/System/Library/Fonts/SFNS.ttf"
CANDY = Image.open(ROOT / "macos" / "CandyCursor.png").convert("RGBA")
FOLDER = Image.open(ROOT / "macos" / "PreviewScene" / "folder.png").convert("RGBA")
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
    dock = Image.new("RGBA", (430, 64))
    ImageDraw.Draw(dock).rounded_rectangle((0, 0, 429, 63), radius=20,
                                           fill=(255, 255, 255, 118), outline=(255, 255, 255, 185), width=2)
    image.alpha_composite(dock, (385, 594))
    for i, icon in enumerate(DOCK_ICONS):
        image.alpha_composite(icon.resize((44, 44), Image.Resampling.LANCZOS), (425 + i*75, 603))
    return image


BASE = desktop()
KEYFRAMES = ((0.0, -120, 490), (0.9, 280, 353), (2.2, 600, 264),
             (3.5, 810, 351), (4.8, 475, 434), (6.1, 760, 278),
             (7.4, 515, 364), (8.25, 780, 400), (9.0, 1310, 520))


def location(t):
    for i in range(len(KEYFRAMES)-1):
        a, b = KEYFRAMES[i], KEYFRAMES[i+1]
        if t <= b[0]:
            p = ease((t-a[0]) / (b[0]-a[0]))
            return a[1] + (b[1]-a[1])*p, a[2] + (b[2]-a[2])*p
    return KEYFRAMES[-1][1:]


def finder_window(selected):
    image = Image.new("RGBA", (W, H))
    shadow = Image.new("RGBA", (W, H))
    ImageDraw.Draw(shadow).rounded_rectangle((162, 120, 1038, 556), radius=25, fill=(25, 31, 39, 72))
    image = Image.alpha_composite(image, shadow.filter(ImageFilter.GaussianBlur(22)))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((170, 105, 1030, 539), radius=22, fill="#fcfcfd", outline="#cdd1d5", width=2)
    draw.rounded_rectangle((170, 105, 1030, 167), radius=22, fill="#f4f5f6")
    draw.rectangle((170, 145, 1030, 167), fill="#f4f5f6")
    for x, color in ((198, "#ff5f57"), (223, "#febc2e"), (248, "#28c840")):
        draw.ellipse((x, 128, x+14, 142), fill=color, outline=(120, 120, 120, 60))
    draw.text((497, 124), "Documents", font=font(20), fill="#4d5359")
    draw.rounded_rectangle((765, 119, 1004, 150), radius=9, fill="#ffffff", outline="#d9dcdf")
    draw.text((789, 124), "Search", font=font(16), fill="#a5a9ad")
    draw.rectangle((170, 167, 363, 539), fill="#e8ecf0")
    draw.line((363, 168, 363, 539), fill="#d3d8dc", width=2)
    draw.text((193, 191), "FAVORITES", font=font(13), fill="#8a949c")
    for j, name in enumerate(("Recents", "Applications", "Desktop", "Documents", "Downloads")):
        y = 229 + j*52
        if name == "Documents":
            draw.rounded_rectangle((180, y-6, 352, y+37), radius=8, fill="#d2dce5")
        icon = "#6f8aa3"
        if j == 0:
            draw.ellipse((201, y+3, 221, y+23), outline=icon, width=2)
            draw.line((211, y+7, 211, y+13, 216, y+16), fill=icon, width=2)
        elif j == 1:
            for row in range(3):
                for col in range(3):
                    draw.rounded_rectangle((202+col*7, y+4+row*7, 207+col*7, y+9+row*7), radius=1, fill=icon)
        elif j == 2:
            draw.rounded_rectangle((200, y+4, 222, y+20), radius=2, outline=icon, width=2)
            draw.line((207, y+24, 215, y+24), fill=icon, width=2)
        elif j == 3:
            draw.rounded_rectangle((204, y+3, 220, y+25), radius=2, outline=icon, width=2)
            draw.line((207, y+10, 217, y+10), fill=icon, width=2)
        else:
            draw.line((211, y+3, 211, y+19), fill=icon, width=2)
            draw.line((205, y+14, 211, y+20, 217, y+14), fill=icon, width=2)
            draw.line((202, y+25, 220, y+25), fill=icon, width=2)
        draw.text((230, y+2), name, font=font(17), fill="#4d5962")
    draw.text((392, 185), "Name", font=font(14), fill="#919aa0")
    draw.text((833, 185), "Date Modified", font=font(14), fill="#919aa0")
    rows = ("Autumn photos", "Halloween ideas", "Projects", "Weekend plans")
    folder_icon = FOLDER.resize((30, 28), Image.Resampling.LANCZOS)
    for j, name in enumerate(rows):
        y = 219+j*72
        if j == selected:
            draw.rounded_rectangle((378, y-5, 1013, y+57), radius=10, fill="#e4edf8")
        elif j % 2 == 0:
            draw.rounded_rectangle((378, y-5, 1013, y+57), radius=10, fill="#f6f7f8")
        image.alpha_composite(folder_icon, (396, y+7))
        draw.text((443, y+9), name, font=font(19), fill="#39444d")
        draw.text((851, y+11), "Today", font=font(16), fill="#929ba2")
    return image


def frame(t):
    image = BASE.copy()
    selected = -1
    for j, (start, end) in enumerate(((1.5, 2.75), (2.95, 4.1), (4.35, 5.4), (6.3, 7.35))):
        if start <= t < end:
            selected = j
    image.alpha_composite(finder_window(selected))
    x, y = location(t)
    angle = 6 * math.sin(t*2.8)
    size = 150 + round(8*math.sin(t*2.4))
    candy = CANDY.resize((size, round(size*CANDY.height/CANDY.width)), Image.Resampling.NEAREST)
    candy = candy.rotate(angle, Image.Resampling.NEAREST, expand=True)
    px, py = round(x-candy.width/2), round(y-candy.height/2)
    if -candy.width < px < W and -candy.height < py < H:
        shadow = Image.new("RGBA", (W, H))
        shadow.alpha_composite(candy, (px+8, py+13))
        shadow.putalpha(shadow.getchannel("A").point(lambda a: round(a*.27)))
        image = Image.alpha_composite(image, shadow.filter(ImageFilter.GaussianBlur(12)))
        image.alpha_composite(candy, (px, py))
    return image.convert("RGB")


def main():
    command = ["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
               "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-an", "-vf", "scale=1280:720:flags=lanczos",
               "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
               "-movflags", "+faststart", str(VIDEO)]
    with subprocess.Popen(command, stdin=subprocess.PIPE) as encoder:
        for i in range(FPS*SECONDS):
            encoder.stdin.write(frame(i/FPS).tobytes())
    if encoder.returncode != 0:
        raise RuntimeError("Could not encode cursor preview")
    frame(3.4).resize((1280, 720), Image.Resampling.LANCZOS).save(POSTER, optimize=True)
    print(VIDEO)
    print(POSTER)


if __name__ == "__main__":
    main()
