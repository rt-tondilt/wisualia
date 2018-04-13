import gi #type: ignore
from gi.repository import GLib,Gtk,Gdk, GObject, GtkSource  #type: ignore
import string
import math
from math import *
import os,sys


builder = Gtk.Builder().new_from_file('gui.glade')

widget_names = [
'window',

'new_button', 'open_button', 'save_button', 'save_as_button', 'export_button',
'run_button', 'typecheck_button', 'home_button', 'grid_button','help_button',

'drawing_area', 'scale', 'play_button', 'status_bar',
'file_label', 'input_view', 'output_view',
]

for name in widget_names:
    widget = builder.get_object(name)
    if widget==None:
        raise Exception('Widget {} does not exsist.'.format(name))
    locals()[name] = widget

input_buffer = input_view.get_buffer()
output_buffer = output_view.get_buffer()

play_icon = Gtk.Image().new_from_stock(Gtk.STOCK_MEDIA_PLAY, Gtk.IconSize.DND)
pause_icon = Gtk.Image().new_from_stock(Gtk.STOCK_MEDIA_PAUSE, Gtk.IconSize.DND)
run_icon = Gtk.Image().new_from_icon_name('gtk-execute', Gtk.IconSize.DND)
abort_icon = Gtk.Image().new_from_icon_name('gtk-stop', Gtk.IconSize.DND)

def setup(): # call this only once in this file

    window.set_title('Wisualia editor')

    language_manager = GtkSource.LanguageManager()
    input_buffer.set_language(language_manager.get_language('python3'))

    style_manager = GtkSource.StyleSchemeManager()
    output_buffer.set_style_scheme(style_manager.get_scheme('cobalt'))

    # Larger font
    context = input_view.get_style_context()
    css = (b"textview {"
                b" font: 12pt monospace;"
                b"}")
    provider = Gtk.CssProvider()
    provider.load_from_data(css)
    context.add_provider(provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

setup()

status_bar.push(1,'')
def set_status_bar_text(text):
    status_bar.pop(1)
    status_bar.push(1, text)

RED_OUTPUT = output_buffer.create_tag(foreground_rgba = Gdk.RGBA(1,0.4,0.4,1),
                                      weight = 900)

def set_output(text, error):
    buf=output_buffer
    buf.remove_tag(RED_OUTPUT, buf.get_start_iter(), buf.get_end_iter())
    buf.set_text(text)
    buf.insert_with_tags(buf.get_end_iter(), error, RED_OUTPUT)
