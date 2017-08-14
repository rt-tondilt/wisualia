import wisualia
from wisualia.shapes import circle
from wisualia.modifiers import Rotate, Move
from wisualia.patterns import HSVA
from wisualia import animation
from math import sin, pi


def loop(t):
    for i in range(36):
        with Rotate(i*10):
            with Move(-(i%6)*sin(t), 0):
                circle((5,0),0.5, HSVA(i/36+t))
    
animation.CAMERA = animation.Camera((20,20), 40)
animation.animate(loop)