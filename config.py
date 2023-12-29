# Настройки экрана
import os.path
from os import listdir
from os.path import isfile, join

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = (1200, 600)
HALF_SCREEN_WIDTH, HALF_SCREEN_HEIGHT = SCREEN_WIDTH >> 1, SCREEN_HEIGHT >> 1
WINDOW_NAME = 'GAME'

# Цвета
ORANGE = 'Orange'
PURPLE = 'Purple'
BLACK = 'Black'
SKYBLUE = 'Skyblue'
DARKGREY = 'Darkgrey'
YELLOW = 'Yellow'
GREEN = 'Green'
RED = 'Red'
WHITE = 'White'
BRICK = (139, 79, 57)
ANTHRACITE = (45, 45, 45)
BLUE = 'Blue'

# Настройки меню
MENU_FPS = 30
FONT = 'font.ttf'
BUTTON_FONT_SIZE = 75
LOGO_FONT_SIZE = 250
MENU_BACKGROUND = 'StartWindow.jpg'
MENU_BACKGROUND_POS = (0, 0)
EXIT_NAME = 'EXIT'
START_NAME = 'START'
BTN_EXIT_BACK_POS = (50, 500)
BTN_EXIT_BACK_SIZE = (150, 60)
BTN_START_BACK_POS = (50, 100)
BTN_START_BACK_SIZE = (200, 60)

# Настройки текстур
TILE = 125
TEXTURES_PATH = 'TextureSprite'
PLAYER_PATH = 'TextureSprite/player'
PLAYER_IMAGE = 'player.png'
PASSABLE_TEXTURES_PATH = 'TextureSprite/passable_textures'
SOLID_TEXTURES_PATH = 'TextureSprite/solid_textures'
PLAYER_TEXTURES_PATH = 'TextureSprite/player'

# Настройки камеры
BOX_LEFT = 0
BOX_RIGHT = 0
BOX_TOP = 0
BOX_BOTTOM = 0
BOX_LEFT_ZOOM = 125
BOX_LEFT_MIN = -375
BOX_TOP_ZOOM = 50
BOX_TOP_MIN = -150
BOX_RIGHT_ZOOM = 125
BOX_RIGHT_MIN = -375
BOX_BOTTOM_ZOOM = 50
BOX_BOTTOM_MIN = -150

# Настройки игрока
FPS = 60
PLAYER_SPEED = 600

# Настройки анимаций
TELLY_FRAMES_COUNT = 2

# Музыка
MENU_THEME = 'music/menu.mp3'
MUSIC_FOLDER = 'Levels_music'
MUSIC_FILES = [os.path.join(MUSIC_FOLDER, file) for file in listdir(MUSIC_FOLDER) if isfile(join(MUSIC_FOLDER, file))]
