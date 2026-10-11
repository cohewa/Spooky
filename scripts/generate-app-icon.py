#!/usr/bin/env python3
"""Create a macOS app icon from the Halloween bat artwork."""
from pathlib import Path
import subprocess
import tempfile
from PIL import Image

root = Path(__file__).resolve().parents[1]
source = root / "macos" / "HalloweenDecorIcon.png"
output = root / "macos" / "HalloweenDecor.icns"
with tempfile.TemporaryDirectory() as directory:
    iconset = Path(directory) / "HalloweenDecor.iconset"
    iconset.mkdir()
    image = Image.open(source).convert("RGBA").resize((1024, 1024), Image.Resampling.LANCZOS)
    for points in (16, 32, 128, 256, 512):
        for scale in (1, 2):
            name = f"icon_{points}x{points}" + ("@2x" if scale == 2 else "") + ".png"
            image.resize((points * scale, points * scale), Image.Resampling.LANCZOS).save(iconset / name)
    subprocess.run(["iconutil", "-c", "icns", "-o", str(output), str(iconset)], check=True)
print(output)
