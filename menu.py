import sys
import pygame
from config import *
from sound import MenuMusic
from load_image import load_image

pygame.init()
background = load_image(TEXTURES_PATH, MENU_BACKGROUND, color_key=None)
button_font = pygame.font.Font(FONT, BUTTON_FONT_SIZE)
logo_font = pygame.font.Font(FONT, LOGO_FONT_SIZE)


def button(screen, name, color, rect_pos, width, height, font):
    text = font.render(name, True, color)
    btn = pygame.Rect(rect_pos[0], rect_pos[1], width, height)
    screen.blit(text, (rect_pos[0], rect_pos[1]))
    return btn, text


class Menu:
    def __init__(self, screen, clock):
        self.x = 0
        self.screen = screen
        self.clock = clock
        self.delay = 0
        self.running = True
        self.delta_x = 0
        self.theme = MenuMusic(MENU_THEME)

    def run(self, delta_x=0):
        self.theme = MenuMusic(MENU_THEME)
        self.play_theme()
        self.delta_x = delta_x
        pygame.time.delay(self.delay)
        pygame.mouse.set_visible(True)
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.operations()
            pygame.display.flip()
            self.clock.tick(MENU_FPS)

    def operations(self):
        self._draw_background()
        self._logo()
        self._create_buttons()
        self._mouse_operations()

    def play_theme(self):
        self.theme.play_music()

    def _draw_background(self):
        self.screen.blit(background, MENU_BACKGROUND_POS,
                         (self.delta_x % SCREEN_WIDTH, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        self.delta_x += 1

    def _logo(self):
        ...

    def set_music_volume(self, volume):
        self.theme.change_music_volume(volume)

    def _create_buttons(self):
        pass

    def _mouse_operations(self):
        pass

    def check_chosen_level(self):
        pass


class MainMenu(Menu):
    def __init__(self, screen, clock):
        super().__init__(screen, clock)
        self.mode = None

    def _mouse_operations(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        self._btn_exit_check(mouse_pos, mouse_click)
        self._btn_start_check(mouse_pos, mouse_click)

    def _create_buttons(self):
        self.btn_exit, self.exit = button(self.screen, EXIT_NAME, WHITE, BTN_EXIT_BACK_POS, *BTN_EXIT_BACK_SIZE,
                                          button_font)
        self.btn_start, self.start = button(self.screen, START_NAME, WHITE, BTN_START_BACK_POS, *BTN_START_BACK_SIZE,
                                            button_font)

    def _btn_exit_check(self, mouse_pos, mouse_click):
        if self.btn_exit.collidepoint(mouse_pos):
            button(self.screen, EXIT_NAME, WHITE, BTN_EXIT_BACK_POS, *BTN_EXIT_BACK_SIZE,
                   button_font)
            if mouse_click[0]:
                pygame.quit()
                sys.exit()

    def _btn_start_check(self, mouse_pos, mouse_click):
        if self.btn_start.collidepoint(mouse_pos):
            button(self.screen, START_NAME, WHITE, BTN_START_BACK_POS, *BTN_START_BACK_SIZE,
                   button_font)
            if mouse_click[0]:
                self.running = False
