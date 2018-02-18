import wisualia
from wisualia.do import fill
from wisualia.shapes import circle
from wisualia.modifiers import Move, Rotate
from wisualia.patterns import ImagePattern, RGBA
from wisualia.image import Image
from wisualia.animation import animate, Camera
imag = Image.from_png('example.png')

def loop(t):
    #white = RGBA(1,0.9,0.9)
    black = RGBA(0.3,0.2,0.2)

    m = (t-10)*5/10*(9.8)-1
    n = 30

    with Rotate(n*m*180):
        with Move(-16, -16):

            im = ImagePattern(imag, 5)
    white = im
    for i in range(n):
        with Rotate(i/n*m*180):
            circle((0, 4),4)
            fill(white)
            circle((0, -4),4)
            fill(black)

    for i in range(9,int(round(t))):
        circle((0,4),1)
        fill(white)
        circle((0,-4),1)
        fill(black)


animate(loop, camera=Camera((20,20), 40))
