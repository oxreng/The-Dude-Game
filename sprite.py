import collections

import pygame.sprite
from load_image import load_image
from config import *


class PassableSprite(pygame.sprite.Sprite):
    def __init__(self, *groups, file_name, x, y, anim_state=1):
        super().__init__()
        for group in groups:
            self.add(group)
        self.animation_state = anim_state
        self.animations = textures_anim_dict[file_name]
        self.image = textures_anim_dict[file_name][anim_state][0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.animation_count = 0
        self.name = file_name

    def image_update(self, animation_speed=SPRITE_ANIMATION_SPEED / 2):
        self.animation_count += 1
        if animation_speed <= self.animation_count:
            self.animations[self.animation_state].rotate(-1)
            self.image = self.animations[self.animation_state][0]
            self.animation_count = 0


class SolidSprite(PassableSprite):
    def __init__(self, *groups, file_name, x, y, anim_state=1, tiling_x=TILE, tiling_y=TILE, partly_passable=False):
        super().__init__(*groups, file_name=file_name, x=x, y=y, anim_state=anim_state)
        if partly_passable:
            self.rect = pygame.rect.Rect((x, y), (tiling_x, tiling_y - TILE * 0.8))


textures_anim_dict = {
    'back_wall': {
        1: collections.deque(
            [pygame.transform.scale(load_image(TEXTURES_PATH, 'map_tiles/back_wall.png'), (800, 200))])
    },
    'side_wall': {
        1: collections.deque(
            [pygame.transform.scale(load_image(TEXTURES_PATH, 'map_tiles/side_wall.png'), (40, 680))])
    },
    'down_wall': {
        1: collections.deque(
            [pygame.transform.scale(load_image(TEXTURES_PATH, 'map_tiles/down_wall.png'), (800, 100))])
    },
    'inside_wall': {
        1: collections.deque(
            [pygame.transform.scale(load_image(TEXTURES_PATH, 'map_tiles/inside_wall.png'), (40, 280))])
    },
    'oven': {
        1:
            collections.deque(
                [pygame.transform.scale(load_image(TEXTURES_PATH, 'solid_textures/oven/off/1.png'), (100, 100))]),
        -1:
            collections.deque(
                [pygame.transform.scale(load_image(f'{TEXTURES_PATH}/solid_textures', f'oven/on/{i}.png'), (100, 100)) for i in range(1, 7)]
            )
    },
    'carpet': {
        1:
            collections.deque(
                [pygame.transform.scale(load_image(TEXTURES_PATH, 'map_tiles/carpet.png'), (400, 250))]
            )
    }
}

player_anim_dict = {
    'normal': {
        'down':
            collections.deque(
                [load_image(f'{PLAYER_PATH}/normal', f'down_frames/{i}.png', color_key=-1) for i in range(1, 5)]),
        'up':
            collections.deque(
                [load_image(f'{PLAYER_PATH}/normal', f'up_frames/{i}.png', color_key=-1) for i in range(1, 5)]),
        'right':
            collections.deque(
                [load_image(f'{PLAYER_PATH}/normal', f'right_frames/{i}.png', color_key=-1) for i in range(1, 5)]),
        'left':
            collections.deque(
                [load_image(f'{PLAYER_PATH}/normal', f'left_frames/{i}.png', color_key=-1) for i in range(1, 5)]),
        'down_idle':
            collections.deque(
                [load_image(f'{PLAYER_PATH}/normal', f'down_idle_frames/{i}.png') for i in range(1, 5)]),
        'up_idle':
            collections.deque(
                [load_image(f'{PLAYER_PATH}/normal', f'up_idle_frames/{i}.png') for i in range(1, 5)]),
        'left_idle':
            collections.deque(
                [load_image(f'{PLAYER_PATH}/normal', f'left_idle_frames/{i}.png') for i in range(1, 5)]),
        'right_idle':
            collections.deque(
                [load_image(f'{PLAYER_PATH}/normal', f'right_idle_frames/{i}.png') for i in range(1, 5)]),
        'left_attack': collections.deque([load_image(f'{PLAYER_PATH}/christmas', f'left_frames/1.png')]),
        'right_attack': collections.deque([load_image(f'{PLAYER_PATH}/christmas', f'right_frames/1.png')]),
        'down_attack': collections.deque([load_image(f'{PLAYER_PATH}/christmas', f'down_frames/1.png')]),
        'up_attack': collections.deque([load_image(f'{PLAYER_PATH}/christmas', f'up_frames/1.png')])
    },
    'christmas': {
        'down':
            collections.deque(
                [load_image(f'{PLAYER_PATH}/christmas', f'down_frames/{i}.png') for i in range(1, 5)]),
        'up':
            collections.deque(
                [load_image(f'{PLAYER_PATH}/christmas', f'up_frames/{i}.png') for i in range(1, 5)]),
        'right':
            collections.deque(
                [load_image(f'{PLAYER_PATH}/christmas', f'right_frames/{i}.png') for i in range(1, 5)]),
        'left':
            collections.deque(
                [load_image(f'{PLAYER_PATH}/christmas', f'left_frames/{i}.png') for i in range(1, 5)]),
        'standing':
            collections.deque(
                [load_image(f'{PLAYER_PATH}/christmas', f'standing_frames/{i}.png') for i in range(1, 5)]),
        'left_attack': collections.deque([load_image(f'{PLAYER_PATH}/normal', f'left_frames/1.png')]),
        'right_attack': collections.deque([load_image(f'{PLAYER_PATH}/normal', f'right_frames/1.png')]),
        'down_attack': collections.deque([load_image(f'{PLAYER_PATH}/normal', f'down_frames/1.png')]),
        'up_attack': collections.deque([load_image(f'{PLAYER_PATH}/normal', f'up_frames/1.png')])
    }
}
