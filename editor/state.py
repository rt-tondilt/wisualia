# This file holds the global state, and GUI bindings that modify it.

from enum import Enum
import os.path
import os
import sys
import webbrowser

import cairo
from gi.repository import Gdk
import mypy
from worker import DrawRequest, Zoom
import audio
import dir_tools
# NB: There is one more import in the middle of this file.


# Some globals.
file_name = None #type: Optional[str]
buffer_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 100, 100)
request = DrawRequest(0, 200, 200, Zoom(40, (-4,-4)), False)
compile_needed = False



running = False
playing = False

# We can't initialize it right now, because loop.py needs to access globals
# defined in this file.
loop = None

def draw(widget, cr):
    cr.set_source_rgb(1,1,1)
    cr.paint()
    cr.set_source_surface(buffer_surface)
    cr.paint()

def change_size(widget, event):
    global request
    request.x = event.width
    request.y = event.height
    loop.start()

def change_time(widget):
    global request
    time = scale.get_value()
    request.t = time
    if playing:
        audio.try_play_from(time)
    loop.start()

def change_zoom(widget, event):
    global request
    if running:
        if event.direction == Gdk.ScrollDirection.UP:
            if request.zoom.k < 5000:
                request.zoom.combine(Zoom(1.1, (event.x, event.y)))
        elif event.direction == Gdk.ScrollDirection.DOWN:
            if request.zoom.k > 10:
                request.zoom.combine(Zoom(1/1.1, (event.x, event.y)))
        else: assert False
        loop.start()


def drag_handler(widget, event):
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



def grid_callback(_):
    global request
    request.grid = grid_button.get_active()
    loop.start()
def home_callback(_):
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
        if running:
            switch_running(None)
        if playing:
            switch_playing(None)
    dialog.destroy()

def save_file(widget):
    print('Turvalisuse põhjustel pole teostatud.')

# TODO: The result gets overwritten if playing is True.
def typecheck(_):
    if playing: switch_playing(None)
    if running: switch_running(None)
    loop.start()

    if file_name is None:
        output_buffer.set_text('File name missing.')
        return

    code = input_buffer.get_text(input_buffer.get_start_iter(), input_buffer.get_end_iter(), True)
    with open(file_name, 'w') as f:
        f.write(code)

    stdout, stderr, exitcode = mypy.api.run([file_name, '--config-file','mypy_user.ini'])
    result = stdout+stderr
    if result == '':
        result = 'Typecheck: No errors were found.'

    output_buffer.set_text(str(result).replace('\n', '\n\n'))

def show_help(_):
    webbrowser.open(os.path.abspath('../docs/_build/index.html'))
def switch_playing(_):
    global playing
    playing = not playing
    if playing:
        play_button.set_image(pause_icon)
    else:
        play_button.set_image(play_icon)
    loop.start()

def switch_running(_):
    global running
    if not running:
        running = True
        run_button.set_stock_id('gtk-stop')
        run_button.set_label('Abort')
    else:
        running = False
        run_button.set_stock_id('gtk-execute')
        run_button.set_label('Run')
    loop.start()

drawing_area.set_events(Gdk.EventMask.SCROLL_MASK |
                        Gdk.EventMask.BUTTON_PRESS_MASK |
                        Gdk.EventMask.BUTTON_MOTION_MASK)

def compile_buffer(buffer, start, end):
    global compile_needed
    compile_needed = True
    if running:
        loop.start()

# Connect events with callbacks.
play_button.connect('clicked', switch_playing)
run_button.connect('clicked', switch_running)
input_buffer.connect('highlight-updated', compile_buffer)
save_button.connect('activate', save_file)
open_button.connect('activate', open_file)
export_button.connect('clicked', export)
grid_button.connect('clicked', grid_callback)
home_button.connect('clicked', home_callback)
typecheck_button.connect('clicked', typecheck)
help_button.connect('clicked', show_help)
drawing_area.connect('draw', draw)
drawing_area.connect('configure-event', change_size)
drawing_area.connect('scroll-event', change_zoom)
drawing_area.connect('button-press-event', drag_handler)
drawing_area.connect('motion-notify-event', drag_handler)
scale.connect('value-changed', change_time)
