import pygame
from pyth_files.config import *
from pyth_files.sprite import *
from pyth_files.sound import SpritesSound

"""Враги"""


class Enemy(Entity):
    def __init__(self, *groups, monster_name, x, y, solid_sprites, id_numb, enemy_log, damage_player_func=None):
        super().__init__(groups)

        # Картинки
        self.animations = enemy_anim_dict[monster_name]
        self.status = 'down_idle'
        self.image = pygame.transform.scale(self.animations['down_idle'][self.frame_index], (TILE, TILE))

        # Передвижение
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = self.rect.copy()
        self.solid_sprites = solid_sprites

        # Статы
        self.monster_name = monster_name
        info = monster_data[self.monster_name]
        self.health = info['health']
        self.money = info['money']
        self.speed = info['speed']
        self.attack_damage = info['damage']
        self.attack_radius = info['attack_radius']
        self.attack_type = info['attack_type']
        self.resistance = info['resistance']
        self.notice_radius = info['notice_radius']

        # Взаимодействие с игроком
        self.can_attack = True
        self.attack_time = None
        self.attacking = False
        self.attack_cooldown = info['attack_cooldown']
        self.damage_player = damage_player_func

        # Спавнить или нет врага
        self.enemy_log = enemy_log
        if id_numb not in enemy_log:
            enemy_log[id_numb] = True
        else:
            self.check_existence(id_numb)
        self.id_numb = id_numb

        # Таймер для ударов игрока
        self.vulnerable_duration = ENEMY_VULNERABLE_DURATION

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)
        self.image_update()
        self.cooldowns()
        self.hit_reaction()
        self.move(self.speed)

    def get_player_distance_direction(self, player):
        """Путь до игрока + направление"""
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return distance, direction

    def get_status(self, player):
        """Обновление анимаций"""
        distance, direction = self.get_player_distance_direction(player)
        if distance <= self.attack_radius and self.can_attack and not self.attacking:
            if 'attack' not in self.status:
                self.frame_index = 0
            if abs(direction.x) >= abs(direction.y):
                if direction.x > 0:
                    self.status = 'right_attack'
                else:
                    self.status = 'left_attack'
            else:
                if direction.y > 0:
                    self.status = 'down_attack'
                else:
                    self.status = 'up_attack'
        elif distance <= self.notice_radius and not self.attacking:
            if abs(direction.x) >= abs(direction.y):
                if direction.x > 0:
                    self.status = 'right'
                else:
                    self.status = 'left'
            else:
                if direction.y > 0:
                    self.status = 'down'
                else:
                    self.status = 'up'
        elif self.attacking:
            pass
        else:
            self.status = 'down_idle'

    def actions(self, player):
        """Взаимодействие с игроком (удар, идти к игроку, стоять)"""
        if 'attack' in self.status and self.can_attack and not self.attacking:
            self.attack_time = pygame.time.get_ticks()
            self.can_attack = False
            self.attacking = True
            SpritesSound.damage_receiving_sound(4)
            self.damage_player(self, self.attack_damage, self.attack_type)
        elif self.status in ('up', 'down', 'left', 'right'):
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def image_update(self):
        """Делаем анимации врагам"""
        animations = self.animations[self.status]

        self.frame_index += self.animation_speed if not self.attacking else self.animation_speed * 2
        if self.frame_index >= len(animations):
            if self.attacking:
                self.attacking = False
                self.frame_index = len(animations) - 1
            else:
                self.frame_index = 0

        self.image = pygame.transform.scale(animations[int(self.frame_index)], (TILE, TILE))
        self.rect = self.image.get_rect(center=self.hitbox.center)

        # При получении урона делаем "анимацию"
        if not self.vulnerable:
            alpha = self.alpha_get()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldowns(self):
        """Обновляем кулдауны"""
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.vulnerable_duration:
                self.vulnerable = True

    def get_damage(self, player):
        """Функция для получения урона"""
        if self.vulnerable:
            self.direction = self.get_player_distance_direction(player)[1]
            self.health -= player.get_all_damage()
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def check_death(self, player):
        """Функция для проверки смерти"""
        if self.health <= 0:
            self.kill()
            self.enemy_log[self.id_numb] = False
            player.money += self.money
            SpritesSound.death_sound(2)

    def check_existence(self, id_numb):
        """Функция для проверки на 'убили' ли врага"""
        if self.enemy_log[id_numb] is False:
            self.kill()

    def hit_reaction(self):
        """Отбрасываем врага, если его ударили"""
        if not self.vulnerable:
            self.direction *= -self.resistance
