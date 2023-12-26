from config import *
import pygame
from player import Player
from menu import MainMenu
from sound import Music
from render import Render
from sprite import *


class Game:
    def __init__(self):
        self._screen = pygame.display.set_mode(SCREEN_SIZE, pygame.DOUBLEBUF)
        self._clock = pygame.time.Clock()
        self._caption = WINDOW_NAME
        self.sprites = pygame.sprite.Group()
        self.solid_sprites = pygame.sprite.Group()

    def _pre_init(self):
        pygame.display.set_caption(self._caption)
        self._menu = MainMenu(self._screen, self._clock)

    def run(self):
        self._pre_init()
        # self._menu.run()
        self._init()
        self._play_theme()
        self._config()
        self._update()
        self._finish()

    def _init(self):
        # self.sprites = create_sprites(self._menu.chosen_level)
        self._player = Player(HALF_SCREEN_WIDTH - TILE // 2, SCREEN_HEIGHT - TILE, self.sprites, self.solid_sprites)
        self._render = Render(self._screen, self._player, self.sprites)
        self._running = True
        pygame.init()

    def _config(self):
        pygame.display.set_caption(self._caption)
        pygame.mouse.set_visible(True)

    def _update(self):
        while self._running:
            self._screen.fill(SKYBLUE)
            self._clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.run()
            self._player.update()
            self._render.render()

            pygame.display.set_caption('FPS: ' + str(int(self._clock.get_fps())))
            pygame.display.flip()

    @staticmethod
    def _finish():
        pygame.quit()

    @staticmethod
    def _play_theme():
        theme = Music()
        theme.play_music()


if __name__ == '__main__':
    game = Game()
    game.run()
