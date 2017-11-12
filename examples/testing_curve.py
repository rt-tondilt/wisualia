from wisualia import *
from wisualia.shapes import circle
from wisualia.patterns import RGBA, ImagePattern, LinearGradient, RadialGradient
from wisualia.pencil import Pencil, Path
from wisualia.image import Image
from wisualia.animation import animate


im = Image.from_png('example.png')
def loop(t):
    p1=(0,0)
    p2=(0,0)
    p3=(-t,3)
    p4=(3,3)
    cr = core.context
    cr.rectangle(0,0,3,3)
    cr.clip()
    
    with Pencil() as p:
        p.move_to(*p1)
        p.curve_to(p3,p3,p4)
        circle(p2,0.1)
        circle(p3,0.1)
        path=p.copy()
    p.line_to(-5,-5)
    p.line_to(-6,-6)
    p.line_to(-3,0)
    p.draw_fill(RGBA(0,1,0))

animate(loop)
