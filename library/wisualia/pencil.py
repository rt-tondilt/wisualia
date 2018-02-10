from typing import Tuple, List, Optional
from abc import ABCMeta, abstractmethod
from enum import Enum
from math import radians, sin, cos, atan2

import cairo #type: ignore

from wisualia import core
from wisualia.patterns import Pattern, RED, GREEN, BLUE
from wisualia.shapes import begin_shape
from wisualia.geometry import Point, PointLike

class Pencil(object):
    def __init__(self) -> None:
        self.context = cairo.Context(core.context.get_target())
        self.image = core.image # for sanity checks
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
    def move(self, x:float, y:float) -> None:
        self._refresh()
        self.context.move_to(x, y)
    def line(self, x:float, y:float) -> None:
        self._refresh()
        self.context.line_to(x, y)
    def arc(self, centre:PointLike, rel_angle:float) -> None:
        self._refresh()
        rel_angle = radians(rel_angle)
        start = self.context.get_current_point()
        start_angle = atan2(start[1]-centre[1], start[0]-centre[0])
        end_angle = start_angle + rel_angle
        radius = Point(*start).distance(centre)
        if rel_angle >= 0:
            self.context.arc(*centre, radius, start_angle, end_angle)
        else:
            self.context.arc_negative(*centre, radius, start_angle, end_angle)
    def curve(self,
                 control1:PointLike,
                 control2:PointLike,
                 end:PointLike) -> None:
        self._refresh()
        self.context.curve_to(*control1, *control2, *end)
    def close_path(self) -> None:
        self._refresh()
        self.context.close_path()


    def draw(self) -> None:
        self._refresh()
        cr = begin_shape()
        cr.append_path(self.context.copy_path())
    def copy(self) -> 'Pencil':
        self._refresh()
        p = Pencil()
        p.context.append_path(self.context.copy_path())
        return p
