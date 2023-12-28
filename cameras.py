import pygame
from config import *
from load_image import load_image


class CameraGroup_ysort(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self._display_surface = pygame.display.get_surface()
        # Для фона
        # self._ground_surf = load_image(..., ...)
        # self._ground_rect = self._ground_surf.get_rect(topleft=(0, 0))

    def custom_draw(self):
        # Рисуем фон
        # self._display_surface.blit(self._ground_surf, self._ground_rect)

        # Обрабатываем объекты
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            self._display_surface.blit(sprite.image, sprite.rect)


class CameraGroup_center_player(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self._display_surface = pygame.display.get_surface()

        # camera offset
        self.offset = pygame.math.Vector2()

        # Для фона
        # self._ground_surf = load_image(..., ...)
        # self._ground_rect = self._ground_surf.get_rect(topleft=(0, 0))

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - HALF_SCREEN_WIDTH
        self.offset.y = target.rect.centery - HALF_SCREEN_HEIGHT

    def custom_draw(self, *groups, player):
        self.center_target_camera(player)
        # Рисуем фон
        # groind_offset = self._ground_rect - self.offset
        # self._display_surface.blit(self._ground_surf, groind_offset)

        # Обрабатываем объекты
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self._display_surface.blit(sprite.image, offset_pos)


class CameraGroup_box_camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self._display_surface = pygame.display.get_surface()

        # camera offset
        self._offset = pygame.math.Vector2()

        # box setup
        self._camera_borders = {'left': BOX_LEFT, 'right': BOX_RIGHT, 'top': BOX_TOP, 'bottom': BOX_BOTTOM}
        left = self._camera_borders['left']
        top = self._camera_borders['top']
        w = SCREEN_WIDTH - left - self._camera_borders['right']
        h = SCREEN_HEIGHT - top - self._camera_borders['bottom']
        self._camera_rect = pygame.Rect(left, top, w, h)

        # Для фона
        # self._ground_surf = load_image(..., ...)
        # self._ground_rect = self._ground_surf.get_rect(topleft=(0, 0))

    def center_target_camera(self, target):
        self._offset.x = target.rect.centerx - HALF_SCREEN_WIDTH
        self._offset.y = target.rect.centery - HALF_SCREEN_HEIGHT

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

    def custom_draw(self, *groups, player):
        # self.center_target_camera(player)
        self.box_target_camera(player)
        # Рисуем фон
        # ground_offset = self._ground_rect - self._offset
        # self._display_surface.blit(self._ground_surf, ground_offset)

        # Обрабатываем объекты
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self._offset
            self._display_surface.blit(sprite.image, offset_pos)
