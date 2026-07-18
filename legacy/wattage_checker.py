#!/usr/bin/env python3
"""
Cross-Platform Laptop Wattage Checker
A simple desktop application to display current laptop charging wattage.
Supports Windows, macOS, and Linux.
"""

import tkinter as tk
from tkinter import font
import subprocess
import platform
import os
import re


class WattageChecker:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_gui()
        
    def setup_gui(self):
        """Initialize the GUI components."""
        self.root.title("Wattage Checker")
        self.root.geometry("280x120")
        self.root.resizable(False, False)
        
        # Center the window
        self.root.eval('tk::PlaceWindow . center')
        
        # Static label
        label_font = font.Font(size=12)
        static_label = tk.Label(self.root, text="Current Charge Rate:", font=label_font)
        static_label.pack(pady=(20, 10))
        
        # Dynamic display label (large, bold)
        display_font = font.Font(size=16, weight="bold")
        self.display_label = tk.Label(self.root, text="Checking...", font=display_font, fg="blue")
        self.display_label.pack(pady=15)
        
        # Auto-update status label (small)
        status_font = font.Font(size=9)
        self.status_label = tk.Label(self.root, text="Updates every 3 seconds", font=status_font, fg="gray")
        self.status_label.pack(pady=(5, 10))
        
        # Start auto-updates
        self.auto_update()
    
    def get_wattage(self):
        """
        Get current wattage based on the operating system.
        Returns a tuple (wattage_float, display_string).
        """
        system = platform.system().lower()
        
        try:
            if system == "windows":
                return self._get_windows_wattage()
            elif system == "darwin":  # macOS
                return self._get_macos_wattage()
            elif system == "linux":
                return self._get_linux_wattage()
            else:
                return 0, f"Unsupported OS: {system}"
        except Exception as e:
            return 0, f"Error: {str(e)}"
    
    def _get_windows_wattage(self):
        """Get wattage on Windows using PowerShell WMI query."""
        try:
            # Run PowerShell command to get charging rate
            cmd = ["powershell", "-Command", 
                   "(Get-WmiObject -Class BatteryStatus -Namespace root\\wmi).ChargeRate"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode != 0:
                return 0, "No battery found"
            
            output = result.stdout.strip()
            if not output or output == "":
                return 0, "No battery found"
            
            # Convert milliwatts to watts
            charge_rate_mw = float(output)
            if charge_rate_mw <= 0:
                return 0, "Discharging"
            
            wattage = charge_rate_mw / 1000
            return wattage, f"{wattage:.1f} W"
            
        except subprocess.TimeoutExpired:
            return 0, "Command timeout"
        except ValueError:
            return 0, "Invalid data"
        except Exception as e:
            return 0, f"Windows error: {str(e)}"
    
    def _get_macos_wattage(self):
        """Get wattage on macOS using ioreg command."""
        try:
            # Run ioreg command to get battery information
            cmd = ["ioreg", "-r", "-c", "AppleSmartBattery"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode != 0:
                return 0, "No battery found"
            
            output = result.stdout
            
            # Check charging status first - this is the most reliable indicator
            charging_current_match = re.search(r'"ChargingCurrent"\s*=\s*(\d+)', output)
            
            if charging_current_match:
                charging_current = int(charging_current_match.group(1))
                if charging_current == 0:
                    # Not charging, device is on battery power
                    return 0, "Discharging"
            
            # If we're charging, try to get direct wattage from adapter
            adapter_watts_match = re.search(r'"Watts"\s*=\s*(\d+)', output)
            
            if adapter_watts_match and charging_current_match:
                charging_current = int(charging_current_match.group(1))
                if charging_current > 0:
                    adapter_watts = int(adapter_watts_match.group(1))
                    return adapter_watts, f"{adapter_watts:.1f} W"
            
            # Fallback: Parse voltage and amperage manually (for when ChargingCurrent > 0)
            voltage_match = re.search(r'"Voltage"\s*=\s*(\d+)', output)
            amperage_match = re.search(r'"(?:Instant)?Amperage"\s*=\s*(\d+)', output)
            
            if not voltage_match or not amperage_match:
                return 0, "Could not parse battery data"
            
            voltage_mv = int(voltage_match.group(1))
            amperage_raw = int(amperage_match.group(1))
            
            # Handle signed/unsigned conversion for amperage
            # macOS reports negative values as large unsigned integers
            if amperage_raw > 2**63:  # If it's a very large number, it's likely negative
                amperage_ma = amperage_raw - 2**64  # Convert to signed
            else:
                amperage_ma = amperage_raw
            
            # Convert to watts: (mV / 1000) * (mA / 1000)
            voltage_v = voltage_mv / 1000
            amperage_a = amperage_ma / 1000
            
            # Only calculate wattage if we have positive charging current
            if charging_current_match:
                charging_current = int(charging_current_match.group(1))
                if charging_current > 0:
                    wattage = voltage_v * abs(amperage_a)  # Use absolute value for calculation
                    return wattage, f"{wattage:.1f} W"
                else:
                    return 0, "Discharging"
            else:
                # Fallback if no ChargingCurrent field found
                if amperage_a <= 0:
                    return 0, "Discharging"
                wattage = voltage_v * abs(amperage_a)
                return wattage, f"{wattage:.1f} W"
            
        except subprocess.TimeoutExpired:
            return 0, "Command timeout"
        except ValueError:
            return 0, "Invalid data"
        except Exception as e:
            return 0, f"macOS error: {str(e)}"
    
    def _get_linux_wattage(self):
        """Get wattage on Linux using /sys/class/power_supply/."""
        try:
            power_supply_path = "/sys/class/power_supply/"
            
            if not os.path.exists(power_supply_path):
                return 0, "No power supply found"
            
            # Find battery directory (usually BAT0, BAT1, etc.)
            battery_dir = None
            for item in os.listdir(power_supply_path):
                if item.startswith("BAT"):
                    battery_dir = os.path.join(power_supply_path, item)
                    break
            
            if not battery_dir:
                return 0, "No battery found"
            
            # Try to read power_now directly (in microwatts)
            power_now_path = os.path.join(battery_dir, "power_now")
            if os.path.exists(power_now_path):
                with open(power_now_path, 'r') as f:
                    power_uw = int(f.read().strip())
                
                # Check if charging
                status_path = os.path.join(battery_dir, "status")
                if os.path.exists(status_path):
                    with open(status_path, 'r') as f:
                        status = f.read().strip().lower()
                    
                    if status != "charging":
                        return 0, "Discharging"
                
                if power_uw <= 0:
                    return 0, "Discharging"
                
                wattage = power_uw / 1000000  # Convert microwatts to watts
                return wattage, f"{wattage:.1f} W"
            
            # Fallback: calculate from voltage and current
            voltage_path = os.path.join(battery_dir, "voltage_now")
            current_path = os.path.join(battery_dir, "current_now")
            
            if os.path.exists(voltage_path) and os.path.exists(current_path):
                with open(voltage_path, 'r') as f:
                    voltage_uv = int(f.read().strip())
                with open(current_path, 'r') as f:
                    current_ua = int(f.read().strip())
                
                # Check charging status
                status_path = os.path.join(battery_dir, "status")
                if os.path.exists(status_path):
                    with open(status_path, 'r') as f:
                        status = f.read().strip().lower()
                    
                    if status != "charging":
                        return 0, "Discharging"
                
                if current_ua <= 0:
                    return 0, "Discharging"
                
                # Convert microvolts and microamps to watts
                voltage_v = voltage_uv / 1000000
                current_a = current_ua / 1000000
                wattage = voltage_v * current_a
                
                return wattage, f"{wattage:.1f} W"
            
            return 0, "Could not read battery data"
            
        except (OSError, ValueError) as e:
            return 0, f"Linux error: {str(e)}"
        except Exception as e:
            return 0, f"Unexpected error: {str(e)}"
    
    def auto_update(self):
        """Automatically update the display every 3 seconds."""
        # Get current wattage
        wattage, display_text = self.get_wattage()
        
        # Set color based on result
        if "error" in display_text.lower() or "not found" in display_text.lower():
            color = "red"
        elif display_text == "Discharging" or wattage == 0:
            color = "orange"
        else:
            color = "green"
        
        # Update display
        self.display_label.config(text=display_text, fg=color)
        
        # Schedule next update in 3 seconds (3000 milliseconds)
        self.root.after(3000, self.auto_update)
    
    def run(self):
        """Start the application."""
        self.root.mainloop()


def main():
    """Main entry point."""
    app = WattageChecker()
    app.run()


if __name__ == "__main__":
    main()
