# Halloween Decor 0.1.0

First local development release with six independent effects controlled from a macOS menu bar app.

- Safari: corner cobwebs, occasional bursts of two or three falling skeletons, and a custom page cursor.
- macOS: three movable desktop stickers, autumn icons for folders on the Desktop, and an autumn wallpaper.
- Individual toggles and Restore Everything.

Build the app from source or unzip `Halloween-Decor-0.1.0-macOS.zip` and move the app to Applications. Load the `safari-extension` folder as a temporary extension in Safari. The extension is removed by Safari when it quits or after 24 hours. See README for exact steps and limitations.

This app is ad-hoc signed without a Developer ID, and it is unnotarized. macOS may require Open Anyway for the first launch. The packaged Safari extension and native messaging bridge require full Xcode and are not included in this release; this build uses a loopback bridge for local development.
