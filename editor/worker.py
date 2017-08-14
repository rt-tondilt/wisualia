from typing import Dict, Any, Optional, Tuple
from multiprocessing import Process, Pipe #type:ignore
from time import process_time
import array
import os.path
import os
import sys
from io import StringIO
from contextlib import redirect_stdout

import cairo #type: ignore

from error_format import get_error
import dir_tools

sys.path.append(dir_tools.get_dir('library'))
# NB: In worker thread, library directory will appear twice inside sys.path.

class Zoom(object):
    def __init__(self, k: float, centre_point: Tuple[float, float]) -> None:
        self.k = k
        self.b_x = centre_point[0] * (1-k)
        self.b_y = centre_point[1] * (1-k)
    @classmethod
    def from_eq(cls, k:float, b_x:float, b_y:float) -> 'Zoom':
        a = cls(k, (0, 0))
        a.b_x = b_x
        a.b_y = b_y
        return a
    def combine(self, other: 'Zoom') -> 'Zoom':
        self.k = other.k *self.k
        self.b_x = other.k * self.b_x + other.b_x
        self.b_y = other.k * self.b_y + other.b_y
        return self


class BytesImage(object):
    def __init__(self, surf):
        self.data = bytes(surf.get_data())
        self.width = surf.get_width()
        self.height = surf.get_height()
    def get_surface(self):
        a = array.array('b', self.data)
        surf= cairo.ImageSurface.create_for_data(a, cairo.FORMAT_ARGB32,
                                                 self.width, self.height)
        return surf


class Request(object):
    def __init__(self, t: float, x: int, y: int, zoom: Zoom, grid: bool) -> None:
        self.t = t
        self.x = x
        self.y = y
        self.zoom = zoom
        self.grid = grid

class Response(object):
    pass
class InitSuccess(Response):
    def __init__(self, audio_file_name: str):
        self.audio_file_name = audio_file_name
class Success(Response):
    def __init__(self, data: BytesImage, result: str) -> None:
        self.data = data
        self.result = result

class Failure(Response):
    def __init__(self, error: str) -> None:
        self.error = error
t='''
from library import wisualia
def loop():
    return 7
'''




def worker_fn(con):
    (code, file_name) = con.recv() # type: str

    sys.path[0]=os.path.dirname(file_name)
    os.chdir(os.path.dirname(file_name))
    assert isinstance(code, str)
    vars = {} # type: Dict[str, Any]
    try:
        code = compile(code, file_name, 'exec')
        exec(code, vars)
        audio_file_name = vars['wisualia'].animation.AUDIO
    except Exception:
        con.send(Failure(get_error()))
        return
    con.send(InitSuccess(audio_file_name)) # Succesful init
    # TODO: Check whether wisualia was properly imported.

    while True:
        request = con.recv() # type: Request
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, request.x, request.y)
        cr = cairo.Context(surf)


        try:
            if request.grid:
                vars['wisualia'].core._draw_grid(
                    cr,
                    request.zoom.k,
                    request.zoom.b_x,
                    request.zoom.b_y,
                    request.x,
                    request.y)
            cr.translate(request.zoom.b_x, request.zoom.b_y)
            cr.scale(request.zoom.k, - request.zoom.k)
            vars['wisualia'].core.context = cr
            vars['wisualia'].core.image = vars['wisualia'].image.Image.from_cairo_surface(surf)
            f = StringIO()
            with redirect_stdout(f):
                vars['loop'](request.t)
            result = f.getvalue()
            vars['wisualia'].animation.CAMERA.draw(cr)
        except Exception :
            con.send(Failure(get_error()))
            return
        surf.flush()

        con.send(Success(BytesImage(surf), result)) #type: ignore


class Worker(object):
    def __init__(self, code: str, file_name: str) -> None:
        parent, child = Pipe()
        self.process = Process(target=worker_fn, name='WISUALIA ENGINE', args=(child,), daemon=True)
        self.con = parent
        self.process.start()
        self.con.send((code, file_name))
    def __del__(self):
        self.process.terminate()
    '''def recv_init(self):
        return self.con.recv()'''
    def send(self, r: Request):
        self.con.send(r)
    def recv(self) -> Optional[Response]:
        if self.con.poll():
            return self.con.recv()
        return None
