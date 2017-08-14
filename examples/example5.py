import wisualia
from wisualia import animation, core

import cairo #type: ignore

def cairo_loop(t,cr):
    cr.rectangle(1,1,10,10)
    cr.fill()

USE_ZOOM = True

def loop(t):
    cr = cairo.Context(core.image.surf)
    if USE_ZOOM:
        cr.set_matrix(core.context.get_matrix())
    cairo_loop(t,cr)


animation.animate(loop)
