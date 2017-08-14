'''Patterns

A pattern is a paint that is used for drawing. Patterns can be used to fill
shapes or to draw lines.
'''

from typing import Tuple, Sequence
import colorsys
import cairo #type: ignore
from wisualia import core
from wisualia.image import Image




class Pattern(object):
    '''A base class of all patterns.

    Args:
        cairo_pattern: an internal cairo_pattern

    Users should not use it.

    '''
    def __init__(self, cairo_pattern): #type: ignore
        '''Pattern init'''
        cr = core.context
        m = cr.get_matrix()
        m.invert()
        cairo_pattern.set_matrix(m)
        self.cairo_pattern = cairo_pattern
    def _use_as_source_on(self, cr): #type: ignore
        m = cr.get_matrix()
        cr.identity_matrix()
        cr.set_source(self.cairo_pattern)
        cr.set_matrix(m)

'''
See tekst on siin vahel lollakas.
'''

class RGBA(Pattern):
    '''
    Args:
        r: red
        g: green
        b: blue
        a: alpha

    Solid color Pattern.

    All arguments are in range 0 to 1. Values that are
    outside of that range will be clamped when drawn.
    '''
    def __init__(self, r:float, g:float, b:float, a:float=1) -> None:
        self.r = r
        self.g = g
        self.b = b
        self.a = a
    def get_rgba(self) -> Tuple[float,float,float,float]:
        '''Returns rgba values as a tuple of floats.
        Values may be outside of range 0 to 1.'''
        return self.r, self.g, self.b, self.a
    def _use_as_source_on(self, cr): #type: ignore
        cr.set_source(cairo.SolidPattern(*self.get_rgba()))




def HSVA(h:float, s:float=1, v:float=1, a:float=1) -> RGBA:
    '''
    Args:
        h: hue
        s: saturation
        v: value
        a: alpha
    Returns:
        Color with all values in range 0 to 1

    Convenience function that creates RGBA Pattern.

    All hue values that are outside of range 0 to 1 are divided by 1 and the
    reminder is used as the hue. This means that hue values 1.3, 7.3, and -2.3
    all produce the same color. All other parameters that are outside of that
    range will be clamped.

    .. testcode::

        import wisualia
        from wisualia.shapes import circle
        circle((1,1), 0.5)

    .. testcleanup::

        wisualia_x.core.image.write_to_png('_images/circle.png')

    .. image:: /_images/circle.png
    '''
    # colorsys.hsv_to_rgb misbehaves if s or v are out of range.
    if s>1: s=1
    elif s<0: s=0
    if v>1: v=1
    elif v<0: v=0
    if a>1: a=1
    elif a<0: a=0
    return RGBA(*colorsys.hsv_to_rgb(h,s,v), a)

def LinearGradient(start:Tuple[float,float],
                   end:Tuple[float,float],
                   color_stops:Sequence[Tuple[float, RGBA]]) -> Pattern:
    '''
    Args:
        start: starting point of the line
        end: ending point of the line
        color_stops: relative locations on the gradient control vector

    Creates linear gradient along a straight line.
    Selgitus saa oled.
    '''
    gradient = cairo.LinearGradient(*start, *end)
    for offset, color in color_stops:
        gradient.add_color_stop_rgba(offset, *color.get_rgba())
    return Pattern(gradient)

def RadialGradient(start_centre:Tuple[float,float],
                   start_radius:float,
                   end_centre:Tuple[float,float],
                   end_radius:float,
                   color_stops:Sequence[Tuple[float, RGBA]]) -> Pattern:
    gradient = cairo.RadialGradient(*start_centre, start_radius,
                                    *end_centre, end_radius)
    for offset, color in color_stops:
        gradient.add_color_stop_rgba(offset, *color.get_rgba())
    return Pattern(gradient)

def ImagePattern(image:Image, pixels_per_unit:float) -> Pattern:
        cr = core.context
        cr.save()
        cr.scale(1/pixels_per_unit, 1/pixels_per_unit)
        pattern = Pattern(cairo.SurfacePattern(image.surf))
        cr.restore()
        return pattern


RED = RGBA(1,0,0)
GREEN = RGBA(0,1,0)
BLUE = RGBA(0,0,1)
