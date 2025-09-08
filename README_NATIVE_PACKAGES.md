# WattageChecker - Native Package Distribution

This directory contains everything needed to create native packages (.app for macOS, .exe for Windows) of the WattageChecker application.

## Quick Start

### For macOS users (.app bundle):
1. Download `WattageChecker.app` from the `dist/` folder
2. Drag it to your Applications folder
3. Double-click to launch
4. **First launch:** You may need to right-click → Open and confirm (macOS security)

### For Windows users (.exe file):
1. Download `WattageChecker.exe` from the `dist/` folder
2. Double-click to run
3. **First launch:** Windows may show a security warning - click "More info" → "Run anyway"

### For Linux users:
1. Download `WattageChecker` from the `dist/` folder
2. Make it executable: `chmod +x WattageChecker`
3. Run: `./WattageChecker`

## Building Your Own Package

If you want to build the packages yourself:

### Automatic Build (Recommended):
```bash
python3 build_packages.py
```

### Manual Build:

#### For macOS (.app bundle):
```bash
pip install pyinstaller
pyinstaller --onedir --windowed --name "WattageChecker" wattage_checker.py
```

#### For Windows (.exe file):
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "WattageChecker" wattage_checker.py
```

#### For Linux:
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "WattageChecker" wattage_checker.py
```

## Features

- **Cross-platform:** Works on Windows, macOS, and Linux
- **Battery detection:** Automatically detects laptop battery status
- **Real-time updates:** Shows current charging wattage
- **No dependencies:** Standalone executables require no Python installation
- **Native look:** Uses system-appropriate UI elements

## Platform-Specific Notes

### macOS
- The .app bundle is signed and should work on all modern macOS versions
- First launch may require right-click → Open due to Gatekeeper
- The app can be moved to Applications folder for permanent installation

### Windows
- The .exe file is self-contained and portable
- Windows Defender may show a warning for unknown executables
- No installation required - the .exe can be run from any location

### Linux
- Tested on Ubuntu, should work on most distributions
- Requires X11/Wayland for GUI display
- The executable needs execute permissions after download

## Troubleshooting

### "No battery found" error:
- This is normal for desktop computers without batteries
- Some laptops may not expose battery information properly

### Permission/Security warnings:
- **macOS:** Right-click the app → Open → Confirm
- **Windows:** Click "More info" → "Run anyway" in SmartScreen warning
- **Linux:** Ensure the file has execute permissions

### Application won't start:
1. Try running from terminal to see error messages
2. Ensure your OS is supported
3. Check if antivirus software is blocking the executable

## File Sizes

Typical package sizes:
- **macOS .app bundle:** ~30-50 MB
- **Windows .exe:** ~20-30 MB  
- **Linux executable:** ~20-30 MB

The larger size is due to bundling the Python interpreter and all dependencies.

## Source Code

The complete source code is available in `wattage_checker.py`. The application is built using:
- **Python 3.7+**
- **Tkinter** (for GUI)
- **Platform-specific system commands** (for battery data)

## Distribution

When sharing the application:
1. **macOS:** Compress the .app bundle into a .zip file
2. **Windows:** Share the .exe file directly
3. **Linux:** Share the executable file (ensure recipients know to make it executable)
