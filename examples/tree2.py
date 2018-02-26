import wisualia
from wisualia.do import fill,stroke, LineCap
from wisualia.shapes import circle,line
from wisualia.modifiers import Move, Rotate,Scale
from wisualia.animation import animate
from wisualia.patterns import RGBA,HSVA
from wisualia.geometry import Point
from wisualia.pencil import Pencil

from random import random, uniform,seed,choice, shuffle
from math import sin,pi,cos


def cilrand(n):
    a= random()*pi
    return cos(random()*pi)*n,sin(n)




leaves=[]
def tree(count,t,sf):
    if sf<0.1:
        leaves.append(Point(0,0))
        return
    line((0,0),(0,1))
    stroke(1,HSVA(0,0,0), cap=LineCap.ROUND)
    wind=t/sf/10
    if count%5!=3:
        with Move(0,1), Rotate(uniform(-20,20)+wind),Scale((0.93,0.93)):
            tree(count-1,t,sf*0.93)
        if random()<0.1:
            with Move(0,1), Rotate(uniform(-20,20)+wind),Scale((0.5,0.5)):
                tree(count//4,t,sf*0.5)
        return
    br=[]
    for i in range(choice([2,3,3,3,4])):
        d,s=cilrand(40)
        br.append((d,s))
    for d,s in br:
        d+=wind

        val=[0.6,0.5]
        shuffle(val)
        with Move(0,1), Rotate(d),Scale((0.9*s,0.95)):
            tree(count-1,t,sf*0.9)

def loop(t):
    global leaves
    leaves=[]
    seed(t)
    with Move(0,-5),Scale((0.7,0.7)):
        tree(40,3*sin(2*t*pi),1)
        for l in leaves:
            circle(tuple(l),0.5)
        fill(HSVA(0,0,0.5))

animate(loop, duration=3)
