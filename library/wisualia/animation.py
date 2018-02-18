from typing import Tuple, Callable, Optional
import cairo #type: ignore
import wisualia.core

class Camera(object):
    def __init__(self, size_in_units:Tuple[float, float], pixels_per_unit:float) -> None:
        self.width, self.height = size_in_units
        self.k = pixels_per_unit
    def to_matrix(self): #type: ignore
        m = cairo.Matrix()
        m.scale(self.k, -self.k)
        m.translate(self.width/2, -self.height/2)
        return m
    def draw(self, cr) -> None: #type: ignore
        x = -self.width/2
        y = -self.height/2
        width = self.width
        height = self.height

        INNER, INNER2 = cr.device_to_user_distance(5, 5)
        print(INNER, INNER2)

        cr.new_path()

        cr.set_source_rgba(0.2,0.2,0.2,0.4)
        cr.set_line_width(INNER)
        cr.rectangle(x-INNER/2, y-INNER/2, width+INNER, height+INNER)
        cr.stroke()
        OUTER, OUTER2 = cr.device_to_user_distance(20, 20)
        cr.set_source_rgba(0.2,0.2,0.2,0.2)
        cr.set_line_width(OUTER)
        cr.rectangle(x-OUTER/2, y-OUTER/2, width+OUTER, height+OUTER)
        cr.stroke()

ANIMATION = None #type: Optional[_Animation]

class _Animation(object):
    def __init__(self,
                loop_fn: Callable[[float], None],
                camera:Camera,
                duration:float,
                fps:int,
                audio:Optional[str]) -> None:
        self.loop_fn = loop_fn
        self.camera = camera
        self.duration = duration
        self.fps = fps
        self.audio = audio
    def animate(self) -> None:
        import __main__ #type: ignore
        import moviepy.editor as mpy #type: ignore
        import numpy #type: ignore
        import os
        from contextlib import redirect_stdout
        from io import StringIO

        output_buf = StringIO()

        print('ANIMATSIOON',__main__.__file__)
        def make_frame(numpy_t:numpy.float64) -> numpy.array:
            t = float(numpy_t)
            x = int(self.camera.width * self.camera.k)
            y = int(self.camera.height * self.camera.k)
            surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, x, y)
            cr = cairo.Context(surface)
            cr.set_source_rgb(1,1,1)
            cr.paint()
            cr.set_matrix(self.camera.to_matrix())
            wisualia.core.context = cr
            with redirect_stdout(output_buf):
                self.loop_fn(t)

            transparent = False
            im = 0+numpy.frombuffer(surface.get_data(), numpy.uint8)
            im.shape = (y, x, 4)
            im = im[:,:,[2,1,0,3]] # put RGB back in order
            if False:
                im = im[::-1]
            return im if transparent else im[:,:, :3]

        name = os.path.splitext(__main__.__file__)[0]+ '.mp4'
        try:
            if self.audio is not None:
                audio = mpy.AudioFileClip(self.audio)
                audio.duration = self.duration
            else:
                audio = None
            clip = mpy.VideoClip(make_frame, duration=self.duration)
            clip.audio = audio
            clip.write_videofile(name,fps=self.fps, audio=True)
        except Exception as e:
            print()
            print('ERROR WHILE WRITING VIDEO')
            print('PROGRAMM OUTPUT:')
            print(output_buf.getvalue())
            print('RERAISING EXCEPTION')
            raise e
        output = output_buf.getvalue()
        if output != '':
            print('PROGRAMM OUTPUT:')
            print(output)
            os.system('pause')

def animate(loop_fn: Callable[[float], None],
            camera:Camera=Camera(size_in_units=(16, 12), pixels_per_unit=40), # VGA 640 x 480
            duration:float=10,
            fps:int=25,
            audio:Optional[str]=None) -> None:
    global ANIMATION
    ANIMATION = _Animation(loop_fn, camera, duration, fps, audio)
    import sys
    if len(sys.argv) != 2: return
    if sys.argv[1] != 'animate': return
    ANIMATION.animate()
