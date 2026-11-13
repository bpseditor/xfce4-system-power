# System & Power

XFCE Genmon widget using Python 3, GTK3/PyGObject and xfconf. Reads battery, CPU, memory, temperature, disk and network counters from `/proc` and `/sys`. Panel fields have fixed widths; click to open readings and settings. Brightness uses login1; presentation mode uses XFCE Power Manager.

Install in an XFCE/X11 session:

```sh
python3 install.py
```

Requires Python 3, PyGObject, GTK3 and xfce4-genmon-plugin. Add Generic Monitor to the panel with command `~/.local/bin/system-power-widget` and a 5-second interval. Settings: `~/.config/system-power-widget/settings.json`. No telemetry is uploaded. Battery watts describe battery flow, not wall power.

Tests: `python3 -m unittest discover -s tests`.

Panel preferences support a compact layout, font family/size, per-metric visibility and drag-and-drop or arrow-based ordering. Full telemetry remains in the hover tooltip. Display changes are saved with the always-visible Apply button; closing with unsaved edits offers to discard or keep editing. Settings are written atomically. Brightness and presentation mode take effect immediately.

Warnings color only the triggering battery, memory or temperature field. Multiple alerts are independent; the tooltip lists the measured values and thresholds, including hidden fields. The dashboard highlights the corresponding readings as well. Visual check with simulated readings: `python3 tests/gui_alerts.py`.
