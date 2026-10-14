> Historical entries below describe development builds. Uploaded ZIPs through 0.4.2 were removed from GitHub on 2026-10-14. Source tags remain; no signed, notarized Spooky installer is available yet.

## Spooky 0.5.23 — source preview

- Restored the earlier user-supplied Halloween candy sprite as the Mac and Safari cursor; the project owner confirmed its redistribution rights and selected MIT licensing for project artwork.
- Replaced the app and Safari icon with newly generated bat artwork, and drew the web and animated loading bat as original vector graphics.

# Spooky 0.5.22

- Replaced the pumpkin wallpaper, all 52 separate stickers, candy pointer, and six folder icons with newly generated original illustrations; saved source sheets and provenance in `art/`.
- Prepared screenshots, feature images, and a short overview video for the GitHub project page.
- Limited the local settings bridge to extension access and kept original Desktop folder icons unchanged when backup creation fails.
- Removed unused reference-derived source art from the project tree and refreshed the preview media.

Build from source with `./scripts/build-app.sh`.

# Spooky 0.5.21

- Enlarged the Candy Cursor preview to show the actual candy artwork clearly in a close-up Finder scene.
- Reframed the Spider Web preview around the macOS menu bar, notch, and desktop widgets so the web and hanging spiders are easy to see.

Build from source with `./scripts/build-app.sh`.

# Spooky 0.5.20

- When macOS places the pumpkin status item beneath the display notch, Spooky shows a clickable pumpkin in the visible menu bar area. It disappears when the system item becomes visible again.

Build from source with `./scripts/build-app.sh`.

# Spooky 0.5.19

- Attached widget webs directly to varied top and bottom corners.
- Added hanging twig, leaf, and pinecone garlands along widget tops and updated the Wallpaper preview.

Build from source with `./scripts/build-app.sh`.

# Spooky 0.5.18

- Animated previews now fill each preview tile from edge to edge, without side bars.

Build from source with `./scripts/build-app.sh`.

# Spooky 0.5.17

- Wallpaper now frames desktop widgets with autumn leaves, corner webs, and golden stars.
- Decorations automatically track widget positions and sizes, allow clicks through, and disappear when Wallpaper is disabled.

Build from source with `./scripts/build-app.sh`.

# Spooky 0.5.16

- Rebuilt all five previews around a macOS desktop scene with system app icons, menu bar, Dock, Finder window, and labeled desktop folders.
- Used the actual feature artwork and showed individual sticker dragging and the candy beneath the pointer. Previews now render at 24 fps and fill their tiles more closely.

Build from source with `./scripts/build-app.sh`.

# Spooky 0.5.15

- Split the Halloween object sheet into 44 independent transparent stickers, for a total of 52 movable desktop stickers.
- Added a desktop grid for new stickers, preserved the saved positions of existing designs, and updated the preview to show separate objects.

Build from source with `./scripts/build-app.sh`.

# Spooky 0.5.14

- Removed the flying ghost from the wallpaper effect and preview. The setting is now called Pumpkin Wallpaper.

Build from source with `./scripts/build-app.sh`.

# Spooky 0.5.13

- Added a slow, subtle sway to the screen-top spider web and its preview. The web remains attached to the top edge and respects Reduce Motion.

Build from source with `./scripts/build-app.sh`.

# Spooky 0.5.12

- Recolored the animated loading bat and Applying… label to match the orange switches.

Build from source with `./scripts/build-app.sh`.

# Spooky 0.5.11

- Removed the Restore Everything and Quit Spooky labels from the bottom of the settings window.
- Extended the feature list into the freed space.

Build from source with `./scripts/build-app.sh`.

# Spooky 0.5.10

- Reduced the settings window to 780 × 760 points and narrowed the animated previews from 306 to 226 points.
- Switched the settings typography to the bundled Anonymous Pro family.

Build from source with `./scripts/build-app.sh`.

# Spooky 0.5.9

- Restyled the Mac app window to match the supplied dark, glossy reference: rounded double frame, typography, close button, shadows, orange gradients, and switches.
- Enlarged the animated feature previews and placed the five effects in a scrollable list without left-side icons.

Build from source with `./scripts/build-app.sh`.

# Spooky 0.5.8

- Replaced the three drawn desktop stickers with nine transparent stickers based on the supplied references.
- Added the nine designs to the animated Desktop Stickers preview and kept each sticker movable on the desktop.

Build from source with `./scripts/build-app.sh`.

# Spooky 0.5.7

- Replaced the wallpaper with the pumpkin field based on the supplied reference, with the character removed.
- Replaced the flying ghost with the supplied pixel-art ghost as a transparent animated sprite.
- Updated the animated wallpaper preview to use the same images.

Build from source with `./scripts/build-app.sh`.

# Spooky 0.5.6

- Back up a missing original wallpaper from the matching macOS wallpaper cache so the effect can still be applied and restored.

Build from source with `./scripts/build-app.sh`.

# Spooky 0.5.5

- Shift the candy artwork below the pointer hotspot so it does not sit beneath a native arrow when macOS restores one.

Build from source with `./scripts/build-app.sh`.

# Spooky 0.5.4

- Restored the pumpkin emoji in the macOS menu bar; the candy remains the custom cursor.

Build from source with `./scripts/build-app.sh`.

# Spooky 0.5.3

- Replaced the pumpkin pointer with the candy cursor from the supplied reference in the Mac overlay, Safari, and the animated preview.

Build from source with `./scripts/build-app.sh`.

