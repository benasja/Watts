# Watts ⚡

Live charging/discharging wattage in your **macOS menu bar**. Native, ~800 KB, no dependencies.

This is a ground-up Rust rewrite of the original Python/tkinter window app — instead of a floating window, the number now lives where it belongs: the menu bar.

| State | Menu bar shows |
|---|---|
| Charging | `⚡ 64W` — actual watts flowing into the battery |
| On battery | `🔋 8.4W` — current power draw from the battery |
| Plugged in, full | `🔌` |

Click it for details: charge state, battery percentage, power in/out, and the connected adapter's rated wattage.

## Why

macOS shows you the battery percentage, but not *how fast* you're charging — or whether that USB-C cable from the junk drawer is silently limiting you to 20 W. Plug in, glance at the menu bar, know immediately.

## Install

Requires [Rust](https://rustup.rs). Then:

```bash
git clone https://github.com/benasja/Watts.git
cd Watts
./make_app.sh
```

This produces **Watts.app** — drag it to `/Applications`, and add it to **System Settings → General → Login Items** to have it start automatically.

Or just run the binary directly:

```bash
cargo run --release
```

## How it works

Polls the battery controller (`AppleSmartBattery` via `ioreg`) every 3 seconds, parses the plist output, and computes real battery power as `Voltage × Amperage`. Signed amperage distinguishes charging from discharging. No kernel extensions, no elevated privileges, no network.

- [tao](https://github.com/tauri-apps/tao) event loop (Accessory activation policy — no Dock icon)
- [tray-icon](https://github.com/tauri-apps/tray-icon) menu bar item
- [plist](https://crates.io/crates/plist) parsing

## Legacy

The original cross-platform Python/tkinter version lives in [`legacy/`](legacy/).

## License

MIT
