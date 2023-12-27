import collections

import pygame.sprite
from load_image import load_image
from config import *


class PassableSprite(pygame.sprite.Sprite):
    def __init__(self, *group, file_name, x, y):
        super().__init__(*group)
        self.image = pygame.transform.scale(load_image(PASSABLE_TEXTURES_PATH, file_name, color_key=None), (TILE, TILE))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class SolidSprite(pygame.sprite.Sprite):
    def __init__(self, *group, file_name, x, y):
        super().__init__(*group)
        self.image = pygame.transform.scale(load_image(SOLID_TEXTURES_PATH, file_name), (TILE, TILE))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.mask = pygame.mask.from_surface(self.image)


textures_anim_dict = {
    'wooden_floor': {
        collections.deque([load_image(PASSABLE_TEXTURES_PATH, 'wooden_floor.jpg')])
    },
    'wooden_crate': {
        collections.deque([load_image(SOLID_TEXTURES_PATH, 'solid_tile.png')])
    },
    'telly': {
        collections.deque(
            [load_image(SOLID_TEXTURES_PATH, f'telly/{i}.png') for i in range(TELLY_FRAMES_COUNT)]
        )
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
