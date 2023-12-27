import pygame
from load_image import load_image
from config import *


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, player_group, solid_sprites: pygame.sprite.Group):
        super().__init__(player_group)
        self._now_name_of_image = PLAYER_IMAGE
        self.image = pygame.transform.scale(load_image(PLAYER_PATH + '/default', PLAYER_IMAGE), (TILE, TILE))
        self.rect = self.image.get_rect().move(x, y)
        self.mask = pygame.mask.from_surface(self.image)
        self._on_ground = True
        self.solid_sprites = solid_sprites
        self.last_y = y
        self._dx = self._dy = 0

    def update(self):
        self._process_keyboard()

    def _process_keyboard(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_SPACE] and self._on_ground:
            self.last_y = self.rect.y
            self._dy -= 40
            self._on_ground = False
        if pressed_keys[pygame.K_a] or pressed_keys[pygame.K_LEFT]:
            self._dx -= PLAYER_SPEED / FPS
        if pressed_keys[pygame.K_d] or pressed_keys[pygame.K_RIGHT]:
            self._dx += PLAYER_SPEED / FPS
        if self._can_move():
            self.rect.x += self._dx
        self._dx = 0
        if self._on_ground:
            if pressed_keys[pygame.K_w] or pressed_keys[pygame.K_UP]:
                self._dy -= PLAYER_SPEED / FPS
            if pressed_keys[pygame.K_s] or pressed_keys[pygame.K_DOWN]:
                self._dy += PLAYER_SPEED / FPS
            if self._can_move():
                self.rect.y += self._dy
            self._dy = 0
        else:
            if self.rect.y > self.last_y:
                self._on_ground = True
                self.rect.y = self.last_y
                self._dy = 0
            else:
                self._dy += 3
            self.rect.y += self._dy

    def _can_move(self):
        self.rect.x += self._dx
        self.rect.y += self._dy
        if pygame.sprite.spritecollide(self, self.solid_sprites, False, pygame.sprite.collide_mask):
            self.rect.x -= self._dx
            self.rect.y -= self._dy
            return False
        self.rect.x -= self._dx
        self.rect.y -= self._dy
        return True

