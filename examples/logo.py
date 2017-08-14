import wisualia
from wisualia.shapes import paint, Stroke
from wisualia.modifiers import Move
from wisualia.patterns import RGBA, ImagePattern, LinearGradient, RadialGradient
from wisualia.pencil import Path, Pencil
from wisualia.image import Image
from wisualia import animation

import random
from math import sqrt


def length(a,b): 
    return sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)



def draw_buf(buf, g):
    s = Stroke(width=0.03, pattern=g)
    with Pencil(stroke=s) as p:
        for a in buf:
            for b in buf:
                if a!=b and 0.3<length(a,b) < 0.5:
                    p.move_to(*a)
                    p.line_to(*b)

def explain():
    f = RGBA(0.2,0.2,0.2,1)
    s = Stroke(pattern = RGBA(0,0,0,0))
    with Move(1,-3):
        with Pencil(fill=f, stroke=s) as p:
            p.text('Python inside',0.7)
        with Pencil(stroke=Stroke(pattern=RGBA(0,0,0,1),width=0.05)) as p:
            p.move_to(0,0.1)
            p.line_to(5,0.1)
            p.move_to(0,0.27)
            p.line_to(5,0.27)
                    
                
def loop(t):
    paint(RGBA(0,0,0))
    g = LinearGradient((0,-2),(0,2),[(0,RGBA(1,0,0)),(1,(RGBA(0,0,1)))])
    if t>9: 
        g=RGBA(1,1,1,abs(9.2-t)*10)
        if t>9.2:
            explain()
        t=9.2
    random.seed(t)
    p = Path()
    p.move_to(-4,-1.8)
    p.text('Vila', 5)
    a,b,c,d = p.fill_extents()
    buf = []
    nr = int(t*70)
    for _ in range(nr):
        x = random.uniform(a,c)
        y = random.uniform(b,d)
        if p.in_fill(x,y):
            buf.append((x,y))
    #draw_noise()
    draw_buf(buf, g)
    
                
            
    

animation.animate(loop)
