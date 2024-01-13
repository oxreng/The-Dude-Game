import pygame
from sprite import player_anim_dict, Entity
from config import *
from sound import *


class Player(Entity):
    def __init__(self, *groups, x, y, solid_sprites: pygame.sprite.Group,
                 animations='normal', hp=PLAYER_STAT_HP, attack=PLAYER_STAT_ATTACK,
                 speed=PLAYER_SPEED, level=None):
        super().__init__(groups)

        # Анимации
        self.status = 'down_idle'
        self.animations_state = animations
        self.animations = player_anim_dict[self.animations_state]
        self.image = pygame.transform.scale(self.animations[self.status][self.frame_index], (TILE, TILE))
        self.rect = self.image.get_rect(center=(x, y))
        self.attacking = False
        self.can_attack = True
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
        self.damage = PLAYER_DAMAGE

        # Центровка игрока
        self._central_offset = None
        self.center_target()

        # Атака
        self.attacking_rect = self.hitbox.copy()

        # Таймер для получения урона
        self.vulnerable_duration = PLAYER_HURT_TIME

        self.level = level

    def _image_update(self):
        animations = self.animations[self.status]

        self.frame_index += self.animation_speed if not self.attacking else self.animation_speed * 4
        if self.frame_index >= len(animations):
            if self.attacking:
                self.attacking = False
                self.frame_index = len(animations) - 1
            else:
                self.frame_index = 0

        self.image = pygame.transform.scale(animations[int(self.frame_index)], (TILE, TILE))
        self.rect = self.image.get_rect(center=self.rect.center)

        # При получении урона делаем "анимацию"
        if not self.vulnerable:
            alpha = self.alpha_get()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

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
                if 'right' in self.status:
                    self.attacking_rect = self.hitbox.copy().move(PLAYER_ATTACK_OFFSET, 0)
                elif 'left' in self.status:
                    self.attacking_rect = self.hitbox.copy().move(-PLAYER_ATTACK_OFFSET, 0)
                elif 'down' in self.status:
                    self.attacking_rect = self.hitbox.copy().move(0, PLAYER_ATTACK_OFFSET)
                else:
                    self.attacking_rect = self.hitbox.copy().move(0, -PLAYER_ATTACK_OFFSET)
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '_idle')

    def get_all_damage(self):
        return self.damage

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
                self.level.player_interaction()

            # Ввод для атаки
            if pressed_keys[pygame.K_SPACE] and self.can_attack:
                self.frame_index = 0
                self.attack_time = pygame.time.get_ticks()
                self.attacking = True
                self.can_attack = False

    def _cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if self.interacting:
            if current_time - self.interact_time >= self.interact_cooldown:
                self.interacting = False

        if not self.vulnerable:
            if current_time - self.hit_time >= self.vulnerable_duration:
                self.vulnerable = True

    def _play_sound(self):
        if self.direction.x or self.direction.y:
            SpritesSound.footstep(1)

    def change_animation_state(self):
        if self.animations_state == 'normal':
            self.animations_state = 'christmas'
        else:
            self.animations_state = 'normal'
        self.animations = player_anim_dict[self.animations_state]
