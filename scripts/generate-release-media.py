#!/usr/bin/env python3
"""Create public-facing Spooky artwork from the app window and feature videos."""
from io import BytesIO
from pathlib import Path
import subprocess

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/media"
OUT.mkdir(parents=True, exist_ok=True)
FONT = ROOT / "macos/Fonts/AnonymousPro-Regular.ttf"
BOLD = ROOT / "macos/Fonts/AnonymousPro-Bold.ttf"
SCREENSHOT = ROOT / "docs/mac-app-window.png"
FEATURES = [
    ("webs", "Spider Web", "A web across the top of your screen"),
    ("stickers", "Desktop Stickers", "Move Halloween stickers around your Desktop"),
    ("folders", "Autumn Folder Icons", "Six illustrated styles for Desktop folders"),
    ("wallpaper", "Pumpkin Wallpaper", "A pumpkin field with decorated widgets"),
    ("cursor", "Candy Cursor", "A candy that follows your pointer"),
]
ORANGE = "#ff790e"
BG = "#101112"


def font(size, bold=False):
    return ImageFont.truetype(str(BOLD if bold else FONT), size)


def frame(name, second=1):
    data = subprocess.check_output([
        "ffmpeg", "-loglevel", "error", "-ss", str(second), "-i",
        str(ROOT / "macos/Previews" / f"{name}.mp4"), "-frames:v", "1",
        "-f", "image2pipe", "-vcodec", "png", "-",
    ])
    return Image.open(BytesIO(data)).convert("RGB")


def background(size):
    image = Image.new("RGB", size, BG)
    glow = Image.new("RGBA", size)
    draw = ImageDraw.Draw(glow)
    w, h = size
    draw.ellipse((w*.52, -h*.25, w*1.15, h*.72), fill=(255, 96, 14, 62))
    draw.ellipse((-w*.25, h*.61, w*.38, h*1.3), fill=(169, 55, 19, 42))
    image.paste(glow.filter(ImageFilter.GaussianBlur(90)), (0, 0), glow.filter(ImageFilter.GaussianBlur(90)))
    return image


def outlined_card(image, box, radius=24):
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle(box, radius=radius, fill="#191b1c", outline="#424344", width=2)


def make_cover():
    image = background((1600, 900))
    draw = ImageDraw.Draw(image)
    icon = Image.open(ROOT / "macos/HalloweenDecorIcon.png").convert("RGBA")
    icon = ImageOps.contain(icon, (105, 105))
    image.paste(icon, (112, 118), icon)
    draw.text((112, 270), "Spooky", font=font(104, True), fill="#ffffff")
    draw.text((116, 399), "A little Halloween", font=font(42), fill="#f5f2eb")
    draw.text((116, 449), "for your Mac.", font=font(42), fill="#f5f2eb")
    draw.rounded_rectangle((114, 565, 505, 620), radius=27, fill=ORANGE)
    draw.text((139, 575), "5 desktop effects", font=font(31, True), fill="#19110b")
    screenshot = Image.open(SCREENSHOT).convert("RGBA")
    screenshot = ImageOps.contain(screenshot, (765, 796))
    shadow = Image.new("RGBA", image.size)
    shadow.paste(Image.new("RGBA", screenshot.size, (0, 0, 0, 130)), (805, 60))
    image.paste(shadow.filter(ImageFilter.GaussianBlur(32)), (0, 0), shadow.filter(ImageFilter.GaussianBlur(32)))
    image.paste(screenshot, (800, 50), screenshot)
    image.save(OUT / "cover.png", optimize=True)


def make_feature_images():
    for name, title, detail in FEATURES:
        image = background((1280, 720))
        draw = ImageDraw.Draw(image)
        draw.text((66, 52), title, font=font(58, True), fill="#ffffff")
        draw.text((68, 122), detail, font=font(27), fill="#a6a6a6")
        outlined_card(image, (60, 203, 1220, 639), 28)
        preview = ImageOps.fit(frame(name), (1120, 420), Image.Resampling.LANCZOS)
        image.paste(preview, (80, 211))
        image.save(OUT / f"{name}.png", optimize=True)


