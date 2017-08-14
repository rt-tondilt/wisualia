import wisualia
from wisualia.shapes import circle
from wisualia import animation


def loop(t):
    for x in range(0, int(t*8+1)):
        for y in range(0, int(t*8+1)):
            circle((x/5+t-7, y/5-4), 0.08)
    circle((40, 40), 20)


animation.animate(loop)