from typing import Tuple
from wisualia.core import Modifier, derive_repr
from  wisualia.geometry import PointLike
from math import radians

@derive_repr
class DoNothing(Modifier):
    '''
    Literally does nothing.
    '''
    def modify(self, cr): #type: ignore
        pass

@derive_repr
class Move(Modifier):
    '''
    Args:
        x:
        y:

    Moves all values inside ``with`` statement with vector (x, y).
    '''
    def __init__(self, x:float, y:float) -> None:
        self.x = x
        self.y = y
    def modify(self, cr): #type: ignore
        cr.translate(self.x, self.y)

@derive_repr
class Rotate(Modifier):
    '''
    Args:
        degrees:
        centre:

    Rotates all values inside ``with`` by number of degrees around centre point.
    '''
    def __init__(self, degrees:float, centre:PointLike=(0, 0)) -> None:
        self.degrees = degrees
        self.centre = centre
    def modify(self, cr): #type: ignore
        cr.translate(self.centre[0], self.centre[1])
        cr.rotate(radians(self.degrees))
        cr.translate(-self.centre[0], -self.centre[1])

@derive_repr
class Scale(Modifier):
    '''
    Args:
        factors:
        centre:

    Scales all values inside ``with`` by given factors and with given centre
    point.
    '''
    def __init__(self, factors:Tuple[float, float], centre:PointLike=(0, 0)) -> None:
        self.factors = factors
        self.centre = centre
    def modify(self, cr): #type: ignore
        cr.translate(self.centre[0], self.centre[1])
        cr.scale(*self.factors)
        cr.translate(-self.centre[0], -self.centre[1])
