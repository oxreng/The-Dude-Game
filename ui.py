import pygame
from config import *


class UI:
    def __init__(self):
        self._display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # Настройка плашки
        self.health_bar_rect = pygame.Rect(*UI_HEALTH_BAR_COORDS, UI_HEALTH_BAR_WIDTH, UI_BAR_HEIGHT)

    def show_bar(self, current, max_amount, bg_rect, color):
        # Рисуем фон
        pygame.draw.rect(self._display_surface, UI_BG_COLOR, bg_rect)

        # Изменяем статы на пиксели для полоски
        ratio = current / max_amount
        current_rect = bg_rect.copy()
        current_rect.width = bg_rect.width * ratio

        # Рисуем саму полоску
        pygame.draw.rect(self._display_surface, color, current_rect)
        pygame.draw.rect(self._display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def show_money(self, money):
        text_surf = self.font.render(str(round(money)), False, UI_TEXT_COLOR)
        x = SCREEN_WIDTH - 20
        y = SCREEN_HEIGHT - 20
        text_rect = text_surf.get_rect(bottomright=(x, y))

        pygame.draw.rect(self._display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        self._display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self._display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)

    def show_in_display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, UI_HEALTH_COLOR)

        self.show_money(player.money)
