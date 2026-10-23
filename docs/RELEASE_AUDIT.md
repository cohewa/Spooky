# Spooky release audit — 2026-10-23

## Checked locally

- `scripts/check-release-technical.sh` completed: metadata and source syntax passed, the app built, ad-hoc code signature verified, and all five bundled preview videos were readable.
- The installed development app launches. Its local settings bridge returns the five expected switches, sets `X-Content-Type-Options: nosniff`, and does not expose `Access-Control-Allow-Origin: *`.
- The active Desktop wallpaper, while the wallpaper switch is on, has the same bytes as the new bundled pumpkin artwork.
- The built app contains 52 independent sticker PNGs and six new folder icons; it does not contain the removed `halloween-objects.png` or `ghost.png` source files.
- The overview video is 18 seconds. Frames across all five effects were inspected visually; the app screenshot shows only the isolated Spooky window and has no screenshot metadata.
- At the earlier source audit, text files and the 14 Git commits then present were scanned for common API-token formats, private-key headers, and local home paths; no matches were found. This is a targeted scan, not a guarantee against every secret format.
- On 2026-10-14, the earlier user-supplied candy cursor was restored to the Mac and Safari assets. The project owner confirmed redistribution rights and chose MIT for all project artwork. The app icon and web were replaced with original project artwork; 0.5.24 uses a drawn peeking ghost for the applying indicator.
- Apple accepted notarization submission `9e86384c-cc03-4cdd-9c43-b2730c2f0227` for `Spooky-0.5.24-macOS.zip`. The ticket was stapled before the final archive was made.
- The final ZIP passed SHA-256 verification. After extracting it into a fresh temporary directory, `codesign --verify --deep --strict`, `xcrun stapler validate`, and `spctl --assess --type execute` passed; Gatekeeper reported `source=Notarized Developer ID`. The app reports version 0.5.24 and contains `x86_64` and `arm64` executables.

## Public GitHub state

The repository is already public. Its 11 existing Halloween Decor releases had 22 uploaded Mac and Safari ZIPs. The latest archive, `v0.4.2`, was inspected without running it: its app had an ad-hoc signature, no Developer ID team identifier, and Gatekeeper assessment returned `rejected`.

On 2026-10-14, all 22 ZIPs were backed up locally in the Git-ignored `dist/legacy-release-backup/` directory and their sizes and SHA-256 hashes matched GitHub's release metadata. The uploaded ZIPs were then deleted. A fresh GitHub API read confirmed that all 11 release pages remain, each has zero uploaded assets, and each description warns that the old builds are not installable Spooky releases. GitHub's automatically generated source archives remain available through the preserved tags; they can contain earlier artwork.

On 2026-10-22, version 0.5.24 source and new feature media were pushed to `cohewa/Spooky`. Apple issued a Developer ID Application certificate for the project owner. When the login Keychain did not allow unattended signing, a second certificate with the same Developer ID rights was issued and imported into a dedicated local Spooky keychain. Temporary private-key and PKCS#12 files were removed. The notarization profile is stored locally in Keychain. No signing credentials or keychain files are tracked by Git.

The [0.5.24 GitHub release](https://github.com/cohewa/Spooky/releases/tag/v0.5.24) contains the notarized, stapled universal Mac app ZIP and its SHA-256 checksum.

## Remaining follow-up

1. Package the Safari Web Extension in a signed containing app before advertising Safari support in a future binary release.
2. Perform an additional install and visual smoke check on a second Mac, including Desktop restoration and multiple displays.

The 0.5.23 source preview remains available without an installable ZIP. The Safari extension remains a development-only component of the public source tree.
