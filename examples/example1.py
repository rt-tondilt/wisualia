import wisualia
from wisualia.do import fill,stroke, paint, Clip,mask
from wisualia.shapes import circle, polygon, rect
from wisualia.modifiers import Move, Rotate
from wisualia.animation import animate
from wisualia.patterns import RGBA, LinearGradient,ImagePattern
from wisualia.image import Image
from wisualia.geometry import Point
from wisualia.pencil import Pencil

image=Image.from_png('example.png')

def loop(t):
    #paint(RGBA(0,0,0))
    
    circle((0,0),1)
    circle((1,0),1)
    with Move(2,1):
        p=Point(1,1)
    a,b=p
    rect(p,p)
    print(p[0])
    print(p)
    with Clip():
        circle((0.5,0),t)
        with Clip():
        
        #fill()
            paint(RGBA(1,0,0))

        #fill()
    #circle((0,1),1)
    #stroke()
    #with Move(2,0):
    ip=ImagePattern(image,40)
    g=LinearGradient((0,0),(3,3),[(0,RGBA(1,0,0,0)),(1,RGBA(1,0,0))])
    
    
    mask(ip,g)
    p=Pencil()
    p.line(1,1)
    p.line(2,1)
    p.draw()
    stroke()
animate(loop, duration=3)
