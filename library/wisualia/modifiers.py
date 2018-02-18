from typing import Tuple
from wisualia.core import Modifier, derive_repr
from  wisualia.geometry import PointLike
from math import radians

@derive_repr
class Move(Modifier):
    def __init__(self, x:float, y:float) -> None:
        self.x = x
        self.y = y
    def modify(self, cr): #type: ignore
        cr.translate(self.x, self.y)

@derive_repr
class Rotate(Modifier):
    def __init__(self, degrees:float, centre:PointLike=(0, 0)) -> None:
        self.degrees = degrees
        self.centre = centre
    def modify(self, cr): #type: ignore
        cr.translate(self.centre[0], self.centre[1])
        cr.rotate(radians(self.degrees))
        cr.translate(-self.centre[0], -self.centre[1])

@derive_repr
class Scale(Modifier):
    def __init__(self, factors:Tuple[float, float], centre:PointLike=(0, 0)) -> None:
        self.factors = factors
        self.centre = centre
    def modify(self, cr): #type: ignore
        cr.translate(self.centre[0], self.centre[1])
        cr.scale(*self.factors)
        cr.translate(-self.centre[0], -self.centre[1])
