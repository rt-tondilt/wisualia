from typing import Tuple, List
from abc import ABCMeta, abstractmethod
from enum import Enum
from math import radians

import cairo #type: ignore

from wisualia import core
from wisualia.patterns import Pattern, RED, GREEN, BLUE
from wisualia.shapes import Stroke, _fill_and_stroke


class Path(object):
    def __init__(self) -> None:
        self.context = cairo.Context(core.context.get_target())
        self.image = core.image
    def _refresh(self) -> None:
        if self.image != core.image:
            message = (
            'Can not use path on other images.\n'
            'This path belongs to {} but was used on {}.'
            ).format(self.image, core.image)
            raise Exception(message)
        self.context.set_matrix(core.context.get_matrix())
    def move_to(self, x:float, y:float) -> None:
        self._refresh()
        self.context.move_to(x, y)
    def line_to(self, x:float, y:float) -> None:
        self._refresh()
        self.context.line_to(x,y)
    def close_path(self) -> None:
        self._refresh()
        self.context.close_path()
    def arc(self,
            centre:Tuple[float, float],
            radius:float,
            angles:Tuple[float, float]) -> None:
        self._refresh()
        self.context.arc(*centre, radius, radians(angles[0]), radians(angles[1]))
    def curve_to(self,
                 control1:Tuple[float,float],
                 control2:Tuple[float,float],
                 end:Tuple[float,float]) -> None:
        self._refresh()
        self.context.curve_to(*control1, *control2, *end)
    def text(self, text:str, size:float) -> None:
        self._refresh()
        self.context.save()
        self.context.scale(1,-1)
        self.context.set_font_size(size)
        self.context.text_path(text)
        self.context.restore()

    def draw_fill(self, pattern:Pattern) -> None:
        self._refresh()
        pattern._use_as_source_on(self.context)
        self.context.fill_preserve()
    def draw_stroke(self, stroke:Stroke) -> None:
        self._refresh()
        stroke.pattern._use_as_source_on(self.context)
        stroke._use_shape(self.context)
        self.context.stroke_preserve()

    def in_fill(self, x:float, y:float) -> bool:
        self._refresh()
        return self.context.in_fill(x,y) #type: ignore
    def in_stroke(self, x:float, y:float, stroke:Stroke) -> bool:
        self._refresh()
        stroke._use_shape(self.context)
        return self.context.in_stroke(x,y) #type: ignore
    def fill_extents(self) -> Tuple[float,float,float,float]:
        self._refresh()
        return self.context.fill_extents() #type: ignore
    def stroke_extents(self, stroke:Stroke) -> Tuple[float,float,float,float]:
        self._refresh()
        stroke._use_shape(self.context)
        return self.context.stroke_extents() #type: ignore
    def copy(self) -> 'Path':
        self._refresh()
        p = Path()
        p.context.append_path(self.context.copy_path())
        return p


class Pencil(object):
    def __init__(self,  fill:Pattern=RED, stroke:Stroke=Stroke()) -> None:
        self.stroke = stroke
        self.fill = fill
        self.path = Path()
    def __enter__(self) -> Path:
        return self.path
    def __exit__(self, exc_type: None, exc_value: None, traceback: None) -> bool:
        self.path._refresh()
        _fill_and_stroke(self.fill, self.stroke, self.path.context)
        return False # reraise potential exception
