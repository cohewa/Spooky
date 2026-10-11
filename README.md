# Halloween Decor

![Halloween Decor icon](safari-extension/icon-128.png)

A small, original Halloween decoration kit for macOS and Safari. A menu bar app controls six independent effects: Safari webs, falling skeletons, desktop stickers, autumn icons for folders on the Desktop, a wallpaper, and a Safari page cursor.

## Requirements

- macOS 13 or later, Safari 17 or later
- Apple Command Line Tools (`swiftc`)

## Build and run the Mac app

```sh
./scripts/build-app.sh
open "build/Halloween Decor.app"
```

The app creates its own wallpaper and icons. It stores backups in `~/Library/Application Support/Halloween Decor/`. Its menu has six toggles and **Restore Everything**. Changes to folder icons and wallpaper are restored when their toggles are switched off.

## Load the Safari extension

Safari → Settings → Advanced → Show features for web developers. Then Safari → Settings → Developer → Allow unsigned extensions → Add Temporary Extension… and choose `safari-extension`. Grant website access when Safari asks. Keep the Mac app running so Safari can read the six toggle states at `127.0.0.1:47831`.

Safari removes temporary extensions after quitting or after 24 hours. The Safari toolbar, address bar, Spotlight, and other apps' cursors are outside the extension's reach. The menu bar app remains installed locally until deleted.

## Install locally

Drag `build/Halloween Decor.app` to Applications. This local build is ad-hoc signed, without a Developer ID or notarization. macOS may require System Settings → Privacy & Security → Open Anyway on first launch. A distributable Safari extension needs an Xcode containing app and signing; this repository currently provides a temporary development extension.

## Privacy and safety

All effects and settings stay on the Mac. The bridge listens only on `127.0.0.1`. No analytics or remote requests. The app backs up icons for Desktop folders before changing them and records the current wallpaper for each display. **Restore Everything** restores recorded changes and turns all effects off. Do not delete the app's Application Support data while folder icons or wallpaper are active.

## Art

Vector art and drawings in this project are original and use a warm autumn palette. The attached Pinterest references informed the mood only; no Peanuts characters or third-party artwork is copied.

## Status

This is a local development build. See `docs/IMPLEMENTATION.md` for architecture and current limitations.
