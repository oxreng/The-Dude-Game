import pygame
from load_image import load_image
from config import *


class Player(pygame.sprite.Sprite):
    def __init__(self, *groups, x, y, solid_sprites: pygame.sprite.Group, partly_sprites: pygame.sprite.Group):
        super().__init__()
        for group in groups:
            self.add(group)
        self._now_name_of_image = PLAYER_IMAGE
        self.image = pygame.transform.scale(load_image(PLAYER_PATH + '/default', PLAYER_IMAGE), (TILE, TILE))
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self._on_ground = True
        self.solid_sprites = solid_sprites
        self.partly_passable_sprites = partly_sprites
        self.last_y = y
        self.direction = pygame.math.Vector2()

    def update(self):
        self._process_keyboard()

    def _process_keyboard(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_SPACE] and self._on_ground:
            self.last_y = self.rect.y
            self.direction.y -= 40
            self._on_ground = False
        if pressed_keys[pygame.K_a] or pressed_keys[pygame.K_LEFT]:
            self.direction.x -= PLAYER_SPEED / FPS
        if pressed_keys[pygame.K_d] or pressed_keys[pygame.K_RIGHT]:
            self.direction.x += PLAYER_SPEED / FPS
        if self._can_move():
            self.rect.x += self.direction.x
        self.direction.x = 0
        if self._on_ground:
            if pressed_keys[pygame.K_w] or pressed_keys[pygame.K_UP]:
                self.direction.y -= PLAYER_SPEED / FPS
            if pressed_keys[pygame.K_s] or pressed_keys[pygame.K_DOWN]:
                self.direction.y += PLAYER_SPEED / FPS
            if self._can_move():
                self.rect.y += self.direction.y
            self.direction.y = 0
        else:
            if self.rect.y > self.last_y:
                self._on_ground = True
                self.rect.y = self.last_y
                self.direction.y = 0
            else:
                self.direction.y += 3
            self.rect.y += self.direction.y

    def _can_move(self):
        self.rect.center += self.direction
        if pygame.sprite.spritecollide(self, self.solid_sprites, False, pygame.sprite.collide_mask) or (
                pygame.sprite.spritecollide(self, self.partly_passable_sprites, False, pygame.sprite.collide_mask)):
            self.rect.center -= self.direction
            return False
        self.rect.center -= self.direction
        return True
