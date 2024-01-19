import pygame
from config import *


class Fade:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.alpha_surf = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA, 32)
        self.now_alpha = 0
        self.alpha_surf.fill((0, 0, 0))
        self.alpha_surf.set_alpha(self.now_alpha)

    def draw(self):
        self.screen.blit(self.alpha_surf, (0, 0))
        pygame.display.update()

    def fade_in(self, last_screen):
        for alpha in range(0, 255, FADE_SPEED):
            self.now_alpha = alpha
            self.alpha_surf.set_alpha(self.now_alpha)
            pygame.time.delay(20)
            self.screen.blit(last_screen, (0, 0))
            self.draw()

    def fade_out(self, last_screen):
        for alpha in range(0, 255, FADE_SPEED):
            self.now_alpha = 255 - alpha
            self.alpha_surf.set_alpha(self.now_alpha)
            pygame.time.delay(20)
            self.screen.blit(last_screen, (0, 0))
            self.draw()
