#!/bin/zsh
set -euo pipefail
cd "${0:A:h}/.."

echo 'Checking source formatting and metadata…'
git diff --check
plutil -lint macos/Info.plist
python3 -m json.tool safari-extension/manifest.json >/dev/null
python3 - <<'PY'
from pathlib import Path
for path in Path('scripts').glob('*.py'):
    compile(path.read_bytes(), str(path), 'exec')
print('Python scripts: syntax OK')
PY

if command -v node >/dev/null; then
  node --check safari-extension/background.js
  node --check safari-extension/content.js
else
  echo 'Node.js unavailable: JavaScript syntax check skipped'
fi

echo 'Checking committed file names for local credentials…'
if git ls-files | rg -i '(^|/)(\.env(\.|$)|[^/]+\.(p12|pfx|p8|cer|pem|key|mobileprovision|provisionprofile)$)'; then
  echo 'Potential credential file is tracked. Stop before publishing.' >&2
  exit 1
fi

echo 'Building development app…'
./scripts/build-app.sh
codesign --verify --deep --strict build/Spooky.app

echo 'Checking bundled preview videos…'
for name in webs stickers folders wallpaper cursor; do
  file="build/Spooky.app/Contents/Resources/Previews/$name.mp4"
  test -s "$file"
  ffprobe -v error -select_streams v:0 -show_entries stream=width,height,duration -of default=nw=1 "$file" >/dev/null
done

echo 'Technical checks passed. Developer ID notarization, Safari packaging, and clean-Mac behavior remain separate release gates.'
