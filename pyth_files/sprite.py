import collections

import pygame.sprite
from pyth_files.load_image import load_image
from pyth_files.config import *
from math import sin

"""Классы всех спрайтов"""


class PassableSprite(pygame.sprite.Sprite):
    """Проходимые спрайты"""

    def __init__(self, *groups, file_name, x, y, anim_state=1, animation_speed=SPRITE_ANIMATION_SPEED / 2):
        super().__init__(*groups)
        self.animation_state = anim_state
        self.animations = textures_anim_dict[file_name]
        self.image = textures_anim_dict[file_name][anim_state][0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = self.rect.copy()
        self.animation_count = 0
        self.name = file_name
        self.animation_speed = animation_speed

    def update(self):
        self.image_update()

    def image_update(self):
        self.animation_count += 1
        if self.animation_speed <= self.animation_count:
            self.animations[self.animation_state].rotate(-1)
            self.image = self.animations[self.animation_state][0]
            self.animation_count = 0


class SolidSprite(PassableSprite):
    """Спрайты, через которые нельзя пройти"""

    def __init__(self, *groups, file_name, x, y, anim_state=1, tiling_x=TILE, tiling_y=TILE, partly_passable=False,
                 breakable=False, breakble_log, id_numb=None):
        super().__init__(*groups, file_name=file_name, x=x, y=y, anim_state=anim_state)
        self.breakable_log = breakble_log
        if breakable:
            if id_numb not in self.breakable_log:
                self.breakable_log[id_numb] = True
            else:
                self.check_existence(id_numb)
            self.id_numb = id_numb
        if partly_passable:
            self.hitbox = pygame.rect.Rect((x, y), (tiling_x, tiling_y - TILE * 0.8))

    def check_existence(self, id_numb):
        if self.breakable_log[id_numb] is False:
            self.kill()

    def break_object(self):
        self.breakable_log[self.id_numb] = False


class Entity(pygame.sprite.Sprite):
    """Класс существа"""

    def __init__(self, groups, speed=PLAYER_ANIMATION_SPEED):
        super().__init__(*groups)
        self.hitbox = self.rect = self.solid_sprites = None
        # Движение
        self.direction = pygame.math.Vector2()
        self.animation_speed = speed
        self.frame_index = 0
        self.vulnerable = True
        self.hit_time = None

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.solid_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
        if direction == 'vertical':
            for sprite in self.solid_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    @staticmethod
    def alpha_get():
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0


"""Словарики с картинками"""
textures_anim_dict = {
    # level 1
    'floor': {
        1: collections.deque(
            [pygame.transform.scale(load_image(TEXTURES_PATH_LEVEL, 'level_1/floor.png'), (800, 400))]
        )
    },
    'back_wall': {
        1: collections.deque(
            [pygame.transform.scale(load_image(TEXTURES_PATH_LEVEL, 'level_1/back_wall.png'), (800, 200))])
    },
    'side_wall': {
        1: collections.deque(
            [pygame.transform.scale(load_image(TEXTURES_PATH_LEVEL, 'level_1/side_wall.png'), (40, 680))])
    },
    'down_wall': {
        1: collections.deque(
            [pygame.transform.scale(load_image(TEXTURES_PATH_LEVEL, 'level_1/down_wall.png'), (800, 100))])
    },
    'inside_wall': {
        1: collections.deque(
            [pygame.transform.scale(load_image(TEXTURES_PATH_LEVEL, 'level_1/inside_wall.png'), (40, 280))])
    },
    'oven': {
        1:
            collections.deque(
                [pygame.transform.scale(load_image(TEXTURES_PATH, 'solid_textures/oven/off/0.png'), (100, 100))]),
        -1:
            collections.deque(
                [pygame.transform.scale(load_image(f'{TEXTURES_PATH}/solid_textures', f'oven/on/{i}.png'), (100, 100))
                 for i in range(6)]
            )
    },
    'wardrobe': {
        1: collections.deque(
            [pygame.transform.scale(load_image(TEXTURES_PATH, 'solid_textures/wardrobe/wardrobe.png'), (60, 200))])
    },
    'carpet': {
        1:
            collections.deque(
                [pygame.transform.scale(load_image(TEXTURES_PATH, 'passable_textures/carpet.png'), (400, 250))]
            )
    },
    # level 2
    'back_wall_2': {
        1:
            collections.deque(
                [pygame.transform.scale(load_image(TEXTURES_PATH_LEVEL, 'level_2/back_wall.png'), (1920, 200))]
            )
    },
    'down_wall_1': {
        1:
            collections.deque(
                [pygame.transform.scale(load_image(TEXTURES_PATH_LEVEL, 'level_2/down_wall_1.png'), (1520, 100))]
            )
    },
    'down_wall_2': {
        1:
            collections.deque(
                [pygame.transform.scale(load_image(TEXTURES_PATH_LEVEL, 'level_2/down_wall_2.png'), (943, 100))]
            )
    },
    'floor_2': {
        1:
            collections.deque(
                [pygame.transform.scale(load_image(TEXTURES_PATH_LEVEL, 'level_2/floor.png'), (1920, 960))]
            )
    },
    'store_back': {
        1:
            collections.deque(
                [pygame.transform.scale(load_image(TEXTURES_PATH_LEVEL, 'level_2/store_back.png'), (219, 140))]
            )
    },
    'store_front': {
        1:
            collections.deque(
                [pygame.transform.scale(load_image(TEXTURES_PATH_LEVEL, 'level_2/store_front.png'), (200, 80))]
            )
    },
    'flowerbed': {
        1:
            collections.deque(
                [pygame.transform.scale(load_image(f'{TEXTURES_PATH}/solid_textures', f'flowerbed/{i}.png'), (120, 60))
                 for i in range(2)]
            )
    },
    'down_roof_1': {
        1:
            collections.deque(
                [pygame.transform.scale(load_image(TEXTURES_PATH_LEVEL, 'level_2/roofs/down_roof_1.png'), (1545, 160))]
            )
    },
    'down_roof_2': {
        1:
            collections.deque(
                [pygame.transform.scale(load_image(TEXTURES_PATH_LEVEL, 'level_2/roofs/down_roof_2.png'), (580, 160))]
            )
    },
    'left_roof_1': {
        1:
            collections.deque(
                [pygame.transform.scale(load_image(TEXTURES_PATH_LEVEL, 'level_2/roofs/left_roof_1.png'), (200, 900))]
            )
    },
    'left_roof_2': {
        1:
            collections.deque(
                [pygame.transform.scale(load_image(TEXTURES_PATH_LEVEL, 'level_2/roofs/left_roof_2.png'), (195, 600))]
            )
    },
    'right_roof': {
        1:
            collections.deque(
                [pygame.transform.scale(load_image(TEXTURES_PATH_LEVEL, 'level_2/roofs/right_roof.png'), (200, 1500))]
            )
    },
    'up_roof': {
        1:
            collections.deque(
                [pygame.transform.scale(load_image(TEXTURES_PATH_LEVEL, 'level_2/roofs/up_roof.png'), (1920, 200))]
            )
    },
    # level 3
    'floor_3': {
        1:
            collections.deque(
                [pygame.transform.scale(load_image(TEXTURES_PATH_LEVEL, 'level_3/floor.png'), (1160, 760))]
            )
    },
    'back_wall_3': {
        1:
            collections.deque(
                [pygame.transform.scale(load_image(TEXTURES_PATH_LEVEL, 'level_3/back_wall.png'), (1160, 200))]
            )
    },
    'down_wall_3': {
        1:
            collections.deque(
                [pygame.transform.scale(load_image(TEXTURES_PATH_LEVEL, 'level_3/down_wall.png'), (1160, 120))]
            )
    },
    'side_wall_3': {
        1:
            collections.deque(
                [pygame.transform.scale(load_image(TEXTURES_PATH_LEVEL, 'level_3/side_wall.png'), (40, 1000))]
            )
    },
    'cage': {
        1:
            collections.deque(
                [pygame.transform.scale(load_image(TEXTURES_PATH_LEVEL, 'level_3/cage.png'), (400, 400))]
            )
    },
    'machine': {
        1:
            collections.deque(
                [pygame.transform.scale(load_image(TEXTURES_PATH_LEVEL, 'level_3/machine.png'), (280, 320))]
            )
    },
}

player_anim_dict = {
    'normal': {
        'down':
            collections.deque(
                [load_image(f'{PLAYER_TEXTURES_PATH}/normal', f'down_frames/{i}.png', color_key=-1) for i in
                 range(4)]),
        'up':
            collections.deque(
                [load_image(f'{PLAYER_TEXTURES_PATH}/normal', f'up_frames/{i}.png', color_key=-1) for i in
                 range(4)]),
        'right':
            collections.deque(
                [load_image(f'{PLAYER_TEXTURES_PATH}/normal', f'right_frames/{i}.png', color_key=-1) for i in
                 range(4)]),
        'left':
            collections.deque(
                [load_image(f'{PLAYER_TEXTURES_PATH}/normal', f'left_frames/{i}.png', color_key=-1) for i in
                 range(4)]),
        'down_idle':
            collections.deque(
                [load_image(f'{PLAYER_TEXTURES_PATH}/normal', f'down_idle_frames/{i}.png') for i in range(4)]),
        'up_idle':
            collections.deque(
                [load_image(f'{PLAYER_TEXTURES_PATH}/normal', f'up_idle_frames/{i}.png') for i in range(4)]),
        'left_idle':
            collections.deque(
                [load_image(f'{PLAYER_TEXTURES_PATH}/normal', f'left_idle_frames/{i}.png') for i in range(4)]),
        'right_idle':
            collections.deque(
                [load_image(f'{PLAYER_TEXTURES_PATH}/normal', f'right_idle_frames/{i}.png') for i in range(4)]),
        'left_attack': collections.deque(
            [load_image(f'{PLAYER_TEXTURES_PATH}/normal', f'attack_left_frames/{i}.png') for i in range(7)]),
        'right_attack': collections.deque(
            [load_image(f'{PLAYER_TEXTURES_PATH}/normal', f'attack_right_frames/{i}.png') for i in range(7)]),
        'down_attack': collections.deque(
            [load_image(f'{PLAYER_TEXTURES_PATH}/normal', f'attack_down_frames/{i}.png') for i in range(7)]),
        'up_attack': collections.deque(
            [load_image(f'{PLAYER_TEXTURES_PATH}/normal', f'attack_up_frames/{i}.png') for i in range(7)]),
    },
    'christmas': {
        'down':
            collections.deque(
                [load_image(f'{PLAYER_TEXTURES_PATH}/christmas', f'down_frames/{i}.png') for i in range(4)]),
        'up':
            collections.deque(
                [load_image(f'{PLAYER_TEXTURES_PATH}/christmas', f'up_frames/{i}.png') for i in range(4)]),
        'right':
            collections.deque(
                [load_image(f'{PLAYER_TEXTURES_PATH}/christmas', f'right_frames/{i}.png') for i in range(4)]),
        'left':
            collections.deque(
                [load_image(f'{PLAYER_TEXTURES_PATH}/christmas', f'left_frames/{i}.png') for i in range(4)]),
        'down_idle':
            collections.deque(
                [load_image(f'{PLAYER_TEXTURES_PATH}/christmas', f'down_idle_frames/{i}.png') for i in range(4)]),
        'up_idle':
            collections.deque(
                [load_image(f'{PLAYER_TEXTURES_PATH}/christmas', f'up_idle_frames/{i}.png') for i in range(4)]),
        'left_idle':
            collections.deque(
                [load_image(f'{PLAYER_TEXTURES_PATH}/christmas', f'left_idle_frames/{i}.png') for i in range(4)]),
        'right_idle':
            collections.deque(
                [load_image(f'{PLAYER_TEXTURES_PATH}/christmas', f'right_idle_frames/{i}.png') for i in range(4)]),
        'left_attack': collections.deque([load_image(f'{PLAYER_TEXTURES_PATH}/normal', f'left_frames/0.png')]),
        'right_attack': collections.deque([load_image(f'{PLAYER_TEXTURES_PATH}/normal', f'right_frames/0.png')]),
        'down_attack': collections.deque([load_image(f'{PLAYER_TEXTURES_PATH}/normal', f'down_frames/0.png')]),
        'up_attack': collections.deque([load_image(f'{PLAYER_TEXTURES_PATH}/normal', f'up_frames/0.png')])
    }
}

player_particles_dict = {
    'leaf': (collections.deque(
        [load_image(f'{PARTICLES_TEXTURES_PATH}', f'leaf1/{i}.png') for i in range(12)]),
             collections.deque(
                 [load_image(f'{PARTICLES_TEXTURES_PATH}', f'leaf2/{i}.png') for i in range(12)]
             ),
             collections.deque(
                 [pygame.transform.flip(load_image(f'{PARTICLES_TEXTURES_PATH}', f'leaf1/{i}.png'), True, False) for i
                  in range(12)]),
             collections.deque(
                 [pygame.transform.flip(load_image(f'{PARTICLES_TEXTURES_PATH}', f'leaf2/{i}.png'), True, False) for i
                  in range(12)]
             ))
}

enemy_anim_dict = {
    'skeleton': {
        'down':
            collections.deque(
                [load_image(f'{ENEMY_TEXTURES_PATH}/skeleton', f'down_frames/{i}.png') for i in range(4)]),
        'up':
            collections.deque(
                [load_image(f'{ENEMY_TEXTURES_PATH}/skeleton', f'up_frames/{i}.png') for i in range(4)]),
        'right':
            collections.deque(
                [load_image(f'{ENEMY_TEXTURES_PATH}/skeleton', f'right_frames/{i}.png') for i in range(4)]),
        'left':
            collections.deque(
                [load_image(f'{ENEMY_TEXTURES_PATH}/skeleton', f'left_frames/{i}.png') for i in range(4)]),
        'down_idle':
            collections.deque(
                [load_image(f'{ENEMY_TEXTURES_PATH}/skeleton', f'idle_frames/{i}.png') for i in range(4)]),
        'left_attack': collections.deque(
            [load_image(f'{ENEMY_TEXTURES_PATH}/skeleton', f'attack_left_frames/{i}.png') for i in range(7)]),
        'right_attack': collections.deque(
            [load_image(f'{ENEMY_TEXTURES_PATH}/skeleton', f'attack_right_frames/{i}.png') for i in range(7)]),
        'down_attack': collections.deque(
            [load_image(f'{ENEMY_TEXTURES_PATH}/skeleton', f'attack_down_frames/{i}.png') for i in range(7)]),
        'up_attack': collections.deque(
            [load_image(f'{ENEMY_TEXTURES_PATH}/skeleton', f'attack_up_frames/{i}.png') for i in range(7)])
    }
}

textures_buttons_dict = {
    'menu': {
        'normal':
            collections.deque(
                [pygame.transform.scale(load_image(f'{MENU_BUTTONS_TEXTURES_PATH}/menu', f'0.png'),
                                        (BUTTON_WIDTH, BUTTON_HEIGHT))]),
        'hovered':
            collections.deque(
                [pygame.transform.scale(load_image(f'{MENU_BUTTONS_TEXTURES_PATH}/menu', f'1.png'),
                                        (BUTTON_WIDTH, BUTTON_HEIGHT))]),
        'clicked':
            collections.deque(
                [pygame.transform.scale(load_image(f'{MENU_BUTTONS_TEXTURES_PATH}/menu', f'2.png'),
                                        (BUTTON_WIDTH, BUTTON_HEIGHT))])
    }
}

tag_images_dict = {
    '1': {'correct': collections.deque([pygame.transform.scale(
        load_image(f'{TAG_TEXTURES_PATH}', f'correct/{i}.png'), (TAG_TRICK_SIZE, TAG_TRICK_SIZE)) for i in range(16)]),
        'messed_up': collections.deque([pygame.transform.scale(
            load_image(f'{TAG_TEXTURES_PATH}', f'messed_up/{i}.png'), (TAG_TRICK_SIZE, TAG_TRICK_SIZE)) for i in
            range(16)]),
        'to_correct': collections.deque(
            [pygame.transform.scale(
                load_image(f'{TAG_TEXTURES_PATH}', f'to_correct/{i}.png'), (TAG_TRICK_SIZE, TAG_TRICK_SIZE)) for i in
                range(16)])}
}
