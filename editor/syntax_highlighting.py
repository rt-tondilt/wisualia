import sys
import os
import gi #type: ignore
from gi.repository import Gdk,GtkSource #type: ignore
import colorsys
from gui import input_buffer

MULTICOLOR_KILL_SWITCH=True

color_tags = []

def try_parse_color(text):
    # example 'RGBA( 1.0 , 0.0 , 0.1 )'
    # text = text.replace(' ', '')
    try:
        l=len(text)
        step=round(10/l,2)
        #print(text,l,step)
        rgb=[]
        args=text[5:-1] #funktsiooni argumendid
        ttt=0.0
        for i in range(l):
            if MULTICOLOR_KILL_SWITCH:
                global t # Lüliti tööpõhimõte: kui programm ei leia muutujat t, väljastab vea
                t=ttt # Kui funk. ei kasuta t-d, pole probleemi.
            numbers = list(map(lambda x:float(eval(x)), args.split(',')))
            ttt+=step
            assert len(numbers) < 5
            if text[ :4] == 'RGBA':
                numbers = map(lambda x: 0 if x<0 else (x if x<1 else 1), numbers)
                r, g, b, *_ = numbers
                rgb.append((r,g,b))
            elif text[ :4] == 'HSVA':
                s, v = 1, 1
                h = numbers[0]
                try:
                    s = numbers[1]
                    v = numbers[2]
                    s, v = map(lambda x: 0 if x<0 else (x if x<1 else 1), [s,v])
                except Exception: pass
                r, g, b = colorsys.hsv_to_rgb(h, s, v)
                #rgb.append((r**0.3,g**0.3,b**0.3))
                rgb.append((r,g,b))
            else: assert False
    except Exception as e:

        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(e)
        return None
    return rgb


def get_fg_and_bg(r, g, b):
    l=0.299*r+0.587*g+0.114*b
    if l > 0.5:
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
        while True:
            tex=buffer.get_text(start, end, True)
            if tex.count('(')!=tex.count(')'):
                end.forward_char()
            else:
                break
            if end.ends_line():
                break
        tex=buffer.get_text(start, end, True)
        rgb = try_parse_color(tex)
        if rgb != None:
            start2=start.copy()
            start2.forward_char()
            for i in rgb:
                fg, bg = get_fg_and_bg(*i)
                new_tag = buffer.create_tag(foreground_rgba = fg,
                                            background_rgba = bg,
                                            weight = 700)
                buffer.apply_tag(new_tag, start, start2)
                start.forward_char()
                start2.forward_char()
                color_tags.append(new_tag)
    print('HIGHLIGHT UPDATED')

input_buffer.connect('highlight-updated', on_highlight_updated)
