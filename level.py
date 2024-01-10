from config import *
import pygame
from player import Player
from sprite import *
from interactions import interaction_group
from cameras import *
from debug import debug
from ui import UI
from enemy import Enemy
import csv


class Level:
    def __init__(self):
        # Получить экран
        self.solid_sprites = self.passable_sprites = self.player_group = self.camera_group = self._player = None
        self._display_surface = pygame.display.get_surface()

        # Создаём уровень
        self.change_level()

        # Создаём UI пользователю
        self.ui = UI()

    def change_level(self, level_name='level_1'):
        self.solid_sprites = pygame.sprite.Group()
        self.passable_sprites = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle()
        self.camera_group = CameraGroup()
        with open(f'{TEXTURES_PATH}/level_csv/{level_name}.csv') as level_file:
            reader = csv.DictReader(level_file, delimiter=';', quotechar='"')
            for item in reader:
                print(item)
                if item['type'] == 'passable':
                    PassableSprite(self.passable_sprites, interaction_group,
                                   file_name=item['name'], x=int(item['x']), y=int(item['y']))
                else:
                    SolidSprite(self.solid_sprites, self.camera_group, interaction_group,
                                file_name=item['name'], x=int(item['x']), y=int(item['y']),
                                tiling_x=int(item['tiling_x']), tiling_y=int(item['tiling_y']),
                                partly_passable=(False if item['partly_passable'] == '0' else True))

        Enemy(self.camera_group, monster_name='normal', x=300, y=300,
              solid_sprites=self.solid_sprites)
        self._player = Player(self.camera_group, self.player_group, x=HALF_SCREEN_WIDTH - 200,
                              y=HALF_SCREEN_HEIGHT - 200,
                              solid_sprites=self.solid_sprites)
        # self.camera_group.center_target_camera(self._player)

    def show(self):
        self._player.update()
        self.passable_sprites.update()
        self.camera_group.custom_draw(self.passable_sprites, player=self._player)
        self.ui.show_in_display(self._player)

    def zoom_cam(self, event_button):
        self.camera_group.zooming(event_button)
