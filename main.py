from config import *
import pygame
from player import Player
from menu import MainMenu
from sound import Music
from sprite import *


class Game:
    def __init__(self):
        self._screen = pygame.display.set_mode(SCREEN_SIZE, pygame.DOUBLEBUF)
        self._clock = pygame.time.Clock()
        self._caption = WINDOW_NAME
        self.sprites = pygame.sprite.Group()
        self.solid_sprites = pygame.sprite.Group()
        self.passable_sprites = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()

    def _pre_init(self):
        pygame.display.set_caption(self._caption)
        self._menu = MainMenu(self._screen, self._clock)

    def run(self):
        self._pre_init()
        self._menu.run()
        self._init()
        self._play_theme()
        self._config()
        self._update()
        self._finish()

    def _init(self):
        # self.sprites = create_sprites(self._menu.chosen_level)
        self._player = Player(HALF_SCREEN_WIDTH - TILE // 2, SCREEN_HEIGHT - TILE, self.player_group, self.solid_sprites)
        for i in range(3):
            PassableSprite(self.passable_sprites, file_name='wooden_floor.jpg', x=125 * i, y=0)
        self._running = True
        pygame.init()

    def _config(self):
        pygame.display.set_caption(self._caption)
        pygame.mouse.set_visible(True)


    def _render(self):
        self.passable_sprites.draw(self._screen)
        self.solid_sprites.draw(self._screen)
        self.player_group.draw(self._screen)


    def _update(self):
        while self._running:
            self._screen.fill(SKYBLUE)
            self._render()
            self._clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.run()
            self._player.update()

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
