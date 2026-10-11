# Halloween Decor 0.2.0

The pumpkin now opens a native macOS window with six independent cards. Each card includes a short, silent looping video preview and applies its effect immediately. The window opens on launch and can be reopened from the menu bar pumpkin.

- Added Russian card labels, visible on/off buttons, and a single **Вернуть всё** action.
- Kept Safari webs, skeletons, and cursor, plus Mac stickers, Desktop folder icons, and wallpaper.
- Fixed a crash when hiding stickers by reusing their windows.
- Wallpaper changes now store a copy of the original image, so restoration can work even if its original file later disappears.
- Added a screenshot of the native window to the README.

Build the app from source or unzip `Halloween-Decor-0.2.0-macOS.zip` and move the app to Applications. Load the `safari-extension` folder as a temporary extension in Safari. The extension is removed by Safari when it quits or after 24 hours. See README for exact steps and limitations.

This app is ad-hoc signed without a Developer ID, and it is unnotarized. macOS may require Open Anyway for the first launch. A packaged Safari extension and native messaging bridge require full Xcode and are not included in this release; this build uses a loopback bridge for local development.

## Earlier release

### 0.1.0

First local development release with six independent effects controlled from a macOS menu bar app.

- Safari: corner cobwebs, occasional bursts of two or three falling skeletons, and a custom page cursor.
- macOS: three movable desktop stickers, autumn icons for folders on the Desktop, and an autumn wallpaper.
- Individual toggles and Restore Everything.

Build the app from source or unzip `Halloween-Decor-0.1.0-macOS.zip` and move the app to Applications. Load the `safari-extension` folder as a temporary extension in Safari. The extension is removed by Safari when it quits or after 24 hours. See README for exact steps and limitations.

This app is ad-hoc signed without a Developer ID, and it is unnotarized. macOS may require Open Anyway for the first launch. The packaged Safari extension and native messaging bridge require full Xcode and are not included in this release; this build uses a loopback bridge for local development.
