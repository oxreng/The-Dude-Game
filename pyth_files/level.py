from pyth_files.config import *
import pygame
from pyth_files.player import Player
from pyth_files.sprite import *
from pyth_files.cameras import *
from pyth_files.fade import Fade
from pyth_files.ui import UI
from pyth_files.enemy import Enemy
import csv
from random import randint
from pyth_files.death_window import DeathWindow
from pyth_files.minigames.tag import Tag

"""Класс уровня, по которому ходит игрок"""


class Level:
    def __init__(self, screen, clock, to_menu_func, statistic):
        # Получить экран
        self.solid_sprites = self.passable_sprites = self.player_group = self.camera_group = self.player = \
            self.interaction_group = self.attackable_sprites = self.particles_sprites = self.first_group = \
            self.last_group = None
        self.now_level = 'level_1'
        self.screen = screen
        self.clock = clock
        self.to_menu_func = to_menu_func
        self.statistic = statistic
        # Учет уничтожаемых предметов
        self.enemy_log, self.breakable_log = {}, {}

        # Создаём уровень
        self.change_level()

        # Создаём UI пользователю
        self.ui = UI()

    def change_level(self, level_name='level_1', first_player=True, interact_time=None,
                     player_x=HALF_SCREEN_WIDTH - 200, player_y=HALF_SCREEN_HEIGHT - 200):
        """Функция для перехода на уровень, который записан в csv"""
        self.now_level = level_name
        self.solid_sprites = pygame.sprite.Group()
        self.passable_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle()
        self.camera_group = CameraGroup()
        self.interaction_group = pygame.sprite.Group()
        self.particles_sprites = pygame.sprite.Group()
        self.first_group = pygame.sprite.Group()
        self.last_group = pygame.sprite.Group()
        with open(f'{TEXTURES_PATH}/level_csv/{level_name}.csv') as level_file:
            reader = csv.DictReader(level_file, delimiter=';', quotechar='"')
            for item in reader:
                if item['type'] == 'passable':
                    if item['blit'] == 'y':
                        groups = [self.passable_sprites, self.interaction_group]
                    elif item['blit'] == 'first':
                        groups = [self.passable_sprites, self.first_group, self.interaction_group]
                    elif item['blit'] == 'last':
                        groups = [self.passable_sprites, self.last_group, self.interaction_group]
                    PassableSprite(*groups,
                                   file_name=item['name'], x=int(item['x']), y=int(item['y']))
                elif item['type'] == 'solid':
                    if item['blit'] == 'y':
                        groups = [self.solid_sprites, self.camera_group, self.interaction_group]
                    elif item['blit'] == 'first':
                        groups = [self.solid_sprites, self.first_group, self.interaction_group]
                    elif item['blit'] == 'last':
                        groups = [self.solid_sprites, self.last_group, self.interaction_group]
                    SolidSprite(*groups,
                                file_name=item['name'], x=int(item['x']), y=int(item['y']),
                                tiling_x=int(item['tiling_x']) if int(item['tiling_x']) != 0 else TILE,
                                tiling_y=int(item['tiling_y']) if int(item['tiling_y']) != 0 else TILE,
                                partly_passable=(bool(item['partly_passable'])), breakble_log=self.breakable_log)
                elif item['type'] == 'breakable':
                    if item['blit'] == 'y':
                        groups = [self.solid_sprites, self.camera_group, self.interaction_group,
                                  self.attackable_sprites]
                    elif item['blit'] == 'first':
                        groups = [self.solid_sprites, self.first_group, self.interaction_group, self.attackable_sprites]
                    elif item['blit'] == 'last':
                        groups = [self.solid_sprites, self.last_group, self.interaction_group, self.attackable_sprites]
                    SolidSprite(self.solid_sprites, self.camera_group, self.attackable_sprites, self.interaction_group,
                                file_name=item['name'], x=int(item['x']), y=int(item['y']),
                                tiling_x=int(item['tiling_x']), tiling_y=int(item['tiling_y']),
                                breakable=True, id_numb=int(item['id']), partly_passable=bool(item['partly_passable']),
                                breakble_log=self.breakable_log)
                else:
                    Enemy(self.camera_group, self.attackable_sprites, monster_name=item['name'],
                          x=int(item['x']), y=int(item['y']), id_numb=int(item['id']),
                          solid_sprites=self.solid_sprites, damage_player_func=self.damage_player,
                          enemy_log=self.enemy_log)
        if first_player:
            self.player = Player(self.camera_group, self.player_group, x=HALF_SCREEN_WIDTH - 200,
                                 y=HALF_SCREEN_HEIGHT - 200,
                                 solid_sprites=self.solid_sprites, level=self, statistics=self.statistic)
        else:
            self.player = Player(self.camera_group, self.player_group, x=player_x,
                                 y=player_y,
                                 solid_sprites=self.solid_sprites, level=self, hp=self.player.health,
                                 money=self.player.money,
                                 animations=self.player.animations_state, interacting=True,
                                 interact_time=interact_time, statistics=self.statistic)

    def damage_player(self, amount, attack_type):
        """Функция для получения урона игроком"""
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hit_time = pygame.time.get_ticks()
            # Создаём партиклы
            if self.player.health <= 0:
                self.ui.show_in_display(self.player)
                if DeathWindow(self.screen, self.clock, self.start_new_game).run():
                    self.to_menu_func()

    def show(self):
        """Функция для обновления и рисования всего"""
        self.player.update()
        self.particles_sprites.update()
        self.solid_sprites.update()
        self.camera_group.custom_draw(self.first_group, self.last_group, player=self.player, now_level=self.now_level)
        self.player_attack_logic()
        self.ui.show_in_display(self.player)

    def player_attack_logic(self):
        """Логика ударов игрока"""
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
                                                               particle_name='leaf', pos=pos - offset)
                        target_spr.kill()
                        target_spr.break_object()

    def player_interaction(self, interact_time):
        """Взаимодействие игрока с интерактивными объектами"""
        for obj in collide_areas[self.now_level]:
            if obj.rect.colliderect(self.player.rect):
                if obj.type == 'switch_animation':
                    for sprite in self.interaction_group:
                        if sprite.name == obj.name:
                            sprite.animation_state = -sprite.animation_state
                elif obj.type == 'change_outfit':
                    self.player.change_animation_state()
                elif obj.type == 'change_level':
                    Fade(self.screen).fade_in()
                    self.change_level(obj.where, False, interact_time, obj.destination_x, obj.destination_y)
                    self.camera_group.custom_draw(self.first_group, self.last_group, player=self.player,
                                                  now_level=self.now_level)
                    self.ui.show_in_display(self.player)
                    Fade(self.screen).fade_out()
                elif obj.type == 'minigame':
                    if Tag(self.screen, self.clock, tag_images_dict['1']['messed_up'],
                           tag_images_dict['1']['correct']).run():
                        self.change_level(obj.where, False, interact_time, obj.destination_x, obj.destination_y)
                    self.show()
                    Fade(self.screen).fade_out(FADE_SPEED_MENU)

    def start_new_game(self):
        """Старт новой игры"""
        self.enemy_log, self.breakable_log = {}, {}
        self.change_level()
