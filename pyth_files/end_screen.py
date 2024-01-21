import datetime
import sys
import pygame
from pyth_files.config import *
from pyth_files.buttons import Button
from pyth_files.sprite import *

"""Окно, которое будет появляться, когда закончится игра"""


class EndScreen:
    def __init__(self, screen, clock, statistics):
        self.screen = screen
        self.clock = clock
        self.statistics = statistics
        self.running = True
        self.buttons_group = pygame.sprite.Group()
        self.alpha_screen = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA, 32)
        self.alpha_screen.fill((0, 0, 0, 100))

    def run(self):
        self._create_buttons()
        pygame.mouse.set_visible(True)
        self.screen.blit(self.alpha_screen, (0, 0))
        self.running = True
        self._draw_text()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                    if self._mouse_operations(event):
                        return True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
            self.operations()
            pygame.display.flip()
            self.clock.tick(MENU_FPS)

    def operations(self):
        """Обновляем анимации кнопок и рисуем сами кнопки"""
        self._mouse_operations()
        self._draw_buttons()

    def _draw_buttons(self):
        for button in self.buttons_group:
            button.draw(self.screen)

    def _create_buttons(self):
        self.btn_back_to_menu = Button(self.buttons_group, PAUSE_BTN_BACK_TO_MENU_POS, PAUSE_BACK_TO_MENU_NAME,
                                       textures_buttons_dict['menu']['normal'][0],
                                       textures_buttons_dict['menu']['hovered'][0],
                                       textures_buttons_dict['menu']['clicked'][0])

    def _mouse_operations(self, event=pygame.event.Event):
        mouse_pos = pygame.mouse.get_pos()
        return self._back_to_menu_check(mouse_pos, event)

    def _draw_text(self):
        """Выводим статистику"""
        font = pygame.font.Font(MENU_FONT, MENU_FONT_SIZE)
        text_surface = font.render('END', True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(HALF_SCREEN_WIDTH, 200))
        self.screen.blit(text_surface, text_rect)

        font = pygame.font.Font(MENU_FONT, MENU_FONT_SIZE)
        text_surface = font.render('STATS', True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(HALF_SCREEN_WIDTH, 250))
        self.screen.blit(text_surface, text_rect)

        time = round((datetime.datetime.now() - self.statistics.launch_time).total_seconds())
        font = pygame.font.Font(MENU_FONT, MENU_FONT_SIZE)
        text_surface = font.render(f'TIME: {time} S', True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(HALF_SCREEN_WIDTH, 300))
        self.screen.blit(text_surface, text_rect)

        font = pygame.font.Font(MENU_FONT, MENU_FONT_SIZE)
        text_surface = font.render(f'HEALED HP: {self.statistics.health_refilled}', True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(HALF_SCREEN_WIDTH, 350))
        self.screen.blit(text_surface, text_rect)

    def _back_to_menu_check(self, mouse_pos, event):
        if self.btn_back_to_menu.check_event(mouse_pos, event):
            return True
