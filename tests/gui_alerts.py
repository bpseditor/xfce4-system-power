import runpy,contextlib,io,re
from pathlib import Path
from unittest.mock import patch
import gi
gi.require_version('Gtk','3.0');gi.require_version('Gdk','3.0')
from gi.repository import Gtk,GLib,Gdk
m=runpy.run_path(str(Path(__file__).resolve().parents[1]/'bin/system-power-widget'))
art=Path.home()/'.local/state/widget-ui-review'
art.mkdir(parents=True,exist_ok=True)
cfg=dict(m['DEFAULTS'],panel_font='Monospace 10')
_,real_rows,note=m['sample']()
readings=dict(status='Discharging',percent=55,cpu_temp=60,memory_percent=30)
def fake(panel_mode=False):
 warnings=m['warning_metrics'](cfg,**readings)
 fields=[('power',f'BAT {readings["percent"]}% −8.0W'),('cpu','C 12%'),('memory',f'M {readings["memory_percent"]}%'),('temperature',f'{readings["cpu_temp"]}°'),('network','↓ 12K ↑ 2K')]
 fake.warning=bool(warnings);fake.warnings=warnings;fake.markup=m['metric_markup'](fields,warnings,cfg,' · ')
 rows=list(real_rows);rows[0]=('Power source',f'Running on battery · {readings["percent"]}%');rows[10]=('Temperatures',f'CPU: {readings["cpu_temp"]} °C');rows[12]=('Memory',f'{readings["memory_percent"]}% used')
 return ' · '.join(v for _,v in fields),rows,note

def shot(win,name):
 w=win.get_window();pix=Gdk.pixbuf_get_from_window(w,0,0,w.get_width(),w.get_height());pix.savev(str(art/name),'png',[],[])
# Render the exact XML/Pango text produced for Genmon, at its configured font size.
win=Gtk.Window(title='Power panel warning review');box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=16,margin=18);win.add(box)
with patch.dict(m['panel'].__globals__,sample=fake,settings=lambda:cfg):
 for title,changes in [('Normal',{}),('Temperature only',{'cpu_temp':85}),('Memory only',{'memory_percent':95}),('Low battery only',{'percent':10}),('Simultaneous warnings',{'cpu_temp':85,'memory_percent':95,'percent':10})]:
  readings.update(status='Discharging',percent=55,cpu_temp=60,memory_percent=30);readings.update(changes)
  with contextlib.redirect_stdout(io.StringIO()) as output:m['panel']()
  text=re.search(r'<txt>(.*?)</txt>',output.getvalue(),re.S)[1]
  label=Gtk.Label(label=title,xalign=0);box.pack_start(label,False,False,0)
  line=Gtk.Label(xalign=0);line.set_markup(text);box.pack_start(line,False,False,0)
win.show_all()
loop=GLib.MainLoop()
def capture():shot(win,'power-panel-alerts.png');win.destroy();loop.quit();return False
GLib.timeout_add(250,capture);loop.run()
original_run=Gtk.Application.run
def run(app,args):
 def capture():
  win=app.get_active_window()
  def walk(w):
   yield w
   if isinstance(w,Gtk.Container):
    for c in w.get_children():yield from walk(c)
  tabs=next(w for w in walk(win) if isinstance(w,Gtk.Notebook));tabs.set_current_page(1)
  def finish():shot(win,'power-dashboard-alerts.png');win.destroy();app.quit();return False
  GLib.timeout_add(250,finish);return False
 GLib.timeout_add(250,capture);return original_run(app,args)
with patch.dict(m['window'].__globals__,sample=fake,settings=lambda:cfg),patch.object(Gtk.Application,'run',run):m['window']()
print('Panel and dashboard warning screenshots saved:',art)
