import sys
import pygame
from pyth_files.config import *
from pyth_files.sound import SoundEffect
from pyth_files.buttons import Button, Slider
from pyth_files.sprite import *
from pyth_files.fade import Fade

"""Классы разных меню-окон"""

pygame.init()


class Menu:
    def __init__(self, screen, clock, theme):
        self.x = 0
        self.screen = screen
        self.clock = clock
        self.theme = theme
        self.running = True
        self.background = pygame.transform.scale(load_image(TEXTURES_PATH, MENU_BACKGROUND, color_key=None),
                                                 (1536, 864))
        self.buttons_group = pygame.sprite.Group()

    def run(self):
        Fade(self.screen).fade_in(FADE_SPEED_MENU)
        self._create_buttons()
        self.operations()
        Fade(self.screen).fade_out(FADE_SPEED_MENU)
        self.running = True
        while self.running:
            self.operations()
            pygame.display.flip()
            self.clock.tick(MENU_FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                    self._mouse_operations(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if len(self.buttons_group) != 3:
                            self.running = False

    def operations(self):
        """Рисуем и обрабатываем все действия пользователя"""
        self._draw_background()
        self._mouse_operations()
        self._draw_buttons()
        self.draw_text()

    def _draw_background(self):
        self.screen.blit(self.background, MENU_BACKGROUND_POS)

    def _draw_buttons(self):
        for button in self.buttons_group:
            button.draw(self.screen)

    def _create_buttons(self):
        pass

    def _mouse_operations(self, event=pygame.event.Event):
        pass

    def draw_text(self):
        pass


class MainMenu(Menu):
    """Класс главного меню"""

    def __init__(self, screen, clock, theme):
        super().__init__(screen, clock, theme)
        self.play_theme()

    def play_theme(self):
        self.theme.play_music()

    def _mouse_operations(self, event=pygame.event.Event):
        mouse_pos = pygame.mouse.get_pos()
        self._btn_exit_check(mouse_pos, event)
        self._btn_start_check(mouse_pos, event)
        self._btn_settings_check(mouse_pos, event)

    def _create_buttons(self):
        self.btn_exit = Button(self.buttons_group, MENU_BTN_EXIT_POS, MENU_EXIT_NAME,
                               textures_buttons_dict['menu']['normal'][0],
                               textures_buttons_dict['menu']['hovered'][0], textures_buttons_dict['menu']['clicked'][0])
        self.btn_start = Button(self.buttons_group, MENU_BTN_START_POS, MENU_START_NAME,
                                textures_buttons_dict['menu']['normal'][0],
                                textures_buttons_dict['menu']['hovered'][0],
                                textures_buttons_dict['menu']['clicked'][0])
        self.btn_setting = Button(self.buttons_group, MENU_BTN_SETTINGS_POS, MENU_SETTING_NAME,
                                  textures_buttons_dict['menu']['normal'][0],
                                  textures_buttons_dict['menu']['hovered'][0],
                                  textures_buttons_dict['menu']['clicked'][0])

    def _btn_exit_check(self, mouse_pos, event):
        if self.btn_exit.check_event(mouse_pos, event):
            pygame.quit()
            sys.exit()

    def _btn_start_check(self, mouse_pos, event):
        if self.btn_start.check_event(mouse_pos, event):
            self.running = False

    def _btn_settings_check(self, mouse_pos, event):
        if self.btn_setting.check_event(mouse_pos, event):
            Settings(self.screen, self.clock, self.theme).run()
            self.operations()
            Fade(self.screen).fade_out(FADE_SPEED_MENU)

    def set_music_volume(self, volume):
        self.theme.change_music_volume(volume)


class Settings(Menu):
    """Класс настроек"""

    def __init__(self, screen, clock, theme):
        super().__init__(screen, clock, theme)

    def _mouse_operations(self, event=pygame.event.Event):
        mouse_pos = pygame.mouse.get_pos()
        self._btn_exit_check(mouse_pos, event)
        self._slider_effects_check(mouse_pos, event)
        self._slider_music_check(mouse_pos, event)

    def _create_buttons(self):
        """Создаём кнопки и слайдеры"""
        self.btn_exit = Button(self.buttons_group, SETTINGS_BACK_TO_MENU_POS, SETTINGS_BACK_TO_MENU_NAME,
                               textures_buttons_dict['menu']['normal'][0],
                               textures_buttons_dict['menu']['hovered'][0], textures_buttons_dict['menu']['clicked'][0])
        self.slider_effects = Slider(self.buttons_group, SETTINGS_MUSIC_EFFECTS_POS, SETTINGS_MUSIC_EFFECTS_SIZE,
                                     SoundEffect.return_volume() / MAX_EFFECT_VOLUME, 0,
                                     MAX_EFFECT_VOLUME)
        self.slider_music = Slider(self.buttons_group, SETTINGS_MUSIC_MUSIC_POS, SETTINGS_MUSIC_MUSIC_SIZE,
                                   self.theme.return_volume() / MAX_MUSIC_VOLUME, 0,
                                   MAX_MUSIC_VOLUME)

    def draw_text(self):
        """Рисуем текст около слайдеров"""
        up_offset = pygame.Vector2(0, -50)
        right_offset = pygame.Vector2(50, 0)

        font = pygame.font.Font(MENU_FONT, MENU_FONT_SIZE)
        text_surface = font.render(SETTINGS_MUSIC_EFFECTS_NAME, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.slider_effects.container_rect.center + up_offset)
        self.screen.blit(text_surface, text_rect)

        text_surface = font.render(SETTINGS_MUSIC_MUSIC_NAME, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.slider_music.container_rect.center + up_offset)
        self.screen.blit(text_surface, text_rect)

        text_surface = font.render(f'{round(SoundEffect.return_volume() / MAX_EFFECT_VOLUME * 100)} %', True,
                                   (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.slider_effects.container_rect.midright + right_offset)
        self.screen.blit(text_surface, text_rect)

        text_surface = font.render(f'{round(self.theme.return_volume() / MAX_MUSIC_VOLUME * 100)} %', True,
                                   (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.slider_music.container_rect.midright + right_offset)
        self.screen.blit(text_surface, text_rect)

    def _btn_exit_check(self, mouse_pos, event):
        if self.btn_exit.check_event(mouse_pos, event):
            Fade(self.screen).fade_in(FADE_SPEED_MENU)
            self.running = False

    def _slider_effects_check(self, mouse_pos, event):
        value = self.slider_effects.check_event(mouse_pos, event)
        if value:
            SoundEffect.change_effects_volume(value)

    def _slider_music_check(self, mouse_pos, event):
        value = self.slider_music.check_event(mouse_pos, event)
        if value:
            self.theme.change_music_volume(value)
