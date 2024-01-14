import collections

import pygame.sprite
from load_image import load_image
from config import *
from math import sin


class PassableSprite(pygame.sprite.Sprite):
    def __init__(self, *groups, file_name, x, y, anim_state=1):
        super().__init__(*groups)
        self.animation_state = anim_state
        self.animations = textures_anim_dict[file_name]
        self.image = textures_anim_dict[file_name][anim_state][0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hitbox = self.rect.copy()
        self.animation_count = 0
        self.name = file_name

    def update(self):
        self.image_update()

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
            self.hitbox = pygame.rect.Rect((x, y), (tiling_x, tiling_y - TILE * 0.8))


class Entity(pygame.sprite.Sprite):
    def __init__(self, groups, speed=PLAYER_ANIMATION_SPEED):
        super().__init__(*groups)
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


textures_anim_dict = {
    'floor': {
        1: collections.deque(
            [pygame.transform.scale(load_image(TEXTURES_PATH, 'map_tiles/floor.png'), (800, 400))]
        )
    },
    'floor_2': {
        1: collections.deque(
            [pygame.transform.scale(load_image(TEXTURES_PATH, 'map_tiles/floor_2.png'), (1540, 1160))]
        )
    },
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
    # 'inside_wall_2': {
    #     1: collections.deque(
    #         [pygame.transform.scale(load_image(TEXTURES_PATH, 'map_tiles/inside_wall_2.png'), (160, 120))])
    # },
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
                [pygame.transform.scale(load_image(TEXTURES_PATH, 'map_tiles/carpet.png'), (400, 250))]
            )
    }
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
