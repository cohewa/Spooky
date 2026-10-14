#!/usr/bin/env python3
"""Draw Spooky's original screen-top web and four dangling spiders."""
from math import pi, sin
from pathlib import Path
from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parents[1] / "macos" / "WebDecor"
OUT.mkdir(parents=True, exist_ok=True)
S, WIDTH, HEIGHT = 2, 1756, 750
INK = (12, 11, 12, 255)

def artwork(width):
    canvas = Image.new("RGBA", (width*S, HEIGHT*S), (0, 0, 0, 0))
    return canvas, ImageDraw.Draw(canvas)

def point(xy):
    return tuple(round(value*S) for value in xy)

def line(draw, points, width=4):
    draw.line([point(p) for p in points], fill=INK, width=width*S, joint="curve")

def curve(a, b, c, d, steps=100):
    result = []
    for index in range(steps+1):
        t = index/steps
        u = 1-t
        result.append((u**3*a[0]+3*u*u*t*b[0]+3*u*t*t*c[0]+t**3*d[0],
                       u**3*a[1]+3*u*u*t*b[1]+3*u*t*t*c[1]+t**3*d[1]))
    return result

center, draw = artwork(WIDTH)
line(draw, [(0, 0), (WIDTH, 0)], 7)
for left, right, drop in [(0, 420, 180), (420, 850, 210), (850, 1295, 192), (1295, WIDTH, 172)]:
    middle = (left+right)/2
    spokes = []
    for index in range(9):
        fraction = index/8
        x = left + fraction*(right-left)
        y = max(8, drop*sin(pi*fraction)**.75)
        a, d = (middle, -38), (x, y)
        b, c = (middle+(x-middle)*.18, 12), (middle+(x-middle)*.75, y*.65)
        spokes.append((a, b, c, d))
        line(draw, curve(a, b, c, d))
    for level in (.28, .48, .68, .86, 1.0):
        anchors = [curve(*spoke)[round(level*100)] for spoke in spokes]
        for a, d in zip(anchors, anchors[1:]):
            dx = d[0]-a[0]
            sag = 12+15*level
            line(draw, curve(a, (a[0]+dx*.28, a[1]+sag),
                             (d[0]-dx*.28, d[1]+sag), d), 3)

def spider(cx, thread, radius):
    line(draw, [(cx, 0), (cx, thread)], 3)
    head = thread+radius*.38
    body = thread+radius*1.23
    draw.ellipse(point((cx-radius*.34, head-radius*.34))+
                 point((cx+radius*.34, head+radius*.34)), fill=INK)
    draw.ellipse(point((cx-radius*.68, body-radius*.72))+
                 point((cx+radius*.68, body+radius*.72)), fill=INK)
    for side in (-1, 1):
        for index in range(4):
            start = thread+radius*(.78+index*.24)
            knee = (cx+side*radius*(.88+index*.12), start-radius*(.48-index*.12))
            end = (cx+side*radius*(1.28+index*.15), start+radius*(.33+index*.13))
            line(draw, [(cx+side*radius*.43, start), knee, end], 4)

for x, length, size in [(185, 193, 34), (619, 326, 42), (1035, 422, 48), (1518, 258, 39)]:
    spider(x, length, size)
center = center.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
center.save(OUT/"center-web.png", optimize=True)

panel_width = WIDTH*2
panel, draw = artwork(panel_width)
origin = (-130, -35)
spokes = []
for index in range(13):
    t = index/12
    end = (panel_width*t, 190*sin(pi*t))
    controls = (origin, (origin[0]+(end[0]-origin[0])*.35, 8),
                (origin[0]+(end[0]-origin[0])*.82, end[1]-25), end)
    spokes.append(controls)
    line(draw, curve(*controls, steps=90))
for level in (.29, .47, .65, .83, 1.0):
    anchors = [curve(*spoke)[round(level*100)] for spoke in spokes]
    for a, d in zip(anchors, anchors[1:]):
        dx = d[0]-a[0]
        line(draw, curve(a, (a[0]+dx*.33, a[1]+28*level),
                         (d[0]-dx*.33, d[1]+28*level), d), 3)
panel = panel.resize((panel_width, HEIGHT), Image.Resampling.LANCZOS)
wide = Image.new("RGBA", (WIDTH*5, HEIGHT), (0, 0, 0, 0))
wide.alpha_composite(panel)
wide.alpha_composite(center, (panel_width, 0))
wide.alpha_composite(panel.transpose(Image.Transpose.FLIP_LEFT_RIGHT),
                     (panel_width+WIDTH, 0))
wide.save(OUT/"wide-web.png", optimize=True)
