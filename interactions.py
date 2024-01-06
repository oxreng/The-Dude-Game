import pygame


class InteractionObject:
    def __init__(self, rect, name):
        self.rect = rect
        self.name = name


interaction_group = pygame.sprite.Group()


def player_interaction(player):
    for obj in collide_areas:
        if obj.rect.colliderect(player.rect):
            if obj.name in interaction_types['switch_animation']:
                for sprite in interaction_group:
                    if sprite.name == obj.name:
                        sprite.animation_state = -sprite.animation_state
            ...


collide_areas = [
    InteractionObject(pygame.Rect((320, -140,), (80, 140)), 'door'),
    InteractionObject(pygame.Rect((40, -60), (100, 100)), 'oven')
]

interaction_types = {
    'switch_animation': ['oven']
}
