import collections
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
            self.theme.set_volume(0.08)
            self.theme.play(-1)

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
    def __init__(self, path):
        self.effect = None
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.mixer.init()
        self.init_track(path)

    def init_track(self, path):
        self.effect = pygame.mixer.Sound(path)

    def play_sound(self, channel=2):
        if not pygame.mixer.Channel(channel).get_busy():
            pygame.mixer.Channel(channel).play(self.effect)

    @staticmethod
    def change_effects_volume(volume):
        for channel in range(1, 5):
            pygame.mixer.Channel(channel).set_volume(volume)

    @staticmethod
    def return_volume():
        return pygame.mixer.Channel(1).get_volume()


class SpritesSound:
    @staticmethod
    def footstep_sound(channel=2):
        current_step = steps_collection[0]
        steps_collection.rotate(-1)
        SoundEffect(f'sound/{current_step}.mp3').play_sound(channel)

    @staticmethod
    def punching_sound(channel=2):
        SoundEffect(SOUND_PUNCH).play_sound(channel)

    @staticmethod
    def damage_receiving_sound(channel=2):
        SoundEffect(SOUND_DAMAGE_RECEIVING).play_sound(channel)

    @staticmethod
    def death_sound(channel=2):
        SoundEffect(SOUND_DEATH).play_sound(channel)

    @staticmethod
    def button_sound(channel=2):
        SoundEffect(SOUND_BUTTON_PUSH).play_sound(channel)


steps_collection = collections.deque(
    [f'step_{i}' for i in range(3)])