# Spooky 0.5.2

- Reapply native cursor hiding when apps activate, and hide Safari's default cursor on editable fields so the pumpkin is the only page pointer.

Build from source with `./scripts/build-app.sh`.

# Spooky 0.5.1

- Added a native click-through pumpkin pointer overlay across macOS and kept Safari's page cursor active on all allowed websites.
- Replaced the menu bar emoji with a transparent, white template bat mark; the Safari extension icons now use the same bat silhouette.
- Kept the app and extension versions aligned at 0.5.1.

Build from source with `./scripts/build-app.sh`.

# Spooky 0.5.0

- Replaced the previous Spider Web scene with one centered, transparent black web and four hanging spiders, based on the supplied reference.
- Removed the side webs, garland, and flying bats from this effect. The composition stays click-through on every display.
- Removed Falling Skeletons from the app, Safari extension, and settings bridge.
- Reworked the app as a compact dark list with a preview icon and native toggle per effect; the menu bar shortcut now uses the app's bat logo.
- Updated previews, the app screenshot, and the installation notes.

This historical build has no downloadable installer.

# Halloween Decor 0.4.2

- Reduced both screen decorations to 60% of their previous size. The left web starts below the macOS menu bar; the pumpkin-and-bat garland now sits at the lower right above the Dock.
- Changed the dangling spider to black and softened the free ends of the web strands.
- Bats now fly diagonally from below the left side of the screen toward the upper right, once when Webs is enabled and once each hour afterward.
- The overlay uses a floating window level so the menu bar and Dock stay above it. Updated the card preview.

This historical build has no downloadable installer.

# Halloween Decor 0.4.1

- Added a small bat loading indicator in the Mac window using the same silhouette as the app icon. Its wings flap while an effect is being applied or all effects are restored.
- The indicator also appears while Desktop folder icons are applied at launch. Reduce Motion keeps the bat still while retaining the status text.

This historical build has no downloadable installer.

# Halloween Decor 0.4.0

- The Webs switch now decorates the entire Mac screen, including Safari and other apps, with a white left web and dangling spider plus the referenced pumpkin-and-bat garland on the right.
- Spider and garland move once per minute; a group of bats flies across the lower-right area when switched on and once per hour afterward. Decorations allow clicks to pass through.
- Updated the card video preview and removed duplicate Safari-only web artwork.

This historical build has no downloadable installer. Safari still uses a temporary extension for the skeleton and cursor effects.

# Halloween Decor 0.3.3

- Rebuilt the knit folder icon from the supplied reference at its original wide proportions so the whole folder shape is visible.
- Used the exact bat silhouette from the supplied reference in both the folder style and app icon.
- Preserved folder artwork proportions in the preview and Finder icon canvas.

This historical build has no downloadable installer. The temporary Safari ZIP has also been removed.

# Halloween Decor 0.3.2

- Added a safe margin around folder artwork when applying icons so their edges remain visible in Finder.
- Updated the folder preview animation to match the Finder spacing.

This historical build has no downloadable installer. The temporary Safari ZIP has also been removed.

# Halloween Decor 0.3.1

- Replaced the app's pumpkin icon with the supplied style of soft black bat on a light background.
- Added the high-resolution icon artwork to the repository and updated the icon generator.

This historical build has no downloadable installer. The temporary Safari ZIP has also been removed.

# Halloween Decor 0.3.0

- Added seven autumn folder icon styles: maple bouquet, pumpkin, knit, stripes, original skeleton illustration, bat, and kitten with pumpkin.
- Assigns a random style to each Desktop folder when enabled and keeps that assignment stable until the effect is disabled.
- Added a folder-style preview montage to the README and show all seven styles in the app's looping preview.

This historical build has no downloadable installer. The Safari extension was a temporary development workflow.

# Halloween Decor 0.2.1

The six cards now use native macOS switches instead of text buttons. Clicking anywhere on a card still toggles its effect. The window screenshot and installed app icon are included.

This historical build has no downloadable installer. The temporary Safari ZIP has also been removed.

## Earlier releases

### 0.2.0

The pumpkin now opens a native macOS window with six independent cards. Each card includes a short, silent looping video preview and applies its effect immediately. The window opens on launch and can be reopened from the menu bar pumpkin.

- Added Russian card labels, visible on/off buttons, and a single **Вернуть всё** action.
- Kept Safari webs, skeletons, and cursor, plus Mac stickers, Desktop folder icons, and wallpaper.
- Fixed a crash when hiding stickers by reusing their windows.
- Wallpaper changes now store a copy of the original image, so restoration can work even if its original file later disappears.
- Added a screenshot of the native window to the README.

This historical build has no downloadable installer. The Safari extension was a temporary development workflow.

This app was ad-hoc signed without a Developer ID and was not notarized. A packaged Safari extension and native messaging bridge require full Xcode and are not included in this release; this build uses a loopback bridge for local development.

### 0.1.0

First local development release with six independent effects controlled from a macOS menu bar app.

- Safari: corner cobwebs, occasional bursts of two or three falling skeletons, and a custom page cursor.
- macOS: three movable desktop stickers, autumn icons for folders on the Desktop, and an autumn wallpaper.
- Individual toggles and Restore Everything.

This historical build has no downloadable installer. The Safari extension was a temporary development workflow.

This app was ad-hoc signed without a Developer ID and was not notarized. The packaged Safari extension and native messaging bridge require full Xcode and are not included in this release; this build uses a loopback bridge for local development.
