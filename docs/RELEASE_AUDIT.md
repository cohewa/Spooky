# Spooky release audit — 2026-10-22

## Checked locally

- `scripts/check-release-technical.sh` completed: metadata and source syntax passed, the app built, ad-hoc code signature verified, and all five bundled preview videos were readable.
- The installed development app launches. Its local settings bridge returns the five expected switches, sets `X-Content-Type-Options: nosniff`, and does not expose `Access-Control-Allow-Origin: *`.
- The active Desktop wallpaper, while the wallpaper switch is on, has the same bytes as the new bundled pumpkin artwork.
- The built app contains 52 independent sticker PNGs and six new folder icons; it does not contain the removed `halloween-objects.png` or `ghost.png` source files.
- The overview video is 18 seconds. Frames across all five effects were inspected visually; the app screenshot shows only the isolated Spooky window and has no screenshot metadata.
- Current text files and all 14 existing Git commits were scanned for common API-token formats, private-key headers, and local home paths; no matches were found. This is a targeted scan, not a guarantee against every secret format.
- On 2026-10-14, the earlier user-supplied candy cursor was restored to the Mac and Safari assets. The project owner confirmed redistribution rights and chose MIT for all project artwork. The app icon, web, and loader bat were replaced with original project artwork.

## Public GitHub state

The repository is already public. Its 11 existing Halloween Decor releases had 22 uploaded Mac and Safari ZIPs. The latest archive, `v0.4.2`, was inspected without running it: its app had an ad-hoc signature, no Developer ID team identifier, and Gatekeeper assessment returned `rejected`.

On 2026-10-14, all 22 ZIPs were backed up locally in the Git-ignored `dist/legacy-release-backup/` directory and their sizes and SHA-256 hashes matched GitHub's release metadata. The uploaded ZIPs were then deleted. A fresh GitHub API read confirmed that all 11 release pages remain, each has zero uploaded assets, and each description warns that the old builds are not installable Spooky releases. GitHub's automatically generated source archives remain available through the preserved tags; they can contain earlier artwork.

On 2026-10-22, version 0.5.24 source and new feature media were pushed to `cohewa/Spooky`. Apple issued a Developer ID Application certificate for the project owner; its private key is in the local login Keychain, and the temporary key and PKCS#12 files were removed from the working directory. The build script now produces a universal Intel/Apple Silicon binary targeting macOS 13. The signed download still requires notarization, stapling, and a Gatekeeper check before it can be published.

## Still required before a binary release

1. Store an Apple notarytool credential in the local Keychain, then run and review `scripts/package-release.sh`.
2. Package the Safari Web Extension in a signed containing app if the binary release advertises Safari support.
3. Verify the actual signed archive on a clean Mac, including Desktop restoration, multiple displays, Safari permissions, and Gatekeeper behavior.

The 0.5.23 source preview remains available without an installable ZIP. A 0.5.24 installable ZIP must not be uploaded until notarization passes. The Safari extension remains a development-only component of the public source tree.
