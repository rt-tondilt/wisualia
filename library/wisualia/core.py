from abc import ABCMeta, abstractmethod
from typing import Any

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

def _draw_grid(cr, step, zoom_b_x, zoom_b_y, width, height):
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
