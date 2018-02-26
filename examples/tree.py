import wisualia
from wisualia.do import fill,stroke
from wisualia.shapes import circle,line
from wisualia.modifiers import Move, Rotate,Scale
from wisualia.animation import animate
from wisualia.patterns import HSVA
from wisualia.geometry import Point


from random import random, uniform,seed,choice
from math import sin


leaves=[]
def tree(count,t):
    if count==0:
        leaves.append(Point(0,0))
        return
    line((0,0),(0,1))
    stroke(0.2,HSVA(0,0,0))
    for d,w,n in [(-35,0.4,1),(0,0.7,1),(20,0.5,1)]:
        if True:
            d+=t*10/count**2
        with Move(0,n), Rotate(d),Scale((w,1.3*w)):
            tree(count-1,t)

def loop(t):
    global k,r, leaves
    leaves=[]
 
    seed(6736)
    tree(7,3*sin(t*5))
    for l in leaves:
        circle(tuple(l),0.1)
    fill(HSVA(0,0,0.5))


animate(loop)
