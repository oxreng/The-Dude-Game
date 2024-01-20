import sys

import numpy as np
import pygame
from config import *
from random import sample


class Trick(pygame.sprite.Sprite):
    def __init__(self, group, pos, image):
        super().__init__(group)
        self.image = pygame.transform.scale(image, (TAG_TRICK_SIZE, TAG_TRICK_SIZE))
        self.rect = self.image.get_rect(topleft=pos)

    def draw(self, screen, free_pos):
        pygame.draw.rect(screen, BLACK, self.rect)
        if self.rect.topleft != free_pos:
            screen.blit(self.image, self.rect.topleft)
        pygame.draw.rect(screen, WHITE, self.rect, 1)


class Tag:
    def __init__(self, screen, clock, images):
        self.screen = screen
        self.clock = clock
        self.images = images
        self.running = True
        self.tricks_list = np.array([None for _ in range(TAG_TRICK_QUANTITY)]).reshape(int(TAG_TRICK_QUANTITY ** 0.5),
                                                                                       int(TAG_TRICK_QUANTITY ** 0.5))
        self.free_pos = (TAG_TRICK_MAX_X, TAG_TRICK_MAX_Y)
        self.tricks_group = pygame.sprite.Group()
        self.alpha_screen = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA, 32)
        self.alpha_screen.fill((0, 0, 0, 100))

    def run(self):
        self._create_tricks()
        pygame.mouse.set_visible(True)
        self.screen.blit(self.alpha_screen, (0, 0))
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self._mouse_operations(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
            self.operations()
            pygame.display.flip()
            self.clock.tick(MENU_FPS)

    def operations(self):
        self._mouse_operations()
        self._draw_tricks()

    def _draw_tricks(self):
        for trick in self.tricks_group:
            trick.draw(self.screen, self.free_pos)

    def _create_tricks(self):
        for y in range(int(TAG_TRICK_QUANTITY ** 0.5)):
            for x in range(int(TAG_TRICK_QUANTITY ** 0.5)):
                x_pos, y_pos = TAG_FIRST_X_POS + x * TAG_TRICK_MOVE, TAG_FIRST_Y_POS + y * TAG_TRICK_MOVE
                self.tricks_list[y][x] = Trick(self.tricks_group, (x_pos, y_pos), self.images[y * 2 + x])

    def check_pos(self, trick, y, x):
        for smt_trick, index in ([(self.tricks_list[y - 1, x], (y - 1, x))] if y > 0 else []) + \
                                ([(self.tricks_list[y + 1, x], (y + 1, x))] if y < self.tricks_list.shape[
                                    0] - 1 else []) + \
                                ([(self.tricks_list[y, x - 1], (y, x - 1))] if x > 0 else []) + \
                                ([(self.tricks_list[y, x + 1], (y, x + 1))] if x < self.tricks_list.shape[
                                    1] - 1 else []):
            if smt_trick.rect.topleft == self.free_pos:
                self.free_pos = trick.rect.topleft
                self.tricks_list[y, x], self.tricks_list[index] = self.tricks_list[index], self.tricks_list[y, x]
                smt_trick.rect, trick.rect = trick.rect.copy(), smt_trick.rect.copy()
                break

    def _mouse_operations(self, event=pygame.event.Event):
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for row, lst in enumerate(self.tricks_list):
                for col, trick in enumerate(lst):
                    if trick.rect.collidepoint(mouse_pos):
                        self.check_pos(trick, row, col)
                        break
