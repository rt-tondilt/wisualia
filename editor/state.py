# This file holds the global state, and GUI bindings that modify it.

from enum import Enum
import os.path
import os
import sys
import webbrowser

import cairo
from gi.repository import Gdk
from worker import Request, Zoom
#from audio import Audio
import dir_tools
# NB: There is one more import in the middle of this file.


# Some globals.
file_name = None #type: Optional[str]
buffer_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 100, 100)
request = Request(0, 200, 200, Zoom(40, (-4,-4)), False)


# Variables to direct control flow in generators.
class Please(Enum): Run=1; Idle=2; Restart=3
engine = Please.Idle
playing = False

# We can't initialize it right now, because loop.py needs to access globals
# defined in this file.
loop = None

def update(_):
    loop.start()

def draw(widget, cr):
    cr.set_source_rgb(1,1,1)
    cr.paint()
    cr.set_source_surface(buffer_surface)
    cr.paint()

def run_engine(_):
    global engine
    if engine == Please.Idle:
        engine = Please.Run
    elif engine == Please.Run:
        engine = Please.Restart
    loop.start()

def abort_engine(_):
    global engine
    engine = Please.Idle
    loop.start()

def resize(widget, event):
    global request
    print('resize')
    request.x = event.width
    request.y = event.height
    loop.start()

def retime(widget):
    global request
    request.t = scale.get_value()
    loop.start()

def rezoom(widget, event):
    global request
    if engine == Please.Run:
        if event.direction == Gdk.ScrollDirection.UP:
            if request.zoom.k < 5000:
                request.zoom.combine(Zoom(1.1, (event.x, event.y)))
        elif event.direction == Gdk.ScrollDirection.DOWN:
            if request.zoom.k > 10:
                request.zoom.combine(Zoom(1/1.1, (event.x, event.y)))
        else: assert False
        loop.start()


def remotion(widget, event):
    global last_x, last_y # used in this function only
    if event.type == Gdk.EventType.BUTTON_PRESS:
        last_x = event.x
        last_y = event.y
    elif event.type == Gdk.EventType.MOTION_NOTIFY:
        request.zoom.b_x += event.x -last_x
        request.zoom.b_y += event.y - last_y
        last_x = event.x
        last_y = event.y
    # ignore GDK_2BUTTON_PRESS and GDK_2BUTTON_PRESS events
    loop.start()



def regrid(_):
    global request
    request.grid = grid_button.get_active()
    loop.start()
def home(_):
    global request
    request.zoom.k = 40
    request.zoom.b_x = request.x/2
    request.zoom.b_y = request.y/2
    loop.start()
def export(_):
    if file_name == None:
        return
    dirpath = os.path.dirname(file_name)
    libpath = dir_tools.get_dir('library')
    interpath = sys.executable #python interpreter path
    task = ('start cmd /c '
            '"cd {} && set PYTHONPATH=%PYTHONPATH%;{} && '
            '{} {} animate || '
            'pause"').format(dirpath, libpath, interpath, file_name)
    os.system(task)


# The following callbacks need to change the gui.
from gui import *

def open_file(widget):
    global file_name
    dialog = Gtk.FileChooserDialog("Ava", window,
        Gtk.FileChooserAction.OPEN,
        (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
         Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
    dialog.set_current_folder(dir_tools.get_dir('examples'))
    if dialog.run() == Gtk.ResponseType.OK:
        name = dialog.get_filename()
        with open(name, 'r') as f:
            input_buffer.set_text(f.read())
        file_name = name
        file_label.set_text(os.path.basename(name))

    dialog.destroy()

def save_file(widget):
    print('Turvalisuse põhjustel pole teostatud.')

def show_help(_):
    webbrowser.open(os.path.abspath('../docs/_build/index.html'))
def play(_):
    global playing
    playing = not playing
    if playing:
        play_button.set_image(pause_icon)
    else:
        play_button.set_image(play_icon)
    loop.start()

drawing_area.set_events(Gdk.EventMask.SCROLL_MASK |
                        Gdk.EventMask.BUTTON_PRESS_MASK |
                        Gdk.EventMask.BUTTON_MOTION_MASK)

# Connect events with callbacks.
play_button.connect('clicked', play)
run_button.connect('clicked', run_engine)
abort_button.connect('clicked', abort_engine)
save_button.connect('activate', save_file)
open_button.connect('activate', open_file)
export_button.connect('clicked', export)
grid_button.connect('clicked', regrid)
home_button.connect('clicked', home)
help_button.connect('clicked', show_help)
drawing_area.connect('draw', draw)
drawing_area.connect('configure-event', resize)
drawing_area.connect('scroll-event', rezoom)
drawing_area.connect('button-press-event', remotion)
drawing_area.connect('motion-notify-event', remotion)
scale.connect('value-changed', retime)
