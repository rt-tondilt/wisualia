import wisualia
from wisualia.do import fill, stroke,paint
from wisualia.shapes import circle,line,rect,polygon
from wisualia.patterns import RGBA,HSVA,LinearGradient,ImagePattern
from wisualia.modifiers import Move, Rotate, Scale
from wisualia.animation import animate, Camera
from wisualia.geometry import Point
from wisualia.image import Image

image=Image.from_png('floor.png')

def kaheksa(x,y,t):
    s=[]
    for d in range(8):
        with Rotate((d)*45*3):
            s.append(Point(6,0))
    polygon(*s)

def seitse(x,y,t,d):
    with Rotate(d*90,(6,6)):
        polygon((6,6),(0,0),(12,0))
    
                            
def ruudu(t,sisu,*args):
    for x in range(9):
        for y in range(6):
            with Move(x,y),Scale((1/12,1/12)):
                sisu(x,y,t,*args)


def loop(t):
    with  Scale((2.5,2.5)),Move(-4,-3):
        colors=[HSVA(0,0.4,0.7),HSVA(0.17,0.5,0.9),HSVA(0.17,0.5,0.56),HSVA(0.1,0.5)]
        if int(t)%2==0:
            colors=[HSVA(0,1,0.9),HSVA(0.17,1,0.9),HSVA(0.7,1,0.8),HSVA(0.1,1)]
        
        for d,c in zip(range(4),colors):
            ruudu(t,seitse,d)
            fill(c)

        ruudu(t,kaheksa)
        fill(HSVA(0,0.9,0.3))

        im=ImagePattern(image,300)
        paint(im,0.2)
        
        for d,c in zip(range(4),colors):
            ruudu(t,seitse,d)
        ruudu(t,kaheksa)
        
        n=0.56
        stroke(0.02,RGBA(n,n,n))
        paint(im,0.3)
    
animate(loop,camera=Camera((16,9),120),duration=5)
