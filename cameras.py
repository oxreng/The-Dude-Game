import pygame
from config import *
from load_image import load_image


class CameraGroup(pygame.sprite.Group):
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

        # camera zoom
        self._zoom_scale = 0.8
        self._internal_surface_size = (2500, 2500)
        self._internal_surface = pygame.Surface(self._internal_surface_size, pygame.SRCALPHA)
        self._internal_rect = self._internal_surface.get_rect(center=(HALF_SCREEN_WIDTH, HALF_SCREEN_HEIGHT))
        self._internal_surface_size_vector = pygame.math.Vector2(self._internal_surface_size)
        self._internal_offset = pygame.math.Vector2()
        self._internal_offset.x = self._internal_surface_size[0] // 2 - HALF_SCREEN_WIDTH
        self._internal_offset.y = self._internal_surface_size[1] // 2 - HALF_SCREEN_HEIGHT

        # Для фона
        self._ground_surf = pygame.transform.scale(load_image(TEXTURES_PATH, 'map_tiles/floor.png', color_key=None), (800, 400))
        self._ground_rect = self._ground_surf.get_rect(topleft=(0, 0))

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

    def zoom_keyboard_control(self, mouse):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z] and mouse == 4:
            self._zoom_scale = min(0.8, self._zoom_scale + 0.1)
        if keys[pygame.K_z] and mouse == 5:
            self._zoom_scale = max(0.5, self._zoom_scale - 0.1)

    def custom_draw(self, *groups, player):
        # Меняем координаты всем объектам
        self.box_target_camera(player)

        # Делаем зум
        self._internal_surface.fill(BLACK)

        # Рисуем фон
        ground_offset = self._ground_rect.topleft - self._offset + self._internal_offset
        self._internal_surface.blit(self._ground_surf, ground_offset)

        # Обрабатываем объекты
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self._offset + self._internal_offset
            self._internal_surface.blit(sprite.image, offset_pos)

        scaled_surf = pygame.transform.scale(self._internal_surface,
                                             self._internal_surface_size_vector * self._zoom_scale)
        scaled_rect = scaled_surf.get_rect(center=(HALF_SCREEN_WIDTH, HALF_SCREEN_HEIGHT))
        self._display_surface.blit(scaled_surf, scaled_rect)
