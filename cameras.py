import pygame
from config import *
from load_image import load_image


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self._display_surface = pygame.display.get_surface()
        # Central first launch
        self._offset_central = pygame.math.Vector2()

        # camera offset
        self._offset = pygame.math.Vector2()
        # camera zoom
        self._zoom_scale = 0.8
        self._internal_surface_size = (2500, 2500)
        self._internal_surface = pygame.Surface(self._internal_surface_size, pygame.SRCALPHA)
        self._internal_rect = self._internal_surface.get_rect(center=(HALF_SCREEN_WIDTH, HALF_SCREEN_HEIGHT))
        self._internal_surface_size_vector = pygame.math.Vector2(self._internal_surface_size)
        self._internal_offset = pygame.math.Vector2()
        self._internal_offset.x = self._internal_surface_size[0] // 2 - HALF_SCREEN_WIDTH
        self._internal_offset.y = self._internal_surface_size[1] // 2 - HALF_SCREEN_HEIGHT

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

    def zooming(self, mouse):
        if self._zoom_keyboard_control(mouse):
            self._box_rect_resize()

    def _box_rect_resize(self):
        left = self._camera_borders['left']
        top = self._camera_borders['top']
        w = SCREEN_WIDTH - left - self._camera_borders['right']
        h = SCREEN_HEIGHT - top - self._camera_borders['bottom']
        self._camera_rect = pygame.Rect(left, top, w, h)

    def _zoom_keyboard_control(self, mouse):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z] and mouse == 4:
            self._zoom_scale = min(0.8, self._zoom_scale + 0.1)
            self._camera_borders['left'] = min(self._camera_borders['left'] + BOX_LEFT_ZOOM, BOX_LEFT)
            self._camera_borders['top'] = min(self._camera_borders['top'] + BOX_TOP_ZOOM, BOX_TOP)
            self._camera_borders['right'] = min(self._camera_borders['right'] + BOX_RIGHT_ZOOM, BOX_RIGHT)
            self._camera_borders['bottom'] = min(self._camera_borders['bottom'] + BOX_BOTTOM_ZOOM, BOX_BOTTOM)
            return True
        if keys[pygame.K_z] and mouse == 5:
            self._zoom_scale = max(0.5, self._zoom_scale - 0.1)
            self._camera_borders['left'] = max(self._camera_borders['left'] - BOX_LEFT_ZOOM, BOX_LEFT_MIN)
            self._camera_borders['top'] = max(self._camera_borders['top'] - BOX_TOP_ZOOM, BOX_TOP_MIN)
            self._camera_borders['right'] = max(self._camera_borders['right'] - BOX_RIGHT_ZOOM, BOX_RIGHT_MIN)
            self._camera_borders['bottom'] = max(self._camera_borders['bottom'] - BOX_BOTTOM_ZOOM, BOX_BOTTOM_MIN)
            return True
        return False

    def custom_draw(self, *groups, player):
        # Меняем координаты всем объектам
        self.box_target_camera(player)

        # Делаем зум
        self._internal_surface.fill(SKYBLUE)

        # Рисуем фон
        # ground_offset = self._ground_rect - self._offset + self._internal_offset + self._offset_central
        # self._internal_surface.blit(self._ground_surf, ground_offset)
        # Обрабатываем объекты
        for sprite in [sprite for group in groups for sprite in group.sprites()] + sorted(self.sprites(), key=lambda
                sprite: sprite.rect.centery):
            if sprite != player:
                offset_pos = sprite.rect.topleft - self._offset + self._internal_offset + self._offset_central
            else:
                offset_pos = sprite.rect.topleft - self._offset + self._internal_offset
            self._internal_surface.blit(sprite.image, offset_pos)
        scaled_surf = pygame.transform.scale(self._internal_surface,
                                             self._internal_surface_size_vector * self._zoom_scale)
        scaled_rect = scaled_surf.get_rect(center=(HALF_SCREEN_WIDTH, HALF_SCREEN_HEIGHT))
        self._display_surface.blit(scaled_surf, scaled_rect)
