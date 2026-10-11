# Halloween Decor 0.4.2

- Reduced both screen decorations to 60% of their previous size. The left web starts below the macOS menu bar; the pumpkin-and-bat garland now sits at the lower right above the Dock.
- Changed the dangling spider to black and softened the free ends of the web strands.
- Bats now fly diagonally from below the left side of the screen toward the upper right, once when Webs is enabled and once each hour afterward.
- The overlay uses a floating window level so the menu bar and Dock stay above it. Updated the card preview.

Build from source or unzip `Halloween-Decor-0.4.2-macOS.zip`.

# Halloween Decor 0.4.1

- Added a small bat loading indicator in the Mac window using the same silhouette as the app icon. Its wings flap while an effect is being applied or all effects are restored.
- The indicator also appears while Desktop folder icons are applied at launch. Reduce Motion keeps the bat still while retaining the status text.

Build from source or unzip `Halloween-Decor-0.4.1-macOS.zip`.

# Halloween Decor 0.4.0

- The Webs switch now decorates the entire Mac screen, including Safari and other apps, with a white left web and dangling spider plus the referenced pumpkin-and-bat garland on the right.
- Spider and garland move once per minute; a group of bats flies across the lower-right area when switched on and once per hour afterward. Decorations allow clicks to pass through.
- Updated the card video preview and removed duplicate Safari-only web artwork.

Build from source or unzip `Halloween-Decor-0.4.0-macOS.zip`. Safari still uses a temporary extension for the skeleton and cursor effects.

# Halloween Decor 0.3.3

- Rebuilt the knit folder icon from the supplied reference at its original wide proportions so the whole folder shape is visible.
- Used the exact bat silhouette from the supplied reference in both the folder style and app icon.
- Preserved folder artwork proportions in the preview and Finder icon canvas.

Build from source or unzip `Halloween-Decor-0.3.3-macOS.zip`. Safari still uses a temporary extension; `Halloween-Decor-0.3.3-Safari-temporary.zip` contains the browser extension.

# Halloween Decor 0.3.2

- Added a safe margin around folder artwork when applying icons so their edges remain visible in Finder.
- Updated the folder preview animation to match the Finder spacing.

Build from source or unzip `Halloween-Decor-0.3.2-macOS.zip`. Safari still uses a temporary extension; `Halloween-Decor-0.3.2-Safari-temporary.zip` contains the browser extension.

# Halloween Decor 0.3.1

- Replaced the app's pumpkin icon with the supplied style of soft black bat on a light background.
- Added the high-resolution icon artwork to the repository and updated the icon generator.

Build from source or unzip `Halloween-Decor-0.3.1-macOS.zip`. Safari still uses a temporary extension; `Halloween-Decor-0.3.1-Safari-temporary.zip` contains the browser extension.

# Halloween Decor 0.3.0

- Added seven autumn folder icon styles: maple bouquet, pumpkin, knit, stripes, original skeleton illustration, bat, and kitten with pumpkin.
- Assigns a random style to each Desktop folder when enabled and keeps that assignment stable until the effect is disabled.
- Added a folder-style preview montage to the README and show all seven styles in the app's looping preview.

Build the app from source or unzip `Halloween-Decor-0.3.0-macOS.zip` and move the app to Applications. Load the `safari-extension` folder as a temporary extension in Safari. The extension is removed by Safari when it quits or after 24 hours. See README for exact steps and limitations.

# Halloween Decor 0.2.1

The six cards now use native macOS switches instead of text buttons. Clicking anywhere on a card still toggles its effect. The window screenshot and installed app icon are included.

Build from source or unzip `Halloween-Decor-0.2.1-macOS.zip`. Safari still uses a temporary extension; `Halloween-Decor-0.2.1-Safari-temporary.zip` contains the same browser effects as 0.2.0.

## Earlier releases

### 0.2.0

The pumpkin now opens a native macOS window with six independent cards. Each card includes a short, silent looping video preview and applies its effect immediately. The window opens on launch and can be reopened from the menu bar pumpkin.

- Added Russian card labels, visible on/off buttons, and a single **Вернуть всё** action.
- Kept Safari webs, skeletons, and cursor, plus Mac stickers, Desktop folder icons, and wallpaper.
- Fixed a crash when hiding stickers by reusing their windows.
- Wallpaper changes now store a copy of the original image, so restoration can work even if its original file later disappears.
- Added a screenshot of the native window to the README.

Build the app from source or unzip `Halloween-Decor-0.2.0-macOS.zip` and move the app to Applications. Load the `safari-extension` folder as a temporary extension in Safari. The extension is removed by Safari when it quits or after 24 hours. See README for exact steps and limitations.

This app is ad-hoc signed without a Developer ID, and it is unnotarized. macOS may require Open Anyway for the first launch. A packaged Safari extension and native messaging bridge require full Xcode and are not included in this release; this build uses a loopback bridge for local development.

### 0.1.0

First local development release with six independent effects controlled from a macOS menu bar app.

- Safari: corner cobwebs, occasional bursts of two or three falling skeletons, and a custom page cursor.
- macOS: three movable desktop stickers, autumn icons for folders on the Desktop, and an autumn wallpaper.
- Individual toggles and Restore Everything.

Build the app from source or unzip `Halloween-Decor-0.1.0-macOS.zip` and move the app to Applications. Load the `safari-extension` folder as a temporary extension in Safari. The extension is removed by Safari when it quits or after 24 hours. See README for exact steps and limitations.

This app is ad-hoc signed without a Developer ID, and it is unnotarized. macOS may require Open Anyway for the first launch. The packaged Safari extension and native messaging bridge require full Xcode and are not included in this release; this build uses a loopback bridge for local development.
