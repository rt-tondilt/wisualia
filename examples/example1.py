import wisualia
from wisualia.do import fill,stroke, paint
from wisualia.shapes import circle, polygon
from wisualia.modifiers import Move, Rotate
from wisualia.animation import animate
from wisualia.patterns import RGBA

def loop(t):
    paint(RGBA(0,0,0))
    circle((0,0),1)
    circle((0,1),1)
    
    #stroke()
    fill()


animate(loop, duration=20)
