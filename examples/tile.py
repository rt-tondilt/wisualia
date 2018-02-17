import wisualia
from wisualia.do import fill,stroke, paint, Clip,mask
from wisualia.shapes import circle, polygon, rect, line
from wisualia.modifiers import Move, Rotate,Scale
from wisualia.animation import animate
from wisualia.patterns import RGBA,HSVA, LinearGradient,ImagePattern
from wisualia.image import Image
from wisualia.geometry import Point
from wisualia.pencil import Pencil

dolomiit = Image.from_png('dolomiit.png')

from math import sin
def q(a,b):
    circle((a,b),0.3)
    fill(RGBA(1,0,0))
    return (a,b)

def sq(t):
    #rect((0,0),(1,1))
    #fill()
    p=Pencil()
    for i in range(4):
        with Rotate(i*90,(0.5,0.5)),Scale((0.1,0.1)):
            #line((0.2,0.2),(1,t))
            p.move(0,5)
            p.curve((2,2-t),(4,2),(4.7,4))
            #p.move(0,0)
            #p.line(3,1)
        circle((0,0),0.1)
        stroke(0.05,HSVA(0,0,1,0.1))
        circle((0,0),0.15)
        stroke(0.05,HSVA(0,0,0,0.1))
    #g=LinearGradient((0,0.5),(0.5,0.5),[(0,RGBA(0,0,0)),(1,RGBA(0,1,0))])
    p.draw()
    stroke(0.05,HSVA(0,0,0,0.3))

def loop(t):
    
    '''with Move(-t,0):
        d=ImagePattern(dolomiit,40)
        paint(HSVA(t,1,1))'''
    d=ImagePattern(dolomiit,40)
    g=LinearGradient((0,0),(40,40),[(0,HSVA(0,0,0,0.6)),(1,HSVA(1,1,1,1))])
    mask(d,g)
    #paint(d)
    for x in range(8):
        for y in range(8):
            with Scale((5,5)),Move(x,y):
                sq(0)
    
animate(loop)