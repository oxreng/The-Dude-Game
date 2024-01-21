import sys
import pygame
from pyth_files.config import *
from pyth_files.buttons import Button
from pyth_files.sprite import *

"""Окно, которое будет при смерти игрока"""


class DeathWindow:
    def __init__(self, screen, clock, restart_func):
        self.screen = screen
        self.clock = clock
        self.restart_func = restart_func
        self.running = True
        self.buttons_group = pygame.sprite.Group()
        self.alpha_screen = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA, 32)
        self.alpha_screen.fill((0, 0, 0, 100))

    def run(self):
        self._create_buttons()
        pygame.mouse.set_visible(True)
        self.screen.blit(self.alpha_screen, (0, 0))
        self.running = True
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
                        self.restart_func()
            self._operations()
            pygame.display.flip()
            self.clock.tick(MENU_FPS)

    def _operations(self):
        """Обновляем анимации кнопок и рисуем сами кнопки"""
        self._mouse_operations()
        self._draw_buttons()

    def _draw_buttons(self):
        for button in self.buttons_group:
            button.draw(self.screen)

    def _create_buttons(self):
        self.btn_back_to_menu = Button(self.buttons_group, DEATH_BACK_TO_MENU_POS, DEATH_BACK_TO_MENU_NAME,
                                       textures_buttons_dict['menu']['normal'][0],
                                       textures_buttons_dict['menu']['hovered'][0],
                                       textures_buttons_dict['menu']['clicked'][0])
        self.btn_restart = Button(self.buttons_group, DEATH_RESTART_POS, DEATH_RESTART_NAME,
                                  textures_buttons_dict['menu']['normal'][0],
                                  textures_buttons_dict['menu']['hovered'][0],
                                  textures_buttons_dict['menu']['clicked'][0])

    def _mouse_operations(self, event=pygame.event.Event):
        mouse_pos = pygame.mouse.get_pos()
        self._btn_restart_check(mouse_pos, event)
        return self._back_to_menu_check(mouse_pos, event)

    def _back_to_menu_check(self, mouse_pos, event):
        if self.btn_back_to_menu.check_event(mouse_pos, event):
            return True

    def _btn_restart_check(self, mouse_pos, event):
        if self.btn_restart.check_event(mouse_pos, event):
            self.running = False
            self.restart_func()
