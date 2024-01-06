import pygame
from sprite import player_anim_dict
from interactions import player_interaction
from config import *
from sound import *


class Player(pygame.sprite.Sprite):
    def __init__(self, *groups, x, y, solid_sprites: pygame.sprite.Group,
                 animations=player_anim_dict['christmas']):
        super().__init__()
        for group in groups:
            self.add(group)

        self.animations = animations.copy()
        self.image = pygame.transform.scale(self.animations['standing'][0], (TILE, TILE))
        self.rect = self.image.get_rect(center=(x, y))

        # Анимации
        self.animation_speed = PLAYER_ANIMATION_SPEED
        self.frame_index = 0
        self.status = 'standing'
        self.attacking = False
        self.interacting = False
        self.attack_cooldown = PLAYER_ATTACK_COOLDOWN
        self.interact_cooldown = PLAYER_INTERACTION_COOLDOWN
        self.attack_time = 0
        self.interact_time = 0

        self.solid_sprites = solid_sprites

        # Движение
        self.direction = pygame.math.Vector2()

        # Центровка игрока
        self._central_offset = None
        self.center_target()

    def _image_update(self):
        animations = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animations):
            self.frame_index = 0

        self.image = pygame.transform.scale(animations[int(self.frame_index)], (TILE, TILE))
        self.rect = self.image.get_rect(center=self.rect.center)

    def _get_status(self):
        if self.direction.x == 0 and self.direction.y == 0 and not self.attacking:
            self.status = 'standing'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if self.status == 'standing':
                self.status = 'down_attack'
            elif 'attack' not in self.status:
                self.status += '_attack'

    def update(self):
        self._process_keyboard()
        self._get_status()
        self._cooldowns()
        self._play_sound()
        self._image_update()
        self._move(PLAYER_SPEED)

    def center_target(self):
        self._central_offset = pygame.math.Vector2(self.rect.centerx - HALF_SCREEN_WIDTH,
                                                   self.rect.centery - HALF_SCREEN_HEIGHT)
        self.rect.center -= self._central_offset

    def _process_keyboard(self):
        if not self.attacking:
            pressed_keys = pygame.key.get_pressed()

            # Ввод для движения
            if (pressed_keys[pygame.K_w] or pressed_keys[pygame.K_UP]) and not (
                    pressed_keys[pygame.K_s] or pressed_keys[pygame.K_DOWN]):
                self.direction.y = -1
                self.status = 'up'
            elif (pressed_keys[pygame.K_s] or pressed_keys[pygame.K_DOWN]) and not (
                    pressed_keys[pygame.K_w] or pressed_keys[pygame.K_UP]):
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0
            if (pressed_keys[pygame.K_d] or pressed_keys[pygame.K_RIGHT]) and not (
                    pressed_keys[pygame.K_a] or pressed_keys[pygame.K_LEFT]):
                self.direction.x = 1
                self.status = 'right'
            elif (pressed_keys[pygame.K_a] or pressed_keys[pygame.K_LEFT]) and not (
                    pressed_keys[pygame.K_d] or pressed_keys[pygame.K_RIGHT]):
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            if pressed_keys[pygame.K_e] and not self.interacting:
                self.interact_time = pygame.time.get_ticks()
                self.interacting = True
                player_interaction(self)

            # Ввод для атаки
            if pressed_keys[pygame.K_SPACE] and not self.attacking:
                self.attack_time = pygame.time.get_ticks()
                self.attacking = True
                print('ATTACK')

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

    def _cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
        if self.interacting:
            if current_time - self.interact_time >= self.interact_cooldown:
                self.interacting = False

    def _play_sound(self):
        if self.direction.x or self.direction.y:
            SpritesSound.footstep(1)
