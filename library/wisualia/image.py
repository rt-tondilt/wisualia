import cairo #type: ignore
from wisualia import core

class Image(object):
    def __init__(self, width:int, height:int) -> None:
        self.surf = cairo.ImageSurface(cairo.Format.ARGB32, width, height)
    def create_similar(self) -> 'Image':
        surf = self.surf.create_similar_image(self.surf.get_format(),
                                              self.surf.get_width(),
                                              self.surf.get_height())
        return Image.from_cairo_surface(surf)
    def copy(self) -> 'Image':
        copy = self.create_similar()
        cr = cairo.Context(copy.surf)
        cr.set_source(cairo.SurfacePattern(self.surf))
        cr.paint()
        return copy
    def write_to_png(self, name: str) -> None:
        self.surf.write_to_png(name)
    @classmethod
    def from_cairo_surface(cls, cairo_surface) -> 'Image': #type: ignore
        image = cls.__new__(cls) #type: ignore
        image.surf = cairo_surface
        return image #type:ignore
    @classmethod
    def from_png(cls, file_name:str) -> 'Image':
        return cls.from_cairo_surface(cairo.ImageSurface.create_from_png(file_name))

class RedirectDrawingTo(object):
    def __init__(self, image:Image) -> None:
        self.image = image
    def __enter__(self) -> None:
        self.old_image = core.image
        self.old_cr = core.context
        core.image = self.image
        core.context = cairo.Context(core.image.surf)
    def __exit__(self, exc_type: None, exc_value: None, traceback: None) -> bool:
        core.image = self.old_image
        core.context = self.old_cr
        return False # reraise potential exception
