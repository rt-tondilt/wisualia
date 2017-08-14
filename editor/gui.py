
import gi #type: ignore
from gi.repository import GLib,Gtk,Gdk, GObject, GtkSource #type: ignore
import string
import colorsys

builder = Gtk.Builder().new_from_file('gui.glade')

window = builder.get_object("window")
window.set_title('Wisualia editor')
drawing_area = builder.get_object("drawing_area")
scale = builder.get_object("scale")
file_label = builder.get_object("file_label")

play_button = builder.get_object("play_button")
pause_button = builder.get_object("pause_button")
export_button = builder.get_object("export_button")
home_button =  builder.get_object("home_button")
grid_button = builder.get_object("grid_button")
save_button =  builder.get_object("save_button")
open_button =  builder.get_object("open_button")
run_button =  builder.get_object("run_button")
abort_button = builder.get_object("abort_button")
help_button = builder.get_object("help_button")

status_bar = builder.get_object("status_bar")

input_buffer = builder.get_object("input_view").get_buffer()
output_buffer = builder.get_object("output_view").get_buffer()
input_view = builder.get_object("input_view")

language_manager = GtkSource.LanguageManager()
input_buffer.set_language(language_manager.get_language('python3'))

style_manager = GtkSource.StyleSchemeManager()
output_buffer.set_style_scheme(style_manager.get_scheme('cobalt'))

play_icon = Gtk.Image().new_from_stock(Gtk.STOCK_MEDIA_PLAY, Gtk.IconSize.DND)
pause_icon = Gtk.Image().new_from_stock(Gtk.STOCK_MEDIA_PAUSE, Gtk.IconSize.DND)

def bigger_font():
    context = input_view.get_style_context()
    css = (b"textview {"
                b" font: 12pt monospace;"
                b"}")
    provider = Gtk.CssProvider()
    provider.load_from_data(css)
    context.add_provider(provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

bigger_font()

status_bar.push(1,'')
def set_status_bar_text(text):
    status_bar.pop(1)
    status_bar.push(1, text)


color_tags = []

def try_parse_color(text):
    # example 'RGBA( 1.0 , 0.0 , 0.1 )'
    text = text.replace(' ', '')
    try:
        numbers = list(map(float, text[5:-1].split(',')))
        assert len(numbers) < 5
        if text[ :4] == 'RGBA':
            numbers = map(lambda x: 0 if x<0 else (x if x<1 else 1), numbers)
            r, g, b, *_ = numbers
        elif text[ :4] == 'HSVA':
            s, v = 1, 1
            h = numbers[0]
            try:
                s = numbers[1]
                v = numbers[2]
                s, v = map(lambda x: 0 if x<0 else (x if x<1 else 1), [s,v])
            except Exception: pass
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
        else: assert False
    except Exception:
        return None
    return r, g, b

def get_fg_and_bg(r, g, b):
    if r+g+b > 1.5:
        fg = Gdk.RGBA(0,0,0,1)
    else:
        fg = Gdk.RGBA(1,1,1,1)
    return fg, Gdk.RGBA(r, g, b, 1)



SEARCH_REGEX = r'(RGBA|HSVA)\(.*?\)'
SEARCH_SETTINGS = GtkSource.SearchSettings(search_text=SEARCH_REGEX,
                                           wrap_around=False,
                                           regex_enabled=True,
                                           case_sensitive=True)

def on_highlight_updated(buffer, start, end):
    global color_tags
    for tag in color_tags:
        buffer.remove_tag(tag, buffer.get_start_iter(), buffer.get_end_iter())
    color_tags = []

    searcher = GtkSource.SearchContext(buffer=buffer, settings=SEARCH_SETTINGS)
    current_iter = buffer.get_start_iter()
    while True:
        found, start, end, _ = searcher.forward2(current_iter)

        if not found:
            break
        current_iter = end
        rgb = try_parse_color(buffer.get_text(start, end, True))
        if rgb != None:
            fg, bg = get_fg_and_bg(*rgb)
            new_tag = buffer.create_tag(foreground_rgba = fg,
                                        background_rgba = bg,
                                        weight = 700)
            buffer.apply_tag(new_tag, start, end)
            color_tags.append(new_tag)
    print('HIGHLIGHT UPDATED')

input_buffer.connect('highlight-updated', on_highlight_updated)
