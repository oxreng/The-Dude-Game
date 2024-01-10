import pygame
from sprite import player_anim_dict, Entity
from interactions import player_interaction
from config import *
from sound import *


class Player(Entity):
    def __init__(self, *groups, x, y, solid_sprites: pygame.sprite.Group,
                 animations='normal', hp=PLAYER_STAT_HP, attack=PLAYER_STAT_ATTACK,
                 speed=PLAYER_SPEED):
        super().__init__(groups)

        # Анимации
        self.status = 'down_idle'
        self.animations_state = animations
        self.animations = player_anim_dict[self.animations_state]
        self.image = pygame.transform.scale(self.animations[self.status][self.frame_index], (TILE, TILE))
        self.rect = self.image.get_rect(center=(x, y))
        self.attacking = False
        self.interacting = False
        self.attack_cooldown = PLAYER_ATTACK_COOLDOWN
        self.interact_cooldown = PLAYER_INTERACTION_COOLDOWN
        self.attack_time = 0
        self.interact_time = 0
        self.hitbox = self.rect.inflate((-20, 0))

        # Спрайты, через которые мы не проходим
        self.solid_sprites = solid_sprites

        # Статистика
        self.stats = {'health': hp, 'attack': attack, 'speed': speed}
        self.health = self.stats['health']
        self.money = 123
        self.speed = self.stats['speed']

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
            if 'idle' not in self.status and 'attack' not in self.status:
                self.status += '_idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if 'attack' not in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status += '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    def update(self):
        self._process_keyboard()
        self._get_status()
        self._cooldowns()
        self._play_sound()
        self._image_update()
        self.move(self.speed)

    def center_target(self):
        # self._central_offset = pygame.math.Vector2(self.rect.centerx - HALF_SCREEN_WIDTH,
        # self.rect.centery - HALF_SCREEN_HEIGHT)
        # self.rect.center -= self._central_offset
        pass

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

    def change_animation_state(self):
        if self.animations_state == 'normal':
            self.animations_state = 'christmas'
        else:
            self.animations_state = 'normal'
        self.animations = player_anim_dict[self.animations_state]
