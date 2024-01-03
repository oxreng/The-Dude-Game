import collections

import pygame.sprite
from load_image import load_image
from config import *


class PassableSprite(pygame.sprite.Sprite):
    def __init__(self, *groups, file_name, x, y, colorkey=None):
        super().__init__()
        for group in groups:
            self.add(group)
        self.image = pygame.transform.scale(load_image(PASSABLE_TEXTURES_PATH, file_name, color_key=colorkey), (200, 125))
        self.rect = self.image.get_rect(topleft=(x, y))

    def image_update(self, *args, **kwargs):
        pass


class SolidSprite(pygame.sprite.Sprite):
    def __init__(self, *groups, file_name, x, y, anim_state=1):
        super().__init__()
        for group in groups:
            self.add(group)
        self.animation_state = anim_state
        self.animations = textures_anim_dict[file_name]
        self.image = textures_anim_dict[file_name][anim_state][0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0

    def image_update(self, animation_speed=SPRITE_ANIMATION_SPEED / 2):
        self.animation_count += 1
        if animation_speed <= self.animation_count:
            self.animations[self.animation_state].rotate(-1)
            self.image = self.animations[self.animation_state][0]
            self.animation_count = 0


class PartlyPassableSprite(SolidSprite):
    def __init__(self, *groups, file_name, x, y, tiling_x=TILE, tiling_y=TILE, anim_state=1):
        super().__init__(*groups, file_name=file_name, x=x, y=y, anim_state=anim_state)
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
        'standing':
            collections.deque(
                [load_image(f'{PLAYER_PATH}/normal', f'standing_frames/{i}.png') for i in range(1, 5)]),
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

collide_areas = {
    'door': pygame.Rect((320, -140,), (80, 140)),
    'oven': pygame.Rect((40, -60), (100, 100))
}

hint_text = {
    'door': 'Press  E  to  open',
    'oven': 'Press  E  to  interact'
}

# def sprites_update(sprites, player):
#     for sprite in sprites:
#         sprite.update()
#         if isinstance(sprite, ...):
#             sprite.full_update(player)
#
#             if sprite.can_attack(player):
#                 ....damage()
#                 ....get_damage(3)
#
#                 if not sprite.is_dead:
#                     sprite.attack()
#                     player.damage(sprite.damage)
#             else:
#                 sprite.stop_attack()
#         elif isinstance(sprite, ...):
#             if sprite.can_pick(player.pos):
#                 sprite.pick()
#                 player.pick(sprite.type)
#     return sprites
