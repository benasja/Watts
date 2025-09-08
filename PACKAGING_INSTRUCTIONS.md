# Packaging Instructions

This document provides step-by-step instructions to package the `wattage_checker.py` script into native executables using PyInstaller.

## Prerequisites

First, ensure you have Python 3.7+ installed and install PyInstaller:

```bash
pip install pyinstaller
```

## For Windows (.exe files)

Open Command Prompt or PowerShell and navigate to the directory containing `wattage_checker.py`, then run:

```bash
# Navigate to the script directory
cd path\to\your\script

# Create a standalone .exe file
pyinstaller --onefile --windowed --name "WattageChecker" wattage_checker.py

# Optional: Add an icon (if you have a .ico file)
# pyinstaller --onefile --windowed --icon=icon.ico --name "WattageChecker" wattage_checker.py
```

**Flags explained:**
- `--onefile`: Creates a single .exe file instead of a directory
- `--windowed`: Prevents a console window from appearing (GUI-only mode)
- `--name "WattageChecker"`: Sets the name of the output executable

**Result:** The `.exe` file will be created in the `dist/` folder as `WattageChecker.exe`. This single file can be distributed to Windows users without requiring Python installation.

## For macOS (.app bundles)

Open Terminal and navigate to the directory containing `wattage_checker.py`, then run:

### Option 1: Optimized .app bundle (Recommended)
```bash
# Navigate to the script directory
cd /path/to/your/script

# Create a proper .app bundle (directory-based)
pyinstaller --onedir --windowed --name "WattageChecker" wattage_checker.py

# Optional: Add an icon (if you have a .icns file)
# pyinstaller --onedir --windowed --icon=icon.icns --name "WattageChecker" wattage_checker.py
```

### Option 2: Single file approach (with deprecation warning)
```bash
# Creates both single executable and .app bundle
pyinstaller --onefile --windowed --name "WattageChecker" wattage_checker.py
```

**Flags explained:**
- `--onedir`: Creates a directory-based .app bundle (recommended for macOS)
- `--onefile`: Creates a single executable + .app bundle (will show deprecation warning)
- `--windowed`: Creates a proper macOS .app bundle
- `--name "WattageChecker"`: Sets the name of the output application

**Result:** The `.app` bundle will be created in the `dist/` folder as `WattageChecker.app`. macOS users can double-click this to launch the application, and it behaves like a native macOS app.

## For Linux

Open Terminal and navigate to the directory containing `wattage_checker.py`, then run:

```bash
# Navigate to the script directory
cd /path/to/your/script

# Create a standalone executable
pyinstaller --onefile --windowed --name "WattageChecker" wattage_checker.py
```

The executable will be created in the `dist/` folder as `WattageChecker`.

## Distribution

After running PyInstaller:

### Windows Distribution
- **File:** `dist/WattageChecker.exe`
- **Type:** Single executable file
- **Distribution:** Send the `.exe` file to Windows users
- **Requirements:** No Python installation needed on target machines

### macOS Distribution
- **File:** `dist/WattageChecker.app` (appears as an application bundle)
- **Type:** Native macOS application
- **Distribution:** Compress the `.app` bundle into a `.zip` file for sharing
- **Installation:** Users drag the `.app` to their Applications folder
- **Requirements:** No Python installation needed on target machines

### Linux Distribution
- **File:** `dist/WattageChecker`
- **Type:** Single executable file
- **Distribution:** Send the executable file to Linux users
- **Requirements:** No Python installation needed on target machines

All executables contain the Python interpreter and all necessary dependencies.

## Notes

- The `--windowed` flag is important for GUI applications as it prevents a console window from appearing
- The first run of the executable may be slower as PyInstaller extracts files to a temporary directory
- The executable size will be larger (typically 20-50MB) as it includes the Python interpreter and all dependencies
- On macOS, you may need to allow the app in System Preferences > Security & Privacy if it's blocked

## Troubleshooting

If you encounter issues:

1. **Permission denied on macOS/Linux**: Make the executable file executable:
   ```bash
   chmod +x dist/WattageChecker
   ```

2. **Missing modules error**: Install any missing dependencies and re-run PyInstaller

3. **Large file size**: This is normal for PyInstaller executables as they bundle the Python interpreter

4. **Antivirus false positive**: Some antivirus software may flag PyInstaller executables. This is a known issue with packaged Python applications.
