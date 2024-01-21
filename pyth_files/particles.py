import pygame
from pyth_files.config import *
from pyth_files.sprite import *


"""Класс партиклов"""


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, *groups,  pos, animations):
        super().__init__(*groups)
        self.frame_index = 0
        self.animation_speed = PARTICLES_ANIMATION_SPEED
        self.animations = animations.copy()
        self.image = self.animations[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def image_update(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animations):
            self.kill()
        else:
            self.image = self.animations[int(self.frame_index)]

    def update(self):
        self.image_update()
