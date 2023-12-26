import random

import pygame
from config import *


"""
Принцип работы музыки в игре
"""


class Music:
    def __init__(self, path=MUSIC_FILES):
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.mixer.init()
        self.path = path
        self.theme = pygame.mixer.music
        self.init_track()

    def init_track(self):
        self.theme.load(random.choice(self.path))
        for file in self.path:
            self.theme.queue(file)

    def play_music(self):
        if self.theme.get_volume() != 0:
            self.theme.set_volume(0.1)
            self.theme.play()

    def change_music_volume(self, volume):
        self.theme.set_volume(volume)

    def return_volume(self):
        return self.theme.get_volume()


class MenuMusic(Music):
    def __init__(self, path):
        super().__init__(path)
        self.path = path

    def init_track(self):
        self.theme.load(self.path)


class SoundEffect:
    ...


class SpritesSound:
    ...