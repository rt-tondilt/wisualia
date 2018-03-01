import wisualia
from wisualia.do import paint, stroke,fill, Dash, fill_extents, in_fill
from wisualia.shapes import circle, rect,text
from wisualia.modifiers import Scale, Rotate
from wisualia.patterns import RGBA, ImagePattern, LinearGradient, RadialGradient
from wisualia.pencil import Pencil
from wisualia.image import Image
from wisualia.animation import animate

im = Image.from_png('example.png')
def loop(t):
    t=t+0.1
    with Rotate(0*90):
        stops = [(0,RGBA(1,0,0,0.3)), (1,RGBA(0,0,0.5,0.3))]
        f=LinearGradient((0,0),(5,5), stops)
        f2=RadialGradient((0,0),1, (5,5), 10, stops)
    paint(f2, alpha=0.2)
    with Scale((1.5,1)):
        circle((0,0),1)
        stroke(width=0.5)
        paint(ImagePattern(im, pixels_per_unit=40), alpha=0.7)
        
        p=Pencil()
        p.move(0,3)
        p.line(0,6)
        p.line(3,6)
        p.line(3,3)
        with Scale((1,1)):
            p.arc((-1,-1),t*30)
        
        p.draw()
        (a,b),(c,d) = fill_extents()
        
        for x in range(int(a),int(c)):
            for y in range(int(b), int(d)):
                if in_fill(x,y):
                    circle((x,y), 0.5)
                    print(x,y)
        rect((a,b),(c,d))
        fill(RGBA(0.2,0,0,0.3))
        
        text((0,0),'Hell World.',2)
        (a,b),(c,d) = fill_extents()
        rect((a,b),(c,d))
        fill(RGBA(0.2,0,0,0.3))
    
animate(loop)
