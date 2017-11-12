import wisualia
from wisualia.shapes import circle, paint, rect, Stroke, Dash
from wisualia.modifiers import Scale, Rotate
from wisualia.patterns import RGBA, ImagePattern, LinearGradient, RadialGradient
from wisualia.pencil import Pencil
from wisualia.image import Image
from wisualia.animation import animate

im = Image.from_png('example.png')
def loop(t):
    with Rotate(0*90):
        stops = [(0,RGBA(1,0,0,0.3)), (1,RGBA(0,0,0.5,0.3))]
        f=LinearGradient((0,0),(5,5), stops)
        f2=RadialGradient((0,0),1, (5,5), 10, stops)
    paint(f2, alpha=0.2)
    with Scale((t,t)):
        circle((0,0),1, stroke=Stroke(width=0.5))
        paint(ImagePattern(im, pixels_per_unit=40), alpha=0.7)
        with Pencil(fill=f2, stroke=Stroke(width=0.5, dash=Dash([0.2,0.2],4))) as p:
            p.move_to(0,3)
            p.line_to(0,6)
            p.line_to(3,6)
            p.line_to(3,3)
            with Scale((1,1)):
                p.arc((-1,-1),3,(0,180))
            a,b,c,d = p.fill_extents()
            for x in range(int(a),int(c)):
                for y in range(int(b), int(d)):
                    if p.in_fill(x,y):
                        circle((x,y), 0.5)
                        print(x,y)
            rect((a,b),(c,d),fill=RGBA(0.2,0,0,0.3))
        with Pencil() as p:
            p.text('Hell World.',2)
            a,b,c,d = p.fill_extents()
            rect((a,b),(c,d),fill=RGBA(0.2,0,0,0.3))
    
animate(loop)
