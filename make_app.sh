#!/bin/bash
# Builds Watts.app — a menu-bar-only app bundle you can add to Login Items.
set -euo pipefail

cargo build --release

APP="Watts.app"
rm -rf "$APP"
mkdir -p "$APP/Contents/MacOS"

cat > "$APP/Contents/Info.plist" <<'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>            <string>Watts</string>
    <key>CFBundleIdentifier</key>      <string>com.benasja.watts</string>
    <key>CFBundleVersion</key>         <string>1.0.0</string>
    <key>CFBundleShortVersionString</key> <string>1.0.0</string>
    <key>CFBundleExecutable</key>      <string>watts</string>
    <key>CFBundlePackageType</key>     <string>APPL</string>
    <key>LSMinimumSystemVersion</key>  <string>11.0</string>
    <key>LSUIElement</key>             <true/>
</dict>
</plist>
PLIST

cp target/release/watts "$APP/Contents/MacOS/watts"
codesign --force --sign - "$APP" 2>/dev/null || true

echo "Built $APP — drag it to /Applications and add it to Login Items."
