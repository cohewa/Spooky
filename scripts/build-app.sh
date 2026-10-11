#!/bin/zsh
set -euo pipefail
cd "${0:A:h}/.."
mkdir -p 'build/Halloween Decor.app/Contents/MacOS' 'build/Halloween Decor.app/Contents/Resources'
swiftc -O -framework AppKit -framework AVFoundation -framework Network -o 'build/Halloween Decor.app/Contents/MacOS/Halloween Decor' macos/HalloweenDecor.swift
cp macos/Info.plist 'build/Halloween Decor.app/Contents/Info.plist'
cp macos/HalloweenDecor.icns 'build/Halloween Decor.app/Contents/Resources/'
mkdir -p 'build/Halloween Decor.app/Contents/Resources/Previews'
cp macos/Previews/*.mp4 'build/Halloween Decor.app/Contents/Resources/Previews/'
mkdir -p 'build/Halloween Decor.app/Contents/Resources/FolderStyles'
cp macos/FolderStyles/*.png 'build/Halloween Decor.app/Contents/Resources/FolderStyles/'
mkdir -p 'build/Halloween Decor.app/Contents/Resources/WebDecor'
cp macos/WebDecor/*.png 'build/Halloween Decor.app/Contents/Resources/WebDecor/'
codesign --force --deep --sign - 'build/Halloween Decor.app'
echo 'Built build/Halloween Decor.app'
