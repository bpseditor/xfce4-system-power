#!/usr/bin/python3
"""Install standalone widget without applying a desktop theme."""
from pathlib import Path
import shutil
root=Path(__file__).resolve().parent; home=Path.home()
dest=home/'.local/bin/system-power-widget'; dest.parent.mkdir(parents=True,exist_ok=True)
shutil.copy2(root/'bin/system-power-widget',dest)
config=home/'.config/system-power-widget/settings.json'; config.parent.mkdir(parents=True,exist_ok=True)
if not config.exists(): shutil.copy2(root/'config/widget.json',config)
entry=home/'.local/share/applications/system-power-widget.desktop'; entry.parent.mkdir(parents=True,exist_ok=True)
entry.write_text(f'[Desktop Entry]\nType=Application\nName=System & Power\nExec="{dest}" --window\nIcon=utilities-system-monitor\nTerminal=false\nCategories=System;Monitor;\n')
print('Installed. Existing Genmon panel entry is preserved. On a new panel add Genmon with command '+str(dest))
