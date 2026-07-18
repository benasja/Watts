//! watts — live charging/discharging wattage in the macOS menu bar.
//!
//! Polls the battery controller (AppleSmartBattery via `ioreg`) every few
//! seconds and shows the actual power flowing in or out of the battery:
//!   ⚡ 64W   charging at 64 W
//!   🔋 8.4W  running on battery, drawing 8.4 W
//!   🔌       plugged in, battery full / not charging

use std::process::Command;
use std::time::Duration;

use tao::event_loop::{ControlFlow, EventLoopBuilder};
use tray_icon::{
    menu::{Menu, MenuEvent, MenuItem, PredefinedMenuItem},
    TrayIconBuilder,
};

#[cfg(target_os = "macos")]
use tao::platform::macos::{ActivationPolicy, EventLoopExtMacOS};

const POLL_INTERVAL: Duration = Duration::from_secs(3);

#[derive(Debug, Clone, Default)]
struct BatteryReading {
    external_connected: bool,
    is_charging: bool,
    fully_charged: bool,
    battery_percent: Option<i64>,
    /// Power flowing into (+) or out of (-) the battery, in watts.
    battery_watts: Option<f64>,
    /// Rated wattage of the connected power adapter, if any.
    adapter_watts: Option<i64>,
}

#[derive(Debug)]
enum UserEvent {
    Reading(Box<Option<BatteryReading>>),
    MenuEvent(MenuEvent),
}

fn plist_i64(dict: &plist::Dictionary, key: &str) -> Option<i64> {
    match dict.get(key) {
        Some(plist::Value::Integer(n)) => n
            .as_signed()
            .or_else(|| n.as_unsigned().map(|u| u as i64)),
        _ => None,
    }
}

fn plist_bool(dict: &plist::Dictionary, key: &str) -> Option<bool> {
    match dict.get(key) {
        Some(plist::Value::Boolean(b)) => Some(*b),
        _ => None,
    }
}

fn read_battery() -> Option<BatteryReading> {
    let output = Command::new("ioreg")
        .args(["-arn", "AppleSmartBattery"])
        .output()
        .ok()?;
    if !output.status.success() || output.stdout.is_empty() {
        return None;
    }

    let value: plist::Value = plist::from_bytes(&output.stdout).ok()?;
    let dict = value
        .as_array()?
        .first()?
        .as_dictionary()?;

    let voltage_mv = plist_i64(dict, "Voltage")?;
    let amperage_ma = plist_i64(dict, "Amperage")?;
    let battery_watts = (voltage_mv as f64 / 1000.0) * (amperage_ma as f64 / 1000.0);

    let adapter_watts = dict
        .get("AdapterDetails")
        .and_then(|v| v.as_dictionary())
        .and_then(|d| plist_i64(d, "Watts"))
        .filter(|w| *w > 0);

    Some(BatteryReading {
        external_connected: plist_bool(dict, "ExternalConnected").unwrap_or(false),
        is_charging: plist_bool(dict, "IsCharging").unwrap_or(false),
        fully_charged: plist_bool(dict, "FullyCharged").unwrap_or(false),
        battery_percent: plist_i64(dict, "CurrentCapacity"),
        battery_watts: Some(battery_watts),
        adapter_watts,
    })
}

fn tray_title(reading: &Option<BatteryReading>) -> String {
    let Some(r) = reading else {
        return "⚡ --".to_string();
    };
    let watts = r.battery_watts.unwrap_or(0.0);
    if r.external_connected {
        if r.is_charging && watts > 0.5 {
            format!("⚡ {watts:.0}W")
        } else {
            "🔌".to_string()
        }
    } else {
        format!("🔋 {:.1}W", watts.abs())
    }
}

fn detail_lines(reading: &Option<BatteryReading>) -> [String; 3] {
    let Some(r) = reading else {
        return [
            "State: no battery data".into(),
            "Battery: --".into(),
            "Adapter: --".into(),
        ];
    };
    let state = if r.external_connected {
        if r.is_charging {
            "Charging"
        } else if r.fully_charged {
            "Plugged in — full"
        } else {
            "Plugged in — not charging"
        }
    } else {
        "On battery"
    };
    let flow = match r.battery_watts {
        Some(w) if w > 0.5 => format!(" · {w:.1} W in"),
        Some(w) if w < -0.5 => format!(" · {:.1} W out", w.abs()),
        _ => String::new(),
    };
    let battery = match r.battery_percent {
        Some(p) => format!("Battery: {p}%{flow}"),
        None => format!("Battery: --{flow}"),
    };
    let adapter = match r.adapter_watts {
        Some(w) => format!("Adapter: {w} W"),
        None => "Adapter: none".into(),
    };
    [format!("State: {state}"), battery, adapter]
}

fn main() {
    #[cfg(not(target_os = "macos"))]
    {
        eprintln!("watts currently supports macOS only");
        std::process::exit(1);
    }

    #[cfg(target_os = "macos")]
    {
        let mut event_loop = EventLoopBuilder::<UserEvent>::with_user_event().build();
        // Menu-bar accessory: no Dock icon, no app menu.
        event_loop.set_activation_policy(ActivationPolicy::Accessory);

        let proxy = event_loop.create_proxy();
        MenuEvent::set_event_handler(Some({
            let proxy = proxy.clone();
            move |event: MenuEvent| {
                let _ = proxy.send_event(UserEvent::MenuEvent(event));
            }
        }));

        let menu = Menu::new();
        let state_item = MenuItem::new("State: …", false, None);
        let battery_item = MenuItem::new("Battery: …", false, None);
        let adapter_item = MenuItem::new("Adapter: …", false, None);
        let quit_item = MenuItem::new("Quit Watts", true, None);
        menu.append_items(&[
            &state_item,
            &battery_item,
            &adapter_item,
            &PredefinedMenuItem::separator(),
            &quit_item,
        ])
        .expect("failed to build menu");
        let quit_id = quit_item.id().clone();

        let tray = TrayIconBuilder::new()
            .with_menu(Box::new(menu))
            .with_title("⚡ --")
            .build()
            .expect("failed to create tray icon");

        // Poll the battery off the main thread; deliver results via the proxy.
        std::thread::spawn(move || loop {
            let reading = read_battery();
            if proxy
                .send_event(UserEvent::Reading(Box::new(reading)))
                .is_err()
            {
                break;
            }
            std::thread::sleep(POLL_INTERVAL);
        });

        event_loop.run(move |event, _, control_flow| {
            *control_flow = ControlFlow::Wait;

            if let tao::event::Event::UserEvent(user_event) = event {
                match user_event {
                    UserEvent::Reading(reading) => {
                        tray.set_title(Some(tray_title(&reading)));
                        let [state, battery, adapter] = detail_lines(&reading);
                        state_item.set_text(state);
                        battery_item.set_text(battery);
                        adapter_item.set_text(adapter);
                    }
                    UserEvent::MenuEvent(menu_event) => {
                        if menu_event.id() == &quit_id {
                            *control_flow = ControlFlow::Exit;
                        }
                    }
                }
            }
        });
    }
}