def make_gallery():
    image = background((1600, 1000))
    draw = ImageDraw.Draw(image)
    draw.text((76, 50), "Five ways to make your Mac Spooky", font=font(58, True), fill="#ffffff")
    for index, (name, title, _) in enumerate(FEATURES):
        column, row = index % 2, index // 2
        x, y = 75 + column*735, 162 + row*267
        outlined_card(image, (x, y, x+705, y+230), 19)
        preview = ImageOps.fit(frame(name), (675, 185), Image.Resampling.LANCZOS)
        image.paste(preview, (x+15, y+13))
        draw.text((x+19, y+202), title, font=font(22, True), fill="#f6f6f4")
    x, y = 75 + 735, 162 + 2*267
    outlined_card(image, (x, y, x+705, y+230), 19)
    screenshot = Image.open(SCREENSHOT).convert("RGBA")
    screenshot = ImageOps.fit(screenshot, (250, 190), Image.Resampling.LANCZOS)
    image.paste(screenshot, (x+24, y+20), screenshot)
    draw.text((x+296, y+50), "Make it yours", font=font(31, True), fill="#ffffff")
    draw.text((x+297, y+103), "Turn each effect on", font=font(23), fill="#b8b8b8")
    draw.text((x+297, y+135), "or off in one place.", font=font(23), fill="#b8b8b8")
    image.save(OUT / "gallery.png", optimize=True)


def video_base(title, detail):
    image = background((960, 540))
    draw = ImageDraw.Draw(image)
    draw.text((56, 42), title, font=font(48, True), fill="#ffffff")
    draw.text((58, 99), detail, font=font(24), fill="#a6a6a6")
    outlined_card(image, (48, 153, 912, 490), 20)
    return image


def read_frame(stream, size):
    chunks = []
    remaining = size
    while remaining:
        chunk = stream.read(remaining)
        if not chunk:
            break
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def make_overview():
    width, height, fps = 960, 540, 15
    command = ["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pixel_format", "rgb24",
               "-video_size", f"{width}x{height}", "-framerate", str(fps), "-i", "-", "-an",
               "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-movflags", "+faststart",
               str(OUT / "overview.mp4")]
    with subprocess.Popen(command, stdin=subprocess.PIPE) as encoder:
        cover = ImageOps.fit(Image.open(OUT / "cover.png").convert("RGB"), (width, height))
        for _ in range(fps*2):
            encoder.stdin.write(cover.tobytes())
        for name, title, detail in FEATURES:
            base = video_base(title, detail)
            decoder = subprocess.Popen([
                "ffmpeg", "-loglevel", "error", "-i", str(ROOT / "macos/Previews" / f"{name}.mp4"),
                "-t", "3", "-vf", "fps=15,scale=840:315", "-f", "rawvideo", "-pix_fmt", "rgb24", "-",
            ], stdout=subprocess.PIPE)
            frame_bytes = 840*315*3
            for _ in range(fps*3):
                data = read_frame(decoder.stdout, frame_bytes)
                if len(data) != frame_bytes:
                    raise RuntimeError(f"Missing preview frames: {name}")
                image = base.copy()
                image.paste(Image.frombytes("RGB", (840, 315), data), (60, 164))
                encoder.stdin.write(image.tobytes())
            decoder.stdout.close()
            if decoder.wait() != 0:
                raise RuntimeError(f"Could not decode preview: {name}")
        for _ in range(fps):
            encoder.stdin.write(cover.tobytes())
    if encoder.returncode != 0:
        raise RuntimeError("Could not encode overview")


if __name__ == "__main__":
    make_cover()
    make_feature_images()
    make_gallery()
    make_overview()
    print("Created release media in", OUT)
