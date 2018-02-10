from wisualia import *
from wisualia.do import fill,stroke
from wisualia.shapes import circle
from wisualia.patterns import RGBA, ImagePattern, LinearGradient, RadialGradient
from wisualia.pencil import Pencil
from wisualia.image import Image
from wisualia.animation import animate



im = Image.from_png('example.png')
def loop(t):
    p1=(0,0)
    p2=(0,0)
    p3=(-t,3)
    p4=(3,3)

    p=Pencil()
    p.move(*p1)
    p.curve(p3,p3,p4)
    circle(p2,0.1)
    circle(p3,0.1)
    fill(RGBA(1,0,0))
    p.line(-5,-5)
    p.line(-6,-6)
    p.line(-3,0)
    p.draw()
    stroke(0.1,RGBA(0,1,0))

animate(loop)
