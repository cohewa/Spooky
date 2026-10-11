#!/usr/bin/env python3
"""Render six original, silent looping previews for the native Mac window."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import math
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "macos" / "Previews"
OUT.mkdir(exist_ok=True)
W, H, FPS, FRAMES = 640, 162, 12, 36
FONT = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 17)
FOLDER_STYLES = [Image.open(ROOT / "macos" / "FolderStyles" / f"{name}.png").convert("RGBA") for name in ("maple", "pumpkin", "knit", "stripes", "skeleton", "bat", "kitten")]


def rounded(draw, box, fill, radius=16, outline=None, width=1):
    draw.rounded_rectangle(box, radius, fill=fill, outline=outline, width=width)


def pumpkin(draw, x, y, scale=1):
    for dx, color in [(-13, "#c45b27"), (13, "#c45b27"), (0, "#ed9140")]:
        draw.ellipse((x + (dx - 24)*scale, y - 27*scale, x + (dx + 24)*scale, y + 27*scale), fill=color)
    draw.rounded_rectangle((x-4*scale, y-35*scale, x+4*scale, y-21*scale), radius=2, fill="#4b562f")
    draw.ellipse((x-17*scale, y-5*scale, x-12*scale, y), fill="#442322")
    draw.ellipse((x+12*scale, y-5*scale, x+17*scale, y), fill="#442322")
    draw.arc((x-12*scale, y-2*scale, x+12*scale, y+15*scale), 8, 170, fill="#442322", width=max(1, int(2*scale)))


def ghost(draw, x, y):
    draw.ellipse((x-22, y-28, x+22, y+16), fill="#f7ead9")
    draw.polygon([(x-22,y-3),(x-22,y+28),(x-12,y+19),(x,y+28),(x+10,y+19),(x+22,y+28),(x+22,y-3)], fill="#f7ead9")
    draw.ellipse((x-10,y-5,x-4,y+3), fill="#38252b")
    draw.ellipse((x+5,y-5,x+11,y+3), fill="#38252b")


def leaf(draw, x, y, angle=0):
    points=[]
    for i in range(9):
        t=2*math.pi*i/8
        radius=17 if i % 2 == 0 else 9
        points.append((x+math.cos(t+angle)*radius, y+math.sin(t+angle)*radius))
    draw.polygon(points, fill="#d88939")
    draw.line((x,y,x+22*math.cos(angle+.5),y+22*math.sin(angle+.5)), fill="#7f4b25", width=2)


def browser(draw):
    rounded(draw, (38, 12, 603, 151), "#fff8e9", 15)
    rounded(draw, (38, 12, 603, 37), "#e6d7c4", 15)
    draw.rectangle((38, 26, 603, 37), fill="#e6d7c4")
    for x in (55,68,81): draw.ellipse((x,21,x+7,28), fill="#aa806d")
    rounded(draw, (178,19,446,32), "#f6eee3", 6)
    draw.text((285,17), "autumn.page", font=FONT, fill="#866753")
    draw.text((78,66), "A little bit of magic", font=FONT, fill="#6d4b3d")
    draw.line((80,102,370,102), fill="#d7c4ad", width=3)
    draw.line((80,116,320,116), fill="#e3d4bf", width=3)


def web(draw, right=False, shift=0):
    cx=603 if right else 38
    sx=-1 if right else 1
    for radius in (29,49,69):
        draw.arc((cx-radius if right else cx, 38, cx if right else cx+radius, 38+radius), 0 if right else 0, 90, fill="#907e6d", width=1)
    for dx,dy in ((70,0),(50,35),(0,70)):
        draw.line((cx,38,cx+sx*dx+shift,38+dy), fill="#907e6d", width=1)


def skeleton(draw, x, y):
    bone="#f6e8d7"; shadow="#8e655d"
    draw.line((x,y+15,x,y+45),fill=bone,width=5)
    draw.ellipse((x-14,y-12,x+14,y+16),fill=bone,outline=shadow,width=2)
    draw.ellipse((x-8,y-1,x-4,y+3),fill=shadow)
    draw.ellipse((x+4,y-1,x+8,y+3),fill=shadow)
    for sign in (-1,1):
        draw.line((x,y+25,x+sign*18,y+42),fill=bone,width=4)
        draw.line((x,y+44,x+sign*11,y+62),fill=bone,width=4)
    draw.arc((x-11,y+19,x+11,y+38),0,180,fill=bone,width=3)


def folder(draw,x,y,leafy=True):
    rounded(draw,(x,y,x+94,y+67),"#794831",10)
    rounded(draw,(x,y-11,x+39,y+15),"#794831",6)
    rounded(draw,(x+3,y+13,x+91,y+65),"#b2764b",9)
    if leafy: pumpkin(draw,x+48,y+40,.32)


def frame(kind, i):
    im=Image.new("RGB",(W,H),"#2f2027")
    d=ImageDraw.Draw(im)
    t=i/FRAMES
    if kind in ("webs","skeletons","cursor"):
        browser(d)
        if kind=="webs":
            web(d,shift=math.sin(t*2*math.pi)*2)
            web(d,True,shift=math.sin(t*2*math.pi+1)*2)
            d.ellipse((90+230*t,66,98+230*t,74),fill="#493237")
            d.line((94+230*t,38,94+230*t,66),fill="#9b8b7a",width=1)
        elif kind=="skeletons":
            for j in range(3):
                y=-25+((t+j*.31)%1)*175
                skeleton(d,425+j*67,y)
        else:
            x=350+110*math.sin(t*2*math.pi)
            y=78+20*math.cos(t*2*math.pi)
            d.polygon([(x-15,y-21),(x-10,y+14),(x-3,y+5),(x+7,y+18),(x+13,y+14),(x+3,y+2),(x+18,y)],fill="#f9e6c5",outline="#5a302c")
            d.ellipse((x-8,y-5,x-3,y),fill="#e98842")
            rounded(d,(80,120,275,140),"#f6ead9",5,outline="#c6b19e")
            d.line((110,124,110,136),fill="#5b453e",width=1)
    elif kind=="stickers":
        for y in range(H): d.line((0,y,W,y),fill=(71+y//11,47+y//9,55+y//12))
        d.rectangle((13,12,626,147),outline="#ad8c73",width=1)
        pumpkin(d,150+18*math.sin(t*2*math.pi),85,.95)
        ghost(d,320,79+9*math.sin(t*2*math.pi+1))
        leaf(d,482+13*math.sin(t*2*math.pi+2),85, t)
        d.text((28,19),"desktop",font=FONT,fill="#f8dfb8")
    elif kind=="folders":
        d.rectangle((0,0,W,H),fill="#52373a")
        d.ellipse((512,20,588,96),fill="#e4a45e")
        for j, style in enumerate(FOLDER_STYLES):
            x = 12 + j * 88
            icon = ImageOps.contain(style, (78, 74), Image.Resampling.LANCZOS)
            padded = Image.new("RGBA", (82, 82), (0, 0, 0, 0))
            padded.alpha_composite(icon, ((82-icon.width)//2, (82-icon.height)//2))
            im.paste(padded, (x, 31 + int(2*math.sin(t*2*math.pi+j))), padded)
    else:
        for y in range(H): d.line((0,y,W,y),fill=(56+y//10,34+y//8,49+y//9))
        d.ellipse((458,21,544,107),fill="#efd09d")
        d.ellipse((444,11,528,100),fill="#61404a")
        d.polygon([(0,119),(95,91),(190,126),(311,87),(436,131),(640,91),(640,162),(0,162)],fill="#262d2d")
        for j in range(20):
            x=(j*83+23+int(t*50))%W
            y=(j*57+13)%118
            d.ellipse((x,y,x+2,y+2),fill="#d6a56e")
    return im


for kind in ("webs","skeletons","stickers","folders","wallpaper","cursor"):
    command=["ffmpeg","-loglevel","error","-y","-f","rawvideo","-pixel_format","rgb24","-video_size",f"{W}x{H}","-framerate",str(FPS),"-i","-","-an","-c:v","libx264","-pix_fmt","yuv420p","-crf","28","-movflags","+faststart",str(OUT / f"{kind}.mp4")]
    with subprocess.Popen(command,stdin=subprocess.PIPE) as process:
        for i in range(FRAMES): process.stdin.write(frame(kind,i).tobytes())
    print(kind, (OUT / f"{kind}.mp4").stat().st_size)
