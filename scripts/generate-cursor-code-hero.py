#!/usr/bin/env python3
"""Make a light code-editor still using the exact Spooky cursor asset."""

from pathlib import Path
import re

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "media" / "cursor-code-hero.png"
BACKGROUND = ROOT / "docs" / "media" / "cursor-code-background.png"
W, H = 1600, 900
SF = "/System/Library/Fonts/SFNS.ttf"
MONO = "/System/Library/Fonts/Menlo.ttc"


def font(size, mono=False):
    return ImageFont.truetype(MONO if mono else SF, size)


image = Image.new("RGB", (W, H), "#f6f7f8").convert("RGBA")
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, W, 42), fill="#fbfbfc")
draw.text((30, 10), "●", font=font(18), fill="#242a30")
draw.text((73, 10), "Code    File    Edit    Selection    View    Go    Run    Terminal    Help", font=font(18), fill="#30353b")
draw.text((1403, 10), "◉   12:28", font=font(17), fill="#53606a")

shadow = Image.new("RGBA", (W, H))
ImageDraw.Draw(shadow).rounded_rectangle((72, 77, 1530, 851), radius=22, fill=(29, 37, 48, 72))
image = Image.alpha_composite(image, shadow.filter(ImageFilter.GaussianBlur(29)))
draw = ImageDraw.Draw(image)
draw.rounded_rectangle((78, 68, 1522, 833), radius=20, fill="#ffffff", outline="#d6dce3", width=2)
draw.rounded_rectangle((78, 68, 1522, 127), radius=20, fill="#f5f6f8")
draw.rectangle((78, 104, 1522, 127), fill="#f5f6f8")
for x, color in ((108, "#ff5f57"), (134, "#ffbd2e"), (160, "#28c840")):
    draw.ellipse((x, 91, x+16, 107), fill=color)
draw.text((648, 84), "Spooky — HalloweenDecor.swift", font=font(18), fill="#68727b")
draw.line((78, 127, 1522, 127), fill="#e5e8eb", width=2)

# Activity bar and a compact, believable project explorer.
draw.rectangle((79, 128, 135, 831), fill="#f0f2f5")
draw.rectangle((136, 128, 368, 831), fill="#f7f8fa")
draw.line((368, 128, 368, 832), fill="#e4e8ed", width=2)
draw.rounded_rectangle((80, 162, 84, 207), radius=2, fill="#f47d2c")
for cy in (188, 247, 306, 365):
    draw.rounded_rectangle((97, cy-12, 117, cy+10), radius=3, outline="#8995a0", width=2)
    draw.line((102, cy-4, 112, cy-4), fill="#8995a0", width=2)
draw.text((155, 156), "EXPLORER", font=font(16), fill="#72808c")
draw.text((156, 205), "▾  SPOOKY", font=font(18), fill="#39434d")
draw.text((162, 250), "▾  macos", font=font(18), fill="#45515b")
draw.rounded_rectangle((144, 287, 357, 330), radius=7, fill="#e8edf3")
draw.text((184, 295), "HalloweenDecor.swift", font=font(16), fill="#39444e")
draw.text((184, 347), "CandyCursor.png", font=font(16), fill="#64717b")
draw.text((162, 404), "▸  scripts", font=font(18), fill="#45515b")
draw.text((162, 449), "▸  docs", font=font(18), fill="#45515b")
draw.text((162, 494), "   README.md", font=font(16), fill="#64717b")

# Editor chrome, tabs, breadcrumbs, and line numbers.
draw.rectangle((369, 128, 1521, 178), fill="#fbfbfc")
draw.rectangle((370, 128, 643, 178), fill="#ffffff")
draw.line((370, 177, 643, 177), fill="#f47d2c", width=3)
draw.rounded_rectangle((394, 143, 413, 162), radius=4, fill="#ed7a35")
draw.text((399, 143), "S", font=font(15), fill="#ffffff")
draw.text((424, 144), "HalloweenDecor.swift", font=font(18), fill="#303b46")
draw.text((618, 143), "×", font=font(18), fill="#9aa4ac")
draw.text((399, 190), "macos  ›  HalloweenDecor.swift  ›  CandyPointerView", font=font(16), fill="#86929d")
draw.line((369, 216, 1521, 216), fill="#f0f1f3", width=2)

source = (ROOT / "macos" / "HalloweenDecor.swift").read_text().splitlines()
start, end = 591, 610
code_font = font(20, mono=True)
code_image = Image.new("RGBA", (W, H))
code_draw = ImageDraw.Draw(code_image)
line_y = 238
line_height = 28
palette = {"comment": "#718b73", "keyword": "#a144ad", "type": "#29788e", "string": "#aa6044", "plain": "#303943"}
pattern = re.compile(r'(//.*$|\b(?:private|final|class|var|let|override|guard|else|return|func|if)\b|\b(?:NSView|NSPoint|NSImage|Bundle|NSRect|NSSize|NSGraphicsContext|CGFloat|CandyPointerView)\b|"[^"\n]*")')
for offset, raw in enumerate(source[start-1:end]):
    y = line_y + offset*line_height
    code_draw.text((408, y), str(start+offset), font=font(17, mono=True), fill="#a7b1ba")
    x = 463
    cursor = 0
    for match in pattern.finditer(raw):
        before = raw[cursor:match.start()]
        code_draw.text((x, y), before, font=code_font, fill=palette["plain"])
        x += code_draw.textlength(before, font=code_font)
        token = match.group()
        kind = "comment" if token.startswith("//") else "string" if token.startswith('"') else "keyword" if token in {"private","final","class","var","let","override","guard","else","return","func","if"} else "type"
        code_draw.text((x, y), token, font=code_font, fill=palette[kind])
        x += code_draw.textlength(token, font=code_font)
        cursor = match.end()
    code_draw.text((x, y), raw[cursor:], font=code_font, fill=palette["plain"])
image.alpha_composite(code_image.crop((370, 217, 1521, 800)), (370, 217))
draw.rectangle((370, 800, 1521, 831), fill="#f7f8fa")
draw.text((394, 806), "main  ·  Swift  ·  UTF-8", font=font(15), fill="#7d8993")
draw.text((1357, 806), "Ln 592, Col 1", font=font(15), fill="#7d8993")
image.convert("RGB").save(BACKGROUND, optimize=True)

# Use the exact source PNG. Nearest-neighbor enlargement preserves its pixel artwork.
candy = Image.open(ROOT / "macos" / "CandyCursor.png").convert("RGBA")
candy = candy.resize((550, 576), Image.Resampling.NEAREST)
position = (957, 224)
candy_shadow = Image.new("RGBA", (W, H))
candy_shadow.alpha_composite(candy, (position[0]+12, position[1]+18))
candy_shadow.putalpha(candy_shadow.getchannel("A").point(lambda alpha: round(alpha * 0.27)))
image = Image.alpha_composite(image, candy_shadow.filter(ImageFilter.GaussianBlur(21)))
image.alpha_composite(candy, position)
image.convert("RGB").save(OUTPUT, optimize=True)
print(OUTPUT)
