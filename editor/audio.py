import os, os.path
import pygame


pygame.mixer.init()
pygame.init()

pmm = pygame.mixer.music

class Audio(object):
    def __init__(self):
        self.file = None
    def set_file(self, file, path):
        self.file = file
        if file != None and path != None:
            os.chdir(os.path.dirname(path))
            try:
                pmm.load(file)
            except:
                print('can not open file')
                self.file = None
    def play_from(self, time):
        print('PLAY FROMMMMMMMMMMMMMMMMMMM')
        if self.file != None:
            pmm.stop()
            pmm.play()
            pmm.rewind()
            pmm.set_pos(time)
    def pause(self):
        pmm.stop()
