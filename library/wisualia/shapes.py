from typing import Tuple, Optional, List
from enum import Enum, IntEnum
from math import pi

from wisualia import core
from wisualia.patterns import Pattern, RGBA,  RED, GREEN, BLUE
from wisualia.geometry import Point, PointLike

def begin_shape(): #type: ignore
    cr = core.context
    if core.current_path_is_used:
        cr.new_path()
        core.current_path_is_used=False
    cr.new_sub_path()
    return cr

def rect(point1:PointLike, point2:PointLike) -> None:
    '''
    Args:
        point1:
        point2:
    Returns:
        Nothing

    Draw a rectangle to the current image with edges parallel to the x- and
    y-axis. The edges may not be parallel if the function is called inside a
    transformation.
    '''
    cr = begin_shape()
    cr.rectangle(*point1, point2[0]-point1[0], point2[1]-point1[1])

def circle(centre:PointLike=(0, 0),
           radius:float=1) -> None:
    '''
    Args:
        centre:
        radius:
    Returns:
        Nothing

    Draw a circle to the current image.
    '''
    cr = begin_shape()
    cr.arc(centre[0], centre[1], radius , 0, 2 * pi)

def polygon(*points: PointLike) -> None:
    '''
    Args:
        points:
    Returns:
        Nothing

    Draw a polygon to the current image.
    '''
    cr = begin_shape()
    cr.move_to(*points[0])
    for i in range(1, len(points)):
        cr.line_to(*points[i])
    cr.close_path()

def text(start:PointLike, text:str, size:float) -> None:
        cr = begin_shape()
        cr.save()
        cr.translate(*start)
        cr.scale(1,-1)
        cr.set_font_size(size)
        cr.text_path(text)
        cr.restore()
