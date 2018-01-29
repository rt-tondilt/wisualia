import wisualia
from wisualia.do import fill,stroke, paint, Clip,mask
from wisualia.shapes import circle, polygon
from wisualia.modifiers import Move, Rotate
from wisualia.animation import animate
from wisualia.patterns import RGBA
from wisualia.turtle import Turtle




def loop(t):
    tu = Turtle()

    tu.line_to(2,0)
    tu.turn_to(90)
    tu.forward(3)
    #tu.arc(0.3,(t-5)*90)
    #tu.forward(1)
    with Move(t,0):
        tu.curve_to((2,0),(2,2),(0,0))
    tu.draw()
    stroke()
animate(loop)
