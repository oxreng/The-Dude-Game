from config import *
import pygame
from player import Player
from menu import MainMenu
from sound import Music
from sprite import *
from cameras import *


class Game:
    def __init__(self):
        self._screen = pygame.display.set_mode(SCREEN_SIZE, pygame.DOUBLEBUF)
        self._clock = pygame.time.Clock()
        self._caption = WINDOW_NAME

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
        self.solid_sprites = pygame.sprite.Group()
        self.passable_sprites = pygame.sprite.Group()
        self.partly_passable_sprites = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle()
        self.camera_group = CameraGroup()
        # self.sprites = create_sprites(self._menu.chosen_level)
        self._player = Player(self.camera_group, self.player_group, x=HALF_SCREEN_WIDTH, y=HALF_SCREEN_HEIGHT,
                              solid_sprites=self.solid_sprites, partly_sprites=self.partly_passable_sprites)

        # Создание спрайтов карты
        PartlyPassableSprite(self.camera_group, self.partly_passable_sprites, file_name='map_tiles/back_wall.png', x=0, y=-200,
                    colorkey=None, tiling_x=800, tiling_y=200)
        SolidSprite(self.camera_group, self.solid_sprites, file_name='map_tiles/side_wall.png', x=-40, y=-200,
                    colorkey=None, tiling_x=40, tiling_y=680)
        SolidSprite(self.camera_group, self.solid_sprites, file_name='map_tiles/side_wall.png', x=800, y=-200,
                    colorkey=None, tiling_x=40, tiling_y=680)
        SolidSprite(self.camera_group, self.solid_sprites, file_name='map_tiles/down_wall.png', x=0, y=380,
                    colorkey=None, tiling_x=800, tiling_y=100)
        PartlyPassableSprite(self.camera_group, self.solid_sprites, file_name='map_tiles/inside_wall.png', x=180, y=-200,
                    colorkey=None, tiling_x=40, tiling_y=280)
        self.camera_group.center_target_camera(self._player)
        self._running = True
        pygame.init()

    def _config(self):
        pygame.display.set_caption(self._caption)
        pygame.mouse.set_visible(True)

    def _render(self):
        # self.passable_sprites.draw(self._screen)
        self.camera_group.custom_draw(self.passable_sprites, player=self._player)
        # self.solid_sprites.draw(self._screen)
        # self.player_group.draw(self._screen)

    def _update(self):
        while self._running:
            self._screen.fill(BLACK)
            self._player.update()
            self._render()
            self._clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.run()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.camera_group.zooming(event.button)

            # keys = pygame.key.get_pressed()
            # if keys[pygame.K_h]:
                # self.camera_group.center_target_camera(self._player)

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
