import pygame
from pyth_files.config import *

"""Тень при переходе"""


class Fade:
    def __init__(self, screen):
        self.screen = screen
        self.alpha_surf = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA, 32)
        self.now_alpha = 0
        self.alpha_surf.fill((0, 0, 0))
        self.alpha_surf.set_alpha(self.now_alpha)

    def draw(self):
        self.screen.blit(self.alpha_surf, (0, 0))
        pygame.display.update()

    def fade_in(self, speed=FADE_SPEED_LEVELS):
        """Закрашиваем экран чёрным"""
        last_screen = self.screen.copy()
        for alpha in range(0, 255, speed):
            self.now_alpha = alpha
            self.alpha_surf.set_alpha(self.now_alpha)
            pygame.time.delay(20)
            self.screen.blit(last_screen, (0, 0))
            self.draw()

    def fade_out(self, speed=FADE_SPEED_LEVELS):
        """Убираем с экрана чёрный 'занавес'"""
        last_screen = self.screen.copy()
        for alpha in range(0, 255, speed):
            self.now_alpha = 255 - alpha
            self.alpha_surf.set_alpha(self.now_alpha)
            pygame.time.delay(20)
            self.screen.blit(last_screen, (0, 0))
            self.draw()
