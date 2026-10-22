#!/bin/zsh
set -euo pipefail
cd "${0:A:h}/.."
mkdir -p 'build/Spooky.app/Contents/MacOS' 'build/Spooky.app/Contents/Resources'
export CLANG_MODULE_CACHE_PATH="${CLANG_MODULE_CACHE_PATH:-$PWD/build/clang-module-cache}"
swiftc -O -target arm64-apple-macos13.0 -framework AppKit -framework AVFoundation -framework Network -o 'build/Spooky-arm64' macos/HalloweenDecor.swift
swiftc -O -target x86_64-apple-macos13.0 -framework AppKit -framework AVFoundation -framework Network -o 'build/Spooky-x86_64' macos/HalloweenDecor.swift
lipo -create 'build/Spooky-arm64' 'build/Spooky-x86_64' -output 'build/Spooky.app/Contents/MacOS/Spooky'
rm 'build/Spooky-arm64' 'build/Spooky-x86_64'
cp macos/Info.plist 'build/Spooky.app/Contents/Info.plist'
cp macos/HalloweenDecor.icns 'build/Spooky.app/Contents/Resources/'
cp macos/HalloweenDecorIcon.png 'build/Spooky.app/Contents/Resources/'
cp macos/CandyCursor.png 'build/Spooky.app/Contents/Resources/'
mkdir -p 'build/Spooky.app/Contents/Resources/Fonts'
rsync -a --delete macos/Fonts/ 'build/Spooky.app/Contents/Resources/Fonts/'
mkdir -p 'build/Spooky.app/Contents/Resources/Stickers'
rsync -a --delete macos/Stickers/ 'build/Spooky.app/Contents/Resources/Stickers/'
mkdir -p 'build/Spooky.app/Contents/Resources/Wallpaper'
rsync -a --delete macos/Wallpaper/ 'build/Spooky.app/Contents/Resources/Wallpaper/'
mkdir -p 'build/Spooky.app/Contents/Resources/Previews'
rsync -a --delete macos/Previews/ 'build/Spooky.app/Contents/Resources/Previews/'
mkdir -p 'build/Spooky.app/Contents/Resources/FolderStyles'
rsync -a --delete macos/FolderStyles/ 'build/Spooky.app/Contents/Resources/FolderStyles/'
mkdir -p 'build/Spooky.app/Contents/Resources/WebDecor'
rsync -a --delete macos/WebDecor/ 'build/Spooky.app/Contents/Resources/WebDecor/'
rm -rf 'build/Spooky.app/Contents/Resources/LoadingBat'
codesign --force --deep --sign - 'build/Spooky.app'
echo 'Built build/Spooky.app'
