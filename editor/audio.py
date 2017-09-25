from typing import Optional
from time import perf_counter as program_time
import os, os.path
import pyglet
player = pyglet.media.Player()

got_file = False
delta_t = 0


def set_file(audio_file_name: Optional[str], program_path: str):
    global got_file
    old_dir = os.getcwd()
    os.chdir(os.path.dirname(program_path))
    print(audio_file_name, program_path)
    try:
        music = pyglet.media.load(audio_file_name)
        player.next_source()
        player.queue(music)
        got_file = True
    except Exception as e:
        print('can not open file',e)
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
