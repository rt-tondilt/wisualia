import wisualia
from wisualia.shapes import circle,rect
from wisualia.modifiers import Move,Scale
from wisualia.animation import animate
from wisualia.patterns import RGBA, RadialGradient,LinearGradient
from timeit import timeit

new = True

try:
    from wisualia.do import fill,stroke
except:
    new=False
def ring(pattern):
    r=10
    if new:
        for x in range(r):
            for y in range(r):
                with Move(x*0.5,y*0.5):
                    #circle((0,0),0.15)
                    rect((0,0),(0.3,0.3))
        fill(pattern)
    else:
        for x in range(r):
            for y in range(r):
                with Move(x*0.5,y*0.5):
                    rect((0,0),(0.3,0.3),pattern)
                    #circle((0,0),0.15,pattern)


def ring_1():
    ring(RGBA(1,0,0))
def ring_2():
    p=RadialGradient((1,1),0,(1,1),6,[(0,RGBA(1,0,0)),(1,RGBA(0,0,1))])
    #p=LinearGradient((0,1),(7,1),[(0,RGBA(1,0,0)),(1,RGBA(0,0,1))])
    ring(p)
    
def time(fn):
    cr=wisualia.core.context
    cr.save()
    cr.identity_matrix()
    with Scale((100,100)),Move(0.5,0.5):
        t=timeit(fn, number=10, globals=globals())
    cr.restore()
    print('{:<12} {}'.format(fn.__name__,t))
    
def loop(t):
    print('new =',new)
    time(ring_1)
    time(ring_2)


animate(loop)