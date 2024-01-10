import pygame
from config import *
from sprite import *


class Enemy(Entity):
    def __init__(self, *groups, monster_name, x, y, solid_sprites):
        super().__init__(groups)

        # Картинки
        self.animations = player_anim_dict[monster_name]
        self.status = 'down_idle'
        self.image = pygame.transform.scale(self.animations['down_idle'][self.frame_index], (TILE, TILE))

        # Передвижение
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = self.rect.inflate(-30, -10)
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
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius:
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'down_idle'

    def actions(self, player):
        if self.status == 'attack':
            print('ATTACK')
        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)
        self.move(self.speed)

    def image_update(self):
        pass
