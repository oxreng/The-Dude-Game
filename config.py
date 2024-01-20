# Настройки экрана
import os.path
from os import listdir
from os.path import isfile, join

import pygame

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
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
UI_TEXT_COLOR = '#EEEEEE'
UI_HEALTH_COLOR = RED
UI_BORDER_COLOR_ACTIVE = 'gold'

# Настройки меню
MENU_FPS = 60
MENU_FONT = 'fonts/joystix.ttf'
BUTTON_FONT_SIZE = 75
LOGO_FONT_SIZE = 250
MENU_BACKGROUND = 'StartWindow.jpg'
MENU_BACKGROUND_POS = (0, 0)
MENU_EXIT_NAME = 'EXIT'
MENU_START_NAME = 'START'
MENU_SETTING_NAME = 'SETTINGS'
MENU_FONT_SIZE = 18
MENU_BTN_START_POS = (50, 105)
MENU_BTN_SETTINGS_POS = (50, 270)
MENU_BTN_EXIT_POS = (50, 435)
MENU_MUSIC_UP_NAME = '+'
MENU_MUSIC_DOWN_NAME = '-'
MENU_BTN_MUSIC_UP_POS = (866, 240)
MENU_BTN_MUSIC_DOWN_POS = (50, 240)
MENU_MUSIC_POS = (300, 240)
MENU_MUSIC_SIZE = (500, 60)

# Настройка перехода
FADE_SPEED_LEVELS = 15
FADE_SPEED_MENU = 30

# Настройки паузы
PAUSE_CONTINUE_NAME = 'CONTINUE'
PAUSE_BACK_TO_MENU_NAME = 'BACK TO MENU'
PAUSE_BTN_CONTINUE_POS = (50, 105)
PAUSE_BTN_SETTINGS_POS = (50, 270)
PAUSE_BTN_BACK_TO_MENU_POS = (50, 435)


# Настройки текстур
TILE = 100
TEXTURES_PATH = 'TextureSprite'
TEXTURES_PATH_LEVEL = 'TextureSprite/map_tiles/'
PASSABLE_TEXTURES_PATH = 'TextureSprite/passable_textures'
SOLID_TEXTURES_PATH = 'TextureSprite/solid_textures'
PLAYER_TEXTURES_PATH = 'TextureSprite/player'
ENEMY_TEXTURES_PATH = 'TextureSprite/enemies'
MENU_BUTTONS_TEXTURES_PATH = 'TextureSprite/buttons_ui'
SPRITE_ANIMATION_SPEED = 50

# Настройки камеры
BOX_LEFT = 200
BOX_RIGHT = BOX_LEFT
BOX_TOP = 150
BOX_BOTTOM = BOX_TOP

# Настройки игрока
FPS = 60
PLAYER_SPEED = 8
PLAYER_ANIMATION_SPEED = 0.1
PLAYER_ATTACK_COOLDOWN = 750
PLAYER_INTERACTION_COOLDOWN = 500
PLAYER_STAT_HP = 100
PLAYER_STAT_ATTACK = 60
PLAYER_ATTACK_OFFSET = 20
PLAYER_DAMAGE = 10
PLAYER_HURT_TIME = 500

# UI
UI_BAR_HEIGHT = 20
UI_HEALTH_BAR_WIDTH = 200
UI_HEALTH_BAR_COORDS = (10, 10)
UI_FONT = 'fonts/joystix.ttf'
UI_FONT_SIZE = 18

# Настройки врагов
monster_data = {
    'skeleton': {'health': 100, 'money': 10000, 'damage': 5, 'attack_type': 'slash', 'attack_sound': 'slash',
                 'speed': 3, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 360, 'attack_cooldown': 400}
}
ENEMY_VULNERABLE_DURATION = 400

# Настройки партиклов
PARTICLES_ANIMATION_SPEED = 0.15
PARTICLES_TEXTURES_PATH = 'TextureSprite/particles'

# Музыка
MENU_THEME = 'music/menu.mp3'
MUSIC_FOLDER = 'Levels_music'
SOUND_BUTTON_PUSH = 'sound/button_push.mp3'
SOUND_PUNCH = 'sound/fight/punching.mp3'
SOUND_DAMAGE_RECEIVING = 'sound/fight/damage_receiving.mp3'
SOUND_DEATH = 'sound/fight/death_sound.mp3'
MUSIC_FILES = [os.path.join(MUSIC_FOLDER, file) for file in listdir(MUSIC_FOLDER) if isfile(join(MUSIC_FOLDER, file))]
MAX_EFFECTS_VOLUME = 0.8
EFFECTS_VOLUME_CHANGING = 0.1
MUSIC_VOLUME_CHANGING = 0.1
STANDARD_EFFECTS_VOLUME = 0.4

# Подсказки
hint_text = {
    'door': 'Press  E  to  open',
    'oven': 'Press  E  to  interact',
    'wardrobe': 'Press  E  to  get  changed'
}
