# Настройки экрана
import os.path
from os import listdir
from os.path import isfile, join

SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = (1200, 600)
HALF_SCREEN_WIDTH, HALF_SCREEN_HEIGHT = SCREEN_WIDTH >> 1, SCREEN_HEIGHT >> 1
WINDOW_NAME = 'The Dude'

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
WOODEN = (154, 126, 97)
WOODEN_DARKER = (92, 75, 58)
BLUE = 'Blue'
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
UI_TEXT_COLOR = '#EEEEEE'
UI_HEALTH_COLOR = RED
UI_BORDER_COLOR_ACTIVE = 'gold'

# Настройки меню
MENU_FPS = 60
MENU_FONT = 'data/fonts/joystix.ttf'
BUTTON_FONT_SIZE = 75
LOGO_FONT_SIZE = 250
MENU_BACKGROUND = 'StartWindow.jpg'
MENU_BACKGROUND_POS = (0, 0)
MENU_EXIT_NAME = 'ВЫХОД'
MENU_START_NAME = 'НАЧАТЬ'
MENU_SETTING_NAME = 'НАСТРОЙКИ'
MENU_FONT_SIZE = 18
MENU_BTN_START_POS = (50, 105)
MENU_BTN_SETTINGS_POS = (50, 270)
MENU_BTN_EXIT_POS = (50, 435)

# Настройки настроек
SETTINGS_MUSIC_EFFECTS_POS = (350, 380)
SETTINGS_MUSIC_EFFECTS_SIZE = (500, 60)
SETTINGS_MUSIC_MUSIC_POS = (350, 160)
SETTINGS_MUSIC_MUSIC_SIZE = (500, 60)
SETTINGS_BACK_TO_MENU_POS = (50, 490)
SETTINGS_BACK_TO_MENU_NAME = 'НАЗАД'
SETTINGS_MUSIC_EFFECTS_NAME = 'ГРОМКОСТЬ ЭФФЕКТОВ'
SETTINGS_MUSIC_MUSIC_NAME = 'ГРОМКОСТЬ МУЗЫКИ'

# Настройки экрана смерти
DEATH_BACK_TO_MENU_POS = (50, 490)
DEATH_BACK_TO_MENU_NAME = 'В МЕНЮ'
DEATH_RESTART_POS = (50, 50)
DEATH_RESTART_NAME = 'ЗАНОВО'

# Настройка перехода
FADE_SPEED_LEVELS = 15
FADE_SPEED_MENU = 30

# Настройки пятнашек
TAG_FIRST_X_POS = 500
TAG_FIRST_Y_POS = 200
TAG_TRICK_MOVE = 60
TAG_TRICK_QUANTITY = 16
TAG_TRICK_MAX_X = TAG_FIRST_X_POS + TAG_TRICK_MOVE * (TAG_TRICK_QUANTITY ** 0.5 - 1)
TAG_TRICK_MAX_Y = TAG_FIRST_Y_POS + TAG_TRICK_MOVE * (TAG_TRICK_QUANTITY ** 0.5 - 1)
TAG_TRICK_SIZE = TAG_TRICK_MOVE
TAG_BACK_NAME = 'НАЗАД'
TAG_BTN_BACK_POS = (50, 435)

# Настройки паузы
PAUSE_CONTINUE_NAME = 'ПРОДОЛЖИТЬ'
PAUSE_BACK_TO_MENU_NAME = 'В МЕНЮ'
PAUSE_BTN_CONTINUE_POS = (50, 105)
PAUSE_BTN_SETTINGS_POS = (50, 270)
PAUSE_BTN_BACK_TO_MENU_POS = (50, 435)

# Настройки текстур
TILE = 100
TEXTURES_PATH = 'data/images'
TEXTURES_PATH_LEVEL = 'data/images/map_tiles'
PASSABLE_TEXTURES_PATH = 'data/images/passable_textures'
SOLID_TEXTURES_PATH = 'data/images/solid_textures'
PLAYER_TEXTURES_PATH = 'data/images/player'
ENEMY_TEXTURES_PATH = 'data/images/enemies'
MENU_BUTTONS_TEXTURES_PATH = 'data/images/buttons_ui'
TAG_TEXTURES_PATH = 'data/images/minigame'
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
PLAYER_ATTACK_COOLDOWN = 900
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
UI_FONT = 'data/fonts/joystix.ttf'
UI_FONT_SIZE = 18

# Настройки врагов
monster_data = {
    'skeleton': {'health': 100, 'money': 100, 'damage': 5, 'attack_type': 'slash', 'attack_sound': 'slash',
                 'speed': 6, 'resistance': 3, 'attack_radius': 80, 'notice_radius': 560, 'attack_cooldown': 400}
}
ENEMY_VULNERABLE_DURATION = 400

# Настройки партиклов
PARTICLES_ANIMATION_SPEED = 0.15
PARTICLES_TEXTURES_PATH = 'data/images/particles'

# Музыка
MENU_THEME = ['data/music/menu_music/menu.mp3']
MUSIC_FOLDER = 'data/music'
GAME_MUSIC_FOLDER = 'data/music/levels_music'
SOUND_BUTTON_PUSH = 'data/music/sound/button_push.mp3'
SOUND_PUNCH = 'data/music/sound/fight/punching.mp3'
SOUND_DAMAGE_RECEIVING = 'data/music/sound/fight/damage_receiving.mp3'
SOUND_DEATH = 'data/music/sound/fight/death_sound.mp3'
MUSIC_FILES = [os.path.join(GAME_MUSIC_FOLDER, file) for file in listdir(GAME_MUSIC_FOLDER) if
               isfile(join(GAME_MUSIC_FOLDER, file))]
MAX_EFFECT_VOLUME = 0.8
MAX_MUSIC_VOLUME = 0.18
STANDARD_MUSIC_VOLUME = 0.09
STANDARD_EFFECT_VOLUME = 0.4

# Подсказки
hint_text = {
    'door': 'Press  E  to  open',
    'oven': 'Press  E  to  interact',
    'wardrobe': 'Press  E  to  get  changed'
}
