from typing import Dict, Any, Optional, Tuple
from multiprocessing import Process, Pipe #type:ignore
from time import process_time
import array
import os.path
import os
import sys
from io import StringIO
from contextlib import redirect_stdout
from enum import Enum

import cairo #type: ignore

from error_format import get_error
import dir_tools

sys.path.append(dir_tools.relative_to_wisualia('library'))
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


class DrawRequest(object):
    def __init__(self, t: float, x: int, y: int, zoom: Zoom, grid: bool) -> None:
        self.t = t
        self.x = x
        self.y = y
        self.zoom = zoom
        self.grid = grid
class CompileRequest(object):
    def __init__(self, code, file_name):
        self.code = code
        self.file_name = file_name

class Response(object):
    pass
class InitSuccess(Response):
    def __init__(self,animation_duration: float, audio_file_name: str):
        self.animation_duration = animation_duration
        self.audio_file_name = audio_file_name
class Success(Response):
    def __init__(self, data: BytesImage, result: str) -> None:
        self.data = data
        self.result = result

class Failure(Response):
    def __init__(self, output: str, error: str) -> None:
        self.output = output
        self.error = error


def worker_fn(con):
    code = None
    wisualia = None
    while True:
        request = con.recv()

        if isinstance(request, CompileRequest):

            sys.path[0]=os.path.dirname(request.file_name)
            os.chdir(os.path.dirname(request.file_name))
            assert isinstance(request.code, str)
            vars = {} # type: Dict[str, Any]
            try:
                # Forget any previous animation configuration
                if wisualia != None:
                    wisualia.animation.ANIMATION = None

                code = compile(request.code, request.file_name, 'exec')
                f = StringIO()
                with redirect_stdout(f):
                    exec(code, vars)
                wisualia = vars['wisualia']
                animation_duration = vars['wisualia'].animation.ANIMATION.duration
                audio_file_name = vars['wisualia'].animation.ANIMATION.audio
                assert (isinstance(animation_duration, float) or
                        isinstance(animation_duration, int))
                assert isinstance(audio_file_name, str) or audio_file_name == None
            except Exception:
                output=''
                try:
                    output=f.getvalue()
                except: pass
                con.send(Failure(output, get_error()))
                continue
            con.send(InitSuccess(animation_duration, audio_file_name))
            # TODO: Check whether wisualia was properly imported.

        elif isinstance(request, DrawRequest):
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
                    vars['wisualia'].animation.ANIMATION.loop_fn(request.t)
                result = f.getvalue()
                vars['wisualia'].animation.ANIMATION.camera.draw(cr)
            except Exception :
                output=''
                try:
                    output=f.getvalue()
                except: pass
                con.send(Failure(output, get_error()))
                return
            surf.flush()
            con.send(Success(BytesImage(surf), result)) #type: ignore
        else: assert False


class Worker(object):
    def __init__(self) -> None:
        parent, child = Pipe()
        self.process = Process(target=worker_fn, name='WISUALIA ENGINE', args=(child,), daemon=True)
        self.con = parent
        self.process.start()
        self.working = False
    def send(self, data):
        assert not self.working
        self.con.send(data)
        self.working = True
    def recv(self):
        if self.con.poll():
            self.working = False
            return self.con.recv()
        return None
    def is_working(self):
        return self.working

    def __del__(self):
        self.process.terminate()
