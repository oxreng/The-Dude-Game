import pygame
from pyth_files.config import *
from pyth_files.interactions import collide_areas
from pyth_files.enemy import Enemy
from pyth_files.particles import ParticleEffect
from random import choice
from pyth_files.sprite import player_particles_dict

"""Файл камеры, в котором мы работаем со всеми объектами"""


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self._screen = pygame.display.get_surface()
        # Central first launch
        self._offset_central = pygame.math.Vector2()

        # camera offset
        self._offset = pygame.math.Vector2()

        # box setup
        self._camera_borders = {'left': BOX_LEFT, 'right': BOX_RIGHT, 'top': BOX_TOP, 'bottom': BOX_BOTTOM}
        left = self._camera_borders['left']
        top = self._camera_borders['top']
        w = SCREEN_WIDTH - left - self._camera_borders['right']
        h = SCREEN_HEIGHT - top - self._camera_borders['bottom']
        self._camera_rect = pygame.Rect(left, top, w, h)

    def _box_target_camera(self, target):
        """Бокс-камера для игрока"""
        if target.rect.left < self._camera_rect.left:
            self._camera_rect.left = target.rect.left
        if target.rect.right > self._camera_rect.right:
            self._camera_rect.right = target.rect.right
        if target.rect.top < self._camera_rect.top:
            self._camera_rect.top = target.rect.top
        if target.rect.bottom > self._camera_rect.bottom:
            self._camera_rect.bottom = target.rect.bottom
        self._offset.x = self._camera_rect.left - self._camera_borders['left']
        self._offset.y = self._camera_rect.top - self._camera_borders['top']

    def _enemy_update(self, player):
        """Обновляем всех врагов (двигаем, бьём и тд)"""
        for enemy in [sprite for sprite in self.sprites() if isinstance(sprite, Enemy)]:
            enemy.enemy_update(player)

    def custom_draw(self, first_group, last_group, player, now_level):
        """Рисуем подсказки, все объекты"""
        self._box_target_camera(player)
        self._enemy_update(player)

        self._screen.fill(BLACK)

        # Обрабатываем объекты
        for sprite in [sprite for sprite in first_group.sprites()] + \
                sorted(self.sprites(), key=lambda sprite: sprite.rect.centery) + \
                      [sprite for sprite in last_group.sprites()]:
            if sprite != player:
                offset_pos = sprite.rect.topleft - self._offset + self._offset_central
            else:
                offset_pos = sprite.rect.topleft - self._offset
            self._screen.blit(sprite.image, offset_pos)

        # Отрисовка pop-up подсказок
        for obj in collide_areas[now_level]:
            if obj.rect.colliderect(player.rect):
                font = pygame.font.Font('data/fonts/font.ttf', 25)
                text = font.render(hint_text[obj.name], True, WHITE)
                text_pos_x = (obj.rect.topleft - self._offset + self._offset_central)[0] - (
                        text.get_width() - obj.rect.width) / 2
                text_pos_y = (obj.rect.topleft - self._offset + self._offset_central)[1] - text.get_size()[1] - 10
                self._screen.blit(text, (text_pos_x, text_pos_y))

    @staticmethod
    def particles_create(*groups, particle_name, pos):
        """Создание партиклов"""
        animations = choice(player_particles_dict[particle_name])
        ParticleEffect(*groups, pos=pos, animations=animations)
