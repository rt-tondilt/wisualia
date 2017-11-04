from abc import ABCMeta, abstractmethod
from typing import Any
import inspect

import cairo #type: ignore

context = None #type: Any
image = None #type: Any

class Modifier(metaclass = ABCMeta):
    # DO NOT OVERRIDE, EXPLODES!
    def __enter__(self) -> None:
        self.__old__matrix = context.get_matrix()
        self.modify(context)
    # DO NOT OVERRIDE, EXPLODES!
    def __exit__(self, exc_type: None, exc_value: None, traceback: None) -> bool:
        context.set_matrix(self.__old__matrix)
        return False # reraise potential exception
    @abstractmethod
    def modify(self, cr): #type: ignore
        pass

def derive_repr(cls): #type:ignore
    '''Decorator that derives __repr__ method based on class initializer arguments.

    For example the following class
        @derive_repr
        class Example(object):
            def __init__(self, a, b):
                self.a = a
                self.b = b
    would generate a __repr__ method with behaviour identical to:
        def __repr__(self):
            return 'Example({}, {})'.format(self.a, self.b)

    derive_repr does not read the source code of the initializer and does not
    know wheter the class has parameters named a and b. Therefore it should only
    be used on relatively "struct-like" classes.
    '''
    arg_names = list(inspect.signature(cls).parameters.keys())
    format_str = '{}({})'.format(cls.__name__, ', '.join('{}' for _ in arg_names))
    get_params_str = repr(['self.'+n for n in arg_names]).replace("'","")
    get_params = compile(get_params_str, 'core.py', 'eval')
    def representation(self): #type:ignore
        return format_str.format(*eval(get_params))
    cls.__repr__ = representation
    return cls

def _draw_grid(cr, step, zoom_b_x, zoom_b_y, width, height): #type:ignore
    x = zoom_b_x
    y = zoom_b_y
    right = width
    down  = height
    up = 0
    left = 0

    cr.set_source_rgb(0.6,0.6,0.6)
    cr.set_line_width(3.0)
    cr.move_to(x, down)
    cr.line_to(x, up)
    cr.move_to(left, y)
    cr.line_to(right, y)
    cr.stroke()

    cr.set_line_width(1.0)
    x_pix = x % step
    y_pix = y % step
    while x_pix < right:
        cr.move_to(round(x_pix)+0.5, down)
        cr.line_to(round(x_pix)+0.5, up)
        x_pix += step
    while y_pix < down:
        cr.move_to(left, round(y_pix)+0.5)
        cr.line_to(right, round(y_pix)+0.5)
        y_pix += step
    cr.stroke()
