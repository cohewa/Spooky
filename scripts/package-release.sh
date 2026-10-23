#!/bin/zsh
set -euo pipefail
cd "${0:A:h}/.."

if [[ -z "${SPOOKY_DEVELOPER_ID:-}" || -z "${SPOOKY_NOTARY_PROFILE:-}" ]]; then
  echo 'Set SPOOKY_DEVELOPER_ID and SPOOKY_NOTARY_PROFILE before packaging.' >&2
  exit 1
fi
if ! xcrun --find notarytool >/dev/null 2>&1; then
  echo 'Apple notarytool is required.' >&2
  exit 1
fi
if ! xcrun --find stapler >/dev/null 2>&1; then
  echo 'Apple stapler is required.' >&2
  exit 1
fi
keychain_args=()
identity_keychain_args=()
if [[ -n "${SPOOKY_SIGNING_KEYCHAIN:-}" ]]; then
  keychain_args=(--keychain "$SPOOKY_SIGNING_KEYCHAIN")
  identity_keychain_args=("$SPOOKY_SIGNING_KEYCHAIN")
  if [[ ! -f "$SPOOKY_SIGNING_KEYCHAIN" ]]; then
    echo 'The requested signing keychain does not exist.' >&2
    exit 1
  fi
fi
if ! security find-identity -v -p codesigning "${identity_keychain_args[@]}" | grep -Fq "$SPOOKY_DEVELOPER_ID"; then
  echo 'The requested Developer ID Application identity is not in the keychain.' >&2
  exit 1
fi

./scripts/build-app.sh
app='build/Spooky.app'
version=$(/usr/libexec/PlistBuddy -c 'Print CFBundleShortVersionString' "$app/Contents/Info.plist")
archive="Spooky-${version}-macOS.zip"
mkdir -p dist
codesign --force --deep --options runtime --timestamp "${keychain_args[@]}" --sign "$SPOOKY_DEVELOPER_ID" "$app"
codesign --verify --deep --strict --verbose=2 "$app"
ditto -c -k --sequesterRsrc --keepParent "$app" "dist/$archive"
xcrun notarytool submit "dist/$archive" --keychain-profile "$SPOOKY_NOTARY_PROFILE" --wait
xcrun stapler staple "$app"
spctl --assess --type execute --verbose "$app"
ditto -c -k --sequesterRsrc --keepParent "$app" "dist/$archive"
(cd dist && shasum -a 256 "$archive" > "$archive.sha256")
echo "Ready for release review: dist/$archive and dist/$archive.sha256"
