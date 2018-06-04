
from typing import Optional
import sys

# Pyglet audio works only on windows because on Windows we can play audio
# without starting the Pyglet main loop.

if sys.platform == 'win32':


    from time import perf_counter as program_time # TODO: use player.time instead
    import os, os.path
    import pyglet

    # these variables are private to this module
    player = pyglet.media.Player()
    got_file = False
    delta_t = 0

    def set_file(audio_file_name: Optional[str], program_path: str):
        global got_file
        old_dir = os.getcwd()
        os.chdir(os.path.dirname(program_path))
        print(audio_file_name, program_path)
        try:
            # pyglet.media.load(None) crashes.
            # According to MS event viewer:
            #     "Faulting module name: msvcrt.dll, version: 7.0.15063.0"
            # TODO: Investigate more.
            assert isinstance(audio_file_name, str)
            music = pyglet.media.load(audio_file_name)
            player.next_source()
            player.queue(music)
            got_file = True
        except Exception as e:
            print('can not open audio file',e)
            got_file = False
            stop()
        os.chdir(old_dir)

    def play_from(time):
        global delta_t
        if got_file:
            player.seek(time)
            player.play()
            delta_t = program_time() - time

    def try_play_from(time):
        if got_file:
            if abs(delta_t - (program_time() - time)) > 0.05:
                play_from(time)

    def stop():
        player.pause()


else:
    # Define fake functions.
    def set_file(audio_file_name: Optional[str], program_path: str):
        pass
    def play_from(time):
        pass
    def try_play_from(time):
        pass
    def stop():
        pass
