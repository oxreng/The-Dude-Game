from config import *
import pygame
from player import Player
from sprite import *
from interactions import collide_areas
from cameras import *
from debug import debug
from ui import UI
from enemy import Enemy
import csv
from random import randint


class Level:
    def __init__(self):
        # Получить экран
        self.solid_sprites = self.passable_sprites = self.player_group = self.camera_group = self.player = \
            self.interaction_group = self.attackable_sprites = self.particles_sprites = None
        self.now_level = 'level_1'
        self._display_surface = pygame.display.get_surface()

        # Создаём уровень
        self.change_level()

        # Создаём UI пользователю
        self.ui = UI()

    def change_level(self, level_name='level_1', first_player=True, area=None, interact_time=None):
        self.now_level = level_name
        self.solid_sprites = pygame.sprite.Group()
        self.passable_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle()
        self.camera_group = CameraGroup()
        self.interaction_group = pygame.sprite.Group()
        self.particles_sprites = pygame.sprite.Group()
        with open(f'{TEXTURES_PATH}/level_csv/{level_name}.csv') as level_file:
            reader = csv.DictReader(level_file, delimiter=';', quotechar='"')
            for item in reader:
                if item['type'] == 'passable':
                    PassableSprite(self.passable_sprites, self.interaction_group,
                                   file_name=item['name'], x=int(item['x']), y=int(item['y']))
                elif item['type'] == 'solid':
                    SolidSprite(self.solid_sprites, self.camera_group, self.interaction_group,
                                file_name=item['name'], x=int(item['x']), y=int(item['y']),
                                tiling_x=int(item['tiling_x']) if int(item['tiling_x']) != 0 else TILE,
                                tiling_y=int(item['tiling_y']) if int(item['tiling_y']) != 0 else TILE,
                                partly_passable=(bool(item['partly_passable'])))
                elif item['type'] == 'breakable':
                    SolidSprite(self.solid_sprites, self.camera_group, self.attackable_sprites, self.interaction_group,
                                file_name=item['name'], x=int(item['x']), y=int(item['y']),
                                tiling_x=int(item['tiling_x']), tiling_y=int(item['tiling_y']),
                                breakable=True, id_numb=int(item['id']), partly_passable=bool(item['partly_passable']))
                else:
                    Enemy(self.camera_group, self.attackable_sprites, monster_name=item['name'],
                          x=int(item['x']), y=int(item['y']), id_numb=int(item['id']),
                          solid_sprites=self.solid_sprites, damage_player_func=self.damage_player)
        if first_player:
            self.player = Player(self.camera_group, self.player_group, x=HALF_SCREEN_WIDTH - 200,
                                 y=HALF_SCREEN_HEIGHT - 200,
                                 solid_sprites=self.solid_sprites, level=self)
        else:
            self.player = Player(self.camera_group, self.player_group, x=area.x + 50,
                                 y=area.y + 150,
                                 solid_sprites=self.solid_sprites, level=self, hp=self.player.health,
                                 animations=self.player.animations_state, interacting=True,
                                 interact_time=interact_time)
        # self.camera_group.center_target_camera(self.player)

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hit_time = pygame.time.get_ticks()
            # Создаём партиклы

    def show(self):
        self.player.update()
        self.particles_sprites.update()
        self.solid_sprites.update()
        self.camera_group.custom_draw(self.passable_sprites, player=self.player, now_level=self.now_level)
        self.player_attack_logic()
        self.ui.show_in_display(self.player)

    def zoom_cam(self, event_button):
        self.camera_group.zooming(event_button)

    def player_attack_logic(self):
        if self.player.attacking:
            rect = self.player.attacking_rect
            for target_spr in self.attackable_sprites:
                if rect.colliderect(target_spr.hitbox):
                    if isinstance(target_spr, Enemy):
                        target_spr.get_damage(self.player)
                    else:
                        pos = target_spr.rect.center
                        offset = pygame.math.Vector2(0, 75)
                        for _ in range(randint(3, 6)):
                            self.camera_group.particles_create(self.camera_group, self.particles_sprites,
                                                               particle_name='leaf', pos=pos-offset)
                        target_spr.kill()
                        target_spr.break_object()

    def player_interaction(self, interact_time):
        for obj in collide_areas[self.now_level]:
            if obj.rect.colliderect(self.player.rect):
                if obj.type == 'switch_animation':
                    for sprite in self.interaction_group:
                        if sprite.name == obj.name:
                            sprite.animation_state = -sprite.animation_state
                elif obj.type == 'change_outfit':
                    self.player.change_animation_state()
                elif obj.type == 'change_level':
                    self.change_level(obj.where, False, obj.rect, interact_time)
