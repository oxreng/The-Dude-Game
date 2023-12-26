import pygame

from load_image import load_image
from config import *


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, all_sprites, solid_sprites):
        super().__init__(all_sprites)
        self._now_name_of_image = PLAYER_IMAGE
        self.image = pygame.transform.scale(load_image(PLAYER_PATH + '/default', PLAYER_IMAGE), (TILE, TILE))
        self.rect = self.image.get_rect().move(x, y)
        self._x, self._y = x, y
        self.solid_sprites = solid_sprites

    def update(self):
        self._process_keyboard()

    def _process_keyboard(self):
        pressed_keys = pygame.key.get_pressed()
