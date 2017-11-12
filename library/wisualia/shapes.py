from typing import Tuple, Optional, List
from enum import Enum, IntEnum
from math import pi

from wisualia import core
from wisualia.patterns import Pattern, RGBA,  RED, GREEN, BLUE
from wisualia.core import derive_repr

class LineJoin(IntEnum):
    '''
    Style of the corner between two joined lines.
    '''
    MITER = 0
    ROUND = 1
    BEVEL = 2
class LineCap(IntEnum):
    '''
    Style of the start and end of a line if it is not joined with another one.
    '''
    BUTT = 0
    ROUND = 1
    SQUARE = 2
@derive_repr
class Dash(object):
    '''
    Args:
        dashes:
        offset:

    Todo:
        Experimentad and undocumented.
    '''
    def __init__(self, dashes:List[float], offset:int=0) -> None:
        self.dashes = dashes
        self.offset = offset
@derive_repr
class Stroke(object):
    '''
    Args:
        width:
        pattern:
        join:
        cap:
        dash:

    The style of drawn lines or paths. All parameters of this class are public
    and mutable.
    '''
    def __init__(self,
                 width:float=0.1,
                 pattern:Pattern=RGBA(0,0,0,1),
                 join:LineJoin=LineJoin.MITER,
                 cap:LineCap=LineCap.BUTT,
                 dash:Dash=Dash([],0)) -> None:
        self.width = width
        self.pattern = pattern
        self.join = join
        self.cap = cap
        self.dash = dash
    def _use_shape(self, cr): #type: ignore
        cr.set_line_width(self.width)
        cr.set_line_join(self.join)
        cr.set_line_cap(self.cap)
        cr.set_dash(self.dash.dashes, self.dash.offset)

def _fill_and_stroke(fill:Optional[Pattern], stroke:Optional[Stroke], cr) -> None: #type: ignore
    if fill is not None:
        fill._use_as_source_on(cr)
        if stroke is None:
            cr.fill()
            return
        cr.fill_preserve()
    if stroke is not None:
        stroke.pattern._use_as_source_on(cr)
        stroke._use_shape(cr)
        cr.stroke()

def rect(point1:Tuple[float, float],
         point2:Tuple[float, float],
         fill:Optional[Pattern]=GREEN,
         stroke:Optional[Stroke]=None) -> None:
    '''
    Args:
        point1:
        point2:
        fill:
        stroke:
    Returns:
        Nothing

    Draw a rectangle to the current image with edges parallel to the x- and
    y-axis. The edges may not be parallel if the function is called inside a
    transformation.
    '''
    cr = core.context
    cr.save()
    cr.rectangle(*point1, point2[0]-point1[0], point2[1]-point1[1])
    _fill_and_stroke(fill, stroke, cr)
    cr.restore()

def circle(centre:Tuple[float, float]=(0, 0),
           radius:float=1,
           fill:Optional[Pattern]=GREEN,
           stroke:Optional[Stroke]=None) -> None:
    '''
    Args:
        centre:
        radius:
        fill:
        stroke:
    Returns:
        Nothing

    Draw a circle to the current image.
    '''
    cr = core.context
    cr.save()
    cr.arc(centre[0], centre[1], radius , 0, 2 * pi)
    _fill_and_stroke(fill, stroke, cr)
    cr.restore()

def polygon(*points: Tuple[float, float],
            fill:Optional[Pattern]=RED,
            stroke:Optional[Stroke]=None) -> None:
    '''
    Args:
        points:
        fill:
        stroke:
    Returns:
        Nothing

    Draw a polygon to the current image.
    '''
    cr = core.context
    cr.save()

    cr.move_to(*points[0])
    for i in range(1, len(points)):
        cr.line_to(*points[i])
    cr.close_path()

    _fill_and_stroke(fill, stroke, cr)
    cr.restore()

def paint(pattern:Pattern, alpha:float=1) -> None:
    '''
    Args:
        pattern:
        alpha:
    Returns:
        Nothing

    Paints a pattern to the current image, using given alpha value.
    '''
    cr = core.context
    cr.save()
    pattern._use_as_source_on(cr)
    cr.paint_with_alpha(alpha)
    cr.restore()
