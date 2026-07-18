# 🔋 WattageChecker - Laptop Charging Wattage Monitor

A simple, cross-platform desktop application that displays your laptop's current charging wattage in real-time.

![Platform Support](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-blue)
![Python](https://img.shields.io/badge/Python-3.7%2B-green)
![License](https://img.shields.io/badge/License-MIT-blue)

---

## 🚀 **Download & Install**

### 📱 macOS (Recommended)
**Option 1: Professional Installer (.dmg)**
1. Download `WattageChecker-macOS.dmg` from [GitHub Releases](#)
2. Double-click the .dmg file to open it
3. Drag WattageChecker to Applications folder
4. Launch from Applications or Launchpad

**Option 2: Direct App Bundle (.zip)**  
1. Download `WattageChecker-macOS.zip` from [GitHub Releases](#)
2. Extract the zip file
3. Drag `WattageChecker.app` to Applications folder

### 💻 Windows
1. Download `WattageChecker-Windows-Setup.exe` from [GitHub Releases](#)
2. Double-click to run the installer
3. Follow the installation wizard
4. Launch from Start Menu or Desktop shortcut

### 🐧 Linux
1. Download `WattageChecker-Linux` from [GitHub Releases](#)
2. Make it executable: `chmod +x WattageChecker-Linux`
3. Run: `./WattageChecker-Linux`

---

## 🛠️ **For Developers**

### Build from Source
```bash
pip install pyinstaller
python3 build_packages.py
```

### Run Directly
```bash
python3 wattage_checker.py
```

---

## 🎯 What Does This Do?

WattageChecker shows you exactly how many watts your laptop is drawing while charging. Perfect for:
- ⚡ Monitoring charging efficiency
- 🔌 Comparing different chargers
- 📊 Understanding power consumption
- 🔋 Checking battery health

**Example Display:**
- `45.7 W` - Currently charging at 45.7 watts
- `Discharging` - Running on battery power
- `No battery found` - Desktop computer or battery not detected

## 🚀 Quick Start (For Users)

### Option 1: Download Pre-Built App (Easiest)

#### 📱 For macOS Users:
1. **Download** the `WattageChecker.app.zip` file
2. **Extract** the zip file (double-click it)
3. **Move** `WattageChecker.app` to your Applications folder
4. **Launch** by double-clicking the app
5. **First time only:** Right-click → "Open" → "Open" (to bypass security warning)

#### 💻 For Windows Users:
1. **Download** the `WattageChecker.exe` file
2. **Run** by double-clicking the .exe file
3. **First time only:** Click "More info" → "Run anyway" (if Windows Defender warns)

#### 🐧 For Linux Users:
1. **Download** the `WattageChecker` file
2. **Make executable:** Right-click → Properties → Permissions → "Allow executing as program"
   - OR in terminal: `chmod +x WattageChecker`
3. **Run** by double-clicking or: `./WattageChecker`

### Option 2: Run from Python Source

If you have Python installed:

```bash
# Download the script
curl -O https://raw.githubusercontent.com/your-repo/wattage_checker.py

# Run directly
python3 wattage_checker.py
```

## 🛠️ Building from Source

### Prerequisites
```bash
# Install Python 3.7 or newer
# Install PyInstaller
pip install pyinstaller
```

### Automatic Build (Recommended)
```bash
# Clone or download this repository
git clone https://github.com/your-repo/WattageChecker.git
cd WattageChecker

# Run the automated build script
python3 build_packages.py
```

The build script will:
- ✅ Detect your operating system
- ✅ Clean previous builds
- ✅ Create the appropriate package type
- ✅ Show you exactly where to find the result

### Manual Build

#### For macOS (.app bundle):
```bash
pyinstaller --onedir --windowed --name "WattageChecker" wattage_checker.py
# Result: dist/WattageChecker.app
```

#### For Windows (.exe file):
```bash
pyinstaller --onefile --windowed --name "WattageChecker" wattage_checker.py
# Result: dist/WattageChecker.exe
```

#### For Linux:
```bash
pyinstaller --onefile --windowed --name "WattageChecker" wattage_checker.py
# Result: dist/WattageChecker
```

## 📋 How It Works

### Windows
- Uses PowerShell WMI query: `(Get-WmiObject -Class BatteryStatus -Namespace root\wmi).ChargeRate`
- Converts milliwatts to watts automatically

### macOS  
- Uses `ioreg -r -c 'AppleSmartBattery'` command
- Prefers direct adapter wattage when available and charging
- Calculates watts from voltage (mV) × amperage (mA) as fallback
- Handles macOS signed/unsigned integer conversion correctly
- Positive amperage = charging, negative = discharging

### Linux
- Reads from `/sys/class/power_supply/BAT*/` filesystem
- Uses `power_now` directly, or calculates from `voltage_now` × `current_now`
- Checks charging status from `status` file

## 🎨 User Interface

The app features a clean, minimal interface:
- **Title:** "Current Charge Rate:"
- **Display:** Large, bold text showing wattage or status
- **Auto-update:** Refreshes every 3 seconds automatically
- **Colors:** 
  - 🟢 Green: Charging normally
  - 🟠 Orange: Discharging/not charging  
  - 🔴 Red: Error or no battery found

**Window:** Small (280x120), non-resizable, auto-updating

## 🔧 Troubleshooting

### ❌ "No battery found"
**This is normal for:**
- Desktop computers
- Some older laptops
- Laptops with removed batteries

**Try:**
- Ensure your laptop has a battery
- Check if battery is properly connected
- Try running as administrator (Windows) or with sudo (Linux)

### ⚠️ Security Warnings

#### macOS: "App can't be opened"
1. **Right-click** the app → **"Open"**
2. Click **"Open"** in the dialog
3. App will now open normally in the future

#### Windows: "Windows protected your PC"
1. Click **"More info"**
2. Click **"Run anyway"**
3. App will run normally

#### Linux: "Permission denied"
```bash
chmod +x WattageChecker
./WattageChecker
```

### 💻 Command Line Testing

Test the core functionality:

```bash
# Windows (PowerShell)
(Get-WmiObject -Class BatteryStatus -Namespace root\wmi).ChargeRate

# macOS
ioreg -r -c 'AppleSmartBattery' | grep -E '(Voltage|Amperage)'

# Linux
cat /sys/class/power_supply/BAT*/power_now
cat /sys/class/power_supply/BAT*/status
```

## 📂 File Structure

```
WattageChecker/
├── README.md              # 📖 Complete guide (this file)  
├── wattage_checker.py     # 🔋 Main application source
├── build_packages.py      # 🔨 Build script for all platforms
└── dist/                  # 📦 Built applications
    └── WattageChecker.app # macOS app bundle (auto-updates every 3s)
```

Simple and clean - just 3 essential files!

## 📦 **Creating Releases**

To create installers for distribution:

### Build All Platforms
```bash
# macOS (creates .dmg and .zip)
python3 create_installer.py

# Windows (creates installer script + .exe)
# 1. Build the .exe first:
pyinstaller --onefile --windowed wattage_checker.py
# 2. Create installer with Inno Setup using WattageChecker-installer.iss

# Linux 
pyinstaller --onefile --windowed wattage_checker.py
```

### Upload to GitHub Releases
1. Create a new release on GitHub
2. Upload these files:
   - `WattageChecker-macOS.dmg` (macOS installer)
   - `WattageChecker-macOS.zip` (macOS direct download)
   - `WattageChecker-Windows-Setup.exe` (Windows installer)
   - `WattageChecker-Linux` (Linux executable)
3. Users can now download and install without any command line usage!

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature-name`
3. **Test** on your platform
4. **Submit** a pull request

### Testing Checklist
- [ ] App launches without errors
- [ ] Displays correct wattage when charging
- [ ] Shows "Discharging" when on battery
- [ ] Auto-updates every 3 seconds
- [ ] Handles "no battery" gracefully
- [ ] Window appears correctly sized

## 📊 Technical Details

- **Language:** Python 3.7+
- **GUI Framework:** Tkinter (built-in)
- **Package Size:** 20-50 MB (includes Python runtime)
- **Dependencies:** None (for end users)
- **Update Frequency:** Manual refresh or on-demand

## 📞 Support

### Before Asking for Help:
1. ✅ Check the troubleshooting section above
2. ✅ Try the command-line tests for your platform
3. ✅ Ensure your laptop actually has a battery
4. ✅ Check if the issue occurs on battery vs. plugged in

### Reporting Issues:
Include in your report:
- Operating system and version
- Laptop make/model
- Error messages (if any)
- Whether you're on battery or plugged in
- Output from command-line tests

## 📄 License

MIT License - feel free to use, modify, and distribute.

---

## 🎉 Quick Success Checklist

**For Users:**
- [ ] Downloaded the right file for your OS
- [ ] Bypassed security warnings (first time only)
- [ ] App shows your charging wattage or "Discharging"

**For Developers:**
- [ ] Python 3.7+ installed
- [ ] PyInstaller installed (`pip install pyinstaller`)
- [ ] Built successfully with `python3 build_packages.py`
- [ ] App launches from dist/ folder

**Need help?** Check the troubleshooting section or the detailed instructions in `PACKAGING_INSTRUCTIONS.md`.

---

*Made with ❤️ for laptop users who want to know their charging wattage*
