import collections
import json
import random
import pygame
from pyth_files.config import *

"""
Принцип работы музыки в игре
"""


def get_volume_from_fson():
    with open(VOLUME_ALL_PATH, 'r') as f:
        return [*json.load(f).values()]


class Music:
    def __init__(self, path=MUSIC_FILES):
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.mixer.init()
        self.path = path
        self.theme = pygame.mixer.music
        self.init_track()
        self.change_music_volume(get_volume_from_fson()[0])

    def init_track(self):
        self.theme.load(random.choice(self.path))

    def play_music(self):
        self.theme.play(-1)

    def change_music_volume(self, volume):
        self.theme.set_volume(volume)

    def return_volume(self):
        return self.theme.get_volume()


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
        for channel in range(1, 7):
            pygame.mixer.Channel(channel).set_volume(volume)

    @staticmethod
    def return_volume():
        return pygame.mixer.Channel(1).get_volume()


class SpritesSound:
    @staticmethod
    def footstep_sound(channel=2):
        current_step = steps_collection[0]
        steps_collection.rotate(-1)
        SoundEffect(f'data/music/sound/{current_step}.mp3').play_sound(channel)

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

    @staticmethod
    def boom_sound(channel=2):
        SoundEffect(SOUND_END_SCREEN_BOOM).play_sound(channel)

    @staticmethod
    def player_death_sound(channel=2):
        SoundEffect(SOUND_PLAYER_DEATH).play_sound(channel)

    @staticmethod
    def open_door_sound(channel=2):
        SoundEffect(SOUND_OPEN_DOOR).play_sound(channel)

    @staticmethod
    def hatch_sound(channel=2):
        SoundEffect(SOUND_HATCH).play_sound(channel)

    @staticmethod
    def tag_trick_sound(channel=2):
        SoundEffect(SOUND_TAG_TRICK).play_sound(channel)

    @staticmethod
    def enemy_spawn_sound(channel=2):
        SoundEffect(SOUND_ENEMY_SPAWN).play_sound(channel)


# Коллекция для звуков шагов
steps_collection = collections.deque(
    [f'step_{i}' for i in range(3)])
