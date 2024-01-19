from config import *
import pygame
from player import Player
from menu import MainMenu
from sound import Music
from sprite import *
from cameras import *
from sound import SoundEffect
from interactions import dialogue_markers
from debug import debug
from level import Level
from dialogue import Dialogue
from pause import Pause
from death_window import DeathWindow


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(SCREEN_SIZE, pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        self._caption = WINDOW_NAME

    def _pre_init(self):
        pygame.display.set_caption(self._caption)
        self._menu = MainMenu(self.screen, self.clock)
        self._level = Level(self.screen, self.clock, self.run)
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
        FIRSTDIALOGUETIMER = pygame.USEREVENT + 1
        pygame.time.set_timer(FIRSTDIALOGUETIMER, 500)
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
                if event.type == FIRSTDIALOGUETIMER:
                    if not dialogue_markers['dialogue_1']:
                        Dialogue(self.screen, self.clock, 'dialogue_1').run()
                        dialogue_markers['dialogue_1'] = True
                    pygame.time.set_timer(FIRSTDIALOGUETIMER, 0)

    def set_pause(self):
        if Pause(self.screen, self.clock).run():
            self.run()

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
