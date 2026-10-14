#!/usr/bin/env python3
"""Render feature previews in a recognizable macOS desktop scene."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
import math
import os
import subprocess
from functools import lru_cache

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "macos/Previews"
OUT.mkdir(exist_ok=True)
SCENE = ROOT / "macos/PreviewScene"
if not (SCENE / "desktop.png").exists():
    subprocess.run(["swift", str(ROOT / "scripts/export-preview-scene.swift")], cwd=ROOT, check=True)
subprocess.run(["python3", str(ROOT / "scripts/generate-web-art.py")], check=True)
W, H, FPS, FRAMES = 640, 240, 24, 168
SCALE = 2
FONT_PATH = "/System/Library/Fonts/SFNS.ttf"
@lru_cache
def font(size):
    return ImageFont.truetype(FONT_PATH, size * SCALE)

def load(path):
    return Image.open(path).convert("RGBA")

DESKTOP = load(SCENE / "desktop.png")
WALLPAPER = load(ROOT / "macos/Wallpaper/pumpkin-field.png")
WEB = load(ROOT / "macos/WebDecor/wide-web.png")
CANDY = load(ROOT / "macos/CandyCursor.png")
DOCK = [load(SCENE / f"{name}.png") for name in ("finder", "safari", "calendar", "notes", "settings")]
FOLDER = load(SCENE / "folder.png")
FOLDER_STYLES = [load(ROOT / "macos/FolderStyles" / f"{name}.png") for name in ("maple", "pumpkin", "knit", "stripes", "bat", "kitten")]
STICKERS = [load(ROOT / "macos/Stickers/Objects" / f"{name}.png") for name in ("sheet-ghost", "iron-cauldron", "enamel-mug", "moon", "frog", "witch-hat", "black-cat", "pumpkin-spice-candle", "ghost-cocoa", "mushroom", "jack-o-lantern", "oak-leaf")]
BACKGROUNDS = [ImageOps.fit(asset,(W*SCALE,H*SCALE),method=Image.Resampling.LANCZOS) for asset in (DESKTOP,WALLPAPER)]
FITTED_ASSETS = {}
WEB_CLOSEUP = WEB.crop((3100, 0, 5500, 750)).resize((W*SCALE, 200*SCALE), Image.Resampling.LANCZOS)
CANDY_CLOSEUP = CANDY.resize((154*SCALE, 161*SCALE), Image.Resampling.NEAREST)
WIDGET_LEAVES = [load(ROOT / "macos/Stickers/Objects" / f"{name}.png") for name in ("oak-leaf","autumn-leaf")]
WIDGET_STAR = load(ROOT / "macos/Stickers/Objects/star.png")
WIDGET_PINECONE = load(ROOT / "macos/Stickers/Objects/pinecone.png")

def rect(draw, box, fill, radius=0, outline=None):
    draw.rounded_rectangle(tuple(round(x * SCALE) for x in box), radius * SCALE, fill=fill, outline=outline, width=SCALE)

def text(draw, xy, label, size=9, fill="white", anchor=None):
    draw.text(tuple(round(x * SCALE) for x in xy), label, font=font(size), fill=fill, anchor=anchor)

def paste(image, asset, xy, size):
    key = (id(asset), size)
    if key not in FITTED_ASSETS:
        FITTED_ASSETS[key] = ImageOps.contain(asset, tuple(round(v*SCALE) for v in size), Image.Resampling.LANCZOS)
    fitted = FITTED_ASSETS[key]
    x = round(xy[0] * SCALE + (size[0] * SCALE - fitted.width) / 2)
    y = round(xy[1] * SCALE + (size[1] * SCALE - fitted.height) / 2)
    image.alpha_composite(fitted, (x, y))

def pointer(draw, x, y):
    points = [(x,y),(x,y+15),(x+4,y+11),(x+7,y+17),(x+10,y+15),(x+7,y+9),(x+13,y+9)]
    draw.polygon([(round(a*SCALE),round(b*SCALE)) for a,b in points], fill="#141414", outline="white", width=SCALE)

def desktop(wallpaper=False):
    image = BACKGROUNDS[int(wallpaper)].copy()
    bar = Image.new("RGBA",image.size)
    rect(ImageDraw.Draw(bar),(0,0,W,18),(244,244,248,210))
    image.alpha_composite(bar)
    draw = ImageDraw.Draw(image)
    text(draw,(12,1),"",10,"#24242c")
    for x, label in [(29,"Finder"),(70,"File"),(94,"Edit"),(120,"View"),(151,"Go"),(172,"Window"),(216,"Help")]:
        text(draw,(x,3),label,8,"#24242c")
    text(draw,(524,3),"Wi-Fi   100%   12:41",8,"#24242c")
    rect(draw,(237,H-35,403,H-3),(237,239,246,170),8, (255,255,255,100))
    for j, icon in enumerate(DOCK):
        paste(image,icon,(245+j*31,H-32),(27,27))
    return image

def desktop_folder(image, asset, x, y, label, size=(38,35)):
    paste(image,asset,(x,y),size)
    draw=ImageDraw.Draw(image)
    text(draw,(x+size[0]/2,y+size[1]+2),label,11 if size[0]>38 else 8,anchor="mt")

def finder_window(image):
    shadow=Image.new("RGBA",image.size)
    rect(ImageDraw.Draw(shadow),(47,34,487,207),(0,0,0,120),8)
    image.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(7*SCALE)))
    draw=ImageDraw.Draw(image)
    rect(draw,(45,29,485,199),"#f9f9fa",7, "#c2c2c6")
    rect(draw,(45,29,159,199),"#e7e7ed",7)
    rect(draw,(45,29,485,61),"#ededf0",7)
    rect(draw,(45,51,485,61),"#ededf0")
    for x,color in [(56,"#ff5f57"),(68,"#febc2e"),(80,"#28c840")]:
        rect(draw,(x,40,x+7,47),color,4)
    text(draw,(172,39),"‹   ›     Documents",11,"#34343b")
    rect(draw,(389,38,474,52),"#e1e1e6",4)
    text(draw,(399,39),"Search",8,"#777780")
    text(draw,(58,68),"Favorites",8,"#81818c")
    for j,label in enumerate(("Recents","Applications","Desktop","Documents","Downloads")):
        y=86+j*19
        if label=="Documents": rect(draw,(51,y-2,151,y+13),"#d0d0dc",4)
        text(draw,(62,y),"◇",9,"#647db5")
        text(draw,(77,y),label,9,"#51515c")
    text(draw,(177,69),"Name",8,"#7c7c85")
    text(draw,(360,69),"Date Modified",8,"#7c7c85")
    for j,label in enumerate(("Project notes","Inspiration","Autumn photos","Weekend plans")):
        y=88+j*23
        if j%2==0:rect(draw,(161,y-3,480,y+17),"#f0f0f4",2)
        paste(image,FOLDER,(176,y-2),(19,17))
        text(draw,(202,y),label,9,"#404049")
        text(draw,(360,y),"Today, 12:30",8,"#81818a")

def autumn_widgets(image):
    draw = ImageDraw.Draw(image)
    rect(draw,(47,47,153,151),"#3678b4",13)
    text(draw,(58,58),"San Francisco",9)
    text(draw,(58,77),"21°",28)
    text(draw,(58,118),"Sunny",10)
    rect(draw,(179,47,366,151),"#fffdf8",13)
    text(draw,(192,60),"TUESDAY",8,"#e55e37")
    text(draw,(192,74),"13",25,"#303038")
    text(draw,(192,111),"October",10,"#5a5a63")
    for left,right,corner in ((47,153,"bottom-left"),(179,366,"top-right")):
        top,bottom=47,151
        width=right-left
        branch=[((left+6+width*t/24)*SCALE,(top+1+7*math.sin(math.pi*t/24))*SCALE) for t in range(25)]
        draw.line(branch,fill="#503220",width=3)
        count=3 if width<150 else 4
        for j in range(count):
            fraction=(j+.4)/count
            x=left+6+(width-12)*fraction
            y=top+1+7*math.sin(math.pi*fraction)
            drop=11+(j*5)%7
            dx=-3 if j%2==0 else 3
            draw.line(((x*SCALE,y*SCALE),((x+dx)*SCALE,(y+drop)*SCALE)),fill="#654329",width=2)
            asset=WIDGET_LEAVES[j%2].rotate(158 if j%2==0 else 202,expand=True,resample=Image.Resampling.BICUBIC)
            paste(image,asset,(x+dx-13,y+drop-3),(26,26))
            if j%2==0:
                draw.line(((x*SCALE,y*SCALE),((x-6)*SCALE,(y-3)*SCALE)),fill="#654329",width=2)
        for fraction in ([.67] if width<150 else [.28,.75]):
            x=left+6+(width-12)*fraction
            y=top+1+7*math.sin(math.pi*fraction)
            draw.line(((x*SCALE,y*SCALE),((x+1)*SCALE,(y+10)*SCALE)),fill="#654329",width=2)
            paste(image,WIDGET_PINECONE,(x-7,y+8),(15,18))
        paste(image,WIDGET_STAR,(right+2,91),(11,11))
        if corner=="bottom-left":
            origin,xd,yd=(left,bottom),1,-1
        else:
            origin,xd,yd=(right,top),-1,1
        for angle in (0,math.pi/6,math.pi/3,math.pi/2):
            draw.line((origin[0]*SCALE,origin[1]*SCALE,(origin[0]+xd*math.cos(angle)*25)*SCALE,(origin[1]+yd*math.sin(angle)*25)*SCALE),fill="#503525",width=2)
        for radius in (8,16,25):
            points=[((origin[0]+xd*math.cos(j*math.pi/6)*radius)*SCALE,(origin[1]+yd*math.sin(j*math.pi/6)*radius)*SCALE) for j in range(4)]
            draw.line(points,fill="#503525",width=2)

def web_scene(t):
    image = Image.new("RGBA", (W*SCALE, H*SCALE))
    draw = ImageDraw.Draw(image)
    for y in range(H*SCALE):
        fraction = y / (H*SCALE)
        draw.line((0,y,W*SCALE,y), fill=(round(118+68*fraction),round(145+42*fraction),round(143+33*fraction),255))
    rect(draw,(0,0,W,38),(204,219,214,105))
    text(draw,(16,17),"●   Finder    File    Edit    View    Window",11,"#f5f7f4")
    rect(draw,(272,-9,370,40),"#171b1c",12)
    text(draw,(475,17),"◈   ◉   100%   12:41",10,"#f5f7f4")
    rect(draw,(27,67,318,274),(235,239,235,226),19,(255,255,255,160))
    rect(draw,(336,67,631,274),(248,241,225,231),19,(255,255,255,170))
    text(draw,(52,85),"63",35,"#5b6b68")
    text(draw,(52,127),"Reminders",17,"#5b6b68")
    draw.line((52*SCALE,160*SCALE,292*SCALE,160*SCALE),fill="#b7c4bf",width=2*SCALE)
    for j,label in enumerate(("Plan autumn trip","Pick up pumpkins")):
        y=175+j*36
        draw.ellipse((53*SCALE,y*SCALE,67*SCALE,(y+14)*SCALE),outline="#a0aba7",width=2*SCALE)
        text(draw,(76,y-2),label,10,"#687471")
    text(draw,(360,88),"TUESDAY",11,"#bb6f54")
    text(draw,(359,106),"13",43,"#564d42")
    text(draw,(428,128),"October",13,"#706b61")
    draw.line((358*SCALE,166*SCALE,607*SCALE,166*SCALE),fill="#d5d0c3",width=2*SCALE)
    text(draw,(359,181),"Today",11,"#786f65")
    web = WEB_CLOSEUP.rotate(.28*math.sin(t*math.tau),Image.Resampling.BICUBIC,expand=False,center=(W*SCALE/2,0))
    image.alpha_composite(web,(round(2*SCALE*math.sin(t*math.tau)),6*SCALE))
    return image

def cursor_scene(t):
    image=Image.new("RGBA",(W*SCALE,H*SCALE),"#d9dbd9")
    draw=ImageDraw.Draw(image)
    rect(draw,(0,0,W,27),"#c6c8c6")
    text(draw,(15,7),"●   Finder     File     Edit     View",9,"#3d4543")
    rect(draw,(29,34,611,269),"#fafafa",13,"#bbc1c1")
    rect(draw,(29,34,611,75),"#edeff0",13)
    rect(draw,(29,61,611,75),"#edeff0")
    for x,color in ((46,"#ff605b"),(60,"#ffbd44"),(74,"#00ca4e")):
        draw.ellipse((x*SCALE,50*SCALE,(x+8)*SCALE,58*SCALE),fill=color)
    text(draw,(252,46),"Documents",12,"#3f4546")
    rect(draw,(29,75,160,269),"#e8ebed")
    text(draw,(49,91),"FAVORITES",8,"#879094")
    for j,label in enumerate(("Recents","Desktop","Documents","Downloads")):
        y=113+j*28
        if label=="Documents": rect(draw,(40,y-3,150,y+19),"#d2d8dc",5)
        text(draw,(50,y),"◇",11,"#667c9a")
        text(draw,(70,y),label,10,"#596166")
    text(draw,(183,89),"Name",9,"#8b9295")
    text(draw,(484,89),"Date Modified",9,"#8b9295")
    for j,label in enumerate(("Autumn photos","Halloween ideas","Projects","Weekend plans")):
        y=111+j*30
        if j%2==0:rect(draw,(164,y-3,600,y+22),"#f2f4f5")
        paste(image,FOLDER,(182,y),(21,19))
        text(draw,(212,y+2),label,10,"#5d666a")
        text(draw,(492,y+2),"Today",9,"#9aa0a2")
    x=281+35*math.sin(t*math.tau)
    y=40+8*math.cos(t*math.tau)
    shadow=Image.new("RGBA",image.size)
    shadow.alpha_composite(CANDY_CLOSEUP,(round((x+5)*SCALE),round((y+8)*SCALE)))
    shadow.putalpha(shadow.getchannel("A").point(lambda a: round(a*.26)))
    image.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(8*SCALE)))
    image.alpha_composite(CANDY_CLOSEUP,(round(x*SCALE),round(y*SCALE)))
    return image

def frame(kind, index):
    t=index/FRAMES
    if kind=="webs":
        image=web_scene(t)
    elif kind=="cursor":
        image=cursor_scene(t)
    else:
        image=desktop(kind=="wallpaper")
    if kind=="stickers":
        for j,sticker in enumerate(STICKERS):
            x=26+(j%6)*102
            y=31+(j//6)*84
            if j==7:
                x+=round(18*math.sin(t*2*math.pi))
                y+=round(5*math.sin(t*2*math.pi))
            paste(image,sticker,(x,y),(68,72))
            if j==7:pointer(ImageDraw.Draw(image),x+42,y+36)
    elif kind=="folders":
        for j,asset in enumerate(FOLDER_STYLES):
            desktop_folder(image,asset,17+j*102,70,("Projects","Photos","Ideas","Work","Notes","Personal")[j],size=(76,68))
    elif kind=="wallpaper":
        autumn_widgets(image)
        for j,label in enumerate(("Projects","Photos")):
            desktop_folder(image,FOLDER,561,42+j*67,label)
    return image.convert("RGB").resize((W,H),Image.Resampling.LANCZOS)

for kind in ("webs","stickers","folders","wallpaper","cursor"):
    if os.environ.get("SPOOKY_PREVIEW_KIND",kind)!=kind:continue
    command=["ffmpeg","-loglevel","error","-y","-f","rawvideo","-pixel_format","rgb24","-video_size",f"{W}x{H}","-framerate",str(FPS),"-i","-","-an","-c:v","libx264","-pix_fmt","yuv420p","-crf","20","-movflags","+faststart",str(OUT/f"{kind}.mp4")]
    with subprocess.Popen(command,stdin=subprocess.PIPE) as process:
        for i in range(FRAMES):process.stdin.write(frame(kind,i).tobytes())
    print(kind,(OUT/f"{kind}.mp4").stat().st_size)
