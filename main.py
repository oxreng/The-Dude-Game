import datetime
from config import *
import pygame
from menu import MainMenu
from sound import Music
from sprite import *
from cameras import *
from sound import SoundEffect
from debug import debug
from level import Level
from pause import Pause
from fade import Fade
from end_screen import EndScreen
from statistic import Statistics
from minigames.tag import Tag


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(SCREEN_SIZE, pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        self._caption = WINDOW_NAME

    def _pre_init(self):
        pygame.display.set_caption(self._caption)
        self.statistics = Statistics()
        self._menu = MainMenu(self.screen, self.clock)
        self._level = Level(self.screen, self.clock, self.run, self.statistics)
        SoundEffect.change_effects_volume(
            STANDARD_EFFECTS_VOLUME if SoundEffect.return_volume() == 1 else SoundEffect.return_volume())

    def run(self):
        self._pre_init()
        self._menu.run()
        self._init()
        self._play_theme()
        self._config()
        self._update()
        self._finish()

    def _init(self):
        self._running = True
        pygame.init()

    def _config(self):
        pygame.display.set_caption(self._caption)
        pygame.mouse.set_visible(True)

    def _update(self):
        Fade(self.screen).fade_in(FADE_SPEED_MENU)
        self._level.show()
        Fade(self.screen).fade_out(FADE_SPEED_MENU)
        while self._running:
            self._level.show()
            self.clock.tick(FPS)
            pygame.display.set_caption('FPS: ' + str(int(self.clock.get_fps())))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.set_pause()
                    if event.key == pygame.K_z:
                        self.end_screen()
                    if event.key == pygame.K_m:
                        self.minigame()

    def set_pause(self):
        if Pause(self.screen, self.clock).run():
            self.run()

    def end_screen(self):
        if EndScreen(self.screen, self.clock, self.statistics).run():
            self.run()

    def minigame(self):
        Tag(self.screen, self.clock, player_particles_dict['leaf'][0]).run()

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
