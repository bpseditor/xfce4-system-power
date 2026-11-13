# System & Power

XFCE Genmon widget using Python 3, GTK3/PyGObject and xfconf. Reads battery, CPU, memory, temperature, disk and network counters from `/proc` and `/sys`. Panel fields have fixed widths; click to open readings and settings. Brightness uses login1; presentation mode uses XFCE Power Manager.

Install in an XFCE/X11 session:

```sh
python3 install.py
```

Requires Python 3, PyGObject, GTK3 and xfce4-genmon-plugin. Add Generic Monitor to the panel with command `~/.local/bin/system-power-widget` and a 5-second interval. Settings: `~/.config/system-power-widget/settings.json`. No telemetry is uploaded. Battery watts describe battery flow, not wall power.

Tests: `python3 -m unittest discover -s tests`.
