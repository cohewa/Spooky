# Original Spooky artwork

Generated on 2026-10-13 and 2026-10-14 with OpenAI ImageGen for this project. These source files are retained so that the cutouts and bundled app artwork can be traced back to the generation outputs. Earlier user-supplied reference images are not used as source files in this directory. The generated candy below remains an unused alternative after the user-authorized candy cursor was restored on 2026-10-14.

| Source file | Prompt direction | Packaged output |
| --- | --- | --- |
| `source/pumpkin-garden.png` | Original cozy pumpkin garden at blue hour; gouache and colored pencil, teal and plum sky, sage leaves, low pumpkin rows, no characters or text | `macos/Wallpaper/pumpkin-field.png` |
| `source/stickers-01.png` | 16 new isolated autumn and Halloween objects in a unified cream, copper, plum, teal palette; transparent 4×4 sheet | Part of 52 independent stickers |
| `source/stickers-02.png` | 16 further original isolated objects including raven, mushroom, potion, watch, books, kettle, owl; transparent 4×4 sheet | Part of 52 independent stickers |
| `source/stickers-03.png` | 16 further original isolated objects including bat, pumpkins, candle, fox, pie, leaves; transparent 4×4 sheet | Part of 52 independent stickers |
| `source/stickers-04.png` | Four original isolated objects: frog, skull, ghost cocoa cup, candy corn; transparent 2×2 sheet | Part of 52 independent stickers |
| `source/candy-cursor.png` | Face-free amber pixel-art candy with plum crescent and asymmetrical orange and teal wrappers, transparent | Unused alternative; the earlier user-supplied candy is active |
| `source/folder-icons.png` | Six new isolated folder illustrations with leaf, pumpkin, knit, stripes, bat, and cat motifs; transparent 3×2 sheet | Six bundled folder styles |
| `source/app-icon-bat.png` | Original charcoal bat silhouette on a warm off-white field, generated without a reference image | macOS app icon and Safari extension icons |

Run `python3 scripts/split-sticker-sheet.py` to recreate the 52 sticker PNGs from the four source sheets. `scripts/generate-web-art.py` draws the spider web and four spiders; the loader bat is drawn with Swift vector paths. The previous candy cursor is an explicit user-authorized exception. The ignored `dist/reference-assets-archive/` holds local rollback copies and must never be published.

These prompts and saved outputs document the creative process. They are not a legal warranty for third-party material. The project owner chose the repository's MIT License for original Spooky artwork and confirmed rights to redistribute the restored candy under MIT.
