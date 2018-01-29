from typing import Tuple, List, Optional
from abc import ABCMeta, abstractmethod
from enum import Enum
from math import radians, sin, cos, atan2

import cairo #type: ignore

from wisualia import core
from wisualia.patterns import Pattern, RED, GREEN, BLUE
from wisualia.shapes import begin_shape


'''class Turtle(object):
    def __init__(self) -> None:
        self.context = cairo.Context(core.context.get_target())
        self.image = core.image # for sanity checks
        self.direction = 0.0 #radians
        self._refresh()
        self.context.move_to(0,0)
    def _refresh(self) -> None:
        if self.image != core.image:
            message = (
            'Can not use path on other images.\n'
            'This path belongs to {} but was used on {}.'
            ).format(self.image, core.image)
            raise Exception(message)
        self.context.set_matrix(core.context.get_matrix())
    def turn_to(self, degrees:float):
        self._refresh()
        self.direction = radians(degrees)

    def get_position(self) -> Tuple[float, float]:
        self._refresh()
        return self.context.get_current_point()
    def forward(self, length:float):
        self._refresh()
        a = self.direction
        self.context.rel_line_to(cos(a)*length, sin(a)*length)

    def line_to(self, x:float, y:float) -> None:
        self._refresh()
        self.context.line_to(x,y)
    def close_path(self) -> None:
        self._refresh()
        self.context.close_path()
    def arc(self, radius:float, degrees:float) -> None:
        if radius<0:
            raise ValueError('Negative arc radius ({}).'.format(radius))
        self._refresh()
        a = self.direction
        b = radians(degrees)
        start = self.get_position()
        centre = 0,0
        if b>0:
            centre = start[0] - sin(a)*radius, start[1] + cos(a)*radius
            angle1 = a-radians(90)
            angle2 = angle1 + b
            self.context.arc(*centre, radius, angle1, angle2)
            self.direction = angle2 + radians(90)
        else:
            centre = start[0] + sin(a)*radius, start[1] - cos(a)*radius
            angle1 = a+radians(90)
            angle2 = angle1 + b
            self.context.arc_negative(*centre, radius, angle1, angle2)
            self.direction = angle2 - radians(90)



    def arc_old(self,
            centre:Tuple[float, float],
            radius:float,
            angles:Tuple[float, float]) -> None:
        self._refresh()
        self.context.arc(*centre, radius, radians(angles[0]), radians(angles[1]))
    def curve_to_old(self,
                 control1:Tuple[float,float],
                 control2:Tuple[float,float],
                 end:Tuple[float,float]) -> None:
        self._refresh()
        self.context.curve_to(*control1, *control2, *end)
    def draw(self):
        self._refresh()
        cr = begin_shape()
        cr.append_path(self.context.copy_path())

    def copy(self) -> 'Turtle':
        self._refresh()
        p = Turtle()
        p.context.append_path(self.context.copy_path())
        return p'''


''' def text(self, text:str, size:float) -> None:
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
        return self.context.stroke_extents() #type: ignore'''
