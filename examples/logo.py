import wisualia
from wisualia.do import paint, stroke,fill,fill_extents, in_fill
from wisualia.modifiers import Move
from wisualia.patterns import RGBA, ImagePattern, LinearGradient, RadialGradient
from wisualia.shapes import text
from wisualia.pencil import Pencil
from wisualia.image import Image
from wisualia.animation import animate, Camera

import random
from math import sqrt


def length(a,b): 
    return sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)



def draw_buf(buf, g):
    p=Pencil()
    for a in buf:
        for b in buf:
            if a!=b and 0.2<length(a,b) < 0.3:
                p.move(*a)
                p.line(*b)
    p.draw()
    stroke(width=0.03, pattern=g)

def explain():
    f = RGBA(0.2,0.2,0.2,1)
    with Move(1,-2.5):
        text((0,0),'Python inside',0.7)
        fill(f)
        p=Pencil()
        p.move(0,0.1)
        p.line(5,0.1)
        p.move(0,0.27)
        p.line(5,0.27)
        p.draw()
        stroke(pattern=RGBA(0,0,0),width=0.05)
                    
                
def loop(t):
    paint(RGBA(0,0,0))
    g = LinearGradient((0,-2),(0,2),[(0,RGBA(1,0,0)),(1,(RGBA(0,0,1)))])
    if t>9: 
        g=RGBA(1,1,1,abs(9.2-t)*10)
        if t>9.2:
            explain()
        t=9.2
    random.seed(t)

    text((-5.8,-1),'Wisualia',3)
    (a,b),(c,d) = fill_extents()
    buf = []
    nr = int(t*150)
    for _ in range(nr):
        x = random.uniform(a,c)
        y = random.uniform(b,d)
        if in_fill(x,y):
            buf.append((x,y))
    fill(RGBA(0,0,0,0))
    draw_buf(buf, g)
    
animate(loop, Camera((16,8),40))
