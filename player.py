import pygame
from sprite import player_anim_dict
from config import *


class Player(pygame.sprite.Sprite):
    def __init__(self, *groups, x, y, solid_sprites: pygame.sprite.Group,
                 animations=player_anim_dict['christmas'], animation_speed=SPRITE_ANIMATION_SPEED / 2):
        super().__init__()
        for group in groups:
            self.add(group)

        self.default_animations = animations.copy()
        self.animations = animations
        self.image = pygame.transform.scale(self.animations['standing'][0], (TILE, TILE))
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_speed = animation_speed
        self.left = self.right = self.down = self.up = False

        self.solid_sprites = solid_sprites

        self.last_y = y
        self.direction = pygame.math.Vector2()
        self.center_target()

    def _image_update(self):
        self.animation_count += 1
        if self.animation_speed <= self.animation_count:
            if not any([self.left, self.right, self.down, self.up]):
                self.animations['standing'].rotate(-1)
                image = self.animations['standing'][0]
            elif self.up:
                self.animations['up'].rotate(-1)
                image = self.animations['up'][0]
            elif self.down:
                self.animations['down'].rotate(-1)
                image = self.animations['down'][0]
            elif self.right:
                self.animations['right'].rotate(-1)
                image = self.animations['right'][0]
            else:
                self.animations['left'].rotate(-1)
                image = self.animations['left'][0]
            self.image = pygame.transform.scale(image, (TILE, TILE))
            self.mask = pygame.mask.from_surface(self.image)
            self.animation_count = 0

    def _rotation_switch(self):
        pressed_keys = pygame.key.get_pressed()
        if any([self.left != (pressed_keys[pygame.K_a] or pressed_keys[pygame.K_LEFT]),
                self.right != (pressed_keys[pygame.K_d] or pressed_keys[pygame.K_RIGHT]),
                self.up != (pressed_keys[pygame.K_w] or pressed_keys[pygame.K_UP]),
                self.down != (pressed_keys[pygame.K_s] or pressed_keys[pygame.K_DOWN])]):
            self.animation_count = self.animation_speed
        self.left = pressed_keys[pygame.K_a] or pressed_keys[pygame.K_LEFT]
        self.right = pressed_keys[pygame.K_d] or pressed_keys[pygame.K_RIGHT]
        self.up = pressed_keys[pygame.K_w] or pressed_keys[pygame.K_UP]
        self.down = pressed_keys[pygame.K_s] or pressed_keys[pygame.K_DOWN]

    def update(self):
        self._rotation_switch()
        self._image_update()
        self._process_keyboard()
        self._move(PLAYER_SPEED)

    def center_target(self):
        self.rect.center -= pygame.math.Vector2(self.rect.centerx - HALF_SCREEN_WIDTH,
                                                self.rect.centery - HALF_SCREEN_HEIGHT)

    def _process_keyboard(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_a] or pressed_keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif pressed_keys[pygame.K_d] or pressed_keys[pygame.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0
        if pressed_keys[pygame.K_w] or pressed_keys[pygame.K_UP]:
            self.direction.y = -1
        elif pressed_keys[pygame.K_s] or pressed_keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

    def _move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.rect.x += self.direction.x * speed
        self._collision('horizontal')
        self.rect.y += self.direction.y * speed
        self._collision('vertical')

    def _collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.solid_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.rect.left = sprite.rect.right
        if direction == 'vertical':
            for sprite in self.solid_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom
