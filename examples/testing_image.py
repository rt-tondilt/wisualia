import wisualia
from wisualia.shapes import circle, paint
from wisualia.patterns import RGBA, ImagePattern, LinearGradient, RadialGradient
from wisualia.pencil import Pencil
from wisualia.image import Image, RedirectDrawingTo
from wisualia.animation import animate

imi = Image.from_png('example.png')
def loop(t):
    im = imi.copy()
    #with Pencil() as p:
      #  pp =p
    print(im, im.surf.get_data())
    with RedirectDrawingTo(im):
        circle((t*5,0),30)
       #pp.move_to(0,0)
    print(im, im.surf.get_data())
    ip = ImagePattern(im, pixels_per_unit=40)
    paint(ip, alpha=1)

animate(loop)
