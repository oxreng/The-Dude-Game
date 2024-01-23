from pyth_files.config import *
import pygame
from pyth_files.end_screen import EndScreen
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
from pyth_files.dialogue import Dialogue

"""Класс уровня, по которому ходит игрок"""


class Level:
    def __init__(self, screen, clock, to_menu_func, statistic, theme):
        # Получить экран
        self.solid_sprites = self.passable_sprites = self.player_group = self.camera_group = self.player = \
            self.interaction_group = self.attackable_sprites = self.particles_sprites = self.first_group = \
            self.last_group = None
        self.now_level = 'level_1'
        self.screen = screen
        self.clock = clock
        self.to_menu_func = to_menu_func
        self.statistic = statistic
        self.theme = theme
        # Учет уничтожаемых предметов
        self.enemy_log, self.breakable_log = {}, {}

        # Маркеры диалогов
        self.dialogue_markers = standard_dialogue_markers.copy()

        # Маркер появления босса на 3 лвл-е
        self.enemy_markers = standard_enemy_markers.copy()

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
        with open(f'{LEVELS_PATH}/{level_name}.csv') as level_file:
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

    def damage_player(self, enemy, amount, attack_type):
        """Функция для получения урона игроком"""
        if enemy != self.player.last_enemy:
            self.player.vulnerable = True
            self.player.last_enemy = enemy
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hit_time = pygame.time.get_ticks()
            # Создаём партиклы
            if self.player.health <= 0:
                self.ui.show_in_display(self.player)
                pygame.display.flip()
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
        if self.now_level in self.enemy_markers:
            if not self.enemy_markers[self.now_level]:
                self.check_spawn()

    def dialogs_check(self, dialogue_name):
        """Функция для проверки диалогов (Их вызов и отключение таймера))"""
        self.player.image.set_alpha(255)
        self.show()
        pygame.time.set_timer(pygame.event.Event(pygame.USEREVENT, dialogue=dialogue_name), 0)
        if not self.dialogue_markers[dialogue_name]:
            Dialogue(self.screen, self.clock, dialogue_name, self).run()
            self.dialogue_markers[dialogue_name] = True
        self.player.can_attack = False
        self.player.attack_time = pygame.time.get_ticks()

    def check_spawn(self):
        for obj in collide_areas[self.now_level]:
            if obj.rect.colliderect(self.player.rect) and obj.type == 'spawn_enemy':
                self.enemy_markers[self.now_level] = True
                Enemy(self.camera_group, self.attackable_sprites, monster_name='the_thief_lord',
                      x=100, y=100, id_numb=-1,
                      solid_sprites=self.solid_sprites, damage_player_func=self.damage_player,
                      enemy_log=self.enemy_log)
                self.show()
                pygame.time.set_timer(pygame.event.Event(pygame.USEREVENT, dialogue='spawn_enemies_3'), 10)

    def player_attack_logic(self):
        """Логика ударов игрока"""
        if self.player.attacking:
            rect = self.player.attacking_rect
            for target_spr in self.attackable_sprites:
                if rect.colliderect(target_spr.hitbox):
                    if isinstance(target_spr, Enemy):
                        target_spr.get_damage(self.player)
                        target_spr.check_death(self.player)
                        if not self.dialogue_markers['killed_all_2'] and self.now_level == 'level_2':
                            if not len([sprite for sprite in self.camera_group.sprites() if isinstance(sprite, Enemy)]):
                                pygame.time.set_timer(pygame.event.Event(pygame.USEREVENT, dialogue='killed_all_2'),
                                                      100)
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
                    if not self.dialogue_markers['teach_hit'] and obj.where == 'level_2':
                        pygame.time.set_timer(pygame.event.Event(pygame.USEREVENT, dialogue='teach_hit'), 10)
                elif obj.type == 'minigame':
                    if not len([sprite for sprite in self.camera_group.sprites() if isinstance(sprite, Enemy)]):
                        if Tag(self.screen, self.clock, tag_images_dict['1']['to_correct'],
                               tag_images_dict['1']['correct']).run():
                            self.change_level(obj.where, False, interact_time, obj.destination_x, obj.destination_y)
                        self.show()
                        Fade(self.screen).fade_out(FADE_SPEED_MENU)
                elif obj.type == 'heal':
                    if self.player.health < PLAYER_STAT_HP and self.player.money >= 200:
                        raz = min(100 - self.player.health, PLAYER_HEAL)
                        self.player.money -= 200
                        self.statistic.health_refilled += raz
                        self.player.health += raz
                elif obj.type == 'end_event':
                    if not len([sprite for sprite in self.camera_group.sprites() if isinstance(sprite, Enemy)]):
                        self.theme
                        if EndScreen(self.screen, self.clock, self.statistic).run():
                            self.to_menu_func()

    def start_new_game(self):
        """Старт новой игры"""
        self.enemy_log, self.breakable_log = {}, {}
        self.enemy_markers = standard_enemy_markers.copy()
        self.change_level()
