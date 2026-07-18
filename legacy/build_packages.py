#!/usr/bin/env python3
"""
Build script to create native packages for all platforms.
Run this script to automatically create .app, .exe, and Linux executables.
"""

import subprocess
import platform
import sys
import os


def run_command(cmd):
    """Run a command and return success status."""
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {cmd}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {cmd}")
        print(f"Error: {e.stderr}")
        return False


def clean_build():
    """Clean previous build artifacts."""
    print("Cleaning previous builds...")
    for item in ["build", "dist", "*.spec"]:
        if os.path.exists(item):
            if os.path.isdir(item):
                run_command(f"rm -rf {item}")
            else:
                run_command(f"rm -f {item}")


def build_for_platform():
    """Build package for the current platform."""
    system = platform.system().lower()
    
    print(f"Building for {system}...")
    
    if system == "windows":
        # Windows: Create .exe file
        cmd = 'pyinstaller --onefile --windowed --name "WattageChecker" wattage_checker.py'
        if run_command(cmd):
            print("✓ Windows .exe created in dist/WattageChecker.exe")
        else:
            print("✗ Failed to create Windows .exe")
            
    elif system == "darwin":  # macOS
        # macOS: Create .app bundle (recommended approach)
        cmd = 'pyinstaller --onedir --windowed --name "WattageChecker" wattage_checker.py'
        if run_command(cmd):
            print("✓ macOS .app bundle created in dist/WattageChecker.app")
        else:
            print("✗ Failed to create macOS .app bundle")
            
    elif system == "linux":
        # Linux: Create executable
        cmd = 'pyinstaller --onefile --windowed --name "WattageChecker" wattage_checker.py'
        if run_command(cmd):
            print("✓ Linux executable created in dist/WattageChecker")
        else:
            print("✗ Failed to create Linux executable")
    else:
        print(f"✗ Unsupported platform: {system}")
        return False
    
    return True


def main():
    """Main build process."""
    print("Wattage Checker - Package Builder")
    print("=" * 40)
    
    # Check if PyInstaller is installed
    try:
        subprocess.run(["pyinstaller", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ PyInstaller not found. Please install it:")
        print("  pip install pyinstaller")
        sys.exit(1)
    
    # Clean previous builds
    clean_build()
    
    # Build for current platform
    if build_for_platform():
        print("\n✓ Build completed successfully!")
        print("Check the 'dist/' directory for your package.")
        
        system = platform.system().lower()
        if system == "darwin":
            print("\nTo distribute the macOS app:")
            print("1. Compress WattageChecker.app into a .zip file")
            print("2. Share the .zip file with macOS users")
            print("3. Users can extract and drag to Applications folder")
        elif system == "windows":
            print("\nTo distribute the Windows app:")
            print("1. Share the WattageChecker.exe file with Windows users")
            print("2. No installation required - just double-click to run")
        elif system == "linux":
            print("\nTo distribute the Linux app:")
            print("1. Share the WattageChecker file with Linux users")
            print("2. Make executable with: chmod +x WattageChecker")
            print("3. Run with: ./WattageChecker")
    else:
        print("\n✗ Build failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
