import pygame
from config import *
from sprite import *


class Enemy(Entity):
    def __init__(self, *groups, monster_name, x, y, solid_sprites):
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
        self.monster_name = 'skeleton'
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
        self.attack_cooldown = info['attack_cooldown']

    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return distance, direction

    def get_status(self, player):
        distance, direction = self.get_player_distance_direction(player)

        if distance <= self.attack_radius and self.can_attack:
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
        elif distance <= self.notice_radius:
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
        else:
            self.status = 'down_idle'

    def actions(self, player):
        if 'attack' in self.status:
            self.attack_time = pygame.time.get_ticks()
        elif self.status in ('up', 'down', 'left', 'right'):
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def image_update(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if 'attack' in self.status:
                self.can_attack = False
            self.frame_index = 0

        self.image = pygame.transform.scale(animation[int(self.frame_index)], (TILE, TILE))
        self.rect = self.image.get_rect(center=self.hitbox.center)
        
    def cooldown(self):
        if not self.can_attack:
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)
        self.image_update()
        self.cooldown()
        self.move(self.speed)
