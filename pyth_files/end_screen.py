import datetime
import sys
import pygame
from pyth_files.config import *
from pyth_files.buttons import Button
from pyth_files.sprite import *
from pyth_files.sound import SpritesSound

"""Окно, которое будет появляться, когда закончится игра"""


class EndScreenFade:
    def __init__(self, screen):
        self.screen = screen
        self.alpha_surf = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA, 32)
        self.now_alpha = 0
        self.alpha_surf.fill((255, 255, 255))
        self.alpha_surf.set_alpha(self.now_alpha)

    def draw(self):
        self.screen.blit(self.alpha_surf, (0, 0))
        pygame.display.update()

    def fade_in(self):
        """Закрашиваем экран белым"""
        last_screen = self.screen.copy()
        for alpha in range(0, 255, END_SCREEN_FADE_SPEED):
            self.now_alpha = alpha
            self.alpha_surf.set_alpha(self.now_alpha)
            pygame.time.delay(20)
            self.screen.blit(last_screen, (0, 0))
            self.draw()


class EndScreen:
    def __init__(self, screen, clock, statistics, theme):
        self.screen = screen
        self.clock = clock
        self.statistics = statistics
        self.theme = theme
        self.running = True
        self.buttons_group = pygame.sprite.Group()
        self.alpha_screen = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA, 32)
        self.alpha_screen.fill((0, 0, 0, 100))

    def run(self):
        SpritesSound.boom_sound()
        EndScreenFade(self.screen).fade_in()
        self._create_buttons()
        pygame.mouse.set_visible(True)
        self.theme.path = END_SCREEN_THEME
        self.theme.init_track()
        self.theme.play_music()
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
                        return True
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
        self.btn_back_to_menu = Button(self.buttons_group, END_SCREEN_TO_MENU_POS, END_SCREEN_TO_MENU_NAME,
                                       textures_buttons_dict['menu']['normal'][0],
                                       textures_buttons_dict['menu']['hovered'][0],
                                       textures_buttons_dict['menu']['clicked'][0])

    def _mouse_operations(self, event=pygame.event.Event):
        mouse_pos = pygame.mouse.get_pos()
        return self._back_to_menu_check(mouse_pos, event)

    def _draw_text(self):
        """Выводим статистику"""
        font = pygame.font.Font(MENU_FONT, END_SCREEN_FONT_SIZE)
        text_surface = font.render(END_SCREEN_END_NAME, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(HALF_SCREEN_WIDTH, 200))
        self.screen.blit(text_surface, text_rect)

        text_surface = font.render(END_SCREEN_STATS_NAME, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(HALF_SCREEN_WIDTH, 250))
        self.screen.blit(text_surface, text_rect)

        time = round((datetime.datetime.now() - self.statistics.launch_time).total_seconds())
        text_surface = font.render(f'{END_SCREEN_PASSING_TIME_NAME}: {time} C', True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(HALF_SCREEN_WIDTH, 300))
        self.screen.blit(text_surface, text_rect)

        text_surface = font.render(f'{END_SCREEN_HEALED_HP_NAME}: {self.statistics.health_refilled}', True,
                                   (255, 255, 255))
        text_rect = text_surface.get_rect(center=(HALF_SCREEN_WIDTH, 350))
        self.screen.blit(text_surface, text_rect)

    def _back_to_menu_check(self, mouse_pos, event):
        if self.btn_back_to_menu.check_event(mouse_pos, event):
            return True
