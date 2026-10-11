#!/bin/zsh
set -euo pipefail
cd "${0:A:h}/.."
mkdir -p 'build/Halloween Decor.app/Contents/MacOS' 'build/Halloween Decor.app/Contents/Resources'
swiftc -O -framework AppKit -framework Network -o 'build/Halloween Decor.app/Contents/MacOS/Halloween Decor' macos/HalloweenDecor.swift
cp macos/Info.plist 'build/Halloween Decor.app/Contents/Info.plist'
echo 'Built build/Halloween Decor.app'
