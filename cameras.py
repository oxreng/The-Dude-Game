import pygame
from config import *
from load_image import load_image
from interactions import collide_areas
from enemy import Enemy
from particles import ParticleEffect
from random import choice
from sprite import player_particles_dict


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self._display_surface = pygame.display.get_surface()
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

    def center_target_camera(self, target):
        self._offset_central.x = target.rect.centerx - HALF_SCREEN_WIDTH
        self._offset_central.y = target.rect.centery - HALF_SCREEN_HEIGHT

    def box_target_camera(self, target):
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

    def enemy_update(self, player):
        for enemy in [sprite for sprite in self.sprites() if isinstance(sprite, Enemy)]:
            enemy.enemy_update(player)

    def custom_draw(self, first_group, last_group, player, now_level):
        # Меняем координаты всем объектам
        self.box_target_camera(player)
        self.enemy_update(player)

        # Делаем зум
        self._display_surface.fill(BLACK)

        # Обрабатываем объекты
        for sprite in [sprite for sprite in first_group.sprites()] + sorted(self.sprites(), key=lambda
                sprite: sprite.rect.centery) + [sprite for sprite in last_group.sprites()]:
            if sprite != player:
                offset_pos = sprite.rect.topleft - self._offset + self._offset_central
            else:
                offset_pos = sprite.rect.topleft - self._offset
            self._display_surface.blit(sprite.image, offset_pos)

        # Отрисовка pop-up подсказок
        for obj in collide_areas[now_level]:
            if obj.rect.colliderect(player.rect):
                font = pygame.font.Font('fonts/font.ttf', 25)
                text = font.render(hint_text[obj.name], True, WHITE)
                text_pos_x = (obj.rect.topleft - self._offset + self._offset_central)[0] - (
                        text.get_width() - obj.rect.width) / 2
                text_pos_y = (obj.rect.topleft - self._offset + self._offset_central)[1] - \
                             text.get_size()[1] - 10
                self._display_surface.blit(text, (text_pos_x, text_pos_y))

    @staticmethod
    def particles_create(*groups, particle_name, pos):
        animations = choice(player_particles_dict[particle_name])
        ParticleEffect(*groups, pos=pos, animations=animations)
