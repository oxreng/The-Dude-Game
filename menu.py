import sys
import pygame
from config import *
from sound import MenuMusic, SoundEffect
from load_image import load_image
from buttons import Button, Slider
from sprite import *

pygame.init()
background = load_image(TEXTURES_PATH, MENU_BACKGROUND, color_key=None)
button_font = pygame.font.Font(MENU_FONT, BUTTON_FONT_SIZE)
logo_font = pygame.font.Font(MENU_FONT, LOGO_FONT_SIZE)


class Menu:
    def __init__(self, screen, clock):
        self.x = 0
        self.screen = screen
        self.clock = clock
        self.running = True
        self.buttons_group = pygame.sprite.Group()

    def run(self):
        self._create_buttons()
        pygame.mouse.set_visible(True)
        self.running = True
        while self.running:
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
            self.operations()
            pygame.display.flip()
            self.clock.tick(MENU_FPS)

    def operations(self):
        self._draw_background()
        self._mouse_operations()
        self._draw_buttons()

    def _draw_background(self):
        self.screen.blit(background, MENU_BACKGROUND_POS,
                         (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    def _draw_buttons(self):
        for button in self.buttons_group:
            button.draw(self.screen)

    def _create_buttons(self):
        pass

    def _mouse_operations(self, event=pygame.event.Event):
        pass


class MainMenu(Menu):
    def __init__(self, screen, clock):
        super().__init__(screen, clock)
        self.theme = MenuMusic(MENU_THEME)
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
            Settings(self.screen, self.clock).run()

    def set_music_volume(self, volume):
        self.theme.change_music_volume(volume)


class Settings(Menu):
    def __init__(self, screen, clock):
        super().__init__(screen, clock)

    def _mouse_operations(self, event=pygame.event.Event):
        mouse_pos = pygame.mouse.get_pos()
        self._btn_exit_check(mouse_pos, event)
        self._slider_music_check(mouse_pos, event)

    def _create_buttons(self):
        self.btn_exit = Button(self.buttons_group, MENU_BTN_EXIT_POS, PAUSE_BACK_TO_MENU_NAME,
                               textures_buttons_dict['menu']['normal'][0],
                               textures_buttons_dict['menu']['hovered'][0], textures_buttons_dict['menu']['clicked'][0])
        self.slider_music = Slider(self.buttons_group, MENU_MUSIC_POS, MENU_MUSIC_SIZE,
                                   SoundEffect.return_volume() / MAX_EFFECTS_VOLUME, 0,
                                   MAX_EFFECTS_VOLUME)

    def _btn_exit_check(self, mouse_pos, event):
        if self.btn_exit.check_event(mouse_pos, event):
            self.running = False

    def _slider_music_check(self, mouse_pos, event):
        value = self.slider_music.check_event(mouse_pos, event)
        if value:
            SoundEffect.change_effects_volume(value)
