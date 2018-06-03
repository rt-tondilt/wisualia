# This file holds the global state, and GUI bindings that modify it.

from enum import Enum
import os.path
import os
import sys
import webbrowser

import cairo
from gi.repository import Gdk
from worker import DrawRequest, Zoom
import audio
from gui import *

# Some globals.
buffer_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 100, 100)
request = DrawRequest(0, 200, 200, Zoom(40, (-4,-4)), False)
compile_needed = False

running = False
playing = False


# We can't initialize it right now, because loop.py needs to access globals
# defined in this file.
loop = None


def compile_buffer(_buffer, _start, _end): #because it is highlight callback.
    global compile_needed
    compile_needed = True
    if running:
        loop.start()

def switch_playing(_widget):
    global playing
    playing = not playing
    if playing:
        play_button.set_image(pause_icon)
    else:
        play_button.set_image(play_icon)
    loop.start()

def switch_running(_widget):
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

def stop_running_and_playing():
    if running:
        switch_running(None)
    if playing:
        switch_playing(None)


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

def grid_callback(_widget):
    global request
    request.grid = grid_button.get_active()
    loop.start()

def home_callback(_widget):
    global request
    request.zoom.k = 40
    request.zoom.b_x = request.x/2
    request.zoom.b_y = request.y/2
    loop.start()

def show_help(_widget):
    webbrowser.open(os.path.abspath('../docs/_build/index.html'))


drawing_area.set_events(Gdk.EventMask.SCROLL_MASK |
                        Gdk.EventMask.BUTTON_PRESS_MASK |
                        Gdk.EventMask.BUTTON_MOTION_MASK)

# Connect events with callbacks.
play_button.connect('clicked', switch_playing)
run_button.connect('clicked', switch_running)
input_buffer.connect('highlight-updated', compile_buffer)
grid_button.connect('clicked', grid_callback)
home_button.connect('clicked', home_callback)
help_button.connect('clicked', show_help)
drawing_area.connect('draw', draw)
drawing_area.connect('configure-event', change_size)
drawing_area.connect('scroll-event', change_zoom)
drawing_area.connect('button-press-event', drag_handler)
drawing_area.connect('motion-notify-event', drag_handler)
scale.connect('value-changed', change_time)
