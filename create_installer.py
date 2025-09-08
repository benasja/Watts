#!/usr/bin/env python3
"""
Create installers for WattageChecker
- macOS: Creates a .dmg installer
- Windows: Creates installer script for Inno Setup
"""

import subprocess
import platform
import os
import sys


def create_macos_dmg():
    """Create a .dmg installer for macOS."""
    print("🍎 Creating macOS .dmg installer...")
    
    app_path = "dist/WattageChecker.app"
    dmg_path = "dist/WattageChecker-macOS.dmg"
    
    if not os.path.exists(app_path):
        print("❌ WattageChecker.app not found. Run 'python3 build_packages.py' first.")
        return False
    
    # Remove existing DMG
    if os.path.exists(dmg_path):
        os.remove(dmg_path)
    
    try:
        # Create DMG using hdiutil
        cmd = [
            "hdiutil", "create",
            "-volname", "WattageChecker",
            "-srcfolder", app_path,
            "-ov", "-format", "UDZO",
            dmg_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Created: {dmg_path}")
            print("   Users can download this .dmg file and install normally")
            return True
        else:
            print(f"❌ Failed to create DMG: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating DMG: {e}")
        return False


def create_windows_installer_script():
    """Create an Inno Setup script for Windows installer."""
    print("🪟 Creating Windows installer script...")
    
    inno_script = """
; WattageChecker Windows Installer Script
; Requires Inno Setup: https://jrsoftware.org/isinfo.php

[Setup]
AppName=WattageChecker
AppVersion=1.0
AppPublisher=WattageChecker
AppPublisherURL=https://github.com/your-username/WattageChecker
DefaultDirName={autopf}\\WattageChecker
DefaultGroupName=WattageChecker
OutputBaseFilename=WattageChecker-Windows-Setup
OutputDir=dist
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\\WattageChecker.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\\WattageChecker"; Filename: "{app}\\WattageChecker.exe"
Name: "{group}\\{cm:UninstallProgram,WattageChecker}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\\WattageChecker"; Filename: "{app}\\WattageChecker.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\\WattageChecker.exe"; Description: "{cm:LaunchProgram,WattageChecker}"; Flags: nowait postinstall skipifsilent
"""
    
    script_path = "WattageChecker-installer.iss"
    
    with open(script_path, 'w') as f:
        f.write(inno_script)
    
    print(f"✅ Created: {script_path}")
    print("   Windows users can:")
    print("   1. Install Inno Setup (https://jrsoftware.org/isinfo.php)")
    print("   2. Build the Windows .exe first")
    print("   3. Compile this script to create Setup.exe")
    
    return True


def create_github_release_package():
    """Create a zip package for GitHub releases."""
    print("📦 Creating GitHub release package...")
    
    if platform.system().lower() == "darwin":
        # Create compressed app for GitHub
        try:
            subprocess.run([
                "zip", "-r", "dist/WattageChecker-macOS.zip", 
                "dist/WattageChecker.app"
            ], check=True)
            print("✅ Created: dist/WattageChecker-macOS.zip")
            print("   This can be uploaded to GitHub releases")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to create zip package")
            return False
    
    return True


def main():
    """Main installer creation process."""
    print("🚀 WattageChecker Installer Creator")
    print("=" * 50)
    
    system = platform.system().lower()
    
    if system == "darwin":
        # macOS
        success = True
        success &= create_macos_dmg()
        success &= create_github_release_package()
        
        if success:
            print("\n🎉 macOS installers created successfully!")
            print("\nFor distribution:")
            print("  • dist/WattageChecker-macOS.dmg    (Professional installer)")
            print("  • dist/WattageChecker-macOS.zip    (GitHub release)")
        
    elif system == "windows":
        # Windows
        print("First, build the Windows executable:")
        print("  python build_packages.py")
        print("\nThen create installer:")
        create_windows_installer_script()
        
    else:
        print("Creating installer scripts for all platforms...")
        create_windows_installer_script()
        print("\nFor Linux: Users typically prefer the standalone executable")
    
    print(f"\n📋 Next steps for distribution:")
    print("1. Upload installers to GitHub Releases")
    print("2. Users download and install normally (no command line needed)")
    print("3. Add download links to README.md")


if __name__ == "__main__":
    main()
