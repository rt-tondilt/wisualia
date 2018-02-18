import wisualia
from wisualia import animation, core

import cairo #type: ignore

def cairo_loop(t,cr):
    cr.scale(0.1,0.1)
    pattern = cairo.MeshPattern()
    pattern.begin_patch()
    pattern.move_to(0, 0)
    pattern.curve_to(30, -30, 60, 30, 100, 0)
    pattern.curve_to(60, 30, 130, 60, 100, 100)
    pattern.curve_to(60, 70, 30, 130, 0, 100)
    pattern.curve_to(30, 70, -30, 30, 0, 0)
    pattern.set_corner_color_rgb(0, 1, 0, 0)
    pattern.set_corner_color_rgb(1, 0, 1, 0)
    pattern.set_corner_color_rgb(2, 0, 0, 1)
    pattern.set_corner_color_rgb(3, 1, 1, 0)
    pattern.end_patch()

    # Add a Gouraud-shaded triangle
    pattern = cairo.MeshPattern()
    pattern.begin_patch()
    pattern.move_to(100, 100)
    pattern.line_to(130, 130)
    pattern.line_to(130, 70)
    pattern.set_corner_color_rgb(0, 1, 0, 0)
    pattern.set_corner_color_rgb(1, 0, 1, 0)
    pattern.set_corner_color_rgb(2, 0, 0, 1)
    pattern.end_patch()
    cr.set_source(pattern)
    cr.paint()

USE_ZOOM = True

def loop(t):
    cr = cairo.Context(core.image.surf)
    if USE_ZOOM:
        cr.set_matrix(core.context.get_matrix())
    cairo_loop(t,cr)


animation.animate(loop,animation.Camera((30,30),40))
