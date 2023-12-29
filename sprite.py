import collections

import pygame.sprite
from load_image import load_image
from config import *


class PassableSprite(pygame.sprite.Sprite):
    def __init__(self, *groups, file_name, x, y, colorkey=None):
        super().__init__()
        for group in groups:
            self.add(group)
        self.image = pygame.transform.scale(load_image(PASSABLE_TEXTURES_PATH, file_name, color_key=colorkey), (TILE, TILE))
        self.rect = self.image.get_rect(topleft=(x, y))


class SolidSprite(pygame.sprite.Sprite):
    def __init__(self, *groups, file_name, x, y, colorkey=-1, tiling_x=TILE, tiling_y=TILE):
        super().__init__()
        for group in groups:
            self.add(group)
        self.image = pygame.transform.scale(load_image(TEXTURES_PATH, file_name, color_key=colorkey), (tiling_x, tiling_y))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)


class PartlyPassableSprite(pygame.sprite.Sprite):
    def __init__(self, *groups, file_name, x, y, colorkey=-1, tiling_x=TILE, tiling_y=TILE):
        super().__init__()
        for group in groups:
            self.add(group)
        self.image = pygame.transform.scale(load_image(TEXTURES_PATH, file_name, color_key=colorkey), (tiling_x, tiling_y))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(pygame.transform.scale(load_image(
            TEXTURES_PATH, file_name, color_key=colorkey), (tiling_x, tiling_y - (TILE * 0.8))))
        # self.mask_rect = self.mask.get_rect()
        # self.mask_rect.width = tiling_x
        # self.mask_rect.height = tiling_y - TILE
        # self.s = self.mask.to_surface()
        # self.s.set_colorkey((255, 255, 255))


textures_anim_dict = {
    'wooden_floor': {
        1: collections.deque([load_image(PASSABLE_TEXTURES_PATH, 'wooden_floor.jpg')])
    },
    'wooden_crate': {
        1: collections.deque([load_image(SOLID_TEXTURES_PATH, 'solid_tile.png')])
    },
    'telly': {
        1: collections.deque(
            [load_image(SOLID_TEXTURES_PATH, f'telly/{i}.png') for i in range(TELLY_FRAMES_COUNT)]
        )
    }
}

player_anim_dict = {
    'down': {
        1: collections.deque(
            [load_image(PLAYER_PATH, f'down_frames/{i}.png') for i in range(1, 5)])
    },
    'up': {
        1: collections.deque(
            [load_image(PLAYER_PATH, f'up_frames/{i}.png') for i in range(1, 5)])
    },
    'right': {
        1: collections.deque(
            [load_image(PLAYER_PATH, f'right_frames/{i}.png') for i in range(1, 5)])
    },
    'left': {
        1: collections.deque(
            [load_image(PLAYER_PATH, f'left_frames/{i}.png') for i in range(1, 5)])
    },
    'standing': {
        1: collections.deque(
            [load_image(PLAYER_PATH, f'standing_frames/{i}.png') for i in range(1, 5)])
    }
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
