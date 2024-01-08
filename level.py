from config import *
import pygame
from player import Player
from sprite import *
from interactions import interaction_group
from cameras import *
from debug import debug
from ui import UI


class Level:
    def __init__(self):
        # Получить экран
        self.solid_sprites = self.passable_sprites = self.player_group = self.camera_group = self._player = None
        self._display_surface = pygame.display.get_surface()

        # Создаём уровень
        self.change_level()

        # Создаём UI пользователю
        self.ui = UI()

    def change_level(self, level='start'):
        self.solid_sprites = pygame.sprite.Group()
        self.passable_sprites = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle()
        self.camera_group = CameraGroup()
        if level == 'start':
            # Создание спрайтов карты
            SolidSprite(self.camera_group, self.solid_sprites, interaction_group, file_name='back_wall', x=0, y=-200,
                        tiling_x=800, tiling_y=200, partly_passable=True)
            SolidSprite(self.camera_group, self.solid_sprites, interaction_group, file_name='side_wall', x=-40, y=-200)
            SolidSprite(self.camera_group, self.solid_sprites, interaction_group, file_name='side_wall', x=800, y=-200)
            SolidSprite(self.camera_group, self.solid_sprites, interaction_group, file_name='down_wall', x=0, y=380)
            SolidSprite(self.camera_group, self.solid_sprites, interaction_group, file_name='inside_wall', x=180,
                        y=-200,
                        tiling_x=40, tiling_y=280, partly_passable=True)

            # Создание спрайтов окружения
            SolidSprite(self.camera_group, self.solid_sprites, interaction_group, file_name='oven', x=40, y=-60,
                        anim_state=1,
                        partly_passable=True)
            PassableSprite(self.passable_sprites, interaction_group, file_name='carpet', x=100, y=100)
            SolidSprite(self.camera_group, self.solid_sprites, interaction_group, file_name='wardrobe', x=720, y=-150,
                        tiling_x=60, tiling_y=200, anim_state=1, partly_passable=True)
            self._player = Player(self.camera_group, self.player_group, x=HALF_SCREEN_WIDTH - 200, y=HALF_SCREEN_HEIGHT - 200,
                                  solid_sprites=self.solid_sprites)
        # self.camera_group.center_target_camera(self._player)

    def show(self):
        self._player.update()
        self.camera_group.custom_draw(self.passable_sprites, player=self._player)
        self.ui.show_in_display(self._player)

    def zoom_cam(self, event_button):
        self.camera_group.zooming(event_button)
