from typing import Tuple
from wisualia.core import Modifier
from math import radians

class Move(Modifier):
    def __init__(self, x:float, y:float) -> None:
        self.x = x
        self.y = y
    def modify(self, cr): #type: ignore
        cr.translate(self.x, self.y)

class Rotate(Modifier):
    def __init__(self, degrees:float, centre:Tuple[float, float]=(0, 0)) -> None:
        self.degrees = degrees
        self.centre = centre
    def modify(self, cr): #type: ignore
        cr.translate(self.centre[0], self.centre[1])
        cr.rotate(radians(self.degrees))
        cr.translate(-self.centre[0], -self.centre[1])

class Scale(Modifier):
    def __init__(self, factors:Tuple[float, float], centre:Tuple[float, float]=(0, 0)) -> None:
        self.factors = factors
        self.centre = centre
    def modify(self, cr): #type: ignore
        cr.translate(self.centre[0], self.centre[1])
        cr.scale(*self.factors)
        cr.translate(-self.centre[0], -self.centre[1])
